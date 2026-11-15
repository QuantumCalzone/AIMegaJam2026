# T61 build sheet: the stagehand's earpiece, the tips toggle and How to play

Back to [T61](T61.md). A Mac prep session wrote this on 2026-11-15, without the editor. It is written against **`noHumansOnSet` at `42b1189` (T36)**. When I finished, `origin/noHumansOnSet` was at `407a9e6`, which changes only `Tools/ClaudeMods/` and nothing this sheet names. The design doc was read, not changed: Rules tab rev 27 ("Onboarding": "The Stagehand", "What the player sees, and when", "Supporting pieces").

**What moves before T61 runs.** The PC's chain runs T52, T54, T55, T57, T58, T38, T34 and T60 before T61, and each one changes `BP_Show` or `WBP_Stage`. So this sheet keeps the `BP_Show` part short (part 7) and names each place by its function and the node next to it, not by node number. Every row marked **re-check** must be found again in the editor first. The parts that are new and won't move are written out in full: the data file (part 1), `BPC_Stagehand` (part 2), `WBP_Earpiece` (part 3), the progress file (part 4), `WBP_Title` (part 5) and `WBP_HowToPlay` (part 6).

Drafts in [`T61-build/`](T61-build/):

- [`stagehand.json`](T61-build/stagehand.json): the data file, ready to copy to `Content/NHOS/Data/stagehand.json`. Every moment's line is the doc's earpiece line word for word, with straight apostrophes, as `prompts.json` copies the doc. The longest line is 22 words (`free_talk_1`); the style tips are 13 words or fewer.
- [`how_to_play.md`](T61-build/how_to_play.md): the six How to play bullets. **A draft waiting for my person's OK** (T61 step 6).

## In short

- **A data file,** `Content/NHOS/Data/stagehand.json`: seven moments with the doc's earpiece lines, five style tips keyed by the moment they follow, the three opening lines and the hold times.
- **A new component, `BPC_Stagehand`,** on `BP_Show` as `Stagehand`. `BeginShow()` decides at each show's draw whether this show teaches. `Say(Key)` shows a key's lines once per show. `EndShow(Win, Reason)` says the win or lose line and turns the tips off for the next show. `TipsNext()` and `SetTipsNext(On)` serve the title's toggle. It never touches the shared log, `game_messages` or `BPC_LLMClient`.
- **A new overlay, `WBP_Earpiece`,** in the viewport at Z 15, like `WBP_MoneyBurn`: a full-screen `HitTestInvisible` canvas with one ink panel at the bottom center (over the house floor, clear of the card, the clapperboard, the chat column and the bill). The line is in a new `UIStyle` color, `Earpiece` (rose, `#FF9EC4`). It fades in, holds for its reading time, and fades out. On the end screens it moves up above the buttons. `WBP_Stage` doesn't change.
- **The first-show flag:** `Local/progress.json` holds `{"tips": true|false}`. A missing file means tips on. The end of a teaching show writes `false`. The title's toggle writes `true`. Autoplay never writes it.
- **`WBP_Title`:** T33's How to play ink panel becomes "Tonight's show": the three opening lines, a **How to play** button and a **Stagehand tips: on/off** button, both Secondary, focusable, with T33's gold focus ring.
- **A new screen, `WBP_HowToPlay`:** an ink panel with the six bullets and a Close button (Primary, focused). Escape closes it too.
- **`BP_Show`:** the component, one new function (`CueTip`, a "tip" cue in T30's line queue, so a tip shows when the screen reaches its moment), one new branch in `RunCue`, and one call per moment (seven places).
- **`check_prompts.py --offline`:** the file is valid, every moment has a line, no line is over 25 words (style tips: 15), the three opening lines are on `Docs/ItchPage.md`, no banned name. `--log` fails a stagehand line found in an `NHOS: LOG`, `STATE` or `CLOSING` line.
- **`Docs/ItchPage.md`:** the three opening lines at the top of "Page text".

## Decisions made for my person

My person asked prep sessions to take the task's default or their own recommendation on calls that are theirs. Each is open to change. The T61 session shows this list to my person when it closes the task.

1. **The three opening lines** are the doc's "Before the show" On screen cell, one phrase per line, with capitals and full stops added and one comma: "You're the only human." / "Each scene, the cast cuts whoever seems human." / "Survive to the final two or the last scene." The doc gives them only as a list separated by semicolons.
2. **Where the opening lines show:** on the title screen, in place of T33's How to play block, under a "Tonight's show" heading. That is the "before the show" screen, and T33 left the block there for T61 to replace. The title shows before every show except autoplay and a relaunch, so the lines show every time, as the doc's On screen column means them to. A Play Again restart skips the title, so it skips the lines too.
3. **When the "before the show" earpiece line plays:** at the first Scene Prep, just before the Scene Prep line, in the same queue. The earpiece is an in-show channel, and nothing in the show happens between the title and the first Scene Prep.
4. **Where the style tips go** ("one idea per line across the first scene"): plain sentences after the Scene Prep line, the 15-word cap after the turn 1 line, no caps or emoji at turn 2, don't go quiet at turn 3, and don't over-polish at Free Talk round 2. That spreads five lines over the first round, never two new ideas at once, except the paired line at Scene Prep and turn 1. "Don't over-polish" lands in Free Talk because that is where the bots judge polish (T57). Their wording is mine: the doc lists only the ideas.
5. **The lose line names T60's top reason.** The doc's earpiece cell says the lose line "names the reason with the most votes", with "They caught you copying late." as its example. So `lose.line` holds that example, and `EndShow` says T60's top-reason line instead when there is one. T60 also shows that reason as the lose screen's large line, so on a first show the same words show twice: once in the earpiece, once on the screen. I recommend keeping both, because later shows have no earpiece and still need the lesson. If the screenshot reads as a repeat, the other way is to skip the earpiece on a loss when T60's line is on screen (an empty `Reason` and `lose.line` set to ""; the checker then needs `lose` allowed an empty line).
6. **The toggle turns tips on for the next show only.** "On brings the tips back for the next show" (T61 step 5). When that show ends, the tips go off again, as after a first show. The toggle shows the state the next show will have. The other way, a toggle that stays on until turned off, needs a second field in the progress file.
7. **A show that never reaches its end screen leaves the tips on:** quitting mid-show, the relay going down, or Back to title. A judge who quits the first show halfway still gets the tips next time.
8. **Autoplay:** tips are off unless a new switch, `stagehand_tips`, is true in `Local/switches.json`. Autoplay never writes `Local/progress.json`, so a check run doesn't use up my first show. The switch goes into `Docs/switches.example.json` (outside T61's Touches: name it in the commit message).
9. **The earpiece is its own overlay, not part of `WBP_Stage`,** in the viewport at Z 15 (`WBP_Stage` is under it, `WBP_EndScreen` and `WBP_MoneyBurn` are at 10, the title at 20). It has to show over the end screen, which hides `WBP_Stage`, and T34 rebuilds `WBP_Stage` just before T61. So `WBP_Stage` doesn't change, though T61's Touches name it. `WBP_MoneyBurn` (T35) is the same kind of overlay.
10. **Where it sits:** bottom center, 24 px from the bottom (`UISize "Edge"`), at most 720 px wide. Today that is the empty house floor between the chat column (bottom left, 640 wide) and the bill (bottom right, 220 wide); it is clear of the card (top right), the clapperboard (top left, under the header) and the banner (top). On the end screens it rises by a button's height plus two edges (96 px), above the button row. T34 and T38 change the in-show screen first, so T61 checks both spots in its screenshots.
11. **Its look:** an ink panel (`StylePanel "Ink"`) with a 6 px rose bar on the left, a caption "Stagehand, in your earpiece" in quiet text, and the line in rose at speech size (20). Rose is a new `UIStyle` role, `Earpiece`, `#FF9EC4`: no seat, no state and no stamp uses a pink, and it measures about 9.6:1 on ink. It needs one line in `UIStyle.UIColor` (outside T61's Touches: name it in the commit) and a row in the doc's palette after my person's OK (part 8).
12. **Its timing:** each line holds for 2.0 + 0.3 s per word, between 4 and 9 s, with a 0.25 s fade in and out (`UITime "Panel"`) and a 0.5 s gap before the next line. The hold numbers live in `stagehand.json`, like `pacing.json`'s. A 20-word line holds 8 s.
13. **The tips toggle is a button, not a check box:** "Stagehand tips: on" / "Stagehand tips: off", Secondary. A check box has no `UIStyle` style, and a button takes T33's focus ring and works by keyboard (T33: Slate inspector clicks don't land on the Mac).
14. **Escape closes How to play,** as well as the Close button. The doc says it's never forced.
15. **The Free Talk moment's key is `free_talk_1`,** to match `scene_turn_1`; Free Talk raises `free_talk_<round>`, and the style tip uses `free_talk_2`.
16. **The check for "no tip text in any state sent to an AI":** the game doesn't log request bodies (no `BPC_LLMClient` graph prints one), so the check searches what the log has: every `NHOS: LOG`, `STATE` and `CLOSING` line, with a new `--log` check in `check_prompts.py`, plus a search of `BPC_Stagehand`'s graphs for any node that reads `SharedLog`, `GameMessages` or `BPC_LLMClient` (there must be none). Adding a body print to `BPC_LLMClient` for one run is the other way; I recommend against it, because that component has no lock in T61's Touches.
17. **Two docs outside T61's Touches** get one line each: the `Local/` row of `CLAUDE.md` and of `README.md` name `progress.json`, and the packaging notes say to delete it with `llm_key.json` before zipping. I recommend doing it in T61's commit and naming the files.

