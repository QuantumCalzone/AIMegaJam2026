# T78 build sheet: I can pick my robot's emotion

Back to [T78](T78.md). A PC prep session wrote this on 2026-11-15, without the editor, against **`noHumansOnSet` at `61199ce`** (T71 on top of the T76 and T47 sheets). It is a plan, not a record: nothing here was written to the editor. When T78 writes a graph, its source goes to `Graphs/` as usual.

It is written for `WBP_ActionBuilder`, `WBP_Stage` and `BP_Show` **as T63, T64, T65, T66, T75 and T77 leave them**. None of them had been built. This sheet was written from their build sheets: [T63-build.md](T63-build.md) (the sends), [T64-build.md](T64-build.md) (the builder, `WBP_Chip`, the preview line), [T65-build.md](T65-build.md) (the speech row, `AtDraw`, `SpeechKey`, the preview drawn word by word), [T66-build.md](T66-build.md) (the timer, `ShapeRow`, the row in each phase) and [T75-build.md](T75-build.md) (`emotes.json`). **T77's build sheet was not written yet.** This sheet uses [T77.md](T77.md) for it, so check item 1 of part 0 against T77's sheet and what T77 built.

Each place is named by its text first. Find each line by its text before you change it.

**Sources read:** `T78.md` and its plan entry; `T77.md` and its plan entry; the T63 (parts 5 and 8), T64 (all), T65 (decisions, parts 2, 4, 5 and 6), T66 (all), T75 (part 1 and `LoadEmotes`) and T76 (the doc edit 1a, part 9) build sheets; `Graphs/WBP_Stage/` and `Graphs/UIStyle/StyleButton.txt` at `61199ce`. The design doc was not read: T76 adds the Rules tab's "Emotions" section, and T78 checks it (part 7).

## Re-check before you write anything

T78 builds on five tasks that weren't built when this sheet was written. Before you write anything, compare each point below with what was pushed. Where one differs, follow what was built and change this sheet's part to match.

1. **T77: how my turn carries my emotion. This is the point to check most closely.** `Docs/tasks/T77-build.md` was being written by another session and wasn't on `origin/noHumansOnSet` when this sheet was pushed. Read it, `T77.md`'s Findings and T77's `Graphs/BP_Show/` files, and find:
   - **Where T77 settles my emotion.** That is where it prints `NHOS: HUMAN emotion=<id> from=<llm|keywords|none>`. This sheet calls that place **T77's emotion step**. Part 5c puts one `ApplyFace` call there. If T77 settles it in more than one place (for example `HumanSay` for a typed line and the "pass" branch of `SendHumanTalk` or `SendHumanReact` for a pass), put the call in each one.
   - **Whether a pass and an empty line go through that step** (T77 step 6: "If I say nothing ... my emotion is `neutral`"). They must, or a pick can't reach a pass (decision 5).
   - **What carries my emotion to the line** (a variable, an entry field or a `HandleReply` pin) and its name. `ApplyFace` returns an id. T78 changes only the value that goes into T77's carrier, not the carrier itself.
   - **The `from` values** T77 prints. T78 adds `pick`.
2. **T64:** `Graphs/WBP_ActionBuilder/` (`PreviewText`, `ChipClicked`, `OpenTurn`, `Refresh`, `Close`), `Graphs/WBP_Chip/Setup.txt` (inputs `Owner`, `Index`, `Label`, `Actor`, `Picked`; a click calls `Owner.ChipClicked(Index)`), and `Graphs/WBP_Stage/FitBuilder.txt`, `SetPrepMode.txt` and `SetPhase.txt`. Also T64's widget names: `ActionBuilder`, `SendButton`, `LowerSize`, `ChatSize`, and the variables `LowerWide` and `LowerWideBuild`.
3. **T65:** `InputRow`'s children and slot paddings (its Findings), `Graphs/WBP_Stage/AtDraw.txt`, `AtPlace.txt`, `SpeechKey.txt` and `SetPrompt.txt`, the variable `TmpK` in `WBP_ActionBuilder`, and whether T65 made the preview a `WrapBox` of `WBP_Word`s (`DrawPreview`). Part 2c's preview change goes into `PreviewText()` either way.
4. **T66:** `InputRow`'s last child (`TimerSize`), `SetPrompt.txt` ending with `TickTimer`, `SetPrepMode.txt`, `ShapeRow.txt` and `TimeUp.txt`. `TimeUp` must reach `HandleSend` → `SendHumanTurn` (scene) or `HandleSend` with "pass".
5. **T63:** `Graphs/BP_Show/SendHumanTurn.txt`, and T63's Findings for the node edits in `SendHumanTalk`, `SendHumanReact` and `SendHumanVote`. Each send must still start at its entry, with the "pass" branches after it (T63 part 5e.5).
6. **T75:** `Content/NHOS/Data/emotes.json`: the `emotes` list with `id` and `word`, `neutral` first with an empty word. Also `Graphs/BP_Robot/LoadEmotes.txt`: the JSON nodes that worked and the type of `EmList`. Part 2b copies them.
7. **T76's doc edit:** the Rules tab's "Emotions" section, bullet 4 (T76-build 1a): "The game picks yours from your line, unless you pick it yourself before you send." Part 7 checks it.

