# T53 build sheet: the scene clock

Back to [T53](T53.md). A Mac prep session wrote this on 2026-11-15, without the editor. It is written against **`noHumansOnSet` at `6ada2ab` (T51)**. The repo folder was at `0dcf08a` when I finished, which adds only T44's prep files and changes nothing this sheet names. All line numbers are from `6ada2ab`.

T50 and T59 run before T53, and both change `Content/NHOS/Data/prompts.json` and `Tools/check_prompts.py` (their plans are in [T50-build.md](T50-build.md) and [T59-build.md](T59-build.md)). So every place below is named by its text as well as its line number. Find each line by its text before you change it. Part 0 lists what to check first.

The design doc was read, not changed: Rules tab rev 27, Bot Prompts tab rev 81, and the UI section of the Art Inspiration tab rev 28.

## In short

- **`BP_Show`:**
  - `SceneCount` = `SeatCount` − 1, a pin edit in `SetupShow`.
  - `show.scenes` follows it with no change, if `ActorState` reads `SceneCount`.
  - The `SETUP` line gets `scenes=<n>`.
  - The scene banner says "Scene 2: Title", or "Last scene: Title" on the last scene.
  - The end check after the reactions adds "or the last scene is done", through a new `LastSceneDone()` that T52 calls after a tie too.
  - `ShowPrep` calls the new `WBP_Stage.SetClapper`.
- **`WBP_Stage`:** a small slate under the header, top left, that says `SCENE 2 / 4`. It is built from `UIStyle` (an `Ink` panel plus a striped clapstick), and two new functions (`StyleClapper`, `SetClapper`) fill it.
- **`prompts.json` `game`:** one line changes ("How a show works", line 22). One line in "Reading the state" is optional. The Bot Prompts tab has no line for the scene count, so both are marked "not in the doc".
- **`check_prompts.py`:** the three `"scenes": 3` become `SAMPLE_SCENES` (= the cast size − 1 = 4). An optional `--log` check compares the scene count with the seat count.
- **The 4-actor show** needs a way to seat 3 AIs in free mode. Nothing does that today, so this sheet adds an `ai_seats` switch, read in `LoadSwitches` and used in `DrawCast` (part 1g).
- **No run can reach the last scene before T52.** Every scene cuts one actor, so a 5-actor show ends at two actors after scene 3. The new branch is built here and first played by T52's `force_tie` run.

## Decisions made for my person

My person was asleep and asked me to take my own recommendation on design calls. Each is open to change. The T53 session should show this list to my person when it closes the task.

1. **Where the clapperboard goes:** at the top left, under the header (part 2a). The other three corners are taken: my card is at the top right (and in Scene Prep it can reach 1032 px down the right side), the chat and input are at the bottom left, and the money burn is at the bottom right. The fallback, if a screenshot shows it over a robot's name tag, is inside the header, left of the phase text.
2. **How it looks:** a slate. The body is an `Ink` panel (`UIStyle.StylePanel`) with `SCENE n / total` in `Header` type (32, bold, white). Above it sits a clapstick of six sheared stripes in paper and ink, with an old-gold trim. The stick's corner radius is 4 (`UISize "S1"`), which is not in the doc's corner list (panels 16, buttons 12, tags 10). The last scene gets no special look.
3. **Its text:** `SCENE 2 / 4`, in caps, exactly as the doc writes it (Rules, "The Cut" step 6, and the Onboarding row "Always"). It is a label, not a sentence, so the doc's "no sentence in all caps" rule allows it.
4. **The scene banner:** "Scene 2 of 4: Title" becomes "Scene 2: Title", and the last scene's banner reads "Last scene: Title". The count lives on the clapperboard only ("each instruction is said once"). "Last scene" warns me that the show can end there, which matters once T52 and T54 are in.
5. **The end check uses `SceneNum >= SceneCount`,** not `==`, so a show that somehow overshoots still ends. It sits in its own function, `LastSceneDone()`, so T52's tie path can call it (T52 step 3 points at "T53's end check").
6. **A new `ai_seats` switch** for the 4-actor check run, in `Local/switches.json`. It adds `Docs/switches.example.json` to T53's commit, which is outside T53's Touches. Name it in the commit message. The other way, setting `MaxCast` to 4 and back, needs two saves of `BP_Show` and changes `FindRobots`' slot count.
7. **Two new check lines:** `NHOS: CLAPPER scene=<n> total=<m>` from `SetClapper`, and `NHOS: STATE <seat> show=<json>` from `ActorState` on each turn-1 scene ask, so the log shows `"scenes": 4` in the state the AIs read. No line prints the state today.
8. **`SETUP` gets `scenes=<n>` at its end:** `NHOS: SETUP human=human scene=<card> note=<id> category=<cat> scenes=4`. The checker's `scene=(\S+)` regex can't match `scenes=`.
9. **The new `game` line 22** (part 3) words the rule for the AIs. It is not in the Bot Prompts tab. It follows the Rules tab's "Cast & personas" and "The Cut" step 6. A new "show" line in "Reading the state" is optional (part 3b). I recommend adding it.
10. **`check_prompts.py`:** a `SAMPLE_SCENES` constant instead of three literals, and an optional `--log` check (part 4c) that fails a show whose `SETUP` lines don't say `scenes = seats − 1`. I recommend adding it, because T52 and T54 get the check for free.
11. **`Docs/ItchPage.md` lines 58 and 116** state "three scenes" and "two scenes". They are outside T53's Touches, and T54 rewrites the win lines there. I recommend that T53 changes only the counts (part 6) and names the file in its commit, so the page is never wrong in between.
12. **A Components row for the design doc** (part 6): the UI section has no clapperboard piece. Per the build note "The design doc follows the game", the T53 session shows my person the row and adds it only after their OK.

