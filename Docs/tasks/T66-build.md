# T66 build sheet: the turn timer, the auto-send and the other phases

Back to [T66](T66.md). A Mac prep session wrote this on 2026-11-15, without the editor, against **`noHumansOnSet` at `42a917c`** (the T65 sheet, T67's part 1 and the T71 prep on top of `944978c`). It is a plan, not a record: nothing here was written to the editor. When T66 writes a graph, its source goes to `Graphs/` as usual.

It is written for `BP_Show`, `WBP_Stage`, `input.json` and `Tools/check_prompts.py` **as T57, T58, T62, T63, T64 and T65 leave them**, none of which had pushed. The sheets it took into account:

- [T65-build.md](T65-build.md) (all): the speech row (`InputStack`, `CountSize`, `SendButton` as **Action!**, `PassButton`, then room for the timer), `ShowRef` and `NullShow` in `WBP_Stage`, `AtDraw` (closes the @ list), `HoldFocus` and the speech functions, all called from `SetPrompt` every frame. Its part 9 says where the timer goes and that a timeout's send resets the counter and closes the list.
- [T64-build.md](T64-build.md) (parts 2c, 4 and 9): `WBP_ActionBuilder.GetAction` (an unfinished action comes back as `around` with `Ready` false), `Seal`, `IsOn`, `Close`; `WBP_Stage.TakeAction`, `SubmitInput` with T64's `Blocks` gate, `SetPhase` with `PhaseShown` and `FitBuilder`, `SetPrepMode`; `BP_Show.HandleSend` calling `TakeAction` then `SendHumanTurn` in a scene turn. Its part 9: "the timer's auto-send calls the same path as Action! (`HandleSend` → `WBP_Stage.TakeAction`)", and the builder already closes at every header but a scene turn's.
- [T63-build.md](T63-build.md) (parts 2, 5, 6 and 8): `Content/NHOS/Data/input.json` with `spelling_wait` and a `_readme` that ends "T66 adds 'timers' here."; `SpellWait`, the form `TimerSecs` copies; the checker's `input.json` block in `check_files`; `AutoTurn` sends at once.
- [T58-build.md](T58-build.md): the last words stay in Free Talk (`Phase` "free talk") with the flag `LastWordOn`; `NextLastWord` enables Pass on my last word and sends a canned one with autoplay.
- [T57-build.md](T57-build.md): the Pass button stays as it is (`SetPassEnabled`); a pass shows "passed" by the robot's name.
- [T62-build.md](T62-build.md): nothing here calls the stage director; an unfinished action falls back to a look around in `SendHumanTurn` already (T63).

Each place is named by its text first. Find each line by its text before you change it.

**Sources read:** `T66.md` and its plan entry; `T62.md` (the input spec: "Submitting", "Other phases"), `T65.md`; the T57, T58, T62 (names), T63, T64 and T65 build sheets; the findings of T08 (Free Talk, Pass), T09 (the vote row, `SendHumanVote`), T10 (the reactions: `NextReactor`, `SendHumanReact`, "pass"), T27 (the input row), T30 (`LinePrompt`: my input stays closed while the lines play; the `if`/`return` rule); the dropped T24 (`git show df7df63^:Docs/tasks/T24.md`: 30, 45 and 15 s, a reaction "stays silent"); `Graphs/WBP_Stage/` (all), `Graphs/BP_Show/LinePrompt.txt`, `PrepPrompt.txt`; `Graphs/UIStyle/UIColor.txt`; `Tools/check_prompts.py` at `42a917c` (`check_files`, `check_log`, `main`). The design doc wasn't read: T62's edit, which puts the input spec in the Rules tab, isn't made yet, so step 9 is the T66 session's (part 7).

**Re-check against the `Graphs/` sources of your day:** `Graphs/WBP_Stage/SetPrompt.txt` (T64, T65), `SetPrepMode.txt` (T64, T65), `SetPhase.txt` and `SubmitInput.txt` (T64 writes both from a read-back), `TakeAction.txt` (T64); `Graphs/WBP_ActionBuilder/GetAction.txt` (T64); `Graphs/BP_Show/SpellWait.txt` (T63), `NextLastWord.txt` (T58); `Content/NHOS/Data/input.json` and the checker's `input.json` block as T63 left them.

## In short

- **`input.json`** (part 1) gets `timers`: `scene` 30, `free_talk` 0 (no timer), `last_word` 15, `reaction` 15, and a `_readme` line for them.
- **`BP_Show`** (part 2): two new functions and no node edit. `TimerFor()` tells the screen which timer my open input has, from `Phase` and T58's `LastWordOn` (0 with autoplay, in the vote and in Scene Prep). `TimerSecs(Kind)` reads `input.json`'s `timers` at each turn, as T63's `SpellWait` reads `spelling_wait`.
- **`WBP_Stage`** (part 3): the timer lives on the screen side, so it starts when my input opens on screen (after the lines before it, T30) and not when the logic gets there. `TickTimer`, called by `SetPrompt` every frame, starts it when my input opens, draws "0:21" in a new `TimerText` at the right end of the speech row, stops it when my input closes, and calls **`TimeUp`** at 0.
- **`TimeUp`** sends through the paths Action! and Pass already use: a scene turn through `SubmitInput` with T64's gate let through (`HandleSend` → `TakeAction` → `SendHumanTurn`, so an unfinished action goes as a look around); a last word, a reaction or a timed Free Talk line sends what's typed, or a pass when the field is empty. It prints `NHOS: TIMEOUT scene <finished|unfinished|none>` or `NHOS: TIMEOUT <last_word|reaction|free_talk>`.
- **The input row per phase** (part 4): one new `ShapeRow` at the end of `SetPhase` hides Pass while the builder shows (my scene turns) and shows it everywhere else. The builder, the vote row and the rest already follow the phases (T64, T09).
- **The checker** (part 5): `timers` is checked (each kind 0 or 5 to 120 s; scene, last word and reaction never 0; no unknown kind). Tried on a scratch copy (part 5d).

## Questions for my person

None. The task's steps and the input spec settle what gets built; the calls they leave open are below as decisions.

## Decisions made for my person (open to change)

My person asked prep sessions to take their own recommendation on design calls. The T66 session shows this list to my person when it closes the task.

1. **The timer runs in `WBP_Stage`, on screen time.** It starts the frame my input opens (`SetPrompt`'s `CanType` goes true: the lines before my turn have played, T30) and stops the frame it closes. `BP_Show` only answers which timer that is (`TimerFor`). So `BP_Show` gets no node edit: nothing in `StartTurn`, `NextTalker`, `NextLastWord` or `NextReactor` changes.
2. **"Unfinished", "finished" and "none"** in `NHOS: TIMEOUT scene <...>`: unfinished is an action picked with a chip missing (it goes as a look around); none is No action (the default, so my robot stands still); finished is any other ready action, Look around included.
3. **An empty field at a last word's or a reaction's timeout sends a pass**, exactly as the Pass button does. "Sends nothing" can't mean no send at all: the phase waits for my seat. So the reaction shows as "stays silent" and the last word as "passes" with T57's "passed" by my name, as a pressed Pass would. A field with words in it sends them as they are.
4. **Free Talk has no timer** (`free_talk` 0, the spec's call). If my person sets it above 0, a Free Talk line times out like a reaction (what's typed, or a pass); `TimeUp` handles it with no other change.
5. **The vote has no timer** (the spec gives none, and T66 doesn't ask for one). A vote needs a pick, which a timeout would have to make for me; that would be its own task. `TimerFor` gives the vote 0.
6. **Pass is hidden in my scene turns.** The spec's scene row is the field, the counter, Action! and the timer; No action is how a scene turn says nothing. Pass shows in every other phase, enabled only on my Free Talk line, last word or reaction, as now.
7. **The timer's look:** "0:21" in the mono face (T64's `"Mono"`), quiet, in a 72 px box last in the speech row; **the last 5 seconds in gold** ("act now" in the palette; about 10:1 on ink). Red stays for the vote, the cut and errors. When my input closes, the timer hides but keeps its space until the next turn decides, so the field doesn't jump at my send; a turn with no timer collapses it.
8. **A timer that is interrupted restarts.** If my input closed and reopened in the same turn (it shouldn't: nothing plays while the game waits for me), the timer would start again from its full time. The `TIMER start` line would show it.
9. **Real time:** the timer counts with `GetRealTimeSeconds`, which `BP_Show` already uses. The game has no pause.
10. **New check lines:** `NHOS: TIMER start <kind> <secs>` when a timer starts, `NHOS: TIMEOUT scene <finished|unfinished|none>` and `NHOS: TIMEOUT <kind>` when one runs out. Nothing about time reaches the shared log, `game_messages` or any ask (step 7): the timer is on the screen only, and a timeout sends the same turn a click would.

## Step coverage

| T66 step | Where |
|---|---|
| 1. `timers` in `input.json`; the checker checks them | Parts 1 and 5 |
| 2. The timer at the right end of the speech row, from `UIStyle`, starting on screen time | Part 3 (`TickTimer`, `TimerStart`, `DrawTimer`; the tree in 3a) |
| 3. A scene timeout sends through `SendHumanTurn`: finished as built, unfinished as a look around, the text as is; the print | Part 3 (`TimeUp`), via T64's `HandleSend` → `TakeAction` path |
| 4. Free Talk: no builder, no preview, the field, Action! and Pass, no timer | Part 4 (T64 already closes the builder; `ShapeRow` keeps Pass); `free_talk` 0 |
| 5. The last word and the reactions: the field only, their own timers; typed text goes, empty sends nothing; the prints | Parts 2 (`TimerFor`) and 3 (`TimeUp`), decision 3 |
| 6. The Cut's vote keeps its row, no builder | Nothing to build (T64 closes the builder at the Cut's header); part 6 run A checks it |
| 7. No times anywhere the AIs read | Decision 10; part 6 checks the log |
| 8. Autoplay sends at once and never waits | `TimerFor` gives 0 with autoplay; `AutoTurn` and the canned lines send at once (T63, T58, T10); part 6 run B |
| 9. Check the design doc's Rules tab against what was built | Part 7 |

## 0. Before you start (after T65 is pushed)

1. `git log --oneline -15` shows T57, T58, T62, T63, T64 and T65; `Docs/claims/T65` is released. `git lfs locks` shows no lock on `Content/NHOS/Core/BP_Show.uasset` or `Content/NHOS/UI/WBP_Stage.uasset`. Claim T66 (`git lfs lock Docs/claims/T66`) and lock both.
2. **Read what T63, T64 and T65 left:**
   - `Content/NHOS/Data/input.json` matches T63-build part 2 (the `_readme` ends "T66 adds 'timers' here."), and the checker has T63's `input.json` block in `check_files` (find `# input.json: the player's turn input (T63)`). If T63 built it differently, put part 1 and part 5 into what is there.
   - `Graphs/BP_Show/SpellWait.txt`: the JSON nodes that worked (`Json|LoadJsonfromFile`, `Json|HasField`, `Json|GetField`). Part 2's `TimerSecs` copies them.
   - `Graphs/WBP_Stage/SubmitInput.txt` (T64): its inputs (none, or the typed text), its `Blocks` gate, and whether it drops an empty line outside a scene turn. `Graphs/WBP_Stage/SetPhase.txt` (T64): it ends with `PhaseShown` and `FitBuilder`. `Graphs/WBP_ActionBuilder/GetAction.txt`: outputs `Verb`, `Item`, `Target`, `Ready`.
   - `Graphs/WBP_Stage/SetPrompt.txt` (T65): it ends with `(CallFunction|HoldFocus :CanType CanType)`. `ShowRef`, `NullShow` and `AtDraw` exist (T65).
   - T65's `InputRow` order: `InputStack`, `CountSize`, `SendButton`, `PassButton`, `ContinueButton`, `StartButton` (and T38's `ChatButton` if it landed), with their slot paddings in T65's findings.
3. `python Tools/check_prompts.py --offline` passes before you start.
4. **The survey** (each item a separate `call_tool`; save each read to `Saved/T66/<name>.read.txt`; never write a read-back to the editor):
   1. **The Pass button's `OnClicked` chain** in `WBP_Stage`'s EventGraph (`find_nodes` for event nodes, full class paths, T30): what it calls with "pass" (expected: the `OnSend` dispatcher, which `BP_Show` binds to `HandleSend`, with the text `pass`, as the vote buttons send `#vote <i>`, T09). `TimeUp`'s pass does exactly the same; part 3 writes it as `BP_Show.HandleSend` with "pass", so use the chain's real call if it differs.
   2. **`BP_Show.HandleSend`'s input pin name** (`find_nodes` on its entry; `Text` below) and the `Phase` texts it switches on: expected `"scene"`, `"free talk"`, `"the cut"`, `"reactions"` (T07, T08, T09, T10). `TimerFor` uses the same texts.
   3. **Variables** in `BP_Show`: `Phase` (String), `Autoplay` (Boolean), `LastWordOn` (Boolean, T58) exist; `TimerKind`, `TimerDef`, `TimersObj`, `TimerSecsV` don't. In `WBP_Stage`: `TimerOn`, `TimerWasOpen`, `TimerEnd`, `TimerKind`, `TimerShown`, `ForceSend` don't exist yet.
   4. **Node names** with `find_node_types` (`context_pins: []`, T29): in `WBP_Stage`, `Math|Float|Ceil` (the "Ceil" node that returns an Integer), integer division and remainder (the DSL's `/` and `%` if `dslpp.py` or `write_graph_dsl` has them, else the `Math|Integer` nodes), `Class|BPShow|TimerFor` (after part 2 compiles). In `BP_Show`, the type `Json|GetField` gives a nested object: the variable type that holds `timers` (`JsonObject`, the Json Blueprint Utilities wrapper; `TimersObj` below).

## 1. `Content/NHOS/Data/input.json` (step 1)

The whole file after T66 (tabs for indents, as T63 wrote it). T63's `spelling_wait` line stays word for word; the first and last `_readme` lines change, and one line is new:

```json
{
	"_readme": [
		"Settings for the player's turn input (T63, T66). The game reads this file at each line the player sends (BP_Show.SpellWait) and each time the player's input opens (BP_Show.TimerSecs), so a change takes effect at the next line or turn, even mid-show.",
		"spelling_wait: seconds the input LLM gets to fix the spelling of a typed line (BP_Show.SpellAsk). If it fails, is refused or takes longer, the line goes as typed, with provider names turned into Player names (ScrubLabels), and the log prints NHOS: SPELLING skipped <off|failed|empty|late>. A reply that comes late is dropped. 0 sends every line as typed, with no call. A missing file or field means 4.",
		"timers: the seconds the player has for each kind of turn, counted from when their input opens on screen, after the lines before it have played (WBP_Stage.TickTimer). scene is a scene turn, free_talk a Free Talk line, last_word the reply after being named in the final round, reaction a reaction after the Cut. When one runs out the turn sends itself (NHOS: TIMEOUT): a scene turn sends the action as built, an unfinished one as a look around, with whatever is typed; the others send what is typed, or a pass if nothing is. 0 means no timer; the vote has none. A missing file or field gives scene 30, free_talk 0, last_word 15, reaction 15. Autoplay never waits for a timer, and no time ever reaches the AIs.",
		"Tools/check_prompts.py checks this file."
	],
	"spelling_wait": 4,
	"timers": {
		"scene": 30,
		"free_talk": 0,
		"last_word": 15,
		"reaction": 15
	}
}
```

- The values are the task's: scene 30 (the spec), last word and reaction 15 each (T24's value for a reaction), Free Talk 0 (the spec gives it none).
- `DefaultGame.ini` stages `Content/NHOS/Data` as loose files, so a build reads the new field with no config change (T63-build part 2).
- **No relay change:** nothing in `Relay/` reads `input.json` (`grep -rn "input.json" Relay/` finds nothing at `42a917c`), so this file needs no deploy OK. Run the grep again before the commit.

## 2. `BP_Show`: which timer my input has (steps 2, 5 and 8)

Two new functions with files, no node edit. **New variables:** `TimerKind` (String, ""), `TimerDef` and `TimerSecsV` (Float, 0.0), `TimersObj` (the type survey 4 found for a nested JSON object). Create both functions and their parameters, compile, then write `TimerSecs` first (T18, T54).

| Function | Inputs | Outputs | Called by |
|---|---|---|---|
| `TimerSecs` | `Kind` (String) | Float | `TimerFor` |
| `TimerFor` | — | `Kind` (String), `Secs` (Float) | `WBP_Stage.TimerStart` |

`Graphs/BP_Show/TimerSecs.txt`:

```lisp
; T66: input.json's timers.<Kind> in seconds, read at each turn so a test can change it mid-show (SpellWait's form, T63).
; A missing file or field gives the spec's value: scene 30, free_talk 0 (no timer), last_word and reaction 15.
(fn TimerSecs (Kind)
  (set TimerDef (select (streq Kind "scene") 30.0 (select (streq Kind "free_talk") 0.0 15.0)))
  (bind _cdir (Utilities|Paths|GetProjectContentDirectory))
  (bind (_o _ok) (Json|LoadJsonfromFile (Utilities|Struct|MakeFilePath (cat _cdir "NHOS/Data/input.json"))))
  (if (not _ok)
    (return (V TimerDef)))
  (bind _h (Json|HasField _o "timers"))
  (if (not _h)
    (return (V TimerDef)))
  (bind _t (Json|GetField _o "timers"))
  (set TimersObj _t)
  (bind _hk (Json|HasField (V TimersObj) Kind))
  (if (not _hk)
    (return (V TimerDef)))
  (bind _v (Json|GetField (V TimersObj) Kind))
  (set TimerSecsV _v)
  (return (V TimerSecsV)))
```

- `GetField`'s output takes the type of the variable it is set to (`SpellWait.txt`: `(set SpellSecs _w)`), so `TimersObj` must be the JSON object type and `TimerSecsV` a Float. **If a nested object won't read that way,** read the whole file as a string with `LoadFileToString` and, for each kind, take the number after `"<kind>":` with `Split` (two `Split` calls, then `Conv_StringToFloat`), and write under "Findings" what the JSON nodes did.
- Every `if` returns, and the last statement is a plain `return` (T30).

`Graphs/BP_Show/TimerFor.txt`:

```lisp
; T66: the timer for my input as it opens on screen (WBP_Stage.TimerStart asks at that moment, when the logic is waiting
; for me): its kind and its seconds from input.json. A scene turn, a Free Talk line, a last word (T58: LastWordOn, inside
; Free Talk) and a reaction each have their own; the vote and Scene Prep have none. 0 seconds means no timer. Autoplay
; never waits for a timer (step 8): it sends at once (AutoTurn, the canned lines).
(fn TimerFor ()
  (set TimerKind "")
  (if (streq (V Phase) "scene")
    (set TimerKind "scene"))
  (if (streq (V Phase) "free talk")
    (set TimerKind (select (V LastWordOn) "last_word" "free_talk")))
  (if (streq (V Phase) "reactions")
    (set TimerKind "reaction"))
  (if (or (V Autoplay) (Utilities|String|IsEmpty (V TimerKind)))
    (return (V TimerKind) 0.0))
  (bind _s (CallFunction|TimerSecs :Kind (V TimerKind)))
  (return (V TimerKind) _s))
```

- The three `if`s that set `TimerKind` don't return and come before any that does, so they join (T01, T30).
- **Why the logic's `Phase` is right here, though the logic runs ahead of the screen (T30):** my input opens only on my turn, and the logic can't pass my turn before I send. So when `CanType` rises, `Phase` is my turn's phase. Use survey 2's phase texts if they differ.
- `(return a b)` fills the outputs in the order they were made (T64-build part 2c).

Compile `BP_Show` with warnings as errors; the editor log after the compile has no `LogBlueprint: Error`. Close every game window before you save (T53).

## 3. `WBP_Stage`: the timer and the auto-send (steps 2, 3 and 5)

### 3a. The widget tree

Add to `InputRow` as its **last** child (after `StartButton`, or after T38's `ChatButton` if it is last):

```
TimerSize     SizeBox; WidthOverride 72; slot: VAlign Center, padding left = SendButton's left padding (T65's findings; T28: 10); Collapsed at design time
└ TimerText   TextBlock; text "0:30"; justify Center
```

`bIsVariable` on for both. 72 px holds "0:30" or "1:00" in the mono face at 18 pt, so the field keeps its width while the timer counts. With T64's wide panel (1000 px in scene turns), the row is: field, counter (72), Action!, timer (72). At 640 (Free Talk, the last word, the reactions), Pass sits between Action! and the timer.

### 3b. New variables

| Variable | Type | Default | Used by |
|---|---|---|---|
| `TimerOn`, `TimerWasOpen`, `ForceSend` | Boolean | false | part 3 |
| `TimerEnd` | Float | 0.0 | `TimerStart`, `TimerTick` |
| `TimerKind` | String | "" | `TimerStart`, `TimeUp` |
| `TimerShown` | Integer | -1 | `TimerStart`, `TimerTick` |

### 3c. The functions

Create each with its parameters, compile, then write them callee first: `DrawTimer`, `TimeUp`, `TimerTick`, `TimerStart`, `TimerStop`, `TickTimer`, `ShapeRow` (part 4).

`Graphs/WBP_Stage/DrawTimer.txt` (input `Secs`: Integer):

```lisp
; T66: the timer at the right end of the speech row (step 2): "0:21" in the mono face, quiet; the last 5 seconds in gold,
; the palette's "act now" (about 10:1 on the ink panel). Red stays for the vote, the cut and errors.
(fn DrawTimer (Secs)
  (bind _m (/ Secs 60))
  (bind _r (% Secs 60))
  (bind _txt (cat (str _m) ":" (select (< _r 10) "0" "") (str _r)))
  (bind fMono (Class|UIStyle|UIFont :Role "Mono"))
  (bind cGold (Class|UIStyle|UIColor :Role "Gold"))
  (bind cQuiet (Class|UIStyle|UIColor :Role "Quiet"))
  (Class|Text|SetFont :self (Variables|WBP_Stage|GetTimerText) :Font fMono)
  (Class|Text|SetColorandOpacity :self (Variables|WBP_Stage|GetTimerText) :ColorAndOpacity (Utilities|Struct|MakeSlateColor :SpecifiedColor (select (<= Secs 5) cGold cQuiet)))
  (Class|Text|SetText :self (Variables|WBP_Stage|GetTimerText) :Text (Utilities|Text|ToText(String) _txt)))
```

`/` and `%` are integer division and remainder; use survey 4's nodes if the DSL has neither.

`Graphs/WBP_Stage/TimeUp.txt`:

```lisp
; T66: my time ran out. A scene turn (step 3) sends itself as Action! would, with T64's gate let through: HandleSend takes
; the action with TakeAction, so a finished action goes as built, an unfinished one as a look around (GetAction's Ready
; false, the fallback a bot gets), and the typed words as they are. A last word, a reaction or a timed Free Talk line
; (step 5) sends what's typed, or a pass when the field is empty, exactly as the Pass button does (decision 3).
(fn TimeUp ()
  (set TimerOn false)
  (CallFunction|AtDraw :Open false)
  (bind _typed (Utilities|String|Trim (Utilities|String|ToString(Text) (Class|TextBox|GetText :self (Variables|WBP_Stage|GetInputBox)))))
  (if (streq (V TimerKind) "scene")
    (bind (_v _i _t _r) (Class|WBPActionBuilder|GetAction :self (Variables|WBP_Stage|GetActionBuilder)))
    (print (cat "NHOS: TIMEOUT scene " (select (not _r) "unfinished" (select (streq _v "none") "none" "finished"))))
    (set ForceSend true)
    (CallFunction|SubmitInput)
    (set ForceSend false)
    (return))
  (print (cat "NHOS: TIMEOUT " (V TimerKind)))
  (if (Utilities|String|IsEmpty _typed)
    (bind _sh (CallFunction|ShowRef))
    (Class|BPShow|HandleSend :self _sh :Text "pass")
    (return))
  (CallFunction|SubmitInput))
```

- `GetAction` (T64) reads the builder without sealing it; `HandleSend` seals it through `TakeAction` and prints `NHOS: BUILDER send <verb> ... ready=<yes|no>`. With `Ready` false the verb is already `around`, so `NHOS: HUMAN around - - says=<typed>` follows (T63).
- **`SubmitInput`'s call:** if survey 0.2 found it takes the typed text, pass `_typed` (untrimmed if it trims itself). It reads, clears and sends the box as Action! does, so the counter resets and the @ list stays closed (T65).
- **The pass** is survey 1's: replace `(Class|BPShow|HandleSend :self _sh :Text "pass")` with whatever the Pass button's chain calls. `HandleSend` refuses a send that isn't my turn (T08, T10: `HumanSent`, `TalkSeat`, `ReactSeat`), so a timeout racing a click can't send twice.
- Both `if`s return; the last statement is a plain call (T30).

`Graphs/WBP_Stage/TimerTick.txt`:

```lisp
; T66: one frame of the running timer: redraw when the shown second changes, and send the turn at 0.
(fn TimerTick ()
  (bind _left (- (V TimerEnd) (Utilities|Time|GetRealTimeSeconds)))
  (bind _s (Math|Float|Ceil (select (< _left 0.0) 0.0 _left)))
  (if (!= _s (V TimerShown))
    (set TimerShown _s)
    (CallFunction|DrawTimer :Secs _s))
  (if (<= _left 0.0)
    (CallFunction|TimeUp)))
```

`Graphs/WBP_Stage/TimerStart.txt`:

```lisp
; T66: my input just opened on screen (the lines before it have played, T30). BP_Show says which timer this turn has
; (TimerFor: 0 for the vote, Free Talk and autoplay); a timer above 0 shows and starts counting.
(fn TimerStart ()
  (bind _sh (CallFunction|ShowRef))
  (if (== _sh (V NullShow))
    (return))
  (bind (_kind _secs) (Class|BPShow|TimerFor :self _sh))
  (set TimerKind _kind)
  (set TimerOn (> _secs 0.0))
  (set TimerEnd (+ (Utilities|Time|GetRealTimeSeconds) _secs))
  (set TimerShown -1)
  (if (V TimerOn)
    (Widget|SetVisibility :self (Variables|WBP_Stage|GetTimerSize) :InVisibility "HitTestInvisible")
    (print (cat "NHOS: TIMER start " _kind " " (str (Math|Float|Round _secs))))
    (CallFunction|TimerTick)
    (else
      (Widget|SetVisibility :self (Variables|WBP_Stage|GetTimerSize) :InVisibility "Collapsed"))))
```

The `if`/`else` is the last statement after the early return, so nothing has to join it (T30).

`Graphs/WBP_Stage/TimerStop.txt`:

```lisp
; T66: my input closed (I sent, or a timeout sent for me): the timer stops and hides, keeping its space until the next
; turn, so the field doesn't jump at my send (decision 7).
(fn TimerStop ()
  (if (V TimerOn)
    (Widget|SetVisibility :self (Variables|WBP_Stage|GetTimerSize) :InVisibility "Hidden"))
  (set TimerOn false))
```

`Graphs/WBP_Stage/TickTimer.txt` (input `CanType`: Boolean):

```lisp
; T66: the turn timer, once a frame from SetPrompt. It starts when my input opens on screen (CanType rises), stops when it
; closes (CanType falls), and ticks while it runs. TimerWasOpen is its own copy of CanType, apart from SetPrompt's
; LastCanType, so the order inside SetPrompt doesn't matter.
(fn TickTimer (CanType)
  (bind _rise (and CanType (not (V TimerWasOpen))))
  (bind _fall (and (not CanType) (V TimerWasOpen)))
  (set TimerWasOpen CanType)
  (if _rise
    (CallFunction|TimerStart))
  (if _fall
    (CallFunction|TimerStop))
  (if (and CanType (V TimerOn))
    (CallFunction|TimerTick)))
```

- No `if` returns, so each joins the next.
- On the rising frame `TimerStart` already ticks once; the third `if` ticks again in the same frame, which only redraws nothing (the shown second is the same).
- **Why `CanType`:** `BP_Show.ComputePrompt` opens my input only on my turn, and `LinePrompt` keeps it closed while lines play (T30), so its rise is "my turn opens on screen". After my send, `HumanSent` closes it.

### 3d. Rewrites of T64's and T65's files

**`SetPrompt`** (T65's file): after T65's last line `(CallFunction|HoldFocus :CanType CanType)`, add

```lisp
  (CallFunction|TickTimer :CanType CanType)
```

and the header comment `; T66: the turn timer follows my input (TickTimer).` Commit to `Graphs/WBP_Stage/SetPrompt.txt`.

**`SubmitInput`** (T64's file): T64's gate

```lisp
  (bind _blk (Class|WBPActionBuilder|Blocks :self (Variables|WBP_Stage|GetActionBuilder)))
  (if _blk
```

becomes

```lisp
  (bind _blk (Class|WBPActionBuilder|Blocks :self (Variables|WBP_Stage|GetActionBuilder)))
  (if (and _blk (not (V ForceSend)))
```

with `; T66: a timeout (ForceSend) sends an unfinished action too; HandleSend gets it as a look around.` in the header. Nothing else changes. Commit to `Graphs/WBP_Stage/SubmitInput.txt`.

**`SetPrepMode`** (T65's file): in the `Prep` branch, after T65's `CountSize` line, add

```lisp
    (Widget|SetVisibility :self (Variables|WBP_Stage|GetTimerSize) :InVisibility "Collapsed")
    (Variables|Default|SetTimerOn false)
```

so a Scene Prep (a restart included, T28) never leaves a timer up. Header: `; T66: Scene Prep hides the turn timer.` Commit to `Graphs/WBP_Stage/SetPrepMode.txt`.

## 4. The input row per phase (steps 4 to 6)

What each phase shows after T64, T65 and T66:

| Phase (my input open) | Preview and builder | Field, counter, Action! | Pass | Timer | Vote row |
|---|---|---|---|---|---|
| My scene turn | shown (T64) | shown | **hidden** (decision 6) | `scene`, 30 s | hidden |
| Free Talk, my line | closed (T64: any other header) | shown | shown, enabled (T08) | none (`free_talk` 0) | hidden |
| My last word | closed | shown | shown, enabled (T58) | `last_word`, 15 s | hidden |
| The Cut, my vote | closed | shown (the reason, T09) | shown, disabled (as now) | none | shown (T09) |
| My reaction | closed | shown | shown, enabled (T10) | `reaction`, 15 s | hidden |

`Graphs/WBP_Stage/ShapeRow.txt`:

```lisp
; T66: the input row per phase. In my scene turns the builder shows and Pass doesn't: No action is how a scene turn says
; nothing (the spec's row: the field, the counter, Action! and the timer). Every other header shows Pass, enabled only on
; my Free Talk line, last word or reaction (SetPassEnabled, as now). T64 opens and closes the builder at the same header.
(fn ShapeRow ()
  (bind _on (Class|WBPActionBuilder|IsOn :self (Variables|WBP_Stage|GetActionBuilder)))
  (if _on
    (Widget|SetVisibility :self (Variables|WBP_Stage|GetPassButton) :InVisibility "Collapsed")
    (else
      (Widget|SetVisibility :self (Variables|WBP_Stage|GetPassButton) :InVisibility "Visible"))))
```

**`SetPhase`** (T64's file): after T64's last line `(CallFunction|FitBuilder)`, add `(CallFunction|ShapeRow)`, with `; T66: Pass hides in my scene turns (ShapeRow).` in the header. Commit to `Graphs/WBP_Stage/SetPhase.txt`.

- **Not in `FitBuilder`:** `SetPrepMode(true)` calls `FitBuilder` right after it collapses Pass for Scene Prep (T64 part 4e), so a Pass rule there would show Pass in Scene Prep. `SetPhase` runs only at headers.
- `SetPrepMode(false)` shows Pass when the scene starts; the turn's header comes next and hides it again before my input opens, so it never shows in a scene turn while I can type.

Compile `WBP_Stage` with warnings as errors, save. Close every game window before you save (T53).

## 5. `Tools/check_prompts.py` (step 1)

Line numbers move with T57, T58, T62 and T63; find each place by its text.

**a. A constant**, right after T63's `INPUT_RULES` block (find `# T63: the input LLM fixes spelling only; prompts.json 'input' must keep these rules word for word.`; if T63 named it otherwise, put it after T63's constants):

```python
# T66: input.json 'timers', the seconds the player has per kind of turn (BP_Show.TimerFor). 0 = no timer.
TIMER_KINDS = ("scene", "free_talk", "last_word", "reaction")
# A turn the game must never wait on forever: a scene turn, a last word and a reaction always have a timer.
TIMED_KINDS = ("scene", "last_word", "reaction")
```

**b. The check**, in `check_files`, inside T63's `if inp is not None:` block, after its `_readme` check (`errors.append("input.json: _readme must be an array of lines")`):

```python
        # T66: the turn timers, in seconds. Each kind is 0 (no timer) or 5 to 120 seconds; Free Talk may be 0 (the spec
        # gives it none), the others never, so a turn can't hang on the player.
        timers = inp.get("timers")
        if not isinstance(timers, dict):
            errors.append("input.json: timers must be an object of seconds per kind of turn (T66)")
        else:
            for k in TIMER_KINDS:
                v = timers.get(k)
                if isinstance(v, bool) or not isinstance(v, (int, float)) or not (v == 0 or 5 <= v <= 120):
                    errors.append(f"input.json: timers.{k} must be 0 (no timer) or 5 to 120 seconds, not {v!r}")
                elif k in TIMED_KINDS and v == 0:
                    errors.append(f"input.json: timers.{k} can't be 0: the game would wait for the player forever")
            for k in sorted(set(timers) - set(TIMER_KINDS)):
                errors.append(f"input.json: timers.{k} is not a kind of turn the game times ({', '.join(TIMER_KINDS)})")
```

**c. The docstring:** after the sentence T63 adds about `input.json` (find `input.json holds`), add: `Since T66 it also holds 'timers', the seconds per kind of turn (scene, free_talk, last_word, reaction): each 0 (no timer) or 5 to 120, and never 0 for a scene turn, a last word or a reaction.`

T63 already puts `input.json` in the `Files OK` line, so `main` doesn't change.

**d. Tried on a scratch copy** (this session, at `42a917c`: `Tools/check_prompts.py`, `Content/NHOS/Data` with part 1's `input.json`, the rest of `Content/NHOS` linked in for the props check, and `Relay/`). T63 hasn't pushed, so the copy got the `input.json` part of T63-build part 6d's block (`spelling_wait` and `_readme`, not its `INPUT_RULES` lines), then parts 5a and 5b. `python3 -I Tools/check_prompts.py --offline` exits 0 with part 1's file, and each break below exits 1 with exactly this one line:

| Break | Line |
|---|---|
| `"scene": 0` | `FAIL file: input.json: timers.scene can't be 0: the game would wait for the player forever` |
| `"reaction": "15"` | `FAIL file: input.json: timers.reaction must be 0 (no timer) or 5 to 120 seconds, not '15'` |
| `"last_word": 3` | `FAIL file: input.json: timers.last_word must be 0 (no timer) or 5 to 120 seconds, not 3` |
| `"vote": 10` added | `FAIL file: input.json: timers.vote is not a kind of turn the game times (scene, free_talk, last_word, reaction)` |
| `timers` removed | `FAIL file: input.json: timers must be an object of seconds per kind of turn (T66)` |

Run the same five breaks on the real file after the edit, then put it back (`git diff Content/NHOS/Data/input.json` shows only part 1).

## 6. The check

**Before the runs:** `Local/switches.json` in the repo folder with `"mode": "free"`, `"autoplay": false`, `"fast_lines": false`, `"ai_seats": 0`, **`"spare_human": true`** (so I'm never cut and get a reaction turn every scene), `"force_tie": false`. PIE in a floating window at 1600 × 900; pick **Test for Free**. Screenshots with `SlateInspectorToolset.Screenshot` to `Saved/T66/shots/` (not in git).

### Run A: one show played by hand in PIE

1. **`timer_scene.png`:** press Start the scene. When turn 1 opens (the lines stop): `NHOS: TIMER start scene 30`, the timer at the right end of the speech row, no Pass in the row. Screenshot at about 0:21.
2. **A finished action left to time out:** click **Grab** and a prop chip, type `Mine.`, touch nothing else. At 0:05 the timer turns gold (`timer_gold.png`). At 0: `NHOS: TIMEOUT scene finished`, `NHOS: BUILDER send grab <prop> - ready=yes`, `NHOS: HUMAN grab <prop> - says=Mine.`, later my robot's grab and the `NHOS: LOG` line with "grabs the <prop>" and "Mine.". It plays as built. (If a free bot grabbed the same prop first, T62's race makes it a look around; grab again on turn 2.)
3. **An unfinished Throw left to time out:** turn 2: click **Throw**, click the held prop, pick no target, type `Catch this!`. At 0: `NHOS: TIMEOUT scene unfinished`, `NHOS: BUILDER send around - - ready=no`, `NHOS: HUMAN around - - says=Catch this!`, then `NHOS: ACT human look around ...` and the `NHOS: LOG` line "looks around" with "Catch this!". My robot looks around (`timeout_unfinished.png`).
4. **No action left to time out:** turn 3: touch nothing. At 0: `NHOS: TIMEOUT scene none`, `NHOS: HUMAN none - - says=-`, the `NHOS: LOG` line "stands still".
5. **`freetalk.png`:** my Free Talk line: no builder and no preview, the field, the counter, Action! and Pass, **no timer** and no `NHOS: TIMER start` line. Send a line, or press Pass.
6. **The last word** (only if a free bot names me in the final round; free mode does it in about a third of scenes, T58): `NHOS: TIMER start last_word 15`, the field, Action!, Pass and the timer (`lastword.png`). Type `I was framed.` and let it run out: `NHOS: TIMEOUT last_word`, and the line reaches the log as my last word. If nobody names me in the show, write under "Findings" that the last word's timer wasn't seen; `TimerFor` gives it the same path as a reaction.
7. **`cut.png`:** the vote: the vote row, no builder, no timer, no `TIMER start` line.
8. **`reaction.png`:** my reaction after the cut: `NHOS: TIMER start reaction 15`, the field, Action!, Pass and the timer, no builder. Leave the field empty: at 0, `NHOS: TIMEOUT reaction`, then my reaction as a pass ("stays silent" on screen; the `NHOS: LOG` line has the pass's `does`), and no `NHOS: SPELLING` or `NHOS: LLM spell-` line (nothing is said).
9. **A reaction with words:** in the next scene's reaction, type `Told you.` and let it run out: `NHOS: TIMEOUT reaction`, and "Told you." reaches the log.
10. **Step 7:** search the editor log from this show for the `NHOS: LOG` lines of steps 2 to 9: none holds a time, a "timeout" or a "timer". If the log shows the asks' state (the `NHOS: LLM` or ask lines), search the next AI asks after a timeout for "TIMEOUT", "timer" and "seconds": none.

Stop PIE.

### Run B: a free autoplay show in a game window

`"autoplay": true`, `"fast_lines": true`, `"mode": "free"`, `"spare_human": false`; the game-window command from `CLAUDE.md` with `-log=T66auto.log`. In the log: `NHOS: SHOW END`, **no `LogScript` line**, and **no `NHOS: TIMER start` or `NHOS: TIMEOUT` line at all** (autoplay sends at once, and `TimerFor` gives it 0). Close the game window by its `-log=` name.

### Run C: the checker

`python Tools/check_prompts.py --offline` passes, and part 5d's five breaks each fail with their line.

**Afterward:** `autoplay`, `fast_lines` and `spare_human` back to false, the PIE window settings back, every game window closed, `input.json` as part 1 left it.

### Findings to write in `T66.md`

- **The design review** from the shots, as a critical first-time player: do I notice the timer before it runs out, does gold read as "hurry", is it clear my turn went by itself (the `TIMEOUT` turn looks like any other in the chat), does the row read right in each phase.
- What survey 1 found (the Pass chain) and how `TimeUp`'s pass calls it; whether `TimersObj` read the nested object (part 2).
- Whether the last word's timer was seen (run A step 6).
- **Unreal MCP rules found in this task**, as earlier tasks do.

## 7. The design doc (step 9)

By T66, T62 has put the input spec in the Rules tab, and T65 may have proposed its chip wording. Read the Rules tab (and the Turn Input tab, if T62 kept it) with the Claude Docs connector and compare it with what T66 built:

- the scene turn's 30-second timer, counted from when my turn opens on screen;
- the auto-send: finished as built, unfinished as a look around, the typed words as they are;
- the last word and the reactions: the speech field only, 15 seconds each; an empty field at the timeout is a pass;
- Free Talk: no timer; the vote: no timer;
- Pass hidden in scene turns (decision 6), shown in Free Talk, the last word and the reactions;
- no time ever reaches the AIs.

**Propose a fix for each difference** to my person, in the doc's words, and edit only after their OK (the plan's "The design doc follows the game"). A likely one: if the doc says only "Last word and reactions after the Cut: speech field only, with their own timers", propose adding "15 seconds each. If time runs out, what you typed is sent; an empty field is a pass." Write what was proposed and what my person said under "Findings".

## 8. The commit

One commit, `T66: The turn timer, the auto-send and the other phases`: `Content/NHOS/Core/BP_Show.uasset`, `Content/NHOS/UI/WBP_Stage.uasset`, `Content/NHOS/Data/input.json`, `Tools/check_prompts.py`; `Graphs/BP_Show/` (new: `TimerSecs`, `TimerFor`), `Graphs/WBP_Stage/` (new: `DrawTimer`, `TimeUp`, `TimerTick`, `TimerStart`, `TimerStop`, `TickTimer`, `ShapeRow`; changed: `SetPrompt`, `SubmitInput`, `SetPrepMode`, `SetPhase`); `Docs/tasks/T66.md` (Result, Findings), `Docs/Plan.md` (the box, the "Next up" line), `Docs/DevLog.md`. If step 9 changed the design doc, say so in the message. Stage by path. Unlock both assets after the push.

## 9. Knock-on: tell, don't change

- **T67 to T69** (analytics and after; T67 depends on T66's phases): a timeout is worth an analytics event (`timeout` with the kind and finished, unfinished or none). `TimeUp` is the one place to call it from.
- **T34:** the timer's gold (decision 7) and Pass hidden in scene turns (decision 6) are its to revisit with the rest of the screen. If T34 makes in-show buttons focusable (T33-1), T65's `HoldFocus` still takes the focus back while I can type.
- **T61** (the stagehand): a first-scene tip can mention the timer ("You have 30 seconds; your turn goes by itself when time runs out").
- **The vote has no timer** (decision 5). If shows stall there, a small task can add `timers.vote` and a random pick at the timeout.
- **`Docs/ItchPage.md`, "Controls":** one line after T66: "Each scene turn has 30 seconds; when time runs out, your turn goes as it stands. Last words and reactions have 15."
