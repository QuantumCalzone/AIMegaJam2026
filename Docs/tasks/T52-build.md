# T52 build sheet: a tie cuts nobody

Back to [T52](T52.md). A Mac prep session wrote this on 2026-11-15, without the editor. It is written against **`noHumansOnSet` at `62ddaac` (T49)**, with `BP_Show` as **T53 leaves it** by its build sheet ([T53-build.md](T53-build.md)). T53 had not pushed when this sheet was committed, so part 0 lists what to check against T53's commit first. Line numbers are from `62ddaac`. Find each line by its text before you change it.

The design doc was read, not changed: Rules tab rev 27 ("The Cut", steps 3, 5 and 6) and Bot Prompts tab rev 81 (the last line of "Opening prompt: game rules").

**My person's answer to step 1 is in (2026-11-15): after a tie the reactions still run, with no reveal, because nobody is cut.** Don't ask the question again. Step 1 is done; write the answer under "Findings" in `T52.md`.

## In short

- **`BP_Show`:**
  - **`Tally`:** the tie branch (today: the tie message, the `TIE` print, the banner "... The Director breaks the tie." and `AskDirector`) becomes one call to a new function, **`TieCut`** (part 1c).
  - **`TieCut`** (new, with a file): finds the tied seats, adds "The vote is tied between Player 2 and Player 5, with 2 votes each. Nobody is cut." to `GameMsgs`, sets `CutSeat` to -1, keeps the votes for the end screen (`RecordVotes`), cues the banner, prints `NHOS: TIE ... cut=none` and queues a new `"tie"` cue.
  - **`RunCue`** (has a file): the `"tie"` cue stops the drum roll, plays the audience's laughs and calls `EndCut`, so the reactions start after the vote lines and the banner, the same way a cut's reactions do (part 1d).
  - **`StartReactions`:** don't put seat -1 at the head of the reaction order (part 1e).
  - **Nothing else changes.** T53's end check in `EndReactions` already sends a scene with no cut on to the next Scene Prep, or to `EndShow(true)` after the last scene. A tie never changes who is on stage, so the cast, the stamp, the robots and the vote row need nothing new (part 1f).
- **`prompts.json`:** The Cut's line loses "and the Director breaks ties"; the doc's tie line goes under it word for word; `asks.reaction` also covers a tie; the `_readme` gets a tie example (part 2).
- **`Docs/switches.example.json`:** `force_tie` now gives a scene with no cut (part 3).
- **`Tools/check_prompts.py`:** a reaction ask after a tie for each persona, the doc's tie line in the file check, a `--log` check that every scene's vote ends in one `CUT` or one `TIE`, and `CALLS_PER_SHOW` for a 4-scene show (part 4). Tried on a scratch copy of `62ddaac`: `--offline` passes.
- **Left for T55:** `AskDirector`, `PlayTiebreak`, `DirectorCut`, `DirectorState`, `HandleReply`'s tiebreak branch, the `Tiebreak` flag and `TiedNames` (part 6).

## Decisions made for my person

My person asked prep sessions to take their own recommendation on design calls. Each is open to change. The T52 session shows this list to my person when it closes the task.

