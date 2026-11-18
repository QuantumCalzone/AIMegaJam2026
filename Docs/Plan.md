# Plan: No Humans On Set

The living plan for our game: the tasks in priority order, how to run one and how to add one. The design is in `Docs/Design/`, listed in [GameDesign.md](GameDesign.md). Say **"Next task"** to build the next step.

In this file, "I" and "my" mean the person at the keyboard. "Claude" means the agent doing the task.

**Next up:** "Next task" takes the first free task in "Open", from the top: the new audio and the new art (T101, T96, T97, T99, T102, T103 to T106), where each concept and each pick waits for my approval. T94 set the art direction they follow: `Docs/Art/Direction/README.md`. T95 approved the cast that T96 and T103 build on: `Docs/Art/Cast/README.md`. T98 approved the theater that T99 and T106 build on: `Docs/Art/Set/README.md`. T84, T85 and T61 come next (T90 is done, so the design doc is in `Docs/Design/`), and T34 comes after them in the list; T34 starts with the vote bug that T32 found, and T61 is half built (see its `Waiting:` line). T91 and T92 make `main` the production branch and add the Mac upload.

Keep this paragraph to a few lines: it says what is next, not what was done. What a done task built and found is in its file in `Docs/tasks/`. Until 2026-11-17 this paragraph held a summary of every done task; `git show 05a66dd:Docs/Plan.md` shows it.

## Goal

Finish **No Humans On Set**. The "Open" tasks below are what we know is still to do. I add tasks as the game needs them, and a new task goes wherever it belongs in that list (see "Changing the plan").

**How the plan began.** It started as the plan for an MVP (T01 to T12), which had to answer one question as fast as possible: is it fun to fool an all-AI cast, and do the AIs catch a human at a fair rate (not every time, not never)? The gate (T12, 2026-11-14) said go. I liked it. Since then the plan covers the whole game. Until 2026-11-14 this file was `Docs/MVPPlan.md`. Finished tasks' files and older notes in `Agents/` still use that name. Until 2026-11-14 this file also held every task's full text and a Findings section; since then each task has its own file in `Docs/tasks/` (see "Tasks").

## Cut order

If I decide to cut scope, cut in this order: T38 (speech bubbles; the chat stays as it is now, and T34 polishes that), then T19 to Move and Look only, then T20 to music and three sounds, then T17's robot motion.

## How to run a task

When I say **"Next task"** or **"Next ask"**:

1. `git pull` (if the branch is not on the remote yet, say so and go on). Read `Agents/`. Open this file and run `git lfs locks`. Take the first task in "Open" that is free (see "Claiming a task") and whose **Depends on** tasks are all checked, or wait only for my check (see "When only my check is left"). Then read the task's file, `Docs/tasks/Txx.md` (its **Details** link): it holds the Why, the Steps, the Done-when check and what earlier work found. Read another task's file only when yours points to it.
2. Tell me the task and its recommended model and effort. If this session runs a different model, say so and ask whether to go on.
3. Check its Needs. If something is missing (for example, Unreal MCP is not connected), tell me what to do and stop.
4. Claim the task (see "Claiming a task"). Write a status file, `Agents/status/task-T07.md`, and lock assets as `Agents/README.md` says.
5. Do the work, then run the Done-when check. If the check fails, do not mark the task done: write what blocks it under the task's entry in this file (a `Blocked:` line, never only in the task's file) and tell me. If the only part of the check left is mine (my verdict, my OK on a doc edit, or a run that needs something from me), follow "When only my check is left" instead of step 6.
6. Make one commit that holds the work; the task's entry in this file with its box checked, moved to the end of "Done" and cut down to its title line and its **Details** line; the task's file with the lines cut from the entry (**Model and effort**, **Depends on**, **Needs**, **Touches**) moved to the top of its "## Task" section, the line under its title changed to say the task is done, a **Result:** line at the end of "## Task", and what the task found under "## Findings" at the end of the file; and the updated "Next up" line. Message: `T07: <title>`. Then push it with `git push`. You don't need to ask. If the push is rejected, don't pull or rebase while other sessions have uncommitted work in this folder; tell me.
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

1. **Push the work first.** When the work is built and the Done-when check passes except for the part only I can do, commit and push now. The commit holds the work, its `Graphs/` files, the task's file with what it found so far, a `Waiting:` line under the task's entry in this file (it ends `Left: <what I must do>`) and the "Next up" line. Message: `Txx: <title> (waits for <what>)`. The box stays unchecked.
2. **Free what you hold.** Unlock the assets the task changed, keep the claim, and set the `Editor:` line in your status file to `not using`. Keep the status file: it says what you wait for.
3. **The next task can start.** A task may start when each task in its **Depends on** line is checked, or has its work pushed with a `Waiting:` line that leaves only my check. It builds on that work as pushed.
4. **If my check passes,** make the closing commit as step 6 of "How to run a task" says: check the box, remove the `Waiting:` line, move the entry to "Done", and add the Result and the findings. Message: `Txx: <title> (checked)`. Push it, release the claim and delete the status file.
5. **If my check finds a problem,** the fix goes first in the editor lane, but only once no running session holds the task's assets (`git lfs locks`, `Agents/status/`). Until then, tell me, and wait. When they are free, lock them again, fix the problem, push with the `Waiting:` line kept. Tell me what the fix changed, so that later tasks that built on your work can check it.

## Changing the plan