## 0. Before you start (after T50 and T59 are pushed)

1. `git log --oneline -5` shows T50 and T59, `Docs/claims/T59` is released, and `git lfs locks` shows no lock on `BP_Show.uasset` or `WBP_Stage.uasset`.
2. `prompts.json`: line 22 (part 3a) is still word for word as quoted. T50 adds sub-bullets after lines 23, 24 and 25, and a `scene_card` line after line 34. T59 changes lines 39 and 59. None of them changes line 22. If one did, replace whatever is there.
3. `check_prompts.py`: find the three `"scenes": 3` with `git grep -n '"scenes": 3' Tools/check_prompts.py`. T50 changes the `scene_card` line right below the first two (`actor_state` and `card_cases`), so expect `note_category` on the next line. T50 adds a docstring paragraph ("Director's note (T50)") after "Rivals (T56)", and `DOC_NOTE_LINES` after `MAX_WORDS`. T59 sets `MAX_WORDS = 15`.
4. `Graphs/BP_Show/`: see whether T50 or T59 wrote `ScenePrep.txt`, `ShowPrep.txt`, `ActorState.txt` or `CapWords.txt`. If one exists, start from it instead of reading that graph from the editor.
5. T50's findings in `T50.md`: anything it learned about `ShowPrep` (it changes what `SetInfoTop` gets) and `ActorState` (it adds `note_category`). T51's findings already say `ScenePrep` must be edited node by node (part 1d).
6. `python Tools/check_prompts.py --offline` passes before you start, so any failure afterward is T53's.

## 1. `BP_Show`

### 1a. Which graphs to read, which have files

| Graph | File in `Graphs/BP_Show/` | T53 changes | How |
|---|---|---|---|
| `SetupShow` | **none** | `SceneCount` = `SeatCount` − 1 | Pin edit (1b). T18 put `DrawCast`'s call and a Branch in by hand, so don't rewrite it with the DSL. |
| `ScenePrep` | **none** (T51 edited it node by node) | `scenes=` on the `SETUP` line | Node edit (1d). |
| `ShowPrep` | **none** | The banner and the clapperboard call | Node swap plus one call node (1e). |
| `EndReactions` | **none** | The end check | Node edit (1f). |
| `ActorState(Seat, AskKey, Now)` | **none** | Check `show.scenes`, add the `STATE` print | Read it, then add nodes (1c). |
| `LoadSwitches` | **none** | Read `ai_seats` | Node edit (1g). |
| `DrawCast` | `DrawCast.txt` | Apply `ai_seats` | DSL write from the file (1g). |
| `LastSceneDone` | new | — | DSL write, new file (1f). |
| `CueSceneBanner` | new | — | DSL write, new file (1e). |
| `RestartShow` | **none** | Optional: hide the clapperboard | One call node (1e). |
| `DirectorState` | **none** | Check only: if it writes `show.scenes`, it follows `SceneCount` too | Read. T55 removes it. |
| `RunCue`, `CuePrep`, `OpenPrep`, `StartFromPrep`, `CueBanner`, `CueHeader` | yes | Nothing | `RunCue`'s `"prep"` cue calls `ScenePrep`, so the clapperboard changes at the moment the queue reaches the new scene. |

**First, one survey call:** `find_nodes` in `BP_Show` for the title `Get SceneCount` (and `Set SceneCount`), with `node_class` `/Script/BlueprintGraph.K2Node_VariableGet` (`…VariableSet`). Use the full path; T30 found that `find_nodes` needs it. The result lists every graph that reads the count. Expected: `SetupShow` (set), `ActorState`, `ShowPrep`, maybe `DirectorState` and `EndShow`. Any other reader that builds visible text ("Scene n of m") gets the treatment in 1e. Also look at the `CueHeader` text that `ShowPrep` sends (T30: the former `SetPhase` node 79). If it holds "of <SceneCount>", drop the count there too.

### 1b. `SceneCount` in `SetupShow`

- **Now** (T06, unchanged by T26): `SceneCount` = `SeatCount` − 2. Since T26, `SeatCount` counts every seat, mine included (5 in a full show), so a full show has 3 scenes.
- **New:** `SeatCount` − 1, so 4 scenes with 5 actors and 3 with 4.
- **The edit:** the integer subtract node that feeds `Set SceneCount` has the literal `2` on its B pin. Set it to `1`. If the graph computes it another way (for example from `PersonaArr` + 1), keep the form and make the result the seat count − 1.
- **Order:** the set must come after the seats are built (`SeatCount` final) and before `SetupShow` calls `ScenePrep` (T30: node 25), because `ShowPrep` reads it for the banner and the clapperboard.
- No file to update: `SetupShow` has none. Write the edit under "Findings" in `T53.md`.

### 1c. `show.scenes` in `ActorState`, and the `STATE` line