## 0. Before you start

1. The chain's tasks before T61 are pushed (T52, T54, T55, T57, T58, T38, T34, T60), their claims are released, and `git lfs locks` shows no lock on `BP_Show.uasset`, `WBP_Title.uasset` or `UIStyle.uasset`.
2. **Re-read the rules the lines teach** in the doc's Rules tab. If a line in the Onboarding table changed since rev 27, copy the new words into `stagehand.json` (and fix the `--offline` check's list, part 9). If T60 or T57 changed a rule (for example the Free Talk round count), check that `how_to_play.md` still says it.
3. **Re-check every row marked re-check in part 7a** against the graphs as the chain left them. Start from `Graphs/BP_Show/` files where they exist, and read only the graphs named there.
4. **T60's top reason:** find how `ShowEndScreen` (or the function T60 added) holds the top reason's line. Part 7a's `end` row passes it to `EndShow`. If T60 kept no line in a variable, add one there (T60's `NHOS: TOP REASON <tell>` line names the tell; the line comes from T60's data file).
5. **T34's layout:** where the in-show panels sit now. If anything new is at the bottom center (a roster strip, T38's bubbles, the vote tickets), move the earpiece's stage spot (part 3c) before you build the rest.
6. **The Mac clicks rule (T33):** on the Mac, Slate inspector clicks don't land; drive the title's new buttons by keyboard (Tab, Enter). If T34 made the in-show buttons focusable (row T33-1), a whole show can be played by keyboard.
7. `python Tools/check_prompts.py --offline` passes before you start.

## 1. The data file: `Content/NHOS/Data/stagehand.json`

Copy [`T61-build/stagehand.json`](T61-build/stagehand.json) to `Content/NHOS/Data/stagehand.json` as it is (step 2 of part 0 says when to change a line). `DefaultGame.ini` already stages `Content/NHOS/Data` as loose files, so a build picks it up with no config change.

| Field | What it holds | Who reads it |
|---|---|---|
| `moments.<key>.line` | The doc's earpiece line, word for word | `BPC_Stagehand.Say` |
| `moments.<key>.when` | Where `BP_Show` raises the key (for people) | nobody |
| `moments.<key>.spot` | `stage` or `end` | `BPC_Stagehand.Next` → `WBP_Earpiece.SetSpot` |
| `moments.lose.from` | `top_reason`: `EndShow`'s `Reason` replaces the line | people; `EndShow` does it for `lose` |
| `style.<key>` | One style tip, played after that key's moment line | `BPC_Stagehand.Say` |
| `opening_lines` | The three lines before the show | `WBP_Title` (Construct), the checker, `Docs/ItchPage.md` |
| `hold.base`, `per_word`, `min`, `max`, `gap` | Seconds | `BPC_Stagehand.Load` |

The keys `BP_Show` raises: `before_show`, `scene_prep`, `scene_turn_1` to `scene_turn_3`, `free_talk_1` to `free_talk_3`, `the_cut`, and `EndShow` raises `win` or `lose`. A key with neither a moment nor a style tip is fine (for example `scene_turn_2` in a later scene, or `free_talk_3`): `Say` marks it shown and shows nothing.

## 2. The component: `BPC_Stagehand`

`/Game/NHOS/Core/BPC_Stagehand`, an `ActorComponent` Blueprint, made the way T20 made `BPC_ShowAudio` and T30 made `BPC_LinePlayer` (read their findings for the create call). Add it to `BP_Show`'s components as `Stagehand` (part 7). It needs no tick.

### 2a. Variables

