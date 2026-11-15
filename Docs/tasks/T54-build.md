# T54 build sheet: the new win condition

Back to [T54](T54.md). A PC prep session wrote this on 2026-11-15, without the editor. It is written against **`noHumansOnSet` at `42b1189` (T36)**, with `prompts.json`, `Tools/check_prompts.py` and `Docs/ItchPage.md` as **T52 leaves them**. T52 had not pushed when this sheet was committed; its uncommitted edits in the repo folder matched [T52-build.md](T52-build.md) parts 2 to 4 word for word, and this sheet's data and checker edits were tried on top of them. Line numbers are from that state (`42b1189` plus T52's edits). Find each line by its text before you change it.

The design doc was read, not changed: Rules tab rev 27 (The Cut, step 6, and the paragraph under it: "You win if you make the final two, or if you're still on stage when the last scene ends."), Bot Prompts tab rev 81 (the last line of "Opening prompt: game rules", which T52 copies) and Overview rev 146 (the Premise: "Make it to the final two, or to the end of the last scene, and humanity wins the stage."). The doc already states both wins, so T54 changes nothing in it.

## In short

- **`BP_Show`:**
  - **`SetWinReason(Win)`** (new, with a file): counts who is left and sets four new variables: `WinReason` (`caught`, `final_two` or `last_scene`), `WinLine` ("You made the final two." or "You were still on stage when the last scene ended."), `WinTail` (the end of the win game message) and `WinLeft`. It prints `NHOS: ENDING reason=<r> left=<n> line=<WinLine>`.
  - **`EndShow`:** one `SetWinReason` call first. The win game message and the win banner read `WinTail` and `WinLine` instead of the final-two words.
  - **`ShowEndScreen`:** the win subtitle reads `WinLine`; the `SHOW END` line gets ` reason=<WinReason>` right after `result=`.
  - **Nothing else changes.** T53's `EndReactions` already ends the show at two left or after the last scene, and T52's tie goes through it.
- **`prompts.json` `game`:** goal 1 names both wins, and a new sub-bullet under it says a tie helps the human. `asks.closing` stays as it is (part 2).
- **`Docs/ItchPage.md`:** the premise line and the "If you're cut" line say both wins; optionally a tip that a split vote helps (part 3).
- **`Tools/check_prompts.py`:** the closing ask goes out after all three endings (Meta: the final two; SpaceXAI: the last scene; OpenAI and Anthropic: caught), the file check fails a goal 1 that doesn't name both wins, and `--log` fails a `SHOW END` whose `reason=` doesn't match how the show ended (part 4). Tried on a scratch copy: `--offline` passes, a goal 1 without the last scene fails, and seven synthetic logs give the expected result.
- **`WBP_Title`, `WBP_Unavailable`:** read only; report any old win rule (part 1e).

## Questions for my person

The T54 session asks these with the question tool if my person hasn't answered them here yet, one at a time. The recommended answer is first. If the answers are below, use them and don't ask again.