1. **The reactions run after a tie** (my person's answer, not a decision): every actor on stage reacts with the `reaction` ask, in the usual order (the AIs in random order, then me), with no reveal and no stamp.
2. **The tie message keeps today's form and adds T52's sentence:** `The vote is tied between Player 2 and Player 5, with 2 votes each. Nobody is cut.` With 1 vote each it says "with 1 vote each". Three or more names read "Player 1, Player 2 and Player 4". Today's text is "The vote is tied between Player 2 and Player 3, with 2 votes each." (the Mac's `auto1.log`).
3. **The banner** is that message as I see it, plus "The scene still counts.": `The vote is tied between OpenAI and Anthropic, with 2 votes each. Nobody is cut. The scene still counts.` It replaces the two Director banners (the tie and the Director's pick), so a tie now shows one banner after the tally, not two.
4. **A new `"tie"` cue** starts the reactions, so they wait for the vote lines and the banner, as the `"cut"` cue makes them do after a cut. Calling `EndCut` straight from `Tally` would send the reaction asks while the vote lines still play.
5. **The sound of a tie:** the drum roll stops (nothing else stops it: `BPC_ShowAudio.Reveal` stops it after a cut), and the audience laughs (`Sfx "laughs"`). No stinger and no applause, since nobody is revealed.
6. **`asks.reaction` covers both endings** (part 2b), instead of a new `reaction_tie` ask. A new ask would need a new phase in `free_mode.json`, which the relay bundles, so it would need a relay deploy and my person's OK. Not in the doc: the Bot Prompts tab doesn't hold the asks.
7. **The doc's tie line goes under The Cut's line** as a sub-bullet, the way T50's note lines sit under their parts. The Cut's line changes only by dropping ", and the Director breaks ties".
8. **The `NHOS: TIE` line** keeps today's form (`NHOS: TIE <the message>`) and adds ` tied=<seat ids> cut=none`.
9. **`Tally` deletes its `Set Tiebreak` node** in the tie branch. `NHOS: CUT ... tiebreak=` then always says `no` until T55 removes the field.
10. **The checker** gets four tie reaction asks per full run (one per persona, 4 more calls), the `--log` check (part 4f; old logs with a Director tiebreak now fail it, which is right), and `CALLS_PER_SHOW = 125`.
11. **Free mode's pre-written reactions** include "Wow, that was a robot. The human is still here." and "One less robot on stage.", which are wrong after a tie. `free_mode.json` is outside T52's Touches and needs a relay deploy, so T52 leaves them. I recommend that T55 adds tie-neutral lines when it edits that file and deploys the relay (part 6).
12. **Natural ties count as a pass in the check run with `force_tie` off.** Free-mode votes are random, and 2 of the Mac's last 4 free autoplay shows had a natural tie. The check is that each scene ends in one cut or one tie, and that a scene with one clear top seat cuts it.

## 0. Before you start (after T53 is pushed)

1. `git log --oneline -5` shows T53, `Docs/claims/T53` is released, and `git lfs locks` shows no lock on `BP_Show.uasset`.
2. **T53's files:** `Graphs/BP_Show/LastSceneDone.txt` and `CueSceneBanner.txt` exist. Read T53's findings in `T53.md` for how `EndReactions` came out (T53-build 1f: a `LastSceneDone` call before the branch-2 Branch, whose condition is `OR(two or fewer left, LastSceneDone)`). If T53 built it another way, check that a scene with no cut still reaches its end check. Nothing in this sheet depends on more than that.
3. **T53's other changes this sheet meets:** `prompts.json` line 23 ("The cast has 4 or 5 actors ...") and maybe a new "show" line after line 37; `check_prompts.py`'s `SAMPLE_SCENES` and maybe its own `check_log` additions (`seats`, `total`, `clock_bad`). None of them touches a line part 2 or part 4 changes. Where both change `check_log`'s summary line or its return, keep both (part 4f says how).
4. `python Tools/check_prompts.py --offline` passes before you start.
5. **One survey script in `BP_Show`** (`find_nodes` needs the full node class path, T30):
   - **`Tally`:** the `AskDirector` call, both `CueBanner` calls, the `CueCut` call, the `Set Tiebreak` node, the `PrintString` nodes and the `Branch` that chooses between `CueCut` and the tie. Expected (T09, T29, T30): the tie branch is `Set Tiebreak` → add the tie message to `GameMsgs` → `PrintString "NHOS: TIE " + message` → `CueBanner(DisplayText(message) + " The Director breaks the tie.")` → `AskDirector`, in some order. Record which `Branch` output starts it.
   - **Every `Get CutSeat`** (`/Script/BlueprintGraph.K2Node_VariableGet`, title `Get CutSeat`), to list the graphs that read it. Expected: `StartReactions`, `NextReactor`, maybe `EndReactions` and `PlayReact`. **Any reader that indexes an array with `CutSeat`, or adds it to a list,** needs the guard in part 1e.
   - **`VoteCount`:** its type, and how `Tally` indexes it. `TieCut` (part 1b) assumes an Integer array indexed by seat, like `VoteTarget`. If `Tally` keeps it parallel to another list, loop over that list in `TieCut` instead of `OnStage`.
   - **`OnStage`:** an Integer array of the seats on stage (T09). `SeatName` and `SeatId` are String arrays indexed by seat (T06, T26).
6. **Read these graphs** (about 6 s each; none has a file): `StartReactions`, `NextReactor`, `EndCut`, `RecordVotes`, and `CutActor` only for its reveal message. Confirm:
   - `EndCut` sets `Phase` to "cut done" and calls `StartReactions`, nothing more (T10).
   - `RecordVotes` reads only the vote arrays (`VoteTarget`, `VoteReason`) and `SceneNum`, not `CutSeat`.
   - `CutActor`'s reveal message has no scene prefix ("Player 4 is cut with 2 votes. Reveal: ..."). If it starts with "Scene <n>: ", give the tie message the same prefix in `TieCut`.
   - Where `StartReactions` adds `CutSeat` to `ReactOrder` (part 1e).

## 1. `BP_Show`

### 1a. Which graphs, which have files

| Graph | File in `Graphs/BP_Show/` | T52 changes | How |
|---|---|---|---|
| `Tally` | none | The tie branch becomes one `TieCut` call | Node edit (1c). It is big (36 s to write in T09), and a read-back is unsafe to write back. |
| `TieCut` | new | — | DSL write, new file (1b). |
| `RunCue` | `RunCue.txt` | A `"tie"` cue | DSL write from the file (1d). |
| `StartReactions` | none | Skip `CutSeat` when it is -1 | Node edit (1e). |
| `NextReactor`, `EndCut`, `RecordVotes`, `CutActor` | none | Nothing | Read (part 0). |
| `EndReactions`, `LastSceneDone` | `LastSceneDone.txt` (T53) | Nothing | T53's end check serves the tie too. |
| `CueBanner`, `CueVotes`, `CueCut` | yes | Nothing | `TieCut` calls `CueBanner`. |
| `AskDirector`, `PlayTiebreak`, `DirectorCut`, `DirectorState`, `HandleReply` | none | Nothing | No longer reached. T55 deletes them. |

### 1b. `TieCut` (new)

**New variables in `BP_Show`:** `TieTop` (Integer, 0), `TieText` (String), `TieNames` (String array), `TieIds` (String array). They are variables, not binds, because the loops carry them (T51: a bind inside a `ForLoop` can be hoisted out of it).

`Graphs/BP_Show/TieCut.txt` (new):

```lisp
; T52: a tie for the most votes cuts nobody (the Rules tab, The Cut, step 3). Tally calls it in place
; of the Director's tiebreak. The scene still counts: the "tie" cue (RunCue) stops the drum roll and
; starts the reactions with no reveal, and EndReactions then goes on to the next Scene Prep, or ends
; the show after the last scene (T53's LastSceneDone).
(fn TieCut ()
  (set TieTop 0)
  (for _s (V OnStage)
    (if (> (get (V VoteCount) _s) (V TieTop))
      (set TieTop (get (V VoteCount) _s))))
  (clear (V TieNames))
  (clear (V TieIds))
  (for _s (V OnStage)
    (if (== (get (V VoteCount) _s) (V TieTop))
      (add (V TieNames) (get (V SeatName) _s))
      (add (V TieIds) (get (V SeatId) _s))))
  (set TieText (get (V TieNames) 0))
  (for _i (range (- (len (V TieNames)) 1))
    (set TieText (cat (V TieText) (select (== (+ _i 2) (len (V TieNames))) " and " ", ") (get (V TieNames) (+ _i 1)))))
  (bind _each (select (== (V TieTop) 1) "1 vote" (cat (str (V TieTop)) " votes")))
  (bind _msg (cat "The vote is tied between " (V TieText) ", with " _each " each. Nobody is cut."))
  (add (V GameMsgs) _msg)
  (set CutSeat -1)
  (CallFunction|RecordVotes)
  (bind _shown (CallFunction|DisplayText :Text _msg))
  (CallFunction|CueBanner :Text (cat _shown " The scene still counts."))
  (print (cat "NHOS: TIE " _msg " tied=" (Utilities|String|JoinStringArray (V TieIds) ",") " cut=none"))
  (Class|BPCLinePlayer|Cue :self (Variables|Default|GetLinePlayer) :Kind "tie" :Text "" :Num 0))
```

- Create it with `add_function_graph` (no parameters), expand the file with `Tools/dslpp.py`, and write it with `write_graph_dsl`.
- Every form here is already in a pushed source: `(for _i (range ...))` and `(get ... _i)` in `BPC_LLMClient/FlushLocal.txt`, `select` on strings in `WBP_EndScreen`, `JoinStringArray` in `DrawCast.txt`, `CallFunction|DisplayText` in `ShowLine.txt`, `Class|BPCLinePlayer|Cue` in `CueBanner.txt`.
- If `(set CutSeat -1)` doesn't take a negative literal, write `(set CutSeat (- 0 1))`.
- **Why `CutSeat` = -1:** `CutActor` sets it at each cut and nothing resets it (T09, T10). Without the reset, a tie in scene 2 would hand scene 1's cut seat the first reaction and the `reaction_cut` ask ("You were just cut").
- **Why `RecordVotes`:** it adds the scene's votes to the history that the end screen shows (T10). `CutActor` calls it at a cut; nothing else does.
- **The order on screen:** the tally banner (`Votes: OpenAI 2, SpaceXAI 1, Anthropic 2.`, already in `Tally`), then this banner (held 2 s by `cue_hold.banner`), then the `"tie"` cue. `pacing.json` has no `cue_hold.tie`, so that cue holds 0 s, and the first reaction follows the banner.
- **The two texts:** the AIs read Player names in `GameMsgs`; the banner gets `DisplayText`, which shows each name as I see it ("OpenAI", "Player 3 (you)").

### 1c. `Tally`: the tie branch

Node edit, no file.

1. From the `Branch` output that starts the tie branch (part 0), unlink the exec wire into the first tie node, and link it to a new `CallFunction|TieCut` node.
2. Delete the old tie branch's exec nodes: `Set Tiebreak`, the `GameMsgs` add, the `TIE` `PrintString`, the tie `CueBanner` and the `AskDirector` call. Then the pure nodes that fed only them (the tie message's `Append` chain, the `" The Director breaks the tie."` literal), or leave those, since a pure node with no consumer never runs.
3. **Keep** everything before the branch (the force-tie rewrite, the count, the vote lines, `CueVotes("")`, the `TALLY` print and the tally banner) and the one-top-seat path (`CueCut`).
4. Leave `TiedNames` as it is if `Tally` fills it to decide the tie; T55 removes it if nothing reads it.
5. If `Tally` does anything after `AskDirector` in the tie branch, move it after `TieCut`.

