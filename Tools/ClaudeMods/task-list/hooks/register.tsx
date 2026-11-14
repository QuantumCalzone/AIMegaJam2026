import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register } from 'claude-code'

import type { SessionRef, Snapshot, Task, TaskFlag } from '../types'

// The task list of Docs/Plan.md in a pane beside the chat:
// done tasks collapsed and crossed out, in-progress tasks with the Code
// sessions that work on them (a click opens one), and the tasks not started.
// Tasks keep the plan's order, which is the priority order: a new task can
// sit anywhere in the plan, whatever its number.

type Engine = EngineInterface

const PANE = 'task-list'
const TITLE = 'Tasks'
const PLAN = 'Docs/Plan.md'
const STATUS_DIR = 'Agents/status'
const TICK_MS = 20_000
// `git lfs locks` asks GitHub, so claims refresh every 6 ticks (2 minutes).
const CLAIM_EVERY = 6

const EMPTY: Snapshot = { tasks: [], updatedAt: 0 }
const snapshot = atom({ plugin: 'task-list', key: 'snapshot' } as const, EMPTY, {
  shape: 'snapshot-1',
})
const isDoneOpen = atom({ plugin: 'task-list', key: 'isDoneOpen' } as const, false)

// Module state: lost on a reload, and rebuilt by the refresh at session.start.
let claims = new Map<string, string>()
let tick = 0
let isBusy = false

type PlanTask = {
  id: string
  title: string
  section: string
  isDone: boolean
  deps: string[]
  waiting?: string
  blocked?: string
}