- **Check:** the `show` object's `scenes` field is fed by `Get SceneCount`. If so, nothing changes there. If it has a literal or another variable, wire `SceneCount` in.
- **New print (decision 7):** at the end of `ActorState`, before its return, print the `show` object once per AI per scene, on turn 1 of the scene:

  ```lisp
  (if (and (streq AskKey "scene_turn") (== (V TurnNum) 1))
    (print (cat "NHOS: STATE " (get (V SeatName) Seat) " show=" (Json|GetJsonString <the show object>))))
  ```

  - `<the show object>` is whatever node holds `show` in this graph. If `show` is built as a string template, print that string.
  - Check that `TurnNum` is 1 while turn 1's asks go out. `StartScene` sets it to 0, so `StartTurn` likely adds 1 before it asks. If it adds 1 after, compare with 0.
  - Check that the parameter's name is `AskKey` and that its value for a scene turn is `"scene_turn"` (T50-build names the signature `ActorState(Seat, AskKey, Now)`).
  - A 5-actor show prints 4 lines per scene, for example `NHOS: STATE Player 2 show={"scene":1,"scenes":4,"now":"the scene, turn 1 of 3"}`.
  - The line never goes to the shared log or to any AI. It is a log line like the others.

### 1d. The `SETUP` line in `ScenePrep`