### 1d. `RunCue`: the `"tie"` cue

New content of `Graphs/BP_Show/RunCue.txt` (the change is the block marked T52, after `"cut"`):

```lisp
; T30: a cued screen change, run by BPC_LinePlayer when its turn in the queue comes.
; T20: the cues also carry the sound: the show music under every header, the drum roll with the vote row,
; the stinger and the crowd at the cut, the applause or laughs at the end screen.
(fn RunCue (Kind Text Num)
  (if (streq Kind "phase")
    (Class|BPCShowAudio|PlayMusic :self (V Audio) :Key "show")
    (Class|WBPStage|SetPhase :self (Variables|Default|GetStage) :Phase Text)
    (return))
  (if (streq Kind "banner")
    (Class|WBPStage|ShowBanner :self (Variables|Default|GetStage) :Line Text)
    (return))
  (if (streq Kind "votes")
    (if (Utilities|String|IsEmpty Text)
      (Class|WBPStage|SetVoteOptions :self (Variables|Default|GetStage) :Names (Variables|Default|GetNoNames))
      (return))
    (Class|BPCShowAudio|StartDrum :self (V Audio))
    (CallFunction|ShowVotePick)
    (return))
  (if (streq Kind "cut")
    (Class|BPCShowAudio|Reveal :self (V Audio) :IsHuman (== Num (V HumanSeat)))
    (CallFunction|CutActor :Seat Num)
    (return))
  ; T52: a tie cuts nobody. The drum roll stops with no stinger, the audience laughs, and the reactions start.
  (if (streq Kind "tie")
    (Class|BPCShowAudio|StopDrum :self (V Audio))
    (Class|BPCShowAudio|Sfx :self (V Audio) :Key "laughs" :Pitch 1.0)
    (CallFunction|EndCut)
    (return))
  (if (streq Kind "prep")
    (Class|BPCShowAudio|PlayMusic :self (V Audio) :Key "show")
    (CallFunction|ScenePrep)
    (return))
  (if (streq Kind "end")
    (Class|BPCShowAudio|EndCheer :self (V Audio) :Win (V ShowWin))
    (CallFunction|ShowEndScreen)
    (return))
  (print (cat "NHOS: CUE unknown " Kind)))
```