const clean = (text: string) =>
  text
    .replace(/\*\*/g, '')
    .replace(/`/g, '')
    .replace(/\[([^\]]+)\]\([^)]*\)/g, '$1')
    .trim()

function parsePlan(text: string): PlanTask[] {
  const tasks: PlanTask[] = []
  let isInTasks = false
  let section = ''
  let current: PlanTask | undefined
  for (const line of text.split(/\r?\n/)) {
    if (/^## /.test(line)) {
      isInTasks = /^## Tasks\b/.test(line)
      current = undefined
      continue
    }
    if (!isInTasks) continue
    const heading = /^### (.+)/.exec(line)
    if (heading) {
      section = (heading[1] ?? '').trim()
      current = undefined
      continue
    }
    const task = /^- \[([ xX])\] \*\*(T\d+)\s+(.+?)\*\*/.exec(line)
    if (task) {
      current = {
        id: task[2] ?? '',
        title: clean(task[3] ?? ''),
        section,
        isDone: task[1] !== ' ',
        deps: [],
      }
      tasks.push(current)
      continue
    }
    if (!current) continue
    const deps = /^\s+- \*\*Depends on:\*\*(.*)/.exec(line)
    if (deps) {
      const required = (deps[1] ?? '').replace(/T\d+ if it is done/g, '')
      current.deps = [...required.matchAll(/\bT\d+\b/g)].map(m => m[0])
    }
    const waiting = /^\s+- \*\*Waiting:\*\*\s*(.*)/.exec(line)
    if (waiting) {
      const left = /\bLeft:\s*(.*)/.exec(waiting[1] ?? '')
      current.waiting = clean((left ? left[1] : waiting[1]) ?? '')
    }
    const blocked = /^\s+- (?:\*\*)?Blocked:(?:\*\*)?\s*(.*)/.exec(line)
    if (blocked) current.blocked = clean(blocked[1] ?? '')
  }
  return tasks
}

// Agents/status/task-T18.md: a session works on T18. Its "Waiting on" or
// "State" line is the note shown under the task. Status files from before
// the plan was renamed are called mvp-T18.md, and count too.
async function readStatus($: Engine, root: string) {
  const notes = new Map<string, string>()
  const entries = await $.fs.list(`${root}/${STATUS_DIR}`).catch(() => [])
  for (const entry of entries) {
    const match = /^(?:task|mvp)-(T\d+)\.md$/.exec(entry.name)
    if (!match) continue
    const text = await $.fs.read(`${root}/${STATUS_DIR}/${entry.name}`).catch(() => '')
    const line =
      /^- Waiting on:\s*(.*)$/m.exec(text)?.[1] ?? /^- State:\s*(.*)$/m.exec(text)?.[1] ?? ''
    if (match[1]) notes.set(match[1], clean(line))
  }
  return notes
}

async function readClaims($: Engine, root: string) {
  try {
    const ran = await $.process.run(['git', 'lfs', 'locks'], {
      cwd: root,
      timeoutMs: 45_000,
      env: { GIT_TERMINAL_PROMPT: '0' },
    })
    if (ran.exitCode !== 0) return undefined
    const found = new Map<string, string>()
    for (const m of ran.stdout.matchAll(/^Docs\/claims\/(T\d+)\s+(\S+)/gm)) if (m[1] && m[2]) found.set(m[1], m[2])
    return found
  } catch {
    return undefined
  }
}

const textOf = (result: { content: { text?: string }[] }) =>
  result.content.map(block => block.text ?? '').join('\n')

type SessionRow = {
  sessionId: string
  title?: string
  name?: string
  isRunning?: boolean
  link?: string
  lastActivityAt?: string
}

// The desktop app's other sessions, each filed under every task its title
// (`T18: ...`) or its dispatcher name (`t18-...`) names.
async function readSessions($: Engine) {
  const byTask = new Map<string, SessionRef[]>()
  const result = await $.mcp.call('ccd_session_mgmt', 'list_sessions', { limit: 100 })
  const text = textOf(result)
  if (result.isError) throw new Error(text || 'list_sessions failed')
  const rows = JSON.parse(text) as SessionRow[]
  for (const row of rows) {
    const ids = new Set<string>()
    for (const m of (row.title ?? '').matchAll(/\bT(\d+)\b/g)) ids.add(`T${m[1]}`)
    const named = /^t(\d+)(?:-|$)/i.exec(row.name ?? '')
    if (named) ids.add(`T${named[1]}`)
    const ref: SessionRef = {
      id: row.sessionId,
      title: row.title ?? row.name ?? row.sessionId,
      isRunning: row.isRunning === true,
      link: row.link,
      lastActivityAt: row.lastActivityAt,
    }
    for (const id of ids) byTask.set(id, [...(byTask.get(id) ?? []), ref])
  }
  for (const list of byTask.values()) {
    list.sort(
      (a, b) =>
        Number(b.isRunning) - Number(a.isRunning) ||
        (b.lastActivityAt ?? '').localeCompare(a.lastActivityAt ?? ''),
    )
  }
  return byTask
}

async function refresh($: Engine, options: { withClaims?: boolean } = {}) {
  if (isBusy) return
  isBusy = true
  try {
    const root = await $.session.root()
    if (options.withClaims) {
      const found = await readClaims($, root)
      if (found) claims = found
    }
    let planText: string
    try {
      planText = await $.fs.read(`${root}/${PLAN}`)
    } catch {
      const error = `No ${PLAN} in ${root}.`
      await update($, snapshot, old => ({ ...old, error, updatedAt: Date.now() }))
      return
    }
    const plan = parsePlan(planText)
    const notes = await readStatus($, root)
    let sessions = new Map<string, SessionRef[]>()
    let sessionsError: string | undefined
    try {
      sessions = await readSessions($)
    } catch (err) {
      sessionsError = err instanceof Error ? err.message : String(err)
    }
    const doneIds = new Set(plan.filter(t => t.isDone).map(t => t.id))
    const tasks: Task[] = plan.map(t => {
      const own = sessions.get(t.id) ?? []
      const claimedBy = claims.get(t.id)
      const status = notes.get(t.id)
      const isRunning = own.some(s => s.isRunning)
      const isActive =
        t.blocked !== undefined ||
        t.waiting !== undefined ||
        status !== undefined ||
        claimedBy !== undefined ||
        isRunning
      const flag: TaskFlag =
        t.blocked !== undefined
          ? 'blocked'
          : t.waiting !== undefined
            ? 'waiting'
            : isRunning
              ? 'running'
              : claimedBy !== undefined
                ? 'claimed'
                : 'idle'
      return {
        id: t.id,
        title: t.title,
        section: t.section,
        state: t.isDone ? 'done' : isActive ? 'progress' : 'todo',
        flag: t.isDone || !isActive ? undefined : flag,
        note: t.blocked || t.waiting || status || undefined,
        waitsOn: t.deps.filter(d => !doneIds.has(d)),
        claimedBy,
        sessions: own,
      }
    })
    await update($, snapshot, () => ({ tasks, updatedAt: Date.now(), sessionsError }))
  } finally {
    isBusy = false
  }
}

const REFUSED = /refus|not started|ask the user|only (this|sessions)|cannot|can't|unknown|not found/i

// Shows the session in this window's main pane. The app lets a session focus
// only the sessions it started, so for any other the session's own app link
// is handed to the OS, which brings it up in the app.
async function openSession($: Engine, session: SessionRef) {
  let why = ''
  try {
    const result = await $.mcp.call('ccd_window', 'open_session_in', {
      session_id: session.id,
      target: 'focus',
    })
    const text = textOf(result)
    $.ui.log(`open_session_in ${session.id}: ${result.isError ? 'error' : 'ok'}: ${text}`, {
      to: 'debug',
    })
    if (!result.isError && !REFUSED.test(text)) return
    why = text
  } catch (err) {
    why = err instanceof Error ? err.message : String(err)
  }
  if (session.link) {
    const root = await $.session.root()
    const isWindows = /^[A-Za-z]:[\\/]/.test(root) || root.includes('\\')
    const argv = isWindows ? ['cmd', '/c', 'start', '', session.link] : ['open', session.link]
    try {
      const ran = await $.process.run(argv, { timeoutMs: 15_000 })
      if (ran.exitCode === 0) return
      why = ran.stderr.trim() || `exit code ${ran.exitCode}`
    } catch (err) {
      why = err instanceof Error ? err.message : String(err)
    }
  }
  $.ui.toast(`Couldn't open "${session.title}" (${why}). Open it from the sidebar.`)
}

