import { expect, test } from 'claude-code/testing'
import type { TestBody } from 'claude-code/testing'

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
// A row of Not started: ○ can start, ◌ waits on tasks in progress, └ nested.
const TODO_ROW = /^[○◌└] T\d+/

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
    // Not started keeps the plan's order, not the order of the numbers. T19
    // waits only on tasks in progress, so it stays at the top level, and T22
    // sits under T19, the task it waits on (T24 counts only if it is done).
    const todo = await ui.findAll({ type: 'Text', text: TODO_ROW })
    expect(todo.map(row => row.text)).toEqual([
      '○ T27 Added later, placed first · ready',
      '◌ T19 Robots act · after T17, T18',
      '└ T22 Package',
    ])
    expect((await ui.find({ key: 'todo:T22' }))?.props.paddingLeft).toBe(2)
    // Done is collapsed until its header is pressed, then crossed out.
    expect(await ui.find({ type: 'Text', text: /T01 Spike one/ })).toBeUndefined()
    await ui.press({ key: 'done-toggle' })
    const doneRow = await ui.find({ type: 'Text', text: /T01 Spike one/ })
    expect(doneRow?.props.strikethrough).toBe(true)
    await ui.press({ key: 'done-toggle' })

    expect((await ui.find({ type: 'Text', text: /I watch a show/ }))?.text).toBe('I watch a show.')
    expect(await ui.find({ type: 'Text', text: /planning done/ })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: /T98|T99/ })).toBeUndefined()
    expect(await ui.find({ key: 'session:T17:local_b' })).toBeDefined()
    expect(await ui.find({ key: 'session:T18:local_c' })).toBeUndefined()

    await ui.press({ key: 'task:T18' })
    await ui.unmount()
  }

  expect(opened[0]).toEqual({ session_id: 'local_a', target: 'focus' })
})

// The plan's Depends on lines as a tree: each task under the task it waits on
// that comes last in the plan, the others named on its row.
const TREE_PLAN = [
  '# Plan',
  '## Tasks',
  '### Open',
  '- [ ] **T52 A tie cuts nobody**',
  '  - **Depends on:** T53 (the spare scene)',
  '- [ ] **T54 New win condition**',
  '  - **Depends on:** T53, T52',
  '- [ ] **T55 Remove the Director AI**',
  '  - **Depends on:** T52',
  '- [ ] **T57 A pass shows**',
  '  - **Depends on:** T55',
  '- [ ] **T38 Speech bubbles**',
  '  - **Depends on:** T30',
  // T38 is named twice, and T57 comes before T38 in the plan: T34 sits
  // under T38 and names T57.
  '- [ ] **T34 Fix the in-show screen**',
  '  - **Depends on:** T38 (the bubbles). If T38 is cut, take it off this line. Also T57.',
  // T60 waits on T54 and T55; T55 comes later in the plan.
  '- [ ] **T60 End screens**',
  '  - **Depends on:** T54, T55',
  '- [ ] **T36 Logos on bills**',
  '  - **Depends on:** T34',
  // A loop: neither task may vanish from the list.
  '- [ ] **T70 Loop one**',
  '  - **Depends on:** T71',
  '- [ ] **T71 Loop two**',
  '  - **Depends on:** T70',
  '- [ ] **T24 Timers**',
  '  - **Depends on:** T30',
  '### Done',
  '- [x] **T53 Scene clock**',
  '- [x] **T30 Line queue**',
].join('\n')

