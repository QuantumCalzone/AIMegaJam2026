# T34 build sheet: the in-show screen

Back to [T34](T34.md) and [the plan](../Plan.md). A Mac prep session wrote this on 2026-11-16 (UTC), without the editor, against `noHumansOnSet` at `88cec78` (T64 checked at `4d91f0c`). It is a plan, not a record: nothing here was written to the editor. When T34 writes a graph, its source goes to `Graphs/` as usual.

## Read this first

**What is on the screen today, and what is still coming.** T64 is in: the action builder (`WBP_ActionBuilder`, `WBP_Chip`), the preview line, Action! (`SendButton`, label `SendLabel`) and `FitBuilder`. Still to come, each before T34 (its **Depends on**): T65 (the word counter, the @ list, `HoldFocus`, the preview's mention chips), T66 (the timer, Pass hidden in scene turns), T78 (the emotion chip, the panel at 1000 on the whole play side) and the rest of T38 (the speech bubbles on the robots, the chat hidden behind a Show chat button). Everything in this sheet that one of them moves is marked **⟳ re-check after Txx** and kept short: read what that task built (its Findings, its `Graphs/` files) before you act on it.

**Sources read:** `T34.md` and its plan entry; T32's audit table (`T32.md`, "T32: UI audit"); `Docs/UIStyle.md`; `Graphs/WBP_Stage/` (all 18 files), `Graphs/UIStyle/` (all), `Graphs/BP_Robot/{SetPassed,SetCut,ResetLook,SetPersona,InitHome,InitLift,WatchShow}.txt`, `Graphs/WBP_SpeechBubble/Place.txt`, `Graphs/WBP_EndScreen/{ShowRing,EventGraph}.txt`, `Graphs/BP_Show/{RunCue,CueHeader,CueVotes,MarkPass,LinePrompt,PrepPrompt,LastWordPrompt,DrawCast}.txt`; the Findings of T09, T26, T27, T28, T29, T30, T33, T50, T51, T52, T53, T55, T63 and T64; the T38, T65, T66 and T78 build sheets (only what they leave on the screen); T01's DSL rules.

**Graphs with no file in `Graphs/` (read in the editor first; this sheet doesn't guess their nodes):**

| Blueprint | Graph | What T34 needs from it |
|---|---|---|
| `BP_Show` | `HandleSend` | Row 1: the `#vote` branch. |
| `BP_Show` | `PickVote`, `ShowVotePick` | Row 1: how an index becomes a seat. |
| `BP_Show` | `ComputePrompt` | Rows 4, 5, 12, C5: the turn line and hint literals. |
| `BP_Show` | `CutActor` | Row 17: the stamp text it passes to `SetStamp` and `BP_Robot.SetCut`. |
| `BP_Show` | `ShowPrep`, `ScenePrep` | Rows 13, 14, C3, C4: `SetInfo`, `SetInfoTop`, `SetStageInfo` calls and the cast bars' colors. |
| `BP_Show` | `Tally` | C6: the tally banner's text. |
| `WBP_Stage` | `EventGraph` (all chains but `StartButton` and the builder's) | Row 1 and T33-1: `OnClicked` of `VoteBtn0` to `VoteBtn3`, `PassButton`, `ContinueButton`, `SendButton`; `OnTextCommitted(InputBox)`; whether `EventConstruct` exists. |
| `WBP_Stage` | `SetVoteOptions`, `SetVotePick`, `SetVoteEnabled`, `SetStamp`, `SetContinue`, `AddChatLine`, `ClearLog`, `SetInfo`, `SetInfoTop`, `SetStageInfo`, `CleanText` | Rows 1, 3, 6, 7, 13, 17, C2, C3, C4, C6. |

**Rules from earlier tasks that cost time:**
- `read_graph_dsl` marks the Blueprint it reads as changed (T64). Read only what this sheet lists, and save or revert on purpose.
- `HandleSend` held three dead copies of its graph, cut off from the entry (T63). Trace from `K2Node_FunctionEntry_0`'s `then` before you trust a `find_nodes` hit.
- `write_graph_dsl` keeps the `EventGraph` chains it doesn't name, so a new chain can be written alone (T64, `EventGraph.Builder.txt`).
- `UIStyle`'s functions are impure: bind each result before you use it (T32). Call them as `Class|UIStyle|<Function>`.
- On the Mac, `SlateInspectorToolset.Click` never lands, but `PressKey` and `Type` go to the focused widget (T33). T33-1 is what makes a show playable by keyboard there.
- `WBP_Stage` is laid out in `RootBox` (an Overlay that fills the window, T27); `ProjectWorldLocationtoWidgetPosition` lands in its space (T38 part 1).

**Who holds what (2026-11-16):** the PC's sessions hold `BP_Robot.uasset` and `BPC_LinePlayer.uasset`. T34's **Touches** list neither, and this sheet keeps it that way: the robot tags are hidden from `WBP_Stage` through `BP_Robot`'s `Label` component getter, not by editing `BP_Robot` (see 1c). T34's Touches also lack a new widget; row 2's tag can live inside `WBP_Stage` (no new asset) or in a new `WBP_NameTag` (add it to Touches first, with my person's OK).

**WCAG notes for the checks:** a disabled control is exempt from contrast (WCAG 1.4.3 and 1.4.11 exclude inactive components), so a 40% disabled Pass isn't a failure, but it must still look disabled (C1). Every ratio below that isn't measured from a screenshot was computed from `UIStyle`'s hex values with `python Tools/ui_shots.py --colors`.

## In short: every T34 row

The status column says what T34 does: **change** (a named edit), **confirm only** (an earlier task fixed it; T34 only checks it on screen), or **decide in T34** (with the reason and a recommendation). ⟳ marks parts a later task moves.

| Row | Problem in one line | Where | Status |
|---|---|---|---|
| **1** | The fourth vote button votes for the third name | `BP_Show.HandleSend` `#vote` branch; `WBP_Stage` `OnClicked(VoteBtn3)` | **change, first** (1a) |
| **T33-1** | In-show buttons can't take keyboard focus | `WBP_Stage`: `StartButton`, `VoteBtn0`–`3`, `ContinueButton`; new `ShowRing`, `RingTick`; `SubmitInput` | **change** (1b) ⟳ T65, T66 |
| **T33-2** | Robot tags show through full-screen panels | `BP_Robot`'s `Label` (TextRender), hidden from `WBP_Stage`; row 2's tags | **change** (1c) |
| 2 | Robot name tags: overlap, hidden by set and props, no plate, "ROBOT" in prep | New screen-space tags in `WBP_Stage` (`TagLayer`, `TagTick`) | **change** (2.1) ⟳ T38 |
| 3 | Vote buttons all red; a pick barely shows | `SetVoteOptions`, `SetVotePick`; `UIStyle.StyleButton(..., "Paper")` | **change** (2.2) |
| 4 | The turn said twice; header and line disagree; header width jumps | `SetPhase`, `PhaseHeader`, `HeaderSize`; `ComputePrompt` literals | **change** (2.3), the literals **decide in T34** |
| 5 | My move doesn't stand out | `SetPrompt` (turn colors), `InputBox` style, `SetPrepMode` | **change** (2.4); Action! Primary and Pass hidden in scene turns are **confirm only** (T64; T66 ⟳) |
| 6 | See-through panels; plain boxes | `UIStyle.StylePanel` on `HeaderBar`, `LowerPanel`, the card, `NoteFrame`; new `StyleStage` | **change** (2.5); "collapse the empty chat" ⟳ T38 |
| 7 | Sizes off the scale | `UIStyle.UIFont` / `UISize` in `StyleStage`, `NextBanner`, `SetStamp` | **change** (2.6); the decoy line is **confirm only** (T51, `6ada2ab`) |
| 11 | The oldest chat line cut mid-entry | `ChatSize` > a stepped top fade | **change** (2.7) ⟳ T38 |
| 12 | Hints cut off with an ellipsis | `ComputePrompt` hint literals; `LastWordPrompt.txt` | **change** (2.8); the scene-turn hint is **confirm only** (T64) ⟳ T65 |
| 13 | Scene Prep needs a scroll; one weight for everything | `PrepBox`, `InfoSize`, card text fonts | **decide in T34** (2.9) |
| 14 | Card's cast bars use `BP_Show.SeatColors` | `SetStageInfo` (or wherever `CastBox` is filled) → `UIStyle.SeatColor` | **change** (2.10); robots' bodies **confirm only** (T79–T83 use the doc's colors) |
| 15 | A tie made four banners in a row | `BP_Show.Tally`, `TieCut` | **confirm only** (T52 `d2d4cdc`, T55 `9d76733`) (2.11) |
| 17 | The stamp: flat box, 1.8:1, "META: AI" is cryptic | `StampText` in `StageArea`, `SetStamp` | **change** (2.12) |
| C1 | Button labels fail contrast; enabled Pass looks disabled | `UIStyle.StyleButton` on `PassButton`, `ContinueButton`, `StartButton`, ballots | **change** (2.13); Action! **confirm only** (T64) |
| C2 | Director's note heading gold on mustard, 2.7:1 | `NoteFrame` → `StylePanel "Note"`, `NoteTitle` / `NoteText` / `NoteHidden` in `PaperText` | **change** (2.14) |
| C3 | "You" means two things; card headline is "Player 1" | Card: `YouAre`, `MeText`, `RoleText`; vote reasons (T60) | **change** (card, 2.15); the reasons are **confirm only** (T60 `cbd50fa`) |
| C4 | No roster of who is still in | New `RosterRow` in the card | **change** (2.16) |
| C5 | Header says "click the actor", only the buttons take it | `ComputePrompt` vote literal | **change** (2.17), with row 4's literals |
| C6 | The tally is a wrapping gold sentence | `Tally`'s banner text, or a chip row | **decide in T34** (2.18) |
| C7 | Weak hover; no focused state | `UIStyle.UIColor` `.Hover` roles; `ShowRing` | the ring is **change** (1b); the hover is **decide in T34** (2.19) |

Rows that are not T34's: 8, 9, 10, 16 and C8 (T33, fixed in `d8f4325`), 18 (T61). Nothing to do.

---

## Part 1: the three known bugs (do these first)

### 1a. Row 1: the fourth vote button votes for the third name

**What we know.** T09 built three buttons that each send `OnSend("#vote <i>")`, and `HandleSend` sends a line that starts with `#vote ` to `PickVote(Index)`. T26 added the fourth button (`VoteBtn3`, `VoteLbl3`) for a cast of five. T28 read `HandleSend` and found checks for `#vote 0` and `#vote 1` and a fallback of 2, with no `#vote 2` or `#vote 3` check. T32 then clicked Meta (the fourth name), the header said "You picked SpaceXAI" (the third), and the log showed `Player 1 | votes for Player 5`.

**Likely cause:** `HandleSend`'s `#vote` branch is an if-chain written for three buttons: "is it `#vote 0`? then 0; is it `#vote 1`? then 1; else 2". T26 added the button but not a branch, so `#vote 3` falls through to 2. A second, smaller chance: `VoteBtn3`'s `OnClicked` chain was copied from `VoteBtn2`'s and still sends `#vote 2`. Either way the fix belongs in `HandleSend`, so it can't happen again for any count.

**Read in the editor (three things):**
1. `BP_Show.HandleSend`: `find_nodes` for `EqualExactly` (or `StartsWith`) nodes whose literal is `#vote`, and trace from the entry which branch feeds `PickVote`'s `Index` pin. Record the node names and the literals (`#vote 0`, `#vote 1`) and where the fallback 2 comes from (a literal on a `Select` or a third `PickVote` call).
2. `WBP_Stage`'s `EventGraph`: the four `OnClicked(VoteBtnN)` chains and the literal each sends (expected `#vote 0` to `#vote 3`).
3. `BP_Show.PickVote` and `ShowVotePick`: that `Index` indexes `PickSeats`, and that `SetVoteOptions` fills `VoteLbl<i>` from the same `PickSeats[i]` order.

**Fix (node edit in `HandleSend`, no file):** replace the if-chain with a parse, so every index maps to itself:

```lisp
; HandleSend, the #vote branch (T34 row 1): every button's index, not three cases and a fallback.
(bind _idx (Utilities|String|Conv_StringToInt (Utilities|String|RightChop Line 6)))
(CallFunction|PickVote :Index _idx)
```

`RightChop(Line, 6)` drops `#vote ` (6 characters). The two node names are guesses in the DSL's form: check them with `find_node_types` ("RightChop", "String to Int") before a write; as this is a node edit, `create_node` and `connect_pins` work as well. Keep the branch's input the same pin that feeds the old `EqualExactly` nodes (the function's `Line` input, if read 1 shows that). Wire `_idx` into the existing `PickVote` call and delete the `EqualExactly` nodes and the fallback. `PickVote` should already refuse an index outside `PickSeats` (T09: "(No vote to cast right now.)" was its old message); if it doesn't, add `(if (or (< _idx 0) (>= _idx (len (V PickSeats)))) (return))` before the call. If read 2 shows `VoteBtn3` sends `#vote 2`, change its literal to `#vote 3` too.

**Check:** in one PIE vote, click (or, on the Mac, focus with T33-1 and press Enter on) each of the four tickets in turn, and read the header ("You picked X") and the `VOTE` / `NHOS: LOG ... votes for` line after a reason. Then repeat with a 4-actor show (`ai_seats` 3) so only three tickets show. Screenshot `vote_pick4_p16.png`.

### 1b. T33-1: the in-show buttons can't take keyboard focus

**Why it matters twice:** a judge can't play the show by keyboard, and on the Mac an agent can't play a show by hand at all (Slate inspector clicks miss; only `PressKey` and `Type` to the focused widget work, T33). So this also unblocks T34's own "Claude plays one show by hand".

**The tension:** T64 keeps every builder button and chip unfocusable on purpose, and T65's `HoldFocus` (⟳ re-check after T65) pulls the focus back into the speech field every frame while `CanType` is true. So focusable buttons must only ask for focus while my input is closed. That is already true for the three that matter:

| Button | When it shows | Input open? | Keyboard plan |
|---|---|---|---|
| `StartButton` (Start the scene) | Scene Prep | No (T28: the box stays disabled in prep) | Focusable, takes focus in `SetPrepMode(true)` |
| `VoteBtn0`–`VoteBtn3` (the ballot) | The Cut, before and after a pick | No until a pick (T27's `4_vote.png`: "Click a name above first.", box disabled); confirm in `ComputePrompt` | Focusable; `VoteBtn0` takes focus when the row shows; Tab and Shift+Tab move, Enter picks; after the pick `HoldFocus` moves the focus to the field for the reason |
| `ContinueButton` (See the results) | After the last reactions | No | Focusable, takes focus in `SetContinue(true)` |
| `SendButton` (Action!) | My turns | Yes | Stays unfocusable: Enter in the field already does what it does (`SubmitInput`) |
| `PassButton` | Free Talk, last word, reactions (T66 hides it in scene turns ⟳) | Yes | Stays unfocusable; **Enter on an empty field sends "pass" while Pass is enabled** (below) |

**Changes:**

1. **Designer:** set `IsFocusable` true on `StartButton`, `VoteBtn0`–`VoteBtn3` and `ContinueButton` (`ObjectTools` property `IsFocusable`). Wrap each in a `Border` named `StartRing`, `VoteRing0`–`VoteRing3`, `ContinueRing` (padding 0, as T33's rings are; `UISize "S1"` of gap is in the brush radius), visibility `SelfHitTestInvisible`.
2. **`Graphs/WBP_Stage/ShowRing.txt` (new, the same as T33's):**

```lisp
; WBP_Stage.ShowRing(Ring, On): the gold focus ring (UIStyle FocusRing) on the Border that wraps an in-show button (T34, T33-1).
; RingTick calls it each frame for each focusable button. A ButtonStyle has no focused brush (T32, C7).
(fn ShowRing (Ring On)
  (bind w (Class|UIStyle|UISize :Role "FocusRing"))
  (bind r (Class|UIStyle|UISize :Role "ButtonRadius"))
  (bind gap (Class|UIStyle|UISize :Role "S1"))
  (bind gold (Class|UIStyle|UIColor :Role "Gold"))
  (bind clear (Utilities|Struct|MakeLinearColor 0.0 0.0 0.0 0.0))
  (Class|Border|SetBrushColor :self Ring :BrushColor (Utilities|Struct|MakeLinearColor 1.0 1.0 1.0 1.0))
  (bind b (Class|UIStyle|Brush :Fill clear :Outline (select On gold clear) :Width w :Radius (+ r gap)))
  (Appearance|SetBrush :self Ring :InBrush b))
```

3. **`Graphs/WBP_Stage/RingTick.txt` (new):** the ring follows the focus. It touches a ring only when its state changes (`RingOn`, a new Boolean array of 6, false), as `SyncAction` does, so a frame costs six `HasKeyboardFocus` calls and no brush writes.

```lisp
; T34 (T33-1): the gold ring shows on whichever in-show button has the keyboard focus. SetPrompt calls this every frame.
(fn RingTick ()
  (bind _btns (Utilities|Array|MakeArray (Variables|WBP_Stage|GetStartButton) (Variables|WBP_Stage|GetVoteBtn0) (Variables|WBP_Stage|GetVoteBtn1) (Variables|WBP_Stage|GetVoteBtn2) (Variables|WBP_Stage|GetVoteBtn3) (Variables|WBP_Stage|GetContinueButton)))
  (bind _rings (Utilities|Array|MakeArray (Variables|WBP_Stage|GetStartRing) (Variables|WBP_Stage|GetVoteRing0) (Variables|WBP_Stage|GetVoteRing1) (Variables|WBP_Stage|GetVoteRing2) (Variables|WBP_Stage|GetVoteRing3) (Variables|WBP_Stage|GetContinueRing)))
  (for _i (range 6)
    (bind _on (Widget|HasKeyboardFocus :self (get _btns _i)))
    (if (xor _on (get (V RingOn) _i))
      (Utilities|Array|SetArrayElem (V RingOn) _i _on)
      (CallFunction|ShowRing :Ring (get _rings _i) :On _on))))
```

   If `MakeArray` of two widget types won't take in the DSL, make `RingBtns` and `RingBorders` widget-array variables filled once in `StyleStage` (2.5) and loop over them. Call `ShowRing(…, false)` on all six once in `StyleStage`, so they start clear.
4. **`SetPrompt`** (rewrite from its file): add `(CallFunction|RingTick)` after `(CallFunction|FitBuilder)`. ⟳ re-check after T65 and T66: both rewrite `SetPrompt` (T65 adds `HoldFocus` at the end, T66 `TickTimer`); add the line to whatever the file holds then.
5. **Focus when a button appears** (only while my input is closed, so it never fights `HoldFocus`):
   - `SetPrepMode` (rewrite from its file), inside `(if Prep ...)` after the `StartButton` line: `(Widget|SetKeyboardFocus :self (Variables|WBP_Stage|GetStartButton))`.
   - `SetVoteOptions` (no file; read first): after the row shows with at least one name, `(if (not (Variables|Default|GetLastCanType)) (Widget|SetKeyboardFocus :self (Variables|WBP_Stage|GetVoteBtn0)))`.
   - `SetContinue` (no file; read first): on show, `(Widget|SetKeyboardFocus :self (Variables|WBP_Stage|GetContinueButton))`.
6. **Pass by keyboard** (`SubmitInput`, rewrite from its file). An empty Enter while Pass is enabled sends "pass", exactly as T66's `TimeUp` does with an empty field (T66-build decision 3), so the keyboard and the timer agree:

```lisp
  ; T34 (T33-1): Enter on an empty field passes while Pass is enabled (Free Talk, a last word, a reaction), as the Pass
  ; button and T66's TimeUp do; with the builder up (a scene turn) an empty line is No action, as before.
  (if (and (Utilities|String|IsEmpty _text) (not _bon) (Variables|Default|GetPassOn) (Variables|Default|GetLastCanType))
    (print "NHOS: TYPED pass")
    (Default|CallOnSend self "pass")
    (return))
```

   Insert it right after `_text` is bound, before the `(if (or (not (Utilities|String|IsEmpty _text)) _bon) ...)` line. Confirm in the `OnClicked(PassButton)` chain (read 2 of 1a's list) that Pass sends the text `pass` through `OnSend`; T66-build expects the same. ⟳ re-check after T66 (its `TimeUp` and `ShapeRow` touch `SubmitInput` and Pass). The hint must say so: see 2.8.

**Check (keyboard only, on the Mac through `PressKey` and `Type`):** title → Test for Free → Scene Prep (Start the scene has the ring; Enter starts) → a scene turn (type, Enter sends) → Free Talk (Enter on empty passes; `NHOS: TYPED pass`) → the vote (ring on the first ticket; Tab to the fourth; Enter; type a reason; Enter) → reactions → See the results (ring; Enter) → end screen. Screenshots `focus_start_p16.png`, `focus_vote_p16.png`, `focus_continue_p16.png`.

### 1c. T33-2: the robots' name tags show through full-screen panels

**Cause:** each robot's tag is `BP_Robot`'s `Label`, a world-space `TextRenderComponent` (`ResetLook`, `SetPassed`, `SetCut` set its text and color; `InitHome` makes its rotation absolute). It is part of the 3D scene, not of `WBP_Stage`, so the title and end screens, which hide the stage UI by setting `WBP_Stage`'s render opacity to 0 (`WBP_EndScreen`'s `EventConstruct`), don't hide it; bright white text then shows through the 92% ink.

**Fix, with row 2:** once row 2 draws the tags in `WBP_Stage` (2.1), the TextRender labels are never shown again, and the new tags vanish with `WBP_Stage`'s opacity like every other stage widget. Hide the 3D labels from `WBP_Stage`, without editing `BP_Robot` (held by the PC; not in Touches):

```lisp
; T34 (T33-2, row 2): the robots' 3D labels stay hidden; WBP_Stage draws the tags in screen space instead (TagTick).
; Called once from StyleStage. BP_Robot sets the label's text and color but never its visibility, so the hide holds.
(fn HideRobotLabels ()
  (bind _show (Actor|GetActorOfClass :ActorClass "/Game/NHOS/Core/BP_Show.BP_Show_C"))
  (for _rb (Class|BPShow|GetRobots :self _show)
    (Utilities|IsValid _rb
      (:"Is Valid"
        (Rendering|SetVisibility :self (Class|BPRobot|GetLabel :self _rb) :bNewVisibility false :bPropagateToChildren false))
      (:"Is Not Valid"))))
```

It walks `BP_Show`'s `Robots` array (typed, so no cast; `MarkPass` walks it the same way) and reads another Blueprint's variable as `BP_Robot.WatchShow` reads `BP_Show`'s (`Class|BPShow|GetSceneNum :self ...`). Read first: that `Label` is reachable as `Class|BPRobot|GetLabel` (component variables are public by default), and that `Robots` is filled before `WBP_Stage`'s construct; if not, call `HideRobotLabels` from `SetPrepMode(true)` too (it is cheap and idempotent). **If row 2 is cut for time,** the smallest fix for T33-2 alone is the same loop with `bNewVisibility` = (stage opacity > 0), called from `SetPrompt` each frame and touching the labels only when that changes; that leaves the 3D tags in play and hides them under the title and end screens.

**Check:** `title_p12.png`, `end_lose_p16.png` and `end_win_p16.png` show no tag through the ink (T33's `after_title_p12.png` and `after_end_lose_p16.png` are the "before").

---

## Part 2: every other T34 row

### 2.1 Row 2: the robots' name tags, in screen space ⟳ re-check after T38

T38 puts a speech bubble over each robot, 14 cm above the label (T38 part 1), and either as a screen-space `WidgetComponent` on `BP_Robot` or in a `BubbleLayer` in `WBP_Stage` (T38-build "Layer mode"). Read which one T38 used; the tags go in the same space so the bubble's tail can keep clear of them (T38's `SetKeepOut` takes rects).

- **Tree:** a `TagLayer` (CanvasPanel, fills `RootBox`, `HitTestInvisible`) after `HeaderSize`, `LowerSize` and `InfoSize` and before `BubbleLayer` (if any) and `StageArea`, so the panels never cover a tag's text badly and the stamp and banner draw over them. Five tags, `Tag0`–`Tag4`, each a `Border` (pill) with a `TextBlock`, in canvas slots with alignment (0.5, 1).
- **Look (all from `UIStyle`):** fill `SeatColor(Name, Fallback)`, outline 2 px `InkSolid` (`UISize "InputOutline"`), radius `TagRadius` 10, padding `S2` × `S1`; text `UIFont "Name"` (20 bold) in `PaperText`. Ink text passes on every seat color (computed: OpenAI 11.1:1, Anthropic 7.1:1, SpaceXAI 14.4:1, Meta 5.8:1, You 9.7:1); white fails on all five (1.3 to 3.2:1), so never white. "You" carries the word, not only teal (WCAG 1.4.1). Passed (T57): the tag gets a quiet line "(passed)" above it in `Quiet` on a small `Ink` plate, as `SetPassed` does today. Cut: the tag hides (T32 row 2), since C4's roster shows who is out.
- **`TagTick`** (new, called from `SetPrompt` each frame): for each robot, project its label's world location (the `Label` component's, so T47's hats still lift it) with `ProjectWorldLocationtoWidgetPosition` into `RootBox` space, set the slot position, clamp inside the 24 px edge (`UISize "Edge"`), and when two tags overlap, push the later one up by its height plus `S1` (stacked when close). Text: the robot's `DisplayName`; passed from the label's own text starting with "(passed)" (if `TextRender`'s text isn't readable from Blueprint, keep a `PassedSeats` array in `WBP_Stage` fed by a new `BP_Show.MarkPass` call; a `BP_Show` node edit); cut from `BP_Robot`'s `IsCut`. Write the text only when it changes.
- **Scene 1's "ROBOT" in Scene Prep** (`p12_prep.png`): the tags read `DisplayName`, so read where `ScenePrep` sets it. If the names are set only at `StartFromPrep`, set them in `ScenePrep` (T32's fix). Read first.

Screenshots: every phase, both sizes; the worst cases are robots standing close (Free Talk) and a thrown prop between the camera and a robot (T35's `m1.png`).

### 2.2 Row 3: the ballot

- `SetVoteOptions` (no file; read first) and `SetVotePick` (no file): each `VoteBtn<i>` goes through `UIStyle.StyleButton(VoteBtn<i>, VoteLbl<i>, "Paper")` (cream, ink text 13.5:1), with a 6 px seat bar (`UISize "SeatBar"`, `SeatColor(name)`) at its left: a new `Border` `VoteBar<i>` in the button's content before `VoteLbl<i>`.
- The pick: a red **HUMAN?** stamp on the picked ticket (`Red` fill, white `UIFont "Button"`, 5.7:1), a new `VoteStamp<i>` TextBlock in an Overlay over the label, rotated −8° like the reveal stamp. The other tickets stay at full contrast, since I can still change my pick (cold review).
- Keyboard: T33-1's rings (1b) sit around the tickets.
- Without color: the stamp is a word and a shape; the seat bar is backed by the name. Check `vote_after_p16_gray.png` and `_deut.png`.

### 2.3 Row 4: the header says one thing, from one state

- **`SetPhase`** (rewrite from its file) gets the header's look: `UIFont "Header"` (32), `Text` color, set once in `StyleStage`, not per call. The header's text is the phase in display type ("FREE TALK", "THE CUT"); the scene and turn move to pips.
- **Drop the scene from the header** (T53: "T34 can drop it", since the clapperboard shows "SCENE 2 / 4"). The header text comes from `BP_Show`'s `CueHeader` callers, which have no files (`StartTurn`, `StartTalkRound`, `StartCut`, `StartReactions`, `EndShow`, and `StartLastWords` for "LAST WORD: SCENE n"). Rather than edit six callers, `SetPhase` can cut the text at its first ":" (`Utilities|String|Split` on ":" and keep the left part; "THE SCENE: SCENE 2, TURN 1 OF 3" → "THE SCENE"), and show the turn as pips from the right part. **Decide in T34**: the cut in `SetPhase` keeps `BP_Show` untouched (recommended); confirm every header text has the form "PHASE: detail" first (`find_nodes` for `CueHeader` calls).
- **Turn pips:** a new `TurnPips` HorizontalBox under `PhaseHeader` with three small `Border` dots (`S3` square, radius `S2`): done in `Gold`, now in `Gold` with a `Text` outline, to come in `Raised` with a `Quiet` outline (10.7:1 on ink). Fed from the header's "TURN n OF m"; collapsed outside scene turns.
- **The turn line (`TurnText`)** says only what to do now. It comes from `ComputePrompt` (no file), `LinePrompt`, `PrepPrompt` and `LastWordPrompt` (files). `ComputePrompt`'s scene literal today is `"Turn n" + " of 3. YOUR MOVE: pick an action, say a line if you like, then press Action!"` (T64 changed it; node `K2Node_CommutativeAssociativeBinaryOperator_4`'s `B`). **Decide in T34**, because the plan's Touches allow `BP_Show` only for a widget's call: changing the literals is the clean fix (recommended; T64 did the same), so ask my person or note it as covered by "the widget's call". New text: "YOUR MOVE: pick an action, then press Action!" (the pips carry the turn).
- **The disagreement in T29's shots** ("THE CUT" over "Free Talk. Your line is on its way..."): since T30 the header is a cue and the turn line follows the queue (`LinePrompt`), so they should now agree. **Confirm only**: watch the phase changes in the screenshots.
- **Fixed width:** `HeaderSize` gets a fixed `WidthOverride` (720 at 1080p, so the longest line, "YOUR MOVE: pick an action, then press Action!", fits in two lines at 20) instead of "max 860" (T27). ⟳ re-check after T38 (T38's bubbles measure the header rect live; T38.md "Layout to watch" asks for a shorter header).

### 2.4 Row 5: my move stands out

- **`SetPrompt`** (rewrite from its file): the turn line's two literal colors become `UIStyle` colors. Today: `(select CanType (MakeLinearColor 1.0 0.85 0.45 1.0) (MakeLinearColor 0.8 0.83 0.9 1.0))`. New, bound before the `if`:

```lisp
  (bind cGold (Class|UIStyle|UIColor :Role "Gold"))
  (bind cQuiet (Class|UIStyle|UIColor :Role "Quiet"))
  ...
    (Class|Text|SetColorandOpacity :ColorAndOpacity (Utilities|Struct|MakeSlateColor (select CanType cGold cQuiet)) :self (Variables|WBP_Stage|GetTurnText))
```

   Bind them inside the `(if (xor CanType ...))` block, so they run only when `CanType` changes, not every frame. Gold on ink 10.9:1; Quiet on ink 10.7:1. The turn line starts "YOUR MOVE" when it's mine (2.3's literal).
- **A gold focus ring on the input:** `InputBox`'s style (T27: teal outline when focused, gray otherwise). Set its focused outline to `Gold` and its normal outline to `Quiet`, 2 px (`UISize "InputOutline"`): measured on T27's `4_vote.png`, today's gray outline is **1.5:1** against the panel, under 3:1 (WCAG 1.4.11). The box's fill is `Inset` (1.1:1 against ink), so the outline carries the edge. This is a designer style (`WidgetStyle`), or set in `StyleStage` with `SetWidgetStyle` if MCP can't reach the brush; read first. ⟳ re-check after T65 (the counter pill sits beside the box).
- **Action! Primary on my move:** done by T64 (`SetPrepMode` styles `SendButton` Primary). **Confirm only.** Secondary off my move: Action! is disabled off my move (`SetPrompt`), and disabled is 40% Primary, which reads as "not now"; leave it.
- **Pass hidden when it can't be used:** T66 hides it in scene turns (decision 6). **Confirm only, ⟳ re-check after T66.**

### 2.5 Row 6: the panels (`StyleStage`, new)

A new `Graphs/WBP_Stage/StyleStage.txt`, called once from `EventConstruct` (add the event if `WBP_Stage` has none; read first) and from `EventPreConstruct` with `IsDesignTime` so the designer shows the look:

```lisp
; T34: the stage's look, all from UIStyle (row 6, row 7). Ink on the running talk, paper on what is mine, the gold note.
(fn StyleStage ()
  (Class|UIStyle|StylePanel :Panel (Variables|WBP_Stage|GetHeaderBar) :Look "Ink")
  (Class|UIStyle|StylePanel :Panel (Variables|WBP_Stage|GetLowerPanel) :Look "Ink")
  (Class|UIStyle|StylePanel :Panel (Variables|WBP_Stage|GetInfoPanel) :Look "Paper")
  (Class|UIStyle|StylePanel :Panel (Variables|WBP_Stage|GetNoteFrame) :Look "Note")
  (Widget|SetRenderOpacity :self (Variables|WBP_Stage|GetHeaderBar) :InOpacity 1.0)
  (Widget|SetRenderOpacity :self (Variables|WBP_Stage|GetLowerPanel) :InOpacity 1.0)
  (Widget|SetRenderOpacity :self (Variables|WBP_Stage|GetInfoPanel) :InOpacity 1.0)
  ; fonts (row 7), rings (T33-1), robot labels (T33-2) follow
  )
```

- `HeaderBar` and `LowerPanel` are T27's names; the card's Border inside `InfoSize` has no name in the Findings: read it, make it a variable, and use its real name for `InfoPanel`. Each must be a `Border` (`StylePanel` sets a brush). If one is another panel type, wrap it in a Border.
- The 78% / 75% / 82% opacities (T27) go to 1.0: the 92% now comes from `Ink`'s alpha, and `Paper` is opaque (my card).
- On paper, the card's text changes from white to `PaperText` (13.5:1) and `PaperQuiet` (5.4:1) for small labels. Every TextBlock on the card: `YouAre`, `MeText`, `RoleText`, `WantText`, `SceneTitle`, `SceneText`, `CastTitle`, `SetTitle`, `PlacesText`, `PropsText`.
- "Collapse the chat while it is empty": ⟳ re-check after T38, which hides the chat at each show's start behind Show chat; if T38 is in, skip this.

### 2.6 Row 7: the type scale

In `StyleStage`, every text gets its role (bind each `UIFont` once):

| Widget | Role | Size |
|---|---|---|
| `PhaseHeader` | `Header` | 32 (today 28) |
| `TurnText` | `Body` | 20 |
| `HintLabel` | `Hint` | 18 (keep T27's 5.1:1 gray, or `Quiet` for 10.7:1 on `Inset`) |
| `BannerText` | `Banner` | 48 (today 30) |
| `StampText` | `Stamp` | 120 (today 64; 2.12) |
| `TypingText` | `Action` | 18, `Quiet` |
| Card titles (`YouAre`, `NoteTitle`, `CastTitle`, `SetTitle`, `SceneTitle`) | `CardTitle` | 24 (today 18, like the body) |
| Card body (`RoleText`, `WantText`, `SceneText`, `PlacesText`, `PropsText`, `NoteText`, `NoteHidden`) | `Body` | 20 |
| `ClapText` | `Header` | already (T53's `StyleClapper`) |

- `NextBanner` (rewrite from its file): the hold `:Time 3.5` becomes `UITime "Banner"` (4), bound first: `(bind tBanner (Class|UIStyle|UITime :Role "Banner"))` and `:Time tBanner`. T37 asked T34 to lengthen it for long lines: hold `max(UITime "Banner", 1.5 + words / 3.5)` seconds (the reading rate T30's pacing uses; confirm in `pacing.json`), so a 20-word error note holds about 7 s. **Decide in T34** whether the extra time is worth the slower show; recommended yes for banners over 12 words only.
- The decoy line (16 pt): removed by T51 (`6ada2ab`). **Confirm only.**
- The builder's `MonoFont` (Droid Sans Mono 18) stays on the builder (T64 Part 1); a `"Mono"` role in `UIFont` is optional. ⟳ T65 and T66 read the same `MonoFont` through `WBP_Stage.Mono()`; if T34 adds the role, change `Mono()` only.

### 2.7 Row 11: the chat's cut top line ⟳ re-check after T38

A stepped fade with no new asset: an Overlay over `ChatSize`'s top with three 8 px `Border`s (`HitTestInvisible`) filled `InkSolid` at alpha 0.9, 0.6 and 0.3 from the top down. A smooth gradient needs a material (a new asset): not worth it. If T38's chat stays hidden most of the time, still do it: the chat shows on a click.

### 2.8 Row 12: hints that fit

The doc asks for hints of about 30 characters; the example goes in a chip, not the header. Literals today:
- Scene turn: "Say something (optional)..." (T64). **Confirm only.** ⟳ re-check after T65 (the @ list and counter).
- Last word: `LastWordPrompt.txt`'s hint "Answer who named you, like: @Meta, I only grabbed the rose for the story." (74 characters) → "Answer who named you." Edit the file's `(set PHint ...)` line and write it; its turn line "Last word. You were named. One last line before the vote, or press Pass." becomes "LAST WORD: answer, or press Enter to pass." (T33-1's Enter).
- Free Talk, the vote, reactions: `ComputePrompt` (no file; read the `SetPHint` literals). Targets: Free Talk "Say a line, or Enter to pass."; the vote before a pick "Pick a name below." (C5); after "Why them? (one line)"; reactions "One line, or Enter to pass." These are `BP_Show` literals: see 2.3's "decide in T34".
- `HintLabel` keeps its ellipsis as a safety net, but no hint should reach it at 1280 × 720 (check `*_p12.png`).

### 2.9 Row 13: Scene Prep — decide in T34

**Why decide:** the row asks for the doc's call sheet in the center during prep, ranked. That moves `PrepBox` out of the card into a new centered panel, a layout change T28 and T50 didn't plan for, and T61's stagehand (its earpiece in Scene Prep) may want the same space. **Recommended:** keep the card on the right but rank it so nothing scrolls at 1600 × 900: my role as the headline (`CardTitle` 24), then the note box (C2), then the scene title and text in `Body`, then cast and stage in `Caption` (18) on one line each ("Cast: OpenAI, Meta, …"; "Places: …"; "Props: …"). Check `prep_p16.png` and `prep_p12.png` with the longest card (`p16_prep2_long.png`'s scene). Center it only if the ranked card still scrolls at 1280 × 720. ⟳ T61's earpiece: read `WBP_Earpiece`'s place (T61 Part 1) so the card doesn't sit under it.

### 2.10 Row 14: seat colors

- The card's cast bars: filled where `CastBox` is built (`SetStageInfo` or `ShowPrep`; no file; read first) from `BP_Show.SeatColors` (`StagePrep.txt` sets them). Change that one color pin to `UIStyle.SeatColor(Name, <the old color>)`, as `WBP_ChatLine.SetActor` and `WBP_EndCard.Setup` do. If C4's roster (2.16) replaces the cast list after prep, do it there too.
- The robots' bodies: `BP_Robot.SetPersona` sets `BaseColor` to the doc's colors (OpenAI `#A8CCFF`, Anthropic `#E8894A`, SpaceXAI `#D8F04A`, Meta `#5B8CFF`, me `#3FD0C9` as linear values; checked against `UIStyle.SeatColor`, they match). **Confirm only.**

### 2.11 Row 15: the tie's banners — confirm only

T52 (`d2d4cdc`) made a tie cut nobody with one banner ("The vote is tied, so nobody is cut. The scene still counts.") after the tally banner, and T55 (`9d76733`) removed the Director's line. So a tie now shows two banners (the tally, then the tie), not four. Check one `force_tie` show: two `NHOS: BANNER` lines per tie, about 8 s.

### 2.12 Row 17: the reveal stamp

- `StampText` (in `StageArea`, T09; `SetStamp(Stamp)`, no file). Look: `UIFont "Stamp"` (120, bold, 2 px ink outline), render angle −8°, a double outline: wrap it in two `Border`s (outer `Brush(clear, color, ButtonOutline 3, PanelRadius)`, inner the same 6 px in), then the fill: **ink text on `Amber`** for an AI (8.4:1) and **white on `Red`** for the human (5.7:1). The cold review measured today's white on amber at about 1.8:1.
- Slam in: scale from 1.4 to 1.0 and opacity 0 to 1 over `UITime "StampIn"` (0.2 s), hold `StampHold` (3.5), fade `StampFade` (1). A UMG animation in `WBP_Stage` is simplest; a timer like `FadeBanner` works too.
- Words: today `CutActor` passes "META: AI" or "YOU: HUMAN" (T26). Rewrite in `SetStamp`, not in `CutActor`, so `GameMsgs` ("Reveal: ...") and `NHOS: CUT` keep their form: ": AI" → " IS AN AI", "YOU: HUMAN" → "YOU ARE THE HUMAN", any other ": HUMAN" → " IS THE HUMAN" (the last can't happen, but costs nothing). Pick the fill from the word HUMAN.
- `BP_Robot.SetCut(Stamp)` also writes the stamp into the robot's 3D label in red (1.0, 0.12, 0.08); with 2.1 the 3D label is hidden, and the cut tag hides. Nothing to change in `BP_Robot`.
- T27's rule: no robot, label or prop sits behind the stamp; check `stamp_p16.png` and `stamp_p12.png`. A free autoplay show is too fast to catch the stamp (T32): play the vote by hand.

### 2.13 C1: button labels

Every in-show button through `UIStyle.StyleButton`, in `StyleStage`: `StartButton` Primary (gold, ink 10.2:1 measured on T33's screens), `PassButton` Secondary (plum, white 14.0:1), `ContinueButton` Primary, the ballots Paper (2.2). Action! is already Primary (T64). Disabled is 40% with no outline, so an enabled Pass (white on `Raised`, quiet outline) and a disabled one now look different. ⟳ re-check after T38 (its Show chat button, Secondary) and T78 (the face chip).

### 2.14 C2: the director's note

`NoteFrame` → `StylePanel "Note"` (gold fill, old-gold trim), and `NoteTitle`, `NoteText`, `NoteHidden` in `PaperText` (ink on gold, 9.7:1). Today's gold on mustard measures **4.2:1** on T27's `4_vote.png` (the cold review guessed 2.7:1; either way under 4.5). T50's blacked-out bar in `NoteHidden` stays.

### 2.15 C3: "you" on my card

The card's headline is my role, not "Player 1": `RoleText` in `CardTitle` 24 first; `YouAre` + `MeText` become one small `Caption` line, "The cast knows you as Player 1", in `PaperQuiet`. The text comes from `SetInfoTop` (no file; read first, and T50's `Note` pin). The vote reasons in the third person were T60's (`cbd50fa`): **confirm only** on the end screen.

### 2.16 C4: a roster of who is still in

A `RosterRow` (HorizontalBox) on my card under the role: one chip per seat on stage at the show's start, each `Border` in `SeatColor` with the screen name in `PaperText` `Caption`, a cut one at 40% opacity with its name struck through (a 2 px `PaperText` `Border` across the middle; UMG has no strike style). Fill it in `ScenePrep` (no file; read where `SetStageInfo` gets the cast) and refresh at each `CutActor`. Without color, the names carry it.

### 2.17 C5: "Pick a name below"

`ComputePrompt`'s vote turn line "... click the actor you think is the human" (T27's `4_vote.png`) → "THE CUT: pick a name below, then say why." Same "decide in T34" as 2.3's literals. Making the robots clickable is out of scope.

### 2.18 C6: the tally — decide in T34

**Why decide:** the tally is a banner sentence built in `Tally` (no file) and queued as a cue (T30). A chip row needs new widgets fed from `VoteCount`. **Recommended:** keep it a banner, but write it so it never breaks inside a name: "Votes — You 1 · SpaceXAI 1 · Meta 2" in `Banner` type with the names joined by " · " and each "Name n" joined by a non-breaking space (U+00A0) in `Tally`'s join. That is one node edit in `Tally`, no new widget. The chips are the fuller fix if time allows.

### 2.19 C7: hover and focus

The focus ring is 1b. Hover: T32 left `.Hover` at 15% toward white. **Decide in T34** after the screenshots of a hovered Primary and Paper button (`hover_primary_p16.png`); if it reads weak, raise the mix to 25% in `UIColor`'s `Gold.Hover` and `Paper.Hover` (and the doc's States bullet, after my person's OK: the doc holds the value).

---

## Part 3: what T65, T66, T78 and T38 leave on the screen (read their Findings first)

| Task | Leaves | Touches T34's rows |
|---|---|---|
| T65 | `CountPill` with `WordCount` ("12/15", red at 15) between `InputStack` and `SendButton`; `AtPop` (the @ list) in `RootBox`; `HoldFocus` in `SetPrompt`; mention chips in the preview line (`WBP_Word`) | T33-1 (focus), 2.4 (input outline), 2.8 (hints) |
| T66 | `TimerText` ("0:21", mono, gold for the last 5 s) at the right end of the speech row; `ShapeRow` hides Pass in scene turns; `TimeUp` sends through `SubmitInput` / `OnSend` | T33-1 (`SubmitInput`, Pass), 2.4 (Pass hidden), C1 |
| T78 | `FaceBtn` "Face: Auto" first in `InputRow`, paper after a pick, its `FacePop`; the lower panel at 1000 on the whole play side | 2.5 (panel width), C1 |
| T38 | A `WBP_SpeechBubble` over each robot (14 cm above the label); the typing dots bubble; the chat hidden at each show's start with a Show chat / Hide chat button in the input row | 2.1 (tags and bubbles share the space), 2.5 (empty chat), 2.7, C1 |

The input row's final width (field, counter, Action!, Pass, timer, face chip, chat button) is T34's to settle with the rest of the screen: T65, T66 and T78 each ask for it. Look at the row at 1280 × 720 first; if the field is under about 250 units, drop the chat button's label to an icon-like "Chat" or move it to the header.

---

## Part 4: the order in the editor

Lock `WBP_Stage.uasset` (and `BP_Show.uasset` for 1a, 2.3's literals, 2.16) before the first write; keep each graph's source in `Graphs/` as you write it.

1. **Before anything:** read the graphs in "Read this first" that the bugs need (1a's three reads), take the "before" screenshots (Part 5), and run `python Tools/ui_shots.py` on them.
2. **Bugs:** 1a (the vote), then 1b (focus, rings, Enter to pass), then 1c (labels). Compile, PIE one vote by keyboard. Commit point.
3. **`StyleStage` and the panels** (2.5, 2.6, C1, C2): one function, the biggest visible change. Screenshot every phase.
4. **Phase by phase**, screenshot, critique, change, screenshot again (T34 step 3):
   - **Scene Prep:** 2.9 (the card), 2.15, 2.16 (roster), 2.10 (cast bars), 2.1 (tags read their names in prep).
   - **A scene turn, mine and the AIs':** 2.3 (header, pips), 2.4 (my move, input ring), 2.8 (hints), row 2 tags with props flying.
   - **Free Talk and the last word:** 2.7 (chat fade), the passed marker on the tags, Enter to pass.
   - **The vote:** 2.2 (ballot), 2.17, 2.18 (tally).
   - **A cut and its reactions:** 2.12 (stamp), the cut tag hidden, the roster updated, See the results focused.
   - **A tie:** 2.11 (two banners).
5. **Cold review** (T34 step 5): a subagent reads only the final screenshots.
6. **Without color** (step 6): `python Tools/ui_shots.py Saved/T34/shots/after_*.png --no-contrast`, then look at each `_gray` and `_deut`: who is speaking (chat seat bar plus name, the bubble's edge plus the tag), whose turn it is (gold turn line plus YOUR MOVE), which ballot is which (the name on each ticket).
7. **Measure contrast** from the 1600 × 900 screenshots with `--text` and `--edge` boxes (Part 6), and write the table under "## Findings" in `T34.md`.
8. **Autoplay show** in a game window (`NHOS: SHOW END`, no new `LogScript`, `NHOS: LOG` lines in the same form), then **one show played by hand** (on the Mac by keyboard, thanks to 1b).

## Part 5: the screenshots T34 must take

At 1600 × 900 (`_p16`) and 1280 × 720 (`_p12`), in `Saved/T34/shots/` (not in git), each as `before_<name>` and `after_<name>`, with `_gray` and `_deut` from the script:

| Name | Phase and state |
|---|---|
| `prep` | Scene 1's Scene Prep (tags read their names, not "ROBOT") |
| `prep2_long` | Scene 2's Scene Prep with the longest card, a cut robot lying on stage, the roster |
| `turn_ais` | A scene turn while the AIs' lines play (bubbles, tags, header pips) |
| `turn_mine` | My scene turn: builder, YOUR MOVE, input ring, counter, timer, face chip (⟳ T65, T66, T78) |
| `turn_mine_look` | My scene turn with Look picked (three chip rows; `FitBuilder` at its smallest chat) |
| `burn` | A scene turn with a burning bill (T35/T36) |
| `freetalk` | Free Talk, my line open, a passed tag on another robot |
| `lastword` | My last word |
| `vote_before` | The vote before a pick, first ticket focused |
| `vote_after` | After picking the fourth ticket (row 1's check) |
| `tally` | The tally banner |
| `stamp_ai`, `stamp_human` | The reveal stamp, each kind (play by hand: autoplay is too fast) |
| `tie` | The tie banner (`force_tie`) |
| `reactions` | A reaction after a cut, the cut robot's tag hidden |
| `continue` | See the results, focused |
| `title`, `end_win`, `end_lose` | No tag through the ink (T33-2) |
| `focus_start`, `focus_vote`, `focus_continue` | The gold ring on each (T33-1) |
| `hover_primary` | A hovered Primary button (C7) |
| `chat_open` | The chat opened with T38's button, with the top fade (⟳ T38) |

## Part 6: the screenshot checks (`Tools/ui_shots.py`)

`Tools/ui_shots.py` makes the two versions and measures contrast from the PNGs, with the standard library only (Python 3.10 or newer; `python3` on the Mac). Its docstring has the full usage.

```bash
python Tools/ui_shots.py Saved/T34/shots/after_vote_after_p16.png
python Tools/ui_shots.py Saved/T34/shots/*.png --no-contrast
python Tools/ui_shots.py Saved/T34/shots/after_vote_after_p16.png --no-variants --md --text ballot4=326,848,52,22 --edge input=26,912,40,912
python Tools/ui_shots.py --colors F2C14E 161225
```

- **Versions:** `<name>_gray.png` is each pixel's WCAG relative luminance, so a ratio measured on it equals the original's; `<name>_deut.png` is Machado 2009 deuteranopia at full strength, in linear sRGB (T33 used the same model). Files already ending in `_gray` or `_deut` are skipped.
- **Text** (`--text NAME=X,Y,W,H`, needs 4.5:1): the box's median color is the background, its 1st or 99th luminance percentile the text (T33's method). Draw the box tight around the text and its own fill.
- **Edges** (`--edge NAME=X0,Y0,X1,Y1`, needs 3:1): a short line from outside a button or border across its edge.
- **Coordinates** are pixels of the saved PNG, title bar included (a 1600 × 900 PIE window saves as 1600 × 968 on the Mac). `--md` prints rows for the Findings table. Exit code 1 when a box or edge fails.

**Tried on 2026-11-16** (Mac, Python 3.13.0). On `Docs/ItchMedia/cover.png`, the plain run wrote both versions and the rough figure in 1.5 s:

```
Docs/ItchMedia/cover.png  630x500
  wrote  <out>/cover_gray.png
  wrote  <out>/cover_deut.png
  image  whole image (rough)    #FDE192 on #5A2E18    8.9:1  info
```

On T33's `Saved/T33/shots/after_end_win_p16.png` (1600 × 968, about 3 s), the boxes match T33's own measured figures (10.2:1 ink on gold, 14.0:1 white on plum):

```
  text   playagain              #1C192A on #F2C04F   10.2:1  ok (needs 4.5:1)
  text   quit                   #FFFFFF on #2E2844   14.0:1  ok (needs 4.5:1)
  text   subtitle               #FFFFFF on #22212E   15.8:1  ok (needs 4.5:1)
  text   card_body              #2F2219 on #F5E8CE   12.7:1  ok (needs 4.5:1)
  text   card_quiet             #6B5B4B on #F5E8CE    5.4:1  ok (needs 4.5:1)
  edge   quit_border            #C8C2D9 on #1C1928   10.0:1  ok (needs 3:1)
  edge   card_border            #F5E8CE on #1A1726   14.5:1  ok (needs 3:1)
```

On T27's in-show `Saved/T27/shots/4_vote.png` (the pre-T32 look, so a "before" for T34), it finds the problems T32 listed (exit code 1):

```
  text   header                 #FBE69E on #33242B   11.8:1  ok (needs 4.5:1)
  text   vote_meta              #FFFFFF on #CB6F66    3.5:1  FAIL (needs 4.5:1)
  text   vote_spacexai          #FFFFFF on #CB6F66    3.5:1  FAIL (needs 4.5:1)
  text   note_heading           #FBE69E on #7D6A35    4.2:1  FAIL (needs 4.5:1)
  text   tag_spacexai           #D0CECC on #926A57    3.0:1  FAIL (needs 4.5:1)
  text   tag_you                #C6C5C4 on #805844    3.6:1  FAIL (needs 4.5:1)
  text   send_disabled          #AAABAF on #66656D    2.5:1  FAIL (needs 4.5:1)
  text   hint                   #8C8E96 on #212126    4.9:1  ok (needs 4.5:1)
  edge   vote_btn               #CB7066 on #242329    4.5:1  ok (needs 3:1)
  edge   input_box              #3F4049 on #232228    1.5:1  FAIL (needs 3:1)
```

(`send_disabled` is a disabled control, which WCAG exempts.) The same two boxes on the `_gray` version give the same 3.5:1 and 4.2:1. A JPEG saved as `.png` (several files under `Docs/BotArt/`) is refused with "it is a JPEG with a .png name" and the run goes on to the next file (exit code 2).

**`UIStyle` pairs, computed with `--colors`** (for the rows above): Gold on ink 10.9:1; Quiet on ink 10.7:1; ink on Paper 15.2:1; PaperText on Paper 13.5:1; PaperQuiet on Paper 5.4:1; PaperText on Gold 9.7:1; white on Red 5.7:1; ink on Amber 8.4:1; white on Raised 14.8:1; OldGold trim on ink 5.4:1 but on Paper only 2.8:1 (the paper fill carries a card's edge, 15:1 on ink); Raised on ink 1.2:1 and Inset on ink 1.1:1 (their outlines carry the edge); ink on every seat color 5.8 to 14.4:1, white on every seat color 1.3 to 3.2:1.
