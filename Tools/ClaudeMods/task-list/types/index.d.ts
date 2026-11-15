export type TaskState = 'done' | 'progress' | 'todo'

/** Why an in-progress task is in progress, the strongest reason first. */
export type TaskFlag = 'blocked' | 'waiting' | 'running' | 'claimed' | 'idle'

/** The system of the machine that has a task in progress: 🪟 or 🍎 in the pane. */
export type Machine = 'windows' | 'mac'

/** A Code session whose title or name names the task (`T18: ...`, `t18-...`). */
export type SessionRef = {
  id: string
  title: string
  isRunning: boolean
  link?: string
  lastActivityAt?: string
}

export type Task = {
  id: string
  title: string
  section: string
  state: TaskState
  flag?: TaskFlag
  /** The machine that has the task, when the pane can tell. */
  machine?: Machine
  /** One line from the plan's Waiting/Blocked line or the task's status file. */
  note?: string
  /** Unfinished tasks this one depends on. */
  waitsOn: string[]
  claimedBy?: string
  sessions: SessionRef[]
}

export type Snapshot = {
  tasks: Task[]
  updatedAt: number
  error?: string
  sessionsError?: string
}

declare module 'claude-code' {
  interface PluginState {
    'task-list': {
      snapshot: Shaped<Snapshot>
      isDoneOpen: boolean
    }
  }
}