- `StopDrum` and `Sfx` are `BPC_ShowAudio` functions with sources (`Graphs/BPC_ShowAudio/`). `Sfx` prints `NHOS: SOUND laughs`. If either call node won't resolve from `BP_Show` (a private function), make it public in `BPC_ShowAudio`, which T52 doesn't hold: then drop the two lines and tell my person instead.
- `EndCut` → `StartReactions` → the reaction asks. That is the same path `CutActor` takes, without the reveal, the stamp, the fallen robot and `BuildCast`.

### 1e. `StartReactions`: no seat -1 in the reaction order

T10: `StartReactions` builds `ReactOrder` as the cut seat first, then the AI seats that aren't cut in random order, then my seat if I wasn't cut.

- **The edit:** put a `Branch` on `CutSeat >= 0` before the node that adds `CutSeat` to `ReactOrder`, so the add runs only when someone was cut. The rest of the order needs nothing: no seat's `SeatCut` changed, so all 4 AIs and I react, me last.
- **"If the human was cut"** (it adds "The human is caught. The AIs win the show.") compares `CutSeat` with `HumanSeat` or reads `SeatCut`. Either is false after a tie. Check which, and change nothing.
- **`NextReactor`:** the cut seat gets `reaction_cut` and the others `reaction`. With `CutSeat` = -1, every seat gets `reaction`. Change nothing.
- If part 0 found another reader that indexes an array with `CutSeat` (for example in `PlayReact`), guard it the same way, and list it under "Findings".

### 1f. After a tie: what every later phase starts with (step 3)