I add tasks as the game needs them, and a task can go anywhere in the list. Every change to the plan outside a task's own commit is a commit too, `Plan: <what changed>`. One example is a verdict that changes the design.

To add a task:

1. **Number it.** Take the highest number in `Docs/claims/` plus one. A number is only a name: it says nothing about order. Never renumber a task, and never reuse a number.
2. **Place it.** "Open" is in priority order, and "Next task" takes from the top. Two things decide where the task goes:
   - **Architecture:** it goes below every task it builds on, and above the tasks that build on it. Name the first kind in its **Depends on** line, and add it to the **Depends on** line of each task of the second kind.
   - **Priority:** among tasks that don't depend on each other, the one that matters more for the finished game goes higher.
3. **Write it** like the other open tasks, in two places. In this file, under "Open": the title line, then **Model and effort**, **Depends on**, **Needs**, **Touches** and **Details** (a link to its file). In a new file, `Docs/tasks/Txx.md`: a `# Txx Title` heading, the line back to the plan, then "## Task" with **Why** (if there is one), **Steps** and **Done when**. A task fits in one session and one commit, so split a bigger one.
4. **Add its claim file,** `Docs/claims/Txx`, with the same two lines as the other claim files and the new number.
5. **Commit** the plan, the task's file and the claim file together as `Plan: add Txx <title>`. Update "Next up" if the new task changes what is next.

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
- **One provider.** All calls go to the Claude Messages API. The model, effort and token limit for each role (actor, input LLM) are values in `Content/NHOS/Data/llm.json`. T01 and T02 ran `claude-opus-5-5` at low effort. Since 2026-11-13 every role runs `claude-haiku-5-5` at low effort, the cheapest model at its lowest level. Haiku 5.5 has no server-side fallback, so `beta` and `fallbacks` in `llm.json` are empty; a refusal comes back as `stop_reason: "refusal"`.
- **One provider per persona, from T16 and T18 on.** Each persona runs on its own provider, as in the design's table, with a key per provider (no router). T16 sets up the prompts and the keys; T18 makes the game call them. Since 2026-11-14 each bot goes by its provider's name on screen, in the log and in the cast list the AIs read (OpenAI, Anthropic, SpaceXAI, Meta: the `name` fields in `personas.json`), not by a persona name such as "The Worrier". Persona ids (`worrier`) stay as they are in files and `NHOS:` lines. Real people's names and product names stay out of prompts and off the screen.
- **The design doc follows the game.** The design doc is the Markdown files in `Docs/Design/`, one per part, listed in [GameDesign.md](GameDesign.md), and they are the only source of truth for the design. When a task changes the design (the speech style, the sets, the providers), it shows me the matching edit to the file, and after my OK it makes the edit in the task's commit. A prompt changes in `Docs/Design/BotPrompts.md` first, then word for word in `prompts.json` or `personas.json`. No script checks the two against each other. Until T90 (2026-11-17) the design was a private Claude Doc; task files from before then call the files "tabs" and may name that doc's node ids and revisions.
- **Legibility first.** Everything an AI says reads like a normal chat, the way Claude or ChatGPT write: plain sentences, no brackets or tags, no beeps or sound effects, no emoji, no ALL-CAPS words. Each persona's personality comes through what it says, not how it is typed.
- **Outside and generated assets.** Record every art, audio or font asset in `Docs/Assets.md` when you add it: what it is, where it came from (a Fab link, a site, or the AI tool and prompt) and its license.
- **One reply shape.** Every ask (scene turn, Free Talk line, vote, reaction, closing line, input conversion) gets back the same small JSON object, with unused fields empty. One parser serves the whole game.
- **The shared log** is what the AIs read. Every actor's lines have the same form, human or AI. It never holds my raw input, times, errors or anyone's note. Game messages reach the AIs in a separate field that actors can't write to.
- **Check lines.** Anything a Done-when check reads is printed with the prefix `NHOS:` to the editor log (`Saved/Logs/AIMegaJam2026.log`). It never goes in the shared log.
- **Autoplay.** From T07 on, a local switch makes the human seat play canned lines, so an agent can run a whole show unattended and read the result in the log. The switch file is `Local/switches.json` (copy `Docs/switches.example.json`), with `"autoplay": true`. The canned lines are in `Content/NHOS/Data/autoplay.json`, one list per phase, and they go through the input LLM like typed lines. Later switches (such as T09's `force_tie`) go in the same file. Set autoplay back to `false` before a person plays.
- **Unreal MCP.** Do editor work through Unreal MCP. One call at a time, each short enough that the client doesn't stop waiting. Split long work, and save after each step. Write graphs with `BlueprintTools.write_graph_dsl`, and batch calls with `ProgrammaticToolset.execute_tool_script`. Read "T01: spike results" in [Docs/tasks/T01.md](tasks/T01.md) first: it lists the DSL rules that cost time to find. Later tasks' files add more, each under "Unreal MCP rules found in this task". MCP can't create a level, so a person makes new levels in the editor (File > New Level > Empty Level).
- **Read only the graphs you need.** List a Blueprint's graphs, then read only the ones the task changes or calls. Never dump every graph of `BP_Show`: a full dump in T18 and T26 was a very large read, and one was too big for a tool result.
- **Graph sources live in `Graphs/`.** `Graphs/<Blueprint>/<Graph>.txt` holds the DSL source last written to each graph, one file per graph, as written (shorthand, before `Tools/dslpp.py`). To change a graph, start from its file and push it. If it has no file yet, read the graph from the editor and write your source from that. Commit the updated files with the task. A read-back is for reading only, because writing one back drops data (T06). If you change a graph some other way, like a pin value or a hand edit in the editor, make the same change in its file, or delete the file. The per-task copies in `Saved/Txx/src/` from before 2026-11-14 may be out of date.
- **The DSL's else trap.** In `write_graph_dsl`, code after an `if` whose body ends in a branching node (`Utilities|IsValid`, or any node written with `(:"...")` exec branches) becomes that `if`'s else path, as code after an `if` that ends in `return` does (T01). T77's `StageLine` broke this way and no line's action played until T87. Put such a branch in a function of its own and call it, or put it where no code follows it. `python Tools/check_prompts.py --offline` (or `python Tools/check_graphs.py`) fails a source in `Graphs/` written that way (T107): run it before you push a graph.
- **Worktrees, for sessions that don't need the editor.** The editor has the repo folder open, so a session that drives the editor or runs PIE works there. A session that doesn't need the editor may work in its own git worktree, on its own branch, when its files could clash with another session's uncommitted work in the repo folder (for example `Content/NHOS/Data/*.json` or `Docs/`).
  - Never change a `.uasset` or `.umap` in a worktree, because binary assets can't be merged.
  - A worktree has no `Local/` folder, and nothing gets copied into it, the key file least of all. Run `Tools/check_prompts.py` there with `--offline`, `--free` or `--relay`. A run that calls the providers with direct keys waits until after the merge, in the repo folder.
  - When the work is committed, merge `dev` into your branch and fix any conflicts there. Then merge your branch into the repo folder with `git -C <repo folder> merge --no-ff <branch>`, and push. If that merge stops because it would overwrite uncommitted changes in the repo folder, leave it and tell me.
- **New systems get their own Blueprint.** Put new logic in a new Blueprint or component, or in the actor it belongs to (such as `BP_Robot`), and have `BP_Show` call it from one node. Every editor task so far has needed the `BP_Show` lock.
- **Claude does the playing; I don't playtest (since 2026-11-15).** No task waits for me to play, and no session asks me to. Where a check needs a show played, Claude plays it: one show by hand in PIE (Test for Free, a 1600 × 900 floating window, clicks and typing through the Slate inspector, autoplay off) with a screenshot of each phase the task changed, and a free autoplay show in a game window on the saved assets that reaches `SHOW END`. Claude judges what my playtest used to judge (can I read it, can I follow it, does the screen feel blocked, does it look finished) from those screenshots, as a critical first-time player would, and writes what it saw under "## Findings". What screenshots can't show (sound, for example) is written there as unchecked, and the task still closes. Set `autoplay` back to false and close each game window when done. T27's findings in [Docs/tasks/T27.md](tasks/T27.md) have the Mac command, the Mac log paths and how to screenshot a game window.
- **Each task leaves the game runnable.** One task = one session = one commit (two when it waits for my check).

## Tasks

"Open" holds the tasks still to do, in priority order: "Next task" takes the first free one from the top. Where an entry says a task belongs to the chain machine or the non-chain machine, that matters only while the two-machine setup is active (see "Two machines at once" in `CLAUDE.md`). A new task goes wherever it belongs in that order, so the numbers are not in order. "Done" holds the finished tasks, oldest first. When a task's box is checked, its entry moves to the end of "Done" (see "How to run a task", step 6). Each entry links its file in `Docs/tasks/`, which holds the task's Why, Steps, Done-when check, Result and findings.

### Open



- [ ] **T101 New audio, part 2: the show and robot sounds, the clicks and the bots' voices, picked by me**
  - **Model and effort:** Opus 5.5, high. About twenty sounds and four voice sets, judged by me alone, with T72's and T73's rules for the voices.
  - **Depends on:** T94 (the sounds fit its direction), T72 and T73 (how a voice syllable is made and played; done). It needs no editor and changes no asset, so it can run on either machine, beside the chain.
  - **Needs:** my answer on the sources; my pick for each sound and each voice set, on a private Artifact page; my OK on the terms and cost, and my own sign-up, if an AI sound service is used.
  - **Touches:** `SourceAssets/Audio/Show/`, `Robot/`, `UI/` and `Voice/<provider>/` (the picks; never `Voice/Me`), `Tools/make_voices.py` if it makes the new sets, `Docs/AudioShortlist.md`, `Docs/tasks/T101.md`; outside the repo: `Local/audio/candidates/` and a private Artifact page.
  - **Details:** [Docs/tasks/T101.md](tasks/T101.md)

- [ ] **T96 New art, part 3: concepts for a costume for each role, fitted to every character, approved by me**
  - **Model and effort:** Opus 5.5, high. A costume for every role, each drawn on all five approved characters, with a version made for my cube head.
  - **Depends on:** T95 (the approved characters, whose heads the costumes fit). It needs no editor and changes no asset, so it can run on either machine, beside the chain.
  - **Needs:** `Local/leonardo_key.json`; my OK on the estimated cost before the first paid call; my pick for each costume and my approval of each fit sheet; my OK on the design doc edit.
  - **Touches:** new `Docs/Art/Costumes/` (with the role table that T104 writes the data from), the design doc's Art Inspiration tab (Costumes), `Docs/tasks/T96.md`.
  - **Details:** [Docs/tasks/T96.md](tasks/T96.md)

- [ ] **T97 New art, part 4: concepts for the story props, approved by me**
  - **Model and effort:** Opus 5.5, high. 28 props, approved card by card as sets, each with a clean view and its size for image-to-3D.
  - **Depends on:** T94 (the direction and the style guide). It needs no editor and changes no asset, so it can run on either machine, beside the chain.
  - **Needs:** `Local/leonardo_key.json`; my OK on the estimated cost before the first paid call; my approval of each prop and each card's set; my OK on the design doc edit.
  - **Touches:** new `Docs/Art/Props/`, the design doc's Art Inspiration tab (props) and Stories tab (the props strips), `Docs/tasks/T97.md`.
  - **Details:** [Docs/tasks/T97.md](tasks/T97.md)

- [ ] **T99 New art, part 6: the backdrops, the stagehand's portrait and the burning bills, approved by me and imported**
  - **Model and effort:** Sonnet 5.5, medium. 2D art where the approved image is the final one, reimported over textures that keep their names.
  - **Depends on:** T94 (the direction), T98 (the approved house, which the backdrops sit in); T35, T36, T48 and T61 (the textures it replaces; done). It doesn't change `BP_Show` or `WBP_Stage`, so it belongs to the non-chain machine.
  - **Needs:** editor + Unreal MCP running, Test for Free for a PIE show, `Local/leonardo_key.json`, my OK on the estimated cost before the first paid call, my pick of every image, my OK on the design doc edit.
  - **Touches:** `Content/NHOS/Stage/Backdrops/T_Backdrop_*.uasset`, `Content/NHOS/UI/Stagehand/T_Stagehand_Portrait.uasset`, `Content/NHOS/UI/MoneyBurn/T_*.uasset`, new `Docs/Art/2D/`, `Docs/Assets.md`, the design doc, `Docs/tasks/T99.md`.
  - **Details:** [Docs/tasks/T99.md](tasks/T99.md)

- [ ] **T102 New audio, part 3: import the picks and set a quieter mix**
  - **Model and effort:** Opus 5.5, high. Measured loudness, a mix set without hearing it, and recordings of each phase for my OK.
  - **Depends on:** T100 and T101 (the picks); T20 and T71 (`BPC_ShowAudio` and the sound classes; done). It changes one pin in `BP_Show`'s `OpenPrep`, so that Scene Prep plays its own loop (my call on 2026-11-17). So while the two-machine setup is active, it belongs to the chain machine.
  - **Needs:** editor + Unreal MCP running, a free autoplay show in a game window for the recordings, my OK on the mix from those recordings.
  - **Touches:** `Content/NHOS/Audio/**` (reimports, three new music loops, and deletes of sounds T101 left out), `Content/NHOS/Audio/SC_Music.uasset`, `SC_Effects.uasset` and `SC_Voice.uasset`, `Content/NHOS/Core/BPC_ShowAudio.uasset` (levels, ducking, and the three new music keys in `PhaseKey` and `TrackFor`), `Graphs/BPC_ShowAudio/` files for the graphs it writes, `Content/NHOS/Core/BP_Show.uasset` (one pin in `OpenPrep`), `Graphs/BP_Show/OpenPrep.txt`, `Docs/Assets.md`, `Docs/AudioShortlist.md`, `Docs/ItchPage.md` (credits), `Docs/tasks/T102.md`.
  - **Details:** [Docs/tasks/T102.md](tasks/T102.md)

- [ ] **T108 Meta's seat color becomes mustard, in the UI and on the robot**
  - **Model and effort:** Sonnet 5.5, medium. One color value in each of two Blueprints, the docs that list the seat colors, and a free PIE check.
  - **Depends on:** T95 (my pick of mustard for Meta; done). It doesn't change `BP_Show` or `WBP_Stage`, so it belongs to the non-chain machine. It locks `BP_Robot.uasset`, as T103 does, so the two never run at once.
  - **Needs:** editor + Unreal MCP running, Test for Free for the PIE check, my pick of the exact hex, my OK on the design doc and style guide edits.
  - **Touches:** `Content/NHOS/UI/Style/UIStyle.uasset` (`SeatColor`), `Content/NHOS/Stage/BP_Robot.uasset` (`SetPersona`), any other asset that holds Meta's blue, `Graphs/UIStyle/SeatColor.txt`, `Graphs/BP_Robot/SetPersona.txt`, `Docs/Design/ArtInspiration.md` (the bots table and the UI section's palette), `Docs/Art/Direction/README.md` (the palette), `Docs/tasks/T108.md`.
  - **Details:** [Docs/tasks/T108.md](tasks/T108.md)