test('not started nests each task under the task it waits on', async ($, on) => {
  on('ui.open', () => ({ value: { isPlaced: true } }))
  on('ui.log', () => ({ value: undefined }))
  on('session.root', () => ({ value: '/repo' }))
  on('fs.read', (_, e) =>
    slashes(e.path).endsWith('/repo/Docs/Plan.md') ? { value: TREE_PLAN } : { deny: `ENOENT: ${e.path}` },
  )
  on('fs.list', () => ({ value: [] }))
  on('process.run', (_, e) => ran(e.argv[1] === 'worktree' ? worktrees('/repo') : ''))
  on('mcp.call', () => ({ value: { content: [{ type: 'text', text: '[]' }], isError: false } }))

  await $.command.run({
    command: 'task-list',
    args: '',
    origin: { kind: 'composer' },
    presentation: { isFullscreen: true, columns: 80 },
  })

  const ui = await $.ui.mount({ ...PANE, surface: 'desktop' })
  const todo = await ui.findAll({ type: 'Text', text: TODO_ROW })
  expect(todo.map(row => row.text)).toEqual([
    '○ T52 A tie cuts nobody · ready',
    '└ T54 New win condition',
    '└ T55 Remove the Director AI',
    '└ T57 A pass shows',
    '└ T60 End screens · also after T54',
    '○ T38 Speech bubbles · ready',
    '└ T34 Fix the in-show screen · also after T57',
    '└ T36 Logos on bills',
    '○ T24 Timers · ready',
    '◌ T70 Loop one · after T71',
    '└ T71 Loop two',
  ])
  const indent = async (id: string) => (await ui.find({ key: `todo:${id}` }))?.props.paddingLeft
  expect(await indent('T52')).toBe(0)
  expect(await indent('T55')).toBe(2)
  expect(await indent('T57')).toBe(4)
  expect(await indent('T60')).toBe(4)
  expect(await indent('T36')).toBe(4)
  expect(await indent('T71')).toBe(2)
  await ui.unmount()
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

// Two machines: this one has the tasks with a status file or a running
// session here; a claim of yours with nothing here is your other machine's;
// a teammate's claim names no machine.
const MACHINE_PLAN = [
  '# Plan',
  '## Tasks',
  '### Open',
  '- [ ] **T52 A tie cuts nobody**',
  '- [ ] **T37 Error messages**',
  '- [ ] **T40 A teammate takes it**',
  '- [ ] **T41 Runs here with no status file**',
  '- [ ] **T42 Waits on me**',
  '  - **Waiting:** the work is pushed. Left: my check.',
  '- [ ] **T43 Not started**',
].join('\n')

const lock = (path: string, owner: string) => ({ id: path, path, owner: { name: owner }, locked_at: '' })
const VERIFIED = JSON.stringify({
  ours: [
    lock('Docs/claims/T52', 'QuantumCalzone'),
    lock('Content/NHOS/Core/BP_Show.uasset', 'QuantumCalzone'),
    lock('Docs/claims/T37', 'QuantumCalzone'),
  ],
  theirs: [lock('Docs/claims/T40', 'Robotresistance')],
})

const mountMachines = async (
  $: Parameters<TestBody>[0],
  on: Parameters<TestBody>[1],
  root: string,
  locks: (argv: readonly string[]) => ReturnType<typeof ran>,
) => {
  on('ui.open', () => ({ value: { isPlaced: true } }))
  on('ui.log', () => ({ value: undefined }))
  on('session.root', () => ({ value: root }))
  on('fs.read', (_, e) => {
    const path = slashes(e.path)
    if (path.endsWith('/Docs/Plan.md')) return { value: MACHINE_PLAN }
    if (path.endsWith('/Agents/status/task-T52.md')) return { value: '- State: building' }
    return { deny: `ENOENT: ${path}` }
  })
  on('fs.list', () => ({ value: [file('task-T52.md')] }))
  on('process.run', (_, e) => (e.argv[1] === 'worktree' ? ran(worktrees(root)) : locks(e.argv)))
  on('mcp.call', () => ({
    value: {
      content: [
        {
          type: 'text',
          text: JSON.stringify([{ sessionId: 'local_r', title: 'T41: Runs here', isRunning: true }]),
        },
      ],
      isError: false,
    },
  }))
  await $.command.run({
    command: 'task-list',
    args: '',
    origin: { kind: 'composer' },
    presentation: { isFullscreen: true, columns: 80 },
  })
  return $.ui.mount({ ...PANE, surface: 'desktop' })
}

test('each task in progress shows the machine that has it', async ($, on) => {
  const ui = await mountMachines($, on, 'C:/repo', argv =>
    argv.includes('--verify') ? ran(VERIFIED) : ran(''),
  )
  const row = async (id: string) => (await ui.find({ key: `task:${id}` }))?.text ?? ''
  expect((await ui.find({ type: 'Text', text: /done · / }))?.text).toBe(
    '0 done · 5 in progress · 1 not started',
  )
  // This PC: T52's status file is here, and a session here runs T41.
  expect(await row('T52')).toContain('🪟 T52')
  expect(await row('T41')).toContain('🪟 T41')
  // The Mac: the claim is ours and nothing here works on it.
  expect(await row('T37')).toContain('🍎 T37')
  // A teammate's claim, and a task that only waits on me: no machine.
  expect(await row('T40')).toMatch(/^● T40/)
  expect(await row('T42')).toMatch(/^● T42/)
  expect(await ui.find({ type: 'Text', text: /claimed by Robotresistance/ })).toBeDefined()
  await ui.unmount()
})

test('without --verify every claim counts as yours, seen from a Mac', async ($, on) => {
  const asked: string[] = []
  const failed = { value: { exitCode: 1, stdout: '', stderr: 'no push access', isStdoutTruncated: false, isStderrTruncated: false } }
  const ui = await mountMachines($, on, '/Users/me/repo', argv => {
    asked.push(argv.join(' '))
    return argv.includes('--verify') ? failed : ran('Docs/claims/T37\tQuantumCalzone\tID:2\n')
  })
  const row = async (id: string) => (await ui.find({ key: `task:${id}` }))?.text ?? ''
  expect(asked).toEqual(['git lfs locks --verify --json', 'git lfs locks'])
  expect(await row('T52')).toContain('🍎 T52')
  expect(await row('T37')).toContain('🪟 T37')
  await ui.unmount()
})