| State | After a tie | Why it is right |
|---|---|---|
| Who is on stage (`OnStage`, `SeatCut`, the cast panel) | unchanged | `CutActor` and `BuildCast` don't run. The next `ScenePrep` shows the same 5 actors. |
| The stamp | hidden | `StartCut` cleared it, and only `CutActor` sets it. `StartScene` clears it again. |
| The robots | all standing | `StageCut` runs only from `CutActor`. `StagePrep` places them again at the next Scene Prep. |
| The vote row | hidden | `Tally`'s `CueVotes("")` runs before the branch. `StartCut` fills it again next scene. |
| `CutSeat` | -1 | `TieCut`. The next cut sets it again. |
| `Phase` | "the cut", then "cut done" and "reactions" | The `"tie"` cue → `EndCut` → `StartReactions`. |
| The drum roll | stopped | The `"tie"` cue. |
| `GameMsgs` | holds the tie message | Like a reveal, it stays for the rest of the show (`StartScene` clears `GameMsgs` only in scene 1), so later asks know a tie happened. |
| The vote history | holds the scene's votes | `RecordVotes` in `TieCut`. `CutScene` stays empty for everyone, since nobody was cut. |
| `Tiebreak` | false | `Tally` no longer sets it (decision 9). |
| The end | `EndReactions` (T53) | My seat isn't cut; two or fewer left is false (a tie keeps everyone); so `LastSceneDone` decides: the last scene → `EndShow(true)`; otherwise the banner "That's scene n. 5 actors are left, and the show goes on." and `CuePrep`. |

## 2. `prompts.json`

Each line is as it sits in the file (two tabs before it, escaped quotes as written). Tried on a scratch copy of `62ddaac`: the JSON loads and `--offline` passes with part 4.

**a. `game`, The Cut, line 30.** Replace the line, and add the doc's line right after it.

- Now: `"- The Cut: everyone votes in secret for who they think is the human. Nobody can vote for themselves. The most votes is cut, and the Director breaks ties. The cut actor is revealed as AI or HUMAN, and everyone reacts.",`
- New, two lines. The first is today's line without ", and the Director breaks ties". The second is the doc's line (Bot Prompts rev 81, the last line of "Opening prompt: game rules"), word for word:

```
		"- The Cut: everyone votes in secret for who they think is the human. Nobody can vote for themselves. The most votes is cut. The cut actor is revealed as AI or HUMAN, and everyone reacts.",
		"  - A tied vote cuts nobody and still uses up a scene. If the human is still on stage when the last scene ends, the human wins.",
```

- Goal 1, line 15 ("If the human makes it to the final two, the human wins.") stays: it is T54's. The new sub-bullet already tells the bots that a tie helps the human (T54 step 1 then makes goal 1 say both wins).
- No other line in `game` mentions the Director. The `director` prompt, `asks.tiebreak` and the `_readme`'s Director sentences are T55's.

**b. `asks.reaction`, line 125.** After a tie nobody was "just cut and revealed", and the AIs react with this ask (decision 6). Not in the doc.

- Now: `"reaction": "Reactions. An actor was just cut and revealed (see game_messages). React in character. If an AI was cut, the human is still among you. Fill: speech, and at most 1 action.",`
- New: `"reaction": "Reactions. The vote just ended, and the last of game_messages says how: an actor was cut and revealed, or the vote was tied and nobody was cut. React in character. If an AI was cut, or nobody was, the human is still among you. Fill: speech, and at most 1 action.",`
- **Free mode still finds it:** `free_mode.json` matches phases in order by `ask_contains`. The new text contains "Reactions" and none of "Tiebreak", "The show is over", "The Cut", "You were just cut", "Free Talk" or "The scene, your turn", in any case, so it still matches the `reaction` phase (checked on the scratch copy).
- "The last of game_messages": after a human is caught, `StartReactions` adds "The human is caught. The AIs win the show." after the reveal, and that line says how too.

**c. Optional, `_readme`, line 8.** I recommend it, since the readme is where the game messages are shown.

- Now (part of the line): `game_messages example: 'Player 4 is cut with 2 votes. Reveal: PLAYER 4: AI.'`
- New: `game_messages examples: 'Player 4 is cut with 2 votes. Reveal: PLAYER 4: AI.' and, after a tie, 'The vote is tied between Player 2 and Player 4, with 2 votes each. Nobody is cut.'`

## 3. `Docs/switches.example.json`

`force_tie` stays `false`. In `_readme`, replace one sentence. T53 may have added `ai_seats` to this file; find the sentence by its text.

- Now: `force_tie: The Cut rewrites the vote targets into a cycle, so every actor on stage gets one vote and the Director breaks the tie.`
- New: `force_tie: The Cut rewrites the vote targets into a cycle, so every actor on stage gets one vote and the tie cuts nobody. The reactions still run and the scene still counts, so a show with force_tie on plays every scene and ends after the last one with the human still on stage. Set it back to false before a person plays.`

## 4. `Tools/check_prompts.py`

