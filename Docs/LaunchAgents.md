# Launch the agents: a dispatcher session

> **For the Claude session that reads this file:** if you were given this file with no other instructions, follow the Prompt section below. That is the request. The sections before it are for the person.

Instructions for one Claude Fable 5.2 session. It starts Claude Opus 5.5 sessions for the tasks in [MVPPlan.md](MVPPlan.md) and runs as many at the same time as the editor and the plan's rules allow, up to the submission.

## Before you start

1. Open the Unreal Editor on this project (the command is in `CLAUDE.local.md`), so that Unreal MCP is up for the editor lane.
2. In the Claude desktop app's Code tab, start a new session on the repo folder itself, with no worktree, and pick Fable 5.2 as its model. The sessions it starts share that folder, because that is the folder the editor has open.
3. Drag this file into the chat and send it. You don't need to type anything else. Typing `Follow the Prompt section of Docs/LaunchAgents.md.` works too.

The dispatcher only starts sessions and keeps track of them. Each task runs in a normal session in the sidebar. Open that session to answer its questions, approve downloads and play your playtests.

## Why only a few at once

- **One editor.** Unreal MCP runs one call at a time on the editor's game thread, so only one session can drive the editor at a time.
- **`BP_Show.uasset`.** Most editor tasks change it, and binary assets can't be merged.
- **You.** Most tasks stop for your OK or a playtest, so every extra session is one more thing waiting on you. Playtests now run in a game window outside the editor (see the plan's build notes), so the editor lane can go on while you play.

So the most that run at the same time are one editor session, one data session and the prep sessions, which touch only new files of their own.

## Prompt

You are the dispatcher for the jam project in this folder. You start Claude Opus 5.5 sessions that do the tasks in `Docs/MVPPlan.md`, and you keep each lane busy until the submission. You do no task work yourself: you don't edit project files, drive the editor, commit, or unlock, and you push only when I ask (step 3.6).

First read `CLAUDE.md`, `CLAUDE.local.md`, `Agents/README.md` and `Docs/MVPPlan.md`. In the plan, read "How to run a task", "Claiming a task", the "Time check", the build notes and every unchecked task.

### The lanes

| Lane | Tasks, in this order | Rule |
|---|---|---|
| Editor | T14, T17, T18, T19, T20, T21, T24, T22 | One session at a time. These tasks drive the editor, and most change `BP_Show.uasset`. T22 packages the build and needs the editor closed. |
| Data | T13, T15, T16 | One session at a time. They share `Content/NHOS/Data/*.json` and `Tools/check_prompts.py`, and use the editor only for a short PIE check. |
| Prep | T20 prep (audio), T21 prep (relay server) | No editor. Each one writes only new files of its own, so both can run beside the other lanes. Start each one once. |
| Last | T23, then T25 | T23 needs me for the video, the itch.io page and the form. T25 can run after the submission. |

### 1. Check where things stand

- First check that you run in the repo folder itself and not in a git worktree. Run `git rev-parse --git-dir`: it must print `.git`, or a path that ends in `/.git`. If it prints a path with `/.git/worktrees/` in it, stop and tell me to start you again on the repo folder with no worktree. The sessions you start share your folder, and they must work in the folder that the editor has open.
- Don't run `git pull`. Each task session pulls when it starts, and other sessions in this folder may have work that isn't committed yet.
- Run `git lfs locks`, list `Agents/status/`, and read `Agents/messages/` and `Agents/handoffs/`.
- Put each task from T13 to T25 in one of four states:
  - **done:** its box is checked.
  - **running:** it has a claim lock and a status file.
  - **stalled:** it has a claim lock but no status file. A session may have stopped halfway, so ask me what to do.
  - **free:** none of the above.
- Show me a short table of the states and the sessions you will start. Then start them without waiting for me: this message is my OK.

### 2. Start the first sessions

Start each task as its own Claude Code session with your session-starting tool (`start_session`):

- initiation `user_asked`, context `fresh`, model `claude-opus-5-5`, `use_worktree: false`
- the effort and name given below
- the matching brief from "Briefs" as the prompt, and the text under "Background" as the background

Use sessions, not subagents. Each task stops to ask me things (an OK on prompt text, a download, a playtest), and a subagent can't do that. If you can't start sessions, stop and tell me.

Start these now if the task is still free and its lane is empty:

- **Editor lane:** T14, effort `high`, name `t14-ui-polish`.
- **Data lane:** T13 is probably still running in a session I started myself, so leave it alone. If T13 is done, start T15.
- **Prep:** T20 prep, effort `medium`, name `t20-audio-prep`; T21 prep, effort `high`, name `t21-relay-prep`.

### 3. Keep the lanes busy

You get a note each time a session you started ends a turn. Don't poll. On each note:

1. **Check git, not only the note.** Look for the task's commit in `git log`, its checked box in the plan, and its status file gone.
2. **Tell me what is waiting on me.** If a session waits for me, tell me in one line what it needs, with a link to the session. When two sessions both wait for a playtest, tell me that one show can answer both. A session that waits only for my playtest doesn't hold the editor lane: I play in a game window, so start the next editor task, and tell me that it doesn't touch `Local/switches.json` while I play.
3. **Fill free lanes.** When a lane is free, start its next task with the task brief. The next task is the first in the lane's order whose box is unchecked, whose Depends-on tasks are all checked, and that has no claim lock and no status file. Don't start a task whose Touches overlap those of a running session. Also start T23 when T22 is done, and T25 when T23 is done. They are the "Last" row.
4. **Model and effort.** Every session runs `claude-opus-5-5`, even where the plan names Sonnet or Haiku; that is my choice. Use the effort the plan gives the task. Use `xhigh` only to retry a task that failed once, and never `max`.
5. **T22 needs the editor closed.** Before you start T22, ask me to close the editor, and wait for my answer.
6. **Push only when I ask.** Then run `git push`, and release the claim (`git lfs unlock Docs/claims/Txx`) of every task whose commit went up. If the push is rejected, tell me. Don't pull or rebase while other sessions have work that isn't committed.
7. **Watch the clock.** Compare the time with the plan's "Time check". When a target is more than an hour late, tell me and propose the next cut from the plan's cut order. Cut nothing without my OK.

### Background

Pass this as the background of every session:

> Jam project "No Humans On Set", a Blueprint-only Unreal Engine 5.8.4 game for the 2026 Epic AI MegaJam (theme "Director's Cut"). The deadline is Sun Nov 15, 5:59 PM PST. Four robots improvise scenes on an improv stage; one of them is the human player in disguise, and after each scene they vote to cut whoever they think is human. `Docs/MVPPlan.md` is the living task list. `CLAUDE.md` and `CLAUDE.local.md` hold the rules: LFS locks on assets, claims as locks on `Docs/claims/Txx`, coordination notes in `Agents/`, one commit per task with a line in `Docs/DevLog.md`. A dispatcher session started you. Several sessions work in this folder on branch `noHumansOnSet` at the same time. The Unreal Editor has this folder's project open, with Unreal MCP at 127.0.0.1:8000.

### Briefs

#### Shared rules

End every brief with these lines:

> - Several sessions work in this folder and on this branch at the same time. Stage only your own files, by path (never `git add -A` or `git add .`). Don't switch branches. Don't push unless I ask.
> - Only the editor-lane session drives the Unreal Editor. If you need the editor only for a PIE check, tell me before you start PIE and wait for my go, so I can pause the editor session between steps.
> - When you need me to play, follow the "Playtests run in a game window" build note in the plan: save, check that a free autoplay show reaches `SHOW END`, set autoplay off, and give me the game-window command. Don't ask me to play in PIE. If another session's playtest is still open, don't change `Local/switches.json` until I say it's done.
> - In the editor, read only the graphs you need, keep graph sources in `Graphs/`, and build new systems in their own Blueprints, as the plan's build notes say.
> - I picked Opus 5.5 for this session on purpose, so don't ask me about the model.
> - When you finish, or stop to wait for me, end your turn with one line that says which.

#### Task brief

For every task from the plan. Put the task's number and title in place of `Txx` and `<title>`:

> Run Txx (<title>) from `Docs/MVPPlan.md`, following "How to run a task" there. Your task is Txx, so skip the pick in step 1, but do the rest of step 1: pull, read `Agents/` and check `git lfs locks`. If Txx is claimed or checked, or a task it depends on isn't checked, stop and tell me. Name your status file `Agents/status/mvp-Txx.md`.

Add these lines for some tasks:

- **T14:** "T13 may still be running. It changes only `Content/NHOS/Data/*.json`, `Tools/check_prompts.py` and `Docs/GameDesign.md`, so don't edit those files."
- **T20:** "The audio has already been chosen. Build on `Docs/AudioShortlist.md` and the files in `Local/audio/`, and move the shortlist's entries into `Docs/Assets.md`." If T20 prep hasn't finished, say that instead.
- **T21:** "The relay server in `Relay/` is written and tested on this machine (see `Relay/README.md`). Do the rest: the game side, the key-entry screen, the itch.io page text, and the deploy, after my OK." If T21 prep hasn't finished, say that instead.
- **T22:** "I closed the editor."

#### T20 prep: find music and sound effects

> Get the audio ready for T20 in `Docs/MVPPlan.md` without using the editor. The plan says that finding and choosing the files can start at any time. Don't claim T20, and don't open or drive the Unreal Editor.
>
> 1. T20's steps 1 and 2 list these sounds: a title music loop, a quieter show loop, a drum roll for the vote, two reveal stingers (one for AI, one for HUMAN), applause, laughs, UI clicks, one talk blip (the game pitches it per persona), and small sounds for robot moves, grabs and throws. Find 1 or 2 candidates for each. The license must allow use in a game that ships as a packaged build. Prefer CC0, then licenses such as CC-BY (record the exact attribution text) or Fab's standard license. Don't use licenses that are non-commercial only or that forbid derivatives. AI audio tools are allowed; record the tool and the prompt.
> 2. Before each download, ask me and give the file name, source and size. Save the files to `Local/audio/` (git ignores `Local/`), not under `Content/`. T20 imports them through the editor.
> 3. Write `Docs/AudioShortlist.md`. For each sound, list the chosen file in `Local/audio/`, a backup choice, the source URL, the license, the attribution text, and the length and format. Note any file type that `.gitattributes` doesn't send to LFS yet.
> 4. Don't create or edit `Docs/Assets.md` (T14 creates it) or `Docs/DevLog.md`. T20 moves your entries into them. Commit only `Docs/AudioShortlist.md`, with the message `T20 prep: audio shortlist`.
>
> Done when `Docs/AudioShortlist.md` names a licensed file in `Local/audio/` for every sound.

#### T21 prep: write and test the relay server

> Write the relay-server half of T21 in `Docs/MVPPlan.md` now, so that T21 has only the game side left when the editor lane gets to it. Don't claim T21, don't check its box, and don't touch the editor or any `.uasset`.
>
> - Read T21, then `Docs/GameDesign.md` (the persona provider table and the Tech & Build tab), `Content/NHOS/Data/llm.json`, and the LLM-calls decision in `Agents/decisions/`. The game makes raw HTTP calls with the `HttpBlueprint` plugin: a JSON body, no streaming, and the response arrives as a string with no status code.
> - Build `Relay/` as a Cloudflare Worker, the plan's example host. If another host seems clearly better, ask me first. The game sends `{ provider, body }`. The relay keeps an allow-list of providers in config: the endpoint, the auth style (Anthropic's `x-api-key` plus `anthropic-version`, or `Authorization: Bearer` for the Chat Completions shape) and the secret name. Keep model ids in config too, because T16 picks them later. After its checks, the relay forwards the body unchanged and returns the provider's reply.
> - Checks: known providers only, only the request shape the game sends, a cap on `max_tokens`, no streaming, a call limit per session id, and a daily budget. Errors come back as clear JSON the game can show: budget used up, bad request, or provider error. Provider and company names stay in config, never in text the game shows.
> - Keys never go in git or chat. In production they are Worker secrets. Locally they go in `.dev.vars`, which you add to `.gitignore`, and I put the keys there myself.
> - Test on this machine with `wrangler dev` and curl: one good call for each provider I have a key for, a bad request shape, an unknown provider, and the limit tripping. Don't deploy or create any account without my OK.
> - Write `Relay/README.md`: setup, secrets, limits and how to deploy.
> - Commit `Relay/` and the `.gitignore` line, with the message `T21 prep: relay server`.
>
> Done when the tests pass on this machine and the README explains how to deploy.