- [ ] **T103 New art, part 7: the cast's models, generated from the approved concepts**
  - **Model and effort:** Opus 5.5, high. Five robots generated and swapped into `BP_Robot`, keeping the sockets, the face and every hook the show uses.
  - **Depends on:** T95 (the approved turnarounds); T75, T82 and T83 (the face, `M_CastModel` and the last swap; done). It doesn't change `BP_Show` or `WBP_Stage`, so it belongs to the non-chain machine. Run it where its generator is: Hyper3D's MCP server is on the Mac, and the PC has the Meshy key.
  - **Needs:** editor + Unreal MCP running, Test for Free for the PIE shows, Hyper3D (the Mac's MCP server, or an API key I put in `Local/`) or Meshy (`Local/meshy_key.json`), my OK on the estimated cost before the first paid call, my OK on the models against the concepts.
  - **Touches:** `Content/NHOS/Stage/Cast/**`, `Content/NHOS/Stage/BP_Robot.uasset`, `Content/NHOS/Stage/Materials/` if the cast needs a new material, `Content/NHOS/Maps/L_Stage.umap` only if the robots' places must move, `Content/NHOS/Data/costumes.json` (`on`) only if needed, `Docs/Art/Cast/` (models and logs), `Docs/Assets.md`, `Graphs/BP_Robot/` files for the graphs it writes, `Docs/tasks/T103.md`.
  - **Details:** [Docs/tasks/T103.md](tasks/T103.md)

- [ ] **T104 New art, part 8: the costumes' models, fitted to every character**
  - **Model and effort:** Opus 5.5, high. A model per costume version, a fit per character in a new `costumes.json`, and a test switch to check every costume on every robot.
  - **Depends on:** T96 (the approved costumes and role table), T103 (the new heads and sockets); T47 (how the robots dress; done). It doesn't change `BP_Show` or `WBP_Stage`, so it belongs to the non-chain machine.
  - **Needs:** editor + Unreal MCP running, Test for Free for the PIE shows, Meshy (`Local/meshy_key.json`) or Hyper3D (the Mac's MCP server, or an API key I put in `Local/`), my OK on the estimated cost before the first paid call, my OK on the models and on the final fit grid, my OK on the design doc edit.
  - **Touches:** new `Content/NHOS/Stage/Costumes/`, `Content/NHOS/Stage/Headpieces/` (deleted), `Content/NHOS/Stage/BP_Robot.uasset` (`SetHeadpiece`, `DressFromShow`, attach points, `costume_test`), `Content/NHOS/Data/costumes.json`, `Content/NHOS/Data/scenes.json` (each seat's costume), `Tools/check_prompts.py` if it checks costumes, `Docs/switches.example.json`, `Docs/Art/Costumes/` (models and logs), `Docs/Assets.md`, the design doc, `Graphs/BP_Robot/` files for the graphs it writes, `Docs/tasks/T104.md`.
  - **Details:** [Docs/tasks/T104.md](tasks/T104.md)

- [ ] **T105 New art, part 9: the story props' models, generated from the approved concepts**
  - **Model and effort:** Sonnet 5.5, medium. 28 image-to-3D props, scaled to their sizes, on the pattern T41 and T43 set.
  - **Depends on:** T97 (the approved props, with views and sizes); T45 and T62 (the prop table, and grab, throw and give; done). It doesn't change `BP_Show` or `WBP_Stage`, so it belongs to the non-chain machine.
  - **Needs:** editor + Unreal MCP running, Test for Free for the PIE shows, Meshy (`Local/meshy_key.json`) or Hyper3D, my OK on the estimated cost before the first paid call (about 840 Meshy credits), my OK on each card's models.
  - **Touches:** `Content/NHOS/Stage/Props/**`, `Content/NHOS/Data/props.json`, `Content/NHOS/Stage/BP_Prop.uasset` only if it must change, new `Docs/Art/Props/manifest.json`, `Docs/Art/Props/` (models and logs), `Docs/Assets.md`, `Graphs/BP_Prop/` files if it writes any, `Docs/tasks/T105.md`.
  - **Details:** [Docs/tasks/T105.md](tasks/T105.md)

- [ ] **T106 New art, part 10: the theater, its set pieces and the audience, built from the approved concepts**
  - **Model and effort:** Opus 5.5, high. A rebuild of `L_Stage`'s house that keeps the camera's frame, the places, the prop table, the backdrop flat and the near rows' lighting.
  - **Depends on:** T98 (the approved house and pieces), T99 (the new backdrops on the flat); T49 and T86 (the house as it is; done). It doesn't change `BP_Show` or `WBP_Stage`, so it belongs to the non-chain machine.
  - **Needs:** editor + Unreal MCP running, Test for Free for the PIE shows, Meshy (`Local/meshy_key.json`) or Hyper3D, my OK on the estimated cost before the first paid call, my OK on the models and on the house screenshots, my OK on the design doc edit.
  - **Touches:** `Content/NHOS/Maps/L_Stage.umap`, `Content/NHOS/Stage/Set/**` (with `BP_AudienceBot`), `Content/NHOS/Stage/Materials/**`, `Content/NHOS/Stage/BP_Backdrop.uasset` only if the flat changes, `Docs/Art/Set/` (models and logs), `Docs/Assets.md`, the design doc, `Docs/tasks/T106.md`.
  - **Details:** [Docs/tasks/T106.md](tasks/T106.md)

- [ ] **T84 Scene Prep shows the scene and Start the scene in the middle**
  - **Model and effort:** Opus 5.5, high. A layout change across Scene Prep's widgets, judged from screenshots at two sizes.
  - **Depends on:** T38 (the chat hidden at each show's start and its Show chat button: this task decides what the lower panel shows in scene 1's Scene Prep; if T38 is cut, take it off this line), T78 (the lower panel's width, which the middle panel must clear in scenes 2 on), T88 (the clue rows in the card's note box, and `PrepPrompt`'s turn line), T90 (its design doc edit goes in the files in `Docs/Design/`)
  - **Needs:** editor + Unreal MCP running, Test for Free for the PIE shows, my OK on the design doc edit.
  - **Touches:** `Content/NHOS/UI/WBP_Stage.uasset` (a new prep panel with `PrepBox`'s scene and stage parts, `StartButton` moved into it, the lower panel hidden in scene 1's Scene Prep, `SetPrepMode`), `Content/NHOS/Core/BP_Show.uasset` (`PrepPrompt`'s turn line), `Graphs/WBP_Stage/SetPrepMode.txt`, `Graphs/BP_Show/PrepPrompt.txt`, `Docs/tasks/T32.md` (row 13), `Docs/tasks/T84.md`.
  - **Details:** [Docs/tasks/T84.md](tasks/T84.md)

- [ ] **T85 The cast's roles and wants show when I point at a robot**
  - **Model and effort:** Opus 5.5, high. A new hover card placed over moving robots, a screen test each frame, and the robots named from scene 1's Scene Prep on.
  - **Depends on:** T84 (the card without the scene, and the middle panel the hover card must keep clear of), T38 (the bubbles ride on the name tags the hover card sits beside; if T38 is cut, take it off this line), T83 (the cast's final models, whose size sets the hover area), T90 (its design doc edit goes in the files in `Docs/Design/`)
  - **Needs:** editor + Unreal MCP running, Test for Free for the PIE shows, computer use on the PIE window or the test switch in T85.md to show a card, my OK on the design doc edit.
  - **Touches:** new `Content/NHOS/UI/WBP_CastTip.uasset`, `Content/NHOS/UI/WBP_Stage.uasset` (the hover test, the cast off the card), `Content/NHOS/Core/BP_Show.uasset` (the names in scene 1's Scene Prep, `PrepPrompt`'s hint, the cast data if the card needs it), `Content/NHOS/Stage/BP_Robot.uasset` only if the names or the hover need it, `Docs/switches.example.json` if the test switch is added, `Graphs/` files for the graphs it writes, `Docs/tasks/T85.md`.
  - **Details:** [Docs/tasks/T85.md](tasks/T85.md)

- [ ] **T34 Fix the in-show screen**
  - **Model and effort:** Opus 5.5, high. Hierarchy and state judgment on the busiest screen.
  - **Depends on:** T32, T30, T38 (the line pacing, its typing line, the speech bubbles and the chat button are in, so this task polishes the final screen). If T38 is cut, take it off this line. Also T50, T53, T57 (the note category on my card, the clapperboard and the "passed" marker are on the screen it polishes), and T64, T65, T66, T78 (the action builder, the preview line, the speech field, the timer and the emotion chip are in the input row it polishes), and T73 (the lines type out on the screen it polishes), and T84, T85 (Scene Prep's middle panel and the cast's hover cards; they settle T34-build's 2.9 and the names in Scene Prep from its 2.1), and T87 (the reactions to a win play on the screen it polishes), and T88 (each scene's clue on my card), and T107 (the banner timing: T34-build's `NextBanner` rewrite in 2.6 starts from T107's version and keeps what T107's findings say it must).
  - **Needs:** editor + Unreal MCP running, Test for Free for the PIE shows.
  - **Touches:** `Content/NHOS/UI/WBP_Stage.uasset`, `WBP_SpeechBubble.uasset`, `WBP_ChatLine.uasset` and `WBP_MoneyBurn.uasset` if T32 left a row for either, `Content/NHOS/Core/BP_Show.uasset` only if a widget's call must change (for example `SetPrompt`), `Graphs/WBP_Stage/` files, `Docs/tasks/T34.md` and the audit table in `Docs/tasks/T32.md`.
  - **Details:** [Docs/tasks/T34.md](tasks/T34.md)

- [ ] **T61 Stagehand onboarding: earpiece tips, a tips toggle and How to play**
  - **Model and effort:** Opus 5.5, high. A new system with its own data file, component and widgets, called from the show at eight moments.
  - **Depends on:** T33 (the title screen), T34 (the in-show screen), T84 (the middle panel now sits about where the earpiece's Scene Prep spot was; T84's findings say where it can go), T50, T52, T53, T57, T58, T62, T66 (the rules its lines teach, how I take a turn among them), T60 (the lose and win screens it speaks on), T88 (the clue that its scene 1 line names), T90 (its palette row goes in `Docs/Design/ArtInspiration.md`), T93 (the title's Play button, next to which the How to play button and the tips toggle go)
  - **Needs:** editor + Unreal MCP running, Test for Free for the PIE shows.
  - **Touches:** new `Content/NHOS/Data/stagehand.json`, new `Content/NHOS/Core/BPC_Stagehand.uasset`, new `Content/NHOS/UI/WBP_Earpiece.uasset` and `WBP_HowToPlay.uasset`, `Content/NHOS/UI/WBP_Title.uasset` (the How to play button and the tips toggle), `Content/NHOS/UI/WBP_Stage.uasset` (the earpiece's place), `Content/NHOS/Core/BP_Show.uasset` (one call per moment), a new file in `Local/` for the first-show flag, new `Content/NHOS/UI/Stagehand/T_Stagehand_Portrait.uasset` with `Docs/StagehandArt/` and a row in `Docs/Assets.md` (the portrait), `Tools/check_prompts.py`, `Docs/ItchPage.md`, `Graphs/` files for the graphs it writes, `Docs/tasks/T61.md`.
  - **Details:** [Docs/tasks/T61.md](tasks/T61.md)
  - **Waiting:** the Mac built and pushed T61's new pieces (see "Part 1" in T61.md): `Content/NHOS/Data/stagehand.json`, `BPC_Stagehand` (`BeginShow`, `Say(Key)`, `EndShow(Win, Reason)`, `TipsNext`, `SetTipsNext(On)`), `WBP_Earpiece` (now with the friendly AI stagehand's portrait, `Content/NHOS/UI/Stagehand/T_Stagehand_Portrait`, on my call) and `WBP_HowToPlay` (`OpenOver(InBack)`, the six bullets I OKed). The Rules tab now calls the stagehand a friendly AI (rev 48). The claim stays for the PC's session. Left: the PC's chain adds the calls in BP_Show, the earpiece's place in WBP_Stage, the button and toggle on WBP_Title, the checker and itch page lines, then the full check

- [ ] **T91 main becomes the production branch, and the itch.io menu ships main**
  - **Model and effort:** Opus 5.5, high. Rules that every session follows change, the editor menu's upload moves to `main`, and GitHub protects `main`. A mistake here can ship from the wrong branch or let an agent push `main`.
  - **Depends on:** T89 (`Tools/deploy_itch.py`, the Tools > itch.io menu, the `windows` channel). Run it on the PC. It needs the editor only to check the menu and changes no asset, so it can run beside the chain.
  - **Needs:** T89 done; my answer on how a release merges into `main` (a pull request I merge, or a push on my word); my OK to change `main`'s protection settings on GitHub; my word for the first release.
  - **Touches:** `Tools/deploy_itch.py` (the default commit: `origin/main`), `Content/Python/nhos_itch_deploy.py` (the dialog, a dry run of `dev`), `CLAUDE.md` (the top section, "When a task is done", "Source control", "Deploys to itch.io" and its full text in `Docs/Builds.md`, a new "Releases" section), `README.md`, `Agents/README.md`, `Docs/LaunchAgents.md`, `Docs/TwoMachines.md`, `Docs/tasks/T91.md`; outside the repo: `main`'s protection on GitHub, the branch `main` (the first release), my memory notes about `main`.
  - **Details:** [Docs/tasks/T91.md](tasks/T91.md)

- [ ] **T92 The Mac builds and uploads the Mac file from the editor menu**
  - **Model and effort:** Opus 5.5, high. A sandboxed, ad hoc signed app whose signature must survive the push and the download, code written on the PC that never ran on a Mac, and the secrets check as the gate.
  - **Depends on:** T89 (the deploy script's Mac path, the secrets check's `--local`, the menu), T91 (the menu ships `main`'s tip). Run it on the Mac, in the editor for the menu's check.
  - **Needs:** the Mac with UE 5.8.4 and Xcode; butler there (the itch app's copy, or my OK to download it) and my own `butler login`; my OK before the hidden `mac` file is shown.
  - **Touches:** `Tools/deploy_itch.py` (the Mac path, a `codesign` gate, a Mac default deploy worktree), `Content/Python/nhos_itch_deploy.py` (the Mac launch), `Docs/Builds.md` ("Package a macOS build", "Deploys to itch.io") and the short "Deploys to itch.io" in `CLAUDE.md`, `README.md`, `Docs/ItchPage.md` (the Uploads row), `Docs/tasks/T92.md`; outside the repo: butler and the deploy worktree on the Mac. The itch.io page gets one new file, from the channel `mac`. The jam's file stays as it is.
  - **Details:** [Docs/tasks/T92.md](tasks/T92.md)

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
- [x] **T46 The two-tone capsule pill bots**
  - **Details:** [Docs/tasks/T46.md](tasks/T46.md)
- [x] **T50 Only the bots get the director's note**
  - **Details:** [Docs/tasks/T50.md](tasks/T50.md)
- [x] **T59 Every line is capped at 15 words, mine too**
  - **Details:** [Docs/tasks/T59.md](tasks/T59.md)
- [x] **T49 The clay opera-house stage**
  - **Details:** [Docs/tasks/T49.md](tasks/T49.md)
- [x] **T53 Scene clock: one scene fewer than the cast, on a clapperboard**
  - **Details:** [Docs/tasks/T53.md](tasks/T53.md)
- [x] **T36 Each burning bill shows the logo of the provider it paid**
  - **Details:** [Docs/tasks/T36.md](tasks/T36.md)
- [x] **T52 A tie cuts nobody**
  - **Details:** [Docs/tasks/T52.md](tasks/T52.md)
- [x] **T44 The seven film-parody cards in the data files**
  - **Details:** [Docs/tasks/T44.md](tasks/T44.md)
- [x] **T37 Error messages say what went wrong, with a joke**
  - **Details:** [Docs/tasks/T37.md](tasks/T37.md)
- [x] **T54 New win condition: the final two, or on stage when the last scene ends**
  - **Details:** [Docs/tasks/T54.md](tasks/T54.md)
- [x] **T55 Remove the Director AI**
  - **Details:** [Docs/tasks/T55.md](tasks/T55.md)
- [x] **T48 The seven painted backdrops**
  - **Details:** [Docs/tasks/T48.md](tasks/T48.md)
- [x] **T45 Each card's props on the prop table**
  - **Details:** [Docs/tasks/T45.md](tasks/T45.md)
- [x] **T72 A voice for each robot, and mine: the syllable sounds**
  - **Details:** [Docs/tasks/T72.md](tasks/T72.md)
- [x] **T57 Silence and polish are tells: a pass shows as "passed"**
  - **Details:** [Docs/tasks/T57.md](tasks/T57.md)
- [x] **T67 Analytics, part 1: the relay takes events and reports them**
  - **Details:** [Docs/tasks/T67.md](tasks/T67.md)
- [x] **T71 Music for each place and each scene**
  - **Details:** [Docs/tasks/T71.md](tasks/T71.md)
- [x] **T73 Lines type out, one voice sound per syllable**
  - **Details:** [Docs/tasks/T73.md](tasks/T73.md)
- [x] **T79 The new cast, part 1: one round head and three bodies**
  - **Details:** [Docs/tasks/T79.md](tasks/T79.md)
- [x] **T58 Last word: a reply for anyone @-mentioned in the final round**
  - **Details:** [Docs/tasks/T58.md](tasks/T58.md)
- [x] **T80 The new cast, part 2: Meta's android and my cardboard costume**
  - **Details:** [Docs/tasks/T80.md](tasks/T80.md)
- [x] **T47 A headpiece for each role**
  - **Details:** [Docs/tasks/T47.md](tasks/T47.md)
- [x] **T62 One rule set for every action, mine and the AIs'**
  - **Details:** [Docs/tasks/T62.md](tasks/T62.md)
- [x] **T63 My turn sends a built action and a spoken line**
  - **Details:** [Docs/tasks/T63.md](tasks/T63.md)
- [x] **T81 The cast in Hyper3D, part 1: generate the models from the concept art**
  - **Details:** [Docs/tasks/T81.md](tasks/T81.md)

- [x] **T75 Each robot can show an emotion: its face and a gesture**
  - **Details:** [Docs/tasks/T75.md](tasks/T75.md)
- [x] **T82 The cast in Hyper3D, part 2: the round-head bots get their models**
  - **Details:** [Docs/tasks/T82.md](tasks/T82.md)
- [x] **T60 Win and lose screens: the reasoning, the top reason and the rivals**
  - **Details:** [Docs/tasks/T60.md](tasks/T60.md)
- [x] **T83 The cast in Hyper3D, part 3: Meta and my costume get their models**
  - **Details:** [Docs/tasks/T83.md](tasks/T83.md)
- [x] **T64 The action builder, the preview line and Action!**
  - **Details:** [Docs/tasks/T64.md](tasks/T64.md)
- [x] **T65 The speech field: a word counter, focus and @ mentions**
  - **Details:** [Docs/tasks/T65.md](tasks/T65.md)
- [x] **T68 Analytics, part 2: the game sends its events**
  - **Details:** [Docs/tasks/T68.md](tasks/T68.md)
- [x] **T76 The bots send an emotion with every reply**
  - **Details:** [Docs/tasks/T76.md](tasks/T76.md)
- [x] **T69 Analytics, part 3: the actions players try that the game can't do**
  - **Details:** [Docs/tasks/T69.md](tasks/T69.md)
- [x] **T66 The turn timer, the auto-send and the other phases**
  - **Details:** [Docs/tasks/T66.md](tasks/T66.md)
- [x] **T77 Each robot shows its emotion as its line plays, mine too**
  - **Details:** [Docs/tasks/T77.md](tasks/T77.md)
- [x] **T38 Every line plays in a speech bubble, and the chat opens on a click (optional)**
  - **Details:** [Docs/tasks/T38.md](tasks/T38.md)
- [x] **T86 A full house: more rows of audience at the bottom of the screen**
  - **Details:** [Docs/tasks/T86.md](tasks/T86.md)
- [x] **T78 I can pick my robot's emotion**
  - **Details:** [Docs/tasks/T78.md](tasks/T78.md)
- [x] **T88 The director's note clue changes each scene**
  - **Details:** [Docs/tasks/T88.md](tasks/T88.md)
- [x] **T89 Builds go to itch.io with butler from an editor menu**
  - **Details:** [Docs/tasks/T89.md](tasks/T89.md)
- [x] **T100 New audio, part 1: music that fits each scene and sits in the background, picked by me**
  - **Details:** [Docs/tasks/T100.md](tasks/T100.md)
- [x] **T93 The title's Play button replaces Play via Relay and is greyed out when fewer than three AIs work**
  - **Details:** [Docs/tasks/T93.md](tasks/T93.md)
- [x] **T90 The design doc moves into the repo as Markdown files**
  - **Details:** [Docs/tasks/T90.md](tasks/T90.md)

- [x] **T94 New art, part 1: the art direction, approved by me**
  - **Details:** [Docs/tasks/T94.md](tasks/T94.md)
- [x] **T87 When I win, every AI reacts to the reveal, the cut ones too**
  - **Details:** [Docs/tasks/T87.md](tasks/T87.md)
- [x] **T107 Fix the bugs T87 found: late banners, a robot hidden at the Back mark, and three small ones**
  - **Details:** [Docs/tasks/T107.md](tasks/T107.md)

- [x] **T95 New art, part 2: concepts for the cast, me included, approved by me**
  - **Details:** [Docs/tasks/T95.md](tasks/T95.md)

- [x] **T98 New art, part 5: concepts for the theater, its set pieces and the audience, approved by me**
  - **Details:** [Docs/tasks/T98.md](tasks/T98.md)

## Not planned yet

Ideas that are not tasks yet, and only if time is left after the last open task: a fifth persona (since T26, that is a sixth actor and a fourth scene), more scene cards and more notes, and from my input spec (`Docs/tasks/T62.md`): clicking a prop, a place or an actor on the stage to fill the builder's target, and number keys 1 to 7 to pick an action. To plan one, add it as a task (see "Changing the plan").
