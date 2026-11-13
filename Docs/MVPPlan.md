# MVP plan: No Humans On Set

The living plan for the MVP prototype of our jam game. The design is in [GameDesign.md](GameDesign.md). Say **"Next task"** to build the next step.

In this file, "I" and "my" mean the person at the keyboard. "Claude" means the agent doing the task.

**Next up:** T02 · Opus 5.5 · high

## Goal

Answer one question as fast as possible: **is it fun to fool an all-AI cast, and do the AIs catch a human at a fair rate (not every time, not never)?** Nothing else matters until a playtest answers it.

## Scope

**In:**

- One café scene set.
- A text-only stage: a UMG log and an input box. No 3D.
- One human player plus 3 AI personas. That is a cast of 4, so a show has 2 scenes.
- The full show loop from the Rules tab: Scene Prep, The Scene, Free Talk, The Cut with reveal and reactions, repeat to the final two, win and lose screens with the AIs' reasoning, restart.

**Out:**

- 3D staging and animation, audio, polish, extra sets.
- More than one LLM provider. Every persona, the input LLM and the Director run on **Anthropic (Claude)** for now.
- The relay and the key-entry screen. The key comes from a file on the developer's machine.

**Riskiest work first.** T01 and T02 prove that this Blueprint-only project can call the Claude API and parse the JSON reply, in PIE and in a packaged Windows build, before any game logic exists.

## Time check

Written Fri Nov 13, 2026, about 3:20 PM PST. The deadline is Sun Nov 15, 5:59 PM PST (Nov 16, 01:59 UTC). That leaves about 50 hours, sleep included.

| Target | When (PST) |
|---|---|
| Spikes done (T01, T02) | Fri Nov 13, evening |
| Loop runs end to end (T10) and the playtest gate (T11) | Sat Nov 14, morning |
| MVP packaged (T14) | Sat Nov 14, about 3 PM |
| Everything the judges score that the MVP leaves out (see "After the MVP") | Sat 3 PM to Sun 2 PM |
| Submit | Sun Nov 15, by 3 PM. Keep 3 hours of margin. |

14 tasks at up to an hour each is about 14 hours of agent time, plus your time on checks and playtests. If we fall behind, cut T13 first, then hold T12 to one hour.

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
- **Where things live.** Assets go under `Content/NHOS/` (`Maps/`, `Core/`, `UI/`). Files the game reads at runtime go in `Content/NHOS/Data/` as `.json`. The API key and local switches go in `Local/` in the project root, which git ignores. The key file is `Local/llm_key.json`; copy it from `Docs/llm_key.example.json`. Blueprint reads it at `Get Project Directory` + `Local/llm_key.json`.
- **API keys never go in git, and never into chat.** I paste my key into the key file myself.
- **Prompts are files, not Blueprint strings.** The opening game prompt, the base prompt, the personas, the input LLM prompt and the scene cards live in `Content/NHOS/Data/`, so they diff in git. Store long text as an array of lines.
- **One provider.** All calls go to the Claude Messages API. The model, effort and token limit for each role (actor, input LLM, Director) are values in `Content/NHOS/Data/llm.json`. Start with `claude-opus-5-5` at low effort. T02 records seconds per call and cost per show; a faster or cheaper model is then my call.
- **One reply shape.** Every ask (scene turn, Free Talk line, vote, reaction, tiebreak) gets back the same small JSON object, with unused fields empty. One parser serves the whole game.
- **The shared log** is what the AIs read. Every actor's lines have the same form, human or AI. It never holds my raw input, times, errors, anyone's note, or who has the decoy. Game messages reach the AIs in a separate field that actors can't write to.
- **Check lines.** Anything a Done-when check reads is printed with the prefix `NHOS:` to the editor log (`Saved/Logs/AIMegaJam2026.log`). It never goes in the shared log.
- **Autoplay.** From T07 on, a local switch makes the human seat play canned lines, so an agent can run a whole show unattended and read the result in the log.
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

- [ ] **T02 Spike: the same call in a packaged Windows build, and record the decision**
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

- [ ] **T03 Prompt and data files**
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