| Name | Type | Default | What for |
|---|---|---|---|
| `Loaded` | Boolean | false | The file was read |
| `Data` | JsonObject | | The whole file |
| `Moments` | JsonObject | | `Data.moments` |
| `Style` | JsonObject | | `Data.style` |
| `HoldBase`, `HoldPerWord`, `HoldMin`, `HoldMax`, `Gap` | Float | 2.0, 0.3, 4.0, 9.0, 0.5 | `Data.hold` (the defaults hold if the file lacks them) |
| `TipsOn` | Boolean | false | This show teaches |
| `Autoplay` | Boolean | false | From `Local/switches.json` at `BeginShow` |
| `Shown` | Array of String | | Keys already raised in this show |
| `QKey`, `QLine`, `QSpot` | Array of String | | The queue of lines still to show |
| `Busy` | Boolean | false | A line is on screen |
| `Ear` | `WBP_Earpiece` object reference | | Made on first use |
| `TmpS` | String | | For a JSON field read (the `set` resolves `GetField`'s type, as `LoadPacing` does) |
| `TmpB` | Boolean | | Same, for a boolean field |

### 2b. Functions

Sources go in `Graphs/BPC_Stagehand/<Function>.txt`, one per function, and through `Tools/dslpp.py` before `write_graph_dsl`. The node names follow the pushed sources (`LoadPacing`, `SaveKeys`, `DrawCast`, `NextBanner`). Two are new to this repo and need a `find_node_types` check first: `Utilities|Array|Contains` (the array "Contains Item" node; `Utilities|Array|FindItem` ≥ 0 does the same) and the shape of `Json|GetField` into a `JsonObject` variable (`LoadPacing` does it with `Pace`).

**`Load()`**

```lisp
; T61: reads Content/NHOS/Data/stagehand.json once per run. A missing or broken file leaves Loaded false,
; and every Say does nothing (the show plays on without tips).
(fn Load ()
  (set Loaded false)
  (bind _p (cat (Utilities|Paths|GetProjectContentDirectory) "NHOS/Data/stagehand.json"))
  (bind (_o _ok) (Json|LoadJsonfromFile (Utilities|Struct|MakeFilePath _p)))
  (if (not _ok)
    (print "NHOS: STAGEHAND file missing or not valid JSON")
    (return))
  (set Data _o)
  (bind _m (Json|GetField (V Data) "moments"))
  (set Moments _m)
  (bind _s (Json|GetField (V Data) "style"))
  (set Style _s)
  (bind _hh (Json|HasField (V Data) "hold"))
  (if _hh
    (bind _h (Json|GetField (V Data) "hold"))
    (bind _h1 (Json|GetField _h "base"))
    (set HoldBase _h1)
    (bind _h2 (Json|GetField _h "per_word"))
    (set HoldPerWord _h2)
    (bind _h3 (Json|GetField _h "min"))
    (set HoldMin _h3)
    (bind _h4 (Json|GetField _h "max"))
    (set HoldMax _h4)
    (bind _h5 (Json|GetField _h "gap"))
    (set Gap _h5))
  (set Loaded true)
  (print "NHOS: STAGEHAND loaded"))
```

`_h` is a JsonObject from `GetField`; if the DSL can't bind a wildcard to an object, add a `Hold` JsonObject variable and `set` it, as `LoadPacing` does with `Pace`.

**`BeginShow()`**: `BP_Show` calls it at each show's draw (part 7a). It resets the show and decides whether this show teaches.

```lisp
; T61: a new show. Tips show on a teaching show: the first show (no Local/progress.json), or after the
; title's toggle set tips to true. With autoplay on, only if switches.json has stagehand_tips true.
(fn BeginShow ()
  (if (not (V Loaded))
    (CallFunction|Load))
  (CallFunction|Hush)
  (clear (V Shown))
  (bind _dir (Utilities|Paths|GetProjectDirectory))
  (set Autoplay false)
  (set TmpB false)
  (bind (_sw _swok) (Json|LoadJsonfromFile (Utilities|Struct|MakeFilePath (cat _dir "Local/switches.json"))))
  (if _swok
    (bind _ha (Json|HasField _sw "autoplay"))
    (if _ha
      (bind _a (Json|GetField _sw "autoplay"))
      (set Autoplay _a))
    (bind _ht (Json|HasField _sw "stagehand_tips"))
    (if _ht
      (bind _t (Json|GetField _sw "stagehand_tips"))
      (set TmpB _t)))
  (if (V Autoplay)
    (set TipsOn (V TmpB))
    (print (cat "NHOS: STAGEHAND tips=" (select (V TipsOn) "on" "off") " why=autoplay"))
    (return))
  (bind _next (CallFunction|TipsNext))
  (set TipsOn (and _next (V Loaded)))
  (print (cat "NHOS: STAGEHAND tips=" (select (V TipsOn) "on" "off") " why=progress")))
```

**`TipsNext()` → Boolean**: what the next show will do. The title's toggle shows it.

```lisp
; T61: Local/progress.json's "tips". A missing file, or one without the field, means true (a first show).
(fn TipsNext ()
  (bind _p (cat (Utilities|Paths|GetProjectDirectory) "Local/progress.json"))
  (bind (_o _ok) (Json|LoadJsonfromFile (Utilities|Struct|MakeFilePath _p)))
  (if (not _ok)
    (return true))
  (bind _h (Json|HasField _o "tips"))
  (if (not _h)
    (return true))
  (bind _t (Json|GetField _o "tips"))
  (set TmpB _t)
  (return (V TmpB)))
```

**`SetTipsNext(On)` → Boolean (saved)**: the title's toggle, and `EndShow`.

```lisp
; T61: writes Local/progress.json. The key screen's SaveKeys writes Local/llm_key.json the same way.
(fn SetTipsNext (On)
  (bind _o (Json|LoadJsonfromString "{}"))
  (Json|SetField _o "tips" On)
  (bind _p (cat (Utilities|Paths|GetProjectDirectory) "Local/progress.json"))
  (bind _ok (Json|SaveJsontoFile _o (Utilities|Struct|MakeFilePath _p)))
  (print (cat "NHOS: STAGEHAND saved tips=" (Utilities|String|ToString(Boolean) On) " ok=" (Utilities|String|ToString(Boolean) _ok)))
  (return _ok))
```

`Json|SetField` takes a wildcard value (`BPC_LLMClient` uses it with strings and objects). If it won't take a Boolean, build the object from a string instead: `(Json|LoadJsonfromString (select On "{\"tips\": true}" "{\"tips\": false}"))` (T01: escaped quotes in a DSL string come through as plain quotes).

**`Say(Key)`**: one node per moment in `BP_Show`.

```lisp
; T61: shows a key's moment line, then its style tip, once per show, on a teaching show only.
; Static text for the player's screen: it never goes to the shared log, game_messages or an AI.
(fn Say (Key)
  (if (not (V TipsOn))
    (return))
  (if (Utilities|Array|Contains (V Shown) Key)
    (return))
  (add (V Shown) Key)
  (bind _hm (Json|HasField (V Moments) Key))
  (if _hm
    (bind _m (Json|GetField (V Moments) Key))
    (bind _l (Json|GetField _m "line"))
    (set TmpS _l)
    (bind _sp (Json|GetField _m "spot"))
    (CallFunction|Enqueue :Key Key :Line (V TmpS) :Spot _sp))
  (bind _hs (Json|HasField (V Style) Key))
  (if _hs
    (bind _st (Json|GetField (V Style) Key))
    (set TmpS _st)
    (CallFunction|Enqueue :Key (cat Key " style") :Line (V TmpS) :Spot "stage")))
```

`_sp` is a String from `GetField`; if it stays a wildcard, `set` it into a second string variable first, as `TmpS`.

**`Enqueue(Key, Line, Spot)`**

```lisp
(fn Enqueue (Key Line Spot)
  (if (Utilities|String|IsEmpty Line)
    (return))
  (add (V QKey) Key)
  (add (V QLine) Line)
  (add (V QSpot) Spot)
  (if (not (V Busy))
    (CallFunction|Next)))
```

**`Next()`**: one line on screen at a time, like `BPC_LinePlayer.Pump` and `WBP_Stage.NextBanner`.

```lisp
; T61: puts the next line in the earpiece, then waits for its fade in, its hold, its fade out and the gap.
(fn Next ()
  (if (== (len (V QKey)) 0)
    (set Busy false)
    (return))
  (set Busy true)
  (bind _k (get (V QKey) 0))
  (bind _l (get (V QLine) 0))
  (bind _s (get (V QSpot) 0))
  (Utilities|Array|RemoveIndex (V QKey) 0)
  (Utilities|Array|RemoveIndex (V QLine) 0)
  (Utilities|Array|RemoveIndex (V QSpot) 0)
  (if (not (Kismet|IsValid (V Ear)))
    (bind _w (UserInterface|CreateWidget "/Game/NHOS/UI/WBP_Earpiece.WBP_Earpiece_C" (Game|GetPlayerController 0)))
    (set Ear _w)
    (UserInterface|Viewport|AddtoViewport :self (V Ear) :ZOrder 15))
  (bind _n (len (Utilities|String|ParseIntoArray :SourceString _l :Delimiter " " :CullEmptyStrings true)))
  (bind _hold (Math|Float|Clamp(Float) :Value (+ (V HoldBase) (* (V HoldPerWord) _n)) :Min (V HoldMin) :Max (V HoldMax)))
  (bind _fade (Class|UIStyle|UITime :Role "Panel"))
  (print (cat "NHOS: TIP " _k " words=" (str _n) " hold=" (Utilities|String|ToString(Float) _hold)))
  (Class|WBPEarpiece|SetSpot :self (V Ear) :Spot _s)
  (Class|WBPEarpiece|Play :self (V Ear) :Line _l :Hold _hold)
  (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "Next" :Time (+ (+ _hold (* 2.0 _fade)) (V Gap)) :bLooping false))
```

- `NHOS: TIP <key>` prints when the line reaches the screen, not when it is raised, so the log shows what I saw. A style tip prints `NHOS: TIP scene_turn_2 style`.
- The IsValid node's name is a guess (`Kismet|IsValid` or `Utilities|IsValid`); check with `find_node_types`.
- `UITime` is impure (T32), so it is bound before use.

**`Hush()`**: clears the queue and the earpiece (a new show, or a restart mid-line).

```lisp
(fn Hush ()
  (Utilities|Time|ClearTimerbyFunctionName :Object self :FunctionName "Next")
  (clear (V QKey))
  (clear (V QLine))
  (clear (V QSpot))
  (set Busy false)
  (if (Kismet|IsValid (V Ear))
    (Class|WBPEarpiece|Clear :self (V Ear))))
```

**`EndShow(Win, Reason)`**: one node at the end screen (part 7a).

```lisp
; T61: the win or lose line over the end screen, then the next show won't teach (until the title's toggle).
; Reason is T60's top-reason line on a loss, or "" (then the doc's example line is said).
(fn EndShow (Win Reason)
  (if (V TipsOn)
    (if (or Win (Utilities|String|IsEmpty Reason))
      (CallFunction|Say :Key (select Win "win" "lose"))
      (else
        (add (V Shown) "lose")
        (CallFunction|Enqueue :Key "lose" :Line Reason :Spot "end")))
    (if (not (V Autoplay))
      (CallFunction|SetTipsNext :On false))))
```

- `TipsOn` stays true until the next `BeginShow`, so the end line still shows after the file says false.
- A show that never reaches its end screen never calls `EndShow`, so the tips stay on (decision 7).
- A show that taught nothing (tips off) writes nothing.

### 2c. What it must never do

No node in `BPC_Stagehand` reads or writes `SharedLog`, `GameMessages`, `LineEntry` or anything on `BPC_LLMClient`, and no `BP_Show` graph passes a stagehand line on. Check it with `find_nodes` in `BPC_Stagehand` for `SharedLog`, `GameMessages` and `BPC_LLMClient` (none), and in `BP_Show` for callers of `BPC_Stagehand` (only part 7a's nodes, and `WBP_Title`'s calls).

## 3. The earpiece: `WBP_Earpiece`

`/Game/NHOS/UI/WBP_Earpiece`, a new Widget Blueprint, built as T35 built `WBP_MoneyBurn` (a full-screen overlay that never takes a click or focus). Every value comes from `UIStyle`.

### 3a. Tree

```
Root            CanvasPanel, full screen, HitTestInvisible
└ EarBox        SizeBox, MaxDesiredWidth 720; canvas slot anchored bottom center (0.5, 1), alignment (0.5, 1),
                position (0, -24), auto size; Collapsed at design time (Play shows it)
  └ EarFrame    Border (StylePanel "Ink"), padding 16 left and right, 12 top and bottom
    └ EarRow    HorizontalBox
      ├ EarBarBox   SizeBox, WidthOverride 6 (UISize "SeatBar"), slot VAlign Fill
      │ └ EarBar    Border (PreConstruct: the Earpiece color, radius 3)
      ├ Spacer      12 wide (UISize "S3")
      └ EarCol      VerticalBox, slot Size Fill 1.0
        ├ EarLabel  TextBlock "Stagehand, in your earpiece", Caption, Quiet
        └ EarText   TextBlock, Speech, Earpiece color, AutoWrapText on, top padding 4 (S1)
```

- The canvas slot's position is the spot. `SetSpot` moves it between the stage spot (y −24) and the end spot (y −96).
- Use a CanvasPanel slot, not an Overlay slot, so `SetSpot` only changes the position (`Layout|CanvasPanelSlot|SetPosition` on `SlotAsCanvasSlot` of `EarBox`; check the names with `find_node_types`).
- `HitTestInvisible` on the root, so the earpiece never blocks a click on the input row, the ballot or Play Again under it.

### 3b. Graphs

`Graphs/WBP_Earpiece/EventGraph.txt`:

```lisp
; WBP_Earpiece.EventGraph (T61). The stagehand's line: an ink panel with a rose bar, a caption and the line in rose.
; Every color, size and font comes from UIStyle. It never takes a click or keyboard focus.
(event UserInterface|EventPreConstruct (IsDesignTime)
  (bind ear (Class|UIStyle|UIColor :Role "Earpiece"))
  (bind quiet (Utilities|Struct|MakeSlateColor :SpecifiedColor (Class|UIStyle|UIColor :Role "Quiet")))
  (Class|UIStyle|StylePanel :Panel (Variables|WBP_Earpiece|GetEarFrame) :Look "Ink")
  (Appearance|SetBrush :self (Variables|WBP_Earpiece|GetEarBar) :InBrush (Class|UIStyle|Brush :Fill ear :Outline ear :Width 0.0 :Radius 3.0))
  (Class|Text|SetFont :self (Variables|WBP_Earpiece|GetEarLabel) :Font (Class|UIStyle|UIFont :Role "Caption"))
  (Class|Text|SetColorandOpacity :self (Variables|WBP_Earpiece|GetEarLabel) :ColorAndOpacity quiet)
  (Class|Text|SetFont :self (Variables|WBP_Earpiece|GetEarText) :Font (Class|UIStyle|UIFont :Role "Speech"))
  (Class|Text|SetColorandOpacity :self (Variables|WBP_Earpiece|GetEarText) :ColorAndOpacity (Utilities|Struct|MakeSlateColor :SpecifiedColor ear))
  (Class|TextLayoutWidget|SetAutoWrapText :self (Variables|WBP_Earpiece|GetEarText) :AutoWrapText true)
  (if IsDesignTime
    (Widget|SetVisibility :self (Variables|WBP_Earpiece|GetEarBox) :InVisibility "HitTestInvisible")
    (Class|Text|SetText :self (Variables|WBP_Earpiece|GetEarText) :Text (Utilities|Text|ToText(String) "I could only get you the category. They have the full note, and they know you don't. Watch turn 1."))))
```

Variables: `Alpha` (Float), `Fading` (Integer: 1 in, 0 hold, −1 out), `HoldLeft` (Float).

`Play(Line, Hold)`:

```lisp
(fn Play (Line Hold)
  (Class|Text|SetText :self (Variables|WBP_Earpiece|GetEarText) :Text (Utilities|Text|ToText(String) Line))
  (set HoldLeft Hold)
  (set Alpha 0.0)
  (set Fading 1)
  (Widget|SetRenderOpacity :self (Variables|WBP_Earpiece|GetEarBox) :InOpacity 0.0)
  (Widget|SetVisibility :self (Variables|WBP_Earpiece|GetEarBox) :InVisibility "HitTestInvisible")
  (Utilities|Time|ClearTimerbyFunctionName :Object self :FunctionName "Step")
  (CallFunction|Step))
```

`Step()`: a 0.05 s timer, as `WBP_Stage.FadeBanner` does, so no UMG animation is needed.

```lisp
; T61: fades in over UITime "Panel", holds, fades out over the same time, then collapses.
(fn Step ()
  (bind _f (Class|UIStyle|UITime :Role "Panel"))
  (bind _d (/ 0.05 (Math|Float|Max(Float) _f 0.05)))
  (if (== (V Fading) 1)
    (set Alpha (Math|Float|Min(Float) (+ (V Alpha) _d) 1.0))
    (if (>= (V Alpha) 1.0)
      (set Fading 0)))
  (if (== (V Fading) 0)
    (set HoldLeft (- (V HoldLeft) 0.05))
    (if (<= (V HoldLeft) 0.0)
      (set Fading -1)))
  (if (== (V Fading) -1)
    (set Alpha (Math|Float|Max(Float) (- (V Alpha) _d) 0.0)))
  (Widget|SetRenderOpacity :self (Variables|WBP_Earpiece|GetEarBox) :InOpacity (V Alpha))
  (if (and (== (V Fading) -1) (<= (V Alpha) 0.0))
    (Widget|SetVisibility :self (Variables|WBP_Earpiece|GetEarBox) :InVisibility "Collapsed")
    (return))
  (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "Step" :Time 0.05 :bLooping false))
```

`Clear()`: stops the timer, sets the opacity to 0 and collapses `EarBox`.

`SetSpot(Spot)`:

```lisp
; T61: "stage" sits on the house floor, 24 from the bottom; "end" rises above the end screen's buttons.
(fn SetSpot (Spot)
  (bind _e (Class|UIStyle|UISize :Role "Edge"))
  (bind _b (Class|UIStyle|UISize :Role "ButtonHeight"))
  (bind _y (select (streq Spot "end") (- 0.0 (+ _b (* 2.0 _e))) (- 0.0 _e)))
  (Layout|CanvasPanelSlot|SetPosition :self (Widget|SlotAsCanvasSlot :Widget (Variables|WBP_Earpiece|GetEarBox)) :InPosition (Utilities|Struct|MakeVector2D 0.0 _y)))
```

`UISize "ButtonHeight"` (48) and `"Edge"` (24) are T32's roles, as `Graphs/UIStyle/UISize.txt` names them.

### 3c. Where it sits: re-check after T34

Today (T53-build part 2a, in 1920 × 1080 units): the chat column is bottom left (x 24 to 664), the bill bottom right (x 1676 to 1896), the card top right, the clapperboard top left under the header, the banner top (x 900 to 1460). A 720-wide panel centered at x 960 runs from 600 to 1320, so at its widest it overlaps the chat column's last 64 px. Lines up to about 12 words fit on one row and stay narrower than 600 px. **If the screenshots show it over the chat or the input row,** narrow `MaxDesiredWidth` to 560 (x 680 to 1240) and let the text wrap to two rows, or move the panel's center right to x 1000. Check the reactions too: the cut robot's last words play there.

## 4. The first-show flag: `Local/progress.json`

```json
{ "tips": false }
```

- A missing file, or a file without `tips`, means tips on (a first show). Only `BPC_Stagehand.SetTipsNext` writes it; `EndShow` writes `false`, the title's toggle writes what it shows.
- `Local/` is git-ignored, and a worktree has none, so this file never reaches the repo.
- **Packaged build:** the key screen writes `Local/llm_key.json` beside the game the same way (`SaveKeys`). **Check in T61 whether `Json|SaveJsontoFile` makes a missing `Local/` folder:** a packaged build that was never given keys has none. If it doesn't, the save fails (`ok=false` in the log), and every show teaches. The fix then is a `Local/.keep` staged with the build, or a folder make before the save (`Utilities|Paths|...` has no node for that; `BlueprintFileUtilsBPLibrary.MakeDirectory` is in the `BlueprintFileUtils` plugin, which is off).
- **Before you zip a build,** delete `Packaged/Windows/AIMegaJam2026/Local/progress.json` along with `llm_key.json`, so judges get a first show (decision 17).
- **To test a first show:** delete `Local/progress.json` in the repo folder.

## 5. The title: `WBP_Title`

T33's title is a paper playbill (`Bill`) with an ink panel beside it (`HowFrame`, holding `HowTitle` and `HowText`, the old rules). T61 keeps the playbill and refills `HowFrame` with "Tonight's show". Start from [`Graphs/WBP_Title/EventGraph.txt`](../../Graphs/WBP_Title/EventGraph.txt) and `ShowRing.txt`.

### 5a. Tree changes inside `HowFrame`

```
HowFrame        Border (StylePanel "Ink"), unchanged
└ HowBox        VerticalBox (T33's; keep its name if it has one)
  ├ HowTitle    TextBlock, CardTitle, Text: "Tonight's show"                 (T33's, new text)
  ├ HowText     TextBlock, Body, Text, top padding 12: the three opening lines (T33's, filled at Construct)
  ├ HelpRing    Border (ShowRing), top padding 24                            (new)
  │ └ HelpButton    Button, focusable                                         (new)
  │   └ HelpLabel   TextBlock "How to play"
  ├ TipsRing    Border (ShowRing), top padding 12                            (new)
  │ └ TipsButton    Button, focusable                                         (new)
  │   └ TipsLabel   TextBlock "Stagehand tips: on"
  └ TipsCap     TextBlock, Caption, Quiet, top padding 4: "A stagehand whispers tips during your first show."   (new)
```

- Both buttons `UIStyle.StyleButton(..., "Secondary")`, so Play via Relay stays the one primary button on the title.
- Tab order: Play via Relay, Test for Free, Use my own API keys, How to play, Stagehand tips. Play via Relay keeps first focus (T33).
- `HowText` gets the three lines from `stagehand.json`, so the title, the itch page and the file never disagree. If the read fails, it keeps its design-time text, the same three lines.
- **Row 18 of T32's audit** (a judge may read the burning bill as an error) asks T61 for one line about it on the title or in How to play. The caption under the tips button is the place that's free: "A stagehand whispers tips during your first show." covers the tips only. I recommend leaving row 18 to How to play's draft if my person wants it there; `how_to_play.md` doesn't have it yet, because the doc's six bullets are the rules only.

### 5b. Graph changes (in `EventGraph.txt`)

PreConstruct, after T33's `HowText` lines:

```lisp
  (Class|UIStyle|StyleButton :Button (Variables|WBP_Title|GetHelpButton) :Label (Variables|WBP_Title|GetHelpLabel) :Kind "Secondary")
  (Class|UIStyle|StyleButton :Button (Variables|WBP_Title|GetTipsButton) :Label (Variables|WBP_Title|GetTipsLabel) :Kind "Secondary")
  (Class|Text|SetFont :self (Variables|WBP_Title|GetTipsCap) :Font fCap)
  (Class|Text|SetColorandOpacity :self (Variables|WBP_Title|GetTipsCap) :ColorAndOpacity (Utilities|Struct|MakeSlateColor :SpecifiedColor (Class|UIStyle|UIColor :Role "Quiet")))
  (CallFunction|ShowRing :Ring (Variables|WBP_Title|GetHelpRing) :On false)
  (CallFunction|ShowRing :Ring (Variables|WBP_Title|GetTipsRing) :On false)
```

Construct, after the focus line:

```lisp
  (CallFunction|ShowOpening)
  (CallFunction|ShowTips)
```

Tick, with the other three rings:

```lisp
  (CallFunction|ShowRing :Ring (Variables|WBP_Title|GetHelpRing) :On (Widget|HasKeyboardFocus :self (Variables|WBP_Title|GetHelpButton)))
  (CallFunction|ShowRing :Ring (Variables|WBP_Title|GetTipsRing) :On (Widget|HasKeyboardFocus :self (Variables|WBP_Title|GetTipsButton)))
```

Two new events:

```lisp
(event OnClicked(HelpButton)
  (print "NHOS: TITLE click howtoplay")
  (bind _w (UserInterface|CreateWidget "/Game/NHOS/UI/WBP_HowToPlay.WBP_HowToPlay_C" (Game|GetPlayerController 0)))
  (UserInterface|Viewport|AddtoViewport :self _w :ZOrder 30))

(event OnClicked(TipsButton)
  (bind _show (Actor|GetActorOfClass "/Game/NHOS/Core/BP_Show.BP_Show_C"))
  (bind _sh (Class|BPShow|GetStagehand :self _show))
  (bind _on (Class|BPCStagehand|TipsNext :self _sh))
  (Class|BPCStagehand|SetTipsNext :self _sh :On (not _on))
  (print (cat "NHOS: TITLE click tips=" (select _on "off" "on")))
  (CallFunction|ShowTips))
```

New functions, each in its own file in `Graphs/WBP_Title/`:

```lisp
; WBP_Title.ShowOpening (T61): the three opening lines from stagehand.json, one per row.
(fn ShowOpening ()
  (bind (_o _ok) (Json|LoadJsonfromFile (Utilities|Struct|MakeFilePath (cat (Utilities|Paths|GetProjectContentDirectory) "NHOS/Data/stagehand.json"))))
  (if (not _ok)
    (return))
  (bind _l (Json|GetField _o "opening_lines"))
  (set OpenLines _l)
  (Widget|SetText(Text) :self (Variables|WBP_Title|GetHowText) :InText (Utilities|Text|ToText(String) (Utilities|String|JoinStringArray (V OpenLines) (V NL)))))

; WBP_Title.ShowTips (T61): the toggle's label says what the next show will do.
(fn ShowTips ()
  (bind _show (Actor|GetActorOfClass "/Game/NHOS/Core/BP_Show.BP_Show_C"))
  (bind _on (Class|BPCStagehand|TipsNext :self (Class|BPShow|GetStagehand :self _show)))
  (Widget|SetText(Text) :self (Variables|WBP_Title|GetTipsLabel) :InText (Utilities|Text|ToText(String) (select _on "Stagehand tips: on" "Stagehand tips: off"))))
```

- `OpenLines` is a new String array variable; `NL` a String variable holding one line break (`BP_Show` has `NL`; make the same on the title, or join with `" "` and let `HowText` wrap, if a line break won't go into a DSL string).
- `Class|BPShow|GetStagehand`: the component's getter from outside, as `Class|BPShow|GetLLMClient` (`WBP_Title` already uses it). The component variable must be public.
- The tips toggle and How to play don't change the mode note or start anything.

## 6. How to play: `WBP_HowToPlay`

`/Game/NHOS/UI/WBP_HowToPlay`, a new Widget Blueprint, built like T33's `WBP_Keys` frame (an ink panel over an ink scrim). Opened by the title's How to play button, at Z 30; nothing opens it on its own.

### 6a. Tree

```
Root            Overlay, full screen, Visible (blocks clicks to the title under it)
├ Scrim         Border, fill UIColor "Ink" (PreConstruct), slot Fill
└ Panel         SizeBox, MaxDesiredWidth 880, slot HAlign Center, VAlign Center
  └ Frame       Border (StylePanel "Ink"), padding 24
    └ Col       VerticalBox
      ├ Title       TextBlock "How to play", Header, Text
      ├ Bullets     VerticalBox, top padding 16
      │ └ Bullet0 … Bullet5   RichTextBlock or TextBlock each, Body, Text, AutoWrapText, top padding 12
      └ CloseRing   Border (ShowRing), top padding 24, slot HAlign Left
        └ CloseButton   Button, focusable
          └ CloseLabel  TextBlock "Close"
```

- **The bullets' text** is set at design time from [`T61-build/how_to_play.md`](T61-build/how_to_play.md) after my person's OK, one bullet per TextBlock, with the bold lead and a "•" mark: "• You're the human. Four AI actors and you, ...". A plain TextBlock can't bold only the lead; use the lead in `UIFont "Name"` (bold 20) as its own TextBlock in a HorizontalBox, or a RichTextBlock if T34 made a text style table for one. **If neither is quick, drop the bold** and keep the lead as the first words.
- 880 px holds the longest bullet (38 words) in three rows at 20 pt. At 1280 × 720 the panel is 704 px tall at most; six bullets of up to three rows plus the title and button fit in about 640. If not, wrap `Bullets` in a ScrollBox.
- Copy `ShowRing` from `WBP_Title` (`Graphs/WBP_Title/ShowRing.txt`), as T33 did on each screen.

### 6b. Graphs

```lisp
; WBP_HowToPlay.EventGraph (T61). The full rules in six bullets, never forced. Close or Escape returns to the title.
(event UserInterface|EventPreConstruct (IsDesignTime)
  (bind fBody (Class|UIStyle|UIFont :Role "Body"))
  (bind cText (Utilities|Struct|MakeSlateColor :SpecifiedColor (Class|UIStyle|UIColor :Role "Text")))
  (Class|Border|SetBrushColor :self (Variables|WBP_HowToPlay|GetScrim) :BrushColor (Class|UIStyle|UIColor :Role "Ink"))
  (Class|UIStyle|StylePanel :Panel (Variables|WBP_HowToPlay|GetFrame) :Look "Ink")
  (Class|Text|SetFont :self (Variables|WBP_HowToPlay|GetTitle) :Font (Class|UIStyle|UIFont :Role "Header"))
  (Class|Text|SetColorandOpacity :self (Variables|WBP_HowToPlay|GetTitle) :ColorAndOpacity cText)
  ; one SetFont and SetColorandOpacity pair per bullet, Bullet0 to Bullet5, with fBody and cText
  (Class|UIStyle|StyleButton :Button (Variables|WBP_HowToPlay|GetCloseButton) :Label (Variables|WBP_HowToPlay|GetCloseLabel) :Kind "Primary")
  (CallFunction|ShowRing :Ring (Variables|WBP_HowToPlay|GetCloseRing) :On false))

(event UserInterface|EventConstruct
  (print "NHOS: HOWTOPLAY open")
  (Widget|SetKeyboardFocus :self (Variables|WBP_HowToPlay|GetCloseButton)))

(event UserInterface|EventTick (MyGeometry InDeltaTime)
  (CallFunction|ShowRing :Ring (Variables|WBP_HowToPlay|GetCloseRing) :On (Widget|HasKeyboardFocus :self (Variables|WBP_HowToPlay|GetCloseButton))))

(event OnClicked(CloseButton)
  (CallFunction|CloseHelp))
```

`CloseHelp()`:

```lisp
(fn CloseHelp ()
  (print "NHOS: HOWTOPLAY close")
  (bind _show (Actor|GetActorOfClass "/Game/NHOS/Core/BP_Show.BP_Show_C"))
  (bind _t (Class|BPShow|GetTitleScreen :self _show))
  (Widget|RemovefromParent :self self)
  (Widget|SetKeyboardFocus :self _t))
```

- `TitleScreen` is `BP_Show`'s variable (`ShowTitle` sets it). Giving the title focus back lets Tab reach its buttons again (T33 found the same after Back on the key screen). Focusing the How to play button itself would be better; `WBP_Title` can expose it with a one-line function if T61 wants that.
- **Escape:** override `OnKeyDown` (`UserInterface|OnKeyDown`, returns an `EventReply`): if the key is Escape, `CloseHelp` and return Handled; else Unhandled. The focus is on the Close button, inside the widget, so the widget sees the key. If the override is hard to make through MCP, leave Escape out (Close and Enter already work) and say so in Findings.

## 7. `BP_Show`: the component and one call per moment

### 7a. The places, as the pushed sources stand at `42b1189`

| Moment (key) | Graph | Place | Call | Re-check |
|---|---|---|---|---|
| — (a new show) | `DrawCast` ([file](../../Graphs/BP_Show/DrawCast.txt)) | After the `NHOS: DRAW` print and the `< 3` check, just before the last `(return true)` | `(Class|BPCStagehand|BeginShow :self (V Stagehand))` | **re-check**: any chain task that moves the draw. It runs at every show's start, restarts included. |
| `before_show`, `scene_prep` | `OpenPrep` ([file](../../Graphs/BP_Show/OpenPrep.txt)) | After the `NHOS: PREP shown` print, before `LoadSwitches` | `(Class|BPCStagehand|Say :self (V Stagehand) :Key "before_show")` then the same with `"scene_prep"` | **re-check**: T34 may restyle Scene Prep; `OpenPrep` runs at the "prep" cue, so it is already at screen time. |
| `scene_turn_<n>` | `StartTurn` (no file) | Right after its `CueHeader` node (T30 swapped the header in) | `(CallFunction|CueTip :Key (cat "scene_turn_" (str (V TurnNum))))` | **re-check**: T38 and T34 may touch it. `StartTurn` adds 1 to `TurnNum` first (T06), so turn 1 is 1. |
| `free_talk_<r>` | `StartTalkRound` (no file) | Right after its `CueHeader` node | `(CallFunction|CueTip :Key (cat "free_talk_" (str (V TalkRound))))` | **re-check**: T57 and T58 change Free Talk; `StartTalkRound` adds 1 to `TalkRound` first (T08). |
| `the_cut` | `RunCue` ([file](../../Graphs/BP_Show/RunCue.txt)) | The `votes` branch, after `(CallFunction|ShowVotePick)`, before its `(return)` | `(Class|BPCStagehand|Say :self (V Stagehand) :Key "the_cut")` | **re-check**: T34 rebuilds the ballot (T32 row 3). |
| `win`, `lose` | `RunCue` | The `end` branch, after `(CallFunction|ShowEndScreen)`, before its `(return)` | `(Class|BPCStagehand|EndShow :self (V Stagehand) :Win (V ShowWin) :Reason <T60's top-reason line, or "">)` | **re-check**: T60 changes `ShowEndScreen`; part 0 step 4. |
| — (the tip cue) | `RunCue` | A new branch, with the others | `(if (streq Kind "tip") (Class|BPCStagehand|Say :self (V Stagehand) :Key Text) (return))` | — |
| — (restart) | `RestartShow` (no file) | Nothing needed | `BeginShow` (through `DrawCast`) hushes the earpiece | **re-check**: that `RestartShow` reaches `DrawCast`. If it doesn't, add a `BeginShow` there. |

New function, `Graphs/BP_Show/CueTip.txt`:

```lisp
; T61: a stagehand tip that shows when the line queue reaches it, like the header and the banner.
; pacing.json has no cue_hold for "tip", so the queue doesn't wait for it; the earpiece keeps its own queue.
(fn CueTip (Key)
  (Class|BPCLinePlayer|Cue :self (Variables|Default|GetLinePlayer) :Kind "tip" :Text Key :Num 0))
```

- **Why the cue:** since T30 the show's logic runs ahead of the screen (`LinePrompt`), so `StartTurn` for turn 2 can run while turn 1's lines still play. Through the queue, the turn 2 tip shows when my input opens for turn 2, not under turn 1's lines. `OpenPrep` and `RunCue`'s branches already run at the queue's turn, so they call `Say` directly.
- Each `CueTip` also prints `NHOS: CUE tip <key>` (`BPC_LinePlayer.Pump`), in every show; only a teaching show prints `NHOS: TIP`.
- **The component:** add `BPC_Stagehand` to `BP_Show`'s components as `Stagehand`, the way T20 added `BPC_ShowAudio` as `Audio`.
- **Update `RunCue.txt`, `OpenPrep.txt` and `DrawCast.txt`** in `Graphs/BP_Show/` with the new nodes, and write `CueTip.txt`. `StartTurn` and `StartTalkRound` have no files: write each node edit under "Findings" in `T61.md`.

## 8. `UIStyle`: the `Earpiece` color

One branch in `UIStyle.UIColor`, in `Graphs/UIStyle/UIColor.txt` after `Raised`:

```lisp
  ; Earpiece: #FF9EC4, the stagehand's tips (T61, proposed)
  (if (Utilities|String|EqualExactly(String) Role "Earpiece")
    (return (Utilities|Struct|MakeLinearColor 1.0000 0.3419 0.5520 1.00)))
```

- Linear values from `#FF9EC4` (the 0x9E channel is 0.3419, as in `Amber`'s green).
- Contrast: luminance 0.497 against the ink panel's ~0.007, about 9.6:1. Measure it from a screenshot, as T33 did.
- `UIStyle.uasset` is outside T61's Touches: lock it, and name it in the commit message.
- **The doc:** the Art Inspiration tab's palette table has no row for it. Per the build note "The design doc follows the game", show my person the row "Earpiece | #FF9EC4 | The stagehand's tips, only on your screen" and add it after their OK.

## 9. `Tools/check_prompts.py`

Add to the docstring, after "Scene clock (T53)":

```
Stagehand (T61): stagehand.json has a line for every moment in STAGEHAND_MOMENTS
and the three opening lines, every line is MAX_TIP_WORDS (25) words or fewer and a
style tip MAX_WORDS (15), no line holds a banned name, and Docs/ItchPage.md carries
the opening lines word for word. --log fails a show whose NHOS: LOG, STATE or
CLOSING lines hold a stagehand line: the tips never reach an AI.
```

Constants, after `MAX_WORDS`:

```python
STAGEHAND_MOMENTS = ["before_show", "scene_prep", "scene_turn_1", "free_talk_1", "the_cut", "lose", "win"]
MAX_TIP_WORDS = 25
ITCH_PAGE = ROOT / "Docs" / "ItchPage.md"
```

A new function, called from `check_files` after `prewritten_problems`, with `stagehand = load_json("stagehand.json", errors)` added to the loads at the top:

```python
def stagehand_problems(data) -> list[str]:
    """T61: the earpiece tips. Every moment has a line, no line runs long, no banned name."""
    out = []
    moments = data.get("moments", {})
    for key in STAGEHAND_MOMENTS:
        line = moments.get(key, {}).get("line")
        if not isinstance(line, str) or not line.strip():
            out.append(f"stagehand.json: moment {key} needs a line")
    for key in moments:
        if key not in STAGEHAND_MOMENTS:
            out.append(f"stagehand.json: unknown moment {key!r}")
        if moments[key].get("spot") not in ("stage", "end"):
            out.append(f"stagehand.json: moment {key} needs a spot, stage or end")
    tips = [(f"moment {k}", v.get("line", "")) for k, v in moments.items()]
    style = data.get("style", {})
    for k, v in style.items():
        if not isinstance(v, str) or not v.strip():
            out.append(f"stagehand.json: style.{k} needs a line")
        elif words(v) > MAX_WORDS:
            out.append(f"stagehand.json: style.{k} is {words(v)} words (most {MAX_WORDS})")
        tips.append((f"style {k}", v if isinstance(v, str) else ""))
    opening = data.get("opening_lines")
    if not is_lines(opening) or len(opening) != 3:
        out.append("stagehand.json: opening_lines needs the three lines shown before the show")
        opening = []
    tips += [("opening line", s) for s in opening]
    for where, line in tips:
        if words(line) > MAX_TIP_WORDS:
            out.append(f"stagehand.json: {where} is {words(line)} words (most {MAX_TIP_WORDS})")
        for w in BANNED + PUN_NAMES:
            if re.search(r"(?i)\b" + re.escape(w) + r"\b", line):
                out.append(f"stagehand.json: {where} holds a banned name: {w!r}")
    hold = data.get("hold", {})
    if not all(isinstance(hold.get(k), (int, float)) for k in ["base", "per_word", "min", "max", "gap"]):
        out.append("stagehand.json: hold needs base, per_word, min, max and gap (seconds)")
    page = ITCH_PAGE.read_text(encoding="utf-8") if ITCH_PAGE.exists() else ""
    for s in opening:
        if s not in page:
            out.append(f"Docs/ItchPage.md: missing the opening line {s!r}")
    return out
```

- `words()` is the checker's own word count (line 998, a Player name counts as one word, as the game's cut counts it), defined below `check_files`; Python finds it at call time, so the order doesn't matter.
- `--log`: in `check_log`, collect the stagehand lines once (moments, style) and fail any `NHOS: LOG`, `STATE` or `CLOSING` line that contains one. `LOG_RE` (line 1101) doesn't match `STATE` today; add it to the group if T53 didn't.
- The lines are static text for my screen, so the legibility and story checks for AI lines don't apply. The banned-name check does.

Check it: `python Tools/check_prompts.py --offline` passes; then, on a scratch copy, a moment with 26 words and a missing `win` each fail with their message. **Tried in prep** (the function run on its own against the draft, at `42b1189`): the draft gives only the three "missing the opening line" errors for `Docs/ItchPage.md`, which part 10 fixes; a 26-word `the_cut` and an empty `win` each fail with their message.

## 10. `Docs/ItchPage.md`: the three opening lines

At the top of "Page text", between the `---` rule and "### Tonight: the world's first all-AI improv show":

```markdown
**You're the only human.**
**Each scene, the cast cuts whoever seems human.**
**Survive to the final two or the last scene.**
```

Each line ends with two spaces (a Markdown line break) or sits in its own paragraph, whichever renders as three lines on itch.io. The check in part 9 looks for each line's words, so the bold marks don't matter. T54 and T55 rewrite this page before T61; if they left a line that contradicts these three (a win only at the final two, the Director), tell my person.

## 11. `Docs/switches.example.json`: `stagehand_tips`

Add `"stagehand_tips": false` and, to `_readme`: "stagehand_tips: with autoplay on, the stagehand's earpiece tips show anyway, as on a first show, for checking them; autoplay never saves Local/progress.json. With autoplay off it does nothing: the first show (no Local/progress.json) and the title's Stagehand tips toggle decide. It is read at each show's draw. Set it back to false before a person plays." T55 rewrites the `force_tie` text first; start from its version.

## 12. The check (T61 step 8)

Log lines to look for:

| Line | When |
|---|---|
| `NHOS: STAGEHAND loaded` | The first show of a run |
| `NHOS: STAGEHAND tips=on why=progress` / `tips=off why=progress` / `why=autoplay` | Each show's draw |
| `NHOS: TIP <key> words=<n> hold=<s>` | Each line on screen; `<key> style` for a style tip |
| `NHOS: CUE tip <key>` | Every show, from the queue, tips on or off |
| `NHOS: STAGEHAND saved tips=false ok=true` | The end screen of a teaching show |
| `NHOS: TITLE click tips=on` / `tips=off`, `NHOS: TITLE click howtoplay`, `NHOS: HOWTOPLAY open` / `close` | The title |

**Run A: a first free show in PIE, by hand.** Delete `Local/progress.json`. `autoplay` false, Test for Free, a 1600 × 900 window.

- The title shows "Tonight's show" with the three lines and "Stagehand tips: on". Screenshot.
- Play to the end. Expected `NHOS: TIP` keys, in this order: `before_show`, `scene_prep`, `scene_prep style`, `scene_turn_1`, `scene_turn_1 style`, `scene_turn_2 style`, `scene_turn_3 style`, `free_talk_1`, `free_talk_2 style`, `the_cut`, then `win` or `lose`. Each key once. Scene 2 and later print none.
- Screenshots of the earpiece at Scene Prep, turn 1, Free Talk and The Cut, and on the end screen. In each, it covers no card, clapperboard, input row, ballot, chat line or button, and it reads as neither chat nor the banner.
- Then `Local/progress.json` holds `{"tips": false}`.
- **No tip in any AI state:** `python Tools/check_prompts.py --log` passes (part 9's stagehand check). `grep -F` for each stagehand line's text in the log finds nothing at all, since `NHOS: TIP` prints the key, not the text, so any hit is a leak. Part 2c's `find_nodes` searches find nothing.

**Run B: a second show.** Play Again from the end screen (no title): `tips=off why=progress` and no `NHOS: TIP`. Then quit, start PIE again: the title says "Stagehand tips: off".

**Run C: the toggle.** On the title, Tab to Stagehand tips, Enter: "Stagehand tips: on", `NHOS: TITLE click tips=on`, `progress.json` says `true`. Start a show: `tips=on why=progress` and the tips again.

**Run D: How to play.** On the title, Tab to How to play, Enter: the six bullets, Close focused. Screenshot at 1600 × 900 and 1280 × 720. Enter closes it, and Escape does too if built. Tab reaches the title's buttons again.

**Run E: autoplay.** A free autoplay show in a game window on the saved assets, `stagehand_tips` false: `tips=off why=autoplay`, no `NHOS: TIP`, `progress.json` unchanged, `NHOS: SHOW END`. Then with `stagehand_tips` true and `fast_lines` false: the tips play, in Run A's order, and `progress.json` is still unchanged. Set both back.

**By hand, as a first-time player** (the task's Done when): a first show and then a second one, judged from the screenshots: do the tips teach the rules at the moment they matter, are they readable before they fade, and do they ever hide something I need?

## 13. Coverage of T61's steps

| T61 step | Where |
|---|---|
| 1. `stagehand.json`: each moment's line word for word, the style tips, the three opening lines | Part 1, [`T61-build/stagehand.json`](T61-build/stagehand.json); decisions 1, 4, 5 |
| 2. `BPC_Stagehand`, one call per moment, never to an LLM or the log | Parts 2 and 7; 2c |
| 3. `WBP_Earpiece`: own color, own channel, holds then fades, T32's style, clear of the card, clapperboard and input | Parts 3 and 8; decisions 9 to 12 |
| 4. First show only, `Local/progress.json`, autoplay off unless a switch | Parts 2 (`BeginShow`, `EndShow`), 4 and 11; decisions 6 to 8 |
| 5. The tips toggle on `WBP_Title` | Part 5; decisions 6, 13 |
| 6. How to play: `WBP_HowToPlay`, six bullets, Close, shown to my person first | Part 6, [`T61-build/how_to_play.md`](T61-build/how_to_play.md); decision 14 |
| 7. `check_prompts.py --offline`, the itch page's three lines | Parts 9 and 10 |
| 8. The check: screenshots, `NHOS: TIP`, no tip in an AI state, a second show, the toggle, How to play | Part 12; decision 16 |

If T61 runs long, the task says to push steps 1 to 4 and split 5 and 6 off. In this sheet that is parts 1 to 4, 7, 8 and 11, with part 9's check and part 12's Runs A, B and E; parts 5, 6 and 10 and Runs C and D go with the split.

## 14. Knock-on: tell, don't change

- **`CLAUDE.md` and `README.md`:** the `Local/` row names `llm_key.json` and `switches.json`; add `progress.json` ("the stagehand's first-show flag; delete it to see the tips again"). The packaging notes say to delete `llm_key.json` before zipping; add `progress.json` (decision 17).
- **`Docs/Submission.md`** may list the title screen's screenshot ("the title screen with the three ways to play"): the title now has "Tonight's show" beside it. Nothing to change unless the shot list says otherwise.
- **T32's audit, row 8:** T33 left How to play "in an ink panel beside it until T61". Mark T61's part fixed in `T32.md`, as T33 did for its rows, with the before and after screenshot names.
- **T32's audit, row 18** (the burning bill's label) names T61. Decision: it isn't in the doc's six bullets. Tell my person, and mark it open or move it to T34.
- **The design doc:** the palette row (part 8). The Onboarding section needs no edit, unless my person changes a decision above that the doc states (the opening lines' wording, decision 1).
