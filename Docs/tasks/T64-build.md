# T64 build sheet: the action builder, the preview line and Action!

Back to [T64](T64.md). A PC prep session wrote this on 2026-11-15, without the editor, against **`noHumansOnSet` at `3911715`** (the T62 sheet on top of T54). It is a plan, not a record: nothing here was written to the editor. When T64 writes a graph, its source goes to `Graphs/` as usual.

It is written for `WBP_Stage`, `BP_Show` and `UIStyle` **as T55, T57, T58, T62 and T63 leave them**. What each of those changes here:

- **T53** (done) is the last task that changed `WBP_Stage`'s tree: `TopLeftStack` around `HeaderSize`, then `ClapperBox` under it, with `StyleClapper` and `SetClapper`. Nothing T64 touches.
- **T57** puts its "passed" marker on the robot's name (`BP_Robot.SetPassed`, [T57-build.md](T57-build.md) decision 1) and leaves `WBP_Stage` and the Pass button as they are.
- **T58** keeps the last words inside Free Talk and sets its turn line from a new `BP_Show.LastWordPrompt` ([T58-build.md](T58-build.md) part 1); it doesn't change `WBP_Stage` either. So `UpdatePrompt` runs `ComputePrompt` → `PrepPrompt` → `LastWordPrompt` → `LinePrompt` → `SetPrompt`.
- **T59** capped every line at 15 words (`BP_Show.CapWords`, `MaxWords`).
- **T62** gives the chips' choices: `BP_StageDirector.ItemsFor`, `TargetsFor`, `HoldingOf`, `CanDo` and the `MaxHeld` variable ([T62-build.md](T62-build.md), parts 2b, 2c and 8).
- **T63** gives the send: `BP_Show.SendHumanTurn(Verb, Item, Target, Line)`, rewritten with a file (`Graphs/BP_Show/SendHumanTurn.txt`), which `HandleSend`'s scene case calls with `none`, `""`, `""` until T64 ([T63-build.md](T63-build.md) parts 5d, 5e.2 and 8). Autoplay's scene turn doesn't go through `HandleSend`: `StartTurn` calls T63's new `AutoTurn(Line)` (5e.3). `SendHumanTurn` sets `HumanSent` first, and `HumanSay` prints `NHOS: HUMAN <verb> <item|-> <target|-> says=<line|->` once the line is back from the spelling step. An empty line makes no LLM call (its decision 6). T63-build landed on `origin` (`2159294`) while this sheet was being written; the parts that lean on it were checked against it.

Each place is named by its text first. Find each line by its text before you change it.

**Sources read:** `T64.md` and its plan entry; `T62.md` (the input spec), `T63.md`, `T65.md`, `T66.md`; `T62-build.md` (all), `T63-build.md` (parts 0, 5 and 8), `T57-build.md`, `T58-build.md`, `T53-build.md` (the clapperboard part, the model for part 4), `T60-build.md` (the model for the form); the findings of T04, T08, T27, T28, T29, T30, T32, T33 and T53; `T34.md`; every file in `Graphs/WBP_Stage/`, `Graphs/UIStyle/`, `Graphs/WBP_EndScreen/`, `Graphs/WBP_Keys/RowStatus.txt`; `Graphs/BP_Show/` (`LinePrompt`, `PrepPrompt`, `CapWords`, `StartFromPrep`, `RunCue`, `CueHeader`, `LineInfo`, `StateLine`, `StagePrep`); `Tools/dslpp.py`; `prompts.json` (`does_templates`), `scenes.json` (the props and places); `Docs/ItchPage.md`; `Docs/Assets.md`. **A byte search** of the repo folder's `WBP_Stage.uasset` and `BP_Show.uasset` (read only; the worktree holds LFS pointers) for widget, function and literal names that have no `Graphs/` file. **The design doc, read and not changed:** the Turn Input tab rev 1 and the Art Inspiration tab rev 30 (UI: Palette and type, Components, Screens, Motion and rules).

## In short