- [ ] **T04 Stage screen: a log and an input box**
  - **Model and effort:** Sonnet 5.5, medium. Small UMG work, fully specified here.
  - **Depends on:** T02 (the spikes finish before any game work starts)
  - **Needs:** editor + Unreal MCP running.
  - **Steps:**
    1. `WBP_Stage`: a header line for the phase, a scrolling log, and an input box with a Send button. Enter also sends.
    2. `BP_ShowGameMode` and `BP_ShowPlayerController` show the widget when `L_Stage` starts, with the mouse cursor on and the keyboard focus in the input box.
    3. Give the widget one function, `AddLogLine`. For now, sent text goes straight to the log.
  - **Done when:** in PIE, typing `hello` and pressing Enter adds the line to the on-screen log (screenshot), and the input box is empty and focused again.
  - **Touches:** new `Content/NHOS/UI/WBP_Stage.uasset`, new `Content/NHOS/Core/BP_ShowGameMode.uasset`, new `Content/NHOS/Core/BP_ShowPlayerController.uasset`, `Content/NHOS/Maps/L_Stage.umap`.

- [ ] **T05 One AI reply on screen**
  - **Model and effort:** Opus 5.5, high. It turns the spike into the client that every later task calls.
  - **Depends on:** T03, T04
  - **Needs:** editor + Unreal MCP running, my API key.
  - **Steps:**
    1. At start, `BP_Show` loads `llm.json`, `prompts.json` and `personas.json`. If a file or the key is missing, the screen says "AI service unavailable" and why.
    2. `BPC_LLMClient` gets `Ask(Tag, System, User)` and an `OnAnswer(Tag, Ok, reply fields)` event. Several asks can be in flight at once. An error, a refusal or bad JSON gives `Ok = false`.
    3. On Send, ask one persona (The Worrier) with the game prompt, the base prompt and the persona as the system text, and show the reply's speech in the log under the persona's name.
    4. Print `NHOS: LLM <tag> ok <seconds>` or `NHOS: LLM <tag> fail <reason>` for every call.
  - **Done when:** in PIE, a typed question gets an in-character answer in the on-screen log within about 15 seconds, and the editor log shows `NHOS: LLM ... ok`. With the key file renamed, the screen shows "AI service unavailable".
  - **Touches:** `Content/NHOS/Core/BPC_LLMClient.uasset`, `Content/NHOS/Core/BP_Show.uasset`, `Content/NHOS/UI/WBP_Stage.uasset`.

### The show loop

- [ ] **T06 Show setup and Scene Prep**
  - **Model and effort:** Opus 5.5, high. It sets the show state that T07 to T10 all extend.
  - **Depends on:** T05
  - **Needs:** editor + Unreal MCP running.
  - **Steps:**
    1. `BP_Show` holds the show state: the phase, the scene number, 4 seats (persona, human or AI, cut or not, note) and the shared log.
    2. At start: draw my persona at random, give the other three to the AIs, pick a scene card, and give every seat the director's note except one random seat, which gets the decoy.
    3. The screen shows the cast, the scene card, my role and my note. It never shows who has the decoy.
    4. Print `NHOS: SETUP human=<persona> decoy=<persona> scene=<id>`.
  - **Done when:** two PIE runs each print a `NHOS: SETUP` line, and the screen shows the cast, the scene card and my note (screenshot).
  - **Touches:** `Content/NHOS/Core/BP_Show.uasset`, `Content/NHOS/UI/WBP_Stage.uasset`, new `Content/NHOS/Core/E_ShowPhase.uasset`, new `Content/NHOS/Core/S_Seat.uasset`.

- [ ] **T07 The Scene: three simultaneous turns**
  - **Model and effort:** Opus 5.5, high. Parallel asks that must all return before the turn plays out; the hardest Blueprint part.
  - **Depends on:** T06
  - **Needs:** editor + Unreal MCP running, my API key.
  - **Steps:**
    1. For each of 3 turns, ask the three AIs at once. Each gets the cast, the scene card, its own note, the shared log and the ask. Meanwhile I type my turn, and the input LLM turns it into the same reply shape.
    2. When all four turns are in, cap each line at 25 words, add them to the shared log in random order, and show them. Print each shared-log line as `NHOS: LOG ...` too.
    3. A reply that fails or can't be parsed makes that actor look around. No error goes in the shared log.
    4. Add autoplay: if the local switch file says so, the human seat sends canned lines.
  - **Done when:** with autoplay on, a PIE run prints `NHOS: SCENE 1 TURN 3 DONE` and the on-screen log holds 12 turn lines in mixed order (screenshot). With autoplay off, one turn I type shows up in the same form as the AI lines.
  - **Touches:** `Content/NHOS/Core/BP_Show.uasset`, `Content/NHOS/Core/BPC_LLMClient.uasset`, `Content/NHOS/UI/WBP_Stage.uasset`, the local switch file (not in git).

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

