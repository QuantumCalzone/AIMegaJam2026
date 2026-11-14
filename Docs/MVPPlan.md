# MVP plan: No Humans On Set

The living plan for the MVP prototype of our jam game. The design is in [GameDesign.md](GameDesign.md). Say **"Next task"** to build the next step.

In this file, "I" and "my" mean the person at the keyboard. "Claude" means the agent doing the task.

**Next up:** T08 · Sonnet 5.5 · medium (then T09 · Opus 5.5 · high, which needs T08)

## Goal

Answer one question as fast as possible: **is it fun to fool an all-AI cast, and do the AIs catch a human at a fair rate (not every time, not never)?** Nothing else matters until a playtest answers it.

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

Written Fri Nov 13, 2026, about 3:20 PM PST. The deadline is Sun Nov 15, 5:59 PM PST (Nov 16, 01:59 UTC). That leaves about 50 hours, sleep included.

| Target | When (PST) |
|---|---|
| Spikes done (T01, T02) | Fri Nov 13, evening |
| Loop runs end to end (T10), robots on stage (T11) and the playtest gate (T12) | Sat Nov 14, morning |
| MVP packaged (T15) | Sat Nov 14, about 3 PM |
| Everything the judges score that the MVP leaves out (see "After the MVP") | Sat 3 PM to Sun 2 PM |
| Submit | Sun Nov 15, by 3 PM. Keep 3 hours of margin. |

15 tasks at up to an hour each is about 15 hours of agent time, plus your time on checks and playtests. If we fall behind, cut T14 first, then hold T13 to one hour. T11 can also move after the gate.

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

- [ ] **T08 Free Talk**
  - **Model and effort:** Sonnet 5.5, medium. The same ask-and-log pattern as T07, with one speaker at a time.
  - **Depends on:** T07
  - **Needs:** editor + Unreal MCP running, my API key.
  - **Steps:**
    1. After turn 3, run 2 rounds. Each round has a new random order and one speaker at a time, so each AI sees the lines before its own.
    2. On my turn I type a line or press Pass. My line goes through the input LLM and into the shared log in the same form as an AI line.
    3. An AI can pass. A pass is logged as a pass.
  - **Done when:** with autoplay on, a PIE run prints `NHOS: FREETALK DONE` after 8 talk entries (lines or passes).
  - **Touches:** `Content/NHOS/Core/BP_Show.uasset`, `Content/NHOS/UI/WBP_Stage.uasset`.

- [ ] **T09 The Cut: votes, tiebreak and reveal**
  - **Model and effort:** Opus 5.5, high. Several new parts: the vote screen, the tally and the Director call.
  - **Depends on:** T08
  - **Needs:** editor + Unreal MCP running, my API key.
  - **Steps:**
    1. Ask all AIs at once for a vote and a one-line reason. I pick a name with a button and type a reason. Nobody can vote for themselves; a bad vote is asked again once, then replaced by a random valid one.
    2. Count the votes. Show each vote with its reason, and add them to the shared log.
    3. On a tie, ask the Director, who is not an actor, to choose among the tied actors with a one-line reason.
    4. Show the stamp, `<NAME>: AI` or `<NAME>: HUMAN`, and mark that seat as cut.
  - **Done when:** with autoplay on, a PIE run prints `NHOS: CUT <persona> tiebreak=<yes|no>` and the stamp shows (screenshot). With the local `force_tie` switch on, the Director's line appears.
  - **Touches:** `Content/NHOS/Core/BP_Show.uasset`, `Content/NHOS/UI/WBP_Stage.uasset`.

- [ ] **T10 Reactions, the final two, end screens and restart**
  - **Model and effort:** Opus 5.5, high. Many parts, and the first run of the whole loop usually needs debugging.
  - **Depends on:** T09
  - **Needs:** editor + Unreal MCP running, my API key.
  - **Steps:**
    1. Reactions: the cut actor first, then each remaining bot, then me, one line each, all into the shared log.
    2. Then branch: if I was cut, I lose. If two actors remain, I win. Otherwise go back to Scene Prep with a new scene card and a new note.
    3. `WBP_EndScreen`: win or lose, each AI's vote reasons from the show, and one closing line from each AI on who it thought was human.
    4. A Restart button starts a new show without leaving PIE.
  - **Done when:** with autoplay on, a PIE run plays a whole show and prints `NHOS: SHOW END result=<win|lose> scenes=<n>`. Restart starts a second show that also reaches `NHOS: SHOW END` (screenshots of the end screen).
  - **Touches:** `Content/NHOS/Core/BP_Show.uasset`, `Content/NHOS/UI/WBP_Stage.uasset`, new `Content/NHOS/UI/WBP_EndScreen.uasset`.

