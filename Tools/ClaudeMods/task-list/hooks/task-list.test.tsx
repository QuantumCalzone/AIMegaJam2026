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

const PLAN = [
  '# Plan',
  '## How to run a task',
  '- [ ] **T98 Not a task: outside the Tasks section**',
  '## Tasks',
  '### Spikes',
  '- [x] **T01 Spike one**',
  '  - **Depends on:** nothing',
  '- [ ] **T17 Stage art**',
  '  - **Waiting:** the work is done (see `Findings`). Left: I watch a show.',
  '- [ ] **T18 One LLM per AI player**',
  '  - **Depends on:** T16, T17',
  '- [ ] **T19 Robots act**',
  '  - **Depends on:** T17, T18',
  '- [ ] **T22 Package**',
  '  - **Depends on:** T19, and T24 if it is done',
  '## Findings',
  '- [ ] **T99 Not a task either**',
].join('\n')

const SESSIONS = [
  { sessionId: 'local_a', title: 'T18: One LLM per AI player', isRunning: true, link: 'claude://x/local_a' },
  { sessionId: 'local_b', title: 'Stage art', name: 't17-stage-art', isRunning: false },
  { sessionId: 'local_c', title: 'Unrelated chat', isRunning: true },
]

test('the pane sorts tasks and opens a session on a press, on every surface', async ($, on) => {
  const opened: unknown[] = []
  on('ui.open', () => ({ value: { isPlaced: true } }))
  on('ui.log', () => ({ value: undefined }))
  on('ui.toast', () => ({ value: undefined }))
  on('session.root', () => ({ value: '/repo' }))
  on('fs.read', (_, e) => ({
    value: e.path.endsWith('MVPPlan.md') ? PLAN : '- State: planning done; waiting for a go',
  }))
  on('fs.list', () => ({
    value: [{ name: 'mvp-T18.md', kind: 'file', size: 1, mtimeMs: 0, isLink: false }],
  }))
  on('process.run', () => ({
    value: {
      exitCode: 0,
      stdout: 'Docs/claims/T18\tQuantumCalzone\tID:1\n',
      stderr: '',
      isStdoutTruncated: false,
      isStderrTruncated: false,
    },
  }))
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
      '1 done · 2 in progress · 2 not started',
    )
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
