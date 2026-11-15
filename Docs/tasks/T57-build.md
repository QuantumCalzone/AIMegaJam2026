# T57 build sheet: a pass shows as "passed"

Back to [T57](T57.md). A Mac prep session wrote this on 2026-11-15, without the editor. It is written against **`noHumansOnSet` at `b88c6a2`** (T44 and the T45 prep on top of T36), with `BP_Show` and the data files **as T52, T54 and T55 leave them**: by [T52-build.md](T52-build.md), [T54-build.md](T54-build.md) and [T55-build.md](T55-build.md). None of the three had pushed. Line numbers are at `b88c6a2`; T44 moved the checker's lines, not the `prompts.json` lines this sheet changes. Find each line by its text before you change it.

The design doc was read, not changed: Rules rev 27 ("Free Talk": "Passes are visible: “passed” shows next to anyone who passes. The AIs treat silence, and lines that sound too polished, as evidence.") and Bot Prompts rev 81 (the sixth line of "Opening prompt: game rules"). **T57 needs no doc edit.**

The names in this sheet that have no `Graphs/` file (`TalkRound`, `DoesPass`, `Robots`, `SeatId`, `SceneNum`, `Phase`) were confirmed by a byte search of `BP_Show.uasset` at `42b1189` (the method of T55-build part 0).

> **WAITING FOR MY PERSON'S OK (step 1):** the new wording of the old "How a line is typed is never evidence" line, in part 3a. Show it before the commit, with the line it replaces. The doc's line under it goes in word for word and needs no OK.

## In short

- **`BP_Robot`:** a new `SetPassed(On)` (with a file). On: the name over the robot reads "OpenAI (passed)" in `UIStyle`'s `Quiet` color. Off: the plain name in white, as `ResetLook` sets it. A cut robot keeps its stamp (part 1).
- **`BP_Show`** (part 2):
  - **`ShowLine`** (has a file): in Free Talk it calls the new **`PassCue`** before it queues the line. **`PlayTalk` doesn't change:** in Free Talk only `PlayTalk` calls `ShowLine`, and `ShowLine` already gets the `does` text ("passes" for a pass).
  - **`PassCue(Seat, Does)`** (new, file): a pass queues a `"passed"` cue; a spoken line from an actor whose marker is up queues `"unpass"`. `PassSeats` tracks whose marker is up.
  - **`PassClear()`** (new, file): queues `"unpass"` for every seat. **`StartFreeTalk`** and **`EndFreeTalk`** call it (one node each, no files).
  - **`MarkPass(Seat, On)`** (new, file): calls `SetPassed` on one seat's robot, or all of them for seat -1.
  - **`RunCue`** (has a file): the `"passed"` cue calls `MarkPass` and prints `NHOS: PASSED <id> scene=<n> round=<r>`; the `"unpass"` cue calls `MarkPass` with `false`.
- **`prompts.json`:** the old typing line gets a new wording (waiting for the OK), the doc's silence line goes under it word for word, and `asks.free_talk` says a pass is seen (part 3).
- **`free_mode.json`:** no change. `pass_chance` stays 0.1 (part 4, step 2).
- **`Tools/check_prompts.py`:** the doc's line in the file check, the old line refused, a round-2 Free Talk ask after a pass, and a `--log` check that every Free Talk pass shows one marker (part 5). Tried on scratch copies of `42b1189` and `b88c6a2` with part 3: `--offline` passes, 4 more jobs (63 at `b88c6a2`), and `--log` fails a real pre-T57 log (`t36auto.log`) and passes it with the `PASSED` line added.

## Decisions made for my person

My person asked prep sessions to take their own recommendation on design calls. Each is open to change. The T57 session shows this list to my person when it closes the task.