- **`WBP_ActionBuilder`** (new, part 2): a block of three rows that sits in `WBP_Stage`'s lower panel right above the input row. The **preview line** on an inset box in a mono font (`> throw rose at @Meta: "Oops, my servo slipped."`), the **seven action buttons** in a `WrapBox`, and the **chips** of the picked action in a second `WrapBox`. All its logic lives in it: the state (`Verb`, `Item`, `Target`, `Line`), the greyed actions and their tips, the chips, the preview, and what Action! sends.
- **`WBP_Chip`** (new, part 3): one chip, a `Button` with a seat-color bar and a label. It calls `WBP_ActionBuilder.ChipClicked(Index)` on its owner (the DSL can't bind a dispatcher, T05).
- **The choices come from T62's rules** on the stage director, read when my turn opens and after every pick: `ItemsFor(HumanSeat, Verb)` for the prop step, `TargetsFor(HumanSeat, Verb)` for the target step. Actors show by `SeatLabel` ("Meta") with a seat bar, and the builder keeps their Player names for the call.
- **`WBP_Stage`** (part 4): the builder goes in `LowerBox` above `InputRow`; `SendButton`'s label becomes **Action!** and it is styled Primary; new `BuilderTurn(Seat)`, `TakeAction()`, `SyncAction()` and `FitBuilder()`; edits to `SetPrompt`, `SetPrepMode`, `SetPhase` and `SubmitInput`; a new `OnTextChanged(InputBox)` chain feeds the preview.
- **`BP_Show`** (part 5): **one call at each scene turn**, `WBP_Stage.BuilderTurn(HumanSeat)` in `StartTurn`, just before its header cue; one call in `HandleSend`'s scene branch, `WBP_Stage.TakeAction()`, whose three outputs replace T63's `none`, `""`, `""` on `SendHumanTurn`; and two text literals in `ComputePrompt` (step 9's hints).
- **`UIStyle`** (part 1) gets a mono font: `F_Mono`, a copy of the engine's Droid Sans Mono (Apache 2.0, ships with the engine, nothing to download), as `UIFont("Mono")` at `UISize("Mono")` 18. `Docs/Assets.md` gets its row.
- **The builder opens when the turn's header shows on screen** (the `"phase"` cue runs `SetPhase`), not when the logic reaches `StartTurn`, and closes at the next header or Scene Prep. So it shows only in my scene turns (step 8), never over the last turn's lines.
- **One question for my person** (below), answered: while the builder shows, the lower panel widens to 1000 and the chat shortens to 160.

## Questions for my person

The recommended answer is first.

**Answer (my person, 2026-11-15, to the prep session):** 1: **widen to 1000, chat 160**, as recommended. Don't ask again; copy this answer under "Findings" in `T64.md`. The sheet is written for it.

1. **How the lower panel makes room for the builder.** The builder adds about 220 px at 1080p (the preview line, a row of action buttons, and up to three rows of chips: Look offers 4 actors, 4 props and 7 places). The lower panel is 640 wide, and its top already sits about 50 px under the robots' feet (T27). If it grows upward, the leftmost robot ends up behind it, which the doc forbids ("Nothing covers a robot, its name tag or a thrown prop").
   - **While the builder shows, the lower panel widens from 640 to 1000 and the chat shortens from 380 to 160 (Recommended).** The seven actions fit one row at the normal 48 px button size, most chip lists fit one row, and the panel's top doesn't move. The chat keeps its newest lines at the bottom (about three entries; at 1000 wide, fewer of them wrap). The panel goes back to 640 × 380 in Free Talk, the vote and the reactions. Nothing in `UIStyle` changes but the mono font. T34 can make the wider panel permanent when it polishes the screen.
   - The panel keeps 640: the seven actions wrap to two rows and Look's chips to four, so the chat shortens to about 100 (one or two entries) during my turn.
   - The panel grows upward and the chat keeps 380. The leftmost robot's feet and name tag can end up behind it.

## Decisions this sheet makes (open to change)

The T64 session shows this list to my person when it closes the task.

1. **The preview line lives in `WBP_ActionBuilder`,** at its top: T65's Touches put "the chip in the preview line" in `WBP_ActionBuilder.uasset`. `WBP_Stage` hands it the typed text on every change.
2. **Action! is the existing `SendButton`,** relabeled "Action!" and styled Primary (gold, ink text), in every phase: the spec's speech row has one Action! button, and T66 keeps "the speech field, Action! and the Pass button" in Free Talk. Its name stays `SendButton`, so `SetPrepMode`, `SetPrompt` and `SubmitInput` keep their references.
3. **The picked action and the picked chips are paper** (`StyleButton(..., "Paper")`: cream, dark text), the rest Secondary (plum, white text). Gold stays only on Action! ("Nothing else in the play area is gold"). A greyed action is the button's disabled state (40%, no outline) with a tooltip.
4. **A throw or give shows my held props first; once I pick one, that prop stays as the first chip (paper), followed by its targets.** Clicking it again unpicks it and the target (step 3's "and the chips after it"). In a one-step action (move, look, grab), the whole list stays, the picked chip is paper, and a click on another chip switches to it.
5. **An actor's chip has a 6 px seat-color bar before its screen name,** so a seat shows by color and by name (the doc: "Color never carries meaning alone"). Props and places have no bar. The chip's label stays white or dark text, because seat colors on the plum fill don't all reach 4.5:1.
6. **The preview line's wording**, prefixed `> ` like the doc's mock-up: `move to Left`, `look at @Meta`, `look at bowling ball`, `look around`, `grab bowling ball`, `throw bowling ball at @Meta`, `throw bowling ball at Left`, `give bowling ball to @Meta`, and **No action reads `stand still`**, the log's "stands still". The typed line follows as `: "..."`. An unfinished action shows `...` where the choice is missing: `throw ...`, `throw rose at ...`, `move to ...`.
7. **When the builder shows:** `BuilderTurn` (logic time, from `StartTurn`) only arms it. It opens at the turn's header cue (screen time, `SetPhase`), reads the choices and resets to No action. Any other header or a Scene Prep closes it. Between my send and the next turn's header it stays up, sealed, still showing what I sent.
8. **After I send, the builder is sealed** (`Sent`): its buttons and chips are disabled and the preview keeps the sent turn, until the next turn opens. Action! is disabled by `SetPrompt`'s `CanType`, as now.
9. **The hints (step 9):** the scene turn's hint becomes the spec's "Say something (optional)...", which T65 keeps; the turn line's "Type what your robot does and says." part becomes "pick an action, say a line if you like, then press Action!" (part 5c).
10. **The tips:** Throw and Give with nothing held: "Grab something first." Grab with every prop held: "Nothing free to grab." Grab with full hands (only with T62's two-prop cap): "Your hands are full." Give when every other actor's hands are full: "Nobody has a free hand." Action! while a picked action lacks a chip: "Pick a target first." (the task's words, for a missing prop too).
11. **The chips are made again on every refresh** (`ClearChildren`, then one `WBP_Chip` per choice). At most 16 widgets, a few times a turn; no pool.
12. **No scroll in the chip rows.** Every choice stays in view (three rows at most for Look at 1000 wide).
13. **The mono face is the engine's Droid Sans Mono** (part 1). With `F_UI` that makes two typefaces, the doc's limit ("at most two typefaces"), as long as the display face (Lilita One) isn't imported; see part 9.
14. **New check lines:** `NHOS: BUILDER open turn=<n> seat=<id> greyed=<verbs|->` when the builder opens, `NHOS: BUILDER pick <verb> <item|-> <target|-> | <preview>` on every pick, `NHOS: BUILDER blocked` when Enter is pressed on an unfinished action, and `NHOS: BUILDER send <verb> <item|-> <target|-> ready=<yes|no>` when `HandleSend` takes the action.

## Wording that comes from the task or the doc

- **"Grab something first."**, **"Nothing free to grab."**, **"Pick a target first."** and the seven button labels (Move, Look, Grab, Throw, Give, Look around, No action) are the task's and the doc's (Turn Input tab).
- **"Your hands are full."** is T62-build's wording (its question 2, part 8).
- **"Say something (optional)..."** is the spec's speech-field hint, word for word.
- **"Action!"** is the spec's button. **`stand still`** is this sheet's pick (the task asks for one, and it matches the log's "stands still").
- **The preview line's form** (`throw rose at @Meta: "Oops, my servo slipped."`, `throw rose at ...`) is the task's example.

## 0. Before you start (after T63 is pushed)

1. `git log --oneline -12` shows T55, T57, T58, T62 and T63; `Docs/claims/T63` is released. `git lfs locks` shows no lock on `Content/NHOS/UI/WBP_Stage.uasset`, `Content/NHOS/Core/BP_Show.uasset` or `Content/NHOS/UI/Style/UIStyle.uasset`. Claim T64 (`git lfs lock Docs/claims/T64`) and lock all three. The two new widgets need no lock.
2. **Read what T62 and T63 found** (their "Findings"):
   - **T62's answers to its four questions.** This sheet assumes question 1's recommended answer (the check runs when a line enters the shared log, so `HoldBy` is right at my turn's start). If my person chose "at play time", the chips at a turn's start can lag a turn behind the stage; tell my person before you build. Question 2 decides whether "Your hands are full." can show: the builder reads `MaxHeld` from the director either way.
   - **T62's names:** `ItemsFor`, `TargetsFor`, `HoldingOf` (String arrays), `MaxHeld` (Integer) on `BP_StageDirector`, and the names in `RNames` (Player names, from `BP_Show.SeatName`). If any differs, use T62's real name everywhere below.
   - **T63's findings and `Graphs/BP_Show/SendHumanTurn.txt`:** the inputs `Verb`, `Item`, `Target`, `Line` in that order and the verb words (`move`, `look`, `grab`, `throw`, `give`, `around`, `none`; T63-build 5d); the `HandleSend` scene-case node edit it wrote under "Findings" (5e.2: `Verb` `none`, `Item` and `Target` empty, `Line` from the typed text), which part 5b replaces; that autoplay's scene turn is `StartTurn` → `AutoTurn` (5e.3), not `HandleSend`; the form of `NHOS: HUMAN` (`HumanSay`, 5c). If T63 built any of these differently, follow what it built.
3. `python Tools/check_prompts.py --offline` passes before you start. T64 changes no data file, so it should pass after too.
4. **The survey** (each item a separate `call_tool`; calls stop at about 120 s; save each read to `Saved/T64/<graph>.read.txt`; never write a read-back to the editor):
   1. **`WBP_Stage`'s tree** (the UMG toolset from `list_toolsets`; T33 and T53 read trees with it). Record:
      - `LowerSize` (SizeBox, `WidthOverride` 640 expected) > `LowerPanel` > `LowerBox` (VerticalBox): its children in order with their slot paddings. Expected (T27, T29, T30, T38-build A6): `ChatSize` (SizeBox, `HeightOverride` 380) holding `BodyRow` > `LogScroll` (maybe in a VerticalBox with `TypingText`), `TypingText` (if it is a `LowerBox` child), `VoteRow`, then `InputRow`.
      - `InputRow` (HorizontalBox): its children in order with paddings. Expected: `InputStack` (Overlay: `InputBox`, `HintLabel`), `SendButton` (`SendLabel`), `PassButton` (`PassLabel`), `ContinueButton` (`ContinueLabel`), `StartButton` (`StartLabel`). `WrapWidgets` drops slot paddings (T28), so write each one down.
      - Whether `LowerSize`, `ChatSize` and `LogScroll` are variables (`bIsVariable`). Part 4 needs all three; turn it on for any that isn't.
      - `SendButton`'s `IsFocusable` (off since T04) and `SendLabel`'s text ("Send").
   2. **`WBP_Stage` graphs with no file:** `read_graph_dsl` of **`SubmitInput`** (record: how it reads `InputBox`, whether it skips an empty line, the `OnSend` call, how it clears the box), **`SetPhase`** (expected: sets `PhaseHeader`'s text from `Phase`; record its input's name) and **`CleanText`** (record its input and output names; part 4f uses it).
   3. **`WBP_Stage`'s EventGraph events:** `find_nodes` for event nodes (full class paths, T30). Expected: `OnTextCommitted(InputBox)` (Text, CommitMethod) → `SubmitInput` on Enter; `OnClicked` of `SendButton`, `PassButton`, `ContinueButton`, `StartButton` and `VoteBtn0` to `VoteBtn3`. Confirm there is **no `OnTextChanged(InputBox)`** yet (the byte search found none) and whether `EventConstruct` or `EventPreConstruct` exist (part 4 adds neither).
   4. **`BP_Show.StartTurn`** (`read_graph_dsl`): the `CueHeader` call node and the exec link into it; whether `StartTurn` runs once per scene turn for turns 1 to 3 (T07, T30). Record the getter names `Stage` and `HumanSeat` (both used in `RunCue.txt`).
   5. **`BP_Show.HandleSend`** (`read_graph_dsl`): the `"scene"` branch and its `SendHumanTurn` call with T63's literals (T63-build 5e.2); where `Line` comes from; the checks before it (`Phase` is "scene", `HumanSent` false, T07); and whether it drops an empty line before the call (T63's `SpellAsk` handles an empty line itself, so nothing after `HandleSend` needs one).
   6. **`BP_Show.ComputePrompt`:** don't read the whole graph (its read-back is lossy, T28, T55). `find_nodes` for `K2Node_CallFunction` nodes titled `Append` and `get_node_infos` on them, to find the two literals of part 5c by their text.
   7. **Node names** with `find_node_types` (`context_pins: []`, T29), in `WBP_ActionBuilder` once it exists: `Widget|AddChildToWrapBox` (its `Content` pin and return), `Widget|ClearChildren`, `Widget|SetToolTipText` (pin `InToolTipText`), `Widget|SetIsEnabled` (`bInIsEnabled`), `UserInterface|CreateWidget`, `Utilities|Array|FindItem`, `Utilities|String|ParseIntoArray`; in `WBP_Stage`: `Class|SizeBox|SetWidthOverride` (`InWidthOverride`), `Class|SizeBox|SetHeightOverride` (`InHeightOverride`), `Class|ScrollBox|ScrollToEnd`. **The other Blueprints' variables:** `Class|BPShow|GetSeatName`, `GetSeatLabel`, `GetSeatId`, `GetTurnNum` and `Class|BPStageDirector|GetMaxHeld`, each with `:self` (the form `WBP_EndScreen` uses for `Class|BPShow|GetStage`, T33). A function library must be loaded first: `BlueprintTools.list_functions` on `UIStyle` (T33).
   8. **The engine font:** `ObjectTools.list_properties` on `/Engine/EngineFonts/DroidSansMono`: its `fontCacheType` must be `Runtime` (an `Offline` font is a bitmap and won't do), and record the name of its default typeface's first entry (`compositeFont` > `defaultTypeface` > `fonts[0]` > `name`, expected `Regular`).
   9. **Hover:** `describe_toolset` for the Slate inspector toolset: does it have a hover or mouse-move action? Part 7's tooltip screenshot needs one (else see part 7, shot 2).

## 1. `UIStyle`: a mono font (step 6)

**Does `UIStyle` have one?** No. `UIFont` (`Graphs/UIStyle/UIFont.txt`) has only `F_UI` (the engine's Roboto), and `Content/NHOS/UI/Fonts/` holds only `F_UI.uasset`. Add one.

**Which:** the engine's **Droid Sans Mono** (`/Engine/EngineFonts/DroidSansMono`, its face `/Engine/EngineFonts/Faces/DroidSansMono`), the same way T32 made `F_UI` from the engine's Roboto. It ships with UE 5.8 (`Engine/Content/Slate/Fonts/DroidSansMono.ttf`, `DroidSans.tps`) under the Apache License 2.0, so **nothing is downloaded**. It has one face (Regular), which is all the preview line needs.

1. `AssetTools.duplicate` `/Engine/EngineFonts/DroidSansMono` to `/Game/NHOS/UI/Fonts/F_Mono`. Check survey 8's `fontCacheType` (`Runtime`) and typeface name on the copy. Save.
2. **`Graphs/UIStyle/UIFont.txt`:** add one branch before the last line (the `Regular` fallback), and a sentence to the header comment:

```lisp
; Mono (T64): F_Mono (the engine's Droid Sans Mono), no outline, for the preview line's terminal look.
  (if (Utilities|String|EqualExactly(String) Role "Mono")
    (return (SlateFont|MakeSlateFontInfo :FontObject "/Game/NHOS/UI/Fonts/F_Mono.F_Mono" :TypefaceFontName "Regular" :Size size :OutlineSettings none)))
```

   The comment line goes after the file's third comment line (`; Body roles: ...`). The branch goes right after the `"Action"` branch. Use survey 8's typeface name if it isn't `Regular`.
3. **`Graphs/UIStyle/UISize.txt`:** after the `"Hint"` branch, add:

```lisp
  ; Mono = 18: the preview line (T64), terminal style
  (if (Utilities|String|EqualExactly(String) Role "Mono")
    (return 18.00))
```

   18 is the doc's floor ("Nothing under 18"). A mono face is wide: at 18 pt, about 89 characters fit a 1000 px line, so a full 15-word line with its action takes two lines at most.
4. Write both files with `write_graph_dsl`, compile `UIStyle` with warnings as errors, save.
5. **`Docs/Assets.md`** (outside T64's Touches; name it in the commit message), a row under "Fonts":

   `| Content/NHOS/UI/Fonts/F_Mono | The mono font for the action builder's preview line (T64). A copy of the engine's /Engine/EngineFonts/DroidSansMono composite font, so it uses the engine's Droid Sans Mono face. | Droid Sans Mono, shipped with Unreal Engine 5.8 (Engine/Content/Slate/Fonts/DroidSansMono.ttf, DroidSans.tps). | Apache License 2.0. |`

   (with the usual backticks on the paths, as the `F_UI` row has them). The note under the table ("Neither font draws emoji ...") becomes "None of these fonts draws emoji ...".

## 2. `WBP_ActionBuilder` (new)

`Content/NHOS/UI/WBP_ActionBuilder.uasset`, made with `UMGToolSet.CreateWidgetBlueprint` (T04). Its graphs go in `Graphs/WBP_ActionBuilder/`.

### 2a. The widget tree

```
BuilderBox        VerticalBox (root)
├ PreviewBox      Border; padding 12 left and right, 8 top and bottom (S3, S2); slot: HAlign Fill, padding bottom 8 (S2)
│ └ PreviewText   TextBlock; AutoWrapText on; justify Left; text "> stand still"
├ ActionsWrap     WrapBox; InnerSlotPadding (8, 8) (S2); slot: HAlign Fill, padding bottom 8 (S2)
│ ├ MoveBtn       Button > MoveLabel     TextBlock "Move"
│ ├ LookBtn       Button > LookLabel     TextBlock "Look"
│ ├ GrabBtn       Button > GrabLabel     TextBlock "Grab"
│ ├ ThrowBtn      Button > ThrowLabel    TextBlock "Throw"
│ ├ GiveBtn       Button > GiveLabel     TextBlock "Give"
│ ├ AroundBtn     Button > AroundLabel   TextBlock "Look around"
│ └ NoneBtn       Button > NoneLabel     TextBlock "No action"
└ ChipsBox        SizeBox (no overrides); slot: HAlign Fill, padding bottom 8 (S2); Collapsed at design time
  └ ChipsWrap     WrapBox; InnerSlotPadding (8, 8) (S2); the chips go here at run time (WBP_Chip)
```

- **Every `Button`: `IsFocusable` off** (step 5), set in the designer for all seven. The user widget itself stays unfocusable (the default). Nothing in the builder can take keyboard focus, so the caret stays in `InputBox` while I click (T04 did the same for `SendButton`).
- `bIsVariable` on for `PreviewBox`, `PreviewText`, `ActionsWrap`, the seven buttons and seven labels, `ChipsBox` and `ChipsWrap`.
- **No colors, fonts or sizes in the designer.** `StyleAll` (2c) sets them from `UIStyle`; paddings are the doc's spacing steps.
- The root's visibility is set by the graph: `Construct` collapses it, `OpenTurn` shows it.
- At 1000 wide (question 1's first answer) the seven buttons take about 755 px at the normal button size (48 tall, 20 px side padding, 20 pt labels), so they fit one row; at 640 they wrap to two.

### 2b. Variables

| Variable | Type | Default | Used by |
|---|---|---|---|
| `Show` | `BP_Show` object reference | none | `OpenTurn` |
| `Dir`, `NullDir` | `BP_StageDirector` object reference | none (`NullDir` is never set: the `StagePrep.txt` pattern for a missing director) | `OpenTurn`, `WhyNot`, `BuildChips` |
| `Seat`, `ArmSeat` | Integer | -1 | everywhere / `Arm`, `OpenTurn` |
| `Names`, `Labels` | String array | empty | `ScreenName`, `AddChip` |
| `Verb` | String | `none` | everywhere |
| `Item`, `Target`, `Line` | String | "" | everywhere |
| `Armed`, `Sent`, `Live`, `PendingTurn` | Boolean | false | everywhere |
| `ActBtns` | `Button` object reference array | empty | `FillLists`, `Refresh` |
| `ActLbls` | `TextBlock` object reference array | empty | `FillLists`, `Refresh` |
| `ActVerbs`, `ActTip`, `GreyArr`, `Choices`, `ChipRole`, `TmpList` | String array | empty | `FillLists`, `ReadOk`, `Refresh`, `BuildChips`, `AddChip`, `ChipClicked` |
| `ActOk` | Boolean array | empty | `ReadOk`, `Refresh` |
| `TmpStr`, `Kind`, `GreyList` | String | "" | helpers |

### 2c. Functions, in the order to make them

T18 and T54: a call node goes stale when its function gets a new parameter, so create every function and its parameters first, compile, then write the graphs callee first. **Make `ChipClicked(Index)` and compile before `WBP_Chip` exists** (part 3 calls it), then make `WBP_Chip`, then write the rest here.

| Function | Inputs | Outputs | Called by |
|---|---|---|---|
| `NeedsItem`, `NeedsTarget` | `Act` (String) | Boolean | many |
| `ScreenName`, `PreviewName` | `Value` (String) | String | `AddChip`, `PreviewText` |
| `WhyNot` | `Act` (String) | String | `ReadOk` |
| `ReadOk` | — | — | `OpenTurn` |
| `PreviewText` | — | String | `Refresh`, `PickLine`, `SetLine` |
| `AddChip` | `Value`, `Role` (String), `Picked` (Boolean) | — | `BuildChips` |
| `BuildChips` | — | — | `Refresh` |
| `Refresh` | — | — | many |
| `PickLine` | — | — | `PickVerb`, `ChipClicked` |
| `IsReady` | — | Boolean | `GetAction`, `Blocks` |
| `StyleAll`, `FillLists` | — | — | the events |
| `Arm` | `Seat` (Integer) | — | `WBP_Stage.BuilderTurn` |
| `OpenTurn` | — | — | `PhaseShown` |
| `PhaseShown` | `Text` (String) | — | `WBP_Stage.SetPhase` |
| `Close` | — | — | `PhaseShown`, `WBP_Stage.SetPrepMode` |
| `SetLive` | `On` (Boolean) | — | `WBP_Stage.SetPrompt` |
| `SetLine` | `Text` (String) | — | `WBP_Stage`'s `OnTextChanged(InputBox)` |
| `PickVerb` | `Act` (String) | — | the seven buttons |
| `ChipClicked` | `Index` (Integer) | — | `WBP_Chip` |
| `GetAction` | — | `Verb`, `Item`, `Target` (String), `Ready` (Boolean) | `Seal` |
| `Seal` | — | `Verb`, `Item`, `Target` (String), `Ready` (Boolean) | `WBP_Stage.TakeAction` |
| `Blocks`, `IsOn` | — | Boolean | `WBP_Stage.SubmitInput`, `SyncAction`, `FitBuilder` |

Outputs: `add_function_param` with the output flag (T62-build 0.6.8 checks the form). `(return a b c d)` fills them in the order they were made, as `BP_Show.LineInfo` returns two (`Graphs/BP_Show/LineInfo.txt`, read with `(bind (_id _ty) ...)` in `BPC_LinePlayer.Push`).

**The helpers.** `NeedsItem.txt`:

```lisp
; T64: true for the actions that take a prop: grab, throw, give.
(fn NeedsItem (Act)
  (return (or (streq Act "grab") (or (streq Act "throw") (streq Act "give")))))
```

`NeedsTarget.txt`:

```lisp
; T64: true for the actions that take a target: move (a place), look (an actor, a prop or a place),
; throw (an actor or a place), give (an actor). Look around and No action take none.
(fn NeedsTarget (Act)
  (return (or (streq Act "move") (or (streq Act "look") (or (streq Act "throw") (streq Act "give"))))))
```

`ScreenName.txt`:

```lisp
; T64: the name I see for a choice. A Player name ("Player 3") becomes its seat's screen name (SeatLabel: "Meta");
; props and places stay as the card and the set name them. The call keeps the Player name (T62's names).
(fn ScreenName (Value)
  (bind _s (Utilities|Array|FindItem (V Names) Value))
  (if (< _s 0)
    (return Value))
  (return (get (V Labels) _s)))
```

`PreviewName.txt`:

```lisp
; T64: a target in the preview line: an actor as an @ mention by its screen name ("@Meta"), a prop or a place as is.
(fn PreviewName (Value)
  (if (Utilities|String|IsEmpty Value)
    (return ""))
  (bind _s (Utilities|Array|FindItem (V Names) Value))
  (if (< _s 0)
    (return Value))
  (return (cat "@" (get (V Labels) _s))))
```

`(get (V Labels) _s)` only runs once `_s` is known to be 0 or more: a `select` would read index -1 too and print a `LogScript` warning.

**The rules.** `WhyNot.txt`:

```lisp
; T64: "" when I can pick the action Act now, else the tip its greyed button shows (step 4). The choices come from
; the stage director's rules (T62: ItemsFor, TargetsFor, HoldingOf, MaxHeld), the same rules that check every AI's action.
; Look around and No action are always open.
(fn WhyNot (Act)
  (bind _ni (CallFunction|NeedsItem :Act Act))
  (bind _nt (CallFunction|NeedsTarget :Act Act))
  (if (not (or _ni _nt))
    (return ""))
  (if (== (V Dir) (V NullDir))
    (return "The stage isn't ready."))
  (bind _items (Class|BPStageDirector|ItemsFor :self (V Dir) :Seat (V Seat) :Verb Act))
  (bind _targs (Class|BPStageDirector|TargetsFor :self (V Dir) :Seat (V Seat) :Verb Act))
  (bind _held (Class|BPStageDirector|HoldingOf :self (V Dir) :Seat (V Seat)))
  (bind _max (Class|BPStageDirector|GetMaxHeld :self (V Dir)))
  (if (and _ni (== (len _items) 0))
    (if (streq Act "grab")
      (return (select (>= (len _held) _max) "Your hands are full." "Nothing free to grab.")))
    (return "Grab something first."))
  (if (and _nt (== (len _targs) 0))
    (return (select (streq Act "give") "Nobody has a free hand." "Nothing to pick.")))
  (return ""))
```

- T62's three functions each return a shared variable (`RList`, `RHeld`). A call node keeps its own copy of its output, so `_items` survives the `TargetsFor` call; part 7's `BUILDER open` line shows it (a greyed Grab on turn 1 would mean the copy was lost; then copy each result into its own variable right after its call).
- For throw and give, `TargetsFor` doesn't depend on the prop, so the check is right before a prop is picked.
- With T62's "no limit" answer, `MaxHeld` is 99, so "Your hands are full." never shows.

`ReadOk.txt`:

```lisp
; T64: which of the seven actions I can pick this turn, with each greyed one's tip. OpenTurn calls it once: the rules'
; state doesn't change during my turn (T62 accepts every action of a turn only after everyone has sent).
(fn ReadOk ()
  (clear (V ActOk))
  (clear (V ActTip))
  (clear (V GreyArr))
  (for _v (V ActVerbs)
    (bind _w (CallFunction|WhyNot :Act _v))
    (set TmpStr _w)
    (add (V ActTip) (V TmpStr))
    (add (V ActOk) (Utilities|String|IsEmpty (V TmpStr)))
    (if (not (Utilities|String|IsEmpty (V TmpStr)))
      (add (V GreyArr) _v)))
  (set GreyList (select (> (len (V GreyArr)) 0) (Utilities|String|JoinStringArray (V GreyArr) ",") "-")))
```

**The preview.** `PreviewText.txt`:

```lisp
; T64: the preview line (step 6), in the terminal style: the action as built, then the typed line, live.
;   > throw rose at @Meta: "Oops, my servo slipped."
; An unfinished action shows what's missing ("> throw rose at ..."). No action reads "stand still", the log's
; "stands still"; Look around reads "look around". An empty line adds nothing.
(fn PreviewText ()
  (bind _noi (Utilities|String|IsEmpty (V Item)))
  (bind _it (select _noi "..." (V Item)))
  (bind _tn (CallFunction|PreviewName :Value (V Target)))
  (bind _tg (select (Utilities|String|IsEmpty (V Target)) "..." _tn))
  (set TmpStr "stand still")
  (if (streq (V Verb) "move")
    (set TmpStr (cat "move to " _tg)))
  (if (streq (V Verb) "look")
    (set TmpStr (cat "look at " _tg)))
  (if (streq (V Verb) "around")
    (set TmpStr "look around"))
  (if (streq (V Verb) "grab")
    (set TmpStr (cat "grab " _it)))
  (if (streq (V Verb) "throw")
    (set TmpStr (select _noi "throw ..." (cat "throw " _it " at " _tg))))
  (if (streq (V Verb) "give")
    (set TmpStr (select _noi "give ..." (cat "give " _it " to " _tg))))
  (if (Utilities|String|IsEmpty (V Line))
    (return (cat "> " (V TmpStr))))
  (return (cat "> " (V TmpStr) ": \"" (V Line) "\"")))
```

- None of the `if`s before the last one returns, so each joins the next (T30). The escaped quotes come through as plain quotes (T01).
- T65 replaces the plain `@Meta` with a chip in the preview line (its step 5); keep `PreviewName` the one place that makes it.

**The chips.** `AddChip.txt`:

```lisp
; T64: one chip in ChipsWrap. Its place in Choices is its Index, so a click tells the builder which choice it was.
; An actor shows by its screen name with a seat-color bar (WBP_Chip.Setup); the builder keeps its Player name (Value).
(fn AddChip (Value Role Picked)
  (bind _lab (CallFunction|ScreenName :Value Value))
  (bind _s (Utilities|Array|FindItem (V Names) Value))
  (bind _chip (UserInterface|CreateWidget "/Game/NHOS/UI/WBP_Chip.WBP_Chip_C" (Widget|GetOwningPlayer self)))
  (Class|WBPChip|Setup :self _chip :Owner self :Index (len (V Choices)) :Label _lab :Actor (>= _s 0) :Picked Picked)
  (Widget|AddChildToWrapBox :self (Variables|WBP_ActionBuilder|GetChipsWrap) :Content _chip)
  (add (V Choices) Value)
  (add (V ChipRole) Role))
```

`CreateWidget` is `WBP_EndScreen/AddCard.txt`'s form. If `:Owner self` doesn't take, bind `self` first or use a `Self` node (`get_node_type_pins`).

`BuildChips.txt`:

```lisp
; T64: the chips for the step I'm on (step 3). Only the picked action's valid choices show, read from T62's rules on
; every refresh. Throw and Give: my held props first; once I pick one, that prop as a picked chip, then its targets.
; Move, Look, Grab: the whole list, the picked one in paper. Look around and No action: none.
(fn BuildChips ()
  (Widget|ClearChildren :self (Variables|WBP_ActionBuilder|GetChipsWrap))
  (clear (V Choices))
  (clear (V ChipRole))
  (if (== (V Dir) (V NullDir))
    (return))
  (bind _ni (CallFunction|NeedsItem :Act (V Verb)))
  (bind _nt (CallFunction|NeedsTarget :Act (V Verb)))
  (bind _hasi (not (Utilities|String|IsEmpty (V Item))))
  (if (and _ni (and _nt _hasi))
    (CallFunction|AddChip :Value (V Item) :Role "item" :Picked true)
    (bind _ts (Class|BPStageDirector|TargetsFor :self (V Dir) :Seat (V Seat) :Verb (V Verb)))
    (set TmpList _ts)
    (for _t (V TmpList)
      (CallFunction|AddChip :Value _t :Role "target" :Picked (streq _t (V Target))))
    (return))
  (if _ni
    (bind _is (Class|BPStageDirector|ItemsFor :self (V Dir) :Seat (V Seat) :Verb (V Verb)))
    (set TmpList _is)
    (for _i (V TmpList)
      (CallFunction|AddChip :Value _i :Role "item" :Picked (streq _i (V Item))))
    (return))
  (if _nt
    (bind _ts2 (Class|BPStageDirector|TargetsFor :self (V Dir) :Seat (V Seat) :Verb (V Verb)))
    (set TmpList _ts2)
    (for _t2 (V TmpList)
      (CallFunction|AddChip :Value _t2 :Role "target" :Picked (streq _t2 (V Target))))))
```

- `TmpList` holds the list while `AddChip` runs, so no later call to the director can change what the loop walks.
- T62 lists Look's targets as actors, then props, then places (its part 2b), so the chips come in that order.

`ChipClicked.txt`:

```lisp
; T64: a chip was clicked (WBP_Chip passes its Index). An "item" chip picks that prop, or unpicks it if it was the picked
; one, and clears the target after it. A "target" chip picks that target, or unpicks it if it was picked.
(fn ChipClicked (Index)
  (if (or (not (V Armed)) (V Sent))
    (return))
  (if (or (< Index 0) (>= Index (len (V Choices))))
    (return))
  (set TmpStr (get (V Choices) Index))
  (set Kind (get (V ChipRole) Index))
  (if (streq (V Kind) "item")
    (set Item (select (streq (V TmpStr) (V Item)) "" (V TmpStr)))
    (set Target ""))
  (if (streq (V Kind) "target")
    (set Target (select (streq (V TmpStr) (V Target)) "" (V TmpStr))))
  (CallFunction|Refresh)
  (CallFunction|PickLine))
```

**The buttons.** `PickVerb.txt`:

```lisp
; T64: an action button (step 2). Picking another action clears the chips I picked; clicking the picked one keeps
; them. A greyed button is disabled, so Act is always an action I can do.
(fn PickVerb (Act)
  (if (or (not (V Armed)) (V Sent))
    (return))
  (if (not (streq Act (V Verb)))
    (set Verb Act)
    (set Item "")
    (set Target ""))
  (CallFunction|Refresh)
  (CallFunction|PickLine))
```

`PickLine.txt`:

```lisp
; T64: a check line on every pick, with the preview it gives.
(fn PickLine ()
  (bind _p (CallFunction|PreviewText))
  (bind _i (select (Utilities|String|IsEmpty (V Item)) "-" (V Item)))
  (bind _t (select (Utilities|String|IsEmpty (V Target)) "-" (V Target)))
  (print (cat "NHOS: BUILDER pick " (V Verb) " " _i " " _t " | " _p)))
```

**Drawing.** `Refresh.txt`:

```lisp
; T64: draws the builder from its state: the picked action in paper, the rest plum; greyed actions disabled with
; their tips (step 4); the chips of the step I'm on; the preview line. Everything is off until my turn is live
; (SetPrompt's CanType) and after I send.
(fn Refresh ()
  (bind _on (and (V Armed) (and (not (V Sent)) (V Live))))
  (for _k (range (len (V ActBtns)))
    (bind _b (get (V ActBtns) _k))
    (bind _l (get (V ActLbls) _k))
    (Class|UIStyle|StyleButton :Button _b :Label _l :Kind (select (streq (get (V ActVerbs) _k) (V Verb)) "Paper" "Secondary"))
    (Widget|SetIsEnabled :self _b :bInIsEnabled (and _on (get (V ActOk) _k)))
    (Widget|SetToolTipText :self _b :InToolTipText (Utilities|Text|ToText(String) (get (V ActTip) _k))))
  (CallFunction|BuildChips)
  (Widget|SetIsEnabled :self (Variables|WBP_ActionBuilder|GetChipsWrap) :bInIsEnabled _on)
  (if (> (len (V Choices)) 0)
    (Widget|SetVisibility :self (Variables|WBP_ActionBuilder|GetChipsBox) :InVisibility "SelfHitTestInvisible")
    (else
      (Widget|SetVisibility :self (Variables|WBP_ActionBuilder|GetChipsBox) :InVisibility "Collapsed")))
  (bind _p (CallFunction|PreviewText))
  (Class|Text|SetText :self (Variables|WBP_ActionBuilder|GetPreviewText) :Text (Utilities|Text|ToText(String) _p)))
```

- `ActOk` and `ActTip` are filled by `OpenTurn` before the first `Refresh`, so `(get (V ActOk) _k)` never reads past the end.
- An open action's tooltip is "" (no tooltip). **Does a disabled button show its tooltip?** Slate shows tooltips on disabled widgets (the editor's own greyed buttons do); part 7 checks it. If it doesn't, wrap each action button in a `Border` (`MoveTip` …) that stays enabled and carries the tooltip instead.

`StyleAll.txt`:

```lisp
; T64: the builder's look, all from UIStyle (T32): the preview line on an inset box with the input box's 2 px quiet
; outline, in the mono font, white on near-black like a terminal; the seven actions as Secondary buttons. UIStyle's
; functions are impure, so every value is bound before use.
(fn StyleAll ()
  (bind fMono (Class|UIStyle|UIFont :Role "Mono"))
  (bind cText (Class|UIStyle|UIColor :Role "Text"))
  (bind cInset (Class|UIStyle|UIColor :Role "Inset"))
  (bind cQuiet (Class|UIStyle|UIColor :Role "Quiet"))
  (bind w (Class|UIStyle|UISize :Role "InputOutline"))
  (bind r (Class|UIStyle|UISize :Role "ButtonRadius"))
  (bind bPrev (Class|UIStyle|Brush :Fill cInset :Outline cQuiet :Width w :Radius r))
  (Class|Border|SetBrushColor :self (Variables|WBP_ActionBuilder|GetPreviewBox) :BrushColor (Utilities|Struct|MakeLinearColor 1.0 1.0 1.0 1.0))
  (Appearance|SetBrush :self (Variables|WBP_ActionBuilder|GetPreviewBox) :InBrush bPrev)
  (Class|Text|SetFont :self (Variables|WBP_ActionBuilder|GetPreviewText) :Font fMono)
  (Class|Text|SetColorandOpacity :self (Variables|WBP_ActionBuilder|GetPreviewText) :ColorAndOpacity (Utilities|Struct|MakeSlateColor :SpecifiedColor cText))
  (Class|UIStyle|StyleButton :Button (Variables|WBP_ActionBuilder|GetMoveBtn) :Label (Variables|WBP_ActionBuilder|GetMoveLabel) :Kind "Secondary")
  (Class|UIStyle|StyleButton :Button (Variables|WBP_ActionBuilder|GetLookBtn) :Label (Variables|WBP_ActionBuilder|GetLookLabel) :Kind "Secondary")
  (Class|UIStyle|StyleButton :Button (Variables|WBP_ActionBuilder|GetGrabBtn) :Label (Variables|WBP_ActionBuilder|GetGrabLabel) :Kind "Secondary")
  (Class|UIStyle|StyleButton :Button (Variables|WBP_ActionBuilder|GetThrowBtn) :Label (Variables|WBP_ActionBuilder|GetThrowLabel) :Kind "Secondary")
  (Class|UIStyle|StyleButton :Button (Variables|WBP_ActionBuilder|GetGiveBtn) :Label (Variables|WBP_ActionBuilder|GetGiveLabel) :Kind "Secondary")
  (Class|UIStyle|StyleButton :Button (Variables|WBP_ActionBuilder|GetAroundBtn) :Label (Variables|WBP_ActionBuilder|GetAroundLabel) :Kind "Secondary")
  (Class|UIStyle|StyleButton :Button (Variables|WBP_ActionBuilder|GetNoneBtn) :Label (Variables|WBP_ActionBuilder|GetNoneLabel) :Kind "Paper"))
```

The node names are the ones `UIStyle.StylePanel`, `WBP_Stage.StyleClapper` and `WBP_EndScreen`'s event graph already use. `Appearance|SetBrush` resolves to the Border's `SetBrush` (T32). **Contrast:** white on Inset is about 19:1; the labels are T33's pairs (white on plum 14.0:1, dark on paper 12.7:1).

`FillLists.txt`:

```lisp
; T64: the seven action buttons as lists, in the spec's order, so Refresh can walk them.
(fn FillLists ()
  (clear (V ActBtns))
  (clear (V ActLbls))
  (add (V ActBtns) (Variables|WBP_ActionBuilder|GetMoveBtn))
  (add (V ActBtns) (Variables|WBP_ActionBuilder|GetLookBtn))
  (add (V ActBtns) (Variables|WBP_ActionBuilder|GetGrabBtn))
  (add (V ActBtns) (Variables|WBP_ActionBuilder|GetThrowBtn))
  (add (V ActBtns) (Variables|WBP_ActionBuilder|GetGiveBtn))
  (add (V ActBtns) (Variables|WBP_ActionBuilder|GetAroundBtn))
  (add (V ActBtns) (Variables|WBP_ActionBuilder|GetNoneBtn))
  (add (V ActLbls) (Variables|WBP_ActionBuilder|GetMoveLabel))
  (add (V ActLbls) (Variables|WBP_ActionBuilder|GetLookLabel))
  (add (V ActLbls) (Variables|WBP_ActionBuilder|GetGrabLabel))
  (add (V ActLbls) (Variables|WBP_ActionBuilder|GetThrowLabel))
  (add (V ActLbls) (Variables|WBP_ActionBuilder|GetGiveLabel))
  (add (V ActLbls) (Variables|WBP_ActionBuilder|GetAroundLabel))
  (add (V ActLbls) (Variables|WBP_ActionBuilder|GetNoneLabel))
  (set ActVerbs (Utilities|String|ParseIntoArray "move look grab throw give around none")))
```

`ParseIntoArray` splits on spaces by default (`CapWords.txt` uses it that way), which avoids a literal on `Array Add`'s wildcard pin (T01). The verbs are T63's words.

**The turn.** `Arm.txt`:

```lisp
; T64: BP_Show.StartTurn arms the builder for my scene turn (through WBP_Stage.BuilderTurn). It opens when the
; turn's header shows on screen (PhaseShown), after the last turn's lines have played (T30's queue).
(fn Arm (Seat)
  (set ArmSeat Seat)
  (set PendingTurn true))
```

`PhaseShown.txt`:

```lisp
; T64: WBP_Stage.SetPhase calls it with the input box's text each time a header shows (the "phase" cue). A header
; right after Arm opens my scene turn; any other header closes the builder (step 8: it shows only in my scene turns).
(fn PhaseShown (Text)
  (if (V PendingTurn)
    (set PendingTurn false)
    (set Line Text)
    (CallFunction|OpenTurn)
    (return))
  (CallFunction|Close))
```

`OpenTurn.txt`:

```lisp
; T64: a scene turn opens: No action picked, nothing else picked, the choices read from the rules' state as the last
; turn left it (the same state the AIs read). Players show by their screen names, so the names come from BP_Show.
(fn OpenTurn ()
  (set Show (Actor|GetActorOfClass :ActorClass "/Game/NHOS/Core/BP_Show.BP_Show_C"))
  (set Dir (Actor|GetActorOfClass :ActorClass "/Game/NHOS/Stage/BP_StageDirector.BP_StageDirector_C"))
  (set Seat (V ArmSeat))
  (set Names (Class|BPShow|GetSeatName :self (V Show)))
  (set Labels (Class|BPShow|GetSeatLabel :self (V Show)))
  (set Verb "none")
  (set Item "")
  (set Target "")
  (set Armed true)
  (set Sent false)
  (CallFunction|ReadOk)
  (CallFunction|Refresh)
  (Widget|SetVisibility :self self :InVisibility "SelfHitTestInvisible")
  (bind _ids (Class|BPShow|GetSeatId :self (V Show)))
  (bind _turn (Class|BPShow|GetTurnNum :self (V Show)))
  (print (cat "NHOS: BUILDER open turn=" (str _turn) " seat=" (get _ids (V Seat)) " greyed=" (V GreyList))))
```

- `GetActorOfClass` is `StagePrep.txt`'s and `WBP_EndScreen`'s form. With no director, `ReadOk` greys the five actions that need a choice ("The stage isn't ready.") and `BuildChips` adds no chip, so nothing reads a None reference.
- **The `Show` and `Dir` setters take an actor reference from `GetActorOfClass`.** If `set` can't cast it, give each variable the `Actor` type and cast at the call, or bind the result and use `Utilities|Casting|CastTo...` (`get_node_type_pins`).

`Close.txt`:

```lisp
; T64: Free Talk, the vote, the reactions, Scene Prep and a restart: no builder (T66 shapes those phases).
(fn Close ()
  (set Armed false)
  (set PendingTurn false)
  (Widget|SetVisibility :self self :InVisibility "Collapsed"))
```

`SetLive.txt`:

```lisp
; T64: WBP_Stage.SetPrompt tells the builder when my input opens and closes (CanType): closed while the lines play
; (T30) and after I send.
(fn SetLive (On)
  (set Live On)
  (if (V Armed)
    (CallFunction|Refresh)))
```

`SetLine.txt`:

```lisp
; T64: the typed line, live, for the preview line (WBP_Stage's OnTextChanged on the input box). After I send, the
; preview keeps the turn I sent, so the box being cleared doesn't change it.
(fn SetLine (Text)
  (if (V Sent)
    (return))
  (set Line Text)
  (bind _p (CallFunction|PreviewText))
  (Class|Text|SetText :self (Variables|WBP_ActionBuilder|GetPreviewText) :Text (Utilities|Text|ToText(String) _p)))
```

**The send.** `IsReady.txt`:

```lisp
; T64: true when the picked action has every chip it needs. No action and Look around are always ready.
(fn IsReady ()
  (bind _ni (CallFunction|NeedsItem :Act (V Verb)))
  (bind _nt (CallFunction|NeedsTarget :Act (V Verb)))
  (return (and (or (not _ni) (not (Utilities|String|IsEmpty (V Item)))) (or (not _nt) (not (Utilities|String|IsEmpty (V Target)))))))
```

`GetAction.txt`:

```lisp
; T64: the action as built, for T63's SendHumanTurn: Verb (move, look, grab, throw, give, around, none), Item and Target
; (prop, place and Player names). An unfinished action comes back as a look around with Ready false, the fallback a bot
; gets (T66's timer sends it that way; Action! and Enter wait for Ready).
(fn GetAction ()
  (bind _r (CallFunction|IsReady))
  (if _r
    (return (V Verb) (V Item) (V Target) true))
  (return "around" "" "" false))
```

`Seal.txt`:

```lisp
; T64: Action! or Enter (or T66's timer) sends my turn: BP_Show.HandleSend takes the action through WBP_Stage.TakeAction.
; From here until the next turn opens, the builder is disabled and the preview keeps the turn I sent (step 7).
(fn Seal ()
  (bind (_v _i _t _r) (CallFunction|GetAction))
  (if (V Armed)
    (set Sent true)
    (CallFunction|Refresh))
  (bind _di (select (Utilities|String|IsEmpty _i) "-" _i))
  (bind _dt (select (Utilities|String|IsEmpty _t) "-" _t))
  (print (cat "NHOS: BUILDER send " _v " " _di " " _dt " ready=" (select _r "yes" "no")))
  (return _v _i _t _r))
```

`Blocks.txt`:

```lisp
; T64: true while my scene turn is open and the picked action still lacks a chip: Action! is greyed and Enter does nothing.
(fn Blocks ()
  (if (or (not (V Armed)) (V Sent))
    (return false))
  (bind _r (CallFunction|IsReady))
  (return (not _r)))
```

`IsOn.txt`:

```lisp
; T64: true while the builder is up (my scene turn, before and after I send). WBP_Stage.FitBuilder reads it.
(fn IsOn ()
  (return (V Armed)))
```

### 2d. The event graph

Bind each button's `OnClicked` first with `UMGToolSet.BindToEventProperty` (T04), then write `Graphs/WBP_ActionBuilder/EventGraph.txt`:

```lisp
; WBP_ActionBuilder.EventGraph (T64). The action builder for my scene turns (the Turn Input tab): the preview line, the
; seven actions and the chips of the picked one. Every color, size and font comes from UIStyle. No button or chip takes
; keyboard focus (IsFocusable off in the designer), so what I type stays in WBP_Stage's input box while I click.
(event UserInterface|EventPreConstruct (IsDesignTime)
  (CallFunction|StyleAll)
  (if IsDesignTime
    (Class|Text|SetText :self (Variables|WBP_ActionBuilder|GetPreviewText) :Text (Utilities|Text|ToText(String) "> throw rose at @Meta: \"Oops, my servo slipped.\""))))

(event UserInterface|EventConstruct
  (CallFunction|FillLists)
  (CallFunction|Close))

(event OnClicked(MoveBtn)
  (CallFunction|PickVerb :Act "move"))

(event OnClicked(LookBtn)
  (CallFunction|PickVerb :Act "look"))

(event OnClicked(GrabBtn)
  (CallFunction|PickVerb :Act "grab"))

(event OnClicked(ThrowBtn)
  (CallFunction|PickVerb :Act "throw"))

(event OnClicked(GiveBtn)
  (CallFunction|PickVerb :Act "give"))

(event OnClicked(AroundBtn)
  (CallFunction|PickVerb :Act "around"))

(event OnClicked(NoneBtn)
  (CallFunction|PickVerb :Act "none"))
```

`StyleAll` styles No action as paper at design time, so the designer shows the picked look. Compile with warnings as errors, save.

## 3. `WBP_Chip` (new)

`Content/NHOS/UI/WBP_Chip.uasset`. Its graphs go in `Graphs/WBP_Chip/`.

### 3a. The widget tree

```
ChipButton        Button (root); IsFocusable off
└ ChipRow         HorizontalBox
  ├ SeatBar       SizeBox; WidthOverride 6 (SeatBar), HeightOverride 20; slot: VAlign Center, padding right 8 (S2); Collapsed at design time
  │ └ SeatFill    Border (no padding)
  └ ChipLabel     TextBlock; text "rose"; slot VAlign Center
```

`bIsVariable` on for `ChipButton`, `SeatBar`, `SeatFill` and `ChipLabel`. The button's own padding comes from `StyleButton` (20 and 8), so a chip is 48 px tall like every button.

### 3b. Variables and graphs

Variables: `Builder` (`WBP_ActionBuilder` object reference), `ChipIndex` (Integer, -1). Function: `Setup(Owner, Index, Label, Actor, Picked)` (`Owner`: `WBP_ActionBuilder` object reference; `Index`: Integer; `Label`: String; `Actor`, `Picked`: Boolean).

`Graphs/WBP_Chip/Setup.txt`:

```lisp
; WBP_Chip.Setup(Owner, Index, Label, Actor, Picked), called by WBP_ActionBuilder.AddChip (T64). One choice of the picked
; action: paper when picked, plum otherwise (UIStyle's Paper and Secondary buttons). An actor's chip has a seat-color bar
; before its screen name, so the seat shows by color and by name. The button never takes keyboard focus.
(fn Setup (Owner Index Label Actor Picked)
  (set Builder Owner)
  (set ChipIndex Index)
  (Class|UIStyle|StyleButton :Button (Variables|WBP_Chip|GetChipButton) :Label (Variables|WBP_Chip|GetChipLabel) :Kind (select Picked "Paper" "Secondary"))
  (Class|Text|SetText :self (Variables|WBP_Chip|GetChipLabel) :Text (Utilities|Text|ToText(String) Label))
  (if (not Actor)
    (Widget|SetVisibility :self (Variables|WBP_Chip|GetSeatBar) :InVisibility "Collapsed")
    (return))
  (bind cQuiet (Class|UIStyle|UIColor :Role "Quiet"))
  (bind cBar (Class|UIStyle|SeatColor :Name Label :Fallback cQuiet))
  (bind cInk (Class|UIStyle|UIColor :Role "InkSolid"))
  (bind trim (Class|UIStyle|UISize :Role "PanelTrim"))
  (bind rad (Class|UIStyle|UISize :Role "S1"))
  (bind bBar (Class|UIStyle|Brush :Fill cBar :Outline cInk :Width trim :Radius rad))
  (Class|Border|SetBrushColor :self (Variables|WBP_Chip|GetSeatFill) :BrushColor (Utilities|Struct|MakeLinearColor 1.0 1.0 1.0 1.0))
  (Appearance|SetBrush :self (Variables|WBP_Chip|GetSeatFill) :InBrush bBar)
  (Widget|SetVisibility :self (Variables|WBP_Chip|GetSeatBar) :InVisibility "HitTestInvisible"))
```

The bar has an ink outline, so lime and pale blue still show on a picked (paper) chip, as T33 did for the end cards' seat bars.

Bind `ChipButton`'s `OnClicked`, then `Graphs/WBP_Chip/EventGraph.txt`:

```lisp
; WBP_Chip.EventGraph (T64): a click tells the builder which choice this chip is.
(event OnClicked(ChipButton)
  (Class|WBPActionBuilder|ChipClicked :self (V Builder) :Index (V ChipIndex)))
```

Compile with warnings as errors, save. The chip calls the builder and the builder makes chips; Blueprints allow that. The order in part 2c (builder's `ChipClicked` first) keeps both compiling.

## 4. `WBP_Stage`

### 4a. Which graphs, which have files

| Graph | File in `Graphs/WBP_Stage/` | T64 changes | How |
|---|---|---|---|
| `BuilderTurn(Seat)`, `TakeAction`, `SyncAction`, `FitBuilder` | new | new | `add_function_graph`, params, compile, then write (4c) |
| `SetPrompt` | `SetPrompt.txt` | the builder hears `CanType`; Action! moves to `SyncAction` | Rewrite from the file (4d) |
| `SetPrepMode` | `SetPrepMode.txt` | Scene Prep closes the builder; Action! is styled Primary | Rewrite from the file (4e) |
| `SetPhase` | **none** | one call at the end | Read first (survey 2), then write with a new file (4f) |
| `SubmitInput` | **none** | a gate at the start; an empty line goes through in a scene turn | Read first (survey 2), then write with a new file (4g) |
| EventGraph | `EventGraph.StartButton.txt` only | a new `OnTextChanged(InputBox)` chain | A partial write with a new file, `EventGraph.Builder.txt` (4h) |
| `SetPassEnabled`, `SetTyping`, `ShowBanner`, `NextBanner`, `FadeBanner`, `SetClapper`, `StyleClapper` | yes | nothing | — |

**New variables:** `LastBlock` (Boolean, false), `LowerWide` (Float, 640), `LowerWideBuild` (Float, 1000), `ChatTall` (Float, 380), `ChatTallBuild` (Float, 160). Set the two plain ones to the values survey 1 read from the designer, if they differ. With question 1's second answer: `LowerWideBuild` = `LowerWide` and `ChatTallBuild` 100. With the third: both equal the plain values.

### 4b. The widget tree

1. **The builder:** add a `WBP_ActionBuilder` (the user widget) to `LowerBox` as the child right before `InputRow`, named **`ActionBuilder`**, `bIsVariable` on. Slot: HAlign Fill, padding top 0, bottom 8 (`S2`). It collapses itself on `Construct`, so the designer's visibility doesn't matter.
2. **Action!:** `SendLabel`'s designer text becomes `Action!`. `SendButton` keeps its name and `IsFocusable` off (T04). Its look comes from `SetPrepMode` (4e).
3. **Check:** `LowerSize`, `ChatSize` and `LogScroll` are variables (survey 1).
4. No other widget changes. T65 adds the counter and T66 the timer to `InputRow` after `SendButton`'s place (T65 step 1 puts the counter left of Action!).

### 4c. The new functions

`Graphs/WBP_Stage/BuilderTurn.txt` (input `Seat`, Integer):

```lisp
; T64: BP_Show.StartTurn calls this once per scene turn, just before the turn's header cue. It only arms the builder:
; the builder opens when that header shows on screen (SetPhase), so it never opens over the last turn's lines (T30).
(fn BuilderTurn (Seat)
  (Class|WBPActionBuilder|Arm :self (Variables|WBP_Stage|GetActionBuilder) :Seat Seat))
```

`Graphs/WBP_Stage/TakeAction.txt` (outputs `Verb`, `Item`, `Target`: String; `Ready`: Boolean):

```lisp
; T64: what Action! sends. BP_Show.HandleSend calls it in a scene turn, right before SendHumanTurn (T63), and passes
; Verb, Item and Target on with the typed line. It seals the builder until the next turn. An unfinished action comes
; back as a look around with Ready false; only T66's timer can send one, since Action! and Enter wait for Ready.
(fn TakeAction ()
  (bind (_v _i _t _r) (Class|WBPActionBuilder|Seal :self (Variables|WBP_Stage|GetActionBuilder)))
  (return _v _i _t _r))
```

`Graphs/WBP_Stage/SyncAction.txt`:

```lisp
; T64: Action! (SendButton) is on while I can type (LastCanType) and the builder holds no unfinished action. Greyed by
; the builder, its tip says why. SetPrompt calls this every frame; the tip changes only when the reason does, so a
; tooltip on screen doesn't flicker.
(fn SyncAction ()
  (bind _blk (Class|WBPActionBuilder|Blocks :self (Variables|WBP_Stage|GetActionBuilder)))
  (Widget|SetIsEnabled :self (Variables|WBP_Stage|GetSendButton) :bInIsEnabled (and (Variables|Default|GetLastCanType) (not _blk)))
  (if (xor _blk (V LastBlock))
    (set LastBlock _blk)
    (Widget|SetToolTipText :self (Variables|WBP_Stage|GetSendButton) :InToolTipText (Utilities|Text|ToText(String) (select _blk "Pick a target first." "")))))
```

`Graphs/WBP_Stage/FitBuilder.txt`:

```lisp
; T64 (question 1): while the builder shows, the lower panel widens and the chat shortens, so the panel's top doesn't
; move up over the robots (T27) and the seven actions fit one row. The chat stays scrolled to its newest line.
(fn FitBuilder ()
  (bind _on (Class|WBPActionBuilder|IsOn :self (Variables|WBP_Stage|GetActionBuilder)))
  (Class|SizeBox|SetWidthOverride :self (Variables|WBP_Stage|GetLowerSize) :InWidthOverride (select _on (V LowerWideBuild) (V LowerWide)))
  (Class|SizeBox|SetHeightOverride :self (Variables|WBP_Stage|GetChatSize) :InHeightOverride (select _on (V ChatTallBuild) (V ChatTall)))
  (Class|ScrollBox|ScrollToEnd :self (Variables|WBP_Stage|GetLogScroll)))
```

If survey 1 found `LogScroll` inside a VerticalBox with `TypingText` (not directly in `ChatSize`), `ScrollToEnd` still works on it. If `LowerSize` has no width override (a slot width instead), change the slot's size there and note it under "Findings".

### 4d. `SetPrompt` (rewrite from `SetPrompt.txt`)

Two changes in the `(if (xor CanType ...))` block, and one call at the end. The whole new file:

```lisp
; T64: the builder hears when my input opens (SetLive), and Action! (SendButton) follows SyncAction every frame instead
; of the CanType block, so an unfinished action keeps it greyed.
(fn SetPrompt (Turn Hint CanType)
  (Widget|SetRenderOpacity :self (Variables|WBP_Stage|GetHintLabel) :InOpacity (select (Utilities|Text|TextIsEmpty :InText (Class|TextBox|GetText :self (Variables|WBP_Stage|GetInputBox))) 1.0 0.0))
  (if (not (Utilities|String|EqualExactly(String) Turn (Variables|Default|GetLastTurn)))
    (Variables|Default|SetLastTurn Turn)
    (Class|Text|SetText :Text (Utilities|Text|ToText(String) Turn) :self (Variables|WBP_Stage|GetTurnText)))
  (if (not (Utilities|String|EqualExactly(String) Hint (Variables|Default|GetLastHint)))
    (Variables|Default|SetLastHint Hint)
    (Class|Text|SetText :Text (Utilities|Text|ToText(String) Hint) :self (Variables|WBP_Stage|GetHintLabel)))
  (if (xor CanType (Variables|Default|GetLastCanType))
    (Variables|Default|SetLastCanType CanType)
    (Widget|SetIsEnabled :self (Variables|WBP_Stage|GetInputBox) :bInIsEnabled CanType)
    (Widget|SetIsEnabled :self (Variables|WBP_Stage|GetPassButton) :bInIsEnabled (and CanType (Variables|Default|GetPassOn)))
    (Class|WBPActionBuilder|SetLive :self (Variables|WBP_Stage|GetActionBuilder) :On CanType)
    (Class|Text|SetColorandOpacity :ColorAndOpacity (Utilities|Struct|MakeSlateColor (select CanType (Utilities|Struct|MakeLinearColor 1.0 0.85 0.45 1.0) (Utilities|Struct|MakeLinearColor 0.8 0.83 0.9 1.0))) :self (Variables|WBP_Stage|GetTurnText))
    (if CanType
      (Widget|SetKeyboardFocus :self (Variables|WBP_Stage|GetInputBox))))
  (CallFunction|SyncAction))
```

- Gone from the block: `(Widget|SetIsEnabled :self (Variables|WBP_Stage|GetSendButton) :bInIsEnabled CanType)`. `SyncAction` sets it every frame, after `LastCanType` is set.
- `UpdatePrompt` calls `SetPrompt` once a frame (T27), so `SyncAction` runs once a frame: one `Blocks` call and one `SetIsEnabled`.
- The turn line's colors are T27's literals. T34 moves them to `UIStyle`; T64 leaves them.

### 4e. `SetPrepMode` (rewrite from `SetPrepMode.txt`)

```lisp
; T64: Scene Prep closes the builder and gives the lower panel back its size; the play side styles Action! as the one
; Primary button (gold, ink text: "act now").
(fn SetPrepMode (Prep)
  (if Prep
    (Widget|SetVisibility :self (Variables|WBP_Stage|GetPrepBox) :InVisibility "SelfHitTestInvisible")
    (Widget|SetVisibility :self (Variables|WBP_Stage|GetStartButton) :InVisibility "Visible")
    (Widget|SetVisibility :self (Variables|WBP_Stage|GetSendButton) :InVisibility "Collapsed")
    (Widget|SetVisibility :self (Variables|WBP_Stage|GetPassButton) :InVisibility "Collapsed")
    (Class|WBPActionBuilder|Close :self (Variables|WBP_Stage|GetActionBuilder))
    (CallFunction|FitBuilder)
    (else
      (Widget|SetVisibility :self (Variables|WBP_Stage|GetPrepBox) :InVisibility "Collapsed")
      (Widget|SetVisibility :self (Variables|WBP_Stage|GetStartButton) :InVisibility "Collapsed")
      (Widget|SetVisibility :self (Variables|WBP_Stage|GetSendButton) :InVisibility "Visible")
      (Widget|SetVisibility :self (Variables|WBP_Stage|GetPassButton) :InVisibility "Visible")
      (Class|UIStyle|StyleButton :Button (Variables|WBP_Stage|GetSendButton) :Label (Variables|WBP_Stage|GetSendLabel) :Kind "Primary"))))
```

- `SetPrepMode(true)` runs at every Scene Prep, a restart included (T28), so a restart can't leave a builder up.
- `SetPrepMode(false)` runs from `StartFromPrep` right before `StartScene` → `StartTurn`, so Action! is gold before my first turn. T32 row 5 wants Send Primary on my move and Secondary otherwise; T34 can split it.

### 4f. `SetPhase` (no file; read first)

Read `SetPhase` (survey 2) and write it back from what you read, with one change: at the end of the function, add

```lisp
  ; T64: the builder opens at my scene turn's header and closes at any other (WBP_ActionBuilder.PhaseShown).
  (bind _typed (Utilities|String|ToString(Text) (Class|TextBox|GetText :self (Variables|WBP_Stage|GetInputBox))))
  (Class|WBPActionBuilder|PhaseShown :self (Variables|WBP_Stage|GetActionBuilder) :Text _typed)
  (CallFunction|FitBuilder)
```

and the header comment `; T64: also opens or closes the action builder (PhaseShown, FitBuilder).` Commit the whole function as `Graphs/WBP_Stage/SetPhase.txt`. If the read-back holds anything you can't write back cleanly (T06), place the three nodes by hand at the end of its exec chain instead, delete no file, and write the edit under "Findings".

- **Why the header:** `BP_Show.StartTurn` queues its header through `CueHeader` → `BPC_LinePlayer.Cue("phase")`, and `RunCue` runs `SetPhase` when the queue reaches it, after the last turn's lines (`Graphs/BP_Show/RunCue.txt`). Every other phase (`StartTalkRound`, `EndFreeTalk`, `StartCut`, `StartReactions`, `EndShow`) also queues a header (T30), and Scene Prep comes as a `"prep"` cue that calls `SetPrepMode(true)`. So the builder is up exactly from my scene turn's header to the next phase's header.
- If the queue is idle, `CueHeader` runs `SetPhase` at once, inside `StartTurn`. That is why `BuilderTurn` goes **before** `CueHeader` there (part 5a).

### 4g. `SubmitInput` (no file; read first)

Read `SubmitInput` (survey 2) and write it back from what you read, with a gate as its first statements:

```lisp
  ; T64: while a picked action still lacks a chip, Enter (and a click on the greyed Action!) does nothing (step 7).
  (bind _blk (Class|WBPActionBuilder|Blocks :self (Variables|WBP_Stage|GetActionBuilder)))
  (if _blk
    (print "NHOS: BUILDER blocked")
    (return))
```

and, **if survey 2 found that it skips an empty line**, let an empty line through while the builder is up, so a No action turn with no words sends (T64 step 7):

```lisp
  (bind _bon (Class|WBPActionBuilder|IsOn :self (Variables|WBP_Stage|GetActionBuilder)))
```

with the empty check changed from "the text is empty" to "the text is empty and not `_bon`". If survey 5 found that `HandleSend`'s scene case drops an empty line too, let it through there the same way (in the scene case only, since Free Talk's empty line means nothing to send); T63's `SpellAsk` sends an empty line with no LLM call (T63-build decision 6). Commit the function as `Graphs/WBP_Stage/SubmitInput.txt`. `SendButton`'s `OnClicked` and `OnTextCommitted(InputBox)` both call `SubmitInput`, so one gate covers Action! and Enter.

### 4h. The event graph: the preview follows my typing

`write_graph_dsl` keeps the event chains it doesn't name (`EventGraph.StartButton.txt`'s note), so write only the new chain. Bind `InputBox`'s `OnTextChanged` first with `UMGToolSet.BindToEventProperty` (T04), then write `Graphs/WBP_Stage/EventGraph.Builder.txt`:

```lisp
; Only the builder's chain of WBP_Stage's EventGraph (T64). The rest of EventGraph has no source here.
; The preview line follows what I type, live, with the symbols the fonts can't draw removed first, as in the chat (CleanText).
(event OnTextChanged(InputBox) (Text)
  (bind _clean (CallFunction|CleanText :Text (Utilities|String|ToString(Text) Text)))
  (Class|WBPActionBuilder|SetLine :self (Variables|WBP_Stage|GetActionBuilder) :Text _clean))
```

Use `CleanText`'s real input and output names (survey 2). **T65 extends this chain** (the counter, the 15-word cut) rather than binding a second one.

Compile `WBP_Stage` with warnings as errors, save. Close every game window before you save (T53).

## 5. `BP_Show`

### 5a. `StartTurn`: the one call at each scene turn (no file; node edit)

Insert one node, `Class|WBPStage|BuilderTurn :self (Variables|Default|GetStage) :Seat (Variables|Default|GetHumanSeat)`, in `StartTurn`'s exec chain **right before the `CueHeader` call** (survey 4). Link the node that led into `CueHeader` to `BuilderTurn`, and `BuilderTurn`'s exec out to `CueHeader`. T28's insert recipe; place it after `WBP_Stage` compiles (T18).

- It runs on every scene turn, with autoplay too: the builder opens, shows "> stand still" and stays disabled while autoplay sends (T63's `AutoTurn`, in the same graph since T63's node edit 5e.3, picks its own action). `BuilderTurn` doesn't touch that call.
- If `StartTurn` checks that `Stage` is valid before the header, put the node inside that branch.
- Write the edit under "Findings" in `T64.md` (no file).

### 5b. `HandleSend`: the built action goes to `SendHumanTurn` (no file; node edit)

In the `"scene"` branch, T63 calls `SendHumanTurn` with `Verb` `none`, `Item` `""`, `Target` `""` and the typed line (T63-build 5e.2, "the bridge until T64"; its part 8 asks T64 to replace it). Put one node, `Class|WBPStage|TakeAction :self (Variables|Default|GetStage)`, in the exec chain right before that call, and wire its `Verb`, `Item` and `Target` outputs into `SendHumanTurn`'s three pins. `Line` stays as T63 wired it.

- `TakeAction` seals the builder and prints `NHOS: BUILDER send ...`, so it must run only when the turn is really sent: after `HandleSend`'s checks that the phase is "scene" and `HumanSent` is false, never on a refused send.
- **Autoplay doesn't pass here:** `StartTurn` calls T63's `AutoTurn`, which brings its own random allowed action (T63-build 5e.3). So `TakeAction` runs only for a typed turn, and run B shows no `BUILDER send` line.
- `SendHumanTurn` lower-cases and trims the fields and pre-checks them with `CanDo` (T63-build 5d), so the builder's Player, prop and place names go in exactly as T62's lists gave them.
- Write the edit under "Findings".

### 5c. `ComputePrompt`: the hints follow (step 9; no file; two literals)

Two text literals, found by their text (survey 6). The byte search of `BP_Show.uasset` at `3911715` found each twice (the pin and the compiled script):

| Now | New |
|---|---|
| ` of 3. YOUR MOVE: everyone acts at once. Type what your robot does and says.` | ` of 3. YOUR MOVE: pick an action, say a line if you like, then press Action!` |
| `Type what you do and say, like: walk to Left and say "Hi, @Meta!"` | `Say something (optional)...` |

- Change each pin's default value; don't rewrite the graph (its read-back is lossy, T28, T55).
- The first is the turn line on my scene turn ("Turn 1 of 3. YOUR MOVE: ..."). " of 3. Type what your robot does and says." also sits in the bytes; if `find_nodes` shows it live in `ComputePrompt` (not an orphan), change its tail the same way.
- The hint is about 27 characters, so it no longer cuts off (T32 row 12). It is the spec's speech-field hint, which T65 keeps.
- Other phases' hints ("Say something, like: @Meta, why did you grab the rose?", the vote's and the reactions') don't mention actions, so they stay.
- Run the byte search again after the save (`LC_ALL=C grep -a -c "Type what your robot" Content/NHOS/Core/BP_Show.uasset` gives 0, or only the orphan's copies).

Compile `BP_Show` with warnings as errors; the editor log after the compile has no `LogBlueprint: Error`. Close every game window before you save (T53).

## 6. The order of the build

1. Part 0 (claim, locks, reads, survey).
2. `F_Mono`, then `UIStyle` (part 1). Compile, save.
3. `WBP_ActionBuilder`: the tree, the variables, every function with its parameters (empty), compile (part 2c's table).
4. `WBP_Chip`: the tree, variables, `Setup`, the event graph. Compile, save (part 3).
5. `WBP_ActionBuilder`'s graphs, callee first: `NeedsItem`, `NeedsTarget`, `ScreenName`, `PreviewName`, `WhyNot`, `ReadOk`, `PreviewText`, `AddChip`, `BuildChips`, `Refresh`, `PickLine`, `IsReady`, `GetAction`, `StyleAll`, `FillLists`, `Arm`, `Close`, `OpenTurn`, `PhaseShown`, `SetLive`, `SetLine`, `PickVerb`, `ChipClicked`, `Seal`, `Blocks`, `IsOn`; then the event graph. Compile with warnings as errors, save. Batch the writes with `ProgrammaticToolset.execute_tool_script` and `AssetTools.read_file` (T33), a few per call to stay under 100 s.
6. `WBP_Stage`: the tree (4b), the variables, the new functions (4c), `SetPrompt`, `SetPrepMode`, `SetPhase`, `SubmitInput`, the event graph chain. Compile, save.
7. `BP_Show`: 5a, 5b, 5c. Compile, save.
8. The check (part 7).

## 7. The check

**Before the runs:** `Local/switches.json` (in the repo folder; a worktree has no `Local/`) with `"mode": "free"`, `"autoplay": false`, `"fast_lines": false`, `"ai_seats": 0`, `"spare_human": false`, `"force_tie": false`. PIE in a floating window: `LevelEditorPlaySettings` `newWindowWidth` 1600, `newWindowHeight` 900 (T33's names; put them back after). Pick **Test for Free** on the title. On the PC the Slate inspector's `Click` and `Type` land (T33's Mac problem doesn't apply). Screenshots with `SlateInspectorToolset.Screenshot` (true colors, T32), saved to `Saved/T64/shots/` (not in git).

### Run A: one show played by hand in PIE

1. **`turn1_open.png`:** press Start the scene. At turn 1, once the lines stop: the builder shows over the input box, **No action** in paper, **Throw and Give greyed**, the preview `> stand still`, Action! gold, the lower panel wider and the chat shorter (question 1). Log: `NHOS: BUILDER open turn=1 seat=human greyed=throw,give`.
2. **`turn1_tip.png`:** hover Throw: the tooltip "Grab something first." With no hover action in the Slate inspector (survey 9), read the button's tooltip text in PIE through MCP (`GetToolTipText` on `ThrowBtn`), screenshot the greyed state, and write under "Findings" that the hover itself wasn't shot. Computer use on the editor needs my person's OK; ask only if the hover matters.
3. **The focus check:** click the input box once, `Type` "Mine now", click **Grab** (`Click` on `GrabBtn`), `Type` ", finders keepers." Every letter lands in the box (the preview shows the whole line).
4. **`turn1_grab.png`:** Grab in paper, the card's four props as chips. Log: `NHOS: BUILDER pick grab - - | > grab ...: "Mine now, finders keepers."`.
5. **`turn1_unfinished.png`:** while no prop is picked, Action! is greyed. Press Enter in the box: nothing is sent, and the log prints `NHOS: BUILDER blocked` and no `NHOS: HUMAN`. Hover Action! for "Pick a target first." (or read its tooltip, as in shot 2).
6. **`turn1_chip.png`:** click a prop chip: it turns paper, Action! lights, the preview reads `> grab <prop>: "Mine now, finders keepers."`. Log: `NHOS: BUILDER pick grab <prop> - | ...`.
7. Press **Action!**. Log, in this order: `NHOS: BUILDER send grab <prop> - ready=yes`, then T63's `NHOS: HUMAN grab <prop> - says=Mine now, finders keepers.` (the whole line: every letter reached the box). Later: T62's `NHOS: HOLD <prop> human`, the `NHOS: LOG` line with "grabs the <prop>", and my robot's `NHOS: ACT human grab ...` when it plays. **`turn1_sent.png`:** the builder and Action! disabled, the preview still showing the sent turn. **`turn1_play.png`:** my robot holding the prop, and my line in the chat.
   - **If a free bot grabbed the same prop first** (T62: the first in the log's order gets it), my grab falls back: `NHOS: ACT human look around - (someone holds it: ...)`. Grab another prop on turn 2 and throw on turn 3.
8. **`turn2_throw.png`:** turn 2 opens: `NHOS: BUILDER open turn=2 seat=human greyed=-` (or `grab` if every prop is held). Click **Throw**: the one chip is the held prop, the preview `> throw ...`.
9. **`turn2_targets.png`:** click the prop: it stays as the first chip (paper), then the actors on stage (each with its seat bar, by screen name, never me) and the places. The preview `> throw <prop> at ...`.
10. Click **Meta** (or any actor), type "Oops, my servo slipped.", press **Enter**. Log: `NHOS: BUILDER send throw <prop> Player <n> ready=yes`, `NHOS: HUMAN throw <prop> Player <n> says=Oops, my servo slipped.`, later `NHOS: HOLD <prop> -` and my robot's throw. **`turn2_play.png`:** the throw on stage.
11. **Turn 3:** leave No action, type nothing, press Action!. Log: `NHOS: BUILDER send none - - ready=yes`, then `NHOS: HUMAN none - - says=-` (T63's `HumanSay`), with no `NHOS: SPELLING` line (an empty line makes no call). My robot stands still, and its `NHOS: LOG` line says "stands still".
12. **`freetalk.png`:** Free Talk starts: no builder, the lower panel back to 640 × 380, Action! and Pass in the input row.
13. **`turn1_open_p12.png`:** optional, the same as shot 1 at 1280 × 720 (the doc checks both sizes).

Then stop PIE. In every shot check that no robot, name tag or thrown prop sits behind the lower panel (T27, the doc's rule), and that the leftmost robot is clear.

### Run B: a free autoplay show in a game window

`"autoplay": true`, `"fast_lines": true`, `"mode": "free"`; the game-window command from `CLAUDE.local.md` with `-log=T64auto.log`. It plays the saved assets. Look for, in `Saved/Logs/T64auto.log`:

- `NHOS: SHOW END` and **no `LogScript` line** (above all no "Accessed None" and no "Attempted to access index").
- One `NHOS: BUILDER open turn=<t>` for each scene turn played (3 per scene), each near T63's autoplay `NHOS: HUMAN` line (`AutoTurn` sends at once, so the `HUMAN` line may come first: the builder opens at the header on screen). No `NHOS: BUILDER send` lines: autoplay doesn't take the builder's action (part 5b).
- The `NHOS: LOG` lines in the same form as before (T62 and T63's runs).

Close the game window (match its `-log=` name, so the editor is spared).

### Run C: the checker

`python Tools/check_prompts.py --offline` passes. If T62 or T63 gave it a `--log` mode that reads `HUMAN` or `ACT` lines, run it on `T64auto.log` too.

**Afterward:** set `autoplay` and `fast_lines` back to false in `Local/switches.json`, put the PIE window settings back, close each game window.

### Findings to write in `T64.md`

- **Step 6's pick:** No action with an empty line reads `> stand still` (and with a line, `> stand still: "..."`).
- **The design review** (the Done-when's last line), from the shots, as a critical first-time player: can I tell which action is picked, what each greyed action needs, what the chips mean before I click, and when my turn is ready to send; does the preview read as "what my robot will do"; does the shorter chat hide what I need from the last turn. Name what you'd change for T34.
- The node edits in `StartTurn`, `HandleSend` and `ComputePrompt`, old and new (no files). Whether `SetPhase` and `SubmitInput` were written from a read-back or edited by hand.
- What survey 8 and 9 found (the font's typeface name; the hover).
- **Unreal MCP rules found in this task**, as earlier tasks do.

## 8. The commit

One commit, `T64: The action builder, the preview line and Action!`: `Content/NHOS/UI/WBP_ActionBuilder.uasset`, `Content/NHOS/UI/WBP_Chip.uasset`, `Content/NHOS/UI/Fonts/F_Mono.uasset`, `Content/NHOS/UI/WBP_Stage.uasset`, `Content/NHOS/Core/BP_Show.uasset`, `Content/NHOS/UI/Style/UIStyle.uasset`; `Graphs/WBP_ActionBuilder/` (all), `Graphs/WBP_Chip/` (`Setup.txt`, `EventGraph.txt`), `Graphs/WBP_Stage/` (`BuilderTurn`, `TakeAction`, `SyncAction`, `FitBuilder`, `SetPhase`, `SubmitInput`, `EventGraph.Builder` new; `SetPrompt`, `SetPrepMode` changed), `Graphs/UIStyle/UIFont.txt` and `UISize.txt`; `Docs/Assets.md` (the `F_Mono` row). The plan's Touches name neither `F_Mono.uasset` (it names `UIStyle.uasset` "only to add a mono font") nor `Docs/Assets.md`, so name both in the message; `Docs/tasks/T64.md` (Result, Findings), `Docs/Plan.md` (the box, the "Next up" line), `Docs/DevLog.md`. Stage by path. `F_Mono.uasset` is new: check `.gitattributes` sends `.uasset` to LFS (it does). Unlock the three assets after the push.

## 9. Knock-on: tell, don't change

- **The design doc's UI section** (Art Inspiration tab), which still describes typing a turn. Show my person, edit only after their OK (the plan's "The design doc follows the game"):
  - Components, the "Input row" row: "Dark box with a 2 px outline, a gold Send and an outline Pass." → "Dark box with a 2 px outline, a gold Action! and an outline Pass. In your scene turns the action builder sits above it: the preview line in a mono face, the seven action buttons and the picked action's chips."
  - Screens, "Scene turn, your move", Do next: "Type what your robot does and says" → "Pick an action, add a line if you like, press Action!"
  - Palette and type, after the body face: "Mono face: Droid Sans Mono (ships with the engine), for the preview line only."
  - The doc allows "at most two typefaces". `F_UI` and `F_Mono` make two. **If the display face (Lilita One) is ever imported, that is three:** then use `F_UI` for the preview line (it drops the terminal look) or ask my person to allow three.
- **`Docs/ItchPage.md`, "Controls"** (lines 68 to 73 at `3911715`): "Type in the box ... (or click Send)" and the scene-turn bullet ("say what your robot does and says, in your own words. For example: `walk to Left and say "Hi, @Meta!"`", the verbs, the old eight props) describe typing. After T64: "**Your scene turn:** click an action (Move, Look, Grab, Throw, Give, Look around or No action), then click its chips: a place, a prop or an actor. Type what your robot says, if anything (15 words at most), and press **Action!** or Enter." The props now come from each scene card (T44, T45). T63 also touches these lines; whichever lands last takes them, or a small docs task after T66.
- **`prompts.json` `game`**: "- The human types into a converter that turns their text into the same form as your lines. ..." is T63's (T62-build part 9).
- **T65:** extend `WBP_Stage`'s `OnTextChanged(InputBox)` chain (`EventGraph.Builder.txt`) for the counter and the 15-word cut; put the counter in `InputRow` left of `SendButton`. `PreviewName` is the one place that writes `@Meta` in the preview, for its mention chip. The builder never takes focus, so T65's step 3 only has to check the rest of the screen.
- **T66:** the timer's auto-send calls the same path as Action! (`HandleSend` → `WBP_Stage.TakeAction`): `Ready` false means "unfinished" for `NHOS: TIMEOUT scene unfinished`, and the action is already a look around. `WBP_ActionBuilder.Close` and `IsOn` are there for the other phases. The builder closes itself at every non-scene header, so Free Talk already shows no builder.
- **T34:** the lower panel's size switch (question 1) and Action!'s Primary style in every phase (T32 row 5 wants Secondary off my move); the turn line's two colors in `SetPrompt` are still literals. The builder's buttons never take keyboard focus, on purpose (T34.md step 1 already says so).
- **T61:** a stagehand tip can point at the builder on the first scene turn ("Click an action, then what it acts on.").