- **Now** (T51's run): `NHOS: SETUP human=human scene=star_crossed note=never_back category=Movement`.
- **New:** `NHOS: SETUP human=human scene=star_crossed note=never_back category=Movement scenes=4`.
- **The edit, node by node** (T51's finding: `ScenePrep`'s read-back hoists binds out of a `ForLoop`, so a source written from it could change what it does): take the last `Append` in the chain that feeds the `SETUP` `PrintString` and add two pins, `" scenes="` and `ToString(Integer)` of `Get SceneCount`. Or put one new `Append` between the chain's output and the `PrintString`.
- `ScenePrep` runs once per scene, so every scene prints its own `SETUP` with the same `scenes=`.
- **Checker safety:** `check_log` reads `re.search(r"scene=(\S+)", rest)` from `SETUP` for the card. `scenes=4` doesn't match it, because "scene" there is followed by "s", not "=".

### 1e. `ShowPrep`: the banner and the clapperboard

**The banner.** T29 made the scene-title banner from `ShowPrep`'s old chat line. T30 turned that node (14) into `CueBanner`, fed from an inner `Append` chain that builds `"Scene " + SceneNum + " of " + SceneCount + ": " + CardTitle`.

- **Now:** `Scene 2 of 3: Wherefore Art Thou, Robot?` (the `NHOS: BANNER` line).
- **New (decision 4):** `Scene 2: Wherefore Art Thou, Robot?`, and on the last scene `Last scene: Wherefore Art Thou, Robot?`.
- **How:** a new function holds the text, so `ShowPrep` changes by one node swap.

  `Graphs/BP_Show/CueSceneBanner.txt` (new):

  ```lisp
  ; T53: the banner that opens each Scene Prep. The clapperboard shows the count,
  ; so the banner names the scene, or says it is the last one.
  (fn CueSceneBanner ()
    (bind _t (select (>= (V SceneNum) (V SceneCount))
               (cat "Last scene: " (V CardTitle))
               (cat "Scene " (str (V SceneNum)) ": " (V CardTitle))))
    (CallFunction|CueBanner :Text _t))
  ```

  - Create the function with `add_function_graph` (no parameters), then `write_graph_dsl` from this file (after `Tools/dslpp.py`).
  - In `ShowPrep`, replace the `CueBanner` node (T30's node 14) with a `CueSceneBanner` call in the same place in the exec chain. That is the same kind of swap T30 made. The old `Append` chain then feeds nothing. Delete it, or leave it, since pure nodes with no consumer never run.
  - Check that `CardTitle` is the variable the old chain used for the title. T06 lists it. T29 notes that a title ending in "?" gets a "." added on the card; that is `SetInfoTop`'s text, not the banner's.

**The clapperboard call.** `ShowPrep` fills the screen for a new scene (`SetInfoTop`, the cast, the banner), so the call goes there, at once (not through the cue queue, since `ScenePrep` itself already runs at its cue's turn):

```lisp
(Class|WBPStage|SetClapper :self (Variables|Default|GetStage) :Scene (V SceneNum) :Total (V SceneCount))
```

Put one call node right after the `SetInfoTop` call, with exec in and out, `Scene` from `Get SceneNum` and `Total` from `Get SceneCount`.

**Optional, `RestartShow`:** next to its `ClearLog` call (T10), add `SetClapper(0, 0)`, which hides the board until the new show's first Scene Prep. Without it, the old count can show for a moment after Play Again. That rarely shows, because `SetupShow` calls `ScenePrep` at once, but it would show behind the unavailable screen if `DrawCast` fails on a restart.

### 1f. The end check after the reactions

**Now** (T10, then T29 and T30): `EndReactions` prints `NHOS: REACTIONS DONE scene=<n> entries=<n>` and branches:

1. My seat is cut → `EndShow(false)`.
2. Two or fewer seats are left → `EndShow(true)`.
3. Otherwise: the banner "That's scene n. k actors are left, and the show goes on." (T29's node 14, a `CueBanner` since T30), then the next Scene Prep (`ScenePrep` from node 13, which is `CuePrep` if T30 swapped it).

**New:** branch 2 becomes "two or fewer left, **or** the last scene is done". Branch 1 stays first, so a cut human still loses on the last scene.

`Graphs/BP_Show/LastSceneDone.txt` (new):

```lisp
; T53: true when the scene that just ended was the show's last (SceneNum >= SceneCount).
; EndReactions calls it after the reactions; T52 calls it after a tie, which cuts nobody.
(fn LastSceneDone ()
  (return (>= (V SceneNum) (V SceneCount))))
```

- Create it with `add_function_graph`, add a Boolean output (T30: `add_function_param`), and write it. MCP can't make a function pure (T32), so its call node needs exec pins.
- In `EndReactions`, put a `LastSceneDone` call into the exec chain before the branch-2 `Branch`. Then feed that Branch's Condition from a new `OR` (Boolean): A = the old condition, B = `LastSceneDone`'s return value.
- **The banner in branch 3 stays** ("That's scene n. k actors are left, and the show goes on."). It now runs only when another scene follows.
- **`EndShow(true)`** still prints `NHOS: SHOW END result=win scenes=<SceneNum>`. T54 adds `reason=final_two|last_scene` and the two win texts. T53 doesn't tell the two wins apart.
- **For T52:** after a tie, `if LastSceneDone → EndShow(true)`, else the next Scene Prep. A tie never changes how many actors are left, so the two-actor test can't newly pass there.

### 1g. The `ai_seats` switch (for the 4-actor run)

Free mode seats every persona, since `CanSeat` lets any provider sit in free and relay mode (T18). So nothing seats 3 AIs without keys today.

**New variables in `BP_Show`:** `AiSeats` (Integer, 0) and `DropCount` (Integer, 0).

**`LoadSwitches`** (no file; T07: it reads `Local/switches.json` at the start of each scene, and `ShowTitle` calls it before `SetupShow`): read `ai_seats` into `AiSeats` the way it reads the other switches. Connect the `GetField` wildcard output to the typed `Set AiSeats`, since a wildcard takes the type of what it is connected to (T01). A missing file or field must leave `AiSeats` at 0, the same as the other switches are reset there.

**`DrawCast`**, new content of `Graphs/BP_Show/DrawCast.txt` (the change is the block marked T53, between the loop and the `DRAW` print):

```lisp
(fn DrawCast ()
  (if (== (len (V AllPersonas)) 0)
    (set AllPersonas (V PersonaArr)))
  (bind (_ok _err) (Class|BPCLLMClient|StartShowSession :self (V LLMClient)))
  (if (not _ok)
    (CallFunction|SetUnavailable :Reason _err)
    (return false))
  (clear (V PersonaArr))
  (clear (V DrawList))
  (for _p (V AllPersonas)
    (bind _pv (Json|GetField _p "provider"))
    (set DrawProv _pv)
    (bind _c (Class|BPCLLMClient|CanSeat :self (V LLMClient) :Prov (V DrawProv)))
    (if _c
      (add (V PersonaArr) _p)
      (else
        (add (V DrawList) (V DrawProv)))))
  ; T53: the ai_seats switch seats fewer AIs (3 or more), dropped at random, for a 4-actor test show.
  ; 0 or missing seats every AI that can sit. DropCount is a variable, because a pure count would shrink as the loop removes.
  (if (and (>= (V AiSeats) 3) (< (V AiSeats) (len (V PersonaArr))))
    (set DropCount (- (len (V PersonaArr)) (V AiSeats)))
    (for _d (range (V DropCount))
      (Utilities|Array|RemoveIndex (V PersonaArr) (Math|Random|RandomIntegerinRange 0 (- (len (V PersonaArr)) 1)))))
  (print (cat "NHOS: DRAW ai=" (str (len (V PersonaArr))) " providers=" (Utilities|String|JoinStringArray (V DrawList) ",")))
  (if (< (len (V PersonaArr)) 3)
    (CallFunction|SetUnavailable :Reason "fewer than 3 AI players can take a seat.")
    (return false))
  (return true))
```

- The `if` has no `return`, at the top level, so the code after it joins both paths (T01). T30's warning about an `if` inside an else path doesn't apply here.
- `PersonaArr` is rebuilt from `AllPersonas` at every show, so the drop never loses a persona for good.
- The `DRAW` line then says `ai=3`. `providers=` lists only the providers `CanSeat` turned away, not the dropped persona.

**`Docs/switches.example.json`** (decision 6): add `"ai_seats": 0` after `"fast_lines": false`, and this sentence at the end of `_readme`: `ai_seats: seat only this many AI actors (3 or more), dropped at random from those that can sit, for a 4-actor test show; 0 or missing seats every AI that can sit. Set it back to 0 before a person plays.`

## 2. `WBP_Stage`: the clapperboard

### 2a. Where it goes

Today's layout (T27, T28, T29, T35), in 1920 × 1080 units (the UI scales by the short side, so 1600 × 900 and 1280 × 720 look the same):

| Piece | Where |
|---|---|
| `HeaderSize` (the header) | top left, 24 from the edges, at most 860 wide (right edge 884) |
| `BannerSize` (the banner) | top, x 900 to 1460, 24 from the top, in `StageArea` |
| `InfoSize` (my card) | top right, 420 wide, x 1476 to 1896, up to 1032 tall in Scene Prep |
| `LowerSize` (chat, vote row, input) | bottom left, 640 wide |
| `WBP_MoneyBurn`'s `BillSlot` | bottom right, 220 × 140, 24 from the edges (another widget, Z-order 10) |
| `StageArea` | last child of `RootBox`, so the stamp and the banner draw over everything |

**The clapperboard goes under the header,** left-aligned at x 24, 16 px (`S4`) below it (decision 1). The robots stand between the panels, and their feet sit above 47% of the height (T27), so the board keeps to the left edge over the proscenium column. Check the leftmost robot's name tag in the screenshots (part 5).

**Tree change:**

1. Wrap `HeaderSize` in a new VerticalBox, `TopLeftStack` (`UMGToolSet.WrapWidgets`; T14 used it). It takes `HeaderSize`'s place and slot in `RootBox` (HAlign Left, VAlign Top, padding 24). `HeaderSize` gets padding 0 inside it, so the header doesn't move. `TopLeftStack` is `SelfHitTestInvisible`.
2. Add the clapperboard as `TopLeftStack`'s second child (HAlign Left, top padding 16):

```
ClapperBox        VerticalBox, Collapsed at design time (SetClapper shows it), HitTestInvisible when shown
├ ClapStick       SizeBox, HeightOverride 24, Clipping ClipToBounds, slot HAlign Fill
│ └ ClapStickFrame  Border (StyleClapper sets an ink fill with an old-gold trim, radius 4), padding 2
│   └ ClapStripes   HorizontalBox, render transform Shear (-20, 0) set at design time
│     └ ClapStripe0 … ClapStripe5   Border each, slot Size Fill 1.0 (StyleClapper colors them: even paper, odd ink)
└ ClapBody        Border (StyleClapper: StylePanel "Ink"), padding 16 left and right, 8 top and bottom
  └ ClapText      TextBlock, "SCENE 1 / 4" at design time, justified left
```

- The stick fills the board's width, which `ClapBody`'s text sets (about 230 px for `SCENE 1 / 4` at 32 pt bold).
- The shear runs the stripes past the stick's ends; `ClipToBounds` on `ClapStick` cuts them off.
- **Is the shear property right?** In `ObjectTools.set_properties` the names are camelCase (T35): look for `renderTransform` with `shear` in `list_properties` on `ClapStripes`.
- **Anything that reads `HeaderSize`'s slot** breaks when the slot becomes a VerticalBox slot. Search `WBP_Stage` and `BP_Show` with `find_nodes` for `SlotAsOverlaySlot`. T38's bubble keep-out uses `HeaderSize`'s geometry, not its slot, so it still works (part 6).
- **Hiding:** the title (`WBP_Title`) and the end screen (`WBP_EndScreen`) set the whole stage widget's render opacity to 0 and back to 1 (`Graphs/WBP_Title/EventGraph.txt` lines 45 and 50, `Graphs/WBP_EndScreen/EventGraph.txt` lines 20 and 25). The board is inside `WBP_Stage`, so it hides with them and needs nothing more.

### 2b. Its text in each state

| When | The board | Set by |
|---|---|---|
| The title, and a show's start before the first Scene Prep | hidden (`Collapsed`, the design-time default) | the designer; `SetClapper(0, 0)` on Restart (optional, 1e) |
| Scene Prep, the 3 turns, Free Talk, the Cut, the reactions | `SCENE n / total`, for example `SCENE 2 / 4`, the same in every phase of a scene | `ShowPrep` → `SetClapper(SceneNum, SceneCount)` at each Scene Prep |
| The last scene | `SCENE 4 / 4` (no other look; the banner says "Last scene") | the same |
| After the show ends (the closing lines, "See the results") | the last count stays | nothing changes it |
| The end screen | hidden with the whole stage | `WBP_EndScreen` |

A 4-actor show reads `SCENE 1 / 3`, `SCENE 2 / 3`.

### 2c. The two functions

Both are new, so each gets a file. Create them with `add_function_graph`. `SetClapper` takes two Integer inputs, `Scene` and `Total` (`add_function_param`), and needs a compile before `BP_Show`'s call node is placed (T18: a function's call nodes go stale when it gets a new parameter).

`Graphs/WBP_Stage/StyleClapper.txt`:

```lisp
; T53: the clapperboard's look, all from UIStyle: an Ink slate under a striped clapstick.
; UIStyle's functions are impure (T32), so every value is bound before use.
(fn StyleClapper ()
  (bind fHead (Class|UIStyle|UIFont :Role "Header"))
  (bind cText (Class|UIStyle|UIColor :Role "Text"))
  (bind cPaper (Class|UIStyle|UIColor :Role "Paper"))
  (bind cInk (Class|UIStyle|UIColor :Role "InkSolid"))
  (bind cGold (Class|UIStyle|UIColor :Role "OldGold"))
  (bind trim (Class|UIStyle|UISize :Role "PanelTrim"))
  (bind rStick (Class|UIStyle|UISize :Role "S1"))
  (Class|UIStyle|StylePanel :Panel (Variables|WBP_Stage|GetClapBody) :Look "Ink")
  (bind bStick (Class|UIStyle|Brush :Fill cInk :Outline cGold :Width trim :Radius rStick))
  (Class|Border|SetBrushColor :self (Variables|WBP_Stage|GetClapStickFrame) :BrushColor (Utilities|Struct|MakeLinearColor 1.0 1.0 1.0 1.0))
  (Appearance|SetBrush :self (Variables|WBP_Stage|GetClapStickFrame) :InBrush bStick)
  (Class|Border|SetBrushColor :self (Variables|WBP_Stage|GetClapStripe0) :BrushColor cPaper)
  (Class|Border|SetBrushColor :self (Variables|WBP_Stage|GetClapStripe1) :BrushColor cInk)
  (Class|Border|SetBrushColor :self (Variables|WBP_Stage|GetClapStripe2) :BrushColor cPaper)
  (Class|Border|SetBrushColor :self (Variables|WBP_Stage|GetClapStripe3) :BrushColor cInk)
  (Class|Border|SetBrushColor :self (Variables|WBP_Stage|GetClapStripe4) :BrushColor cPaper)
  (Class|Border|SetBrushColor :self (Variables|WBP_Stage|GetClapStripe5) :BrushColor cInk)
  (Class|Text|SetFont :self (Variables|WBP_Stage|GetClapText) :Font fHead)
  (Class|Text|SetColorandOpacity :self (Variables|WBP_Stage|GetClapText) :ColorAndOpacity (Utilities|Struct|MakeSlateColor :SpecifiedColor cText)))
```

- The node names are the ones `UIStyle.StylePanel` and `WBP_UIStyleSheet`'s `EventGraph` already use (`Class|Border|SetBrushColor`, `Appearance|SetBrush`, `Class|Text|SetFont`, `Class|Text|SetColorandOpacity`).
- `Appearance|SetBrush` resolves to the Border's `SetBrush`; check it with `get_node_infos` (T32).
- The stripes keep their default white box brush, which `SetBrushColor` tints.
- **Contrast:** white 32 pt bold with a 2 px ink outline on the 92% ink panel, the same pair as the header (the doc measures text on ink at 5.4:1 or better). The stick's paper on ink is non-text and far above 3:1.

`Graphs/WBP_Stage/SetClapper.txt`:

```lisp
; T53: the clapperboard under the header, "SCENE n / total" from Scene Prep to the end of the show.
; BP_Show.ShowPrep calls it at each Scene Prep with SceneNum and SceneCount. A Scene under 1 hides it.
(fn SetClapper (Scene Total)
  (if (< Scene 1)
    (Widget|SetVisibility :self (Variables|WBP_Stage|GetClapperBox) :InVisibility "Collapsed")
    (return))
  (CallFunction|StyleClapper)
  (Class|Text|SetText :self (Variables|WBP_Stage|GetClapText) :Text (Utilities|Text|ToText(String) (cat "SCENE " (str Scene) " / " (str Total))))
  (Widget|SetVisibility :self (Variables|WBP_Stage|GetClapperBox) :InVisibility "HitTestInvisible")
  (print (cat "NHOS: CLAPPER scene=" (str Scene) " total=" (str Total))))
```

- It restyles on every call (once per scene, about 20 nodes), so the board never depends on an event chain in `WBP_Stage`'s `EventGraph`, which has no full source (`Graphs/WBP_Stage/EventGraph.StartButton.txt` holds only the Start button's chain). T34 can call `StyleClapper` from its own style pass.
- Widget variables need "Is Variable" on (`ClapperBox`, `ClapStickFrame`, `ClapStripe0` to `5`, `ClapBody`, `ClapText`).

### 2d. What `Graphs/WBP_Stage/` shows

- **No existing function updates a scene number or would carry the board.** The sources are `ShowBanner`, `NextBanner`, `FadeBanner` (the banner queue: `ShowBanner` prints `NHOS: BANNER <line>`, which part 5 reads), `SetPrompt` (the hint), `SetPrepMode` (shows or hides `PrepBox`, Start, Send and Pass; the board is outside `PrepBox` and stays as it is), `SetPassEnabled`, `SetTyping` and the Start button's `OnClicked`. None needs a change.
- **The calls that change the screen per scene come from `BP_Show`,** mostly through `BPC_LinePlayer`'s cue queue (`RunCue`: `"phase"` → `SetPhase`, `"banner"` → `ShowBanner`, `"prep"` → `ScenePrep`). `SetPhase` and `SetInfoTop` have no files. `SetClapper` joins them as an immediate call from `ShowPrep`.

## 3. `prompts.json`: `game`

Each line is given as it sits in the file (two tabs before it, escaped quotes as written). The Bot Prompts tab (rev 81) has no line that states the number of scenes. Its last rule line, `A tied vote cuts nobody and still uses up a scene. If the human is still on stage when the last scene ends, the human wins.`, is T52's to copy (T52 step 4; T50-build part 1 says the same), so T53 doesn't add it.

**a. "How a show works", line 22.** It keeps its number after T50 and T59, which change only lines below it.

- Now: `"- The cast has 4 or 5 actors. Scenes repeat until the human is cut or only two actors remain. Each scene has four parts.",`
- New, **not in the doc** (it words the Rules tab's "Number of scenes = cast size − 1: four scenes with 5 actors, three with 4" and "Repeat from Scene Prep until two actors remain or the last scene ends"): `"- The cast has 4 or 5 actors, and a show has one scene fewer than the cast: 4 scenes with 5 actors, 3 with 4. Scenes repeat until the human is cut, only two actors remain, or the last scene ends. Each scene has four parts.",`

**b. Optional (decision 9), "Reading the state", a new line right after line 33** (`"- The user message is a JSON object holding the state of the show. The game writes it.",`; about line 36 after T50), **not in the doc**:

`"- \"show\" says which scene this is (\"scene\"), how many scenes the show has (\"scenes\") and what is happening now (\"now\").",`

No line explains `show` today. After T52 and T54, the bots must weigh the last scene, so they need to know that `scenes` is the total.

**Lines that state the end of the show and stay as they are in T53:**

- Line 15: `"1. Find the human and get them cut. If the human is cut, the AIs win. If the human makes it to the final two, the human wins.",` is T54's (goal 1 gains the last-scene win). Until T54, line 22 says a show can end at its last scene while line 15 names only the final-two win. No run reaches the last scene before T52, and T52 and T54 come right after T53, so the gap is short.
- Line 18: `"  - You also want to reach the final two yourself.",` stays.
- Line 26 (The Cut, "the Director breaks ties") is T52 and T55's.
- `_readme` line 5 already lists `show {scene, scenes, now}`. No change.

## 4. `Tools/check_prompts.py`

**a. A new constant**, right after `SAMPLE_CAST` (line 471, `SAMPLE_CAST = ["visionary", "worrier", HUMAN, "overclocker", "copycat"]`):

```python
SAMPLE_SCENES = len(SAMPLE_CAST) - 1  # T53: a show has one scene fewer than the cast (4 with 5 actors)
```

**b. The three states.** Each `"scenes": 3` becomes `"scenes": SAMPLE_SCENES`:

| Line | Function | Now |
|---|---|---|
| 638 | `Show.actor_state` | `"show": {"scene": 1, "scenes": 3, "now": now},` (T50 changes `scene_card` on the line below) |
| 732 | `Show.card_cases` | `"show": {"scene": scene, "scenes": 3, "now": "the scene, turn 1 of 3"},` (T50 changes `scene_card` two lines below) |
| 766 | `Show.tiebreak_state` | `"show": {"scene": 1, "scenes": 3, "now": "the cut, tiebreak"},` (T55 removes this function later) |

The card sweep's cast list always holds all 5 actors (the cut ones as "cut, revealed AI"), so 4 is right for its scene 2 and scene 3 states too. The closing case's game messages ("Scene 2: ... Scene 3: ... who made the final two") still describe a possible show, since the human can reach the final two after 3 scenes.

**c. Optional (decision 10), `check_log`.** It checks that each show's scene count is its seat count − 1:

- After `human = None` / `cards = []` (lines 1058 and 1059), add `seats = total = None`.
- In the `SEATS` branch (from line 1061), after the `human=` match:

  ```python
                  m = re.search(r"seats=(\d+)", rest)
                  if m:
                      seats = int(m.group(1))
  ```

- In the `SETUP` branch (from line 1067), after the `scene=` match:

  ```python
                  m = re.search(r"\bscenes=(\d+)", rest)
                  if m:
                      total = int(m.group(1))
  ```

- Before the `Show {i}` summary (line 1106):

  ```python
          if seats and total and total != seats - 1:
              clock_bad += 1
              print(f"[FAIL] show {i} | SETUP | scenes={total}, but {seats} seats means {seats - 1} scenes")
  ```

  Add `clock_bad = 0` next to `n = bad = 0`, and append ` scene count = {total or 'unknown'}` to the summary line. Make the return `return 1 if bad or clock_bad else 0` (line 1108).
- Older logs have no `scenes=`, so `total` stays `None` and nothing fails.

**d. The module docstring.** Add a paragraph before `Exit code 0 means ...` (line 67), after T50's "Director's note (T50)" paragraph:

```
Scene clock (T53): a show has one scene fewer than the cast, so every sample
state says scenes = 4 (SAMPLE_SCENES). --log also fails a show whose SETUP
lines don't say scenes = its seat count - 1.
```

Drop the last sentence if you skip c.

**Not changed:** `CALLS_PER_SHOW = 90` (line 103) is the cost estimate for a 3-scene show. With T53 alone, no show plays a 4th scene. T52 makes a tie keep all 5 actors for another scene, so T52 should raise it.

**Run:** `python Tools/check_prompts.py --offline` must pass. If you add c, also `--log --all-shows <log>` on both run logs (part 5).

## 5. The check

The Done-when: a free autoplay show with 5 actors prints `scenes=4` in its `SETUP` line and sends `"scenes": 4` in the state; one with 4 actors gives 3; screenshots of the board in Scene Prep and in a scene turn; both shows reach `NHOS: SHOW END`.

### Run A: 5 actors, in a game window on the saved assets

`Local/switches.json`: `"autoplay": true`, `"mode": "free"`, `"spare_human": true`, `"fast_lines": true`, `"force_tie": false`, `"burn_test": false`, `"ai_seats": 0`.

- `spare_human` keeps me on stage, so the show plays every scene it can (three, down to two actors) and the board counts 1, 2, 3. Without it, the AIs usually cut me in scene 1 and the run shows one `SETUP`.
- `force_tie` stays off. Until T52, a forced tie only sends the tie to the Director, who still cuts.

```bash
"<UE_ROOT>/Engine/Binaries/Win64/UnrealEditor.exe" "<PROJECT>" -game -windowed -ResX=1600 -ResY=900 -log=T53five.log
```

On Windows the log is `Saved/Logs/T53five.log`. On a Mac it is `~/Library/Logs/AIMegaJam2026/T53five.log` (T27). Then:

```bash
grep -E "NHOS: (DRAW|SEATS|SETUP|STATE|CLAPPER|BANNER (Scene|Last)|REACTIONS DONE|SHOW END)" Saved/Logs/T53five.log
```

Expected, in order (`<…>` varies):

```
NHOS: DRAW ai=4 providers=
NHOS: SEATS human=<n> seats=5 cast=<ids>
NHOS: SETUP human=human scene=<card> note=<id> category=<cat> scenes=4
NHOS: CLAPPER scene=1 total=4
NHOS: BANNER Scene 1: <title>
NHOS: STATE Player <k> show={"scene":1,"scenes":4,"now":"the scene, turn 1 of 3"}      (4 lines, one per AI)
NHOS: REACTIONS DONE scene=1 entries=<n>
... the same for scenes 2 and 3 (3 and 2 AIs on stage, so 3 and 2 STATE lines) ...
NHOS: SHOW END result=win scenes=3
```

No `LogScript` warning, and the `NHOS: LOG` lines have the same 4 fields as before.

### Run B: 4 actors

The same switches with `"ai_seats": 3`, and `-log=T53four.log`. Expected:

```
NHOS: DRAW ai=3 providers=
NHOS: SEATS human=<n> seats=4 cast=<ids>
NHOS: SETUP ... scenes=3
NHOS: CLAPPER scene=1 total=3
NHOS: STATE Player <k> show={"scene":1,"scenes":3,...}      (3 lines)
... scene 2 ...
NHOS: SHOW END result=win scenes=2
```

Both runs end at two actors before the last scene, as T53.md says. The `LastSceneDone` branch is built but not played here. T52's `force_tie` run plays it (`SHOW END` after scene 4 of 4).

### The screenshots: PIE by hand

PIE in a 1600 × 900 floating window, Test for Free, `autoplay` false, `ai_seats` 0. On the PC the Slate inspector's clicks land. On the Mac they don't (T33-1), so play this part on the PC. Save the shots in `Saved/T53/shots/` (not in git):

1. **`prep.png`:** Scene Prep of scene 1. The board reads `SCENE 1 / 4` under the header, the banner reads "Scene 1: <title>", and the full card is at the right. Nothing needs a click: Scene Prep waits for Start the scene.
2. **`turn1.png`:** press Start the scene (the Start button, or Enter if T34 made it focusable). Turn 1 waits for my line. The board is still `SCENE 1 / 4`, and the header shows the turn.
3. The same two at 1280 × 720 (`prep_p12.png`, `turn1_p12.png`). The doc checks every screen at both sizes.

In each shot, check what a first-time player would see:

- The board doesn't touch the header or cover a robot, its name tag or a thrown prop. Look hardest at the leftmost robot.
- The stripes read as a clapperboard, not as a warning bar.
- The count is readable at a glance.

If the board covers a name tag, use the fallback in decision 1 and say so under Findings. A scene-2 shot (`SCENE 2 / 4`) is optional: run A's `CLAPPER` lines already show the count moving.

**Afterward:** set `autoplay`, `spare_human` and `fast_lines` back to false and `ai_seats` to 0 in `Local/switches.json`, and close each game window.

## 6. Knock-on: tell, don't change (except where noted)

- **`Docs/ItchPage.md`** (decision 11; outside T53's Touches, so name it in the commit):
  - Line 58, now: `5. Repeat until two actors are left. A full cast plays three scenes.` New: `5. Repeat until two actors are left or the last scene ends. A cast of five has four scenes, a cast of four has three.` T54 rewrites the win wording around it.
  - Line 116, now: `- With all 4 keys, the cast is four AIs and you, over three scenes. With 3 keys, the lab without a key sits out, and the show has three AIs and you, over two scenes. ...` New: `- With all 4 keys, the cast is four AIs and you, over up to four scenes. With 3 keys, the lab without a key sits out, and the show has three AIs and you, over up to three scenes. ...` (the rest unchanged).
- **The design doc's UI section** (decision 12; show it to my person, edit only after their OK): a new row in the Components table, after "Header": `Clapperboard | A small ink slate under the header, top left, with a striped clapstick. SCENE 2 / 4 in display type. | Set at each Scene Prep; the same in every phase of a scene. Hides with the stage on the title and end screens.` The Rules tab already has the rule and the "Always" row. Nothing else in the doc changes.
- **T52:** call `LastSceneDone()` after a tie (1f). Raise `CALLS_PER_SHOW` in the checker, since a tie keeps all 5 actors for another scene.
- **T54:** `game` line 15 (the win), `EndShow`'s two win texts, and `Docs/ItchPage.md`'s win lines. `reason=last_scene` comes from the `LastSceneDone` branch.
- **T34 (the header):** the doc's header shows "scene and turn as pips". The board now carries the scene, so the header needs only the turn. Keep the board under the header, or move it into the header if T34 redraws it, and call `StyleClapper` from T34's style pass.
- **T38 (the speech bubbles):** add `ClapperBox` to `WBP_Stage.KeepOut` next to `HeaderSize` (`T38-build.md`, part E5 and the `AddKeep` calls), so a bubble never covers the board. `HeaderSize` now sits inside `TopLeftStack`. Its geometry is unchanged, but E5's survey of `RootBox`'s children will list `TopLeftStack` in its place.
- **T44:** `Docs/tasks/T44-build/check_prompts.patch` has `"scenes": 3` in its context lines (patch lines 318 and 327). After T53 they read `SAMPLE_SCENES`, so that patch won't apply as it is. T44's session refreshes it, or uses `patch_check_prompts.py` if that script matches by text.
- **T61 (the stagehand):** the doc's tip list says later shows "keep the scene card, the clapperboard and the 'passed' markers". Nothing to do now.