The checker builds no tie game message today except in `tiebreak_state` (the Director's, which T55 removes). T52 adds a tie to what the actors read, and a check for it. Each block is given with the text it goes after or replaces. Tried on a scratch copy of `62ddaac` with part 2: `--offline` passes, `build_jobs` makes 60 jobs (4 more: "Player 1 after a tie" and so on), and the `--log` check fails a synthetic scene with `TIE + CUT` and one with neither.

**a. The docstring.** Before `Exit code 0 means the files are valid and every reply passed its checks.` (line 78):

```
A tie (T52): a tie for the most votes cuts nobody, and the reactions still run.
Each persona's reaction ask also goes out after a tie (Player 2 and Player 5
tied 2 to 2), and the file check finds the design doc's tie line in
prompts.json 'game', word for word (DOC_TIE_LINE). --log fails a scene whose
vote ended in no NHOS: CUT or TIE line, or in more than one.
```

T53 may add a "Scene clock (T53)" paragraph in the same place. Put this one after it.

**b. `CALLS_PER_SHOW`, line 114.** Replace the line:

```python
# T52: about 7 calls per actor per scene (T26: 87 for a 3-scene show of 5, 4 and 3 actors), plus 4 closing.
# A 4-scene show with one tie (5, 5, 4 and 3 actors) makes about 7 x 17 + 4 = 123; with a tie in every scene, 144.
CALLS_PER_SHOW = 125
```

Each actor makes about 7 calls a scene: 3 turns, 2 Free Talk lines, a vote and a reaction, each mine through the input LLM. T58 (the last word) will add a few.

**c. `DOC_TIE_LINE`**, right after the `DOC_NOTE_LINES` list closes (its `]` is line 129; before `# Real people and products that must never appear`):

```python
# T52: the design doc's tie rule (Bot Prompts, "Opening prompt: game rules"), word for word.
DOC_TIE_LINE = "A tied vote cuts nobody and still uses up a scene. If the human is still on stage when the last scene ends, the human wins."
```

**d. The file check.** After the `for line in DOC_NOTE_LINES:` loop in `check_files` (its `errors.append(f"prompts.json: 'game' lost a note rule ...")` line, line 498):

```python
    if not any(DOC_TIE_LINE in g for g in game):
        errors.append("prompts.json: 'game' lost the design doc's tie rule (DOC_TIE_LINE)")
    if any("Director breaks" in g for g in game):
        errors.append("prompts.json: 'game' still says the Director breaks ties; since T52 a tie cuts nobody")
```

**e. A reaction after a tie.** In `Show.actor_cases`, before `        # Reaction to its own cut.` (line 747):

```python
        # T52: reaction after a tie, which cuts nobody. Player 2 and Player 5 tied 2 to 2, Player 1 got 1.
        w, cc = self.name("worrier"), self.name("copycat")
        votes = [("visionary", "worrier", self.vote_reason(w)), ("overclocker", "worrier", self.vote_reason(w)),
                 (HUMAN, "copycat", self.vote_reason(cc)), ("worrier", "copycat", self.vote_reason(cc)),
                 ("copycat", "visionary", self.vote_reason(self.name("visionary")))]
        cases["reaction_tie"] = self.actor_state(
            pid, "reaction", "the cut, reactions", self.log(turns=3, talk=2, votes=votes),
            game_messages=[f"The vote is tied between {w} and {cc}, with 2 votes each. Nobody is cut."])

```

In `build_jobs`, inside `for pid in personas:`, right after the `for ask in ACTOR_ASKS:` loop (after its `jobs.append((ask, show.name(pid), ...))` line, line 1199, and before `        if "scene_turn" in asks:`):

```python
            if "reaction" in asks:  # T52: the same ask after a tie, which cuts nobody
                st = cases["reaction_tie"]
                ctx = {"places": places, "props": props, "actors": actors, "me": show.name(pid), "options": [],
                       "note": st["you"]["note"]}
                pv = provider_for(data, "actor", pid)
                jobs.append(("reaction", f"{show.name(pid)} after a tie", pv,
                             request_body(data, pv, "actor", system_text(data, "actor", pid), st), ctx))
```

- The job's ask is `"reaction"`, so `check_reply` checks its shape as a reaction (speech, at most 1 action), and the leak and note checks cover it.
- `ACTOR_ASKS` doesn't change, and `--ask reaction` runs both reaction cases.
- The state's `show.scenes` comes from `actor_state`, which T53 changes to `SAMPLE_SCENES`.

**f. `--log`: one cut or one tie per scene.**

- `LOG_RE` (line 1096) becomes:

  ```python
  LOG_RE = re.compile(r"NHOS: (SHOW READY|RESTART|SEATS|SETUP|LOG|CLOSING|DIRECTOR|CUT|TIE|REACTIONS DONE)\b ?(.*)$")
  ```

  `NHOS: CUE cut cut` doesn't match `CUT`.
- After `    n = bad = 0` (line 1127): `    vote_bad = 0  # T52: scenes whose vote didn't end in exactly one CUT or TIE`
- After `        cards = []` (line 1130): `        ends, scene, ties = [], 0, 0  # T52`
- At the top of `for kind, rest in show:`, before `            if kind == "SEATS":`:

  ```python
              if kind in ("CUT", "TIE"):
                  ends.append(kind)
                  continue
              if kind == "REACTIONS DONE":
                  # T52: each scene's vote ends in one cut or one tie (which cuts nobody), then the reactions.
                  scene += 1
                  ties += ends.count("TIE")
                  if len(ends) != 1:
                      vote_bad += 1
                      print(f"[FAIL] show {i} | scene {scene} | the vote ended in {' + '.join(ends) or 'no CUT or TIE line'}; one CUT or one TIE expected")
                  ends = []
                  continue
  ```

  These `continue`s matter: without them the new kinds fall into the `else: # DIRECTOR` branch.
- The summary line (line 1177) gets `, ties = {ties}` before its final period: `print(f"Show {i}: human = {human or 'unknown'}, scenes = {', '.join(cards) or 'unknown'}, ties = {ties}.")`. If T53 appended ` scene count = ...`, keep both.
- The return (line 1179) becomes `return 1 if bad or vote_bad else 0`, or `return 1 if bad or clock_bad or vote_bad else 0` if T53 added `clock_bad`.
- **Order in the log:** `TIE` prints at once in `Tally`; `CUT` prints when its cue plays (T30). Both come before that scene's `REACTIONS DONE`, because the reactions start from the `"tie"` and `"cut"` cues.
- A log from before T52 with a Director tiebreak fails this check (`TIE + CUT`), which is right. The Mac's `auto1.log` does.

**Runs:** `python Tools/check_prompts.py --offline`. If the relay is up, `python Tools/check_prompts.py --relay --free --ask reaction` (no tokens) shows the 8 reaction asks come back in the right shape. A paid run of the reaction ask is not needed for the Done-when; offer it to my person if they want to see how the bots react to a tie (`--ask reaction`, 8 calls).

## 5. The check

The Done-when: with `force_tie` on, a free autoplay show plays every scene with no cut and ends after the last with `NHOS: SHOW END result=win`; with it off, a show still cuts; no `director-` ask in either run; a screenshot of the tie banner.

### Run A: `force_tie` on, in a game window on the saved assets

`Local/switches.json`: `"autoplay": true`, `"mode": "free"`, `"force_tie": true`, `"spare_human": false`, `"fast_lines": true`, `"burn_test": false`, `"ai_seats": 0`.

```bash
"<UE_ROOT>/Engine/Binaries/Win64/UnrealEditor.exe" "<PROJECT>" -game -windowed -ResX=1600 -ResY=900 -log=T52tie.log
```

On Windows the log is `Saved/Logs/T52tie.log` (on a Mac, `~/Library/Logs/AIMegaJam2026/T52tie.log`). Then:

```bash
grep -E "NHOS: (SETUP|CLAPPER|SWITCHES force|TALLY|TIE|CUT |DIRECTOR|CUE tie|SOUND (laughs|sting)|BANNER (The vote|That's|Last)|REACTIONS DONE|SHOW END|LLM director)" Saved/Logs/T52tie.log
```

Expected for each scene n = 1 to 4 (`<…>` varies; names in seat order):

```
NHOS: SETUP human=human scene=<card> note=<id> category=<cat> scenes=4
NHOS: CLAPPER scene=<n> total=4
NHOS: SWITCHES force_tie=true spare_human=false
NHOS: TALLY Player <a> 1, Player <b> 1, Player <c> 1, Player <d> 1, Player <e> 1
NHOS: TIE The vote is tied between Player 1, Player 2, Player 3, Player 4 and Player 5, with 1 vote each. Nobody is cut. tied=<5 ids> cut=none
NHOS: BANNER The vote is tied between <5 names as I see them>, with 1 vote each. Nobody is cut. The scene still counts.
NHOS: CUE tie
NHOS: SOUND laughs
NHOS: REACTIONS DONE scene=<n> entries=5
NHOS: BANNER That's scene <n>. 5 actors are left, and the show goes on.     (scenes 1 to 3 only)
```

and at the end, after scene 4: `NHOS: SHOW END result=win scenes=4 human=human show=1`.

The run must have **none** of these: `NHOS: CUT`, `NHOS: DIRECTOR`, `NHOS: LLM director-`, `NHOS: SOUND sting_`, a `LogScript` warning. The cut seat's free-mode lines must not appear either, since nobody gets `reaction_cut`:

```bash
grep -cE "I was an AI all along|best on this stage|after my next update|You cut a real robot" Saved/Logs/T52tie.log
```

must print 0. (The plain `reaction` lines include "Wow, that was a robot." which is wrong after a tie: decision 11.)

Then `python Tools/check_prompts.py --log Saved/Logs/T52tie.log` passes, with `ties = 4`.

### Run B: `force_tie` off

The same switches with `"force_tie": false` and `"spare_human": true` (so I'm never cut and the show plays on), and `-log=T52cut.log`.

- Each scene ends in one `NHOS: CUT <id> tiebreak=no ...` or, when the random free votes tie, one `NHOS: TIE ... cut=none` (decision 12). A scene whose `TALLY` has one top seat has a `CUT`.
- The show ends with `NHOS: SHOW END result=win scenes=3` when two actors are left, or `scenes=4` if a natural tie kept one more actor on stage.
- None of `NHOS: DIRECTOR`, `NHOS: LLM director-`, `LogScript` warnings.
- `python Tools/check_prompts.py --log Saved/Logs/T52cut.log` passes. Its `ties =` count tells whether the run saw a natural tie; a run with a tie followed by a cut also proves that the next cut works after `CutSeat` was -1.

A third, optional run with `spare_human` off shows a caught human still loses (`result=lose`); T53 and T54 cover that path too.

### The screenshots: PIE by hand

PIE in a 1600 × 900 floating window, Test for Free, `autoplay` false, `force_tie` true, `fast_lines` false. Play scene 1 by hand (on the PC, where the Slate inspector's clicks land; T33-1). Save the shots in `Saved/T52/shots/` (not in git):

1. **`tie_banner.png`:** after my vote, `NHOS: TIE` prints at once, but the banner waits for the vote lines and the tally banner. Watch the log for `NHOS: BANNER The vote is tied` and take the screenshot right away (the banner holds about 4 s). Expect: the banner with the tie line, no stamp, all five robots standing, every vote with its reason in the chat.
2. **`tie_reactions.png`:** the first reaction. Expect: the header says reactions, an AI reacts first (not a "cut" robot), and no stamp.
3. **`prep2.png`:** Scene Prep of scene 2. Expect: the clapperboard `SCENE 2 / 4`, the banner "Scene 2: <title>", the cast panel with all 5 actors and nobody gray, no vote row, no stamp.
4. `tie_banner_p12.png`: the banner again at 1280 × 720 (the doc checks every screen at both sizes); scene 2's tie works for it.

As a first-time player, judge: is it clear that nobody was cut and the show goes on? Does the banner fit without covering a robot's name tag? Write what you saw under "Findings".

**Afterward:** set `autoplay`, `force_tie`, `spare_human` and `fast_lines` back to false in `Local/switches.json`, and close each game window.

### The commit

`Content/NHOS/Core/BP_Show.uasset`, `Content/NHOS/Data/prompts.json`, `Tools/check_prompts.py`, `Docs/switches.example.json`, `Graphs/BP_Show/TieCut.txt` (new), `Graphs/BP_Show/RunCue.txt`, `Docs/tasks/T52.md`, `Docs/Plan.md` (the box), `Docs/DevLog.md`. All are in T52's Touches. Write the node edits to `Tally` and `StartReactions` under "Findings" in `T52.md`, since those graphs have no files.

## 6. Knock-on: tell, don't change

- **T55 removes what T52 leaves unused.** Nothing calls these after T52, but T52 doesn't delete them:
  - `BP_Show`: `AskDirector`, `PlayTiebreak`, `DirectorCut`, `DirectorState`, the "tiebreak" branch of `HandleReply`, the `Tiebreak` flag (still read by `CutActor`'s `tiebreak=` field, which now always says `no`) and `TiedNames` (if `Tally` still fills it to find the tie, keep the fill and drop only the Director's use).
  - `prompts.json`: `director`, `asks.tiebreak` and the `_readme`'s Director sentences. `llm.json`: `roles.director`. `free_mode.json`: the `tiebreak` phase.
  - `check_prompts.py`: `TIE_PAIRS`, `tiebreak_state`, the tiebreak jobs, `"tiebreak"` in `ALL_ASKS` and in `check_reply` and `check_note_deal`, the `DIRECTOR` kind in `LOG_RE` and `check_log`. Keep T52's `TIE` kind.
  - **Also for T55** (decision 11): when it edits `free_mode.json` and deploys the relay, replace the two `reaction` lines that assume a robot was cut ("Wow, that was a robot. The human is still here." and "One less robot on stage. I feel a little lonely.") with lines that fit a tie too.
  - `Docs/ItchPage.md` line 48 ("When the vote ties, the Director ...") and line 117 ("the Director who breaks ties") are T55's (in its Touches). Line 48 should say that a tie cuts nobody.
- **T54:** goal 1 in `game` (line 15) and `EndShow`'s win text. After a tie on the last scene, `EndShow(true)` runs with up to 5 actors on stage, so a win text that says "who made the final two" is wrong until T54. Run A shows it: write the end screen's text under "Findings" for T54.
- **The title screen's How to play** (`WBP_Title`, designer text in the asset, no source here) may still say the Director breaks ties. T52 doesn't hold `WBP_Title`: read it in the editor, and if it does, name it under "Findings" for T55 or T61 (which replaces How to play).
- **T60 (end screens):** after a tie, the vote history holds a scene in which nobody was cut. `ShowEndScreen` lists votes by scene and marks the cut from `CutScene`, which a tie leaves empty. Check the end screen of run A reads sensibly (four scenes of votes, nobody cut), and write what it shows under "Findings".
- **T61 (the stagehand):** its earpiece line for The Cut is "Most votes is cut. A tie cuts nobody but burns a scene." (the Rules tab's Onboarding table). Nothing to do now.