const FLAG_LABEL: Record<TaskFlag, string> = {
  blocked: 'blocked',
  waiting: 'waits on you',
  running: 'running',
  claimed: 'claimed',
  idle: 'no session running',
}
const FLAG_COLOR: Record<TaskFlag, string> = {
  blocked: 'error',
  waiting: 'warning',
  running: 'success',
  claimed: 'suggestion',
  idle: 'inactive',
}

const clock = (ms: number) => {
  const d = new Date(ms)
  const pad = (n: number) => String(n).padStart(2, '0')
  return `${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({
      name: 'task-list',
      description: "Show the plan's task list in a pane",
    })
    void $.ui.open({ id: PANE, title: TITLE })
    void refresh($, { withClaims: true })
    $.clock.every(TICK_MS, () => {
      tick += 1
      void refresh($, { withClaims: tick % CLAIM_EVERY === 0 })
    })

    return next(e)
  })

  on('command.run', { command: 'task-list' }, async $ => {
    await $.ui.open({ id: PANE, title: TITLE })
    await refresh($, { withClaims: true })

    return { text: 'Task list pane opened.' }
  })

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const { Box, Text, Button } = $.ui.resolve(e)
    const snap = await read($, snapshot)
    const isOpen = await read($, isDoneOpen)
    const done = snap.tasks.filter(t => t.state === 'done')
    const active = snap.tasks.filter(t => t.state === 'progress')
    const todo = snap.tasks.filter(t => t.state === 'todo')

    const heading = (text: string) => (
      <Text size="caption" weight="semibold" dimColor>
        {text}
      </Text>
    )

    return (
      <Box flexDirection="column" gap={1}>
        <Box flexDirection="row" justifyContent="space-between" alignItems="center">
          <Text dimColor>
            {snap.updatedAt === 0
              ? 'Reading the plan...'
              : `${done.length} done · ${active.length} in progress · ${todo.length} not started`}
          </Text>
          <Button
            key="refresh"
            plain
            dimColor
            label="Refresh"
            onPress={() => void refresh($, { withClaims: true })}
          />
        </Box>
        {snap.error !== undefined && <Text color="error">{snap.error}</Text>}

        <Box flexDirection="column">
          <Button
            key="done-toggle"
            plain
            onPress={() => void update($, isDoneOpen, open => !open)}
          >
            <Text weight="semibold">
              {isOpen ? '▾' : '▸'} Done ({done.length})
            </Text>
          </Button>
          {isOpen &&
            done.map(t => (
              <Box key={`done:${t.id}`} paddingLeft={2}>
                <Text dimColor strikethrough wrap="truncate-end">
                  {t.id} {t.title}
                </Text>
              </Box>
            ))}
        </Box>

        <Box flexDirection="column" gap={1}>
          {heading(`IN PROGRESS (${active.length})`)}
          {active.length === 0 && <Text dimColor>Nothing in progress.</Text>}
          {snap.sessionsError !== undefined && (
            <Text color="warning" wrap="truncate-end">
              Sessions unavailable: {snap.sessionsError}
            </Text>
          )}
          {active.map(t => {
            const flag = t.flag ?? 'idle'
            const first = t.sessions[0]
            return (
              <Box key={`active:${t.id}`} flexDirection="column">
                <Button
                  key={`task:${t.id}`}
                  plain
                  onPress={() => {
                    if (first) void openSession($, first)
                    else $.ui.toast(`No session found for ${t.id}.`)
                  }}
                >
                  <Text color={FLAG_COLOR[flag]}>●</Text> <Text weight="semibold">{t.id}</Text>{' '}
                  {t.title} <Text color={FLAG_COLOR[flag]}>· {FLAG_LABEL[flag]}</Text>
                </Button>
                {t.note !== undefined && (
                  <Box paddingLeft={2}>
                    <Text dimColor wrap="truncate-end">
                      {t.note}
                    </Text>
                  </Box>
                )}
                {t.sessions.length === 0 && (
                  <Box paddingLeft={2}>
                    <Text dimColor italic>
                      No session found{t.claimedBy ? ` · claimed by ${t.claimedBy}` : ''}
                    </Text>
                  </Box>
                )}
                {t.sessions.map(s => (
                  <Box key={`row:${t.id}:${s.id}`} paddingLeft={2}>
                    <Button
                      key={`session:${t.id}:${s.id}`}
                      plain
                      dimColor
                      onPress={() => void openSession($, s)}
                    >
                      ↳ {s.title} <Text color={s.isRunning ? 'success' : 'inactive'}>
                        · {s.isRunning ? 'running' : 'idle'}
                      </Text>
                    </Button>
                  </Box>
                ))}
              </Box>
            )
          })}
        </Box>

        <Box flexDirection="column">
          {heading(`NOT STARTED (${todo.length})`)}
          {todo.length === 0 && <Text dimColor>Nothing left.</Text>}
          {todo.map(t => (
            <Box key={`todo:${t.id}`}>
              <Text wrap="truncate-end">
                ○ <Text weight="semibold">{t.id}</Text> {t.title}{' '}
                <Text dimColor>
                  {t.waitsOn.length > 0 ? `· after ${t.waitsOn.join(', ')}` : '· ready'}
                </Text>
              </Text>
            </Box>
          ))}
        </Box>

        {snap.updatedAt > 0 && (
          <Text size="footnote" dimColor>
            Updated {clock(snap.updatedAt)} from {PLAN}, Agents/status, claims and sessions.
          </Text>
        )}
      </Box>
    )
  })
}
