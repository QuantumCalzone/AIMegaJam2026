# T84 build sheet: Scene Prep shows the scene and Start the scene in the middle

Back to [T84](T84.md). A PC prep session wrote this on 2026-11-16, without the editor. It is a plan, not a record: nothing here was written to the editor, the design doc or any file but this one. When T84 writes a graph, its source goes to `Graphs/` as usual.

## Written against, and what to re-check after T88

**Written against `noHumansOnSet` at `4150a0b`** (the plan with T90 added). At that commit T78 and T38 are in; **T88 is being built** (the `t88` session drives the editor and holds the locks on `BP_Show.uasset` and `WBP_Stage.uasset`), and none of its graphs are pushed yet. The design doc was read, not changed: Rules tab **rev 59** (T88's doc edits are already in it: the Scene Prep bullets say "clue", not "category") and Art Inspiration **rev 41**.

T84 comes after T88. T88's sheet ([T88-build.md](T88-build.md), parts 5c, 5d, 6 and 12) plans these changes under T84. **Before T84 writes anything, check each one against T88's push:**

1. **`PrepPrompt`'s turn line** (part 4 here). `git log --oneline 4150a0b..HEAD -- Graphs/BP_Show/PrepPrompt.txt`. T88 changes "the note's category" to "the note's clue" in the `SetPTurn` string and adds a comment line. Part 4's draft is written for the line after T88; take the file as T88 left it and change only the `SetPTurn` string and the comment.
2. **`SetPrepMode`** (part 3). T88's plan doesn't change it. `git log --oneline 4150a0b..HEAD -- Graphs/WBP_Stage/SetPrepMode.txt` should print nothing; if it prints a commit, merge its lines into part 3's draft by meaning.
3. **My card's note box.** After T88, `NoteBox` holds `NoteTitle`, `NoteText` ("Clue: <label>"), the new wrapped **`ClueText`** and `NoteHidden`. It stays on the card; T84 doesn't touch it. The longest clue (Pig Latin of the note `hold_prop`, about five lines) makes the card taller in every phase, which is why the card-scroll check in part 6 forces it.
4. **`ShowPrep`** (no file). T88 changes its `SetInfoTop` note pin and adds a `SetClue` call. T84 doesn't change `ShowPrep`, but part 0 reads where it fills `SceneTitle`, `SceneText`, `PlacesText` and `PropsText`: they must be filled by widget variable, so moving the widgets doesn't break the fill.
5. **The locks and claims.** `git lfs locks` shows no lock on `BP_Show.uasset` or `WBP_Stage.uasset` and none on `Docs/claims/T88`. Then reload both packages in the editor if the pull changed them (memory "Editor stale after a pull").
6. **The design doc.** T90 moved the doc into the repo, so the doc edit in part 5 goes into `Docs/Design/Rules.md` and `Docs/Design/ArtInspiration.md`. Read the two files again: if a quoted passage changed since this sheet read it (rev 59 / rev 41 of the old Claude Doc), put the OKed edit into the new text by meaning.
7. **T85's prep sheet** (`Docs/tasks/T85-build.md`, written by a parallel prep session). If it names T84's new widgets, check it uses the names in part 2 (`PrepSize`, `PrepPanel`, `PrepPanelBox`). If it doesn't, tell the dispatcher; don't edit it.
8. **T61.** Still open (it depends on T84). `WBP_Earpiece`'s stage spot is T61's; T84 only writes where it can go (part 7).

## In short

| T84 step | Where in this sheet |
|---|---|
| 1. A prep panel in the middle | Part 2a, 2b (the tree), part 3 (`PrepInit`) |
| 2. Where it sits | Part 2c (the spot rule and the numbers to measure), question 1 |
| 3. Start the scene in the middle | Part 2b (the move), part 3 (its line in `SetPrepMode` stays) |
| 4. No lower panel in scene 1's Scene Prep | Part 3 (`SetPrepMode`), question 1 (scenes 2 on) |
| 5. The turn line | Part 4 (`PrepPrompt`) |
| 6. Room for T61's earpiece | Part 7 |
| 7. The design doc | Part 5, question 2 |
| 8. T32's row 13 | Part 8 |
| Done when | Part 6 |

- **One asset changes for the layout:** `WBP_Stage` (a new panel `PrepSize` > `PrepPanel` > `PrepPanelBox` in `RootBox`; `SceneTitle`, `SceneText`, `SetTitle`, `PlacesText`, `PropsText` and `StartButton` move into it; two new functions' worth of logic in `SetPrepMode` and a new `PrepInit`; two new variables). `BP_Show` changes only `PrepPrompt`'s string.
- **What stays on the card:** `YouAre`, `MeText`, `RoleText`, `WantText`, `NoteFrame` (with T88's `ClueText`), and in Scene Prep `PrepBox` with only `CastTitle` and `CastBox` left in it (T85 takes those off later).
- **The lower panel:** collapsed in scene 1's Scene Prep (`LowerSize` `Collapsed`); in the Scene Preps of scenes 2 on it shows at 640 wide (question 1), holding the Show chat button and the greyed field; at `SetPrepMode(false)` it is back, at `LowerWide` (1080).
- **No new `NHOS:` line.** The Done-when check wants the same lines as before on a click, so nothing here prints.
- **Locks:** `Content/NHOS/UI/WBP_Stage.uasset`, `Content/NHOS/Core/BP_Show.uasset`. **Costs money:** nothing (Test for Free and free autoplay).

## Questions for my person

Two questions, each asked on its own with the multiple-choice tool, the recommendation first. **Neither is answered yet.** T84 can build question 1's recommendation and ask both at the doc step (step 7), or the dispatcher can ask them before T84 starts.

1. **The lower panel in the Scene Preps of scenes 2 on.** T84 step 4 keeps it there (the chat holds the earlier scenes; T38 asks to keep Show chat reachable). But since T38 the panel is 1080 wide in every phase (the doc's Input row says so), and its right edge (about x 1104 of 1920) leaves only about 300 px before my card: too narrow for the scene. With the chat open, the panel's top is at about y 590 of 1080, the robots' feet line, so the middle panel can't sit above it either.
   - **"640 wide in Scene Prep (Recommended)":** in the Scene Preps of scenes 2 on the panel narrows to 640 (its width before T38; it holds only Show chat and the greyed field), and the middle panel sits in the gap between it and my card, in the same spot in every scene. It goes back to 1080 when the scene starts. Why: it keeps the chat one click away, as T38 asked, and leaves the middle panel 600 to 700 wide, enough for the longest scene with no scroll.
   - "Hide it in every Scene Prep": no lower panel in any Scene Prep, so the middle panel can be centered on the screen. Simpler, but the last scene's talk can't be read during prep (against T38's note and T84 step 4).
   - "Keep 1080, panel above it": the middle panel stacks above the input row in scenes 2 on. It covers the robots when I open the chat, so not recommended.
2. **The design doc edit** (part 5), with the full text. Options: "OK all edits (Recommended)", "OK, but not the Art Inspiration tab", "Change some edits". Why: the Rules bullet and the UI direction's call sheet line both describe the old screen; the Art Inspiration edits keep the layout rows true (the "1080 in every phase" sentence and the call sheet that shrinks into the corner, which was never built).

## Decisions this sheet makes (open to change)

1. **The middle panel is an ink panel**, styled with `UIStyle.StylePanel :Look "Ink"` like T61's earpiece and the face list, unless part 0 finds the card itself has a Paper look: then the panel takes the card's look, so the moved texts keep the colors they have today. The moved widgets keep their own fonts and colors except where step 2 sets a role (part 3's `PrepInit`).
2. **One spot in every scene.** The panel doesn't move between scene 1 (no lower panel) and scene 2 (the 640 panel): a panel that jumps between scenes reads as a bug. Part 2c says how to pick the spot.
3. **The scene number comes from `BP_Show` in `SetPrepMode`**, through `WBP_Stage`'s own `ShowRef()` (T65), as T84 step 4 asks. `OpenPrep` and `StartFromPrep` don't change. `SceneNum` goes up before `OpenPrep` (T47's `WatchShow` note), so it is 1 in scene 1's prep, also after Play Again (`RestartShow` → `ScenePrep` with `SceneNum` 1). The test is `<= 1`, so a 0 never shows the panel.
4. **`StartButton` keeps its visibility line in `SetPrepMode`** (step 3: T34-build 1b's focus ring finds it there), even though it now lives inside `PrepSize`, which hides with it.
5. **The hint changes too:** `PrepPrompt`'s `SetPHint` "Read your card first." becomes "Read the scene first." It shows in the greyed field in scenes 2 on, and the card no longer holds the scene. One-line change in the same graph; drop it if my person prefers.
6. **No animation.** The doc's "shrinks into the corner in 400 ms" was never built and isn't in T84's steps; question 2's edit takes it out of the doc instead.
7. **`BPC_LinePlayer.BubbleKeep` doesn't change.** No line plays in Scene Prep (scene 2's prep comes through the queue's `prep` cue, after the last reaction), so no bubble needs to keep clear of the middle panel. If a screenshot shows a bubble over it, tell T34 (it is T34's to add `PrepSize` to `KeepArr`).

## 0. Before you start

1. Do the eight checks under "Written against".
2. Claim T84 (`git lfs lock Docs/claims/T84`) and lock `WBP_Stage.uasset` and `BP_Show.uasset`. Set `Editor: driving` in your status file.
3. **Read `WBP_Stage`'s tree** (save each read to `Saved/T84/`; never write a read-back to the editor). Record:
   - `RootBox`: its class (the comments in `BPC_LinePlayer.BubbleKeep` call it "the overlay that fills the window", `LowerSize`'s parent; if it is a CanvasPanel instead, part 2c's slot becomes anchors) and its children in order (`LowerSize`, the header, the card's `InfoSize`, `ClapperBox`, T65's `AtPop`, T78's `FacePop`, ...).
   - **`LowerSize`:** its slot (alignment, padding), its design-time **visibility** (part 3 sets it back to this value; the draft assumes `SelfHitTestInvisible`) and `WidthOverride` (1080 since T38). Also `LowerWide` and `LowerWideBuild` on the class defaults (both 1080).
   - **`InfoSize`** (the card): its slot, width and the card's border brush (Ink or Paper look), for decision 1 and part 2c.
   - **`PrepBox`:** its 7 children in order (`SceneTitle`, `SceneText`, `CastTitle`, `CastBox`, `SetTitle`, `PlacesText`, `PropsText`, as T28 built it), each one's class, slot padding, font and color.
   - **`InputRow`:** its children in order with paddings (expected: T78's `FaceSize`, T38's `ChatButton`, `InputStack`, `CountSize`, `SendButton`, `PassButton`, `ContinueButton`, `StartButton`, `TimerSize`); `StartButton`'s slot padding (T28: 10 left) and `IsFocusable`.
   - What sets `StartButton`'s Primary style and the `PrepBox` texts' fonts: `find_nodes` for `StartButton`, `SceneTitle`, `SceneText`, `PlacesText`, `PropsText` across `WBP_Stage`'s graphs (`StyleStage` or `EventConstruct` have no file). They are set by variable, so they follow the move; note whether a font is set at every Scene Prep (then `PrepInit`'s fonts must go there instead, or they are overwritten).
   - `ShowRef`'s `Show` variable type: it must be `BP_Show` (object), so `Class|BPShow|GetSceneNum` takes it with no cast. If it is `Actor`, add a cast in part 3.
4. **Read `ShowPrep` in `BP_Show`** (no file): the nodes that set `SceneTitle`/`SceneText`/`PlacesText`/`PropsText` (through `SetInfoTop`, `ShowCast` or others) and the text they write (does `PlacesText` hold the places' names only, or "name: what" lines? It decides whether the stage lines need `Caption`). Don't change it.
5. **Find what else touches `LowerSize`:** `find_nodes` for `LowerSize` in `WBP_Stage` and `BP_Show`. At `4150a0b` the files show only `FitBuilder` (width) and `BPC_LinePlayer.BubbleKeep` (geometry). If a no-file graph sets its visibility (an end screen, the title), part 3's restore must not fight it: tell the dispatcher before you go on.
6. **List the UMG tools:** `describe_toolset` for the UMG toolset. You need a tool that **moves an existing widget to a new parent** and keeps the widget object (its name, `Is Variable`, and for `StartButton` its bound `OnClicked` event). Never delete and re-create `StartButton` or the five texts: `ShowPrep`, `SetPrepMode`, T34's ring and the click chain all reach them by variable. If no move tool exists, an editor Python script on the `WidgetTree` (remove from the old panel and add to the new one, same object) does it; read `Docs/tasks/T28.md`'s MCP rules first (`WrapWidgets` drops slot paddings).
7. **Take the "before" screenshots** in PIE (Test for Free, autoplay off, 1600 × 900): scene 1's Scene Prep and scene 2's Scene Prep, and note the `NHOS:` lines from a Start click (`PREP start scene=1` and what follows) for the Done-when comparison. **Measure** in the scene 1 shot: the robots' lowest point (feet, held props, name tags, in px of 900), the card's left edge and the chat column's right edge (scene 2, chat open).

## 1. The order of the build

T18 and T63: a call node made before a compile has the old pins, so create each function and variable first, compile, then write the graphs callee first.

1. Part 0.
2. `WBP_Stage` tree (part 2): add `PrepSize` > `PrepPanel` > `PrepPanelBox` to `RootBox`; move the five texts and `StartButton`; set the slots. Compile, save.
3. `WBP_Stage` variables and functions (part 3): `LowerPrep`, `PrepReady`; `PrepInit` (empty), compile; write `PrepInit`, then `SetPrepMode`. Compile with warnings as errors, save.
4. `BP_Show` (part 4): `PrepPrompt`'s strings. Compile, save.
5. Part 6: the checks. Then parts 5 (doc, after my person's OK), 7 and 8 (the task file and T32's row).

## 2. `WBP_Stage`: the tree

### 2a. New widgets

| Widget | Class | Parent | Settings |
|---|---|---|---|
| `PrepSize` | SizeBox | `RootBox`, right after `LowerSize` (so `AtPop` and `FacePop` still draw over it) | `WidthOverride` from part 2c (expected 600 to 680); `MaxDesiredHeight` = the room under the robots (part 2c); visibility `Collapsed` at design time (`SetPrepMode` shows it); `Is Variable` on |
| `PrepPanel` | Border | `PrepSize` | brush from `PrepInit` (decision 1); padding `UISize "S5"` (24) on all sides; visibility `SelfHitTestInvisible`; `Is Variable` on |
| `PrepPanelBox` | VerticalBox | `PrepPanel` | visibility `SelfHitTestInvisible`; `Is Variable` off |

### 2b. The move

Into `PrepPanelBox`, in this order (the reading order: the scene, then the stage, then the button):

1. `SceneTitle` (fill, left; top padding 0)
2. `SceneText` (fill, left; top padding `S2` 8; Auto Wrap on, as on the card)
3. `SetTitle` (top padding `S4` 16)
4. `PlacesText` (top padding `S1` or 4; wrap on)
5. `PropsText` (top padding `S1`; wrap on)
6. `StartButton` (**horizontal alignment Center**, top padding `S4` 16, left padding 0, not 10). Keep its name, its label `StartLabel` or whatever its child is, its `IsFocusable` and its style; the click chain in `Graphs/WBP_Stage/EventGraph.StartButton.txt` is not rewritten.

`CastTitle` and `CastBox` stay in `PrepBox` on the card, in their old order and paddings. `PrepBox` keeps its `SetPrepMode` line, so the cast still shows only in Scene Prep (T85 changes that).

**After T88:** nothing in this part moves under T88. `NoteFrame` and its four rows are outside `PrepBox`.

### 2c. Where it sits (step 2)

Work in the virtual 1920 × 1080 layout (UMG scales by the short side, T61: 1600 × 900 and 1280 × 720 are both 16:9, so the layout is the same at both; only the pixel size changes, × 0.833 and × 0.667). Measure, from part 0's numbers:

- `C` = the chat column's right edge in scenes 2 on, with the panel at 640: about 24 + 640 = **664** (check `LowerSize`'s left padding).
- `K` = the card's left edge (`InfoSize`'s left), about **1400 to 1420** (T61's earpiece at `StageX` 112 sat about 40 px clear of it).
- `F` = the robots' lowest point in Scene Prep (feet, name tags, held props), about **590** (T38: the chat's top with the chat open, about y 493 of 900, is the line T27 set under the robots' feet).
- The gap is `[C + 24, K − 24]`, about 688 to 1380: about **690 wide**.

The rule:

1. If a panel of the width the content needs (at least 560) fits centered on the screen inside the gap (its left edge `960 − W/2` ≥ `C + 24` and its right edge ≤ `K − 24`), center it on the screen: slot horizontal alignment Center, padding 0.
2. Otherwise (expected: a 600+ panel centered at 960 reaches x 660, over the chat column), center it in the gap, the same in every scene (decision 2): `W` = min(680, gap width), slot horizontal alignment **Left**, left padding = `C + 24 + (gap width − W) / 2`. With the numbers above that is about `W` 680 at x 693.
3. Vertically: slot vertical alignment **Bottom**, bottom padding `UISize "Edge"` (24). `PrepSize.MaxDesiredHeight` = `1080 − 24 − F − 16` (about 450), so the panel's top never goes above the robots' feet.
4. **The longest scene must fit with no scroll:** "The Ring Is Mine, I Mean Ours" has the longest premise (290 characters); Dino Island has the longest wants (but the wants stay on the card); also the scene in T32's `p16_prep2_long.png`. At `W` 680 less 48 of padding, the premise at `Body` 20 is about 5 lines. If the panel would exceed `MaxDesiredHeight`, first set `PlacesText` and `PropsText` to `Caption` 18 (part 3), then lower the panel's padding to `S4` 16; if it still doesn't fit, say so under Findings for T34 rather than shrink `Body`.

If question 1's answer is "Hide it in every Scene Prep", rule 1 applies with `C` = 0 (center on the screen, `W` up to 720), and part 3's scenes-2-on branch collapses `LowerSize` too.

## 3. `WBP_Stage`: `SetPrepMode` and `PrepInit`

### 3a. New variables

| Variable | Type | Default | Used by |
|---|---|---|---|
| `LowerPrep` | Float | 640 | `SetPrepMode` (the lower panel's width in the Scene Preps of scenes 2 on; question 1) |
| `PrepReady` | Boolean | false | `PrepInit` |

### 3b. `Graphs/WBP_Stage/PrepInit.txt` (new)

```lisp
; T84: once, the middle panel's look and its type (T84 step 2): the scene's title in CardTitle, its text in Body, the
; stage lines in Caption. The ink panel is UIStyle's (decision 1: the card's look if part 0 found the card is Paper).
(fn PrepInit ()
  (if (V PrepReady)
    (return))
  (set PrepReady true)
  (Class|UIStyle|StylePanel :Panel (Variables|WBP_Stage|GetPrepPanel) :Look "Ink")
  (Class|TextBlock|SetFont :self (Variables|WBP_Stage|GetSceneTitle) :InFontInfo (Class|UIStyle|UIFont :Role "CardTitle"))
  (Class|TextBlock|SetFont :self (Variables|WBP_Stage|GetSceneText) :InFontInfo (Class|UIStyle|UIFont :Role "Body"))
  (Class|TextBlock|SetFont :self (Variables|WBP_Stage|GetSetTitle) :InFontInfo (Class|UIStyle|UIFont :Role "Name"))
  (Class|TextBlock|SetFont :self (Variables|WBP_Stage|GetPlacesText) :InFontInfo (Class|UIStyle|UIFont :Role "Caption"))
  (Class|TextBlock|SetFont :self (Variables|WBP_Stage|GetPropsText) :InFontInfo (Class|UIStyle|UIFont :Role "Caption")))
```

- Sizes from `UISize`: `CardTitle` 24, `Body` 20, `Name` 20, `Caption` 18 (read at `4150a0b`). `SetTitle` ("THE STAGE" or what T28 wrote) takes `Name` (bold 20), a step under the scene's title; if part 0 finds it already uses a role, keep it.
- If the texts are on an ink panel now but were dark on a Paper card, also set their colors here: `Class|TextBlock|SetColorandOpacity` with `UIColor "Text"` for the texts and `"OldGold"` for the two titles. If part 0 found a graph that sets these fonts or colors at every Scene Prep, put these lines there instead and drop them here.
- Check each node name with `find_node_types` before you write (T29): the `SetFont` name is the one T88-build part 6b uses.

### 3c. `Graphs/WBP_Stage/SetPrepMode.txt` (whole file; the lines marked T84 are new, every other line is as pushed)

```lisp
; T64: Scene Prep closes the builder and gives the lower panel back its size; the play side styles Action! as the one
; Primary button (gold, ink text: "act now").
; T65: the word counter shows with Action! and Pass, and hides in Scene Prep.
; T66: Scene Prep hides the turn timer and gives up its wide panel.
; T78: the face chip's row is the play side (FaceRowOn); Scene Prep hides the chip and its list and resets the pick.
; T84: Scene Prep shows the scene, the stage and Start the scene in the middle panel (PrepSize); PrepBox keeps only the
; cast on the card. In scene 1's Scene Prep the whole lower panel is collapsed (no chat line yet, the field is greyed and
; Start the scene has moved); in the Scene Preps of scenes 2 on it shows at LowerPrep (640), so the middle panel clears
; it. The play side gives it back at LowerWide. The width goes after FitBuilder, which would set LowerWide on a change.
(fn SetPrepMode (Prep)
  (bind _n (Class|BPShow|GetSceneNum :self (CallFunction|ShowRef)))
  (if Prep
    (CallFunction|PrepInit)
    (Widget|SetVisibility :self (Variables|WBP_Stage|GetPrepSize) :InVisibility "SelfHitTestInvisible")
    (Widget|SetVisibility :self (Variables|WBP_Stage|GetPrepBox) :InVisibility "SelfHitTestInvisible")
    (Widget|SetVisibility :self (Variables|WBP_Stage|GetStartButton) :InVisibility "Visible")
    (Widget|SetVisibility :self (Variables|WBP_Stage|GetSendButton) :InVisibility "Collapsed")
    (Widget|SetVisibility :self (Variables|WBP_Stage|GetPassButton) :InVisibility "Collapsed")
    (Widget|SetVisibility :self (Variables|WBP_Stage|GetCountSize) :InVisibility "Collapsed")
    (Widget|SetVisibility :self (Variables|WBP_Stage|GetTimerSize) :InVisibility "Collapsed")
    (set TimerOn false)
    (set TimerWide false)
    (set FaceRowOn false)
    (set FaceShownV false)
    (Widget|SetVisibility :self (Variables|WBP_Stage|GetFaceSize) :InVisibility "Collapsed")
    (CallFunction|FaceShow :Open false)
    (Class|WBPActionBuilder|ResetFace :self (Variables|WBP_Stage|GetActionBuilder))
    (Class|WBPActionBuilder|Close :self (Variables|WBP_Stage|GetActionBuilder))
    (CallFunction|FitBuilder)
    (if (<= _n 1)
      (Widget|SetVisibility :self (Variables|WBP_Stage|GetLowerSize) :InVisibility "Collapsed")
      (else
        (Widget|SetVisibility :self (Variables|WBP_Stage|GetLowerSize) :InVisibility "SelfHitTestInvisible")
        (Layout|SizeBox|SetWidthOverride :self (Variables|WBP_Stage|GetLowerSize) :InWidthOverride (V LowerPrep))))
    (else
      (Widget|SetVisibility :self (Variables|WBP_Stage|GetPrepSize) :InVisibility "Collapsed")
      (Widget|SetVisibility :self (Variables|WBP_Stage|GetPrepBox) :InVisibility "Collapsed")
      (Widget|SetVisibility :self (Variables|WBP_Stage|GetStartButton) :InVisibility "Collapsed")
      (Widget|SetVisibility :self (Variables|WBP_Stage|GetSendButton) :InVisibility "Visible")
      (Widget|SetVisibility :self (Variables|WBP_Stage|GetPassButton) :InVisibility "Visible")
      (Class|UIStyle|StyleButton :Button (Variables|WBP_Stage|GetSendButton) :Label (Variables|WBP_Stage|GetSendLabel) :Kind "Primary")
      (Widget|SetVisibility :self (Variables|WBP_Stage|GetCountSize) :InVisibility "HitTestInvisible")
      (bind _n0 (CallFunction|CountWords :Text (Utilities|String|ToString(Text) (Class|TextBox|GetText :self (Variables|WBP_Stage|GetInputBox)))))
      (bind _m0 (CallFunction|MaxWords))
      (CallFunction|SyncCount :N _n0 :Max _m0)
      (set FaceRowOn true)
      (Widget|SetVisibility :self (Variables|WBP_Stage|GetLowerSize) :InVisibility "SelfHitTestInvisible")
      (Layout|SizeBox|SetWidthOverride :self (Variables|WBP_Stage|GetLowerSize) :InWidthOverride (V LowerWide)))))
```

Notes:

- **Keep every T64, T65, T66 and T78 line** (T66.md and T78.md ask for it): `TimerSize` collapsed, `TimerOn` and `TimerWide` false; `FaceRowOn`/`FaceShownV` false, `FaceSize` collapsed, `FaceShow(false)`, `ResetFace`; `FaceRowOn` true on the play side. The draft has them all in their old order.
- `"SelfHitTestInvisible"` for `LowerSize` is a guess: use the design-time value part 0 recorded, in both places. A `SizeBox` that was `Visible` would block clicks on the stage under it, so don't change the value, only restore it.
- **Why the width goes after `FitBuilder`:** in prep `FitBuilder` sees the builder closed and `TimerWide` false, so if `FitWide` was true it sets `LowerWide` (1080). Setting `LowerPrep` after it wins, and `FitBuilder` touches the width again only when `_wide` changes, which can't happen in prep (the builder is closed and the timer is off). On the play side `_wide` starts false, so `FitBuilder` wouldn't restore 1080 by itself until the builder opens; the last line does it.
- `_n` is bound once at the top so both branches can read it (the play branch doesn't need it). If the DSL rejects an unused bind in a branch, move the bind inside `(if Prep`.
- `ChatShown` stays as it is: in scene 1's prep the chat is hidden anyway (T38: hidden at every show's start), and in scenes 2 on it is open or closed as I left it.
- With question 1's "Hide it in every Scene Prep": drop the inner `(if (<= _n 1)` and collapse `LowerSize` in every prep; drop `LowerPrep`.
- Autoplay calls `StartFromPrep` in the same frame as `OpenPrep` (T47's note), so `SetPrepMode(true)` then `(false)` run back to back: the lower panel ends shown at 1080.

**After T88:** T88 doesn't change this file by its plan (re-check 2).

## 4. `BP_Show`: `PrepPrompt.txt` (step 5)

As pushed (before T88) the turn line is "Read the card on the right: the scene, your role, the note's category, the cast and the stage. Press Start the scene when you are ready." **After T88** it reads "… the note's clue …" (T88-build 5d). T84 writes:

```lisp
; T28: the turn line during Scene Prep. UpdatePrompt calls it after ComputePrompt and before LinePrompt.
; T58: then LastWordPrompt sets the turn line during the last words.
; T88: "the note's clue".
; T84: the scene sits in the middle panel now, my part and the clue stay on the card on the right, and the hint names
; the scene (the greyed field shows it in scenes 2 on).
(fn PrepPrompt ()
  (if (and (Variables|Default|GetReady) (Utilities|String|EqualExactly(String) (Variables|Default|GetPhase) "scene prep"))
    (Variables|Default|SetPTurn "Read the scene in the middle, then your role and the note's clue on the right. Press Start the scene when you are ready.")
    (Variables|Default|SetPHint "Read the scene first."))
  (CallFunction|LastWordPrompt))
```

- Keep whatever comment line T88 wrote (the draft's "; T88: …" stands in for it).
- 120 characters, against 136 for today's line, which fits the header in two lines at 1600 × 900; check it at 1280 × 720 in part 6. T85 adds a hint about the cast to this line later ("Point at a robot to see its role and want."), so a shorter line leaves it room.
- The cast stays on the card in T84 (T85 takes it off), but the line doesn't name it: T85's hint will. If my person wants it named until T85, use "… then your role, the note's clue and the cast on the right. …".
- `PrepPrompt` has a source (T28), so write the whole graph with `write_graph_dsl`, or set the two pin values in the editor (T50 did the first that way); either way `Graphs/BP_Show/PrepPrompt.txt` gets this text.
- Decision 5 changes the hint; if my person says no, keep "Read your card first.".

## 5. The design doc (step 7; question 2)

Read at Rules rev 59 and Art Inspiration rev 41. Nothing was changed. Each edit names its node id. Show my person the whole set (question 2) and, after the OK, make the edits in the Markdown files (re-check 6), in T84's commit.

**Where these places are now (T90):** the node ids and revisions in this part are from the old Claude Doc. In `Docs/Design/Rules.md`, `.8385` is the last bullet under "## Scene Prep", `.8620` the first bullet under "## The Scene & acting", and `.6880` the Scene Prep row of the table under "### What the player sees, and when". In `Docs/Design/ArtInspiration.md`, `.7488` (Your part), `.7995` (Input row) and `.7754` (Chat) are rows of the table under "#### Components", `.12156` is the paragraph under the layout picture in "#### Layout", `.9853` and `.9884` are the Scene Prep row of the table under "#### Screens", `.10448` is the first bullet under "#### Motion and rules", and `.11890` is item 5 under "#### Fix first".

### 5a. Rules tab, Scene Prep, the pause (`.8385`)

- Old: "Scene Prep is a pause. Your screen shows the whole card: the scene, your role and your want, the note’s clue, the cast with their roles and wants, and the stage’s places and props. The scene starts when you press Start the scene."
- New: "Scene Prep is a pause. The scene and the stage’s places and props show in a panel in the middle of your screen, with Start the scene under them. Your card on the right shows your role and your want, the note’s clue, and the cast with their roles and wants. The scene starts when you press Start the scene."
- Left as it is: "During the scene, your screen shows only your own card: your role, your want and the note’s clue." (`.8620`, still true). The onboarding table's Scene Prep row (`.6880`, "Scene card: story, your role, …") still lists what I see; leave it.

### 5b. Art Inspiration tab

1. **Your part, Behavior** (`.7488`). Old: "Scene Prep shows the full call sheet in the center. When the scene starts, it shrinks into the corner, so you see where it went." New: "In Scene Prep, the scene and the stage show on an ink panel in the lower middle, under the robots’ feet, with Start the scene under them; your part and the note’s clue stay on the card. When the scene starts, the panel goes and the card stays."
2. **Input row, Look** (`.7995`), its last sentence. Old: "The panel is 1080 wide in every phase." New (question 1's recommendation): "The panel is 1080 wide in every phase but Scene Prep, where it is 640 wide and holds only Show chat and the greyed field. In scene 1’s Scene Prep it is hidden, with the chat." (With "Hide it in every Scene Prep": "The panel is 1080 wide, and hidden in Scene Prep.")
3. **Layout** (`.12156`). Old: "The input row sits bottom left, with the chat above it when you open it. Your part sits top right, and the robots own the band between them. …" New: insert after the second sentence: "In Scene Prep, the scene sits on a panel at the bottom, in the middle, with Start the scene under it."
4. **The screens table, Scene Prep row** (`.9853`, "See first"). Old: "Your part and the secret note". New: "The scene in the middle, then your part and the note’s clue". ("Do next", `.9884`, "Start the scene", stays.) "Secret note" was already out of date (T50).
5. **Motion times** (`.10448`). Old: "Motion times: hovers and presses 120 ms; panels in and out 250 ms, easing out; the call sheet shrinks to its corner in 400 ms." New: "Motion times: hovers and presses 120 ms; panels in and out 250 ms, easing out." (decision 6)
6. **Left as they are:** the "Fix first" item "The scene premise fills the card during play. Show it in Scene Prep only; …" (`.11890`: a list of the 2026-11-14 playtest's faults, and T84 does what it asks); the Chat row (`.7754`, still true: the chat is hidden at each show's start). The tab's layout picture ("In-show screen layout", now `Docs/Design/images/ArtInspiration/layout.svg`) is T34's to redraw (T38's note).

### 5c. My person's answer to question 2

Not asked yet. Copy the answer here and under Findings in `T84.md`.

## 6. The checks (Done when)

Close every game window before a save (T53, T63). Set `autoplay` back to false at the end.

1. **Compile** `WBP_Stage` and `BP_Show` with warnings as errors; trace `SetPrepMode` and `PrepInit` from their entries (T63: no stale call nodes). `is_dirty` false for every other asset.
2. **PIE by hand** (Test for Free, autoplay off, a 1600 × 900 floating window, clicks through the Slate inspector, as the plan's "Claude does the playing" says). With **T88's longest clue forced** (`"clue": "pig_latin"` in `Local/switches.json`; restart until the `SETUP` line names `note=hold_prop`, T88-build 6c) so the card is at its tallest. Screenshots:
   - `prep1_p16`: scene 1's Scene Prep. The scene and the stage in the middle panel, Start the scene centered under them, **no lower panel** (no Show chat, no field, no hint), the card on the right with **no scroll bar** (my part, the clue, the cast).
   - `prep2_p16`: scene 2's Scene Prep, once with the chat hidden and once open (`prep2open_p16`). The 640 panel on the left with Show chat and the greyed field ("Read the scene first."), clear of the middle panel; no Start the scene in the row.
   - `turn1_p16`: scene 1's first turn. The middle panel gone, the lower panel back at 1080, the builder and the chip as before.
   - The same four at 1280 × 720 (`*_p12`).
   - The longest scenes: "The Ring Is Mine, I Mean Ours" and the scene of T32's `p16_prep2_long.png`, in Scene Prep at both sizes (restart until the `SETUP` line names them): no scroll, no clipped text.
   - Check each: no robot, name tag, held prop or speech bubble behind the middle panel (T27); the panel clear of the header, the clapperboard, the card and the chat column; the turn line in two lines in the header.
3. **The click:** a click on Start the scene in the middle prints `NHOS: PREP start scene=1` and then the same `NHOS:` lines as part 0's "before" run (turn 1's `STATE`/`TURN` lines in the same form). A second click does nothing (`StartFromPrep`'s phase check). Also Play Again from the end screen if a show ends in the PIE session (or call `ClearLog` and restart as T38 did): scene 1's prep has no lower panel again.
4. **T61's earpiece:** on a first show (no `Local/progress.json`, or the tips toggle on), scene 1's Scene Prep plays the stagehand's tip at T61's stage spot. Take `prep1_tip_p16` and write in Findings what it covers (part 7). Don't move it.
5. **A free autoplay show in a game window** on the saved assets (`mode: free`, `autoplay: true`, `fast_lines: true`, `clue` back to `""`): reaches `NHOS: SHOW END` with no new `LogScript` warning, and every `PREP shown` has its `PREP start`.
6. **Findings** in `T84.md`, as a critical first-time player: is the reading order clear (the scene, then my part and the clue, then Start the scene)? Does anything look empty (the wide-open bottom left in scene 1's prep) or crowded (the card with the cast and a five-line clue)? What is left for T34 (the card's ranking, T34-build 2.9), T85 (the hover card must keep clear of `PrepSize`) and T61 (part 7).

## 7. For T61: where the earpiece can go (step 6; write it under Findings, change nothing)

- `WBP_Earpiece`'s "stage" spot is one `Edge` (24) from the bottom, `StageX` 112 right of center, 560 to 720 wide (T61's findings): about x 712 to 1432 at 1920 wide. That is right where the middle panel sits (part 2c, about x 693 to 1373), so on the first show the Scene Prep tip covers the stage lines and Start the scene while it holds.
- **Where it can go in Scene Prep:** in scene 1's Scene Prep (the only Scene Prep with a tip, T88 decision 10) the bottom left is empty now (no lower panel). A "prep" spot at the bottom left (left edge at `Edge` 24, the same bottom line) is clear of the middle panel by about 100 px with a 560-wide earpiece. T61 would add that spot to `WBP_Earpiece.SetSpot` and pass it for the `scene_prep` moment in `BPC_Stagehand`. Measure from `prep1_tip_p16` and write the numbers.
- **Seen in passing (not T84's):** in the scene's phases the lower panel is 1080 wide since T38 (x 24 to 1104), so T61's stage spot (from x about 712) overlaps it in every tip after Scene Prep too. T61 set `StageX` when the panel was 640. Say so in Findings for T61 and T34.

## 8. `T32.md` row 13 (step 8)

In "T32: UI audit", row 13's last column (today "T34") becomes "done by T84 (`prep1_p16.png`, `prep2_p16.png`, `prep1_p12.png`, `prep2_p12.png`)" plus "the card's ranking: T34". T34-build 2.9 already says T84 and T85 replace its recommendation; it is T34's file, so T84 doesn't edit it.

## 9. The commit

One commit for T84, as "How to run a task" in the plan lists: `Content/NHOS/UI/WBP_Stage.uasset`, `Content/NHOS/Core/BP_Show.uasset`, `Graphs/WBP_Stage/SetPrepMode.txt`, `Graphs/WBP_Stage/PrepInit.txt` (new), `Graphs/BP_Show/PrepPrompt.txt`, `Docs/tasks/T32.md`, `Docs/tasks/T84.md`, `Docs/Plan.md` (the box and the "Next up" line), `Docs/DevLog.md`. Unlock both Blueprints and the claim after the push. `PrepInit.txt` is new, so it is not in T84's Touches line: say so in the commit message.

## 10. Knock-ons: tell, don't change

- **T85** (the cast's hover cards): the card keeps `CastTitle` and `CastBox` in `PrepBox` until T85; the hover card must keep clear of `PrepSize` (part 2c's spot) in Scene Prep. After T85, `PrepBox` holds nothing, and its `SetPrepMode` line can go.
- **T34:** `StartButton` now sits in `PrepPanelBox`, centered. T34-build 1b's `StartRing` wraps it there (padding 0), and `SetPrepMode(true)` is where it takes focus. The lower panel's width in prep (`LowerPrep`) and `FitBuilder`'s dead width branch (T38's note) are T34's to tidy. The card's ranking (2.9) is now only my part, the clue and the cast.
- **T61:** part 7.
- **T86** (the floor): in scene 1's Scene Prep more floor shows at the bottom left now (T86 step 1 already expects it).
- **T90:** done first. Re-check 6 and part 5 now point at the files in `Docs/Design/`.
