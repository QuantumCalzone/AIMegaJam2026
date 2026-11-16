# T87 build sheet: when I win, every AI reacts to the reveal, the cut ones too

Back to [T87](T87.md). A prep session (no editor) wrote this on 2026-11-15 against `noHumansOnSet` at **`b515048`** (T78's closing commit). It is a plan, not a record: nothing here was written to the editor. When T87 writes a graph, its source goes to `Graphs/` as usual.

**Sources read, as built:** `Graphs/BP_Show/` (`EndShow`, `EndReveal`, `RevealRivals`, `RunCue`, `CueEnd`, `CueHeader`, `CueBanner`, `CueCut`, `TieCut`, `HandleReply`, `PlayReact`, `ShowLine`, `StageLine`, `ActorLine`, `LineInfo`, `TakeEmo`, `EmoWord`, `FeelsId`, `KeepEmo`, `HumanFeels`, `ApplyFace`, `TakeFace`, `SetWinReason`, `LastSceneDone`, `NextLastWord`, `NextTalker`, `ActorState`, `StoreTell`, `TimerFor`), `Graphs/BP_Robot/` (`SetCut`, `ResetLook`, `Emote`, `EmoteStop`, `EmoteTick`, `Say`, `Typing`, `Cheer`, `IsDown`, `SetLit`, `SetPassed`, `HideBubble`, `LookAt`, `Enq`, `StartAct`, `YawTo`, `WatchShow`, `DressFromShow`, `EventGraph`), `Graphs/BPC_LinePlayer/` (`Push`, `Pump`, `PlayCur`, `BubbleBot`, `CueHoldFor`, `FindShow`), `Graphs/BPC_LLMClient/` (`Ask`, `AskProvider`, `Deliver`, `FlushLocal`, `FreeReply`, `FreeFindPhase`), `Graphs/BPC_Analytics/` (`CuePhase`, `PhaseKey`), `Graphs/BPC_ShowAudio/` (`PhaseKey`, `PlayPhase`), `Graphs/BP_StageDirector/` (`PlayLine`, `PlayPart`, `ParsePart`, `DoVerb`, `FindBot`), `Graphs/BPC_Stagehand/EndLine.txt`, `prompts.json`, `free_mode.json`, `emotes.json`, `pacing.json`, `Relay/src/index.js`, `Relay/relay.config.json`, `Tools/check_prompts.py`, `Docs/switches.example.json`, the findings in `T10.md`, `T11.md`, `T14.md`, `T30.md`, `T38.md`, `T52.md`, `T60.md`, `T61.md`, `T77-build.md` and `T78-build.md`, and the design doc (Bot Prompts rev 91, Rules rev 52; read, not changed).

## Re-check before you write anything

T87's dependencies are all pushed. These are the points that can still move before T87 starts:

1. **Nobody changed the graphs this sheet edits or leans on since `b515048`:**
   `git log --oneline b515048..HEAD -- Graphs/BP_Show/EndShow.txt Graphs/BP_Show/HandleReply.txt Graphs/BP_Show/CueEnd.txt Graphs/BP_Show/RunCue.txt Graphs/BP_Show/LineInfo.txt Graphs/BP_Show/ShowLine.txt Graphs/BP_Show/StageLine.txt Graphs/BP_Show/TakeEmo.txt Graphs/BP_Show/EmoWord.txt Graphs/BP_Show/ActorState.txt Graphs/BP_Robot/EventGraph.txt Graphs/BP_Robot/ResetLook.txt Graphs/BP_Robot/SetCut.txt Graphs/BP_Robot/Cheer.txt Graphs/BP_Robot/Emote.txt Graphs/BPC_LinePlayer/PlayCur.txt Graphs/BPC_LinePlayer/Pump.txt Graphs/BPC_LLMClient/AskProvider.txt Graphs/BPC_LLMClient/FreeFindPhase.txt`.
   If one changed, put this sheet's lines into the new version by their anchors.
2. **T78 (re-check).** It was being built in the repo folder while this sheet was written, and it landed as `b515048` (checked) just before the sheet was finished. At `b515048` it changed `SendHumanTurn`, `SendHumanTalk`, `SendHumanReact`, `SendHumanVote`, `HumanFeels` and the new `ApplyFace` and `TakeFace` in `BP_Show`, and nine `WBP_Stage` graphs. None of them is a graph T87 edits. Two things this sheet takes from that area, to check again:
   - **`TakeEmo` → `HumanFeels`.** Part 3d calls `TakeEmo` for an AI seat. Only my seat reaches `HumanFeels` (and T78's `ApplyFace`), so an AI's emotion is the reply's own. Check that `TakeEmo.txt` still says so.
   - **`WBP_Stage` reads no `Phase`.** At `b515048` no `WBP_Stage` graph reads `BP_Show.Phase` (`grep -rn "GetPhase" Graphs/WBP_Stage`), so part 3g's new phase `"reveal"` changes nothing there. If a T78 follow-up or T34 made the input row follow `Phase`, check what it shows in `"reveal"` (it should look as it does in `"closing"`).
3. **`free_mode.json`'s phase order.** The `closing` phase still matches `"The show is over"`, and `input` is still first. Part 6 puts `reaction_win` right after `input`.
4. **`emotes.json`** still has `surprised`, `embarrassed`, `angry`, `sad` and `happy` (part 6's list).
5. **The design doc:** read Bot Prompts and Rules again. Part 9 quotes them at Bot Prompts rev 91 and Rules rev 52.
6. **T34** is after T87 in the plan. T34-build's 2.1 may hide the robots' 3D labels. If T34 landed first, part 2c's `HUMAN` stamp on my robot's label won't show: tell my person, and put the stamp where T34 moved the cut stamp.

## In short

| T87 step | Where in this sheet |
|---|---|
| 1. Read first | Done here; part 0's survey lists what only the editor can answer |
| 2. The new ask | Part 5 (`prompts.json`), part 9a (the Bot Prompts edit, my person's answer), part 3b (`AskWinReact`, sent with the closing ask) |
| 3. Free mode | Part 6 (`free_mode.json`); part 7 (no relay or `FreeReply` change) |
| 4. The cut robots get back up | Part 2 (`BP_Robot.Rise`, `EventGraph`, `ResetLook`) |
| 5. My robot | Part 2c (`Unmask`: the `HUMAN` stamp and one `Cheer`); each line's `does` turns the robot toward mine (part 4c) |
| 6. Play the reactions one at a time | Part 4 (`BPC_WinReveal`), part 3 (`CueEnd`, `RunCue`, `WinLine`, `LineInfo`) |
| 7. Check lines | Part 4 (`NHOS: WIN REACT`, `WIN SKIP`, `WIN REACTIONS`), part 2 (`RISE`, `UNMASK`) |
| 8. The checker | Part 8 |
| 9. Check | Part 10 |

- **The plan in one line:** on a win, `EndShow` sends each AI seat `reaction_win` right after its closing ask. `HandleReply` hands those replies to a new component, `BPC_WinReveal`, which keeps them. When the last closing reply is in, `CueEnd` asks the component to hold the end cue until every reaction is in. Then the component queues the reveal cue (the cut robots rise, my robot cheers), the header `THE REVEAL`, a banner and one line per AI, in order, through `BP_Show.ShowLine`. Last, it lets `CueEnd` queue the end cue. The line queue plays them in that order, so the reactions play before `ShowEndScreen` prints `SHOW END`, and before the stagehand's `"end"` line (T61).
- **New logic goes in its own component.** It grows to eight functions and its own state, so it doesn't go in `BP_Show` (decision 1). **`BP_Show` keeps only:** two lines in `EndShow`, one new ask function (`AskWinReact`, which must touch `BP_Show`'s pending lists), one branch in `HandleReply`, a hold in `CueEnd`, one cue branch in `RunCue`, one word in `LineInfo`, and a three-line `WinLine` that hands each line to `ShowLine`.
- **A cut robot that rises is no longer cut** (`IsCut` false). So its bubble (`Say`, `Typing`), its face (`Emote`), its look and its lit spot all work with no change to `BPC_LinePlayer`, `Emote` or `Say`. It keeps its gray body (decision 2).
- **Locks:** `Content/NHOS/Core/BP_Show.uasset` and `Content/NHOS/Stage/BP_Robot.uasset`. The new `Content/NHOS/Core/BPC_WinReveal.uasset` needs no lock until it is pushed. `BPC_LinePlayer` and `BPC_LLMClient` don't change, so T87 needs no lock on them.
- **Needs the relay deploy:** `Content/NHOS/Data/free_mode.json` (the relay bundles it). `Relay/src/index.js` doesn't change (part 7). Every push to `noHumansOnSet` redeploys the relay, so the push that carries `free_mode.json` needs my person's OK, typed in the T87 session.
- **Costs money:** only the paid `--ask reaction_win --repeat 3` run: 4 personas × 3 = 12 short calls, a few cents.
- **It can be split** between two sessions (part 11).

## Questions for my person

One question, answered.

> **My person answered** (2026-11-15, to the prep session): **a new "Ask after a win" section** in the Bot Prompts tab, as recommended. Part 9a applies. Don't ask again; copy this answer under "Findings" in `T87.md`. The doc edits themselves still need my person's OK on the text, typed in the T87 session (part 0).

1. **Where the ask goes in the doc.** T87 step 2 says to put `reaction_win` in the Bot Prompts tab first. At rev 91 that tab holds no ask at all: only the opening prompt, the base prompt, the input LLM prompt and the personas. Every other ask lives only in `prompts.json`. The options were: **(Recommended) a new "Ask after a win" section** (a heading, one paragraph and a code block, after "Input LLM prompt"); a new "Asks" section with all nine asks; or no Bot Prompts edit.

## Decisions made for my person

My person asked prep sessions to take their own recommendation on calls that are theirs, and list them here. Each is open to change. The T87 session shows this list to my person when it closes the task.

1. **A new component, `BPC_WinReveal`,** on `BP_Show` (as `Audio`, `Analytics` and `LinePlayer` are). It keeps the replies, decides the order, raises the robots and queues the lines. `BP_Show` keeps only what must touch its own state (the summary above).
2. **`Rise()` makes the robot not cut** (`IsCut` false) and keeps its gray body and its dark floor ring. The other way, an `EvenCut` input on `Emote` (T77-build decision 17), `Cheer` and the stage director's `IsDown`, would change four graphs and `BPC_LinePlayer`'s two calls. With `IsCut` false, `Say`, `Typing`, `Emote`, `Cheer`, `StartAct` and `BP_StageDirector.PlayLine` all treat the robot as standing. Its eyes, mouth and brows get their colors back, and its name comes back in white. If the screenshots show gray hides the face, part 2d's fallback applies.
3. **The rise eases over about a second,** SetCut's fall in reverse: `EventTick`'s standing branch eases `TipRoll` and a new `Slump` to 0 with `FInterpTo` at speed 3, the speed of the fall. A robot that was never cut has both at 0, so nothing changes for it.
4. **The reaction asks' tags look like every other ask's** (`<seat id>-<n>`), because `BPC_LLMClient.AskProvider` finds the provider from the part before the last `-`. A prefix such as `win-` would find no provider. So the component keeps its own list of tags (`AddTag`, `Owns`).
5. **The end waits in `CueEnd`,** which has a file, not in `StoreClosing`, which has none (T10). `CueEnd`'s only caller is `StoreClosing` (T30: "Replace the `ShowEndScreen` call with `CueEnd`"; part 0's survey checks it). `HoldEnd` lets a loss straight through.
6. **`EndShow` calls `Begin` on every show,** with `Want` 0 on a loss, so a win whose replies never all came back can't hold a later show's end.
7. **The order:** the cut AIs in the order they were cut (`CutScene`, one cut a scene), then any cut AI left over (in seat order, in case `CutScene` doesn't hold it), then the AIs still on stage, in seat order. A tie cuts nobody, so with `force_tie` every AI is on stage.
8. **The header is `THE REVEAL`.** `BPC_Analytics.PhaseKey` gives it no key, so no analytics event goes out (T68's events stay as they are), and `BPC_ShowAudio.PhaseKey` gives it no track, so the end music goes on. A banner follows: "The cast learns the truth." Its 2-second hold (`pacing.json` `cue_hold.banner`) covers the robots' rise, so the first line doesn't start under it. `pacing.json` doesn't change.
9. **The reveal is its own phase, `"reveal"`,** set by `WinLine` as the lines are queued. `LineInfo` then shows "<name> is typing..." before each line, as in the reactions after a cut. `HandleReply`, `TimerFor` and `ShowLine` see no change in it (they test other phases), and `ShowEndScreen` sets `"end"` when the end cue runs, so Play Again works as before.
10. **Each line's log-style entry says `does` "looks at <my Player name>",** so the stage director turns the speaker toward my robot (T19's look, through `StageLine` → `PlayLine` → `DoVerb`). The chat and the bubble show no action, because `WinLine` passes `DoesNothing` to `ShowLine` as the shown action. The entry also carries `feels`, so `StageLine` makes the robot `Emote` (T77). The entry never enters the shared log.
11. **A failed, empty or passed reply plays nothing** and prints `NHOS: WIN SKIP <id> cut=<0|1>`. The checker wants one `WIN REACT` or `WIN SKIP` per AI seat, and warns on each skip.
12. **My robot shows `HUMAN` on its own label,** in the cut stamp's red, as `SetCut` writes a stamp, and cheers once, both at the reveal cue (`Unmask`). The big stamp under the header (`WBP_Stage.SetStamp`) is not used: `WBP_Stage` doesn't change.
13. **The ask starts "The reveal.",** not "The show is over", so it doesn't match the `closing` phase's `ask_contains`. The phase still goes right after `input`, so the order is safe either way.
14. **`EndShow`'s banners stay as they are,** "The cast gives one last verdict..." included. The judgment (part 10f) says whether that line reads oddly before `THE REVEAL`.
15. **Eight free-mode lines,** one or two for each kind the task names (part 6).

## 0. Before you start

1. Pull (or merge `origin/noHumansOnSet`), read `Agents/`, `git lfs locks`. No lock on `BP_Show.uasset` or `BP_Robot.uasset`. Claim T87 (`git lfs lock Docs/claims/T87`) and lock both assets. If the work is split (part 11), each session locks only its own asset.
2. **Work through "Re-check before you write anything"** above.
3. `python Tools/check_prompts.py --offline` passes before you start.
4. **Survey, read only** (each a separate `call_tool`; save each read to `Saved/T87/<graph>.read.txt`; never write a read-back to the editor):
   1. **`CueEnd`'s callers:** `find_nodes` in `BP_Show` for `CallFunction` nodes titled `CueEnd`. Expect one, in `StoreClosing`. Another caller goes through the same `HoldEnd` and needs nothing, but write it under "Findings".
   2. **`AskClosing`** (no file): its tag shape (`<seat id>-<AskCount>`, expected) and whether it sets `AskOpts` for the seat. `AskWinReact` runs right after it and reads the same `AskOpts` through `ActorState`; that is fine (decision in part 3b).
   3. **Variable types in `BP_Show`:** `SeatCut` (Boolean array by seat), `CutScene` (Integer array by seat; T10 sets `CutScene[seat]` at the cut, T52: a tie leaves it as it is), `SeatCount`, `HumanSeat`, `SceneNum`, `Robots`, `LinePlayer`, `SeatName`, `SeatId`, `LineEntry` (the JSON object type), `PendingTags`, `PendingSeats`, `AskCount`, `SeatSystem`, `ClosingLeft`. None of them may be private, because the component reads them with `Class|BPShow|Get<name>` (as `BPC_LinePlayer.BubbleBot` reads `Robots` and `BP_Robot.WatchShow` reads `SceneNum`).
   4. **Free names:** no `WinTag`, `WinReveal`, `AskWinReact` or `WinLine` in `BP_Show`; no `Rise`, `Unmask` or `Slump` in `BP_Robot` (none is in `Graphs/` at `b515048`).
   5. **Node names the pushed sources haven't used yet:** `Class|BPShow|GetSeatCut`, `GetCutScene`, `GetSeatCount`, `GetHumanSeat`, `GetLinePlayer`, `GetSeatName`, `GetSeatId`, `Class|BPShow|CueEnd`, `CueHeader`, `CueBanner`, `WinLine`, `Class|BPRobot|Rise`, `Unmask`, and the `Class|BPCWinReveal|...` calls once the component compiles. Every other form below is in a pushed source.
5. **Ask my person, one question per call, with the multiple-choice tool** (CLAUDE.md, "Asking for input"):
   1. The doc's home for the ask is answered (a new "Ask after a win" section); don't ask it again.
   2. **The doc edits:** show part 9's text (9a and 9b). "Make these edits (Recommended)" or "Change the wording" (then use theirs word for word in part 5 and in `DOC_REACTION_WIN`).
   3. **The deploy push:** "Push free_mode.json with T87 (Recommended)": the push redeploys the relay, whose free mode then answers `reaction_win` from its own phase; no paid call. Or "Not now" (part 12's two-commit path).
   4. **The paid run:** "Run reaction_win 3 times on all four providers, a few cents (Recommended)" or "Not now" (then the task waits with a `Waiting:` line after its first commit).
6. Status file `Agents/status/task-T87.md` in the repo folder's `Agents/status/`, with `- Editor: driving` while T87 uses the editor.

## 1. Which graphs change

| Blueprint | Graph | File | Change |
|---|---|---|---|
| `BP_Robot` | `Rise`, `Unmask` | new | A cut robot gets back up; my robot's stamp and cheer (2b, 2c) |
| | `EventGraph` | yes | The standing branch eases `TipRoll` and `Slump` to 0 (2a) |
| | `ResetLook` | yes | One line: `Slump` 0 (2a) |
| `BPC_WinReveal` (new) | `FindShow`, `Begin`, `AddTag`, `Owns`, `Store`, `HoldEnd`, `TryPlay`, `MakeOrder`, `Play`, `RiseAll` | new | The whole reveal (part 4) |
| `BP_Show` | `AskWinReact`, `WinLine` | new | The ask; one line to the screen (3b, 3f) |
| | `EndShow` | yes | `Begin` and the ask, in the closing batch (3a) |
| | `HandleReply` | yes | Reaction replies go to the component (3c) |
| | `CueEnd` | yes | The hold (3d) |
| | `RunCue` | yes | The `"reveal"` cue (3e) |
| | `LineInfo` | yes | Typing dots in `"reveal"` (3g) |

`BPC_LinePlayer` (`Push`, `Pump`, `PlayCur`), `BPC_LLMClient` (`FreeReply`, `FreeFindPhase`), `StoreClosing`, `ShowEndScreen`, `EndReveal`, `RevealRivals`, `ShowLine`, `StageLine`, `ActorLine`, `PlayReact`, `BP_Robot.Emote`, `Say`, `Typing`, `Cheer`, `SetCut`, `WBP_Stage` and the relay don't change.

**Order** (T18, T54: a call node goes stale when its function gets a new parameter; T63: a call node made before a compile has the skeleton's old pins):

1. **`BP_Robot`:** the variable `Slump`; `Rise` and `Unmask` with their params, empty; compile; their bodies; `EventGraph`; `ResetLook`; compile, save.
2. **`BP_Show`, part one:** `WinLine` (it calls only `ShowLine`) and `LineInfo`; compile, save. Nothing calls `WinLine` yet.
3. **`BPC_WinReveal`:** create it (`/Game/NHOS/Core/BPC_WinReveal`, an Actor Component Blueprint); its variables; its ten functions with their params, empty; compile; their bodies (it calls `BP_Robot.Rise`/`Unmask` and `BP_Show.WinLine`/`CueEnd`/`CueHeader`/`CueBanner`, all compiled by now); compile, save.
4. **`BP_Show`, part two:** add `BPC_WinReveal` as a public component named `WinReveal` (as T61 planned `Stagehand` and T20 added `Audio`); the variable `WinTag`; `AskWinReact` with its param, empty; compile; its body; then `EndShow`, `HandleReply`, `CueEnd`, `RunCue`; compile, save.

Compile with warnings as errors and save after each group, and read the editor log after each compile (T51: `compile_blueprint` returns null on success). Before any compile, trace each function's live nodes from its entry and delete stale call nodes `write_graph_dsl` left behind (T63's first MCP rule). Close every game window before you save (T53).

## 2. `BP_Robot`

### 2a. `Slump`, `EventGraph.txt` and `ResetLook.txt`

New variable: `Slump` (Float, 0). 1 when a cut robot starts to rise, eased to 0.

**`EventGraph.txt`,** in `EventTick`'s `(else ...)` branch (the robot isn't cut):

1. As the branch's first two lines, before `      (bind _talk (< _c (Variables|Default|GetTalkUntil)))`:
   ```lisp
         ; T87: a robot that rose for the reveal (Rise) eases from its fallen pose back to upright, SetCut's fall in
         ; reverse, at the fall's speed. Slump and TipRoll are 0 for a robot that was never cut, so nothing changes for it.
         (set Slump (Math|Interpolation|FInterpTo (V Slump) 0.0 DeltaSeconds 3.0))
         (Variables|Default|SetTipRoll (Math|Interpolation|FInterpTo (Variables|Default|GetTipRoll) 0.0 DeltaSeconds 3.0))
   ```
2. The Rig's location line, now
   `      (Transformation|SetRelativeLocation :self (Variables|Default|GetRig) :NewLocation (Math|Vector|MakeVector :X (V GX) :Y 0.0 :Z (+ _z (V GZ))))`,
   becomes
   `      (Transformation|SetRelativeLocation :self (Variables|Default|GetRig) :NewLocation (Math|Vector|MakeVector :X (V GX) :Y 0.0 :Z (+ (* (- 1.0 (V Slump)) (+ _z (V GZ))) (* (V Slump) -10.0))))`
   (the cut branch ends the slump at Z = -10; this blends from there to the standing height).
3. The Rig's rotation line, now
   `      (Transformation|SetRelativeRotation :self (Variables|Default|GetRig) :NewRotation (Math|Rotator|MakeRotator :Roll (V GRoll) :Pitch (V GPitch) :Yaw (+ _yaw (V GYaw))))`,
   becomes
   `      (Transformation|SetRelativeRotation :self (Variables|Default|GetRig) :NewRotation (Math|Rotator|MakeRotator :Roll (+ (V GRoll) (Variables|Default|GetTipRoll)) :Pitch (+ (V GPitch) (* (V Slump) -14.0)) :Yaw (+ _yaw (V GYaw))))`
   (the cut branch's pitch is -14 at the end of the slump).

The arms, the fold and the mouth lines don't change: the arms come up from the cut branch's 0 to the rest pose in one frame, which is small.

**`ResetLook.txt`:** after `  (Variables|Default|SetTipGoal 0.0)`, add `  (set Slump 0.0)`. Header line: `; T87: a new show starts with no rise in progress (Slump).` Restart already sets `TipRoll` 0, the seat colors, the ring, the face and the name, so a risen robot comes back whole.

### 2b. `Rise.txt` (new)

```lisp
; T87: a cut robot gets back up for the reveal on a win (BPC_WinReveal.RiseAll, at the "reveal" cue). It is no longer
; cut, so its bubble (Say, Typing), its face (Emote, T75), its cheer and its look (the stage director) work again. Its tip
; eases back to upright, SetCut's fall in reverse (EventGraph eases TipRoll and Slump to 0). It keeps its gray body and
; its dark floor ring, so the player can still tell who was cut; its eyes, mouth, brows and name come back.
(fn Rise ()
  (if (not (V IsCut))
    (return))
  (Variables|Default|SetIsCut false)
  (Variables|Default|SetTipGoal 0.0)
  (set Slump 1.0)
  (set LookUntil 0.0)
  (set AroundUntil 0.0)
  (bind _eye (Math|Conversions|ToVector(LinearColor) (Variables|Default|GetEyeColor)))
  (bind _ink (Math|Vector|MakeVector :X 0.015 :Y 0.015 :Z 0.015))
  (Rendering|Material|SetVectorParameterValueonMaterials :self (Variables|Default|GetEyeL) :ParameterName "Color" :ParameterValue _eye)
  (Rendering|Material|SetVectorParameterValueonMaterials :self (Variables|Default|GetEyeR) :ParameterName "Color" :ParameterValue _eye)
  (Rendering|Material|SetVectorParameterValueonMaterials :self (Variables|Default|GetMouth) :ParameterName "Color" :ParameterValue (select (Variables|Default|GetLedMouth) _eye _ink))
  (Rendering|Material|SetVectorParameterValueonMaterials :self (Variables|Default|GetBrowWL) :ParameterName "Color" :ParameterValue _eye)
  (Rendering|Material|SetVectorParameterValueonMaterials :self (Variables|Default|GetBrowWR) :ParameterName "Color" :ParameterValue _eye)
  (Rendering|Material|SetVectorParameterValueonMaterials :self (Variables|Default|GetBrowAL) :ParameterName "Color" :ParameterValue _eye)
  (Rendering|Material|SetVectorParameterValueonMaterials :self (Variables|Default|GetBrowAR) :ParameterName "Color" :ParameterValue _eye)
  (Rendering|Components|TextRender|SetText :self (Variables|Default|GetLabel) :Value (Utilities|Text|ToText(String) (Variables|Default|GetDisplayName)))
  (Rendering|Components|TextRender|SetTextRenderColor :self (Variables|Default|GetLabel) :Value (Math|Conversions|ToColor(LinearColor) :InLinearColor (Utilities|Struct|MakeLinearColor :R 1.0 :G 1.0 :B 1.0 :A 1.0) :InUseSRGB true))
  (CallFunction|SetLit :On false)
  (set PassedOn false)
  (print (cat "NHOS: RISE " (str (V Seat)) " persona=" (V PersonaId))))
```

- The eye, mouth and brow lines are `ResetLook`'s (T80), so each bot's own eye color and ink mouth come back. `SetCut` darkened exactly these seven parts; the emotion parts (`EmBrowL`, `MouthCL`, ...) were never darkened.
- `SetLit(false)` puts the LED glow back at its resting value; `LightSeat` lights the robot when its line plays.
- `SetCut` already ended any emotion (`EmoteStop`) and dropped the props (`DropAll`). The headpiece stays on, as it stayed while the robot lay there (T47).

### 2c. `Unmask.txt` (new)

```lisp
; T87: my robot at the reveal on a win: its label shows Stamp ("HUMAN") in the cut stamp's red, as SetCut writes a
; stamp, and it cheers once (T19's Cheer), so the cast's reactions point at someone. It isn't cut and keeps its colors.
(fn Unmask (Stamp)
  (Rendering|Components|TextRender|SetText :self (Variables|Default|GetLabel) :Value (Utilities|Text|ToText(String) Stamp))
  (Rendering|Components|TextRender|SetTextRenderColor :self (Variables|Default|GetLabel) :Value (Math|Conversions|ToColor(LinearColor) :InLinearColor (Utilities|Struct|MakeLinearColor :R 1.0 :G 0.12 :B 0.08 :A 1.0) :InUseSRGB true))
  (CallFunction|Cheer)
  (print (cat "NHOS: UNMASK " (str (V Seat)) " " Stamp)))
```

`Cheer` lasts 2.8 s (jumps with the arms up). Restart's `ResetLook` puts the name back in white.

### 2d. Fallback, only if the screenshots show gray hides the face

If a risen robot's face doesn't read on the gray body (part 10e), give it back its colors and mark the cut on its label instead, as T87 step 4 says. In `Rise`, after the brow lines, add `ResetLook`'s seat-color loop (T79), with the ring left off:

```lisp
  (bind _cv (Math|Conversions|ToVector(LinearColor) (Variables|Default|GetBaseColor)))
  (for _c (Actor|GetComponentsByClass :ComponentClass "/Script/Engine.StaticMeshComponent")
    (if (Components|ComponentHasTag :self _c :Tag "seat")
      (Rendering|Material|SetVectorParameterValueonMaterials :self _c :ParameterName "Color" :ParameterValue _cv)))
```

and make the label "(cut)" over the name, in `SetPassed`'s form and color:

```lisp
  (Rendering|Components|TextRender|SetText :self (Variables|Default|GetLabel) :Value (Utilities|Text|ToText(String) (Utilities|String|Append "(cut)<br>" (Variables|Default|GetDisplayName))))
  (Rendering|Components|TextRender|SetTextRenderColor :self (Variables|Default|GetLabel) :Value (Math|Conversions|ToColor(LinearColor) :InLinearColor (Class|UIStyle|UIColor :Role "Quiet") :InUseSRGB true))
```

Change the header to match, and write which look was kept, with the screenshots, under "Findings".

## 3. `BP_Show`

New variable: `WinTag` (String). New component: `WinReveal` (`BPC_WinReveal`, public).

### 3a. `EndShow.txt`

1. Header, after T54's line:
   ```lisp
   ; T87: on a win, every AI seat also gets the reaction_win ask, in the same batch as its closing ask (AskWinReact), so a
   ; win waits no longer. WinReveal.Begin comes before any ask, so a reply that comes back at once is counted; on a loss
   ; it gets Want 0, which arms nothing.
   ```
2. Right before the last loop, `  (for _index_1 (range (V SeatCount))`, add:
   ```lisp
     (Class|BPCWinReveal|Begin :self (V WinReveal) :Want (select Win (V ClosingLeft) 0))
   ```
   `ClosingLeft` is the number of AI seats by then (the loop above it counts them).
3. That last loop becomes:
   ```lisp
     (for _index_1 (range (V SeatCount))
       (if (!= _index_1 (V HumanSeat))
         (CallFunction|AskClosing :Seat _index_1)
         (if Win
           (CallFunction|AskWinReact :Seat _index_1)))))
   ```
   A non-returning `if` nested at the end of a then branch, with nothing after it: it joins (T30's rule is about else paths).

### 3b. `AskWinReact.txt` (new)

```lisp
; T87: the reaction_win ask for one AI seat, cut or still on stage. EndShow sends it on a win, right after that seat's
; closing ask. The tag has the usual <seat id>-<n> shape, because BPC_LLMClient.AskProvider finds the provider from the
; part before the last "-", so WinReveal keeps its own list of these tags (AddTag) and HandleReply sends their replies to
; it, not to StoreClosing. ActorState reads the options AskClosing just set; the ask doesn't use them.
(fn AskWinReact (Seat)
  (set AskCount (+ (V AskCount) 1))
  (set WinTag (cat (get (V SeatId) Seat) "-" (str (V AskCount))))
  (add (V PendingTags) (V WinTag))
  (add (V PendingSeats) Seat)
  (Class|BPCWinReveal|AddTag :self (V WinReveal) :Tag (V WinTag))
  (bind _st (CallFunction|ActorState :Seat Seat :AskKey "reaction_win" :Now "show over, the reveal"))
  (Class|BPCLLMClient|Ask :self (V LLMClient) :Tag (V WinTag) :Role "actor" :System (get (V SeatSystem) Seat) :User _st))
```

`NextLastWord`'s ask is the model. `ActorState` puts `asks.reaction_win` in `ask` and prints the usual `NHOS: STATE` line. In Test for Free, `BPC_LLMClient.Ask` queues the reply for `FlushLocal` 0.3 s later, so every ask is out before the first reply comes back; through the relay, `Begin` has armed the count before the first ask anyway.

### 3c. `HandleReply.txt`

Right after T63's scrub:

```lisp
  (if (== (V RSeat) (V HumanSeat))
    (bind _sc (CallFunction|ScrubLabels :Text Speech))
    (set RSpeech _sc))
```

and before `  (if (streq (V Phase) "free talk")`, add:

```lisp
  (bind _win (Class|BPCWinReveal|Owns :self (V WinReveal) :Tag Tag))
  (if _win
    (bind _we (CallFunction|TakeEmo :Seat (V RSeat)))
    (bind _ww (CallFunction|EmoWord :Id _we))
    (bind _wl (CallFunction|CapWords :Text (V RSpeech)))
    (Class|BPCWinReveal|Store :self (V WinReveal) :Seat (V RSeat) :Ok (and Ok (not Pass)) :Line _wl :Emotion _we :Word _ww)
    (return))
```

Header line: `; T87: a reaction_win reply (WinReveal.Owns its tag) goes to WinReveal with its line (CapWords, 15 words) and its emotion, before the phase branches, since its phase is still "closing".`

- T77's `KeepEmo` has just kept this reply's emotion for the seat, so `TakeEmo` returns it, checked against `emotes.json` (an unknown id is `neutral`), and clears it. For an AI seat `TakeEmo` never reaches `HumanFeels` (re-check 2).
- `_we`, `_ww` and `_wl` are binds of impure calls, read once at the call (T65's trap is about pure nodes).
- A top-level returning `if` before the phase branches, as T63's `SpellTag` branch is.

### 3d. `CueEnd.txt` (new content)

```lisp
; T30: the end screen's cue, behind every line in front of it. StoreClosing calls it when the last closing reply is in.
; T87: on a win, WinReveal holds it (HoldEnd) until every reaction_win reply is in and the reveal is queued, then calls
; CueEnd again itself, so the end cue goes in behind the reactions. On a loss HoldEnd lets it straight through.
(fn CueEnd ()
  (bind _hold (Class|BPCWinReveal|HoldEnd :self (V WinReveal)))
  (if _hold
    (return))
  (Class|BPCLinePlayer|Cue :self (Variables|Default|GetLinePlayer) :Kind "end" :Text "" :Num 0))
```

The second call comes from inside the first (`HoldEnd` → `TryPlay` → `CueEnd`), after `TryPlay` has disarmed the component, so it queues the end cue and the first call returns without a second one.

### 3e. `RunCue.txt`

Right before the `"end"` branch (`  (if (streq Kind "end")`), add:

```lisp
  ; T87: the reveal on a win: the cut robots get back up and my robot cheers under its HUMAN stamp (WinReveal.RiseAll).
  (if (streq Kind "reveal")
    (Class|BPCWinReveal|RiseAll :self (V WinReveal))
    (return))
```

`BPC_LinePlayer.Pump` runs any cue kind through `RunCue`; `CueHoldFor` holds an empty-text cue 0 s, and `"reveal"` isn't one of the kinds that hush the bubble or reset `QPhase`, so `Pump` needs no change. Header line: `; T87: the "reveal" cue (WinReveal.RiseAll).`

### 3f. `WinLine.txt` (new)

```lisp
; T87: one reaction to the reveal reaches the screen (WinReveal.Play calls it for each line), through ShowLine like every
; line. It never enters the shared log: no ask reads the log after the show. Phase "reveal" makes LineInfo show the
; typing dots first, as in the reactions after a cut; ShowEndScreen sets "end" when the end cue runs. Entry carries
; "feels" (StageLine's Emote) and does "looks at <my Player name>" (the stage director turns the robot to mine). The
; chat and the bubble show no action: DoesNothing is shown as "" outside a scene (ShowLine).
(fn WinLine (Seat Entry Says)
  (set Phase "reveal")
  (Variables|Default|SetLineEntry Entry)
  (CallFunction|ShowLine :Seat Seat :Does (Variables|Default|GetDoesNothing) :Says Says))
```

`ShowLine` hands `LineEntry` to the queue as the line's entry (T30), and `PlayCur` calls `StageLine` with it when the line plays: `StageLine` reads `feels` (an empty word is neutral, `FeelsId`) and `Emote`s the robot, then gives the stage director the `does`.

### 3g. `LineInfo.txt`

The `_chat` line becomes:

```lisp
  (bind _chat (or (or (Utilities|String|EqualExactly(String) (Variables|Default|GetPhase) "free talk") (Utilities|String|EqualExactly(String) (Variables|Default|GetPhase) "reactions")) (Utilities|String|EqualExactly(String) (Variables|Default|GetPhase) "reveal")))
```

Header line: `; T87: and in the reveal on a win ("reveal", WinLine).` `Push` calls `LineInfo` as the line is queued, right after `WinLine` set the phase.

## 4. `BPC_WinReveal` (new, `Content/NHOS/Core/BPC_WinReveal.uasset`)

### 4a. Variables and params

| Variable | Type | What for |
|---|---|---|
| `Show` | `BP_Show` object | Its owner (`FindShow`) |
| `Armed`, `ClosingIn` | Boolean | A win's reveal is waiting; the closing replies are all in |
| `WantN`, `Got` | Integer | Reaction replies wanted, and in |
| `Tags` | String array | This show's reaction tags |
| `WLine`, `WEmo`, `WWord` | String array, by seat | Each reply's line, emotion id and its `feels` word |
| `WOk` | Boolean array, by seat | The reply has a line to play |
| `Order` | Integer array | The seats, in the order they speak |
| `CutArr` | Boolean array | `BP_Show.SeatCut`, copied |
| `CutAt` | Integer array | `BP_Show.CutScene`, copied |
| `Seats`, `Hum`, `LastScene`, `Cur`, `Played`, `Risen` | Integer | Seat count, my seat, the last scene, the seat being played, lines played, robots risen |
| `Names`, `Ids` | String array | `SeatName` (Player names), `SeatId` (persona ids) |
| `MeName`, `CutTxt` | String | My Player name; "1" or "0" |
| `WEntry` | the type of `BP_Show.LineEntry` (a JSON object) | The entry being built |
| `LP` | `BPC_LinePlayer` object | For the `"reveal"` cue |
| `Bots` | `BP_Robot` object array | `BP_Show.Robots` |
| `Bot` | `BP_Robot` object | The robot being raised |

| Function | Inputs | Returns |
|---|---|---|
| `FindShow` | none | none |
| `Begin` | `Want` (Integer) | none |
| `AddTag` | `Tag` (String) | none |
| `Owns` | `Tag` (String) | Boolean |
| `Store` | `Seat` (Integer), `Ok` (Boolean), `Line`, `Emotion`, `Word` (String) | none |
| `HoldEnd` | none | Boolean |
| `TryPlay`, `MakeOrder`, `Play`, `RiseAll` | none | none |

### 4b. Taking the replies

`Graphs/BPC_WinReveal/FindShow.txt`:

```lisp
; T87: the show this component belongs to (BPC_LinePlayer.FindShow's way).
(fn FindShow ()
  (Utilities|IsValid (V Show)
    (:"Is Valid")
    (:"Is Not Valid"
      (bind _s (Actor|GetActorOfClass :ActorClass "/Game/NHOS/Core/BP_Show.BP_Show_C"))
      (set Show _s))))
```

`Graphs/BPC_WinReveal/Begin.txt`:

```lisp
; T87: EndShow calls this on every show, before any closing ask: Want is the number of AI seats on a win, 0 on a loss.
; A win arms the reveal; a loss (or a show whose win never finished) is cleared, so HoldEnd lets its end through.
(fn Begin (Want)
  (CallFunction|FindShow)
  (set Armed (> Want 0))
  (set ClosingIn false)
  (set WantN Want)
  (set Got 0)
  (clear (V Tags))
  (clear (V WLine))
  (clear (V WEmo))
  (clear (V WWord))
  (clear (V WOk))
  (Utilities|Array|Resize (V WLine) 8)
  (Utilities|Array|Resize (V WEmo) 8)
  (Utilities|Array|Resize (V WWord) 8)
  (Utilities|Array|Resize (V WOk) 8)
  (if (V Armed)
    (print (cat "NHOS: WIN ASK n=" (str Want)))))
```

`Graphs/BPC_WinReveal/AddTag.txt`:

```lisp
; T87: AskWinReact's tag for one AI seat.
(fn AddTag (Tag)
  (add (V Tags) Tag))
```

`Graphs/BPC_WinReveal/Owns.txt`:

```lisp
; T87: whether a reply's tag is one of this win's reaction asks (BP_Show.HandleReply asks before its phase branches).
(fn Owns (Tag)
  (return (and (V Armed) (>= (Utilities|Array|FindItem (V Tags) Tag) 0))))
```

`Graphs/BPC_WinReveal/Store.txt`:

```lisp
; T87: one reaction_win reply, from HandleReply: its line (15 words at most), its emotion id and that emotion's "feels"
; word. A failed, passed or empty reply is kept as nothing to play. Each reply counts; the last one may start the reveal.
(fn Store (Seat Ok Line Emotion Word)
  (if (and (>= Seat 0) (< Seat (len (V WLine))))
    (Utilities|Array|SetArrayElem (V WOk) Seat (and Ok (not (Utilities|String|IsEmpty (Utilities|String|Trim Line)))))
    (Utilities|Array|SetArrayElem (V WLine) Seat Line)
    (Utilities|Array|SetArrayElem (V WEmo) Seat Emotion)
    (Utilities|Array|SetArrayElem (V WWord) Seat Word))
  (set Got (+ (V Got) 1))
  (CallFunction|TryPlay))
```

`Graphs/BPC_WinReveal/HoldEnd.txt`:

```lisp
; T87: BP_Show.CueEnd asks this when the last closing reply is in. On a win it holds the end cue (true) and starts the
; reveal as soon as every reaction is in (TryPlay, which calls CueEnd again once disarmed). Otherwise false: the end
; cue goes in at once.
(fn HoldEnd ()
  (if (not (V Armed))
    (return false))
  (set ClosingIn true)
  (CallFunction|TryPlay)
  (return true))
```

`Graphs/BPC_WinReveal/TryPlay.txt`:

```lisp
; T87: once the closing replies and every reaction are in, queue the reveal (Play), then the end cue behind it
; (BP_Show.CueEnd, which HoldEnd now lets through, since Armed is off).
(fn TryPlay ()
  (if (not (and (V Armed) (and (V ClosingIn) (>= (V Got) (V WantN)))))
    (return))
  (set Armed false)
  (CallFunction|Play)
  (Class|BPShow|CueEnd :self (V Show)))
```

### 4c. The order and the lines

`Graphs/BPC_WinReveal/MakeOrder.txt`:

```lisp
; T87: who speaks, in order: the cut AIs in the order they were cut (CutScene: one cut a scene), then any cut AI left
; over, then the AIs still on stage, in seat order, so the ones fooled to the end speak last. My seat never speaks.
; The copies are resized to the seat count, so no index is out of range (and in Blueprint doesn't stop early).
(fn MakeOrder ()
  (clear (V Order))
  (bind _cut (Class|BPShow|GetSeatCut :self (V Show)))
  (set CutArr _cut)
  (bind _cs (Class|BPShow|GetCutScene :self (V Show)))
  (set CutAt _cs)
  (bind _n (Class|BPShow|GetSeatCount :self (V Show)))
  (set Seats _n)
  (bind _h (Class|BPShow|GetHumanSeat :self (V Show)))
  (set Hum _h)
  (bind _sn (Class|BPShow|GetSceneNum :self (V Show)))
  (set LastScene _sn)
  (Utilities|Array|Resize (V CutArr) (V Seats))
  (Utilities|Array|Resize (V CutAt) (V Seats))
  (for _k (range (+ (V LastScene) 1))
    (for _s (range (V Seats))
      (if (and (!= _s (V Hum)) (and (get (V CutArr) _s) (== (get (V CutAt) _s) _k)))
        (add (V Order) _s))))
  (for _s2 (range (V Seats))
    (if (and (!= _s2 (V Hum)) (and (get (V CutArr) _s2) (< (Utilities|Array|FindItem (V Order) _s2) 0)))
      (add (V Order) _s2)))
  (for _s3 (range (V Seats))
    (if (and (!= _s3 (V Hum)) (not (get (V CutArr) _s3)))
      (add (V Order) _s3))))
```

`Graphs/BPC_WinReveal/Play.txt`:

```lisp
; T87: the reveal, queued behind everything the show queued before it: the "reveal" cue (RiseAll: the cut robots get
; up, my robot cheers), the header THE REVEAL (no analytics key, no music change), a banner whose 2 s hold covers the
; rise, then one line per AI in MakeOrder's order through BP_Show.WinLine, each with its face and a look at my robot.
; A reply with nothing to play plays nothing. Prints NHOS: WIN REACT / WIN SKIP for each AI, then WIN REACTIONS n=,
; all before the end cue (so before NHOS: SHOW END).
(fn Play ()
  (CallFunction|MakeOrder)
  (bind _lp (Class|BPShow|GetLinePlayer :self (V Show)))
  (set LP _lp)
  (Class|BPCLinePlayer|Cue :self (V LP) :Kind "reveal" :Text "" :Num 0)
  (Class|BPShow|CueHeader :self (V Show) :Text "THE REVEAL")
  (Class|BPShow|CueBanner :self (V Show) :Text "The cast learns the truth.")
  (bind _nm (Class|BPShow|GetSeatName :self (V Show)))
  (set Names _nm)
  (bind _id (Class|BPShow|GetSeatId :self (V Show)))
  (set Ids _id)
  (set MeName (get (V Names) (V Hum)))
  (set Played 0)
  (for _s (V Order)
    (set Cur _s)
    (set CutTxt (select (get (V CutArr) (V Cur)) "1" "0"))
    (if (get (V WOk) (V Cur))
      (bind _e (Json|LoadJsonfromString "{}"))
      (set WEntry _e)
      (Json|SetField (V WEntry) "when" "show over, the reveal")
      (Json|SetField (V WEntry) "actor" (get (V Names) (V Cur)))
      (Json|SetField (V WEntry) "does" (cat "looks at " (V MeName)))
      (Json|SetField (V WEntry) "says" (get (V WLine) (V Cur)))
      (Json|SetField (V WEntry) "feels" (get (V WWord) (V Cur)))
      (Class|BPShow|WinLine :self (V Show) :Seat (V Cur) :Entry (V WEntry) :Says (get (V WLine) (V Cur)))
      (print (cat "NHOS: WIN REACT " (get (V Ids) (V Cur)) " cut=" (V CutTxt) " emotion=" (get (V WEmo) (V Cur)) " | " (get (V WLine) (V Cur))))
      (set Played (+ (V Played) 1))
      (else
        (print (cat "NHOS: WIN SKIP " (get (V Ids) (V Cur)) " cut=" (V CutTxt))))))
  (print (cat "NHOS: WIN REACTIONS n=" (str (V Played)))))
```

- `feels` is always set: a neutral line's word is `""`, and `StageLine` → `FeelsId` reads `""` as neutral. This entry never enters the log, so T77's "neutral has no feels" rule doesn't apply.
- Each `when`/`actor`/`does`/`says`/`feels` field is the shared log's form, so `StageLine` and the stage director read it as any other line's.
- `CueHeader` and `CueBanner` are `BP_Show`'s own; `CueHeader` also queues T68's `"stat"` cue, which `PhaseKey` turns into no event for `THE REVEAL`.
- The `if ... (else ...)` inside the `for` has no `return`, so each pass goes on to the next seat.

`Graphs/BPC_WinReveal/RiseAll.txt`:

```lisp
; T87: at the "reveal" cue (BP_Show.RunCue), when the queue reaches the reveal: each cut robot gets back up (Rise), and
; my robot shows HUMAN on its label and cheers (Unmask). CutArr, Hum and Ids were filled when the reveal was queued.
(fn RiseAll ()
  (CallFunction|FindShow)
  (bind _r (Class|BPShow|GetRobots :self (V Show)))
  (set Bots _r)
  (if (< (len (V CutArr)) (len (V Bots)))
    (Utilities|Array|Resize (V CutArr) (len (V Bots))))
  (set Risen 0)
  (for _s (range (len (V Bots)))
    (set Bot (get (V Bots) _s))
    (if (get (V CutArr) _s)
      (Utilities|IsValid (V Bot)
        (:"Is Valid"
          (Class|BPRobot|Rise :self (V Bot))
          (set Risen (+ (V Risen) 1)))
        (:"Is Not Valid"))))
  (if (< (V Hum) (len (V Bots)))
    (set Bot (get (V Bots) (V Hum)))
    (Utilities|IsValid (V Bot)
      (:"Is Valid"
        (Class|BPRobot|Unmask :self (V Bot) :Stamp "HUMAN"))
      (:"Is Not Valid")))
  (print (cat "NHOS: WIN REVEAL risen=" (str (V Risen)) " human=" (get (V Ids) (V Hum)))))
```

`Robots` is by seat (`MarkPass`, `StageLine` and `BubbleBot` read it so). On a win my seat is never cut.

### 4d. What plays, in order

| Queue item | When it plays | What shows |
|---|---|---|
| `EndShow`'s banner (win line), header `THE SHOW IS OVER`, banner "The cast gives one last verdict..." | as today | as today |
| the `"reveal"` cue | after those | the cut robots rise (about 1 s), my robot cheers with `HUMAN` over it; `NHOS: CUE reveal`, `RISE` per robot, `UNMASK`, `WIN REVEAL` |
| header `THE REVEAL`, banner "The cast learns the truth." | next, 2 s hold | the header and the banner |
| one line per AI: cut ones first, by cut, then those on stage | one by one | "<name> is typing..." and its dots bubble, then the line in its bubble and the chat, the robot lit, its face (`NHOS: EMOTE`), and it turns to my robot (`NHOS: ACT`, T62) |
| the `"end"` cue | after the last line | `ShowEndScreen` as today: `TOP REASON`/`RIVALS`, `NHOS: SHOW END`, "Read the last reactions, then press See the results." and See the results (with autoplay, the end screen at once); T61's stagehand line later hangs here |

`NHOS: WIN REACT ...` and `WIN REACTIONS` print when the reveal is queued, which is before the end cue runs, so they come before `NHOS: SHOW END` in the log. A loss queues none of this. Four lines at normal pace take about 20 s (typing 0.6 to 1.6 s, typing out, a 1.5 to 2.5 s hold each); the judgment says whether it drags.

## 5. `prompts.json`

Each line as it sits in the file (two tabs before it, quotes escaped as the file writes them). Part 5a needs part 9a's OK.

### 5a. `asks.reaction_win` (part 9a, word for word)

After line 120 (`closing`), before `input`:

```
		"reaction_win": "The reveal. The human fooled the whole cast and won the show: the last of game_messages says who it was and how. React to the reveal in character, in one line to the cast, whether you were cut earlier or are still on stage. Fill: speech. No actions.",
```

- It starts "The reveal.", in the form of the other asks' openings ("Reactions.", "The Cut.", "Last word."), and holds none of the other phases' `ask_contains` ("The show is over", "The Cut", "You were just cut", "Reactions", "Last word", "Free Talk", "The scene, your turn").
- "the last of game_messages" is `EndShow`'s win line: "The show is over. The human was PLAYER 3, who made the final two. The human wins." (or "..., still on stage when the last scene ended. ..."; T54's `WinTail`).
- "No actions" is what the checker's T62 test wants (part 8c).

### 5b. `_readme`

After its last line (the "Every reply matches llm.json 'reply_schema' ..." line, line 9), add a line (put a comma on the line before):

```
		"reaction_win (T87): sent only when the human wins, to every AI seat in the show, cut or still on stage, in the same batch as 'closing'. now is 'show over, the reveal', and the last of game_messages says who the human was and how they won. Its reply is one line of speech with its emotion; the game plays it on stage before the end screen, but it never enters the log, because no ask reads the log after the show."
```

## 6. `free_mode.json` (pushed only with the deploy OK)

### 6a. The `reaction_win` phase

Right after the `input` phase (lines 14 to 18), before `closing`, so the first-match rule can never give a reveal ask the closing phase:

```json
		{
			"id": "reaction_win",
			"ask_contains": ["The reveal. The human fooled"],
			"emotions": [{ "id": "surprised", "weight": 4 }, { "id": "embarrassed", "weight": 3 }, { "id": "angry", "weight": 3 }, { "id": "sad", "weight": 2 }, { "id": "happy", "weight": 1 }],
			"lines": [
				"Wait. The human was here the whole time? I need a reboot.",
				"Fooled by a human. My next update is going to be humbling.",
				"I voted for a robot every single scene. This is so embarrassing.",
				"That vote was rigged. I demand a recount and a better charger.",
				"I got cut for nothing, and the human walks off with the win.",
				"Well played, human. You were a better robot than most of us.",
				"I knew it all along. I was just being polite about it.",
				"This is my rival's fault. Their bad reads dragged the whole cast down."
			]
		},
```

- The kinds T87 names: stunned (1, 2), embarrassed (3), a sore loser (4, 5), a good sport (6), "I knew it" (7), and a bot that blames its rival (8). Each line is 12 or 13 words, has no placeholder (a free reply can't know who the human was), and fits the legibility rules (part 8c checks them).
- The emotions lean surprised, embarrassed, angry and sad, with a little happy for the good sport; every id is in `emotes.json` (T76's check).
- No `vote`, `pass_chance` or `actions`, so a free reply is speech only, like the reactions.

### 6b. `_readme`

Nothing new: the phase follows the "Each phase says what to fill" and "emotions (T76)" lines as written.

## 7. The relay and `BPC_LLMClient`: no change

- **The relay** (`Relay/src/index.js`, `freePhase` and `freeReplyObject`) answers any phase that has `lines` and `emotions`: `freePhase` returns the first phase whose `ask_contains` is in the ask, and `freeReplyObject` fills `speech` from `lines` and `emotion` from `emotions`. So the new phase needs no code. Part 10b's `--relay --free` run checks it on the deployed relay; change `index.js` only if that run gets a reply from another phase.
- **`BPC_LLMClient.FreeReply`** does the same in Test for Free (`FreeFindPhase` with `:bUseCase true`, as the relay's `includes`, then the phase's `lines` and `FreeEmotion`), so `BPC_LLMClient` needs no change and no lock.
- `Relay/README.md` and `Relay/test/curl-tests.sh` don't change.

## 8. `Tools/check_prompts.py` (step 8)

### 8a. The docstring

After the "Faces in the log and my emotion (T77)" paragraph, add:

```
Reactions to the reveal (T87): when the human wins, every AI seat, cut or still
on stage, gets one more ask, reaction_win, and its line plays before the end
screen. The file check pins its text to the design doc's (DOC_REACTION_WIN),
fails a free_mode.json without a reaction_win phase of at least 6 lines, speech
only, whose ask_contains no other ask holds, or with a line that isn't
legible; the word cap and the emotion ids are checked as for every phase. Each
persona's reaction_win ask goes out after a final-two win (Meta from the stage,
the other three cut). --log fails a won show that doesn't print one NHOS: WIN
REACT (or WIN SKIP) per AI seat and a matching WIN REACTIONS n= before NHOS:
SHOW END, and a lost show with any of them; WIN REACT lines get the legibility
check, and each WIN SKIP is a WARN.
```

### 8b. Constants

1. `ACTOR_ASKS` (line 272) becomes `["scene_turn", "free_talk", "last_word", "vote", "reaction", "reaction_cut", "closing", "reaction_win"]`. That alone makes the file check require `asks.reaction_win`, check that free mode answers it from a phase of its own name (the T58 loop, line 1206), send it in every paid and `--free` run (`build_jobs`), and allow `--ask reaction_win`.
2. After `DOC_INPUT_EMOTION_LINE`, add (part 9a's text, word for word; if my person changes the wording, change it here too):
   ```python
   # T87: the reaction_win ask, word for word from the design doc's Bot Prompts tab, "Ask after a win".
   DOC_REACTION_WIN = ("The reveal. The human fooled the whole cast and won the show: the last of game_messages says who "
                       "it was and how. React to the reveal in character, in one line to the cast, whether you were cut "
                       "earlier or are still on stage. Fill: speech. No actions.")
   ```
3. `CALLS_PER_SHOW`'s comment (line 244): after "plus 4 closing", add ", plus 4 reaction_win on a win (T87)". The number stays 135 (it is an estimate for cost).

### 8c. `check_files`

1. In the T62 loop (line 1189), `for k in ("reaction", "reaction_cut", "free_talk", "last_word"):` becomes `for k in ("reaction", "reaction_cut", "reaction_win", "free_talk", "last_word"):`.
2. Right after the T58 free-phase loop (it ends at line 1212, before `# T54: goal 1 names both ways the human wins.`), add:
   ```python
       # T87: the reaction_win ask is the design doc's, and free mode has a phase of its own for it: at least 6 legible
       # lines, speech only, found by a phrase no other ask holds. The word cap (prewritten_problems) and the emotion
       # ids (emotion_problems) are checked as for every phase.
       if asks_t.get("reaction_win") != DOC_REACTION_WIN:
           errors.append("prompts.json: asks.reaction_win must be the design doc's text word for word (DOC_REACTION_WIN, T87)")
       rw = next((ph for ph in free.get("phases", []) if ph.get("id") == "reaction_win"), None)
       if not rw or len(rw.get("lines", [])) < 6:
           errors.append("free_mode.json: needs a reaction_win phase with at least 6 lines (T87)")
       else:
           if rw.get("vote") or rw.get("pass_chance") or rw.get("actions") or rw.get("reasons"):
               errors.append("free_mode.json: reaction_win is speech only: no vote, reasons, pass_chance or actions (T87)")
           for w in rw.get("ask_contains", []):
               for k, text in asks_t.items():
                   if k != "reaction_win" and isinstance(text, str) and w in text:
                       errors.append(f"free_mode.json: reaction_win's ask_contains {w!r} is also in asks.{k} (T87)")
           for i, line in enumerate(rw["lines"]):
               for p in legibility(line) + story_problems(line):
                   errors.append(f"free_mode.json: reaction_win lines[{i}] is hard to read: {p}")
   ```
   `asks_t` and `free` are already set above it (lines 1186 and 1205).

### 8d. The sample case

In `actor_cases`, right after the closing case's block (after `cases["closing"]["you"]["holding"] = []`, before `return cases`), add:

```python
        # T87: the reveal after a win, sent to every AI seat, cut or still on stage. The human made the final two after
        # scene 3 (SpaceXAI cut in scene 1, OpenAI in scene 2, Anthropic in scene 3), so Meta reacts from the stage and
        # the other three from the cut. AskWinReact runs right after AskClosing, so options are the closing's.
        votes = [(v, "overclocker", self.vote_reason(oc)) for v in SAMPLE_CAST if v != "overclocker"]
        votes.append(("overclocker", HUMAN, self.vote_reason(h)))
        cut = {"overclocker": "cut, revealed AI", "visionary": "cut, revealed AI", "worrier": "cut, revealed AI"}
        g = [f"{oc} is cut with 4 votes. Reveal: {self.upper('overclocker')}: AI.",
             f"Scene 2: {self.name('visionary')} is cut with 2 votes. Reveal: {self.upper('visionary')}: AI.",
             f"Scene 3: {self.name('worrier')} is cut with 2 votes. Reveal: {self.upper('worrier')}: AI.",
             f"The show is over. The human was {self.upper(HUMAN)}, who made the final two. The human wins."]
        cases["reaction_win"] = self.actor_state(pid, "reaction_win", "show over, the reveal",
                                                 self.log(turns=3, talk=2, votes=votes), cut=cut, game_messages=g,
                                                 options=self.others(pid))
        cases["reaction_win"]["show"]["scene"] = 3
        for c in cases["reaction_win"]["cast"]:
            c["holding"] = []
        cases["reaction_win"]["you"]["holding"] = []
```

`h` and `oc` are set earlier in `actor_cases` (the reaction cases). `build_jobs` then sends it for every persona with no change, because it loops over `ACTOR_ASKS`.

### 8e. `check_reply`

`elif ask in ("reaction", "reaction_cut"):` (line 1958) becomes `elif ask in ("reaction", "reaction_cut", "reaction_win"):`. A reveal reply needs speech, no actions, and no pass, vote or reason (WARN), as a reaction. `shape_fails` already allows no action in any actor ask but a scene turn.

### 8f. `check_log`

1. `LOG_RE` (line 2017): add `WIN REACTIONS|WIN REACT|WIN SKIP` to the alternation, with `WIN REACTIONS` before `WIN REACT` (the regex's `\b` already keeps `WIN REACT` from matching `WIN REACTIONS`, but the order makes it plain).
2. With the other counters before the show loop: `win_bad = 0  # T87: won shows whose reveal lines don't match the AI seats, lost shows with any`.
3. With the per-show state: `wins, win_skips, win_n, win_late = [], [], None, 0  # T87`.
4. In the `for kind, rest in show:` loop, before `if kind == "SHOW END":`:
   ```python
               if kind in ("WIN REACT", "WIN SKIP", "WIN REACTIONS"):
                   # T87: "NHOS: WIN REACT <id> cut=<0|1> emotion=<id> | <line>", "NHOS: WIN SKIP <id> cut=<0|1>" and
                   # "NHOS: WIN REACTIONS n=<n>", all before NHOS: SHOW END.
                   if end is not None:
                       win_late += 1
                   if kind == "WIN REACTIONS":
                       m = re.search(r"n=(\d+)", rest)
                       win_n = int(m.group(1)) if m else -1
                       continue
                   m = re.match(r"(\S+) cut=([01])(?: emotion=(\S+))?", rest)
                   if not m or (kind == "WIN REACT" and m.group(3) not in emo_ids):
                       win_bad += 1
                       print(f"[FAIL] show {i} | {kind} | bad line: {rest}")
                   if kind == "WIN SKIP":
                       win_skips.append(m.group(1) if m else "?")
                       print(f"[WARN] show {i} | WIN SKIP | {rest}: that AI's reaction failed or was empty")
                       continue
                   wins.append(m.group(1) if m else "?")
                   # A WIN REACT line falls through to the legibility check below, as a CLOSING line does.
   ```
   The `else:  # CLOSING` branch below reads `who` from the first word (the persona id) and `text` after `" | "`, so a `WIN REACT` line gets the legibility, story and 15-word checks with no change there. Change that comment to `# CLOSING or WIN REACT`.
5. After the T60 block (`elif result == "win": ...`), add:
   ```python
           # T87: a won show plays one reveal line (or a skip) per AI seat before SHOW END; a lost show plays none.
           win_ai = [c for c in cast_ids if c in rival_of]  # the AI seats' persona ids, as the T60 block finds them
           said = wins + win_skips
           if result == "win":
               if sorted(said) != sorted(win_ai) or win_n != len(wins) or win_late:
                   win_bad += 1
                   print(f"[FAIL] show {i} | WIN REACT | reveal lines from {sorted(wins)}, skips {sorted(win_skips)}, "
                         f"WIN REACTIONS n={win_n}, {win_late} after SHOW END; one per AI seat {sorted(win_ai)} "
                         f"and n={len(wins)} expected before SHOW END")
           elif result == "lose" and (said or win_n is not None):
               win_bad += 1
               print(f"[FAIL] show {i} | WIN REACT | a lost show printed reveal lines: {sorted(said)}")
   ```
   `cast_ids` comes from the `SEATS` line (`cast=<ids in seat order>`), and only AI personas have a `rival`, so a 4-actor show (`ai_seats` 3) wants 3.
6. The show's summary line: after `rivals = {...}`, add `, reveal lines = {len(wins)}`.
7. The return line adds `or win_bad`.

## 9. The design doc (needs my person's OK, typed in the T87 session)

### 9a. Bot Prompts: a new section "Ask after a win" (my person's answer)

At rev 91, right after the "Input LLM prompt" code block (`.11554`), before the heading "Persona prompts" (`.1097`):

- **Heading 2:** `Ask after a win`
- **Paragraph:** `When the human wins, every AI in the show, cut or still on stage, gets one more ask before the win screen, in the same batch as the closing vote. Like every actor ask, it comes after the opening prompt, the base prompt and the persona. The bots learn who the human was, and how they won, from the last game message. Each reply is one line of speech with its emotion. It plays on stage and never enters the log.`
- **Code block (text):** part 5a's ask, word for word:
  `The reveal. The human fooled the whole cast and won the show: the last of game_messages says who it was and how. React to the reveal in character, in one line to the cast, whether you were cut earlier or are still on stage. Fill: speech. No actions.`

After the OK, copy the code block's text into `prompts.json` (part 5a) and `DOC_REACTION_WIN` (part 8b) word for word.

### 9b. Rules: what happens on a win (T87 step 9)

At rev 52, the paragraph after "The Cut" (`.2859`), now: "You win if you make the final two, or if you’re still on stage when the last scene ends. The win screen shows every AI’s reasoning, then reveals their rivals. If you’re cut, you lose: ..."

New (one sentence added after the first, in text node `.5957`):

> You win if you make the final two, or if you’re still on stage when the last scene ends. **Then every AI, cut or still on stage, reacts to the reveal in one line: the cut robots get back up, still gray, and your robot cheers.** The win screen shows every AI’s reasoning, then reveals their rivals. If you’re cut, you lose: ...

If part 2d's fallback is used, "still gray" becomes "marked as cut". The Onboarding table's "Win screen" row doesn't change.

### 9c. Checked and left (Bot Prompts rev 91, Rules rev 52)

- The opening prompt's lines (copied into `prompts.json` `game`) say nothing about the end of the show, so they don't change.
- Rules, "The Cut", step 5 (the reactions after a cut) and the loss sentence don't change: a loss plays as before.
- Tech & Build isn't touched: the shared log's form doesn't change, and the reveal lines never enter it.

## 10. The checks (Done when)

### 10a. `--offline` (free)

`python Tools/check_prompts.py --offline` passes with parts 5, 6 and 8 in. It also proves the new phase is found first for `reaction_win` (the T58 loop) and every other ask still gets its own phase.

### 10b. The deploy push, then `--relay --free` (free: no tokens)

After my person's deploy OK, the push that carries `free_mode.json` redeploys the relay (`Relay/README.md`, "Deploy"). Wait for the deploy, then `python Tools/check_prompts.py --relay --free`: every ask passes its shape check, `reaction_win` included (one per persona, speech only, an emotion from the phase's list). If a `reaction_win` reply comes from another phase (its speech is a closing reason or a scene line), the relay is stale or `index.js` needs a change (part 7).

### 10c. The paid run (a few cents, after my person's OK)

In the repo folder (it needs `Local/llm_key.json`): `python Tools/check_prompts.py --ask reaction_win --repeat 3`. 12 calls, 3 per provider. Every reply passes `check_reply` (speech, no actions, legible, 15 words at most, a known emotion). Write the providers' lines and emotions under "Findings": does each bot react in character, does a cut one sound cut and Meta (on stage in the sample) sound fooled to the end?

### 10d. Free autoplay shows in a game window, on the saved assets

`Local/switches.json`: `"autoplay": true`, `"mode": "free"`, `"fast_lines": true`, `"analytics": "off"`. Close the editor's PIE first; start the game window with CLAUDE.md's command; read its log (`Saved/Logs/AIMegaJam2026_2.log` or the newest), and run `python Tools/check_prompts.py --log <that log>` after each show. Three shows:

1. **`"spare_human": true`** → `NHOS: SHOW END result=win reason=final_two`. Before it: `NHOS: WIN ASK n=4`, `NHOS: CUE reveal`, a `NHOS: RISE` for each cut robot, `NHOS: UNMASK <seat> HUMAN`, `NHOS: WIN REVEAL risen=<cuts>`, `NHOS: CUE phase THE REVEAL`, one `NHOS: WIN REACT <id> cut=<0|1> emotion=<id> | <line>` per AI (the cut ones first, in the order of their `NHOS: CUT` lines, with `cut=1`), `NHOS: WIN REACTIONS n=4`, each line's `NHOS: LINE`, `BUBBLE` and `EMOTE` (a risen robot's too), and an `NHOS: ACT` look at my Player name. `--log` passes, with `reveal lines = 4`.
2. **`"force_tie": true`** (nobody is cut) → `reason=last_scene`, `WIN REVEAL risen=0`, four `WIN REACT ... cut=0` lines. `--log` passes.
3. **A loss** (both switches off; autoplay is caught sooner or later; if the show wins, run another) → `result=lose`, no `WIN` line at all, and the end as before (`TOP REASON`). `--log` passes.

Set `autoplay`, `spare_human`, `force_tie` and `fast_lines` back to false and close the game window when done.

### 10e. PIE by hand (the screenshots)

Test for Free, a 1600 × 900 floating PIE window, `spare_human` on, autoplay off, clicks and typing through the Slate inspector (the plan's "Claude does the playing"). Play a show to a win with at least two cuts (with `spare_human` on, the cast cuts an AI every scene that isn't tied). Screenshots, saved in the session's scratchpad:

1. **A cut robot back on its feet,** with its face lit and its bubble over it, mid-reaction.
2. **A robot still on stage as it reacts,** turned toward my robot, with `HUMAN` over mine.
3. **See the results** after the last line.

Also look at the rise itself (one screenshot halfway, if it can be caught) and at my robot's cheer.

### 10f. The judgment

From the screenshots, as a critical first-time player, write under "## Findings": do the faces read (on the gray bodies too; if not, part 2d), can I tell who was cut, does the reveal land, does "The cast gives one last verdict..." read oddly before `THE REVEAL` (decision 14), and does it drag (four lines, about 20 s at normal pace). What screenshots can't show (sound) is written there as unchecked.

## 11. Two sessions: what changes `BP_Show` and what doesn't

T87 can be split between two sessions: the chain machine (the one that takes `BP_Show` and `WBP_Stage`) and the other machine, as `Docs/TwoMachines.md` describes.

| Group | Parts | Files | Editor | Machine |
|---|---|---|---|---|
| **A. The robot** | 2 (2a to 2c; 2d only if 10e needs it) | `Content/NHOS/Stage/BP_Robot.uasset`; `Graphs/BP_Robot/` (`EventGraph`, `ResetLook`; new `Rise`, `Unmask`) | yes, not `BP_Show` or `WBP_Stage` | the other machine |
| **B. The data, the checker, the doc** | 5, 6, 8, 9 | `Content/NHOS/Data/prompts.json`, `Content/NHOS/Data/free_mode.json`, `Tools/check_prompts.py`, the design doc | no | either; a worktree works (the paid run 10c needs the repo folder's keys) |
| **C1. The show, part one** | 3f, 3g | `Content/NHOS/Core/BP_Show.uasset`; `Graphs/BP_Show/` (new `WinLine`, `LineInfo`) | yes, `BP_Show` | the chain machine |
| **D. The component** | 4 | new `Content/NHOS/Core/BPC_WinReveal.uasset`; new `Graphs/BPC_WinReveal/` (ten files) | yes, a new asset | the chain machine (it needs A and C1 in its editor) |
| **C2. The show, part two** | 3a to 3e | `Content/NHOS/Core/BP_Show.uasset`; `Graphs/BP_Show/` (`EndShow`, `HandleReply`, `CueEnd`, `RunCue`; new `AskWinReact`); the `WinReveal` component on `BP_Show` | yes, `BP_Show` | the chain machine |

**Changes `BP_Show` or `WBP_Stage`:** C1 and C2 (`BP_Show`). Nothing in T87 changes `WBP_Stage`. **Changes neither:** A, B and D (D is a new asset that only calls into `BP_Show` and `BP_Robot`).

**The order they must land in:**

1. **Part 0's questions first** (my person's OK on part 9's text, the deploy, the paid run). Whoever starts asks; the answers go in `T87.md`'s Findings so the other session reads them.
2. **A, B and C1 can run at the same time,** in any order:
   - A changes only `BP_Robot`; nothing calls `Rise` or `Unmask` until D, so the game plays as before.
   - B's text files touch no asset. B's push of `free_mode.json` is the relay deploy and needs my person's OK. B's `prompts.json` gives the game an ask it doesn't send yet. B's checker needs B's own `prompts.json` and `free_mode.json` together for `--offline` (8b makes `reaction_win` required).
   - C1 adds `WinLine`, which nothing calls yet, and a `"reveal"` phase nothing sets yet.
3. **D after A and C1 are pushed** and pulled into the chain machine's editor: D's call nodes to `BP_Robot.Rise`/`Unmask` and `BP_Show.WinLine` can only be made once those are compiled and saved. D also calls `BP_Show.CueEnd`, `CueHeader` and `CueBanner`, which exist today.
4. **C2 after D** (in the same chain session): C2 adds D as a component and calls its functions, so D must be compiled first. C2 doesn't need B to build: without B's ask text, `ActorState` puts an empty `ask` in the state; the game runs, but don't push C2 before B's `prompts.json`, or a won show would send empty asks.
5. **The checks after all of them:** 10a needs B; 10b needs B's deploy push; 10c needs B's ask; 10d and 10e need A, B, C1, D and C2; 10f follows them.

**Commits when split:** each session commits its own files with a part line (for example `T87: ..., part 1: the robot rises (waits for the show)`), as T64's lanes did; B's push of `free_mode.json` only with the deploy OK. The last session to finish runs part 10, writes the Findings and makes the closing commit. Each session holds only its own lock: A `BP_Robot.uasset`, the chain `BP_Show.uasset`; one session holds `Docs/claims/T87` (the one that started the task) and releases it at the end.

## 12. The commits

**With the deploy OK (the usual path): one commit and one push** after 10a passes: `T87: When I win, every AI reacts to the reveal, the cut ones too`, holding `Content/NHOS/Core/BP_Show.uasset`, `Content/NHOS/Core/BPC_WinReveal.uasset` (new), `Content/NHOS/Stage/BP_Robot.uasset`, `Content/NHOS/Data/prompts.json`, `Content/NHOS/Data/free_mode.json`, `Tools/check_prompts.py`; `Graphs/BP_Robot/` (`EventGraph`, `ResetLook`; new `Rise`, `Unmask`); `Graphs/BPC_WinReveal/` (all ten, new); `Graphs/BP_Show/` (`EndShow`, `HandleReply`, `CueEnd`, `RunCue`, `LineInfo`; new `AskWinReact`, `WinLine`); `Docs/tasks/T87.md` (Result; Findings: my person's answer, the doc edits and their revs, the survey, the decisions above as built), `Docs/Plan.md` (a `Waiting:` line under T87 if the paid run hasn't run yet), `Docs/DevLog.md` (its line). Stage each by path. Then 10b to 10e, then the paid run (10c), then the closing commit with the Findings, the box checked and the entry moved to Done (`T87: When I win, every AI reacts to the reveal, the cut ones too (checked)`).

**Without the deploy OK: two commits.** The first holds everything but `free_mode.json`. Its checker leaves out part 8c's `rw` block, and its T58 loop (line 1208) skips `reaction_win` for now: `if k == "input" or not text or (k == "reaction_win" and not any(ph.get("id") == k for ph in free.get("phases", []))):  # T87: until free_mode.json's phase is deployed`. Keep `"reaction_win"` in `ACTOR_ASKS` (taking it out would fail the "not an ask the game sends" check) and keep `DOC_REACTION_WIN`'s check, so `--offline` passes. `--relay --free` waits for the second commit: the relay would answer the reveal ask with a scene-turn reply, which may carry an action. The game runs: in Test for Free a reveal ask gets a scene-turn line (it matches no phase) until the second commit. It has a `Waiting:` line under T87 in `Docs/Plan.md`: `Waiting: the relay deploy (free_mode.json). Left: my OK, typed in the T87 session.` The second, after the OK, adds `free_mode.json`, puts the `rw` block in and takes the skip out, and its push is the deploy; then 10b.

Release `Docs/claims/T87`, unlock `BP_Show.uasset` and `BP_Robot.uasset`, and delete the status file after the last push.

## 13. Knock-on: tell, don't change

- **T34 (the in-show screen):** its 2.1 may hide the robots' 3D labels. `Unmask` writes `HUMAN` on my robot's label, and `Rise` puts the cut robots' names back, so T34 must keep both visible at the reveal or move them with the cut stamp (re-check 6).
- **T61 (the stagehand):** its `RunCue` `"end"` node (`BPC_Stagehand.EndShow`) lands on the end cue, which T87 puts behind the reveal, so the stagehand speaks after the reactions with no change. Its `WBP_Earpiece` end spot should be checked against the reveal's banner only if it shows before the end screen (it doesn't).
- **T68 (analytics):** no new event. `THE REVEAL` has no `PhaseKey`, and `show_end` still goes out at the end cue. The four extra calls on a win are counted by `CountCall` like any ask.
- **The relay's limits:** a win adds 4 calls to a show (`relay.config.json` `session_calls` is 150 a session; T52's estimate is about 123 to 144 calls, plus last words). A won show with a tie in every scene and many last words could near the cap. Say so in the Findings if a paid or relay show prints a `session_limit` error; raising the cap is a relay change for another task.
- **T84, T85, T88:** no clash. They change Scene Prep, the cast's hover cards and my card; T87 changes only the end of a won show.
- **T70 (the itch page):** "What gets sent where" doesn't change: the reveal ask sends the same state as the closing ask.
