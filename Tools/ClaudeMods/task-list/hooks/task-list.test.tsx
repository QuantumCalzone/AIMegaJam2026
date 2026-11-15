import { expect, test } from 'claude-code/testing'

const PANE = {
  plugin: 'task-list',
  component: 'Pane',
  requestId: 'task-list',
  props: {
    title: 'Tasks',
    isFocused: false,
    bodyColumns: 60,
    placement: 'dock',
    scroll: { offset: 0, bodyRows: 40 },
    view: {},
  },
} as const

// The plan's form: open tasks in priority order, then the done ones. T27 was
// added last and placed above T19 and T22, so the numbers are not in order.
const PLAN = [
  '# Plan',
  '## How to run a task',
  '- [ ] **T98 Not a task: outside the Tasks section**',
  '## Tasks',
  '### Open',
  '- [ ] **T17 Stage art**',
  '  - **Waiting:** the work is done (see `Findings`). Left: I watch a show.',
  '- [ ] **T18 One LLM per AI player**',
  '  - **Depends on:** T16, T17',
  '- [ ] **T27 Added later, placed first**',
  '  - **Depends on:** T01',
  '- [ ] **T19 Robots act**',
  '  - **Depends on:** T17, T18',
  '- [ ] **T22 Package**',
  '  - **Depends on:** T19, and T24 if it is done',
  '- [ ] **T23 Submission**',
  '  - **Depends on:** T22',
  '### Done',
  '- [x] **T01 Spike one**',
  '  - **Depends on:** nothing',
  '## Findings',
  '- [ ] **T99 Not a task either**',
].join('\n')

const SESSIONS = [
  { sessionId: 'local_a', title: 'T18: One LLM per AI player', isRunning: true, link: 'claude://x/local_a' },
  { sessionId: 'local_b', title: 'Stage art', name: 't17-stage-art', isRunning: false },
  { sessionId: 'local_c', title: 'Unrelated chat', isRunning: true },
]

const ran = (stdout: string) => ({
  value: { exitCode: 0, stdout, stderr: '', isStdoutTruncated: false, isStderrTruncated: false },
})
const CLAIMS = 'Docs/claims/T18\tQuantumCalzone\tID:1\n'
// `git worktree list --porcelain`: the repo folder first, then each worktree.
const worktrees = (repo: string, ...others: string[]) =>
  [repo, ...others].map(path => `worktree ${path}\nHEAD 0123abc\nbranch refs/heads/x\n`).join('\n')
const file = (name: string) => ({ name, kind: 'file', size: 1, mtimeMs: 0, isLink: false }) as const
const slashes = (path: string) => path.replace(/\\/g, '/')

test('the pane sorts tasks and opens a session on a press, on every surface', async ($, on) => {
  const opened: unknown[] = []
  on('ui.open', () => ({ value: { isPlaced: true } }))
  on('ui.log', () => ({ value: undefined }))
  on('ui.toast', () => ({ value: undefined }))
  on('session.root', () => ({ value: '/repo' }))
  on('fs.read', (_, e) => {
    if (e.path.replace(/\\/g, '/').endsWith('/repo/Docs/Plan.md')) return { value: PLAN }
    // A status file. The older name, mvp-T23.md, still counts. A file with
    // any other name, such as notes-T19.md, is not a task's status file.
    return {
      value: e.path.endsWith('mvp-T23.md')
        ? '- State: an older status file'
        : '- State: planning done; waiting for a go',
    }
  })
  on('fs.list', () => ({
    value: [
      { name: 'task-T18.md', kind: 'file', size: 1, mtimeMs: 0, isLink: false },
      { name: 'mvp-T23.md', kind: 'file', size: 1, mtimeMs: 0, isLink: false },
      { name: 'notes-T19.md', kind: 'file', size: 1, mtimeMs: 0, isLink: false },
    ],
  }))
  on('process.run', (_, e) => ran(e.argv[1] === 'worktree' ? worktrees('/repo') : CLAIMS))
  on('mcp.call', (_, e) => {
    if (e.tool === 'list_sessions') {
      return { value: { content: [{ type: 'text', text: JSON.stringify(SESSIONS) }], isError: false } }
    }
    opened.push(e.args)
    return { value: { content: [{ type: 'text', text: 'Showing it.' }], isError: false } }
  })

  await $.command.run({
    command: 'task-list',
    args: '',
    origin: { kind: 'composer' },
    presentation: { isFullscreen: true, columns: 80 },
  })

  for (const surface of ['terminal', 'desktop', 'vscode', 'mobile'] as const) {
    const ui = await $.ui.mount({ ...PANE, surface })

    expect((await ui.find({ type: 'Text', text: /done · / }))?.text).toBe(
      '1 done · 3 in progress · 3 not started',
    )
    expect(await ui.find({ type: 'Text', text: /an older status file/ })).toBeDefined()
    // Not started keeps the plan's order, not the order of the numbers.
    const todo = await ui.findAll({ type: 'Text', text: /^○ T\d+/ })
    expect(todo.map(row => /T\d+/.exec(row.text ?? '')?.[0])).toEqual(['T27', 'T19', 'T22'])
    expect((await ui.find({ type: 'Text', text: /T27 Added later/ }))?.text).toContain('· ready')
    // Done is collapsed until its header is pressed, then crossed out.
    expect(await ui.find({ type: 'Text', text: /T01 Spike one/ })).toBeUndefined()
    await ui.press({ key: 'done-toggle' })
    const doneRow = await ui.find({ type: 'Text', text: /T01 Spike one/ })
    expect(doneRow?.props.strikethrough).toBe(true)
    await ui.press({ key: 'done-toggle' })

    expect((await ui.find({ type: 'Text', text: /I watch a show/ }))?.text).toBe('I watch a show.')
    expect(await ui.find({ type: 'Text', text: /planning done/ })).toBeDefined()
    expect((await ui.find({ type: 'Text', text: /after T19/ }))?.text).toContain('· after T19')
    expect((await ui.find({ type: 'Text', text: /after T19/ }))?.text).not.toContain('T24')
    expect(await ui.find({ type: 'Text', text: /T98|T99/ })).toBeUndefined()
    expect(await ui.find({ key: 'session:T17:local_b' })).toBeDefined()
    expect(await ui.find({ key: 'session:T18:local_c' })).toBeUndefined()

    await ui.press({ key: 'task:T18' })
    await ui.unmount()
  }

  expect(opened[0]).toEqual({ session_id: 'local_a', target: 'focus' })
})

