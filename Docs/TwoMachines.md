# Two machines at once: dispatchers and scheduled runs

How to work on the jam from two machines at the same time, for example the Mac and the Windows PC. We first did this on 2026-11-15. Either machine can take either role, so the same steps work from both.

[LaunchAgents.md](LaunchAgents.md) holds the dispatcher's own instructions. This file says how the two machines fit together, what we learned, and the text to paste.

## The parts

| Part | What it does | Where it lives |
|---|---|---|
| The split | Says which machine may take which task, so that the machines don't race for an asset. | This file, and each dispatcher's ledger. |
| A dispatcher session, one per machine | Keeps the ledger, talks to the other machine's dispatcher, tells you what waits on you. It starts task sessions only when you type to it. | A Claude session on the repo folder. Its ledger is `Agents/status/dispatcher.md`, which git ignores. |
| A scheduled task, one per machine | Every hour, starts a fresh session that takes the next free task for this machine and runs it, or exits. This is what keeps the work going while nobody is at the keyboard. | The Claude desktop app's scheduled tasks: `~/.claude/scheduled-tasks/next-task/SKILL.md` on each machine. It is not in git. |
| Claims and locks | The only thing both machines see at once. A claim is an LFS lock on `Docs/claims/Txx`. | GitHub, through `git lfs locks`. |

## The split

Most editor tasks change `BP_Show.uasset` or `WBP_Stage.uasset`, and only one session on either machine can hold those. So:

- **The chain machine** keeps the in-show editor chain: it takes only tasks whose Touches line names `BP_Show.uasset` or `WBP_Stage.uasset`.
- **The other machine** takes the rest, in the plan's order: editor tasks on other assets, and tasks that need no editor (data files, docs, generated art, the relay).

Pick the chain machine once: the one that holds an asset of the chain now, or else the one with the faster editor. On 2026-11-15 the PC was the chain machine and the Mac was the other machine.

**Tasks that fall between.** A task that names neither `BP_Show` nor `WBP_Stage`, but shares another asset with the chain (`BP_Robot`, `WBP_MoneyBurn`, `BPC_LLMClient`, `BPC_LinePlayer`, `WBP_ChatLine`), belongs to the other machine, but the scheduled runs skip it. On 2026-11-15 these were T36 and T46. Start such a task by hand when the chain doesn't hold its assets, or move it to the chain machine.

## Set it up

Do this on each machine:

1. `git pull` on `noHumansOnSet`, then open the Unreal Editor on the project, so that Unreal MCP is up.
2. In the Claude desktop app's Code tab, start a session on the repo folder itself, with no worktree, on Fable 5.2. Turn on Remote Control in it, so that the two dispatchers can see and message each other. Paste the dispatcher message below.
3. Make the scheduled task. The easy way is to tell any session on that machine: "Make an hourly scheduled task named `next-task` from `Docs/TwoMachines.md`, for the chain machine" (or "for the other machine"). To do it by hand, make a scheduled task in the app, set it to run every hour in the repo folder, and paste the prompt below with the right split block.
4. Set the scheduled task's model to Opus 5.5 at xhigh effort and its permission mode to auto. A session that stops at a permission prompt holds its claim until you come back.
5. Before you leave: keep the machine plugged in and awake with the lid open, and leave the Claude app and the editor open.
6. Write down your answer for every open task that needs one before it can work (its Needs line says "my answer" or "my OK"), in the task's file. A scheduled run skips a task that still waits for an answer.

To stop: turn the scheduled task off in the app on each machine, and tell each dispatcher that you are stopping ([LaunchAgents.md](LaunchAgents.md), step 4).

## What we learned

- **A dispatcher can't start a session by itself.** The app allows a start only on a message that you type in the desktop app. It refuses a start on a turn that a session's note, the other dispatcher's message or a scheduled prompt woke, and while you work over Remote Control. On those turns the dispatcher can only post a card for you to click, or tell you.
- **A scheduled task can.** Each run is a new session with a fresh context, which runs one task itself. So the scheduled runs do the starting, and no session's context grows over many tasks.
- **Scheduled runs send the dispatcher no notes.** The dispatcher sees them only through `Agents/status/`, `git lfs locks` and `origin`. The runs read the dispatcher's ledger for the split, so the ledger names a machine for every open task.
- **Rejected pushes are normal,** because both machines push to one branch. A session may run `git pull --rebase` and push again when `git status` shows no uncommitted work from another session. Never `--autostash`, never a force-push.
- **`Docs/Plan.md` and `Docs/DevLog.md` conflict often.** Every task commit changes the "Next up" line and adds a dev log line. When both machines finish close together, the second one's rebase stops there, and that session waits for you. The fix is to keep both sides' lines. Whether a session may do that by itself is not decided yet; until it is, the prompt below tells it to stop.
- **The usage limit stops every session at once,** on both machines. A stopped session keeps its claim and its status file. After the limit resets, message the session to go on, or archive it and release its claim so that a scheduled run can take the task again.
- **Each scheduled run costs usage,** also when it finds nothing free and exits.
- **A paid step needs a cap.** Each art task names its Meshy credits. Give the running session the balance it should find, and tell it to stop if the balance is lower.

## Text to paste

### The dispatcher message

Fill in the two machine names and pick one of the two last sentences:

```text
Be this machine's dispatcher. Follow the Prompt section of Docs/LaunchAgents.md, and read Docs/TwoMachines.md first.

This machine is <the Mac | the PC>. A second dispatcher runs at the same time on <the other machine>, with its own editor and its own sessions. Both machines use the same branch and the same GitHub account. A scheduled task named next-task runs every hour on each machine and takes this machine's next free task, so check the claims before every start, and keep a machine for every open task in your ledger, because the scheduled runs read it.

<This machine is the chain machine: it keeps the BP_Show / WBP_Stage chain. | This machine is the other machine: it takes editor tasks on other assets, tasks that need no editor, and prep pieces the chain machine hasn't started.>
```

### The scheduled task

Paste this as the task's prompt. Put the machine's name in place of `<MACHINE>`, and put one of the two split blocks in place of `<SPLIT BLOCK>`.

```text
You are one task session for the jam project "No Humans On Set", in the project folder this session runs in (the folder that holds AIMegaJam2026.uproject), on <MACHINE>. A schedule started you, and nobody is at the keyboard. Start the next task that waits for no unfinished task, that conflicts with no task in progress, and that is this machine's to take. Run that one task yourself. If there is none, exit early and change nothing.

"I" and "my" below mean the person who owns this project.

## Read first

1. `CLAUDE.md`, then "How to run a task", "Claiming a task", "When only my check is left" and the build notes in `Docs/Plan.md`.
2. `Agents/status/dispatcher.md`, if it exists. It is this machine's dispatcher's ledger. If it names a machine for each task, follow it. Read the other files in `Agents/status/` too.
3. Run `git status`, `git fetch` and `git lfs locks`. Pull only if `noHumansOnSet` is behind `origin/noHumansOnSet`, and never with `--autostash`. If the pull would overwrite another session's uncommitted changes, exit.

## Which task you may take

A second machine works on the same branch with the same GitHub account. Locks belong to the account, so a lock that no status file in this folder explains is the other machine's. Leave it alone. The two machines split the work so they don't race:

<SPLIT BLOCK>

Go down "Open" in `Docs/Plan.md` and take the first task that passes every one of these:

- It is this machine's by the split above.
- It isn't T70. Only I start T70, by name.
- Its box is unchecked, it has no `Waiting:` or `Blocked:` line, and its claim file has no lock. Never take a claimed task, even if its session looks stopped.
- Each task in its Depends on line is checked, or is pushed and waits only for my check.
- Its Needs are met without me. Skip a task that needs my answer or my OK before it can do its work (a download, a design question), unless its task file or the plan already holds my answer. A task that only ends with my look or verdict is fine.
- Nothing it touches is held: no path in its Touches line is locked, named in another session's status file, or shown as another session's uncommitted change in `git status`.
- If it needs the editor: Unreal MCP is connected in your session, and no status file says `Editor: driving`.

If no task passes, say so in one line and exit. Don't start a prep piece, don't change the plan, and don't touch `Agents/status/dispatcher.md` (it has one writer).

## Run the task

Follow "How to run a task" from step 2. Skip its question about the model and effort: I chose them. Claim the task before anything else; if the claim fails, another session got there first, so go on to the next task that passes. Name your status file `Agents/status/task-Txx.md`, with a line `- Editor: driving` or `- Editor: not using`.

- Stage only your own files, by path (never `git add -A` or `git add .`). Don't switch branches. Push your commit with `git push` without asking. Never force-push, and never push `main`.
- If the push is rejected: you may run `git pull --rebase` and push again when `git status` shows no uncommitted work from another session. Never use `--autostash`. If another session has uncommitted changes, the rebase stops on a conflict, or it would change an asset the editor has open, stop and write what happened in your status file.
- Never ask me to playtest. Where your check needs a show played, play it yourself, as the build note "Claude does the playing" says, and test in Test for Free.
- Never deploy the relay, and never spend paid credits or tokens past the cap the task names, without my OK. If a balance is lower than the task's file says it should be, stop. If the task can't finish without my OK, push the rest, add a `Waiting:` line that says what is left, and stop.
- Before any long wait (a mesh batch, a cook), write in your status file how to resume without paying or building twice. A usage limit may stop you without warning.
- When only my check is left, follow "When only my check is left": push first, free what you hold, keep the claim, and leave the status file to say what you wait for.
- When the task is done and leaves me nothing to decide, archive yourself as the very last step (`archive_session` with `session_id: "self"`). First check that your commits are pushed, your claim and your asset locks are released and your status file is gone. Never archive yourself while you wait for me or are blocked.
```

Split block for **the chain machine**:

```text
- **This machine keeps the in-show editor chain.** Take only a task whose Touches line names `BP_Show.uasset` or `WBP_Stage.uasset`, unless the ledger marks it for the other machine.
- **The other machine takes the rest:** editor tasks on other assets, and tasks that need no editor (data files, docs, generated art). Never take one of those, even if it is free.
```

Split block for **the other machine**:

```text
- **The other machine keeps the in-show editor chain.** Never take a task whose Touches line names `BP_Show.uasset`, `WBP_Stage.uasset`, `BPC_LinePlayer`, `BP_Robot`, `WBP_ChatLine`, `WBP_MoneyBurn` or `BPC_LLMClient`, or a task that the ledger marks for the other machine.
- **This machine takes the rest,** in the plan's order: editor tasks that share no asset with that chain, and tasks that need no editor (data files, docs, generated art).
```

The asset names in the second block are the ones the chain held on 2026-11-15. When the chain's tasks change, take the names from the Touches lines of the chain's open tasks.
