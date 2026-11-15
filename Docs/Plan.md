# Plan: No Humans On Set

The living plan for our jam game: the tasks in priority order, how to run one and how to add one. The design is a private Claude Doc, linked from [GameDesign.md](GameDesign.md). Say **"Next task"** to build the next step.

In this file, "I" and "my" mean the person at the keyboard. "Claude" means the agent doing the task.

**Next up:** T21 (how a judge plays) is done: with a wrong relay address, keys entered on the AI service unavailable screen passed the key test and played a show in key mode, with answers from all four labs. Its claim is released. T35 (the money burn) is done too. The first free task is T28 (Opus 5.5 · xhigh): Scene Prep shows the whole card, the scene shows only mine. T29 follows T28, then the UI/UX sweep starts with T32 (the audit, the style guide and the shared pieces). T30 (the lines play one at a time), then T38 (every line in a speech bubble, and the chat opens on a click), T33 (the title, key entry and end screens) and T34 (the in-show screen) come after T32. T20 (audio) is free too, but every one of these tasks changes `BP_Show` or `WBP_Stage`, so they go one at a time in the editor.

## Goal

Finish **No Humans On Set** and submit it to the 2026 Epic AI MegaJam before the deadline (see "Time check"). The "Open" tasks below are what we know is still to do. I add tasks as the game needs them, and a new task goes wherever it belongs in that list (see "Changing the plan").

**How the plan began.** It started as the plan for an MVP (T01 to T12), which had to answer one question as fast as possible: is it fun to fool an all-AI cast, and do the AIs catch a human at a fair rate (not every time, not never)? The gate (T12, 2026-11-14) said go. I liked it. Since then the plan covers the whole game. Until 2026-11-14 this file was `Docs/MVPPlan.md`. Finished tasks' files, the dev log and older notes in `Agents/` still use that name. Until 2026-11-14 this file also held every task's full text and a Findings section; since then each task has its own file in `Docs/tasks/` (see "Tasks").

## Time check

First written Fri Nov 13, 2026, about 3:20 PM PST. Rewritten at the gate (T12), Fri Nov 13, about 10 PM PST. The deadline is Sun Nov 15, 5:59 PM PST (Nov 16, 01:59 UTC). That leaves about 44 hours, sleep included. T01 to T12 finished ahead of the first schedule.

| Target | When (PST) |
|---|---|
| Plain speech (T13), UI/UX polish (T14) and story scenes (T15) | Sat Nov 14, by noon |
| One LLM per AI player (T16, T18) and the stage art (T17) | Sat Nov 14, by 6 PM |
| Robots act out their actions (T19), the UI fixes from my playtest (T27 to T31), speech bubbles (T38), the money burn (T35), the UI/UX sweep (T32 to T34), audio (T20), relay and key entry (T21) | Sun Nov 15, by 10 AM |
| Packaged and played (by me, by hand; T22 was dropped), submission ready (T23) | Sun Nov 15, by 2 PM |
| Submit | Sun Nov 15, by 3 PM. Keep 3 hours of margin. |

12 tasks at up to an hour each is about 12 hours of agent time, plus your time on checks and playtests. Two lanes can run at once: tasks that need no editor (T13, T15, T16, and finding audio files for T20) beside the editor tasks (T14, T17, T18 to T21), which go one at a time. If we fall behind, cut in this order: T24 (timers), then T31 (Tab completion), then T19 to Move and Look only, then T20 to music and three sounds, then T17's robot motion.

## How to run a task

When I say **"Next task"** or **"Next ask"**:

1. `git pull` (if the branch is not on the remote yet, say so and go on). Read `Agents/`. Open this file and run `git lfs locks`. Take the first task in "Open" that is free (see "Claiming a task") and whose **Depends on** tasks are all checked, or wait only for my check (see "When only my check is left"). Then read the task's file, `Docs/tasks/Txx.md` (its **Details** link): it holds the Why, the Steps, the Done-when check and what earlier work found. Read another task's file only when yours points to it.
2. Tell me the task and its recommended model and effort. If this session runs a different model, say so and ask whether to go on.
3. Check its Needs. If something is missing (for example, Unreal MCP is not connected), tell me what to do and stop.
4. Claim the task (see "Claiming a task"). Write a status file, `Agents/status/task-T07.md`, and lock assets as `Agents/README.md` says.
5. Do the work, then run the Done-when check. If the check fails, do not mark the task done: write what blocks it under the task's entry in this file (a `Blocked:` line, never only in the task's file) and tell me. If the only part of the check left is mine (a playtest, my verdict, or a run that needs something from me), follow "When only my check is left" instead of step 6.
6. Make one commit that holds the work; the task's entry in this file with its box checked, moved to the end of "Done" and cut down to its title line and its **Details** line; the task's file with the lines cut from the entry (**Model and effort**, **Depends on**, **Needs**, **Touches**) moved to the top of its "## Task" section, the line under its title changed to say the task is done, a **Result:** line at the end of "## Task", and what the task found under "## Findings" at the end of the file; the updated "Next up" line; and one line in [DevLog.md](DevLog.md) (the jam's Glass Box category needs a dev log). Message: `T07: <title>`. Then push it with `git push`. You don't need to ask. If the push is rejected, don't pull or rebase while other sessions have uncommitted work in this folder; tell me.
7. Delete the status file. Once the commit that checks the box is pushed, release the claim. Unlock the assets the task changed too, unless another running session still has uncommitted changes in them (`git status`, `Agents/status/`). End by naming the next task with its model and effort, so I can switch before I send "Next task".

## Claiming a task

A claim is an LFS lock on the task's claim file. Everyone sees it at once, on every machine, with no push.

- **Claim:** `git lfs lock Docs/claims/T07`
- **See all claims:** `git lfs locks`
- **Release:** `git lfs unlock Docs/claims/T07`, after the commit that checks the task's box is pushed. Until the push, other machines see neither the work nor the checked box, so the lock is what tells them the task is taken. A task that waits for my playtest or verdict keeps its claim until its box is checked. Whoever pushes releases the claims of every checked task that went up.
- A task is free when its box is unchecked here, it has no `Waiting:` line, and `git lfs locks` shows no lock on its claim file.
- If the lock fails because a teammate holds it, take the next free task.
- If my own account holds the lock on an unchecked task and there is no status file for it in `Agents/status/`, an earlier session may have stopped halfway. Ask me before taking it.
- If you stop without finishing, add a `Blocked:` line under the task and commit it as `Plan: T07 blocked`. Release the claim only if someone else should take the task.

Never edit the claim files. They exist only to be locked.

## When only my check is left

Most tasks end with my playtest, my verdict, or a run that needs something from me. The next task doesn't wait for it:

1. **Push the work first.** When the work is built and the Done-when check passes except for the part only I can do, commit and push now. The commit holds the work, its `Graphs/` files, the task's file with what it found so far, a `Waiting:` line under the task's entry in this file (it ends `Left: <what I must do>`), the "Next up" line and one line in [DevLog.md](DevLog.md). Message: `Txx: <title> (waits for <what>)`. The box stays unchecked.
2. **Free what you hold.** Unlock the assets the task changed, keep the claim, and set the `Editor:` line in your status file to `not using`. Keep the status file: it says what you wait for.
3. **Playtest from a copy.** If I must play, make a playtest copy at your commit, and give me the game-window command for the copy's `.uproject`, not the repo folder's:
   - `git worktree add --detach "<repo folder>-playtest/Txx" <your commit>`
   - The copy holds the committed work and nothing else, so the next task can change the same assets in the repo folder while I play. Never change anything in the copy.
   - It has no `Local/` folder, so every switch is off. If the playtest needs a switch, write `Local/switches.json` in the copy. Never copy the key file there, so key mode doesn't work in a copy. A key-mode playtest runs in the repo folder, as before, and no session saves the assets under test until I say I'm done.
   - The game's log is in the copy's `Saved/Logs/`. The first launch from a new copy may take a few minutes while it builds its caches.
4. **The next task can start.** A task may start when each task in its **Depends on** line is checked, or has its work pushed with a `Waiting:` line that leaves only my check. It builds on that work as pushed.
5. **If my check passes,** make the closing commit as step 6 of "How to run a task" says: check the box, remove the `Waiting:` line, move the entry to "Done", and add the Result and the findings. It needs a DevLog line only if the check changed something. Message: `Txx: <title> (checked)`. Push it, release the claim, delete the status file, and remove the copy with `git worktree remove "<repo folder>-playtest/Txx"`.
6. **If my check finds a problem,** the fix goes first in the editor lane, but only once no running session holds the task's assets (`git lfs locks`, `Agents/status/`). Until then, tell me, and wait. When they are free, lock them again, fix the problem, push with the `Waiting:` line kept, and give me a new copy at the new commit. That copy also holds the work of any task that started after yours, so one show checks both. Tell me what the fix changed, so that later tasks that built on your work can check it.

## Changing the plan

I add tasks as the game needs them, and a task can go anywhere in the list. Every change to the plan outside a task's own commit is a commit too, `Plan: <what changed>`, with a line in [DevLog.md](DevLog.md). One example is a playtest that changes the design.

To add a task:

1. **Number it.** Take the highest number in `Docs/claims/` plus one. A number is only a name: it says nothing about order. Never renumber a task, and never reuse a number.
2. **Place it.** "Open" is in priority order, and "Next task" takes from the top. Two things decide where the task goes:
   - **Architecture:** it goes below every task it builds on, and above the tasks that build on it. Name the first kind in its **Depends on** line, and add it to the **Depends on** line of each task of the second kind.
   - **Priority:** among tasks that don't depend on each other, the one that matters more for the submission goes higher.
3. **Write it** like the other open tasks, in two places. In this file, under "Open": the title line, then **Model and effort**, **Depends on**, **Needs**, **Touches** and **Details** (a link to its file). In a new file, `Docs/tasks/Txx.md`: a `# Txx Title` heading, the line back to the plan, then "## Task" with **Why** (if there is one), **Steps** and **Done when**. A task is about an hour of agent work at most, so split a bigger one.
4. **Add its claim file,** `Docs/claims/Txx`, with the same two lines as the other claim files and the new number.
5. **Commit** the plan, the task's file, the claim file and the dev log line together as `Plan: add Txx <title>`. Update "Next up" if the new task changes what is next.

To move a task, cut its entry in this file and paste it at its new place. Its number and its file stay. To drop a task, delete its entry and its file, and say why in the commit message. Its claim file stays, so that the number is never used again. To change a task's steps, edit its file; to change its **Depends on**, **Needs** or **Touches**, edit its entry here.

**Keep the form.** Every task is an entry here plus a file, `Docs/tasks/Txx.md`. An open task's entry holds its title line and the short lines that other readers need (**Model and effort**, **Depends on**, **Needs**, **Touches**, any **Waiting:** or **Blocked:** line, and **Details**); its file holds the rest. A done task's entry holds only its checked title line and its **Details** line; its file holds everything else, its findings included. Findings that belong to no one task are in `Docs/tasks/Background.md`. The task-list pane (`Tools/ClaudeMods/task-list`) reads only this file, never the task files, and lists the tasks in this file's order. It finds a task only under `## Tasks`, as a line that starts `- [ ] **Txx Title**`, or `- [x]` when the task is done. It reads the boxes, not the "Open" and "Done" headings. Under a task, it reads these indented lines:

- `- **Depends on:**` and the task numbers in it. A task that waits for an unfinished one shows as "after Txx".
- `- **Waiting:**` on a task whose work is committed but still needs me. End the line with `Left: <what I must do>`, because that is the part the pane shows.
- `- **Blocked:**` with what blocks the task.

## Model and effort rubric

- **Opus 5.5, high:** the spike, architecture, AI prompt design, Blueprint systems with many parts, debugging.
- **Sonnet 5.5, medium:** well-specified Blueprint or UMG work that follows a pattern already in the project.
- **Haiku 5.5, low:** docs, config and small mechanical edits.
- **Since 2026-11-14, every task runs on Opus 5.5 at xhigh**, whatever its own "Model and effort" line says. That is my choice. Never use **max**.
- Start a session for any work that conflicts with no running session, rather than leave it waiting (see `Docs/LaunchAgents.md`, step 3).

## Build notes for every task

These hold for every task, and for editor work outside the task list too. If one changes, change it here in a `Plan:` commit.

- **Blueprint-only.** No C++ unless the spikes show it is needed. The choice goes in `Agents/decisions/`.
- **Where things live.** Assets go under `Content/NHOS/` (`Maps/`, `Core/`, `UI/`, and `Stage/` for the 3D set from T11 on). Files the game reads at runtime go in `Content/NHOS/Data/` as `.json`. The API key and local switches go in `Local/` in the project root, which git ignores. The key file is `Local/llm_key.json`; copy it from `Docs/llm_key.example.json`. Blueprint reads it at `Get Project Directory` + `Local/llm_key.json`.
- **API keys never go in git, and never into chat.** I paste my key into the key file myself.
- **Prompts are files, not Blueprint strings.** The opening game prompt, the base prompt, the personas, the input LLM prompt and the scene cards live in `Content/NHOS/Data/`, so they diff in git. Store long text as an array of lines.
- **One provider.** All calls go to the Claude Messages API. The model, effort and token limit for each role (actor, input LLM, Director) are values in `Content/NHOS/Data/llm.json`. T01 and T02 ran `claude-opus-5-5` at low effort. Since 2026-11-13 every role runs `claude-haiku-5-5` at low effort, the cheapest model at its lowest level. Haiku 5.5 has no server-side fallback, so `beta` and `fallbacks` in `llm.json` are empty; a refusal comes back as `stop_reason: "refusal"`.
- **One provider per persona, from T16 and T18 on.** Each persona runs on its own provider, as in the design's table, with a key per provider (no router). T16 sets up the prompts and the keys; T18 makes the game call them. Since 2026-11-14 each bot goes by its provider's name on screen, in the log and in the cast list the AIs read (OpenAI, Anthropic, SpaceXAI, Meta: the `name` fields in `personas.json`), not by a persona name such as "The Worrier". Persona ids (`worrier`) stay as they are in files and `NHOS:` lines. Real people's names and product names stay out of prompts and off the screen.
- **The design doc follows the game.** The Claude Doc is the only source of truth for the design, and the repo keeps no copy of it: [GameDesign.md](GameDesign.md) only links it. When a task changes the design (the speech style, the sets, the providers), it shows me the matching edit to the Claude Doc, and after my OK it makes the edit with the Claude Docs connector. A prompt changes in the doc's Bot Prompts tab first, then word for word in `prompts.json` or `personas.json`. No script checks the two against each other.
- **Legibility first.** Everything an AI says reads like a normal chat, the way Claude or ChatGPT write: plain sentences, no brackets or tags, no beeps or sound effects, no emoji, no ALL-CAPS words. Each persona's personality comes through what it says, not how it is typed.
- **Outside and generated assets.** Record every art, audio or font asset in `Docs/Assets.md` when you add it: what it is, where it came from (a Fab link, a site, or the AI tool and prompt) and its license. The submission form needs the list.
- **One reply shape.** Every ask (scene turn, Free Talk line, vote, reaction, tiebreak) gets back the same small JSON object, with unused fields empty. One parser serves the whole game.
- **The shared log** is what the AIs read. Every actor's lines have the same form, human or AI. It never holds my raw input, times, errors, anyone's note, or who has the decoy. Game messages reach the AIs in a separate field that actors can't write to.
- **Check lines.** Anything a Done-when check reads is printed with the prefix `NHOS:` to the editor log (`Saved/Logs/AIMegaJam2026.log`). It never goes in the shared log.
- **Autoplay.** From T07 on, a local switch makes the human seat play canned lines, so an agent can run a whole show unattended and read the result in the log. The switch file is `Local/switches.json` (copy `Docs/switches.example.json`), with `"autoplay": true`. The canned lines are in `Content/NHOS/Data/autoplay.json`, one list per phase, and they go through the input LLM like typed lines. Later switches (such as T09's `force_tie`) go in the same file. Set autoplay back to `false` before a person plays.
- **Unreal MCP.** Do editor work through Unreal MCP. One call at a time, each under about 100 seconds (the client stops waiting at about 120). Split long work, and save after each step. Write graphs with `BlueprintTools.write_graph_dsl`, and batch calls with `ProgrammaticToolset.execute_tool_script`. Read "T01: spike results" in [Docs/tasks/T01.md](tasks/T01.md) first: it lists the DSL rules that cost time to find. Later tasks' files add more, each under "Unreal MCP rules found in this task". MCP can't create a level, so a person makes new levels in the editor (File > New Level > Empty Level).
- **Read only the graphs you need.** List a Blueprint's graphs, then read only the ones the task changes or calls, at about 6 s each. Never dump every graph of `BP_Show`: a full dump took 7 to 8 minutes in T18 and T26, and one was too big for a tool result.
- **Graph sources live in `Graphs/`.** `Graphs/<Blueprint>/<Graph>.txt` holds the DSL source last written to each graph, one file per graph, as written (shorthand, before `Tools/dslpp.py`). To change a graph, start from its file and push it. If it has no file yet, read the graph from the editor and write your source from that. Commit the updated files with the task. A read-back is for reading only, because writing one back drops data (T06). If you change a graph some other way, like a pin value or a hand edit in the editor, make the same change in its file, or delete the file. The per-task copies in `Saved/Txx/src/` from before 2026-11-14 may be out of date.
- **Worktrees, for sessions that don't need the editor.** The editor has the repo folder open, so a session that drives the editor or runs PIE works there. A session that doesn't need the editor may work in its own git worktree, on its own branch, when its files could clash with another session's uncommitted work in the repo folder (for example `Content/NHOS/Data/*.json` or `Docs/`).
  - Never change a `.uasset` or `.umap` in a worktree, because binary assets can't be merged.
  - A worktree has no `Local/` folder, and nothing gets copied into it, the key file least of all. Run `Tools/check_prompts.py` there with `--offline`, `--free` or `--relay`. A run that calls the providers with direct keys waits until after the merge, in the repo folder.
  - When the work is committed, merge `noHumansOnSet` into your branch and fix any conflicts there. Then merge your branch into the repo folder with `git -C <repo folder> merge --no-ff <branch>`, and push. If that merge stops because it would overwrite uncommitted changes in the repo folder, leave it and tell me.
- **New systems get their own Blueprint.** Put new logic in a new Blueprint or component, or in the actor it belongs to (such as `BP_Robot`), and have `BP_Show` call it from one node. Scripts that wrote `BP_Show` graphs took about 43 s each, and every editor task so far has needed the `BP_Show` lock.
- **Playtests run in a game window, not PIE.** When a task needs me to play, it saves every asset it changed, checks that the saved game runs (a free autoplay show reaches `SHOW END`), sets `autoplay` to false in `Local/switches.json`, pushes its work, and gives me the game-window command from `CLAUDE.md` for a playtest copy at that commit (see "When only my check is left"). The copy plays only the committed work, so the editor stays free and the next task can start, even on the same assets, while I play. A key-mode playtest runs in the repo folder instead, because the key file never goes in a copy. Until I say I'm done with it, no session changes `Local/switches.json` or saves the assets under test. Its log is a second file in `Saved/Logs/`. T27 was the first task to use it; its findings in [Docs/tasks/T27.md](tasks/T27.md) have the Mac command, the Mac log paths and how to screenshot a game window.
- **Each task leaves the game runnable.** One task = one session = one commit (two when it waits for my check), about an hour of agent work at most.

## Tasks

"Open" holds the tasks still to do, in priority order: "Next task" takes the first free one from the top. A new task goes wherever it belongs in that order (see "Changing the plan"), so the numbers are not in order. "Done" holds the finished tasks, oldest first. When a task's box is checked, its entry moves to the end of "Done" (see "How to run a task", step 6). Each entry links its file in `Docs/tasks/`, which holds the task's Why, Steps, Done-when check, Result and findings.

### Open

- [ ] **T28 Scene Prep shows the whole card, the scene shows only mine**
  - **Model and effort:** Opus 5.5, high. It adds a pause to the show loop and splits the info card by phase.
  - **Depends on:** T27 (the card's place and size), T19 (the lock on `BP_Show`)
  - **Needs:** editor + Unreal MCP running, Test for Free for the PIE shows, my playtest (one show).
  - **Touches:** `Content/NHOS/UI/WBP_Stage.uasset`, `Content/NHOS/Core/BP_Show.uasset` (`ScenePrep`, the Start button's call, `ShowPrep` if the card's fill changes), `Graphs/` files for the graphs it writes, the design doc.
  - **Details:** [Docs/tasks/T28.md](tasks/T28.md)

- [ ] **T29 The chat holds only chat**
  - **Model and effort:** Opus 5.5, high. It reroutes every game line in `BP_Show` without reading every graph.
  - **Depends on:** T28 (the same widgets and `BP_Show`; the Scene Prep lines move into its card)
  - **Needs:** editor + Unreal MCP running, Test for Free for the PIE shows, my playtest (one show).
  - **Touches:** `Content/NHOS/Core/BP_Show.uasset`, `Content/NHOS/UI/WBP_Stage.uasset`, `Graphs/` files for the graphs it writes, `Docs/tasks/T29.md`.
  - **Details:** [Docs/tasks/T29.md](tasks/T29.md)

- [ ] **T32 UI/UX audit, style guide and shared pieces**
  - **Model and effort:** Opus 5.5, high. Design judgment across every screen, and one style that all the widgets share.
  - **Depends on:** T28, T29, T35 (Scene Prep, my card and the chat's content are final, `WBP_Stage` is unlocked, and the money-burn overlay exists to audit). T27 is done. T30 comes after this task, so its typing line is T34's to check.
  - **Needs:** editor + Unreal MCP running, Test for Free for the PIE shows. No playtest: I read the findings and any doc edits and say go.
  - **Touches:** the design doc's UI section (after my OK), `Docs/Assets.md`, a new style Blueprint under `Content/NHOS/UI/`, `Content/NHOS/UI/WBP_ChatLine.uasset`, `Docs/tasks/T32.md`, `Graphs/` files for the graphs it writes. It only reads the other widgets.
  - **Details:** [Docs/tasks/T32.md](tasks/T32.md)

- [ ] **T30 The lines play one at a time**
  - **Model and effort:** Opus 5.5, high. Timing across the show loop, the chat and the stage.
  - **Depends on:** T19 (the stage acts out each line), T29 (only actor lines and the banner are left to pace)
  - **Needs:** editor + Unreal MCP running, Test for Free for the PIE shows, my playtest (one show).
  - **Touches:** new `Content/NHOS/Core/BPC_LinePlayer.uasset`, `Content/NHOS/Core/BP_Show.uasset` (`ShowLine`, `ActorLine`, the waits), `Content/NHOS/UI/WBP_Stage.uasset` (the typing line), a data file in `Content/NHOS/Data/`, `Docs/switches.example.json`, `Graphs/` files for the graphs it writes, the design doc.
  - **Details:** [Docs/tasks/T30.md](tasks/T30.md)

- [ ] **T38 Every line plays in a speech bubble, and the chat opens on a click**
  - **Model and effort:** Opus 5.5, high. A new widget placed over moving robots, timed by the line queue, and a new hidden state for the chat.
  - **Depends on:** T30 (the line queue: a bubble shows when its line plays, and the typing line becomes a bubble), T32 (the style Blueprint and the shared button style)
  - **Needs:** editor + Unreal MCP running, Test for Free for the PIE shows, my playtest (one show, in a game window).
  - **Touches:** new `Content/NHOS/UI/WBP_SpeechBubble.uasset`, `Content/NHOS/Stage/BP_Robot.uasset` (the bubble, `Say`, `Hush`), `Content/NHOS/Core/BPC_LinePlayer.uasset` (the call when a line plays, the typing bubble), `Content/NHOS/UI/WBP_Stage.uasset` (the chat button, the chat hidden at the start, the typing line), `Content/NHOS/Core/BP_Show.uasset` only if a call must change, `Graphs/` files for the graphs it writes, the design doc, `Docs/tasks/T38.md`.
  - **Details:** [Docs/tasks/T38.md](tasks/T38.md)

- [ ] **T34 Fix the in-show screen**
  - **Model and effort:** Opus 5.5, high. Hierarchy and state judgment on the busiest screen.
  - **Depends on:** T32, T30, T38 (the line pacing, its typing line, the speech bubbles and the chat button are in, so this task polishes the final screen)
  - **Needs:** editor + Unreal MCP running, Test for Free for the PIE shows, my playtest (one show, in a game window).
  - **Touches:** `Content/NHOS/UI/WBP_Stage.uasset`, `WBP_SpeechBubble.uasset`, `WBP_ChatLine.uasset` and `WBP_MoneyBurn.uasset` if T32 left a row for either, `Content/NHOS/Core/BP_Show.uasset` only if a widget's call must change (for example `SetPrompt`), `Graphs/WBP_Stage/` files, `Docs/tasks/T34.md` and the audit table in `Docs/tasks/T32.md`.
  - **Details:** [Docs/tasks/T34.md](tasks/T34.md)

- [ ] **T20 Audio**
  - **Model and effort:** Sonnet 5.5, medium. Finding sounds and playing them at points the show loop already has.
  - **Depends on:** T19 (the locks on `BP_Show` and `BP_Robot`). Finding and choosing the files needs no editor and can start any time.
  - **Needs:** editor + Unreal MCP running, my ears for one show.
  - **Touches:** new `Content/NHOS/Audio/`, `Content/NHOS/Core/BP_Show.uasset`, `Content/NHOS/Stage/BP_Robot.uasset`, `Content/NHOS/UI/`, `Docs/Assets.md`.
  - **Details:** [Docs/tasks/T20.md](tasks/T20.md)

- [ ] **T33 Fix the title, key entry and end screens**
  - **Model and effort:** Sonnet 5.5, medium. Well-specified UMG work from T32's table and style guide.
  - **Depends on:** T32, T21 (it changes `WBP_Keys` and adds a screen)
  - **Needs:** editor + Unreal MCP running, Test for Free for the PIE shows, my playtest (one show, from the title to the end screen).
  - **Touches:** `Content/NHOS/UI/WBP_Title.uasset`, `WBP_Keys.uasset`, `WBP_EndScreen.uasset`, `WBP_EndCard.uasset`, T21's unavailable-screen widget, `Graphs/` files for the graphs it writes, `Docs/tasks/T33.md` and the audit table in `Docs/tasks/T32.md`.
  - **Details:** [Docs/tasks/T33.md](tasks/T33.md)

- [ ] **T36 Each burning bill shows the logo of the provider it paid**
  - **Model and effort:** Sonnet 5.5, medium. Four small images, one image added to a widget that is already built, and one value passed through two calls.
  - **Depends on:** T35 (the money burn), T34 (it may change `WBP_MoneyBurn`). Steps 1 and 2 (find the logos and make the badges) need no editor and can run as prep at any time.
  - **Needs:** my OK before each logo download, editor + Unreal MCP running, Test for Free with `burn_test` on for the checks, and my look at one free show in a game window. No relay show: in relay mode, `Burn` reads the same `CurProv` that `Deliver` prints for each relay reply.
  - **Touches:** new `Docs/MoneyBurnArt/logo_*.png` and `Content/NHOS/UI/MoneyBurn/T_Logo_*.uasset`, `Content/NHOS/UI/WBP_BurningBill.uasset`, `Content/NHOS/UI/WBP_MoneyBurn.uasset` (`Burn`), `Content/NHOS/Core/BPC_LLMClient.uasset` (`Burn` only), `Docs/MoneyBurnArt.md`, `Docs/Assets.md`, `Graphs/BPC_LLMClient/Burn.txt`, `Graphs/WBP_MoneyBurn/Burn.txt`, new `Graphs/WBP_BurningBill/SetLogo.txt`.
  - **Details:** [Docs/tasks/T36.md](tasks/T36.md)

- [ ] **T37 Error messages say what went wrong, with a joke**
  - **Model and effort:** Opus 5.5, high. It sorts every error path in the client into cases, and adds one note that crosses the client, the show and the banner.
  - **Depends on:** T29 (the banner), T30 (the banner waits for the line queue), T33 (it lays out the key screen and the unavailable screen that show these lines). T21 is done.
  - **Needs:** editor + Unreal MCP running, Test for Free with the new `error_test` switch for the PIE shows, T21's local stub relay for the budget message, and one fake Anthropic key for the key test (no tokens). No relay or key-mode show.
  - **Touches:** new `Content/NHOS/Data/errors.json`, `Content/NHOS/Core/BPC_LLMClient.uasset` (new `ErrorKind` and `ErrorLine`; `ParseReply`, `HandleHttp`, `OnHealth`, `OnKeyTest`, `KeyTestResult`, `SetMode`, `Deliver` and the free-mode path for `error_test`), `Content/NHOS/Core/BP_Show.uasset` (one node that shows the note on the banner), `Content/NHOS/UI/WBP_Stage.uasset` only if the banner needs a longer hold for a note, `Tools/check_prompts.py`, `Docs/switches.example.json`, `Graphs/` files for the graphs it writes.
  - **Details:** [Docs/tasks/T37.md](tasks/T37.md)

- [ ] **T31 Tab completes names, places and props (cut if we fall behind)**
  - **Model and effort:** Sonnet 5.5, medium. Input-box work on a widget that is already laid out.
  - **Depends on:** T27 (the input row), T30 (the lock on `WBP_Stage`)
  - **Needs:** editor + Unreal MCP running, Test for Free for the PIE shows, my playtest (one show).
  - **Touches:** `Content/NHOS/UI/WBP_Stage.uasset` (the input box's keys and the suggestion row), maybe `Content/NHOS/Core/BP_Show.uasset` (to hand the names, places and props to the widget), `Graphs/` files for the graphs it writes, the design doc.
  - **Details:** [Docs/tasks/T31.md](tasks/T31.md)

- [ ] **T23 Submission**
  - **Model and effort:** Sonnet 5.5, medium. Writing and checklists.
  - **Depends on:** T19, T20, T21, T27, T28, T29, T30, T32, T33, T34, T35, T38, T24 if it is done, T31 if it is done, T36 if it is done, and T37 if it is done
  - **Needs:** me, to record the video, set up the itch.io page and send the form. The packaged build, which I make myself.
  - **Touches:** `Docs/ItchPage.md`, new `Docs/Submission.md`, `Packaged/` (not in git).
  - **Details:** [Docs/tasks/T23.md](tasks/T23.md)

- [ ] **T24 Timers (only if time allows)**
  - **Model and effort:** Sonnet 5.5, medium. Small additions to phases that already work.
  - **Depends on:** T19, T30 (the input row and the line queue; it took over this task's AI typing delay on 2026-11-14). Cut it first if we fall behind.
  - **Needs:** editor + Unreal MCP running, my API key.
  - **Touches:** `Content/NHOS/Core/BP_Show.uasset`, `Content/NHOS/UI/WBP_Stage.uasset`, `Content/NHOS/Data/scenes.json`.
  - **Details:** [Docs/tasks/T24.md](tasks/T24.md)

### Done

- [x] **T01 Spike: one Claude call from Blueprint, in PIE**
  - **Details:** [Docs/tasks/T01.md](tasks/T01.md)
- [x] **T02 Spike: the same call in a packaged Windows build, and record the decision**
  - **Details:** [Docs/tasks/T02.md](tasks/T02.md)
- [x] **T03 Prompt and data files**
  - **Details:** [Docs/tasks/T03.md](tasks/T03.md)
- [x] **T04 Stage screen: a log and an input box**
  - **Details:** [Docs/tasks/T04.md](tasks/T04.md)
- [x] **T05 One AI reply on screen**
  - **Details:** [Docs/tasks/T05.md](tasks/T05.md)
- [x] **T06 Show setup and Scene Prep**
  - **Details:** [Docs/tasks/T06.md](tasks/T06.md)
- [x] **T07 The Scene: three simultaneous turns**
  - **Details:** [Docs/tasks/T07.md](tasks/T07.md)
- [x] **T08 Free Talk**
  - **Details:** [Docs/tasks/T08.md](tasks/T08.md)
- [x] **T09 The Cut: votes, tiebreak and reveal**
  - **Details:** [Docs/tasks/T09.md](tasks/T09.md)
- [x] **T10 Reactions, the final two, end screens and restart**
  - **Details:** [Docs/tasks/T10.md](tasks/T10.md)
- [x] **T11 The cast on stage: four box robots**
  - **Details:** [Docs/tasks/T11.md](tasks/T11.md)
- [x] **T12 Go/no-go gate: I play 3 shows**
  - **Details:** [Docs/tasks/T12.md](tasks/T12.md)
- [x] **T13 The AIs talk like a normal chat**
  - **Details:** [Docs/tasks/T13.md](tasks/T13.md)
- [x] **T14 UI/UX polish**
  - **Details:** [Docs/tasks/T14.md](tasks/T14.md)
- [x] **T15 Story scenes on an improv stage**
  - **Details:** [Docs/tasks/T15.md](tasks/T15.md)
- [x] **T16 One LLM per AI player: prompts and keys**
  - **Details:** [Docs/tasks/T16.md](tasks/T16.md)
- [x] **T18 One LLM per AI player: in the game, and three ways to play**
  - **Details:** [Docs/tasks/T18.md](tasks/T18.md)
- [x] **T26 Five actors: one AI per provider, plus me**
  - **Details:** [Docs/tasks/T26.md](tasks/T26.md)
- [x] **T17 Stage art and personality**
  - **Details:** [Docs/tasks/T17.md](tasks/T17.md)
- [x] **T19 Robots act out their actions**
  - **Details:** [Docs/tasks/T19.md](tasks/T19.md)
- [x] **T27 The screen floats over the stage**
  - **Details:** [Docs/tasks/T27.md](tasks/T27.md)
- [x] **T25 The design docs point to the Claude Doc**
  - **Details:** [Docs/tasks/T25.md](tasks/T25.md)
- [x] **T35 A bill burns in the bottom-right corner for every relay call**
  - **Details:** [Docs/tasks/T35.md](tasks/T35.md)
- [x] **T21 How a judge plays: the relay's limits on screen, and the itch.io page**
  - **Details:** [Docs/tasks/T21.md](tasks/T21.md)

## Not planned yet

Ideas that are not tasks yet, and only if time is left after T23: a fifth persona (since T26, that is a sixth actor and a fourth scene), more scene cards and more notes. To plan one, add it as a task (see "Changing the plan").