## In short

- **The chip goes first in the input row in every phase where I speak**, left of the speech field, so it is in the same place in my scene turns, Free Talk, the last word and the reactions. It is a `FaceBtn` button in `WBP_Stage`'s `InputRow` that reads **"Face: Auto"**, or "Face: worried" in paper (cream) after a pick. Its list is a pop-up over the chip (`FacePop`, like T65's @ list), so nothing on the screen moves.
- **The logic and the list's chips are in `WBP_ActionBuilder`** (part 2), as the task says: it reads `emotes.json` once, keeps the pick (`Face`), makes the list's chips as T64's `WBP_Chip`s, and writes the preview line. A chip in the list has an `Index` of 1000 or more, and T64's `ChipClicked` sends those to `PickFace`. `WBP_Chip` doesn't change.
- **The panel is 1000 wide on the whole play side** (my person's answer below). The chat keeps its 380 px outside my scene turns.
- **The preview line:** `> looks worried · throw rose at @Meta: "Oops."`. Auto adds nothing.
- **My sends carry the pick:** each of my four sends (`SendHumanTurn`, `SendHumanTalk`, `SendHumanReact`, `SendHumanVote`) starts with one new call, `BP_Show.TakeFace()`. It copies the chip as it stands into `HFace`. T77's emotion step calls `ApplyFace`: with a pick, my emotion is the pick and the print says `from=pick`; with Auto, T77's way stays.
- **Back to Auto each turn:** the chip resets when my input opens (`SetPrompt`'s `CanType` goes true) and when a scene turn's builder opens.
- **New check lines:** `NHOS: FACE loaded <n> emotions`, `NHOS: FACE list <n>`, `NHOS: FACE pick <id|auto>[ | <preview>]`, `NHOS: FACE close`, `NHOS: FACE reset`. T77's `NHOS: HUMAN emotion=<id> from=pick`.

## Questions for my person

The recommended answer is first.

**Answer (my person, 2026-11-15, to the prep session):** 1: **widen to 1000**, as recommended. Don't ask again; copy this answer under "Findings" in `T78.md`. The sheet is written for it.

1. **Room for the chip.** At 640 px, Free Talk, the last word and the reactions have no room for the chip: with the counter, Action!, Pass and the timer, the speech field shrinks to about 120 px. T64's answer kept the panel at 640 outside scene turns.
   - **Widen to 1000 wherever the chip shows (Recommended).** The chip stays in one place in every phase, and the panel's top doesn't move. The chat keeps its 380 px outside scene turns. The speech field stays about 450 px wide even with the timer. This changes T64's answer for Free Talk, the last word and the reactions only.
   - The chip in its own row above the input row: in scene turns next to the preview line, elsewhere in a face-only strip. The panel keeps 640, and the chat shortens by about 56 px.
   - Keep 640 with a short chip ("Auto", "worried", no "Face:"). The field is about 170 px in the last word and the reactions.

## Decisions this sheet makes (open to change)

My person asked prep sessions to take their own recommendation on design calls. The T78 session shows this list to my person when it closes the task.

1. **The chip is in the input row, the logic is in the builder.** The task puts the chip in `WBP_ActionBuilder`, but T64 collapses the builder outside my scene turns, and step 2 wants the chip in every phase where I speak. So the button and its pop-up are in `WBP_Stage`, and the builder keeps the pick, makes the list's chips and writes the preview. `WBP_Stage` reads the builder every frame (`SyncFace`), as T64's `SyncAction` does.
2. **The panel stays 1000 wide on the whole play side**, the vote included, and goes back to 640 only in Scene Prep. The chip hides in the vote (decision 4). A panel that narrowed for the vote and widened again for the reactions would jump twice in each scene. This goes a little past my person's answer ("wherever the chip shows"), so ask if it should narrow for the vote.
3. **The labels:** the chip reads "Face: Auto", or "Face: <word>" with the emotion's `word` from `emotes.json`. **Neutral is "calm"** (its `word` is empty; T76's Rules bullet 1 says "a calm neutral face"). The list reads "Auto", then each emotion's word in `emotes.json`'s order: calm, happy, sad, angry, worried, scared, surprised, confused, disgusted, suspicious, smug, embarrassed (T75's draft). A picked chip and the picked entry are paper; Auto is plum (Secondary), like T64's chips.
4. **The phases:** the chip shows in my scene turns, Free Talk (my last word is inside it, T58) and the reactions. It is enabled only while I can type (`CanType`), and hidden in the vote and in Scene Prep. Step 2 doesn't list the vote. With the chip hidden, a vote's face stays T77's way.
5. **A pick applies to a pass and to a turn with no words.** T77 gives those `neutral` (`from=none`). With a pick they show the pick (`from=pick`). That is why I would pick one: to say nothing and still look worried. T76's base prompt says the same to the bots ("A pass shows a face too").
6. **The list is a pop-up grid**, 560 px wide, about four rows of chips, over the chip, on an ink panel. It closes when I pick, click the chip again, press Escape, start an @ mention (T65's list), or when my input closes. It never takes keyboard focus: `FaceBtn` and every `WBP_Chip` have `IsFocusable` off, and T65's `HoldFocus` takes the focus back anyway.
7. **The chip has a tooltip:** "The face your robot shows with this line. Auto: the game reads it from your words."
8. **The reset prints only when it clears a pick** (`NHOS: FACE reset`), so a show without picks doesn't print it every turn.
9. **A pick changes only my emotion.** The input LLM still fixes my spelling (T63), and its `emotion` is ignored when I picked. The keyword table runs too, and T78 ignores its answer.

## Step coverage

| T78 step | Where |
|---|---|
| 1. The chip "Face: Auto", its list from `emotes.json` (Auto, then each word), styled from `UIStyle`, never focused | Part 2 (`LoadFaces`, `FaceWord`, `FaceLabel`, `BuildFaces`, `AddFaceChip`, `PickFace`), part 3 (`FaceBtn`, `FacePop`, `SyncFace`, `FaceShow`); decisions 1, 3 and 6 |
| 2. In every phase where I speak, in each phase's input row | Part 3 (`FaceBtn` first in `InputRow`; `SyncFace`'s shown rule; `FitBuilder` and `SetPrepMode`); decision 4 |
| 3. My sends carry the pick; Auto is T77's way; a pick overrides it and prints `from=pick` | Part 5 (`TakeFace` at each send, `ApplyFace` in T77's emotion step) |
| 4. Back to Auto each turn | Part 2 (`ResetFace`; T64's `OpenTurn`), part 3 (`SyncFace` on the rising `CanType`); part 6 Findings |
| 5. The timer sends the chip as it stands; the preview line shows a pick in words, nothing for Auto | Part 5 (`TimeUp` reaches the sends, which call `TakeFace`); part 2 (`PreviewText`, `FacePhrase`) |

## 0. Before you start (after T77 is pushed)

1. `git log --oneline -20` shows T63, T64, T65, T66, T75 and T77. `Docs/claims/T77` is released. `git lfs locks` shows no lock on `Content/NHOS/UI/WBP_ActionBuilder.uasset`, `Content/NHOS/UI/WBP_Stage.uasset` or `Content/NHOS/Core/BP_Show.uasset`. Claim T78 (`git lfs lock Docs/claims/T78`) and lock all three.
2. Do "Re-check before you write anything" above, and write what differs under "Findings".
3. `python Tools/check_prompts.py --offline` passes. T78 changes no data file.
4. **The survey** (each item a separate `call_tool`; calls stop at about 120 s; save each read to `Saved/T78/<name>.read.txt`; never write a read-back to the editor):
   1. **`WBP_Stage`'s tree:** `InputRow`'s children in order with their slot paddings (expected after T66: `InputStack`, `CountSize`, `SendButton`, `PassButton`, `ContinueButton`, `StartButton`, maybe T38's `ChatButton`, `TimerSize`); `RootBox`'s last children (T65's `AtPop`); and **`VoteRow`**: its name, whether it is a variable, and that it is `Visible` only while my vote is open (T09). `SyncFace` hides the chip while it shows. If the vote row stays up longer (while the votes are read), the chip hides then too, which is fine.
   2. **`WBP_ActionBuilder`'s variables:** `TmpK` (T65), `Armed`, `Sent`. The new names in part 2a must not exist yet.
   3. **`BP_Show`:** the four sends' entries (`SendHumanTurn`, `SendHumanTalk`, `SendHumanReact`, `SendHumanVote`) and the first node after each entry (`find_nodes`). Also T77's emotion step (re-check item 1) and the getter `Stage`. **Don't read `BP_Show`'s whole graphs.** `SendHumanTurn` has a file. Read only the starts of the other three.
   4. **Node names** with `find_node_types` (`context_pins: []`, T29): `Widget|IsVisible` in `WBP_Stage`; `Class|WBPStage|FaceTake` in `BP_Show` (after part 3 compiles); `Class|WBPActionBuilder|...` for each new builder function in `WBP_Stage` (after part 2 compiles).

## 1. The order of the build

T18 and T54: a call node goes stale when its function gets a new parameter. So create each function and its parameters first, compile, then write the graphs callee first.

1. Part 0.
2. `WBP_ActionBuilder` (part 2): the variables; every new function with its parameters, empty; compile. Then write `LoadFaces`, `FaceWord`, `FaceLabel`, `FacePhrase`, `AddFaceChip`, `BuildFaces`, `PickFace`, `ResetFace`, `GetFace`, `TakeFacePicked`, `SetFaceLive`, then T64's `PreviewText`, `ChipClicked` and `OpenTurn` with T78's lines. Compile with warnings as errors, save.
3. `WBP_Stage` (part 3): the tree, the variables, the new functions (`FaceInit`, `FacePlace`, `FaceShow`, `FaceClick`, `SyncFace`, `FaceTake`), the edits (`SetPrompt`, `SetPrepMode`, `FitBuilder`, `AtDraw`, `SpeechKey`), the event chain. Compile, save.
4. `BP_Show` (part 5): `HFace`, `FaceOut`, `TakeFace`, `ApplyFace`, `SendHumanTurn`, the three node edits, T77's emotion step. Compile, save.
5. The check (part 6).

Batch the writes with `ProgrammaticToolset.execute_tool_script` and `AssetTools.read_file` (T33), a few per call, so each call stays under 100 s. Close every game window before you save (T53).

## 2. `WBP_ActionBuilder`: the pick, the list's chips and the preview

### 2a. New variables

| Variable | Type | Default | Used by |
|---|---|---|---|
| `FaceIds`, `FaceWords` | String array | empty | `LoadFaces`, `FaceWord`, `BuildFaces`, `PickFace` |
| `FaceList` | the type of T75's `EmList` (a JSON object array) | empty | `LoadFaces` |
| `Face` | String | "" (Auto) | everywhere |
| `TmpId`, `TmpWord` | String | "" | `LoadFaces` |
| `FacesLoaded`, `FacePicked`, `FaceLive` | Boolean | false | `LoadFaces` / `PickFace`, `TakeFacePicked` / `PickFace`, `SetFaceLive` |

`TmpK` is T65's (Integer). If T65 didn't make it, add it.

### 2b. New functions

| Function | Inputs | Outputs | Called by |
|---|---|---|---|
| `LoadFaces` | — | — | `BuildFaces`, `WBP_Stage.FaceInit` |
| `FaceWord` | `Id` (String) | String | `FaceLabel`, `FacePhrase` |
| `FaceLabel`, `FacePhrase` | — | String | `WBP_Stage.SyncFace` / `PreviewText` |
| `AddFaceChip` | `Index` (Integer), `Label` (String), `Picked` (Boolean), `Wrap` (`WrapBox` object reference) | — | `BuildFaces` |
| `BuildFaces` | `Wrap` (`WrapBox` object reference) | Integer | `WBP_Stage.FaceShow` |
| `PickFace` | `K` (Integer) | — | `ChipClicked` |
| `ResetFace` | — | — | `OpenTurn`, `WBP_Stage.SyncFace`, `WBP_Stage.SetPrepMode` |
| `GetFace` | — | String | `WBP_Stage.FaceTake` |
| `TakeFacePicked` | — | Boolean | `WBP_Stage.SyncFace` |
| `SetFaceLive` | `On` (Boolean) | — | `WBP_Stage.SyncFace` |

`Graphs/WBP_ActionBuilder/LoadFaces.txt` (T75's `LoadEmotes` form; use the JSON nodes and the `EmList` type that T75's file shows):

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

- If T75's Findings say a `bind` inside the loop didn't work (T51), move the two `GetField`s into a helper that takes `_e`, as T65's `MakeWord` does for its create.

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
; and 1001 + k for emotion k, so ChipClicked tells it from the action chips (0 to 15). No seat bar.
(fn AddFaceChip (Index Label Picked Wrap)
  (bind _chip (UserInterface|CreateWidget "/Game/NHOS/UI/WBP_Chip.WBP_Chip_C" (Widget|GetOwningPlayer self)))
  (Class|WBPChip|Setup :self _chip :Owner self :Index Index :Label Label :Actor false :Picked Picked)
  (Widget|AddChildToWrapBox :self Wrap :Content _chip))
```

`BuildFaces.txt`:

```lisp
; T78: the face list, made again each time it opens (13 chips at most, T64 decision 11): Auto, then each emotion by its
; word. The current pick is paper. Returns how many entries it made.
(fn BuildFaces (Wrap)
  (CallFunction|LoadFaces)
  (Widget|ClearChildren :self Wrap)
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
(fn PickFace (K)
  (if (not (V FaceLive))
    (return))
  (set Face "")
  (if (and (>= K 0) (< K (len (V FaceIds))))
    (set Face (get (V FaceIds) K)))
  (set FacePicked true)
  (bind _p (CallFunction|PreviewText))
  (print (cat "NHOS: FACE pick " (select (Utilities|String|IsEmpty (V Face)) "auto" (V Face)) (select (V Armed) (cat " | " _p) "")))
  (if (and (V Armed) (not (V Sent)))
    (CallFunction|Refresh)))
```

- The `get` runs only inside the `if`, once `K` is known to be in range. A `select` would read index -1 too and print a `LogScript` warning (T64, `PreviewName`).
- No `if` before the last returns, so each joins the next (T30).

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

**`ChipClicked.txt`:** a new first statement, before T64's `(if (or (not (V Armed)) (V Sent)) (return))`, because the face list works when the builder isn't armed (Free Talk, the reactions):

```lisp
  ; T78: an entry of the face list (Index 1000 and up), in any phase where I speak.
  (if (>= Index 1000)
    (CallFunction|PickFace :K (- Index 1001))
    (return))
```

Header: `; T78: the face list's chips (Index 1000 and up) go to PickFace.`

**`PreviewText.txt`:** the pick goes before the action. Add these lines after the last `(if (streq (V Verb) "give") ...)` and before `(if (Utilities|String|IsEmpty (V Line)) ...)`:

```lisp
  ; T78: a picked face comes first, in words: "> looks worried · throw rose at @Meta: \"Oops.\"". Auto adds nothing.
  (bind _fp (CallFunction|FacePhrase))
  (if (not (Utilities|String|IsEmpty _fp))
    (set TmpStr (cat _fp " · " (V TmpStr))))
```

- The `if` doesn't return, and both `if`s after it do, so it joins them (T30).
- **`·` (U+00B7) must reach the asset as one character.** `F_Mono` (Droid Sans Mono) draws it. If the write turns it into something else (T01: escapes come through as written), use `-` instead and write that under "Findings".
- T65's `DrawPreview` splits on spaces, so "looks", "worried" and "·" become plain words, and only the @ mention is a chip.
- T64's `PickLine` prints the preview, so `NHOS: BUILDER pick` shows the face too.

**`OpenTurn.txt`:** after T64's `(set Sent false)`, add `(CallFunction|ResetFace)`, so the builder never opens showing the last turn's pick before my input opens. Header: `; T78: a scene turn opens at Auto (ResetFace).`

Compile with warnings as errors, save.

## 3. `WBP_Stage`: the chip, its list and the row

### 3a. The widget tree

1. **The chip**, as `InputRow`'s **first** child, before `InputStack`:

```
FaceSize    SizeBox; MinDesiredWidth 150; slot: VAlign Center, padding right = the row's gap (T28: 10); Collapsed at design time
└ FaceBtn   Button; IsFocusable off; bIsEnabled off at design time
  └ FaceLabel   TextBlock; text "Face: Auto"
```

   - 150 px holds "Face: Auto" with the button's 20 px side padding (T32), so the field doesn't move when I pick a short word. A long word ("Face: embarrassed", about 210 px) makes the chip wider and the field narrower while the pick lasts.
   - `bIsVariable` on for all three.
   - At 1000 px (part 3d), the row in a reaction is: chip 150, field about 450, counter 72, Action!, Pass, timer 72.

2. **The list**, as `RootBox`'s **last** child, after T65's `AtPop`, so it draws on top:

```
FacePop       Border; slot: HAlign Left, VAlign Bottom, padding set at run time (FacePlace); Collapsed at design time
└ FaceWrapSize   SizeBox; WidthOverride 560
  └ FaceWrap     WrapBox; InnerSlotPadding (8, 8) (S2); the chips go here at run time (WBP_Chip, from the builder)
```

   `bIsVariable` on for `FacePop` and `FaceWrap`. `FacePop` is styled as T65's `AtPop` is (`StylePanel(..., "Ink")`, padding 8).

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
; the chip's top.
(fn FacePlace ()
  (bind _g (Widget|GetCachedGeometry :self (Variables|WBP_Stage|GetFaceBtn)))
  (bind _rg (Widget|GetCachedGeometry :self (Variables|WBP_Stage|GetRootBox)))
  (bind _tl (Utilities|Geometry|AbsoluteToLocal _rg (Utilities|Geometry|LocalToAbsolute _g (Math|Vector2D|MakeVector2D :X 0.0 :Y 0.0))))
  (bind _view (Utilities|Geometry|GetLocalSize _rg))
  (bind _gap (Class|UIStyle|UISize :Role "S2"))
  (bind (_x _y) (Math|Vector2D|BreakVector2D _tl))
  (bind (_vx _vy) (Math|Vector2D|BreakVector2D _view))
  (bind _slot (Widget|SlotAsOverlaySlot (Variables|WBP_Stage|GetFacePop)))
  (Class|OverlaySlot|SetPadding :self _slot :InPadding (Utilities|Struct|MakeMargin :Left _x :Top 0.0 :Right 0.0 :Bottom (+ (- _vy _y) _gap))))
```

Use the node names T65's `AtPlace.txt` ended up with.

`FaceShow.txt` (input `Open`: Boolean):

```lisp
; T78: opens or closes the face list. Opening closes T65's @ list, so the two pop-ups never overlap.
(fn FaceShow (Open)
  (bind _was (V FaceOpen))
  (set FaceOpen Open)
  (if Open
    (CallFunction|AtDraw :Open false)
    (bind _n (Class|WBPActionBuilder|BuildFaces :self (Variables|WBP_Stage|GetActionBuilder) :Wrap (Variables|WBP_Stage|GetFaceWrap)))
    (CallFunction|FacePlace)
    (Widget|SetVisibility :self (Variables|WBP_Stage|GetFacePop) :InVisibility "SelfHitTestInvisible")
    (print (cat "NHOS: FACE list " (str _n)))
    (else
      (Widget|SetVisibility :self (Variables|WBP_Stage|GetFacePop) :InVisibility "Collapsed")
      (if _was
        (print "NHOS: FACE close")))))
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
; FaceWasOpen is its own copy of CanType, apart from LastCanType, so the order inside SetPrompt doesn't matter.
(fn SyncFace (CanType)
  (CallFunction|FaceInit)
  (bind _rise (and CanType (not (V FaceWasOpen))))
  (bind _fall (and (not CanType) (V FaceWasOpen)))
  (set FaceWasOpen CanType)
  (if _rise
    (Class|WBPActionBuilder|ResetFace :self (Variables|WBP_Stage|GetActionBuilder))
    (Class|WBPActionBuilder|SetFaceLive :self (Variables|WBP_Stage|GetActionBuilder) :On true)
    (Widget|SetIsEnabled :self (Variables|WBP_Stage|GetFaceBtn) :bInIsEnabled true))
  (if _fall
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

- No `if` returns, so each joins the next (T30).
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

Each file is the one T66 left (re-check items 2 to 4). Add each line by the text it follows.

| File | Change |
|---|---|
| `SetPrompt.txt` | After T66's last line `(CallFunction|TickTimer :CanType CanType)`, add `(CallFunction|SyncFace :CanType CanType)`. Header: `; T78: the face chip follows my input (SyncFace).` |
| `FitBuilder.txt` | The width line's `(select _on (V LowerWideBuild) (V LowerWide))` becomes `(select (or _on (V FaceRowOn)) (V LowerWideBuild) (V LowerWide))`. The chat height line stays T64's (`_on` only). Header: `; T78: the panel is 1000 wide on the whole play side, so the face chip fits (my person's answer); the chat shortens only with the builder.` |
| `SetPrepMode.txt` | **Prep branch**, before T64's `(CallFunction|FitBuilder)`: `(set FaceRowOn false)`, `(set FaceShownV false)`, `(Widget|SetVisibility :self (Variables|WBP_Stage|GetFaceSize) :InVisibility "Collapsed")`, `(CallFunction|FaceShow :Open false)`, `(Class|WBPActionBuilder|ResetFace :self (Variables|WBP_Stage|GetActionBuilder))`. **Else branch**, at its end: `(set FaceRowOn true)` and `(CallFunction|FitBuilder)`. Header: `; T78: the face chip's row is the play side; Scene Prep hides it and gives the panel back 640.` |
| `AtDraw.txt` | In the `Open` branch, before `(CallFunction|AtShow ...)`: `(if (V FaceOpen) (CallFunction|FaceShow :Open false))`. Header: `; T78: the @ list closes the face list.` |
| `SpeechKey.txt` | After T65's `(if (and (V AtOpen) (streq Key "Escape")) ...)` block: `(if (and (V FaceOpen) (streq Key "Escape")) (CallFunction|FaceShow :Open false) (return true))`. Header: `; T78: Escape closes the face list too.` |

- **`FitBuilder` widens the panel at the scene's start:** `SetPrepMode(false)` runs right before `StartScene` (T64 part 4e), and the panel stays 1000 until the next Scene Prep (decision 2). `SetPhase`'s `FitBuilder` call (T64) gives the same width, because `FaceRowOn` stays true.
- **`AtDraw` and `FaceShow` don't loop:** `FaceShow(true)` calls `AtDraw(false)`, which never calls `FaceShow`. `AtDraw(true)` calls `FaceShow(false)`, which only calls `AtDraw` when it opens.
- If T66 left `SetPrompt` ending in another line, put `SyncFace` last anyway.

### 3e. The event chain

Bind `FaceBtn`'s `OnClicked` with `UMGToolSet.BindToEventProperty` (T04), then write `Graphs/WBP_Stage/EventGraph.Face.txt`:

```lisp
; Only the face chip's chain of WBP_Stage's EventGraph (T78). A click opens or closes the face list.
(event OnClicked(FaceBtn)
  (CallFunction|FaceClick))
```

`write_graph_dsl` keeps the chains it doesn't name (`EventGraph.StartButton.txt`'s note). Compile `WBP_Stage` with warnings as errors, save.

## 4. What the row looks like in each phase (step 2)

| Phase | Chip | Panel | Preview line |
|---|---|---|---|
| Scene Prep | hidden | 640 × 380 | — |
| My scene turn | first in the row; on while I can type | 1000, chat 160 (T64) | `> looks <word> · <action>: "<line>"` with a pick, T64's line with Auto |
| Free Talk, my line and my last word | first in the row; on while I can type | 1000, chat 380 | none (the chip's label shows the pick) |
| The Cut, my vote | hidden (decision 4) | 1000, chat 380 | none |
| My reaction | first in the row; on while I can type | 1000, chat 380 | none |

Others' turns in every phase: the chip shows, off ("Face: Auto", 40%), so the row doesn't shift when my turn opens.

## 5. `BP_Show`: my sends carry the pick

### 5a. New variables

`HFace`, `FaceOut` (String, ""). `FaceAuto`, `FaceFrom` (String, "") if `ApplyFace`'s returns need copies (see below).

### 5b. New functions

`Graphs/BP_Show/TakeFace.txt`:

```lisp
; T78: each of my sends starts here (SendHumanTurn, SendHumanTalk, SendHumanReact, SendHumanVote): the face chip as it
; stands goes with the turn. A timeout sends the chip as it stands too (T66's TimeUp reaches the same sends). Autoplay's
; sends read Auto, since my input never opens. ApplyFace uses it once and clears it.
(fn TakeFace ()
  (bind _f (Class|WBPStage|FaceTake :self (V Stage)))
  (set HFace _f))
```

`Graphs/BP_Show/ApplyFace.txt` (inputs `AutoId`, `AutoFrom`: String; outputs `Id`, `From`: String, made in that order):

```lisp
; T78: T77's emotion step calls this with the emotion it picked (the input LLM's, the keyword table's, or neutral for a
; pass or no words) and where it came from. A pick on the chip overrides it, for a pass and a silent turn too (the
; reason to pick one). Used once: HFace is cleared, so a pick never reaches a later line.
(fn ApplyFace (AutoId AutoFrom)
  (set FaceOut (V HFace))
  (set HFace "")
  (if (Utilities|String|IsEmpty (V FaceOut))
    (return AutoId AutoFrom))
  (return (V FaceOut) "pick"))
```

- `FaceOut` is set before `HFace` is cleared. A `bind` of `(V HFace)` would be a getter that reads "" after the clear.
- `(return a b)` fills the outputs in the order they were made (T64-build part 2c).

### 5c. Where they are called

1. **`SendHumanTurn`** (T63's file, `Graphs/BP_Show/SendHumanTurn.txt`): after `(set HumanSent true)`, add `(CallFunction|TakeFace)`. Header: `; T78: the face chip goes with the turn (TakeFace).` `AutoTurn` calls `SendHumanTurn` too and gets Auto.
2. **`SendHumanTalk`, `SendHumanReact`, `SendHumanVote`** (no files; node edits): put one `CallFunction|TakeFace` node right after each function's entry, before the "pass" branch (survey 3). Link the entry's exec to it, and its exec out to the node that followed the entry. My last word goes through `SendHumanTalk` (T58). In the vote the chip is hidden and at Auto, so `SendHumanVote` takes "", which stops a pick from an earlier line from reaching the vote. Write each edit under "Findings".
3. **T77's emotion step** (re-check item 1): right before T77's `NHOS: HUMAN emotion=` print, add

```lisp
  ; T78: a pick on the face chip overrides T77's pick (ApplyFace); from=pick.
  (bind (_fid _ffrom) (CallFunction|ApplyFace :AutoId <T77's emotion> :AutoFrom <T77's from>))
```

   Then point T77's print and T77's carrier (the variable, entry field or pin that takes my emotion to the line) at `_fid` and `_ffrom` in place of T77's own values. If that step has a file, change the file. If it has none, make the same change as a node edit, and write it under "Findings". If T77 settles my emotion in more than one place, do this in each one.
   - If T77 skips the keyword table or the input LLM's emotion in some cases, keep that. `ApplyFace` only replaces the result.
   - If T77's step is inside `HumanSay` or after it, `HFace` is still the one that send set, since nothing else sends in between: the logic waits for my line (T63).

Compile `BP_Show` with warnings as errors. The editor log after the compile has no `LogBlueprint: Error`. Close every game window before you save (T53).

## 6. The check

**Before the runs:** `Local/switches.json` in the repo folder with `"mode": "free"`, `"autoplay": false`, `"fast_lines": false`, `"ai_seats": 0`, **`"spare_human": true`** (so I'm never cut and get a reaction turn every scene, as in T66's check), `"force_tie": false`, and `emote_test` false. PIE in a floating window at 1600 × 900 (`LevelEditorPlaySettings` `newWindowWidth` and `newWindowHeight`; put them back after). Pick **Test for Free**. Screenshots with `SlateInspectorToolset.Screenshot` to `Saved/T78/shots/` (not in git). On the PC the Slate inspector's `Click` and `Type` land (T33).

### Run A: one show played by hand in PIE

1. **`face_auto.png`:** press Start the scene. At turn 1, once the lines stop: the chip "Face: Auto" first in the input row (plum), the field right of it, the panel 1000 wide. Read `FaceLabel`'s text through MCP: "Face: Auto". Log: `NHOS: FACE loaded 12 emotions` (or the count in `emotes.json`).
2. **The focus check:** click the field once, `Type` "Calm down", click the chip. **`face_list.png`:** the list over the chip, Auto in paper, then calm, happy, sad, ..., embarrassed. Nothing in the lower panel moved, and no robot or name tag is covered by anything but the list. Log: `NHOS: FACE list 13`. Click **worried**: the list closes, the chip reads "Face: worried" in paper. Log: `NHOS: FACE pick worried | > looks worried · stand still: "Calm down"`. `Type` ", everyone." Every letter lands in the field.
3. **`face_preview.png`:** the preview line reads `> looks worried · stand still: "Calm down, everyone."`. Click **Look around**: `> looks worried · look around: "Calm down, everyone."`.
4. Press **Action!**. Log, in order: `NHOS: BUILDER send around - - ready=yes`, `NHOS: HUMAN around - - says=Calm down, everyone.`, `NHOS: HUMAN emotion=worried from=pick`. When my line plays: `NHOS: EMOTE <my seat> worried ...` (T75, T77). **`face_play.png`:** my robot's worried face while my line types out. An actor state printed to the log has `feels` "worried" on my entry (T77).
5. **Turn 2 starts at Auto:** when it opens, `NHOS: FACE reset` and the chip "Face: Auto" (read its text). The preview has no "looks". Type "sorry, my bad", pick No action, press Action!: `NHOS: HUMAN emotion=<id> from=<llm|keywords>`, **not** `from=pick` (T77's way; embarrassed if the keyword table or the input step catches "sorry").
6. **Turn 3, a pick left to time out:** pick **smug**, type nothing, touch nothing else. At 0: `NHOS: TIMEOUT scene none`, `NHOS: HUMAN none - - says=-`, `NHOS: HUMAN emotion=smug from=pick` (decision 5: a silent turn shows the pick). My robot shows smug while it stands still.
7. **Escape and the @ list:** at a turn of mine, open the list and press Escape: `NHOS: FACE close`. Open it again, then type `@`: the @ list opens and the face list closes (`NHOS: FACE close`, then `NHOS: MENTION open ...`).
8. **`freetalk_face.png`:** my Free Talk line: no builder, the chip first in the row, the panel 1000 wide, the chat at its full height. Pick **suspicious**, type "Who moved the rose?", send: `NHOS: HUMAN emotion=suspicious from=pick`, and my robot shows suspicious when the line plays.
9. **A pass with a face:** at my next Free Talk line (or my last word), pick **confused** and press Pass: `NHOS: HUMAN emotion=confused from=pick`, and my robot shows confused next to T57's "passed" marker.
10. **`vote.png`:** the Cut's vote: the vote row, no chip, the panel still 1000.
11. **`reaction_face.png`:** my reaction: the chip at "Face: Auto" (reset), the timer. Pick **sad**, leave the field empty, let it time out: `NHOS: TIMEOUT reaction`, my reaction as a pass, `NHOS: HUMAN emotion=sad from=pick`.

Stop PIE. In every shot, check that no robot, name tag or thrown prop sits behind the lower panel (T27).

### Run B: a free autoplay show in a game window

`"autoplay": true`, `"fast_lines": true`, `"mode": "free"`, `"spare_human": false`. Use the game-window command from `CLAUDE.local.md` with `-log=T78auto.log`. In the log: `NHOS: SHOW END`, **no `LogScript` line** (above all no "Accessed None" and no "Attempted to access index"), **no `NHOS: FACE pick`** and **no `from=pick`**: autoplay's lines take T77's way. Close the game window by its `-log=` name.

### Run C: the checker

`python Tools/check_prompts.py --offline` passes. If T77 gave `--log` a count of `from=` values, run it on `T78auto.log`: no `pick`.

**Afterward:** `autoplay`, `fast_lines` and `spare_human` back to false, the PIE window settings back, every game window closed.

### Findings to write in `T78.md`

- **My person's answer** to question 1 (above), and decisions 1 to 9 for my person to look over.
- **The reset (step 4):** judge, as a critical first-time player, whether I'd expect a pick to stay from one turn to the next. Look at `face_play.png` and the turn 2 shot: does a chip that goes back to "Face: Auto" read as "it's per line" or as "my pick was lost"? If a first-time player would expect it to stay, say so and ask my person (multiple-choice tool) before you close the task.
- **The design review** (the Done-when's last line), from the shots: is the chip easy to find, does "Face:" say what it does, does it crowd the input row at 1000 px, and does the list read as "pick a face". List anything for T34 (the row's polish).
- The node edits in `SendHumanTalk`, `SendHumanReact`, `SendHumanVote` and, if it has no file, T77's emotion step, old and new.
- Whether `·` reached the preview line, or `-` replaced it (part 2c).
- **Unreal MCP rules found in this task**, as earlier tasks do.

## 7. The design doc (tell, don't change)

T78's Touches don't name the design doc. Read it with the Claude Docs connector, propose each fix to my person in the doc's words, and edit only after their OK (the plan's "The design doc follows the game"):

- **Rules tab, "Emotions" (T76's section), bullet 4:** "The game picks yours from your line, unless you pick it yourself before you send." It matches what T78 builds. Propose adding: "The Face chip in your input row picks it for one line; it goes back to Auto each turn."
- **Turn Input tab:** it has no Face chip (T76-build 1d). Propose a line in the speech row's description: "A Face chip, first in the row: Auto, or the emotion your robot shows with this line."

## 8. The commit

One commit, `T78: I can pick my robot's emotion`: `Content/NHOS/UI/WBP_ActionBuilder.uasset`, `Content/NHOS/UI/WBP_Stage.uasset`, `Content/NHOS/Core/BP_Show.uasset`; `Graphs/WBP_ActionBuilder/` (new: `LoadFaces`, `FaceWord`, `FaceLabel`, `FacePhrase`, `AddFaceChip`, `BuildFaces`, `PickFace`, `ResetFace`, `GetFace`, `TakeFacePicked`, `SetFaceLive`; changed: `PreviewText`, `ChipClicked`, `OpenTurn`), `Graphs/WBP_Stage/` (new: `FaceInit`, `FacePlace`, `FaceShow`, `FaceClick`, `SyncFace`, `FaceTake`, `EventGraph.Face`; changed: `SetPrompt`, `FitBuilder`, `SetPrepMode`, `AtDraw`, `SpeechKey`), `Graphs/BP_Show/` (new: `TakeFace`, `ApplyFace`; changed: `SendHumanTurn`, and T77's file for its emotion step if it has one); `Docs/tasks/T78.md` (Result, Findings), `Docs/Plan.md` (the box, the "Next up" line), `Docs/DevLog.md`. If part 7 changed the design doc, say so in the message. Stage by path. Unlock the three assets after the push.

## 9. Knock-on: tell, don't change

- **T34** (the input row's polish): the chip's place (first in the row), its 150 px minimum, paper for a pick, and the panel at 1000 on the whole play side (decision 2) are its to revisit. The chip and the list never take keyboard focus, on purpose.
- **T61** (the stagehand): a tip at the first scene turn can point at the chip: "Pick your robot's face, or leave it on Auto."
- **`Docs/ItchPage.md`, "Controls":** one line after T78: "**Face:** pick the face your robot shows with your line, or leave it on Auto and the game picks one from your words."
- **T70:** the chip is worth a second in the gameplay video (a pick, then the face on stage).
