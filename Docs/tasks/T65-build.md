# T65 build sheet: the speech field: a word counter, focus and @ mentions

Back to [T65](T65.md). A Mac prep session wrote this on 2026-11-15 against `944978c`, before T62, T63 and T64 were built. **A PC prep session brought it up to date on 2026-11-15, without the editor, against `noHumansOnSet` at `47f95a3`** (T83 on top of T64's two lane parts, T60, T63, T62, T58, T57 and T73). It is a plan, not a record: nothing here was written to the editor. When T65 writes a graph, its source goes to `Graphs/` as usual.

## This update (2026-11-15, against `47f95a3`)

**Why:** the first version planned against T64's sheet. T64's two lane parts are now built and pushed (`WBP_ActionBuilder`, `WBP_Chip`, and the input row in `WBP_Stage`), and some of what they built differs from that sheet. Every graph, widget, variable, function and line this sheet names was checked against `Graphs/WBP_Stage/`, `Graphs/WBP_ActionBuilder/`, `Graphs/WBP_Chip/`, `Graphs/BP_Show/` (`CapWords`, `SendHumanTurn`, `SendHumanTalk`, `SendHumanReact`, `SendHumanVote`, `SpellAsk`, `SpellSkip`, `InputState`, `HumanSay`, `LastWordPrompt`, `LinePrompt`, `PrepPrompt`), `Graphs/BP_StageDirector/` (`ItemsFor`, `TargetsFor`, `CanDo`), `Graphs/UIStyle/`, `Content/NHOS/Data/input.json` and `pacing.json`, and the findings in `T64.md` (parts 1 and 2), `T63.md`, `T62.md`, `T58.md`, `T57.md`, `T73.md` and `T60.md`.

**What changed in this sheet:**

1. **The mono font.** `UIStyle` has no `"Mono"` role: T64 kept the font on the builder, as its variable `MonoFont` (the engine's Droid Sans Mono, typeface `Default`, 18). Every `UIFont("Mono")` here is gone. A new one-line `WBP_Stage.Mono()` returns the builder's `MonoFont`, and `SyncCount` uses it (part 2). `WBP_Word.Setup` takes the font as a new input, `Font`, and `PutWord` passes the builder's `MonoFont` (part 6). T66's timer uses `Mono()` too.
2. **The preview's names.** T64 named the string builder `MakePreview` (the TextBlock is still `PreviewText`). Part 6b's table now quotes today's lines in `Refresh.txt`, `SetLine.txt`, `StyleAll.txt` and `EventGraph.txt`, where `StyleAll` sets the font from `(V MonoFont)`.
3. **The change chain.** `CleanText`'s input pin is `In` (T64 part 2). `SpeechApply` ends with T64's chain as `Graphs/WBP_Stage/EventGraph.Builder.txt` has it.
4. **Focus.** T64 found that `IsFocusable` off isn't enough: on a mouse-down that sets no focus, Slate gives the focus to the game viewport. The builder already gives it back after its own clicks (`KeepFocus`, armed by `SetFocusBack(InputBox)` in `BuilderTurn`). So `HoldFocus` (part 4) still matters, for the clicks the builder doesn't cover: my card, the chat, the stage, the vote row, and every phase with no builder. Part 0's focus survey now expects the game viewport to take the focus on any click.
5. **`SetPrompt` and `SetPrepMode`** are planned from today's files. `SetPrompt` now ends with `SyncAction`, then `FitBuilder`, so `HoldFocus` goes after `FitBuilder`. `SetPrepMode`'s `Prep` branch now also calls the builder's `Close` and `FitBuilder`.
6. **The seat swatch is 14 × 20, not 6 px wide** (T64 finding 8: at 6 px, with its 2 px ink outline, the color barely showed). The @ list's bars follow.
7. **Node names that T64 found:** `Panel|AddChildtoWrapBox` (not `Widget|AddChildToWrapBox`), `Widget|Panel|ClearChildren`, `Widget|SetText(TextBox)` with `InText`, `Layout|SizeBox|SetWidthOverride`. `Class|BPShow|Get<Var> :self <show>` works (the builder reads `SeatName`, `SeatLabel`, `SeatId` and `TurnNum` that way), and `(set Show (Actor|GetActorOfClass ...))` needs no cast (`OpenTurn`), so the old cast note is gone.
8. **The panel's sizes.** In my scene turns the lower panel is 1080 wide (T64's `LowerWideBuild`, not 1000), and the chat gives up the builder's height every frame (`FitBuilder`). Elsewhere it is 640. The counter's 72 px come out of the field. Part 7 now checks the field's width at 640 with the counter, Action! and Pass.
9. **`SubmitInput` as T64 built it:** while the builder `Blocks`, Enter prints `NHOS: BUILDER blocked` and keeps the text. Otherwise it sends the text, an empty one too while the builder is up, then clears the box. That clear reaches the change chain, so the counter resets to 0/15 (part 3c).
10. **Unreal MCP rules from T62 to T64** are in part 0 and part 7: `read_graph_dsl` marks a Blueprint as changed, `get_node_type_pins` puts a node in the graph, `call_tool` takes `toolset_name` and `tool_name` apart, the Slate inspector's `PressKey` types no characters and its `Hover` raises no tooltip, a click lands only while the PIE window is active, and the PIE window's ref changes on every start.

**No decision changed.** The 14 decisions below all stand, with their wording updated for items 1, 4, 6 and 8. None of them was my person's answer: the first version asked my person nothing, and this update asks nothing new.

**T64's chain part isn't pushed yet** (the session `t64-chain-calls` is adding it as this update is written). Its three `BP_Show` edits: `StartTurn` calls `BuilderTurn` (without it the builder never opens in a real show), `HandleSend` calls `TakeAction` (without it Action! sends Verb `none`), and `ComputePrompt` gets the two new hint texts (the scene hint "Say something (optional)..."). T65 builds on all three. The re-checks below and part 0 mark what depends on them.

**What T65 must still check in the editor** (besides part 0's survey):

- **T64's chain is in** (part 0.1): the builder opens at my scene turns, Action! sends the built action, and the empty field's hint reads "Say something (optional)...". Run A steps 1, 8 and 9 depend on it. Read `T64.md`'s part 9 notes for T65 first.
- `InputRow`'s children and their paddings (survey 1). No source has them: T64 added `ActionBuilder` above `InputRow` and changed nothing in the row itself.
- The `OnTextCommitted(InputBox)` chain sends only on Enter (survey 4). It has no source file.
- The getter names `Class|WBPActionBuilder|GetMonoFont`, `Class|BPShow|GetOnStage`, `GetHumanSeat` and `GetMaxWords` (survey 6). `GetSeatLabel` is confirmed.
- Whether an `OnPreviewKeyDown` override can be made through MCP (survey 5), and whether the Slate inspector's `PressKey` reaches it (survey 8).

## What this sheet builds on (as pushed at `47f95a3`)

- **T64** (`T64.md` parts 1 and 2): `WBP_ActionBuilder` with its preview line (`PreviewBox` > `PreviewText`, filled from `MakePreview` by `Refresh` and `SetLine`), its `MonoFont`, `Labels` (screen names), `Names` (Player names), `Seat`, `SetFocusBack` and `KeepFocus`; `WBP_Chip` with its 14 × 20 seat swatch; and in `WBP_Stage`: `ActionBuilder` in `LowerBox` right before `InputRow`, `SendLabel` reading **Action!**, `BuilderTurn`, `TakeAction`, `SyncAction`, `FitBuilder`, the rewritten `SetPrompt`, `SetPrepMode`, `SetPhase` and `SubmitInput`, and `Graphs/WBP_Stage/EventGraph.Builder.txt`: `OnTextChanged(InputBox)` → `CleanText(In)` → `WBP_ActionBuilder.SetLine`. `PreviewName` is the one place that writes `@Meta` in the preview.
- **T63:** every line of mine goes through `SpellAsk`. A mention reaches the AIs as "@Player N" through `ResolveMentions` (in `InputState` when the spelling call runs, in `SpellSkip` when the line goes as typed). `HumanSay` caps the line with `CapWords`. So T65 changes nothing after the send.
- **T62:** nothing in T65 calls the stage director (`ItemsFor`, `TargetsFor` and `CanDo` are the builder's and `HumanCheck`'s).
- **T57, T58:** Free Talk and the last word use the same input box (`SendHumanTalk`), as do the reactions (`SendHumanReact`) and the vote's reason (`SendHumanVote`). So the counter, the focus and the @ list work there too, with no branch of their own. T58's last-word hint ("Answer who named you, like: @Meta, ...") and Free Talk's ("Say something, like: @Meta, why did you grab the rose?") already show the @ form.
- **T73, T60:** they don't touch the input row. T73 types each line out; `LinePrompt` keeps my input closed until the queue is empty (`BPC_LinePlayer.IsBusy`), so my input still opens only after the last line has typed and held.

Each place is named by its text first. Find each line by its text before you change it.

**Sources the first version read:** `T65.md` and its plan entry; `T62.md` (the input spec: "Layout" row 3, "Saying a line"), `T64.md`, `T66.md`; the T57, T58, T62 (names only), T63 and T64 build sheets; the findings of T04 (`ClearKeyboardFocusOnCommit` off, `IsFocusable` off), T26 (`ResolveMentions`, `DisplayText`), T27 (`RootBox` is an Overlay, `InputStack`, `HintLabel`), T30 (the `if`/`return` rule), T33 and T38-build (geometry in `RootBox`'s space); the dropped T31 (`git show df7df63^:Docs/tasks/T31.md`, the Tab note); `Graphs/UIStyle/` (`SeatColor`, `UIColor`, `UISize`, `UIFont`), `Graphs/WBP_Keys/EventGraph.txt` (`HasKeyboardFocus`), `Tools/dslpp.py`; `personas.json` (the four screen names). **A byte search** of the repo folder's `WBP_Stage.uasset` at `944978c`: `RootBox`, `InputStack`, `InputRow`, `LowerBox`, `HintLabel`, `CleanText`, `SubmitInput`, `OnTextCommitted` and `ClearKeyboardFocusOnCommit` were there; `OnPreviewKeyDown`, `OnKeyDown`, `CanvasPanel` and `WrapBox` were not. (T64 has since added `OnTextChanged`.)

## In short

- **The counter** (part 2): a `CountPill` (Border) with `WordCount` (TextBlock, in the builder's mono font) between `InputStack` and `SendButton`: "12/15" in quiet text, and a red pill with white text at 15.
- **The 15-word cap** (part 3): a new `SpeechChanged` takes over T64's `OnTextChanged(InputBox)` chain. It counts words as `CapWords` does, refuses a 16th word (the first 15 words and a space stay, so the next letter is refused too), cuts a paste the same way, then feeds the counter, the @ list and T64's preview.
- **Focus** (part 4): a new `HoldFocus`, called by `SetPrompt` every frame, gives the focus back to the speech field the frame after anything took it, while my input is open. The builder's own `KeepFocus` already does this for its clicks.
- **The @ list** (part 5): a pop-up of up to four buttons (`AtPop` in `RootBox`, the full-screen overlay), placed right over the field each time it opens, so nothing on the screen moves. It lists the actors still on stage but me, by their screen names, each with a seat-color swatch, filtered by the letters after the "@". A new `OnPreviewKeyDown` override hands Up, Down, Enter, Tab and Escape to a new `SpeechKey`, which returns Handled for them.
- **A mention is a unit and a chip** (part 6): a picked name goes in as "@Meta " (one Backspace right after it removes it all), and T64's preview line draws every mention as a chip in the actor's seat color. To do that, the preview line becomes a `WrapBox` of words from a new small widget, **`WBP_Word`**.
- **`BP_Show` doesn't change.** `WBP_Stage` reads `SeatLabel`, `OnStage`, `HumanSeat` and `MaxWords` from it with getters, as the builder reads `SeatName` and `SeatLabel`.

## Questions for my person

None. The task's steps and what T64 built settle what gets built; the calls they leave open are below as decisions.

## Decisions made for my person (open to change)

My person asked prep sessions to take their own recommendation on design calls. The T65 session shows this list to my person when it closes the task.

1. **The @ list is a pop-up, not a row in the panel.** `AtPop` is a child of `RootBox` (T27 made it the full-screen Overlay), placed each time it opens so its left edge is the field's and its bottom sits 8 px (`S2`) above the field's top. It covers the bottom of the chat, or in my scene turns the builder's lower row of chips, while it is open, and nothing moves. A new row in `LowerBox` would push the panel's top up over the robots (the doc's rule; T64 worked to keep that top still with `FitBuilder`).
2. **Its entries** are buttons like T64's chips: a 14 × 20 seat-color swatch with an ink outline (T64's size), then "@Meta" in white on plum (Secondary). The highlighted one is paper (cream, dark text), as T64's picked chip. The first match is highlighted when the list opens. The swatch carries the color, because white or dark text on four seat colors doesn't reach 4.5:1 everywhere.
3. **The filter is a prefix, in any case:** "@me" leaves Meta, "@" alone lists everyone. No match closes the list.
4. **Only the word at the end of the line opens the list**, which is where the caret is while I type. UMG gives a Blueprint no caret position, so an "@" typed mid-line after I move the caret back gets no list. It still reaches the AIs as "@Player N", because `ResolveMentions` resolves any "@Meta" I type.
5. **Escape closes the list until a new "@"** (another "@" word). Typing more letters after the same "@" doesn't reopen it.
6. **The counter** is "n/15" in the builder's mono font (T64's `MonoFont`, so the digits don't jump), in `Quiet`, always next to the field while the input row shows (all play phases, Scene Prep excepted). **At 15 it is a red pill with white text:** `UIStyle`'s Red is a fill color (its comment: "fill, white text"), and red text on the ink panel is only about 3.2:1. White on Red is about 5.7:1.
7. **A 16th word is refused, not trimmed afterward:** when a change makes 16 words or more, the line becomes its first 15 words and one space. So the trailing space stays, and the next letter is refused again instead of growing word 15. A paste is cut the same way. Each refusal prints `NHOS: SPEECH cap words=<n> -> 15`.
8. **A mention is "@Meta " as one unit.** One Backspace right after it, at the end of the line, removes the whole mention: the space after it (the line would end in "@Meta") or its last letter (the line would end in "@Met"). A Backspace elsewhere is a plain Backspace. A picked name uses the screen name's own capitals ("@Meta").
9. **The chip is drawn in T64's preview line** (step 5's fallback), because UMG's editable text can't hold a widget. Every mention in the preview, typed or picked, and the action's own target ("throw rose at @Meta") becomes a chip: filled with the seat color, ink text, round corners, in the mono font. What's glued to it (", " or a quote) stays plain. **The preview line shows only in my scene turns** (T64), so in Free Talk, the last word, the vote and the reactions the mention shows as plain "@Meta" in the field; T34 can add a preview line there if the screenshots say it's needed.
10. **The preview line becomes a `WrapBox` of words** (`PreviewWrap`), each a `WBP_Word` (a new widget, outside T65's Touches; the commit message names it), from a pool of 40 made once. T64's chips are made fresh on every refresh, but the preview redraws on every keystroke, so a pool is cheaper. A `RichTextBlock` can color a run but can't draw a chip without a C++ decorator.
11. **The focus comes back every frame** while my input is open (`HoldFocus`), not only on the clicks the task lists (the builder, my card, the chat). That covers any click on the screen, the game viewport's included. `NHOS: FOCUS back` prints once each time it has to. The builder's own `KeepFocus` stays as T64 built it.
12. **Tab never moves the focus.** With the list closed, Tab does nothing. Up and Down are always Handled in the field, so they never move the focus either.
13. **No `BP_Show` change.** `WBP_Stage` finds `BP_Show` once (`ShowRef`) and reads `SeatLabel`, `OnStage`, `HumanSeat` and `MaxWords` with getters. My own seat ("You") never shows in the list and never becomes a chip.
14. **New check lines:** `NHOS: SPEECH cap words=<n> -> <max>`, `NHOS: MENTION open <names>`, `NHOS: MENTION pick <name>`, `NHOS: MENTION close`, `NHOS: MENTION removed <@name>`, `NHOS: FOCUS back`.

## Step coverage

| T65 step | Where |
|---|---|
| 1. The speech field, its hint, the counter, Action!, room for the timer | Part 2 (the counter between `InputStack` and `SendButton`; T66's timer goes last in `InputRow`). The hint "Say something (optional)..." is `ComputePrompt`'s scene hint, which T64's chain sets; part 7 checks it. |
| 2. The 15-word cap, the red counter, a 16th word refused, a paste cut | Parts 2 and 3 |
| 3. Focus stays in the field; check nothing else takes it | Part 4, and part 0's focus survey (T64 found the game viewport takes it on any click) |
| 4. The @ list, its keys, `OnPreviewKeyDown` | Part 5 |
| 5. A mention is a chip (or a unit plus a chip in the preview line) | Parts 3 (`UnitBackspace`) and 6, and part 7's Findings |
| 6. Speech never acts | Nothing to build (T63's input LLM makes no action; the builder reads no typed text but the preview's `Line`); part 7 run A step 9 checks it |

## 0. Before you start (after T64 is pushed)

1. `git log --oneline -15` shows T64's chain commit (its title starts `T64:` and its box is checked in the plan); `Docs/claims/T64` is released. **Read `T64.md`'s part 9 notes for T65** and take them in where they change a part below. `git lfs locks` shows no lock on `Content/NHOS/UI/WBP_Stage.uasset` or `Content/NHOS/UI/WBP_ActionBuilder.uasset`. Claim T65 (`git lfs lock Docs/claims/T65`) and lock both. `WBP_Word` is new and needs no lock. **`BP_Show` needs no lock** (decision 13). Don't read `BP_Show`'s graphs: `read_graph_dsl` marks a Blueprint as changed (T64 part 2), and T65 doesn't hold it. If the editor asks to save `BP_Show` at the end, answer "Don't Save".
2. **Compare with today's files** (if any of these moved since `47f95a3`, use what is there):
   - `Graphs/WBP_Stage/EventGraph.Builder.txt`: `OnTextChanged(InputBox)` → `CleanText :In` → `WBP_ActionBuilder.SetLine :Text`. Part 3 takes this chain over.
   - `Graphs/WBP_Stage/SetPrompt.txt` ends with `(CallFunction|SyncAction)` then `(CallFunction|FitBuilder)`; its `CanType` block ends with `(if CanType (Widget|SetKeyboardFocus ...))`. `SetPrepMode.txt`: the `Prep` branch has the builder's `Close` and `FitBuilder`; the `else` branch ends with `StyleButton` on `SendButton`. Parts 2 and 4 add to both.
   - `Graphs/WBP_ActionBuilder/Refresh.txt` and `SetLine.txt` end with `SetText` on `PreviewText` from `_p`; `StyleAll.txt` sets `PreviewText`'s font from `(V MonoFont)`; `EventGraph.txt`'s `EventPreConstruct` sets a design-time sample. Part 6 rewrites these four.
   - How T64 replaced an `EventGraph` chain: part 2 wrote the new `OnTextChanged` chain with `write_graph_dsl`, and "the EventGraph's other 13 events kept their chains". Part 3d replaces that same chain.
3. `python Tools/check_prompts.py --offline` passes before you start. T65 changes no data file.
4. **The survey** (each item a separate `call_tool`, with `toolset_name` and `tool_name` as separate fields, T64; calls stop at about 120 s; save each read to `Saved/T65/<name>.read.txt`; never write a read-back to the editor):
   1. **`WBP_Stage`'s tree** (the UMG toolset): `RootBox` is the root, an Overlay, filling the window (T27, T38-build E5), and is a variable (turn `bIsVariable` on if not). `LowerBox`'s children: expected `ChatSize`, `TypingText`, `VoteRow`, `ActionBuilder`, `InputRow` (T64 part 2). `InputRow`'s children in order with their slot paddings (`WrapWidgets` drops them, T28): expected `InputStack`, `SendButton`, `PassButton`, `ContinueButton`, `StartButton` (T38's `ChatButton` isn't built yet). `InputBox`'s height in the designer or its style (part 5's pop-up sits on its top edge; any height works, since `AtPlace` reads the geometry).
   2. **Focus:** `IsFocusable` on every `Button` in `WBP_Stage` (T04, T33-1: all off is expected) and in `WBP_ActionBuilder` and `WBP_Chip` (T64: all off). Whether the info card (`InfoBox`, `InfoScroll`) or `LogScroll` can take focus (a `ScrollBox` normally can't). **T64 found that a click on a widget that can't take focus gives it to the game viewport**, so expect that for my card and the chat. List what can take focus for "## Findings" (step 3's check); `HoldFocus` (part 4) gives it back either way.
   3. **`InputBox`'s settings:** `ClearKeyboardFocusOnCommit` off (T04), and the value of `SelectAllTextWhenFocused` (must be off, or `CaretEnd`'s re-focus and `HoldFocus` would select the line).
   4. **`OnTextCommitted(InputBox)`** in `WBP_Stage`'s EventGraph (`find_nodes` for event nodes, full class paths, T30): does it call `SubmitInput` only when `CommitMethod` is `OnEnter`? If it calls it on every commit, a lost focus would send the line: then add that check to the chain (a `Switch` on `CommitMethod`, or an `==` with `OnEnter`), and write the chain to `Graphs/WBP_Stage/EventGraph.Commit.txt`. (T64 part 2 never lost the focus with text in the box, so it didn't see this either way.)
   5. **The override.** `OnPreviewKeyDown` is a `UserWidget` function that returns an `EventReply`, so it is a function override, not an event. Find how to make one through MCP, on a scratch Widget Blueprint first (`/Game/Scratch/WBP_KeyTest`, deleted after): `describe_toolset` on the Blueprint and UMG toolsets for an override or "implement function" tool; failing that, `write_graph_dsl` with `(fn OnPreviewKeyDown (MyGeometry InKeyEvent) ...)` and check that the graph shows as an override of the parent function (its entry has the parent's pins) and that it compiles. Write the way that worked under "Findings" (T61's Escape will need it too). **If no way works,** use part 5e's fallback.
   6. **Node names** with `find_node_types` (`context_pins: []`, T29), in `WBP_Stage`. **Don't use `get_node_type_pins` on a real graph:** it puts a node in it (T64 part 1). The names: `Utilities|Input|GetKey` (or the "Get Key" node on a Key Event), `Utilities|Key|GetKeyDisplayName`, `Widget|EventReply|Handled`, `Widget|EventReply|Unhandled`, `Widget|SlotAsOverlaySlot`, `Class|OverlaySlot|SetPadding` (`InPadding`), `Utilities|Struct|MakeMargin`, `Utilities|Geometry|LocalToAbsolute`, `Utilities|Geometry|AbsoluteToLocal`, `Utilities|Geometry|GetLocalSize`, `Widget|GetCachedGeometry`, `Widget|SetFocusToGameViewport`, `Utilities|Array|Contains`, `Utilities|String|Left`, `Utilities|String|GetSubstring`, `Utilities|String|RightChop`. Already confirmed by T64: `Math|Vector2D|BreakVector2D`, `Math|Integer|Max(Integer)`, `Math|Integer|Min(Integer)`, `Widget|SetText(TextBox)` (`InText`), `Widget|HasKeyboardFocus` (`WBP_Keys`), `Panel|AddChildtoWrapBox`, `Widget|Panel|ClearChildren`. The getters: `Class|WBPActionBuilder|GetMonoFont` on `ActionBuilder`, and `Class|BPShow|GetSeatLabel` (works, T64), `GetOnStage`, `GetHumanSeat`, `GetMaxWords` with `:self`. Each variable must not be Private. **If `GetMonoFont` isn't offered,** add a `MonoFont` variable to `WBP_Stage` with the builder's default (`/Engine/EngineFonts/DroidSansMono`, typeface `Default`, size 18) and have `Mono()` return it. If a name differs, use the real one below.
   7. **Key names:** add a temporary `(print (cat "NHOS: KEY " _key))` to the override in part 5d and press Enter, Tab, Escape, Up and Down once in PIE (or with the Slate inspector's key action, item 8). Expected: `Enter`, `Tab`, `Escape`, `Up`, `Down`. Use what prints in `SpeechKey`, then remove the print.
   8. **The Slate inspector's keys:** T64 found that its `PressKey` sends no characters to a text box (and its `Type` does). Check, with item 7's print, whether `PressKey` still reaches `OnPreviewKeyDown` for Enter, Tab, Escape, Up, Down and Backspace. Part 7 needs it. If it doesn't, part 7 calls `WBP_Stage.SpeechKey("<key>")` on the PIE widget through MCP for each key (the way T64 called `BuilderTurn` and `SetPhase` from editor Python), and the Findings say the keys themselves weren't pressed. A Backspace can then be made with `SetText` of the line one letter shorter, which runs the same change chain.

## 1. The order of the build

1. Part 0.
2. `WBP_Word` (part 6a): tree, `Setup`, compile, save.
3. `WBP_ActionBuilder` (part 6b): the tree change, the variables, `MakeWord`, `MakeWords`, `TryLabel`, `MatchLabel`, `PutWord`, `DrawToken`, `DrawPreview` (create every function and its parameters first, compile, then write the graphs callee first: T18, T54), then the rewrites of `Refresh`, `SetLine`, `StyleAll` and the event graph. Compile with warnings as errors, save.
4. `WBP_Stage`: the tree (parts 2a and 5a), the variables, every new function with its parameters (empty), compile; then the graphs callee first: `Mono`, `ShowRef`, `MaxWords`, `ReadNames`, `LastToken`, `IsMention`, `CountWords`, `CutWords`, `SyncCount`, `CaretEnd`, `AtLists`, `AtPlace`, `AtEntry`, `AtShow`, `AtDraw`, `AtFollow`, `AtMove`, `AtPick`, `UnitBackspace`, `SpeechApply`, `SpeechChanged`, `SpeechKey`, `HoldFocus`; then the override `OnPreviewKeyDown`; then `SetPrompt` and `SetPrepMode` from their files; then the event graph chains. Compile with warnings as errors, save. Close every game window before you save (T53).
5. The check (part 7).

**The DSL's `if` rule (T30):** an `if` with no `return`, after an earlier `(if ... (return))`, doesn't join the code after it. Every function below keeps to it: after an early return, each later `if` ends in `return`, uses `else`, or is the last statement.

**Before you change a function's parameters** (here only `WBP_Word.Setup` is new; nothing existing gains a parameter), find every call node to it, live or dead (T63: stale chains left by `write_graph_dsl` fail the compile).

## 2. The counter (steps 1 and 2)

### 2a. The widget tree

Insert into `InputRow`, right after `InputStack` and before `SendButton`:

```
CountSize       SizeBox; WidthOverride 72; slot: VAlign Center, padding left = SendButton's left padding (survey 1; T28: 10)
└ CountPill     Border; padding 8 left and right, 2 top and bottom; HAlign Center
  └ WordCount   TextBlock; text "0/15"; justify Center
```

- `bIsVariable` on for `CountSize`, `CountPill` and `WordCount`.
- 72 px holds "15/15" in the mono font at 18 pt (about 5 × 11 px) with the pill's padding, so the field doesn't shift as the count grows.
- **The field pays for it.** At 1080 (my scene turns) there is room. At 640 (Free Talk, the last word, the vote, the reactions) the row is the field, the counter, Action! and Pass, and after T66 also the timer's 72 px. Part 7 step 10 checks the field there.
- **T66's timer goes last in `InputRow`** (the spec: "12/15 [Action!] 0:21"), after `PassButton` and the collapsed `ContinueButton` and `StartButton`. T65 adds nothing for it.

### 2b. `Mono` and `SyncCount` (new)

`Graphs/WBP_Stage/Mono.txt` (output `Font`: Slate Font Info):

```lisp
; T65: the mono font of the speech row (the counter; T66's timer), the builder's own MonoFont (T64: UIStyle has no
; "Mono" role yet). If T34 adds one to UIStyle, this one line reads UIFont "Mono" instead.
(fn Mono ()
  (return (Class|WBPActionBuilder|GetMonoFont :self (Variables|WBP_Stage|GetActionBuilder))))
```

`Graphs/WBP_Stage/SyncCount.txt` (inputs `N`, `Max`: Integer):

```lisp
; T65: the counter right of the speech field: "12/15" in the mono font, quiet. At the cap, a red pill with white text:
; UIStyle's Red is a fill ("fill, white text"), and red text on the ink panel would be only about 3:1.
(fn SyncCount (N Max)
  (bind _full (>= N Max))
  (bind fMono (CallFunction|Mono))
  (bind cRed (Class|UIStyle|UIColor :Role "Red"))
  (bind cText (Class|UIStyle|UIColor :Role "Text"))
  (bind cQuiet (Class|UIStyle|UIColor :Role "Quiet"))
  (bind r (Class|UIStyle|UISize :Role "ButtonRadius"))
  (bind clear (Utilities|Struct|MakeLinearColor 0.0 0.0 0.0 0.0))
  (bind fill (select _full cRed clear))
  (bind bPill (Class|UIStyle|Brush :Fill fill :Outline fill :Width 0.0 :Radius r))
  (Class|Border|SetBrushColor :self (Variables|WBP_Stage|GetCountPill) :BrushColor (Utilities|Struct|MakeLinearColor 1.0 1.0 1.0 1.0))
  (Appearance|SetBrush :self (Variables|WBP_Stage|GetCountPill) :InBrush bPill)
  (Class|Text|SetFont :self (Variables|WBP_Stage|GetWordCount) :Font fMono)
  (Class|Text|SetColorandOpacity :self (Variables|WBP_Stage|GetWordCount) :ColorAndOpacity (Utilities|Struct|MakeSlateColor :SpecifiedColor (select _full cText cQuiet)))
  (Class|Text|SetText :self (Variables|WBP_Stage|GetWordCount) :Text (Utilities|Text|ToText(String) (cat (str N) "/" (str Max)))))
```

`SpeechApply` calls it on every change, and `SetPrepMode(false)` once before the first turn (2c). The node names are `WBP_ActionBuilder.StyleAll`'s and `StyleClapper`'s (T64, T53).

### 2c. `SetPrepMode` (rewrite from today's file)

Add one line to the `Prep` branch and four to the `else` branch of `Graphs/WBP_Stage/SetPrepMode.txt`, and nothing else:

- In the `Prep` branch, after `(Widget|SetVisibility :self (Variables|WBP_Stage|GetPassButton) :InVisibility "Collapsed")` (before T64's `Close` and `FitBuilder` lines):

```lisp
    (Widget|SetVisibility :self (Variables|WBP_Stage|GetCountSize) :InVisibility "Collapsed")
```

- In the `else` branch, after its last line, `(Class|UIStyle|StyleButton :Button (Variables|WBP_Stage|GetSendButton) :Label (Variables|WBP_Stage|GetSendLabel) :Kind "Primary")`:

```lisp
      (Widget|SetVisibility :self (Variables|WBP_Stage|GetCountSize) :InVisibility "HitTestInvisible")
      (bind _n0 (CallFunction|CountWords :Text (Utilities|String|ToString(Text) (Class|TextBox|GetText :self (Variables|WBP_Stage|GetInputBox)))))
      (bind _m0 (CallFunction|MaxWords))
      (CallFunction|SyncCount :N _n0 :Max _m0)
```

and the header comment `; T65: the word counter shows with Action! and Pass, and hides in Scene Prep.` Commit the whole function to `Graphs/WBP_Stage/SetPrepMode.txt`.

## 3. The 15-word cap and the change chain (steps 2 and 5)

### 3a. New variables in `WBP_Stage`

| Variable | Type | Default | Used by |
|---|---|---|---|
| `Show`, `NullShow` | `BP_Show` object reference | none (`NullShow` is never set: T64's `NullDir` and `NullWidget` pattern) | `ShowRef` |
| `PrevText`, `NewText`, `AtToken`, `TmpLab`, `TmpFound` | String | "" | the speech functions |
| `AllLabels`, `LiveLabels`, `AtNames`, `TmpWords`, `TmpLabels` | String array | empty | the speech functions |
| `TmpOn` | Integer array | empty | `ReadNames` |
| `MySeat` | Integer | -1 | `ReadNames` |
| `AtOpen`, `FocusAsked`, `CaretRefocus` | Boolean | false | parts 4 and 5 |
| `AtSel`, `TmpK` | Integer | 0 | part 5 |
| `AtPos`, `AtShutPos` | Integer | -1 | part 5 |
| `AtBtns` | `Button` object reference array | empty | `AtEntry` |
| `AtLbls` | `TextBlock` object reference array | empty | `AtEntry` |
| `AtBars` | `Border` object reference array | empty | `AtEntry` |

T64 added `LastBlock`, `FitOn`, `LowerWide`, `LowerWideBuild`, `ChatTall`, `ChatMin` and `LastChat` to `WBP_Stage`; none of these names clash.

### 3b. The helpers

`Graphs/WBP_Stage/ShowRef.txt`:

```lisp
; T65: BP_Show, found once and kept (the StartButton chain's GetActorOfClass; the builder's OpenTurn sets its own Show
; the same way, with no cast).
(fn ShowRef ()
  (if (== (V Show) (V NullShow))
    (set Show (Actor|GetActorOfClass :ActorClass "/Game/NHOS/Core/BP_Show.BP_Show_C")))
  (return (V Show)))
```

`Graphs/WBP_Stage/MaxWords.txt`:

```lisp
; T65: the cap on a line, from BP_Show (T59's MaxWords, 15, which CapWords reads), so the counter and CapWords never
; differ. 15 with no show.
(fn MaxWords ()
  (bind _sh (CallFunction|ShowRef))
  (if (== _sh (V NullShow))
    (return 15))
  (return (Class|BPShow|GetMaxWords :self _sh)))
```

`Graphs/WBP_Stage/ReadNames.txt`:

```lisp
; T65: the names on my screen (BP_Show.SeatLabel, "Meta") of every seat but mine: AllLabels for every seat, LiveLabels only
; for the seats still on stage (OnStage), in seat order. Read on every change, so a cut shows at once.
(fn ReadNames ()
  (clear (V AllLabels))
  (clear (V LiveLabels))
  (bind _sh (CallFunction|ShowRef))
  (if (== _sh (V NullShow))
    (return))
  (set TmpLabels (Class|BPShow|GetSeatLabel :self _sh))
  (set TmpOn (Class|BPShow|GetOnStage :self _sh))
  (set MySeat (Class|BPShow|GetHumanSeat :self _sh))
  (for _i (range (len (V TmpLabels)))
    (set TmpK _i)
    (set TmpLab (get (V TmpLabels) (V TmpK)))
    (if (and (!= (V TmpK) (V MySeat)) (not (Utilities|String|IsEmpty (V TmpLab))))
      (add (V AllLabels) (V TmpLab))
      (if (Utilities|Array|Contains (V TmpOn) (V TmpK))
        (add (V LiveLabels) (V TmpLab))))))
```

- The loop values are variables, not binds (T51, T58-build).
- `OnStage` holds seat numbers (`StartLastWords` walks it as seats: `(get (V SeatName) _s)`). A test show with `ai_seats` 3 has an empty label for the unused seat; the `IsEmpty` check skips it.

`Graphs/WBP_Stage/LastToken.txt` (outputs `Token`: String, `Pos`: Integer):

```lisp
; T65: the word at the end of the line, where the caret is while I type, and the index it starts at. "" when the line
; ends in a space.
(fn LastToken (Text)
  (bind (_l _r _found) (Utilities|String|Split :SourceString Text :InStr " " :SearchDir "FromEnd"))
  (if _found
    (return _r (+ (Utilities|String|Len _l) 1)))
  (return Text 0))
```

`Split`'s form is `BPC_LLMClient`'s and `BP_StageDirector`'s.

`Graphs/WBP_Stage/IsMention.txt`:

```lisp
; T65: true when Token is a whole mention: "@" and the screen name of a seat other than mine, in any case ("@meta").
(fn IsMention (Token)
  (set TmpFound "")
  (for _l (V AllLabels)
    (set TmpLab _l)
    (if (Utilities|String|Equal,CaseInsensitive(String) :A Token :B (cat "@" (V TmpLab)))
      (set TmpFound (V TmpLab))))
  (return (not (Utilities|String|IsEmpty (V TmpFound)))))
```

`Graphs/WBP_Stage/CountWords.txt`:

```lisp
; T65: the words in a line as BP_Show.CapWords counts them (T59): split on spaces, "Player 3" one word, so a mention
; ("@Meta," or, once resolved, "@Player 5") is one word. Keep it in step with CapWords.
(fn CountWords (Text)
  (set TmpWords (Utilities|String|ParseIntoArray (Utilities|String|Replace (Utilities|String|Trim (Utilities|String|TrimTrailing Text)) "Player " "Player~")))
  (return (len (V TmpWords))))
```

`Graphs/WBP_Stage/CutWords.txt` (inputs `Text`: String, `Max`: Integer):

```lisp
; T65: a line over the cap becomes its first Max words and one space (decision 7), so the next letter is refused too
; instead of growing the last word. A line within the cap comes back as it is.
(fn CutWords (Text Max)
  (set TmpWords (Utilities|String|ParseIntoArray (Utilities|String|Replace (Utilities|String|Trim (Utilities|String|TrimTrailing Text)) "Player " "Player~")))
  (if (<= (len (V TmpWords)) Max)
    (return Text))
  (Utilities|Array|Resize (V TmpWords) Max)
  (return (cat (Utilities|String|Replace (Utilities|String|JoinStringArray (V TmpWords)) "Player~" "Player ") " ")))
```

- `ParseIntoArray` and `JoinStringArray` with their default space are `CapWords.txt`'s forms (checked at `47f95a3`: `CapWords` trims, swaps "Player " for "Player~", splits, and resizes to `MaxWords`).
- `CapWords` also turns line breaks into spaces (its `NL`). A single-line editable text box can't hold a line break, so these two skip that.

`Graphs/WBP_Stage/CaretEnd.txt`:

```lisp
; T65: after the game sets the field's text (a cut or a picked name), the caret goes to the end of the line. Slate keeps
; the caret where it was on SetText; on a keyboard focus it moves it to the end. CaretRefocus is set from part 7's
; caret test: false if the caret is already at the end after SetText, true if it needs the re-focus.
(fn CaretEnd ()
  (if (not (V CaretRefocus))
    (return))
  (Widget|SetFocusToGameViewport)
  (Widget|SetKeyboardFocus :self (Variables|WBP_Stage|GetInputBox)))
```

The re-focus commits the text with a focus method, not `OnEnter`, so it sends nothing (survey 4 checks that `SubmitInput` runs on Enter only).

### 3c. The change chain

`Graphs/WBP_Stage/SpeechChanged.txt`:

```lisp
; T65: every change to the speech field (OnTextChanged on InputBox, T64's chain). PrevText is set before any SetText the
; game makes, so the change that SetText fires itself comes back here equal to PrevText and does nothing.
(fn SpeechChanged (Text)
  (if (streq Text (V PrevText))
    (return))
  (CallFunction|SpeechApply :Text Text))
```

`Graphs/WBP_Stage/SpeechApply.txt`:

```lisp
; T65: a real change, in order: a Backspace right after a mention removes the whole mention (step 5); a 16th word is refused
; and a paste over the cap is cut (step 2); then the counter, the @ list (step 4) and T64's preview line follow the line.
(fn SpeechApply (Text)
  (set NewText Text)
  (CallFunction|ReadNames)
  (CallFunction|UnitBackspace)
  (bind _max (CallFunction|MaxWords))
  (bind _n (CallFunction|CountWords :Text (V NewText)))
  (if (> _n _max)
    (bind _cut (CallFunction|CutWords :Text (V NewText) :Max _max))
    (set NewText _cut)
    (print (cat "NHOS: SPEECH cap words=" (str _n) " -> " (str _max))))
  (set PrevText (V NewText))
  (if (not (streq (V NewText) Text))
    (Widget|SetText(TextBox) :self (Variables|WBP_Stage|GetInputBox) :InText (Utilities|Text|ToText(String) (V NewText)))
    (CallFunction|CaretEnd))
  (bind _n2 (CallFunction|CountWords :Text (V NewText)))
  (CallFunction|SyncCount :N _n2 :Max _max)
  (CallFunction|AtFollow)
  (bind _clean (CallFunction|CleanText :In (V NewText)))
  (Class|WBPActionBuilder|SetLine :self (Variables|WBP_Stage|GetActionBuilder) :Text _clean))
```

- No `if` here returns, so each joins the next (T01).
- `Widget|SetText(TextBox)` with `InText` is `SubmitInput`'s form. UMG fires `OnTextChanged` for a text the game sets too; `SpeechChanged`'s first check stops that second pass.
- **The last two lines are T64's chain** (`EventGraph.Builder.txt`): `CleanText`'s input is `In`, and the preview gets the cleaned line.
- After a send, `SubmitInput` clears the box with `SetText("")`: that change comes here with "", so the counter reads "0/15", the list closes, and the builder's `SetLine` ignores it (T64: `Sent`). When `SubmitInput` is blocked (`NHOS: BUILDER blocked`), it keeps the text, so nothing changes here.

`Graphs/WBP_Stage/UnitBackspace.txt`:

```lisp
; T65: a mention goes in as one unit, "@Meta " (step 5). One Backspace right after it, at the end of the line, removes the
; whole mention: the space after it (the line now ends in "@Meta") or its last letter (the line now ends in "@Met").
; Any other change is left alone.
(fn UnitBackspace ()
  (bind _one (and (== (Utilities|String|Len (V NewText)) (- (Utilities|String|Len (V PrevText)) 1)) (Utilities|String|StartsWith :SourceString (V PrevText) :InPrefix (V NewText) :SearchCase "CaseSensitive")))
  (if (not _one)
    (return))
  (bind (_tok _pos) (CallFunction|LastToken :Text (V NewText)))
  (bind (_ptok _ppos) (CallFunction|LastToken :Text (V PrevText)))
  (bind _a (CallFunction|IsMention :Token _tok))
  (bind _b (CallFunction|IsMention :Token _ptok))
  (bind _sp (Utilities|String|EndsWith :SourceString (V PrevText) :InSuffix " "))
  (if (or (and _sp _a) (and _b (not _sp)))
    (print (cat "NHOS: MENTION removed " (select _a _tok _ptok)))
    (set NewText (Utilities|String|Left :SourceString (V NewText) :Count _pos))))
```

- `StartsWith` ignores case by default; here it must not, so `:SearchCase "CaseSensitive"` (the enum's form as `Split` takes `"IgnoreCase"`).
- The first `if` returns; the second is the last statement (T30).
- `_pos` is where the last word of the new line starts, so `Left` keeps everything before the broken mention, the space before it included.

### 3d. The event graph: the change chain takes over T64's

Rewrite `Graphs/WBP_Stage/EventGraph.Builder.txt` (T64's file) as:

```lisp
; Only the speech field's chain of WBP_Stage's EventGraph (T64, T65). The rest of EventGraph has no source here.
; write_graph_dsl keeps the event chains it doesn't name, so this writes only this one.
; Every change to the speech field goes to SpeechChanged: the mention unit, the 15-word cap, the counter, the @ list,
; then T64's preview line (CleanText, WBP_ActionBuilder.SetLine).
(event OnTextChanged(InputBox) (Text)
  (CallFunction|SpeechChanged :Text (Utilities|String|ToString(Text) Text)))
```

Write it as T64 part 2 wrote its chain (`write_graph_dsl` with only this event named). If that adds a second `OnTextChanged` node instead of replacing the chain (a duplicate-event compile error), or leaves T64's `CleanText` and `SetLine` nodes cut off from the event, delete the old chain's nodes first (`find_nodes` on the event node) and write again.

## 4. Focus stays in the speech field (step 3)

`Graphs/WBP_Stage/HoldFocus.txt` (input `CanType`: Boolean):

```lisp
; T65: the speech field holds the keyboard focus for my whole turn (step 3). While my input is open, anything that took the
; focus gives it back the next frame. A click on a widget that can't take focus hands it to the game viewport (T64), so
; this covers my card, the chat and the stage; the builder's own KeepFocus already covers its clicks.
; NHOS: FOCUS back prints once each time.
(fn HoldFocus (CanType)
  (bind _has (Widget|HasKeyboardFocus :self (Variables|WBP_Stage|GetInputBox)))
  (if _has
    (set FocusAsked false))
  (if (and CanType (not _has))
    (Widget|SetKeyboardFocus :self (Variables|WBP_Stage|GetInputBox))
    (if (not (V FocusAsked))
      (print "NHOS: FOCUS back"))
    (set FocusAsked true)))
```

- `HasKeyboardFocus` on the box is true while its inner text has the focus (`WBP_Keys` reads it that way every frame, T33).
- `FocusAsked` keeps the print to one line per loss, even if a frame's `SetKeyboardFocus` doesn't take (a game window in the background).
- **A later in-show widget that needs the keyboard** (a stagehand "Got it" button, T61; T33-1's focusable buttons, T34) must close my input first or be added here as an exception. Part 8 tells them.

**`SetPrompt`** (rewrite from today's file): two changes.

1. Inside the `(if (xor CanType (Variables|Default|GetLastCanType)) ...)` block, its last statement `(if CanType (Widget|SetKeyboardFocus :self (Variables|WBP_Stage|GetInputBox)))` becomes:

```lisp
    (if CanType
      (Widget|SetKeyboardFocus :self (Variables|WBP_Stage|GetInputBox))
      (else
        (CallFunction|AtDraw :Open false)))
```

   so the @ list closes when my input closes (the lines play, or I sent).

2. After the function's last line `(CallFunction|FitBuilder)`, add:

```lisp
  (CallFunction|HoldFocus :CanType CanType)
```

and the header comment `; T65: the speech field keeps the focus while I can type (HoldFocus); the @ list closes with my input.` Commit to `Graphs/WBP_Stage/SetPrompt.txt`. `UpdatePrompt` calls `SetPrompt` once a frame (T27), so `HoldFocus` runs once a frame: one `HasKeyboardFocus` call. The rest of `SetPrompt` (T64's `SetLive`, the `LastBlock` gate on `SendButton`, `SyncAction`, `FitBuilder`) stays as it is.

## 5. The @ list (step 4)

### 5a. The widget tree

Add to `RootBox` (the full-screen Overlay), as its **last** child, so it draws on top of the lower panel:

```
AtPop             Border; slot: HAlign Left, VAlign Bottom, padding set at run time (AtPlace); Collapsed at design time
└ AtList          VerticalBox
  ├ AtBtn0        Button; IsFocusable off; slot: padding bottom 4 (S1)
  │ └ AtRow0      HorizontalBox
  │   ├ AtBarSize0  SizeBox; WidthOverride 14, HeightOverride 20 (T64's swatch); slot: VAlign Center, padding right 8 (S2)
  │   │ └ AtBar0    Border (no padding)
  │   └ AtLbl0    TextBlock; text "@Meta"; slot VAlign Center
  ├ AtBtn1 … AtBtn3   the same, with 1 to 3 in each name (no bottom padding on AtBtn3)
```

- `AtPop` is a quiet ink panel, styled at run time: `StylePanel(AtPop, "Ink")` in `AtLists` (the call `StyleClapper` uses for its slate), with padding 8 (`S2`).
- `bIsVariable` on for `AtPop`, `AtBtn0` to `AtBtn3`, `AtBar0` to `AtBar3` and `AtLbl0` to `AtLbl3`.
- **Every `AtBtn` has `IsFocusable` off,** like T64's chips. A click on one still hands the focus to the game viewport (T64); `AtPick` ends with `CaretEnd`, and `HoldFocus` gives it back the next frame at the latest.
- Four buttons: five actors at most, never me. A test show with 4 actors uses three.
- `StageArea` is `RootBox`'s last child today, so the reveal stamp draws on top (T27). The stamp never shows while I can type, so `AtPop` goes after it.

### 5b. Drawing the list

`Graphs/WBP_Stage/AtLists.txt`:

```lisp
; T65: the @ list's four buttons as lists, made once, and its panel's look (UIStyle's ink panel, T32).
(fn AtLists ()
  (clear (V AtBtns))
  (clear (V AtLbls))
  (clear (V AtBars))
  (add (V AtBtns) (Variables|WBP_Stage|GetAtBtn0))
  (add (V AtBtns) (Variables|WBP_Stage|GetAtBtn1))
  (add (V AtBtns) (Variables|WBP_Stage|GetAtBtn2))
  (add (V AtBtns) (Variables|WBP_Stage|GetAtBtn3))
  (add (V AtLbls) (Variables|WBP_Stage|GetAtLbl0))
  (add (V AtLbls) (Variables|WBP_Stage|GetAtLbl1))
  (add (V AtLbls) (Variables|WBP_Stage|GetAtLbl2))
  (add (V AtLbls) (Variables|WBP_Stage|GetAtLbl3))
  (add (V AtBars) (Variables|WBP_Stage|GetAtBar0))
  (add (V AtBars) (Variables|WBP_Stage|GetAtBar1))
  (add (V AtBars) (Variables|WBP_Stage|GetAtBar2))
  (add (V AtBars) (Variables|WBP_Stage|GetAtBar3))
  (Class|UIStyle|StylePanel :Panel (Variables|WBP_Stage|GetAtPop) :Look "Ink"))
```

`Graphs/WBP_Stage/AtPlace.txt`:

```lisp
; T65: puts the @ list right over the speech field, in RootBox's space (the full-screen Overlay, T27): its left edge on the
; field's, its bottom 8 px (S2) above the field's top. AtPop's slot is HAlign Left, VAlign Bottom, so its height can change.
; The field moves when the panel widens for the builder (T64's FitBuilder), so this runs at each opening and redraw.
(fn AtPlace ()
  (bind _g (Widget|GetCachedGeometry :self (Variables|WBP_Stage|GetInputBox)))
  (bind _rg (Widget|GetCachedGeometry :self (Variables|WBP_Stage|GetRootBox)))
  (bind _tl (Utilities|Geometry|AbsoluteToLocal _rg (Utilities|Geometry|LocalToAbsolute _g (Math|Vector2D|MakeVector2D :X 0.0 :Y 0.0))))
  (bind _view (Utilities|Geometry|GetLocalSize _rg))
  (bind _gap (Class|UIStyle|UISize :Role "S2"))
  (bind (_x _y) (Math|Vector2D|BreakVector2D _tl))
  (bind (_vx _vy) (Math|Vector2D|BreakVector2D _view))
  (bind _slot (Widget|SlotAsOverlaySlot (Variables|WBP_Stage|GetAtPop)))
  (Class|OverlaySlot|SetPadding :self _slot :InPadding (Utilities|Struct|MakeMargin :Left _x :Top 0.0 :Right 0.0 :Bottom (+ (- _vy _y) _gap))))
```

The geometry forms are T38-build's `AddKeep` (`GetCachedGeometry`, `LocalToAbsolute`, `AbsoluteToLocal`, `GetLocalSize`); survey 6 confirms each name. The field's place doesn't change while the list is open (a header, which can widen or narrow the panel, never comes while I type), so placing it once per opening and on each redraw is enough.

`Graphs/WBP_Stage/AtEntry.txt` (input `K`: Integer):

```lisp
; T65: one entry of the @ list: the K-th match, with its seat-color swatch (ink outline, so lime and pale blue show on paper)
; and "@Name". The highlighted entry is paper, the others plum (T64's chips). Past the matches, collapsed.
(fn AtEntry (K)
  (bind _b (get (V AtBtns) K))
  (bind _l (get (V AtLbls) K))
  (bind _f (get (V AtBars) K))
  (if (>= K (len (V AtNames)))
    (Widget|SetVisibility :self _b :InVisibility "Collapsed")
    (return))
  (bind _name (get (V AtNames) K))
  (Class|UIStyle|StyleButton :Button _b :Label _l :Kind (select (== K (V AtSel)) "Paper" "Secondary"))
  (Class|Text|SetText :self _l :Text (Utilities|Text|ToText(String) (cat "@" _name)))
  (bind cQuiet (Class|UIStyle|UIColor :Role "Quiet"))
  (bind cBar (Class|UIStyle|SeatColor :Name _name :Fallback cQuiet))
  (bind cInk (Class|UIStyle|UIColor :Role "InkSolid"))
  (bind trim (Class|UIStyle|UISize :Role "PanelTrim"))
  (bind rad (Class|UIStyle|UISize :Role "S1"))
  (bind bBar (Class|UIStyle|Brush :Fill cBar :Outline cInk :Width trim :Radius rad))
  (Class|Border|SetBrushColor :self _f :BrushColor (Utilities|Struct|MakeLinearColor 1.0 1.0 1.0 1.0))
  (Appearance|SetBrush :self _f :InBrush bBar)
  (Widget|SetVisibility :self _b :InVisibility "Visible"))
```

The swatch is `WBP_Chip.Setup`'s, line for line (checked at `47f95a3`). `(get (V AtNames) K)` runs only once `K` is known to be in range.

`Graphs/WBP_Stage/AtShow.txt` (input `Fresh`: Boolean):

```lisp
; T65: shows the list with the current matches. A fresh list highlights the first match.
(fn AtShow (Fresh)
  (if (== (len (V AtBtns)) 0)
    (CallFunction|AtLists))
  (if Fresh
    (set AtSel 0))
  (set AtSel (Math|Integer|Max(Integer) 0 (Math|Integer|Min(Integer) (V AtSel) (- (len (V AtNames)) 1))))
  (for _k (range 4)
    (set TmpK _k)
    (CallFunction|AtEntry :K (V TmpK)))
  (CallFunction|AtPlace)
  (Widget|SetVisibility :self (Variables|WBP_Stage|GetAtPop) :InVisibility "SelfHitTestInvisible")
  (if Fresh
    (print (cat "NHOS: MENTION open " (Utilities|String|JoinStringArray (V AtNames) ",")))))
```

`Graphs/WBP_Stage/AtDraw.txt` (input `Open`: Boolean):

```lisp
; T65: opens, redraws or closes the @ list.
(fn AtDraw (Open)
  (bind _was (V AtOpen))
  (set AtOpen Open)
  (if Open
    (CallFunction|AtShow :Fresh (not _was))
    (else
      (Widget|SetVisibility :self (Variables|WBP_Stage|GetAtPop) :InVisibility "Collapsed")
      (if _was
        (print "NHOS: MENTION close")))))
```

### 5c. The list follows the line, and the picks

`Graphs/WBP_Stage/AtFollow.txt`:

```lisp
; T65: the @ list follows the word at the end of the line (decision 4). It is open while that word starts with "@", my
; input is open, and an actor still on stage (never me) has a screen name that starts with the letters after the "@", in
; any case. Escape keeps it shut until another "@" word (AtShutPos).
(fn AtFollow ()
  (bind (_tok _pos) (CallFunction|LastToken :Text (V NewText)))
  (set AtToken _tok)
  (set AtPos _pos)
  (clear (V AtNames))
  (bind _at (Utilities|String|StartsWith :SourceString _tok :InPrefix "@"))
  (bind _key (Utilities|String|RightChop :SourceString _tok :Count 1))
  (if (not _at)
    (set AtShutPos -1))
  (if _at
    (for _l (V LiveLabels)
      (set TmpLab _l)
      (if (or (Utilities|String|IsEmpty _key) (Utilities|String|StartsWith :SourceString (V TmpLab) :InPrefix _key))
        (add (V AtNames) (V TmpLab)))))
  (bind _open (and (> (len (V AtNames)) 0) (and (V LastCanType) (!= _pos (V AtShutPos)))))
  (CallFunction|AtDraw :Open _open))
```

- **`StartsWith` with an empty prefix is false in UE** (`FString::StartsWith`), so "@" alone takes the `IsEmpty` side and lists everyone.
- `LastCanType` is `SetPrompt`'s (T30; `SetPrompt` reads it as `Variables|Default|GetLastCanType`, which `(V LastCanType)` expands to), so the list never opens while the lines play.
- No `if` returns, so each joins the next.

`Graphs/WBP_Stage/AtMove.txt` (input `Step`: Integer):

```lisp
; T65: Up (-1) and Down (+1) move the highlight in the open list, round the ends.
(fn AtMove (Step)
  (if (not (V AtOpen))
    (return))
  (bind _n (len (V AtNames)))
  (bind _s (+ (V AtSel) Step))
  (set AtSel (select (< _s 0) (- _n 1) (select (>= _s _n) 0 _s)))
  (CallFunction|AtShow :Fresh false))
```

`Graphs/WBP_Stage/AtPick.txt` (input `K`: Integer):

```lisp
; T65: puts the K-th name in: the "@me" at the end of the line becomes "@Meta " (one unit, step 5), with the caret at the
; end. SetText runs the change chain, which closes the list (the line now ends in a space) and counts the words.
(fn AtPick (K)
  (if (or (not (V AtOpen)) (>= K (len (V AtNames))))
    (return))
  (bind _name (get (V AtNames) K))
  (bind _head (Utilities|String|Left :SourceString (V PrevText) :Count (V AtPos)))
  (bind _max (CallFunction|MaxWords))
  (bind _new (CallFunction|CutWords :Text (cat _head "@" _name " ") :Max _max))
  (print (cat "NHOS: MENTION pick " _name))
  (set AtShutPos -1)
  (Widget|SetText(TextBox) :self (Variables|WBP_Stage|GetInputBox) :InText (Utilities|Text|ToText(String) _new))
  (CallFunction|CaretEnd))
```

- `PrevText` is the field's text (set by `SpeechApply`), and `AtPos` is where the "@" word starts.
- The cap can't break here: "@me" already counted as a word, and "@Meta" is still one.

### 5d. The keys: `SpeechKey` and the `OnPreviewKeyDown` override

`Graphs/WBP_Stage/SpeechKey.txt` (input `Key`: String; output Boolean):

```lisp
; T65: the keys the speech field needs (step 4), by name. True means Handled: the key stops here. While the @ list is open,
; Enter and Tab put the highlighted name in (Enter doesn't send), Escape closes it. Up and Down move in the list, and are
; always Handled, like Tab, so no key moves the focus off the field (by default Tab moves it to the next widget, T31's note).
; OnPreviewKeyDown calls this; part 7 may call it through MCP.
(fn SpeechKey (Key)
  (bind _focus (Widget|HasKeyboardFocus :self (Variables|WBP_Stage|GetInputBox)))
  (if (not _focus)
    (return false))
  (if (and (V AtOpen) (or (streq Key "Enter") (streq Key "Tab")))
    (CallFunction|AtPick :K (V AtSel))
    (return true))
  (if (and (V AtOpen) (streq Key "Escape"))
    (set AtShutPos (V AtPos))
    (CallFunction|AtDraw :Open false)
    (return true))
  (if (streq Key "Up")
    (CallFunction|AtMove :Step -1)
    (return true))
  (if (streq Key "Down")
    (CallFunction|AtMove :Step 1)
    (return true))
  (return (streq Key "Tab")))
```

- Use the key names survey 7 printed if they differ.
- Enter with the list closed is unhandled, so the box commits it and `SubmitInput` runs, as now: T64's `Blocks` gate prints `NHOS: BUILDER blocked` on an unfinished action, and otherwise the line (or an empty No action) goes.
- Escape with the list closed is unhandled, as now.

The override, `OnPreviewKeyDown` (made the way survey 5 found):

```lisp
; T65: WBP_Stage sees each key before the speech field does (a preview event tunnels down to the focused widget).
; SpeechKey decides; Handled stops the key here.
(fn OnPreviewKeyDown (MyGeometry InKeyEvent)
  (bind _key (Utilities|String|ToString(Text) (Utilities|Key|GetKeyDisplayName (Utilities|Input|GetKey InKeyEvent))))
  (bind _h (CallFunction|SpeechKey :Key _key))
  (if _h
    (return (Widget|EventReply|Handled)))
  (return (Widget|EventReply|Unhandled)))
```

Commit it as `Graphs/WBP_Stage/OnPreviewKeyDown.txt`. If the override's entry names its pins differently, use its names.

### 5e. If no override can be made (survey 5's fallback)

Keep everything above but the override, and catch what the box itself reports:

- **Enter:** in the `OnTextCommitted(InputBox)` chain, before `SubmitInput`: if `AtOpen`, call `AtPick(AtSel)` instead and don't send. Write the chain as `Graphs/WBP_Stage/EventGraph.Commit.txt`.
- **Tab and Escape** reach the box as a commit with a focus method (`OnUserMovedFocus` or `OnCleared`): with the list open, pick (Tab) or close (Escape) there; `HoldFocus` gives the focus back the next frame, and `CaretEnd` puts the caret at the end.
- **Up and Down** can't be caught: the first match is the one Enter and Tab pick, and "@" plus a letter or two narrows the list to one name (all four screen names start differently).
- Write under "Findings" which keys work.

### 5f. The clicks

Bind each `AtBtn`'s `OnClicked` with `UMGToolSet.BindToEventProperty` (T04), then write `Graphs/WBP_Stage/EventGraph.Mentions.txt`:

```lisp
; Only the @ list's chains of WBP_Stage's EventGraph (T65). A click on a name puts it in, as Enter or Tab would.
(event OnClicked(AtBtn0)
  (CallFunction|AtPick :K 0))

(event OnClicked(AtBtn1)
  (CallFunction|AtPick :K 1))

(event OnClicked(AtBtn2)
  (CallFunction|AtPick :K 2))

(event OnClicked(AtBtn3)
  (CallFunction|AtPick :K 3))
```

`write_graph_dsl` keeps the chains it doesn't name (`EventGraph.StartButton.txt`'s note), so this leaves `StartButton`, `OnTextCommitted`, the change chain and the other events alone.

## 6. A mention is a chip in the preview line (step 5)

**Why a fallback:** UMG's `EditableTextBox` holds plain text only; no editable text widget in UMG can hold an inline widget, and a `RichTextBlock` can't draw a chip without a C++ decorator (the project has no C++). So, as the task says: the field gets "@Meta " as one unit (part 3, `UnitBackspace`), and the chip is drawn in T64's preview line. Write this under "## Findings".

### 6a. `WBP_Word` (new)

`Content/NHOS/UI/WBP_Word.uasset`, made with `UMGToolSet.CreateWidgetBlueprint` (T04, T64). Outside T65's Touches; the commit message names it.

```
WordBox     Border (root); no padding; HAlign Left, VAlign Center
└ WordText  TextBlock; text "word "
```

`bIsVariable` on for both. Function `Setup(Text, Chip, Fill, Font)` (`Text`: String; `Chip`: Boolean; `Fill`: Linear Color; `Font`: Slate Font Info). `Graphs/WBP_Word/Setup.txt`:

```lisp
; WBP_Word.Setup(Text, Chip, Fill, Font), called by WBP_ActionBuilder.PutWord (T65). One piece of the preview line, in the
; builder's mono font (its MonoFont, passed in as Font): a plain word white on nothing; a mention a chip filled with the
; actor's seat color, ink text, round corners (ink on the four seat colors is 5.8:1 at the lowest, Meta's blue).
(fn Setup (Text Chip Fill Font)
  (bind cText (Class|UIStyle|UIColor :Role "Text"))
  (bind cInk (Class|UIStyle|UIColor :Role "InkSolid"))
  (bind rad (Class|UIStyle|UISize :Role "S1"))
  (bind clear (Utilities|Struct|MakeLinearColor 0.0 0.0 0.0 0.0))
  (bind fill (select Chip Fill clear))
  (bind bChip (Class|UIStyle|Brush :Fill fill :Outline fill :Width 0.0 :Radius rad))
  (bind pad (select Chip 4.0 0.0))
  (Class|Border|SetBrushColor :self (Variables|WBP_Word|GetWordBox) :BrushColor (Utilities|Struct|MakeLinearColor 1.0 1.0 1.0 1.0))
  (Appearance|SetBrush :self (Variables|WBP_Word|GetWordBox) :InBrush bChip)
  (Class|Border|SetPadding :self (Variables|WBP_Word|GetWordBox) :InPadding (Utilities|Struct|MakeMargin :Left pad :Top 0.0 :Right pad :Bottom 0.0))
  (Class|Text|SetFont :self (Variables|WBP_Word|GetWordText) :Font Font)
  (Class|Text|SetColorandOpacity :self (Variables|WBP_Word|GetWordText) :ColorAndOpacity (Utilities|Struct|MakeSlateColor :SpecifiedColor (select Chip cInk cText)))
  (Class|Text|SetText :self (Variables|WBP_Word|GetWordText) :Text (Utilities|Text|ToText(String) Text)))
```

`Class|Border|SetPadding` is used in the pushed sources; `MakeMargin`'s name is survey 6's. Compile with warnings as errors, save.

### 6b. `WBP_ActionBuilder` changes

**The tree:** in `PreviewBox` (Border, padding 12/8), replace T64's `PreviewText` (TextBlock) with:

```
PreviewWrap   WrapBox; InnerSlotPadding (0, 2); slot: HAlign Fill. The words go here at run time (WBP_Word).
```

`bIsVariable` on. Delete `PreviewText` only after the four graphs that use it are rewritten (below), or the compile fails.

**New variables:** `Words` (`WBP_Word` object reference array), `Toks` (String array), `Tok`, `Found` (String, ""), `WordUsed`, `TmpK` (Integer, 0). T64's builder already has `Show`, `Names`, `Labels`, `Seat`, `TmpStr`, `TmpList` and `MonoFont`; none of the new names clash (check `TmpK` in the variable list).

**New functions** (`Graphs/WBP_ActionBuilder/`):

`MakeWord.txt`:

```lisp
; T65: one more word for the preview line's pool.
(fn MakeWord ()
  (bind _w (UserInterface|CreateWidget "/Game/NHOS/UI/WBP_Word.WBP_Word_C" (Widget|GetOwningPlayer self)))
  (Widget|SetVisibility :self _w :InVisibility "Collapsed")
  (Panel|AddChildtoWrapBox :self (Variables|WBP_ActionBuilder|GetPreviewWrap) :Content _w)
  (add (V Words) _w))
```

`MakeWords.txt`:

```lisp
; T65: the pool of 40 words for the preview line, made once: the longest preview is about 7 words of action and 15 of
; line, each mention split in up to three pieces.
(fn MakeWords ()
  (for _k (range 40)
    (CallFunction|MakeWord)))
```

`CreateWidget` and `Panel|AddChildtoWrapBox` are T64's `AddChip` forms (checked at `47f95a3`); the create is in its own function so no bind sits inside the loop (T51).

`TryLabel.txt` (inputs `Rest`: String, `K`: Integer):

```lisp
; T65: sets Found when Rest (what follows an "@") starts with seat K's screen name, in any case, at a word end: the next
; character is a space, , . ! ? ' : ; ) or " or nothing, the ends BP_Show.ResolveMentions accepts (T26). Never my seat.
(fn TryLabel (Rest K)
  (if (== K (V Seat))
    (return))
  (bind _lab (get (V Labels) K))
  (bind _nx (Utilities|String|GetSubstring :SourceString Rest :StartIndex (Utilities|String|Len _lab) :Length 1))
  (bind _end (or (Utilities|String|IsEmpty _nx) (Utilities|String|Contains :SearchIn " ,.!?':;)\"" :Substring _nx)))
  (if (and (not (Utilities|String|IsEmpty _lab)) (and _end (Utilities|String|StartsWith :SourceString Rest :InPrefix _lab)))
    (set Found _lab)))
```

`MatchLabel.txt` (input `Rest`: String; output String):

```lisp
; T65: the screen name a mention names, or "" (TryLabel for each seat).
(fn MatchLabel (Rest)
  (set Found "")
  (for _k (range (len (V Labels)))
    (set TmpK _k)
    (CallFunction|TryLabel :Rest Rest :K (V TmpK)))
  (return (V Found)))
```

`Labels` and `Seat` are T64's, set by `OpenTurn` at each scene turn (`Seat` from `ArmSeat`, `Labels` from `BP_Show.SeatLabel`). Before the first turn they are empty and `Seat` is -1, so nothing is a chip.

`PutWord.txt` (inputs `Text`, `Name`: String; `Chip`: Boolean):

```lisp
; T65: the next word of the pool shows Text, as a chip in Name's seat color or plain, in MonoFont. Empty text adds nothing.
(fn PutWord (Text Chip Name)
  (if (or (Utilities|String|IsEmpty Text) (>= (V WordUsed) (len (V Words))))
    (return))
  (bind _w (get (V Words) (V WordUsed)))
  (bind cQuiet (Class|UIStyle|UIColor :Role "Quiet"))
  (bind cSeat (Class|UIStyle|SeatColor :Name Name :Fallback cQuiet))
  (Class|WBPWord|Setup :self _w :Text Text :Chip Chip :Fill cSeat :Font (V MonoFont))
  (Widget|SetVisibility :self _w :InVisibility "HitTestInvisible")
  (set WordUsed (+ (V WordUsed) 1)))
```

`DrawToken.txt`:

```lisp
; T65: one word of the preview line (Tok). A word with a mention in it ("@Meta,", "\"@meta") becomes what's before the "@"
; (plain), the chip ("@Meta", the screen name's own capitals), and what's after the name plus a space (plain). Any other
; word is plain, with its space.
(fn DrawToken ()
  (bind (_l _r _found) (Utilities|String|Split :SourceString (V Tok) :InStr "@"))
  (bind _lab (CallFunction|MatchLabel :Rest _r))
  (if (or (not _found) (Utilities|String|IsEmpty _lab))
    (CallFunction|PutWord :Text (cat (V Tok) " ") :Chip false :Name "")
    (else
      (CallFunction|PutWord :Text _l :Chip false :Name "")
      (CallFunction|PutWord :Text (cat "@" _lab) :Chip true :Name _lab)
      (CallFunction|PutWord :Text (cat (Utilities|String|RightChop :SourceString _r :Count (Utilities|String|Len _lab)) " ") :Chip false :Name ""))))
```

`DrawPreview.txt` (input `Text`: String):

```lisp
; T65: draws the preview line (T64's MakePreview string) word by word in PreviewWrap, so every mention is a chip (step 5).
; The pool is made on first use; words past the line collapse.
(fn DrawPreview (Text)
  (if (== (len (V Words)) 0)
    (CallFunction|MakeWords))
  (set WordUsed 0)
  (set Toks (Utilities|String|ParseIntoArray Text))
  (for _t (V Toks)
    (set Tok _t)
    (CallFunction|DrawToken))
  (for _k (range (len (V Words)))
    (set TmpK _k)
    (if (>= (V TmpK) (V WordUsed))
      (Widget|SetVisibility :self (get (V Words) (V TmpK)) :InVisibility "Collapsed"))))
```

- **Spaces:** each plain word carries its trailing space, and a chip none, so ", " sits right after "@Meta". **If part 7's screenshot shows the words run together** (the text layout drops a trailing space from a text's width), drop the trailing spaces in `DrawToken` and set `PreviewWrap`'s `InnerSlotPadding` X to one space of the mono font at 18 pt (about 11 px); the comma then sits one space after a chip, which is fine.
- `MakePreview` stays T64's string builder: `PickLine`'s log line and `PreviewName` (the one place that writes "@Meta" for the action's target, T64) don't change. `DrawToken` turns that "@Meta" into a chip too.

**Rewrites of T64's files** (each found by its text, as at `47f95a3`):

| File | T64's line | T65's line |
|---|---|---|
| `Refresh.txt` | `(Class|Text|SetText :self (Variables|WBP_ActionBuilder|GetPreviewText) :Text (Utilities|Text|ToText(String) _p))` (its last line, after `(bind _p (CallFunction|MakePreview))`) | `(CallFunction|DrawPreview :Text _p)` |
| `SetLine.txt` | the same `SetText` line (its last line) | `(CallFunction|DrawPreview :Text _p)` |
| `StyleAll.txt` | `(Class|Text|SetFont :self (Variables|WBP_ActionBuilder|GetPreviewText) :Font (V MonoFont))` and the `SetColorandOpacity` line after it | removed (`WBP_Word.Setup` styles each word); also drop `(bind cText ...)`, which nothing else in `StyleAll` uses |
| `EventGraph.txt` | in `EventPreConstruct`, `(if IsDesignTime (Class|Text|SetText :self (Variables|WBP_ActionBuilder|GetPreviewText) ...))` | removed with its `if`; `EventPreConstruct` keeps `(CallFunction|StyleAll)` (the designer shows an empty preview box). The other eight events stay as they are; commit the whole file. |

Add `; T65: the preview line is drawn word by word (DrawPreview), so a mention is a chip.` to each header. `StyleAll`'s header also says the mono font is `MonoFont` "until UIStyle has a 'Mono' role"; leave that sentence. Compile with warnings as errors, save.

## 7. The check

**Before the runs:** `Local/switches.json` in the repo folder with `"mode": "free"`, `"autoplay": false`, `"fast_lines": false`, `"ai_seats": 0`, `"spare_human": false`, `"force_tie": false`, `"analytics": "off"`. PIE in a floating window at 1600 × 900 (`LevelEditorPlaySettings` `newWindowWidth` and `newWindowHeight`; put them back after). Pick **Test for Free**. Screenshots with `SlateInspectorToolset.Screenshot`, saved to `Saved/T65/shots/` (not in git). Keys with the Slate inspector's `PressKey` if survey 8 found it reaches the override, or `SpeechKey` through MCP; typing with its `Type`.

**The Slate inspector, as T64 found it:** a click lands only while the PIE window is the active window (after a command in the editor's Cmd box, a `Type` into the game's input box makes it active again; a `Click` on the box is not enough). The PIE window's ref changes on every PIE start: take it from `Windows` or a `Snapshot` of `""` each time. `Snapshot` marks the focused widget `[focused]`, a direct focus check.

### Run A: one show played by hand in PIE

1. **`hint.png`:** press Start the scene. At turn 1, once the lines stop: the builder open with No action picked (T64's chain must be in, part 0.1), the field empty with "Say something (optional)..." (`ComputePrompt`'s scene hint after T64's chain), the counter "0/15" between the field and Action!, quiet.
2. **The caret test** (sets `CaretRefocus`): type 15 words ending in a space, then `x`. Log: `NHOS: SPEECH cap words=16 -> 15`; the field shows the 15 words and a space. Type `y`: refused again (one more `cap` line, the field unchanged). If instead `y` lands inside the line, the caret wasn't at the end: set `CaretRefocus` to true, compile, and repeat the step. Write which under "Findings". Then select all and delete.
3. **`count12.png`:** type a 12-word line: the counter "12/15", quiet.
4. **`count15.png`:** type three more words: "15/15" on a red pill with white text. Type a space and a letter: refused, `NHOS: SPEECH cap` in the log.
5. **The paste:** clear the field, then set a 20-word text through MCP (`SetText` on `InputBox`, which runs the same chain as a paste) or paste it with the Slate inspector if it can: the field keeps the first 15 words, `NHOS: SPEECH cap words=20 -> 15`.
6. **`at_list.png`:** clear the field, type `Hey @`: the list over the field with the four AI names and their seat swatches (never "You"), the first in paper. Log: `NHOS: MENTION open <four names>`. Nothing in the lower panel moved (compare with `hint.png`), and no robot or name tag is covered. The list may cover the builder's lowest chips; that is decision 1.
7. **`at_filter.png`:** type `me`: the list holds only Meta. Press Down and Up: the highlight stays (one entry). Clear back to `Hey @`, press Down twice: the third name is paper. Press Escape: the list closes (`NHOS: MENTION close`) and stays closed while you type `x`; Backspace twice and type `@` again: it opens.
8. **`chip.png`:** type `me`, press **Enter**: the field reads `Hey @Meta ` (nothing was sent: no `NHOS: TYPED`), `NHOS: MENTION pick Meta`, the counter "2/15", the list closed. The preview line in the builder: `> stand still: "Hey @Meta "` with **@Meta as a chip** in Meta's blue. Press **Backspace** once: the field reads `Hey `, `NHOS: MENTION removed @Meta`. Type `@op`, press **Tab**: `Hey @OpenAI `, and the focus is still in the field (type `, look!` and every letter lands).
9. **Focus and step 6:** clear the field, type `I throw`, click **Grab** in the builder, type ` the rose`, click a chip, click the chat, click my card, type ` now.`: every letter is in the field (`I throw the rose now.`). The builder's clicks print nothing (its `KeepFocus` gives the focus back at once); the chat and card clicks print `NHOS: FOCUS back` at most once each. Click **Look around** so the action is valid, add ` @Meta` with the list, press **Action!**. Log: `NHOS: TYPED` with "@Meta", `NHOS: BUILDER send around - - ready=yes`, `NHOS: HUMAN around - - says=I throw the rose now. @Player <n>` (T63; the action is the one I clicked, not "throw"; this needs T64's `HandleSend` edit), and the `NHOS: LOG` line with "@Player <n>". The chat shows "@Meta".
10. **Free Talk:** at my Free Talk line, `@` opens the list with the actors still on stage, the counter shows, and the focus holds; no builder (T64). The panel is 640 wide here: check that the field still shows enough of its hint ("Say something, like: @Meta, ...") next to the counter, Action! and Pass, and write how wide it is. One screenshot, `freetalk_at.png`.

In every shot check that nothing covers a robot, its name tag or a thrown prop. Stop PIE.

### Run B: a free autoplay show in a game window

`"autoplay": true`, `"fast_lines": true`, `"mode": "free"`; the game-window command from `CLAUDE.md` with `-log=T65auto.log`. In the log: `NHOS: SHOW END` and **no `LogScript` line** (above all no "Accessed None" and no "Attempted to access index"). Autoplay sends without typing, so no `SPEECH` or `MENTION` lines are expected; the canned "@Anthropic, ..." lines still reach the log as "@Player N" (T26). Close the game window by its `-log=` name.

**Afterward:** `autoplay` and `fast_lines` back to false, the PIE window settings back, every game window closed. `python Tools/check_prompts.py --offline` passes.

### Findings to write in `T65.md`

- **What step 5 built:** "@Meta " as one unit in the field (UMG's editable text holds no widget), and the chip in the preview line (`WBP_Word`), shown in scene turns only.
- How the override was made (survey 5), or which keys the fallback covers (5e). The key names (survey 7), and whether the Slate inspector's `PressKey` reached the override (survey 8).
- `CaretRefocus`'s value and why (run A step 2).
- What can take focus on the screen (survey 2), and which clicks made `HoldFocus` pull it back in run A.
- Whether `Mono()` reads the builder's `MonoFont` or a copy (survey 6).
- **The design review** from the shots, as a critical first-time player: can I read the counter, do I notice the red pill before I try a 16th word, does the list read as "pick a name", is the chip clear in the preview, is the field wide enough at 640; what you'd change for T34.
- **Unreal MCP rules found in this task**, as earlier tasks do.

## 8. The commit, and knock-on notes

**The commit:** one commit, `T65: The speech field: a word counter, focus and @ mentions`: `Content/NHOS/UI/WBP_Stage.uasset`, `Content/NHOS/UI/WBP_ActionBuilder.uasset`, `Content/NHOS/UI/WBP_Word.uasset` (new; outside the Touches, so name it in the message); `Graphs/WBP_Stage/` (new: `Mono`, `ShowRef`, `MaxWords`, `ReadNames`, `LastToken`, `IsMention`, `CountWords`, `CutWords`, `SyncCount`, `CaretEnd`, `AtLists`, `AtPlace`, `AtEntry`, `AtShow`, `AtDraw`, `AtFollow`, `AtMove`, `AtPick`, `UnitBackspace`, `SpeechApply`, `SpeechChanged`, `SpeechKey`, `HoldFocus`, `OnPreviewKeyDown`, `EventGraph.Mentions`, maybe `EventGraph.Commit`; changed: `SetPrompt`, `SetPrepMode`, `EventGraph.Builder`), `Graphs/WBP_ActionBuilder/` (new: `MakeWord`, `MakeWords`, `TryLabel`, `MatchLabel`, `PutWord`, `DrawToken`, `DrawPreview`; changed: `Refresh`, `SetLine`, `StyleAll`, `EventGraph`), `Graphs/WBP_Word/Setup.txt`; `Docs/tasks/T65.md` (Result, Findings), `Docs/Plan.md` (the box, the "Next up" line), `Docs/DevLog.md`. Stage by path. Unlock both assets after the push. Delete `/Game/Scratch/WBP_KeyTest` before the commit if survey 5 made it.

**Knock-on: tell, don't change** (write these under "## Findings", "For later tasks"):

- **T66:** the timer goes last in `InputRow`, after `PassButton` (part 2a), and `Mono()` gives it the mono font. `SyncCount` and `HoldFocus` run in every phase with an open input, so the reaction and last-word rows get the counter, the list and the focus with no change. A timeout that sends through `SubmitInput` clears the field, so the change chain resets the counter and closes the list; `AtDraw(false)` closes the list when my input closes.
- **T61** (the stagehand's tips) and **T34** (T33-1: focusable in-show buttons): `HoldFocus` takes the keyboard back to the speech field every frame while I can type. A tip's button or a focusable in-show button must either show only while my input is closed or be made an exception in `HoldFocus`. T61's Escape can use survey 5's way of making an override.
- **T34:** decision 9 (the chip shows only in scene turns, where the preview line is), decision 6 (the red pill) and the field's width at 640 (part 7 run A step 10) are its to revisit with the rest of the screen. If T34 adds a `"Mono"` role to `UIStyle`, `Mono()`, `StyleAll` and `PutWord` switch to it.
- **The design doc:** the Turn Input tab (T62's edit) says each mention "is inserted as a chip". If my person wants the doc to match what UMG allows, propose: "Each mention goes in as one unit (one Backspace removes it) and shows as a chip in the preview line." Edit only after my person's OK (the plan's "The design doc follows the game").
- **`Docs/ItchPage.md`, "Controls":** after T66, one line for the @ list ("Type @ to pick an actor by name: Up and Down, then Enter or Tab").
