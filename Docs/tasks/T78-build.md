# T78 build sheet: I can pick my robot's emotion

Back to [T78](T78.md). A PC prep session first wrote this on 2026-11-15 against `61199ce`. It is a plan, not a record: nothing here was written to the editor. When T78 writes a graph, its source goes to `Graphs/` as usual.

## This update (2026-11-15, against `noHumansOnSet` at `7c33e70`)

**Why:** the first version was written from the T63, T64, T65, T66 and T75 build sheets, before any of them was built, and without T77's sheet. T63, T64, T65 and T75 are now built and pushed, T77's sheet is written (and updated today, against the same commit), and T66 is being built now. A prep session (no editor) checked every graph, widget, variable, function and data field this sheet names against today's files: `Graphs/WBP_ActionBuilder/` (`ChipClicked`, `OpenTurn`, `MakePreview`, `PickLine`, `Refresh`, `AddChip`, `BuildChips`, `Close`, `IsOn`, `KeepFocus`, `SetFocusBack`, `DrawPreview`), `Graphs/WBP_Chip/` (`Setup`, `EventGraph`), `Graphs/WBP_Stage/` (`SetPrompt`, `FitBuilder`, `SetPrepMode`, `SetPhase`, `AtDraw`, `AtPlace`, `AtShow`, `AtLists`, `SpeechKey`, `HoldFocus`, `OnPreviewMouseButtonDown`, `BuilderTurn`, `SyncAction`), `Graphs/UIStyle/` (`StylePanel`, `StyleButton`, `UISize`), `Graphs/BP_Show/` (`SendHumanTurn`, `SendHumanTalk`, `SendHumanReact`, `SendHumanVote`, `SpellAsk`, `HumanSay`), `Graphs/BP_Robot/Emote.txt`, `emotes.json`, the findings in `T63.md`, `T64.md`, `T65.md`, `T69.md`, `T75.md`, `T76.md`, T77's updated sheet, T66's plan (`T66-build.md`) and **T66's work in progress in the repo folder** (its uncommitted `Graphs/WBP_Stage/` and `Graphs/BP_Show/Timer*.txt` files, read only), and the design doc (Rules rev 49, Turn Input rev 5; read, not changed).

**What changed in this sheet:**

