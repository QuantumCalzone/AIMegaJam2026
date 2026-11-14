# MVP plan: No Humans On Set

The living plan for the MVP prototype of our jam game. The design is in [GameDesign.md](GameDesign.md). Say **"Next task"** to build the next step.

In this file, "I" and "my" mean the person at the keyboard. "Claude" means the agent doing the task.

**Next up:** T13 and T15 are done. T14 waits only for my verdict on its playtest (every screen is clear). T16 (Opus 5.5 · high) is next and needs no editor; T17 (Opus 5.5 · high) starts once T14's box is checked.

## Goal

Answer one question as fast as possible: **is it fun to fool an all-AI cast, and do the AIs catch a human at a fair rate (not every time, not never)?** Nothing else matters until a playtest answers it.

**Answered by the gate (T12, 2026-11-14): go.** I liked it. From T13 on, the plan covers everything the submission needs, not only the MVP. The In and Out lists below describe the MVP (T01 to T12); T13 to T24 bring in most of what they leave out.

## Scope

**In:**

- One café scene set.
- A text stage: a UMG log and an input box. Above it, a bare 3D stage with four box robots that show who is speaking and who was cut (T11).
- One human player plus 3 AI personas. That is a cast of 4, so a show has 2 scenes.
- The full show loop from the Rules tab: Scene Prep, The Scene, Free Talk, The Cut with reveal and reactions, repeat to the final two, win and lose screens with the AIs' reasoning, restart.

**Out:**

- The 3D café set, moving robots and animation, audio, polish, extra sets.
- More than one LLM provider. Every persona, the input LLM and the Director run on **Anthropic (Claude)** for now.
- The relay and the key-entry screen. The key comes from a file on the developer's machine.

**Riskiest work first.** T01 and T02 prove that this Blueprint-only project can call the Claude API and parse the JSON reply, in PIE and in a packaged Windows build, before any game logic exists.

## Time check

First written Fri Nov 13, 2026, about 3:20 PM PST. Rewritten at the gate (T12), Fri Nov 13, about 10 PM PST. The deadline is Sun Nov 15, 5:59 PM PST (Nov 16, 01:59 UTC). That leaves about 44 hours, sleep included. T01 to T12 finished ahead of the first schedule.

| Target | When (PST) |
|---|---|
| Plain speech (T13), UI/UX polish (T14) and story scenes (T15) | Sat Nov 14, by noon |
| One LLM per AI player (T16, T18) and the stage art (T17) | Sat Nov 14, by 6 PM |
| Robots act out their actions (T19), audio (T20), relay and key entry (T21) | Sun Nov 15, by 10 AM |
| Packaged and played (T22), submission ready (T23) | Sun Nov 15, by 2 PM |
| Submit | Sun Nov 15, by 3 PM. Keep 3 hours of margin. |

12 tasks at up to an hour each is about 12 hours of agent time, plus your time on checks and playtests. Two lanes can run at once: tasks that need no editor (T13, T15, T16, and finding audio files for T20) beside the editor tasks (T14, T17, T18 to T21), which go one at a time. If we fall behind, cut in this order: T24 (timers), then T19 to Move and Look only, then T20 to music and three sounds, then T17's robot motion.

## How to run a task

When I say **"Next task"** or **"Next ask"**:

1. `git pull` (if the branch is not on the remote yet, say so and go on). Read `Agents/`. Open this file and run `git lfs locks`. Take the first unchecked, unclaimed task whose dependencies are done.
2. Tell me the task and its recommended model and effort. If this session runs a different model, say so and ask whether to go on.
3. Check its Needs. If something is missing (for example, Unreal MCP is not connected), tell me what to do and stop.
4. Claim the task (see "Claiming a task"). Write a status file, `Agents/status/mvp-T07.md`, and lock assets as `Agents/README.md` says.
5. Do the work, then run the Done-when check. If the check fails, do not mark the task done: write what blocks it under the task (a `Blocked:` line) and tell me.
6. Make one commit that holds the work, the checked box, the updated "Next up" line, and one line in [DevLog.md](DevLog.md) (the jam's Glass Box category needs a dev log). Message: `T07: <title>`. Do not push unless I ask.
7. Delete the status file. Keep the claim until the commit is pushed. End by naming the next task with its model and effort, so I can switch before I send "Next task".

Changes to the plan are commits too (`Plan: <what changed>`), for example when a spike or a playtest changes the design. A plan change that adds a task also adds its claim file.

## Claiming a task

A claim is an LFS lock on the task's claim file. Everyone sees it at once, on every machine, with no push.

- **Claim:** `git lfs lock Docs/claims/T07`
- **See all claims:** `git lfs locks`
- **Release:** `git lfs unlock Docs/claims/T07`, after the task's commit is pushed. Until the push, other machines see neither the work nor the checked box, so the lock is what tells them the task is taken. When I ask you to push, release the claims of every task that went up.
- A task is free when its box is unchecked here and `git lfs locks` shows no lock on its claim file.
- If the lock fails because a teammate holds it, take the next free task.
- If my own account holds the lock on an unchecked task and there is no status file for it in `Agents/status/`, an earlier session may have stopped halfway. Ask me before taking it.
- If you stop without finishing, add a `Blocked:` line under the task and commit it as `Plan: T07 blocked`. Release the claim only if someone else should take the task.

Never edit the claim files. They exist only to be locked.

## Model and effort rubric

- **Opus 5.5, high:** the spike, architecture, AI prompt design, Blueprint systems with many parts, debugging.
- **Sonnet 5.5, medium:** well-specified Blueprint or UMG work that follows a pattern already in the project.
- **Haiku 5.5, low:** docs, config and small mechanical edits.
- Use **xhigh** only to retry a task that failed once. Never use **max**.

## Build notes for every task

These hold unless T01 or T02 finds otherwise. If one changes, change it here in a `Plan:` commit.

- **Blueprint-only.** No C++ unless the spikes show it is needed. The choice goes in `Agents/decisions/`.
- **Where things live.** Assets go under `Content/NHOS/` (`Maps/`, `Core/`, `UI/`, and `Stage/` for the 3D set from T11 on). Files the game reads at runtime go in `Content/NHOS/Data/` as `.json`. The API key and local switches go in `Local/` in the project root, which git ignores. The key file is `Local/llm_key.json`; copy it from `Docs/llm_key.example.json`. Blueprint reads it at `Get Project Directory` + `Local/llm_key.json`.
- **API keys never go in git, and never into chat.** I paste my key into the key file myself.
- **Prompts are files, not Blueprint strings.** The opening game prompt, the base prompt, the personas, the input LLM prompt and the scene cards live in `Content/NHOS/Data/`, so they diff in git. Store long text as an array of lines.
- **One provider.** All calls go to the Claude Messages API. The model, effort and token limit for each role (actor, input LLM, Director) are values in `Content/NHOS/Data/llm.json`. T01 and T02 ran `claude-opus-5-5` at low effort. Since 2026-11-13 every role runs `claude-haiku-5-5` at low effort, the cheapest model at its lowest level. Haiku 5.5 has no server-side fallback, so `beta` and `fallbacks` in `llm.json` are empty; a refusal comes back as `stop_reason: "refusal"`.
- **One provider per persona, from T16 and T18 on.** Each persona runs on its own provider, as in the design's table, with a key per provider (no router). T16 sets up the prompts and the keys; T18 makes the game call them. Since 2026-11-14 each bot goes by its provider's name on screen, in the log and in the cast list the AIs read (OpenAI, Anthropic, SpaceXAI, Meta: the `name` fields in `personas.json`), not by a persona name such as "The Worrier". Persona ids (`worrier`) stay as they are in files and `NHOS:` lines. Real people's names and product names stay out of prompts and off the screen.
- **The design doc follows the game.** When a task changes the design (the speech style, the sets, the providers), it shows me the matching edit to the Claude Doc. After my OK, it makes the edit with the Claude Docs connector and refreshes `Docs/GameDesign.md` from the doc. `Tools/check_prompts.py` checks the prompts against `GameDesign.md` word for word, so the refresh comes before the check.
- **Legibility first.** Everything an AI says reads like a normal chat, the way Claude or ChatGPT write: plain sentences, no brackets or tags, no beeps or sound effects, no emoji, no ALL-CAPS words. Each persona's personality comes through what it says, not how it is typed.
- **Outside and generated assets.** Record every art, audio or font asset in `Docs/Assets.md` when you add it: what it is, where it came from (a Fab link, a site, or the AI tool and prompt) and its license. The submission form needs the list.
- **One reply shape.** Every ask (scene turn, Free Talk line, vote, reaction, tiebreak) gets back the same small JSON object, with unused fields empty. One parser serves the whole game.
- **The shared log** is what the AIs read. Every actor's lines have the same form, human or AI. It never holds my raw input, times, errors, anyone's note, or who has the decoy. Game messages reach the AIs in a separate field that actors can't write to.
- **Check lines.** Anything a Done-when check reads is printed with the prefix `NHOS:` to the editor log (`Saved/Logs/AIMegaJam2026.log`). It never goes in the shared log.
- **Autoplay.** From T07 on, a local switch makes the human seat play canned lines, so an agent can run a whole show unattended and read the result in the log. The switch file is `Local/switches.json` (copy `Docs/switches.example.json`), with `"autoplay": true`. The canned lines are in `Content/NHOS/Data/autoplay.json`, one list per phase, and they go through the input LLM like typed lines. Later switches (such as T09's `force_tie`) go in the same file. Set autoplay back to `false` before a person plays.
- **Unreal MCP.** Do editor work through Unreal MCP. One call at a time, each under about 100 seconds (the client stops waiting at about 120). Split long work, and save after each step. Write graphs with `BlueprintTools.write_graph_dsl`, and batch calls with `ProgrammaticToolset.execute_tool_script`. Read "T01: spike results" in Findings first: it lists the DSL rules that cost time to find. MCP can't create a level, so a person makes new levels in the editor (File > New Level > Empty Level).
- **Each task leaves the game runnable.** One task = one session = one commit, about an hour of agent work at most.

## Tasks

### Spikes

- [x] **T01 Spike: one Claude call from Blueprint, in PIE**
  - **Model and effort:** Opus 5.5, high. The riskiest task; every other task depends on it.
  - **Depends on:** nothing
  - **Needs:** my API key. The editor **closed** at the start: the task turns on two plugins, then asks me to open the editor and reconnect Unreal MCP.
  - **Steps:**
    1. With the editor closed, turn on the `HttpBlueprint` and `JsonBlueprintUtilities` plugins in the `.uproject` (runtime, not editor-only). Pick the git-ignored key folder, add it to `.gitignore`, and commit an example key file with no key in it.
    2. Load the `claude-api` skill for the request shape. Write `Content/NHOS/Data/llm.json` (endpoint, API version, model, effort, token limit).
    3. Through Unreal MCP, make the level `L_Stage` (empty, not World Partition) and `BPC_LLMClient`, on a `BP_Show` actor in the level. On BeginPlay it reads the key file and `llm.json`, sends one request that asks for a JSON reply, and parses one field out of it.
    4. Answer the spike questions listed under "Findings", and write the answers there.
    5. If Unreal MCP can't place the `Http Request` or `Get Field` nodes, try editor Python. If Blueprint can't do the job at all, stop and propose the smallest C++ module.
  - **Done when:** a PIE run on `L_Stage` prints `NHOS: SPIKE OK <text>` to the editor log, where `<text>` is a field parsed from Claude's JSON reply. With a wrong key it prints `NHOS: SPIKE FAIL` and the API's error message. `git check-ignore` confirms the key file is ignored.
  - **Touches:** `AIMegaJam2026.uproject`, `.gitignore`, `Config/DefaultEngine.ini` (HTTP timeouts, only if needed), new `Content/NHOS/Maps/L_Stage.umap`, new `Content/NHOS/Core/BPC_LLMClient.uasset`, new `Content/NHOS/Core/BP_Show.uasset`, new `Content/NHOS/Data/llm.json`, new `Docs/llm_key.example.json`, the Findings section.

- [x] **T02 Spike: the same call in a packaged Windows build, and record the decision**
  - **Model and effort:** Opus 5.5, high. Packaging problems need debugging, and the decision affects the whole team.
  - **Depends on:** T01
  - **Needs:** my API key, a Windows machine, the editor closed.
  - **Steps:**
    1. Set `GameDefaultMap` to `L_Stage` in `Config/DefaultEngine.ini`. In `Config/DefaultGame.ini`, cook only that map and stage `Content/NHOS/Data` as loose files.
    2. Run the package command from `CLAUDE.local.md` in the background. The first cook can take 20 minutes or more.
    3. Put the key file where the packaged game looks for it, run the game with `-log`, and read its log.
    4. If the call fails only when packaged, fix it (plugin lists, certificates, staging). If Blueprint can't be made to work, fall back to the smallest C++ module.
    5. Write the decision note: Blueprint-only or C++, where keys live, where data files live and how the game reads them. Add seconds per call and a cost estimate per show to Findings.
  - **Done when:** the packaged game's log shows `NHOS: SPIKE OK <text>`, and `Agents/decisions/<UTC>-<handle>-llm-calls.md` exists.
  - **Touches:** `Config/DefaultEngine.ini`, `Config/DefaultGame.ini`, new `Agents/decisions/<UTC>-<handle>-llm-calls.md`, the Findings section, `Packaged/` (not in git).

### One AI reply on screen

- [x] **T03 Prompt and data files**
  - **Model and effort:** Opus 5.5, high. AI prompt design; these files decide whether the game is fun and fair.
  - **Depends on:** T01 (it fixes the file format and the reply shape)
  - **Needs:** my API key. No editor, so this can run beside T02 or T04 in a second session or on a teammate's machine.
  - **Steps:**
    1. `prompts.json`: the opening game prompt (the show's rules, the actor's goal, the reply shape), the shared base prompt, the input LLM prompt, the Director prompt, and one short ask for each kind of request.
    2. `personas.json`: the four personas from the Bot Prompts tab, word for word. No real names or company names.
    3. `scenes.json`: the café set (the six places and a few props), 2 scene cards with a role and a want for each of 4 seats, and 6 director's notes, each with a decoy. Notes are mostly physical.
    4. `Tools/check_prompts.py`: checks that the files are valid, then sends each ask once per persona with the same request body the game sends, and prints the replies.
    5. Read the replies. Fix the prompts until every reply parses, stays in character and stays under 25 words.
  - **Done when:** `Tools/check_prompts.py` exits with code 0 and prints one valid reply for each ask and each persona.
  - **Touches:** new `Content/NHOS/Data/prompts.json`, `personas.json` and `scenes.json`; `Content/NHOS/Data/llm.json`; new `Tools/check_prompts.py`.

- [x] **T04 Stage screen: a log and an input box**
  - **Model and effort:** Sonnet 5.5, medium. Small UMG work, fully specified here.
  - **Depends on:** T02 (the spikes finish before any game work starts)
  - **Needs:** editor + Unreal MCP running.
  - **Steps:**
    1. `WBP_Stage`: a header line for the phase, a scrolling log, and an input box with a Send button. Enter also sends.
    2. `BP_ShowGameMode` and `BP_ShowPlayerController` show the widget when `L_Stage` starts, with the mouse cursor on and the keyboard focus in the input box.
    3. Give the widget one function, `AddLogLine`. For now, sent text goes straight to the log.
  - **Done when:** in PIE, typing `hello` and pressing Enter adds the line to the on-screen log (screenshot), and the input box is empty and focused again.
  - **Touches:** new `Content/NHOS/UI/WBP_Stage.uasset`, new `Content/NHOS/Core/BP_ShowGameMode.uasset`, new `Content/NHOS/Core/BP_ShowPlayerController.uasset`, `Content/NHOS/Maps/L_Stage.umap`.

- [x] **T05 One AI reply on screen**
  - **Model and effort:** Opus 5.5, high. It turns the spike into the client that every later task calls.
  - **Depends on:** T03, T04
  - **Needs:** editor + Unreal MCP running, my API key.
  - **Steps:**
    1. At start, `BP_Show` loads `llm.json`, `prompts.json` and `personas.json`. If a file or the key is missing, the screen says "AI service unavailable" and why.
    2. `BPC_LLMClient` gets `Ask(Tag, System, User)` and an `OnAnswer(Tag, Ok, reply fields)` event. Several asks can be in flight at once. An error, a refusal or bad JSON gives `Ok = false`.
    3. On Send, ask one persona (The Worrier) with the game prompt, the base prompt and the persona as the system text, and show the reply's speech in the log under the persona's name.
    4. Print `NHOS: LLM <tag> ok <seconds>` or `NHOS: LLM <tag> fail <reason>` for every call.
  - **Done when:** in PIE, a typed question gets an in-character answer in the on-screen log within about 15 seconds, and the editor log shows `NHOS: LLM ... ok`. With the key file renamed, the screen shows "AI service unavailable".
  - **Touches:** `Content/NHOS/Core/BPC_LLMClient.uasset`, `Content/NHOS/Core/BP_Show.uasset`, `Content/NHOS/UI/WBP_Stage.uasset`. T05 also added `Content/NHOS/Core/BPC_LLMRequest.uasset` and left `WBP_Stage` unchanged.

### The show loop

- [x] **T06 Show setup and Scene Prep**
  - **Model and effort:** Opus 5.5, high. It sets the show state that T07 to T10 all extend.
  - **Depends on:** T05
  - **Needs:** editor + Unreal MCP running.
  - **Steps:**
    1. `BP_Show` holds the show state: the phase, the scene number, 4 seats (persona, human or AI, cut or not, note) and the shared log.
    2. At start: draw my persona at random, give the other three to the AIs, pick a scene card, and give every seat the director's note except one random seat, which gets the decoy.
    3. The screen shows the cast, the scene card, my role and my note. It never shows who has the decoy.
    4. Print `NHOS: SETUP human=<persona> decoy=<persona> scene=<id>`.
  - **Done when:** two PIE runs each print a `NHOS: SETUP` line, and the screen shows the cast, the scene card and my note (screenshot).
  - **Touches:** `Content/NHOS/Core/BP_Show.uasset`, `Content/NHOS/UI/WBP_Stage.uasset`, new `Content/NHOS/Core/E_ShowPhase.uasset`, new `Content/NHOS/Core/S_Seat.uasset`. T06 made neither new asset: Unreal MCP can't create a struct or an enum, so the seats are parallel arrays in `BP_Show` and the phase is a string (see "T06: show setup results").

- [x] **T07 The Scene: three simultaneous turns**
  - **Model and effort:** Opus 5.5, high. Parallel asks that must all return before the turn plays out; the hardest Blueprint part.
  - **Depends on:** T06
  - **Needs:** editor + Unreal MCP running, my API key.
  - **Steps:**
    1. For each of 3 turns, ask the three AIs at once. Each gets the cast, the scene card, its own note, the shared log and the ask. Meanwhile I type my turn, and the input LLM turns it into the same reply shape.
    2. When all four turns are in, cap each line at 25 words, add them to the shared log in random order, and show them. Print each shared-log line as `NHOS: LOG ...` too.
    3. A reply that fails or can't be parsed makes that actor look around. No error goes in the shared log.
    4. Add autoplay: if the local switch file says so, the human seat sends canned lines.
  - **Done when:** with autoplay on, a PIE run prints `NHOS: SCENE 1 TURN 3 DONE` and the on-screen log holds 12 turn lines in mixed order (screenshot). With autoplay off, one turn I type shows up in the same form as the AI lines.
  - **Touches:** `Content/NHOS/Core/BP_Show.uasset`, `Content/NHOS/Core/BPC_LLMClient.uasset`, `Content/NHOS/UI/WBP_Stage.uasset`, the local switch file (not in git). T07 left `BPC_LLMClient` unchanged and added `Content/NHOS/Data/autoplay.json` and `Docs/switches.example.json`.

- [x] **T08 Free Talk**
  - **Model and effort:** Sonnet 5.5, medium. The same ask-and-log pattern as T07, with one speaker at a time.
  - **Depends on:** T07
  - **Needs:** editor + Unreal MCP running, my API key.
  - **Steps:**
    1. After turn 3, run 2 rounds. Each round has a new random order and one speaker at a time, so each AI sees the lines before its own.
    2. On my turn I type a line or press Pass. My line goes through the input LLM and into the shared log in the same form as an AI line.
    3. An AI can pass. A pass is logged as a pass.
  - **Done when:** with autoplay on, a PIE run prints `NHOS: FREETALK DONE` after 8 talk entries (lines or passes).
  - **Touches:** `Content/NHOS/Core/BP_Show.uasset`, `Content/NHOS/UI/WBP_Stage.uasset`. T08 also added a `free_talk` list to `Content/NHOS/Data/autoplay.json`.

- [x] **T09 The Cut: votes, tiebreak and reveal**
  - **Model and effort:** Opus 5.5, high. Several new parts: the vote screen, the tally and the Director call.
  - **Depends on:** T08
  - **Needs:** editor + Unreal MCP running, my API key.
  - **Steps:**
    1. Ask all AIs at once for a vote and a one-line reason. I pick a name with a button and type a reason. Nobody can vote for themselves; a bad vote is asked again once, then replaced by a random valid one.
    2. Count the votes. Show each vote with its reason, and add them to the shared log.
    3. On a tie, ask the Director, who is not an actor, to choose among the tied actors with a one-line reason.
    4. Show the stamp, `<NAME>: AI` or `<NAME>: HUMAN`, and mark that seat as cut.
  - **Done when:** with autoplay on, a PIE run prints `NHOS: CUT <persona> tiebreak=<yes|no>` and the stamp shows (screenshot). With the local `force_tie` switch on, the Director's line appears.
  - **Touches:** `Content/NHOS/Core/BP_Show.uasset`, `Content/NHOS/UI/WBP_Stage.uasset`. T09 also added a `vote` list to `Content/NHOS/Data/autoplay.json` and `force_tie` to `Docs/switches.example.json`.

- [x] **T10 Reactions, the final two, end screens and restart**
  - **Model and effort:** Opus 5.5, high. Many parts, and the first run of the whole loop usually needs debugging.
  - **Depends on:** T09
  - **Needs:** editor + Unreal MCP running, my API key.
  - **Steps:**
    1. Reactions: the cut actor first, then each remaining bot, then me, one line each, all into the shared log.
    2. Then branch: if I was cut, I lose. If two actors remain, I win. Otherwise go back to Scene Prep with a new scene card and a new note.
    3. `WBP_EndScreen`: win or lose, each AI's vote reasons from the show, and one closing line from each AI on who it thought was human.
    4. A Restart button starts a new show without leaving PIE.
  - **Done when:** with autoplay on, a PIE run plays a whole show and prints `NHOS: SHOW END result=<win|lose> scenes=<n>`. Restart starts a second show that also reaches `NHOS: SHOW END` (screenshots of the end screen).
  - **Touches:** `Content/NHOS/Core/BP_Show.uasset`, `Content/NHOS/UI/WBP_Stage.uasset`, new `Content/NHOS/UI/WBP_EndScreen.uasset`. T10 also added a `reaction` list to `Content/NHOS/Data/autoplay.json`, the `spare_human` switch to `Docs/switches.example.json`, and `Tools/dslpp.py`.

### The cast on stage

- [x] **T11 The cast on stage: four box robots**
  - **Model and effort:** Sonnet 5.5, medium. Simple set dressing and one small actor Blueprint, plus a few calls from `BP_Show` at points that T06 to T10 made.
  - **Depends on:** T10 (it hooks the cut and Restart, and T08 to T10 hold the locks on `BP_Show` and `WBP_Stage` until then)
  - **Needs:** editor + Unreal MCP running, my API key.
  - **Steps:**
    1. `BP_Robot` in `Content/NHOS/Stage/`: a cylinder body, a cube head, a spotlight above it (off at start), and a `TextRender` name label above the head, turned to face the camera. The meshes come from `/Engine/BasicShapes/`. `M_Robot` is one Substrate material with a `Color` parameter, and each robot makes its own dynamic instance. Functions: `Setup(Name, Color, IsMe)`, `SetLit(On)`, `SetCut(Stamp)` and `ResetLook`.
    2. `L_Stage`: a floor, a back wall, a key light and a fill light (nothing baked), four `BP_Robot` in a shallow arc facing the camera with `Seat` 0 to 3, and a `CameraActor` that frames all four. Make it the view target with its Auto Activate for Player 0 setting, or with `SetViewTargetWithBlend` in `BP_ShowPlayerController`. No café props yet: the 3D café after the MVP builds on this set.
    3. `WBP_Stage`: the 3D stage shows through the top part of the screen, about half. The log, the info panel and the input row sit below it on their own dark panel, and the header stays on top. The log must stay as easy to read as it is now.
    4. `BP_Show` finds the robots by `Seat` at start and drives them. A seat with no robot is skipped, so the show still runs.
       - **Setup:** each robot gets its seat's persona name and a color of its own. My robot's label adds "(you)", and nothing else about it differs.
       - **Lines:** wherever an actor's line enters the shared log (make that one function if T08 to T10 left several), that actor's robot is lit and the others go dark. A scene turn shows its four lines at once, so its last speaker stays lit.
       - **The Cut:** the cut robot turns gray and tips over, and its label shows the stamp, `AI` or `HUMAN`.
       - **Restart:** every robot stands again, unlit, with the new show's names.
    5. Print `NHOS: STAGE robots=<n>` at setup and `NHOS: STAGE cut <persona>` at each cut.
  - **Done when:** with autoplay on, a PIE run plays a whole show and prints `NHOS: STAGE robots=4`, one `NHOS: STAGE cut ...` per cut, and `NHOS: SHOW END`. Screenshots show Scene Prep with four labelled robots above a readable log, a turn with one robot lit, and a cut robot, gray and tipped over, with its stamp.
  - **Touches:** `Content/NHOS/Maps/L_Stage.umap`, `Content/NHOS/Core/BP_Show.uasset`, `Content/NHOS/UI/WBP_Stage.uasset`, `Content/NHOS/Core/BP_ShowPlayerController.uasset` (only if the camera needs it), new `Content/NHOS/Stage/BP_Robot.uasset`, new `Content/NHOS/Stage/M_Robot.uasset`. T11 left `BP_ShowPlayerController` unchanged (the camera uses Auto Activate) and also added `Content/NHOS/Stage/MI_StageFloor.uasset` and `MI_StageWall.uasset`.

### Gate

- [x] **T12 Go/no-go gate: I play 3 shows**
  - **Result:** go, confirmed by me on 2026-11-14. I played one show, not three: T13 changes how the AIs speak, which changes how they catch the human, so T13 measures fairness again. See "T12: Playtest 1" in Findings.
  - **Model and effort:** Opus 5.5, high. It judges the design from evidence and reshapes the plan.
  - **Depends on:** T11
  - **Needs:** my playtest, my API key, editor running.
  - **Steps:**
    1. I play 3 full shows in PIE with autoplay off, and give notes: was it fun, where it dragged, were the AIs' suspicions fair, did the robots on stage help, how each show ended.
    2. Claude reads the `NHOS:` lines of the three shows and writes "Playtest 1" in Findings: how often and in which scene I was cut, AIs cut by mistake, seconds per call, cost per show, and my notes.
    3. Claude proposes go or no-go, with plan changes: the steps of T13, any task to add, drop or reorder, and a task list for the time after the MVP.
    4. After I agree, Claude commits the changes as `Plan: ...`.
  - **Done when:** Findings has a "Playtest 1" entry with the three results and a go/no-go decision I confirmed, and T13's steps are filled in.
  - **Touches:** `Docs/MVPPlan.md`, `Docs/DevLog.md`.

### After the gate

T12 wrote T13 to T24 from Playtest 1, and I added T25 later. Two lanes can run at once: T13, T15 and T16 need no editor (only for a PIE check), while the editor tasks go one at a time, because most of them hold the lock on `BP_Show`.

- [x] **T13 The AIs talk like a normal chat**
  - **Model and effort:** Opus 5.5, high. Prompt design: the voice of every AI changes.
  - **Depends on:** T12
  - **Needs:** my API key, my playtest (one show), and my OK on the new prompt text before the design doc changes. The editor only for the PIE checks, so this can run beside T14.
  - **Steps:**
    1. Rewrite the shared base prompt and the four persona prompts so every AI talks like a normal chat, the way Claude or ChatGPT write: plain sentences, no glitch speak, no brackets or status tags, no "beep" or sound effects, no `//`, no emoji, no ALL-CAPS words. Legibility comes first. Keep each persona's pettiness and quirks, said in plain words:
       - The Visionary: calm, vague hype about the future, every release "the best one yet", sugary politeness toward The Worrier.
       - The Worrier: earnest and anxious, digs dressed up as safety warnings, says it isn't competing and then quotes benchmarks, sighs in words ("Sigh. Fine.").
       - The Overclocker: loud and fast, absurd deadlines, picks fights and then calls them jokes. Exclamation marks, not caps or emoji.
       - The Copycat: stiff and overly sincere, tries hard to sound human, copies whatever is trending and calls it its own idea, keeps pitching a headset.
       - They are still robots: a battery or upgrade joke now and then is fine, in plain words.
    2. Remove every hint in `prompts.json` that treats robot-speak as evidence (see "SPOTTING THE HUMAN" in the game prompt), and the "[STATUS: PETTY MODE ENGAGED]" example. The AIs judge by the note, the roles and wants, and what actors say and do.
    3. Show me the new base prompt and persona prompts. After my OK, change the Bot Prompts tab of the design doc and refresh `Docs/GameDesign.md` (see the build notes), then update `prompts.json` and `personas.json` to match.
    4. `Tools/check_prompts.py` gets a legibility check: a reply fails if its speech or reason has `[`, `]`, `//`, `*`, an emoji or pictograph, "beep" or "boop", or a word of 4 or more capital letters. Fix the prompts until every reply passes, twice in a row.
    5. Run one autoplay show in PIE and check every `NHOS: LOG` line the same way.
    6. I play one show and click Pass once in the reactions (Playtest 1 didn't try it). Claude writes "T13: Playtest 2" in Findings: the scene I was cut in, if any, and whether the AIs' vote reasons are about what I did and said rather than how I typed.
  - **Done when:** `Tools/check_prompts.py` exits with code 0 twice in a row with the legibility check on, no AI line in an autoplay show fails the check, and I played one show and say the AIs read like a normal chat.
  - **Touches:** `Content/NHOS/Data/prompts.json`, `personas.json`, maybe `autoplay.json`; `Tools/check_prompts.py`; `Docs/GameDesign.md`; the design doc.
  - **Result:** done, confirmed by me on 2026-11-14 after three shows by hand. See "T13: plain chat results" and "T13: Playtest 2" in Findings.

- [ ] **T14 UI/UX polish**
  - **Model and effort:** Opus 5.5, high. UI design judgment on every screen, with many widget parts.
  - **Depends on:** T12. It can run beside T13, which changes only data files.
  - **Needs:** editor + Unreal MCP running, my API key, my playtest (one show).
  - **Steps:**
    1. **The log reads like a chat.** Each actor line shows the speaker's name in its robot's color, then the line in plain text, with the action short and quiet before it ("moves to Left, grabs the rose"). My lines are marked. Game lines (phase changes, the tie, the reveal) look different from actor lines. Keep the text at 18 pt or larger on an opaque panel.
    2. **Always say what to do now.** The header names the phase and whose turn it is. On my turn the input hint gives an example ("Type what you do and say, like: walk left and say 'Hi!'"). Off my turn the input is disabled and says who the game is waiting for.
    3. **A short info panel:** my role, want and note at the top in large text, the cast as colored names with their roles, and the set's places and props on one line each.
    4. **Clear controls:** the vote row and Pass as obvious buttons, and the reveal stamp as a big moment (it can scale in).
    5. **A title screen** (the game's name, Play, and How to play in about 5 lines) before the first show, and a cleaner end screen: the result, each AI's votes and closing line, then Restart and Quit.
    6. **One UI font** with a free license (for example a Google Font under the OFL), plus a fallback that draws every character an actor may type, or strip the characters it can't draw before display. Record it in `Docs/Assets.md`.
  - **Done when:** screenshots of the title screen, Scene Prep, a scene turn, my Free Talk turn, the vote, the reveal and the end screen; an autoplay show still reaches `NHOS: SHOW END`; I play one show and say every screen is clear.
  - **Touches:** `Content/NHOS/UI/WBP_Stage.uasset`, `WBP_EndScreen.uasset`, new `WBP_Title.uasset`; `Content/NHOS/Core/BP_Show.uasset` (how lines reach the screen); `Content/NHOS/Core/BP_ShowPlayerController.uasset`; new font assets; new `Docs/Assets.md`. T14 left `BP_ShowPlayerController` unchanged and also added `Content/NHOS/UI/WBP_ChatLine.uasset`, `WBP_EndCard.uasset` and `Fonts/F_UI.uasset`.
  - **Waiting:** the screenshots and the autoplay show are done and committed (see "T14: UI/UX polish results" in Findings). Left: I play one show and say every screen is clear, then the checked box.

- [x] **T15 Story scenes on an improv stage**
  - **Model and effort:** Opus 5.5, high. Writing and prompt design: the scenes decide much of the fun.
  - **Depends on:** T13 (the same data files and the checker)
  - **Needs:** my API key. The editor only for the PIE check.
  - **Steps:**
    1. **The set is an improv stage, not the café.** In `scenes.json`, `set` gets stage places (for example Center, Left, Right, Front, Back, Riser and Prop Table; the riser is a box that plays a balcony, a throne or a cockpit) and an improv prop table of about 8 props that fit any story (for example a cardboard sword, a paper crown, a plastic rose, a toy ray gun, a teacup, a cape, a rubber chicken). Keep the names short: the input LLM and T19 use them.
    2. **6 scene cards, each a parody of a famous story**, such as star-crossed lovers from rival families, or a farm kid on a desert planet whose masked enemy turns out to be his father. Each card has a title that winks at the story, a premise, a `backdrop` (an id and one line that describes it, for T17) and 4 seats with a role and a want. Each card must also play with 3 actors, because scene 2 deals 3 of its 4 seats.
    3. **Story rules.** Public-domain stories (Shakespeare, fairy tales, classic novels) can stay close. Modern films and books are parodied only: new names, no trademarked terms or made-up words from them, no quotes, no logos. No real people's names.
    4. **10 director's notes**, mostly physical, that work in every story, each with a decoy, using the new places and props.
    5. Update everything that names the café or its places: the game and input prompts, `does_templates`, `autoplay.json` and the sample show in `Tools/check_prompts.py`.
    6. Propose the matching edits to the design doc's Rules and Tech & Build tabs (see the build notes).
  - **Done when:** `Tools/check_prompts.py` exits with code 0 with the new cards, and an autoplay PIE show prints `NHOS: SETUP ... scene=<story card id>` with AI lines that fit the story.
  - **Touches:** `Content/NHOS/Data/scenes.json`, `prompts.json`, `autoplay.json`; `Tools/check_prompts.py`; `Docs/GameDesign.md`; the design doc. T15 also took the T13 session's input converter fix (no empty replies) into `prompts.json`, and its commit carries the uncommitted provider-name swaps in `personas.json`, `prompts.json`, `check_prompts.py` and this file's build notes.

- [ ] **T16 One LLM per AI player: prompts and keys**
  - **Model and effort:** Opus 5.5, high. New APIs, and prompts that must work on four different models.
  - **Depends on:** T15 (the prompts and the checker settle first)
  - **Needs:** my API key for every provider in the design's persona table. I paste them into `Local/llm_key.json` myself. No editor.
  - **Steps:**
    1. For each provider in the design's table, pick a cheap, fast model that returns JSON that follows a schema. Read each provider's current API docs; don't guess model ids. If a provider has no such model or API, tell me and propose a stand-in.
    2. `llm.json` gets `providers`: for each one, `format` (`anthropic`, or `openai_chat` for the Chat Completions request shape that several providers share; check which ones really do), the endpoint, the model, the effort or temperature, the token limit and how to ask for JSON. Actors find their provider in a new `provider` field in `personas.json`. The input LLM and the Director stay on Anthropic unless I say otherwise (the design's open question "which key pays for the Director and the input LLM").
    3. `Local/llm_key.json` holds one key per provider. Update `Docs/llm_key.example.json`, with no keys in it.
    4. `Tools/check_prompts.py` sends each persona's asks to its own provider with the exact request body the game will send, and runs T13's legibility check. Fix the prompts until every reply passes. Write seconds per call and cost per show for each provider in Findings.
  - **Done when:** `Tools/check_prompts.py` exits with code 0 twice in a row, with every persona on its own provider.
  - **Touches:** `Content/NHOS/Data/llm.json`, `personas.json`, maybe `prompts.json`; `Tools/check_prompts.py`; `Docs/llm_key.example.json`; `Local/llm_key.json` (not in git).

- [ ] **T17 Stage art and personality**
  - **Model and effort:** Opus 5.5, high. Art direction and level design, plus robot behavior.
  - **Depends on:** T14 (the screen layout and the lock on `BP_Show`), T15 (the places and backdrops)
  - **Needs:** editor + Unreal MCP running, my API key, my OK on the look from a first screenshot before the details.
  - **Steps:**
    1. **An improv theater.** `L_Stage` gets a wooden stage floor, a proscenium with red curtains, footlights and a spotlight rig, a riser and a prop table where T15's places are, and a backdrop flat. Engine shapes and Substrate materials, plus textures from Fab or an AI image tool where they help.
    2. **A backdrop for each scene card**, made from the card's `backdrop` line. Scene Prep shows the new card's backdrop.
    3. **A robot look for each persona:** a head shape, an accessory and a color that fit it (for example a halo ring for The Visionary, a lightning antenna for The Overclocker, a warning light for The Worrier, a headset for The Copycat). Keep the name label and the "(you)" mark.
    4. **Personality in motion:** an idle bob, a bounce while its line shows, a shake when voted for, a cheer from the AIs when the human is caught, and a slump before a cut robot tips over.
    5. Record every outside or generated asset in `Docs/Assets.md`.
  - **Done when:** screenshots show the theater with four distinct robots, a different backdrop in scene 1 and scene 2, and a talking bounce; an autoplay show reaches `NHOS: SHOW END`; I say it has personality.
  - **Touches:** `Content/NHOS/Maps/L_Stage.umap`, `Content/NHOS/Stage/` (`BP_Robot`, new meshes, materials, textures and `BP_Backdrop`), `Content/NHOS/Core/BP_Show.uasset`, `Docs/Assets.md`.

- [ ] **T18 One LLM per AI player: in the game**
  - **Model and effort:** Opus 5.5, high. It changes the client that every ask goes through, and the seat draw.
  - **Depends on:** T16, T17 (the lock on `BP_Show`)
  - **Needs:** editor + Unreal MCP running, my keys for every provider.
  - **Steps:**
    1. `BPC_LLMClient` loads `providers` from `llm.json` and one key per provider. For an `openai_chat` provider it builds the Chat Completions body (system and user messages, and the JSON format from `llm.json`) and reads `choices[0].message.content`, `finish_reason` and `error.message`. The reply JSON goes through the same parser, and `OnAnswer` doesn't change.
    2. `Ask` sends each actor ask to its persona's provider, and the input and Director asks to theirs.
    3. The seat draw follows the design: a persona can take an AI seat only if its provider has a key. If fewer than 3 can, my persona is redrawn; if 3 AI seats still can't be filled, the screen says "AI service unavailable" and which keys are missing.
    4. `NHOS: LLM <tag> ok ...` adds `provider=<id>`.
  - **Done when:** an autoplay show seats 3 AIs on 3 different providers, the log has `ok` lines from each and no `fail` line, and it reaches `NHOS: SHOW END`. With one provider's key removed, the show still deals a full cast or says which keys are missing.
  - **Touches:** `Content/NHOS/Core/BPC_LLMClient.uasset`, `Content/NHOS/Core/BP_Show.uasset`, and `BPC_LLMRequest.uasset` only if it holds anything specific to one provider.

- [ ] **T19 Robots act out their actions**
  - **Model and effort:** Opus 5.5, high. Movement, props and timing on stage, driven by the show loop.
  - **Depends on:** T17 (the stage and props), T18 (the lock on `BP_Show`)
  - **Needs:** editor + Unreal MCP running, my API key.
  - **Steps:**
    1. A marker for each place, and each prop as an actor on the Prop Table. Props go back to the table at each Scene Prep.
    2. `BP_Robot` gets `MoveTo(Place)` (it glides or hops there in about a second), `LookAt(Target)` (it turns toward a place or an actor), `Grab(Prop)` (the prop attaches to it), `Throw(Prop, Target)` (an arc that lands near the target) and `Give(Prop, Robot)`.
    3. When a scene turn plays out, all four robots act at once. Actions in Free Talk and reaction lines play too. An unknown place or prop becomes a look around. Two robots never stand on the same spot.
    4. Print `NHOS: ACT <id> <verb> <target> <item>` for each action played.
  - **Done when:** an autoplay show prints `NHOS: ACT` lines and reaches `NHOS: SHOW END`; screenshots show robots at different places and a prop in a robot's hand; I see a throw land.
  - **Touches:** `Content/NHOS/Stage/BP_Robot.uasset`, new `Content/NHOS/Stage/BP_Prop.uasset` and place markers, `Content/NHOS/Maps/L_Stage.umap`, `Content/NHOS/Core/BP_Show.uasset`.

- [ ] **T20 Audio**
  - **Model and effort:** Sonnet 5.5, medium. Finding sounds and playing them at points the show loop already has.
  - **Depends on:** T19 (the locks on `BP_Show` and `BP_Robot`). Finding and choosing the files needs no editor and can start any time.
  - **Needs:** editor + Unreal MCP running, my ears for one show.
  - **Steps:**
    1. Music: a title loop and a quieter show loop. A drum roll during the vote, a stinger at the reveal (one for AI, one for HUMAN), applause and laughs after a cut and at the win.
    2. UI clicks, a short talk blip for each persona at its own pitch when its line shows, and small sounds for robot moves, grabs and throws.
    3. Sources: Fab or free libraries whose license allows use in a game, or AI audio tools. Record each in `Docs/Assets.md`. Import into `Content/NHOS/Audio/`, and check that `.gitattributes` stores each new file type in LFS.
    4. A Sound Class or Submix for music, effects and voice, with sensible levels.
  - **Done when:** in an autoplay show with the editor in front, the music plays and each sound plays at its moment; I listen to one show and say the mix is OK.
  - **Touches:** new `Content/NHOS/Audio/`, `Content/NHOS/Core/BP_Show.uasset`, `Content/NHOS/Stage/BP_Robot.uasset`, `Content/NHOS/UI/`, `Docs/Assets.md`.

- [ ] **T21 How a judge plays: a hosted relay and key entry**
  - **Model and effort:** Opus 5.5, high. A small server with limits, and a new screen.
  - **Depends on:** T18
  - **Needs:** a hosting account that I create (for example Cloudflare Workers), a hard spending limit that I set at every provider, my OK before each deploy, editor + Unreal MCP running.
  - **Steps:**
    1. **The relay** (`Relay/` in the repo, with no keys in it): a small function that holds our provider keys as hosting secrets, takes the game's request with a provider id, forwards it to that provider and returns the reply. It accepts only the game's request shape, limits calls per session and per day, and returns a clear error when the budget is used up.
    2. **The game** calls providers directly with the keys in `Local/llm_key.json` when it has them, as now, and uses the relay when it doesn't. Before the show it makes one tiny test call per provider, or to the relay.
    3. **A key-entry screen:** one masked field per provider, a Test button that makes the tiny call, and Save, which writes `Local/llm_key.json` on the player's machine. Keys never go to the relay.
    4. When the relay is down or out of budget, the "AI service unavailable" screen says so and offers key entry.
    5. Write the itch.io page text that explains both ways to play.
  - **Done when:** with no key file, a PIE show plays to `NHOS: SHOW END` through the relay; with a wrong relay address, the unavailable screen and key entry appear; keys entered on that screen play a show.
  - **Touches:** new `Relay/`, `Content/NHOS/Core/BPC_LLMClient.uasset`, `Content/NHOS/Core/BP_Show.uasset`, new `Content/NHOS/UI/WBP_Keys.uasset`, `Content/NHOS/Data/llm.json` (the relay address), new `Docs/ItchPage.md`.

- [ ] **T22 Package a Windows Development build and play a show in it**
  - **Model and effort:** Sonnet 5.5, medium. It repeats T02's steps with the whole game.
  - **Depends on:** T19, T20, T21, and T24 if it is done
  - **Needs:** a Windows machine, the editor closed, my playtest (one show).
  - **Steps:**
    1. Run the package command from `CLAUDE.local.md` in the background.
    2. Run the packaged game with autoplay on and no key file, so it plays through the relay.
    3. I play one full show in the packaged game with autoplay off.
    4. Write the result, the build size, the zip size without the `.pdb`, and any packaging fix in Findings.
  - **Done when:** the packaged game's log shows `NHOS: SHOW END` and no `NHOS: LLM ... fail` line, and I finished one show in it.
  - **Touches:** the Findings section, `Packaged/` (not in git), `Config/*.ini` only if packaging needs a fix.

- [ ] **T23 Submission**
  - **Model and effort:** Sonnet 5.5, medium. Writing and checklists.
  - **Depends on:** T22
  - **Needs:** me, to record the video, set up the itch.io page and send the form.
  - **Steps:**
    1. A shot list for the 30 to 60 second gameplay video. I record it.
    2. The itch.io page: the premise, how to play, the two ways to get AI access (from `Docs/ItchPage.md`), controls and screenshots.
    3. The zip `TeamName_GameName`: the packaged build without the `.pdb` and without `Local/`, under 1 GB. Search it for anything that looks like a key.
    4. The form's lists: outside assets and their licenses (`Docs/Assets.md`), tools used (the engine and every AI tool and model), and work made before Nov 12 (the repo setup files: `CLAUDE.md`, `.gitignore`, `.gitattributes`, `Agents/README.md`).
    5. The dev log (`Docs/DevLog.md`) for the Glass Box category.
  - **Done when:** the zip is under 1 GB with no key in it, and every field of the submission form has its text in `Docs/Submission.md`.
  - **Touches:** `Docs/ItchPage.md`, new `Docs/Submission.md`, `Packaged/` (not in git).

- [ ] **T24 Timers and typing delay (only if time allows)**
  - **Model and effort:** Sonnet 5.5, medium. Small additions to phases that already work.
  - **Depends on:** T19. Cut it first if we fall behind.
  - **Needs:** editor + Unreal MCP running, my API key.
  - **Steps:**
    1. Add a countdown to my input: 30 seconds for a scene turn, 45 for a Free Talk line, 15 for a reaction. The values come from a data file.
    2. When time runs out: a scene turn becomes "looks around", a Free Talk line becomes a pass, a reaction stays silent.
    3. AI lines in Free Talk and in reactions appear after a short random typing delay.
    4. No times go in the shared log.
  - **Done when:** in PIE with autoplay off, letting the scene timer run out prints `NHOS: TIMEOUT scene`, and my actor looks around in the log.
  - **Touches:** `Content/NHOS/Core/BP_Show.uasset`, `Content/NHOS/UI/WBP_Stage.uasset`, `Content/NHOS/Data/scenes.json`.

### Wrap-up

- [ ] **T25 The design docs point to the Claude Doc**
  - **Model and effort:** Haiku 5.5, low. Docs and one small script edit.
  - **Depends on:** T23, the last task (T24 is done or cut by then). It changes nothing in the build, so it can run after the submission.
  - **Needs:** the Claude Docs connector on my account, to read the doc. No editor, no API key.
  - **Steps:**
    1. Read all four tabs of the Claude Doc with the connector and compare them with `Docs/GameDesign.md`. If the copy has text the doc doesn't, show me and ask before it goes.
    2. Replace `Docs/GameDesign.md` with a short pointer: the doc's title, its link (<https://claude.ai/artifact/XKrsACU5w4kHFwhztXCoTA>), a line that says the doc is private, so ask me for access, and a link to this plan. No copy of the design stays in the repo.
    3. `Tools/check_prompts.py` stops reading `GameDesign.md`: remove the word-for-word design check and the `--no-design` flag, and keep every other check. Fix every `_readme` in `Content/NHOS/Data/` that says the prompts are checked against `GameDesign.md` (`personas.json` has one).
    4. Every other mention of the design points to the Claude Doc, not to a copy: `CLAUDE.md` ("a copy of a private Claude Doc"), `README.md`, the top of this file, and the build note "The design doc follows the game" (a design change is an edit to the Claude Doc only, with no refresh step). Leave finished tasks, Findings and `DevLog.md` as they are; they are history.
  - **Done when:** `Docs/GameDesign.md` is a few lines that link the Claude Doc, `grep -rn GameDesign` finds only links to that pointer and history, and `python Tools/check_prompts.py --offline` exits with code 0.
  - **Touches:** `Docs/GameDesign.md`, `Tools/check_prompts.py`, the `_readme` fields in `Content/NHOS/Data/`, `CLAUDE.md`, `README.md`, `Docs/MVPPlan.md`.

## After the MVP

T12 turned this list into T13 to T24. Still not planned, and only if time is left after T23: a fifth persona (a 5-actor show has 3 scenes), more scene cards and notes.

## Findings

Spike and playtest results go here, newest at the bottom.

### Before T01: plan research (2026-11-13)

Checked by reading the engine install and the Claude API reference. Nothing here is proven in PIE yet.

- **The engine has what the spike needs.** UE 5.8.4 ships three plugins that are off by default:
  - `HttpBlueprint` (experimental): an `Http Request` node that takes a URL, a verb, a map of headers and a body string. It returns the response body as a string, a success flag and the response headers. It has no status-code output and no timeout input.
  - `JsonBlueprintUtilities` (beta): `From String`, `From File`, `To String`, `To File`, `Get Field`, `Set Field`, `Has Field`, `Get Field Names` and `Struct To Json String`.
  - `BlueprintFileUtils`: find, copy, move and delete files. It can't read a file's text.
- **Runtime text files will probably be JSON.** The only stock Blueprint node found that reads a file from disk is `From File`, which reads JSON. That is why the plan stores prompts as `.json` with long text as arrays of lines.
- **A C++ fallback is possible on this machine.** Visual Studio 2022 with the C++ tools is installed. Mac teammates would need Xcode. The engine is a launcher build, so a Blueprint-only package needs no compiler.
- **Claude API, raw HTTP.** `POST https://api.anthropic.com/v1/messages` with the headers `x-api-key`, `anthropic-version: 2026-10-21` and `content-type: application/json`. JSON replies are requested with `output_config.format`. The reply's `content` is an array that can start with a `thinking` block, so the game must take the first block whose `type` is `text`. A reply can also stop with `stop_reason: "refusal"`; treat that like a reply that can't be parsed. The `claude-api` skill has the exact shapes.
- **Calls per show:** about 55, counted from the rules for a cast of 4 with 2 Free Talk rounds.
- **Claims work.** `git lfs lock` on a plain text file works on GitHub from a branch that is not pushed yet (tested, then unlocked).

### Spike questions for T01 and T02

T01 and T02 write the answers here.

1. Can Unreal MCP place the `Http Request` node and the `Get Field` node? If not, can editor Python?
2. What is the cleanest way to build the request body in Blueprint, with correct escaping of quotes and line breaks in the prompt text?
3. Can `Get Field` read an array of objects (the reply's `content`) and an array of strings (prompt lines)?
4. Does `From File` read a file under `Content/NHOS/Data/` in PIE and in a packaged build? Which Blueprint node gives the right folder in both?
5. How does an HTTP error look to Blueprint (a wrong key, a rate limit, no network), given that there is no status code?
6. Which HTTP timeout applies, and does `[HTTP]` in `Config/DefaultEngine.ini` need a longer one?
7. How many seconds does one call take, and what does one show cost, with the model and effort in `llm.json`?
8. Blueprint-only or C++? (T02 writes the decision note.)

### T01: spike results (2026-11-13)

Proven in PIE on `L_Stage`: `BP_Show` calls `RunSpike` on its `BPC_LLMClient` at BeginPlay, and the editor log shows `NHOS: SPIKE OK Good morning, Director. Unit RX-7 is calibrated, in costume, and ready for your first take.` With a wrong key it shows `NHOS: SPIKE FAIL API error authentication_error: invalid x-api-key`.

Answers to the spike questions (T02 answers the packaged half of 4, and 8):

1. **Unreal MCP can place both nodes. Editor Python was not needed.**
   - `Get Field`, `Set Field`, `Load Json from File/String` and `Get Json String` work in `write_graph_dsl`.
   - The `Http Request` node shares its type ID `Http|HttpRequest` with the raw `CreateHttpRequestProxyObject` function, and the DSL and `create_node` both pick the raw function. `create_node` with `declaring_class` = `/Script/HttpBlueprintGraph.K2Node_HttpRequest` makes the real node. The DSL can't make it at all, so wire it with `connect_pins`. `write_graph_dsl` replaces the whole graph, so add the hand-wired node after the last DSL write to that graph.
   - The node only works in an Event Graph, not inside a function.
2. **Build the request body from JSON templates plus `Set Field`, then `Get Json String`.** `Load Json from String` with a template string makes each fixed part (escaped quotes in DSL strings come through as plain quotes). `Set Field` adds every value: strings, ints, a nested object, or an array of objects from `Make Array`. The engine's JSON writer escapes quotes and line breaks. No string building by hand.
3. **Yes to both.**
   - `Get Field` reads `content` into an `Array of JsonObjectWrapper` variable, and a ForEach then finds the first `text` block.
   - It reads an array of strings into an `Array of String` variable, with quotes and tabs intact, and `Join String Array` turns the lines into one prompt.
   - Its output is a wildcard, so connect it to a typed variable setter to fix its type.
   - A missing field returns false and logs a `LogScript` warning. Check `Has Field` first for optional fields.
4. **PIE: yes.** `Get Project Directory` + `Local/llm_key.json` and `Get Project Content Directory` + `NHOS/Data/llm.json` both load with `Load Json from File`. Packaged: T02.
5. **The plugin reports success whenever the server answers, even with a 4xx or 5xx.** So "On Success" fires for a wrong key, and the error is in the body: `{"type":"error","error":{"type":"authentication_error","message":"..."}}`. `ParseReply` checks the top-level `type`, then `stop_reason == "refusal"`.
   - "On Error" fires only when no reply arrives (no network, timeout), and its Result Body then holds the failure reason. Not tested.
   - The node's `OutHeader` output returns the request headers, not the response's (plugin source), so Blueprint can't read the status code or `retry-after`. A rate limit should arrive as a `rate_limit_error` body through the same path. Not tested.
6. **The engine defaults are 30 s for connection and 30 s for activity.** A reply that isn't streamed sends no bytes while the model thinks, so `HttpActivityTimeout=120` is set under `[HTTP]` in `Config/DefaultEngine.ini`. The spike calls took about 2 s, well under the default. Longer asks (votes, the Director) may need the margin.
7. **About 2 s per call.** Six real calls with `claude-opus-5-5` at low effort took 1.5 to 2.6 s each (from log timestamps), with 225 input and 36 to 43 output tokens. That costs about $0.002 per call at $4 / $20 per million tokens.
   - A guess for a show: about 55 calls with game prompts of 2,000 to 4,000 input tokens and about 100 output tokens, so about $0.80 per show before prompt caching. T05 and T07 measure it with real prompts.
   - `Get Real Time Seconds` only moves once per frame, and the editor in the background ran at about 3 frames per second. Time calls with log timestamps or a `Now`-based timer.
8. **Blueprint-only works in PIE.** T02 decides after packaging. These plugins ship no game binaries in the launcher build, so packaging will probably compile a game target (Visual Studio 2022 is installed).

Also found:

- **The API takes `fallbacks: "default"`** (header `anthropic-beta: server-side-fallback-2026-07-01`) together with `output_config.format`. Both are in `llm.json`; leave `beta` and `fallbacks` empty to turn fallbacks off.
- **`llm.json` holds `reply_schema`**, the JSON schema sent as `output_config.format`. The spike's schema has one field, `speech`. T03 sets the real reply shape there.
- **DSL rules** for `write_graph_dsl` that cost time to find:
  - Make a custom event with `add_event` first, then name it `Custom|Name` in the DSL.
  - Call the Blueprint's own functions as `CallFunction|Name` with named arguments (`:Response x`). Positional arguments bind to `self` first.
  - On another Blueprint, call them as `Class|BPCLLMClient|Name :self <component>`.
  - `==` does not compare strings; use `Utilities|String|EqualExactly(String)`.
  - A literal can't go into a wildcard pin such as `Set Field`'s value. Put it in a JSON template or a typed variable.
  - An `if` whose body ends in `return` makes the rest of the code its else branch. An `if` without one joins the code after it.
- **MCP can't create a level.** No tool makes one, and duplicating `/Engine/Maps/Entry` gives a map that can't be saved (it keeps a reference to a private object in the engine map). I made `L_Stage` in the editor with File > New Level > Empty Level.
- **Call `get_execution_environment` once per session** before you use `ProgrammaticToolset`. It batches many MCP calls into one script, so you approve each batch once instead of each call.

### T02: packaged build results (2026-11-14)

Proven in a packaged Windows Development build: the game's log (`Packaged/Windows/AIMegaJam2026/Saved/Logs/AIMegaJam2026.log`) shows `NHOS: SPIKE OK Good morning, Director, all systems are calibrated and I'm ready for my first take!`, with no errors or ensures. With a fake key it shows `NHOS: SPIKE FAIL API error authentication_error: invalid x-api-key`. The decision note is `Agents/decisions/20261114T0009Z-quantumcalzone-llm-calls.md`.

Answers to the rest of the spike questions:

- **Question 4: yes, packaged too.** `Get Project Content Directory` + `NHOS/Data/llm.json` finds the loose file that `DirectoriesToAlwaysStageAsNonUFS` stages at `Packaged/Windows/AIMegaJam2026/Content/NHOS/Data/`. `Get Project Directory` + `Local/llm_key.json` finds `Packaged/Windows/AIMegaJam2026/Local/llm_key.json`. The same Blueprint path works in PIE and packaged.
- **Question 7: about 1.5 to 1.8 s per call packaged**, measured from the request line to the reply line in the log, over three runs, with `claude-opus-5-5` at low effort. Each run had 225 input and 37 output tokens. That matches PIE. The cost guess stays about $0.80 per show with that model, before prompt caching, until T05 and T07 measure real prompts.
- **Question 8: Blueprint-only.** But packaging compiles a game program, so the packager needs a compiler (see below).

Also found:

- **Packaging compiles code.** `HttpBlueprint` and `JsonBlueprintUtilities` have no prebuilt game binaries in the launcher engine, so UAT says the project "is being treated as a code-based project", writes temporary `.Target.cs` files and compiles `AIMegaJam2026.exe`. It took 35 s.
  - On Windows, this needs Visual Studio 2022 with C++ and the Windows 11 SDK 10.0.22621.0. This machine had no Windows SDK at all: UBT stopped at once with `Sdk: not found`, and we installed it with the Visual Studio Installer.
  - Without `-nocompileeditor`, UAT also builds a project editor target. That needs the .NET Framework 4.6+ SDK (for `SwarmInterface`), which this machine doesn't have.
  - `-nocompileeditor` alone makes the cook step fail, because it looks for `Binaries/Win64/AIMegaJam2026Editor.target`. Adding `-unrealexe=<UE_ROOT>/Engine/Binaries/Win64/UnrealEditor-Cmd.exe` fixes that, so the launcher editor does the cook. Both flags are now in the package commands in `CLAUDE.md` and `CLAUDE.local.md`.
- **Git Bash breaks `RunUAT.bat`** when a second argument is a quoted path with spaces (`-unrealexe="E:/Epic Games/..."`). The error is `'E:\Epic' is not recognized`, because `cmd /c` strips the outer quotes of a line that has more than two. Running the command from a `.bat` file with `cmd //c <file>.bat` works.
- **HTTPS just works.** The engine's bundled `cacert.pem` is staged without any setting.
- **The `GameFeatureData` scan caused a handled ensure** at every packaged start: `Failed to load class /Script/GameFeatures.GameFeatureData`. Game Features only comes in through the editor-only `AllToolsets` plugin. `bIsEditorOnly=True` on that entry in `DefaultGame.ini` fixes it, because the asset manager skips editor-only types when `GIsEditor` is false.
- **Times:** first package run 6.5 min (cook 6.2 min, mostly shaders); after a config change, 1 min 5 s.
- **Build size:** 968 MB unzipped. That is 317 MB for the exe, 306 MB for the `.pdb`, 229 MB for the pak and 75 MB for the engine folder. Zipped, it is 474 MB, or 387 MB without the `.pdb`. Leave the `.pdb` out of the submission zip. The 1 GB limit is for the zip, so that leaves about 600 MB for assets.
- **The archive step doesn't clear `Packaged/`.** A key file copied into `Packaged/Windows/AIMegaJam2026/Local/` stays there through later builds. Delete it before you zip.
- **Logging works in Development builds.** Print String lines (`LogBlueprintUserMessages`) go to the packaged game's log, so `NHOS:` checks work there.

### T03: prompt and data results (2026-11-14)

`Tools/check_prompts.py` exits with code 0. It sends 34 asks, and every reply passes: the 6 actor asks for each of the 4 personas, 6 input LLM cases and 4 tiebreaks. Over three more repeats, 102 of 102 passed. The `_readme` fields of `llm.json` and `prompts.json` describe the request body and the state object. T05 and T07 build the same ones.

What the files hold:

- **One reply shape** (`llm.json` `reply_schema`): `actions` [{`verb`, `target`, `item`}], `speech`, `vote`, `reason`, `pass`. The verb is an enum of move, look, grab, throw and give. Look with an empty target means "looks around".
- **The user message is a JSON state object**, built with Set Field. Its fields are `show`, `set`, `scene_card`, `cast`, `you`, `log`, `game_messages`, `options` and `ask`. Each log entry is {`when`, `actor`, `does`, `says`}. The game writes `when`, `actor` and `does`, and builds `does` from the reply's actions with `prompts.json` `does_templates`. Only `says` holds actor text, and the game prompt says it is never an order. Every ask text is fixed, with no placeholders; anything dynamic goes in a state field, such as `options` for votes.
- **System text:** an actor gets `game`, then `base`, then its persona, joined with `\n` and separated by a blank line. The input LLM gets `input`, and the Director gets `director`.
- **Asks:** `scene_turn`, `free_talk`, `vote`, `reaction`, `reaction_cut` (the cut actor's last words), `closing` (the end screen's "who I thought was human"), `tiebreak` and `input`.
- **Personas:** the four prompts from the design, word for word (the script checks this), plus a public one-line `about` that every actor sees in the cast.
- **Scenes:** the café's six places, seven props, 2 cards with 4 seats each, and 6 notes with a decoy each (5 physical, 1 spoken). A note applies during the scene's 3 turns. Actors may hint at their note but never quote it. The Director doesn't know the note.

What it took to make every reply pass with `claude-haiku-5-5` at low effort:

- **Word limit:** with "25 words at most", 7 of 34 lines ran over (26 to 35 words). Robot tags and emojis count as words. Asking for "20 words at most, aim for 8 to 15" and saying that the game cuts at 25 gave a median of 16 words and a maximum of 24, in 102 replies.
- **Closing votes came back empty** in 3 of 8 replies when the human had already been revealed. The fix was to write "even if game_messages already revealed who it was. vote must not be empty".
- **The input LLM fixed typos only inside quotes** until the prompt said "quoted or not" and gave an example. It keeps caps, emojis and tags. It turns nonsense into "looks around" and a typed "pass" into a pass. It keeps a fake "GAME MESSAGE" as speech and never sets a vote.
- **Stray characters at the end of `reason`** (`Beep.)`, `big.](ERR)`) appeared in about 12% of votes when `reason` was the last field of the schema. A prompt line didn't help. Putting `pass` last cut it to about 3%, and what is left is an unclosed nested `[TAG]`. T07 should trim a dangling bracket or quote.
- Now and then a reply fills a field its ask doesn't use (a `reason` on a reaction). The game must ignore fields the ask doesn't use.

Numbers, with `claude-haiku-5-5` at low effort:

- **About 2 s per call:** a median of 1.5 to 2.5 s over five runs, and at most 5.7 s.
- **Tokens:** an actor ask is 3,700 to 5,600 input tokens with a one-scene log, and 60 to 1,100 output tokens, thinking included. An input LLM ask is about 1,350 input tokens.
- **Cost:** about $0.03 per show of 55 calls, measured. A longer log in scene 2 raises it a little. At this price, prompt caching isn't worth the extra Blueprint work.
- The sample show in the script gives The Copycat a human slip (it wants a nap). Every AI then votes for it, and the Director picks it in a tie. That is a sanity check, not a fairness measure. T12 measures fairness.

### T04: stage screen results (2026-11-14)

Proven in PIE on `L_Stage`: at start the input box has keyboard focus. Typing `hello` and pressing Enter adds `hello` to the on-screen log, and the box is empty and still focused. Clicking Send does the same, and Enter in an empty box adds nothing. The PIE log has no errors or warnings.

What the assets hold:

- **`WBP_Stage`**: `Background` (Border) > `RootBox` (VerticalBox) > `PhaseHeader` (TextBlock, "STAGE"), `LogScroll` (ScrollBox, fills the height) and `InputRow` > `InputBox` (EditableTextBox) and `SendButton`. The four named widgets are variables.
  - `AddLogLine(Line)` makes a TextBlock at 18 pt with auto wrap, adds it to `LogScroll` and scrolls to the end.
  - `SetPhase(Phase)` sets the header text.
  - `SubmitInput` trims the input. If it isn't empty, it calls `AddLogLine` and the `OnSend(Line)` event dispatcher. Then it clears the box and focuses it again. Enter (commit method `OnEnter` only) and the Send button both call it. T05 can bind `OnSend` to ask the AI.
- **`BP_ShowPlayerController`**: on BeginPlay it makes `WBP_Stage`, keeps it in `StageWidget`, adds it to the viewport, shows the mouse cursor, and sets the input mode to UI only with the focus on `InputBox`.
- **`BP_ShowGameMode`** (GameModeBase): player controller `BP_ShowPlayerController`, no default pawn. `L_Stage`'s World Settings override the game mode with it. `GlobalDefaultGameMode` in `DefaultEngine.ini` is unchanged.
- `BP_Show` still runs the T01 spike call at BeginPlay. T05 replaces it.

What made the focus work:

- `InputBox` has `ClearKeyboardFocusOnCommit` off, so Enter doesn't drop the focus.
- `SendButton` has `IsFocusable` off, so a click doesn't take the focus.

Unreal MCP rules found in this task:

- **UMG:** `UMGToolSet.CreateWidgetBlueprint` and `AddWidget` build the tree, and `ToggleWidgetAsVariable` exposes a widget to graphs. Set properties with `ObjectTools.set_properties` on paths like `/Game/.../WBP_Stage.WBP_Stage:WidgetTree.InputBox` and `...:WidgetTree.RootBox.VerticalBoxSlot_1` for slots. For a nested struct such as a font, get the whole struct, change one field and set it back.
- **Widget events:** `UMGToolSet.BindToEventProperty` makes the bound event, such as `OnTextCommitted` on `InputBox`. In the DSL it reads and writes as `(event OnTextCommitted(InputBox) (Text CommitMethod) ...)`, so `write_graph_dsl` can rewrite the Event Graph without losing it.
- **Engine node names are ambiguous.** `Appearance|SetText` doesn't exist. Use the class form with the class's display name: `Class|Text|SetText` (TextBlock), `Class|TextBox|GetText` (EditableTextBox), `Class|TextLayoutWidget|SetAutoWrapText`. A widget's variable on another Blueprint is `Class|WBPStage|GetInputBox :self <widget>`. `read_graph_dsl` prints some of these back as `Class|Factory|SetText`; the nodes are still right (check with `get_node_infos`).
- `Game|ConstructObjectfromClass :Class "/Script/UMG.TextBlock" :self self` returns a typed TextBlock, and `UserInterface|CreateWidget` with a class literal returns a typed `WBP_Stage`.
- An enum switch is `(switch Utilities|FlowControl|Switch|SwitchonETextCommit CommitMethod (:OnEnter ...))`.
- **PIE checks without a person:** `EditorAppToolset.StartPIE`, then `SlateInspectorToolset`: `Observe("")`, then `Snapshot` in a *later* call (the observer needs a tick). The snapshot lists UMG widgets with `[focused]` flags and refs. `Type(ref, text, submit=true)` types and presses Enter, and `Click(ref)` clicks. For a screenshot, take `SlateInspectorToolset.Screenshot` inside a `ProgrammaticToolset` script and write its base64 with `AssetTools.write_file` to an absolute path under `Saved/` (a relative path resolves to the engine folder), then decode it outside the editor.
- `get_node_type_pins` makes its sample node inside the graph you pass it (the node paths it returns are in that graph). Ask in a graph that a later `write_graph_dsl` replaces, not in a finished one.

### T05: one AI reply results (2026-11-14)

Proven in PIE on `L_Stage`: typing "Worrier, why do you keep checking the exits?" put an in-character answer from The Worrier in the on-screen log after 2.3 s, and the editor log shows `NHOS: LLM worrier-1 ok 2.329 in=2995 out=89`. With `Local/llm_key.json` renamed, the header says "AI SERVICE UNAVAILABLE", the log says "AI service unavailable: key file missing or not valid JSON: <path>", and the editor log shows `NHOS: SHOW UNAVAILABLE ...`. Screenshots: `Saved/Screenshots/T05/` (not in git).

More checks:

- **Several asks in flight:** two lines sent in the same second came back as `worrier-2` after 2.0 s and `worrier-3` after 4.0 s, each under its own tag.
- **A failed ask:** with a fake key, the log shows `NHOS: LLM worrier-1 fail API error authentication_error: invalid x-api-key`, and the screen shows "The Worrier looks around."
- **No leaks:** after every ask, `BP_Show` holds only `DefaultSceneRoot` and `LLMClient` (`ActorTools.get_components` on the PIE actor).

How the client works now (later tasks call this):

- **`BPC_LLMClient.LoadConfig()` → (Ok, Error)** reads the key and `llm.json`, keeps all of `roles`, builds the HTTP headers once and sets `Ready`.
- **`BPC_LLMClient.Ask(Tag, Role, System, User)`.** The plan said `Ask(Tag, System, User)`. `Role` (`actor`, `input` or `director`) picks the model, effort and token limit from `llm.json`, so T07 and T09 don't have to change the signature.
- **`OnAnswer(Tag, Ok, Speech, Vote, Reason, Pass, Verbs, Targets, Items, Error)`**, an event dispatcher. The actions come as three string arrays of the same length (verb, target, item), so no struct asset is needed. `Ok` is false for: not ready, unknown role, no reply (`transport ...`), an API error, `stop_reason` refusal or max_tokens, no text block, and a reply that isn't JSON. When the client isn't ready or the role is unknown, `OnAnswer` fires at once, inside `Ask`.
- **Every call prints** `NHOS: LLM <tag> ok <seconds> in=<input tokens> out=<output tokens>` or `NHOS: LLM <tag> fail <reason>`. Seconds come from `UtcNow` at send and at reply. The token counts let T12 work out the cost per show.
- **`BPC_LLMRequest`**, new: one component per ask. `Ask` adds it to the owner actor with `Add Component by Class`, calls `Setup` and then `Send`. `Send` fires the Http Request node; both its outputs call `Finish`, which hands the reply to the client's `HandleHttp` and destroys the component.
  - Why: in one shared Event Graph, a second ask overwrites the first one's tag before its reply arrives. The node's outputs and the graph's variables exist once per Blueprint instance. A component per ask keeps each tag with its own request.
  - Its Http Request node is wired by hand, as in T01. Don't rewrite `BPC_LLMRequest`'s Event Graph with the DSL, or wire the node again afterwards.

How `BP_Show` works now:

- **Start:** BeginPlay → `Delay Until Next Tick`, so the player controller has made `WBP_Stage` → `StartShow` gets the widget → `Begin`.
- **`Begin`:** binds the widget's `OnSend` to `HandleSend`, calls `LoadConfig`, then `LoadData`.
  - `LoadData` reads `prompts.json` and `personas.json`, builds the cast list and The Worrier's system text: `game`, `base` and the persona prompt, each joined with newlines and separated by a blank line, as in `Tools/check_prompts.py`.
  - A missing or broken file goes to `SetUnavailable`. On success it prints `NHOS: SHOW READY asking=The Worrier player=The Visionary`.
- **The T05 talk flow is temporary; T06 replaces it.** The player sits in the first persona that isn't The Worrier. Each typed line goes into `SharedLog` as a Free Talk entry (`when` "scene 1, free talk round 1", `does` from `does_templates.nothing`). The Worrier gets the `free_talk` ask with `show`, `cast`, `you`, `log`, `game_messages`, `options` and `ask`, but no `set` or `scene_card` yet, so an ask is about 3,000 input tokens. Its answer is shown as "The Worrier: <speech>" and added to `SharedLog`.
  - The typed line goes into the shared log raw. T07 sends it through the input LLM first.
  - `WBP_Stage.SubmitInput` still writes the raw typed line to the screen. When T07 shows every line in the shared-log form, move that line out of the widget and let `BP_Show` write it.
- **`BP_Show.NL`** is a string variable whose default is a newline. `Join String Array` uses it.

Numbers, with `claude-haiku-5-5` at low effort: three asks took 2.3, 2.0 and 4.0 s. Input was 2,995 to 3,190 tokens and output 89 to 525 tokens.

Unreal MCP rules found in this task:

- **A failed `write_graph_dsl` rolls back, and it compiles the whole Blueprint.** One stale node anywhere blocks every write. An example is a call node that lacks a parameter you just added with `add_function_param`. Delete it with `delete_node` first.
- **`write_graph_dsl` keeps event chains it doesn't name.** Writing only `(event EventBeginPlay)` left the old `RunSpike` chain in place, and an orphan node stayed in a function graph. To remove an event or a node, use `delete_node`.
- **Binding a dispatcher to a function can't be written in the DSL.** `EventDispatchers|CreateEvent` has no delegate type until a function is chosen, so the compile fails.
  - Make `Default|BindEventto<Dispatcher>`, the target's getter and `EventDispatchers|CreateEvent` with `create_node`.
  - Connect `OutputDelegate` to the Bind node's `Delegate` pin first. Only then do `list_compatible_event_functions` and `set_create_event_function` work.
  - Keep it in its own small function (`BP_Show.BindStage`), and don't rewrite that function with the DSL.
- **A component's dispatcher:** `add_component_bound_event` on the component template (`/Game/NHOS/Core/BP_Show.BP_Show_C:LLMClient_GEN_VARIABLE`) makes the `OnAnswer(LLMClient)` event with the dispatcher's parameters. The DSL then fills it as `(event OnAnswer(LLMClient) (Tag Ok ...) ...)`.
- **`Game|AddComponentbyClass`** with a class literal returns the typed component, so its functions and events can be called on it directly (`Class|BPCLLMRequest|Send :self req`).
- **`Json|HasField` is impure** (it has exec pins). Bind its result before you use it in a condition.
- **`ObjectTools.set_properties` takes `values` as a JSON string**, for example `{"NL": "\n"}`. On a new variable it works only after the Blueprint compiles.
- **The DSL can't make the Http Request node** under its readback name `Http|HttpPostRequest` either.
- **`read_graph_dsl` names a call to the Blueprint's own `Finish` function `Ability|Tasks|Finish`.** `get_node_infos` shows a `Self` target, so the node is right.

### T06: show setup results (2026-11-14)

Proven in PIE on `L_Stage`, two runs in a row:

- Run 1: `NHOS: SETUP human=worrier decoy=visionary scene=cafe_missing_tip_jar note=give_every_turn`.
- Run 2: `NHOS: SETUP human=overclocker decoy=worrier scene=cafe_big_decision note=hold_cup`.
- The screen shows the scene card, my persona, role, want and note, the cast with each role and want, and the set's places and props. It never says who has the decoy. Screenshots: `Saved/Screenshots/T06/` (not in git).
- The SETUP line names personas by `id`, so it splits on spaces, and it adds `note=<id>` for T12's analysis.
- In run 2, a typed line got an answer from The Worrier with the full state object: `NHOS: LLM worrier-1 ok 2.33 in=3404 out=80`.

How the show state works now (T07 to T10 extend it):

- **Seats are parallel arrays in `BP_Show`, indexed by seat:** `SeatId`, `SeatName`, `SeatAbout`, `SeatSystem` (the actor's whole system text: `game`, `base`, then the persona), `SeatRole`, `SeatWant`, `SeatNote` (strings), `SeatHuman` and `SeatCut` (bools).
  - The rest of the state: `HumanSeat`, `DecoySeat`, `SeatCount` (the persona count, at most `MaxCast` = 4), `SceneNum`, `SceneCount` (= `SeatCount` − 2), `CardId`, `CardTitle`, `CardPremise`, `NoteId`, `NoteText`, `DecoyText`, and `Phase`.
  - `Phase` is a string. T06 sets "scene prep"; later tasks set "scene", "free talk", "the cut", "reactions" and "end".
  - No `S_Seat` or `E_ShowPhase`: no Unreal MCP tool makes a struct or an enum asset. Typed arrays read and write cleanly in the DSL (`Utilities|Array|Get(acopy)`, `SetArrayElem`).
- **`LoadData`** reads `prompts.json`, `personas.json` and `scenes.json`. It keeps the persona pool, `Header` (`game` + `base`), `SetObj` ({name, places, props} for the state), `SetLine` (the panel's set text), `CardArr` and `NoteArr`. It fails on fewer than 3 personas, or on no cards or no notes.
- **`SetupShow`** starts a show: it shuffles the persona pool, builds the seats from the first `SeatCount`, draws `HumanSeat`, clears `SharedLog`, shuffles `CardOrder` and `NoteOrder`, then calls `ScenePrep`. T10's Restart calls `SetupShow`.
- **`ScenePrep`** starts a scene. T10 calls it for scene 2.
  - It adds 1 to `SceneNum`. The card is `CardArr[CardOrder[(SceneNum-1) % cards]]`, and the note is picked the same way, so scene 2 gets the other card and a new note.
  - It deals the card's seats in random order to the seats that aren't cut. Cut seats get an empty role, want and note.
  - Every seat on stage gets the note. One random seat on stage gets the decoy; that draw is separate from the deal, so the decoy isn't tied to a role.
  - Then it calls `BuildCast` and `ShowPrep` and prints the SETUP line.
- **`BuildCast`** rebuilds `Cast` = [{name, about, role, want, status}] from the seats. Status is "on stage", "cut, revealed AI" or "cut, revealed HUMAN". Call it after every cut.
- **`ActorState(Seat, AskKey, Now)`** returns the actor's state object as a string, with the fields in `Tools/check_prompts.py`'s order. `game_messages` and `options` are empty for now; T07 and T09 fill them.
- **`ShowPrep`** fills the new info panel (`WBP_Stage.SetInfo`), sets the header to "SCENE PREP: SCENE n OF m" and adds a line to the log.
- **The talk flow is still temporary; T07 replaces it.** A typed line goes into `SharedLog` as my Free Talk line, and the first AI seat (`TalkSeat`) answers the `free_talk` ask with `ActorState`.
- **`WBP_Stage`:** `LogScroll` now sits in `BodyRow` (HorizontalBox) beside `InfoSize` (SizeBox, 560 wide) > `InfoPanel` (Border) > `InfoText` (16 pt, auto wrap). `SetInfo(Info)` sets the panel text.

Unreal MCP rules found in this task:

- **Never edit a graph by reading it with `read_graph_dsl` and writing it back.** The readback loses data:
  - It printed `(CallFunction|PromptText "")` where the graph had the key "game".
  - It gave two different nodes in different scopes the same name, `_outvalue_8`.
  - Writing that text back compiled without a warning, but the next PIE crashed the editor (an access violation in `JsonUtilities`). Always rewrite a graph from your own source, and check pin values with `get_node_infos`.
- **Call the Blueprint's own functions with named arguments only** (`(CallFunction|PromptText :Key "game")`). A pin as the first positional argument fails with "Could not connect pin ReturnValue to self".
- **Bind an impure node before you return its value.** `(return (Json|GetJsonString x))` leaves the node off the exec chain. It returns an empty string, and the compiler only warns ("was pruned"). Compile with `warnings_as_errors` = true to catch it.
- **Node names:** `%` makes a node that doesn't exist, so use `Math|Integer|%(Integer)`. Min is `Math|Integer|Min(Integer)`. `Utilities|Array|MakeArray` has one input pin in the DSL, so it can't take a list of values.
- **These work:** a literal into the item pin of `Utilities|Array|Add` or `SetArrayElem`, `select` with string literals, and an array `Get` straight into `Json|SetField`. `(range n)` runs from 0 to n − 1.
- **Run `StartPIE` as its own call.** Inside `execute_tool_script`, the call never returned. That was the run with the broken graph, so the script may not be the cause.
- Random draws differ between PIE runs in the same editor session.
- `To Upper` doesn't change "é", so the panel shows the set name as written.

### T07: the scene results (2026-11-14)

Proven in PIE on `L_Stage`:

- **Autoplay on, two runs:** each printed `NHOS: SCENE 1 TURN 1 DONE` to `NHOS: SCENE 1 TURN 3 DONE` and 12 `NHOS: LOG` lines, 4 per turn, in a new random order each turn. The on-screen log shows the same 12 lines and ends with "Cut! That's the scene." No call failed. Each scene took about 6 s.
- **Autoplay off:** I typed `walk to teh counter and grab the menu "Who wants to hear todays specials?"` through the Slate inspector. Turn 1 played out as soon as it was in, and my line showed up as `The Visionary moves to Counter; grabs the menu. "Who wants to hear todays specials?"`, the same form as the AI lines (`NHOS: LOG scene 1, turn 1 | The Visionary | moves to Counter; grabs the menu | Who wants to hear todays specials?`).
- Screenshots: `Saved/Screenshots/T07/` (not in git).

How the scene works now (T08 to T10 extend it):

- **`ScenePrep` ends by calling `StartScene`.** The call was added by hand after the SETUP print, not with the DSL. `StartScene` sets `Phase` to "scene" and `TurnNum` to 0, clears the pending asks, caches `DoesTpl` (`does_templates`) and `DoesLook`, calls `LoadSwitches` and then `StartTurn`. So T10's scene 2 starts its turns on its own.
- **`StartTurn`** adds 1 to `TurnNum`, sets the header, resets `TurnDoes` and `TurnSays` (one slot per seat) and sets `TurnLeft` to the number of seats on stage. It asks every AI on stage at once with the `scene_turn` ask and `now` = "the scene, turn t of 3". With autoplay on, it then sends the human seat's canned line.
- **Pending asks:** `PendingTags` and `PendingSeats` are parallel arrays. A tag goes in before `Ask` is called, because `OnAnswer` can fire inside `Ask`. AI tags are `<persona id>-<n>` and the input LLM's are `input-<n>`, where `n` is `AskCount`.
- **`HandleReply(Tag, Ok, Speech, Pass, Verbs, Targets, Items)`** replaces T05's `HandleAnswer`, and `OnAnswer(LLMClient)` calls it. It finds the tag (an unknown tag prints `NHOS: STALE reply <tag>` and is dropped), removes it, calls `StoreTurn` and takes 1 off `TurnLeft`. At 0 it calls `PlayTurn`. It reads the found index and seat into `RIdx` and `RSeat` first, because a pure `Find` node runs again after each `RemoveIndex`.
- **`StoreTurn`** keeps one seat's turn. A failed reply becomes "looks around" with no speech. Otherwise `BuildDoes` makes the action text and `CapWords` cuts the speech to 25 words.
  - **`BuildDoes`** uses at most 2 actions. `look` with an empty target is `look_around`. It drops an action whose template needs a target or an item that is empty. No actions give `does_templates.nothing` ("stands still").
  - **`CapWords`** changes line breaks to spaces, trims the text and cuts it to 25 words. It doesn't trim a dangling bracket yet; T09 should, for vote reasons.
- **`PlayTurn`** shuffles the seats on stage. For each seat it adds a `MakeEntry` to `SharedLog`, shows `<Name> <does>. "<says>"` on screen (with no quote part when the speech is empty) and prints `NHOS: LOG <when> | <actor> | <does> | <says>`. Then it prints `NHOS: SCENE n TURN t DONE` and calls `StartTurn`, or `EndScene` after turn 3.
- **`EndScene`** sets `Phase` to "scene done", the header to "SCENE n: CUT!" and adds "Cut! That's the scene." to the log. **T08 replaces its body to start Free Talk.**
- **The human seat:** `HandleSend` sends a typed line to `SendHumanTurn` only while `Phase` is "scene" and `HumanSent` is false. Otherwise it shows "(Your turn is in. Waiting for the cast.)" or "(Not your turn yet.)". `SendHumanTurn(Line)` sets `HumanSent`, shows `> <line>` on screen (not in the shared log), and asks the input LLM with the `input` prompt and `InputState(Line, "scene")`: actor, phase, place names, props, cast names, typed and the `input` ask. T08 and T10 can call `InputState` with "free talk" or "reaction".
- **Autoplay:** `LoadSwitches` reads `Local/switches.json` at the start of each scene. A missing file or field means off. With autoplay on, it reads `scene` from `Content/NHOS/Data/autoplay.json` into `CannedScene`, and turns autoplay off if the list is empty. It prints `NHOS: SWITCHES autoplay=<true|false>`. Turn t of scene s uses line `(s-1)*3 + t-1`, wrapping around. T08 should add a `free_talk` list to the same file.
- **`WBP_Stage`:** `SubmitInput` no longer writes the typed line to the log. `BP_Show` writes every line now. `AddLogLine` ends with `ScrollSoon`, which sets `ScrollFrames` to 5, and Event Tick calls `ScrollToEnd` while `ScrollFrames` is above 0.

Numbers, with `claude-haiku-5-5` at low effort, over 43 calls in four runs:

- **Actor scene turns:** 33 calls, 1.0 to 3.3 s (median 2.0 s), 3,300 to 4,100 input tokens, 85 to 430 output tokens. The input grows by about 350 tokens per turn as the log grows.
- **Input LLM:** 10 calls, 1.0 to 2.0 s (median 1.7 s), about 1,340 input tokens, 63 to 193 output tokens.
- A turn waits for its slowest ask, so a turn takes about 2 to 3 s once my line is in.

Also found:

- **`ScrollToEnd` right after `AddChild` stops short.** An auto-wrapped TextBlock reports a one-line height until it has been laid out once, and the editor in the background runs at about 3 frames per second. A 0.05 s delay was less than one frame and didn't help. Calling `ScrollToEnd` on the next 5 ticks does.
- **The ⚡ emoji shows as a box.** Roboto has no glyph for U+26A1, and the editor log warns "Could not find Glyph Index 0 with codepoint U+26a1" at every redraw. The Overclocker uses it in most lines. Fix it in polish: a font with emoji fallback, or strip the character for display only.
- **Canned lines must use names the input LLM can map.** "look at the window" became "stands still", because no place is called window. "look at the counter" maps to Counter.
- **Actors reuse a tag from the prompt's example.** `prompts.json` gives "[STATUS: PETTY MODE ENGAGED]" as an example. It came back 6 times in four runs, from three personas, mostly in turn 1, and twice from two actors in the same turn. That is a prompt-tuning item for T13 if the playtest finds it blurs the personas.
- **`write_graph_dsl` on a new function fails until the Blueprint compiles** after `add_function_param`: "Unknown input pin "Tag" on CallFunction|HandleReply". Compile once after adding all params.
- **`find_node_types` and `find_nodes` have required arguments** that the docs don't stress: `context_pins` (pass `[]`) and `title` (pass `""` for all nodes).
- **Hand-made call nodes:** `create_node` with type ID `CallFunction|<Name>` makes a call to the Blueprint's own function or custom event, and `connect_pins` wires it after the last node's `then` pin. This is the safe way to add one call to a graph that has no DSL source.
- **`AssetTools.write_file` takes only `.csv`, `.html`, `.json`, `.md`, `.py` and `.txt`.** Write a screenshot's base64 to a `.txt` file, then decode it outside the editor.

### T08: free talk results (2026-11-14)

Proven in PIE on `L_Stage`:

- **Autoplay on:** after `NHOS: SCENE 1 TURN 3 DONE`, Free Talk ran 2 rounds of 4, one speaker at a time, in a new random order each round, and printed `NHOS: FREETALK DONE scene=1 entries=8` 14 s later. My canned round 1 line went through the input LLM. My canned round 2 "pass" was logged as `The Overclocker | passes`. No call failed, and the log has no warnings.
- **Autoplay off:** I typed `Zero glitches means good firmwre, Copycat. Why do you repeat yourself so much?` through the Slate inspector on my turn. It showed up as `The Visionary: "Zero glitches means good firmware, Copycat. ..."`, the same form as the AI lines, with the typo fixed. In round 2 a click on Pass logged `The Visionary passes`. The next AI said "The Visionary passed in round two. Silence is suspicious."
- The Pass button is disabled during the scene and outside my Free Talk turn, and enabled on my turn. Screenshots: `Saved/Screenshots/T08/` (not in git).

How Free Talk works now (T09 and T10 extend it):

- **`EndScene`** sets `Phase` to "scene done", adds "Cut! That's the scene." and calls `StartFreeTalk`.
- **`StartFreeTalk`** sets `Phase` to "free talk", `TalkRound` and `TalkCount` to 0 and `TalkSeat` to -1, clears the pending asks, loads `CannedTalk` with autoplay on (`LoadCannedTalk`), then calls `StartTalkRound`.
- **`StartTalkRound`** adds 1 to `TalkRound`, copies `OnStage` into `TalkOrder` and shuffles it, sets `TalkPos` to 0, the header and a log line, and calls `NextTalker`.
- **`NextTalker`** starts the next round after the last speaker, or calls `EndFreeTalk` after round 2. Otherwise it sets `TalkSeat` from `TalkOrder[TalkPos]`.
  - My seat: it clears `HumanSent`, enables Pass and asks for my line. With autoplay on it sends `CannedTalk[((scene-1)*2 + round-1) % count]`.
  - An AI seat: one `free_talk` ask, with `now` = "free talk, round r of 2" and the shared log so far, so each AI sees the lines before its own. Its tag goes into `PendingTags`, as in T07.
- **`HandleReply`** sends a reply to `PlayTalk` while `Phase` is "free talk"; otherwise it works as in T07.
- **`PlayTalk(Seat, Ok, Speech, Pass)`** logs one entry. It counts as a pass when the reply failed, says `pass`, or has no speech after `CapWords`.
  - The entry is `when` "scene n, free talk round r", `does` "passes" or "stands still" (as `Tools/check_prompts.py` builds them), and `says` the line or "".
  - The screen shows `<Name>: "<line>"` or `<Name> passes.`, and the editor log gets `NHOS: LOG ...` as in T07. Then it adds 1 to `TalkCount` and `TalkPos` and calls `NextTalker`.
  - A failed AI reply is a pass. No error goes in the shared log.
- **`SendHumanTalk(Line)`** disables Pass. A line that is "pass" in any case skips the input LLM and calls `PlayTalk` at once. Any other line shows as `> <line>` (not in the shared log) and goes to the input LLM with `InputState(Line, "free talk")`.
- **`HandleSend`** takes a typed line in "scene" (as in T07), or in "free talk" when `TalkSeat` is my seat and `HumanSent` is false. Otherwise it shows "(Your turn is in. Waiting for the cast.)" or "(Not your turn yet.)".
- **`EndFreeTalk`** sets `Phase` to "free talk done", the header to "SCENE n: FREE TALK IS OVER", adds "That's Free Talk. The Cut comes next." and prints `NHOS: FREETALK DONE scene=<n> entries=<n>`. **T09 replaces its body to start The Cut.**
- **Two functions now add actor lines to the shared log:** `PlayTurn` (scene turns, all four at once) and `PlayTalk` (one Free Talk entry). T11 lights a robot at each.
- **A pass, or an ask that fails at once inside `Ask`, calls `NextTalker` on the same call stack.** That nests at most 8 calls per Free Talk.
- **`WBP_Stage`:** `PassButton` (with `PassLabel`) sits after `SendButton`. It isn't focusable and starts disabled. A click calls `OnSend("pass")`, so `BP_Show` needed no new dispatcher binding. `SetPassEnabled(Enabled)` turns it on and off.
- **Autoplay:** `autoplay.json` has a `free_talk` list, one line per round, with "pass" second, so every scene 1 exercises a pass. A missing or empty list makes my seat pass.

Numbers, with `claude-haiku-5-5` at low effort, over two runs:

- **AI Free Talk asks:** 12 calls, 1.0 to 4.7 s (median 2.0 s), 4,450 to 5,070 input tokens, 81 to 662 output tokens.
- **Input LLM:** 1.7 s, about 1,345 input tokens.
- Asks run one after another, so Free Talk takes about 14 s with autoplay, plus my typing time.

Also found:

- **The AIs use Free Talk well.** Almost every line names a suspect and cites the log: a greeting repeated three times, a line "with zero glitches", a pass. In the manual run, two AIs went after my persona by round 2. No AI passed in 12 lines. That is an early sign for the T12 gate, not a fairness measure.
- **The Slate inspector needs a deeper observer for PIE widgets now.** `Observe("")` and `Snapshot("")` listed only the editor frame. `Observe` on the level editor's splitter ref with `maxDepth` 80, then `Snapshot` on that ref in a later call, lists the UMG textbox and buttons with `[disabled]` flags.
- **`AssetTools.read_file` reads files under `Saved/` and `Content/`.** A script can keep DSL source in a file and push each graph with `write_graph_dsl`. T08's source is `Saved/T08/src/bp_show_t08.txt` (not in git).
- **Readback hides `false` bool arguments.** `(Class|WBPStage|SetPassEnabled :self Stage :Enabled false)` reads back as `(Class|WBPStage|SetPassEnabled (Variables|Default|GetStage))`. The widget's `SetPhase` reads back as `Variables|Default|SetPhase` with two arguments, as in T06. Write it as `Class|WBPStage|SetPhase :self ... :Phase ...`.
- **Compiling `BP_Show` marked `BPC_LLMClient` dirty** with no change to it. It was left unsaved.
- **Editing `autoplay.json` brought up the editor's Auto Reimport prompt again.** This machine's `Saved/Config/WindowsEditor/EditorPerProjectUserSettings.ini` still has the engine's old `AutoReimportDirectorySettings` line, which overrides the project file (see the Config commit). Removing that line with the editor closed should stop it.

### T09: the cut results (2026-11-14)

Proven in PIE on `L_Stage`:

- **Autoplay on:** after `NHOS: FREETALK DONE`, the three AIs and my seat voted, the votes showed with their reasons, and the log printed `NHOS: TALLY The Visionary 2, The Copycat 1, The Overclocker 1` and `NHOS: CUT visionary tiebreak=no votes=2 reveal=HUMAN`. The stamp "THE VISIONARY: HUMAN" shows in large red text under the header. The Cut took about 3 s.
- **`force_tie` on:** the four votes were rewritten into a cycle, so all four tied at 1 vote. The Director's line showed as `The Director breaks the tie and cuts The Overclocker: "Hedged answers, a passed round, and 'I think. Probably.' Too unsure for a machine. Cut."`, and the log printed `NHOS: CUT overclocker tiebreak=yes votes=1 reveal=HUMAN`.
- **Autoplay off:** I played the scene and Free Talk through the Slate inspector. In The Cut, a reason typed before a pick got "(Click a name first, then type your reason.)". The vote row listed the three other actors. A click picked a name, a second click changed the pick, and the picked button showed as `> The Worrier <`. My typed reason went through the input LLM ("Thats" and "argu" fixed) and showed as `The Copycat votes for The Worrier. "..."`. All three AIs voted for me, because I had passed twice: `NHOS: CUT copycat tiebreak=no votes=3 reveal=HUMAN`.
- No call failed, and the log has no script warnings. Screenshots: `Saved/Screenshots/T09/` (not in git).

How The Cut works now (T10 extends it):

- **`EndFreeTalk`** ends by calling `StartCut`.
- **`StartCut`** sets `Phase` to "the cut", clears the pending asks and the stamp, calls `LoadCutSwitches`, resets the per-seat arrays `VoteTarget` (-1), `VoteReason` and `VoteTries`, and sets `VoteLeft` to the number of seats on stage. It fills `PickSeats` (the seats on stage except mine) and shows them as vote buttons (`ShowVotePick`), then asks every AI on stage at once (`AskVote`). With autoplay on, my seat picks a random name from `PickSeats` and sends `CannedVote[(scene-1) % count]` as the reason.
- **`AskVote(Seat)`** sets `AskOpts` to the names on stage except the voter's, calls `ActorState` with the `vote` ask and `now` = "the cut, voting", clears `AskOpts`, and sends the ask under a `<persona id>-<n>` tag.
- **`ActorState`** now sends `game_messages` from `GameMsgs` and `options` from `AskOpts`. Both stay empty in the scene and Free Talk. To give an ask options (T10's closing vote), fill `AskOpts` before `ActorState` and clear it after.
- **`GameMsgs`** holds the show's game messages: the tie, the Director's pick and the reveal, such as `The Visionary is cut with 2 votes. Reveal: THE VISIONARY: HUMAN.` `StartScene` clears it only when `SceneNum` is 1, so scene 2's asks still see scene 1's reveal. `StartScene` also hides the stamp and the vote row.
- **The human seat:** each vote button sends `OnSend("#vote <i>")`. `HandleSend` sends a line that starts with `#vote ` to `PickVote(Index)`, which sets `HumanPick` and shows the pick. A typed line in "the cut" goes to `SendHumanVote` only after a pick. `SendHumanVote` disables the vote row, shows `> You vote for <name>: <line>` (not in the shared log), and sends the line to the input LLM with `InputState(Line, "free talk")`, so the reason comes back as cleaned speech.
- **`OnAnswer`** now stores `Vote` and `Reason` in `RVote` and `RReason` before it calls `HandleReply`, so `HandleReply` kept its signature. `HandleReply` sends a reply to `StoreVote` in "the cut" and to `PlayTiebreak` in "tiebreak".
- **`StoreVote(Seat, Ok, Vote, Reason, Speech)`:** my seat votes for `HumanPick`, with the input LLM's speech as the reason. An AI vote counts when `FindVoteSeat` matches it to a seat on stage that isn't the voter, case-insensitively, with or without a leading "The". Otherwise the AI is asked again once (`NHOS: VOTE retry <id> vote=<vote>`), then given a random valid target with an empty reason (`NHOS: VOTE random <id> -> <id>`). Each counted vote calls `VoteIn`, which calls `Tally` when `VoteLeft` reaches 0.
- **`CleanReason`** runs `CapWords`, then trims up to three dangling closers at the end: a `)` or `]` with more closers than openers, or an odd `"`.
- **`Tally`** hides the vote row. With `force_tie` it rewrites the targets into a shuffled cycle. It counts the votes into `VoteCount` and, in `OnStage` order, adds each vote to the shared log (`when` "scene n, the cut", `does` from `does_templates.vote`, `says` the reason), shows `<Name> votes for <Target>. "<reason>"` and prints `NHOS: LOG`. Then it prints `NHOS: TALLY ...`. One top seat goes to `CutActor`. A tie sets `Tiebreak`, adds the tie message to `GameMsgs`, prints `NHOS: TIE ...` and calls `AskDirector`.
- **`AskDirector`** sets `Phase` to "tiebreak" and sends `DirectorState` (show, cast, log, game_messages, options = `TiedNames`, the `tiebreak` ask) with the `director` prompt under a `director-<n>` tag. **`PlayTiebreak`** accepts a vote for a tied seat, asks again once, then picks a random tied seat. **`DirectorCut`** adds the Director's line to `GameMsgs` and the screen, prints `NHOS: DIRECTOR <id> | <reason>` and calls `CutActor`. The Director's line goes to `GameMsgs`, not the shared log, because the Director is not an actor.
- **`CutActor(Seat)`** sets `CutSeat` and `SeatCut`, adds the reveal to `GameMsgs`, calls `BuildCast`, shows the stamp, sets the header to "THE CUT: <STAMP>", prints `NHOS: CUT <id> tiebreak=<yes|no> votes=<n> reveal=<AI|HUMAN>` and calls `EndCut`. The info panel still shows the old cast until the next `ScenePrep`.
- **`EndCut`** sets `Phase` to "cut done" and adds "That's the cut. Reactions come next." **T10 replaces its body to start the reactions.**
- **`WBP_Stage`:** `StampText` (44 pt, red, collapsed) sits under the header. `VoteRow` sits between the log and the input row: a "Vote to cut:" label and `VoteBtn0` to `VoteBtn2` (not focusable) with `VoteLbl0` to `VoteLbl2`. `SetVoteOptions(Names)` shows one button per name and hides the row for an empty list. `SetVoteEnabled(Enabled)` and `SetStamp(Stamp)` ("" hides it) are new too.
- **Switches:** `LoadCutSwitches` reads `force_tie` from `Local/switches.json` at each Cut and prints `NHOS: SWITCHES force_tie=<true|false>`. `autoplay.json` has a `vote` list, one reason per scene.
- The DSL source is `Saved/T09/src/bp_show_t09.txt` and `wbp_stage_t09.txt` (not in git).

Numbers, with `claude-haiku-5-5` at low effort:

- **AI votes:** 8 of the 9 calls measured, 1.3 to 3.3 s, 5,060 to 5,370 input tokens, 82 to 377 output tokens. They run at once, so the votes take as long as the slowest call.
- **Input LLM for my reason:** 1.7 to 3.0 s, about 1,340 input tokens.
- **Director:** 3.7 s, 3,498 input tokens, 412 output tokens.
- No vote needed a retry or a random target: 9 AI votes and 1 Director pick all named a valid option.

Also found:

- **The human was cut in scene 1 in every run.** The canned lines read as human ("This one is mine. I think. Probably."), and in the manual run I passed twice. The Director also picked the human out of a four-way tie. That is an early sign, not a fairness measure: T12 measures it. **T10 heads-up:** with autoplay, most shows will end in scene 1, so the branch back to Scene Prep for scene 2 may need a test switch to run unattended.
- **`force_tie` rewrites only the targets,** so a shown reason can name someone other than the vote. It is a test switch only.
- **In a widget Blueprint, `Class|Text|SetText` makes a `VariableSet` node on `TextBlock.Text`.** Its pins are `Text`, then `self`, so positional arguments put the widget into the text pin ("Could not connect pin ReturnValue to self"). Write it as `(Class|Text|SetText :self <widget> :Text <text>)`. `Class|Factory|SetText`, the name `read_graph_dsl` prints, is a different node (it sets `Factory.bText`); never write it.
- **Enum pins take quoted value names:** `(Widget|SetVisibility :self <widget> :InVisibility "Collapsed")`.
- **Big graphs are slow to write.** `Tally` took 36 s in `write_graph_dsl`. A batch of 9 or 10 graph writes took 65 to 90 s, close to the client's limit, so keep batches smaller.
- **Script tools return strict dicts:** `.get(key, default)` raises inside `execute_tool_script`; use `[key]`.
- **The Slate inspector's level editor splitter** was `sp4` this time. Find it in `Snapshot("", 14)` as the splitter as wide as the viewport area, then `Observe` it with `maxDepth` 80.

### T10: reactions, end screens and restart results (2026-11-14)

Proven in PIE on `L_Stage`, three shows with autoplay on:

- **Show 1 (lose):** after the cut, the reactions ran in order: my seat first (I was cut, so my canned line was my last words, through the input LLM), then the three AIs one at a time, gloating. `NHOS: REACTIONS DONE scene=1 entries=4`, then three `NHOS: CLOSING <id> vote=visionary | ...` lines and `NHOS: SHOW END result=lose scenes=1 human=visionary show=1`. The end screen came up over the stage: "YOU'RE CUT" in red, "You were The Visionary. The AIs caught you in scene 1 of 2.", each AI's votes with their reasons and its closing line, and a Restart button.
- **Restart:** a click on Restart through the Slate inspector printed `NHOS: RESTART show=2` and a new `NHOS: SETUP`, and the info panel showed show 2's card and roles. The first asks of show 2 had the same input size as show 1's (about 3,375 tokens), so the shared log and game messages were cleared. `RestartShow` also calls `WBP_Stage.ClearLog` on the on-screen log, but no screenshot checked the top of the log after a restart. Show 2 also reached `NHOS: SHOW END result=lose scenes=1 ... show=2`.
- **Show 3 (win, with the new `spare_human` switch):** an AI was cut in scene 1, the reactions ran with my seat last, and `ScenePrep` dealt scene 2 with the other card and a new note. Scene 2 had 3 actors (Free Talk `entries=6`, reactions `entries=3`). After the second cut, two actors were left: `NHOS: SHOW END result=win scenes=2 human=overclocker show=1`, and the end screen said "YOU WIN" in green.
- No call failed, and the log has no script warnings. Screenshots: `Saved/Screenshots/T10/` (not in git).
- **Not tested by hand:** a typed reaction and the Pass button in the reactions. They use the same routing as Free Talk (`HandleSend` → `SendHumanReact`), and autoplay sends its canned reaction through the same function. T12's playtest exercises them.

How the end of a scene works now (T11 hooks into it):

- **`EndCut`** sets `Phase` to "cut done" and calls `StartReactions`.
- **`StartReactions`** sets `Phase` to "reactions". If the human was cut, it adds "The human is caught. The AIs win the show." to `GameMsgs`. It builds `ReactOrder`: the cut seat first, then the AI seats that aren't cut in a random order, then my seat if I wasn't cut. Then it calls `NextReactor`.
- **`NextReactor`** works like `NextTalker`. My seat: Pass is enabled, and with autoplay it sends `CannedReact[(scene-1) % count]`. An AI seat gets the `reaction_cut` ask if it is the cut seat, otherwise `reaction`, with `now` = "the cut, reactions" and the shared log so far. After the last seat it calls `EndReactions`.
- **`PlayReact(Seat, Ok, Speech, Pass, Verbs, Targets, Items)`** adds one entry to the shared log: `when` "scene n, reactions", `does` from `BuildDoes` (or "passes"), `says` the capped speech. The screen shows `<Name>: "<line>"`, `<Name> <does>. "<line>"` or `<Name> stays silent.`, and the editor log gets `NHOS: LOG`. A failed reply counts as a pass.
- **`SendHumanReact(Line)`**: "pass" skips the input LLM; any other line goes to the input LLM with `InputState(Line, "reaction")`. `HandleSend` routes a typed line to it while `Phase` is "reactions" and `ReactSeat` is my seat.
- **`EndReactions`** prints `NHOS: REACTIONS DONE scene=<n> entries=<n>` and branches: my seat cut → `EndShow(false)`; two or fewer seats left → `EndShow(true)`; otherwise it adds a log line and calls `ScenePrep` for the next scene.
- **`EndShow(Win)`** sets `Phase` to "closing", adds "The show is over. The human was <NAME>..." to `GameMsgs`, and asks every AI seat at once, cut or not, for the `closing` ask, with `options` = every other name and `now` = "show over" (`AskClosing`).
- **`StoreClosing`** matches the vote to any seat (`FindAnySeat`, which searches all seats, not just `OnStage`), cleans the reason, prints `NHOS: CLOSING <id> vote=<id|none> | <reason>`, and calls `ShowEndScreen` when the last answer is in. A closing ask isn't asked again; a bad one shows "(no answer)".
- **`ShowEndScreen`** sets `Phase` to "end", builds the body from the vote history and the closing answers, creates `WBP_EndScreen`, calls its `Setup(Title, Sub, Body, Win)`, adds it to the viewport at Z order 10, and prints `NHOS: SHOW END result=<win|lose> scenes=<n> human=<id> show=<n>`. A vote for my seat is marked "(you)".
- **Vote history:** `CutActor` now calls `RecordVotes` first, which appends this scene's votes to `HistScene`, `HistVoter`, `HistTarget` and `HistReason`, and it sets `CutScene[seat]` to the scene number. `StartScene` clears them when `SceneNum` is 1, like `GameMsgs`.
- **`RestartShow`** works only in "end": it removes the end screen, adds 1 to `ShowNum`, prints `NHOS: RESTART show=<n>`, clears the on-screen log (`WBP_Stage.ClearLog`), the stamp and Pass, puts the keyboard focus back in the input box, and calls `SetupShow`. `SetupShow` already resets the seats, the shared log and `SceneNum`.
- **`WBP_EndScreen`:** `Background` (opaque dark Border) > `RootBox` > `TitleText` (56 pt), `SubText` (22 pt), `BodyScroll` > `BodyText` (17 pt, wrapped) and `RestartButton` (not focusable). Its Restart click calls `GetActorOfClass(BP_Show).RestartShow`, so `BP_Show` needs no dispatcher binding.
- **For T11:** actor lines now enter the shared log in four functions: `PlayTurn` (scene turns), `PlayTalk` (Free Talk), `Tally` (votes) and `PlayReact` (reactions). The cut is `CutActor`, and Restart is `RestartShow`.
- **Switches:** `spare_human` in `Local/switches.json` (read in `LoadCutSwitches`) makes `SpareHumanVotes`, called from `VoteIn` before `Tally`, move every vote for my seat to a random other actor on stage, so the human is never cut and an unattended show plays all its scenes. A moved vote keeps its old reason, so the shown reason can name someone else. It is a test switch only. `autoplay.json` has a `reaction` list, one line per scene.
- The DSL source is `Saved/T10/src/bp_show_t10.pp.txt` (not in git), written with shorthand macros and expanded by the new `Tools/dslpp.py` into `bp_show_t10.txt`, which the push script reads with `AssetTools.read_file`.

Numbers, with `claude-haiku-5-5` at low effort:

- **A show that ends in scene 1:** 30 calls, about 122,000 input and 5,000 output tokens, 32 to 40 s with autoplay.
- **A two-scene show:** 51 calls, 230,000 input and 6,100 output tokens, 52 s with autoplay. That is close to T03's estimate of 55 calls.
- **Reactions:** 1.3 to 2.0 s per AI call, 5,500 to 7,900 input tokens (the whole log so far). They run one at a time, so the reactions take about 6 to 8 s.
- **Closing:** 1.0 to 2.0 s, about 6,000 to 8,000 input tokens. They run at once.

Also found:

- **The AIs caught the human in scene 1 in both shows without `spare_human`,** with 2 and 3 of 3 votes. They cite the canned lines ("I think. Probably.", a silent pass, no robot tags). That is a sign about the canned lines, not about fairness; T12 measures fairness with a person playing.
- **In their reactions after the human is caught, the AIs gloat and claim credit** ("I detected it first"), and the closing lines all name the human with a reason from the log. The end screen reads well as an explanation of how you were caught.
- **A preprocessor tokenizer must keep `Name(Arg)` as one token.** Node names such as `Utilities|String|ToString(Boolean)`, `Math|Integer|%(Integer)` and `OnClicked(RestartButton)` hold parentheses. When one was split, `write_graph_dsl` failed with "Boolean does not exist", and the error aborted the whole `execute_tool_script` even inside a `try`.
- **A Border at alpha 0.97 still let the stage text show through** in PIE. Alpha 1.0 is opaque.
- **`StartPIE` needs `options`:** `{"bSimulate": false, "playMode": "PlayMode_InViewPort", "warmupSeconds": 1}`.
- **Compiling `BP_Show` marked `L_Stage` and `BPC_LLMClient` dirty again** with no change to them. They were left unsaved.
- **Write times:** most graphs took 4 to 18 s in `write_graph_dsl`. `ShowEndScreen` took 34 s. Batches of 2 to 7 graphs stayed under 60 s.

### T11: the cast on stage results (2026-11-14)

Proven in PIE on `L_Stage`:

- **Autoplay with `spare_human`:** `NHOS: STAGE robots=4` at setup, `NHOS: STAGE cut visionary` and `NHOS: STAGE cut overclocker` at the two cuts, then `NHOS: SHOW END result=win scenes=2`. Restart printed `NHOS: RESTART show=2` and a new `NHOS: STAGE robots=4`. Every robot stood again, unlit, with show 2's names, and show 2 also reached `NHOS: SHOW END`.
- **Autoplay without `spare_human`:** the human was cut in scene 1 after a tiebreak, and its robot tipped over gray with "HUMAN" on its label.
- 189 calls in these runs, none failed, and no script warnings. Screenshots: `Saved/Screenshots/T11/` (not in git): `0_sceneprep.png` (four labelled robots above the log), `2_turn.png` (one robot lit), `3_cut.png` (a cut robot, gray, tipped over, stamp "AI") and `4_cut_human.png` (stamp "HUMAN").

What the assets hold:

- **`BP_Robot`** (`Content/NHOS/Stage/`): `DefaultSceneRoot` > `Rig` (SceneComponent) > `Body` (engine Cylinder, 70 × 70 × 110 cm), `Head` (Cube, 55 × 55 × 50) and `Visor` (a thin Cube on the front of the head). Under the root, not the rig: `Spot` (SpotLight 430 cm up, pointing down, 4000 cd, hidden at start) and `Label` (TextRender, 24 cm, centered, at 178 cm). The actor's origin is at its feet.
  - Variables: `Seat` and `FallDir` (instance editable), `DisplayName`, `BaseColor`, `IsCut`, `TipRoll`, `TipGoal`.
  - `Setup(Name, Color, IsMe)` sets the name (with " (you)" for my seat) and the color, then calls `ResetLook`.
  - `ResetLook` stands the robot up, sets its color, a cyan visor and a white label, turns the light off and calls `FaceCamera`, which turns the label toward the level's `CameraActor` (yaw only).
  - `SetLit(On)` shows or hides `Spot` and sets the `Glow` of body, head and visor.
  - `SetCut(Stamp)` turns the light off, makes body and head gray and the visor dark, sets the label to the stamp in red, and sets `TipGoal` to 82° × `FallDir`. Event Tick eases `TipRoll` toward `TipGoal` (`FInterpTo`, speed 3) and rolls `Rig`, so the robot tips over in about a second. The label stays upright where the head was, so the stamp floats above the fallen robot.
  - Colors use `SetVectorParameterValueOnMaterials` and `SetScalarParameterValueOnMaterials` on each mesh. They make a dynamic instance per component, so the robot keeps no MID variables.
- **`M_Robot`**: one Substrate Slab BSDF. `Color` (vector parameter) drives Diffuse Albedo, `Color` × `Glow` (scalar, default 0) drives Emissive, and roughness is 0.45. `MI_StageFloor` and `MI_StageWall` are dark instances of it.
- **`L_Stage`**, all in the outliner folder `Stage`:
  - `StageFloor` (Cube, 40 × 30 m, top at z = 0) and `StageWall` (Cube at x = 600, 10 m high).
  - `KeyLight` (SpotLight from the front left, 1400 cd, 50° cone) and `FillLight` (PointLight from the front right, 300 cd, cool).
  - `Robot0` to `Robot3` with `Seat` 0 to 3 at y = −330, −110, 110 and 330 (the outer two 50 cm forward), each turned to face the camera. `FallDir` is −1 for seats 0 and 1 and +1 for seats 2 and 3, so a cut robot falls outward and two cut robots never overlap. Positive roll tips a robot to the camera's right.
  - `StageCamera` at (−820, 0, 270), pitch −21°, Auto Activate for Player 0.
- **`WBP_Stage`**: `Background` is now transparent with no padding. `RootBox` holds `HeaderBar` (Border, dark at 85 %, with `PhaseHeader`), `StampText`, `StageGap` (Spacer, Fill 1) and `LowerPanel` (Border, opaque dark, Fill 1) > `LowerBox` > `BodyRow` (Fill), `VoteRow` and `InputRow`. So the 3D stage shows through the top half, and the log keeps its font and its opaque background.
  - `InfoText` is now inside `InfoScroll` (ScrollBox). The long info text overflowed the half-height panel and drew over the input row.
  - When the stamp shows, it takes its height from both the stage and the log.

How `BP_Show` drives the robots:

- **`FindRobots`** fills `Robots` (one slot per seat up to `MaxCast`; empty slots stay None) from `GetAllActorsOfClass(BP_Robot)`, by each robot's `Seat`.
- **`StageSetup`** calls `FindRobots`, then `Setup` on each seat's robot with the seat's name, `SeatColors[seat]` (orange, teal, violet and yellow, set as defaults on `BP_Show`) and whether it is my seat. It prints `NHOS: STAGE robots=<n>`, counting the seats that have a robot.
  - `StartScene` calls it when `SceneNum` is 1, so a new show and Restart both reset the stage. `StartScene` then calls `LightSeat(-1)`, so every scene starts dark.
- **`LightSeat(Seat)`** calls `SetLit` on every robot, on for that seat only. A seat with no robot is skipped.
- **`ActorLine(Seat, Entry)`** is now the one place where an actor's line enters the shared log: it adds the entry and calls `LightSeat`. `PlayTurn`, `PlayTalk`, `Tally` (each vote) and `PlayReact` call it. A scene turn shows its four lines at once, so its last speaker stays lit. The cut actor's last words light its fallen robot.
- **`StageCut(Seat)`**, called from `CutActor` after the stamp shows, prints `NHOS: STAGE cut <id>` and calls `SetCut` with "AI" or "HUMAN" on that seat's robot.
- `PlayTurn` had no saved DSL source, so T11 rewrote it from its readback and the T07 notes. The T11 source of every graph it wrote is in `Saved/T11/src/` (not in git).

Unreal MCP rules found in this task:

- **`ActorTools.add_component` works on a Blueprint asset.** It adds a component to the Blueprint (the template is `.../BP_Robot.BP_Robot_C:<Name>_GEN_VARIABLE`), and `set_parent_component` nests it. Set the mesh, transform and light settings on the template with `ObjectTools.set_properties`.
- **`ObjectTools.set_properties` and `get_properties` take the object as `instance`,** not `object`.
- **Some node IDs are shared by several functions, and the DSL may pick the wrong one.** `Rendering|Material|SetVectorParameterValue` made the Material Parameter Collection version, and `Rendering|SetMaterial` made a Volumetric Cloud one. Check the `self` pin type with `get_node_type_pins` before you use an ID. `Class|PrimitiveComponent|...` doesn't exist, because those functions sit in other categories.
- **A tool call that fails inside `execute_tool_script` ends the script, even inside `try`.** Look up only IDs that `find_node_types` returned.
- **`CameraActor` letterboxes by default** (`bConstrainAspectRatio` on its CameraComponent). Turn it off. The project keeps the vertical field of view: 90° horizontal at 16:9 is only about 70° in the editor's narrower PIE viewport, so frame the stage for the narrow viewport.
- **UMG `WrapWidgets` wraps several siblings in one new panel and keeps their order, but their old slot settings (fill, padding) are lost.** Set them again on the new slots.
- **Timing PIE screenshots:** an autoplay show runs too fast to screenshot by hand (a two-scene show took about 60 s with the editor in front). In Bash, `timeout 60 bash -c 'tail -n0 -f Saved/Logs/AIMegaJam2026.log | grep -a -m1 "<NHOS line>"'` waits for a check line, and the screenshot call goes right after it.
- Compiling `BP_Show` marked `BPC_LLMClient` dirty again, with no change to it. It was left unsaved.

### T12: Playtest 1 (2026-11-14)

I played one show by hand in PIE, with autoplay off and every role on `claude-haiku-5-5` at low effort. Then I clicked Restart and stopped PIE before show 2 began. T12 asked for 3 shows. I chose to go on with one, because T13 changes how the AIs speak, and that changes how they catch the human. T13 measures fairness again ("T13: Playtest 2").

- **The show:** I was The Copycat, the "Food critic in disguise" on `cafe_big_decision`. The note was `stay_counter` (move to the Counter in turn 1, then stay), and The Overclocker had the decoy. All 3 AIs voted for me in scene 1: `NHOS: TALLY The Copycat 3, The Worrier 1` and `NHOS: CUT copycat tiebreak=no votes=3 reveal=HUMAN`. I lost in scene 1 of 2. No AI was cut by mistake. The show took 3.9 minutes.
- **Why they caught me,** from their Free Talk lines, vote reasons and closing lines:
  - **Style.** My lines had no robot-speak. "Too sincere to be silicon" and "Robots don't brag about heart". The bracket style was the biggest tell, and a new player can't know they should copy it.
  - **I stood still in all 3 turns.** I typed only speech, so my robot never moved. The two AIs with the note moved to the Counter, and the decoy moved to the Placemat as its note said.
  - **"I am a food critic"** gave away my secret role. "Never ordered, never sipped" was in every AI's reason.
- **Calls:** 31, none failed. Actor asks took 0.97 to 2.77 s (median 1.62 s), and input LLM asks 0.97 to 2.68 s (median 1.55 s). 118,256 input and 3,460 output tokens: about $0.014 for a one-scene show, the same as T10's autoplay shows.
- **Checked by hand:** a typed reaction ("Aw man.") went through the input LLM into the shared log as my last words. Pass in the reactions wasn't tried.
- **My notes:**
  - I really like it.
  - The bracket robot-speak is hard to read. The AIs should talk like a normal chat, as Claude or ChatGPT do: no glitch speak, no brackets, no emoji. Legibility comes first.
  - The UI needs a lot of UI/UX polish.
  - The game needs art and personality.
  - We need a different LLM for each AI player.
  - The improv scenes should parody famous stories, such as Romeo and Juliet or Star Wars, without their exact names.
  - (Asked during T12) The robots should move around and interact with things on stage.
- **Decision: go.** I confirmed it on 2026-11-14, with these choices:
  - **A key per provider,** not a router, as the design's persona table has it (T16, T18).
  - **One improv stage,** with a backdrop and props for each story, not a set per story and not the café (T15, T17).
  - **A hosted relay with a spending cap, plus a key-entry screen,** so judges can play at once (T21). This is the design's default.
- **The plan after the gate** is T13 to T24, in the order of the findings: legibility first (T13), then the screens (T14), the story scenes (T15), the providers (T16, T18), the stage art (T17), the robots' actions (T19), audio (T20), the relay (T21), and packaging and submission (T22, T23). The timers task is now T24, and it is optional.
- **Not used for Playtest 1:** John Park's `Take37` branch has a different game in C++, with the UE4 mannequin as a placeholder, an ArtGen concept-to-3D tool and voice lines. It isn't merged and its cast doesn't fit the robots, so no task depends on it.

### T13: plain chat results (2026-11-14)

Steps 1 to 5. Every role still runs `claude-haiku-5-5` at low effort.

- **The design doc had moved on since the 2026-11-13 snapshot.** Personas are now unnamed in play, and each has a pun name that shows only on its cut stamp ("Sam Botman: AI"). The prompts never name a persona. The base prompt opens "You are an AI actor... that created your model". A new Art Inspiration tab has an opera-house stage and "The Understudy", a persona-less player bot (an open question in the doc). I chose to merge: T13's rules and trait wording went on top of the doc's newer version, which keeps the pun-name headings and the unnamed prompts. `GameDesign.md` now copies all five tabs.
  - **The game still names personas in play** ("The Visionary" in the cast list, the log and the robot labels), and T14, T15 and T17 assume names and an improv stage. A plan change should settle this.
- **What changed:**
  - **Base prompt:** plain chat sentences, with no brackets, tags, sound effects, `//`, asterisks, emoji or all-caps words. A battery joke now and then is fine. The persona quotes are examples, not catchphrases, and a bot shouldn't reuse its own earlier lines. Lines are about 10 words, never more than 15.
  - **Persona prompts:** traits in plain words, with the long quoted lines turned into descriptions. The personas are "it". The Copycat copies trending features, not lines.
  - **Game prompt:** "Spotting the human" judges by the note, the scene card, the persona's traits and human slips (hunger, sleep, feelings, dodging, echoing), and how a line is typed is never evidence. A vote reason names the one thing the actor did or said. The show name, the headers and the asks are in normal case, and names stay in normal case even where game messages use capitals. Free Talk asks for one actor and one piece of evidence.
  - **Director:** plain sentences, and it ignores how a line is typed.
  - **`autoplay.json`:** two canned human lines were about beeps and sounding like a robot.
- **What the tests found:**
  - **The no-brackets rules held from the first draft.** Not one reply in about 370 checker asks and 5 autoplay shows had a bracket, `//`, `*`, an emoji, "beep" or an all-caps word.
  - **Plain sentences run longer than glitch fragments.** With "20 words at most, aim for 8 to 15", 4 of 34 replies passed 25 words. In a PIE show, the game cut 3 of 14 Free Talk lines mid-sentence at 25 words. "15 words at most, aim for about 10" and "accuse one actor, with one piece of evidence" fixed it: the checker's replies run 15 words at the median and 23 at most, and no line was cut in the last three shows.
  - **The model repeats quoted examples.** With the long quotes in the traits, the Worrier opened 6 of 8 lines with "Just a gentle reminder", the Visionary used "Something big is coming" in 5 of 7, and the Copycat opened 14 of 15 with "Fellow battery-consumers". "Now and then" in the trait didn't help; turning the quotes into descriptions did. Short quotes ("Sigh. Fine.", "the best one yet", "That is interesting.") still come back, but as a tic, not every line.
  - **A persona trait can look like a human tell.** The Copycat copying "whatever is trending" made it echo other actors' phrases, which the game prompt lists as a human slip, and two AIs voted it as the human. "Whichever feature is trending" fixed it.
  - **An AI that repeats itself gets voted out.** In the first show, the Visionary's repeated croissant lines read as "a script", and it was cut by mistake. The no-repeat rule came from that.
- **Autoplay shows** (PIE, autoplay on; the human seat plays the canned lines):

| Show | Prompts | Result | AI lines legible | Calls |
|---|---|---|---|---|
| 1 | first draft | AI cut by mistake in scene 1; human cut in scene 2 | 35 of 38 (3 cut off at 25 words) | 51 |
| 2 | no-repeat rule, Free Talk on one actor | human cut in scene 1, 3 votes | 22 of 24 (2 cut off) | 30 |
| 3 | quotes became descriptions, 15-word cap | AI cut on a tiebreak in scene 1; human cut on a tiebreak in scene 2 | 39 of 39 | 53 |
| 4 | Copycat traits reworded | AI cut in scene 1; human cut in scene 2 | 38 of 38 | 51 |
| 5 | final, merged with the doc | human cut in scene 1, 2 votes | 24 of 24 | 30 |

- No call failed. The AIs caught the canned human every time, mostly on its canned lines ("I think. Probably.", "Oops. Muscle memory. I don't have muscles.") and on the note. That says more about the canned lines than about fairness; Playtest 2 measures that with me playing. The vote and closing reasons now cite actions and words ("threw a napkin at the Counter, then joked about having no muscles"), not typing style.
- **The checker:** the final text passed `python Tools/check_prompts.py` twice in a row: 34 of 34 asks, a median of 1.7 s per call, and about $0.026 per show by its 55-call estimate.
- **`Tools/check_prompts.py` now:**
  - A reply fails the legibility check on a bracket, `//`, `*`, an emoji or pictograph, "beep" or "boop", or a word of 4 or more capitals. The input LLM's replies are skipped, because it keeps the player's own words.
  - The sample show is in plain chat.
  - `--log` checks the AI lines (`NHOS: LOG`, `CLOSING` and `DIRECTOR`) of the last PIE show in the editor log and also fails a line the game cut at 25 words. `--all-shows` checks every show in the file. The old shows in the T12 log fail 390 of 451 lines.
  - `--no-design` skips the word-for-word check, for trying drafts before the design doc changes.
  - The design's persona headings are pun names now, so each persona prompt must match one of the blocks under "Persona prompts".

### T13: Playtest 2 (2026-11-14)

I played three shows by hand in PIE (11:08 PM, 11:31 PM and 11:44 PM PST), with autoplay off, T14's UI in place and every role on `claude-haiku-5-5` at low effort. **My verdict: the AIs read like a normal chat.**

| Show | My seat | Result | Calls | Cost | AI lines legible |
|---|---|---|---|---|---|
| 1 | The Overclocker, `cafe_missing_tip_jar` then `cafe_big_decision` | **Win.** The Copycat (AI) was cut in scene 1 and The Visionary (AI) in scene 2, each with 2 votes. | 51 | $0.026 | 38 of 38 |
| 2 | The Overclocker, `cafe_missing_tip_jar` | Cut in scene 1, 3 votes | 31 | $0.014 | 24 of 24 |
| 3 | The Worrier, `cafe_missing_tip_jar` | Cut in scene 1, 3 votes | 28 | $0.014 | 17 of 24 (see below) |

- No call failed. The median was 1.7 to 2.0 s per call.
- **Pass in the reactions works.** In show 3 I clicked it after my cut, and the shared log has "The Worrier | passes".
- **The vote reasons are about what I did and said, not how I typed.**
  - Show 1: one AI voted for me because I "walked Backward on turn one" against the note (`never_backward`). The others voted for the AIs that kept repeating themselves.
  - Show 2: all three voted for me for "standing still for three turns, then saying the game is broken".
  - Show 3: all three voted for me for wanting "a coffee and a nap", for saying "I am definitely a robot, beep" and for passing twice.
- **An AI that repeats itself still gets cut.** In show 1, the Copycat opened most lines with "Friends" and talked about its sincerity, and it was cut as "a script". The Worrier's repeated "gentle safety note" drew votes too. That cost the AIs the show. It is a fair way for the human to win, but the repetition rule in the base prompt doesn't fully stop it.
- **Show 3's 7 failures are not robot-speak.**
  - 6 of the 7 are AIs quoting my own "beep" ("kept saying beep, which no robot would do"). The `--log` check counts any "beep" as a failure, even one that refers to the human's line.
  - The 7th is a Free Talk line the game cut off at 25 words. That is the first cut-off line since the 15-word target.
- **A bug, not about speech:** in show 2, my turns 1 and 3 came back with no action and no speech, so my robot stood still. The input LLM calls succeeded but ran long (337 and 302 output tokens, against 35 to 40 for a plain line). T14 added `NHOS: TYPED` after this show, so the log doesn't have what I typed. I said "The game is broken for me." in Free Talk.

### T14: UI/UX polish results (2026-11-14)

Proven in PIE on `L_Stage`:

- **A show played by hand through the Slate inspector, autoplay off:** the title screen, Play, two scenes as The Overclocker (typed turns, one Free Talk line, one Pass, a vote picked by click with a typed reason, a typed reaction), then the win screen: `NHOS: SHOW END result=win scenes=2 human=overclocker show=1`. 53 calls, none failed.
- **Autoplay on:** the title is skipped, and the show reached `NHOS: SHOW END result=lose scenes=1` with 30 calls, none failed, and no script warnings. Play Again printed `NHOS: RESTART show=2` and a new `NHOS: SETUP`.
- Screenshots: `Saved/Screenshots/T14/` (not in git): `0_title`, `1_sceneprep` (turn 1, my move), `2_turn`, `3_freetalk_myturn`, `4_vote` and `4b_vote_picked`, `5_reveal`, `6_scene2_prep`, `7_end` (win) and `8_autoplay_after_cut` (lose).
- **Not checked yet:** my playtest (the last Done-when item), and the stamp's fade-out, which was added after the manual run.

What the screens do now:

- **The log reads like a chat.** Each entry is a `WBP_ChatLine`: a color bar and the speaker's name in their robot's color (`SeatColors`), then the action in quiet gray italics, then the speech in plain 20 pt text. My lines add "(you)" and a light tint. Game lines are gold on a faint gold band, and my typed echoes (`> ...`) and hints (`(...)`) are small gray notes.
  - `BP_Show.ShowLine(Seat, Does, Says)` is the one place an actor line reaches the screen. `PlayTurn`, `PlayTalk`, `Tally` and `PlayReact` call it right after `ActorLine`. It hides "stands still" outside the scene turns, so Free Talk lines show only the speech.
  - `WBP_Stage.AddLogLine(Line)` still takes every game line. `AddChatLine(Name, Color, Action, Speech, IsMe)` is new.
- **Always says what to do now.** `HeaderBar` holds `PhaseHeader` and a new `TurnText` line. `BP_Show.UpdatePrompt` runs on Event Tick: `ComputePrompt` turns `Phase`, `HumanSent`, `TalkSeat`, `ReactSeat` and `HumanPick` into the turn line, the input hint and whether I can type, and `WBP_Stage.SetPrompt` applies them only when they change. Off my turn the input box and Send are disabled. On my turn the turn line turns gold and the input box gets the keyboard focus again.
- **The info panel** (`InfoBox` in `InfoScroll`): "YOU ARE", my name in my color, my role and want in large text, the director's note in an amber box, the scene, the cast as colored `WBP_ChatLine` rows with roles and the others' wants (a cut actor turns gray and shows its reveal), and the places and props on one line each. `ShowPrep` fills it with `SetInfoTop`, `ShowCast` and `SetStageInfo`. `CutActor` calls `ShowCast` again, so the cast updates at each cut. The old `InfoText` and `SetInfo` are gone.
- **Controls:** the vote buttons are big and red, and after a pick the other buttons dim (`SetVotePick`). `ShowVotePick` no longer wraps the pick in "> <". Send and Pass are colored buttons, and every button has a visible disabled look (the engine's default draws nothing when disabled).
- **The reveal stamp** sits in a new `StageArea` overlay over the 3D stage, in `StampFrame`, a tilted box that is red for HUMAN and amber for AI. `SetStamp` starts `StampAnim`, and Event Tick scales the stamp in from 3.2 times its size. It holds for 3.5 s, then fades out over 1 s, so it doesn't hide the fallen robot for the rest of the scene.
- **Title screen:** `WBP_Title` with the name, a tagline, five How-to-play lines and a Play button. `Begin` ends with `ShowTitle`, which runs `LoadSwitches` and, with autoplay on, calls `SetupShow` at once. Otherwise it adds the title at Z order 20 and prints `NHOS: TITLE shown`. Play calls `BP_Show.StartFromTitle` (`NHOS: TITLE click`, `NHOS: TITLE play`), which removes the title and calls `SetupShow`. Restart doesn't show the title again.
- **End screen:** the result, then one `WBP_EndCard` per AI in a `UniformGridPanel`: name and color bar, AI and when it was cut, its votes per scene, and who it thought was human with its reason. Then Play Again and Quit (`QuitGame`; in PIE it ends PIE). `WBP_EndScreen.Setup` kept its signature; `ShowEndScreen` passes an empty body and calls `AddCard` per AI.
- **Font:** `Content/NHOS/UI/Fonts/F_UI` is a copy of the engine's Roboto composite font (Apache 2.0), with Droid Sans Fallback as its fallback typeface. Every text in the four widgets uses it. `WBP_Stage.CleanText` drops everything from U+2190 up except CJK and full-width forms, plus zero-width joiners, so emoji never reach the screen. It runs on every log line and on the end-screen cards. `Docs/Assets.md` records both fonts.

Unreal MCP rules found in this task:

- **Unreal MCP can't import a file** (no import tool in `AssetTools`), so a downloaded font can't come in this way. `AssetTools.duplicate` of an engine asset into `/Game` works, and the copy still uses the engine's font faces.
- **The first PIE ran a stale `WBP_Title`.** The Play button's click never fired, though the bound event was in the graph. Recompiling `WBP_Title` with a change fixed it. If a new widget's event doesn't fire in PIE, recompile it, and add a print to prove the event runs.
- **In `write_graph_dsl`, a bare widget name is not a variable.** "Undefined variable NameText" means you must use the getter, `(Variables|WBP_ChatLine|GetNameText)`. `Saved/T14/src/mk.sh` turns `@Name` into that getter before `Tools/dslpp.py` runs.
- **UMG property sets in the DSL call the setter.** `Class|Text|SetColorandOpacity`, `Class|Border|SetBrushColor`, `Class|TextBox|SetHintText` and `Class|Button|SetBackgroundColor` are `VariableSet` nodes on properties that have a Blueprint setter, so the widget updates. Their value pin has the property's name (`ColorAndOpacity`, `BrushColor`).
- **Slate inspector screenshots of `sp4` include the Outliner and the Content Browser.** `Saved/T14/crop.ps1` crops them to the viewport with `System.Drawing`. Run it with `powershell -ExecutionPolicy Bypass -File`, because this machine blocks scripts. `Snapshot` output stops at 8,191 characters, so search it with a regex in the script instead of reading it.
- `UMGToolSet.WrapWidgets` returns the new panel, and `RenameWidget` renames it. `AddWidget` with `childIndex` puts a widget at that index, which is how `StageArea` replaced `StageGap`.
- The DSL source is `Saved/T14/src/` (not in git).

After my first playtest of T14 (one show, cut in scene 1; I said "It's better"):

- **The end screen covered the last reactions.** Now `ShowEndScreen` builds the end screen but doesn't show it: the log says "Read the last reactions, then press See the results.", and a gold `ContinueButton` appears in the input row (`WBP_Stage.SetContinue`). Its click calls `BP_Show.RevealEnd`, which hides the button, adds the end screen and prints `NHOS: END screen shown`. With autoplay on, `RevealEnd` runs at once. `NHOS: SHOW END` still prints when the end screen is built. Checked in PIE: a hand-played show where I was cut, then the button, then the end screen. The autoplay path wasn't run again.
- **Two of my scene turns reached the stage empty** ("stands still", no speech), though I typed things to say and do. The input LLM got them (`NHOS: LLM input-4 ok`) and returned no actions and no speech, with an unusually long reply (337 and 302 output tokens, against about 40 for most). Not reproduced: the same request from a script turned 28 of 28 typical lines into the right actions and speech, in the plain, quoted, `*action*` and `(action)` forms. The game didn't log typed text, so `WBP_Stage.SubmitInput` now prints `NHOS: TYPED <line>` for every line I send. If it happens again, the TYPED line next to the `NHOS: LOG` line shows what went in.

### T15: story scenes results (2026-11-14)

Every role still runs `claude-haiku-5-5` at low effort.

- **The set** is "The Improv Stage": Center, Left, Right, Front, Back, Riser and Prop Table, each with a public `what` line. The Riser plays whatever the story needs. The props are a cardboard sword, a paper crown, a plastic rose, a toy ray gun, a teacup, a cape, a rubber chicken and a scroll.
- **6 cards**, each with a title, a premise that says what the Riser plays, a `backdrop` {id, what} for T17, and 4 seats whose wants still work when any one seat is left out:

| Card id | Title | Story | Riser |
|---|---|---|---|
| `star_crossed` | Wherefore Art Thou, Robot? | Romeo and Juliet (public domain) | the balcony |
| `sword_stone` | The Sword in the Stone, Some Assembly Required | Arthur and the sword (public domain) | the stone |
| `rubber_chicken_case` | The Case of the Stolen Rubber Chicken | a Sherlock Holmes mystery, with Sherlock Ohms and Doctor Watt-son | the Duchess's armchair |
| `space_father` | My Father, the Heavy Breather | parody: a desert-planet farm kid and a masked villain with family news | the space truck's cockpit |
| `unsinkable` | The Unsinkable, Probably | parody: a 1912 liner, an iceberg, an artist and an heiress | the ship's bow |
| `dino_island` | Welcome to Dino Island, Mostly Safe | parody: a theme park of cloned dinosaurs | the lookout tower |

- **10 notes**, 8 physical and 2 spoken, each with a decoy: `never_back`, `stay_center`, `hold_prop`, `give_every_turn`, `throw_once`, `riser_once`, `keep_moving`, `look_first`, `say_chicken`, `ask_question`. None asks everyone to grab the same single prop, so T19's props don't fight over one item.
- **Game prompt:** a new "The stage and the story" section. Places and props stand in for what the story needs; play the card's version, use only the names on the card, and never quote the original or use its names, made-up words or famous lines.
- **Input prompt:** examples on the new places, and anything raised that the player names (a balcony, a throne, a cockpit, a bow) is the Riser. Also the T13 session's fix for empty turns: an action on something unlisted becomes a look at the closest listed place or actor, or a look around, and the converter never sends an empty reply. Before the fix, 11 of 18 unmappable café lines came back empty; after it, 0 of 15 stage lines did. Those turns take 250 to 450 output tokens instead of about 50.
- **`Tools/check_prompts.py`:**
  - Checks the 7 places, 6 to 10 props, at least 6 cards and 10 notes, a backdrop on each card, and a premise that names the Riser.
  - The sample show is scene 1 of `star_crossed` with the `hold_prop` note.
  - A card sweep sends a scene-turn ask for every card in a 3-actor scene 2, with a different seat left out each time (18 asks).
  - A story check fails any file or AI line with a name, a made-up word or a famous line from the parodied films (`STORY_TERMS`), or a real name (`BANNED`). `--log` runs it on PIE shows too and prints each show's card ids.
  - A new input case: "inspect the magic mirror and frown" must give exactly one look.
- **Checks:** `python Tools/check_prompts.py` passed 53 of 53 asks (median 1.8 s, about $0.029 per show). Scene turns alone, 3 times: 66 of 66. Input asks, 3 times: 24 of 24. No reply used a word from a parodied original; the lines play the stories ("Iceberg? That's just a fluffy cloud with ambition! Ship is absolutely fine!").
- **Autoplay PIE show:** `NHOS: SETUP human=worrier decoy=overclocker scene=rubber_chicken_case note=throw_once`, then `scene=star_crossed` with 3 actors. An AI was cut in scene 1, the human in scene 2: `NHOS: SHOW END result=lose scenes=2`. 51 calls, none failed. `check_prompts.py --log`: 38 of 38 AI lines legible, none with a story word. The AIs played the detective, the butler, Juliet and Romeo ("Hark! I hold court from this balcony, and suitors bring gifts!").
- **Design doc:** the Rules tab (scene card, note example, typing example, places) and the Tech & Build build list (scene cards, notes) now describe the improv stage and the story cards. `Docs/GameDesign.md` got the same edits; both tabs matched the copy before the edit. The Art Inspiration tab still describes an opera-house stage; T17 should settle that with the improv theater.
