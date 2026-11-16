# T85 build sheet: the cast's roles and wants show when I point at a robot

Back to [T85](T85.md). A PC prep session wrote this on 2026-11-15, without the editor. It is a plan, not a record: nothing here was written to the editor, the design doc or any data file. When T85 writes a graph, its source goes to `Graphs/` as usual.

## Written against, and what to re-check first

**Written against `noHumansOnSet` at `a966b83`** (Plan: add T89), and checked against **T84's build sheet as pushed in `120c98d`** ("T84 prep: build sheet for Scene Prep's middle panel"), whose names and text this sheet uses: the middle panel is `PrepSize` (SizeBox) > `PrepPanel` (Border) > `PrepPanelBox` (VerticalBox), right after `LowerSize` in `RootBox`; `StartButton` moves into `PrepPanelBox`; `PrepBox` keeps only `CastTitle` and `CastBox`; T84's turn line is in part 4c below. The design doc was read, not changed: Rules tab rev 59, which already holds T88's clue edits (the Scene Prep bullets `.843`, `.4947`, `.11074`, `.8385` and the onboarding row `.6880` say "clue"). T88 and T84 are not built yet. T90 (added in `4150a0b`) moves the design doc into the repo as Markdown; if it has landed, part 6's edit goes into those files instead.

**T85 comes after T88 and T84.** Every step below says what they will have changed under it. Before T85 writes anything:

1. **What landed since `a966b83`.** `git log --oneline a966b83..HEAD -- Graphs/BP_Show Graphs/WBP_Stage Graphs/BP_Robot Graphs/BPC_LinePlayer Docs/tasks/T84* Docs/tasks/T88*`. Each item marked **re-check (T84)** or **re-check (T88)** below is where it matters:
   - `Graphs/BP_Show/PrepPrompt.txt` (part 4c). T88 changes "the note's category" to "the note's clue"; T84 rewrites the whole turn line for the middle panel. T85 adds one sentence to whatever T84 left.
   - `Graphs/BP_Show/OpenPrep.txt` (part 4a). Neither T84 nor T88 names it, but read it again.
   - `Graphs/WBP_Stage/SetPrompt.txt` (part 3c: one call added at its end). T84 should not change it; check.
   - `Graphs/WBP_Stage/SetPrepMode.txt`. **T85 doesn't change it** (the switch is read from `TipTick`, part 3d, so that T84's new version stays T84's). Read it for what shows in Scene Prep.
   - `WBP_Stage`'s tree. T84 adds the middle panel (`PrepSize` > `PrepPanel` > `PrepPanelBox`, T84-build part 2; check the names T84 actually used in `T84.md`'s Result), moves `SceneTitle`, `SceneText`, `SetTitle`, `PlacesText`, `PropsText` into it and moves `StartButton` under it, and collapses the whole lower panel in scene 1's Scene Prep. T88 adds `ClueText` to my card's note box (the card gets up to five lines taller). After both, `PrepBox` on the card holds only `CastTitle` and `CastBox`.
   - `T84.md`'s Findings: where T61's earpiece can go (T84-build part 7 suggests a "prep" spot at the bottom left in scene 1's Scene Prep). Add `PrepSize` and the earpiece (if T61 has placed it in `WBP_Stage` by then) to the keep-out list (part 3e).
   - T84's question 1 (the lower panel in the Scene Preps of scenes 2 on, 640 wide or hidden): either way `LowerSize` drops out of the keep-out list when it is collapsed, so nothing here changes.
2. **The graphs with no file** that T85 reads in the editor (part 0): `BP_Show.StageSetup`, `StartScene`, `ShowPrep`, and `WBP_Stage.ShowCast`. Check that nobody wrote a file for them since.
3. **T34-build 2.1** (the name tags drawn in screen space) is T34's, after T85. Nothing to re-check; part 7 tells T34 what it can reuse.
4. **The design doc.** Read the Rules tab again. T84 rewrites the Scene Prep bullet `.8385`; question 1's edit is written as a change to whatever T84 left (part 6).

## In short

| T85 step | Where in this sheet |
|---|---|
| 1. Names in Scene Prep | Part 4a (`OpenPrep` calls `StageSetup` in scene 1), part 4b (`StartScene` loses its call) |
| 2. A hover card | Part 2 (`WBP_CastTip`), part 3 (`WBP_Stage`: `TipLayer`, `TipTick`, `RobotRect`, `TipPick`, `TipFill`, `TipPlace`, `TipFit`) |
| 3. Not for me, not for the cut | Part 3f (`TipPick`'s eligibility) |
| 4. In every phase | Part 3d (`TipTick`'s guards: any phase while the stage widget shows) |
| 5. Which robot is under the mouse | Part 1 (what the code has today), part 3f (`RobotRect`, `TipPick`) |
| 6. The cast leaves the card | Part 3b (`CastTitle`, `CastBox` collapsed; `ShowCast` kept) |
| 7. Tell me it's there | Part 4c (`PrepPrompt`) |
| 8. A check line | Part 3d (`NHOS: CASTTIP <seat id>` once per show of a card) |
| 9. The design doc | Question 1, part 6 |
| Test switch | Part 5 (`cast_tip`, recommended in addition to a real hover) |
| Checks | Part 8 |

- **One new widget, `WBP_CastTip`**, and one new layer in `WBP_Stage` that holds it. `WBP_Stage` finds the robot under the mouse each frame from `SetPrompt` (which `BP_Show.UpdatePrompt` calls on every tick), fills the card from `BP_Show`'s seat arrays and places it beside the robot with the same fit rule as T38's speech bubble.
- **No `BP_Robot` change.** The robot's screen box comes from its actor location (the feet) and its `Label` component (over the head, raised by T47's hats), projected to the screen.
- **`BP_Show` changes three small things:** `OpenPrep` (a file) runs `StageSetup` in scene 1's Scene Prep, `StartScene` (no file) loses its `StageSetup` call, and `PrepPrompt` (a file) gets the hint.
- **Locks:** `Content/NHOS/UI/WBP_Stage.uasset`, `Content/NHOS/Core/BP_Show.uasset`; new `Content/NHOS/UI/WBP_CastTip.uasset`.
- **Costs money:** nothing. Every run is free (PIE in Test for Free, free autoplay).

## Questions for my person

One question, asked on its own with the multiple-choice tool, the recommendation first, once T84's doc edit is in (so the text is final). T85's Needs line asks for it.

1. **The design doc edit** (part 6), with the full text. Options: "OK the edit (Recommended)", "OK, but only the Scene Prep bullet", "Change the wording".
   - **My recommendation:** OK the edit. It says what the screen does in both places the doc lists what my screen shows (Scene Prep and the scene), so neither bullet lists the cast on my card any more.

**Not asked, decided here (open to change):** the test switch is added (part 5), because computer use alone can't pose every robot at both screen sizes; one real hover with computer use is still part of the check.

## Decisions this sheet makes (open to change)

1. **The hover test runs in `WBP_Stage`, from `SetPrompt`,** as T85 step 5 recommends: project each robot to the screen and test the mouse against it. No collision box and no cursor trace, so no widget can swallow it, and `WBP_Stage`'s full-screen panels need no change.
2. **The card reads `BP_Show`'s seat arrays,** not `ShowCast`'s rows: `SeatLabel` (the screen name), `SeatColors` (through `UIStyle.SeatColor`, as T34-build 2.10 wants), `SeatRole`, `SeatWant`, `SeatId`, `SeatCut`, `HumanSeat` and `Robots`, all indexed by seat. The wording of the role and want lines is copied from `ShowCast` (part 0), so the card says what the cast list said.
3. **`ShowCast` stays,** still called by `ShowPrep` and `CutActor`, and still fills `CastBox`, which is collapsed. Nothing reads it any more; T34 can delete it with the rows.
4. **The robot's screen box** is the rectangle from the label's top (the `Label` component's world location plus 30 cm: the name's height, 24, and a little room) down to the feet (the actor location), and 45 cm either side of the body's center line, measured along the camera's right vector. Overlapping boxes (robots standing close): the robot nearest the camera wins.
5. **No card while the mouse is over a panel** (the header, the clapperboard, my card, the lower panel, the banner, the stamp, the face list, the @ list, T84's panel). The robots are never behind a panel (T27), so this only stops a card popping up while I read the card or type.
6. **The card goes on the side of the robot toward the screen's middle,** with its top at the label's top, then the bubble's fit rule moves it inside the window's `Edge` margin and clear of every panel. If that puts it over its own robot, it goes to the other side. It never takes a click (`HitTestInvisible`).
7. **It follows the robot** each frame while shown (a robot walking in a scene turn), and hides the frame the mouse leaves the box. "Within about 0.1 s" is one frame.
8. **`NHOS: CASTTIP <seat id>` prints when a card appears or changes to another robot.** Moving the mouse within one robot's box prints nothing; leaving and coming back prints again.
9. **The guards:** no card before the show is `Ready`, before scene 1, or while `WBP_Stage`'s render opacity is under 0.5 (the title and end screens set it to 0, T33). So the card works in Scene Prep, the scene, Free Talk, the last words, the vote, the reveal and the reactions.
10. **Step 1 moves `StageSetup`, it doesn't copy it.** `OpenPrep` calls it when `SceneNum` is 1 and `StartScene` no longer does, so a show prints one `NHOS: STAGE robots=<n>` (now before `NHOS: PREP shown scene=1`), and no robot is set up twice. `Tools/check_prompts.py` reads no `STAGE` line (checked at `a966b83`).

## 0. Before you start (read only)

1. Do the four checks in "Written against". `git lfs locks`: no one holds `BP_Show.uasset` or `WBP_Stage.uasset`. Claim T85 and lock both, as the plan says. Pull, and reload both packages if the pull changed them (the memory "Editor stale after a pull").
2. **`BP_Show.StageSetup`** (no file): `read_graph_dsl` and `get_node_infos`. Record what it reads (expected, from T11 and T17: `FindRobots`, then for each seat `Setup(SeatLabel, SeatColors[seat], seat == HumanSeat)` and `SetPersona(SeatId)`, then `NHOS: STAGE robots=<n>`). **Everything it reads must be set by the time `OpenPrep` runs:** the seats (`SetupShow`), `SeatLabel`, and `SeatColors` (`StagePrep`, which `ShowPrep` runs inside `ScenePrep` before `OpenPrep`). If it reads something `StartScene` sets first (for example `OnStage`), stop and use part 4a's fallback.
3. **`BP_Show.StartScene`** (no file): `find_nodes` with title `StageSetup` (titles match with no spaces, T28). Record the node, the branch it sits in (expected: a `SceneNum == 1` branch, as T47 found it runs once a show), and the exec pins on each side.
4. **`WBP_Stage.ShowCast`** (no file): read it. Record the exact strings it builds for each entry: the name (`SeatLabel`, or from `BP_Show.Cast`), the role line and the want line (it calls `WBP_ChatLine.SetActor(Name, Color, Action, Speech, IsMe)`; most likely the role goes in `Action` and the want in `Speech`), and whether it skips my seat. `TipFill` (part 3g) copies those strings. Also `find_nodes` for `CastBox` and `CastTitle` in `WBP_Stage` and `BP_Show`: if anything sets their visibility at run time, part 3b must change that node too.
5. **Getters from `WBP_Stage`:** `find_node_types` with the `BP_Show` class as context for `GetSeatWant`, `GetSeatCut`, `GetSeatColors` and `GetReady`. `GetSeatLabel`, `GetSeatId`, `GetSeatRole`, `GetHumanSeat`, `GetRobots`, `GetSceneNum` and `GetPhase` are already called from other Blueprints. If a variable is private, read it the way `ShowCast` reads it.
6. **The node names this sheet guesses** (no graph in `Graphs/` uses them yet). Look each one up with `find_node_types` and fix the draft before you write:
   - `Viewport|ProjectWorldLocationtoWidgetPosition` (WidgetLayoutLibrary: `PlayerController`, `WorldLocation`, `bPlayerViewportRelative`; out `ScreenPosition` and the bool). Its output order in a `bind` may be (bool, position) or (position, bool).
   - `Viewport|GetMousePositionOnViewport` (WidgetLayoutLibrary; the mouse in the same DPI-scaled viewport units).
   - `Game|GetPlayerCameraManager`, `Class|PlayerCameraManager|GetCameraLocation`, `GetCameraRotation`, `Math|Rotator|GetRightVector`.
   - `Transformation|GetActorLocation :self <robot>` and `Transformation|GetWorldLocation :self <component>`.
   - `Widget|ForceLayoutPrepass`, `Widget|GetDesiredSize`, `Widget|GetRenderOpacity`.
7. **The robots' feet.** In PIE, read one robot's actor location and the floor's height (`BP_PlaceMark` or the stage floor). If the actor's origin is not at the floor, add the difference to `RobotRect`'s feet point.
8. Reading a Blueprint marks it dirty (T47): check `AssetTools.is_dirty` and reload if you must not save yet.

## 1. What the code has today (so T85 doesn't look for it)

- **No graph projects a robot to the screen yet.** T85.md step 5 suggests `BP_Robot.PlaceCorners` and `ScreenX`: they are face shapes, not screen math. `PlaceCorners(W)` bends the mouth's corner bars (T75); `ScreenX(Y, Z)` is how far forward the head's surface is at a point on the face (T75, T82). Neither helps.
- **What does help:** T38's bubble.
  - Each robot's `Label` (a world-space TextRender over the head) is where the bubble anchors (`InitBubble`, `BubbleLift`: the anchor is 26 cm over the label, 50 with "(passed)"). T47's hats raise the label (`InitLift` puts `Label` in `LiftComps`), so the label tracks each robot's real top. OpenAI's 8 cm hover is in it too.
  - `WBP_SpeechBubble.Place` measures the window and the panels in viewport units with `GetCachedGeometry` and `LocaltoViewport`, the same units `ProjectWorldLocationtoWidgetPosition` gives. `WBP_SpeechBubble.Fit` moves a rect inside the margin and clear of the panels. Part 3h copies `Fit` without the tail.
  - `BPC_LinePlayer.BubbleKeep` lists the panels: the header (`TurnText`'s third parent), `ClapperBox`, my card (`MeText`'s fourth parent), `LowerSize`, `EventBanner` and `StampText`. `RootBox` is a `WBP_Stage` variable after all (`Variables|WBP_Stage|GetRootBox`), though `BubbleKeep` walks up to it.
- **The robots and the seats:** `BP_Show.Robots` has one slot per seat, up to `MaxCast` (empty slots are None), filled by `FindRobots` inside `StageSetup` (T11). Today `StageSetup` runs once a show, in scene 1's `StartScene`, so **in scene 1's Scene Prep `Robots` may still be empty** and every label reads "ROBOT". Part 4a fixes both.
- **Names and colors:** `BP_Robot.Setup(Name, Color, IsMe)` sets `DisplayName` and `ResetLook` writes it into the label; `SetPersona(Id)` sets the body's seat color. `SeatColors` comes from `StagePrep` (in `ShowPrep`).
- **Cut:** `BP_Robot.IsDown()` returns `IsCut` (set by `SetCut`); `BP_Show.SeatCut[seat]` is set by `CutActor`.
- **Each frame:** `BP_Show.UpdatePrompt` (Event Tick) → `ComputePrompt` → `PrepPrompt` → `LinePrompt` → `WBP_Stage.SetPrompt(PTurn, PHint, PCan)` (T14, T28, T30). `SetPrompt` already calls `SyncAction`, `FitBuilder`, `HoldFocus`, `TickTimer` and `SyncFace` every frame.
- **Pop-ups to keep clear of:** `FacePop` (T78: over the face chip at the lower left, up to about 250 tall) and `AtPop` (T65's @ list over the input box). Both are `WBP_Stage` variables.

## 2. `WBP_CastTip` (new, `Content/NHOS/UI/WBP_CastTip.uasset`)

### 2a. The tree

Parent class `UserWidget`. Every widget below is a variable.

- `Panel` (Border, root). Padding `S4` × `S3`. Visibility `HitTestInvisible`.
  - `TipBox` (VerticalBox)
    - `NameRow` (HorizontalBox)
      - `Accent` (Border, vertical center) > `AccentSize` (Spacer): the seat-color square, as `WBP_ChatLine`'s accent.
      - `NameText` (TextBlock, left padding `S2`).
    - `RoleText` (TextBlock, top padding `S1`, Auto Wrap Text on).
    - `WantText` (TextBlock, top padding `S1`, Auto Wrap Text on).

No SizeBox: the text wraps at `WrapAt` (360, the widget's own variable; UIStyle has no wrap width, as T38 found for the bubble), so the card is at most about 400 wide.

### 2b. Variables

`WrapAt` (Float, 360).

### 2c. `EventGraph`

```lisp
; T85: the hover card styles itself from UIStyle when it is built, and starts hidden (WBP_Stage shows it).
(event UserInterface|EventConstruct
  (CallFunction|ApplyStyle))
```

### 2d. `ApplyStyle.txt`

```lisp
; T85: every look comes from UIStyle, like the card on the right and the chat lines: an Ink panel with old-gold trim
; (the running talk's panel, so it reads as part of the stage, not as my card), the name in the Name font in its seat
; color with the seat bar, the role in the Action style (quiet italic) and the want in Body white. WrapAt is the
; widget's own (UIStyle has no wrap width).
(fn ApplyStyle ()
  (Class|UIStyle|StylePanel :Panel (Variables|WBP_CastTip|GetPanel) :Look "Ink")
  (bind s1 (Class|UIStyle|UISize :Role "S1"))
  (bind s2 (Class|UIStyle|UISize :Role "S2"))
  (bind s3 (Class|UIStyle|UISize :Role "S3"))
  (bind s4 (Class|UIStyle|UISize :Role "S4"))
  (bind bar (Class|UIStyle|UISize :Role "SeatBar"))
  (Class|Border|SetPadding :self (Variables|WBP_CastTip|GetPanel) :Padding (Utilities|Struct|MakeMargin s4 s3 s4 s3))
  (Class|Spacer|SetSize :self (Variables|WBP_CastTip|GetAccentSize) :Size (Math|Vector2D|MakeVector2D bar bar))
  (Class|Text|SetFont :self (Variables|WBP_CastTip|GetNameText) :Font (Class|UIStyle|UIFont :Role "Name"))
  (Class|Text|SetFont :self (Variables|WBP_CastTip|GetRoleText) :Font (Class|UIStyle|UIFont :Role "Action"))
  (Class|Text|SetFont :self (Variables|WBP_CastTip|GetWantText) :Font (Class|UIStyle|UIFont :Role "Body"))
  (Class|Text|SetColorandOpacity :self (Variables|WBP_CastTip|GetRoleText) :ColorAndOpacity (Utilities|Struct|MakeSlateColor :SpecifiedColor (Class|UIStyle|UIColor :Role "Quiet")))
  (Class|Text|SetColorandOpacity :self (Variables|WBP_CastTip|GetWantText) :ColorAndOpacity (Utilities|Struct|MakeSlateColor :SpecifiedColor (Class|UIStyle|UIColor :Role "Text")))
  (Class|TextLayoutWidget|SetWrapTextAt :self (Variables|WBP_CastTip|GetRoleText) :WrapTextAt (V WrapAt))
  (Class|TextLayoutWidget|SetWrapTextAt :self (Variables|WBP_CastTip|GetWantText) :WrapTextAt (V WrapAt)))
```

- `UIFont "Body"` is the role T88's `SetClue` uses for the card's body; if `Graphs/UIStyle/UIFont.txt` names it otherwise, use what `RoleText` on my card uses.
- If `ShowCast` styles its rows differently (part 0, step 4), follow `ShowCast`: the card must read like the cast entry it replaces.

### 2e. `Fill.txt`

```lisp
; T85: one robot's card. Name is its screen name (SeatLabel), Color the fallback for UIStyle.SeatColor (SeatColors),
; Role and Want the lines exactly as ShowCast wrote them in the cast list (WBP_Stage.TipFill builds them). An empty
; want hides its line.
(fn Fill (Name Color Role Want)
  (bind seat (Class|UIStyle|SeatColor :Name Name :Fallback Color))
  (Class|Border|SetBrushColor :self (Variables|WBP_CastTip|GetAccent) :BrushColor seat)
  (Class|Text|SetText :self (Variables|WBP_CastTip|GetNameText) :Text (Utilities|Text|ToText(String) Name))
  (Class|Text|SetColorandOpacity :self (Variables|WBP_CastTip|GetNameText) :ColorAndOpacity (Utilities|Struct|MakeSlateColor :SpecifiedColor seat))
  (Class|Text|SetText :self (Variables|WBP_CastTip|GetRoleText) :Text (Utilities|Text|ToText(String) Role))
  (Class|Text|SetText :self (Variables|WBP_CastTip|GetWantText) :Text (Utilities|Text|ToText(String) Want))
  (Widget|SetVisibility :self (Variables|WBP_CastTip|GetWantText) :InVisibility (select (Utilities|String|IsEmpty Want) "Collapsed" "HitTestInvisible")))
```

- The seat color as text on Ink: the chat already shows the names that way (`WBP_ChatLine.SetActor`), so the contrast is the chat's. Check Meta's blue in the screenshots; if it reads dark, use the chat's YOU-tag look (a seat-color pill with `InkSolid` text, `TagRadius`) for every name.

## 3. `WBP_Stage`

### 3a. The tree: `TipLayer` and `CastTip`

- **`TipLayer`** (CanvasPanel), the **last** child of `RootBox` (the overlay that fills the window), horizontal and vertical Fill, Visibility `HitTestInvisible`, Is Variable on. Last, so the card draws over the panels it keeps clear of anyway and over the stage. `UMGToolSet.AddWidget` takes the blueprint as `/Game/NHOS/UI/WBP_Stage.WBP_Stage` (T78).
- **`CastTip`** (a `WBP_CastTip`) in `TipLayer`: canvas slot anchors (0, 0), alignment (0, 0), position (0, 0), Size To Content on, Visibility `Collapsed`, Is Variable on. `TipPlace` moves it with its render translation (as the bubble moves `BubbleBox`), so the slot never changes.
- **re-check (T84):** T84 adds `PrepSize` right after `LowerSize` in `RootBox` (T84-build 2a); `TipLayer` still goes last, after it. If part 0 of T84 found `RootBox` is a CanvasPanel, not an overlay, `TipLayer`'s slot gets anchors (0, 0)–(1, 1) with zero offsets instead of Fill.

### 3b. The cast leaves the card (step 6)

- Set `CastTitle` and `CastBox` to `Collapsed` in the designer.
- **re-check (T84):** after T84, `PrepBox` holds only these two (T84-build 2b). Leave `PrepBox` and its line in `SetPrepMode` alone; with both children collapsed it draws nothing. T84-build part 10 says the `SetPrepMode` line can go after T85: leave that to T34, which rebuilds the card, so T85 doesn't rewrite T84's `SetPrepMode`. If `PrepBox` has padding that leaves a gap under the note box in Scene Prep, set its padding to 0 and say so.
- **re-check (T88):** my card in Scene Prep then holds `YouAre`, `MeText`, `RoleText`, `WantText` and the note box with T88's `ClueText`. Check with T88's longest clue (`"clue": "pig_latin"` on `hold_prop`) that the card has no scroll bar at 1600 × 900 and 1440 × 900 (T85's Done when; T88-build 6c and 12.1).
- If part 0 step 4 found a node that sets `CastBox` or `CastTitle` visible at run time, change it to `Collapsed` too.

### 3c. `SetPrompt.txt` (file edit)

Add one line at the end, after `SyncFace`, and one comment line at the top:

```lisp
; T85: the cast's hover card follows the mouse over the robots (TipTick).
...
  (CallFunction|SyncFace :CanType CanType)
  (CallFunction|TipTick))
```

Write the whole graph from the file with `write_graph_dsl` (it has a source) or add the node by hand; either way the file gets the change.

### 3d. `TipTick.txt` (new)

```lisp
; T85: the cast's hover card, each frame from SetPrompt. When the mouse is over an AI robot on stage (its box from
; RobotRect), that robot's card shows beside it; it hides when the mouse leaves. Not my robot, not a cut one (TipPick).
; Nothing before the show is Ready, before scene 1, or while this widget is see-through (the title and end screens
; set its render opacity to 0). Local/switches.json's cast_tip keeps one robot's card shown (TipSwitch, read at each
; new scene). NHOS: CASTTIP <seat id> prints when a card appears or moves to another robot, not each frame.
(fn TipTick ()
  (CallFunction|ShowRef)
  (if (== (V Show) (V NullShow))
    (CallFunction|TipHide)
    (return))
  (bind _scene (Class|BPShow|GetSceneNum :self (V Show)))
  (if (!= _scene (V TipScene))
    (set TipScene _scene)
    (CallFunction|TipSwitch))
  (if (or (or (not (Class|BPShow|GetReady :self (V Show))) (< _scene 1)) (< (Widget|GetRenderOpacity :self self) 0.5))
    (CallFunction|TipHide)
    (return))
  (CallFunction|TipKeepRects)
  (bind _seat (CallFunction|TipPick))
  (if (< _seat 0)
    (CallFunction|TipHide)
    (return))
  (if (!= _seat (V TipSeat))
    (set TipSeat _seat)
    (CallFunction|TipFill :Seat _seat)
    (print (cat "NHOS: CASTTIP " (get (Class|BPShow|GetSeatId :self (V Show)) _seat))))
  (CallFunction|TipPlace :L (V BestL) :T (V BestT) :R (V BestR) :B (V BestB)))
```

**New variables on `WBP_Stage`:** `TipSeat` (Integer, −1), `TipScene` (Integer, −1), `TipForce` (String), `TipShown` (Boolean), `TipKeepW` (Widget array), `TipKTL`, `TipKBR` (Vector2D arrays), `TipVTL`, `TipVBR` (Vector2D), `BestL`, `BestT`, `BestR`, `BestB`, `BestD` (Float), `TipInPanel` (Boolean), `TipBest` (Integer), `TipHalfW` (Float, 45), `TipTopZ` (Float, 30), `TipRobot` (`BP_Robot` object reference), `TipSw` (Json object, for the switch), `TmpStr` (String; reuse one if `WBP_Stage` has it). `Show` and `NullShow` exist (T65's `ShowRef`).

### 3e. `TipKeepRects.txt` (new)

```lisp
; T85: the window and the panels the card keeps clear of, in viewport units (as WBP_SpeechBubble.Place measures them):
; the header (TurnText's third parent), the clapperboard, my card (MeText's fourth parent), the lower panel, the
; banner, the stamp, the face list and the @ list (BPC_LinePlayer.BubbleKeep's list, plus T78's and T65's pop-ups).
; The list is built once; the rects are measured each frame, only for the panels that show.
(fn TipKeepRects ()
  (if (== (len (V TipKeepW)) 0)
    (bind _h1 (Widget|GetParent :self (Variables|WBP_Stage|GetTurnText)))
    (bind _h2 (Widget|GetParent :self _h1))
    (bind _h3 (Widget|GetParent :self _h2))
    (bind _i1 (Widget|GetParent :self (Variables|WBP_Stage|GetMeText)))
    (bind _i2 (Widget|GetParent :self _i1))
    (bind _i3 (Widget|GetParent :self _i2))
    (bind _i4 (Widget|GetParent :self _i3))
    (add (V TipKeepW) _h3)
    (add (V TipKeepW) (Variables|WBP_Stage|GetClapperBox))
    (add (V TipKeepW) _i4)
    (add (V TipKeepW) (Variables|WBP_Stage|GetLowerSize))
    (add (V TipKeepW) (Variables|WBP_Stage|GetEventBanner))
    (add (V TipKeepW) (Variables|WBP_Stage|GetStampText))
    (add (V TipKeepW) (Variables|WBP_Stage|GetFacePop))
    (add (V TipKeepW) (Variables|WBP_Stage|GetAtPop)))
  (bind z (Math|Vector2D|MakeVector2D :X 0.0 :Y 0.0))
  (bind vg (Widget|GetCachedGeometry :self (Variables|WBP_Stage|GetRootBox)))
  (bind vs (UserInterface|Geometry|GetLocalSize :Geometry vg))
  (bind (vp0 vtl) (UserInterface|Geometry|LocaltoViewport :Geometry vg :LocalCoordinate z))
  (bind (vp1 vbr) (UserInterface|Geometry|LocaltoViewport :Geometry vg :LocalCoordinate vs))
  (set TipVTL vtl)
  (set TipVBR vbr)
  (clear (V TipKTL))
  (clear (V TipKBR))
  (for p (V TipKeepW)
    (if (Widget|IsVisible :self p)
      (bind pg (Widget|GetCachedGeometry :self p))
      (bind ps (UserInterface|Geometry|GetLocalSize :Geometry pg))
      (bind (pp0 ptl) (UserInterface|Geometry|LocaltoViewport :Geometry pg :LocalCoordinate z))
      (bind (pp1 pbr) (UserInterface|Geometry|LocaltoViewport :Geometry pg :LocalCoordinate ps))
      (add (V TipKTL) ptl)
      (add (V TipKBR) pbr))))
```

- **re-check (T84):** add T84's middle panel after `AtPop`: `(add (V TipKeepW) (Variables|WBP_Stage|GetPrepSize))` (T84-build 2a makes `PrepSize` a variable; it shows only in Scene Prep, and `IsVisible` handles that). `StartButton` is inside it (T84-build 2b), so it needs no line of its own.
- **re-check (T61):** if T61's chain has placed `WBP_Earpiece` in `WBP_Stage` by then, add it.
- **re-check (T34):** if T34 re-nests `TurnText` or `MeText`, this walk and `BubbleKeep`'s change together (T38's note).
- `Widget|IsVisible` is what the bubble uses; a collapsed lower panel in scene 1's Scene Prep (T84) drops out by itself.

### 3f. `RobotRect.txt` and `TipPick.txt` (new)

```lisp
; T85: a robot's box on screen, in viewport units: from its label's top (the Label component, which T47's hats raise,
; plus TipTopZ for the name's own height) down to its feet (the actor's location), TipHalfW cm either side of the line
; between them along the camera's right. D is the feet's distance from the camera, so the nearest robot wins an
; overlap. Ok is false when a point is behind the camera.
(fn RobotRect (Robot PC CamLoc CamRight)
  (bind _feet (Transformation|GetActorLocation :self Robot))
  (bind _lab (Transformation|GetWorldLocation :self (Class|BPRobot|GetLabel :self Robot)))
  (bind _top (+ _lab (Math|Vector|MakeVector :X 0.0 :Y 0.0 :Z (V TipTopZ))))
  (bind _side (+ _feet (* CamRight (V TipHalfW))))
  (bind (_pf _okf) (Viewport|ProjectWorldLocationtoWidgetPosition :PlayerController PC :WorldLocation _feet :bPlayerViewportRelative true))
  (bind (_pt _okt) (Viewport|ProjectWorldLocationtoWidgetPosition :PlayerController PC :WorldLocation _top :bPlayerViewportRelative true))
  (bind (_ps _oks) (Viewport|ProjectWorldLocationtoWidgetPosition :PlayerController PC :WorldLocation _side :bPlayerViewportRelative true))
  (bind _hw (Math|Float|Absolute(Float) (- (.x _ps) (.x _pf))))
  (bind _cx (* 0.5 (+ (.x _pf) (.x _pt))))
  (return (and _okf (and _okt _oks)) (- _cx _hw) (.y _pt) (+ _cx _hw) (.y _pf) (Math|Vector|Distance _feet CamLoc)))

; T85: the seat whose card shows, or -1. Only an AI robot on stage counts: not my seat (my part is on my card), not a
; cut seat or a fallen robot (the cast list dropped them too). With cast_tip set, that seat (TipForce); otherwise the
; robot whose box holds the mouse, the nearest one if boxes overlap, and none while the mouse is over a panel.
; The winner's box is left in BestL/T/R/B for TipPlace.
(fn TipPick ()
  (set TipInPanel false)
  (set TipBest -1)
  (bind _m (Viewport|GetMousePositionOnViewport :WorldContextObject self))
  (for i (range (len (V TipKTL)))
    (bind ktl (get (V TipKTL) i))
    (bind kbr (get (V TipKBR) i))
    (if (and (and (>= (.x _m) (.x ktl)) (<= (.x _m) (.x kbr))) (and (>= (.y _m) (.y ktl)) (<= (.y _m) (.y kbr))))
      (set TipInPanel true)))
  (bind _robots (Class|BPShow|GetRobots :self (V Show)))
  (bind _cut (Class|BPShow|GetSeatCut :self (V Show)))
  (bind _ids (Class|BPShow|GetSeatId :self (V Show)))
  (bind _me (Class|BPShow|GetHumanSeat :self (V Show)))
  (bind _pc (Game|GetPlayerController 0))
  (bind _cam (Game|GetPlayerCameraManager :PlayerIndex 0))
  (bind _cl (Class|PlayerCameraManager|GetCameraLocation :self _cam))
  (bind _cr (Math|Rotator|GetRightVector (Class|PlayerCameraManager|GetCameraRotation :self _cam)))
  (bind _force (not (Utilities|String|IsEmpty (V TipForce))))
  (set BestD 1.0e9)
  (for s (range (len _robots))
    (set TipRobot (get _robots s))
    (Utilities|IsValid (V TipRobot)
      (:"Is Valid"
        (if (and (and (!= s _me) (< s (len _cut))) (and (not (get _cut s)) (not (Class|BPRobot|IsDown :self (V TipRobot)))))
          (bind (_ok _l _t _r _b _d) (CallFunction|RobotRect :Robot (V TipRobot) :PC _pc :CamLoc _cl :CamRight _cr))
          (bind _hit (and (and (>= (.x _m) _l) (<= (.x _m) _r)) (and (>= (.y _m) _t) (<= (.y _m) _b))))
          (bind _want (select _force (streq (get _ids s) (V TipForce)) (and _hit (not (V TipInPanel)))))
          (if (and (and _ok _want) (< _d (V BestD)))
            (set BestD _d)
            (set BestL _l)
            (set BestT _t)
            (set BestR _r)
            (set BestB _b)
            (set TipBest s))))
      (:"Is Not Valid")))
  (return (V TipBest)))
```

- `TipInPanel` (Boolean) and `TipBest` (Integer) are variables, not `bind` locals, because the loops set them (a local can't be set in a loop, and a `bind` of a variable is read where it is used, T65). Add both to part 3d's list.
- `TipForce` matches a seat id (`SeatId`, what `NHOS: LINE` and `NHOS: CASTTIP` print). `TipSwitch` turns a screen name (`SeatLabel`, for example "Anthropic") into the id, so either works in the switch.
- `RobotRect` returns six values. If the DSL's multi-return `bind` gives trouble for a Blueprint function, set `RrOk`, `RrL`, `RrT`, `RrR`, `RrB`, `RrD` variables inside `RobotRect` and read them after the call.
- `GetMousePositionOnViewport` keeps the last position when the mouse leaves the window, so a card can stay up while the mouse is outside the game window. Say so in the findings if it shows; it is harmless.

### 3g. `TipFill.txt`, `TipHide.txt` and `TipSwitch.txt` (new)

```lisp
; T85: fills the card for Seat from BP_Show's seat arrays, with the role and want lines as ShowCast wrote them.
(fn TipFill (Seat)
  (bind _name (get (Class|BPShow|GetSeatLabel :self (V Show)) Seat))
  (bind _col (get (Class|BPShow|GetSeatColors :self (V Show)) Seat))
  (bind _role (get (Class|BPShow|GetSeatRole :self (V Show)) Seat))
  (bind _want (get (Class|BPShow|GetSeatWant :self (V Show)) Seat))
  (Class|WBPCastTip|Fill :self (Variables|WBP_Stage|GetCastTip) :Name _name :Color _col :Role _role :Want _want))

; T85: the card goes away (the mouse left, a cut, the title or end screen). Only acts when it shows.
(fn TipHide ()
  (if (not (V TipShown))
    (return))
  (set TipShown false)
  (set TipSeat -1)
  (Widget|SetVisibility :self (Variables|WBP_Stage|GetCastTip) :InVisibility "Collapsed"))

; T85: Local/switches.json's cast_tip, a seat id ("worrier") or a screen name ("Anthropic"), keeps that robot's card
; shown for screenshots; "" or missing is off. Read at each new scene (TipTick), so it can change between scenes.
(fn TipSwitch ()
  (set TipForce "")
  (bind (_sw _ok) (Json|LoadJsonfromFile (Utilities|Struct|MakeFilePath (cat (Utilities|Paths|GetProjectDirectory) "Local/switches.json"))))
  (if (not _ok)
    (return))
  (set TipSw _sw)
  (if (not (Json|HasField (V TipSw) "cast_tip"))
    (return))
  (bind _v (Json|GetField (V TipSw) "cast_tip"))
  (set TmpStr _v)
  (bind _li (Utilities|Array|FindItem (Class|BPShow|GetSeatLabel :self (V Show)) (V TmpStr)))
  (if (>= _li 0)
    (set TmpStr (get (Class|BPShow|GetSeatId :self (V Show)) _li)))
  (set TipForce (V TmpStr))
  (if (not (Utilities|String|IsEmpty (V TipForce)))
    (print (cat "NHOS: CASTTIP forced " (V TipForce)))))
```

- **`TipFill`'s role and want:** replace `_role` and `_want` with the exact strings `ShowCast` builds (part 0, step 4), for example `(cat "Plays " _role)` if that is what the cast list said. Don't invent new wording.
- `SeatColors` is the fallback only; `WBP_CastTip.Fill` asks `UIStyle.SeatColor` by name first.
- The switch file is read the way T88's `BPC_NoteClue.ReadSwitches` reads it (T88-build 4d); `BP_Show.LoadSwitches` has no file and isn't touched.

### 3h. `TipPlace.txt` and `TipFit.txt` (new)

```lisp
; T85: puts the card beside the robot whose box is (L, T, R, B): on the side toward the screen's middle, its top at
; the box's top, a gap of S3 from the box; TipFit then moves it inside the window's Edge margin and clear of the
; panels. If that lands it on its own robot, the other side is tried; if both do, the first stays. The card is moved
; with its render translation in TipLayer (which fills the window from its top left), so its slot never changes.
(fn TipPlace (L T R B)
  (bind _tip (Variables|WBP_Stage|GetCastTip))
  (if (not (V TipShown))
    (set TipShown true)
    (Widget|SetVisibility :self _tip :InVisibility "HitTestInvisible"))
  (Widget|ForceLayoutPrepass :self _tip)
  (bind _sz (Widget|GetDesiredSize :self _tip))
  (bind _w (.x _sz))
  (bind _h (.y _sz))
  (bind _gap (Class|UIStyle|UISize :Role "S3"))
  (bind _mid (* 0.5 (+ (.x (V TipVTL)) (.x (V TipVBR)))))
  (bind _rightFirst (< (* 0.5 (+ L R)) _mid))
  (bind _x1 (select _rightFirst (+ R _gap) (- (- L _gap) _w)))
  (bind _x2 (select _rightFirst (- (- L _gap) _w) (+ R _gap)))
  (bind (_dx1 _dy1) (CallFunction|TipFit :L _x1 :T T :R (+ _x1 _w) :B (+ T _h)))
  (bind _ax (+ _x1 _dx1))
  (bind _ay (+ T _dy1))
  (bind _over (and (and (< _ax R) (> (+ _ax _w) L)) (and (< _ay B) (> (+ _ay _h) T))))
  (if _over
    (bind (_dx2 _dy2) (CallFunction|TipFit :L _x2 :T T :R (+ _x2 _w) :B (+ T _h)))
    (bind _bx (+ _x2 _dx2))
    (bind _by (+ T _dy2))
    (if (not (and (and (< _bx R) (> (+ _bx _w) L)) (and (< _by B) (> (+ _by _h) T))))
      (Widget|Transform|SetRenderTranslation :self _tip :Translation (Math|Vector2D|MakeVector2D :X (- _bx (.x (V TipVTL))) :Y (- _by (.y (V TipVTL)))))
      (return)))
  (Widget|Transform|SetRenderTranslation :self _tip :Translation (Math|Vector2D|MakeVector2D :X (- _ax (.x (V TipVTL))) :Y (- _ay (.y (V TipVTL))))))

; T85: WBP_SpeechBubble.Fit without the tail. In: the card's rect (L, T, R, B) in viewport units. Out: the shift (DX, DY)
; that puts it inside the window less Edge, then clear of each visible panel grown by S2, by the shortest of the four
; moves (left, right, down, up) that stays inside the margin.
(fn TipFit (L T R B)
  (set TFX 0.0)
  (set TFY 0.0)
  (bind _m (Class|UIStyle|UISize :Role "Edge"))
  (bind _g (Class|UIStyle|UISize :Role "S2"))
  (bind vl (+ (.x (V TipVTL)) _m))
  (bind vt (+ (.y (V TipVTL)) _m))
  (bind vr (- (.x (V TipVBR)) _m))
  (bind vb (- (.y (V TipVBR)) _m))
  (if (< L vl)
    (set TFX (- vl L)))
  (if (> R vr)
    (set TFX (- vr R)))
  (if (< T vt)
    (set TFY (- vt T)))
  (if (> (+ B (V TFY)) vb)
    (set TFY (- vb B)))
  (for i (range (len (V TipKTL)))
    (bind ktl (get (V TipKTL) i))
    (bind kbr (get (V TipKBR) i))
    (bind kl (- (.x ktl) _g))
    (bind kt (- (.y ktl) _g))
    (bind kr (+ (.x kbr) _g))
    (bind kb (+ (.y kbr) _g))
    (bind nl (+ L (V TFX)))
    (bind nr (+ R (V TFX)))
    (bind nt (+ T (V TFY)))
    (bind nb (+ B (V TFY)))
    (if (and (and (< nl kr) (> nr kl)) (and (< nt kb) (> nb kt)))
      (set TMvD 100000.0)
      (set TMvX 0.0)
      (set TMvY 0.0)
      (bind sl (- kl nr))
      (bind sr (- kr nl))
      (bind sd (- kb nt))
      (bind su (- kt nb))
      (if (and (>= (+ nl sl) vl) (< (- 0.0 sl) (V TMvD)))
        (set TMvD (- 0.0 sl))
        (set TMvX sl)
        (set TMvY 0.0))
      (if (and (<= (+ nr sr) vr) (< sr (V TMvD)))
        (set TMvD sr)
        (set TMvX sr)
        (set TMvY 0.0))
      (if (and (<= (+ nb sd) vb) (< sd (V TMvD)))
        (set TMvD sd)
        (set TMvX 0.0)
        (set TMvY sd))
      (if (and (>= (+ nt su) vt) (< (- 0.0 su) (V TMvD)))
        (set TMvD (- 0.0 su))
        (set TMvX 0.0)
        (set TMvY su))
      (if (< (V TMvD) 100000.0)
        (set TFX (+ (V TFX) (V TMvX)))
        (set TFY (+ (V TFY) (V TMvY))))))
  (return (V TFX) (V TFY)))
```

- New Float variables: `TFX`, `TFY`, `TMvD`, `TMvX`, `TMvY` (the bubble's `FX`, `FY`, `MvD`, `MvX`, `MvY`, renamed so they can't clash with anything in `WBP_Stage`).
- **Fix before writing:** `_bx` and `_by` are bound inside the `if`; the DSL allows it in `Fit`'s loop, but if the compiler prunes them, compute both candidates before the `if` (the second fit is cheap).
- `ForceLayoutPrepass` each frame is one small widget; if the profiler minds, call it only in `TipFill` and keep the size in two variables.
- **The first frame:** `GetCachedGeometry` of the panels is a frame old, as in the bubble. Fine.

## 4. `BP_Show`

### 4a. `OpenPrep.txt` (file edit; step 1)

Add the scene-1 setup before `SetPrepMode`, and a comment line:

```lisp
; T85: in scene 1 the robots get their screen names, seat colors and personas here (StageSetup, moved from StartScene),
; so the labels read the names from Scene Prep on, not "ROBOT". ScenePrep has filled the seats and SeatColors (StagePrep)
; by now. Nothing else of the scene starts: StageSetup moves no robot.
(fn OpenPrep ()
  (clear (V SeatEmo))
  (if (== (Variables|Default|GetSceneNum) 1)
    (CallFunction|StageSetup))
  (Class|WBPStage|SetPrepMode :self (Variables|Default|GetStage) :Prep true)
  ...the rest as it is...)
```

- Write the whole graph from the file (it has a source since T28/T71/T68/T77). **re-check:** if T84 or T88 changed `OpenPrep`, edit their version.
- **Restart:** `RestartShow` → `SetupShow` → `ScenePrep` (scene 1) → `OpenPrep` → `StageSetup`, whose `Setup` → `ResetLook` stands the cut robots back up and clears their stamps. Today that happens one click later, at Start the scene; now Scene Prep of the new show already shows them standing and named.
- **Fallback** (part 0 step 2 found that `StageSetup` reads something `StartScene` sets first): keep `StartScene`'s call and add, in `OpenPrep`'s scene-1 branch, only `FindRobots` and a loop that calls `Setup(SeatLabel[s], SeatColors[s], s == HumanSeat)` and `SetPersona(SeatId[s])` on each valid robot. Then `StageSetup` runs again at the scene's start, which is harmless (both calls only set looks), but say so in the findings.

### 4b. `StartScene` (node edit; no file)

Delete the `StageSetup` call node (part 0 step 3) and connect the exec pin before it to the one after it. Leave the branch it sat in. If the branch is then empty, connect around it too. Don't write a source for `StartScene` from a read-back (T06).

### 4c. `PrepPrompt.txt` (file edit; step 7; **re-check (T84)** and **(T88)**)

T85 adds one sentence to the turn line T84 leaves. T84-build part 4 writes "Read the scene in the middle, then your role and the note's clue on the right. Press Start the scene when you are ready." (120 characters, left short on purpose for this hint). T85 puts the hint before the last sentence, so the line still ends with what to press:

```lisp
    (Variables|Default|SetPTurn "Read the scene in the middle, then your role and the note's clue on the right. Point at a robot to see its role and want. Press Start the scene when you are ready.")
```

- Keep every word T84 wrote (and T84's hint, "Read the scene first."); add only "Point at a robot to see its role and want. " before "Press Start the scene". Add "; T85: the hover card's hint." to the comment.
- If T84 used its alternative ("… then your role, the note's clue and the cast on the right. …", T84-build part 4), take "and the cast" out, since the cast is no longer on the card.
- **Check:** the line is 163 characters, against 136 for T50's line that fits the header in two lines at 1600 × 900. Screenshot it at 1600 × 900 and 1280 × 720. If it needs three lines, shorten the hint to "Point at a robot for its role." (134 characters) and say so.
- At `a966b83` the line is T50's ("… the note's category, the cast and the stage. …"). If T85 runs before T84 after all, write: "Read the card on the right: the scene, your role, the note's clue and the stage. Point at a robot to see its role and want. Press Start the scene when you are ready." and check the fit.

## 5. The test switch (`cast_tip`) and the real hover

**Recommended: both.** The switch gives the exact screenshots the Done when lists (every AI robot, the robot nearest each edge at 1280 × 720, a scene turn, the vote) in one pass each, without aiming a mouse at a moving robot. One real hover with computer use checks the path the player uses (`GetMousePositionOnViewport`, the box, the hide on leave), which the switch skips.

1. **The real hover (do it first, in PIE, 1600 × 900 floating window):** computer use `mouse_move` to the middle of an AI robot's body in the PIE window, wait 0.2 s, screenshot; move to empty floor, screenshot (no card); move onto my robot (no card). Read the log for one `NHOS: CASTTIP <id>` per move onto a robot. If computer use can't reach the PIE window, write under "## Findings" that the real hover is not checked, as T85.md says.
2. **`Docs/switches.example.json`:** a new field after `emote_test` (or after T88's `clue_test` if T88 has landed): `"cast_tip": ""`. Append to `_readme`:

   " cast_tip (T85): keep one robot's hover card shown, by its seat id (the id NHOS: LINE prints, such as worrier) or its screen name (such as Anthropic), for screenshots of the card without moving the mouse. It is read at each Scene Prep. My robot and a cut robot never show one. \"\" or missing shows a card only while the mouse is over a robot. Set it back to \"\" before a person plays."

3. Set it in `Local/switches.json` per screenshot; `NHOS: CASTTIP forced <id>` prints at each Scene Prep, then `NHOS: CASTTIP <id>` when the card shows.

## 6. The design doc (question 1)

Read at Rules rev 59. **T84 rewrites `.8385` first** (T84-build 5a, its question 2), so this edit is written against T84's new text. Before asking, read the tab: if T84's OKed text differs, make the same two changes to it (drop the cast from the card, add the pointing sentence) and show my person the result.

1. **Scene Prep, the pause** (`.8385`).
   - After T84 (T84-build 5a's new text): "Scene Prep is a pause. The scene and the stage’s places and props show in a panel in the middle of your screen, with Start the scene under them. Your card on the right shows your role and your want, the note’s clue, and the cast with their roles and wants. The scene starts when you press Start the scene."
   - New: "Scene Prep is a pause. The scene and the stage’s places and props show in a panel in the middle of your screen, with Start the scene under them. Your card on the right shows your role and your want and the note’s clue. Point at any other robot to see its name, role and want; this works in every phase, but not on a robot that has been cut. The scene starts when you press Start the scene."
   - If T84 hasn't changed `.8385` yet (today's text: "… Your screen shows the whole card: the scene, your role and your want, the note’s clue, the cast with their roles and wants, and the stage’s places and props. …"), drop "the cast with their roles and wants, " and add the same pointing sentence before the last one.
2. **The Scene & acting, your card** (`.8620`).
   - Today: "During the scene, your screen shows only your own card: your role, your want and the note’s clue."
   - New: "During the scene, your screen shows only your own card: your role, your want and the note’s clue. Point at another robot to see its role and want."
3. **Left as they are:** the onboarding table's Scene Prep row (`.6880`) lists only my card's rows, which stay. T84's Art Inspiration edits (T84-build 5b: "your part and the note’s clue stay on the card", the screens table's "The scene in the middle, then your part and the note’s clue") name no cast, so they stay true. This sheet didn't read the rest of the Art Inspiration tab: read its UI rows in T85 and, if one lists the cast on the card, add it to the question with the same change.

T85 saves the edit with the Claude Docs connector after my person's OK, as straight edits, and copies the answer into `T85.md`'s findings.

## 7. Notes for later tasks (copy into `T85.md`'s "For later tasks")

- **T34, 2.1 (the tags in screen space):** `WBP_Stage.RobotRect` already projects each robot's feet and label top every frame (in `TipPick`); `TagTick` can call it, or `Viewport|ProjectWorldLocationtoWidgetPosition` on the label the same way. Hiding the 3D labels (T34's `HideRobotLabels`) doesn't change the label's location, so the hover box keeps working. Put `TagLayer` before `TipLayer`, so the card draws over the tags.
- **T34, keyboard:** the card can't be reached by keyboard. Recommendation for T34: low priority, because the same roles and wants are in the shared talk and nothing in a show needs them to be clicked; if T34 wants a keyboard path, a held key (for example Alt) could show every AI robot's card at once, using `TipFill` and `TipPlace` per robot with several `WBP_CastTip`s.
- **T34, 2.10:** the cast bars in `CastBox` no longer show; the hover card already takes its color from `UIStyle.SeatColor`.
- **T61:** the earpiece goes in `TipKeepW` if T61 places it in `WBP_Stage`. A first-show tip could point at the card: "Point at a robot to see who it plays." (a doc edit first).
- **T38's labels under a bubble** (T38, Part 2): the card goes beside the robot, at its label's height, so it can cover a neighbor's bubble while I point. Say in T85's findings if it does.

## 8. The checks (Done when)

All in Test for Free; nothing costs money. Claude plays and judges (the plan's "Claude does the playing"); never ask my person to play.

1. **Compile** `WBP_CastTip`, `WBP_Stage` and `BP_Show` with `warnings_as_errors` true; no pruned node.
2. **Names in Scene Prep:** PIE, autoplay off, 1600 × 900: scene 1's Scene Prep shows every robot's screen name and seat color over its head, mine "You", none "ROBOT" (`names_prep_p16.png`). The log has `NHOS: STAGE robots=5` once, before `NHOS: PREP shown scene=1`, and not again at `PREP start`.
3. **The real hover** (part 5.1): `hover_real_p16.png`, `hover_none_p16.png`, `hover_me_p16.png`; one `CASTTIP` line per move onto a robot.
4. **Every AI robot in scene 1's Scene Prep** with `cast_tip` set to each AI seat in turn: `tip_<id>_prep_p16.png` (four, or three with `ai_seats` 3). Each card: beside its robot, not over it, inside the 24 px edge, clear of the card on the right, T84's panel and the header; the name in its seat color, the role and want as the cast list had them.
5. **A scene turn and the vote:** one robot's card in turn 1 (`tip_turn_p16.png`) while robots move, and in the vote (`tip_vote_p16.png`), clear of the lower panel and the ballot.
6. **No card for me or the cut:** `cast_tip` set to my seat id: no card, no `CASTTIP` line. After a cut (Test for Free, play to scene 2; or `spare_human` so an AI is cut): `cast_tip` on the cut seat shows nothing in scene 2's Scene Prep (`tip_cut_prep2_p16.png`).
7. **The card on the right:** no THE CAST section and no scroll bar in Scene Prep (scene 1 and 2), with T88's longest clue forced (`"clue": "pig_latin"` on `hold_prop`) at 1600 × 900 and 1440 × 900.
8. **1280 × 720:** the robot nearest the left edge and the one nearest the card (`tip_left_p12.png`, `tip_right_p12.png`): the card flips to the inner side and stays inside the edge.
9. **The hint:** the turn line in two lines at 1600 × 900 (`hint_p16.png`).
10. **A free autoplay show in a game window** (`"mode": "free"`, `"autoplay": true`, `"fast_lines": true`, `"cast_tip": ""`) on the saved assets reaches `NHOS: SHOW END` with no new `LogScript` warning (empty `Robots` slots and a fallen robot must not warn) and no `CASTTIP` line.
11. **Findings:** judge from the screenshots, as a critical first-time player: is the cast's info easy to find, is the hint enough, does the card get in the way of a bubble or a click (it can't take a click: `HitTestInvisible`), and the keyboard note for T34 (part 7). Write the design doc answer (question 1) there too.

Keep the screenshots in the task's scratch folder, not in git. Set `cast_tip` back to "" when done.

## 9. The commit

One commit for T85, as "How to run a task" in the plan lists: `Content/NHOS/UI/WBP_CastTip.uasset`, `Content/NHOS/UI/WBP_Stage.uasset`, `Content/NHOS/Core/BP_Show.uasset`, `Docs/switches.example.json`, `Graphs/WBP_CastTip/EventGraph.txt`, `ApplyStyle.txt`, `Fill.txt`, `Graphs/WBP_Stage/SetPrompt.txt`, `TipTick.txt`, `TipKeepRects.txt`, `RobotRect.txt`, `TipPick.txt`, `TipFill.txt`, `TipHide.txt`, `TipSwitch.txt`, `TipPlace.txt`, `TipFit.txt`, `Graphs/BP_Show/OpenPrep.txt`, `PrepPrompt.txt`, `Docs/tasks/T85.md`, `Docs/Plan.md` (the box and the "Next up" line), `Docs/DevLog.md`. No `BP_Robot` change, so `BP_Robot.uasset` stays out of the commit and needs no lock. Unlock the two Blueprints and the claim after the push.