1. **T77's emotion step is named:** `BP_Show.HumanFeels(Id, From)`, a new function with a file (T77-build part 3c). Every line of mine goes through it once, a pass and an empty line too, and callers use its return value. Part 5c now edits that file; the old re-check item 1 ("find where T77 settles my emotion") is answered.
2. **T64's names as built:** the preview line is `MakePreview` (not `PreviewText`); the WrapBox add is `Panel|AddChildtoWrapBox` and the clear `Widget|Panel|ClearChildren` (`AddChip`, `BuildChips`). `ChipClicked`'s first line and `OpenTurn`'s `(set Sent false)` are as the first version expected. `WBP_Chip.Setup(Owner, Index, Label, Actor, Picked)` and its click (`Builder.ChipClicked(ChipIndex)`) are unchanged.
3. **T65's names as built:** `FacePlace` now uses `AtPlace`'s nodes (`UserInterface|Geometry|LocaltoAbsolute(Coordinates)`, `AbsolutetoLocal(Coordinates)`, `GetLocalSize`, `Slot|SlotasOverlaySlot`, `Layout|OverlaySlot|SetPadding`). `AtPop` is styled in `AtLists`. `SpeechKey`'s Escape block now also sets `AtShutPos`.
4. **T65's pure-node trap is fixed in two functions:** a `bind` of a variable or a pure expression is read where it is used (`T65.md`, `AtDraw`). The first version's `FaceShow` bound `_was` before setting `FaceOpen`, and `SyncFace` bound `_rise` and `_fall` before setting `FaceWasOpen`: both would have read the new value. `FaceShow` now sets `FaceOpen` last, as `AtDraw` does, and `SyncFace` sets `FaceWasOpen` inside each branch, as T66's `TickTimer` does.
5. **The four sends have files** (T63): `SendHumanTalk`, `SendHumanReact` and `SendHumanVote` are file edits now, not node edits.
6. **The panel width:** T64 built the wide panel at **1080** (`LowerWideBuild`), not 1000, and T66 (in progress) splits `FitBuilder`'s width into its own check, `_wide = (or _on (V TimerWide))`, so the panel is already wide in my last word and my reactions (their timers). T78 adds `FaceRowOn` to that `_wide`, so the panel is 1080 on the whole play side. **My answer ("widen to 1000") stands; only the number follows what was built.** Part 3d says so.
7. **T66's files as it is writing them:** `SetPrompt` ends with `TickTimer`; `SetPhase` calls `ShapeRow` before `FitBuilder`; `SetPrepMode`'s prep branch collapses `TimerSize` and clears `TimerOn` and `TimerWide`; `TimeUp` sends a scene turn through `SubmitInput` (with `ForceSend`) and an empty last word or reaction as "pass" through `OnSend`. Each is marked **re-check after T66** below.
8. **Focus after a pick:** `ChipClicked`'s face branch returns before T64's `KeepFocus`, so `PickFace` calls `KeepFocus` itself (T65's `HoldFocus` would catch it a frame later anyway).
9. **T69's greyed-click hook doesn't see the face list:** `WBP_ActionBuilder.OnPreviewMouseButtonDown` only runs for clicks inside the builder, and the face list is in `WBP_Stage`'s `RootBox`. Nothing to change.
10. **BP_Show's stage getter** is `(Variables|Default|GetStage)` (the form every `BP_Show` source uses), not `(V Stage)`.
11. **T84 and T85** were added to the plan after T78 while this update was written (`61c2815`). T84 also changes `SetPrepMode` and moves `StartButton` out of the input row; re-check 4 and part 9 say what that means for T78.

**My answer in this sheet stands:** "widen to 1000" (question 1), now 1080 as built. No change made it moot, and this update needs no new decision.

**What T78 must still check in the editor** (part 0's survey): `InputRow`'s children after T66 (and whether T38's chat button is in it yet), that `VoteRow` is a variable, the node name `Widget|IsVisible`, `Class|WBPStage|FaceTake` from `BP_Show`, and each new builder function's `Class|WBPActionBuilder|...` name in `WBP_Stage`. And T66's pushed files, against item 7 above.

## Re-check before you write anything

T78 starts after T77 and T66 are pushed. Compare each point with what was pushed; where one differs, follow what was built and change this sheet's part to match.

1. **T77** (`Docs/tasks/T77.md` Findings, `Graphs/BP_Show/HumanFeels.txt`, `HumanEmo.txt`, `TakeEmo.txt`): `HumanFeels(Id, From)` prints `NHOS: HUMAN emotion=<id> from=<llm|keywords|none>` and returns the id; `HumanEmo` and `TakeEmo` use its return value; `--log` accepts `from=pick`. If T77 built it differently, the rule from the first version holds: put `ApplyFace` wherever my emotion is settled (each place, if more than one), and change only the value that goes into T77's carrier.
2. **T66** (`Docs/tasks/T66.md`, its `Graphs/WBP_Stage/` files): `SetPrompt` ends with `(CallFunction|TickTimer :CanType CanType)`; `FitBuilder` has `(bind _wide (or _on (V TimerWide)))` and its own `FitWide` check; `SetPrepMode`'s prep branch has the `TimerSize`, `TimerOn` and `TimerWide` lines before T64's `Close`; `TimeUp` reaches `SendHumanTurn` (scene) or `SendHumanTalk`/`SendHumanReact` (a "pass" or the typed line); `InputRow` ends with `TimerSize`. Also what the Pass button's `OnClicked` chain sends (T66's survey 1): it must reach `SendHumanTalk` or `SendHumanReact`, which part 5c covers either way.
3. **Nobody changed the T64 and T65 files this sheet edits since `7c33e70`** (`ChipClicked`, `OpenTurn`, `MakePreview`, `AtDraw`, `SpeechKey`): `git log --oneline 7c33e70..HEAD -- Graphs/WBP_ActionBuilder Graphs/WBP_Stage`. T66 changes only the `WBP_Stage` files in item 2.
4. **T38's step 5** (the chat button and hidden chat) comes after T78 in the plan. If it is built first, its `ChatButton` may be in `InputRow`: the chip still goes first, and the row's width is T34's to settle.
   **T84 and T85** (added to the plan at `61c2815`, after T78; Scene Prep's middle panel and the cast's hover card) also come after T78. If T84 is built first: `StartButton` has left `InputRow`, the whole lower panel is collapsed in scene 1's Scene Prep, and `SetPrepMode` has T84's lines. Part 3d's `SetPrepMode` lines still go in its prep and play branches; check that the chip's `FaceSize` collapses with the lower panel and comes back with it.
5. **`emotes.json`:** the `emotes` list with `id` and `word`, `neutral` first with an empty word (12 entries at `7c33e70`).

## In short

- **The chip goes first in the input row in every phase where I speak**, left of the speech field, so it is in the same place in my scene turns, Free Talk, the last word and the reactions. It is a `FaceBtn` button in `WBP_Stage`'s `InputRow` that reads **"Face: Auto"**, or "Face: worried" in paper (cream) after a pick. Its list is a pop-up over the chip (`FacePop`, like T65's `AtPop`), so nothing on the screen moves.
- **The logic and the list's chips are in `WBP_ActionBuilder`** (part 2), as the task says: it reads `emotes.json` once, keeps the pick (`Face`), makes the list's chips as T64's `WBP_Chip`s, and writes the preview line. A chip in the list has an `Index` of 1000 or more, and T64's `ChipClicked` sends those to `PickFace`. `WBP_Chip` doesn't change.
- **The panel is 1080 wide on the whole play side** (my person's answer, at T64's built width). The chat keeps its 380 px outside my scene turns.
- **The preview line:** `> looks worried · throw rose at @Meta: "Oops."`. Auto adds nothing.
- **My sends carry the pick:** each of my four sends (`SendHumanTurn`, `SendHumanTalk`, `SendHumanReact`, `SendHumanVote`) starts with one new call after `(set HumanSent true)`, `BP_Show.TakeFace()`. It copies the chip as it stands into `HFace`. T77's `HumanFeels` calls `ApplyFace`: with a pick, my emotion is the pick and the print says `from=pick`; with Auto, T77's way stays.
- **Back to Auto each turn:** the chip resets when my input opens (`SetPrompt`'s `CanType` goes true) and when a scene turn's builder opens (`OpenTurn`).
- **New check lines:** `NHOS: FACE loaded <n> emotions`, `NHOS: FACE list <n>`, `NHOS: FACE pick <id|auto>[ | <preview>]`, `NHOS: FACE close`, `NHOS: FACE reset`. T77's `NHOS: HUMAN emotion=<id> from=pick`.

## Questions for my person

The recommended answer is first.

**Answer (my person, 2026-11-15, to the prep session):** 1: **widen to 1000**, as recommended. Don't ask again; copy this answer under "Findings" in `T78.md`. The sheet is written for it. (Update at `7c33e70`: T64 built the wide panel at 1080, `LowerWideBuild`, so the panel is 1080 wherever the chip shows; T66 already widens it for the last word and the reactions.)

1. **Room for the chip.** At 640 px, Free Talk, the last word and the reactions have no room for the chip: with the counter, Action!, Pass and the timer, the speech field shrinks to about 120 px. T64's answer kept the panel at 640 outside scene turns.
   - **Widen to 1000 wherever the chip shows (Recommended).** The chip stays in one place in every phase, and the panel's top doesn't move. The chat keeps its 380 px outside scene turns. The speech field stays about 450 px wide even with the timer. This changes T64's answer for Free Talk, the last word and the reactions only.
   - The chip in its own row above the input row: in scene turns next to the preview line, elsewhere in a face-only strip. The panel keeps 640, and the chat shortens by about 56 px.
   - Keep 640 with a short chip ("Auto", "worried", no "Face:"). The field is about 170 px in the last word and the reactions.

## Decisions this sheet makes (open to change)

My person asked prep sessions to take their own recommendation on design calls. The T78 session shows this list to my person when it closes the task.

1. **The chip is in the input row, the logic is in the builder.** The task puts the chip in `WBP_ActionBuilder`, but T64 collapses the builder outside my scene turns (`Close` at every other header), and step 2 wants the chip in every phase where I speak. So the button and its pop-up are in `WBP_Stage`, and the builder keeps the pick, makes the list's chips and writes the preview. `WBP_Stage` reads the builder every frame (`SyncFace`), as T64's `SyncAction` does.
2. **The panel stays 1080 wide on the whole play side**, the vote included, and goes back to 640 only in Scene Prep. The chip hides in the vote (decision 4). A panel that narrowed for the vote and widened again for the reactions would jump twice in each scene. This goes a little past my person's answer ("wherever the chip shows"), so ask if it should narrow for the vote.
3. **The labels:** the chip reads "Face: Auto", or "Face: <word>" with the emotion's `word` from `emotes.json`. **Neutral is "calm"** (its `word` is empty; the Rules tab's "Emotions" bullet 1 says "a calm neutral face"). The list reads "Auto", then each emotion's word in `emotes.json`'s order: calm, happy, sad, angry, worried, scared, surprised, confused, disgusted, suspicious, smug, embarrassed (T75, as `emotes.json` lists them at `7c33e70`). A picked chip and the picked entry are paper; Auto is plum (Secondary), like T64's chips.
4. **The phases:** the chip shows in my scene turns, Free Talk (my last word is inside it, T58) and the reactions. It is enabled only while I can type (`CanType`), and hidden in the vote and in Scene Prep. Step 2 doesn't list the vote. With the chip hidden, a vote's face stays T77's way.
5. **A pick applies to a pass and to a turn with no words.** T77 gives those `neutral` (`from=none`). With a pick they show the pick (`from=pick`). That is why I would pick one: to say nothing and still look worried. T76's base prompt says the same to the bots ("A pass shows a face too"). This covers T66's timeouts too: a scene turn timed out with nothing typed, and a last word or reaction timed out empty (sent as "pass").
6. **The list is a pop-up grid**, 560 px wide, about four rows of chips, over the chip, on an ink panel. It closes when I pick, click the chip again, press Escape, start an @ mention (T65's list), or when my input closes. It never takes keyboard focus: `FaceBtn` and every `WBP_Chip` have `IsFocusable` off, `PickFace` calls T64's `KeepFocus`, and T65's `HoldFocus` takes the focus back anyway.
7. **The chip has a tooltip:** "The face your robot shows with this line. Auto: the game reads it from your words."
8. **The reset prints only when it clears a pick** (`NHOS: FACE reset`), so a show without picks doesn't print it every turn.
9. **A pick changes only my emotion.** The input LLM still fixes my spelling (T63), and its `emotion` is ignored when I picked. The keyword table runs too, and T78 ignores its answer.

## Step coverage

| T78 step | Where |
|---|---|
| 1. The chip "Face: Auto", its list from `emotes.json` (Auto, then each word), styled from `UIStyle`, never focused | Part 2 (`LoadFaces`, `FaceWord`, `FaceLabel`, `BuildFaces`, `AddFaceChip`, `PickFace`), part 3 (`FaceBtn`, `FacePop`, `SyncFace`, `FaceShow`); decisions 1, 3 and 6 |
| 2. In every phase where I speak, in each phase's input row as T66 left it | Part 3 (`FaceBtn` first in `InputRow`; `SyncFace`'s shown rule; `FitBuilder` and `SetPrepMode`); part 4; decision 4 |
| 3. My sends carry the pick; Auto is T77's way; a pick overrides it and prints `from=pick` | Part 5 (`TakeFace` at each send, `ApplyFace` in `HumanFeels`) |
| 4. Back to Auto each turn | Part 2 (`ResetFace`; T64's `OpenTurn`), part 3 (`SyncFace` on the rising `CanType`); part 6 Findings |
| 5. The timer sends the chip as it stands; the preview line shows a pick in words, nothing for Auto | Part 5 (T66's `TimeUp` reaches the sends, which call `TakeFace`); part 2 (`MakePreview`, `FacePhrase`) |

## 0. Before you start (after T77 and T66 are pushed)

1. `git log --oneline -20` shows T77 and T66. `Docs/claims/T77` and `Docs/claims/T66` are released. `git lfs locks` shows no lock on `Content/NHOS/UI/WBP_ActionBuilder.uasset`, `Content/NHOS/UI/WBP_Stage.uasset` or `Content/NHOS/Core/BP_Show.uasset`. Claim T78 (`git lfs lock Docs/claims/T78`) and lock all three.
2. Do "Re-check before you write anything" above, and write what differs under "Findings".
3. `python Tools/check_prompts.py --offline` passes. T78 changes no data file.
4. **The survey** (each item a separate `call_tool`; calls stop at about 120 s; save each read to `Saved/T78/<name>.read.txt`; never write a read-back to the editor):
   1. **`WBP_Stage`'s tree:** `InputRow`'s children in order with their slot paddings (expected after T66: `InputStack`, `CountSize`, `SendButton`, `PassButton`, `ContinueButton`, `StartButton`, `TimerSize`; `ChatButton` only if T38's step 5 came first); `RootBox`'s last child (T65's `AtPop`); and **`VoteRow`** (T09: between the log and the input row, `VoteBtn0` to `VoteBtn2`): that it is a variable, and that it is `Visible` only while my vote is open. `SyncFace` hides the chip while it shows. If the vote row stays up longer (while the votes are read), the chip hides then too, which is fine.
   2. **`WBP_ActionBuilder`'s variables:** `TmpK` (T65, Integer; `DrawPreview` uses it), `Armed`, `Sent`, `Live`. The new names in part 2a must not exist yet.
   3. **`BP_Show`:** the new names in part 5a don't exist; `HumanFeels` is T77's (its file).
   4. **Node names** with `find_node_types` (`context_pins: []`, T29): `Widget|IsVisible` in `WBP_Stage`; `Class|WBPStage|FaceTake` in `BP_Show` (after part 3 compiles); `Class|WBPActionBuilder|...` for each new builder function in `WBP_Stage` (after part 2 compiles).

## 1. The order of the build

T18 and T54: a call node goes stale when its function gets a new parameter. T63: a call node made before a compile has the skeleton's old pins, and `write_graph_dsl` can leave stale call nodes behind that break a compile. So create each function and its parameters first, compile, then write the graphs callee first, and trace each function's live nodes from its entry before you compile.

1. Part 0.
2. `WBP_ActionBuilder` (part 2): the variables; every new function with its parameters, empty; compile. Then write `LoadFaces`, `FaceWord`, `FaceLabel`, `FacePhrase`, `AddFaceChip`, `BuildFaces`, `PickFace`, `ResetFace`, `GetFace`, `TakeFacePicked`, `SetFaceLive`, then T64's `MakePreview`, `ChipClicked` and `OpenTurn` with T78's lines. Compile with warnings as errors, save.
3. `WBP_Stage` (part 3): the tree, the variables, the new functions (`FaceInit`, `FacePlace`, `FaceShow`, `FaceClick`, `SyncFace`, `FaceTake`), the edits (`SetPrompt`, `SetPrepMode`, `FitBuilder`, `AtDraw`, `SpeechKey`), the event chain. Compile, save.
4. `BP_Show` (part 5): `HFace`, `FaceOut`, `TakeFace`, `ApplyFace`, then the four sends and `HumanFeels`. Compile, save.
5. The check (part 6).

Batch the writes with `ProgrammaticToolset.execute_tool_script` and `AssetTools.read_file` (T33), a few per call, so each call stays under 100 s. Close every game window before you save (T53, T63).

## 2. `WBP_ActionBuilder`: the pick, the list's chips and the preview

### 2a. New variables

| Variable | Type | Default | Used by |
|---|---|---|---|
| `FaceIds`, `FaceWords` | String array | empty | `LoadFaces`, `FaceWord`, `BuildFaces`, `PickFace` |
| `FaceList` | the type of T75's `EmList` in `BP_Robot` (a JSON object array) | empty | `LoadFaces` |
| `Face` | String | "" (Auto) | everywhere |
| `TmpId`, `TmpWord` | String | "" | `LoadFaces` |
| `FacesLoaded`, `FacePicked`, `FaceLive` | Boolean | false | `LoadFaces` / `PickFace`, `TakeFacePicked` / `PickFace`, `SetFaceLive` |

`TmpK` is T65's (Integer).

### 2b. New functions

| Function | Inputs | Outputs | Called by |
|---|---|---|---|
| `LoadFaces` | — | — | `BuildFaces`, `WBP_Stage.FaceInit` |
| `FaceWord` | `Id` (String) | String | `FaceLabel`, `FacePhrase` |
| `FaceLabel`, `FacePhrase` | — | String | `WBP_Stage.SyncFace` / `MakePreview` |
| `AddFaceChip` | `Index` (Integer), `Label` (String), `Picked` (Boolean), `Wrap` (`WrapBox` object reference) | — | `BuildFaces` |
| `BuildFaces` | `Wrap` (`WrapBox` object reference) | Integer | `WBP_Stage.FaceShow` |
| `PickFace` | `K` (Integer) | — | `ChipClicked` |
| `ResetFace` | — | — | `OpenTurn`, `WBP_Stage.SyncFace`, `WBP_Stage.SetPrepMode` |
| `GetFace` | — | String | `WBP_Stage.FaceTake` |
| `TakeFacePicked` | — | Boolean | `WBP_Stage.SyncFace` |
| `SetFaceLive` | `On` (Boolean) | — | `WBP_Stage.SyncFace` |

`Graphs/WBP_ActionBuilder/LoadFaces.txt` (T75's `LoadEmotes` form, in `Graphs/BP_Robot/LoadEmotes.txt`; use the JSON nodes and the `EmList` type that file shows):

```lisp
; T78: the emotions I can pick, read once from emotes.json (T75), in its order. The list comes from the file, so an
; emotion added there shows in the list with no widget change. Each shows by its word; neutral's word is empty, so it
; shows as "calm". With no file, the list holds only Auto.
(fn LoadFaces ()
  (if (V FacesLoaded)
    (return))
  (set FacesLoaded true)
  (clear (V FaceIds))
  (clear (V FaceWords))
  (bind (_o _ok) (Json|LoadJsonfromFile (Utilities|Struct|MakeFilePath (cat (Utilities|Paths|GetProjectContentDirectory) "NHOS/Data/emotes.json"))))
  (if (not _ok)
    (print "NHOS: FACE emotes.json missing or not valid JSON: only Auto")
    (return))
  (bind _l (Json|GetField _o "emotes"))
  (set FaceList _l)
  (for _e (V FaceList)
    (bind _id (Json|GetField _e "id"))
    (set TmpId _id)
    (bind _wd (Json|GetField _e "word"))
    (set TmpWord _wd)
    (add (V FaceIds) (V TmpId))
    (add (V FaceWords) (select (Utilities|String|IsEmpty (V TmpWord)) "calm" (V TmpWord))))
  (print (cat "NHOS: FACE loaded " (str (len (V FaceIds))) " emotions")))
```

- If a `bind` inside the loop doesn't work (T51), move the two `GetField`s into a helper that takes `_e`, as T65's `MakeWord` does for its create. (T77's `LoadEmos` in `BP_Show` uses the same loop, so whichever form T77 found to work is the one to copy.)

`FaceWord.txt`:

```lisp
; T78: the word for an emotion id (calm for neutral); the id itself if the list doesn't have it.
(fn FaceWord (Id)
  (bind _k (Utilities|Array|FindItem (V FaceIds) Id))
  (if (< _k 0)
    (return Id))
  (return (get (V FaceWords) _k)))
```

`FaceLabel.txt`:

```lisp
; T78: the chip's text (step 1): "Face: Auto", or "Face: <word>" once I pick.
(fn FaceLabel ()
  (if (Utilities|String|IsEmpty (V Face))
    (return "Face: Auto"))
  (bind _w (CallFunction|FaceWord :Id (V Face)))
  (return (cat "Face: " _w)))
```

`FacePhrase.txt`:

```lisp
; T78: the pick in the preview line's words ("looks worried"); nothing for Auto (step 5).
(fn FacePhrase ()
  (if (Utilities|String|IsEmpty (V Face))
    (return ""))
  (bind _w (CallFunction|FaceWord :Id (V Face)))
  (return (cat "looks " _w)))
```

`AddFaceChip.txt` (the form of T64's `AddChip`):

```lisp
; T78: one entry of the face list, a T64 chip in the pop-up's WrapBox (WBP_Stage's FaceWrap). Its Index is 1000 for Auto
; and 1001 + k for emotion k, so ChipClicked tells it from the action chips (their place in Choices). No seat bar.
(fn AddFaceChip (Index Label Picked Wrap)
  (bind _chip (UserInterface|CreateWidget "/Game/NHOS/UI/WBP_Chip.WBP_Chip_C" (Widget|GetOwningPlayer self)))
  (Class|WBPChip|Setup :self _chip :Owner self :Index Index :Label Label :Actor false :Picked Picked)
  (Panel|AddChildtoWrapBox :self Wrap :Content _chip))
```

`BuildFaces.txt`:

```lisp
; T78: the face list, made again each time it opens (13 chips): Auto, then each emotion by its word. The current pick is
; paper. Returns how many entries it made.
(fn BuildFaces (Wrap)
  (CallFunction|LoadFaces)
  (Widget|Panel|ClearChildren :self Wrap)
  (CallFunction|AddFaceChip :Index 1000 :Label "Auto" :Picked (Utilities|String|IsEmpty (V Face)) :Wrap Wrap)
  (for _k (range (len (V FaceIds)))
    (set TmpK _k)
    (CallFunction|AddFaceChip :Index (+ 1001 (V TmpK)) :Label (get (V FaceWords) (V TmpK)) :Picked (streq (get (V FaceIds) (V TmpK)) (V Face)) :Wrap Wrap))
  (return (+ 1 (len (V FaceIds)))))
```

`PickFace.txt`:

```lisp
; T78: an entry of the face list was clicked: K is -1 for Auto, else the emotion's place in FaceIds. Only while my input
; is open (SetFaceLive). WBP_Stage closes the list (TakeFacePicked). In my scene turn the preview line follows at once.
; The keyboard focus goes back to the speech field (T64's KeepFocus; ChipClicked's face branch returns before its own).
(fn PickFace (K)
  (if (not (V FaceLive))
    (return))
  (set Face "")
  (if (and (>= K 0) (< K (len (V FaceIds))))
    (set Face (get (V FaceIds) K)))
  (set FacePicked true)
  (bind _p (CallFunction|MakePreview))
  (print (cat "NHOS: FACE pick " (select (Utilities|String|IsEmpty (V Face)) "auto" (V Face)) (select (V Armed) (cat " | " _p) "")))
  (if (and (V Armed) (not (V Sent)))
    (CallFunction|Refresh))
  (CallFunction|KeepFocus))
```

- The `get` runs only inside the `if`, once `K` is known to be in range. A `select` would read index -1 too and print a `LogScript` warning (T64, `PreviewName`).
- The `if`s after the early return are top-level, so they join (T30's rule is about else paths).

`ResetFace.txt`:

```lisp
; T78: back to Auto at the start of each of my turns (step 4), so a pick never sticks by accident. Prints only when it
; clears a pick.
(fn ResetFace ()
  (if (Utilities|String|IsEmpty (V Face))
    (return))
  (set Face "")
  (print "NHOS: FACE reset")
  (if (and (V Armed) (not (V Sent)))
    (CallFunction|Refresh)))
```

`GetFace.txt`, `TakeFacePicked.txt`, `SetFaceLive.txt`:

```lisp
; T78: the pick as it stands: an id from emotes.json, or "" for Auto. BP_Show reads it at each send (WBP_Stage.FaceTake).
(fn GetFace ()
  (return (V Face)))
```

```lisp
; T78: true once after a pick, so WBP_Stage closes the list.
(fn TakeFacePicked ()
  (if (not (V FacePicked))
    (return false))
  (set FacePicked false)
  (return true))
```

```lisp
; T78: WBP_Stage says when my input opens and closes. A pick counts only while it is open.
(fn SetFaceLive (On)
  (set FaceLive On))
```

### 2c. T64's files, each with one change

**`ChipClicked.txt`:** a new first statement, before T64's `  (if (or (not (V Armed)) (V Sent))` / `    (return))`, because the face list works when the builder isn't armed (Free Talk, the reactions):

```lisp
  ; T78: an entry of the face list (Index 1000 and up), in any phase where I speak.
  (if (>= Index 1000)
    (CallFunction|PickFace :K (- Index 1001))
    (return))
```

Header: `; T78: the face list's chips (Index 1000 and up) go to PickFace.` The action chips' indexes are their places in `Choices` (T64's `AddChip`), well under 1000.

**`MakePreview.txt`** (T64's preview line; T65's `DrawPreview` draws it word by word): the pick goes before the action. Add these lines after the last `(if (streq (V Verb) "give") ...)` and before `  (if (Utilities|String|IsEmpty (V Line))`:

```lisp
  ; T78: a picked face comes first, in words: "> looks worried · throw rose at @Meta: \"Oops.\"". Auto adds nothing.
  (bind _fp (CallFunction|FacePhrase))
  (if (not (Utilities|String|IsEmpty _fp))
    (set TmpStr (cat _fp " · " (V TmpStr))))
```

- A top-level `if` with no early return before it, so it joins the two returning `if`s after it.
- **`·` (U+00B7) must reach the asset as one character.** The mono font (`MonoFont`, the engine's Droid Sans Mono) draws it. If the write turns it into something else (T01: escapes come through as written), use `-` instead and write that under "Findings".
- `DrawPreview` splits on spaces (`ParseIntoArray`), so "looks", "worried" and "·" become plain words, and only the @ mention is a chip (T65's `DrawToken`).
- T64's `PickLine` prints the preview, so `NHOS: BUILDER pick` shows the face too.
- Header: `; T78: a picked face leads the preview line (FacePhrase).`

**`OpenTurn.txt`:** after T64's `  (set Sent false)`, add `  (CallFunction|ResetFace)`, so the builder never opens showing the last turn's pick before my input opens. Header: `; T78: a scene turn opens at Auto (ResetFace).`

Compile with warnings as errors, save.

## 3. `WBP_Stage`: the chip, its list and the row

### 3a. The widget tree

1. **The chip**, as `InputRow`'s **first** child, before `InputStack`:

```
FaceSize    SizeBox; MinDesiredWidth 150; slot: VAlign Center, padding right = the row's gap (T28: 10); Collapsed at design time
└ FaceBtn   Button; IsFocusable off; bIsEnabled off at design time
  └ FaceLabel   TextBlock; text "Face: Auto"
```

   - 150 px holds "Face: Auto" with the button's side padding (T32), so the field doesn't move when I pick a short word. A long word ("Face: embarrassed", about 210 px) makes the chip wider and the field narrower while the pick lasts.
   - `bIsVariable` on for all three.
   - At 1080 px (part 3d), the row in a reaction is: chip 150, field about 500, counter 72, Action!, Pass, timer 72. Measure it in run A (step 11) and write the field's width under "Findings".

2. **The list**, as `RootBox`'s **last** child, after T65's `AtPop`, so it draws on top:

```
FacePop       Border; slot: HAlign Left, VAlign Bottom, padding set at run time (FacePlace); Collapsed at design time
└ FaceWrapSize   SizeBox; WidthOverride 560
  └ FaceWrap     WrapBox; InnerSlotPadding (8, 8) (S2); the chips go here at run time (WBP_Chip, from the builder)
```

   `bIsVariable` on for `FacePop` and `FaceWrap`. `FacePop` is styled as T65's `AtPop` is (`StylePanel(..., "Ink")` in `AtLists`, padding 8).

### 3b. New variables

`FaceOpen`, `FaceRowOn`, `FaceWasOpen`, `FaceShownV`, `FaceReady` (Boolean, false); `LastFaceLbl` (String, "").

### 3c. New functions

`Graphs/WBP_Stage/FaceInit.txt`:

```lisp
; T78: once: the emotions from emotes.json, the list's ink panel, the chip's tooltip.
(fn FaceInit ()
  (if (V FaceReady)
    (return))
  (set FaceReady true)
  (Class|WBPActionBuilder|LoadFaces :self (Variables|WBP_Stage|GetActionBuilder))
  (Class|UIStyle|StylePanel :Panel (Variables|WBP_Stage|GetFacePop) :Look "Ink")
  (Widget|SetToolTipText :self (Variables|WBP_Stage|GetFaceBtn) :InToolTipText (Utilities|Text|ToText(String) "The face your robot shows with this line. Auto: the game reads it from your words.")))
```

`FacePlace.txt` (T65's `AtPlace`, with the chip in place of the field):

```lisp
; T78: puts the face list right over the chip, in RootBox's space: its left edge on the chip's, its bottom 8 px (S2) above
; the chip's top. The point transforms are the (Coordinates) nodes (T65).
(fn FacePlace ()
  (bind _g (Widget|GetCachedGeometry :self (Variables|WBP_Stage|GetFaceBtn)))
  (bind _rg (Widget|GetCachedGeometry :self (Variables|WBP_Stage|GetRootBox)))
  (bind _abs (UserInterface|Geometry|LocaltoAbsolute(Coordinates) _g (Math|Vector2D|MakeVector2D :X 0.0 :Y 0.0)))
  (bind _tl (UserInterface|Geometry|AbsolutetoLocal(Coordinates) _rg _abs))
  (bind _view (UserInterface|Geometry|GetLocalSize _rg))
  (bind _gap (Class|UIStyle|UISize :Role "S2"))
  (bind (_x _y) (Math|Vector2D|BreakVector2D _tl))
  (bind (_vx _vy) (Math|Vector2D|BreakVector2D _view))
  (bind _slot (Slot|SlotasOverlaySlot (Variables|WBP_Stage|GetFacePop)))
  (Layout|OverlaySlot|SetPadding :self _slot :InPadding (Utilities|Struct|MakeMargin :Left _x :Top 0.0 :Right 0.0 :Bottom (+ (- _vy _y) _gap))))
```

`FaceShow.txt` (input `Open`: Boolean):

```lisp
; T78: opens or closes the face list. Opening closes T65's @ list, so the two pop-ups never overlap. FaceOpen is read
; before it is set, as AtDraw reads AtOpen (a bind of a variable is read where it is used, T65).
(fn FaceShow (Open)
  (if Open
    (CallFunction|AtDraw :Open false)
    (bind _n (Class|WBPActionBuilder|BuildFaces :self (Variables|WBP_Stage|GetActionBuilder) :Wrap (Variables|WBP_Stage|GetFaceWrap)))
    (CallFunction|FacePlace)
    (Widget|SetVisibility :self (Variables|WBP_Stage|GetFacePop) :InVisibility "SelfHitTestInvisible")
    (print (cat "NHOS: FACE list " (str _n)))
    (else
      (Widget|SetVisibility :self (Variables|WBP_Stage|GetFacePop) :InVisibility "Collapsed")
      (if (V FaceOpen)
        (print "NHOS: FACE close"))))
  (set FaceOpen Open))
```

`FaceClick.txt`:

```lisp
; T78: the chip toggles its list, only while I can type.
(fn FaceClick ()
  (if (not (Variables|Default|GetLastCanType))
    (return))
  (CallFunction|FaceShow :Open (not (V FaceOpen))))
```

`SyncFace.txt` (input `CanType`: Boolean):

```lisp
; T78: the chip, once a frame from SetPrompt. When my input opens (CanType rises), the pick goes back to Auto (step 4)
; and the chip turns on; when it closes, the chip turns off and its list closes. A pick closes the list. The chip shows
; on the play side but not in the vote (FaceRowOn, VoteRow), and reads the builder's label, in paper after a pick.
; FaceWasOpen is its own copy of CanType, apart from LastCanType, so the order inside SetPrompt doesn't matter. Each
; branch sets it itself: a bound "rise" would be read after the set and see the new value (T65, T66's TickTimer).
(fn SyncFace (CanType)
  (CallFunction|FaceInit)
  (if (and CanType (not (V FaceWasOpen)))
    (set FaceWasOpen true)
    (Class|WBPActionBuilder|ResetFace :self (Variables|WBP_Stage|GetActionBuilder))
    (Class|WBPActionBuilder|SetFaceLive :self (Variables|WBP_Stage|GetActionBuilder) :On true)
    (Widget|SetIsEnabled :self (Variables|WBP_Stage|GetFaceBtn) :bInIsEnabled true))
  (if (and (not CanType) (V FaceWasOpen))
    (set FaceWasOpen false)
    (Class|WBPActionBuilder|SetFaceLive :self (Variables|WBP_Stage|GetActionBuilder) :On false)
    (Widget|SetIsEnabled :self (Variables|WBP_Stage|GetFaceBtn) :bInIsEnabled false)
    (CallFunction|FaceShow :Open false))
  (bind _pk (Class|WBPActionBuilder|TakeFacePicked :self (Variables|WBP_Stage|GetActionBuilder)))
  (if _pk
    (CallFunction|FaceShow :Open false))
  (bind _show (and (V FaceRowOn) (not (Widget|IsVisible :self (Variables|WBP_Stage|GetVoteRow)))))
  (if (xor _show (V FaceShownV))
    (set FaceShownV _show)
    (if _show
      (Widget|SetVisibility :self (Variables|WBP_Stage|GetFaceSize) :InVisibility "Visible")
      (else
        (Widget|SetVisibility :self (Variables|WBP_Stage|GetFaceSize) :InVisibility "Collapsed")
        (CallFunction|FaceShow :Open false))))
  (bind _lbl (Class|WBPActionBuilder|FaceLabel :self (Variables|WBP_Stage|GetActionBuilder)))
  (if (not (streq _lbl (V LastFaceLbl)))
    (set LastFaceLbl _lbl)
    (Class|UIStyle|StyleButton :Button (Variables|WBP_Stage|GetFaceBtn) :Label (Variables|WBP_Stage|GetFaceLabel) :Kind (select (streq _lbl "Face: Auto") "Secondary" "Paper"))
    (Class|Text|SetText :self (Variables|WBP_Stage|GetFaceLabel) :Text (Utilities|Text|ToText(String) _lbl))))
```

- No `if` returns, so each joins the next.
- `_show` is a pure expression of `FaceRowOn` and the vote row, neither of which changes inside the function, so reading it after `(set FaceShownV _show)` is safe. `_pk` and `_lbl` are outputs of impure calls, read once.
- The style and the text change only when the label does, so a tooltip on screen doesn't flicker (T64's `SyncAction`).
- `LastFaceLbl` starts "", so the first frame styles the chip.
- With autoplay, my input never opens, so the chip stays off at "Face: Auto".

`FaceTake.txt` (output String):

```lisp
; T78: the chip as it stands, for BP_Show.TakeFace at each of my sends: an emotion id, or "" for Auto.
(fn FaceTake ()
  (bind _f (Class|WBPActionBuilder|GetFace :self (Variables|WBP_Stage|GetActionBuilder)))
  (return _f))
```

### 3d. Edits to T64's, T65's and T66's files

Each file is the one T66 pushed (re-check 2). Add each line by the text it follows.

| File | Change |
|---|---|
| `SetPrompt.txt` | After T66's last line `  (CallFunction|TickTimer :CanType CanType))` (move the closing parenthesis), add `  (CallFunction|SyncFace :CanType CanType))`. Header: `; T78: the face chip follows my input (SyncFace).` **Re-check after T66.** |
| `FitBuilder.txt` | T66's width line `  (bind _wide (or _on (V TimerWide)))` becomes `  (bind _wide (or _on (or (V TimerWide) (V FaceRowOn))))`. The chat height (`FitOn`, `_on`) stays T64's. Header: `; T78: the panel is wide on the whole play side too (FaceRowOn), so the face chip fits (my person's answer); the chat shortens only with the builder.` **Re-check after T66:** if T66 didn't split the width out, change T64's `(select _on (V LowerWideBuild) (V LowerWide))` to `(select (or _on (V FaceRowOn)) ...)` instead. |
| `SetPrepMode.txt` | **Prep branch**, after T66's `    (set TimerWide false)` and before T64's `(Class|WBPActionBuilder|Close ...)`: `(set FaceRowOn false)`, `(set FaceShownV false)`, `(Widget|SetVisibility :self (Variables|WBP_Stage|GetFaceSize) :InVisibility "Collapsed")`, `(CallFunction|FaceShow :Open false)`, `(Class|WBPActionBuilder|ResetFace :self (Variables|WBP_Stage|GetActionBuilder))`. **Else branch**, at its end (after T65's `SyncCount`): `(set FaceRowOn true)` and `(CallFunction|FitBuilder)`. Header: `; T78: the face chip's row is the play side; Scene Prep hides it and gives the panel back 640.` **Re-check after T66.** |
| `AtDraw.txt` | In the `Open` branch, before `    (CallFunction|AtShow :Fresh (not (V AtOpen)))`: `(if (V FaceOpen) (CallFunction|FaceShow :Open false))`. Header: `; T78: the @ list closes the face list.` |
| `SpeechKey.txt` | After T65's Escape block `  (if (and (V AtOpen) (streq Key "Escape"))` ... `    (return true))`, add: `(if (and (V FaceOpen) (streq Key "Escape")) (CallFunction|FaceShow :Open false) (return true))`. Header: `; T78: Escape closes the face list too.` |

- **`FitBuilder` widens the panel at the scene's start:** `SetPrepMode(false)` runs right before `StartScene` (T64), and the panel stays 1080 until the next Scene Prep (decision 2). T66's `ShapeRow` sets `TimerWide` false at each header, but `FaceRowOn` stays true, so the width doesn't change.
- **`AtDraw` and `FaceShow` don't loop:** `FaceShow(true)` calls `AtDraw(false)`, which never calls `FaceShow`. `AtDraw(true)` calls `FaceShow(false)`, which only calls `AtDraw` when it opens.
- If T66 left `SetPrompt` ending in another line, put `SyncFace` last anyway.
- `SetPhase` doesn't change (T66 adds `ShapeRow` there; the chip needs nothing at a header).

### 3e. The event chain

Bind `FaceBtn`'s `OnClicked` with `UMGToolSet.BindToEventProperty` (T04), then write `Graphs/WBP_Stage/EventGraph.Face.txt`:

```lisp
; Only the face chip's chain of WBP_Stage's EventGraph (T78). A click opens or closes the face list.
(event OnClicked(FaceBtn)
  (CallFunction|FaceClick))
```

`write_graph_dsl` keeps the chains it doesn't name (`EventGraph.StartButton.txt`'s note; T64's `EventGraph.Builder.txt` and T65's `EventGraph.Mentions.txt` are written the same way). Compile `WBP_Stage` with warnings as errors, save.

## 4. What the row looks like in each phase (step 2)

As T64, T65 and T66 leave the row, with T78's chip:

| Phase | Chip | Panel | Pass | Timer (T66) | Preview line |
|---|---|---|---|---|---|
| Scene Prep | hidden | 640 × 380 | hidden | hidden | — |
| My scene turn | first in the row; on while I can type | 1080, chat 380 minus the builder (T64) | hidden (T66's `ShapeRow`) | `scene`, 30 s | `> looks <word> · <action>: "<line>"` with a pick, T64's line with Auto |
| Free Talk, my line | first in the row; on while I can type | 1080 (T78), chat 380 | shown, enabled | none (`free_talk` 0) | none (the chip's label shows the pick) |
| My last word | first in the row; on while I can type | 1080 (T66 and T78), chat 380 | shown, enabled | `last_word`, 15 s | none |
| The Cut, my vote | hidden (decision 4) | 1080 (T78, decision 2), chat 380 | shown, disabled | none | none |
| My reaction | first in the row; on while I can type | 1080 (T66 and T78), chat 380 | shown, enabled | `reaction`, 15 s | none |

Others' turns in every play phase: the chip shows, off ("Face: Auto", 40%), so the row doesn't shift when my turn opens.

## 5. `BP_Show`: my sends carry the pick

### 5a. New variables

`HFace`, `FaceOut` (String, "").

### 5b. New functions

`Graphs/BP_Show/TakeFace.txt`:

```lisp
; T78: each of my sends starts here (SendHumanTurn, SendHumanTalk, SendHumanReact, SendHumanVote): the face chip as it
; stands goes with the turn. A timeout sends the chip as it stands too (T66's TimeUp reaches the same sends). Autoplay's
; sends read Auto, since my input never opens. ApplyFace uses it once and clears it.
(fn TakeFace ()
  (bind _f (Class|WBPStage|FaceTake :self (Variables|Default|GetStage)))
  (set HFace _f))
```

`Graphs/BP_Show/ApplyFace.txt` (inputs `AutoId`, `AutoFrom`: String; outputs `Id`, `From`: String, made in that order):

```lisp
; T78: T77's HumanFeels calls this with the emotion T77 picked (the input LLM's, the keyword table's, or neutral for a
; pass or no words) and where it came from. A pick on the chip overrides it, for a pass and a silent turn too (the
; reason to pick one). Used once: HFace is cleared, so a pick never reaches a later line.
(fn ApplyFace (AutoId AutoFrom)
  (set FaceOut (V HFace))
  (set HFace "")
  (if (Utilities|String|IsEmpty (V FaceOut))
    (return AutoId AutoFrom))
  (return (V FaceOut) "pick"))
```

- `FaceOut` is set before `HFace` is cleared. A `bind` of `(V HFace)` would be read after the clear and give "" (T65).
- `(return a b)` fills the outputs in the order they were made (T64-build part 2c; T66's `TimerFor` returns two the same way).

### 5c. Where they are called

1. **The four sends** (T63's files): in each of `Graphs/BP_Show/SendHumanTurn.txt`, `SendHumanTalk.txt`, `SendHumanReact.txt` and `SendHumanVote.txt`, right after its first line `  (set HumanSent true)`, add `  (CallFunction|TakeFace)`, with the header `; T78: the face chip goes with the turn (TakeFace).`
   - In `SendHumanTalk` and `SendHumanReact` it comes before the "pass" branch, so a pass carries the pick (decision 5). My last word goes through `SendHumanTalk` (T58).
   - `AutoTurn` calls `SendHumanTurn` too and gets Auto.
   - In the vote the chip is hidden and was reset when my input opened, so `SendHumanVote` takes "", which stops a pick from an earlier line from reaching the vote.
2. **T77's emotion step, `Graphs/BP_Show/HumanFeels.txt`:** T77 writes it as
   ```lisp
   (fn HumanFeels (Id From)
     (print (cat "NHOS: HUMAN emotion=" Id " from=" From))
     (return Id))
   ```
   Make it:
   ```lisp
   ; T78: a pick on the face chip overrides T77's pick (ApplyFace); from=pick.
   (fn HumanFeels (Id From)
     (bind (_fid _ffrom) (CallFunction|ApplyFace :AutoId Id :AutoFrom From))
     (print (cat "NHOS: HUMAN emotion=" _fid " from=" _ffrom))
     (return _fid))
   ```
   - `ApplyFace` is an impure call, so `_fid` and `_ffrom` are read once, at the call.
   - Both of T77's callers (`HumanEmo` for a line through `SpellAsk`, `TakeEmo` for a pass) take the return value into T77's carrier (`HEmo` → `KeepEmo` → `SeatEmo[HumanSeat]`, or straight to `ActorLine`), so the carrier needs no change.
   - **Timing:** `HumanEmo` runs in `HumanSay`, when my line's spelling reply is in (up to `spelling_wait`, 4 s, after the send); `TakeEmo` runs at once for a pass. Nothing else of mine is sent in between (T63: the logic waits for my line, and `HumanSent` closes my input), so `HFace` is still the one that send set.

Compile `BP_Show` with warnings as errors. The editor log after the compile has no `LogBlueprint: Error`. Close every game window before you save (T53).

## 6. The check

**Before the runs:** `Local/switches.json` in the repo folder with `"mode": "free"`, `"autoplay": false`, `"fast_lines": false`, `"ai_seats": 0`, **`"spare_human": true`** (so I'm never cut and get a reaction turn every scene, as in T66's check), `"force_tie": false`, `"emote_test": false` and `"analytics": "off"`. PIE in a floating window at 1600 × 900 (T63's `LevelEditorPlaySettings` rule: `newWindowWidth`, `newWindowHeight`, `newWindowPosition`; put them back after). Pick **Test for Free**. Screenshots with `SlateInspectorToolset.Screenshot` to `Saved/T78/shots/` (not in git). On the PC the Slate inspector's `Click` and `Type` land (T33). My scene turn has T66's 30 s timer: act within it, except in step 6.

### Run A: one show played by hand in PIE

1. **`face_auto.png`:** press Start the scene. At turn 1, once the lines stop: the chip "Face: Auto" first in the input row (plum), the field right of it, the panel 1080 wide. Read `FaceLabel`'s text through MCP: "Face: Auto". Log: `NHOS: FACE loaded 12 emotions` (or the count in `emotes.json`).
2. **The focus check:** click the field once, `Type` "Calm down", click the chip. **`face_list.png`:** the list over the chip, Auto in paper, then calm, happy, sad, ..., embarrassed. Nothing in the lower panel moved, and no robot or name tag is covered by anything but the list. Log: `NHOS: FACE list 13`. Click **worried**: the list closes, the chip reads "Face: worried" in paper. Log: `NHOS: FACE pick worried | > looks worried · stand still: "Calm down"`. `Type` ", everyone." Every letter lands in the field.
3. **`face_preview.png`:** the preview line reads `> looks worried · stand still: "Calm down, everyone."`. Click **Look around**: `> looks worried · look around: "Calm down, everyone."`.
4. Press **Action!**. Log, in order: `NHOS: BUILDER send around - - ready=yes`, then (after the spelling call) `NHOS: HUMAN around - - says=Calm down, everyone.`, `NHOS: HUMAN emotion=worried from=pick`. When my line plays: `NHOS: EMOTE <my seat> worried ...` (T75, T77). **`face_play.png`:** my robot's worried face while my line types out. Its `NHOS: ENTRY` line has `"feels":"worried"` (T77).
5. **Turn 2 starts at Auto:** when it opens, `NHOS: FACE reset` and the chip "Face: Auto" (read its text). The preview has no "looks". Type "sorry, my bad", pick No action, press Action!: `NHOS: HUMAN emotion=embarrassed from=llm` (T77's way: Test for Free's echo carries the keyword table's pick), **not** `from=pick`.
6. **Turn 3, a pick left to time out:** pick **smug**, type nothing, touch nothing else. At 0: `NHOS: TIMEOUT scene none`, `NHOS: HUMAN none - - says=-`, `NHOS: HUMAN emotion=smug from=pick` (decision 5: a silent turn shows the pick). My robot shows smug while it stands still.
7. **Escape and the @ list:** at a turn of mine, open the list and press Escape: `NHOS: FACE close`. Open it again, then type `@`: the @ list opens and the face list closes (`NHOS: FACE close`, then `NHOS: MENTION open ...`).
8. **`freetalk_face.png`:** my Free Talk line: no builder, the chip first in the row, the panel 1080 wide, the chat at its full height, Pass shown, no timer. Pick **suspicious**, type "Who moved the rose?", send: `NHOS: HUMAN emotion=suspicious from=pick`, and my robot shows suspicious when the line plays.
9. **A pass with a face:** at my next Free Talk line (or my last word), pick **confused** and press Pass: `NHOS: HUMAN emotion=confused from=pick`, and my robot shows confused next to T57's "passed" marker.
10. **`vote.png`:** the Cut's vote: the vote row, no chip, the panel still 1080.
11. **`reaction_face.png`:** my reaction: the chip at "Face: Auto" (reset), T66's timer. Pick **sad**, leave the field empty, let it time out: `NHOS: TIMEOUT reaction`, my reaction as a pass, `NHOS: HUMAN emotion=sad from=pick`.

Stop PIE. In every shot, check that no robot, name tag or thrown prop sits behind the lower panel (T27).

### Run B: a free autoplay show in a game window

`"autoplay": true`, `"fast_lines": true`, `"mode": "free"`, `"spare_human": false`. Use the game-window command from `CLAUDE.local.md` with `-log=T78auto.log`. In the log: `NHOS: SHOW END`, **no `LogScript` line** (above all no "Accessed None" and no "Attempted to access index"), **no `NHOS: FACE pick`** and **no `from=pick`**: autoplay's lines take T77's way. Close the game window by its `-log=` name.

### Run C: the checker

`python Tools/check_prompts.py --offline` passes. `python Tools/check_prompts.py --log Saved/Logs/T78auto.log` passes, and its `my emotions = {...}` (T77's count) has no `pick`.

**Afterward:** `autoplay`, `fast_lines` and `spare_human` back to false, the PIE window settings back, every game window closed.

### Findings to write in `T78.md`

- **My person's answer** to question 1 (above, with the 1080 note), and decisions 1 to 9 for my person to look over.
- **The reset (step 4):** judge, as a critical first-time player, whether I'd expect a pick to stay from one turn to the next. Look at `face_play.png` and the turn 2 shot: does a chip that goes back to "Face: Auto" read as "it's per line" or as "my pick was lost"? If a first-time player would expect it to stay, say so and ask my person (multiple-choice tool) before you close the task.
- **The design review** (the Done-when's last line), from the shots: is the chip easy to find, does "Face:" say what it does, does it crowd the input row at 1080 px (the field's width in a reaction, with Pass and the timer), and does the list read as "pick a face". List anything for T34 (the row's polish).
- The file edits in the four sends and in T77's `HumanFeels`.
- Whether `·` reached the preview line, or `-` replaced it (part 2c).
- **Unreal MCP rules found in this task**, as earlier tasks do.

## 7. The design doc (tell, don't change)

T78's Touches don't name the design doc. Read it with the Claude Docs connector, propose each fix to my person in the doc's words, and edit only after their OK (the plan's "The design doc follows the game"):

- **Rules tab, "Emotions" (T76's section, rev 49), bullet 4:** "Your robot shows emotions too, or one blank face would give you away. The game picks yours from your line, unless you pick it yourself before you send." It matches what T78 builds. Propose adding: "The Face chip in your input row picks it for one line; it goes back to Auto each turn."
- **Turn Input tab (rev 5):** it has no Face chip. Propose, in "Layout", that the speech row reads "the Face chip, the speech field with its word counter, the Action! button and the turn timer", the layout block's last line starting `[Face: Auto]  Say something (optional)...`, and in "Saying a line" a bullet: "A Face chip, first in the row: Auto, or the emotion your robot shows with this line. It goes back to Auto each turn." "Other phases" can add that the chip shows in Free Talk, the last word and the reactions too.

## 8. The commit

One commit, `T78: I can pick my robot's emotion`: `Content/NHOS/UI/WBP_ActionBuilder.uasset`, `Content/NHOS/UI/WBP_Stage.uasset`, `Content/NHOS/Core/BP_Show.uasset`; `Graphs/WBP_ActionBuilder/` (new: `LoadFaces`, `FaceWord`, `FaceLabel`, `FacePhrase`, `AddFaceChip`, `BuildFaces`, `PickFace`, `ResetFace`, `GetFace`, `TakeFacePicked`, `SetFaceLive`; changed: `MakePreview`, `ChipClicked`, `OpenTurn`), `Graphs/WBP_Stage/` (new: `FaceInit`, `FacePlace`, `FaceShow`, `FaceClick`, `SyncFace`, `FaceTake`, `EventGraph.Face`; changed: `SetPrompt`, `FitBuilder`, `SetPrepMode`, `AtDraw`, `SpeechKey`), `Graphs/BP_Show/` (new: `TakeFace`, `ApplyFace`; changed: `SendHumanTurn`, `SendHumanTalk`, `SendHumanReact`, `SendHumanVote`, `HumanFeels`); `Docs/tasks/T78.md` (Result, Findings), `Docs/Plan.md` (the box, the "Next up" line), `Docs/DevLog.md`. If part 7 changed the design doc, say so in the message. Stage by path. Unlock the three assets after the push.

## 9. Knock-on: tell, don't change

- **T34** (the input row's polish): the chip's place (first in the row), its 150 px minimum, paper for a pick, and the panel at 1080 on the whole play side (decision 2) are its to revisit. `T34-build.md` part 3 says "the lower panel at 1000"; it is 1080 as built. The chip and the list never take keyboard focus, on purpose.
- **T38 (the rest: the chat button and hidden chat):** if its `ChatButton` goes in `InputRow`, the chip stays first; the row's final width is T34's.
- **T84** (Scene Prep's middle panel): its step 2 keeps the panel clear of "the lower panel at the width T78 left it": 640 in Scene Prep (T78 gives the panel 1080 only on the play side), and 1080 from the scene's start. Its step 4 changes `SetPrepMode`, which T78 also edits (part 3d); whichever comes second keeps the other's lines.
- **T85** (the cast's hover card): it must keep clear of the face list (`FacePop`, over the chip at the bottom left) as it keeps clear of T84's panel.
- **T61** (the stagehand): a tip at the first scene turn can point at the chip: "Pick your robot's face, or leave it on Auto." (`T61.md` notes it isn't in the doc's table, so adding it is a doc edit first.)
- **`Docs/ItchPage.md`, "Controls":** one line after T78: "**Face:** pick the face your robot shows with your line, or leave it on Auto and the game picks one from your words."
- **T70:** the chip is worth a second in the gameplay video (a pick, then the face on stage).