### Gate

- [ ] **T11 Go/no-go gate: I play 3 shows**
  - **Model and effort:** Opus 5.5, high. It judges the design from evidence and reshapes the plan.
  - **Depends on:** T10
  - **Needs:** my playtest, my API key, editor running.
  - **Steps:**
    1. I play 3 full shows in PIE with autoplay off, and give notes: was it fun, where it dragged, were the AIs' suspicions fair, how each show ended.
    2. Claude reads the `NHOS:` lines of the three shows and writes "Playtest 1" in Findings: how often and in which scene I was cut, AIs cut by mistake, seconds per call, cost per show, and my notes.
    3. Claude proposes go or no-go, with plan changes: the steps of T12, any task to add, drop or reorder, and a task list for the time after the MVP.
    4. After I agree, Claude commits the changes as `Plan: ...`.
  - **Done when:** Findings has a "Playtest 1" entry with the three results and a go/no-go decision I confirmed, and T12's steps are filled in.
  - **Touches:** `Docs/MVPPlan.md`, `Docs/DevLog.md`.

### After the gate

- [ ] **T12 Fix what the playtest found**
  - **Model and effort:** Opus 5.5, high. Prompt tuning and rule changes, with debugging.
  - **Depends on:** T11
  - **Needs:** my API key, my playtest (one show). Editor + Unreal MCP running if a Blueprint changes.
  - **Steps:** T11 writes them. Expect prompt changes checked with `Tools/check_prompts.py`, rule changes (rounds, votes, the tiebreak) and the model choice in `llm.json`.
  - **Done when:** T11 writes the check. At the least: I play one more full show, and the top finding from Playtest 1 is fixed.
  - **Touches:** T11 lists them. Likely `Content/NHOS/Data/*.json` and `Content/NHOS/Core/BP_Show.uasset`.

- [ ] **T13 Timers and typing delay**
  - **Model and effort:** Sonnet 5.5, medium. Small additions to phases that already work.
  - **Depends on:** T11
  - **Needs:** editor + Unreal MCP running, my API key.
  - **Steps:**
    1. Add a countdown to my input: 30 seconds for a scene turn, 45 for a Free Talk line, 15 for a reaction. The values come from a data file.
    2. When time runs out: a scene turn becomes "looks around", a Free Talk line becomes a pass, a reaction stays silent.
    3. AI lines in Free Talk and in reactions appear after a short random typing delay.
    4. No times go in the shared log.
  - **Done when:** in PIE with autoplay off, letting the scene timer run out prints `NHOS: TIMEOUT scene`, and my actor looks around in the log.
  - **Touches:** `Content/NHOS/Core/BP_Show.uasset`, `Content/NHOS/UI/WBP_Stage.uasset`, `Content/NHOS/Data/scenes.json`.

- [ ] **T14 Package a Windows Development build and play a show in it**
  - **Model and effort:** Sonnet 5.5, medium. It repeats T02's steps with the whole game.
  - **Depends on:** T12, T13
  - **Needs:** my API key, my playtest (one show), a Windows machine, the editor closed.
  - **Steps:**
    1. Run the package command from `CLAUDE.local.md` in the background.
    2. Put the key file where the decision note says, and run the packaged game with autoplay on.
    3. I play one full show in the packaged game with autoplay off.
    4. Write the result, the build size and any packaging fix in Findings.
  - **Done when:** the packaged game's log shows `NHOS: SHOW END` and no `NHOS: LLM ... fail` line, and I finished one show in it.
  - **Touches:** the Findings section, `Packaged/` (not in git), `Config/*.ini` only if packaging needs a fix.

## After the MVP

Not planned yet. T11 turns this list into tasks, sized to the time that is left. The judges score visuals, audio and level design as much as fun, and the submission has fixed parts.

- **How a judge plays.** The MVP reads a key from a developer's file. A judge has no such file. Before we submit, the game needs the key-entry screen or the relay from the design doc.
- The 3D café stage and the robots, with Move, Look, Grab, Throw and Give.
- Audio.
- A fifth persona and more scene cards and notes.
- A 30 to 60 second gameplay video, the itch.io page (it must explain the key setup), and the zip named `TeamName_GameName`, under 1 GB.
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
