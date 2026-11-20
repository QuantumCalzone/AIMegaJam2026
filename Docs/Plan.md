# Plan: No Humans On Set

The living plan for our game: the tasks in priority order, how to run one and how to add one. The design is in `Docs/Design/`, listed in [GameDesign.md](GameDesign.md). Say **"Next task"** to build the next step.

In this file, "I" and "my" mean the person at the keyboard. "Claude" means the agent doing the task.

**Next up:** "Next task" takes the first free task in "Open", from the top: T118 (either machine with the editor) hides the title's Play stats button and counts players who had turned stats off again. T119 (either machine with the editor) makes the three glow props glow in the packaged game, where they show the default gray material now. T121 (either machine, no editor) has me pick a costume idea for each of the 8 roles that play bare-headed since my costume pass of 2026-11-19 (a costume goes only on roles where it fits the story), T129 (either machine, no editor) draws them, and T122 (either machine with the editor) makes their models and dresses those seats. T113 (the PC) makes the itch.io page's cover, screenshots and trailer once the art updates are in. T120 (the Mac, with the editor) makes the Mac game remember a player's keys and the stagehand's first show. T116 (the PC, with the editor) makes every event from my own machines a test event, in any build. T117 (either machine) puts a live dashboard of the prod play stats on the relay; it goes live with the next release. T112 tried the stage on the mobile renderer (2026-11-20; `Docs/Mobile/README.md`): it reads well on the Android Vulkan and ES 3.1 previews, with darker stalls, no robot shadows and touch joysticks to fix. My verdict: no Android release; web builds are a go, planned as T123 to T128, which start when Epic ships the full UE 5.9 release: T123 tries the web target in a 5.9 copy, then T124 opens the relay to the web build (CORS), T125 gives the stage a mobile look, T126 cuts its triangles, T127 makes the game's files and modes work in a browser, and T128 puts the web build on itch.io. T111 made each build tell analytics which release it is (2026-11-20): `Tools/deploy_itch.py` stamps `<commit date>-<short sha>`, the label of its file on itch.io, into the build's `llm.json` and stops if the build doesn't report it; the editor and builds packaged by hand report `local`; `Tools/analytics_report.py` lists the builds, marks the releases and takes `--build <label>`. T115 gave the game its own icon (2026-11-20, my pick of six): a grinning person pushes the costume's box head up and off with a wink, on a UIStyle Red tile, on the `.exe`, the window and the taskbar button (`Docs/Art/Icon/README.md`); the Mac icon is in place but waits for the next Mac build to be seen. T91 made `main` the production branch (2026-11-19): `main` holds the last release, a release fast-forwards it to `dev`'s pushed tip only on my word in chat ("Releases" in `CLAUDE.md`), and Tools > itch.io ships `main`'s tip ("Dry run of dev" tries `dev`'s first). The first release is `10f8540`, on itch.io as `2026-11-20-10f8540`. T92 put the Mac file beside it (2026-11-20): `no-humans-on-set-mac.zip`, the same release, from Tools > itch.io on the Mac. T61 put the stagehand in the game (2026-11-19): on my first show a friendly AI stagehand whispers each rule once, at the moment it first matters, in its own earpiece panel; the title has "Tonight's show" with the three opening lines, a How to play screen and a Stagehand tips toggle. T34 fixed the in-show screen (2026-11-19): the fourth ballot ticket votes for the fourth name, a show plays by keyboard, the name tags are on-screen seat-color plates, and every panel, button and the stamp come from `UIStyle`. T110 makes each scene's props fly in from the wing beside the Prop Table, and the last scene's go out (my OK on 2026-11-19). The new art is all in the game. T102 put the new music, sounds and voices in the game with a quieter mix (my OK on 2026-11-19); "The mix (T102)" in `Docs/AudioShortlist.md` has every level. T104 put the costume models in the game, fitted to every character (my OK on 2026-11-19; `Docs/Art/Costumes/game_fit_grid.png`). T109 re-fitted the cast's arms so they no longer float beside their bodies (my OK on 2026-11-19; `Docs/Art/Cast/arms_game_sheet.png`). T94 set the art direction they follow: `Docs/Art/Direction/README.md`. T95 approved the cast that T96 and T103 build on: `Docs/Art/Cast/README.md`. T103 put it in the game as Hyper3D models; T104 fits the costumes to its new heads from "For T104" in `Docs/tasks/T103.md`. T98 approved the theater, and T106 built it in the game (my OK on 2026-11-19; `Docs/Art/Set/game_house_compare.png`): `Docs/Art/Set/README.md`; and T99 put the new backdrops on its flat, with the stagehand and the burning bills: `Docs/Art/2D/README.md`. T105 put T97's props in the game as Hyper3D models: `Docs/Art/Props/manifest.json`. T96 approved the costumes and the role table that T104 builds on: `Docs/Art/Costumes/README.md`. T85 shows the cast's roles and wants on a card when I point at a robot, so the card on the right no longer scrolls (my OK on 2026-11-19).

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



- [ ] **T118 Hide the title's Play stats button**
  - **Model and effort:** Sonnet 5.5, medium. A small change to two Blueprints, in patterns the project already has, checked in PIE.
  - **Depends on:** none (T68 made the button). Either machine with the editor: it changes `WBP_Title` and `BPC_Analytics`, not `BP_Show` or `WBP_Stage`, so it isn't the chain machine's. T116 also changes `BPC_Analytics.Init`: the lock keeps the two apart, and the second to run starts from the first one's pushed `Graphs/BPC_Analytics/Init.txt`.
  - **Needs:** the editor and the locks on `WBP_Title` and `BPC_Analytics`; my OK on the itch page's new Play stats bullet.
  - **Touches:** `Content/NHOS/UI/WBP_Title.uasset`, `Content/NHOS/Core/BPC_Analytics.uasset`, `Graphs/WBP_Title/ShowStats.txt`, `Graphs/BPC_Analytics/Init.txt`, `Content/NHOS/Data/llm.json` (`_readme`), `Relay/README.md` (one sentence), `Docs/ItchPage.md` (the Play stats bullet), `Docs/tasks/T118.md`.
  - **Details:** [Docs/tasks/T118.md](tasks/T118.md)

- [ ] **T119 The three glow props glow in the packaged game**
  - **Model and effort:** Sonnet 5.5, medium. One setting in three materials, with a clear check in PIE and in a cook.
  - **Depends on:** none (T105 made the materials). Either machine with the editor: it changes three prop materials, not `BP_Show` or `WBP_Stage`, so it isn't the chain machine's.
  - **Needs:** the editor and the locks on the three materials; the engine for Tools > itch.io > "Dry run of dev".
  - **Touches:** `Content/NHOS/Stage/Props/space_plans/M_GlowStickSword.uasset`, `Content/NHOS/Stage/Props/glowing_briefcase/M_GlowingBriefcase.uasset`, `Content/NHOS/Stage/Props/mine_bridge/M_GlowingStaff.uasset` (and any other material with the same mismatch), `Docs/tasks/T119.md`.
  - **Details:** [Docs/tasks/T119.md](tasks/T119.md)

- [ ] **T121 New costumes: an idea for each of the 8 roles**
  - **Model and effort:** Opus 5.5, high. Two or three costume ideas for each role that fit its story, one question per role.
  - **Depends on:** none (the costume pass of 2026-11-19 left the 8 roles bare-headed). It needs no editor and changes no asset, so either machine can run it, beside the chain.
  - **Needs:** my pick of an idea for each role.
  - **Touches:** `Docs/Art/Costumes/README.md` (the 8 rows of its role table name the picks), `Docs/tasks/T121.md`, `Docs/tasks/T129.md` (the picks it starts from).
  - **Details:** [Docs/tasks/T121.md](tasks/T121.md)

- [ ] **T129 New costumes, part 1: concepts for the 8 picked costumes, fitted to every character**
  - **Model and effort:** Opus 5.5, high. Eight costumes, each drawn as two candidates for my pick, then on all five characters, with a version made for my cube head.
  - **Depends on:** T121 (my picks; T96 has the method). It needs no editor and changes no asset, so either machine can run it, beside the chain. T96's scripts run only on a Mac; on the PC, port them first (see its file).
  - **Needs:** `Local/leonardo_key.json`; my OK on the estimated cost before the first paid call; my pick of a candidate for each costume, and of the three colors still open; my approval of each fit sheet; my OK on the design doc edit.
  - **Touches:** `Docs/Art/Costumes/` (a folder per new costume, `prompts.json`, `fits.json`, `gen.py`, `fit.py`, and `README.md` with its role table), `Docs/Design/ArtInspiration.md` (Costumes), `Docs/Design/Stories.md` (the 8 Headpiece cells), `Docs/tasks/T129.md`.
  - **Details:** [Docs/tasks/T129.md](tasks/T129.md)

- [ ] **T122 New costumes, part 2: the 8 new costumes' models, fitted to every character**
  - **Model and effort:** Opus 5.5, high. A model per costume version, a fit per character and the 8 seats dressed, judged by eye on every robot.
  - **Depends on:** T129 (the approved costumes and their views). Either machine with the editor: it changes no `BP_Show` or `WBP_Stage`, so it isn't the chain machine's.
  - **Needs:** the editor and Unreal MCP, Test for Free for the shows; the model tool T104 used (Hyper3D, or Meshy with `Local/meshy_key.json`); my OK on the estimated cost before the first paid call; my OK on the models and on the final fit grid; my OK on the design doc edit; the `BP_Robot` lock for the grand leader's collar, a part off the head that I OKed in T121, and for any other new attach point.
  - **Touches:** new `Content/NHOS/Stage/Costumes/<costume>/`, `Content/NHOS/Data/costumes.json`, `Content/NHOS/Data/scenes.json` (the 8 seats and the `_readme`), `Tools/check_prompts.py` (the empty-headpiece allowance goes), `Docs/Art/Costumes/`, `Docs/Assets.md`, `Docs/Design/ArtInspiration.md` (Costumes), `Docs/tasks/T122.md`; `Content/NHOS/Stage/BP_Robot.uasset` and `Graphs/BP_Robot/` for the collar's attach point.
  - **Details:** [Docs/tasks/T122.md](tasks/T122.md)

- [ ] **T113 A cover, screenshots and a trailer that make people want to play**
  - **Model and effort:** Opus 5.5, high. Creative work across the engine, screen recording and ffmpeg, judged by eye; it ends with my pick of the cover and my OK on the trailer.
  - **Depends on:** T114, T119, T121, T129, T122, and every other art task I add before the marketing: my art updates go in first (my words on 2026-11-19), so add each one here. Run it on the PC: the steps use Windows tools. It needs the editor but changes no existing asset, so it isn't the chain machine's.
  - **Needs:** the editor (or a second editor on its own MCP port, if another session drives the main one); my OK before ffmpeg is installed (`winget install Gyan.FFmpeg`); my OK for the cost of the recorded shows on Play (about $0.11 a show, on our relay); my pick of the cover and my OK on the trailer.
  - **Touches:** `Docs/ItchMedia/` (`README.md`, `cover.png` and its source, new `screenshots/`, `trailer.mp4`, `trailer.md`, the scripts that made them), `Docs/ItchPage.md` (the Cover image, Screenshots and Gameplay video rows, and the Graphics answer), `.gitattributes` (only if a GIF ships), new assets under `Content/NHOS/Media/` (only if a shot needs one), `Docs/tasks/T113.md`. No existing asset: never save `L_Stage`, `BP_Show`, `WBP_Stage` or `BP_Robot`. Raw recordings stay in `Saved/ItchMedia/`, out of git.
  - **Details:** [Docs/tasks/T113.md](tasks/T113.md)

- [ ] **T120 The Mac game remembers its keys and its first show**
  - **Model and effort:** Opus 5.5, high. File paths in two Blueprint components, and a sandboxed, translocated Mac app to check them in.
  - **Depends on:** T92 (the Mac build and its checks). Run it on the Mac: its check is a Mac build. It changes `BPC_LLMClient` and `BPC_Stagehand`, not `BP_Show` or `WBP_Stage`, so it isn't the chain machine's.
  - **Needs:** the editor and the locks on `BPC_LLMClient` and `BPC_Stagehand`; the engine for a Mac package; my click on Open Anyway for the test copy.
  - **Touches:** `Content/NHOS/Core/BPC_LLMClient.uasset`, `Content/NHOS/Core/BPC_Stagehand.uasset` (or a new component for the folder), `Graphs/BPC_LLMClient/LoadConfig.txt`, `Graphs/BPC_LLMClient/SaveKeys.txt`, `Graphs/BPC_Stagehand/TipsNext.txt`, `Graphs/BPC_Stagehand/SetTipsNext.txt`, `Docs/Builds.md` ("Package a macOS build"), `Docs/ItchPage.md` ("Where your keys go"), `Docs/tasks/T120.md`.
  - **Details:** [Docs/tasks/T120.md](tasks/T120.md)

- [ ] **T116 My own machines never count in the play stats**
  - **Model and effort:** Opus 5.5, high. It changes the gate on every build's events, and the marker's place must work on both platforms, the sandboxed Mac app included.
  - **Depends on:** none. Run it on the PC with the editor: its check is a Windows build. It changes `BPC_Analytics`, not `BP_Show` or `WBP_Stage`, so it isn't the chain machine's.
  - **Needs:** the editor and the `BPC_Analytics.uasset` lock; the engine, to package a Windows build (about 6 minutes).
  - **Touches:** `Content/NHOS/Core/BPC_Analytics.uasset`, `Graphs/BPC_Analytics/Init.txt`, `Docs/machine.example.json` (new), `Relay/README.md` ("Leaving out our own machines"), `CLAUDE.md` (the analytics sentences under "Unreal MCP"), `README.md` (one setup line), `Docs/tasks/T116.md`; outside the repo: the PC's marker file.
  - **Details:** [Docs/tasks/T116.md](tasks/T116.md)

- [ ] **T117 A live dashboard of the prod play stats, on the relay**
  - **Model and effort:** Opus 5.5, high. A new page on the relay, which ships with a release and keeps the stats key in a browser.
  - **Depends on:** T111 (the build labels the page filters by). T116 makes my machines' events test events; the page needs nothing more for that. Either machine; it needs no editor and changes no asset. It edits `Relay/README.md` and `Tools/analytics_report.py` after T111 and T116 do.
  - **Needs:** Node and `wrangler`, for `wrangler dev` ("Run it locally" in `Relay/README.md`); the built-in browser, for the check. Not the real stats key: the check uses a local one.
  - **Touches:** `Relay/src/index.js` (the `/dashboard` route, `ignore_players` in `/stats`), `Relay/src/dashboard.html` (new), `Relay/wrangler.toml` (only if the HTML import needs a rule), `Relay/test/curl-tests.sh`, `Relay/README.md` ("Analytics events", new "Dashboard"), `Tools/analytics_report.py` (the relay's ignore list), `Docs/tasks/T117.md`.
  - **Details:** [Docs/tasks/T117.md](tasks/T117.md)

- [ ] **T123 The web, part 1: a spike on the full UE 5.9 release**
  - **Model and effort:** Opus 5.5, high. A spike on a new engine version and platform: it ends in my go for T124 to T128 and my choice of moving the project to 5.9 or building the web from a 5.9 copy.
  - **Depends on:** T112 (done). The PC: Epic's preview builds for the Mac lacked web files. It works in a throwaway copy on 5.9, so it holds no lock and needs no editor in the repo folder.
  - **Needs:** the full UE 5.9 release; my OK before any download (UE 5.9, emsdk), with sizes; Chrome; my verdict.
  - **Touches:** a copy of the project outside the repo folder; new `Docs/Web/` (findings, screenshots); `Docs/tasks/T123.md`, and the steps in `Docs/tasks/T124.md` to `T128.md` if the spike changes them. No asset in the repo folder, and the project stays on 5.8.4.
  - **Blocked:** until Epic ships the full UE 5.9 release (2027, Epic says). The web target was a preview in November 2026.
  - **Details:** [Docs/tasks/T123.md](tasks/T123.md)

- [ ] **T124 The web, part 2: the relay answers the web build (CORS)**
  - **Model and effort:** Sonnet 5.5, medium. A small Worker change in the relay's own patterns, with curl tests.
  - **Depends on:** T123 (the go, and the web build's origin). Either machine; it needs no editor and changes no asset.
  - **Needs:** Node and `wrangler`, for `wrangler dev` ("Run it locally" in `Relay/README.md`); my OK before the relay deploys.
  - **Touches:** `Relay/src/index.js` (CORS headers, `OPTIONS`), `Relay/wrangler.toml` (`WEB_ORIGINS`), `Relay/test/curl-tests.sh`, `Relay/README.md`, `Docs/tasks/T124.md`.
  - **Details:** [Docs/tasks/T124.md](tasks/T124.md)

- [ ] **T125 The web, part 3: a mobile look for the stage**
  - **Model and effort:** Opus 5.5, high. Lights and device profiles that keep the art direction on the mobile renderer, while the desktop look stays exactly as it is.
  - **Depends on:** T123 (the go, and how the web tiers look). Either machine with the editor.
  - **Needs:** editor + Unreal MCP running; the mobile preview in a game window ("Ways of working" in `Docs/tasks/T112.md`); my OK on the mobile sheet.
  - **Touches:** `Content/NHOS/Maps/L_Stage.umap` (the house fill, the key spot), `Content/NHOS/Stage/BP_Robot.uasset` (a blob shadow, if I pick it) and its `Graphs/BP_Robot/` files, `Config/DefaultDeviceProfiles.ini` (new: the texture cap) or `Config/DefaultEngine.ini`, `Docs/Art/Direction/README.md` (the mobile look's lighting), `Docs/tasks/T125.md`.
  - **Details:** [Docs/tasks/T125.md](tasks/T125.md)

- [ ] **T126 The web, part 4: fewer triangles on the stage**
  - **Model and effort:** Opus 5.5, high. LODs or a light audience across many meshes, measured on the mobile renderer.
  - **Depends on:** T123 (the go, and the frame rate in a browser). Either machine with the editor. If it swaps the audience's meshes in `L_Stage`, run it after T125, which changes `L_Stage` too.
  - **Needs:** editor + Unreal MCP running; the mobile preview in a game window ("Ways of working" in `Docs/tasks/T112.md`).
  - **Touches:** the static meshes under `Content/NHOS/Stage/` (their LODs); maybe new light audience meshes in `Content/NHOS/Stage/Set/` and the audience in `Content/NHOS/Maps/L_Stage.umap`; `Docs/tasks/T126.md`.
  - **Details:** [Docs/tasks/T126.md](tasks/T126.md)

- [ ] **T127 The web, part 5: the game's files and modes in a browser**
  - **Model and effort:** Opus 5.5, high. File, save and mode changes in several Blueprints, switched by platform.
  - **Depends on:** T123 (how files and saves work in the web build), T124 (the relay from a browser), T120 (where the game keeps `Local/`). It changes `BP_Show`, so it belongs to the chain machine while two machines work.
  - **Needs:** editor + Unreal MCP running; a web build to check in Chrome (T123's setup); my OK on the design doc edit.
  - **Touches:** the Blueprints that read `Content/NHOS/Data/*.json` (`Content/NHOS/Core/BP_Show.uasset`, `BPC_LLMClient.uasset` and others), `Content/NHOS/Core/BPC_Stagehand.uasset` (the first-show flag), `Content/NHOS/Core/SG_Player.uasset` only if the save needs it, `Content/NHOS/UI/WBP_Title.uasset` (no own-keys button on the web), their `Graphs/` files, `Config/DefaultGame.ini` (how the web build gets `Content/NHOS/Data`), the design doc's UI file in `Docs/Design/`, `Docs/tasks/T127.md`.
  - **Details:** [Docs/tasks/T127.md](tasks/T127.md)

- [ ] **T128 The web, part 6: the web build on itch.io**
  - **Model and effort:** Opus 5.5, high. Packaging under itch.io's size limits, a web channel in the deploy tool, and the page.
  - **Depends on:** T124, T125, T126, T127. The machine where T123 packaged the web build.
  - **Needs:** the 5.9 setup that T123 chose; butler; my OK before the upload.
  - **Touches:** `Docs/Builds.md` (the web build), `Tools/deploy_itch.py` and the editor's Tools > itch.io menu (a web channel), `Tools/check_build_secrets.py` (the web build's files, if needed), `Docs/ItchPage.md` (the embed settings), `Docs/tasks/T128.md`.
  - **Details:** [Docs/tasks/T128.md](tasks/T128.md)

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

- [x] **T97 New art, part 4: concepts for the story props, approved by me**
  - **Details:** [Docs/tasks/T97.md](tasks/T97.md)

- [x] **T84 Scene Prep shows the scene and Start the scene in the middle**
  - **Details:** [Docs/tasks/T84.md](tasks/T84.md)

- [x] **T101 New audio, part 2: the show and robot sounds, the clicks and the bots' voices, picked by me**
  - **Details:** [Docs/tasks/T101.md](tasks/T101.md)

- [x] **T108 Meta's seat color becomes mustard, in the UI and on the robot**
  - **Details:** [Docs/tasks/T108.md](tasks/T108.md)

- [x] **T96 New art, part 3: concepts for a costume for each role, fitted to every character, approved by me**
  - **Details:** [Docs/tasks/T96.md](tasks/T96.md)

- [x] **T105 New art, part 9: the story props' models, generated from the approved concepts**
  - **Details:** [Docs/tasks/T105.md](tasks/T105.md)

- [x] **T99 New art, part 6: the backdrops, the stagehand's portrait and the burning bills, approved by me and imported**
  - **Details:** [Docs/tasks/T99.md](tasks/T99.md)

- [x] **T103 New art, part 7: the cast's models, generated from the approved concepts**
  - **Details:** [Docs/tasks/T103.md](tasks/T103.md)

- [x] **T102 New audio, part 3: import the picks and set a quieter mix**
  - **Details:** [Docs/tasks/T102.md](tasks/T102.md)

- [x] **T104 New art, part 8: the costumes' models, fitted to every character**
  - **Details:** [Docs/tasks/T104.md](tasks/T104.md)

- [x] **T106 New art, part 10: the theater, its set pieces and the audience, built from the approved concepts**
  - **Details:** [Docs/tasks/T106.md](tasks/T106.md)

- [x] **T109 Fix the cast's arms, which float beside their bodies**
  - **Details:** [Docs/tasks/T109.md](tasks/T109.md)

- [x] **T85 The cast's roles and wants show when I point at a robot**
  - **Details:** [Docs/tasks/T85.md](tasks/T85.md)

- [x] **T110 Each scene's props come in from the wing, and the last scene's props go out**
  - **Details:** [Docs/tasks/T110.md](tasks/T110.md)

- [x] **T34 Fix the in-show screen**
  - **Details:** [Docs/tasks/T34.md](tasks/T34.md)
- [x] **T61 Stagehand onboarding: earpiece tips, a tips toggle and How to play**
  - **Details:** [Docs/tasks/T61.md](tasks/T61.md)
- [x] **T91 main becomes the production branch, and the itch.io menu ships main**
  - **Details:** [Docs/tasks/T91.md](tasks/T91.md)
- [x] **T92 The Mac builds and uploads the Mac file from the editor menu**
  - **Details:** [Docs/tasks/T92.md](tasks/T92.md)
- [x] **T114 The box audience sits in real box seats**
  - **Details:** [Docs/tasks/T114.md](tasks/T114.md)
- [x] **T115 The game gets its own icon**
  - **Details:** [Docs/tasks/T115.md](tasks/T115.md)
- [x] **T111 Each build tells analytics which release it is**
  - **Details:** [Docs/tasks/T111.md](tasks/T111.md)
- [x] **T112 Spike: the stage on the mobile renderer, for Android and the web**
  - **Details:** [Docs/tasks/T112.md](tasks/T112.md)

## Not planned yet

Ideas that are not tasks yet, and only if time is left after the last open task: a fifth persona (since T26, that is a sixth actor and a fourth scene), more scene cards and more notes, and from my input spec (`Docs/tasks/T62.md`): clicking a prop, a place or an actor on the stage to fill the builder's target, and number keys 1 to 7 to pick an action. To plan one, add it as a task (see "Changing the plan").