// A session in a worktree cut from main: its folder has no Docs/Plan.md, and
// its own Agents/status is a copy nobody writes. The pane reads the repo
// folder's plan and status files, the first path `git worktree list` prints.
test('a session in a worktree reads the repo folder', async ($, on) => {
  const listed: string[] = []
  on('ui.open', () => ({ value: { isPlaced: true } }))
  on('ui.log', () => ({ value: undefined }))
  on('ui.toast', () => ({ value: undefined }))
  on('session.root', () => ({ value: 'C:\repo\.claude\worktrees\wt' }))
  on('fs.read', (_, e) => {
    const path = slashes(e.path)
    if (path === 'C:/repo/Docs/Plan.md') return { value: PLAN }
    if (path === 'C:/repo/Agents/status/task-T18.md') return { value: '- State: from the repo folder' }
    return { deny: `ENOENT: ${path}` }
  })
  on('fs.list', (_, e) => {
    const path = slashes(e.path)
    listed.push(path)
    if (path === 'C:/repo/Agents/status') return { value: [file('task-T18.md')] }
    // The worktree's own copy: never read.
    return { value: [file('task-T23.md')] }
  })
  on('process.run', (_, e) =>
    ran(e.argv[1] === 'worktree' ? worktrees('C:/repo', 'C:/repo/.claude/worktrees/wt') : CLAIMS),
  )
  on('mcp.call', () => ({
    value: { content: [{ type: 'text', text: JSON.stringify(SESSIONS) }], isError: false },
  }))

  await $.command.run({
    command: 'task-list',
    args: '',
    origin: { kind: 'composer' },
    presentation: { isFullscreen: true, columns: 80 },
  })

  const ui = await $.ui.mount({ ...PANE, surface: 'desktop' })
  expect(await ui.find({ type: 'Text', text: /^No Docs/ })).toBeUndefined()
  expect((await ui.find({ type: 'Text', text: /done · / }))?.text).toBe(
    '1 done · 2 in progress · 4 not started',
  )
  expect(await ui.find({ type: 'Text', text: /from the repo folder/ })).toBeDefined()
  expect(listed).toEqual(['C:/repo/Agents/status'])
  await ui.unmount()
})

test('with no plan in either folder, the error names both', async ($, on) => {
  on('ui.open', () => ({ value: { isPlaced: true } }))
  on('ui.log', () => ({ value: undefined }))
  on('session.root', () => ({ value: '/elsewhere/wt' }))
  on('fs.read', (_, e) => ({ deny: `ENOENT: ${e.path}` }))
  on('fs.list', () => ({ value: [] }))
  on('process.run', (_, e) =>
    ran(e.argv[1] === 'worktree' ? worktrees('/elsewhere', '/elsewhere/wt') : ''),
  )
  on('mcp.call', () => ({ value: { content: [{ type: 'text', text: '[]' }], isError: false } }))

  await $.command.run({
    command: 'task-list',
    args: '',
    origin: { kind: 'composer' },
    presentation: { isFullscreen: true, columns: 80 },
  })

  const ui = await $.ui.mount({ ...PANE, surface: 'desktop' })
  expect((await ui.find({ type: 'Text', text: /^No Docs/ }))?.text).toBe(
    'No Docs/Plan.md in /elsewhere/wt or in the repo folder /elsewhere.',
  )
  await ui.unmount()
})
