# T38 build sheet: the speech bubbles and the hidden chat

Back to [T38](T38.md) and [the plan](../Plan.md). This is prep for T38. It was written without the editor on 2026-11-15 at commit `6902f97`, after T29 was pushed and before T30 and T32 were built. It is a plan, not a record: nothing here was written to the editor. The draft graphs live only in this file. When T38 writes a graph, its source goes to `Graphs/` as usual.

Sources read: `Graphs/BP_Robot/{EventGraph,Setup,SetLit,SetCut,SetPersona,InitHome,ResetLook,TickActs,StartAct,IsDown}.txt`, `Graphs/WBP_Stage/*.txt`, `Graphs/BP_Show/*.txt`, `Docs/tasks/T30-build.md` (the plan for `BPC_LinePlayer`), `Tools/dslpp.py`, the DSL rules in "T01: spike results", and the findings and Unreal MCP rules in T09, T17, T19, T27, T28 and T29.

## Read this first

### What the sheet assumes (check each one before you build)

| # | Assumption | How to check | If it is wrong |
|---|---|---|---|
| A1 | **T30 is built as its sheet says.** `BPC_LinePlayer` is a component on `BP_Show` (variable `LinePlayer`). It has a `Pump` with a typing branch that calls `WBP_Stage.SetTyping`, a cue branch that calls `BP_Show.RunCue`, a `PlayCur` that prints `NHOS: LINE <id> hold=<s>` and then calls `AddChatLine`, `LightSeat` and `StageLine`, and an optional `Clear`. Its variables include `Show` (BP_Show), `Stage` (WBP_Stage), `CurKind`, `CurSeat`, `CurColor`, `CurAction`, `CurSpeech`, `CurIsMe` and `CurTyping`. | Read `Graphs/BPC_LinePlayer/*.txt` and T30's Findings. | Put each T38 call at the same moment in T30's real graphs: the bubble call where the chat line appears, the typing bubble where the typing line shows, and the hush where a header, Scene Prep or end-screen cue runs. If T30 has no `LinePlayer` component but an `LP()` getter (its fallback A5), only the getter changes. |
| A2 | **T30's cue kinds are `phase`, `banner`, `stamp`, `votes`, `cut`, `prep` and `end`.** A header change, a Scene Prep and the end screen each come as one cue. | T30's `RunCue` source. | Hush the bubble on the kinds that mean "the phase changes" in T30's real list. |
| A3 | **`CurColor` (the type of `AddChatLine`'s `Color` pin) is `LinearColor`.** `BP_Show.StagePrep` fills `SeatColors` from `PersonaColor`. T30's E1 settles this. | `get_node_type_pins` on `Class\|BPRobot\|Say` after step 7, against `CurColor`'s type in T30's notes. | If it is `SlateColor`, give `Say`, `Typing`, `ShowLine` and `ShowTyping` a `SlateColor` input, and get the `LinearColor` for `SetBrushColor` with `Utilities\|Struct\|BreakSlateColor` (check its name with `find_node_types`). |
| A4 | **T32 made one style Blueprint** (its status file says `Content/NHOS/UI/BP_UIStyle` "or similar"). It holds the doc's palette, type scale, spacing, corner radius and motion times. It has a function that styles a `Button` for every state, which `WBP_ChatLine` and other widgets call. `WBP_ChatLine` gets its text looks from it too, including the action style. | T32's Findings, `Graphs/BP_UIStyle/` (or T32's name), and how `WBP_ChatLine` calls it. | Copy whatever call pattern `WBP_ChatLine` uses. This sheet writes `Class|BPUIStyle|<Fn>` as a placeholder everywhere. |
| A5 | **The style Blueprint has, or can get, every value in "Style values T38 needs" below.** | The same. | A missing value isn't T38's to add: the style Blueprint isn't in T38's Touches. Ask the person (`AskUserQuestion`) whether T38 may add it there (recommended: yes, so every value stays in one place). Until then, use the fallback value as a variable default in `WBP_SpeechBubble`, named `Fb<Value>`, and list it in Findings for T34. |
| A6 | **T29's widget names are in place:** `HeaderSize`, `InfoSize`, `LowerSize`, `LowerPanel`, `ChatSize`, `LogScroll`, `VoteRow`, `InputBox`, `InputStack`, `HintLabel`, `SendButton`, `PassButton`, `ContinueButton`, `StartButton`, `StageArea`, `StampText`, `BannerSize`, `EventBanner`. T30 put `LogScroll` and `TypingText` in a VerticalBox inside `ChatSize`. T32 didn't rename any of them. | Step 2 reads the tree. | Use the real names in `KeepOut` and `ShowChat`. |
| A7 | **Each robot's `PersonaId` is its seat id,** the same id `NHOS: LINE` prints. `StageSetup` calls `SetPersona` with each seat's id (T17). | Step 13's log: each `BUBBLE` id matches the `LINE` id before it. | Pass the id to `Say` from `CurId` instead. |
| A8 | **T34 and T20 haven't started.** T34 polishes the bubble after T38, and T20 adds the talk blip in `PlayCur`. | The plan. | If T20 is in, put the `Say` call after its blip; the order doesn't matter. |

### Questions only the editor can settle (read these first, in this order)

Steps 2 and 3 batch them. Each item is one `find_node_types`, `get_node_type_pins`, `read_graph_dsl` or property read.

- **E1 `BP_Robot`'s parts.** The `Label` TextRender's parent (the root or `Rig`), its relative location (T17: 228 cm), `WorldSize` and vertical alignment. The bubble's anchor goes on the same parent, at `BubbleZ` = the label's top plus about 6 cm. The sheet uses 262 until then. It must not go on `Rig`, or the bubble would bob with the robot.
- **E2 Do the five placed robots get a component added to `BP_Robot`?** T17 found that template edits don't reach instances placed before them; T19 found that new components show on instances placed after them. Check in PIE with `ActorTools.get_components` on a PIE robot after step 7. If `Bubble` is missing there, don't re-place the robots (that changes `L_Stage`, which T38's Touches don't list): use the `AddComponentbyClass` line in the `InitBubble` notes. Either way, `InitBubble` sets every property of the component at run time, so template values never matter.
- **E3 Node names to confirm with `find_node_types`** (with `context_pins: []`, T29), in the Blueprint that uses each:
  - in `WBP_SpeechBubble`: the widget's Tick and Construct events (`EventTick` with `MyGeometry` and `InDeltaTime`, `EventConstruct`); `Class|Border|SetBrushColor`; `Widget|SetRenderTranslation`; `Widget|GetDesiredSize`; `Widget|SlotAsCanvasSlot` and `Class|CanvasPanelSlot|SetPosition` (layer mode only); the geometry calls `LocalToAbsolute`, `AbsoluteToLocal`, `GetLocalSize` (written `Utilities|Geometry|...` here); `Math|Vector2D|MakeVector2D`; whether `(.x v)` reads a `Vector2D` field the way `(.yaw r)` reads a rotator in `InitHome`; `UserInterface|GetAllWidgetsOfClass`.
  - in `BP_Robot`: `UserInterface|CreateWidget` (as `BP_Show.ShowTitle` uses it), and the `WidgetComponent` calls `SetWidget`, `SetWidgetSpace` (its enum value for screen space, probably `"Screen"`), `SetDrawAtDesiredSize`, `SetPivot` (written `UserInterface|WidgetComponent|...` here).
  - in `BPC_LinePlayer`: **how to read `BP_Show`'s `Robots` array from the component.** Try `find_node_types` "Robots" with the `BP_Show` object as context. If there is no such getter, add `BP_Show.RobotAt(Seat)` (draft below) and lock `BP_Show`.
  - in `WBP_Stage`: `Widget|GetCachedGeometry`, `Widget|IsVisible`, `Class|ScrollBox|ScrollToEnd`, and the variable getters for the new widgets (T27: a new widget variable may not show in `find_node_types` after a compile, but `get_node_type_pins` finds it).
- **E4 How a screen-space `WidgetComponent` behaves here** (the probe in step 13; the mode choice hangs on it):
  - (a) the bubble shows over its robot at a constant size and follows a robot that moves or stands on the riser;
  - (b) the bubble widget gets `EventTick`, and its `MyGeometry` converts to `WBP_Stage`'s space with `LocalToAbsolute` then `AbsoluteToLocal` (print one rect and compare it with a screenshot);
  - (c) the bubbles draw under `WBP_Stage` (the screen layer's default `LayerZOrder` is -100, as far as I know), so the stamp and the banner always draw over a bubble. If they draw over it, the keep-out rects must hold.
  If (a) or (b) fails, build layer mode (step 14). Write why under "## Findings", as the task says.
- **E5 `WBP_Stage`'s tree** (step 2): that `RootBox` is the root and fills the window (so its local space is the space `ProjectWorldLocationtoWidgetPosition` returns); each child of the input row with its slot padding (`WrapWidgets` drops them, T28); `ChatSize`'s visibility value today (restore exactly that when the chat shows; `LogScroll` needs hit tests for the mouse wheel); the stamp widget's name (`StampText`, T09).
- **E6 `WBP_Stage`'s events.** List the EventGraph's event nodes (`find_nodes` "Event"). If `EventConstruct` exists, the chat's start state goes in its chain; if not, the draft below adds it.
- **E7 What runs at the start of every show, including a restart.** Find the `WBP_Stage` call that empties the chat at show start (`find_nodes` in `BP_Show.SetupShow` and `RestartShow`; a `ClearLog` or similar). If one exists, `ShowChat(false)` goes at the end of that `WBP_Stage` function, and `BP_Show` doesn't change. If none exists, insert a `Class|WBPStage|ShowChat :Show false` node in `BP_Show.SetupShow` (or whichever runs for every show) with T28's insert recipe, and lock `BP_Show`.
- **E8 How a new widget gets added to a Widget Blueprint.** `describe_toolset UMGToolSet`: T27, T28 and T29 used `ReplaceWidgetWithTemplate`, `WrapWidgets` and `BindToEventProperty`, and T28 and T29 added widgets (`StartButton`, `BannerSize`), so T28's and T29's transcripts or Findings name the call. Also how to create a new Widget Blueprint asset.
- **E9 Whether `write_graph_dsl` takes the literal `"•"`** (U+2022). If not, use `"."`, `". ."`, `". . ."`.
- **E10 `TextBlock` overflow:** check that a 25-word line (the game's cap, `prompts.json`) wraps to at most 4 lines at a wrap of 500 at the speech size. No line limit is set; if one is ever needed, `TextOverflowPolicy` is the property.

### Questions for the person (ask each with `AskUserQuestion` before step 4; one at a time)

- **P1 The cut actor's last words.** The task says a cut robot shows no bubble, and the Done-when counts bubbles only for seats still on stage. But in the reactions the cut actor speaks first (T10), so with the chat hidden its last words show nowhere on stage. Options: (1) **keep the task as written (recommended: the person wrote it twice, and the chat holds the line)**; (2) show a bubble over the fallen robot for its last words only. For (2), remove the `IsCut` check in `Say` for reaction lines and change the Done-when count to every `LINE`.
- **P2 The vote line's target.** At the tally each vote line's action is "votes for X" and its speech is the reason (T09). The bubble shows only the speech, so with the chat hidden the reason shows but not whom it is about; the robot turns to look at its pick (T19). Options: (1) **in the vote phase only, the bubble shows "Votes for X." in the action style above the reason (recommended: the vote is the point of the line)**; (2) the speech only, as written. For (1), `PlayCur` checks `Utilities|String|StartsWith (V CurAction) "votes for"` and passes the action as `Lead` to `Say`: add a `Lead` string input to `Say` and `ShowLine`, and a third TextBlock `LeadText` (the action style) above `SpeechText`. The drafts below leave `Lead` out.

## Design

### The flow

```
BPC_LinePlayer.Pump (typing branch) ── HushBubble ─► Robots[seat].Typing(Color)  ─► bubble: three dots
BPC_LinePlayer.PlayCur ─ NHOS: LINE ─ AddChatLine ─ HushBubble (if another seat) ─► Robots[seat].Say(Text, Color, IsAction)
                                                                                     └► bubble: the line, NHOS: BUBBLE <id>
BPC_LinePlayer.Pump (cue phase / prep / end) ─ HushBubble ─► RunCue
BP_Robot.SetCut, BP_Robot.ResetLook ─► HideBubble (no fade)
WBP_SpeechBubble.EventTick ─► Place ─► Fit (asks WBP_Stage.KeepOut for the panels) ─► moves itself and its tail
```

- **`BubbleSeat`** (new `int` in `BPC_LinePlayer`, default -1) is the seat whose bubble is up. A new line or typing bubble on another seat hushes it first, so at most one bubble is full and one fades. The same seat speaking again just changes the text.
- **The hold comes first.** `Pump` runs after the last line's hold, so hushing the old bubble when the typing bubble shows costs no reading time.
- **The last line stays up** until the next line or a `phase`, `prep` or `end` cue. A `banner`, `stamp`, `votes` or `cut` cue doesn't hush it. T30 sends a `phase` cue for every header change, turn headers included, which counts as "the phase changes".
- **A cut robot:** `Say` and `Typing` return at once when `IsCut` is true and print nothing. `SetCut` hides the bubble at once. So the Done-when count is one `BUBBLE` for each `LINE` of a seat that isn't cut.
- **Text:** the speech when it isn't empty. Otherwise the action, in the action style (`IsAction`). If both are empty, the bubble shows `...` in the action style and still prints `BUBBLE`, so the count holds.
- **Game lines get no bubble.** T29's banner and the header never pass through `PlayCur`, so they stay where they are.
- **The hidden chat still gets every line:** `PlayCur` calls `AddChatLine` whether or not the chat shows, and `ShowChat` only collapses `ChatSize`. So the chat is complete when it opens.
- **Only my screen changes.** No call here touches `ActorLine`, `SharedLog`, `game_messages` or an `NHOS: LOG` line. `ShowLine` stays the one way a line gets in (T30 hooks it).
- **`Say` has a third input, `IsAction` (bool, default false),** beyond the task's `Say(Text, Color)`, so the bubble can use the action style. A call with two arguments still works.

### Sizes and space

- **Units.** `WBP_Stage` is laid out at 1920 × 1080 (T27: the lower panel is 640 wide, a third of 1920), and the UI scales by the short side. At 1600 × 900 one unit is 0.833 px. So "wraps at about 420 px at 1600 × 900" is a wrap of **500 units** (417 px), and every size below is in units.
- **One space for all placement:** `RootBox`'s local space (E5), with (0, 0) at the window's top left and `KeepOut`'s `View` as its size. `ProjectWorldLocationtoWidgetPosition` returns this space, and `ToLocal` converts any widget's geometry into it.
- **What the bubble keeps clear of** (`WBP_Stage.KeepOut`, each only while visible): `HeaderSize`, `InfoSize` (my card), `LowerSize` (the input row, the vote row, and the chat when shown), `EventBanner` (T29's banner) and `StampText` (the reveal stamp). Plus the 24-unit window margin.
- **The crowd at the top.** By my estimate (camera at z 330, pitch −20, T27), a robot's label projects at about 25 to 30% of the height, so a bubble of 100 to 180 units above it reaches the strip where the header (left, up to 884 wide), the banner (900 to 1460) and the card (from 1476) sit. Expect many bubbles to move sideways or down. If the screenshots show most bubbles sitting on the robots' heads, lower the anchor's priority: a narrower wrap (420) or a smaller speech size from the style Blueprint (never under 18 pt) are the next levers. Record what you see.

### The fit rule (`WBP_SpeechBubble.Fit`)

Input: the bubble's rect (L, T, R, B) where it would sit with its tail tip on the anchor, and the anchor's x. Output: a shift (DX, DY), the tail's x offset from the bubble's center (TX), and whether the tail points up (Up).

1. **Window margin:** shift right if L < 24, left if R > View.x − 24, down if T < 24.
2. **Each panel in turn** (grown by an 8-unit gap): if the shifted rect overlaps it, take the smaller sideways move that keeps the bubble inside the margin (left: panel left − R; right: panel right − L). If neither fits, move down to the panel's bottom. One pass, in `KeepOut`'s order. A move that pushes into a later panel is caught by that panel's turn; a move that pushes into an earlier one is a rare case to look for in the screenshots.
3. **Tail:** TX = anchor x − the shifted center, clamped to ±(half the width − 28), so the tail stays under the rounded part and still points at the robot. Up is true when the shifted top is at or below the anchor (the bubble moved entirely under the head); then `TailUp` shows instead of `TailDown`.

`Fit` reads `WBP_Stage` only, so it is the same in both modes. Only `Place` differs.

### The mode: `WidgetComponent` first, the stage's layer if it fails

- **Component mode (try first, as the task says).** `BP_Robot` has a `WidgetComponent` `Bubble` in screen space, with draw-at-desired-size on and its pivot at (0.5, 1.0), so the bubble's bottom center (the tail tip) sits on the anchor and the text keeps one size. Inside the widget, `Root` (never moved) gives the layout rect in `EventTick`'s `MyGeometry`. `Place` converts it to stage space, calls `Fit`, and sets the render translation of `BubbleBox` (everything inside `Root`) to (DX, DY) and of the tails to (TX, 0). Reading `Root`'s geometry and moving only its child keeps the shift from feeding back into the next frame's rect.
- **Layer mode (fallback, step 14).** `WBP_Stage` gets a full-window `BubbleLayer` (CanvasPanel) after the panels and before `StageArea`, so the stamp and the banner draw over it. `BP_Robot.InitBubble` adds its bubble to it with `AddBubble`. Each bubble's `EventTick` projects its robot's `BubblePoint()`, builds its rect from its desired size, calls `Fit`, and sets its canvas slot's position to the anchor plus the shift (slot alignment (0.5, 1.0)). No `WidgetComponent`.
- `Say`, `Typing`, `Hush`, `ShowLine`, `ShowTyping`, the fade and `Fit` are the same in both modes. Only `InitBubble`, `Place` and the `Bubble` component change.

## Style values T38 needs (from T32's style Blueprint, A4 and A5)

| Value | Use | Fallback if missing |
|---|---|---|
| bubble fill | `Panel` brush | near-black (0.008, 0.009, 0.014) linear, opacity 0.92 (T27's input box fill) |
| speech text | `SpeechText` font, size, color | the chat's speech style; else 20 pt, white |
| action text | `ActionText` font, size, color: "the chat's action style" | `WBP_ChatLine`'s action style; else 18 pt italic, gray (0.55, 0.58, 0.65) linear |
| edge width | `Edge` padding (the seat color shows as a ring) | 3 |
| corner radius | `Edge`, `Panel` brushes | 12 (the panel 9, so the ring keeps an even width) |
| bubble padding | `Panel` padding | 16 left and right, 10 top and bottom |
| wrap width | `WrapTextAt` on both text blocks | 500 |
| window margin, gap | `Fit` | 24 (T27), 8 |
| fade time | `FadeStep` | 0.3 s (the task) |
| dots step | `DotStep` | 0.35 s |
| button style | `ChatButton`: the shared style for a secondary action | whatever `ContinueButton` and `StartButton` use after T32 |

**Contrast:** white on the fallback fill is above 15:1, and the fallback action gray is about 10:1. The edge is the seat color and carries no text. Measure from the screenshots as T27 did, with the real values.

## `WBP_SpeechBubble` (new Widget Blueprint, `/Game/NHOS/UI/WBP_SpeechBubble`)

### Widget tree

```
Root                Overlay       never moved; its geometry is the layout rect. Visibility HitTestInvisible.
└ BubbleBox         Overlay       moved by Place (render translation). Collapsed until a line shows.
  ├ TailDown        SizeBox 18×18, slot HAlign Center, VAlign Bottom. Render angle 45°.
  │ └ TailDownFill  Border, RoundedBox brush (radius 2), tinted the seat color with SetBrushColor.
  ├ TailUp          SizeBox 18×18, slot HAlign Center, VAlign Top. Render angle 45°. Collapsed.
  │ └ TailUpFill    Border, as TailDownFill.
  └ Edge            Border, RoundedBox brush (corner radius), white fill tinted the seat color with SetBrushColor.
    │               Slot padding 12 top and 12 bottom, so half of each tail's diamond sticks out past the ring.
    │               Its own padding = the edge width.
    └ Panel         Border, RoundedBox brush, the bubble fill. Padding = the bubble padding.
      └ TextStack   Overlay
        ├ SpeechText  TextBlock, speech style, AutoWrap off, WrapTextAt 500, justify left. Collapsed.
        ├ ActionText  TextBlock, action style, WrapTextAt 500. Collapsed.
        └ DotsBox     SizeBox, width 64 (so the bubble doesn't change width as the dots cycle). Collapsed.
          └ DotsText  TextBlock, speech style, bold, centered.
```

- The tails draw before `Edge`, so the bubble covers the top half of `TailDown`'s diamond and only a colored point shows under it. No new art.
- `Edge` and `Panel` are both RoundedBox Borders, so the seat color shows only as a ring: `SetBrushColor` tints the whole brush, and the inner `Panel` covers all but the ring.
- No text here is set in the designer except `DotsText`'s default. `EventConstruct` applies the style values.

### Variables

| Name | Type | Default | Use |
|---|---|---|---|
| `Shown` | bool | false | A line or the dots are up. `EventTick` places only while true. |
| `Fading` | bool | false | A fade is running. `ShowLine` and `ShowTyping` stop it by setting it false. |
| `Alpha` | float | 1.0 | The fade's opacity. A variable, not a `GetRenderOpacity` read (T29: a pure read runs again at each use). |
| `TypingOn` | bool | false | The dots cycle while true. |
| `Dot` | int | 0 | Which of the three dot texts shows. |
| `LastUp` | bool | false | The tail last set, so visibility changes only when it flips. |
| `Stage` | WBP_Stage ref | | Found once by `FindStage`. |
| `NullStage` | WBP_Stage ref | never set | For the validity check (T19). |
| `FX`, `FY` | float | | `Fit`'s running shift. |
| `Bot`, `NullBot` | BP_Robot ref | | Layer mode only: the robot to follow, and the never-set one. |
| `FadeStepTime` | float | 0.03 | `fade time / 10`, set by `EventConstruct`. |
| `DotTime` | float | 0.35 | From the style Blueprint. |

### Functions

All impure, made with `add_function_graph`. Bind each call's result before an `if`, `return` or `select` uses it (T19).

| Function | Inputs | Outputs | Called by |
|---|---|---|---|
| `ShowLine` | `Text` string, `Color` LinearColor (A3), `IsAction` bool | | `BP_Robot.Say` |
| `ShowTyping` | `Color` LinearColor | | `BP_Robot.Typing` |
| `SetEdge` | `Color` LinearColor | | `ShowLine`, `ShowTyping` |
| `DotStep` | | | `ShowTyping`, its timer |
| `FadeOut` | | | `BP_Robot.Hush` |
| `FadeStep` | | | `FadeOut`, its timer |
| `HideNow` | | | `FadeStep`, `BP_Robot.HideBubble`, `BP_Robot.InitBubble` |
| `FindStage` | | | `Fit` |
| `Fit` | `L`, `T`, `R`, `B`, `AX` float | `DX`, `DY`, `TX` float, `Up` bool | `Place` |
| `Place` | `Geo` Geometry | | `EventTick` |
| `SetRobot` (layer mode only) | `NewBot` BP_Robot ref | | `BP_Robot.InitBubble` |

### Draft sources (shorthand; expand each with `Tools/dslpp.py`)

```lisp
;;; GRAPH EventGraph
; E3: confirm both event names. EventConstruct applies T32's style (A4); the calls are placeholders.
(event EventConstruct
  (Class|BPUIStyle|StyleText :Text (Variables|WBP_SpeechBubble|GetSpeechText) :Role "chat_speech")
  (Class|BPUIStyle|StyleText :Text (Variables|WBP_SpeechBubble|GetActionText) :Role "chat_action")
  (Class|BPUIStyle|StyleText :Text (Variables|WBP_SpeechBubble|GetDotsText) :Role "chat_speech")
  (set FadeStepTime (/ (Class|BPUIStyle|GetFadeTime) 10.0))
  (CallFunction|HideNow))

(event EventTick (MyGeometry InDeltaTime)
  (if (V Shown)
    (CallFunction|Place :Geo MyGeometry)))

;;; GRAPH SetEdge
(fn SetEdge (Color)
  (Class|Border|SetBrushColor :self (Variables|WBP_SpeechBubble|GetEdge) :InBrushColor Color)
  (Class|Border|SetBrushColor :self (Variables|WBP_SpeechBubble|GetTailDownFill) :InBrushColor Color)
  (Class|Border|SetBrushColor :self (Variables|WBP_SpeechBubble|GetTailUpFill) :InBrushColor Color))

;;; GRAPH ShowLine
(fn ShowLine (Text Color IsAction)
  (set TypingOn false)
  (set Fading false)
  (set Alpha 1.0)
  (CallFunction|SetEdge :Color Color)
  (bind _empty (Utilities|String|IsEmpty Text))
  (bind _t (select _empty "..." Text))
  (bind _act (or IsAction _empty))
  (Widget|SetVisibility :self (Variables|WBP_SpeechBubble|GetDotsBox) :InVisibility "Collapsed")
  (if _act
    (Class|Text|SetText :self (Variables|WBP_SpeechBubble|GetActionText) :Text (Utilities|Text|ToText(String) _t))
    (Widget|SetVisibility :self (Variables|WBP_SpeechBubble|GetActionText) :InVisibility "HitTestInvisible")
    (Widget|SetVisibility :self (Variables|WBP_SpeechBubble|GetSpeechText) :InVisibility "Collapsed")
    (else
      (Class|Text|SetText :self (Variables|WBP_SpeechBubble|GetSpeechText) :Text (Utilities|Text|ToText(String) _t))
      (Widget|SetVisibility :self (Variables|WBP_SpeechBubble|GetSpeechText) :InVisibility "HitTestInvisible")
      (Widget|SetVisibility :self (Variables|WBP_SpeechBubble|GetActionText) :InVisibility "Collapsed")))
  (Widget|SetRenderOpacity :self (Variables|WBP_SpeechBubble|GetBubbleBox) :InOpacity 1.0)
  (Widget|SetVisibility :self (Variables|WBP_SpeechBubble|GetBubbleBox) :InVisibility "HitTestInvisible")
  (set Shown true))

;;; GRAPH ShowTyping
(fn ShowTyping (Color)
  (set Fading false)
  (set Alpha 1.0)
  (CallFunction|SetEdge :Color Color)
  (Widget|SetVisibility :self (Variables|WBP_SpeechBubble|GetSpeechText) :InVisibility "Collapsed")
  (Widget|SetVisibility :self (Variables|WBP_SpeechBubble|GetActionText) :InVisibility "Collapsed")
  (Widget|SetVisibility :self (Variables|WBP_SpeechBubble|GetDotsBox) :InVisibility "HitTestInvisible")
  (Widget|SetRenderOpacity :self (Variables|WBP_SpeechBubble|GetBubbleBox) :InOpacity 1.0)
  (Widget|SetVisibility :self (Variables|WBP_SpeechBubble|GetBubbleBox) :InVisibility "HitTestInvisible")
  (set Shown true)
  (set Dot 2)
  (set TypingOn true)
  (CallFunction|DotStep))

;;; GRAPH DotStep
; A timer set again for the same function resets the pending one, so only one chain runs.
(fn DotStep ()
  (if (not (V TypingOn))
    (return))
  (set Dot (select (>= (V Dot) 2) 0 (+ (V Dot) 1)))
  (bind _d (select (== (V Dot) 0) "•" (select (== (V Dot) 1) "• •" "• • •")))
  (Class|Text|SetText :self (Variables|WBP_SpeechBubble|GetDotsText) :Text (Utilities|Text|ToText(String) _d))
  (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "DotStep" :Time (V DotTime) :bLooping false))

;;; GRAPH FadeOut
(fn FadeOut ()
  (if (not (V Shown))
    (return))
  (set TypingOn false)
  (set Fading true)
  (CallFunction|FadeStep))

;;; GRAPH FadeStep
; Ten steps of FadeStepTime: 0.3 s at the fallback. ShowLine or ShowTyping set Fading false, so a pending step stops.
(fn FadeStep ()
  (if (not (V Fading))
    (return))
  (set Alpha (- (V Alpha) 0.1))
  (Widget|SetRenderOpacity :self (Variables|WBP_SpeechBubble|GetBubbleBox) :InOpacity (Math|Float|Max(Float) (V Alpha) 0.0))
  (if (> (V Alpha) 0.01)
    (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "FadeStep" :Time (V FadeStepTime) :bLooping false)
    (else
      (CallFunction|HideNow))))

;;; GRAPH HideNow
(fn HideNow ()
  (set Fading false)
  (set TypingOn false)
  (set Shown false)
  (set Alpha 1.0)
  (Widget|SetVisibility :self (Variables|WBP_SpeechBubble|GetBubbleBox) :InVisibility "Collapsed"))

;;; GRAPH FindStage
(fn FindStage ()
  (if (!= (V Stage) (V NullStage))
    (return))
  (bind _all (UserInterface|GetAllWidgetsOfClass :WidgetClass "/Game/NHOS/UI/WBP_Stage.WBP_Stage_C" :TopLevelOnly true))
  (if (> (len _all) 0)
    (set Stage (get _all 0))))

;;; GRAPH Fit
(fn Fit (L T R B AX)
  (set FX 0.0)
  (set FY 0.0)
  (CallFunction|FindStage)
  (if (== (V Stage) (V NullStage))
    (return 0.0 0.0 0.0 false))
  (bind (_ktl _kbr _view) (Class|WBPStage|KeepOut :self (V Stage)))
  (bind _vr (- (.x _view) 24.0))
  ; 1. the window margin
  (if (< L 24.0)
    (set FX (- 24.0 L)))
  (if (> R _vr)
    (set FX (- _vr R)))
  (if (< T 24.0)
    (set FY (- 24.0 T)))
  ; 2. clear of each panel, in KeepOut's order
  (for _i (range (len _ktl))
    (bind _kl (- (.x (get _ktl _i)) 8.0))
    (bind _kt (- (.y (get _ktl _i)) 8.0))
    (bind _kr (+ (.x (get _kbr _i)) 8.0))
    (bind _kb (+ (.y (get _kbr _i)) 8.0))
    (bind _nl (+ L (V FX)))
    (bind _nr (+ R (V FX)))
    (bind _nt (+ T (V FY)))
    (bind _nb (+ B (V FY)))
    (if (and (and (< _nl _kr) (> _nr _kl)) (and (< _nt _kb) (> _nb _kt)))
      (bind _sl (- _kl _nr))
      (bind _sr (- _kr _nl))
      (bind _okl (>= (+ _nl _sl) 24.0))
      (bind _okr (<= (+ _nr _sr) _vr))
      (if (and _okl (or (not _okr) (<= (- 0.0 _sl) _sr)))
        (set FX (+ (V FX) _sl))
        (else
          (if _okr
            (set FX (+ (V FX) _sr))
            (else
              (set FY (+ (V FY) (- _kb _nt)))))))))
  ; 3. the tail
  (bind _lim (Math|Float|Max(Float) (- (* 0.5 (- R L)) 28.0) 0.0))
  (bind _tx (Math|Float|Clamp(Float) :Value (- AX (+ (* 0.5 (+ L R)) (V FX))) :Min (- 0.0 _lim) :Max _lim))
  (return (V FX) (V FY) _tx (>= (+ T (V FY)) B)))

;;; GRAPH Place
; Component mode. B is the tail tip, which the component's pivot put on the anchor.
(fn Place (Geo)
  (CallFunction|FindStage)
  (if (== (V Stage) (V NullStage))
    (return))
  (bind _tl (Class|WBPStage|ToLocal :self (V Stage) :Abs (Utilities|Geometry|LocalToAbsolute Geo (Math|Vector2D|MakeVector2D :X 0.0 :Y 0.0))))
  (bind _br (Class|WBPStage|ToLocal :self (V Stage) :Abs (Utilities|Geometry|LocalToAbsolute Geo (Utilities|Geometry|GetLocalSize Geo))))
  (bind (_dx _dy _tx _up) (CallFunction|Fit :L (.x _tl) :T (.y _tl) :R (.x _br) :B (.y _br) :AX (* 0.5 (+ (.x _tl) (.x _br)))))
  (Widget|SetRenderTranslation :self (Variables|WBP_SpeechBubble|GetBubbleBox) :Translation (Math|Vector2D|MakeVector2D :X _dx :Y _dy))
  (Widget|SetRenderTranslation :self (Variables|WBP_SpeechBubble|GetTailDown) :Translation (Math|Vector2D|MakeVector2D :X _tx :Y 0.0))
  (Widget|SetRenderTranslation :self (Variables|WBP_SpeechBubble|GetTailUp) :Translation (Math|Vector2D|MakeVector2D :X _tx :Y 0.0))
  (if (xor _up (V LastUp))
    (set LastUp _up)
    (if _up
      (Widget|SetVisibility :self (Variables|WBP_SpeechBubble|GetTailUp) :InVisibility "HitTestInvisible")
      (Widget|SetVisibility :self (Variables|WBP_SpeechBubble|GetTailDown) :InVisibility "Collapsed")
      (else
        (Widget|SetVisibility :self (Variables|WBP_SpeechBubble|GetTailDown) :InVisibility "HitTestInvisible")
        (Widget|SetVisibility :self (Variables|WBP_SpeechBubble|GetTailUp) :InVisibility "Collapsed")))))
```

Notes on the drafts:

- **The DSL rules they follow:** an `if` whose body ends in `return` makes the rest its else branch, and one without joins the code after it (T01). Strings compare with `streq`, never `==` (T01; none here need it). Objects compare with a never-set variable, not `Utilities|IsValid` (T19). Results of impure calls are bound before use (T19), and a call with several outputs binds as `(bind (a b c) ...)` (T19). Enum pins take quoted value names (T09), and an `if` with two `SetVisibility` calls stands in for a `select` on an enum, as `SetPrepMode` does. `Class|Text|SetText` passes `:self` and `:Text` by name (T27). `print` expands to `Development|PrintString ... false`. Each `;;; GRAPH` header is one `write_graph_dsl` call.
- **Literals in `select`:** `(select _empty "..." Text)` and the dot strings go into a string-typed `select`, as `BP_Show` passes literal strings to typed pins. If `select` takes the literal as a wildcard and fails (T01's literal rule), bind each literal to a typed string variable first.
- **`Place` in layer mode** (step 14) replaces the draft above:

```lisp
;;; GRAPH Place
; Layer mode. The canvas slot's alignment is (0.5, 1.0), so its position is the tail tip.
(fn Place (Geo)
  (if (== (V Bot) (V NullBot))
    (return))
  (bind _wp (Class|BPRobot|BubblePoint :self (V Bot)))
  (bind (_sp _ok) (Game|Player|ProjectWorldLocationtoWidgetPosition :PlayerController (Game|GetPlayerController 0) :WorldLocation _wp :bPlayerViewportRelative false))
  (if (not _ok)
    (Widget|SetRenderOpacity :self (Variables|WBP_SpeechBubble|GetRoot) :InOpacity 0.0)
    (return))
  (Widget|SetRenderOpacity :self (Variables|WBP_SpeechBubble|GetRoot) :InOpacity 1.0)
  (bind _ds (Widget|GetDesiredSize :self self))
  (bind _hw (* 0.5 (.x _ds)))
  (bind (_dx _dy _tx _up) (CallFunction|Fit :L (- (.x _sp) _hw) :T (- (.y _sp) (.y _ds)) :R (+ (.x _sp) _hw) :B (.y _sp) :AX (.x _sp)))
  (Class|CanvasPanelSlot|SetPosition :self (Widget|SlotAsCanvasSlot :Widget self) :InPosition (Math|Vector2D|MakeVector2D :X (+ (.x _sp) _dx) :Y (+ (.y _sp) _dy)))
  (Widget|SetRenderTranslation :self (Variables|WBP_SpeechBubble|GetTailDown) :Translation (Math|Vector2D|MakeVector2D :X _tx :Y 0.0))
  (Widget|SetRenderTranslation :self (Variables|WBP_SpeechBubble|GetTailUp) :Translation (Math|Vector2D|MakeVector2D :X _tx :Y 0.0))
  (if (xor _up (V LastUp))
    (set LastUp _up)
    (if _up
      (Widget|SetVisibility :self (Variables|WBP_SpeechBubble|GetTailUp) :InVisibility "HitTestInvisible")
      (Widget|SetVisibility :self (Variables|WBP_SpeechBubble|GetTailDown) :InVisibility "Collapsed")
      (else
        (Widget|SetVisibility :self (Variables|WBP_SpeechBubble|GetTailDown) :InVisibility "HitTestInvisible")
        (Widget|SetVisibility :self (Variables|WBP_SpeechBubble|GetTailUp) :InVisibility "Collapsed")))))

;;; GRAPH SetRobot
(fn SetRobot (NewBot)
  (set Bot NewBot))
```

The projection's output names (`_sp`, `_ok`) and its pin names are E3 items. In layer mode `EventTick` still calls `Place` only while `Shown`.

## `BP_Robot` changes

### New component and variables

- **`Bubble`** (`WidgetComponent`, component mode only), attached to the `Label`'s parent (E1), not to `Rig`. Set space Screen, draw at desired size on, pivot (0.5, 1.0), relative location (0, 0, `BubbleZ`) in the template too, for the editor's view; `InitBubble` sets them again at run time (E2).
- `BubbleW` (WBP_SpeechBubble ref), `HasBubble` (bool, false), `BubbleZ` (float, 262; E1).

### New functions

| Function | Inputs | Outputs |
|---|---|---|
| `InitBubble` | | |
| `Say` | `Text` string, `Color` LinearColor, `IsAction` bool (default false) | |
| `Typing` | `Color` LinearColor | |
| `Hush` | | |
| `HideBubble` | | |
| `BubblePoint` (layer mode) | | Vector |

```lisp
;;; GRAPH InitBubble
; Component mode. Made on first use, not at BeginPlay, so the player controller exists.
; Not called from ResetLook or the construction script, so the editor never makes a widget.
(fn InitBubble ()
  (if (V HasBubble)
    (return))
  (set HasBubble true)
  (bind _w (UserInterface|CreateWidget "/Game/NHOS/UI/WBP_SpeechBubble.WBP_SpeechBubble_C" (Game|GetPlayerController 0)))
  (set BubbleW _w)
  (UserInterface|WidgetComponent|SetWidgetSpace :self (V Bubble) :NewSpace "Screen")
  (UserInterface|WidgetComponent|SetDrawAtDesiredSize :self (V Bubble) :bInDrawAtDesiredSize true)
  (UserInterface|WidgetComponent|SetPivot :self (V Bubble) :InPivot (Math|Vector2D|MakeVector2D :X 0.5 :Y 1.0))
  (Transformation|SetRelativeLocation :self (V Bubble) :NewLocation (Math|Vector|MakeVector :X 0.0 :Y 0.0 :Z (V BubbleZ)))
  (UserInterface|WidgetComponent|SetWidget :self (V Bubble) :Widget (V BubbleW))
  (Class|WBPSpeechBubble|HideNow :self (V BubbleW)))

;;; GRAPH Say
(fn Say (Text Color IsAction)
  (if (V IsCut)
    (return))
  (CallFunction|InitBubble)
  (Class|WBPSpeechBubble|ShowLine :self (V BubbleW) :Text Text :Color Color :IsAction IsAction)
  (print (cat "NHOS: BUBBLE " (V PersonaId))))

;;; GRAPH Typing
(fn Typing (Color)
  (if (V IsCut)
    (return))
  (CallFunction|InitBubble)
  (Class|WBPSpeechBubble|ShowTyping :self (V BubbleW) :Color Color))

;;; GRAPH Hush
(fn Hush ()
  (if (not (V HasBubble))
    (return))
  (Class|WBPSpeechBubble|FadeOut :self (V BubbleW)))

;;; GRAPH HideBubble
(fn HideBubble ()
  (if (not (V HasBubble))
    (return))
  (Class|WBPSpeechBubble|HideNow :self (V BubbleW)))
```

**If E2 finds no `Bubble` on the placed robots,** add a `WidgetComponent` variable `Bubble` and make it at the top of `InitBubble`, after `(set HasBubble true)`: `(bind _c (Game|AddComponentbyClass :Class "/Script/UMG.WidgetComponent" :bManualAttachment false))` then `(set Bubble _c)` (check the node's name and pins with `find_node_types`; T05 found that it returns the typed component). With `bManualAttachment` false it attaches to the root, which is right if E1 finds the `Label` on the root.

**Layer mode** (step 14) replaces `InitBubble` and adds `BubblePoint`:

```lisp
;;; GRAPH InitBubble
(fn InitBubble ()
  (if (V HasBubble)
    (return))
  (set HasBubble true)
  (bind _w (UserInterface|CreateWidget "/Game/NHOS/UI/WBP_SpeechBubble.WBP_SpeechBubble_C" (Game|GetPlayerController 0)))
  (set BubbleW _w)
  (Class|WBPSpeechBubble|SetRobot :self (V BubbleW) :NewBot self)
  (bind _all (UserInterface|GetAllWidgetsOfClass :WidgetClass "/Game/NHOS/UI/WBP_Stage.WBP_Stage_C" :TopLevelOnly true))
  (if (> (len _all) 0)
    (Class|WBPStage|AddBubble :self (get _all 0) :Bubble (V BubbleW)))
  (Class|WBPSpeechBubble|HideNow :self (V BubbleW)))

;;; GRAPH BubblePoint
; The actor's location, not Rig's, so the bubble follows moves and the riser but not the bob.
(fn BubblePoint ()
  (return (+ (Transformation|GetActorLocation) (Math|Vector|MakeVector :X 0.0 :Y 0.0 :Z (V BubbleZ)))))
```

### Changed graphs (both have sources in `Graphs/BP_Robot/`)

- **`SetCut.txt`:** add `(CallFunction|HideBubble)` right after `(CallFunction|SetLit :On false)`. The rest stays.
- **`ResetLook.txt`:** add `(CallFunction|HideBubble)` right after `(CallFunction|SetLit :On false)`. `ResetLook` runs from `Setup` and `SetPersona`, which the construction script also runs (`PreviewPersona`, T17); `HideBubble` does nothing while `HasBubble` is false, so the editor is safe.

Write each from its file with the one line added, and commit the updated files.

## `BPC_LinePlayer` changes (on T30's sources)

- New variable `BubbleSeat` (int, default -1).
- New functions `RobotAt(Seat)` → BP_Robot ref, and `HushBubble()`.
- Three insertions in T30's graphs and one in `Clear`. Write each graph from T30's file in `Graphs/BPC_LinePlayer/` with the lines added.

```lisp
;;; GRAPH RobotAt
; E3: if the component can read BP_Show's Robots, this is the getter. Otherwise call BP_Show.RobotAt (below).
(fn RobotAt (Seat)
  (return (get (Class|BPShow|GetRobots :self (V Show)) Seat)))

;;; GRAPH HushBubble
(fn HushBubble ()
  (if (< (V BubbleSeat) 0)
    (return))
  (bind _hb (CallFunction|RobotAt :Seat (V BubbleSeat)))
  (Class|BPRobot|Hush :self _hb)
  (set BubbleSeat -1))
```

**In `PlayCur`,** right after T30's `AddChatLine` line (so the order stays `NHOS: LINE`, then the chat line, then `NHOS: BUBBLE`):

```lisp
  (if (!= (V BubbleSeat) (V CurSeat))
    (CallFunction|HushBubble))
  (bind _bot (CallFunction|RobotAt :Seat (V CurSeat)))
  (bind _nosp (Utilities|String|IsEmpty (V CurSpeech)))
  (Class|BPRobot|Say :self _bot :Text (select _nosp (V CurAction) (V CurSpeech)) :Color (V CurColor) :IsAction _nosp)
  (set BubbleSeat (V CurSeat))
```

`HushBubble` returns at once when `BubbleSeat` is -1, so the first line needs no special case.

**In `Pump`'s typing branch,** right after T30's `SetTyping` line:

```lisp
    (CallFunction|HushBubble)
    (bind _tb (CallFunction|RobotAt :Seat (V CurSeat)))
    (Class|BPRobot|Typing :self _tb :Color (V CurColor))
    (set BubbleSeat (V CurSeat))
```

T30's `TypingText` in the chat stays: it is inside `ChatSize`, so it hides with the chat, and the chat still shows it when open.

**In `Pump`'s cue branch,** right before T30's `RunCue` line (`RunCue` may push or cue more items, so hush first):

```lisp
    (if (or (streq (V CurKind) "phase") (or (streq (V CurKind) "prep") (streq (V CurKind) "end")))
      (CallFunction|HushBubble))
```

**In `Clear`** (if T30 made it), add `(CallFunction|HushBubble)` at the end.

## `BP_Show` changes (none expected)

Only if E3 finds no way to read `Robots` from the component:

```lisp
;;; GRAPH RobotAt
(fn RobotAt (Seat)
  (return (Utilities|Array|Get(acopy) (Variables|Default|GetRobots) Seat)))
```

`BPC_LinePlayer.RobotAt` then becomes `(return (Class|BPShow|RobotAt :self (V Show) :Seat Seat))`, bound first if the call is impure. And only if E7 finds no `WBP_Stage` call at every show start: one inserted `Class|WBPStage|ShowChat :Show false` node. Either one means locking `BP_Show`. Its graph sources go to `Graphs/BP_Show/` (`RobotAt.txt`; the insert has no source, so note the node in Findings, as T28 did).

## `WBP_Stage` changes

### Widgets

- **`ChatButton`** (Button) in the input row, after `PassButton` and before `ContinueButton` and `StartButton` (E5: read every slot's padding first, and give the new slot the same left padding as `StartButton`, T28: 10). Inside it, **`ChatButtonText`** (TextBlock), "Show chat". Styled by T32's shared button call (A4) as a secondary action. Set `IsFocusable` false, so a click never takes the focus from the input box. Visible in every phase.
- Check the row's width at 1600 × 900: the input box still needs room for a short line. If it gets narrower than about 250 units, tell the person; T34 owns the final layout.
- **Layer mode only:** **`BubbleLayer`** (CanvasPanel), a child of `RootBox` placed after `LowerSize`, `InfoSize` and `HeaderSize` and before `StageArea`, filling the overlay (HAlign and VAlign Fill), visibility `HitTestInvisible`.

### Variables

`ChatShown` (bool, false), `KeepTL` and `KeepBR` (Vector2D arrays). The function that shows the chat is `ShowChat`, not `SetChatShown`, so its name doesn't clash with the variable's setter.

### New graphs

```lisp
;;; GRAPH ShowChat
; E5: use the visibility ChatSize has today in place of "SelfHitTestInvisible".
(fn ShowChat (Show)
  (Variables|Default|SetChatShown Show)
  (if Show
    (Widget|SetVisibility :self (Variables|WBP_Stage|GetChatSize) :InVisibility "SelfHitTestInvisible")
    (Class|Text|SetText :self (Variables|WBP_Stage|GetChatButtonText) :Text (Utilities|Text|ToText(String) "Hide chat"))
    (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "ChatToEnd" :Time 0.05 :bLooping false)
    (else
      (Widget|SetVisibility :self (Variables|WBP_Stage|GetChatSize) :InVisibility "Collapsed")
      (Class|Text|SetText :self (Variables|WBP_Stage|GetChatButtonText) :Text (Utilities|Text|ToText(String) "Show chat")))))

;;; GRAPH ChatToEnd
; A collapsed ScrollBox has no size, so scroll after the chat has had a frame to lay out.
(fn ChatToEnd ()
  (Class|ScrollBox|ScrollToEnd :self (Variables|WBP_Stage|GetLogScroll)))

;;; GRAPH AddKeep
(fn AddKeep (W)
  (bind _v (Widget|IsVisible :self W))
  (if (not _v)
    (return))
  (bind _g (Widget|GetCachedGeometry :self W))
  (bind _rg (Widget|GetCachedGeometry :self (Variables|WBP_Stage|GetRootBox)))
  (bind _tl (Utilities|Geometry|AbsoluteToLocal _rg (Utilities|Geometry|LocalToAbsolute _g (Math|Vector2D|MakeVector2D :X 0.0 :Y 0.0))))
  (bind _br (Utilities|Geometry|AbsoluteToLocal _rg (Utilities|Geometry|LocalToAbsolute _g (Utilities|Geometry|GetLocalSize _g))))
  (add (V KeepTL) _tl)
  (add (V KeepBR) _br))

;;; GRAPH KeepOut
; Rects in RootBox's space, each only while visible. Order matters for Fit: the big panels first.
(fn KeepOut ()
  (clear (V KeepTL))
  (clear (V KeepBR))
  (CallFunction|AddKeep :W (Variables|WBP_Stage|GetHeaderSize))
  (CallFunction|AddKeep :W (Variables|WBP_Stage|GetInfoSize))
  (CallFunction|AddKeep :W (Variables|WBP_Stage|GetLowerSize))
  (CallFunction|AddKeep :W (Variables|WBP_Stage|GetEventBanner))
  (CallFunction|AddKeep :W (Variables|WBP_Stage|GetStampText))
  (bind _view (Utilities|Geometry|GetLocalSize (Widget|GetCachedGeometry :self (Variables|WBP_Stage|GetRootBox))))
  (return (V KeepTL) (V KeepBR) _view))

;;; GRAPH ToLocal
(fn ToLocal (Abs)
  (return (Utilities|Geometry|AbsoluteToLocal (Widget|GetCachedGeometry :self (Variables|WBP_Stage|GetRootBox)) Abs)))
```

- `AddKeep`'s input `W` is a `Widget` object reference, so any panel can go in.
- `KeepOut` runs once a frame for each bubble that is up, at most two. If a profile ever shows it, cache the rects once a frame.
- `StampText` collapses when the stamp is cleared (T09: `""` hides it), and `EventBanner` collapses between banners (T29), so `IsVisible` drops them.

**The click** (T28's recipe: `BindToEventProperty` with `eventName` `OnClicked`, `propertyName` `ChatButton`, `propertyClass` `/Script/UMG.Button`, then write this chain to the EventGraph alone; `write_graph_dsl` keeps the other chains). Its source goes to `Graphs/WBP_Stage/EventGraph.ChatButton.txt`:

```lisp
; Only the ChatButton chain of WBP_Stage's EventGraph (T38).
(event OnClicked(ChatButton)
  (bind _show (not (Variables|Default|GetChatShown)))
  (CallFunction|ShowChat :Show _show)
  (if _show
    (Development|PrintString "NHOS: CHAT shown" false)
    (else
      (Development|PrintString "NHOS: CHAT hidden" false)))
  (if (Variables|Default|GetLastCanType)
    (Widget|SetKeyboardFocus :self (Variables|WBP_Stage|GetInputBox))))
```

`LastCanType` is `SetPrompt`'s copy of "it is my turn to type" (`Graphs/WBP_Stage/SetPrompt.txt`), so the focus goes back to the input box only on my turn.

**The start state.** Per E6 and E7, put `(CallFunction|ShowChat :Show false)` at the end of the `WBP_Stage` function that runs at every show start (E7), and in `EventConstruct` for the first show:

```lisp
; Only if E6 finds no EventConstruct chain. Source: Graphs/WBP_Stage/EventGraph.Construct.txt.
(event EventConstruct
  (CallFunction|ShowChat :Show false))
```

If `EventConstruct` exists, add the call to the end of its chain instead; that chain has no source, so it is a node insert (T28's recipe), noted in Findings.

**Layer mode only:**

```lisp
;;; GRAPH AddBubble
(fn AddBubble (Bubble)
  (bind _slot (Class|CanvasPanel|AddChildtoCanvas :self (Variables|WBP_Stage|GetBubbleLayer) :Content Bubble))
  (Class|CanvasPanelSlot|SetAutoSize :self _slot :InbAutoSize true)
  (Class|CanvasPanelSlot|SetAlignment :self _slot :InAlignment (Math|Vector2D|MakeVector2D :X 0.5 :Y 1.0)))
```

`AddBubble`'s input is a `WBP_SpeechBubble` reference. `BP_Robot` calls it with `Class|WBPStage|AddBubble`.

## Editor steps in order (each one Unreal MCP call, or one short script)

**Before step 1:** `git pull`, read `Agents/`, `git lfs locks`, claim T38, and lock `Content/NHOS/Stage/BP_Robot.uasset`, `Content/NHOS/UI/WBP_Stage.uasset` and `Content/NHOS/Core/BPC_LinePlayer.uasset` (and `BP_Show` only if E3 or E7 needs it). Write the status file with `Editor: driving`. Call `get_execution_environment` once (T01). Expand the drafts with `Tools/dslpp.py` and copy them to `Saved/T38/src/` (`AssetTools.read_file` reads only under `Content/` and `Saved/`, T28). `execute_tool_script`'s `run()` returns a dict with string keys (T29). Keep each call under about 60 s.

1. **No editor:** read T30's and T32's Findings and their `Graphs/` files (A1 to A6), the doc's UI section through the Claude Docs connector, and ask the person P1 and P2. Update the drafts here to match.
2. **Read (one script):** `WBP_Stage`'s tree with every slot's padding and `ChatSize`'s visibility (E5); its EventGraph's event nodes (E6); in `BP_Show`, `find_nodes` for `WBP_Stage` calls in `SetupShow` and `RestartShow` (E7).
3. **Node names (one script):** E3's lists in each Blueprint, `BP_Robot`'s `Label` properties (E1), and `describe_toolset UMGToolSet` (E8).
4. **Create `WBP_SpeechBubble`** and its widget tree (E8).
5. **Set the widgets' properties** (one script): sizes, the RoundedBox brushes, the paddings, `WrapTextAt` 500, the tails' 45° render angle, the starting visibilities. Compile.
6. **Bubble variables and every function's signature** with an empty body. Compile, save.
7. **`BP_Robot` setup:** the `Bubble` component (component mode), the three variables, every new function's signature. Compile, save. Check E2 now: start PIE, `get_components` on one robot, stop PIE.
8. **`WBP_Stage` setup:** `ChatButton` and `ChatButtonText` in the input row with the paddings set back, the shared button style, `IsFocusable` false; the variables; the signatures of `ShowChat`, `ChatToEnd`, `AddKeep`, `KeepOut` and `ToLocal`. Compile, save.
9. **Bubble bodies, batch 1:** `EventGraph` (Construct and Tick), `SetEdge`, `ShowLine`, `ShowTyping`, `DotStep`, `FadeOut`, `FadeStep`, `HideNow`.
10. **`WBP_Stage` bodies:** `AddKeep`, `KeepOut`, `ToLocal`, `ShowChat`, `ChatToEnd`; `BindToEventProperty` for `ChatButton`, then the click chain; the start state (E6, E7). Compile, save.
11. **Bubble bodies, batch 2:** `FindStage`, `Fit`, `Place`. Compile, save.
12. **`BP_Robot` bodies:** `InitBubble`, `Say`, `Typing`, `Hush`, `HideBubble`, and `SetCut` and `ResetLook` with their one new line. Compile, save.
13. **`BPC_LinePlayer`:** `BubbleSeat`, `RobotAt` (or `BP_Show.RobotAt`), `HushBubble`, and the insertions in `PlayCur`, `Pump` and `Clear`. Compile, save. **Then the probe (E4):** PIE in a 1600 × 900 floating window, Test for Free, autoplay off, played by hand through the Slate inspector (T27); take a screenshot during an AI line of a scene turn, and one with a robot at Right; read the log for `NHOS: BUBBLE`. Decide the mode and write why.
14. **Only if E4 fails, layer mode:** remove the `Bubble` component; add `BubbleLayer` and `AddBubble` to `WBP_Stage`; write `BP_Robot`'s layer `InitBubble` and `BubblePoint` and the bubble's layer `Place` and `SetRobot`. Compile, save, and repeat the probe.
15. **Compile and save all.** Read the editor log for `LogBlueprint` errors. Compiling may mark `L_Stage` and `BPC_LLMClient` dirty with no change (T08, T10): leave them unsaved.
16. **The checks below.** Then the `Graphs/` files, the Findings, the doc edit proposal, and the commit, with a `Waiting:` line only if the doc edit still waits for my OK ("When only my check is left" in the plan).

## Checks (the Done-when)

1. **Free autoplay** in a game window: `autoplay: true`, `mode: free` and `fast_lines: true` in `Local/switches.json`, `-log=T38auto.log`. It reaches `NHOS: SHOW END` with no new `LogScript` warning (the missing key file is the only known one), and the pairing check finds no missing or extra bubble:

   ```bash
   python - Saved/Logs/T38auto.log <<'EOF'
   import re, sys
   cut, pend, ok, extra, miss = set(), None, 0, [], []
   for l in open(sys.argv[1], encoding='utf-8', errors='replace'):
       m = re.search(r'NHOS: (LINE|BUBBLE|CUT) (\S+)', l)
       if not m:
           continue
       k, i = m.groups()
       if k == 'CUT':
           cut.add(i)
       elif k == 'LINE':
           if pend: miss.append(pend)
           pend = None if i in cut else i
       elif pend == i:
           ok, pend = ok + 1, None
       else:
           extra.append(i)
   if pend: miss.append(pend)
   print(ok, 'lines with a bubble; missing:', miss, 'extra:', extra)
   EOF
   ```

   The `NHOS: LOG` lines keep their form: compare their count and their number of fields with a T30 run, as T29 did.
2. **Screenshots at 1600 × 900, chat hidden** (PIE floating window, Test for Free, autoplay off, played by hand through the Slate inspector; `line_min` raised in `pacing.json` for the run if the window is too short, then set back): a scene turn, the typing dots in Free Talk, a Free Talk line, the vote with its reasons (and the target, if P2 chose it), and the reactions after a cut. Each shows the newest line in a bubble over its speaker, and nothing above the input row. Save them to `Saved/T38/shots/`.
3. **The same scene turn with the chat shown:** click "Show chat" (`NHOS: CHAT shown` in the log); every line so far is there, newest at the bottom; on my turn the input box has the focus after the click. Click again (`NHOS: CHAT hidden`).
4. **The edge cases:** a long AI line (about 25 words) wraps and stays inside the 24-unit margin; a robot at Right keeps its bubble clear of my card; a robot on the riser or at Left near the header moves its bubble sideways or down with its tail still pointing at it; my own line's bubble shows over my robot ("You"); while the reveal stamp shows, no bubble covers it; a cut robot shows no bubble.
5. **The text:** measure the bubble's text contrast on its fill from a screenshot (4.5:1 or better), and that the speech is at least 18 pt.
6. **Set `autoplay` and `fast_lines` back to false.** Then Claude plays one show by hand (check 2's setup) and checks from screenshots that the talk can be followed from the bubbles, and that the chat opens and hides on a click. No playtest by the person.

## The design doc edit to propose (step 7)

Show these to the person; make them with the Claude Docs connector only after their OK. Read the doc's UI section first, and fit the words to its own headings and component format:

- **Layout (in-show screen):** "The chat is hidden by default. A 'Show chat' button in the input row opens it above the input row, newest line at the bottom; 'Hide chat' closes it. It stays as set until the next show. The input row, the vote row and See the results stay at the bottom left."
- **A new component, the speech bubble:** "Each line plays as a bubble over its speaker's robot, above the name label: a dark rounded panel with a ring and a pointed tail in the speaker's color, speech text in the chat's speech style, wrapping at about 420 px at 1600 × 900. States: *line* (the speech, or the action in the action style when there is no speech); *typing* (three cycling dots, before an AI's line in Free Talk and the reactions); *fading* (0.3 s, when the next line plays on another robot); *hidden* (a cut robot, a new phase, Scene Prep, the end screen). A bubble stays 24 px inside the window and clear of the header, the card, the chat, the input row, the banner and the reveal stamp, moving sideways or down while its tail points at its robot."
- **Rules tab** (only if the person thinks the turns read differently): in "The Scene & acting", "Each line shows in a bubble over the robot that says it; the full chat is one click away."

## Other risks to know

- **The top strip is crowded** (see "Sizes and space"). The fit rule keeps bubbles clear, but often by putting them on the robots' heads. That is the task's rule; screenshot every seat and the riser and record what you see for T34.
- **`EventTick` geometry is one frame old** in component mode, so a bubble over a hopping robot may trail it by a frame. Invisible at a 0.4 s hop.
- **Two bubbles can overlap for 0.3 s** while one fades. The task allows one full and one fading.
- **Many props of a widget in screen space aren't saved to placed instances** (E2). `InitBubble` sets everything at run time for that reason, so the editor's view of the robots shows no bubble, and that is fine.
- **`SetLit` bounces for 2.6 s** (T17) while a bubble stays up for the whole hold. That is T30's note for T34, unchanged here.
- **If T30 changed its plan** (for example, no `phase` cue for turn headers), the bubble may stay up across a turn change. Check that the last bubble of a turn is gone when the next turn's header shows.