### The cast on stage

- [ ] **T11 The cast on stage: four box robots**
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
  - **Touches:** `Content/NHOS/Maps/L_Stage.umap`, `Content/NHOS/Core/BP_Show.uasset`, `Content/NHOS/UI/WBP_Stage.uasset`, `Content/NHOS/Core/BP_ShowPlayerController.uasset` (only if the camera needs it), new `Content/NHOS/Stage/BP_Robot.uasset`, new `Content/NHOS/Stage/M_Robot.uasset`.

### Gate

- [ ] **T12 Go/no-go gate: I play 3 shows**
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

- [ ] **T13 Fix what the playtest found**
  - **Model and effort:** Opus 5.5, high. Prompt tuning and rule changes, with debugging.
  - **Depends on:** T12
  - **Needs:** my API key, my playtest (one show). Editor + Unreal MCP running if a Blueprint changes.
  - **Steps:** T12 writes them. Expect prompt changes checked with `Tools/check_prompts.py`, rule changes (rounds, votes, the tiebreak) and the model choice in `llm.json`.
  - **Done when:** T12 writes the check. At the least: I play one more full show, and the top finding from Playtest 1 is fixed.
  - **Touches:** T12 lists them. Likely `Content/NHOS/Data/*.json` and `Content/NHOS/Core/BP_Show.uasset`.

- [ ] **T14 Timers and typing delay**
  - **Model and effort:** Sonnet 5.5, medium. Small additions to phases that already work.
  - **Depends on:** T12
  - **Needs:** editor + Unreal MCP running, my API key.
  - **Steps:**
    1. Add a countdown to my input: 30 seconds for a scene turn, 45 for a Free Talk line, 15 for a reaction. The values come from a data file.
    2. When time runs out: a scene turn becomes "looks around", a Free Talk line becomes a pass, a reaction stays silent.
    3. AI lines in Free Talk and in reactions appear after a short random typing delay.
    4. No times go in the shared log.
  - **Done when:** in PIE with autoplay off, letting the scene timer run out prints `NHOS: TIMEOUT scene`, and my actor looks around in the log.
  - **Touches:** `Content/NHOS/Core/BP_Show.uasset`, `Content/NHOS/UI/WBP_Stage.uasset`, `Content/NHOS/Data/scenes.json`.

- [ ] **T15 Package a Windows Development build and play a show in it**
  - **Model and effort:** Sonnet 5.5, medium. It repeats T02's steps with the whole game.
  - **Depends on:** T13, T14
  - **Needs:** my API key, my playtest (one show), a Windows machine, the editor closed.
  - **Steps:**
    1. Run the package command from `CLAUDE.local.md` in the background.
    2. Put the key file where the decision note says, and run the packaged game with autoplay on.
    3. I play one full show in the packaged game with autoplay off.
    4. Write the result, the build size and any packaging fix in Findings.
  - **Done when:** the packaged game's log shows `NHOS: SHOW END` and no `NHOS: LLM ... fail` line, and I finished one show in it.
  - **Touches:** the Findings section, `Packaged/` (not in git), `Config/*.ini` only if packaging needs a fix.

## After the MVP

Not planned yet. T12 turns this list into tasks, sized to the time that is left. The judges score visuals, audio and level design as much as fun, and the submission has fixed parts.

- **How a judge plays.** The MVP reads a key from a developer's file. A judge has no such file. Before we submit, the game needs the key-entry screen or the relay from the design doc.
- The 3D café stage, built on T11's set and robots, with Move, Look, Grab, Throw and Give.
- Audio.
- A fifth persona and more scene cards and notes.
- A 30 to 60 second gameplay video, the itch.io page (it must explain the key setup), and the zip named `TeamName_GameName`. The zip must be under 1 GB; the unzipped build can be larger.
- The lists for the submission form: outside assets with their licenses, tools used, and work made before the jam.

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
