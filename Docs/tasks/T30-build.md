# T30 build sheet: the line queue

Back to [T30](T30.md) and [the plan](../Plan.md). This is prep for T30, written without the editor on 2026-11-15 at commit `a60edf8` (before T29 and T32 landed). It is a plan, not a record: nothing here was written to the editor. The draft graphs live only in this file. Once T30 writes a graph, its source goes to `Graphs/` as usual.

Sources read: `Graphs/BP_Show/*.txt`, `Graphs/BP_StageDirector/{PlayLine,PlayPart,Init,EventGraph}.txt`, `Graphs/BP_Robot/{SetLit,EventGraph,TickActs,Enq,StartAct}.txt`, `Graphs/BPC_LLMClient/{Ask,FlushLocal,Deliver,LoadConfig,Burn}.txt`, `Graphs/WBP_Stage/*.txt`, `Tools/dslpp.py`, the DSL rules in T01, the Unreal MCP rules in T05, T08, T09, T10, T17, T19, T27 and T28, and the show-loop findings in T07 to T11 and T14.

## Read this first

### What the sheet assumes (check each one before you build)

| # | Assumption | How to check | If it is wrong |
|---|---|---|---|
| A1 | **T29 is done, and its banner is one `WBP_Stage` function, `ShowBanner(Line)`.** T29's Findings list every call site in `BP_Show`. Seen in T29's uncommitted work while this sheet was written: `Graphs/WBP_Stage/ShowBanner.txt` adds each line to its own `BannerQueue`, and `NextBanner` and `FadeBanner` play them one at a time. So `cue_hold.banner` only keeps the next line from starting under a banner; it doesn't replace T29's queue. | Read `Docs/tasks/T29.md` Findings and `Graphs/WBP_Stage/`. `get_node_type_pins` on the banner function. | Use T29's real name and pins in `RunCue` and `CueBanner`. If T29 wrapped the banner in one `BP_Show` function, change only that wrapper's body to call `CueBanner`, and skip the per-site swaps. |
| A2 | **After T29, `BP_Show` calls `AddLogLine` for no game line.** Echoes (`> ...`) and hints (`(...)`) are gone; hints use the turn line or the input hint. | `find_nodes` `AddLogLine` in `BP_Show`. | A game line that is left is a screen change too. Route it as a `banner` cue, or add a `log` kind to `RunCue` that calls `AddLogLine`. |
| A3 | **T29 did not change `ActorLine`, the signature of `ShowLine(Seat, Does, Says)` or the signature of `WBP_Stage.AddChatLine(Name, Color, Action, Speech, IsMe)`.** It may have changed `ShowLine`'s body. | `read_graph_dsl` `ActorLine` and compare it with `Graphs/BP_Show/ActorLine.txt`. Read `ShowLine` fresh (E1). | Keep the design. Adjust the `Push` pins to match `AddChatLine`. |
| A4 | **Every caller calls `ActorLine` and then `ShowLine` for the same seat, with nothing between them.** Callers: `PlayTurn`, `PlayTalk`, `Tally`, `PlayReact` (T14). | `find_nodes` `ActorLine` and `ShowLine` in `BP_Show`. Each graph has the same count of each. | `StageLine` checks `Json|HasField Entry "does"`, so an empty entry plays nothing and logs no warning. A `ShowLine` with no `ActorLine` before it would replay the last entry's actions, so clear `LineEntry` at the end of `ShowLine` (set it from a `JsonObjectWrapper` variable that is never set). |
| A5 | **A component added to `BP_Show` with `add_component` shows on the `BP_Show` actor already placed in `L_Stage`.** T17 found that template property edits don't reach placed instances. T19 found that new components do show on instances placed after them. | After step 9, start PIE and run `ActorTools.get_components` on the PIE `BP_Show` actor (T05 did the same). `LinePlayer` must be listed. | Fallback without touching `L_Stage`: don't add it as a component. Give `BP_Show` an object variable `LinePlayer` of type `BPC_LinePlayer` and a function `LP()` that creates it with `Game|AddComponentbyClass (self) "/Game/NHOS/Core/BPC_LinePlayer.BPC_LinePlayer_C"` when the variable is still unset (T05 found that this returns the typed component). Every `Variables|Default|GetLinePlayer` below then becomes `CallFunction|LP`. Re-placing the actor would change `L_Stage`, which T30's Touches don't list, and it needs the map lock. |
| A6 | **Phase strings:** `"free talk"` (T08) and `"reactions"` (T10). | Read `StartFreeTalk` and `StartReactions` only if a check fails. | Fix them in `LineInfo`. |
| A7 | **`UpdatePrompt` passes the variables `PTurn` and `PHint` to `SetPrompt`.** T28's `PrepPrompt` sets them. The `CanType` value may be a variable or a direct pin from `ComputePrompt`. | E2. | See the two versions of `LinePrompt` below. |
| A8 | **T32 is done.** Its style Blueprint gives the typing line's font size and color, and `WBP_ChatLine`'s API is unchanged. | `Docs/UIStyle.md` and T32's Findings. | Use 18 pt italic gray (0.55, 0.58, 0.65) linear for the typing line, and leave the polish to T34. |
| A9 | **T24 has added no typing delay or countdown yet.** It depends on T30. | The plan. | No action. |

### Questions only the editor can settle (read these first, in this order)

Each item is one `read_graph_dsl`, `find_nodes` or `get_node_type_pins` call, or one small script. Step 1 below batches them.