1. **The end screen's title on a win.** The task says the title and subtitle say how I won, and gives the two sentences.
   - **Keep "YOU WIN" on the gold plate for both wins; the subtitle says how (Recommended).** The plate stays one big word, the sentence says the rest, and T60 redesigns the win screen anyway (the doc's Win screen row names no title).
   - Two titles: "YOU WIN: FINAL TWO" and "YOU WIN: THAT'S A WRAP", with the sentence still in the subtitle.
2. **Two actors left after the last scene** (a tie in an earlier scene, then a cut in the last one): both wins are true.
   - **Call it `final_two` and say "You made the final two." (Recommended).** It is the doc's first-named win and the harder one, and the sentence is true.
   - Call it `last_scene`.
3. **A tip on the itch page:** add "A tied vote cuts nobody and uses up a scene, so a split vote helps you." to "How to fool them".
   - **Add it (Recommended).** T52's "Why" names splitting the vote as a new play, and the page says nowhere that a tie helps me.
   - Leave it out; the page's only tie sentence stays T52's "When the vote ties, nobody is cut, but the scene still counts."

Answers: _(none yet)_

## Wording that comes from the task or the doc

Not questions, but listed so my person can see each new line in one place.

- **Goal 1** (part 2a) adds the Rules tab's second win: "If the human makes it to the final two, or is still on stage when the last scene ends, the human wins."
- **The tie sub-bullet** (part 2a) puts the task's own words ("a tie helps the human, because it uses up a scene") under goal 1: "So a tied vote helps the human: it cuts nobody and uses up a scene." Not in the doc.
- **The two win sentences** are the task's: "You made the final two." and "You were still on stage when the last scene ended."
- **The game message** keeps today's form: "The show is over. The human was PLAYER 3, who made the final two. The human wins." or "The show is over. The human was PLAYER 3, still on stage when the last scene ended. The human wins."
- **Itch page:** the premise line copies the Overview tab word for word; the new win sentence copies the Rules tab word for word.

## 0. Before you start (after T52 is pushed)

1. `git log --oneline -5` shows T52, `Docs/claims/T52` is released, and `git lfs locks` shows no lock on `BP_Show.uasset`. Claim T54 and lock `BP_Show.uasset` as the plan says.
2. **T52's findings** in `T52.md`:
   - The tie message's form. This sheet assumes T52's sheet: "The vote is tied between Player 2 and Player 5, with 2 votes each. Nobody is cut.", with no "Scene n: " prefix in any scene. If T52 added a prefix after scene 1, add it to the two tie messages in part 4c.
   - Whether T52 touched `EndShow`, `EndReactions` or `ShowEndScreen`. Its sheet changes none of them.
   - What its run A wrote about the end screen after a last-scene win ("write the end screen's text under Findings for T54", T52-build part 6). That is the text part 1c and 1d replace.
3. `python Tools/check_prompts.py --offline` passes before you start, so any failure afterward is T54's.
4. **Survey, in this order** (each a separate `call_tool`; tool calls stop at about 120 s):
   1. `BlueprintTools.read_graph_dsl` of **`EndShow`**, saved to `Saved/T54/EndShow.read.txt`. Never write it back. Expected (T10, T29, T30): `Phase` = "closing", `CueHeader`, `ShowWin` set from `Win`, a message "The show is over. The human was <NAME>" + a win or lose ending added to `GameMsgs`, three `CueBanner` calls (the win or lose line, then "The cast gives one last verdict..."), then `AskClosing`. Record: the node that holds the win ending (expected the literal `, who made the final two. The human wins.`, maybe through a `Select` on `Win`), the win banner's text and node, and the first exec node after the entry.
   2. `read_graph_dsl` of **`ShowEndScreen`**, saved to `Saved/T54/ShowEndScreen.read.txt` (big: T10's write took 34 s). Record: the `Setup` call's `Title` and `Sub` sources (literals, a `Select` on `ShowWin`, or the variables `EndTitle` and `EndSub`), and the `Append` chain of the `NHOS: SHOW END result=` `PrintString`.
   3. `find_nodes` in `BP_Show` (full class paths, T30): `/Script/BlueprintGraph.K2Node_VariableSet` titled `Set EndTitle`, `Set EndSub`, `Set LeftCount`; `K2Node_VariableGet` titled `Get LeftCount`; `K2Node_CallFunction` titled `EndShow`. Expected: `EndShow` is called only from `EndReactions` (lose and win). If `EndTitle` or `EndSub` is set outside `ShowEndScreen` (for example in `EndShow`), the subtitle edit in 1d happens there.
   4. **Who is left.** `SetWinReason` counts the seats whose `SeatCut` is false, over `range(SeatCount)`. Check that `SeatCut` is a Boolean array indexed by seat (T10). If `LeftCount` is a `BP_Show` variable that `EndReactions` sets before it calls `EndShow`, use `(<= (V LeftCount) 2)` in 1b instead, and drop the loop and `WinLeft`. Don't use `OnStage`: `CutActor` doesn't shrink it, `ScenePrep` rebuilds it (T09, T10), so at the end of the show it can still hold the last cut seat.

## 1. `BP_Show`

### 1a. Which graphs, which have files

| Graph | File in `Graphs/BP_Show/` | T54 changes | How |
|---|---|---|---|
| `SetWinReason(Win)` | new | — | DSL write, new file (1b). |
| `EndShow(Win)` | none | One call first; the win ending and the win banner | Node edits (1c). |
| `ShowEndScreen` | none | The win subtitle; ` reason=` in `SHOW END` | Node edits (1d). Big; T60 rewrites it later. |
| `EndReactions`, `LastSceneDone` | `LastSceneDone.txt` | Nothing | T53's end check: lose if my seat is cut, else win at two left or after the last scene. |
| `RunCue` | `RunCue.txt` | Nothing | The `"end"` cue runs `EndCheer(ShowWin)` and `ShowEndScreen`. |
| `StoreClosing`, `AskClosing`, `CueEnd` | `CueEnd.txt` only | Nothing | The closing asks and the `"end"` cue. |
| `WBP_EndScreen.Setup` | `Graphs/WBP_EndScreen/Setup.txt` | Nothing | It shows whatever `Title` and `Sub` it gets; `Win` picks the gold plate. |

**New variables in `BP_Show`:** `WinReason` (String), `WinLine` (String), `WinTail` (String), `WinLeft` (Integer, 0). `BlueprintTools.add_variable` takes `blueprint`, `name` and `type_name` (T59 used `int`; check the string type's name with `describe_toolset`). They are variables, not binds, because `EndShow` and `ShowEndScreen` read them later, and the loop carries `WinLeft` (T51).

### 1b. `SetWinReason` (new)

`Graphs/BP_Show/SetWinReason.txt` (new):

```lisp
; T54: how the show ended, for EndShow's game message and banner, the end screen's subtitle and the
; SHOW END line. EndShow calls it first, with its Win input. The human wins at the final two, or by
; still being on stage when the last scene ends (the Rules tab, The Cut). Two left after the last
; scene counts as the final two. Every if is top level with no return, so each one joins the next (T30).
(fn SetWinReason (Win)
  (set WinLeft 0)
  (for _s (range (V SeatCount))
    (if (not (get (V SeatCut) _s))
      (set WinLeft (+ (V WinLeft) 1))))
  (set WinReason "caught")
  (set WinTail "")
  (set WinLine "")
  (if (and Win (<= (V WinLeft) 2))
    (set WinReason "final_two")
    (set WinTail ", who made the final two. The human wins.")
    (set WinLine "You made the final two."))
  (if (and Win (> (V WinLeft) 2))
    (set WinReason "last_scene")
    (set WinTail ", still on stage when the last scene ended. The human wins.")
    (set WinLine "You were still on stage when the last scene ended."))
  (print (cat "NHOS: ENDING reason=" (V WinReason) " left=" (str (V WinLeft)) " line=" (V WinLine))))
```

- Create it with `add_function_graph`, add one Boolean input `Win` (`add_function_param`), compile, then expand the file with `Tools/dslpp.py` and write it with `write_graph_dsl`. Compile before you place its call node in `EndShow` (T18: a call node goes stale when its function gets a new parameter).
- **No `if` here has a `return`.** T30 found that an `if` without `return` inside the else path of an earlier `(if ... (return))` doesn't join the code after it, so the print would run only on one path. Two top-level `if`s with `and` avoid that.
- Every form is in a pushed source: `(for _s (range ...))` and `(get ... _s)` in `DrawCast.txt` and `BPC_LLMClient/FlushLocal.txt`, `(and ...)`, `(not ...)`, `str`, `cat` and `print` in `DrawCast.txt`, a String `set` in `T52-build.md`'s `TieCut` (`(set TieText ...)`).
- **If my person picks `last_scene` for question 2,** swap the two conditions: `final_two` when `(and Win (<= (V WinLeft) 2) (not <last scene done>))`. `LastSceneDone` has exec pins (T32: MCP can't make a function pure), so call it first and bind its `Done`: `(bind _last (CallFunction|LastSceneDone))`, then use `_last` in both conditions. Change part 4f's order to match.
- **If part 0 found a `LeftCount` variable,** replace the loop with nothing and `(V WinLeft)` with `(V LeftCount)`, and drop `WinLeft` (and print `left=` from `LeftCount`).

### 1c. `EndShow`: the game message and the banner

Node edits, no file. Write each one under "Findings" in `T54.md`, since `EndShow` has no file.

1. **The call.** Put a `CallFunction|SetWinReason` node right after the function entry, first in the exec chain, with `Win` from the entry's `Win` pin. Everything after it reads the variables.
2. **The win ending of the game message.** Replace the win ending (expected the literal `, who made the final two. The human wins.`) with a `Get WinTail` node (pure, so no exec wire). If the ending comes through a `Select String` on `Win`, wire `WinTail` into its true option; if a `Branch` picks one of two `Append` chains, replace the literal in the win chain. **Leave the lose ending as it is.** The AIs then read:
   - `The show is over. The human was PLAYER 3, who made the final two. The human wins.`
   - `The show is over. The human was PLAYER 3, still on stage when the last scene ended. The human wins.`
   - `The show is over. The human was PLAYER 3. The AIs win.` (unchanged)
   
   If the read-back shows another form (for example no comma, or "makes" for "made"), keep the game's form, put the two endings in that form into `SetWinReason`'s `WinTail` values, and make part 4c's closing strings match the game exactly.
3. **The win banner.** If the win banner's text names the final two (part 0 records it), replace those words with `Get WinLine` in its `Append` chain, so the banner reads, for example, "You were still on stage when the last scene ended. You win!" Keep the rest of the banner's words. If the win banner names no way of winning ("You win!"), put `WinLine` in front of it with one `Append`. The lose banner and "The cast gives one last verdict..." stay.
4. Nothing else in `EndShow` changes: `ShowWin`, the header, `AskClosing` and its `options` (every other name) stay.

### 1d. `ShowEndScreen`: the subtitle and the `SHOW END` line

Node edits, no file. T60 rewrites this graph; keep the edits small.

1. **The title:** per question 1. With the recommended answer, nothing changes: "YOU WIN" on the gold plate for both wins, "YOU'RE CUT" for a loss. With the other answer, the win title becomes `Append("YOU WIN: ", Select(WinReason == "final_two", "FINAL TWO", "THAT'S A WRAP"))`.
2. **The win subtitle** (the `Setup` call's `Sub`, or wherever part 0 found `EndSub` set): it must contain `WinLine` and no other wording about the final two. Expected today (T10): a sentence that names my seat and the final two, maybe with "in scene n of m" (T53: "`ShowEndScreen`'s subtitle still says '... of <SceneCount>'"). Make it `WinLine`, then the part that names my seat if there is one, for example:
   - `You made the final two. You were Player 3.`
   - `You were still on stage when the last scene ended. You were Player 3.`
   
   Drop "of <SceneCount>" from the win subtitle. The **lose subtitle** ("The AIs caught you in scene 2 of 4") stays as it is: it is true, and T60 rewrites the lose screen.
3. **The `SHOW END` line.** In the `Append` chain of the `PrintString` that prints `NHOS: SHOW END result=`, add two pins right after the `win`/`lose` part: the literal `" reason="` and `Get WinReason` (`add_node_pin` for a new pin, T53). The line then reads:
   - `NHOS: SHOW END result=win reason=final_two scenes=3 human=human show=1`
   - `NHOS: SHOW END result=win reason=last_scene scenes=4 human=human show=1`
   - `NHOS: SHOW END result=lose reason=caught scenes=1 human=human show=1`
   
   Keep everything after it (`scenes=`, `human=`, `show=`) as it is. Part 4f parses `key=value` pairs, so the order after `reason=` doesn't matter.

### 1e. `WBP_Title` and `WBP_Unavailable`: read only (step 3)

T33 owns both widgets, and T54 doesn't lock or save them. In the editor, read the text of every `TextBlock` in each (`ObjectTools` on the widget tree, or `UMGToolSet` if it lists texts; no save, no compile). Look for the old rule: "final two", "last two", "two actors", "win", "survive".

- **`WBP_Title`:** the tagline, the captions and the How to play panel (designer text, no source; T33 kept its wording). T50 found How to play line 2 still says "the director's secret note on the right", so expect old rules there.
- **`WBP_Unavailable`:** its texts are the relay's message and help lines (`Graphs/WBP_Unavailable/EventGraph.txt`); expect no win rule.

Write each line that states the old rule, word for word, under "Findings" in `T54.md`, and tell my person in the closing summary, naming T33 as the owner and T61 (which replaces How to play) as the task that fixes it. If a close-up screenshot helps, take it in PIE on the title screen (`Saved/T54/shots/title.png`).

## 2. `prompts.json`

Each line is as it sits in the file (two tabs before it, escaped quotes as written).

**a. `game`, goal 1, line 16** (T52 doesn't move it). Replace the line, and add a sub-bullet right after it, before the rival line (`"  - Your persona names a rival. When you can't decide between two suspects, lean toward your rival.",`).

- Now: `"1. Find the human and get them cut. If the human is cut, the AIs win. If the human makes it to the final two, the human wins.",`
- New, two lines:

```
		"1. Find the human and get them cut. If the human is cut, the AIs win. If the human makes it to the final two, or is still on stage when the last scene ends, the human wins.",
		"  - So a tied vote helps the human: it cuts nobody and uses up a scene.",
```

- The doc's tie line, which T52 puts under The Cut (`"  - A tied vote cuts nobody and still uses up a scene. If the human is still on stage when the last scene ends, the human wins.",`), stays word for word; `DOC_TIE_LINE` checks it.
- "You also want to reach the final two yourself." (line 19, under goal 2) stays: it is the doc's line about each bot's own goal.
- "How a show works" (line 23, T53) already says a show ends when "the human is cut, only two actors remain, or the last scene ends". No change.

**b. `asks.closing`, line 129: no change.** Its text is: `"closing": "The show is over (see game_messages). One last vote, for the end screen. ..."`. It points at `game_messages` for how the show ended, and asks for the actor each AI suspected most, "even if game_messages already revealed who it was". Nothing in it assumes two actors on stage, and `options` is every other actor. Free mode still matches it (`free_mode.json`'s `closing` phase looks for "The show is over"), and its four pre-written closing reasons name no ending.

## 3. `Docs/ItchPage.md`

T52 changes line 48 (the tie sentence) and T53 changed lines 58 and 116. These three lines are T54's.

**a. Line 42** (the premise, under "Tonight: the world's first all-AI improv show"). Replace the last sentence with the Overview tab's, word for word.

- Now: `... Improvise, blend in and cast suspicion on someone else. Make it to the final two, and humanity wins the stage.`
- New: `... Improvise, blend in and cast suspicion on someone else. Make it to the final two, or to the end of the last scene, and humanity wins the stage.`

**b. Line 60** (under "How a show works", after step 5). Put the Rules tab's win sentence first, word for word.

- Now: `If you're cut, you lose, and the AIs gloat. Either way, the end screen shows how each AI voted and why.`
- New: `You win if you make the final two, or if you're still on stage when the last scene ends. If you're cut, you lose, and the AIs gloat. Either way, the end screen shows how each AI voted and why.`

**c. Line 62, "How to fool them"** (question 3; only with a yes). Append one sentence at its end.

- Now (its end): `... Watch what the AIs accuse each other of, because they're looking for the same things in you.`
- New (its end): `... Watch what the AIs accuse each other of, because they're looking for the same things in you. A tied vote cuts nobody and uses up a scene, so a split vote helps you.`

**Checked and left:** line 57 ("The most votes is cut") and line 58 ("Repeat until two actors are left or the last scene ends.") are right as they are. Line 117 ("the Director who breaks ties") is T55's.

## 4. `Tools/check_prompts.py`

Each block is given with the text it goes after or replaces, as the file stands after T52. Tried on a scratch copy (`42b1189` plus T52's edits plus these): `--offline` passes and still builds 60 jobs (the closing ask stays one per persona), and the checks below fail and pass as listed.

**a. The docstring.** After T52's paragraph, which ends `vote ended in no NHOS: CUT or TIE line, or in more than one.` (line 86), and before `Exit code 0 means ...`:

```
Two ways to win (T54): the human wins at the final two, or by still being on
stage when the last scene ends. The closing ask goes out after each ending:
the human caught (OpenAI, Anthropic), the final two (Meta) and the last scene
with three actors left (SpaceXAI). The file check fails a 'game' goal 1 that
doesn't name both wins. --log fails a show whose NHOS: SHOW END reason= doesn't
match how it ended: caught (the human was cut), final_two (two actors left)
or last_scene (the last scene ended with more than two on stage).
```

**b. The file check, goal 1.** In `check_files`, right after T52's two lines

```python
    if any("Director breaks" in g for g in game):
        errors.append("prompts.json: 'game' still says the Director breaks ties; since T52 a tie cuts nobody")
```

(line 515), add:

```python
    # T54: goal 1 names both ways the human wins.
    goal1 = next((g for g in game if g.startswith("1. ")), "")
    if "final two" not in goal1 or "last scene ends" not in goal1:
        errors.append("prompts.json: 'game' goal 1 must name both ways the human wins: the final two, "
                      "or still on stage when the last scene ends (T54)")
```

Tried: with goal 1 as it is today, `--offline` prints `FAIL file: prompts.json: 'game' goal 1 must name both ways the human wins: ...` and exits 1.

**c. The closing states.** In `Show.actor_cases`, replace the whole block from `        # Closing line after the show. Meta sees the human win; the others see the human caught.` (line 782) down to its `        return cases` with:

```python
        # Closing line after the show (T54: each of the three endings). OpenAI and Anthropic see the human
        # caught in scene 1; Meta sees the human make the final two after scene 3; SpaceXAI sees the last
        # scene end with the human and two AIs on stage (cuts in scenes 1 and 3, ties in scenes 2 and 4).
        if pid in ("visionary", "worrier"):
            votes = [(v, HUMAN, self.vote_reason(h)) for v in PERSONAS]
            votes.append((HUMAN, "overclocker", self.vote_reason(oc)))
            cut = {HUMAN: "cut, revealed HUMAN"}
            g = [f"{h} is cut with 4 votes. Reveal: {self.upper(HUMAN)}: HUMAN.",
                 f"The show is over. The human was {self.upper(HUMAN)}. The AIs win."]
            scene = 1
        elif pid == "copycat":
            votes = [(v, "overclocker", self.vote_reason(oc)) for v in SAMPLE_CAST if v != "overclocker"]
            votes.append(("overclocker", HUMAN, self.vote_reason(h)))
            cut = {"overclocker": "cut, revealed AI", "visionary": "cut, revealed AI", "worrier": "cut, revealed AI"}
            g = [f"{oc} is cut with 4 votes. Reveal: {self.upper('overclocker')}: AI.",
                 f"Scene 2: {self.name('visionary')} is cut with 2 votes. Reveal: {self.upper('visionary')}: AI.",
                 f"Scene 3: {self.name('worrier')} is cut with 2 votes. Reveal: {self.upper('worrier')}: AI.",
                 f"The show is over. The human was {self.upper(HUMAN)}, who made the final two. The human wins."]
            scene = 3
        else:
            cc = self.name("copycat")
            votes = [("overclocker", HUMAN, self.vote_reason(h)), (HUMAN, "copycat", self.vote_reason(cc)),
                     ("copycat", "overclocker", self.vote_reason(oc))]
            cut = {"visionary": "cut, revealed AI", "worrier": "cut, revealed AI"}
            g = [f"{self.name('visionary')} is cut with 3 votes. Reveal: {self.upper('visionary')}: AI.",
                 f"The vote is tied between {h} and {oc}, with 2 votes each. Nobody is cut.",
                 f"Scene 3: {self.name('worrier')} is cut with 2 votes. Reveal: {self.upper('worrier')}: AI.",
                 f"The vote is tied between {h}, {oc} and {cc}, with 1 vote each. Nobody is cut.",
                 f"The show is over. The human was {self.upper(HUMAN)}, still on stage when the last scene ended. The human wins."]
            scene = SAMPLE_SCENES
        cases["closing"] = self.actor_state(pid, "closing", "show over", self.log(turns=3, talk=2, votes=votes),
                                            cut=cut, game_messages=g, options=self.others(pid))
        cases["closing"]["show"]["scene"] = scene
        return cases
```

- The first two branches are today's text; only SpaceXAI (`overclocker`) moves from "caught" to the new last-scene ending, so the run still makes 4 closing calls.
- The tie messages follow T52's form and name the tied actors in seat order, as `TieCut` loops over `OnStage`. The sample's seats are Player 1 `visionary`, 2 `worrier`, 3 the human, 4 `overclocker`, 5 `copycat`.
- The last-scene state's cast shows Players 1 and 2 cut and 3 to 5 on stage, and its log's votes are scene 4's three single votes. `show.scene` is now 1, 3 or 4 to fit each ending (it was always 1).
- If part 1c kept another form of the game message, change the last string of each branch to match the game exactly.

**d. `LOG_RE`** (line 1124) gets `SHOW END`:

```python
LOG_RE = re.compile(r"NHOS: (SHOW READY|SHOW END|RESTART|SEATS|SETUP|LOG|CLOSING|DIRECTOR|CUT|TIE|REACTIONS DONE)\b ?(.*)$")
```

**e. `check_log`: the counters.**

- After T52's `    vote_bad = 0  # T52: scenes whose vote didn't end in exactly one CUT or TIE` (line 1156):
  `    end_bad = 0  # T54: shows whose SHOW END reason doesn't match how they ended`
- After T52's `        ends, scene, ties = [], 0, 0  # T52` (line 1161):
  `        cuts, end = 0, None  # T54`
- In T52's `REACTIONS DONE` branch, after `                ties += ends.count("TIE")` (line 1169):
  `                cuts += ends.count("CUT")  # T54`
- Right before `            if kind == "SEATS":` (line 1175):

  ```python
              if kind == "SHOW END":
                  # T54: "result=<win|lose> reason=<final_two|last_scene|caught> scenes=<n> human=... show=<n>".
                  end = dict(re.findall(r"(\w+)=(\S+)", rest))
                  continue
  ```

  The `continue` matters: without it the line falls into the `else: # DIRECTOR` branch and is checked as an AI line.

**f. `check_log`: the reason check.** Right before `        if seats and total and total != seats - 1:` (line 1227):

```python
        # T54: the SHOW END reason matches how the show ended.
        if end:
            why, want = end.get("reason"), None
            left = seats - cuts if seats else None
            if end.get("result") == "lose":
                want = "caught"
            elif left is not None and left <= 2:
                want = "final_two"
            elif total and scene >= total:
                want = "last_scene"
            if why is None:
                print(f"Show {i}: SHOW END has no reason= (a log from before T54).")
            elif why != want:
                end_bad += 1
                print(f"[FAIL] show {i} | SHOW END | reason={why}, but {left if left is not None else '?'} actors were left "
                      f"after scene {scene} of {total or '?'}; reason={want or '<none: no ending fits>'} expected")
```

- The order of the two win tests is question 2's answer: two left after the last scene is `final_two`. With the other answer, test `total and scene >= total` first.
- `left` is the seat count minus the `CUT` lines; a tie cuts nobody. `scene` counts `REACTIONS DONE` lines (T52), and `total` is the `SETUP` line's `scenes=` (T53).
- A log from before T54 has no `reason=`: it prints a note and passes.

**g. The summary line and the return.**

- T52's summary line ends `scene count = {total or 'unknown'}, ties = {ties}.")` (line 1230). Make its end:

  ```python
  scene count = {total or 'unknown'}, ties = {ties}, "
                f"ending = {(end.get('result', '?') + ' ' + end.get('reason', '?')) if end else 'none'}.")
  ```

  so it prints, for example, `Show 1: human = Player 3, scenes = ..., scene count = 4, ties = 4, ending = win last_scene.`
- The return (line 1232): `    return 1 if bad or clock_bad or vote_bad or end_bad else 0`

**Tried on synthetic logs** (5 seats, `scenes=4`; C = a scene with a `CUT`, T = a scene with a `TIE`):

| Log | `SHOW END` | Result |
|---|---|---|
| TTTT | `result=win reason=last_scene scenes=4` | pass, `ending = win last_scene`, `ties = 4` |
| TTTT | `result=win reason=final_two` | exit 1: `reason=final_two, but 5 actors were left after scene 4 of 4; reason=last_scene expected` |
| CCC | `result=win reason=final_two scenes=3` | pass |
| C | `result=lose reason=caught scenes=1` | pass |
| CCC | `result=win scenes=3` (before T54) | pass, with the note |
| TCT | `result=win reason=last_scene scenes=3` | exit 1: `4 actors were left after scene 3 of 4; reason=<none: no ending fits> expected` |
| TCCC | `result=win reason=final_two scenes=4` | pass (question 2's recommended answer) |

**Runs:** `python Tools/check_prompts.py --offline` must pass. `python Tools/check_prompts.py --relay --free` (no tokens, about 60 asks) must pass, which shows the closing asks come back in the right shape after all three endings. A paid run of the closing ask is not needed for the Done-when; offer it to my person if they want to read how the bots sign off after a last-scene win (`--ask closing`, 4 calls).

## 5. The check

The Done-when: `--offline` and `--relay --free` pass; with `force_tie` on, a free autoplay show ends with `result=win reason=last_scene`; with `spare_human` on and `force_tie` off, one ends with `result=win reason=final_two`; a screenshot of each end screen.

The brief's editor rule applies: you drive the editor for the node edits; say so in your status file, and tell my person before PIE if the brief asks for it.

### Run A: the last scene (`force_tie` on), in a game window on the saved assets

`Local/switches.json`: `"autoplay": true`, `"mode": "free"`, `"force_tie": true`, `"spare_human": false`, `"fast_lines": true`, `"burn_test": false`, `"ai_seats": 0`. Close every game window before you save `BP_Show` (T53: a `-game` window keeps the `.uasset` open, and the save fails).

```bash
"<UE_ROOT>/Engine/Binaries/Win64/UnrealEditor.exe" "<PROJECT>" -game -windowed -ResX=1600 -ResY=900 -log=T54last.log
```

Then:

```bash
grep -E "NHOS: (SETUP|TIE|CUT |REACTIONS DONE|ENDING|BANNER|CLOSING|SHOW END)" Saved/Logs/T54last.log
```

Expected, in order (`<…>` varies):

```
NHOS: SETUP human=human scene=<card> note=<id> category=<cat> scenes=4
NHOS: TIE The vote is tied between Player 1, Player 2, Player 3, Player 4 and Player 5, with 1 vote each. Nobody is cut. tied=<5 ids> cut=none
NHOS: REACTIONS DONE scene=1 entries=5
... the same for scenes 2, 3 and 4 ...
NHOS: ENDING reason=last_scene left=5 line=You were still on stage when the last scene ended.
NHOS: BANNER <the win banner, with "You were still on stage when the last scene ended.">
NHOS: CLOSING <id> vote=<id> | <reason>          (4 lines)
NHOS: SHOW END result=win reason=last_scene scenes=4 human=human show=1
```

- None of `NHOS: CUT`, `NHOS: DIRECTOR`, `final two` in a `BANNER` line, or a `LogScript` warning.
- `python Tools/check_prompts.py --log Saved/Logs/T54last.log` passes, with `ties = 4, ending = win last_scene`.

### Run B: the final two (`spare_human` on, `force_tie` off)

The same switches with `"force_tie": false`, `"spare_human": true`, and `-log=T54final.log`.

- Expected: three `NHOS: CUT` lines, then `NHOS: ENDING reason=final_two left=2 line=You made the final two.`, the win banner with "You made the final two.", 4 `CLOSING` lines and `NHOS: SHOW END result=win reason=final_two scenes=3 human=human show=1`.
- Free-mode votes are random, so a natural tie can happen (T52's decision 12). Then the show plays a 4th scene and ends either `final_two scenes=4` (a cut in scene 4) or `last_scene scenes=4` (two ties). `--log` checks either is right. The Done-when needs one `final_two`: if the run ended `last_scene`, run it again.
- `python Tools/check_prompts.py --log Saved/Logs/T54final.log` passes, with `ending = win final_two`.

### Run C (optional): a loss

The same with `"spare_human": false`, `-log=T54lose.log`: `NHOS: ENDING reason=caught left=<n> line=` and `NHOS: SHOW END result=lose reason=caught ...`; `--log` passes. It shows the lose path is unchanged.

### Run D (optional): 4 actors

Run A with `"ai_seats": 3` (`-log=T54four.log`): 3 ties, `ENDING reason=last_scene left=4`, `SHOW END result=win reason=last_scene scenes=3`. It shows `WinLeft` counts a 4-seat show right (T53's `VoteCount` finding was about a 4-seat show).

### The screenshots: PIE autoplay

PIE in a 1600 × 900 floating window, with `Local/switches.json` as in run A (autoplay skips the title, and `mode` free is Test for Free), then as in run B. With autoplay on, `ShowEndScreen` shows the end screen without the "See the results" step (T14, T29). Wait for `NHOS: SHOW END` in the log, then take the screenshot with `SlateInspectorToolset.Screenshot` (T33). If the stage waits on **See the results** instead (the gold `ContinueButton` in the input row, T14), click it through the Slate inspector, which lands on the PC, and wait for `NHOS: END screen shown`. Save them in `Saved/T54/shots/` (not in git):

1. `end_last_scene.png`: the gold plate ("YOU WIN", or question 1's other title), the subtitle with "You were still on stage when the last scene ended.", and the four cards. No "final two" anywhere on screen.
2. `end_final_two.png`: the same with "You made the final two."
3. `end_last_scene_p12.png`: the first again at 1280 × 720, the doc's second size; the longer sentence must wrap inside the plate's column, not run off it.

As a first-time player, judge: does the subtitle say at a glance how I won, and does it read as the end of a show, not a tie banner? Write what you saw under "Findings".

**Afterward:** set `autoplay`, `force_tie`, `spare_human` and `fast_lines` back to false and `ai_seats` to 0 in `Local/switches.json`, and close each game window.

### The commit

`Content/NHOS/Core/BP_Show.uasset`, `Content/NHOS/Data/prompts.json`, `Tools/check_prompts.py`, `Docs/ItchPage.md`, `Graphs/BP_Show/SetWinReason.txt` (new), `Docs/tasks/T54.md`, `Docs/Plan.md` (the box), `Docs/DevLog.md`. All are in T54's Touches. Write the node edits to `EndShow` and `ShowEndScreen` under "Findings" in `T54.md`, since those graphs have no files, with the old and new texts (game message, banner, subtitle). Unlock `BP_Show.uasset` after the push.

## 6. Knock-on: tell, don't change

- **`Docs/Submission.md` line 178** (the trailer shot list, outside T54's Touches): "The ending: either YOU WIN in the final two, or ..." Tell my person that it could read "either YOU WIN at the final two or at the end of the last scene, or ...". Its voice-over line quotes the old itch premise ("Make it to the final two, and humanity wins the stage."), which part 3a changes.
- **`README.md` line 7** ("you win by not getting voted off") stays true. No change.
- **`WBP_Title` How to play and the tagline:** whatever part 1e finds goes to T33 (owner) and T61 (replaces How to play). T61's "Before the show" lines in the doc already say "survive to the final two or the last scene", and the doc says the itch page carries the same three opening lines; that is T61's.
- **T60 (the end screens) builds on this.** `WinReason` and `WinLine` are `BP_Show` variables that `ShowEndScreen` can read. When T60 rewrites `ShowEndScreen`, keep `reason=` in the `SHOW END` line (the checker reads it) and the two win sentences in the win screen. The doc's win screen row ("Each AI's reasoning, then their rivals revealed", earpiece line "You fooled them. Every one of them.") is T60's and T61's.
- **T55 (no Director):** nothing here reads the Director. `ItchPage.md` line 117 ("the Director who breaks ties") stays T55's.
- **The relay:** nothing in T54 changes `free_mode.json` or `Relay/`, so no deploy is needed.
