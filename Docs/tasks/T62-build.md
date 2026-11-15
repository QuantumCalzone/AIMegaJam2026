# T62 build sheet: one rule set for every action

Back to [T62](T62.md). A PC prep session wrote this on 2026-11-15, without the editor, against **`noHumansOnSet` at `d2d4cdc` (T52)**. T54, T55, T57 and T58 land before T62 and change `BP_Show`, `prompts.json`, `free_mode.json` and `Tools/check_prompts.py`. This sheet writes the data and checker edits **as T58 leaves those files**, using [T54-build.md](T54-build.md), [T55-build.md](T55-build.md), [T57-build.md](T57-build.md) and [T58-build.md](T58-build.md). Each place is named by its text first; a line number is "about line N" as T58 leaves the file (worked out from those sheets), or "line N at `d2d4cdc`" for the checker, whose lines move too much to predict. Find each line by its text before you change it. [T45-build.md](T45-build.md) also changes `StagePrep` and `BP_StageDirector` (`SetCard`, `ResetStage`); part 3e covers both cases, with and without T45.

**Sources read:** `T62.md` and its plan entry; `T63.md` to `T66.md` (what they need from T62); the T52, T54, T55, T57, T58 and T45 build sheets; `T07`, `T10`, `T19`, `T30`, `T44`, `T50` and `T52` findings; every file in `Graphs/BP_StageDirector/` and `Graphs/BP_Prop/`; `Graphs/BP_Robot/` (`Receive`, `DoGrab`, `DoHanded`, `DropAll`, `SetCut`, `GoHome`, `ToTable`, `StartAct`, `TickActs`); `Graphs/BP_Show/` (`StageLine`, `ActorLine`, `ShowLine`, `StagePrep`, `StateLine`, `RunCue`); `Graphs/BPC_LinePlayer/` (`Push`, `Pump`, `PlayCur`, `Cue`); `Graphs/BPC_LLMClient/` (`FreeReply`, `FreeAction`, `FreeFill`); `prompts.json`, `free_mode.json`, `llm.json`, `scenes.json` (the wants), `Tools/check_prompts.py`, `Relay/src/index.js` (free mode's fill). **The design doc, read and not changed:** Rules tab rev 42, the new **Turn Input** tab rev 1, Bot Prompts rev 82, Tech & Build rev 25.

## In short

- **The doc is already mostly there.** Since T62.md was written, my person put the whole input spec in the doc: a new **Turn Input** tab, and the Rules tab (rev 42) now says "Each turn you click to build one action ... (see Turn Input)" and "Actions: Move, Look, Grab, Throw, Give, Look around and No action. The AIs and you choose from the same set." So step 1 shrinks to the rule set itself: two Rules sentences, two Bot Prompts lines (part 1). They wait for my person's OK.
- **`BP_StageDirector` holds the rules and who holds what** (part 2). New functions: `ItemsFor`, `TargetsFor` and `CanDo` (the task's three), plus the state they read (`SetScene`, `SetOut`, `Accept`, `HoldingOf`) and the step that checks each line before the shared log (`AcceptDoes`, with `ParsePart` split out of `PlayPart`). `DoVerb` learns a look at a prop and loses the move to an actor and the put-down; `BotCands` goes. All with files. **`BP_Prop` doesn't change:** the holder is game state in the director, not the prop's animation slot.
- **`BP_Show`** (part 3): five small new functions with files (`StageRules`, `CheckDoes`, `CheckTurn`, `HeldBy`, `RuleOut`, plus `HoldLine` for the check), one line in `StagePrep` (has a file), and node edits in graphs with no file: one node each in `PlayTurn`, `PlayReact` and `CutActor`, and four nodes in `ActorState` (`holding` in each cast entry and in `you`).
- **`prompts.json`** (part 4): the actions block of `game` says 0 or 1 action and the rules, with the doc's two new lines word for word; a `holding` line under "Reading the state"; `asks.scene_turn` "actions (0 or 1)"; `asks.reaction` and `asks.reaction_cut` "speech. No actions."; `_readme`. `asks.last_word` needs nothing (T58 wrote "No actions."). `does_templates` doesn't change: "looks at {target}" already reads back for a prop.
- **`free_mode.json`** (part 5): a free actor takes 0 or 1 action in a scene turn and none in a reaction, and gets a `look {prop}` action. **This is the only change that redeploys the relay:** the push that carries it needs my person's OK, typed in the T62 session.
- **`Tools/check_prompts.py`** (part 6): the sample show takes one action a turn and its states get `holding`; 0 or 1 action in a scene turn, none in a reaction; a look may take a prop; the holding rules as WARNs; a file check that the templates still read back; the doc's two lines word for word; `--log` fails a log entry with too many actions and counts the rule fallbacks.
- **Four questions for my person** (below). This sheet is written for the recommended answer of each, and says what changes for the other.

## Questions for my person

The recommended answer is first in each.

1. **When does the check run: when a line enters the shared log, or when it plays on stage?** Since T30, a line enters the shared log at once and plays on stage up to half a minute later, and the next turn's asks go out while the lines still play (T30: "The asks for the next step may go out while lines play"). T62.md says `PlayPart` or `DoVerb` calls `CanDo`, which is play time.
   - **When the line enters the shared log (Recommended).** `PlayTurn` checks each seat's action in its shuffled order, right before the entry is made, and `PlayReact` drops a reaction's actions. A failed action goes into the log as "looks around", and `holding` changes at once. Why: then the log, `holding` in the next asks and the stage always agree. Checked at play time, the next turn's asks would show holdings from before the last turn's grabs (the lines haven't played yet), and the log would keep "grabs the rose" for a grab that fell back. `PlayPart` then plays an action that is already checked, and its `Fallback` stays only for a name the stage can't find. The order is the log's random order, so "the first to play gets it" still holds, and my action has the same chance as an AI's.
   - At play time, as T62.md says: `PlayPart` calls `CanDo`; the log keeps the action as written; `holding` lags a turn behind the log.
2. **Can an actor hold any number of props?** A robot has two hands, plus a head (the crown) and a back (the cape) for some props. When a third hand prop reaches a full-handed robot, `BP_Robot.Receive` drops the prop in its right hand at its feet. The spec's rules don't say how many props one actor may hold.
   - **Two props at most (Recommended).** Grab is refused with "hands full" when the actor holds two, and a give goes only to an actor holding fewer than two. Why: the game state and the stage then never disagree (no robot ever gets a third prop, so `Receive` never drops one), it costs one variable (`MaxHeld`, 2) and two checks, and the rule is easy to say. It adds a tip to T64's builder ("Your hands are full.") and a few words to the doc (part 1).
   - No limit: the state keeps every prop an actor takes, but the stage drops one at the robot's feet when a third hand prop arrives. The robot can still throw that prop (the throw picks it up first), and nobody else can grab it although it lies on the floor. Set `MaxHeld` to 99 and drop the cap's words from parts 1, 4 and 6.
   - Mirror the drop in the state (the right-hand prop becomes free, as on stage): about 15 more nodes in `Accept`, with the props' `Wear` and slots tracked; a give played late can still swap which prop drops.
3. **The Done-when's hand-played screenshot of a robot that throws a prop it grabbed on an earlier turn.** In Test for Free, my seat makes no action (free mode's input step only echoes my text as speech), and a free bot throws a prop it holds very rarely (it picks a random prop: by my estimate, well under once per show).
   - **Play scene 1 of the PIE show through the relay (Recommended), about $0.20 to $0.40 of relay credit.** My seat types "grab the <prop>", then "throw the <prop> at @<name>" (the input LLM still turns typing into actions until T63), and the AIs are real models, so the same scene shows whether they follow the new rules and read `holding`. No free run can show that. The look at a prop comes from the free autoplay show or the same scene.
   - Test for Free only: replay free shows until a free bot throws a prop it holds. Likely many runs.
   - Leave the throw screenshot to T64, whose Done-when already has my robot throw a prop it grabbed the turn before, and close T62 without it.
4. **Two card wants ask for a snatch, which T62 removes.** In `scenes.json`, the fellowship card's homebody wants to "snatch the ring back from anyone else who gets hold of it", and the vain elf wants to "take the water bucket away from anyone who might splash you". After T62 a grab of a held prop fails, so an AI that chases either want falls back to a look around.
   - **Reword both in T62 (Recommended),** in the doc's Stories tab first if it holds the wants, then in `scenes.json` (outside T62's Touches): "Grab the cursed ring, cross the Riser bridge to Right, and talk anyone who gets hold of it into giving it back." and "Keep your hair perfect in the footlights at Front, and talk anyone holding the water bucket into handing it to you." Why: a want the rules forbid makes the AI that holds it look broken, and the new wants still give the same scene (the ring changes hands by a give).
   - Leave them; the bots fall back, and a later story task rewords them.

## Decisions this sheet makes (open to change)

1. **The rule state lives in `BP_StageDirector`,** next to the stage it describes, and `BP_Show` reaches it through one-node helpers (the build note "New systems get their own Blueprint"). T64's builder and T63's send call the director directly.
2. **Names match with the stage's own tolerance:** any case, and a name that ends a listed name counts ("rose" finds "plastic rose", "Table" finds "Prop Table"), as `FindMark` and `BP_Prop.NameIs` do today (`Match`).
3. **`BuildDoes` keeps building up to two actions,** so `AcceptDoes` can see the extra one and print `NHOS: EXTRA`. An AI that sends three still shows `1 dropped` (BuildDoes cut the third). `BuildDoes` has no file, and this keeps it untouched.
4. **The fallback prints at log time** in `Fallback`'s form, `NHOS: ACT <id> look around - (<why>: <part>)`, with the rule as `<why>`. At play time the robot's look around prints a second, plain `NHOS: ACT <id> look around - -`.
5. **The rules' reasons** are distinct from `Fallback`'s ("unknown target", "unknown place", "unknown prop"), so the checker can count rule fallbacks: `no such prop`, `someone holds it`, `hands full`, `not holding it`, `not a place`, `not an actor, a prop or a place`, `not an actor or a place`, `not an actor`, `their hands are full`, `unknown verb`, `cut`, `unknown actor`.
6. **A throw frees the prop wherever it lands,** at an actor or a place.
7. **Free mode:** scene turns take `[0, 1]` actions (so No action gets tested too), reactions none, and a new `look {prop}` action (weight 1) so free shows look at props.
8. **New check lines:** `NHOS: RULES scene ...` (each Scene Prep), `NHOS: RULES out <id>` (a cut), `NHOS: HOLD <prop> <id or ->` (each accepted grab, throw or give), `NHOS: EXTRA <id> <n> dropped`, `NHOS: RULE ...` (the Done-when's cases, from `PrintRule`), and `NHOS: YOU <name> you=<json>` (the `you` object an AI reads, once per AI on turn 2 of each scene).
9. **The input LLM's prompt doesn't change here.** It still turns my typing into 0 to 2 actions until T63 rewrites it; `AcceptDoes` keeps the first and checks it like any AI's.

## Wording that comes from the task or the doc

- **The two Bot Prompts lines** (part 1b), which `game` copies word for word (part 4b), are this sheet's wording of the task's "My answers": one action a turn, grab only a prop nobody holds, throw or give only a prop you hold, the AIs see who holds what. "Look around and No action" and "the same set" are the doc's.
- **The Rules sentences** (part 1a) list the task's rules in the Rules tab's own form ("Actions: ...").
- **`holding`** is the task's field name. "0 or 1" is the task's.

## 0. Before you start (after T58 is pushed)

1. `git log --oneline -8` shows T54, T55, T57 and T58; `Docs/claims/T58` is released; `git lfs locks` shows no lock on `BP_Show.uasset` or `BP_StageDirector.uasset`. Claim T62, lock both. **`BP_Prop.uasset` isn't changed** (decision 1), so don't lock it.
2. Read the findings in `T54.md`, `T55.md`, `T57.md`, `T58.md` and, if it has landed, `T45.md`. Note anything they say about `ActorState`, `PlayTurn`, `PlayReact`, `CutActor`, `StagePrep` or `HandleReply`. This sheet assumes none of them changed how a scene turn's `does` is built.
3. `git log --oneline -3 -- Graphs/BP_StageDirector Graphs/BP_Show/StagePrep.txt`: if T45 changed `ResetStage.txt` or `StagePrep.txt`, start from those files (part 3e).
4. `python Tools/check_prompts.py --offline` passes before you start (T58 left 67 jobs), so any failure afterward is T62's.
5. **Ask my person for the two OKs at the start,** each typed in this session: the doc edits (part 1) and the relay deploy (part 5). With both, T62 is one commit; without the deploy OK, `--relay --free` can't pass (part 7b), so T62 can't close.
6. **Survey, in this order** (each a separate `call_tool`; calls stop at about 120 s; save each read to `Saved/T62/<graph>.read.txt`; never write a read-back to the editor):
   1. **`StoreTurn`, `PlayTurn`, `BuildDoes`** (`read_graph_dsl` each). Record: the variable that holds each seat's `does` between `StoreTurn` and `PlayTurn` (expected a String array by seat, called `TurnDoes` below), how `StoreTurn` indexes it (by seat, or by the pending index), `PlayTurn`'s loop over the shuffled seats and the first exec node of its body, and every node that reads the stored `does` in the body (expected `MakeEntry`, `ShowLine` and the `NHOS: LOG` print). T07: "`BuildDoes` uses at most 2 actions. `look` with an empty target is `look_around`. ... No actions give `does_templates.nothing`".
   2. **`PlayReact`.** Record how `does` is made (T10: "`does` from `BuildDoes` (or "passes")", maybe a `Select` on `Pass`), and each node that reads it. T29 found dead `AddLogLine` chains in it; trace from the function entry.
   3. **`PlayTalk`.** Confirm it logs "stands still" or "passes" and ignores the reply's actions (T19: "Since T26 ... `PlayTalk` logs "stands still""). T58's last words go through it. If it calls `BuildDoes` after all, it gets a `CheckDoes(..., 0)` too, as `PlayReact` does.
   4. **`ActorState`**, traced from `K2Node_FunctionEntry_0` (T50: two orphan copies of its chain sit under the live one; use `find_nodes` with `entry_points_only`, then follow the exec wires). Record: the `Set Field` nodes of each cast entry (`name`, `role`, `want`, `status`) and of `you` (`name`, `role`, `want`, `note`), the loop index of the cast loop, how a String array goes into a field (`options` or `set`), where `set` comes from (expected the `SetObj` variable, T45), and how T53 turned the `show` object into the string it gives `StateLine`.
   5. **Where a seat is marked cut:** `find_nodes` in `BP_Show` for `Set SeatCut` and for `SetArrayElem` (full class paths, T30). Expected in `CutActor` (which runs at the cut cue, T30). Record the graph and the node.
   6. **`RestartShow`:** does it clear `SeatCut` before `StagePrep` runs? `StageRules` hands the director `SeatCut` (part 3e).
   7. **Callers:** `find_nodes` in `BP_StageDirector` for `BotCands` (expected only `DoVerb`), `PlayPart` (only `PlayLine`) and `DoVerb` (only `PlayPart`).
   8. **Function outputs:** `describe_toolset` for `BlueprintTools`: how `add_function_param` makes an output and an array (`container_type` `ARRAY`, T30). `CanDo` needs two outputs, `Ok` (Boolean) and `Why` (String); `ItemsFor`, `TargetsFor` and `HoldingOf` return String arrays.

## 1. The design doc (step 1): show my person, edit after the OK

Read each tab again on the day; the revisions below are what this sheet read. **Rules and Tech & Build hold pending suggestions from T44's session** (the scene card example and the build list's card line, 15:16Z): leave them for my person, and don't edit inside them. Edit with the Claude Docs connector after my person's OK (the plan's "The design doc follows the game"). An edit must follow what the doc already has (T30's closing): these add sentences to bullets that exist and lines to the block that exists.

**a. Rules tab, "The Scene & acting"** (rev 42):

- The bullet `Actions: Move, Look, Grab, Throw, Give, Look around and No action. The AIs and you choose from the same set.` becomes:
  `Actions: Move, Look, Grab, Throw, Give, Look around and No action. The AIs and you choose from the same set, by the same rules: one action a turn; Grab takes a prop nobody holds; Throw and Give need a prop you hold; Look can take an actor, a prop or a place; Move goes only to a place. Nobody holds more than two props. The AIs see who holds what.`
  (Question 2 "no limit": drop `Nobody holds more than two props.`)
- The bullet `If an AI’s command can’t be understood, that actor just looks around, and no error appears in the log. Your builder can’t send an invalid action, but an unfinished one becomes “looks around” when the timer runs out.` becomes:
  `If an AI’s command can’t be understood or breaks a rule, that actor just looks around, and no error appears in the log. Your builder can’t send an invalid action, but an unfinished one becomes “looks around” when the timer runs out.`

**b. Bot Prompts tab, "Opening prompt: game rules"** (rev 82): two lines at the end of the code block, after `- The set is a clay opera-house stage. ...`:

```
- Every actor, the human too, takes at most one action a turn: grab only a prop nobody holds, throw or give only a prop you hold, and hold two props at most. "holding" in the state shows who holds what. An action that breaks a rule fails, and the robot only looks around.
- Only scene turns have actions. Free Talk, last words and reactions are speech only.
```

(Question 2 "no limit": the first line reads `... grab only a prop nobody holds, and throw or give only a prop you hold. "holding" ...`.) These two lines are the "Fill:" change too: the tab holds no ask texts, so the rule goes into the block the tab already has, and `asks` follow it in part 4c.

**c. Turn Input tab** (rev 1), only with question 2's recommended answer:

- `Grab: a prop nobody is holding` → `Grab: a prop nobody is holding, while you hold fewer than two`
- `Give: a prop you’re holding, then an actor` → `Give: a prop you’re holding, then an actor whose hands aren’t full`
- At the end of `The builder offers only moves the game would accept from an AI, ... with the tip “Grab something first.”` add: ` Holding two greys out Grab, with the tip “Your hands are full.”`

**d. Checked and left:** Tech & Build already lists "AI action set: add Look around and No action, so the AIs and the player share one set" (T62's "0 or 1" does it: no action is "stands still", a look with no target is "looks around"), and "Input LLM: spelling fixes for speech only" (T63's). The Turn Input tab's other lines match T62.md's spec. Overview wasn't read for this; skim it for "action".

**e. Stories tab** (question 4, if my person says reword): the two wants, if the tab lists them.

## 2. `BP_StageDirector`

### 2a. Graphs and files

| Graph | File in `Graphs/BP_StageDirector/` | T62 | How |
|---|---|---|---|
| `Match`, `IdOf`, `HeldCount`, `IsTarget`, `ItemCheck`, `TargetCheck`, `CanDo`, `ItemsFor`, `TargetsFor`, `HoldingOf`, `Accept`, `SetScene`, `SetOut`, `ParsePart`, `AcceptPart`, `AcceptDoes`, `PrintRule` | new | new | `add_function_graph`, params, compile, then write each file (2c). |
| `PlayPart` | `PlayPart.txt` | its reading moves to `ParsePart` | Rewrite from the file (2d). |
| `DoVerb` | `DoVerb.txt` | a look at a prop; no move to an actor; no put-down | Rewrite from the file (2e). |
| `BotCands` | `BotCands.txt` | gone | Delete the graph if the tools can (else leave it unused and say so), and `git rm` the file. |
| `PlayLine`, `ResetStage`, `Fallback`, `FindProp`, `FindMark`, `FindBot`, `Clean`, `Act`, `Init` | yes | nothing | `ResetStage` as T45 leaves it. |

**New variables:** `RNames`, `RIds`, `RProps`, `RPlaces`, `RList`, `RHeld` (String arrays); `ROut` (Boolean array); `HoldBy` (Integer array: for each `RProps` entry, the seat that holds it, or -1); `RCount`, `AKept`, `ADrop` (Integer); `MaxHeld` (Integer, default **2**; 99 for question 2's "no limit"); `PPart`, `AOut` (String).

**Order** (T18 and T54: a call node goes stale when its function gets a new parameter, so create and compile a function before anything calls it): the variables; `Match`, `IdOf`, `HeldCount`, `IsTarget`; `ItemCheck`, `TargetCheck`; `CanDo`; `ItemsFor`, `TargetsFor`, `HoldingOf`; `Accept`; `SetScene`, `SetOut`; `ParsePart`, then `PlayPart`; `AcceptPart`, `AcceptDoes`, `PrintRule`; `DoVerb`; delete `BotCands`. Compile and save after each group.

**Params** (inputs unless marked):

| Function | Params | Returns |
|---|---|---|
| `Match` | `List` (String array), `Name` (String) | Integer |
| `IdOf`, `HeldCount`, `HoldingOf`, `SetOut`, `AcceptPart` | `Seat` (Integer) | String / Integer / String array / none / none |
| `IsTarget` | `Seat`, `S` (Integer) | Boolean |
| `ItemCheck` | `Seat` (Integer), `Verb`, `Item` (String) | String |
| `TargetCheck` | `Seat` (Integer), `Verb`, `Target` (String) | String |
| `CanDo`, `Accept`, `PrintRule` | `Seat` (Integer), `Verb`, `Item`, `Target` (String) | `Ok` (Boolean), `Why` (String) / none / none |
| `ItemsFor`, `TargetsFor` | `Seat` (Integer), `Verb` (String) | String array |
| `SetScene` | `Names`, `Ids` (String arrays), `Out` (Boolean array), `Props`, `Places` (String arrays) | none |
| `ParsePart` | `Part` (String) | none |
| `AcceptDoes` | `Seat` (Integer), `Does` (String), `Max` (Integer) | String |

### 2b. The rules in one place: what each function answers

Names are Player names, prop names and place names, as a reply writes them. Seats are `BP_Show` seat indexes (`SeatName[Seat]` is the seat's Player name).

- **`ItemsFor(Seat, Verb)`:** grab: the card's props (`RProps`, the state's `set.props`) that nobody holds, if the seat holds fewer than `MaxHeld`. throw and give: the props the seat holds. Any other verb: none.
- **`TargetsFor(Seat, Verb)`:** move: the places. look: the actors still on stage other than the seat, the card's props and the places (the spec's order: actor, prop, place). throw: the actors on stage other than the seat, and the places. give: the actors on stage other than the seat who hold fewer than `MaxHeld`. Any other verb: none.
- **`CanDo(Seat, Verb, Item, Target) → Ok, Why`:** a look with no target is a look around: yes. A verb other than move, look, grab, throw or give: no. Otherwise yes exactly when the item passes `ItemCheck` and the target passes `TargetCheck`, which hold the same rules as `ItemsFor` and `TargetsFor` but name the rule that fails. A verb's unused field is ignored. **None of the three reads a reply's text**, so T63 and T64 call them with fields.
- **Who holds what** (`HoldBy`) changes only in three places: `SetScene` (every Scene Prep and Restart: nobody holds anything, as `ResetStage` sends every prop home), `Accept` (an accepted grab, throw or give), and `SetOut` (a cut: the seat drops everything and can't be a target). Nothing reads a `BP_Prop`'s `Slot` or `Holder` (the animation, which plays later).

### 2c. The new functions

`Graphs/BP_StageDirector/Match.txt`:

```lisp
; T62: the index of Name in List, or -1. The stage's own tolerance (FindMark, BP_Prop.NameIs): any case,
; and a name that ends a listed name counts ("rose" finds "plastic rose", "Table" finds "Prop Table").
(fn Match (List Name)
  (if (Utilities|String|IsEmpty Name)
    (return -1))
  (for _i (range (len List))
    (bind _n (get List _i))
    (if (or (Utilities|String|Equal,CaseInsensitive(String) :A _n :B Name) (Utilities|String|EndsWith :SourceString _n :InSuffix (cat " " Name)))
      (return _i)))
  (return -1))
```

`IdOf.txt`:

```lisp
; T62: the seat's id for check lines, or "?" when the seat isn't in the rules' state.
(fn IdOf (Seat)
  (if (or (< Seat 0) (>= Seat (len (V RIds))))
    (return "?"))
  (return (get (V RIds) Seat)))
```

`HeldCount.txt`:

```lisp
; T62: how many of the card's props the seat holds now (HoldBy).
(fn HeldCount (Seat)
  (set RCount 0)
  (for _h (V HoldBy)
    (if (== _h Seat)
      (set RCount (+ (V RCount) 1))))
  (return (V RCount)))
```

`IsTarget.txt`:

```lisp
; T62: true when seat S is an actor that Seat may target: another seat, still on stage.
(fn IsTarget (Seat S)
  (if (or (< S 0) (or (== S Seat) (>= S (len (V ROut)))))
    (return false))
  (return (not (get (V ROut) S))))
```

`ItemCheck.txt`:

```lisp
; T62: CanDo's item rule, with the reason it fails. Same rule as ItemsFor. Every branch ends in return (T30).
(fn ItemCheck (Seat Verb Item)
  (if (not (or (streq Verb "grab") (or (streq Verb "throw") (streq Verb "give"))))
    (return "ok"))
  (bind _pi (CallFunction|Match :List (V RProps) :Name Item))
  (if (< _pi 0)
    (return "no such prop"))
  (bind _h (get (V HoldBy) _pi))
  (if (streq Verb "grab")
    (if (>= _h 0)
      (return "someone holds it"))
    (bind _n (CallFunction|HeldCount :Seat Seat))
    (if (>= _n (V MaxHeld))
      (return "hands full"))
    (return "ok"))
  (if (!= _h Seat)
    (return "not holding it"))
  (return "ok"))
```

`TargetCheck.txt`:

```lisp
; T62: CanDo's target rule, with the reason it fails. Same rule as TargetsFor.
(fn TargetCheck (Seat Verb Target)
  (if (streq Verb "grab")
    (return "ok"))
  (if (and (streq Verb "look") (Utilities|String|IsEmpty Target))
    (return "ok"))
  (bind _pl (CallFunction|Match :List (V RPlaces) :Name Target))
  (bind _se (CallFunction|Match :List (V RNames) :Name Target))
  (bind _pr (CallFunction|Match :List (V RProps) :Name Target))
  (bind _act (CallFunction|IsTarget :Seat Seat :S _se))
  (if (streq Verb "move")
    (if (>= _pl 0)
      (return "ok"))
    (return "not a place"))
  (if (streq Verb "look")
    (if (or (>= _pl 0) (or _act (>= _pr 0)))
      (return "ok"))
    (return "not an actor, a prop or a place"))
  (if (streq Verb "throw")
    (if (or (>= _pl 0) _act)
      (return "ok"))
    (return "not an actor or a place"))
  (if (not _act)
    (return "not an actor"))
  (bind _hc (CallFunction|HeldCount :Seat _se))
  (if (>= _hc (V MaxHeld))
    (return "their hands are full"))
  (return "ok"))
```

`CanDo.txt`:

```lisp
; T62: the one check for every actor's action, mine and the AIs' (AcceptDoes before the shared log,
; T63's built action). A look with no target is a look around, always allowed. Why is "ok" or the rule.
(fn CanDo (Seat Verb Item Target)
  (if (and (streq Verb "look") (Utilities|String|IsEmpty Target))
    (return true "ok"))
  (if (not (or (streq Verb "move") (or (streq Verb "look") (or (streq Verb "grab") (or (streq Verb "throw") (streq Verb "give"))))))
    (return false "unknown verb"))
  (if (or (< Seat 0) (or (>= Seat (len (V RNames))) (>= Seat (len (V ROut)))))
    (return false "unknown actor"))
  (if (get (V ROut) Seat)
    (return false "cut"))
  (bind _iw (CallFunction|ItemCheck :Seat Seat :Verb Verb :Item Item))
  (if (not (streq _iw "ok"))
    (return false _iw))
  (bind _tw (CallFunction|TargetCheck :Seat Seat :Verb Verb :Target Target))
  (if (not (streq _tw "ok"))
    (return false _tw))
  (return true "ok"))
```

- `(return true "ok")` fills the two outputs in order, as `BP_Show.LineInfo` returns two values (`Graphs/BP_Show/LineInfo.txt`, read by `BPC_LinePlayer.Push` with `(bind (_id _ty) ...)`). Check the read-back's output names: `Ok` and `Why`.
- **No `if` without `return` comes after an `if` with one** (T30's rule), so every branch joins. Each check that needs a called function's result binds it first (T19: functions made with `add_function_graph` are impure).

`ItemsFor.txt`:

```lisp
; T62: the props a verb may use (T64's chips). grab: the card's props nobody holds, while the seat holds
; fewer than MaxHeld. throw, give: the props the seat holds. Any other verb: none.
(fn ItemsFor (Seat Verb)
  (clear (V RList))
  (bind _n (CallFunction|HeldCount :Seat Seat))
  (if (and (streq Verb "grab") (< _n (V MaxHeld)))
    (for _i (range (len (V RProps)))
      (if (< (get (V HoldBy) _i) 0)
        (add (V RList) (get (V RProps) _i)))))
  (if (or (streq Verb "throw") (streq Verb "give"))
    (for _j (range (len (V RProps)))
      (if (== (get (V HoldBy) _j) Seat)
        (add (V RList) (get (V RProps) _j)))))
  (return (V RList)))
```

`TargetsFor.txt`:

```lisp
; T62: the targets a verb may use (T64's chips). move: the places. look: the actors on stage but the seat,
; the card's props, the places. throw: the actors on stage but the seat, the places. give: the actors on
; stage but the seat who hold fewer than MaxHeld. Any other verb: none.
(fn TargetsFor (Seat Verb)
  (clear (V RList))
  (bind _look (streq Verb "look"))
  (bind _throw (streq Verb "throw"))
  (bind _give (streq Verb "give"))
  (if (or _look (or _throw _give))
    (for _s (range (len (V RNames)))
      (bind _ok (CallFunction|IsTarget :Seat Seat :S _s))
      (bind _hc (CallFunction|HeldCount :Seat _s))
      (if (and _ok (or (not _give) (< _hc (V MaxHeld))))
        (add (V RList) (get (V RNames) _s)))))
  (if _look
    (for _p (V RProps)
      (add (V RList) _p)))
  (if (or (streq Verb "move") (or _look _throw))
    (for _m (V RPlaces)
      (add (V RList) _m)))
  (return (V RList)))
```

`HoldingOf.txt`:

```lisp
; T62: the props the seat holds, for the state's "holding" (BP_Show.HeldBy) and T64's preview.
(fn HoldingOf (Seat)
  (clear (V RHeld))
  (for _i (range (len (V RProps)))
    (if (== (get (V HoldBy) _i) Seat)
      (add (V RHeld) (get (V RProps) _i))))
  (return (V RHeld)))
```

`Accept.txt`:

```lisp
; T62: who holds what, as an accepted action leaves it. AcceptPart calls it after CanDo says yes.
; grab: the seat holds it. throw: nobody (it lands free). give: the target holds it.
(fn Accept (Seat Verb Item Target)
  (bind _pi (CallFunction|Match :List (V RProps) :Name Item))
  (if (< _pi 0)
    (return))
  (bind _to (CallFunction|Match :List (V RNames) :Name Target))
  (bind _who (select (streq Verb "grab") Seat (select (streq Verb "give") _to -1)))
  (bind _hid (CallFunction|IdOf :Seat _who))
  (if (or (streq Verb "grab") (or (streq Verb "throw") (streq Verb "give")))
    (Utilities|Array|SetArrayElem (V HoldBy) _pi _who)
    (print (cat "NHOS: HOLD " (get (V RProps) _pi) " " (select (< _who 0) "-" _hid)))))
```

`SetScene.txt`:

```lisp
; T62: the rules' state for a new scene: Player names, seat ids, who is cut, the card's props and the places,
; as the AIs read them. Nobody holds anything: ResetStage sends every prop home. BP_Show.StageRules calls it
; at every Scene Prep and Restart, right after ResetStage.
(fn SetScene (Names Ids Out Props Places)
  (set RNames Names)
  (set RIds Ids)
  (set ROut Out)
  (set RProps Props)
  (set RPlaces Places)
  (clear (V HoldBy))
  (for _p (V RProps)
    (add (V HoldBy) -1))
  (set RCount 0)
  (for _o (V ROut)
    (if _o
      (set RCount (+ (V RCount) 1))))
  (print (cat "NHOS: RULES scene seats=" (str (len (V RNames))) " out=" (str (V RCount)) " props=" (Utilities|String|JoinStringArray :SourceArray (V RProps) :Separator ", ") " places=" (Utilities|String|JoinStringArray :SourceArray (V RPlaces) :Separator ", "))))
```

`SetOut.txt`:

```lisp
; T62: a cut actor leaves the rules: it drops what it holds (as BP_Robot.DropAll does on stage), and nobody
; can target it. BP_Show.RuleOut calls it where the cut seat is marked cut.
(fn SetOut (Seat)
  (if (and (>= Seat 0) (< Seat (len (V ROut))))
    (Utilities|Array|SetArrayElem (V ROut) Seat true)
    (for _i (range (len (V HoldBy)))
      (if (== (get (V HoldBy) _i) Seat)
        (Utilities|Array|SetArrayElem (V HoldBy) _i -1)))
    (bind _id (CallFunction|IdOf :Seat Seat))
    (print (cat "NHOS: RULES out " _id))))
```

`ParsePart.txt` (the first half of today's `PlayPart`, word for word, with `_p` held in `PPart`):

```lisp
; T62: PlayPart's reading of one does part, split out so AcceptDoes reads a part exactly as PlayPart plays it.
; Sets PPart (trimmed), PVerb (move, look, around, vote, grab, throw, give, or "" for "stands still" and
; "passes"), PTgt and PItem (cleaned). It reads the does_templates wording (T19), so change both together.
(fn ParsePart (Part)
  (set PPart (Utilities|String|TrimTrailing (Utilities|String|Trim Part)))
  (set PVerb "")
  (set PTgt "")
  (set PItem "")
  (if (Utilities|String|StartsWith :SourceString (V PPart) :InPrefix "moves to ")
    (set PVerb "move")
    (set PTgt (Utilities|String|RightChop :SourceString (V PPart) :Count 9)))
  (if (Utilities|String|Equal,CaseInsensitive(String) :A (V PPart) :B "looks around")
    (set PVerb "around"))
  (if (Utilities|String|StartsWith :SourceString (V PPart) :InPrefix "looks at ")
    (set PVerb "look")
    (set PTgt (Utilities|String|RightChop :SourceString (V PPart) :Count 9)))
  (if (Utilities|String|StartsWith :SourceString (V PPart) :InPrefix "votes for ")
    (set PVerb "vote")
    (set PTgt (Utilities|String|RightChop :SourceString (V PPart) :Count 10)))
  (if (Utilities|String|StartsWith :SourceString (V PPart) :InPrefix "grabs the ")
    (set PVerb "grab")
    (set PItem (Utilities|String|RightChop :SourceString (V PPart) :Count 10)))
  (if (Utilities|String|StartsWith :SourceString (V PPart) :InPrefix "throws the ")
    (set PVerb "throw")
    (bind (_tl _tr _tok) (Utilities|String|Split :SourceString (Utilities|String|RightChop :SourceString (V PPart) :Count 11) :InStr " at " :SearchDir "FromEnd"))
    (set PItem _tl)
    (set PTgt _tr))
  (if (Utilities|String|StartsWith :SourceString (V PPart) :InPrefix "gives the ")
    (set PVerb "give")
    (bind (_gl _gr _gok) (Utilities|String|Split :SourceString (Utilities|String|RightChop :SourceString (V PPart) :Count 10) :InStr " to " :SearchDir "FromEnd"))
    (set PItem _gl)
    (set PTgt _gr))
  (if (Utilities|String|IsEmpty (V PVerb))
    (return))
  (bind _ct (CallFunction|Clean :S (V PTgt)))
  (set PTgt _ct)
  (bind _ci (CallFunction|Clean :S (V PItem)))
  (set PItem _ci))
```

`AcceptPart.txt`:

```lisp
; T62: one parsed part (ParsePart's PVerb, PItem, PTgt) is checked: a yes keeps it and changes who holds
; what; a no becomes "looks around" and prints the rule, in Fallback's form. "looks around" itself passes.
(fn AcceptPart (Seat)
  (bind _sep (select (Utilities|String|IsEmpty (V AOut)) "" "; "))
  (if (streq (V PVerb) "around")
    (set AOut (cat (V AOut) _sep "looks around"))
    (return))
  (bind (_ok _why) (CallFunction|CanDo :Seat Seat :Verb (V PVerb) :Item (V PItem) :Target (V PTgt)))
  (if _ok
    (CallFunction|Accept :Seat Seat :Verb (V PVerb) :Item (V PItem) :Target (V PTgt))
    (set AOut (cat (V AOut) _sep (V PPart)))
    (return))
  (bind _id (CallFunction|IdOf :Seat Seat))
  (print (cat "NHOS: ACT " _id " look around - (" _why ": " (V PPart) ")"))
  (set AOut (cat (V AOut) _sep "looks around")))
```

`AcceptDoes.txt`:

```lisp
; T62: the step between a reply and the shared log, for every actor's scene turn (Max 1) and reaction (Max 0),
; through BP_Show.CheckDoes. Keeps the first Max actions, prints NHOS: EXTRA for the rest, and checks each
; kept one (AcceptPart). With no action kept, "passes" and "stands still" stay; dropped actions leave "stands still".
(fn AcceptDoes (Seat Does Max)
  (set AOut "")
  (set AKept 0)
  (set ADrop 0)
  (bind _parts (Utilities|String|ParseIntoArray :SourceString Does :Delimiter "; " :CullEmptyStrings true))
  (for _p _parts
    (CallFunction|ParsePart :Part _p)
    (if (not (Utilities|String|IsEmpty (V PVerb)))
      (if (< (V AKept) Max)
        (set AKept (+ (V AKept) 1))
        (CallFunction|AcceptPart :Seat Seat)
        (else
          (set ADrop (+ (V ADrop) 1))))))
  (bind _id (CallFunction|IdOf :Seat Seat))
  (if (> (V ADrop) 0)
    (print (cat "NHOS: EXTRA " _id " " (str (V ADrop)) " dropped")))
  (if (== (V AKept) 0)
    (return (select (> (V ADrop) 0) "stands still" Does)))
  (return (V AOut)))
```

- "stands still" and "looks around" are literals here, as in `PlayPart` today (T19's note: a `does_templates` change needs the same change in the director). Part 6d's file check fails if the templates move.
- `PVerb` "vote" would count as an action, but nothing calls `AcceptDoes` on a vote (`Tally` doesn't).
- `ParsePart`, `AcceptPart` and `PlayPart` share `PVerb`, `PTgt`, `PItem` and `PPart`. They never overlap: `AcceptDoes` runs inside `BP_Show`'s logic, `PlayPart` inside a line's play, both whole on the game thread.

`PrintRule.txt`:

```lisp
; T62: a check line for the Done-when's CanDo cases, run through Unreal MCP in a PIE show (part 7c). The game never calls it.
(fn PrintRule (Seat Verb Item Target)
  (bind (_ok _why) (CallFunction|CanDo :Seat Seat :Verb Verb :Item Item :Target Target))
  (print (cat "NHOS: RULE " Verb " " (select (Utilities|String|IsEmpty Item) "-" Item) " " (select (Utilities|String|IsEmpty Target) "-" Target) " = " (select _ok "yes" "no") " " _why)))
```

**Forms used, each in a pushed source:** `(for _i (range (len List)))` and `(get List _i)` on a param (`PlayLine.txt`'s `Robots`); `Equal,CaseInsensitive(String)` and `EndsWith` (`FindMark.txt`); `SetArrayElem` (`BP_Show/StagePrep.txt`); `JoinStringArray :SourceArray :Separator` (T45-build's `ResetStage`); two returns (`BP_Show/LineInfo.txt`); `(bind (a b) ...)` (`PlayPart.txt`'s `Split`); `(if ... (else ...))` inside a loop (T45-build's `ResetStage`); `(return -1)` is new: if the DSL won't take a negative literal, write `(- 0 1)`.

### 2d. `PlayPart` (rewrite)

```lisp
; T62: the reading moved to ParsePart, which AcceptDoes shares. The part was checked before the shared log
; (BP_Show.CheckDoes), so this only plays it.
(fn PlayPart (Part)
  (CallFunction|ParsePart :Part Part)
  (if (Utilities|String|IsEmpty (V PVerb))
    (return))
  (CallFunction|DoVerb :Part (V PPart)))
```

### 2e. `DoVerb` (rewrite from `DoVerb.txt`)

Three changes, marked `; T62`; the rest is the file word for word.

```lisp
; T62: plays one action that AcceptDoes already checked (CanDo). A look finds a place, an actor or a prop;
; a move goes only to a place (the move to an actor, BotCands, is gone); a give goes only to an actor (the
; put-down is gone). Fallback stays for a name the stage can't find.
(fn DoVerb (Part)
  (if (streq (V PVerb) "around")
    (Class|BPRobot|LookAround :self (V CurBot))
    (CallFunction|Act :Verb "look" :Target "around" :Item "" :Note "")
    (return))
  (bind _isMark (CallFunction|FindMark :Name (V PTgt)))
  (bind _isBot (CallFunction|FindBot :Name (V PTgt)))
  (if (or (streq (V PVerb) "look") (streq (V PVerb) "vote"))
    (if _isMark
      (bind _ml (Transformation|GetActorLocation :self (V TgtMark)))
      (Class|BPRobot|LookAt :self (V CurBot) :Target _ml)
      (CallFunction|Act :Verb "look" :Target (V PTgt) :Item "" :Note "")
      (return))
    (if _isBot
      (bind _bl (Class|BPRobot|GetGoal :self (V TgtBot)))
      (Class|BPRobot|LookAt :self (V CurBot) :Target _bl)
      (CallFunction|Act :Verb "look" :Target (V PTgt) :Item "" :Note "")
      (return))
    ; T62: a look at a prop turns the robot toward the prop, wherever it is (on the table, the floor or in a hand).
    (bind _isLookProp (CallFunction|FindProp :Name (V PTgt)))
    (if _isLookProp
      (bind _pl (Transformation|GetActorLocation :self (V TgtProp)))
      (Class|BPRobot|LookAt :self (V CurBot) :Target _pl)
      (CallFunction|Act :Verb "look" :Target (V PTgt) :Item "" :Note "")
      (return))
    (CallFunction|Fallback :Part Part :Why "unknown target")
    (return))
  (if (streq (V PVerb) "move")
    ; T62: a move goes only to a place.
    (if (not _isMark)
      (CallFunction|Fallback :Part Part :Why "unknown place")
      (return))
    (CallFunction|MarkCands)
    (bind _ok (CallFunction|PickSpot))
    (if _ok
      (Class|BPRobot|MoveTo :self (V CurBot) :Dest (V Pick))
      (CallFunction|Act :Verb "move" :Target (V PTgt) :Item "" :Note "")
      (return))
    (bind _c0 (get (V Cands) 0))
    (Class|BPRobot|LookAt :self (V CurBot) :Target _c0)
    (CallFunction|Act :Verb "look" :Target (V PTgt) :Item "" :Note " (no free spot)")
    (return))
  (bind _isProp (CallFunction|FindProp :Name (V PItem)))
  (if (not _isProp)
    (CallFunction|Fallback :Part Part :Why "unknown prop")
    (return))
  (if (streq (V PVerb) "grab")
    (Class|BPRobot|Grab :self (V CurBot) :Prop (V TgtProp))
    (CallFunction|Act :Verb "grab" :Target "" :Item (V PItem) :Note "")
    (return))
  (if (streq (V PVerb) "throw")
    (if _isBot
      (bind _tg (Class|BPRobot|GetGoal :self (V TgtBot)))
      (bind _me (Transformation|GetActorLocation :self (V CurBot)))
      (bind _len (Math|Vector|Distance2D(Vector) :V1 _me :V2 _tg))
      (bind _f (/ 70.0 (select (> _len 1.0) _len 1.0)))
      (set LandLoc (Math|Vector|MakeVector :X (+ (.x _tg) (* (- (.x _me) (.x _tg)) _f)) :Y (+ (.y _tg) (* (- (.y _me) (.y _tg)) _f)) :Z (.z _tg)))
      (Class|BPRobot|Throw :self (V CurBot) :Prop (V TgtProp) :Target (V LandLoc) :Hit (V TgtBot))
      (CallFunction|Act :Verb "throw" :Target (V PTgt) :Item (V PItem) :Note "")
      (return))
    (if _isMark
      (bind _ml2 (Transformation|GetActorLocation :self (V TgtMark)))
      (set LandLoc (+ _ml2 (Math|Vector|MakeVector :X (Math|Random|RandomFloatinRange :Min -50.0 :Max 50.0) :Y (Math|Random|RandomFloatinRange :Min -50.0 :Max 50.0) :Z 0.0)))
      (Class|BPRobot|Throw :self (V CurBot) :Prop (V TgtProp) :Target (V LandLoc) :Hit (V NullBot))
      (CallFunction|Act :Verb "throw" :Target (V PTgt) :Item (V PItem) :Note "")
      (return))
    (CallFunction|Fallback :Part Part :Why "unknown target")
    (return))
  (if (streq (V PVerb) "give")
    ; T62: a give goes only to an actor; the put-down at a place is gone.
    (if _isBot
      (Class|BPRobot|Give :self (V CurBot) :Prop (V TgtProp) :Bot (V TgtBot))
      (CallFunction|Act :Verb "give" :Target (V PTgt) :Item (V PItem) :Note "")
      (return))
    (CallFunction|Fallback :Part Part :Why "unknown target")))
```

- **The snatch and the grab-first are gone as rules,** because `CanDo` refuses a grab of a held prop and a throw or give of a prop the actor doesn't hold. `BP_Robot` still has the animation for both (`DoGrab` takes a prop from another hand; `DoHanded` grabs first when the robot's hand is empty). They stay as a safety net, since `BP_Robot` isn't in T62's Touches: a give that an earlier line accepted may still be in flight when the next line plays.
- **`ResetStage` and `PlayLine` don't change.** Every prop goes home at Scene Prep (T45's `ResetStage` sends held ones too; before T45, a held prop goes home with its robot, `GoHome` → `ToTable`).

## 3. `BP_Show`

### 3a. Graphs and files

| Graph | File in `Graphs/BP_Show/` | T62 | How |
|---|---|---|---|
| `StageRules`, `CheckDoes`, `CheckTurn`, `HeldBy`, `RuleOut`, `HoldLine` | new | new | `add_function_graph`, params, compile, write (3b). |
| `StagePrep` | `StagePrep.txt` (T45's version if it landed) | one call after `ResetStage` | Rewrite from the file (3e). |
| `PlayTurn` | **none** | one `CheckTurn` node at the start of the loop body | Read first (0.6.1), node edit (3c). |
| `PlayReact` | **none** | one `CheckDoes` node on the `does` wire | Read first (0.6.2), node edit (3d). |
| `CutActor` | **none** | one `RuleOut` node next to the node that marks the seat cut | `find_nodes` first (0.6.5), node edit (3f). |
| `ActorState` | **none** | `holding` in each cast entry and in `you`; one `HoldLine` call | Trace from the entry (0.6.4), node edits (3g). |
| `StoreTurn`, `BuildDoes`, `HandleReply`, `PlayTalk` | **none** | nothing | Read `StoreTurn`, `BuildDoes` and `PlayTalk` for the survey only. |

**New variables:** `RulePlaces`, `RuleProps`, `HeldTmp` (String arrays), `RuleObjs` (`JsonObjectWrapper` array, `/Script/JsonUtilities.JsonObjectWrapper`, T30), `RuleStr` (String).

Write each node edit, old and new, under "Findings" in `T62.md`, since those graphs have no files.

### 3b. The new functions

`Graphs/BP_Show/StageRules.txt`:

```lisp
; T62: hands the stage director the rules' state for a new scene: Player names, seat ids, who is cut, and
; the card's props and the places as the AIs read them in "set" (SetObj; T45 writes the card's props into
; it earlier in StagePrep). StagePrep calls it right after ResetStage, at every Scene Prep and Restart.
(fn StageRules ()
  (bind _dir (Actor|GetActorOfClass :ActorClass "/Game/NHOS/Stage/BP_StageDirector.BP_StageDirector_C"))
  (if (== _dir (V NullDir))
    (return))
  (clear (V RulePlaces))
  (bind _pl (Json|GetField (V SetObj) "places"))
  (set RuleObjs _pl)
  (for _o (V RuleObjs)
    (bind _pn (Json|GetField _o "name"))
    (set RuleStr _pn)
    (add (V RulePlaces) (V RuleStr)))
  (bind _pr (Json|GetField (V SetObj) "props"))
  (set RuleProps _pr)
  (Class|BPStageDirector|SetScene :self _dir :Names (V SeatName) :Ids (V SeatId) :Out (V SeatCut) :Props (V RuleProps) :Places (V RulePlaces)))
```

- The `Json|GetField` into a typed variable is `BPC_LLMClient/FreeReply.txt`'s pattern for the same two fields. If 0.6.4 found that `set` isn't `SetObj`, read the props and places from whatever `ActorState` writes as `set`.
- `SeatName` holds the Player names (`StageLine` hands it to `PlayLine` as `SeatNames`, and `FindBot` matches Player names in it), `SeatId` the ids, `SeatCut` the cut flags (T54-build 0.4.4).

`CheckDoes.txt`:

```lisp
; T62: a scene turn's or a reaction's does passes the stage director's rules before the shared log
; (BP_StageDirector.AcceptDoes): Max 1 in a scene turn, 0 in a reaction. With no director, it goes through as it is.
(fn CheckDoes (Seat Does Max)
  (bind _dir (Actor|GetActorOfClass :ActorClass "/Game/NHOS/Stage/BP_StageDirector.BP_StageDirector_C"))
  (if (== _dir (V NullDir))
    (return Does))
  (bind _d (Class|BPStageDirector|AcceptDoes :self _dir :Seat Seat :Does Does :Max Max))
  (return _d))
```

`CheckTurn.txt` (with the variable 0.6.1 found; `TurnDoes` here):

```lisp
; T62: PlayTurn calls it first for each seat, in the shuffled log order, so "the first to play gets it" holds.
; The checked does replaces the stored one, so MakeEntry, ShowLine and the NHOS: LOG line all read it.
(fn CheckTurn (Seat)
  (bind _d (CallFunction|CheckDoes :Seat Seat :Does (get (V TurnDoes) Seat) :Max 1))
  (Utilities|Array|SetArrayElem (V TurnDoes) Seat _d))
```

If `StoreTurn` stores by pending index rather than by seat, give `CheckTurn` the index the loop reads with, and pass the seat to `CheckDoes`.

`HeldBy.txt`:

```lisp
; T62: the props a seat holds, for the state's "holding" (ActorState). Empty with no director.
(fn HeldBy (Seat)
  (clear (V HeldTmp))
  (bind _dir (Actor|GetActorOfClass :ActorClass "/Game/NHOS/Stage/BP_StageDirector.BP_StageDirector_C"))
  (if (== _dir (V NullDir))
    (return (V HeldTmp)))
  (bind _h (Class|BPStageDirector|HoldingOf :self _dir :Seat Seat))
  (return _h))
```

`RuleOut.txt`:

```lisp
; T62: a cut seat drops what it holds in the rules' state and can't be a target (BP_StageDirector.SetOut).
(fn RuleOut (Seat)
  (bind _dir (Actor|GetActorOfClass :ActorClass "/Game/NHOS/Stage/BP_StageDirector.BP_StageDirector_C"))
  (if (!= _dir (V NullDir))
    (Class|BPStageDirector|SetOut :self _dir :Seat Seat)))
```

`HoldLine.txt` (the check for step 5; its `You` param takes the `you` object as a JSON string, made the way 0.6.4 found T53 made the `show` string):

```lisp
; T62: a check line with the "you" object an AI reads, once per AI on turn 2 of each scene (turn 1 holds nothing).
; ActorState calls it next to StateLine. Never sent to an AI.
(fn HoldLine (Seat AskKey You)
  (if (and (streq AskKey "scene_turn") (== (V TurnNum) 2))
    (print (cat "NHOS: YOU " (get (V SeatName) Seat) " you=" You))))
```

This is `StateLine.txt`'s form. If making a second JSON string costs more than two nodes, skip `HoldLine` and check `holding` by reading `ActorState` back and by part 7c's `HeldBy` call.

### 3c. `PlayTurn`: one node

Add `CallFunction|CheckTurn` as the **first exec node of the loop body** over the shuffled seats, with `Seat` from the loop's seat (the array element, not the loop index, if the loop walks a shuffled list of seats). Link the loop's `Loop Body` to `CheckTurn`, and `CheckTurn`'s exec out to the node the body started with.

- The `NHOS: LOG` line then shows the checked `does`, and so does the chat (`ShowLine`), the shared log (`MakeEntry` → `ActorLine`) and the stage (`StageLine` at play time reads the entry).
- My seat goes through the same loop. Until T63, my `does` comes from the input LLM (up to two actions), so my turn can print `NHOS: EXTRA human 1 dropped` too.

### 3d. `PlayReact`: one node

Put `CallFunction|CheckDoes` with `Max` 0 and `Seat` from the function's `Seat` right after the `BuildDoes` call in the exec chain. Wire `BuildDoes`' result into `CheckDoes.Does`, and `CheckDoes`' result into whatever `BuildDoes`' result fed (expected a `Select` with "passes" on `Pass`, then `MakeEntry`, `ShowLine` and the `LOG` print). A reaction's actions then become "stands still" with `NHOS: EXTRA <id> <n> dropped`, and `ShowLine` hides "stands still" outside the scene (T14). Free mode's reactions make no actions after part 5, so `EXTRA` there comes only from a real reply or my input.

### 3e. `StagePrep`: one line

After T45 (its part 4 text), the director branch becomes:

```lisp
  (if (!= _dir (Variables|Default|GetNullDir))
    (Class|BPStageDirector|SetCard :self _dir :Names (Variables|Default|GetCardProps))   ; T45
    (Class|BPStageDirector|ResetStage :self _dir)
    (CallFunction|StageRules))                                                          ; T62: the rules' state for the new scene
```

Before T45 (today's file), the same `(CallFunction|StageRules)` goes after `ResetStage` in the `(if (!= _dir ...) ...)` branch. Everything else stays as the file has it. Write the whole graph from the file and save it.

- **Restart:** if 0.6.6 found that `RestartShow` clears `SeatCut` after `StagePrep`, the `NHOS: RULES scene ... out=` line of a restarted show shows the old cuts. Then call `StageRules` once more at the end of `RestartShow` (one node), and say so under "Findings".

### 3f. `CutActor`: one node

Put `CallFunction|RuleOut` with the cut seat right after the node that marks the seat cut (0.6.5). It runs at the cut cue (T30), before the next Scene Prep, and the reactions have no actions, so nothing reads the rules between the vote and the cut cue except the reaction asks' `holding`, which may still show the cut actor's props for that one ask. If `SeatCut` is set in `Tally` or `TieCut` instead, put the node there.

### 3g. `ActorState`: `holding`

Node edits, traced from the function entry (T50's orphan chains don't run; leave them).

1. **Each cast entry:** after the entry's `Set Field "status"` node, add a `CallFunction|HeldBy` node (impure, so it takes an exec slot) with `Seat` from the cast loop's seat index, then a `Set Field` node with the key `"holding"` and `HeldBy`'s result, on the same object as `status`. Use the same `Set Field` node type that writes a String array elsewhere in the graph (`options`), so the field is a JSON array of strings, `[]` when empty.
2. **`you`:** after `you`'s `Set Field "note"`, the same two nodes with `Seat` from the function's `Seat`.
3. **Key order** is the checker's (T06): `cast [{name, role, want, status, holding}]`, `you {name, role, want, note, holding}`.
4. **`HoldLine`:** next to T53's `StateLine` call before the return, one `CallFunction|HoldLine` with `Seat`, `AskKey` and the `you` object as a JSON string (3b).
5. Only AI seats get `ActorState` (T50). My seat's state goes through `InputState`, which T63 changes; it gets no `holding` (T64 reads `ItemsFor` instead).

## 4. `prompts.json`

Each line as it sits in the file (two tabs before it, escaped quotes as written), as T58 leaves it. Tried on a scratch copy of `d2d4cdc` together with parts 5 and 6, each edit applied by a script that stops if its anchor text isn't found exactly once: the JSON loads and `--offline` passes (part 6k).

**a. `_readme`.**

- About line 5 (T50 added `note_category`, T55 deletes the Director's sentence). Find `cast [{name, role, want, status}], you {name, role, want, note}` and make it `cast [{name, role, want, status, holding}], you {name, role, want, note, holding}`. Then, right after `ask (text from 'asks').`, add: ` 'holding' lists the props that actor holds now ([] for none), from the stage director's rules (BP_StageDirector.HoldingOf).`
- About line 6 (T58 adds `'scene 1, last word'` to it). Find `'does' is built from the reply's actions with 'does_templates', joined with '; '.` and make it: `'does' is built from the reply's actions with 'does_templates': a scene turn keeps the first action and a reaction none (NHOS: EXTRA <id> <n> dropped), and BP_StageDirector.CanDo checks the kept one against the action rules before the log; a failed check is logged as 'looks around'. No action is 'stands still'.`

**b. `game`.**

- **"Reading the state", the `you` line** (about line 43):
  - Now: `"- \"you\" is your seat: your Player name, your role, your want and the director's note (\"note\"). Only the AI actors have the note. The human's seat has none.",`
  - New: `"- \"you\" is your seat: your Player name, your role, your want, the director's note (\"note\") and the props you hold (\"holding\"). Only the AI actors have the note. The human's seat has none.",`
- **The `cast` line** (about line 44), and a new line after it:
  - Now: `"- \"cast\" lists every actor: Player name, role, want, and whether they are still on stage.",`
  - New, two lines:

```
		"- \"cast\" lists every actor: Player name, role, want, whether they are still on stage, and the props they hold (\"holding\").",
		"- \"holding\" is written by the game, so it is true. A prop in \"set\" that nobody holds is free to grab.",
```

- **The `game_messages` line** (about line 47 after the new line):
  - Now: `"- \"game_messages\" are the game's own announcements, such as reveals. Only they are true game facts.",`
  - New: `"- \"game_messages\" are the game's own announcements, such as reveals. Only they and \"holding\" are true game facts.",`
- **"How to reply", the actions block** (about lines 63 to 69 with the new line; it starts `"- \"actions\": what your robot does, 0 to 2 actions, in order.`). Replace the first line and the look line, and add the doc's two lines (part 1b) as sub-bullets after the `Use only ...` line:

```
		"- \"actions\": what your robot does: 0 or 1 action (none means your robot stands still). The action has a \"verb\", a \"target\" and an \"item\":",
		"  - move: walk to a place. target = the place.",
		"  - look: look at a place, an actor or a prop. target = the place, the actor or the prop, or \"\" to look around.",
		"  - grab: pick up a prop. item = the prop.",
		"  - throw: throw a prop. item = the prop, target = a place or an actor.",
		"  - give: hand a prop to an actor. item = the prop, target = the actor.",
		"  Use only the places, props and actor names in the state, spelled exactly. Leave target or item \"\" when the verb doesn't use it.",
		"  - Every actor, the human too, takes at most one action a turn: grab only a prop nobody holds, throw or give only a prop you hold, and hold two props at most. \"holding\" in the state shows who holds what. An action that breaks a rule fails, and the robot only looks around.",
		"  - Only scene turns have actions. Free Talk, last words and reactions are speech only.",
```

  The move, grab, throw, give and `Use only ...` lines are today's, word for word. Question 2 "no limit": the doc's first line without `, and hold two props at most` (part 1b). The `speech` line after it ("... because what your robot does goes in actions.") stays.
- **Checked and left:** goal 1 (T54), "How a show works" (T53, T58), the note lines (T50) and the silence lines (T57) name no action count. `"- The human types into a converter ..."` (about line 48) becomes untrue with T63, not T62: tell T63 (part 9).

**c. `asks`** (as T58 leaves them: `scene_turn` about line 115, `reaction` about 119, `reaction_cut` about 120):

| Key | Now (its end) | New (its end) |
|---|---|---|
| `scene_turn` | `... react to what just happened in the log. Fill: actions (1 or 2) and speech.",` | `... react to what just happened in the log. Fill: actions (0 or 1) and speech.",` |
| `reaction` | `... If an AI was cut, or nobody was, the human is still among you. Fill: speech, and at most 1 action.",` | `... If an AI was cut, or nobody was, the human is still among you. Fill: speech. No actions.",` |
| `reaction_cut` | `... Say your last words to the cast, in character. Fill: speech, and at most 1 action.",` | `... Say your last words to the cast, in character. Fill: speech. No actions.",` |

- **`last_word`** (T58): already `Fill: speech, or pass. No actions.` No change.
- **Free mode still finds each:** `free_mode.json` matches by `ask_contains`, case-sensitive: "The scene, your turn", "Reactions", "You were just cut" are untouched.

**d. `does_templates`: no change.** "looks at {target}" makes "looks at plastic rose" for a prop, `ParsePart` reads it as `look` with target "plastic rose", and `DoVerb` finds the prop (2e). Part 6d checks every template still reads back.

## 5. `free_mode.json` (the relay deploy)

**Which change needs a deploy: only this file.** `Relay/src/index.js` imports it and Cloudflare rebuilds the relay on every push to `noHumansOnSet` (T55-build part 5, T59), so the push that carries it is the deploy. **No file in `Relay/` changes:** the relay's `freeReply` reads `ph.actions ?? [0, 0]` (a phase with no `actions` makes none) and fills `{prop}` in a target as in an item (`fill(a.target, ctx)`, line 247). The game's `FreeReply` and `FreeFill` do the same.

**The OK:** my person types it in the T62 session (T59: an OK passed on by the dispatcher doesn't clear the permission check). Until then, don't edit the file, not even uncommitted (T55-build part 5: other sessions share the folder and the branch).

As T58 leaves the file (T55 deleted the `tiebreak` phase and swapped three reaction lines; T58 added `last_word` before `free_talk`):

**a. `_readme`, line 6** (T58's version):

- Now: `"Each phase says what to fill: 'lines' (speech), 'reasons' (reason), 'vote' (a random name from options), 'actions' (how many, from 'scene_actions'), 'pass_chance' (Free Talk only; the last word has none), 'echo_typed' (the input step: speech = the player's typed text, cut to 15 words).",`
- New: `"Each phase says what to fill: 'lines' (speech), 'reasons' (reason), 'vote' (a random name from options), 'actions' (how many, from 'scene_actions': 0 or 1, and only in a scene turn since T62), 'pass_chance' (Free Talk only; the last word has none), 'echo_typed' (the input step: speech = the player's typed text, cut to 15 words).",`

**b. `_readme`, line 8:**

- Now: `"scene_actions: the actions a free actor may take, with weights. target and item use the same placeholders.",`
- New: `"scene_actions: the actions a free actor may take, with weights. target and item use the same placeholders. The props are random, so some grabs, throws and gives break the action rules (BP_StageDirector.CanDo), and the game turns them into a look around, which is fine for a test.",`

**c. `reaction_cut` and `reaction`** (about lines 43 and 54): delete the line `			"actions": [0, 1],` in each. The `lines` key follows, so the JSON stays valid.

**d. `scene_turn`** (about line 90): `			"actions": [1, 2],` → `			"actions": [0, 1],`

**e. `scene_actions`** (about lines 102 to 108): add a look at a prop after the look at an actor:

```json
	"scene_actions": [
		{ "verb": "move", "target": "{place}", "item": "", "weight": 3 },
		{ "verb": "look", "target": "{actor}", "item": "", "weight": 2 },
		{ "verb": "look", "target": "{prop}", "item": "", "weight": 1 },
		{ "verb": "grab", "target": "", "item": "{prop}", "weight": 2 },
		{ "verb": "give", "target": "{actor}", "item": "{prop}", "weight": 1 },
		{ "verb": "throw", "target": "{place}", "item": "{prop}", "weight": 1 }
	]
```

**What a free show does then:** about half the AI scene turns take one action. Of those, a look at a prop is 1 in 10; most throws and gives (2 in 10) and some grabs fall back with a rule's reason, so a 3-scene show has several fallbacks (Done-when bullet 3). A free bot throws a prop it really holds rarely (question 3).

**After the push:** wait about 90 s for the build (T59), then run part 7b.

## 6. `Tools/check_prompts.py`

Line numbers are at `d2d4cdc`; T54, T55, T57 and T58 move them. Find each by its text.

**a. The docstring.** After T58's paragraph and before `Exit code 0 means ...`:

```
One rule set for every action (T62): every actor takes 0 or 1 action in a scene
turn and none in a reaction; a grab takes a prop nobody holds, a throw or give a
prop the actor holds, and nobody holds more than MAX_HELD props. Every actor
state says who holds what ('holding' in each cast entry and in 'you'), and the
sample log follows the rules (check_rules). A reply that breaks a holding rule
is a WARN, since the game turns it into a look around and free mode breaks them
on purpose. The file check finds the design doc's two action lines in 'game'
word for word (DOC_ACTION_LINES) and fails a does_templates entry that
BP_StageDirector.ParsePart can't read back. --log fails a log entry with two
actions in a scene turn, or any action in a reaction, and counts the rule
fallbacks (NHOS: ACT <id> look around - (<rule>: <part>)).
```

**b. Constants.** After `VERBS = ["move", "look", "grab", "throw", "give"]` (line 136):

```python
MAX_HELD = 2  # T62: BP_StageDirector.MaxHeld
# T62: the wording BP_StageDirector.ParsePart reads back; change a template only together with ParsePart.
PARSED_TEMPLATES = {"move": "moves to {target}", "look": "looks at {target}", "look_around": "looks around",
                    "grab": "grabs the {item}", "throw": "throws the {item} at {target}",
                    "give": "gives the {item} to {target}", "nothing": "stands still"}
# T62: CanDo's reasons, as NHOS: ACT ... look around - (<reason>: <part>) prints them.
RULE_WHYS = {"no such prop", "someone holds it", "hands full", "not holding it", "not a place",
             "not an actor, a prop or a place", "not an actor or a place", "not an actor",
             "their hands are full", "unknown verb", "cut", "unknown actor"}
```

After `DOC_TIE_LINE = ...` (line 150):

```python
# T62: the design doc's two action lines (Bot Prompts, "Opening prompt: game rules"), word for word.
DOC_ACTION_LINES = [
    "Every actor, the human too, takes at most one action a turn: grab only a prop nobody holds, throw or give only a prop you hold, and hold two props at most. \"holding\" in the state shows who holds what. An action that breaks a rule fails, and the robot only looks around.",
    "Only scene turns have actions. Free Talk, last words and reactions are speech only.",
]
```

(Question 2 "no limit": the first line as part 1b gives it, and `MAX_HELD = 99`.)

**c. `parse_does`,** a new function right after `def act(...)` (line 722):

```python
def parse_does(T, part):
    """T62: one does part back into (verb, item, target), as BP_StageDirector.ParsePart reads it;
    (None, "", "") when no template fits. "looks around" is a look with no target."""
    for key in ("look_around", "move", "look", "grab", "throw", "give"):
        pat = re.escape(T.get(key, "\0")).replace(re.escape("{item}"), "(?P<item>.+)").replace(re.escape("{target}"), "(?P<target>.+)")
        m = re.fullmatch(pat, part)
        if m:
            d = m.groupdict()
            return ("look" if key == "look_around" else key), d.get("item", ""), d.get("target", "")
    return None, "", ""
```

The greedy `item` group splits "throws the X at Y" at the last " at ", as `ParsePart`'s `Split ... FromEnd` does.

**d. `check_files`.** Right after `if not any(DOC_TIE_LINE in g for g in game): errors.append(...)` (line 657), and after T54's goal-1 check and T57's silence check if they sit there:

```python
    # T62: the design doc's action lines, word for word; the asks' action counts; templates that read back.
    for line in DOC_ACTION_LINES:
        if not any(line in g for g in game):
            errors.append(f"prompts.json: 'game' lost an action rule from the design doc: {line[:60]!r}")
    if any("0 to 2 actions" in g for g in game):
        errors.append("prompts.json: 'game' still allows 2 actions; since T62 it is 0 or 1")
    asks = prompts.get("asks", {})
    if "Fill: actions (0 or 1)" not in asks.get("scene_turn", ""):
        errors.append("prompts.json: asks.scene_turn must ask for 'actions (0 or 1)' (T62)")
    for k in ("reaction", "reaction_cut", "free_talk", "last_word"):
        if k in asks and "No actions" not in asks[k]:
            errors.append(f"prompts.json: asks.{k} must say 'No actions' (T62: only scene turns have actions)")
    T = prompts.get("does_templates", {})
    for k, v in PARSED_TEMPLATES.items():
        if T.get(k) != v:
            errors.append(f"prompts.json: does_templates.{k} is {T.get(k)!r}, but BP_StageDirector.ParsePart reads {v!r}")
    for verb, item, target in (("move", "", "Prop Table"), ("look", "", "Player 2"), ("look", "", "tin-can robot"),
                               ("look", "", ""), ("grab", "glow-stick sword", ""), ("throw", "toy blaster", "Player 4"),
                               ("throw", "piggy bank", "Prop Table"), ("give", "tin-can robot", "Player 1")):
        key = "look_around" if verb == "look" and not target else verb
        text = T.get(key, "").replace("{item}", item).replace("{target}", target)
        if parse_does(T, text) != (verb, item, target):
            errors.append(f"prompts.json: does_templates.{key} doesn't read back: {text!r} gives {parse_does(T, text)}")
```

Tried on the scratch copy: every template reads back, and with part 4 in, these checks pass. With today's `prompts.json` they fail, and `--offline` exits 1 with six lines: the two doc lines, "0 to 2 actions", `scene_turn`, `reaction` and `reaction_cut`.

**e. The sample show** (`TURNS`, line 742). One action per actor in turn 1, and a look at a prop in turn 3. The speech stays, and the note story holds: every AI but SpaceXAI grabs a prop in turn 1 and keeps it ("hold_prop").

- Turn 1, each line's action list becomes one action:

| Actor | Now | New |
|---|---|---|
| `worrier` | `[act("move", "Left"), act("grab", item="glow-stick sword")]` | `[act("grab", item="glow-stick sword")]` |
| `HUMAN` | `[act("grab", item="tin-can robot"), act("move", "Center")]` | `[act("grab", item="tin-can robot")]` |
| `overclocker` | `[act("move", "Riser"), act("look", "Player 3")]` | `[act("move", "Riser")]` |
| `copycat` | `[act("grab", item="toy blaster"), act("move", "Right")]` | `[act("grab", item="toy blaster")]` |
| `visionary` | `[act("move", "Back"), act("grab", item="piggy bank")]` | `[act("grab", item="piggy bank")]` |

- Turn 3, `copycat`: `[act("move", "Center")]` → `[act("look", "tin-can robot")]` ("I will now rescue the robot." still fits).
- The comment above `HUMAN = "human"` gains: `# T62: one action a turn, by the rules every actor shares; after turn 1 every prop is held.`
- After turn 1, all four card props are held (worrier, the human, copycat, visionary), so the scene-turn ask (turn 2) tests that an AI doesn't grab a held prop (a WARN if it does). After turn 3, the human gave the tin-can robot to Player 1 (visionary, now holding two).

**f. `Show`: `holding`.**

- In `__init__`, after `self.seat = ...`: `        self.problems = []  # T62: rule breaks in the sample log; check_rules prints them`
- New method after `def entry(...)`:

```python
    def holding(self, log, cut=None):
        """T62: who holds what after the log's scene turns, by the rules every actor shares
        (BP_StageDirector.CanDo). A cut actor holds nothing. A sample action that breaks a rule
        goes to self.problems, so the sample show stays legal."""
        held = {self.name(p): [] for p in SAMPLE_CAST}
        for e in log:
            if ", turn " not in e["when"] or e["does"] == self.T["nothing"]:
                continue
            parts = e["does"].split("; ")
            where = f"{e['when']}, {e['actor']}: {e['does']!r}"
            if len(parts) > 1:
                self.problems.append(f"{where} has {len(parts)} actions, one at most")
            verb, item, target = parse_does(self.T, parts[0])
            mine = held[e["actor"]]
            owner = next((n for n, ps in held.items() if item and item in ps), None)
            if verb is None:
                self.problems.append(f"{where}: does_templates can't read it back")
            elif verb == "grab":
                if owner or len(mine) >= MAX_HELD:
                    self.problems.append(f"{where}: a grab of a held prop, or with full hands")
                else:
                    mine.append(item)
            elif verb in ("throw", "give"):
                if item not in mine:
                    self.problems.append(f"{where}: a {verb} of a prop it doesn't hold")
                elif verb == "give" and (target not in held or target == e["actor"] or len(held[target]) >= MAX_HELD):
                    self.problems.append(f"{where}: a give to someone who can't take it")
                else:
                    mine.remove(item)
                    if verb == "give":
                        held[target].append(item)
        for pid in cut or {}:
            held[self.name(pid)] = []
        return held
```

- `cast` and `you` take the holdings:

```python
    def cast(self, cut=None, held=None):
        cut, held = cut or {}, held or {}
        return [{
            "name": self.name(pid),
            "role": self.seat[pid]["role"],
            "want": self.seat[pid]["want"],
            "status": cut.get(pid, "on stage"),
            "holding": held.get(self.name(pid), []),
        } for pid in SAMPLE_CAST]

    def you(self, pid, held=None):
        return {
            "name": self.name(pid),
            "role": self.seat[pid]["role"],
            "want": self.seat[pid]["want"],
            "note": "" if pid == HUMAN else self.note["note"],
            "holding": (held or {}).get(self.name(pid), []),
        }
```

- In `actor_state`, first line: `        held = self.holding(log, cut)`, and `"cast": self.cast(cut, held),`, `"you": self.you(pid, held),`.
- In `card_cases`, the inline cast entry gets `"holding": []` after `"status"`, and the inline `you` gets `"holding": []` after `"note"` (each card state is turn 1 of a later scene: nobody holds anything after Scene Prep).
- **T54's closing block:** after its `cases["closing"]["show"]["scene"] = scene`, add:

```python
        if scene > 1:  # T62: Scene Prep sent every prop home; the sample log is scene 1's
            for c in cases["closing"]["cast"]:
                c["holding"] = []
            cases["closing"]["you"]["holding"] = []
```

- `check_note_deal` calls `show.you(HUMAN)["note"]`: still works.

**g. `check_reply`** (line 1176):

- The count (line 1194): `    if len(actions) > 2:` / `        fails.append(f"{len(actions)} actions")` becomes:

```python
    limit = 2 if ask == "input" else 1  # T62: one action at most; the input converter keeps 2 until T63
    if len(actions) > limit:
        fails.append(f"{len(actions)} actions, {limit} at most")
```

- The action shapes (lines 1200 to 1206): `look` and `throw` change:

```python
            "look": (tg in places or tg in props or (tg in actors and tg != me) or tg == "") and not it,  # T62: a prop too
            "grab": it in props and not tg,
            "throw": it in props and (tg in places or (tg in actors and tg != me)),
```

- Right after that `for a in actions:` loop, the holding rules as WARNs:

```python
    # T62: the holding rules (BP_StageDirector.CanDo). The game turns a broken one into a look around,
    # so it is a WARN: free mode breaks them on purpose, with random props.
    held = ctx.get("held")
    if held is not None:
        mine = held.get(me, [])
        owner = {p: n for n, ps in held.items() for p in ps}
        for a in actions:
            v, tg, it = a.get("verb"), a.get("target", ""), a.get("item", "")
            if v == "grab" and it in owner:
                warns.append(f"grab of the {it}, which {owner[it]} holds")
            elif v == "grab" and len(mine) >= MAX_HELD:
                warns.append(f"grab with full hands ({', '.join(mine)})")
            elif v in ("throw", "give") and it not in mine:
                warns.append(f"{v} of the {it}, which {me} doesn't hold")
            elif v == "give" and len(held.get(tg, [])) >= MAX_HELD:
                warns.append(f"give to {tg}, whose hands are full")
```

- `scene_turn` (line 1219): delete `        need(1 <= len(actions) <= 2, "a scene turn needs 1 or 2 actions")` (the count check above covers it; 0 actions is now fine).
- `reaction` (line 1235): `        need(len(actions) <= 1, "a reaction has at most 1 action")` → `        need(not actions, "a reaction has no actions (T62)")`

**h. `build_jobs`** (line 1386): each actor `ctx = {...}` (the main loop, the tie reaction, the card sweep; T58's `last_word` rides the main loop) gets `"held": {c["name"]: c["holding"] for c in st["cast"]}`. The input and (if T55 left any) tiebreak contexts don't.

**i. `check_rules`,** a new function after `check_note_deal` (line 1447), and its call in `main`:

```python
def check_rules(show, jobs) -> int:
    """T62: the sample log follows the action rules, and every actor state says who holds what
    ('holding' in each cast entry and in 'you'). Returns the number of problems."""
    bad = 0
    for p in sorted(set(show.problems)):
        bad += 1
        print("FAIL rules: sample log:", p)
    for ask, label, _, body, _ in jobs:
        if ask in ("input", "tiebreak"):
            continue
        if body_text(body).count('"holding"') < 2:
            bad += 1
            print(f"FAIL rules: no 'holding' in cast and you | {ask} | {label}")
    return bad
```

In `main`, right after the `check_note_deal` block (`print("Only the AI seats get the note, ...")`, line 1520):

```python
    if check_rules(show, jobs):
        return 1
    print("The sample show follows the action rules, and every actor state says who holds what.")
```

**j. `check_log`.**

- **`LOG_RE`:** add `ACT|EXTRA` to the alternation T58 leaves (it has T52's `CUT|TIE|REACTIONS DONE`, T54's `SHOW END`, T57's `PASSED`, T58's `LASTWORDS`).
- **Counters:** after T52's `vote_bad = 0 ...` add `    act_bad = 0  # T62: log entries with more actions than the rules allow`; after T52's `ends, scene, ties = [], 0, 0  # T52` add `        falls, extras = 0, 0  # T62`.
- **Two branches,** right before `            if kind == "SEATS":` (the `continue` matters: without it the line falls into the AI-line branch, as T54 found for `SHOW END`):

```python
            if kind == "ACT":
                # T62: "NHOS: ACT <id> look around - (<reason>: <part>)" is a fallback; count the rules' own.
                m = re.match(r"\S+ look around - \((.+?): ", rest)
                if m and m.group(1) in RULE_WHYS:
                    falls += 1
                continue
            if kind == "EXTRA":
                extras += 1
                continue
```

- **In the `LOG` branch,** right after `if len(parts) < 4: continue`:

```python
                # T62: one action a scene turn, none in a reaction, for every actor, the human too.
                n_act = 0 if parts[2] in ("stands still", "passes") else len(parts[2].split("; "))
                if (", turn " in parts[0] and n_act > 1) or (parts[0].endswith("reactions") and n_act > 0):
                    act_bad += 1
                    print(f"[FAIL] show {i} | LOG | {parts[0]} | {parts[1]}: {parts[2]!r} has {n_act} action(s); "
                          f"{'one at most' if ', turn ' in parts[0] else 'none in a reaction'} (T62)")
```

- **The summary line** (`print(f"Show {i}: human = ...")`, as T54 to T58 leave it): add `, rule fallbacks = {falls}, extras dropped = {extras}` before its closing `.")`.
- **The return:** add `or act_bad` to T58's return line.
- A log from before T62 fails the action count (two actions in a turn), which is right.

**k. Runs, and what was tried.** `--offline` must pass with the same job count as after T58 (67): T62 adds no ask. **Tried on a scratch copy of `d2d4cdc` with parts 4, 5 and 6** (T54 to T58 not in it, so the `last_word` and T54 closing edits weren't exercised):

- `--offline` passes, 63 jobs before and after; it prints the new `The sample show follows the action rules, ...` line.
- The sample holdings: at the scene-turn ask, Player 1 `[piggy bank]`, Player 2 `[glow-stick sword]`, Player 3 `[tin-can robot]`, Player 4 `[]`, Player 5 `[toy blaster]`; after three turns Player 1 holds `[piggy bank, tin-can robot]` and Player 3 nothing; in `reaction_cut`, the cut actor holds nothing.
- A sample turn changed to a throw of a prop the actor doesn't hold fails: `FAIL rules: sample log: scene 1, turn 2, Player 1: 'throws the toy blaster at Player 2': a throw of a prop it doesn't hold`.
- `check_reply` on the scene-turn context: a grab of the held toy blaster gives the WARN `grab of the toy blaster, which Player 5 holds`; a throw of a prop the actor holds, a look at a prop and no action pass; two actions fail (`2 actions, 1 at most`); a look at oneself fails (`bad action`); a move in a reaction fails (`a reaction has no actions (T62)`).
- `--log` on a synthetic good log passes and prints `rule fallbacks = 1, extras dropped = 1` (a `someone holds it` fallback counts, an `unknown target` one doesn't); with a two-action turn and a reaction move it exits 1 with one `[FAIL] ... (T62)` line for each.

## 7. The check

The Done-when, mapped: (1) `--offline` and `--relay --free` pass → 7a, 7b. (2) `CanDo` cases through Unreal MCP in PIE → 7c. (3) A free autoplay show → 7d. (4) The hand-played show's two screenshots → 7e.

The brief's editor rule applies: say `Editor: driving` in your status file while you edit and run PIE.

### 7a. `--offline`

```bash
python Tools/check_prompts.py --offline
```

Passes, with the new line `The sample show follows the action rules, and every actor state says who holds what.`

### 7b. `--relay --free` (after the deploy push)

```bash
python Tools/check_prompts.py --relay --free
```

Before the push, the relay's free mode still makes 1 or 2 scene actions and a reaction action, so this fails on the new counts. After the push and about 90 s: it passes. Expect WARN lines from part 6g (free mode grabs held props and throws props it doesn't hold); they don't fail the run.

### 7c. `CanDo` in a PIE show (Test for Free)

`Local/switches.json`: `"autoplay": false`, `"mode": "free"`. PIE in a 1600 × 900 window. Start the show, press **Start the scene**, and wait for my turn 1 (the logic has asked the AIs, but `PlayTurn` hasn't run, so nobody holds anything). Then run this through the toolset that runs editor Python (T45-build 3b uses it):

```python
import unreal
world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
d = unreal.GameplayStatics.get_actor_of_class(world, unreal.load_class(None, "/Game/NHOS/Stage/BP_StageDirector.BP_StageDirector_C"))
names, props = list(d.get_editor_property("RNames")), list(d.get_editor_property("RProps"))
hold, out = list(d.get_editor_property("HoldBy")), list(d.get_editor_property("ROut"))
on = [s for s in range(len(names)) if not out[s]]
free = [p for p, h in zip(props, hold) if h < 0]
a, b, p1, p2 = on[0], on[1], free[0], free[1]
d.call_method("Accept", (a, "grab", p1, ""))               # set up: seat a holds p1
for c in [(b, "grab", p1, ""), (b, "throw", p2, names[a]), (a, "give", p1, "Center"), (b, "move", "", names[a]),
          (b, "look", "", p1), (b, "grab", p2, ""), (a, "throw", p1, names[b])]:
    d.call_method("PrintRule", c)
d.call_method("Accept", (a, "throw", p1, "Center"))        # p1 is free again
print("RULES", names, props, list(d.get_editor_property("HoldBy")))
```

Expected in the log, in order (`<…>` are the names the script picked):

```
NHOS: HOLD <p1> <id of a>
NHOS: RULE grab <p1> - = no someone holds it
NHOS: RULE throw <p2> <Player a> = no not holding it
NHOS: RULE give <p1> Center = no not an actor
NHOS: RULE move - <Player a> = no not a place
NHOS: RULE look - <p1> = yes ok
NHOS: RULE grab <p2> - = yes ok
NHOS: RULE throw <p1> <Player b> = yes ok
NHOS: HOLD <p1> -
```

- If `call_method` can't reach a Blueprint function or read a Blueprint variable by name, run the same calls with the toolset's own call tool, or through a temporary Editor Utility; say under "Findings" what worked.
- **Step 5 too:** in the same PIE show, play on to turn 2 (type a line, wait for the turn), then `grep "NHOS: YOU" Saved/Logs/AIMegaJam2026.log`: each AI's `you` has `"holding":[...]` that matches the `NHOS: HOLD` lines of turn 1. Also call `HeldBy` on `BP_Show` for one seat that grabbed.

### 7d. A free autoplay show in a game window

`Local/switches.json`: `"autoplay": true`, `"mode": "free"`, `"fast_lines": true`, `"spare_human": true` (so the show runs three or four scenes), `"force_tie": false`, `"ai_seats": 0`. Close every game window before you save an asset (T53).

```bash
"<UE_ROOT>/Engine/Binaries/Win64/UnrealEditor.exe" "<PROJECT>" -game -windowed -ResX=1600 -ResY=900 -log=T62auto.log
```

Then:

```bash
grep -cE "LogScript" Saved/Logs/T62auto.log
grep -E "NHOS: (RULES|HOLD|EXTRA|SHOW END)" Saved/Logs/T62auto.log
grep -E "NHOS: ACT \S+ look around - \((no such prop|someone holds it|hands full|not holding it|not a place|not an actor, a prop or a place|not an actor or a place|not an actor|their hands are full):" Saved/Logs/T62auto.log
grep -E "NHOS: ACT \S+ look .* -$" Saved/Logs/T62auto.log
python Tools/check_prompts.py --log Saved/Logs/T62auto.log
```

Expected:

- `LogScript` count 0; `NHOS: SHOW END result=win reason=...` (T54's form).
- One `NHOS: RULES scene seats=5 out=<n> props=<the card's four> places=Center, Left, Right, Front, Back, Riser, Prop Table` per Scene Prep, with `out=` growing by one after each cut, and one `NHOS: RULES out <id>` per cut.
- `NHOS: HOLD` lines for the grabs, throws and gives that passed; **no `NHOS: EXTRA`** from an AI (free mode makes at most one), and none from my seat (free mode's input step makes no actions).
- At least one rule fallback (the third grep). If none (a quiet random show), run again.
- A look at a prop among the `ACT ... look <prop> -` lines (from the new free action).
- `--log` passes: no `[FAIL] ... (T62)` line, and the summary says `rule fallbacks = <n ≥ 1>`.
- **No AI turn plays more than one action:** `--log` checks the `NHOS: LOG` lines, and `grep -E "NHOS: LOG scene [0-9]+, turn [0-9] \| [^|]+ \| [^|]*; " Saved/Logs/T62auto.log` prints nothing.

### 7e. One show played by hand in PIE, two screenshots

**Question 3 decides how.** With the recommended answer: PIE in a 1600 × 900 window, autoplay off, **Play via Relay** (it costs relay credit; my person said yes to about $0.20 to $0.40), scene 1 only, then Restart in Test for Free if the look at a prop hasn't shown yet.

1. Turn 1: type `grab the <a card prop> and say Mine now.` Watch `NHOS: HOLD <prop> human`.
2. Turn 2: type `throw the <prop> at @<a robot's screen name>`. My robot throws it (`NHOS: ACT human throw Player <n> <prop>`, with no fallback). Screenshot the throw in flight with `SlateInspectorToolset.Screenshot` (T33): `Saved/T62/shots/throw_held.png`.
3. A robot that looks at a prop: an AI in the relay scene, or a free bot after Restart in Test for Free (`NHOS: ACT <id> look <prop> -`); screenshot while it faces the prop: `Saved/T62/shots/look_prop.png`.
4. As a first-time player, judge: does the throw read as "it grabbed it, then threw it", and does the robot clearly face the prop? Under "Findings", note whether the real AIs grabbed held props or threw props they didn't hold (the `ACT ... look around - (<rule>: ...)` lines of the relay scene), and quote one line where an AI used `holding`.

**Afterward:** set `autoplay`, `fast_lines` and `spare_human` back to false, `mode` back to what it was, and close each game window.

### 7f. The commit

One commit after both OKs: `Content/NHOS/Stage/BP_StageDirector.uasset`, `Content/NHOS/Core/BP_Show.uasset`, `Content/NHOS/Data/prompts.json`, `Content/NHOS/Data/free_mode.json`, `Tools/check_prompts.py`; the new files in `Graphs/BP_StageDirector/` (the 17 of part 2c) and the rewritten `PlayPart.txt` and `DoVerb.txt`; `git rm Graphs/BP_StageDirector/BotCands.txt`; `Graphs/BP_Show/` (`StageRules`, `CheckDoes`, `CheckTurn`, `HeldBy`, `RuleOut`, `HoldLine` new, `StagePrep` changed); `Docs/tasks/T62.md` (Result, Findings with every node edit), `Docs/Plan.md` (the box), `Docs/DevLog.md`. With question 4's recommended answer, also `Content/NHOS/Data/scenes.json` (outside the Touches: name it in the commit message). Unlock both assets after the push. Without the deploy OK: the T55 pattern (a first commit without `free_mode.json` and with a `Waiting:` line), but `--relay --free` stays red until the second.

## 8. What each later task gets from T62

- **T63 (`SendHumanTurn(Verb, Item, Target, Line)`):** find the director with `GetActorOfClass` and my seat with `BP_Show.HumanSeat`. Call `CanDo` only for move, look, grab, throw and give: `around` is "looks around" and `none` is "stands still" with no check. Write my `does` with the templates, store it where `StoreTurn` stores a seat's turn, and let `PlayTurn`'s `CheckTurn` accept it in the log's order (**don't call `Accept` yourself**, or my grab is counted twice). T63's own `CanDo` call is a pre-check for its `NHOS: HUMAN` line; a race lost to an AI in the same turn still falls back in `CheckTurn`, as the spec says. T63's autoplay picks from `ItemsFor` and `TargetsFor`.
- **T64 (the builder):** `ItemsFor(HumanSeat, Verb)` and `TargetsFor(HumanSeat, Verb)` at the start of my turn and after each pick, on the director. Targets come back as Player names, prop names and place names; show actors by `SeatLabel` (the index of a Player name in `SeatName`). Greyed Grab: "Nothing free to grab." when `ItemsFor(grab)` is empty and `HeldCount(HumanSeat)` is under `MaxHeld`; "Your hands are full." when it isn't (question 2). Throw and Give: "Grab something first." when `HoldingOf(HumanSeat)` is empty. The holdings shown at my turn's start are the last turn's, the same the AIs read; this turn's AI actions are accepted only after everyone has sent.
- **T66:** an unfinished action becomes "looks around", which `AcceptDoes` passes as it is.
- **T61 (How to play, the stagehand):** the doc's two new lines are the rules a tip can teach.

## 9. Knock-on: tell, don't change

- **`Content/NHOS/Data/llm.json` `_readme`** (outside T62's Touches): "the game cuts speech and reason to 15 words and uses at most 2 actions" becomes untrue. The fix is "... and uses at most 1 action (none in a reaction)". Tell my person; the next task that holds `llm.json` can take it.
- **`prompts.json` `input`** still turns my typing into 0 to 2 actions (`- Actions: turn what the player wants to do into 0 to 2 actions`, `- Phase "reaction": at most one action.`) and allows no look at a prop. T63 rewrites `input`. Until then `AcceptDoes` keeps my first action.
- **`game`'s `"- The human types into a converter that turns their text into the same form as your lines. ..."`** becomes untrue with T63 (my action is built, not converted). It is in `game`, not in T63's Touches (`input`, `asks.input`, `_readme`): tell T63.
- **`Docs/ItchPage.md` line 70** ("You can **move** to a place, **look** at someone or something, **grab** a prop, **throw** a prop at someone, or **give** a prop to someone.") stays true; its typing lines (69 to 75) are T63's and T64's. T54's session holds the file now.
- **`BP_Robot`'s snatch and grab-first** stay as animation (2e). A later polish task could take them out once T64 lands.
- **The Overview tab** wasn't read; skim it for an action count.
