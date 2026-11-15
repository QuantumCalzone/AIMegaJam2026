# T73 build sheet: the lines type out, one voice sound per syllable

Back to [T73](T73.md). A Mac prep session wrote this on 2026-11-15, without the editor. It is a plan, not a record: nothing here was written to the editor. When T73 writes a graph, its source goes to `Graphs/` as usual.

- **Written against `noHumansOnSet` at `9fa160a`** (T72 `055eeac` and T67 `c0ae863` in; the T75 and T68 prep on top). Every graph below starts from its pushed source at that commit: `Graphs/BPC_LinePlayer/*` (T30, plus T20's blip line in `PlayCur`), `Graphs/WBP_ChatLine/SetActor.txt` (T32), `Graphs/BPC_ShowAudio/Syllable.txt`, `StopVoice.txt`, `Blip.txt`, `Sfx.txt` (T20, T72), `Graphs/BP_Show/LineBlip.txt`, `LineInfo.txt` (T20, T30), `Graphs/WBP_Stage/SetTyping.txt` (T30), and `Content/NHOS/Data/pacing.json` (T30).
- **Written for the game as the PC's chain leaves it** (T57, T58, T62 to T66, which run before T73). The sheets taken into account: [T57-build.md](T57-build.md), [T58-build.md](T58-build.md), [T62-build.md](T62-build.md), [T63-build.md](T63-build.md), [T64-build.md](T64-build.md), [T65-build.md](T65-build.md), [T66-build.md](T66-build.md). **None of them changes a graph this sheet changes.** What they touch near it:
  - T57 and T58 add two cue kinds (`passed`, `unpass`) that go through `BPC_LinePlayer.Cue` and `BP_Show.RunCue`, with no `cue_hold` entry, and insert `PassCue` into `BP_Show.ShowLine` before `Push`. `Push`, `Pump` and `PlayCur` don't change. T58's last words are ordinary Free Talk lines in the queue (`LineInfo` gives them the typing line).
  - T62 to T66 change the input row, my send and the turn timer. T66's timer starts when my input opens on screen, which `LinePrompt` holds closed while `LinePlayer.IsBusy()` is true (T30). The typing keeps `Busy` true (part 3), so the timer still starts after the last line, typing and hold included.
  - **T57 has landed** (`069d4f6`, merged in `ae8410d`) while this sheet was written, and was checked against it: it wrote `RunCue`, `ShowLine`, `PassCue`, `PassClear`, `MarkPass` and `BP_Robot.SetPassed`, and none of the files this sheet changes. A pass is still a line in the queue with an empty speech, so it doesn't type (decision 2).
  - **The order doesn't matter to this sheet.** The plan lists T73 above T58 and T62 to T66; the dispatcher runs it after them. Nothing below depends on those five tasks, so the sheet holds either way.
  - Also read: [T38-build.md](T38-build.md) (written before today's rule changes; its bubble call goes right after `AddChatLine` in `PlayCur`, and its "typing bubble" builds on this sheet), [T75-build.md](T75-build.md) (T77 later calls `BP_Robot.Emote` from `PlayCur`), [T71-build.md](T71-build.md) (it changes other `BPC_ShowAudio` functions, not `Syllable`, `Blip` or `Sfx`'s `blip` branch).
- **T73 re-checks against the `Graphs/` sources of its day** (part 0): anything marked **RE-CHECK** below.
- **The design doc was read, not changed:** Rules tab rev 45, Tech & Build rev 28, Art Inspiration (its Components table). One edit is proposed in part 7. It **waits for my person's OK in T73**.

## In short

- **The line queue owns a typing timer** (part 3). `PlayCur` plans the line first (`PlanType`: when each letter appears and which letters start a syllable), prints `NHOS: LINE <id> hold=<s> syl=<n> type=<s>`, adds the chat line, then starts the typing (`StartType`). A looping 1/60 s timer (`TypeTick`) shows every letter whose time has come, from the real time since the line started, so the frame rate and `fast_lines` can't stretch it. When the typing ends (`EndType`), the hold starts, then `Pump` plays the next item. `Busy` stays true the whole time, so nothing downstream changes.
- **The chat line types without growing** (part 2). In `WBP_ChatLine`, `SpeechText` goes into a new Overlay with a new TextBlock, `SpeechShown`, on top of it. While a line types, `SpeechText` holds the whole speech at opacity 0, so the line has its final size from the first letter, and `SpeechShown` shows the typed part in the same font. Three small new functions: `TypeBegin(Speech)`, `TypeTo(N)`, `TypeEnd()`. `SetActor` doesn't change, so the cast rows that reuse `WBP_ChatLine` don't either.
- **The queue finds the new line** through a new pure-read function in `WBP_Stage`, `LastChatLine()`: the last child of `LogScroll`, cast to `WBP_ChatLine` (part 4). `AddChatLine` stays as it is.
- **Syllables** (part 3c): each run of vowels (a, e, i, o, u, y) inside a word starts one syllable; a single final "e" after a consonant doesn't count when the word has another syllable; every word gets at least one. When a letter that starts a syllable appears, the queue calls `BPC_ShowAudio.Syllable(Name, IsMe)`, at most 12 a second. Punctuation adds 0.15 s (`,` `;` `:`) or 0.3 s (`.` `?` `!`) before the next letter, and no sound.
- **The blip goes** (part 5): `PlayCur` stops calling `BP_Show.LineBlip`, and T73 deletes `BP_Show.LineBlip` and `BPC_ShowAudio.Blip` (`remove_function_graph`), as it holds both locks in the chain. `Sfx`'s `blip` branch and `S_TalkBlip` stay, unused.
- **`pacing.json`** (part 6): four new values (`type_cps` 30, `type_pause_comma` 0.15, `type_pause_stop` 0.3, `syl_max_rate` 12) and the hold retuned to `line_base` 0.6, `line_per_word` 0.12, `line_min` 1.5, `line_max` 2.5. On the free-mode lines, a scene's lines take 150.2 s after against 150.5 s before (the arithmetic is in part 6).
- **The check** (part 8): time scene 1 of a slow free autoplay show before touching anything, build, time it again, run a fast free autoplay show for the log fields, then play one PIE show by hand with `type_cps` 5 for the half-typed screenshots.

## Decisions made for my person

I took my own recommendation on each, since none changes what gets built in a big way. Each is open to change; the T73 session should show this list to my person when it closes the task.

1. **How the chat line types without jumping: a hidden full copy under the typed part** (the task's own example). `SpeechText` keeps the whole speech at render opacity 0 and sets the line's size; a second TextBlock on top shows the typed part. No new asset. **One known flaw:** a word that is only partly typed at the end of a wrapped row can sit on the first row until it no longer fits, then hop to the next row (the full copy wraps it at once). The box itself never moves. If the screenshots show the hop often, the fallback is a `RichTextBlock` for the typed part with a transparent text style for the untyped rest, which needs a text-style `DataTable` asset and is not built here.
2. **Only the speech types.** The name and the action show at once, as the task says. An action-only line (and a pass) has no typing and no sound.
3. **The queue finds the new chat line with a new `WBP_Stage.LastChatLine()`,** not by changing `AddChatLine` to return it. `AddChatLine` has no `Graphs/` source, so a rewrite would mean reading and checking it whole; one new function is smaller.
4. **The typing follows the real clock** (`GetRealTimeSeconds`), sampled every 1/60 s. A tick that finds several letters due shows all of them and plays at most one sound. So a 30 fps frame rate or `fast_lines` (300 letters a second) never makes the typing longer than its plan.
5. **The sound cap is 12 a second of real time,** not scaled by `fast_scale`. A syllable that comes less than 1/12 s after the last sound is dropped, not delayed, so the babble never lags behind the text. With `fast_lines` most sounds drop, which is fine for an autoplay check.
6. **The pauses and the cap are values in `pacing.json`** (`type_pause_comma`, `type_pause_stop`, `syl_max_rate`), beside `type_cps`, so they can be tuned without a rebuild. A run of punctuation ("?!", "...") pauses once, after its last mark, and there is no pause after a line's last letter.
7. **The syllable rule in detail:** a word is a run of letters, digits and apostrophes (so "don't" is one word and "15" is one word with one syllable). "y" is a vowel everywhere, as the task says ("yes" is one run, "ye"). Letters outside a–z (é, ü) count as breaks between words. A speech with no word at all ("...") still gets one syllable, on its first letter, so `syl` is above 0 on every line with speech.
8. **`syl=` is the line's syllable count from its text, not the number of sounds played,** and `type=` is the typing time after `fast_scale` (the moment the last letter has had its 1/30 s). So `syl=0` exactly when `type=0`, and the check can test that from the log alone (part 8).
9. **The hold keeps T30's formula,** `clamp(line_base + line_per_word × words, line_min, line_max)` over the action's and the speech's words, with new numbers (part 6). It starts when the typing ends. The reader reads while the line types, so the hold only needs to cover the rest.
10. **The new numbers are 0.6, 0.12, 1.5 and 2.5.** `line_min` 1.5 (not the 1.2 the fit allowed) gives an action-only line or a pass enough time to be seen; it changes nothing else in the fit.
11. **`BP_Show` gets no new function.** The queue finds `BPC_ShowAudio` with `GetComponentbyClass` on its owner, as `BPC_LLMClient.BackstageNote` finds the queue. So `BP_Show`'s only change is deleting `LineBlip`.
12. **`Sfx`'s `blip` branch and the `S_TalkBlip` asset stay,** unused. Deleting the asset would also mean its row in `Docs/Assets.md`; T73's Touches don't name either. Say so under "## Findings".
13. **`Clear()` stops the typing and shows the whole line,** so a restart never leaves a half-typed line behind.
14. **The checker doesn't change.** `Tools/check_prompts.py` doesn't read `pacing.json` (T30) and isn't in T73's Touches. Part 8 checks the file with one line of Python instead.

## 0. Before you start

1. `git log --oneline -8` shows T66 (or whichever chain task came last), `Docs/claims/` holds no claim on T73's assets, and `git lfs locks` shows no lock on `BPC_LinePlayer.uasset`, `WBP_ChatLine.uasset`, `WBP_Stage.uasset`, `BPC_ShowAudio.uasset` or `BP_Show.uasset`. Lock all five (`git lfs lock <path>`).
2. **RE-CHECK the sources.** `git log --oneline 9fa160a.. -- Graphs/BPC_LinePlayer Graphs/WBP_ChatLine Graphs/BPC_ShowAudio Graphs/BP_Show/LineBlip.txt Graphs/WBP_Stage Content/NHOS/Data/pacing.json`. For each file a later commit changed, put this sheet's lines into the pushed version instead of using the copies below:
   - `BPC_LinePlayer`: `PlayCur.txt`, `Clear.txt`, `LoadPacing.txt`. No chain sheet changes them. T38 and T77 come after T73.
   - `WBP_ChatLine/SetActor.txt`: T73 doesn't change it, but `TypeBegin` must use the same font and color roles for the speech (`UIFont "Speech"`, `UIColor "Text"`). If T34 or anyone changed them, follow.
   - `BPC_ShowAudio/Syllable.txt`: the signature must still be `Syllable(Name, IsMe)`.
   - `pacing.json`: if someone retuned `line_*` after a relay show (T30's "For later"), rerun the arithmetic in part 6 from their numbers, keeping the scene's total.
3. **Read in the editor (one script, read only):**
   1. `WBP_Stage.AddChatLine`'s graph (`read_graph_dsl`; never write it back). Confirm it creates a `WBP_ChatLine`, calls `SetActor`, adds it to **`LogScroll`** as the last child and scrolls to the end. **RE-CHECK:** if it adds anything else to `LogScroll` after the line (a spacer), or inserts at index 0, change `LastChatLine` (part 4) to find the line it just added.
   2. `WBP_ChatLine`'s tree (`UMGToolSet`): where `SpeechText` sits (its parent and slot), and its text settings: `AutoWrapText`, `WrapTextAt`, `Justification`, `Margin`, `LineHeightPercentage`, `ApplyLineHeightToBottomLine`, `ShadowOffset`, `ShadowColorAndOpacity`, `Clipping`, `bSimpleTextMode`. `SpeechShown` copies every one (part 2a).
   3. `find_nodes` for `LineBlip` in `BP_Show` and for `Blip` in `BPC_ShowAudio` and `BP_Show`: expected only `PlayCur`'s call (in `BPC_LinePlayer`) and `LineBlip`'s own call to `Blip`. Another caller: tell my person before deleting.
4. **Node names the pushed sources haven't used yet** (one script, `find_node_types` with `context_pins: []`, then `get_node_type_pins` on a graph you rewrite anyway, T30): `Class|PanelWidget|GetChildrenCount`, `Class|PanelWidget|GetChildAt`, `Utilities|Casting|CastToWBP_ChatLine` (the form of `CastToStaticMesh` in `BP_Prop/SetProp.txt`, an exec cast with `:then` and `:CastFailed`). Already in pushed sources: `Utilities|Time|GetRealTimeSeconds` (`WBP_MoneyBurn/Burn.txt`), `Utilities|String|GetSubstring :SourceString :StartIndex :Length` and `Utilities|String|Len` (`BPC_LLMClient`), `Utilities|String|Contains :SearchIn :Substring` (case-insensitive by default), `Utilities|String|Equal,CaseInsensitive(String) :A :B`, `Widget|SetRenderOpacity :self :InOpacity` (`WBP_Stage/FadeBanner.txt`), `Math|Float|Max(Float)`, `Actor|GetComponentbyClass :self (Components|GetOwner) :ComponentClass` (`BPC_LLMClient/BackstageNote.txt`), `Utilities|Array|SetArrayElem` (positional, `Syllable.txt`).
5. **Time scene 1 before you change anything** (part 8, run A). It needs the game as it is, so do it first.

**A DSL rule this sheet follows** (T30's findings): after an `(if ... (return))`, an `if` without its own `return` doesn't join the code after it. So every function below either has only returning `if`s after its first early return, or has no early return at all; the per-letter logic is split into small functions for that reason.

## 1. Which graphs change

| Blueprint | Graph | File | Change |
|---|---|---|---|
| `BPC_LinePlayer` | `PlayCur` | yes | Plan, print the new fields, start the typing; the blip call goes; the `Pump` timer only when nothing types (3a) |
| | `Clear` | yes | Stops the typing (3g) |
| | `LoadPacing` | yes | Four new values with defaults, retuned defaults, `type_cps` on the `PACING` line (3h) |
| | `PaceF` | new | A pacing value or its default (3h) |
| | `PlanType`, `PlanChar`, `WordStart`, `SylAt`, `EndWord`, `PauseAt` | new | The plan of a line (3c) |
| | `StartType`, `TypeTick`, `TypeStep`, `TickChar`, `TickHit`, `EndType`, `StopType` | new | The typing timer (3d to 3g) |
| | `SayVoice`, `FindAudio` | new | The syllable sound (3e) |
| `WBP_ChatLine` | tree | – | `SpeechStack` (Overlay) around `SpeechText`, new `SpeechShown` (2a) |
| | `TypeBegin`, `TypeTo`, `TypeEnd` | new | The typed part (2b) |
| `WBP_Stage` | `LastChatLine` | new | The newest chat line (4) |
| `BPC_ShowAudio` | `Blip` | yes | Deleted (5) |
| `BP_Show` | `LineBlip` | yes | Deleted (5) |

`Pump`, `Push`, `Cue`, `IsBusy`, `Scaled`, `ClearTyping`, `CueHoldFor`, `FindShow`, `SetActor`, `AddChatLine`, `SetTyping` and `Syllable` don't change. "<name> is typing..." stays exactly as T30 made it (task step 5): `Pump` shows it before an AI line in Free Talk and the reactions, and `PlayCur` clears it.

## 2. `WBP_ChatLine`: the speech as it types

### 2a. The tree

1. Wrap `SpeechText` in a new Overlay, **`SpeechStack`** (`UMGToolSet.WrapWidgets`, as T14 and T53 did). It takes `SpeechText`'s place and slot in its parent. `SpeechText`'s overlay slot: HAlign Fill, VAlign Top, padding 0.
2. Add a TextBlock, **`SpeechShown`**, as `SpeechStack`'s second child (drawn on top), marked as a variable. Overlay slot: HAlign Fill, VAlign Top, padding 0. Copy every text setting from part 0, step 3.2, so it wraps at the same width as `SpeechText`. Text empty, Visibility **Collapsed**.
3. `SpeechStack` is `SelfHitTestInvisible`, like the rest of the line.
4. **RE-CHECK:** if `SpeechText`'s old slot had a size rule (Fill in a HorizontalBox, a WrapBox fill), `SpeechStack` must have it now; `WrapWidgets` should carry it over. A screenshot of a cast row in Scene Prep (part 8, run D) shows that the cast rows look as before.

Why both blocks fit exactly: they have the same font, the same width and the same wrap settings, so the typed part sits exactly over the hidden full text. At the end, `TypeEnd` brings `SpeechText` back and hides `SpeechShown`: the same pixels, no flicker.

### 2b. Three functions

New variable: `FullSpeech` (String).

```lisp
; T73: a line starts to type. SpeechText keeps the whole speech, invisible, so the line has its final size
; from the first letter (the chat doesn't jump); SpeechShown shows the typed part in the same font on top.
(fn TypeBegin (Speech)
  (set FullSpeech Speech)
  (Class|Text|SetFont :self (Variables|WBP_ChatLine|GetSpeechShown) :Font (Class|UIStyle|UIFont :Role "Speech"))
  (Class|Text|SetColorandOpacity :self (Variables|WBP_ChatLine|GetSpeechShown) :ColorAndOpacity (Utilities|Struct|MakeSlateColor :SpecifiedColor (Class|UIStyle|UIColor :Role "Text")))
  (Class|Text|SetText :self (Variables|WBP_ChatLine|GetSpeechShown) :Text (Utilities|Text|ToText(String) ""))
  (Widget|SetVisibility :self (Variables|WBP_ChatLine|GetSpeechShown) :InVisibility "HitTestInvisible")
  (Widget|SetRenderOpacity :self (Variables|WBP_ChatLine|GetSpeechText) :InOpacity 0.0))
```

```lisp
; T73: the first N letters of the speech are typed.
(fn TypeTo (N)
  (Class|Text|SetText :self (Variables|WBP_ChatLine|GetSpeechShown) :Text (Utilities|Text|ToText(String) (Utilities|String|GetSubstring :SourceString (V FullSpeech) :StartIndex 0 :Length N))))
```

```lisp
; T73: the typing is over (or stopped): the full speech shows as SetActor left it.
(fn TypeEnd ()
  (Widget|SetRenderOpacity :self (Variables|WBP_ChatLine|GetSpeechText) :InOpacity 1.0)
  (Class|Text|SetText :self (Variables|WBP_ChatLine|GetSpeechShown) :Text (Utilities|Text|ToText(String) ""))
  (Widget|SetVisibility :self (Variables|WBP_ChatLine|GetSpeechShown) :InVisibility "Collapsed"))
```

- The text passed in is `CurSpeech`, which `ShowLine` already ran through `DisplayText` (provider names and "@Meta", T26). So the typing types exactly what `SetActor` shows.
- **RE-CHECK:** if `SetActor` sets the speech color or font from other roles on T73's day, use those in `TypeBegin`.

## 3. `BPC_LinePlayer`: the typing timer

### 3a. `PlayCur`

New content of `Graphs/BPC_LinePlayer/PlayCur.txt` (the T20 line and its comment go; the plan, the print and the typing are new; the hold's own lines are T30's):

```lisp
; T30: the line reaches the screen: the chat line, its robot lights up, its stage actions play. Then the queue holds for its reading time.
; T73: the speech types out at type_cps with one voice sound per syllable (StartType, TypeTick), and the hold
; starts when the typing ends (EndType). A line with no speech, or no chat line to type into, holds at once.
(fn PlayCur ()
  (Class|WBPStage|SetTyping :self (V Stage) :Line "")
  (bind _wa (len (Utilities|String|ParseIntoArray :SourceString (V CurAction) :Delimiter " " :CullEmptyStrings true)))
  (bind _ws (len (Utilities|String|ParseIntoArray :SourceString (V CurSpeech) :Delimiter " " :CullEmptyStrings true)))
  (bind _raw (+ (V LineBase) (* (V LinePerWord) (+ _wa _ws))))
  (bind _hold (CallFunction|Scaled :T (Math|Float|Clamp(Float) :Value _raw :Min (V LineMin) :Max (V LineMax))))
  (set CurHold _hold)
  (CallFunction|PlanType :Text (V CurSpeech))
  (bind _ty0 (CallFunction|Scaled :T (V TypeSecs)))
  (bind _ty (select (> (V TypeSecs) 0.0) _ty0 0.0))
  (print (cat "NHOS: LINE " (V CurId) " hold=" (Utilities|String|ToString(Float) _hold) " syl=" (str (V TypeSylN)) " type=" (Utilities|String|ToString(Float) _ty)))
  (Class|WBPStage|AddChatLine :self (V Stage) :Name (V CurName) :Color (V CurColor) :Action (V CurAction) :Speech (V CurSpeech) :IsMe (V CurIsMe))
  (CallFunction|StartType)
  (Class|BPShow|LightSeat :self (V Show) :Seat (V CurSeat))
  (Class|BPShow|StageLine :self (V Show) :Seat (V CurSeat) :Entry (V CurEntry))
  (if (V TypeOn)
    (return))
  (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "Pump" :Time _hold :bLooping false))
```

- The order on screen stays T30's: `NHOS: LINE`, the chat line, the robot lights up and acts. The typing starts with the chat line, so the robot moves while its line types.
- **Hooks for later tasks:** T38's bubble call and T77's `Emote` go right after `StartType` (where T38-build puts them after `AddChatLine`). T38's typing bubble can follow `TypePos` from `TypeStep` (3e), where `TypeTo` is called.
- `Scaled` never returns under 0.01 s, so `_ty` is set to 0 by hand when there is no speech.

New variables (all on `BPC_LinePlayer`):

| Variable | Type | What for |
|---|---|---|
| `TypeCps`, `PauseComma`, `PauseStop`, `SylRate` | Float | From `pacing.json` (3h) |
| `CurHold` | Float | The current line's hold, for `EndType` |
| `TypeText` | String | The speech being typed |
| `TypeLen` | Integer | Its length |
| `TypeAt` | Float array | When each letter appears, in seconds from the start, before `fast_scale` |
| `TypeSyl` | Boolean array | Whether each letter starts a syllable |
| `TypeSylN` | Integer | The line's syllables (`syl=`) |
| `TypeSecs` | Float | The typing time before `fast_scale` |
| `PT` | Float | Running time while planning |
| `PIn`, `PPrevV` | Boolean | Planning: inside a word; the last letter was a vowel |
| `PWordStart`, `PWordSyl`, `PLastRun` | Integer | Planning: the word's first letter, its syllables, where its last vowel run started |
| `TypeOn`, `TypeHit` | Boolean | A line is typing; this tick reached a syllable |
| `TypePos`, `TypeNext` | Integer | Letters shown; letters due this tick |
| `TypeT0`, `LastSyl` | Float | Real time the typing started; real time of the last sound |
| `TypeW`, `NullType` | `WBP_ChatLine` object (`/Game/NHOS/UI/WBP_ChatLine.WBP_ChatLine_C`) | The line being typed; never set (the "none" to compare with, as `NullStage`) |
| `Audio`, `NullAudio` | `BPC_ShowAudio` object (`/Game/NHOS/Core/BPC_ShowAudio.BPC_ShowAudio_C`) | The show's audio component; never set |

`add_variable` with `container_type` `ARRAY` for the two arrays, `add_object_variable` with the `_C` class for the four object refs (T30's findings). `TmpF` exists already (`CueHoldFor`).

### 3b. What a line's plan looks like

For "Hi, you." at 30 letters a second:

| Letter | H | i | , | (space) | y | o | u | . |
|---|---|---|---|---|---|---|---|---|
| `TypeAt` (s) | 0.000 | 0.033 | 0.067 | 0.250 | 0.283 | 0.317 | 0.350 | 0.383 |
| `TypeSyl` | | ✓ | | | ✓ (the run "you") | | | |

The comma adds 0.15 s before the space. `TypeSecs` = 0.383 + 0.033 = 0.417 (no pause after the last letter). `syl=2`.

### 3c. The plan: `PlanType` and its helpers

```lisp
; T73: plans a line's typing: when each letter appears (TypeAt, before fast_scale) and which letters start a
; syllable (TypeSyl). A syllable is a run of vowels (a e i o u y) inside a word; a single final e after a
; consonant is silent when the word has another syllable; every word, and every speech, has at least one.
(fn PlanType (Text)
  (set TypeText Text)
  (clear (V TypeAt))
  (clear (V TypeSyl))
  (set TypeSylN 0)
  (set PT 0.0)
  (set PIn false)
  (set PPrevV false)
  (set TypeLen (Utilities|String|Len Text))
  (for _i (range (V TypeLen))
    (CallFunction|PlanChar :I _i))
  (if (V PIn)
    (CallFunction|EndWord :Last (- (V TypeLen) 1)))
  (if (and (> (V TypeLen) 0) (== (V TypeSylN) 0))
    (Utilities|Array|SetArrayElem (V TypeSyl) 0 true)
    (set TypeSylN 1))
  (set TypeSecs (V PT)))
```

```lisp
; T73: one letter of the plan. No early return (see the DSL rule in part 0).
(fn PlanChar (I)
  (bind _c (Utilities|String|GetSubstring :SourceString (V TypeText) :StartIndex I :Length 1))
  (add (V TypeAt) (V PT))
  (add (V TypeSyl) false)
  (set PT (+ (V PT) (+ (/ 1.0 (V TypeCps)) (CallFunction|PauseAt :I I))))
  (bind _w (Utilities|String|Contains :SearchIn "abcdefghijklmnopqrstuvwxyz0123456789'" :Substring _c))
  (bind _v (Utilities|String|Contains :SearchIn "aeiouy" :Substring _c))
  (if (and (not _w) (V PIn))
    (CallFunction|EndWord :Last (- I 1)))
  (if (and _w (not (V PIn)))
    (CallFunction|WordStart :I I))
  (if (and _w (and _v (not (V PPrevV))))
    (CallFunction|SylAt :I I))
  (set PIn _w)
  (set PPrevV (and _w _v)))
```

```lisp
; T73: a word starts at letter I.
(fn WordStart (I)
  (set PWordStart I)
  (set PWordSyl 0)
  (set PLastRun -1))
```

```lisp
; T73: letter I starts a vowel run, so a syllable.
(fn SylAt (I)
  (Utilities|Array|SetArrayElem (V TypeSyl) I true)
  (set PWordSyl (+ (V PWordSyl) 1))
  (set PLastRun I))
```

```lisp
; T73: the word ends at letter Last. A lone final e (its run starts at Last, so a consonant is before it) is
; silent when the word has another syllable; a word with none gets one on its first letter.
(fn EndWord (Last)
  (bind _e (Utilities|String|Equal,CaseInsensitive(String) :A (Utilities|String|GetSubstring :SourceString (V TypeText) :StartIndex Last :Length 1) :B "e"))
  (if (and (== (V PLastRun) Last) (and _e (> (V PWordSyl) 1)))
    (Utilities|Array|SetArrayElem (V TypeSyl) Last false)
    (set PWordSyl (- (V PWordSyl) 1)))
  (if (== (V PWordSyl) 0)
    (Utilities|Array|SetArrayElem (V TypeSyl) (V PWordStart) true)
    (set PWordSyl 1))
  (set TypeSylN (+ (V TypeSylN) (V PWordSyl))))
```

```lisp
; T73: the pause after letter I: type_pause_comma after , ; : and type_pause_stop after . ? ! (once, after the
; last mark of a run), none after the last letter. Every if returns (see part 0).
(fn PauseAt (I)
  (if (>= (+ I 1) (V TypeLen))
    (return 0.0))
  (bind _c (Utilities|String|GetSubstring :SourceString (V TypeText) :StartIndex I :Length 1))
  (bind _n (Utilities|String|GetSubstring :SourceString (V TypeText) :StartIndex (+ I 1) :Length 1))
  (if (Utilities|String|Contains :SearchIn ",;:.?!" :Substring _n)
    (return 0.0))
  (if (Utilities|String|Contains :SearchIn ",;:" :Substring _c)
    (return (V PauseComma)))
  (if (Utilities|String|Contains :SearchIn ".?!" :Substring _c)
    (return (V PauseStop)))
  (return 0.0))
```

Notes:
- `PauseAt` has a Float output (`add_function_param` with the output flag). Check after the write that `(return 0.0)` filled it.
- `Contains` is case-insensitive by default (`UseCase` false), so "A" and "E" count. `PauseAt` never passes an empty string to `Contains` (an empty `Substring` may count as found), because it returns before reading past the last letter.
- **The curly apostrophe (’)** isn't in the word set, so "don’t" splits into "don" and "t" (one extra syllable on "t"). The LLM replies and free mode use the straight one. If the DSL writes non-ASCII literals cleanly, add `’` to the set.
- The plan costs one pass over at most about 100 letters, once per line.

### 3d. `StartType`

```lisp
; T73: starts the typing of the line PlayCur just added. With no speech, or no chat line, nothing types.
(fn StartType ()
  (set TypeOn false)
  (if (== (V TypeLen) 0)
    (return))
  (bind _w (Class|WBPStage|LastChatLine :self (V Stage)))
  (set TypeW _w)
  (if (== (V TypeW) (V NullType))
    (print "NHOS: TYPE no chat line")
    (return))
  (Class|WBPChatLine|TypeBegin :self (V TypeW) :Speech (V TypeText))
  (set TypePos 0)
  (set TypeT0 (Utilities|Time|GetRealTimeSeconds))
  (set LastSyl -100.0)
  (set TypeOn true)
  (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "TypeTick" :Time 0.016 :bLooping true)
  (CallFunction|TypeTick))
```

The first `TypeTick` runs at once, so the first letter (and its sound, if it starts a syllable) shows with the chat line.

### 3e. `TypeTick` and `TypeStep`

```lisp
; T73: the typing timer, every 1/60 s while a line types.
(fn TypeTick ()
  (if (V TypeOn)
    (CallFunction|TypeStep)))
```

```lisp
; T73: shows every letter whose time has come (real time since the start, against TypeAt x fast_scale), plays
; one syllable if a letter that starts one appeared and the last sound is at least 1/syl_max_rate s old, and
; ends the typing when the plan's time is up. No early return (see part 0).
(fn TypeStep ()
  (bind _now (Utilities|Time|GetRealTimeSeconds))
  (bind _k (select (V Fast) (V FastScale) 1.0))
  (bind _el (- _now (V TypeT0)))
  (set TypeHit false)
  (set TypeNext (V TypePos))
  (for _i (range (V TypeLen))
    (CallFunction|TickChar :I _i :El _el :K _k))
  (if (> (V TypeNext) (V TypePos))
    (set TypePos (V TypeNext))
    (Class|WBPChatLine|TypeTo :self (V TypeW) :N (V TypePos)))
  (if (and (V TypeHit) (>= (- _now (V LastSyl)) (/ 1.0 (V SylRate))))
    (set LastSyl _now)
    (CallFunction|SayVoice))
  (if (>= _el (* (V TypeSecs) _k))
    (CallFunction|EndType)))
```

```lisp
; T73: letter I is due if its time has come.
(fn TickChar (I El K)
  (if (<= (* (get (V TypeAt) I) K) El)
    (CallFunction|TickHit :I I)))
```

```lisp
; T73: letter I shows this tick; if it is new and starts a syllable, this tick plays a sound.
(fn TickHit (I)
  (set TypeNext (+ I 1))
  (if (and (>= I (V TypePos)) (get (V TypeSyl) I))
    (set TypeHit true)))
```

- `TypeAt` rises letter by letter, so the due letters are always the first ones, and `TypeNext` ends at their count.
- Each tick walks the whole line (at most about 100 calls of `TickChar`). That is a fraction of a millisecond; the DSL has no loop that starts at `TypePos`.
- `_now` is a pure call read in two places. A few microseconds between them don't matter.

### 3f. The sound

```lisp
; T73: one syllable in the speaker's voice (T72). CurName is the provider name I see; IsMe picks my own set.
(fn SayVoice ()
  (CallFunction|FindAudio)
  (if (== (V Audio) (V NullAudio))
    (return))
  (Class|BPCShowAudio|Syllable :self (V Audio) :Name (V CurName) :IsMe (V CurIsMe)))
```

```lisp
; T73: the show's BPC_ShowAudio, on the same actor as this component (BP_Show).
(fn FindAudio ()
  (if (== (V Audio) (V NullAudio))
    (bind _a (Actor|GetComponentbyClass :self (Components|GetOwner) :ComponentClass "/Game/NHOS/Core/BPC_ShowAudio.BPC_ShowAudio_C"))
    (set Audio _a)))
```

`Syllable` prints nothing (T72: a show plays thousands), never repeats a clip twice in a row, moves the pitch up to 6% and stops the slot's last clip. So the babble needs nothing more here.

### 3g. `EndType`, `StopType` and `Clear`

```lisp
; T73: the typing is done: the full line shows, and the hold starts (T30's reading time, retuned).
(fn EndType ()
  (Utilities|Time|ClearTimerbyFunctionName :Object self :FunctionName "TypeTick")
  (set TypeOn false)
  (Class|WBPChatLine|TypeEnd :self (V TypeW))
  (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "Pump" :Time (V CurHold) :bLooping false))
```

```lisp
; T73: stops a line that is still typing and shows it whole, with no hold (Clear).
(fn StopType ()
  (Utilities|Time|ClearTimerbyFunctionName :Object self :FunctionName "TypeTick")
  (if (V TypeOn)
    (set TypeOn false)
    (Class|WBPChatLine|TypeEnd :self (V TypeW))))
```

New content of `Graphs/BPC_LinePlayer/Clear.txt`: T30's lines, with `(CallFunction|StopType)` added before `(set Busy false)`, and the comment line `; T73: also stops a line that is still typing.` under T30's.

`Busy` stays true from `Pump` through the typing and the hold, as before, so `IsBusy`, `LinePrompt` and T66's timer see no difference except the time.

### 3h. `LoadPacing` and `PaceF`

```lisp
; T73: a number from the pacing block, or Def when the file doesn't have it.
(fn PaceF (Key Def)
  (bind _h (Json|HasField (V Pace) Key))
  (if (not _h)
    (return Def))
  (bind _v (Json|GetField (V Pace) Key))
  (set TmpF _v)
  (return (V TmpF)))
```

In `Graphs/BPC_LinePlayer/LoadPacing.txt`:

1. The defaults block becomes (`LineBase` to `LineMax` retuned, four new lines after `FastScale`):
   ```lisp
     (set LineBase 0.6)
     (set LinePerWord 0.12)
     (set LineMin 1.5)
     (set LineMax 2.5)
     (set TypeMin 0.6)
     (set TypeMax 1.6)
     (set FastScale 0.1)
     (set TypeCps 30.0)
     (set PauseComma 0.15)
     (set PauseStop 0.3)
     (set SylRate 12.0)
   ```
2. Inside `(if _hp ...)`, after `(set CueHold _f8)`:
   ```lisp
         (set TypeCps (Math|Float|Max(Float) (CallFunction|PaceF :Key "type_cps" :Def 30.0) 1.0))
         (set PauseComma (CallFunction|PaceF :Key "type_pause_comma" :Def 0.15))
         (set PauseStop (CallFunction|PaceF :Key "type_pause_stop" :Def 0.3))
         (set SylRate (Math|Float|Max(Float) (CallFunction|PaceF :Key "syl_max_rate" :Def 12.0) 1.0))
   ```
   Close the parentheses of `(set CueHold _f8)))` after these four lines instead. `Max` keeps a 0 in the file from dividing by zero.
3. The comment line becomes `; T30: reads the pacing block from Content/NHOS/Data/pacing.json and fast_lines from Local/switches.json. T73: the typing values.`, and the print adds `" type_cps=" (Utilities|String|ToString(Float) (V TypeCps))` before its last `)`: `NHOS: PACING file=true fast_lines=false type_cps=30.0`.

## 4. `WBP_Stage`: `LastChatLine`

New variable `NullChat` (`WBP_ChatLine` object, never set). New function with a `WBP_ChatLine` object output:

```lisp
; T73: the newest chat line (the last child of LogScroll, where AddChatLine puts it), so BPC_LinePlayer can
; type its speech. None when the chat is empty or the last child isn't a WBP_ChatLine.
(fn LastChatLine ()
  (bind _n (Class|PanelWidget|GetChildrenCount :self (Variables|WBP_Stage|GetLogScroll)))
  (if (< _n 1)
    (return (V NullChat)))
  (bind _c (Utilities|Casting|CastToWBP_ChatLine :Object (Class|PanelWidget|GetChildAt :self (Variables|WBP_Stage|GetLogScroll) :Index (- _n 1)))
    (:then
      (return _c))
    (:CastFailed
      (return (V NullChat)))))
```

- **RE-CHECK** with part 0, step 3.1. If the chat lines live in another panel on T73's day (T34 hasn't run, but check), use that panel.
- T38 later collapses `ChatSize` when the chat is closed; the lines still go into `LogScroll` (T38-build: "the hidden chat still gets every line"), so they still type, unseen.

## 5. The blip goes

1. `PlayCur`'s new source (3a) has no `LineBlip` call.
2. `remove_function_graph` on `BP_Show.LineBlip`, then on `BPC_ShowAudio.Blip` (T55 removed `BP_Show` functions this way). Compile both (`compile_blueprint` returns null on success; read the editor log, T51). An error naming either means part 0 step 3.3 missed a caller.
3. `git rm Graphs/BP_Show/LineBlip.txt Graphs/BPC_ShowAudio/Blip.txt`.
4. Leave `Sfx`'s `blip` branch and `/Game/NHOS/Audio/Robot/S_TalkBlip` as they are, unused (decision 12). `Syllable.txt`'s comment "like Blip does" stays; the graph doesn't change.
5. If T73 doesn't hold the `BP_Show` or `BPC_ShowAudio` lock on its day, skip step 2 and 3 for that asset, leave the function unused, and say so under "## Findings" (task step 4).

## 6. `pacing.json`, and the arithmetic

### 6a. The file

```json
{
	"_readme": "Line pacing (T30, T73). BPC_LinePlayer reads it at the first line of a run. When a line plays, its name and action show at once and its speech types out at type_cps letters a second, with a pause of type_pause_comma after , ; : and type_pause_stop after . ? ! (none after the last letter). Each syllable plays one sound in the speaker's voice, at most syl_max_rate sounds a second. When the typing ends, the line holds for line_base + line_per_word x its words (action and speech), kept between line_min and line_max, before the next line plays. Before an AI line in Free Talk and the reactions, '<name> is typing...' shows for a random time between typing_min and typing_max. cue_hold: how long the queue waits after a screen change of that kind (a banner, a cut with its reveal stamp), so the next line doesn't play under it; a kind that isn't listed waits 0. fast_scale multiplies every wait, the typing too, when fast_lines is on in Local/switches.json, for autoplay checks. Every time is in seconds.",
	"pacing": {
		"line_base": 0.6,
		"line_per_word": 0.12,
		"line_min": 1.5,
		"line_max": 2.5,
		"type_cps": 30,
		"type_pause_comma": 0.15,
		"type_pause_stop": 0.3,
		"syl_max_rate": 12,
		"typing_min": 0.6,
		"typing_max": 1.6,
		"fast_scale": 0.1,
		"cue_hold": {
			"banner": 2.0,
			"cut": 3.0
		}
	}
}
```

(`typing_min` and `typing_max` are T30's "is typing..." wait, not this task's typing; their names stay so nothing else changes.)

### 6b. One 15-word line

"So here is the whole plan: we wait by the Riser, then grab the chicken." with the action "moves to the Riser": 15 + 4 = 19 words, 71 letters, 17 syllables (here, whole and the each count 1; Riser and chicken 2).

| | Before (T30) | After (T73) |
|---|---|---|
| Typing | 0 (the line appears at once) | 71 ÷ 30 = 2.37 s, + 0.15 (colon) + 0.15 (comma) = **2.67 s** |
| Hold | 1.2 + 0.25 × 19 = 5.95, capped at **5.0 s** | 0.6 + 0.12 × 19 = 2.88, capped at **2.5 s** |
| Line on screen before the next | **5.0 s** | **5.17 s** |
| Sounds | 1 blip | 17 syllables, 16 sounds (one syllable comes within 1/12 s of the last and is dropped) |

A long-worded 15-word line is the worst case: 136 letters with two commas types in 4.8 s, so it takes 7.3 s against 5.0. LLM lines that long are rare (the free-mode lines are 36 to 81 letters).

Shorter lines: "Wow. I did not see that vote coming." (8 words, no action) took 3.2 s before, and now types in 1.50 s and holds 1.56 s: 3.06 s. An action-only line or a pass took 2.0 to 3.0 s before and now holds 1.5 s (`line_min`).

### 6c. A whole scene

The model: one scene of a 5-actor free autoplay show, every line from `free_mode.json` (scene turn, free talk, vote and reaction lines, with `{prop}` = "rubber chicken", `{place}` = "the Riser", `{actor}` = "Anthropic") and `autoplay.json` (my lines): 3 turns × 5 lines (AI lines with one or two actions), 2 Free Talk rounds × 5, 5 votes ("votes for Meta" plus the reason), 5 reactions. 35 lines. A Python model of `PlanType` and the hold (`type_cps` 30, the two pauses) gives:

| Lines | Count | Before, each | After: typing + hold, each |
|---|---|---|---|
| Scene turns | 15 | 4.77 s | 2.21 + 2.34 = 4.55 s |
| Free Talk | 10 | 3.62 s | 2.11 + 1.76 = 3.87 s |
| Votes | 5 | 4.60 s | 2.21 + 2.23 = 4.44 s |
| Reactions | 5 | 3.95 s | 2.29 + 1.92 = 4.21 s |
| **All 35 lines** | | **150.5 s** | **150.2 s** |

What doesn't change adds the same to both: the "is typing..." waits before the 12 AI lines in Free Talk and the reactions (about 1.1 s each, 13 s) and the cue holds (the tally banner 2 s, the cut 3 s, the end-of-scene banner 2 s: 7 s). So the model puts scene 1 at about **171 s before and 170 s after**. Scene turns get a little shorter and the chat phases a little longer, because their lines have no action words to hold for.

The model is a guide; the real numbers come from run A and run C (part 8), and T73 writes both under "## Findings". If the after time is off by more than about 10%, move `line_per_word` first (each 0.01 moves the 35 lines by about 3 s: they average 12.7 words, and the lines at `line_max` don't move), then `line_max`.

## 7. The design doc edit (waits for my person's OK in T73)

The doc says how a line appears in one place: **Art Inspiration, Components table, the row "Chat", its Behavior cell**, which reads: "Actor lines only, newest at the bottom. "Name is typing…" holds the place of the next line."

**Proposed:** add one sentence to that cell, so it reads:

> Actor lines only, newest at the bottom. "Name is typing…" holds the place of the next line. Each line's speech then types out letter by letter in a box already at its full size, while the speaker's voice babbles one gibberish sound per syllable.

Nothing else needs to change:
- The Rules tab's Free Talk bullet "AI lines appear after a short typing delay." is still true (T30's "is typing..." stays).
- The Rules tab's "Every actor submits a turn, then all turns play out at once." is the line my person kept as it is in T30 (an edit must follow what the doc already has). T73 doesn't touch it.
- Art Inspiration's "gibberish blips for voices" already describes T72's voices.
- Tech & Build's "Cut for the jam: voice acting" is about acted voices, not the babble.

Show my person the cell before and after, and make the edit (a direct edit, not a suggestion, unless they say otherwise) only after their OK. If they decline, write that under "## Findings", as T30 did.

## 8. The check

The Windows commands are in `CLAUDE.md`; the game window writes `Saved/Logs/<name>.log` there. On a Mac the log is `~/Library/Logs/AIMegaJam2026/<name>.log` (T27's findings). In `Local/switches.json` for runs A to C: `"autoplay": true`, `"mode": "free"`. Close each game window when its run is done, and set `autoplay` back to false at the end.

To time scene 1 from a log (first `NHOS: LINE` to the first `NHOS: CUE prep`, which is scene 2's Scene Prep, as the first scene's prep isn't a cue):

```bash
python - Saved/Logs/T73before.log <<'EOF'
import re, sys, datetime as dt
L = open(sys.argv[1], encoding='utf-8', errors='replace').read().splitlines()
ts = lambda l: dt.datetime.strptime(re.match(r'\[(\S+?)\]', l).group(1), '%Y.%m.%d-%H.%M.%S:%f')
a = next(l for l in L if 'NHOS: LINE ' in l)
b = next(l for l in L if 'NHOS: CUE prep' in l)
print('scene 1:', round((ts(b) - ts(a)).total_seconds(), 1), 's')
EOF
```

### Run A: scene 1 before (first thing, before any change)

`"fast_lines": false`. Game window with `-log=T73before.log`. Wait for the first `NHOS: CUE prep` (about 3 minutes), then close the window and time it. Write the number under "## Findings".

### Run B: the fast show (after the build)

`"fast_lines": true`, `-log=T73fast.log`, to `NHOS: SHOW END`. Look for:
- `NHOS: PACING file=true fast_lines=true type_cps=30.0`.
- Every `NHOS: LINE` line has `syl=` and `type=`, and `syl` is 0 exactly when `type` is 0 (an empty speech):
  ```bash
  python - Saved/Logs/T73fast.log <<'EOF'
  import re, sys
  L = [l for l in open(sys.argv[1], encoding='utf-8', errors='replace') if 'NHOS: LINE ' in l]
  bad = [l for l in L if not re.search(r' syl=\d+ type=[\d.]+', l)]
  odd = [l for l in L if re.search(r' syl=(\d+) type=([\d.]+)', l) and ((re.search(r' syl=(\d+)', l).group(1) == '0') != (float(re.search(r' type=([\d.]+)', l).group(1)) == 0.0))]
  print(len(L), 'LINE lines,', len(bad), 'missing fields,', len(odd), 'with syl and type out of step')
  EOF
  ```
  Then compare the count of `syl=0` lines with the passes and action-only lines in the `NHOS: LOG` lines (`says=` empty): they should match.
- `NHOS: SHOW END`, and `grep -n "LogScript" Saved/Logs/T73fast.log` shows nothing new (T30's runs had none).
- No `NHOS: TYPE no chat line`.
- The same count of `NHOS: LINE` lines as `NHOS: LOG` lines that reach the screen, as T30 had (nothing lost).

### Run C: scene 1 after

`"fast_lines": false`, `-log=T73after.log`, timed as run A. Write both numbers under "## Findings", with the model's 171 and 170 s for comparison. Each `hold=` should be 1.5 to 2.5 and each `type=` mostly 1.2 to 3.5.

### Run D: PIE by hand, the screenshots

Test for Free, a 1600 × 900 floating window, autoplay off, `fast_lines` off (the "Claude does the playing" build note). **For this run only, set `type_cps` to 5 in `pacing.json`** (a 60-letter line then types for 12 s), so a screenshot can catch a line half typed; set it back to 30 before the commit, and say so under "## Findings".

1. Scene Prep: a cast row in the card looks as before (`WBP_ChatLine`'s new overlay, part 2a).
2. A scene turn: an AI line half typed. Two screenshots about 1 s apart: the line's box (its height and the lines above it) is the same in both, only the text grows.
3. Free Talk: "<name> is typing...", then that line half typed.
4. My own line typing (my turn's line, after the send).
5. Look for the hop (decision 1): a partly typed word at the end of a row that moves to the next row when it completes. Note how often under "## Findings".
6. With `type_cps` back at 30, one more scene turn: judge as a first-time player whether each line can be read before the next one starts.

Under "## Findings", also write: **Claude can't hear the result, so the sound and the pace of the babble are not checked** (task "Done when"), and whether `Blip` and `LineBlip` were deleted (part 5).

## 9. The commit

One commit, `T73: Lines type out, one voice sound per syllable`, with what "How to run a task" lists, staged by path:

- `Content/NHOS/Core/BPC_LinePlayer.uasset`, `Content/NHOS/UI/WBP_ChatLine.uasset`, `Content/NHOS/UI/WBP_Stage.uasset`, `Content/NHOS/Core/BPC_ShowAudio.uasset`, `Content/NHOS/Core/BP_Show.uasset`
- `Content/NHOS/Data/pacing.json` (with `type_cps` 30)
- `Graphs/BPC_LinePlayer/`: `PlayCur.txt`, `Clear.txt`, `LoadPacing.txt`, and new `PaceF.txt`, `PlanType.txt`, `PlanChar.txt`, `WordStart.txt`, `SylAt.txt`, `EndWord.txt`, `PauseAt.txt`, `StartType.txt`, `TypeTick.txt`, `TypeStep.txt`, `TickChar.txt`, `TickHit.txt`, `SayVoice.txt`, `FindAudio.txt`, `EndType.txt`, `StopType.txt`
- `Graphs/WBP_ChatLine/`: new `TypeBegin.txt`, `TypeTo.txt`, `TypeEnd.txt`; `Graphs/WBP_Stage/LastChatLine.txt` (new)
- the removal of `Graphs/BP_Show/LineBlip.txt` and `Graphs/BPC_ShowAudio/Blip.txt`
- `Docs/tasks/T73.md` (Result and Findings), `Docs/Plan.md` (the box and the move to "Done"), `Docs/DevLog.md` (one line)

Then unlock the five assets after the push.
