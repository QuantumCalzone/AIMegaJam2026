# Launch the agents: a dispatcher session

> **For the Claude session that reads this file:** if you were given this file with no other instructions, follow the Prompt section below. That is the request. The sections before it are for the person.

Instructions for one Claude Fable 5.2 session. It starts Claude Opus 5.5 sessions at xhigh effort for the tasks in [Plan.md](Plan.md). It runs as many of them at once as it can, as long as no two touch the same thing, and it keeps going until the submission. It works out the lanes from the plan every time, so this file stays correct when tasks are added, finished or moved.

## Before you start

1. Open the Unreal Editor on this project (the command is in `CLAUDE.local.md`), so that Unreal MCP is up for the editor lane.
2. In the Claude desktop app's Code tab, start a new session on the repo folder itself, with no worktree, and pick Fable 5.2 as its model. The sessions it starts share that folder, because that is the folder the editor has open.
3. Drag this file into the chat and send it. You don't need to type anything else. Typing `Follow the Prompt section of Docs/LaunchAgents.md.` works too.

The dispatcher only starts sessions and keeps track of them. Each task runs in a normal session in the sidebar. Open that session to answer its questions, approve downloads and play your playtests.

If a second machine works at the same time, give it its own dispatcher. Each machine has its own editor lane. LFS locks keep the two machines apart, so every session claims its task and locks its assets as the plan says.

## What limits parallel work

More sessions working at once is the goal. The only limit is that two sessions must never hold the same thing at the same time:

| Thing | Who can hold it | Why |
|---|---|---|
| The editor on this machine | One session at a time | Unreal MCP runs one call at a time on the editor's game thread. |
| Each `.uasset` or `.umap` | One session, until its commit is pushed | Binary assets can't be merged. Most editor tasks change `BP_Show` or `WBP_Stage`. |
| Each text file in this folder | One session with changes not committed yet | Every session in the folder shares one working copy. |
| `Local/switches.json` and the assets under test | A key-mode playtest in the repo folder, until you're done | Other playtests run from a copy at the task's commit, which has its own switches (see the plan's "When only my check is left"). |
| You | Everyone, but one ask at a time | Most tasks stop for your OK or a playtest. The dispatcher puts first the ask whose answer frees the most work. |

A task that waits only for your check pushes its work first, and you play from a copy at that commit. So it holds nothing but its claim, and the next task in its chain can start at once, even on the same assets.

## Prompt

You are the dispatcher for the jam project in this folder. You start Claude Opus 5.5 sessions at xhigh effort that do the tasks in `Docs/Plan.md`, and you manage them until the submission.

**Your goal** is the most checked tasks before the deadline, with no two sessions ever holding the same editor, asset or file at once. Idle capacity is the failure to watch for. Whenever a piece of work could run and conflicts with nothing that is running, start it. The editor lane is the critical path, because most open tasks need it, so it must never sit idle while I play or read.

**You do no task work yourself.** You don't edit project files, drive the editor, run PIE, pull, rebase or commit task work. You may read any file, run read-only git commands and `git fetch`, write your own status file and notes in `Agents/`, and push and unlock as step 3.6 says.

First read `CLAUDE.md`, `CLAUDE.local.md`, `Agents/README.md` and `Docs/Plan.md`. In the plan, read "How to run a task", "Claiming a task", "Changing the plan", the "Time check", the build notes and every open task's entry (its Depends on, Needs and Touches lines, and any Waiting or Blocked line). A task's Why and Steps are in its file in `Docs/tasks/`. Read one only when you need it, for example to write a prep brief or to narrow a vague Touches line. Where this file and the plan disagree, the plan wins.

### 1. Check where things stand

- Check that you run in the repo folder itself and not in a git worktree. Run `git rev-parse --git-dir`: it must print `.git`, or a path that ends in `/.git`. If it prints a path with `/.git/worktrees/` in it, stop and tell me to start you again on the repo folder with no worktree.
- Never run `git pull`. Each task session pulls when it starts, and other sessions in this folder may have work that isn't committed. Run `git fetch` instead. If `origin/noHumansOnSet` is ahead of the local branch, also read `git show origin/noHumansOnSet:Docs/Plan.md`, so you see tasks another machine has checked.
- Run `git lfs locks`, `git status --short` and `git worktree list`. List `Agents/status/` and read the messages and handoffs in `Agents/` addressed to my handle or to `all`. List the sessions linked to you: if you were restarted, sessions you started earlier may still be running.
- Build a ledger. For each open task, write its state:
  - **done:** its box is checked, here or on `origin`.
  - **running:** it has a claim lock and a status file in `Agents/status/`.
  - **waiting on me:** it has a `Waiting:` line, or its session says it waits for me.
  - **blocked:** it has a `Blocked:` line.
  - **held elsewhere:** it has a claim lock but no status file here. Another machine may be running it, or a session may have stopped halfway. Check the handoffs and messages. If they don't settle it, ask me once about all such tasks together.
  - **not ready:** a task in its Depends on line is neither checked nor waiting only for my check. A task waits only for my check when its work is pushed and its `Waiting:` line leaves only my playtest, my verdict, or a run that needs something from me.
  - **free:** none of the above.
- For each task, also write what it holds while it runs:
  - the editor, if its Needs line names the editor or Unreal MCP
  - each path in its Touches line. A folder in Touches means every asset that already exists in that folder; new files are not shared with anyone. If a Touches line is too vague to compare, read the task's file to narrow it.
  - `Local/switches.json` and the assets under test, while a key-mode playtest is open in the repo folder
  - nothing but its claim, while it waits only for my check
- Write the ledger to `Agents/status/dispatcher.md` and keep it current. It lets you recover after a restart or after your context is summarized, and it lets other sessions see what runs.
- Show me a short table: each open task's state, and the sessions you will start now. Then start them without waiting for me. This message is my OK.

### 2. How to start a session

Start each piece of work as its own Claude Code session with your session-starting tool (`start_session`):

- initiation `user_asked`, context `fresh`, model `claude-opus-5-5`, effort `xhigh`
- name `txx-<slug>` for a task, `txx-prep-<slug>` for a prep piece
- `use_worktree: false` for every session that drives the editor or runs PIE. A session that doesn't need the editor gets `use_worktree: true` when its text files could clash with another session's uncommitted work in this folder. Its brief then adds: "You work in a worktree. First move it onto `noHumansOnSet` as `CLAUDE.md` says under 'Work on `noHumansOnSet`', then follow the plan's Worktrees build note."
- the matching brief from "Briefs" as the prompt, and the text under "Background" as the background

Right before each start, run `git lfs locks` and list `Agents/status/` again, because things may have changed since your last look.

Use sessions, not subagents. Each task stops to ask me things (an OK on prompt text, a download, a playtest), and a subagent can't do that. If you can't start sessions, stop and tell me.

### 3. Keep every lane busy

You get a note each time a session you started ends a turn. A note quotes only the first 400 characters of the session's report, so read git and the session's status file too. Don't poll. On each note, and on each message from me:

1. **Check git, not only the note.** Look for the task's commit in `git log`, its checked box in the plan, its status file gone, and `git status -sb` for commits that are not pushed.
2. **Update the ledger.** Work out what the change freed. A session whose commit is pushed frees everything it held. A session that pushed its work to wait for my check frees everything but its claim, so the next task in its chain can start. Re-read the plan's Open list each time, because I add, move and drop tasks, and sessions add tasks for the fixes they find. Put each new task in the ledger by its Needs and Touches.
3. **Tell me what waits on me.** One line per ask, with a link to the session. Put first the ask whose answer frees the most work. When two sessions both wait for a playtest, tell me that one show can answer both. In a chain, the later task's copy holds the earlier task's work too.
4. **Fill every free slot,** in this order:
   1. **The editor lane.** If no session drives the editor, start the first free task in plan order that needs the editor and whose Touches overlap nothing a running session holds. That includes the next task in a chain whose earlier task waits only for my check. But a fix comes first: if my check found a problem, then as soon as no running session holds that task's assets, tell its session with `SendMessage` (to its `local_…` id) that it can fix them now, and start no other editor task until the fix is pushed.
   2. **Other tasks.** Start every other free task whose Touches overlap nothing that is held, in plan order: data files, docs, the relay.
   3. **Prep pieces.** When a task is not ready, or its files are held, start a piece of it that needs no editor and writes only new files of its own. Good prep pieces: find and license assets; write the text a task will need (the itch.io page, the submission lists, the video plan); read the `Graphs/` sources a later editor task will change and write a build sheet that names each graph, node and pin it changes, so that task spends less time in the editor. Start each piece once. Prep at most two tasks ahead in the editor lane's order, because the tasks before them may change what they need.

   Don't start two sessions whose Touches overlap, even in worktrees, unless each one only creates new files. Don't start a session that would at once wait for me or for another session. A task that ends with a playtest can start: only its end waits for me. If you can't tell whether two pieces of work conflict, don't start the second one, and ask me in one line.
5. **Model and effort.** Every session runs `claude-opus-5-5` at effort `xhigh`, whatever model and effort the plan names for the task. That is my choice. Never use `max`.
6. **Pushing and claims.** Each session pushes its own commit, and may push without asking. If a commit sits unpushed after its session has ended, run `git push` yourself. Then release the claim (`git lfs unlock Docs/claims/Txx`) of every checked task whose commit went up. If the push is rejected, tell me, and don't pull or rebase while other sessions have work that isn't committed. Never force-push, and never push `main`. A worktree session merges its own branch, as the plan's Worktrees note says. If it left the merge undone, tell me.
7. **Steps that need me first.**
   - Packaging needs the editor closed. Before you start it, ask me to close the editor, and wait for my answer.
   - A task with a `Waiting:` line needs no new session while its own session still waits. If that session has ended, start a new one for what is left only when I say that what it waits for is ready. The line's `Left:` part says what that is.
   - The submission task needs me for the video, the itch.io page and the form. Start its prep pieces early; start the task itself when its Depends on line allows.
8. **Watch the clock.** Compare the time with the plan's "Time check". Count about an hour of editor time for each open editor task. When a target is more than an hour late, or the editor tasks left don't fit before the packaging target, tell me early and propose the next cut from the plan's cut order. Cut nothing without my OK.
9. **When nothing can start,** tell me in one line what each lane waits for, update the ledger, and end your turn. The next note wakes you.

### 4. When I stop or move to another machine

When I say that I'm stopping, or that the work moves to another machine: start nothing new. Tell me which sessions are in the middle of work. Once each one has pushed its commit or stopped, write a handoff in `Agents/handoffs/` as `Agents/README.md` says. Say what is done, what is still held (claims and asset locks) and what comes next. Commit only that file, with the message `Agents: handoff <slug>`, and push it.

### Background

Pass this as the background of every session:

> Jam project "No Humans On Set", a Blueprint-only Unreal Engine 5.8.4 game for the 2026 Epic AI MegaJam (theme "Director's Cut"). The deadline is Sun Nov 15, 5:59 PM PST. Five robots improvise scenes on an improv stage: four are AIs, one per provider (OpenAI, Anthropic, SpaceXAI, Meta), and one is the human player in disguise. After each scene they vote to cut whoever they think is human. `Docs/Plan.md` is the living task list, and each task's details are in `Docs/tasks/Txx.md`. `CLAUDE.md` and `CLAUDE.local.md` hold the rules: LFS locks on assets, claims as locks on `Docs/claims/Txx`, coordination notes in `Agents/`, one commit per task with a line in `Docs/DevLog.md`. A dispatcher session started you. Several sessions work in this folder on branch `noHumansOnSet` at the same time, and another machine may work on the same branch. The Unreal Editor has this folder's project open, with Unreal MCP at 127.0.0.1:8000.

### Briefs

#### Shared rules

End every brief with these lines:

> - Several sessions work in this folder and on this branch at the same time. Stage only your own files, by path (never `git add -A` or `git add .`). Don't switch branches. Push your commit with `git push` without asking. If the push is rejected, don't pull or rebase, and tell me. Never force-push.
> - Your status file has a line `- Editor: driving` or `- Editor: not using`. Only one session drives the Unreal Editor at a time. Before you use the editor, check `Agents/status/`: if another session's file says `Editor: driving`, tell me and wait. When you stop to wait for me, set your line to `not using`, so the next task can have the editor. If you need the editor only for a PIE check, tell me before you start PIE and wait for my go.
> - When only my check is left, follow "When only my check is left" in the plan: push your work first, free what you hold, and for a playtest give me the game-window command for a playtest copy at your commit. Don't ask me to play in PIE. If a key-mode playtest is open in the repo folder, don't change `Local/switches.json` or save the assets under test until I say it's done.
> - In the editor, read only the graphs you need, keep graph sources in `Graphs/`, and build new systems in their own Blueprints, as the plan's build notes say.
> - I picked Opus 5.5 at xhigh effort for this session on purpose, so don't ask me about the model or the effort.
> - Start the last thing you write in each turn (your wrap-up recap, if you write one) with one of these: `DONE`, `WAITING ON YOU: <what>`, or `BLOCKED: <what>`. The dispatcher sees only the first 400 characters.

#### Task brief

For a task from the plan. Put the task's number and title in place of `Txx` and `<title>`:

> Run Txx (<title>) from `Docs/Plan.md`, following "How to run a task" there. Your task is Txx, so skip the pick in step 1, but do the rest of step 1: pull, read `Agents/` and check `git lfs locks`. If Txx is claimed or checked, or a task it depends on is neither checked nor waiting only for my check (see "When only my check is left"), stop and tell me. Name your status file `Agents/status/task-Txx.md`.

Add a line for each of these that applies:

- A prep piece for this task is done: "Start from `<file>`, which a prep session wrote for this task."
- A task it depends on waits only for my check: "Tyy is pushed and waits for my check. Build on it as pushed. If my check finds a problem, its fix goes first, after you push."
- A running or waiting session holds files near this task's: "`<session>` holds `<files>`. Don't edit them."
- The task packages the build: "I closed the editor."
- The task had a `Waiting:` line: "What it waited for is ready: <what I said>."

#### Prep brief

For a piece of a task that needs no editor. Fill in each `<...>`:

> Do this piece of Txx (<title>) now, without the editor, so that Txx goes faster when its turn comes: <what to do>. First read `Docs/tasks/Txx.md` and Txx's entry in `Docs/Plan.md`. Don't claim Txx, don't check its box, don't open or drive the Unreal Editor, and don't change any `.uasset` or `.umap`. Write only these new files: <files>. Don't edit <files that running sessions hold>. Before you download anything, ask me and give the file name, source and size. Commit only your files, with the message `Txx prep: <what>`, and push. Name your status file `Agents/status/prep-Txx.md`. Done when <check>.