- **E1 `BP_Show.ShowLine` has no source.** Read it. Find its `AddChatLine` node(s), the node that feeds each pin, and the type of the `Color` pin (`LinearColor` or `SlateColor`). The queue's `LColor` and `CurColor` take that type. If `ShowLine` is small and reads back cleanly, rewrite it as a full source and add it to `Graphs/`. A read-back hides `false` bool arguments and may print `Class|Factory|SetText` or `Class|AssetExportTask|...` for other nodes (T08, T09, T28), so check every line of it. If it doesn't read back cleanly, swap the one node (step 13).
- **E2 `BP_Show.UpdatePrompt` has no source, and its read-back is lossy** (T28). Find what feeds `SetPrompt`'s `Turn`, `Hint` and `CanType` pins, and where T28's `PrepPrompt` call sits. That decides which `LinePrompt` to use.
- **E3 Every `WBP_Stage.SetPhase` call in `BP_Show`.** `find_nodes` `SetPhase` also finds the setter of `BP_Show`'s own state variable `Phase` (`Set Phase`). **Swap only the calls whose target is `WBP_Stage`.** The state setter stays as it is: the logic needs the new phase at once.
- **E4 Every banner call** (A1).
- **E5 The vote row.** `StartCut` shows the buttons (T09: `SetVoteOptions(Names)`), and `Tally` hides the row (T09 says only "hides the vote row"). Find both nodes, and the name and type of `SetVoteOptions`' array pin.
- **E6 Every `WBP_Stage.SetStamp` call** (T09: `CutActor` sets it; `StartCut`, `StartScene` and `RestartShow` clear it).
- **E7 Every `CutActor` call** (T09: `Tally` and `DirectorCut`).
- **E8 `EndReactions`' `ScenePrep` call and `StoreClosing`'s `ShowEndScreen` call** (T10).
- **E9 `WBP_Stage.SetPassEnabled` has no source.** Read it before you rewrite it. It may also set the label's look.
- **E10 The widget tree around `ChatSize` in `WBP_Stage`** (T27: `ChatSize` (380 tall) > `BodyRow` > `LogScroll`), to place `TypingText`. Note each slot's padding first: `WrapWidgets` drops it (T28).
- **E11 How a new function gets typed inputs and outputs.** T19 used `add_function_graph`; check `describe_toolset BlueprintTools` for the call that adds parameters. The signature tables below give every type.
- **E12 Node names to confirm with `find_node_types`:** `Utilities|Time|ClearTimerbyFunctionName` (never used here before), `Class|BPCLinePlayer|<fn>` from `BP_Show`, `Class|BPShow|<fn>` from the component, and `Variables|Default|GetLinePlayer` in `BP_Show`. `Utilities|Time|SetTimerbyFunctionName :Object self` works in a component (`BPC_LLMClient.Ask`), and so does `Utilities|String|JoinStringArray` (`DrawCast`).
- **E13 How to add a TextBlock to `WBP_Stage`.** `describe_toolset UMGToolSet`. T27 and T28 used `ReplaceWidgetWithTemplate`, `WrapWidgets` and `BindToEventProperty`, but no add call is written down.

## Design

### The rule: the logic runs ahead, and the screen follows the queue

`BP_Show`'s state machine stays as it is. It still sends the asks for the next step at once, and the shared log still gets each turn's lines at once, in random order (T30 step 5). Only what reaches my screen goes through `BPC_LinePlayer`, one item at a time:

- **A line item:** the chat line appears, its robot lights up and bounces (`LightSeat` → `SetLit`), and its stage actions play (`StageLine` → `BP_StageDirector.PlayLine`). It prints `NHOS: LINE <seat id> hold=<s>`. Then the queue waits `hold` seconds. Before an AI line in Free Talk or the reactions, "<name> is typing..." shows for a random time first.
- **A cue item:** a screen change that must wait for the lines in front of it. It calls `BP_Show.RunCue(Kind, Text, Num)`. Kinds: `phase` (the header), `banner` (T29's banner), `stamp` (the reveal stamp), `votes` (show or hide the vote row), `cut` (all of `CutActor`), `prep` (all of `ScenePrep`) and `end` (all of `ShowEndScreen`). A `banner` or `stamp` cue with text holds the queue for its `cue_hold` time, so the next line doesn't play under it.

When the queue is idle and empty, a new item plays in the same frame. So any path with no lines in front of it works exactly as it does today.

**Why `cut`, `prep` and `end` defer the whole function:** they send no asks, and they change the stage itself. `CutActor` knocks the robot over and updates the cast. `ScenePrep` resets the stage and fills the card. `ShowEndScreen` covers everything. If `CutActor` ran ahead, the robot would fall while the vote lines still play, and `PlayLine` would skip its remaining actions (`IsDown`). Deferring them also bounds how far the logic runs ahead: at most to the next cut or the next Scene Prep. The reaction asks then go out after the vote lines play, which costs one unhidden ask (about 2 s) per scene.

**Why everything that touches the vote row is a cue:** in free autoplay, every vote can be in, and `Tally` can hide the row, before the last Free Talk line has played. If only the show call were cued, the hide would run first, and the row would then show and stay. So `StartCut`'s show and `Tally`'s hide are both cues, and they run in order. My pick and my reason can only happen after the row shows, so `PickVote`, `SetVotePick`, `SetVoteEnabled` and `SendHumanVote` stay immediate. A disable before the row shows is harmless.

### How the show waits for an empty queue

- **The header, banners, the stamp, the vote row, the cut, Scene Prep and the end screen** are cue items, so they wait by their place in the queue.
- **My turn:** `UpdatePrompt` runs on Event Tick (T14). A new `LinePrompt` call, after T28's `PrepPrompt`, asks `LinePlayer.IsBusy()`. While busy: `CanType` is false, the hint is "Wait for the lines to finish.", and a turn line that would invite me ("your turn") becomes "Watch the stage. Your turn comes next." The input box and Send are disabled by `SetPrompt`, as off my turn today.
- **Pass:** `NextTalker` and `NextReactor` turn Pass on for my seat as soon as my turn comes in the logic, even while lines still play. `WBP_Stage` gets a `PassOn` variable: `SetPassEnabled` stores it, and Pass is enabled only when `PassOn` and `CanType` are both true. `SetPrompt`'s `CanType` branch applies it again on every change. This is a state gate, so there is no ordering race with autoplay (which turns Pass on and off at once).
- **Optional safety:** a gate at the top of `HandleSend` that drops a send while busy. The UI gate above already blocks typing, Send, Pass and the hidden vote row, so skip it unless a check shows a leak.
- **Restart:** `RestartShow` works only in `"end"`, after the `end` cue, so the queue is empty by then. One `LinePlayer.Clear` call at its start is optional safety.

### What stays immediate

The shared log (`ActorLine`), every `NHOS: LOG`, `TURN ... DONE`, `FREETALK DONE`, `TALLY`, `REACTIONS DONE` print, every ask, every state variable (`Phase`, `TalkSeat`, `HumanSent`, ...), `SetUnavailable` (an error shows at once), `ShowTitle`, the stamp and vote-row clears in `StartScene` (nothing is queued by then), and `StartScene`'s `LightSeat(-1)`. `NHOS: CUT` and `NHOS: SHOW END` now print when their cue plays, later than before.

### Timing without blocking

The component has no tick and no `Delay` node. Each wait is `Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "<fn>" :Time t :bLooping false` on the component, as `BPC_LLMClient.Ask` does for `FlushLocal`. `PlayCur` runs after the typing wait, and `Pump` after the hold. Only one of the two timers is ever pending. **A timer with a time of 0 or less never fires**, so `Scaled` clamps every wait to 0.01 s or more (`fast_lines` × a 0 value would otherwise stall the queue).

`Busy` is true from the first item until `Pump` finds the queue empty after the last hold. So the last line also gets its full reading time before the header or my turn changes.

### Hooks for later tasks

- **T38:** call `Say` on the seat's robot in `PlayCur`, next to `AddChatLine`. The typing line's call is in `Pump`'s typing branch, and `ClearTyping` and `PlayCur` clear it.
- **T20:** the talk blip goes in `PlayCur`. `ShowLine` stays the only way a line gets in (T30 step 5), and `PlayCur` is the moment it reaches the screen.
- **T37:** an error note on the banner goes through `CueBanner`, so it waits its turn.
- **T24:** a countdown on my input starts when `IsBusy` turns false on my turn, not when the logic reaches my turn.

## `BPC_LinePlayer` (new ActorComponent Blueprint, `/Game/NHOS/Core/BPC_LinePlayer`)

### Variables

| Name | Type | Default | Use |
|---|---|---|---|
| `Loaded` | bool | false | `LoadPacing` has run. |
| `Fast` | bool | false | `fast_lines` from `Local/switches.json`. |
| `LineBase`, `LinePerWord`, `LineMin`, `LineMax` | float | 1.2, 0.25, 2.0, 5.0 | Hold = clamp(`LineBase` + `LinePerWord` × words, `LineMin`, `LineMax`). |
| `TypeMin`, `TypeMax` | float | 0.6, 1.6 | The typing wait's range. |
| `FastScale` | float | 0.1 | The multiplier for every wait when `Fast` is on. |
| `Pace`, `CueHold` | JsonObjectWrapper | | The `pacing` block, and its `cue_hold` object. |
| `TmpF` | float | | A typed target for `Json|GetField` (T01: a wildcard output needs a typed setter). |
| `TmpStr` | string | | A typed source for `Utilities|Array|Add` (no graph here adds a literal to an array; don't rely on it). |
| `Busy` | bool | false | An item is playing or holding. |
| `Show` | BP_Show object ref | | Found once with `GetActorOfClass`. |
| `NullShow` | BP_Show object ref | never set | For the validity check (T19: `Utilities|IsValid` in an expression becomes the exec macro). |
| `Stage` | WBP_Stage object ref | | From `Push`. |
| `NullStage` | WBP_Stage object ref | never set | As `NullShow`. |
| `QKind` | string array | | The order of all items: `"line"` or a cue kind. |
| `LSeat` (int), `LName` (string), `LColor` (E1's type), `LAction` (string), `LSpeech` (string), `LIsMe` (bool), `LEntry` (JsonObjectWrapper), `LId` (string), `LTyping` (bool) | arrays | | The line items, first in, first out. |
| `CText` (string), `CNum` (int) | arrays | | The cue items, first in, first out. |
| `CurKind`, `CurName`, `CurAction`, `CurSpeech`, `CurId`, `CurText` (string); `CurSeat`, `CurNum` (int); `CurColor` (E1's type); `CurIsMe`, `CurTyping` (bool); `CurEntry` (JsonObjectWrapper) | | | The item being played. |

`QKind` holds the order, and the line and cue arrays each stay first in, first out. A pop takes index 0 of the array that `QKind[0]` names, so no item needs filler values. As in `BP_Robot.TickActs`, read every field of item 0 into the `Cur` variables before any `RemoveIndex` (T07: a pure `Get` runs again after each `RemoveIndex`).

### Functions (all impure, made with `add_function_graph`; bind each result before an `if`, `return` or `select` uses it, as T19 found)

| Function | Inputs | Outputs | Called by |
|---|---|---|---|
| `LoadPacing` | | | `Push`, `Cue` (once) |
| `Scaled` | `T` float | float | `Pump`, `PlayCur`, `CueHoldFor` |
| `FindShow` | | | `Push`, `Cue` |
| `IsBusy` | | bool | `BP_Show.LinePrompt` |
| `Push` | `StageW` WBP_Stage ref, `Seat` int, `Name` string, `Color` (E1), `Action` string, `Speech` string, `IsMe` bool, `Entry` JsonObjectWrapper | | `BP_Show.ShowLine` |
| `Cue` | `Kind` string, `Text` string, `Num` int | | `BP_Show.Cue*` |
| `Pump` | | | itself, `Push`, `Cue`, the timer |
| `PlayCur` | | | `Pump`, the timer |
| `CueHoldFor` | `Kind` string, `Text` string | float | `Pump` |
| `ClearTyping` | | | `Pump`, `Clear` |
| `Clear` | | | `BP_Show.RestartShow` (optional) |

`BP_Show` calls the component, and the component calls `BP_Show` and `WBP_Stage`. Blueprints that reference each other already work here (`BP_Show` and `WBP_Stage`). Make every signature in both Blueprints first, compile, then write the bodies (steps 7 to 12).

### Draft sources (shorthand; expand each with `Tools/dslpp.py`, one `;;; GRAPH <Name>` header per graph)

```lisp
;;; GRAPH LoadPacing
(fn LoadPacing ()
  (set Loaded true)
  (set LineBase 1.2)
  (set LinePerWord 0.25)
  (set LineMin 2.0)
  (set LineMax 5.0)
  (set TypeMin 0.6)
  (set TypeMax 1.6)
  (set FastScale 0.1)
  (set Fast false)
  (bind _empty (Json|LoadJsonfromString "{}"))
  (set CueHold _empty)
  (bind _cdir (Utilities|Paths|GetProjectContentDirectory))
  (bind (_o _ok) (Json|LoadJsonfromFile (Utilities|Struct|MakeFilePath (cat _cdir "NHOS/Data/pacing.json"))))
  (if _ok
    (bind _hp (Json|HasField _o "pacing"))
    (if _hp
      (bind _p (Json|GetField _o "pacing"))
      (set Pace _p)
      (bind _f1 (Json|GetField (V Pace) "line_base"))
      (set LineBase _f1)
      (bind _f2 (Json|GetField (V Pace) "line_per_word"))
      (set LinePerWord _f2)
      (bind _f3 (Json|GetField (V Pace) "line_min"))
      (set LineMin _f3)
      (bind _f4 (Json|GetField (V Pace) "line_max"))
      (set LineMax _f4)
      (bind _f5 (Json|GetField (V Pace) "typing_min"))
      (set TypeMin _f5)
      (bind _f6 (Json|GetField (V Pace) "typing_max"))
      (set TypeMax _f6)
      (bind _f7 (Json|GetField (V Pace) "fast_scale"))
      (set FastScale _f7)
      (bind _f8 (Json|GetField (V Pace) "cue_hold"))
      (set CueHold _f8)))
  (bind _dir (Utilities|Paths|GetProjectDirectory))
  (bind (_so _sok) (Json|LoadJsonfromFile (Utilities|Struct|MakeFilePath (cat _dir "Local/switches.json"))))
  (if _sok
    (bind _hf (Json|HasField _so "fast_lines"))
    (if _hf
      (bind _sf (Json|GetField _so "fast_lines"))
      (set Fast _sf)))
  (print (cat "NHOS: PACING file=" (Utilities|String|ToString(Boolean) _ok) " fast_lines=" (Utilities|String|ToString(Boolean) (V Fast)))))

;;; GRAPH Scaled
(fn Scaled (T)
  (bind _s (select (V Fast) (* T (V FastScale)) T))
  (return (select (< _s 0.01) 0.01 _s)))

;;; GRAPH FindShow
(fn FindShow ()
  (if (== (V Show) (V NullShow))
    (bind _s (Actor|GetActorOfClass :ActorClass "/Game/NHOS/Core/BP_Show.BP_Show_C"))
    (set Show _s)))

;;; GRAPH IsBusy
(fn IsBusy ()
  (return (or (V Busy) (> (len (V QKind)) 0))))

;;; GRAPH Push
(fn Push (StageW Seat Name Color Action Speech IsMe Entry)
  (if (not (V Loaded))
    (CallFunction|LoadPacing))
  (CallFunction|FindShow)
  (set Stage StageW)
  (bind (_id _ty) (Class|BPShow|LineInfo :self (V Show) :Seat Seat :IsMe IsMe))
  (set TmpStr "line")
  (add (V QKind) (V TmpStr))
  (add (V LSeat) Seat)
  (add (V LName) Name)
  (add (V LColor) Color)
  (add (V LAction) Action)
  (add (V LSpeech) Speech)
  (add (V LIsMe) IsMe)
  (add (V LEntry) Entry)
  (add (V LId) _id)
  (add (V LTyping) _ty)
  (if (not (V Busy))
    (CallFunction|Pump)))

;;; GRAPH Cue
(fn Cue (Kind Text Num)
  (if (not (V Loaded))
    (CallFunction|LoadPacing))
  (CallFunction|FindShow)
  (add (V QKind) Kind)
  (add (V CText) Text)
  (add (V CNum) Num)
  (if (not (V Busy))
    (CallFunction|Pump)))

;;; GRAPH CueHoldFor
(fn CueHoldFor (Kind Text)
  (if (Utilities|String|IsEmpty Text)
    (return 0.0))
  (bind _h (Json|HasField (V CueHold) Kind))
  (if (not _h)
    (return 0.0))
  (bind _v (Json|GetField (V CueHold) Kind))
  (set TmpF _v)
  (if (<= (V TmpF) 0.0)
    (return 0.0))
  (bind _s (CallFunction|Scaled :T (V TmpF)))
  (return _s))

;;; GRAPH ClearTyping
(fn ClearTyping ()
  (if (!= (V Stage) (V NullStage))
    (Class|WBPStage|SetTyping :self (V Stage) :Line "")))

;;; GRAPH Pump
(fn Pump ()
  (if (== (len (V QKind)) 0)
    (set Busy false)
    (CallFunction|ClearTyping)
    (return))
  (set Busy true)
  (set CurKind (get (V QKind) 0))
  (Utilities|Array|RemoveIndex (V QKind) 0)
  (if (not (streq (V CurKind) "line"))
    (set CurText (get (V CText) 0))
    (set CurNum (get (V CNum) 0))
    (Utilities|Array|RemoveIndex (V CText) 0)
    (Utilities|Array|RemoveIndex (V CNum) 0)
    (bind _h (CallFunction|CueHoldFor :Kind (V CurKind) :Text (V CurText)))
    (print (cat "NHOS: CUE " (V CurKind) " " (V CurText)))
    (Class|BPShow|RunCue :self (V Show) :Kind (V CurKind) :Text (V CurText) :Num (V CurNum))
    (if (> _h 0.0)
      (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "Pump" :Time _h :bLooping false)
      (return))
    (CallFunction|Pump)
    (return))
  (set CurSeat (get (V LSeat) 0))
  (set CurName (get (V LName) 0))
  (set CurColor (get (V LColor) 0))
  (set CurAction (get (V LAction) 0))
  (set CurSpeech (get (V LSpeech) 0))
  (set CurIsMe (get (V LIsMe) 0))
  (set CurEntry (get (V LEntry) 0))
  (set CurId (get (V LId) 0))
  (set CurTyping (get (V LTyping) 0))
  (Utilities|Array|RemoveIndex (V LSeat) 0)
  (Utilities|Array|RemoveIndex (V LName) 0)
  (Utilities|Array|RemoveIndex (V LColor) 0)
  (Utilities|Array|RemoveIndex (V LAction) 0)
  (Utilities|Array|RemoveIndex (V LSpeech) 0)
  (Utilities|Array|RemoveIndex (V LIsMe) 0)
  (Utilities|Array|RemoveIndex (V LEntry) 0)
  (Utilities|Array|RemoveIndex (V LId) 0)
  (Utilities|Array|RemoveIndex (V LTyping) 0)
  (if (V CurTyping)
    (Class|WBPStage|SetTyping :self (V Stage) :Line (cat (V CurName) " is typing..."))
    (bind _t (CallFunction|Scaled :T (Math|Random|RandomFloatinRange :Min (V TypeMin) :Max (V TypeMax))))
    (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "PlayCur" :Time _t :bLooping false)
    (return))
  (CallFunction|PlayCur))

;;; GRAPH PlayCur
(fn PlayCur ()
  (Class|WBPStage|SetTyping :self (V Stage) :Line "")
  (bind _wa (len (Utilities|String|ParseIntoArray :SourceString (V CurAction) :Delimiter " " :CullEmptyStrings true)))
  (bind _ws (len (Utilities|String|ParseIntoArray :SourceString (V CurSpeech) :Delimiter " " :CullEmptyStrings true)))
  (bind _raw (+ (V LineBase) (* (V LinePerWord) (+ _wa _ws))))
  (bind _hold (CallFunction|Scaled :T (Math|Float|Clamp(Float) :Value _raw :Min (V LineMin) :Max (V LineMax))))
  (print (cat "NHOS: LINE " (V CurId) " hold=" (Utilities|String|ToString(Float) _hold)))
  (Class|WBPStage|AddChatLine :self (V Stage) :Name (V CurName) :Color (V CurColor) :Action (V CurAction) :Speech (V CurSpeech) :IsMe (V CurIsMe))
  (Class|BPShow|LightSeat :self (V Show) :Seat (V CurSeat))
  (Class|BPShow|StageLine :self (V Show) :Seat (V CurSeat) :Entry (V CurEntry))
  (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "Pump" :Time _hold :bLooping false))

;;; GRAPH Clear
(fn Clear ()
  (Utilities|Time|ClearTimerbyFunctionName :Object self :FunctionName "Pump")
  (Utilities|Time|ClearTimerbyFunctionName :Object self :FunctionName "PlayCur")
  (clear (V QKind))
  (clear (V LSeat))
  (clear (V LName))
  (clear (V LColor))
  (clear (V LAction))
  (clear (V LSpeech))
  (clear (V LIsMe))
  (clear (V LEntry))
  (clear (V LId))
  (clear (V LTyping))
  (clear (V CText))
  (clear (V CNum))
  (set Busy false)
  (CallFunction|ClearTyping))
```

Notes on the drafts:

- **The DSL rules they follow:** an `if` whose body ends in `return` makes the rest its else branch, and one without joins the code after it (T01). Strings compare with `streq` (T01). Objects compare with a never-set variable, not `Utilities|IsValid` (T19). A chain of `if` with `return` replaces `switch` (T19). Results of impure calls are bound before use (T19). `Utilities|String|Split`-style multiple outputs bind as `(bind (a b) ...)` (T19, `StartShowSession`). `Class|...` calls on another Blueprint pass `:self` by name (T01). `print` expands to `Development|PrintString ... false`.
- **Recursion:** `Pump` calls itself after a cue with no hold. The depth is the number of cues in a row with no hold, at most about 5. A cue's `RunCue` may call `Push` or `Cue` (for example `CutActor` → `CueHeader`, or a failed ask inside `Ask` → `PlayReact` → `ShowLine`). `Busy` is true then, so they only append. They never touch the `Cur` variables, and `Pump` reads `_h` before `RunCue` runs.
- **`(* (V LinePerWord) (+ _wa _ws))`** mixes a float and an int. `BP_Robot.StartAct` does the same (`(* 0.5 (len (V QVerb)))`), so it compiles.
- **If `ClearTimerbyFunctionName` has another name** (E12), use it. `Clear` is only for `RestartShow`, so it may also be skipped.

## `BP_Show` changes

### New variable and component

- Component `LinePlayer` (`BPC_LinePlayer`), added with `ActorTools.add_component` on the Blueprint asset (T11). Check A5.
- Variable `LineEntry` (JsonObjectWrapper): the last entry `ActorLine` added.
- Variable `NoEntry` (JsonObjectWrapper), never set: only if A4 fails.

### New functions (sources to add to `Graphs/BP_Show/` once written)

| Function | Inputs | Outputs |
|---|---|---|
| `StageLine` | `Seat` int, `Entry` JsonObjectWrapper | |
| `LineInfo` | `Seat` int, `IsMe` bool | `Id` string, `Typing` bool |
| `RunCue` | `Kind` string, `Text` string, `Num` int | |
| `CueHeader`, `CueBanner`, `CueStamp` | `Text` string | |
| `CueVotes` | `Names` string array (E5's type) | |
| `CueCut` | `Seat` int | |
| `CuePrep`, `CueEnd` | | |
| `LinePrompt` | (version B only: `CanIn` bool) | (version B only: `CanOut` bool) |

```lisp
;;; GRAPH StageLine
; The director call moved from ActorLine, unchanged, behind a check that the entry has "does".
(fn StageLine (Seat Entry)
  (bind _hd (Json|HasField Entry "does"))
  (if (not _hd)
    (return))
  (bind _dir (Actor|GetActorOfClass :ActorClass "/Game/NHOS/Stage/BP_StageDirector.BP_StageDirector_C"))
  (Utilities|IsValid _dir
    (:"Is Valid"
      (Class|BPStageDirector|PlayLine :self _dir :Seat Seat :Entry Entry :Robots (Variables|Default|GetRobots) :SeatNames (Variables|Default|GetSeatName) :Ids (Variables|Default|GetSeatId)))
    (:"Is Not Valid")))

;;; GRAPH LineInfo
(fn LineInfo (Seat IsMe)
  (bind _id (Utilities|Array|Get(acopy) (Variables|Default|GetSeatId) Seat))
  (bind _chat (or (Utilities|String|EqualExactly(String) (Variables|Default|GetPhase) "free talk") (Utilities|String|EqualExactly(String) (Variables|Default|GetPhase) "reactions")))
  (return _id (and _chat (not IsMe))))

;;; GRAPH RunCue
(fn RunCue (Kind Text Num)
  (if (Utilities|String|EqualExactly(String) Kind "phase")
    (Class|WBPStage|SetPhase :self (Variables|Default|GetStage) :Phase Text)
    (return))
  (if (Utilities|String|EqualExactly(String) Kind "banner")
    (Class|WBPStage|ShowBanner :self (Variables|Default|GetStage) :Line Text)
    (return))
  (if (Utilities|String|EqualExactly(String) Kind "stamp")
    (Class|WBPStage|SetStamp :self (Variables|Default|GetStage) :Stamp Text)
    (return))
  (if (Utilities|String|EqualExactly(String) Kind "votes")
    (bind _names (Utilities|String|ParseIntoArray :SourceString Text :Delimiter "|" :CullEmptyStrings true))
    (Class|WBPStage|SetVoteOptions :self (Variables|Default|GetStage) :Names _names)
    (return))
  (if (Utilities|String|EqualExactly(String) Kind "cut")
    (CallFunction|CutActor :Seat Num)
    (return))
  (if (Utilities|String|EqualExactly(String) Kind "prep")
    (CallFunction|ScenePrep)
    (return))
  (if (Utilities|String|EqualExactly(String) Kind "end")
    (CallFunction|ShowEndScreen)
    (return))
  (Development|PrintString (Utilities|String|Append "NHOS: CUE unknown " Kind) false))

;;; GRAPH CueHeader
(fn CueHeader (Text)
  (Class|BPCLinePlayer|Cue :self (Variables|Default|GetLinePlayer) :Kind "phase" :Text Text :Num 0))

;;; GRAPH CueBanner
(fn CueBanner (Text)
  (Class|BPCLinePlayer|Cue :self (Variables|Default|GetLinePlayer) :Kind "banner" :Text Text :Num 0))

;;; GRAPH CueStamp
(fn CueStamp (Text)
  (Class|BPCLinePlayer|Cue :self (Variables|Default|GetLinePlayer) :Kind "stamp" :Text Text :Num 0))

;;; GRAPH CueVotes
; An empty list hides the row (T09: SetVoteOptions hides the row for an empty list).
(fn CueVotes (Names)
  (Class|BPCLinePlayer|Cue :self (Variables|Default|GetLinePlayer) :Kind "votes" :Text (Utilities|String|JoinStringArray Names "|") :Num 0))

;;; GRAPH CueCut
(fn CueCut (Seat)
  (Class|BPCLinePlayer|Cue :self (Variables|Default|GetLinePlayer) :Kind "cut" :Text "cut" :Num Seat))

;;; GRAPH CuePrep
(fn CuePrep ()
  (Class|BPCLinePlayer|Cue :self (Variables|Default|GetLinePlayer) :Kind "prep" :Text "prep" :Num 0))

;;; GRAPH CueEnd
(fn CueEnd ()
  (Class|BPCLinePlayer|Cue :self (Variables|Default|GetLinePlayer) :Kind "end" :Text "end" :Num 0))

;;; GRAPH LinePrompt
; Version A, when CanType reaches SetPrompt from a variable (named PCan here; use E2's real name).
(fn LinePrompt ()
  (bind _busy (Class|BPCLinePlayer|IsBusy :self (Variables|Default|GetLinePlayer)))
  (if (not _busy)
    (return))
  (if (Variables|Default|GetPCan)
    (Variables|Default|SetPTurn "Watch the stage. Your turn comes next."))
  (Variables|Default|SetPHint "Wait for the lines to finish.")
  (Variables|Default|SetPCan false))
```

**`LinePrompt` version B,** when `ComputePrompt`'s `CanType` output is wired straight into `SetPrompt`: give it the input `CanIn` and the output `CanOut`, and put it in that data path as well as on the exec line.

```lisp
;;; GRAPH LinePrompt
(fn LinePrompt (CanIn)
  (bind _busy (Class|BPCLinePlayer|IsBusy :self (Variables|Default|GetLinePlayer)))
  (if (not _busy)
    (return CanIn))
  (if CanIn
    (Variables|Default|SetPTurn "Watch the stage. Your turn comes next."))
  (Variables|Default|SetPHint "Wait for the lines to finish.")
  (return false))
```

`ShowBanner :Line` is from T29's draft source (A1), and `SetVoteOptions :Names` is a placeholder until E5 gives the real name. Write `SetPhase` as `Class|WBPStage|SetPhase :self ... :Phase ...` (T08: its read-back looks like `Variables|Default|SetPhase`). The literal `"phase"` in `CueHeader` goes into a typed string input, not a wildcard pin, so T01's literal rule doesn't apply.

### Existing graphs that change

| Graph | Has a source? | Change |
|---|---|---|
| `ActorLine` | yes | Full rewrite, below. `LightSeat` and the director call leave it: they move to the moment the line plays. |
| `ShowLine` | no (E1) | Replace the `AddChatLine` node with `LinePlayer.Push`. Connect the same sources to `Name`, `Color`, `Action`, `Speech` and `IsMe`, the old `self` source (the `Stage` getter) to `StageW`, the function's `Seat` input to `Seat`, and a new `LineEntry` getter to `Entry`. The exec links stay the same. If `ShowLine` has two `AddChatLine` nodes (for example one for "stands still" hidden), swap both. Nothing else in `ShowLine` changes. |
| `UpdatePrompt` | no (E2) | Insert `CallFunction\|LinePrompt` after `PrepPrompt` and before `SetPrompt`: `break_pins` the exec link, `create_node`, `connect_pins` (T28's recipe). Version B also goes in the `CanType` data link. |
| every graph with a `WBP_Stage.SetPhase` call (E3), except `ShowTitle` and the `SetUnavailable` path | no (except `ShowTitle`) | Replace each with `CallFunction\|CueHeader`: exec in, exec out, and the `Phase` source to `Text`. Expect `StartTurn`, `EndScene`, `StartTalkRound`, `EndFreeTalk`, `StartCut`, `CutActor`, `AskDirector`, `EndShow` and any T29 added. |
| every graph with a banner call (E4, A1) | per T29 | Replace each with `CallFunction\|CueBanner`, same pins. Expect `StartScene`, `Tally` (the tie), `DirectorCut`, `CutActor`, `EndReactions`. |
| every graph with a `WBP_Stage.SetStamp` call (E6) | no | Replace each with `CallFunction\|CueStamp`. A clear (`""`) holds nothing, so swapping the clears is harmless and keeps the rule simple. |
| `StartCut` | no | Replace `SetVoteOptions(Names)` with `CallFunction\|CueVotes`, with the same `Names` source. `SetVoteEnabled` stays. |
| `Tally` | no | Replace the vote-row hide (E5) with `CallFunction\|CueVotes` and an empty `Names` (a `Utilities\|Array\|MakeArray` with no items, or a never-set string array variable `NoNames`). Replace the `CutActor` call with `CallFunction\|CueCut`, with the same `Seat` source. |
| `DirectorCut` | no | Replace the `CutActor` call with `CallFunction\|CueCut`. |
| `EndReactions` | no | Replace the `ScenePrep` call with `CallFunction\|CuePrep`. |
| `StoreClosing` | no | Replace the `ShowEndScreen` call with `CallFunction\|CueEnd`. |
| `RestartShow` | no | Optional: insert `Class\|BPCLinePlayer\|Clear` on `LinePlayer` as its first call. |

```lisp
;;; GRAPH ActorLine
(fn ActorLine (Seat Entry)
  (Utilities|Array|Add (Variables|Default|GetSharedLog) Entry)
  (Variables|Default|SetLineEntry Entry))
```

`Seat` stays in `ActorLine`'s signature, so its callers don't change.

**One node swap** (T28): `find_nodes` the old call (the title without spaces: `SetPhase`, not `Set Phase`), note the node that feeds each pin and the nodes on its `then` and `execute` links, `delete_node`, `create_node` `CallFunction|<New>`, then `connect_pins` for the exec in (from the previous node's `then`, index 0), the exec out, and each data pin. Do all the swaps in one graph in one `execute_tool_script` call, and keep each call under about 60 s (T09, T10).

## `WBP_Stage` changes

- **New `TypingText`** (TextBlock, 18 pt italic, gray (0.55, 0.58, 0.65) linear or T32's style, one line, ellipsis when too long). Put it inside `ChatSize`, under `LogScroll`: wrap `LogScroll` in a VerticalBox (`LogScroll` fills, `TypingText` is auto height), so the panel keeps its 380 px and the robots stay clear of it (T27). Its visibility is `Hidden`, not `Collapsed`, when empty, so the chat doesn't jump each time it shows. E10 first.
- **New variable `PassOn`** (bool, false).
- **New `SetTyping(Line)`**, rewritten `SetPassEnabled(Enabled)` (E9 first: keep any label change it makes) and one new line in `SetPrompt`'s `CanType` branch.

```lisp
;;; GRAPH SetTyping
(fn SetTyping (Line)
  (Class|Text|SetText :self (Variables|WBP_Stage|GetTypingText) :Text (Utilities|Text|ToText(String) Line))
  (if (Utilities|String|IsEmpty Line)
    (Widget|SetVisibility :self (Variables|WBP_Stage|GetTypingText) :InVisibility "Hidden")
    (else
      (Widget|SetVisibility :self (Variables|WBP_Stage|GetTypingText) :InVisibility "HitTestInvisible"))))

;;; GRAPH SetPassEnabled
(fn SetPassEnabled (Enabled)
  (Variables|Default|SetPassOn Enabled)
  (Widget|SetIsEnabled :self (Variables|WBP_Stage|GetPassButton) :bInIsEnabled (and Enabled (Variables|Default|GetLastCanType))))
```

`SetTyping` uses an `if` with two `SetVisibility` calls, as `SetPrepMode` does, because enum pins take quoted value names (T09) and no graph here passes one through `select`.

`SetPrompt` (has a source, `Graphs/WBP_Stage/SetPrompt.txt`): add one line at the end of the `xor` branch, after the `TurnText` color line and before the focus `if`:

```lisp
    (Widget|SetIsEnabled :self (Variables|WBP_Stage|GetPassButton) :bInIsEnabled (and CanType (Variables|Default|GetPassOn)))
```

## Data

### `Content/NHOS/Data/pacing.json` (new)

`DefaultGame.ini` stages all of `NHOS/Data` as loose files, so the new file ships without a config change.

```json
{
	"_readme": "Line pacing (T30). BPC_LinePlayer reads it at the first line of a run. Each line on my screen holds for line_base + line_per_word x its words (action and speech), kept between line_min and line_max, before the next line plays. Before an AI line in Free Talk and the reactions, '<name> is typing...' shows for a random time between typing_min and typing_max. cue_hold: how long the queue waits after a screen change of that kind with text (a reveal stamp, a banner), so the next line doesn't play under it; a kind that isn't listed waits 0. fast_scale multiplies every wait when fast_lines is on in Local/switches.json, for autoplay checks. Every time is in seconds.",
	"pacing": {
		"line_base": 1.2,
		"line_per_word": 0.25,
		"line_min": 2.0,
		"line_max": 5.0,
		"typing_min": 0.6,
		"typing_max": 1.6,
		"fast_scale": 0.1,
		"cue_hold": {
			"banner": 2.0,
			"stamp": 2.5
		}
	}
}
```

At these values a scene turn of five lines takes about 15 to 25 s, and a two-scene free autoplay show about 4 to 6 minutes. `Tools/check_prompts.py --offline` doesn't read this file. A check for it would add `Tools/check_prompts.py` to T30's Touches, and T37 also changes that file, so leave it out unless the plan agrees.

### `fast_lines`

- `Docs/switches.example.json`: add `"fast_lines": false` after `"burn_test": false`, and add this sentence at the end of `_readme`: `fast_lines: cuts every wait of the line queue (Content/NHOS/Data/pacing.json) to a tenth, so an autoplay check runs fast. It is read at the first line of a run. Set it back to false before a person plays.`
- `Local/switches.json`: add the same field (git ignores it).

## Editor steps in order (each one Unreal MCP call, or one short script)

Before step 1: `git pull`, read `Agents/`, `git lfs locks`, claim T30, lock `Content/NHOS/Core/BP_Show.uasset` and `Content/NHOS/UI/WBP_Stage.uasset`, write the status file with `Editor: driving`, and call `get_execution_environment` once (T01). `AssetTools.read_file` reads only under `Content/` and `Saved/` (T28), so copy the expanded sources to `Saved/T30/src/` first.

1. **Read (one script):** `read_graph_dsl` `ShowLine` (E1) and `UpdatePrompt` (E2).
2. **Find (one script):** in `BP_Show`, `find_nodes` `SetPhase`, `SetStamp`, `SetVoteOptions`, `CutActor`, `ScenePrep`, `ShowEndScreen`, the banner function, `AddLogLine`, `ActorLine` and `ShowLine`. For each node, record the graph, the node id, the target class and the linked pins. Save the list to `Saved/T30/sites.json`. Settles E3 to E8, A2 and A4.
3. **Read `WBP_Stage` (one script):** `read_graph_dsl` `SetPassEnabled` (E9), and the widget tree under `ChatSize` with each slot's padding (E10).
4. **Node names (one script):** `find_node_types` and `get_node_type_pins` for `AddChatLine` (the `Color` type), `SetVoteOptions`, the banner function, `ClearTimerbyFunctionName`, and `describe_toolset` `BlueprintTools` and `UMGToolSet` for E11 and E13.
5. **Files (no MCP):** write `pacing.json`, edit `Docs/switches.example.json` and `Local/switches.json`. Confirm the editor's Auto Reimport prompt doesn't block (T08 saw it for a JSON edit).
6. **`WBP_Stage` layout:** wrap `LogScroll` in a VerticalBox, add `TypingText`, set the paddings back. Compile.
7. **`WBP_Stage` graphs:** add `PassOn`, the `SetTyping` signature, write `SetTyping`, `SetPassEnabled` and `SetPrompt`. Compile, save.
8. **`BPC_LinePlayer`:** create the ActorComponent Blueprint in `/Game/NHOS/Core`, add every variable, and add every function's signature with an empty body. Compile, save.
9. **`BP_Show` setup:** add the `LinePlayer` component, the `LineEntry` variable and every new function's signature with an empty body. Compile, save. Check A5 in PIE now (start PIE, `get_components`, stop PIE).
10. **`BPC_LinePlayer` bodies, batch 1:** `LoadPacing`, `Scaled`, `FindShow`, `IsBusy`, `ClearTyping`, `CueHoldFor`.
11. **Batch 2:** `Push`, `Cue`, `Clear`.
12. **Batch 3:** `Pump`, `PlayCur`. Compile `BPC_LinePlayer`, save.
13. **`BP_Show` bodies, batch 1:** `StageLine`, `LineInfo`, `RunCue`.
14. **Batch 2:** the seven `Cue*` wrappers and `LinePrompt`. Compile, save.
15. **`ActorLine`:** write the new source.
16. **`ShowLine`:** the `Push` swap (or a full source, if E1 allows).
17. **`UpdatePrompt`:** insert `LinePrompt`.
18. **Swaps, part 1:** the `SetPhase` sites, grouped by graph, a few graphs per script.
19. **Swaps, part 2:** the banner and `SetStamp` sites.
20. **Swaps, part 3:** `StartCut`, `Tally`, `DirectorCut`, `EndReactions`, `StoreClosing` (and `RestartShow` if chosen).
21. **Compile and save all.** Read the editor log for `LogBlueprint` errors. Compiling `BP_Show` may mark `L_Stage` and `BPC_LLMClient` dirty with no change (T08, T10): leave them unsaved.
22. **The checks below.** Then the `Graphs/` files, the findings, and the commit, with a `Waiting:` line only if the doc edit still waits for my OK ("When only my check is left" in the plan).

## Checks (the Done-when)

1. **Free autoplay with `fast_lines`:** set `autoplay: true`, `mode: free`, `fast_lines: true` in `Local/switches.json`. Run a game window with `-log=T30fast.log` in the background. It must reach `NHOS: SHOW END`, with a `NHOS: PACING ... fast_lines=true` line, `NHOS: LINE` lines, and no `LogScript` warning except the missing key file. One `NHOS: CUE cut` must come before each `NHOS: CUT`. `spare_human: true` makes it play scene 2 and Scene Prep too.
2. **Free autoplay without `fast_lines`:** the same with `fast_lines: false` and `-log=T30slow.log`. Every two `NHOS: LINE` lines in a row are at least 1 s apart. `line_min` is 2.0 s, so every gap should be 2 s or more. Check it from the log's timestamps:

   ```bash
   python -c "import re,sys,datetime as d;t=[d.datetime.strptime(m.group(1),'%Y.%m.%d-%H.%M.%S:%f') for m in (re.match(r'\[(\d{4}\.\d\d\.\d\d-\d\d\.\d\d\.\d\d:\d{3})\].*NHOS: LINE ',l) for l in open(sys.argv[1],encoding='utf-8',errors='replace')) if m];g=[(b-a).total_seconds() for a,b in zip(t,t[1:])];print(len(t),'lines, smallest gap',min(g))" Saved/Logs/T30slow.log
   ```

3. **Screenshot:** PIE in a 1600 × 900 floating window, Test for Free, autoplay off, played by hand with the Slate inspector (T27, T28). Take it during an AI line of a scene turn: one robot lit and bouncing, maybe moving, and its line the newest in the chat. To widen the window for the shot, set `line_min` to 6.0 in `pacing.json` for that run, then set it back. Also take one shot of "<name> is typing..." in Free Talk. Save to `Saved/T30/shots/`.
4. **The order on screen:** in check 2's log, the `NHOS: CUE phase` for a turn header comes after the last `NHOS: LINE` of the turn before it. Each `NHOS: CUE votes <names>` comes after the last Free Talk `LINE`, and `NHOS: CUE prep` and `NHOS: CUE end` come after the last reaction `LINE`.
5. **Set `autoplay` and `fast_lines` back to false.** Then Claude plays one show by hand (check 3's setup) and checks from screenshots that the lines are easy to follow. No playtest by the person.

## The design doc edit to propose (step 6)

Show this to the person. Make it with the Claude Docs connector only after their OK:

- Rules tab, "The Scene & acting", a new bullet: "Each turn's lines play out on stage one at a time, in a random order. The speaker's robot lights up and acts while its line appears in the chat, and the next line waits until it has been read. In Free Talk and the reactions, '<name> is typing...' shows before each AI line. The header, the vote and your next turn come once the last line has played."

## Other risks to know

- **The logic runs ahead in free mode.** The `NHOS: SCENE n TURN t DONE` and `FREETALK DONE` lines print long before their lines play. That is expected. Read the order on screen from the `LINE` and `CUE` lines.
- **`SetUnavailable` mid-show** writes the header at once, and a later cued header could cover it. T37 owns the error paths. It should send its notes through `CueBanner`, and decide whether an unavailable screen clears the queue (`Clear`).
- **`SetLit` bounces for 2.6 s** (T17), and a hold can be up to 5 s. The robot stays lit but stops bouncing before the next line. Leave it (`BP_Robot` isn't in T30's Touches), or note it for T34.
- **The typing line shows only at play time,** not while an ask is out. If Free Talk feels slow with real providers, an option is to show it from `NextTalker` while the queue is idle and an AI's ask is out.
