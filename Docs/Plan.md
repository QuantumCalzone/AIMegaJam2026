# Plan: No Humans On Set

The living plan for our jam game: the tasks in priority order, how to run one and how to add one. The design is a private Claude Doc, linked from [GameDesign.md](GameDesign.md). Say **"Next task"** to build the next step.

In this file, "I" and "my" mean the person at the keyboard. "Claude" means the agent doing the task.

**Next up:** Since 2026-11-15 no task waits for me to play: Claude plays the shows itself (see "Claude does the playing" under "Build notes for every task"). T29 (the chat holds only chat) is done. T32 (the UI audit, `UIStyle` and the shared pieces) is done: later UI tasks style their widgets with `UIStyle` (see `Docs/tasks/T32.md`). T30 (the lines play one at a time) is done: every line plays one at a time, and `Content/NHOS/Data/pacing.json` sets the pace. The design doc stays as it is, so its Rules tab still says each turn's lines play out at once. Next in the editor: T38 (every line in a speech bubble, and the chat opens on a click) and T34 (the in-show screen); T34 starts with the vote bug T32 found (the fourth vote button votes for the third name), and T33 left it two rows (T33-1: the in-show buttons can't take keyboard focus; T33-2: the robots' tags show through full-screen panels). T33 (the title, key entry and end screens) is done: they are styled from `UIStyle` and play by keyboard. T20 (audio) is done: music, the vote's drum roll, the reveal stingers, applause and laughs, talk blips, robot sounds and button clicks, from the new `BPC_ShowAudio` component on `BP_Show`. Every one of these tasks changes `BP_Show` or `WBP_Stage`, so they go one at a time in the editor. T39 (the art batch tool) is done. T40 (the headpieces) is done. T41 (the story props) is done. T42 (the opera-house pieces) is done (90 credits, balance 60). T43 (the imports and `M_Clay`) is done: all 43 generated models are assets (`Stage/Headpieces/`, `Stage/Props/<card id>/`, `Stage/Set/`), each with its scale and yaw (90 for every Meshy model) in `Docs/PropArt/manifest.json`, and `M_Clay` with `MI_Clay_Neutral` is in `Stage/Materials/`; T45, T46, T47 and T49 build on them. The design's rules changed on 2026-11-15 (only the bots get the director's note, no decoy, a tie cuts nobody, a scene clock, no Director AI, rivals, visible passes, a last word, a 15-word cap, new end screens and a stagehand who teaches the rules); T50 to T61 build them, one task per change. T56 (the rivals) is done: each persona's prompt ends with its rival line, and `personas.json` has a `rival` field for T60. T51 (no decoy note) is done: every actor gets the same note, and each of the 10 notes has a category (Movement, Props, Looks or Speech) that T50 shows to everyone. The others go in this order: T50, T59, T53, T52, T54, T55, T57, T58, all before T38 and T34. T60 and T61 can build on T33's end and title screens.

## Goal

Finish **No Humans On Set** and submit it to the 2026 Epic AI MegaJam. The "Open" tasks below are what we know is still to do. I add tasks as the game needs them, and a new task goes wherever it belongs in that list (see "Changing the plan").

**How the plan began.** It started as the plan for an MVP (T01 to T12), which had to answer one question as fast as possible: is it fun to fool an all-AI cast, and do the AIs catch a human at a fair rate (not every time, not never)? The gate (T12, 2026-11-14) said go. I liked it. Since then the plan covers the whole game. Until 2026-11-14 this file was `Docs/MVPPlan.md`. Finished tasks' files, the dev log and older notes in `Agents/` still use that name. Until 2026-11-14 this file also held every task's full text and a Findings section; since then each task has its own file in `Docs/tasks/` (see "Tasks").

## Cut order

If I decide to cut scope, cut in this order: T24 (timers), then T31 (Tab completion), then T38 (speech bubbles; the chat stays as it is now, and T34 polishes that), then T19 to Move and Look only, then T20 to music and three sounds, then T17's robot motion.

## How to run a task

When I say **"Next task"** or **"Next ask"**:

1. `git pull` (if the branch is not on the remote yet, say so and go on). Read `Agents/`. Open this file and run `git lfs locks`. Take the first task in "Open" that is free (see "Claiming a task") and whose **Depends on** tasks are all checked, or wait only for my check (see "When only my check is left"). Then read the task's file, `Docs/tasks/Txx.md` (its **Details** link): it holds the Why, the Steps, the Done-when check and what earlier work found. Read another task's file only when yours points to it.
2. Tell me the task and its recommended model and effort. If this session runs a different model, say so and ask whether to go on.
3. Check its Needs. If something is missing (for example, Unreal MCP is not connected), tell me what to do and stop.
4. Claim the task (see "Claiming a task"). Write a status file, `Agents/status/task-T07.md`, and lock assets as `Agents/README.md` says.
5. Do the work, then run the Done-when check. If the check fails, do not mark the task done: write what blocks it under the task's entry in this file (a `Blocked:` line, never only in the task's file) and tell me. If the only part of the check left is mine (my verdict, my OK on a doc edit, or a run that needs something from me), follow "When only my check is left" instead of step 6.
6. Make one commit that holds the work; the task's entry in this file with its box checked, moved to the end of "Done" and cut down to its title line and its **Details** line; the task's file with the lines cut from the entry (**Model and effort**, **Depends on**, **Needs**, **Touches**) moved to the top of its "## Task" section, the line under its title changed to say the task is done, a **Result:** line at the end of "## Task", and what the task found under "## Findings" at the end of the file; the updated "Next up" line; and one line in [DevLog.md](DevLog.md) (the jam's Glass Box category needs a dev log). Message: `T07: <title>`. Then push it with `git push`. You don't need to ask. If the push is rejected, don't pull or rebase while other sessions have uncommitted work in this folder; tell me.
7. Delete the status file. Once the commit that checks the box is pushed, release the claim. Unlock the assets the task changed too, unless another running session still has uncommitted changes in them (`git status`, `Agents/status/`). End by naming the next task with its model and effort, so I can switch before I send "Next task".

## Claiming a task

A claim is an LFS lock on the task's claim file. Everyone sees it at once, on every machine, with no push.

- **Claim:** `git lfs lock Docs/claims/T07`
- **See all claims:** `git lfs locks`
- **Release:** `git lfs unlock Docs/claims/T07`, after the commit that checks the task's box is pushed. Until the push, other machines see neither the work nor the checked box, so the lock is what tells them the task is taken. A task that waits for my verdict or OK keeps its claim until its box is checked. Whoever pushes releases the claims of every checked task that went up.
- A task is free when its box is unchecked here, it has no `Waiting:` line, and `git lfs locks` shows no lock on its claim file.
- If the lock fails because a teammate holds it, take the next free task.
- If my own account holds the lock on an unchecked task and there is no status file for it in `Agents/status/`, an earlier session may have stopped halfway. Ask me before taking it.
- If you stop without finishing, add a `Blocked:` line under the task and commit it as `Plan: T07 blocked`. Release the claim only if someone else should take the task.

Never edit the claim files. They exist only to be locked.

## When only my check is left

Some tasks end with my verdict, my OK on a doc edit, or a run that needs something from me. A playtest is never one of them: Claude plays the shows itself (see "Claude does the playing" under "Build notes for every task"). The next task doesn't wait for my check:

1. **Push the work first.** When the work is built and the Done-when check passes except for the part only I can do, commit and push now. The commit holds the work, its `Graphs/` files, the task's file with what it found so far, a `Waiting:` line under the task's entry in this file (it ends `Left: <what I must do>`), the "Next up" line and one line in [DevLog.md](DevLog.md). Message: `Txx: <title> (waits for <what>)`. The box stays unchecked.
2. **Free what you hold.** Unlock the assets the task changed, keep the claim, and set the `Editor:` line in your status file to `not using`. Keep the status file: it says what you wait for.
3. **The next task can start.** A task may start when each task in its **Depends on** line is checked, or has its work pushed with a `Waiting:` line that leaves only my check. It builds on that work as pushed.
4. **If my check passes,** make the closing commit as step 6 of "How to run a task" says: check the box, remove the `Waiting:` line, move the entry to "Done", and add the Result and the findings. It needs a DevLog line only if the check changed something. Message: `Txx: <title> (checked)`. Push it, release the claim and delete the status file.
5. **If my check finds a problem,** the fix goes first in the editor lane, but only once no running session holds the task's assets (`git lfs locks`, `Agents/status/`). Until then, tell me, and wait. When they are free, lock them again, fix the problem, push with the `Waiting:` line kept. Tell me what the fix changed, so that later tasks that built on your work can check it.

## Changing the plan

I add tasks as the game needs them, and a task can go anywhere in the list. Every change to the plan outside a task's own commit is a commit too, `Plan: <what changed>`, with a line in [DevLog.md](DevLog.md). One example is a verdict that changes the design.

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
- **The shared log** is what the AIs read. Every actor's lines have the same form, human or AI. It never holds my raw input, times, errors or anyone's note. Game messages reach the AIs in a separate field that actors can't write to.
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
- **Claude does the playing; I don't playtest (since 2026-11-15).** No task waits for me to play, and no session asks me to. Where a check needs a show played, Claude plays it: one show by hand in PIE (Test for Free, a 1600 × 900 floating window, clicks and typing through the Slate inspector, autoplay off) with a screenshot of each phase the task changed, and a free autoplay show in a game window on the saved assets that reaches `SHOW END`. Claude judges what my playtest used to judge (can I read it, can I follow it, does the screen feel blocked, does it look finished) from those screenshots, as a critical first-time player would, and writes what it saw under "## Findings". What screenshots can't show (sound, for example) is written there as unchecked, and the task still closes. Set `autoplay` back to false and close each game window when done. T27's findings in [Docs/tasks/T27.md](tasks/T27.md) have the Mac command, the Mac log paths and how to screenshot a game window.
- **Each task leaves the game runnable.** One task = one session = one commit (two when it waits for my check), about an hour of agent work at most.

## Tasks

"Open" holds the tasks still to do, in priority order: "Next task" takes the first free one from the top. A new task goes wherever it belongs in that order (see "Changing the plan"), so the numbers are not in order. "Done" holds the finished tasks, oldest first. When a task's box is checked, its entry moves to the end of "Done" (see "How to run a task", step 6). Each entry links its file in `Docs/tasks/`, which holds the task's Why, Steps, Done-when check, Result and findings.

### Open

- [ ] **T50 Only the bots get the director's note**
  - **Model and effort:** Opus 5.5, high. The headline rule change: who gets the note, what my card shows and what the bots are told all change together.
  - **Depends on:** T51 (the categories, and no decoy), T28 (my card)
  - **Needs:** editor + Unreal MCP running, Test for Free for the PIE shows, the relay for a `--relay --free` check, and one relay show that Claude plays by hand itself (the check is how the real AIs play the note).
  - **Touches:** `Content/NHOS/Data/prompts.json` (`game`, `asks.scene_turn`, `asks.free_talk`, `_readme`), `Tools/check_prompts.py`, `Content/NHOS/Core/BP_Show.uasset` (the note deal, `ActorState`), `Content/NHOS/UI/WBP_Stage.uasset` (my card: the category and the blacked-out note), `Graphs/` files for the graphs it writes, `Docs/ItchPage.md`, `Docs/tasks/T50.md`.
  - **Details:** [Docs/tasks/T50.md](tasks/T50.md)

- [ ] **T59 Every line is capped at 15 words, mine too**
  - **Model and effort:** Sonnet 5.5, medium. One number, changed in every place that holds it.
  - **Depends on:** T50 (the lock on `BP_Show`)
  - **Needs:** editor + Unreal MCP running, Test for Free for the PIE shows, the relay for a `--relay --free` check. My OK before the relay is deployed again, if its free mode holds the old cap.
  - **Touches:** `Content/NHOS/Data/prompts.json` (`input`, `game`), `Content/NHOS/Data/llm.json` (`_readme`), `Content/NHOS/Data/free_mode.json`, `Relay/` (free mode, if it cuts at 25), `Tools/check_prompts.py` (`MAX_WORDS`), `Content/NHOS/Core/BP_Show.uasset` (`CapWords`), `Docs/ItchPage.md`, `Graphs/` files for the graphs it writes, `Docs/tasks/T59.md`.
  - **Details:** [Docs/tasks/T59.md](tasks/T59.md)

- [ ] **T53 Scene clock: one scene fewer than the cast, on a clapperboard**
  - **Model and effort:** Opus 5.5, high. The show's length and its end check change, and a new piece goes on the in-show screen.
  - **Depends on:** T59 (the lock on `BP_Show`), T30 (the lock on `WBP_Stage`)
  - **Needs:** editor + Unreal MCP running, Test for Free for the PIE shows.
  - **Touches:** `Content/NHOS/Core/BP_Show.uasset` (`SceneCount` in `SetupShow`, the end check after the reactions, the scene banner's text), `Content/NHOS/UI/WBP_Stage.uasset` (the clapperboard), `Content/NHOS/Data/prompts.json` (`game`), `Tools/check_prompts.py` (`show.scenes`), `Graphs/` files for the graphs it writes, `Docs/tasks/T53.md`.
  - **Details:** [Docs/tasks/T53.md](tasks/T53.md)

- [ ] **T52 A tie cuts nobody**
  - **Model and effort:** Opus 5.5, high. A new branch in The Cut that must leave every later phase in a good state.
  - **Depends on:** T53 (the spare scene, and the show's end after the last scene)
  - **Needs:** editor + Unreal MCP running, Test for Free with `force_tie` for the PIE shows, my answer to one question (do the reactions run after a tie?).
  - **Touches:** `Content/NHOS/Core/BP_Show.uasset` (`Tally` and the step after a tie), `Content/NHOS/Data/prompts.json` (`game`), `Tools/check_prompts.py`, `Docs/switches.example.json` (`force_tie`), `Graphs/` files for the graphs it writes, `Docs/tasks/T52.md`.
  - **Details:** [Docs/tasks/T52.md](tasks/T52.md)

- [ ] **T54 New win condition: the final two, or on stage when the last scene ends**
  - **Model and effort:** Sonnet 5.5, medium. The end is already built (T53, T52); this task makes every text say the new rule.
  - **Depends on:** T53, T52 (a show can now end after its last scene with more than two actors on stage)
  - **Needs:** editor + Unreal MCP running, Test for Free with `force_tie` and `spare_human` for the PIE shows, the relay for a `--relay --free` check.
  - **Touches:** `Content/NHOS/Data/prompts.json` (`game`, `asks.closing`), `Tools/check_prompts.py`, `Content/NHOS/Core/BP_Show.uasset` (`EndShow`, `ShowEndScreen`, the `SHOW END` line), `Docs/ItchPage.md`, `Graphs/` files for the graphs it writes, `Docs/tasks/T54.md`.
  - **Details:** [Docs/tasks/T54.md](tasks/T54.md)

- [ ] **T55 Remove the Director AI**
  - **Model and effort:** Opus 5.5, high. A role comes out of the prompts, the settings, free mode, the checker and `BP_Show` with nothing left pointing at it.
  - **Depends on:** T52 (no tie reaches the Director any more)
  - **Needs:** editor + Unreal MCP running, Test for Free with `force_tie` for the PIE shows, the relay for a `--relay --free` check, my OK before the relay is deployed again (it bundles `free_mode.json`).
  - **Touches:** `Content/NHOS/Data/prompts.json` (`director`, `asks.tiebreak`, `_readme`), `Content/NHOS/Data/llm.json` (`roles.director`, the readmes), `Content/NHOS/Data/free_mode.json` (the `tiebreak` phase), `Tools/check_prompts.py`, `Content/NHOS/Core/BP_Show.uasset` (`AskDirector`, `PlayTiebreak`, `DirectorCut`, `DirectorState`, the tiebreak branch of `HandleReply`), `Relay/`, `Docs/switches.example.json`, `Docs/ItchPage.md`, `Graphs/` files for the graphs it writes, `Docs/tasks/T55.md`.
  - **Details:** [Docs/tasks/T55.md](tasks/T55.md)

- [ ] **T57 Silence and polish are tells: a pass shows as "passed"**
  - **Model and effort:** Opus 5.5, high. A prompt change that reverses an old rule ("how a line is typed is never evidence"), plus a marker on the in-show screen.
  - **Depends on:** T30 (the line queue plays each Free Talk line), T50 (the rule lines it sits beside), T55 (the lock on `BP_Show`)
  - **Needs:** editor + Unreal MCP running, Test for Free for the PIE shows, the relay for a `--relay --free` check.
  - **Touches:** `Content/NHOS/Data/prompts.json` (`game`, `asks.free_talk`), `Tools/check_prompts.py`, `Content/NHOS/Core/BP_Show.uasset` (`PlayTalk`, the start of each Free Talk), `Content/NHOS/UI/WBP_Stage.uasset` or `Content/NHOS/Stage/BP_Robot.uasset` (the "passed" marker), `Graphs/` files for the graphs it writes, `Docs/tasks/T57.md`.
  - **Details:** [Docs/tasks/T57.md](tasks/T57.md)

- [ ] **T58 Last word: a reply for anyone @-mentioned in the final round**
  - **Model and effort:** Opus 5.5, high. A new step between Free Talk and The Cut, with a new ask and a human turn.
  - **Depends on:** T57 (the lock on `BP_Show`, and Free Talk as it leaves it), T30 (the line queue)
  - **Needs:** editor + Unreal MCP running, Test for Free for the PIE shows, the relay for a `--relay --free` check, my OK before the relay is deployed again (a new free-mode phase).
  - **Touches:** `Content/NHOS/Data/prompts.json` (new `asks.last_word`, `game`), `Content/NHOS/Data/free_mode.json`, `Content/NHOS/Data/autoplay.json`, `Tools/check_prompts.py`, `Content/NHOS/Core/BP_Show.uasset` (`NextTalker`, `EndFreeTalk`, new functions, `ComputePrompt`), `Relay/`, `Graphs/` files for the graphs it writes, `Docs/tasks/T58.md`.
  - **Details:** [Docs/tasks/T58.md](tasks/T58.md)

- [ ] **T38 Every line plays in a speech bubble, and the chat opens on a click (optional)**
  - **Model and effort:** Opus 5.5, high. A new widget placed over moving robots, timed by the line queue, and a new hidden state for the chat.
  - **Depends on:** T30 (the line queue: a bubble shows when its line plays, and the typing line becomes a bubble), T32 (the style Blueprint and the shared button style)
  - **Needs:** editor + Unreal MCP running, Test for Free for the PIE shows.
  - **Touches:** new `Content/NHOS/UI/WBP_SpeechBubble.uasset`, `Content/NHOS/Stage/BP_Robot.uasset` (the bubble, `Say`, `Hush`), `Content/NHOS/Core/BPC_LinePlayer.uasset` (the call when a line plays, the typing bubble), `Content/NHOS/UI/WBP_Stage.uasset` (the chat button, the chat hidden at the start, the typing line), `Content/NHOS/Core/BP_Show.uasset` only if a call must change, `Graphs/` files for the graphs it writes, the design doc, `Docs/tasks/T38.md`.
  - **Details:** [Docs/tasks/T38.md](tasks/T38.md)

- [ ] **T34 Fix the in-show screen**
  - **Model and effort:** Opus 5.5, high. Hierarchy and state judgment on the busiest screen.
  - **Depends on:** T32, T30, T38 (the line pacing, its typing line, the speech bubbles and the chat button are in, so this task polishes the final screen). If T38 is cut, take it off this line. Also T50, T53, T57 (the note category on my card, the clapperboard and the "passed" marker are on the screen it polishes).
  - **Needs:** editor + Unreal MCP running, Test for Free for the PIE shows.
  - **Touches:** `Content/NHOS/UI/WBP_Stage.uasset`, `WBP_SpeechBubble.uasset`, `WBP_ChatLine.uasset` and `WBP_MoneyBurn.uasset` if T32 left a row for either, `Content/NHOS/Core/BP_Show.uasset` only if a widget's call must change (for example `SetPrompt`), `Graphs/WBP_Stage/` files, `Docs/tasks/T34.md` and the audit table in `Docs/tasks/T32.md`.
  - **Details:** [Docs/tasks/T34.md](tasks/T34.md)

- [ ] **T60 Win and lose screens: the reasoning, the top reason and the rivals**
  - **Model and effort:** Opus 5.5, high. It turns the vote history into one named reason, and adds a reveal to the end screen.
  - **Depends on:** T33 (the end screens' layout), T56 (the rivals), T54 (the two ways to win), T55 (no Director line in the vote history)
  - **Needs:** editor + Unreal MCP running, Test for Free with `spare_human` and `force_tie` for the PIE shows, my answer to one question (how the top reason is found).
  - **Touches:** `Content/NHOS/Core/BP_Show.uasset` (`ShowEndScreen`, `StoreClosing`, the vote history), `Content/NHOS/UI/WBP_EndScreen.uasset`, `Content/NHOS/UI/WBP_EndCard.uasset`, `Content/NHOS/Data/personas.json` (read only: `rival`), maybe `Content/NHOS/Data/llm.json` and `prompts.json` (if a vote names its tell), `Tools/check_prompts.py`, `Graphs/` files for the graphs it writes, `Docs/tasks/T60.md`.
  - **Details:** [Docs/tasks/T60.md](tasks/T60.md)

- [ ] **T61 Stagehand onboarding: earpiece tips, a tips toggle and How to play**
  - **Model and effort:** Opus 5.5, high. A new system with its own data file, component and widgets, called from the show at eight moments.
  - **Depends on:** T33 (the title screen), T34 (the in-show screen), T50, T52, T53, T57, T58 (the rules its lines teach), T60 (the lose and win screens it speaks on)
  - **Needs:** editor + Unreal MCP running, Test for Free for the PIE shows.
  - **Touches:** new `Content/NHOS/Data/stagehand.json`, new `Content/NHOS/Core/BPC_Stagehand.uasset`, new `Content/NHOS/UI/WBP_Earpiece.uasset` and `WBP_HowToPlay.uasset`, `Content/NHOS/UI/WBP_Title.uasset` (the How to play button and the tips toggle), `Content/NHOS/UI/WBP_Stage.uasset` (the earpiece's place), `Content/NHOS/Core/BP_Show.uasset` (one call per moment), a new file in `Local/` for the first-show flag, `Tools/check_prompts.py`, `Docs/ItchPage.md`, `Graphs/` files for the graphs it writes, `Docs/tasks/T61.md`.
  - **Details:** [Docs/tasks/T61.md](tasks/T61.md)

- [ ] **T36 Each burning bill shows the logo of the provider it paid**
  - **Model and effort:** Sonnet 5.5, medium. Four small images, one image added to a widget that is already built, and one value passed through two calls.
  - **Depends on:** T35 (the money burn), T34 (it may change `WBP_MoneyBurn`). Steps 1 and 2 (find the logos and make the badges) need no editor and can run as prep at any time.
  - **Needs:** my OK before each logo download, editor + Unreal MCP running, Test for Free with `burn_test` on for the checks. No relay show: in relay mode, `Burn` reads the same `CurProv` that `Deliver` prints for each relay reply.
  - **Touches:** new `Docs/MoneyBurnArt/logo_*.png` and `Content/NHOS/UI/MoneyBurn/T_Logo_*.uasset`, `Content/NHOS/UI/WBP_BurningBill.uasset`, `Content/NHOS/UI/WBP_MoneyBurn.uasset` (`Burn`), `Content/NHOS/Core/BPC_LLMClient.uasset` (`Burn` only), `Docs/MoneyBurnArt.md`, `Docs/Assets.md`, `Graphs/BPC_LLMClient/Burn.txt`, `Graphs/WBP_MoneyBurn/Burn.txt`, new `Graphs/WBP_BurningBill/SetLogo.txt`.
  - **Details:** [Docs/tasks/T36.md](tasks/T36.md)

- [ ] **T37 Error messages say what went wrong, with a joke**
  - **Model and effort:** Opus 5.5, high. It sorts every error path in the client into cases, and adds one note that crosses the client, the show and the banner.
  - **Depends on:** T29 (the banner), T30 (the banner waits for the line queue), T33 (it lays out the key screen and the unavailable screen that show these lines). T21 is done.
  - **Needs:** editor + Unreal MCP running, Test for Free with the new `error_test` switch for the PIE shows, T21's local stub relay for the budget message, and one fake Anthropic key for the key test (no tokens). No relay or key-mode show.
  - **Touches:** new `Content/NHOS/Data/errors.json`, `Content/NHOS/Core/BPC_LLMClient.uasset` (new `ErrorKind` and `ErrorLine`; `ParseReply`, `HandleHttp`, `OnHealth`, `OnKeyTest`, `KeyTestResult`, `SetMode`, `Deliver` and the free-mode path for `error_test`), `Content/NHOS/Core/BP_Show.uasset` (one node that shows the note on the banner), `Content/NHOS/UI/WBP_Stage.uasset` only if the banner needs a longer hold for a note, `Tools/check_prompts.py`, `Docs/switches.example.json`, `Graphs/` files for the graphs it writes.
  - **Details:** [Docs/tasks/T37.md](tasks/T37.md)

- [ ] **T44 The seven film-parody cards in the data files**
  - **Model and effort:** Opus 5.5, high. Story data, the director's notes and the checker's rules change together, and the base prompt changes in the doc first.
  - **Depends on:** T34, T33, T36, T37 (my call on 2026-11-15: the art goes in after the UI tasks), T51 (a note has a category and no decoy)
  - **Needs:** my accept of the Rules tab's two suggested edits and my OK on the Bot Prompts edit, the relay for a `--relay --free` check (no tokens). No editor.
  - **Touches:** `Content/NHOS/Data/scenes.json`, `Content/NHOS/Data/prompts.json`, `Tools/check_prompts.py`, the design doc (Rules and Bot Prompts tabs), `Docs/tasks/T44.md`.
  - **Details:** [Docs/tasks/T44.md](tasks/T44.md)

- [ ] **T45 Each card's props on the prop table**
  - **Model and effort:** Opus 5.5, high. Props become data-driven meshes across the prop actor, the stage director and the state the AIs read.
  - **Depends on:** T44 (the cards' props), T43 (the prop models and their fit)
  - **Needs:** editor + Unreal MCP running, Test for Free for the PIE shows.
  - **Touches:** new `Content/NHOS/Data/props.json`, `Content/NHOS/Stage/BP_Prop.uasset`, `Content/NHOS/Stage/BP_StageDirector.uasset` (`ResetStage`), `Content/NHOS/Core/BP_Show.uasset` (the state's `set.props` at Scene Prep), `Content/NHOS/Maps/L_Stage.umap` (four prop actors), `Content/NHOS/Data/scenes.json`, `Tools/check_prompts.py`, `Graphs/` files for the graphs it writes.
  - **Details:** [Docs/tasks/T45.md](tasks/T45.md)

- [ ] **T46 The two-tone capsule pill bots**
  - **Model and effort:** Opus 5.5, high. A new body for every robot that keeps all of T17's and T19's motion working.
  - **Depends on:** T43 (`M_Clay`), T45 (the lock on `L_Stage`)
  - **Needs:** editor + Unreal MCP running, Test for Free for the PIE shows.
  - **Touches:** `Content/NHOS/Stage/BP_Robot.uasset`, `M_Clay` instances in `Content/NHOS/Stage/Materials/`, `Content/NHOS/Maps/L_Stage.umap` (if the robots must be re-placed), `Graphs/BP_Robot/` files for the graphs it writes.
  - **Details:** [Docs/tasks/T46.md](tasks/T46.md)

- [ ] **T47 A headpiece for each role**
  - **Model and effort:** Opus 5.5, high. Costume data per seat, a new component on the robot and one call at Scene Prep.
  - **Depends on:** T44 (the seats), T46 (the head), T43 (the headpiece models)
  - **Needs:** editor + Unreal MCP running, Test for Free for the PIE shows.
  - **Touches:** `Content/NHOS/Data/scenes.json`, `Content/NHOS/Data/props.json` (or a new `costumes.json`), `Content/NHOS/Stage/BP_Robot.uasset`, `Content/NHOS/Core/BP_Show.uasset` (Scene Prep), `Tools/check_prompts.py`, `Graphs/` files for the graphs it writes.
  - **Details:** [Docs/tasks/T47.md](tasks/T47.md)

- [ ] **T48 The seven painted backdrops**
  - **Model and effort:** Opus 5.5, high. Seven images picked by eye, and a backdrop material that the stage lights don't wash out.
  - **Depends on:** T44 (the backdrop ids), T39 (the tool). Steps 1 and 2 (making and picking the images) need no editor and can run as prep once T44 is done.
  - **Needs:** the Leonardo key in `Local/` and a few dollars of its API credit, editor + Unreal MCP running, Test for Free for the PIE shows.
  - **Touches:** new `Docs/BackdropArt/` and `Docs/BackdropArt.md`, `Docs/Assets.md`, new `Content/NHOS/Stage/Backdrops/`, `Content/NHOS/Stage/Materials/M_Backdrop.uasset`, `Content/NHOS/Stage/BP_Backdrop.uasset`, `Graphs/BP_Backdrop/` files for the graphs it writes.
  - **Details:** [Docs/tasks/T48.md](tasks/T48.md)

- [ ] **T49 The clay opera-house stage**
  - **Model and effort:** Opus 5.5, high. Set dressing and materials across the whole level, framed for the house camera.
  - **Depends on:** T42 and T43 (the set pieces and `M_Clay`), T46 (the audience bots' body and the lock on `L_Stage`)
  - **Needs:** editor + Unreal MCP running, Test for Free for the PIE shows.
  - **Touches:** `Content/NHOS/Maps/L_Stage.umap`, `Content/NHOS/Stage/Materials/` (`M_Set` and its instances), `Content/NHOS/Stage/Set/`, `Docs/tasks/T49.md`.
  - **Details:** [Docs/tasks/T49.md](tasks/T49.md)

- [ ] **T31 Tab completes names, places and props (optional)**
  - **Model and effort:** Sonnet 5.5, medium. Input-box work on a widget that is already laid out.
  - **Depends on:** T27 (the input row), T30 (the lock on `WBP_Stage`)
  - **Needs:** editor + Unreal MCP running, Test for Free for the PIE shows.
  - **Touches:** `Content/NHOS/UI/WBP_Stage.uasset` (the input box's keys and the suggestion row), maybe `Content/NHOS/Core/BP_Show.uasset` (to hand the names, places and props to the widget), `Graphs/` files for the graphs it writes, the design doc.
  - **Details:** [Docs/tasks/T31.md](tasks/T31.md)

- [ ] **T24 Timers (optional)**
  - **Model and effort:** Sonnet 5.5, medium. Small additions to phases that already work.
  - **Depends on:** T19, T30 (the input row and the line queue; it took over this task's AI typing delay on 2026-11-14). First in the cut order.
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
- [x] **T39 Art batch tool and asset list**
  - **Details:** [Docs/tasks/T39.md](tasks/T39.md)
- [x] **T29 The chat holds only chat**
  - **Details:** [Docs/tasks/T29.md](tasks/T29.md)
- [x] **T28 Scene Prep shows the whole card, the scene shows only mine**
  - **Details:** [Docs/tasks/T28.md](tasks/T28.md)
- [x] **T32 UI/UX audit, style guide and shared pieces**
  - **Details:** [Docs/tasks/T32.md](tasks/T32.md)
- [x] **T40 Generate the 13 headpieces**
  - **Details:** [Docs/tasks/T40.md](tasks/T40.md)
- [x] **T56 The bots want to survive, and each has a rival**
  - **Details:** [Docs/tasks/T56.md](tasks/T56.md)
- [x] **T41 Generate the story props**
  - **Details:** [Docs/tasks/T41.md](tasks/T41.md)
- [x] **T33 Fix the title, key entry and end screens**
  - **Details:** [Docs/tasks/T33.md](tasks/T33.md)
- [x] **T42 Generate the opera-house pieces**
  - **Details:** [Docs/tasks/T42.md](tasks/T42.md)
- [x] **T20 Audio**
  - **Details:** [Docs/tasks/T20.md](tasks/T20.md)
- [x] **T30 The lines play one at a time**
  - **Details:** [Docs/tasks/T30.md](tasks/T30.md)
- [x] **T43 Import the generated models and make the clay material**
  - **Details:** [Docs/tasks/T43.md](tasks/T43.md)
- [x] **T51 No decoy note, and every note gets a category**
  - **Details:** [Docs/tasks/T51.md](tasks/T51.md)

## Not planned yet

Ideas that are not tasks yet, and only if time is left after the last open task: a fifth persona (since T26, that is a sixth actor and a fourth scene), more scene cards and more notes. To plan one, add it as a task (see "Changing the plan").