1. **The marker is part of the name over the robot:** "OpenAI (passed)", "You (passed)", in `Quiet` (#C9C3DA) instead of white. No new component: template components don't reach the five robots already placed in `L_Stage` until they are destroyed and placed again (T17, T46), and `L_Stage` is outside T57's Touches. The fallback, if the screenshots show `Quiet` too faint on a bright backdrop, is the same text in white (part 1).
2. **When it shows:** a `"passed"` cue goes into the line queue just before the pass line, so the marker shows as that line comes up. For an AI pass that is just before "<name> is typing..." and then "<name> passes"; for my pass, the marker and the line show together. A cue after the line would show the marker about 2 s late, when the next speaker's typing line starts.
3. **When it goes:** the actor's next spoken line takes it off (an `"unpass"` cue just before that line), and every marker comes off at the end of each Free Talk (`EndFreeTalk`) and again at the start of the next (`StartFreeTalk`). Both are cues, so a marker never changes before the lines in front of it have played. A second pass by the same actor shows the marker again and prints a second `PASSED` line.
4. **`PlayTalk` isn't edited** (it is in T57's Touches): `ShowLine`, which has a file, does the work in Free Talk. `StartFreeTalk` and `EndFreeTalk` get one call node each.
5. **The new wording** (part 3a, waiting for the OK): "Typing is never evidence: the converter fixes the human's spelling, so ignore typos, punctuation, capitals and emoji. Judge what each actor says and does, and how it sounds." Capitals and emoji stay ignored, as the task says, even though the converter keeps them.
6. **The doc's line goes right after it**, in "Spotting the human", as a top-level bullet like the line it sits beside. `game`'s Free Talk line ("One line each per round, or a pass.") doesn't change: the bots already see a pass in the log, and T58 edits that line next.
7. **`asks.free_talk`:** "Pass only if you truly have nothing to add." becomes "Pass only if you truly have nothing to add: everyone sees a pass, and silence is evidence." Not in the doc (the doc doesn't hold the asks).
8. **`pass_chance` stays 0.1** (step 2): free-mode votes pick a random name and read no log, so a free-mode pass never makes a bot a suspect. A 3-scene free show has about 18 AI Free Talk lines, so about 2 AI passes, enough to see AI markers.
9. **A failed AI reply still logs a pass** (T08's rule, unchanged), and now shows "passed" too. The bots may hold that silence against the bot, but replies rarely fail (none in T08's, T20's or T36's runs). If failures turn up in real shows, log a failed reply as "stands still" instead; that would be its own small task.
10. **`NHOS: PASSED` prints when the marker shows** (the cue), with the scene and round of the pass. `PassCue` builds the text when the pass is logged, since the logic runs ahead of the screen (T30).
11. **The checker** gets the round-2 Free Talk ask after a pass (4 more calls per full run), the file checks, and the `--log` check (part 5).

## 0. Before you start (after T55 is pushed)

1. `git log --oneline -8` shows T52, T54 and T55. `git lfs locks` shows no lock on `BP_Show.uasset` or `BP_Robot.uasset`, and no claim on T55. **Lock both** (`git lfs lock`); T57 changes `BP_Robot` too.
2. **What the chain left:**
   - `Graphs/BP_Show/RunCue.txt`: T52 added the `"tie"` branch. Part 2e inserts T57's block before the `"prep"` branch of whatever is pushed. Check `T54.md`'s and `T55.md`'s findings for other `RunCue` changes.
   - `Graphs/BP_Show/ShowLine.txt` and `Graphs/BP_Robot/ResetLook.txt` match the copies in part 2b and part 1. If a chain task changed them, insert T57's lines into the pushed version.
   - `prompts.json`: T52 added the tie sub-bullet under The Cut, T54 changed goal 1, T55 removed `director` and `asks.tiebreak`. None of them touches the lines in part 3. `check_prompts.py`: T52 added `CUT|TIE|REACTIONS DONE` to `LOG_RE` and its `vote_bad` check, T54 added `SHOW END` and `end_bad`, T55 removed `DIRECTOR` and `tiebreak`. Part 5 says where each T57 edit goes among theirs. T54-build leaves `RunCue` as it is.
3. `python Tools/check_prompts.py --offline` passes before you start.
4. **One survey script in `BP_Show`** (`find_nodes` needs the full node class path, T30):
   - **`StartFreeTalk`:** the `CallFunction` node `StartTalkRound` and the exec link into it. Expected (T08): the function sets `Phase`, `TalkRound`, `TalkCount` and `TalkSeat`, clears the pending asks, calls `LoadCannedTalk` with autoplay on, then `StartTalkRound`.
   - **`EndFreeTalk`:** the first exec node after the function entry. Expected (T08, T09, T30): `Set Phase` "free talk done", `CueHeader` (": FREE TALK IS OVER"), a `GameMsgs` add, the `FREETALK DONE` print, then `StartCut`.
   - **Variables:** `PassSeats`, `PassIdx` and `PassBot` must not exist yet. `Robots` is an array of `BP_Robot` references indexed by seat, with empty slots None (T11 `FindRobots`). `DoesPass` is a String (the `pass` template, "passes"). `TalkRound` and `SceneNum` are Integers, `SeatId` a String array, `Phase` a String.
   - **`PlayTalk` only for a check:** every `ShowLine` call in `PlayTalk` gets its `Does` pin from the same value as the entry's `does` (T08: "passes" or "stands still"). No edit.
5. **Callers of `ShowLine`** (`find_nodes` `ShowLine` in `BP_Show`): expected `PlayTurn`, `PlayTalk`, `Tally` and `PlayReact` (T29). Only `PlayTalk` runs while `Phase` is "free talk". If another caller does (T58 isn't built yet), tell my person; `PassCue` would treat its line as a Free Talk line.

## 1. `BP_Robot`: `SetPassed` (new)

`Graphs/BP_Robot/SetPassed.txt` (new):

```lisp
; T57: "passed" by this actor's name, while its last Free Talk line was a pass (BP_Show.MarkPass).
; The name over the robot reads "OpenAI (passed)" in UIStyle's Quiet color; off, the plain name in white,
; as ResetLook sets it. A cut robot keeps its stamp.
(fn SetPassed (On)
  (if (Variables|Default|GetIsCut)
    (return))
  (Rendering|Components|TextRender|SetText :self (Variables|Default|GetLabel) :Value (Utilities|Text|ToText(String) (select On (Utilities|String|Append (Variables|Default|GetDisplayName) " (passed)") (Variables|Default|GetDisplayName))))
  (Rendering|Components|TextRender|SetTextRenderColor :self (Variables|Default|GetLabel) :Value (Math|Conversions|ToColor(LinearColor) :InLinearColor (select On (Class|UIStyle|UIColor :Role "Quiet") (Utilities|Struct|MakeLinearColor :R 1.0 :G 1.0 :B 1.0 :A 1.0)) :InUseSRGB true)))
```

- Create it with `add_function_graph` (one Boolean input, `On`) and write it with `write_graph_dsl`. Every node is in a pushed source: the `TextRender` calls and colors in `ResetLook.txt` and `SetCut.txt`, `select` on colors in `SetPersona.txt`, `Class|UIStyle|UIColor` in `WBP_Unavailable/EventGraph.txt`.
- If `Class|UIStyle|UIColor` won't resolve from an actor Blueprint, use `Quiet`'s value from `Graphs/UIStyle/UIColor.txt`: `(Utilities|Struct|MakeLinearColor :R 0.5841 :G 0.5457 :B 0.7011 :A 1.0)`, and say so under "Findings".
- **No change to `ResetLook`:** it already sets the label to `DisplayName` in white, which clears the marker on Restart (`StageSetup` → `Setup` → `ResetLook`).
- **The `IsCut` guard matters:** `PassClear` at the start of the next Free Talk calls `SetPassed(false)` on every robot, and a cut robot's label holds its stamp ("OPENAI: AI", `SetCut`).
- Compile and save `BP_Robot` before `BP_Show`, so `Class|BPRobot|SetPassed` resolves.

**If T38 lands first:** the marker goes in the bubble's place instead of the label: `SetPassed(true)` shows the robot's bubble with "passed" in the quiet style and no fade, `Hush` skips a robot whose marker is up, and `SetPassed(false)` hides it; `BP_Show`'s side is the same.

## 2. `BP_Show`

### 2a. Which graphs, which have files

| Graph | File in `Graphs/BP_Show/` | T57 changes | How |
|---|---|---|---|
| `ShowLine` | `ShowLine.txt` | In Free Talk, calls `PassCue` first | DSL write from the file (2b) |
| `PassCue` | new | — | DSL write, new file (2c) |
| `PassClear` | new | — | DSL write, new file (2d) |
| `MarkPass` | new | — | DSL write, new file (2d) |
| `RunCue` | `RunCue.txt` | The `"passed"` and `"unpass"` cues | DSL write from the file (2e) |
| `StartFreeTalk` | none | A `PassClear` call before `StartTalkRound` | Node edit (2f) |
| `EndFreeTalk` | none | A `PassClear` call first | Node edit (2f) |
| `PlayTalk` | none | Nothing | Survey only (part 0) |

**New variables in `BP_Show`:** `PassSeats` (Integer array), `PassIdx` (Integer), `PassBot` (`BP_Robot` object reference). `PassBot` is a variable, not a bind, because a bind inside a `ForLoop` can be hoisted out of it (T51).

### 2b. `ShowLine`

New content of `Graphs/BP_Show/ShowLine.txt` (the change is the comment line and the first `if`):

```lisp
; T30: the one place a line reaches my screen; it now goes through the line queue (BPC_LinePlayer.Push).
; T57: in Free Talk a pass puts "passed" by the actor's name, and its next line takes it off (PassCue). The cue goes in just before the line.
(fn ShowLine (Seat Does Says)
  (if (Utilities|String|EqualExactly(String) (Variables|Default|GetPhase) "free talk")
    (CallFunction|PassCue :Seat Seat :Does Does))
  (Variables|Default|SetTmpName Does)
  (if (and (Utilities|String|EqualExactly(String) Does (Variables|Default|GetDoesNothing)) (not (Utilities|String|EqualExactly(String) (Variables|Default|GetPhase) "scene")))
    (Variables|Default|SetTmpName ""))
  (bind _act (CallFunction|DisplayText :Text (Variables|Default|GetTmpName)))
  (bind _say (CallFunction|DisplayText :Text Says))
  (Class|BPCLinePlayer|Push :self (Variables|Default|GetLinePlayer) :StageW (Variables|Default|GetStage) :Seat Seat :Name (Utilities|Array|Get(acopy) (Variables|Default|GetSeatLabel) Seat) :Color (Utilities|Array|Get(acopy) (Variables|Default|GetSeatColors) Seat) :Action _act :Speech _say :IsMe (== Seat (Variables|Default|GetHumanSeat)) :Entry (Variables|Default|GetLineEntry)))
```

- `PassCue` must exist before this is written (2c first).
- T30's rule that `ActorLine` and `ShowLine` follow each other with nothing between (T30-build A4) still holds: `PassCue` runs inside `ShowLine` and doesn't touch `LineEntry`.

### 2c. `PassCue` (new)

`Graphs/BP_Show/PassCue.txt` (new):

```lisp
; T57: a Free Talk pass shows "passed" by that actor's name (the Rules tab, Free Talk). ShowLine calls it
; in Free Talk, before the line goes into the queue, so the marker changes as that line comes up.
; A pass queues a "passed" cue; a spoken line from an actor whose marker is up queues "unpass".
; PassSeats holds the seats whose marker is up, as the logic sees it (it runs ahead of the screen).
(fn PassCue (Seat Does)
  (set PassIdx (Utilities|Array|FindItem (V PassSeats) Seat))
  (if (streq Does (V DoesPass))
    (if (< (V PassIdx) 0)
      (add (V PassSeats) Seat))
    (Class|BPCLinePlayer|Cue :self (Variables|Default|GetLinePlayer) :Kind "passed" :Text (cat "scene=" (str (V SceneNum)) " round=" (str (V TalkRound))) :Num Seat)
    (return))
  (if (>= (V PassIdx) 0)
    (Utilities|Array|RemoveIndex (V PassSeats) (V PassIdx))
    (Class|BPCLinePlayer|Cue :self (Variables|Default|GetLinePlayer) :Kind "unpass" :Text "" :Num Seat)))
```

- Inputs: `Seat` (Integer), `Does` (String).
- `Utilities|Array|FindItem` returns -1 when the seat isn't in the list (as in `BPC_LLMClient/AskProvider.txt`).
- `DoesPass` holds "passes" (the `pass` template). If it turns out empty at run time (the survey shows it is filled when the prompts load), compare with the literal `"passes"` and say so under "Findings".
- `pacing.json` has no `cue_hold` for either kind, so neither cue holds the queue.

### 2d. `PassClear` and `MarkPass` (new)

`Graphs/BP_Show/PassClear.txt` (new):

```lisp
; T57: every "passed" marker comes off at the end of each Free Talk (EndFreeTalk) and at the start of the
; next (StartFreeTalk). A cue, so it waits for the lines in front of it.
(fn PassClear ()
  (clear (V PassSeats))
  (Class|BPCLinePlayer|Cue :self (Variables|Default|GetLinePlayer) :Kind "unpass" :Text "" :Num -1))
```

`Graphs/BP_Show/MarkPass.txt` (new):

```lisp
; T57: shows or clears the "passed" marker on one seat's robot, or on every robot when Seat is -1.
; RunCue calls it when a "passed" or "unpass" cue plays. A seat with no robot is skipped.
(fn MarkPass (Seat On)
  (for _i (range (len (V Robots)))
    (if (or (< Seat 0) (== _i Seat))
      (set PassBot (get (V Robots) _i))
      (Utilities|IsValid (V PassBot)
        (:"Is Valid"
          (Class|BPRobot|SetPassed :self (V PassBot) :On On))
        (:"Is Not Valid")))))
```

- `MarkPass` inputs: `Seat` (Integer), `On` (Boolean). `PassClear` has none.
- If `:Num -1` doesn't take a negative literal, write `:Num (- 0 1)` (T52-build 1b has the same note).
- `(for _i (range ...))` and `(get ... _i)` are in `BPC_LLMClient/FlushLocal.txt`; the `IsValid` form is `BPC_ShowAudio/StopDrum.txt`'s.

### 2e. `RunCue`: the `"passed"` and `"unpass"` cues

Insert this block into the pushed `Graphs/BP_Show/RunCue.txt`, right before `  (if (streq Kind "prep")`:

```lisp
  ; T57: a Free Talk pass shows "passed" by that actor's name; "unpass" takes it off one seat, or every seat (Num -1).
  (if (streq Kind "passed")
    (CallFunction|MarkPass :Seat Num :On true)
    (print (cat "NHOS: PASSED " (get (V SeatId) Num) " " Text))
    (return))
  (if (streq Kind "unpass")
    (CallFunction|MarkPass :Seat Num :On false)
    (return))
```

With T52's version of the file (T52-build 1d), the whole new file is:

```lisp
; T30: a cued screen change, run by BPC_LinePlayer when its turn in the queue comes.
; T20: the cues also carry the sound: the show music under every header, the drum roll with the vote row,
; the stinger and the crowd at the cut, the applause or laughs at the end screen.
(fn RunCue (Kind Text Num)
  (if (streq Kind "phase")
    (Class|BPCShowAudio|PlayMusic :self (V Audio) :Key "show")
    (Class|WBPStage|SetPhase :self (Variables|Default|GetStage) :Phase Text)
    (return))
  (if (streq Kind "banner")
    (Class|WBPStage|ShowBanner :self (Variables|Default|GetStage) :Line Text)
    (return))
  (if (streq Kind "votes")
    (if (Utilities|String|IsEmpty Text)
      (Class|WBPStage|SetVoteOptions :self (Variables|Default|GetStage) :Names (Variables|Default|GetNoNames))
      (return))
    (Class|BPCShowAudio|StartDrum :self (V Audio))
    (CallFunction|ShowVotePick)
    (return))
  (if (streq Kind "cut")
    (Class|BPCShowAudio|Reveal :self (V Audio) :IsHuman (== Num (V HumanSeat)))
    (CallFunction|CutActor :Seat Num)
    (return))
  ; T52: a tie cuts nobody. The drum roll stops with no stinger, the audience laughs, and the reactions start.
  (if (streq Kind "tie")
    (Class|BPCShowAudio|StopDrum :self (V Audio))
    (Class|BPCShowAudio|Sfx :self (V Audio) :Key "laughs" :Pitch 1.0)
    (CallFunction|EndCut)
    (return))
  ; T57: a Free Talk pass shows "passed" by that actor's name; "unpass" takes it off one seat, or every seat (Num -1).
  (if (streq Kind "passed")
    (CallFunction|MarkPass :Seat Num :On true)
    (print (cat "NHOS: PASSED " (get (V SeatId) Num) " " Text))
    (return))
  (if (streq Kind "unpass")
    (CallFunction|MarkPass :Seat Num :On false)
    (return))
  (if (streq Kind "prep")
    (Class|BPCShowAudio|PlayMusic :self (V Audio) :Key "show")
    (CallFunction|ScenePrep)
    (return))
  (if (streq Kind "end")
    (Class|BPCShowAudio|EndCheer :self (V Audio) :Win (V ShowWin))
    (CallFunction|ShowEndScreen)
    (return))
  (print (cat "NHOS: CUE unknown " Kind)))
```

`BPC_LinePlayer.Pump` prints `NHOS: CUE passed scene=1 round=2` before it runs the cue, then `RunCue` prints `NHOS: PASSED <id> scene=1 round=2`.

### 2f. `StartFreeTalk` and `EndFreeTalk`: one `PassClear` call each

Node edits, no files (both are small, but their read-backs aren't safe to write back, T06).

- **`StartFreeTalk`:** add a `CallFunction|PassClear` node. Unlink the exec wire into the `StartTalkRound` call, link that source to `PassClear`, and link `PassClear` to `StartTalkRound`. The cue then plays before the round-1 header.
- **`EndFreeTalk`:** add a `CallFunction|PassClear` node between the function entry and its first exec node. Its cue then plays before the "FREE TALK IS OVER" header, so the vote starts with no marker up.
- T58 will put the last words between the final round and `EndFreeTalk`; markers stay up through them, which fits "until the end of that Free Talk".
- Compile and save `BP_Show`. Write these two edits under "Findings" in `T57.md`, since the graphs have no files.

## 3. `prompts.json`

Each line is as it sits in the file (two tabs before it). Line numbers at `b88c6a2` (the same as at `42b1189`); T52 adds a line after line 30, so after T52 these are one lower. Tried on a scratch copy: the JSON loads, and `--offline` passes with part 5.

**a. `game`, "Spotting the human", line 54.** Replace the line with two lines.

- Now: `"- How a line is typed is never evidence. Ignore punctuation, capitals, spelling and emoji, and judge what each actor says and does.",`
- New, two lines. **The first is my proposed wording and waits for my person's OK** (step 1). The second is the doc's line (Bot Prompts rev 81, "Opening prompt: game rules", sixth line), word for word:

```
		"- Typing is never evidence: the converter fixes the human's spelling, so ignore typos, punctuation, capitals and emoji. Judge what each actor says and does, and how it sounds.",
		"- Silence is evidence, and so is a line that sounds too polished. Notice who passes and who sounds unlike the rest.",
```

- Why this wording: it keeps what still holds (typos and capitals mean nothing, because the converter fixes spelling), drops "never evidence" for how a line *sounds*, and hands over to the doc's line, which says what does count. It keeps the old line's "judge what each actor says and does".
- If my person wants a different wording, the checker needs no change, as long as no `game` line still contains "How a line is typed is never evidence".

**b. `asks.free_talk`, line 124.** In the middle of the line:

- Now: `... Talk about one actor, not a list. Pass only if you truly have nothing to add. Fill: speech, or pass. No actions.",`
- New: `... Talk about one actor, not a list. Pass only if you truly have nothing to add: everyone sees a pass, and silence is evidence. Fill: speech, or pass. No actions.",`
- **Free mode still finds it:** `free_mode.json` matches phases in order by `ask_contains` (case-sensitive in both `BPC_LLMClient.FreeFindPhase` and the relay). The new text contains "Free Talk" and none of "The show is over", "The Cut", "You were just cut" or "Reactions", so it still matches `free_talk`.

Nothing else in `prompts.json` changes. `_readme` line 6 already says "A pass is does 'passes' with says ''", which still holds.

## 4. Step 2: the bots see the pass, and `pass_chance`

- **The pass is still in the log after T30.** `PlayTalk` builds the entry before the line queue sees it (T30 left `ActorLine`'s log write immediate). The Mac's `t36auto.log` (a free autoplay show after T30) has `NHOS: LOG scene 1, free talk round 2 | Player 4 | passes |`, my canned round-2 pass. The run in part 6 confirms it again: every Free Talk pass has a `LOG ... | passes |` line, and the checker matches each one to a marker.
- **A failed reply in free mode:** none happens. In Test for Free, `BPC_LLMClient.FreeReply` builds each reply in the game with no network; through the relay's free mode, only a network error could fail one. A pass in free mode comes only from `pass_chance`.
- **Does a pass make a bot a suspect too often in free mode?** No. Free-mode votes and reasons are random (`FreeReply`'s `vote` branch picks any name in `options`), and read no log. So `pass_chance` only sets how often an AI marker shows: 0.1 gives about 2 AI passes in a 3-scene show. **Leave `free_mode.json` unchanged** (decision 8). This also keeps the relay off T57's list.
- **In the run, count failures:** `grep -cE "NHOS: LLM \S+ (fail|error)" <log>` must print 0. If it doesn't, the pass from that failure shows a marker, which is right by T08's rule (decision 9); name it under "Findings".

## 5. `Tools/check_prompts.py`

Each block with the text it goes after or replaces. Line numbers at `b88c6a2` (T44 added about 150 lines above most of them). T52, T54 and T55 change lines around these; each place says how to keep theirs. Tried on scratch copies of `42b1189` and `b88c6a2` with part 3: `--offline` passes; `build_jobs` makes 4 more jobs ("after a pass"; 63 at `b88c6a2`); `--log` on the Mac's `t36auto.log` fails with `Free Talk passes [('human', '1', '2')], but markers []`, and passes (exit 0, `passes = 1`) on the same log with `NHOS: PASSED human scene=1 round=2` added after the pass.

**a. The docstring.** Before `Exit code 0 means the files are valid and every reply passed its checks.` (line 89). After T52's "A tie (T52)" paragraph, if it is there:

```
Passes (T57): a pass in Free Talk shows "passed" by that actor's name, and
silence and too-polished lines are evidence. The file check finds the design
doc's line in prompts.json 'game', word for word (DOC_SILENCE_LINE), and fails
the old rule that how a line is typed is never evidence. Each persona's
free_talk ask also goes out in round 2, after a round 1 with a pass. --log fails
a show whose Free Talk passes (NHOS: LOG ... | passes |) and "passed" markers
(NHOS: PASSED) don't match one for one.
```

**b. `DOC_SILENCE_LINE`**, right after the `DOC_NOTE_LINES` list closes (its `]`, line 140), after T52's `DOC_TIE_LINE` if it is there:

```python
# T57: the design doc's silence rule (Bot Prompts, "Opening prompt: game rules"), word for word.
DOC_SILENCE_LINE = "Silence is evidence, and so is a line that sounds too polished. Notice who passes and who sounds unlike the rest."
```

**c. The file check.** In `check_files`, after the `for line in DOC_NOTE_LINES:` loop's `errors.append(...)` line (line 646), after T52's tie checks if they are there:

```python
    if not any(DOC_SILENCE_LINE in g for g in game):
        errors.append("prompts.json: 'game' lost the design doc's silence rule (DOC_SILENCE_LINE)")
    if any("How a line is typed is never evidence" in g for g in game):
        errors.append("prompts.json: 'game' still says how a line is typed is never evidence; since T57 a too-polished line is evidence")
```

**d. A Free Talk ask in round 2, after a pass.** In `Show.actor_cases`, right after the `cases["vote"] = ...` line (line 882):

```python
        # T57: round 2, after a round 1 in which Player 1 passed (TALK[0]), so the pass is in the log.
        cases["free_talk_r2"] = self.actor_state(pid, "free_talk", "free talk, round 2 of 2", self.log(turns=3, talk=1))
```

In `build_jobs`, inside `for pid in personas:`, right after the `for ask in ACTOR_ASKS:` loop (after its `jobs.append((ask, show.name(pid), ...))` line, line 1363). If T52's `if "reaction" in asks:` block is there, put this after it:

```python
            if "free_talk" in asks:  # T57: Free Talk round 2, with round 1's pass in the log
                st = cases["free_talk_r2"]
                ctx = {"places": places, "props": props, "actors": actors, "me": show.name(pid), "options": [],
                       "note": st["you"]["note"]}
                pv = provider_for(data, "actor", pid)
                jobs.append(("free_talk", f"{show.name(pid)} after a pass", pv,
                             request_body(data, pv, "actor", system_text(data, "actor", pid), st), ctx))
```

- The job's ask is `"free_talk"`, so `check_reply` checks it as a Free Talk line, and `--ask free_talk` runs both Free Talk cases.
- `TALK[0]` has Player 1 (`visionary`) passing, so for `visionary` the pass in the log is its own.

**e. `--log`: every Free Talk pass shows one marker.**

- **`LOG_RE`** (line 1249): add `PASSED` to the alternation, keeping T52's, T54's and T55's kinds. With all three, it reads:

  ```python
  LOG_RE = re.compile(r"NHOS: (SHOW READY|SHOW END|RESTART|SEATS|SETUP|LOG|CLOSING|CUT|TIE|REACTIONS DONE|PASSED)\b ?(.*)$")
  ```

- After `    n = bad = clock_bad = 0` (line 1280), next to T52's `vote_bad` and T54's `end_bad` lines: `    pass_bad = 0  # T57: shows whose passes and "passed" markers don't match`
- After `        seats = total = None` (line 1284): `        cast_ids, passes, marks = [], [], []  # T57`
- At the top of `for kind, rest in show:`, before `            if kind == "SEATS":` (T52 puts its `CUT`/`TIE` block there too, and T54 its `SHOW END` handling; any order works, since each `continue`s):

  ```python
              if kind == "PASSED":
                  # T57: "NHOS: PASSED <seat id> scene=<n> round=<r>", printed when the marker shows.
                  m = re.match(r"(\S+) scene=(\d+) round=(\S+)", rest)
                  if m:
                      marks.append(m.groups())
                  continue
  ```

- In the `SEATS` branch, after `                    seats = int(m.group(1))` and before its `continue`:

  ```python
                  m = re.search(r"cast=(\S+)", rest)
                  if m:
                      cast_ids = m.group(1).split(",")  # T57: Player n is cast_ids[n - 1]
  ```

  `NHOS: SEATS human=4 seats=5 cast=overclocker,copycat,visionary,human,worrier` (from `t36auto.log`): Player 4 is `human`, `cast` is in seat order.
- In the `LOG` branch, between `                parts = rest.split(" | ", 3)` and `                if len(parts) < 4:`:

  ```python
                  # T57: every Free Talk pass shows a "passed" marker (NHOS: PASSED, with the seat id).
                  # A pass's line ends "| passes |", which the strip above leaves as 3 parts.
                  m = re.match(r"scene (\d+), free talk round (\d+)$", parts[0])
                  if m and len(parts) >= 3 and parts[2].rstrip(" |") == "passes":
                      pn = re.match(r"Player (\d+)$", parts[1])
                      k = int(pn.group(1)) if pn else 0
                      passes.append((cast_ids[k - 1] if 0 < k <= len(cast_ids) else parts[1], m.group(1), m.group(2)))
  ```

  It must sit before the length check: a pass's `says` is empty, and `rest` was stripped, so its line splits into 3 parts and the length check would skip it. It also sits before the `if parts[1] == human:` branch, so my passes count.
- Before the `print(f"Show {i}: ...")` summary line (line 1341):

  ```python
          if sorted(passes) != sorted(marks):
              pass_bad += 1
              print(f"[FAIL] show {i} | PASSED | Free Talk passes {sorted(passes)}, but markers {sorted(marks)}")
  ```

  and the summary line gets `, passes = {len(passes)}` before its final period, keeping T52's `ties = {ties}`. T54 prints its `SHOW END` lines separately; keep them.
- The return (line 1343) gets `or pass_bad`: with T52's and T54's it reads `return 1 if bad or clock_bad or vote_bad or end_bad or pass_bad else 0`.
- **Order in the log:** `LOG` prints when the pass is logged; `PASSED` when its cue plays, later. Both are in the same show, and the check compares sets, so the order doesn't matter. A log cut off before a show's queue drains (a Restart mid-Free-Talk) would fail; the check reads the last show by default.

**Runs:** `python Tools/check_prompts.py --offline`. If the relay is up: `python Tools/check_prompts.py --relay --free` (no tokens; every ask comes back in shape). A paid `--ask free_talk` (8 calls) shows whether the bots use passes and polish as evidence; offer it to my person, it isn't needed for the Done-when.

## 6. The check

The Done-when: `--offline` and `--relay --free` pass; a free autoplay show shows "passed" by my robot after my round-2 pass, and by any bot that passes, and the marker is gone in the next scene's Free Talk; screenshots from one free show in a game window show the marker reads well.

### Run A: free autoplay, in a game window on the saved assets

`Local/switches.json`: `"autoplay": true`, `"mode": "free"`, `"spare_human": true`, `"force_tie": false`, `"fast_lines": true`, `"burn_test": false`, `"ai_seats": 0`. `spare_human` keeps me on stage, so the show plays 3 scenes (4 after a natural tie).

```bash
"<UE_ROOT>/Engine/Binaries/Win64/UnrealEditor.exe" "<PROJECT>" -game -windowed -ResX=1600 -ResY=900 -log=T57pass.log
```

On Windows the log is `Saved/Logs/T57pass.log` (on a Mac, `~/Library/Logs/AIMegaJam2026/T57pass.log`). Then:

```bash
grep -E "NHOS: (SEATS|CUE (phase FREE|passed|unpass)|PASSED|LOG scene [0-9]+, free talk round [0-9]+ \| [^|]+ \| passes|FREETALK DONE|SHOW END)" Saved/Logs/T57pass.log
```

Expected for scene 1 (my canned round-2 line is "pass"; `<h>` is my Player number from `SEATS`):

```
NHOS: SEATS human=<h> seats=5 cast=<ids>
NHOS: LOG scene 1, free talk round 2 | Player <h> | passes |
NHOS: FREETALK DONE scene=1 entries=<n>
NHOS: CUE unpass                                  (StartFreeTalk's PassClear, before the round-1 header)
NHOS: CUE phase FREE TALK: SCENE 1, ROUND 1 OF 2
NHOS: CUE phase FREE TALK: SCENE 1, ROUND 2 OF 2
NHOS: CUE passed scene=1 round=2
NHOS: PASSED human scene=1 round=2
NHOS: CUE unpass                                  (EndFreeTalk's PassClear)
```

- The `LOG` and `FREETALK DONE` lines come early, when the logic runs; the `CUE` lines come as the queue plays (T30). The header text is as T53 left it.
- Each AI pass adds one `LOG ... | passes |` line, one `CUE passed` and one `PASSED <ai id> scene=<n> round=<r>`. An AI that speaks again in round 2 after a round-1 pass adds a `CUE unpass` right before its line plays.
- Scene 2's Free Talk: its own `CUE unpass` first, and no `PASSED human` (my scene-2 lines are spoken). In the screenshots, my robot's label is plain again.
- The show ends with `NHOS: SHOW END result=win ...`. No `LogScript` warning and no `NHOS: CUE unknown`.
- `grep -cE "NHOS: LLM \S+ (fail|error)" Saved/Logs/T57pass.log` prints 0 (part 4).

Then `python Tools/check_prompts.py --log Saved/Logs/T57pass.log` passes, with `passes = <n>` equal to the count of `PASSED` lines.

### Run B: the screenshots, in a game window

The same switches with `"fast_lines": false`, and `-log=T57shots.log`. Take screenshots while the show plays: on the Mac, `screencapture -l<window id>` in a loop every ~0.75 s as T36 did; on the PC, the method T52 and T55 used. Keep them in `Saved/T57/shots/` (not in git):

1. **`passed_me.png`:** scene 1, Free Talk round 2, right after `NHOS: PASSED human` prints. Expect: my robot's label reads "<my name> (passed)" in the lavender `Quiet`, the other labels white, and the chat's last line "<my name> passes".
2. **`passed_ai.png`:** any AI pass, if the run has one (`PASSED <ai id>`). If none comes, run again, or name it under "Findings": run A's log already proves AI markers.
3. **`cleared.png`:** scene 2, Free Talk round 1. Expect: no label says "(passed)".
4. **`passed_me_p12.png`:** shot 1 again at `-ResX=1280 -ResY=720` (the doc checks every screen at both sizes); scene 1 of a second run serves.

As a first-time player, judge: can you read "(passed)" at a glance at both sizes, on every backdrop the run shows? Does the lavender read as "went quiet" and never as "cut" (the stamp is red)? Does the longer label run into a neighbor's? If the lavender is too faint, switch to white (decision 1) and say so. Write what you saw under "Findings".

**Afterward:** set `autoplay`, `spare_human` and `fast_lines` back to false in `Local/switches.json`, and close each game window.

### The commit

`Content/NHOS/Core/BP_Show.uasset`, `Content/NHOS/Stage/BP_Robot.uasset`, `Content/NHOS/Data/prompts.json`, `Tools/check_prompts.py`, `Graphs/BP_Show/ShowLine.txt`, `Graphs/BP_Show/RunCue.txt`, `Graphs/BP_Show/PassCue.txt` (new), `Graphs/BP_Show/PassClear.txt` (new), `Graphs/BP_Show/MarkPass.txt` (new), `Graphs/BP_Robot/SetPassed.txt` (new), `Docs/tasks/T57.md`, `Docs/Plan.md` (the box), `Docs/DevLog.md`. All are in T57's Touches. Unlock `BP_Show` and `BP_Robot` after the push.

## 7. Knock-on: tell, don't change

- **T58 (last word):** builds on this sheet (see [T58-build.md](T58-build.md)). A last word goes through `PlayTalk` and `ShowLine` while `Phase` is still "free talk", so a pass in a last word shows "passed" too. T58 makes `PassCue`'s text say `round=last` there, and widens part 5e's `LOG` match to "last word".
- **T38 (speech bubbles):** if it lands after T58 as planned, the marker moves into the bubble's place (the line under part 1). T38's bubble sits at the label's top plus about 6 cm, so the longer label doesn't collide with it.
- **T34 (the in-show screen):** T32's row 2 (name tags with no plate) covers the labels; the "(passed)" text is part of the label, so a plate behind the label covers it too.
- **T61 (the stagehand):** its Free Talk earpiece line ("You can pass, but they notice silence.") now matches what the bots read.
- **The design doc's "2–3 rounds"** (Rules, Free Talk) is still 2 in the game. Not T57's.
