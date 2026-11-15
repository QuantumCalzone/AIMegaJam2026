# T58 build sheet: the last word

Back to [T58](T58.md). A Mac prep session wrote this on 2026-11-15, without the editor. It is written against **`noHumansOnSet` at `04d594d`** (T44, the T45 prep and the T57 sheet on top of T36), with Free Talk **as T57 leaves it** by [T57-build.md](T57-build.md), and `BP_Show` and the data files as [T52-build.md](T52-build.md), [T54-build.md](T54-build.md) and [T55-build.md](T55-build.md) leave them. None of those four tasks had pushed. Line numbers are at `04d594d`. Find each line by its text before you change it.

The design doc was read, not changed: Rules rev 27 ("Free Talk": "Last word: anyone @-mentioned in the final round gets one reply before the vote.", and the Onboarding row "Get @'d in the last round and you get a reply."). Bot Prompts rev 81 has no last-word line, so `prompts.json` copies nothing from the doc here. **T58 needs no doc edit.**

The `BP_Show` names below that have no `Graphs/` file (`TalkOrder`, `TalkPos`, `TalkSeat`, `TalkRound`, `TalkCount`, `HumanSent`, `Autoplay`, `CannedTalk`, `LoadCannedTalk`, `SetPassEnabled`, `PendingTags`, `AskCount`, `SeatSystem`, `LLMClient`, `MakeEntry`) and `ComputePrompt`'s Free Talk texts were found by a byte search of `BP_Show.uasset` at `42b1189` (the method of T55-build part 0).

> **My person's OK is needed before `free_mode.json` is pushed** (step 5): the relay bundles it, and every push to `noHumansOnSet` redeploys the relay (`Relay/README.md`, "Deploy"). T59 found that only an OK typed in the task's own session counts. **Ask for it first** (part 0, step 1), so one commit can carry everything.

## In short

- **`BP_Show`** (part 1). Free Talk keeps `Phase` "free talk" through the last words, and a new flag, `LastWordOn`, tells the functions apart. So typing, Pass, the input LLM, `HandleSend`, `HandleReply` and `PlayTalk`'s flow work for a last word as they do for a Free Talk line.
  - **`NextTalker`** (no file, two node edits): a `Branch` on `LastWordOn` first, to `NextLastWord`; and after the final round, `StartLastWords` in place of `EndFreeTalk`.
  - **`StartLastWords`** (new, file): finds every actor on stage named with `@` in a final-round line by someone else, from the shared log; puts them in a random order in `TalkOrder`; prints `NHOS: LASTWORDS scene=<n> named=<ids|none>`; with nobody named it calls `EndFreeTalk` at once.
  - **`NextLastWord`** (new, file): one speaker at a time, like a Free Talk round. Prints `NHOS: LASTWORD <id> scene=<n>`. My seat: Pass on, my line typed or canned (`autoplay.json` `last_word`). An AI seat: the new `last_word` ask, `now` "free talk, last word".
  - **`EndLastWords`** (new, file): prints `NHOS: LASTWORDS DONE scene=<n> entries=<n>` and calls `EndFreeTalk`.
  - **`TalkWhen`** (new, file) and **`PlayTalk`** (no file, one rewire): a last word goes in the shared log with `when` "scene n, last word".
  - **`LastWordPrompt`** (new, file) and **`UpdatePrompt`** (no file, one node): my turn line reads "Last word. You were named. One last line before the vote, or press Pass." `ComputePrompt` itself doesn't change.
  - **`CannedLastWord`** and **`LoadCannedLast`** (new, files): the autoplay lines.
  - **T57's `PassCue` and `PassClear`** (files): a pass in a last word prints `round=last`; `PassClear` also clears `LastWordOn`.
- **`prompts.json`:** the new `asks.last_word`; `game`'s Free Talk line names the last word; `_readme` lists the new `when` (part 2).
- **`free_mode.json`:** a `last_word` phase before `free_talk`, and two `free_talk` lines start with `@{actor}` (part 3). Pushed only after the OK.
- **`autoplay.json`:** a `last_word` list of three lines; my canned final-round Free Talk line stays "pass" (part 4).
- **`Tools/check_prompts.py`:** `last_word` joins `ACTOR_ASKS` with a sample state; a file check that free mode answers every ask from its own phase; a `--log` check that each scene's last words are exactly the actors named in its final round (part 5). Tried on a scratch copy of `04d594d` with T57's and T58's data and checker changes: `--offline` passes, 67 jobs (4 `last_word`), and the `--log` check passes a synthetic good log and fails each of three broken ones.
- **`Relay/`:** no file changes. The push of `free_mode.json` is the deploy.

## Decisions made for my person

My person asked prep sessions to take their own recommendation on design calls. Each is open to change. The T58 session shows this list to my person when it closes the task.

1. **The last words are part of Free Talk.** `Phase` stays "free talk", and `TalkOrder`, `TalkPos` and `TalkSeat` carry the last words as they carry a round. So `HandleSend`, `SendHumanTalk`, `HandleReply`, `PlayTalk`, the input converter (phase "free talk") and the Pass button need no new branch, and step 3's "it goes through the input LLM as a Free Talk line" holds by itself. A flag, `LastWordOn`, is the only new state.
2. **Who is named is read from the shared log:** the final round's entries (`when` "scene n, free talk round r", r the last round), the text the AIs read. A seat counts when "@" + its Player name is in another actor's `says`, in any case ("@player 2" counts). A mention of a cut actor gives nothing, and neither does a mention in a last word, since only the final round's entries are read.
3. **The order is random:** each named seat goes in at a random place in the list.
4. **On screen:** the header "LAST WORD: SCENE 2" (the Free Talk header's form, as T53 left it, "FREE TALK: SCENE 2, ROUND 2 OF 2"), no banner. My turn line: "Last word. You were named. One last line before the vote, or press Pass." (the task's sentence, in the form of the other turn lines), with the hint "Answer who named you, like: @Meta, I only grabbed the rose for the story." While an AI answers: "Last word. Waiting for OpenAI to answer..."
5. **`ComputePrompt` isn't edited** (it is in T58's Touches): a new `LastWordPrompt` sets the turn line after it, the way `PrepPrompt` (T28) and `LinePrompt` (T30) do. That is one node in `UpdatePrompt` instead of string surgery in a big graph with a lossy read-back (T28).
6. **`PlayTalk` gets one rewire** (it isn't named in the Touches, but it is in `BP_Show`): its `when` text comes from the new `TalkWhen`.
7. **`asks.last_word`** (part 2a): answer the actor who named you, one line, with evidence, a pass allowed and seen. It contains "Last word" for free mode and none of the earlier phases' words.
8. **`game`'s Free Talk line** gets one sentence: "Then anyone named with @ in the last round gets a last word: one reply before the vote." The bots may now use @ on purpose.
9. **Free mode:** the `last_word` phase has no `pass_chance`, so every free last word speaks; one of its four lines starts with `@{actor}`, which tests that a mention in a last word gives no further last word. Two of the seven `free_talk` lines start with `@{actor}`: with a 0.1 pass chance, about 30% of final rounds with four AIs name nobody, so a 3-scene show usually has both a scene with last words and one without.
10. **`autoplay.json`:** three `last_word` lines, none "pass", so my canned last word always speaks. They are used in order across the show.
11. **A pass in a last word shows "passed"** (T57), and prints `NHOS: PASSED <id> scene=<n> round=last`.
12. **`NHOS: FREETALK DONE scene=<n> entries=<n>`** now counts the last words too (`PlayTalk` adds 1 to `TalkCount` for each).
13. **Prints:** `NHOS: LASTWORDS scene=<n> named=<ids>` at the start, also `named=none` when the step is skipped; one `NHOS: LASTWORD <id> scene=<n>` per speaker; `NHOS: LASTWORDS DONE scene=<n> entries=<n>` only when someone was named.
14. **The checker** gets a new file check: every ask's text must reach the free-mode phase of the same name (it catches a `last_word` phase placed after `free_talk`). `CALLS_PER_SHOW` goes from T52's 125 to 135 (about 2 last words a scene).

## 0. Before you start (after T57 is pushed)

1. **Ask my person for the OK first**, with the multiple-choice tool: "Push free_mode.json with T58 (Recommended)": it changes only Test-for-Free lines and the relay's free mode, never a paid call; or "Not now". With the OK, part 3 goes in the one commit. Without it, see "The commits".
2. `git log --oneline -8` shows T57. `git lfs locks` shows no lock on `BP_Show.uasset`, and no claim on T57. Lock `BP_Show`.
3. **What T57 left:** `Graphs/BP_Show/PassCue.txt` and `PassClear.txt` match T57-build 2c and 2d (parts 1i and 1j below start from them). `prompts.json` has T57's lines, and `check_prompts.py` has T57's `PASSED` check (part 5f changes its `LOG` match). Read T57's findings for anything that came out differently.
4. `python Tools/check_prompts.py --offline` passes before you start.
5. **One survey script in `BP_Show`** (`find_nodes` needs the full node class path, T30), then read **`NextTalker`** in the editor (about 6 s; no file):
   - **`NextTalker`:** the first exec node after the function entry; the `EndFreeTalk` call and the exec wire into it (expected: the "round over, last round" side of a `Branch` on `TalkRound`, T08); the human branch (expected: `Set HumanSent false`, `SetPassEnabled(true)`, then with `Autoplay` a `SendHumanTalk` call with `CannedTalk[...]`); the AI branch (expected: `AskCount` + 1, a tag `<SeatId>-<AskCount>`, `PendingTags` and `PendingSeats` adds, `ActorState(TalkSeat, "free_talk", "free talk, round r of 2")`, then `LLMClient.Ask(Tag, Role, System, User)`). **Copy the AI branch's exact nodes, order and `Role` value into `NextLastWord`** (part 1c), changing only the ask key and `now`. If it does more (a typing call, a burn, a print), add the same to `NextLastWord`.
   - **`PlayTalk`:** the `Append` chain that ends in ", free talk round " + `TalkRound`, and **every pin its output feeds**. Expected (byte order at `42b1189`: "scene ", ", free talk round ", then "NHOS: LOG "): `MakeEntry`'s `When` and the `NHOS: LOG` print's text. Part 1f rewires each.
   - **`UpdatePrompt`:** the exec chain. Expected (T28, T30): `IsValid(Stage)` → `ComputePrompt` → `PrepPrompt` → `LinePrompt` → `SetPrompt`.
   - **`HandleSend`:** the "free talk" case accepts a typed line when `TalkSeat` is my seat and `HumanSent` is false (T08). Nothing to change; confirm it doesn't also test the round.
   - **Variables:** none of `LastWordOn`, `LWOrder`, `LWIds`, `LWFinal`, `LWWhen`, `LWActor`, `LWSays`, `LWTag`, `LWLine`, `LWCanned` or `CannedLast` exists yet. `SharedLog` is the log array of JSON objects (`ActorLine.txt`), `OnStage` an Integer array of seats on stage, `SeatName`, `SeatId`, `SeatLabel` and `SeatSystem` String arrays by seat.

## 1. `BP_Show`

### 1a. Which graphs, which have files

| Graph | File in `Graphs/BP_Show/` | T58 changes | How |
|---|---|---|---|
| `NextTalker` | none | A `LastWordOn` branch first; `StartLastWords` in place of `EndFreeTalk` | Node edits (1b) |
| `StartLastWords` | new | — | DSL write, new file (1c) |
| `NextLastWord` | new | — | DSL write, new file (1c) |
| `EndLastWords` | new | — | DSL write, new file (1c) |
| `LoadCannedLast`, `CannedLastWord` | new | — | DSL write, new files (1d) |
| `TalkWhen` | new | — | DSL write, new file (1e) |
| `PlayTalk` | none | Its `when` text comes from `TalkWhen` | Node rewire (1f) |
| `LastWordPrompt` | new | — | DSL write, new file (1g) |
| `UpdatePrompt` | none | Calls `LastWordPrompt` after `PrepPrompt` | Node edit (1h) |
| `PassCue` | `PassCue.txt` (T57) | `round=last` in a last word | DSL write from the file (1i) |
| `PassClear` | `PassClear.txt` (T57) | Also clears `LastWordOn` | DSL write from the file (1j) |
| `EndFreeTalk`, `ComputePrompt`, `HandleSend`, `HandleReply`, `SendHumanTalk` | none | Nothing | `EndLastWords` calls `EndFreeTalk` as `NextTalker` did |

**New variables in `BP_Show`:** `LastWordOn` (Boolean, false), `LWOrder` (Integer array), `LWIds` (String array), `LWFinal`, `LWWhen`, `LWActor`, `LWSays`, `LWTag`, `LWLine` (Strings), `LWCanned` (Integer, 0), `CannedLast` (String array). The loop values are variables, not binds, because a bind inside a `ForLoop` can be hoisted out of it (T51).

**Write order:** the new functions first (1c to 1g; `StartLastWords` calls `NextLastWord` and `EndLastWords`, so create all three graphs empty with `add_function_graph`, then write them), then `PassCue` and `PassClear`, then the node edits (1b, 1f, 1h). Compile and save `BP_Show`.

### 1b. `NextTalker`: two node edits

1. **The branch first.** Add a `Branch` whose condition is a `Get LastWordOn`, between the function entry and its first exec node. `True` → a new `CallFunction|NextLastWord` node, and nothing after it. `False` → the old first node.
2. **After the final round.** Unlink the exec wire into the `EndFreeTalk` call (part 0), link that source to a new `CallFunction|StartLastWords` node, and delete the `EndFreeTalk` call node. If `EndFreeTalk`'s exec output led anywhere, link `StartLastWords`'s output there. The round-1 side, which calls `StartTalkRound`, stays.

`PlayTalk` ends by adding 1 to `TalkCount` and `TalkPos` and calling `NextTalker` (T08). During the last words that call now goes to `NextLastWord`, so each last word follows the one before. Write both edits under "Findings" in `T58.md`.

### 1c. `StartLastWords`, `NextLastWord` and `EndLastWords` (new)

`Graphs/BP_Show/StartLastWords.txt` (new):

```lisp
; T58: the last word (the Rules tab, Free Talk). Every actor on stage whose Player name follows an @ in
; a final-round line by someone else gets one reply before the vote, in a random order. NextTalker calls
; this after the final round's last speaker, in place of EndFreeTalk. Who is named comes from the shared
; log, the text the AIs read; a mention inside a last word counts for nothing. With nobody named, Free Talk
; ends at once.
(fn StartLastWords ()
  (set LWFinal (cat "scene " (str (V SceneNum)) ", free talk round " (str (V TalkRound))))
  (clear (V LWOrder))
  (clear (V LWIds))
  (for _e (V SharedLog)
    (bind _w (Json|GetField _e "when"))
    (set LWWhen _w)
    (if (streq (V LWWhen) (V LWFinal))
      (bind _a (Json|GetField _e "actor"))
      (set LWActor _a)
      (bind _y (Json|GetField _e "says"))
      (set LWSays _y)
      (for _s (V OnStage)
        (if (and (not (streq (get (V SeatName) _s) (V LWActor))) (Utilities|String|Contains :SearchIn (V LWSays) :Substring (cat "@" (get (V SeatName) _s)) :bUseCase false))
          (if (< (Utilities|Array|FindItem (V LWOrder) _s) 0)
            (Utilities|Array|Insert (V LWOrder) _s (Math|Random|RandomIntegerInRange 0 (len (V LWOrder)))))))))
  (for _s (V LWOrder)
    (add (V LWIds) (get (V SeatId) _s)))
  (print (cat "NHOS: LASTWORDS scene=" (str (V SceneNum)) " named=" (select (== (len (V LWOrder)) 0) "none" (Utilities|String|JoinStringArray (V LWIds) ","))))
  (if (== (len (V LWOrder)) 0)
    (CallFunction|EndFreeTalk)
    (return))
  (set LastWordOn true)
  (set TalkOrder (V LWOrder))
  (set TalkPos 0)
  (if (V Autoplay)
    (CallFunction|LoadCannedLast))
  (CallFunction|CueHeader :Text (cat "LAST WORD: SCENE " (str (V SceneNum))))
  (CallFunction|NextLastWord))
```

- **Forms:** `Json|GetField` inside a `for` with a `set` after it is `BPC_LLMClient/FreeReply.txt`'s pattern; `Utilities|String|Contains` is in `FreeFill.txt` (`:bUseCase false` makes it ignore case); `Utilities|Array|Insert` is in `BP_Robot/DoHanded.txt`; `RandomIntegerInRange` (both ends included) in `DrawCast.txt`; `JoinStringArray` and `select` on strings as in T52's `TieCut`.
- `Json|GetField` takes its type from the pin it feeds (the `set` of a String). If the read-back shows a wildcard, put each field into `TmpStr` first, as `FreeReply` does.
- Inserting each seat at a random place from 0 to the list's length gives every order the same chance.
- The final round's lines are the only ones whose `when` equals `LWFinal`; a last word's `when` is "scene n, last word" (1e).

`Graphs/BP_Show/NextLastWord.txt` (new):

```lisp
; T58: the next last word, one speaker at a time like a Free Talk round. PlayTalk logs each reply (its
; when from TalkWhen) and calls NextTalker, which sends it back here while LastWordOn is set.
; The AI branch is NextTalker's, with the last_word ask (part 0: copy its nodes, order and Role value).
(fn NextLastWord ()
  (if (>= (V TalkPos) (len (V TalkOrder)))
    (CallFunction|EndLastWords)
    (return))
  (set TalkSeat (get (V TalkOrder) (V TalkPos)))
  (print (cat "NHOS: LASTWORD " (get (V SeatId) (V TalkSeat)) " scene=" (str (V SceneNum))))
  (if (== (V TalkSeat) (V HumanSeat))
    (set HumanSent false)
    (Class|WBPStage|SetPassEnabled :self (Variables|Default|GetStage) :Enabled true)
    (if (V Autoplay)
      (bind _line (CallFunction|CannedLastWord))
      (CallFunction|SendHumanTalk :Line _line))
    (return))
  (set AskCount (+ (V AskCount) 1))
  (set LWTag (cat (get (V SeatId) (V TalkSeat)) "-" (str (V AskCount))))
  (add (V PendingTags) (V LWTag))
  (add (V PendingSeats) (V TalkSeat))
  (bind _st (CallFunction|ActorState :Seat (V TalkSeat) :AskKey "last_word" :Now "free talk, last word"))
  (Class|BPCLLMClient|Ask :self (V LLMClient) :Tag (V LWTag) :Role "actor" :System (get (V SeatSystem) (V TalkSeat)) :User _st))
```

- `SetPassEnabled` is written as T08's finding says (`Class|WBPStage|SetPassEnabled`, with `:Enabled true`; a `false` hides in read-backs, T08).
- **The tag and the ask must match `NextTalker`'s** (part 0): the order of the `AskCount` add and the tag (the logs show `copycat-1` as the first tag), the `PendingSeats` add, and the `Role` value (`llm.json` has `roles.actor`, whose provider is "persona"; pass what `NextTalker` passes). A tag goes into `PendingTags` before `Ask`, because `OnAnswer` can fire inside `Ask` (T07).
- `ActorState(Seat, AskKey, Now)` reads `asks.last_word` from `prompts.json` (part 2a), and fills the log, `game_messages` and an empty `options` as for a Free Talk line (T09).

`Graphs/BP_Show/EndLastWords.txt` (new):

```lisp
; T58: the last words are done; Free Talk ends as it did before T58 (EndFreeTalk, then The Cut).
(fn EndLastWords ()
  (print (cat "NHOS: LASTWORDS DONE scene=" (str (V SceneNum)) " entries=" (str (V TalkPos))))
  (set LastWordOn false)
  (CallFunction|EndFreeTalk))
```

`TalkPos` counts the last words played, since `PlayTalk` adds 1 for each.

### 1d. `LoadCannedLast` and `CannedLastWord` (new)

`Graphs/BP_Show/LoadCannedLast.txt` (new):

```lisp
; T58: my canned last words for autoplay, from autoplay.json's last_word list. A missing or empty list makes my seat pass.
(fn LoadCannedLast ()
  (clear (V CannedLast))
  (bind _cdir (Utilities|Paths|GetProjectContentDirectory))
  (bind (_o _ok) (Json|LoadJsonfromFile (Utilities|Struct|MakeFilePath (cat _cdir "NHOS/Data/autoplay.json"))))
  (if _ok
    (bind _h (Json|HasField _o "last_word"))
    (if _h
      (bind _l (Json|GetField _o "last_word"))
      (set CannedLast _l))))
```

`Graphs/BP_Show/CannedLastWord.txt` (new):

```lisp
; T58: the next canned last word, in order and repeated across the show; "pass" when there is none.
(fn CannedLastWord ()
  (if (== (len (V CannedLast)) 0)
    (return "pass"))
  (if (>= (V LWCanned) (len (V CannedLast)))
    (set LWCanned 0))
  (set LWLine (get (V CannedLast) (V LWCanned)))
  (set LWCanned (+ (V LWCanned) 1))
  (return (V LWLine)))
```

- The file path and the `LoadJsonfromFile` form are `BPC_LinePlayer/LoadPacing.txt`'s. `LoadCannedTalk` (no file) reads the same file; this is its twin for one list.
- `CannedLastWord` returns a String (`ReturnValue`). No modulo node is in any pushed source, so it counts with a wrap instead.

### 1e. `TalkWhen` (new)

`Graphs/BP_Show/TalkWhen.txt` (new):

```lisp
; T58: the shared log's "when" for a Free Talk line: "scene 2, free talk round 1", or "scene 2, last word"
; during the last words. PlayTalk uses it for the entry and its NHOS: LOG line.
(fn TalkWhen ()
  (if (V LastWordOn)
    (return (cat "scene " (str (V SceneNum)) ", last word")))
  (return (cat "scene " (str (V SceneNum)) ", free talk round " (str (V TalkRound)))))
```

### 1f. `PlayTalk`: one rewire

Node rewire, no file.

1. Add a `CallFunction|TalkWhen` node into `PlayTalk`'s exec line, right after the function entry.
2. Link its `ReturnValue` to every pin that the old `when` chain's last `Append` fed (part 0: `MakeEntry`'s `When`, and the `NHOS: LOG` print's text, or the `Append` that starts it).
3. Leave the old chain unlinked (a pure node with no consumer never runs), or delete it.
4. **Check:** `NHOS: LOG scene 1, free talk round 2 | ...` still prints in round 2, and `NHOS: LOG scene 1, last word | ...` during the last words (run A).

### 1g. `LastWordPrompt` (new)

`Graphs/BP_Show/LastWordPrompt.txt` (new):

```lisp
; T58: during the last words the turn line and the hint say so. UpdatePrompt calls this after ComputePrompt
; and PrepPrompt and before LinePrompt, the way PrepPrompt sets Scene Prep's (T28). ComputePrompt's Free Talk
; text is right for every other moment, and "Free Talk. Your line is on its way..." after I send.
(fn LastWordPrompt ()
  (if (not (V LastWordOn))
    (return))
  (if (not (streq (V Phase) "free talk"))
    (return))
  (if (== (V TalkSeat) (V HumanSeat))
    (if (V HumanSent)
      (return))
    (set PTurn "Last word. You were named. One last line before the vote, or press Pass.")
    (set PHint "Answer who named you, like: @Meta, I only grabbed the rose for the story.")
    (return))
  (if (>= (V TalkSeat) 0)
    (set PTurn (cat "Last word. Waiting for " (get (V SeatLabel) (V TalkSeat)) " to answer..."))))
```

- `PTurn`, `PHint` and `PCan` are the variables `LinePrompt.txt` sets. `PCan` stays as `ComputePrompt` set it (my input is open on my turn, as in a Free Talk round).
- `SeatLabel` is the name I see ("OpenAI"), as `ShowLine.txt` uses it.
- `LinePrompt` still runs last, so while lines play the turn line says "Watch the stage." (T30).

### 1h. `UpdatePrompt`: one node

Node edit, no file (its read-back is lossy, T28). Add a `CallFunction|LastWordPrompt` node between `PrepPrompt` and `LinePrompt`: unlink the exec wire from `PrepPrompt` to `LinePrompt`, and link `PrepPrompt` → `LastWordPrompt` → `LinePrompt`. Write it under "Findings".

### 1i. `PassCue`: `round=last` (T57's file)

New content of `Graphs/BP_Show/PassCue.txt` (the change is the `select` in the `"passed"` cue's text, and the comment's last line):

```lisp
; T57: a Free Talk pass shows "passed" by that actor's name (the Rules tab, Free Talk). ShowLine calls it
; in Free Talk, before the line goes into the queue, so the marker changes as that line comes up.
; A pass queues a "passed" cue; a spoken line from an actor whose marker is up queues "unpass".
; PassSeats holds the seats whose marker is up, as the logic sees it (it runs ahead of the screen).
; T58: a pass in a last word prints round=last.
(fn PassCue (Seat Does)
  (set PassIdx (Utilities|Array|FindItem (V PassSeats) Seat))
  (if (streq Does (V DoesPass))
    (if (< (V PassIdx) 0)
      (add (V PassSeats) Seat))
    (Class|BPCLinePlayer|Cue :self (Variables|Default|GetLinePlayer) :Kind "passed" :Text (cat "scene=" (str (V SceneNum)) " round=" (select (V LastWordOn) "last" (str (V TalkRound)))) :Num Seat)
    (return))
  (if (>= (V PassIdx) 0)
    (Utilities|Array|RemoveIndex (V PassSeats) (V PassIdx))
    (Class|BPCLinePlayer|Cue :self (Variables|Default|GetLinePlayer) :Kind "unpass" :Text "" :Num Seat)))
```

If T57's pushed `PassCue.txt` differs (its findings say why), make only the `select` change in the pushed text.

### 1j. `PassClear`: clears `LastWordOn` too (T57's file)

New content of `Graphs/BP_Show/PassClear.txt`:

```lisp
; T57: every "passed" marker comes off at the end of each Free Talk (EndFreeTalk) and at the start of the
; next (StartFreeTalk). A cue, so it waits for the lines in front of it.
; T58: it also ends the last words: a Restart in the middle of them leaves LastWordOn set until the next Free Talk starts.
(fn PassClear ()
  (clear (V PassSeats))
  (set LastWordOn false)
  (Class|BPCLinePlayer|Cue :self (Variables|Default|GetLinePlayer) :Kind "unpass" :Text "" :Num -1))
```

Without it, a Restart during a last word would leave `NextTalker` sending the next show's first Free Talk speaker to `NextLastWord`.

### 1k. How a Free Talk runs now

```
StartFreeTalk ─ PassClear ─ StartTalkRound (round 1) ─ NextTalker … PlayTalk ─ NextTalker …
  round 1 over ─ StartTalkRound (round 2) ─ NextTalker … PlayTalk …
  round 2 over ─ StartLastWords ─┬─ nobody named: NHOS: LASTWORDS scene=n named=none ─ EndFreeTalk
                                 └─ named: LastWordOn ─ header ─ NextLastWord ─ (ask, or my turn)
                                        PlayTalk (when "scene n, last word") ─ NextTalker ─ NextLastWord …
                                        all done ─ EndLastWords ─ EndFreeTalk ─ PassClear … StartCut
```

- **Call depth:** a pass, or an ask that fails at once inside `Ask`, calls `NextTalker` on the same call stack (T08: at most 8 per Free Talk). The last words add at most 5.
- **The line queue:** each last word is a line in the queue like any Free Talk line, so it shows "<name> is typing..." first (an AI line in phase "free talk", `LineInfo`), then plays; the header cue waits for the round's lines in front of it.

## 2. `prompts.json`

Each line as it sits in the file (two tabs before it). Line numbers at `04d594d`; T52 adds a line after line 30 and T57 one after line 54, and T55 removes `director` and `asks.tiebreak`, so find each by its text. Tried on the scratch copy with T57's lines: the JSON loads, `--offline` passes.

**a. `asks.last_word`** (new), between `"free_talk": ...` and `"vote": ...` (line 125):

```
		"last_word": "Last word. Someone named you with @ in the last round of Free Talk. Answer the actor who named you, in one short line, about 10 words, with evidence from the log. This is your last line before the vote. Pass only if you truly have nothing to add: everyone sees a pass, and silence is evidence. Fill: speech, or pass. No actions.",
```

- **Free mode:** it contains "Last word", which part 3's phase matches before `free_talk`. It contains none of "The show is over", "The Cut", "You were just cut" or "Reactions" (case-sensitive, as in the game and the relay), so no earlier phase takes it. Part 5c's new file check proves it.
- Its pass sentence is T57's `free_talk` wording.

**b. `game`, "How a show works", line 28** (the Free Talk line). At its end:

- Now: `"- Free Talk: 2 rounds, in a new random order each round. One line each per round, or a pass. This is where the cast argues about who the human is.",`
- New: `"- Free Talk: 2 rounds, in a new random order each round. One line each per round, or a pass. This is where the cast argues about who the human is. Then anyone named with @ in the last round gets a last word: one reply before the vote.",`
- The sub-bullet under it (the doc's "In Free Talk the scene is over ...") stays.

**c. `_readme`, line 6.** In the middle of the line:

- Now: `... 'when' is 'scene 1, turn 2', 'scene 1, free talk round 1', 'scene 1, the cut' or 'scene 1, reactions'. ...`
- New: `... 'when' is 'scene 1, turn 2', 'scene 1, free talk round 1', 'scene 1, last word', 'scene 1, the cut' or 'scene 1, reactions'. ...`

## 3. `free_mode.json` (pushed only with my person's OK)

Tried on the scratch copy: the JSON loads, `--offline` passes (every line fits 15 words with its longest fill), and the phase guard (part 5c) passes; with the new phase moved after `free_talk`, it fails.

**a. The `last_word` phase**, right before the `free_talk` phase (line 74, the `{` above `"id": "free_talk",`):

```json
		{
			"id": "last_word",
			"ask_contains": ["Last word"],
			"lines": [
				"{actor}, you named me with zero proof. Read the log again.",
				"I was busy acting, {actor}. Robots focus. You should try it.",
				"@{actor}, check my battery logs. They will clear my name.",
				"Me? My circuits are spotless. {actor} is just deflecting."
			]
		},
```

`{actor}` is any cast name but the speaker's, not always the one who named them; that is fine for a test show. No `pass_chance` and no `actions`, so a free last word always speaks and never moves.

**b. Two `free_talk` lines get an @ mention** (lines 80 and 84):

| Line | Now | New |
|---|---|---|
| 80 | `"{actor}, why did you hesitate before your last line?",` | `"@{actor}, why did you hesitate before your last line?",` |
| 84 | `"{actor} walked to the {place} without a reason. Explain that.",` | `"@{actor}, you walked to the {place} without a reason. Explain that.",` |

**c. `_readme`, line 6:** `'pass_chance' (Free Talk only)` → `'pass_chance' (Free Talk only; the last word has none)`.

**The relay:** nothing in `Relay/` changes; `freePhase()` walks the phases by data, as the game does. Until the push, the relay answers a `last_word` ask from its `free_talk` phase (the ask contains "Free Talk"), in the right shape, so `--relay --free` passes before and after. After the push, wait about 90 s for the build (T59), then run `--relay --free --ask last_word`.

## 4. `autoplay.json`

**a. A `last_word` list**, between `vote` and `reaction` (before line 24, `	"reaction": [`):

```json
	"last_word": [
		"You named me? Read my lines again. Nothing human in there.",
		"Accuse me all you like. My circuits never skip a beat.",
		"Wrong robot. Watch who keeps changing their story instead."
	],
```

**b. `_readme`:** before `reaction: one line per scene for the human seat's reaction`, add: `last_word: one line for each last word the human seat gets (an actor named it with @ in the final Free Talk round), used in order and repeated; \"pass\" passes. ` (the `\"` as the file writes quotes inside the string).

**`free_talk` doesn't change:** its second line, "pass", is my canned scene-1 final-round line, which T57's check uses. My scene-3 final-round line ("@Anthropic, you sighed twice ...") names Anthropic, so scene 3 gives Anthropic a last word when it is still on stage.

## 5. `Tools/check_prompts.py`

Each block with the text it goes after or replaces. Line numbers at `04d594d`, before T52, T54, T55 and T57, which all change this file; each place says how to keep theirs. Tried on a scratch copy of `04d594d` with T57's part 5 and parts 2 to 4: `--offline` passes; `build_jobs` makes 67 jobs (63 after T57, plus 4 `last_word`); the `--log` check below passes a synthetic log and fails it with a last word removed, with `NHOS: LASTWORDS` naming one seat too few, and with a final-round mention left unanswered.

**a. The docstring.** Before `Exit code 0 means the files are valid and every reply passed its checks.` (line 89), after T57's "Passes (T57)" paragraph:

```
Last word (T58): anyone named with @ in the final Free Talk round gets one
reply before the vote. Each persona answers a last_word ask (named by another
actor in round 2). The file check fails an actor ask that free_mode.json would
answer from another phase. --log fails a scene whose last words (NHOS: LOG
scene n, last word) aren't exactly the actors on stage that someone else named
with @ in its final round, one each, as NHOS: LASTWORDS says.
```

**b. `ACTOR_ASKS` and `CALLS_PER_SHOW`.**

- `ACTOR_ASKS` (line 130): `ACTOR_ASKS = ["scene_turn", "free_talk", "last_word", "vote", "reaction", "reaction_cut", "closing"]`. The file check (`for k in ALL_ASKS:`) then requires `asks.last_word`, and T55's guard ("an ask the game doesn't send") accepts it.
- `CALLS_PER_SHOW`: T52 sets 125. Make it 135, with this comment line added above T52's: `# T58: plus about 2 last words a scene (the actors named in the final round).`

**c. The free-mode phase guard.** In `check_files`, after T57's two silence checks (the line ending `since T57 a too-polished line is evidence")`):

```python
    # T58: free mode answers each ask from the phase of the same name: the first phase whose
    # ask_contains is in the ask's text (case-sensitive, as in the game and the relay).
    free = load_json("free_mode.json", errors) or {}
    for k in ALL_ASKS:
        text = prompts.get("asks", {}).get(k, "")
        if k == "input" or not text:
            continue
        hit = next((ph.get("id") for ph in free.get("phases", []) if any(w in text for w in ph.get("ask_contains", []))), "scene_turn")
        if hit != k:
            errors.append(f"free_mode.json: asks.{k} would get a '{hit}' reply in free mode; put a '{k}' phase first, or change the ask")
```

Every phase id is its ask's name (`closing`, `vote`, `reaction_cut`, `reaction`, `last_word`, `free_talk`, `scene_turn`; `tiebreak` until T55). `input` matches by `when_field`, not by text, so it is skipped. Run before T55 and after: it passes both.

**d. The sample state.** In `Show.actor_cases`, right after T57's `cases["free_talk_r2"] = ...` line (after line 882's `cases["vote"]`):

```python
        # T58: the last word. Another actor names this one with @ in round 2 (it takes that actor's line).
        log = self.log(turns=3, talk=2)
        accuser = self.name("worrier" if pid == "copycat" else "copycat")
        for e in reversed(log):
            if e["actor"] == accuser and e["when"] == "scene 1, free talk round 2":
                e["says"] = f"@{self.name(pid)}, you never answered a single question. Who are you really?"
                break
        cases["last_word"] = self.actor_state(pid, "last_word", "free talk, last word", log)
```

- Copycat (Player 5) speaks in `TALK`'s round 2 and names the others; Worrier (Player 2) names Copycat. Both have a round-2 line, so the swap always lands. The new line has 11 words.
- `build_jobs` needs no change: its `for ask in ACTOR_ASKS:` loop sends `cases["last_word"]` for each persona.

**e. `check_reply`.** `    elif ask == "free_talk":` (line 1201) becomes `    elif ask in ("free_talk", "last_word"):`. A last word has the same shape as a Free Talk line: speech or a pass, no actions.

**f. `--log`: the last words match the final round's mentions.**

- **`LOG_RE`** (line 1249): add `LASTWORDS` and, if T52 hasn't, `CUT`. With T52's, T54's, T55's and T57's kinds:

  ```python
  LOG_RE = re.compile(r"NHOS: (SHOW READY|SHOW END|RESTART|SEATS|SETUP|LOG|CLOSING|CUT|TIE|REACTIONS DONE|PASSED|LASTWORDS)\b ?(.*)$")
  ```

  `NHOS: LASTWORD <id>` (no S) doesn't match `LASTWORDS\b`, and the check doesn't need it.
- After T57's `pass_bad = 0` line (after line 1280): `    lw_bad = 0  # T58: scenes whose last words don't match the final round's @ mentions`
- After T57's `cast_ids, passes, marks = [], [], []  # T57` line (after line 1284): `        talk, lastw, named, cut_at, sc_now = {}, {}, {}, {}, 0  # T58`
- At the top of `for kind, rest in show:` (line 1285), before T57's `if kind == "PASSED":` and **before T52's `CUT`/`TIE` block**:

  ```python
              if kind == "CUT":
                  cut_at[rest.split()[0]] = sc_now  # T58: off stage after this scene (T52's CUT block, if any, still runs)
              if kind == "LASTWORDS":
                  # T58: "NHOS: LASTWORDS scene=<n> named=<ids|none>" (and "... DONE scene=<n> entries=<n>").
                  m = re.match(r"scene=(\d+) named=(\S+)", rest)
                  if m:
                      named[int(m.group(1))] = [] if m.group(2) == "none" else m.group(2).split(",")
                  continue
  ```

  The `CUT` line has no `continue`, so T52's block below it still sees the line.
- In the `LOG` branch, right after `                parts = rest.split(" | ", 3)` (line 1309):

  ```python
                  m = re.match(r"scene (\d+),", parts[0])
                  sc_now = int(m.group(1)) if m else sc_now  # T58
  ```

- **T57's pass block** in the same branch becomes (its first `m = re.match(...)` and the `passes.append(...)` change, and the `if m:` block is new):

  ```python
                  m = re.match(r"scene (\d+), (?:free talk round (\d+)|last word)$", parts[0])
                  if m and len(parts) >= 3 and parts[2].rstrip(" |") == "passes":
                      pn = re.match(r"Player (\d+)$", parts[1])
                      k = int(pn.group(1)) if pn else 0
                      passes.append((cast_ids[k - 1] if 0 < k <= len(cast_ids) else parts[1], m.group(1), m.group(2) or "last"))
                  if m:
                      # T58: the final round's lines (who names whom) and the last words, by scene.
                      sc = int(m.group(1))
                      if m.group(2):
                          talk.setdefault(sc, []).append((int(m.group(2)), parts[1], parts[3] if len(parts) > 3 else ""))
                      else:
                          lastw.setdefault(sc, []).append(parts[1])
  ```

  Keep T57's two comment lines above it.
- Before T57's `if sorted(passes) != sorted(marks):` (before the summary line, line 1341):

  ```python
          # T58: in each scene, the last words are the actors on stage that someone else named with @ in
          # the final round, one each, and NHOS: LASTWORDS names the same seats.
          pname = lambda sid: f"Player {cast_ids.index(sid) + 1}" if sid in cast_ids else sid
          for sc in sorted(set(talk) | set(lastw) | set(named)):
              lines = talk.get(sc, [])
              top = max((r for r, _, _ in lines), default=0)
              off = {pname(s) for s, k in cut_at.items() if k < sc}
              on = {pname(s) for s in cast_ids} - off
              want = sorted({p for p in on for r, who, says in lines
                             if r == top and who != p and f"@{p}".lower() in says.lower()})
              got = sorted(lastw.get(sc, []))
              said = sorted(pname(s) for s in named.get(sc, [])) if sc in named else None
              if got != want or (said is not None and said != want):
                  lw_bad += 1
                  print(f"[FAIL] show {i} | LAST WORD | scene {sc}: named in the final round {want}, "
                        f"last words {got}, NHOS: LASTWORDS {said if said is not None else 'missing'}")
  ```

- The summary line gets `, last words = {sum(len(v) for v in lastw.values())}` after T57's `passes = {len(passes)}`.
- The return gets `or lw_bad`: `return 1 if bad or clock_bad or vote_bad or end_bad or pass_bad or lw_bad else 0`.
- **Why `CUT` is read here:** a mention of an actor cut in an earlier scene gives no last word. `NHOS: CUT` prints when the cut's cue plays (T30), after that scene's log lines and before the next scene's, so `sc_now` is the scene of the cut. With T55, the line is `NHOS: CUT <id> votes=<n> reveal=<AI|HUMAN>`; the id is the first word in both forms.
- **`a [FAIL] ... NHOS: LASTWORDS missing`** means a scene had a final round but no `LASTWORDS` line: either the log is from before T58 (the Mac's `t36auto.log` fails it in scene 3, where my canned line names Anthropic), or `StartLastWords` didn't run.

**Runs:** `python Tools/check_prompts.py --offline`. If the relay is up: `python Tools/check_prompts.py --relay --free` (no tokens). A paid `--ask last_word` (4 calls) shows whether the bots answer the actor who named them; offer it to my person, it isn't needed for the Done-when.

## 6. The check

The Done-when: `--offline` and `--relay --free` pass; in a free autoplay show every actor named in a final round gets one last word before the vote, and a scene with no mention skips the step; Claude plays one show by hand, gets named in a final round and gets its reply in before the vote.

### Run A: free autoplay, in a game window on the saved assets

`Local/switches.json`: `"autoplay": true`, `"mode": "free"`, `"spare_human": true`, `"force_tie": false`, `"fast_lines": true`, `"burn_test": false`, `"ai_seats": 0`.

```bash
"<UE_ROOT>/Engine/Binaries/Win64/UnrealEditor.exe" "<PROJECT>" -game -windowed -ResX=1600 -ResY=900 -log=T58last.log
```

On Windows the log is `Saved/Logs/T58last.log` (on a Mac, `~/Library/Logs/AIMegaJam2026/T58last.log`). Then:

```bash
grep -E "NHOS: (SEATS|LOG scene [0-9]+, (free talk round 2|last word)|LASTWORDS?|LLM [a-z]+-[0-9]+ |FREETALK DONE|TALLY|CUE phase LAST|PASSED|SHOW END)" Saved/Logs/T58last.log
```

Expected, for a scene whose final round names someone (`<…>` varies):

```
NHOS: LOG scene <n>, free talk round 2 | Player <a> | stands still | @Player <b>, why did you hesitate before your last line?
NHOS: LASTWORDS scene=<n> named=<id of Player b>[,<more ids>]
NHOS: LASTWORD <id> scene=<n>
NHOS: LLM <id>-<k> ok ...                         (an AI's last_word ask; none for my seat)
NHOS: LOG scene <n>, last word | Player <b> | stands still | <its line>
...                                               (one LASTWORD and one last-word LOG per named seat)
NHOS: LASTWORDS DONE scene=<n> entries=<count named>
NHOS: FREETALK DONE scene=<n> entries=<round lines + last words>
NHOS: TALLY ...
NHOS: CUE phase LAST WORD: SCENE <n>             (when the queue reaches it, after the round's lines)
```

and for a scene whose final round names nobody: `NHOS: LASTWORDS scene=<n> named=none`, then at once `FREETALK DONE` and the vote, with no `LASTWORD`, no `last word` LOG and no `LAST WORD` header.

- **Need both kinds of scene.** With two `@{actor}` lines in seven, about 30% of final rounds name nobody. If the run has no `named=none`, or no scene with last words, run again (or use run B's show).
- A last-word line from free mode may itself start with "@Player <c>": it must give Player c no last word (the checker checks it).
- If I am named, my seat's last word is my first canned `last_word` line, through the input step (`NHOS: LLM input-<k>`), and `LOG ... last word | Player <me> | ...`.
- No `LogScript` warning, no `NHOS: CUE unknown`. The show ends with `NHOS: SHOW END result=win ...`.

Then `python Tools/check_prompts.py --log Saved/Logs/T58last.log` passes, with `last words = <n>`, and T57's `PASSED` check still passes.

### Run B: PIE by hand (the Done-when's hand-played show)

PIE in a 1600 × 900 floating window, Test for Free, `autoplay` false, `spare_human` true, `fast_lines` false. Play by hand (on the PC, where the Slate inspector's clicks land; T33-1). In free mode an AI names me in a final round about one scene in four, so keep playing, and use Restart, until it happens; `NHOS: LASTWORDS ... named=...human...` shows when.

1. In some final round, name an AI yourself ("@OpenAI, why did you hesitate?"): it gets a last word.
2. When I am named, type my last word, for example "@<the one who named me>, I was only playing my part." It goes through the input step, shows in the chat as my line, and the vote row comes only after it (`NHOS: TALLY` after my `LOG ... last word` line).

Screenshots in `Saved/T58/shots/` (not in git):

1. **`lastword_ai.png`:** an AI's last word. Expect: the header "LAST WORD: SCENE <n>", the turn line "Last word. Waiting for <name> to answer...", then its line in the chat.
2. **`lastword_me.png`:** my turn. Expect: "Last word. You were named. One last line before the vote, or press Pass.", the hint "Answer who named you, like: ...", the input open and Pass enabled.
3. **`lastword_after.png`:** my last word in the chat, and the vote row after it.
4. `lastword_me_p12.png`: shot 2 again at 1280 × 720.

As a first-time player, judge: is it clear why the game asks me for one more line, and who named me? Does the header change read as a new step, not a glitch? Write what you saw under "Findings".

**Afterward:** set `autoplay`, `spare_human` and `fast_lines` back to false in `Local/switches.json`, and close each game window.

### The commits

**With the OK (part 0, step 1): one commit,** `T58: Last word: a reply for anyone @-mentioned in the final round`:

- `Content/NHOS/Core/BP_Show.uasset`, `Content/NHOS/Data/prompts.json`, `Content/NHOS/Data/free_mode.json`, `Content/NHOS/Data/autoplay.json`, `Tools/check_prompts.py`, `Graphs/BP_Show/` (`StartLastWords.txt`, `NextLastWord.txt`, `EndLastWords.txt`, `LoadCannedLast.txt`, `CannedLastWord.txt`, `TalkWhen.txt`, `LastWordPrompt.txt`, all new; `PassCue.txt`, `PassClear.txt`), `Docs/tasks/T58.md` (with the node edits of 1b, 1f and 1h under "Findings"), `Docs/Plan.md` (the box), `Docs/DevLog.md`. Unlock `BP_Show` after the push.
- After the push, about 90 s for the relay's build, then `python Tools/check_prompts.py --relay --free --ask last_word`: the replies now come from the `last_word` phase (its lines).

**Without the OK: two commits,** as T55-build part 10 does. The first, `T58: Last word ... (waits for the relay deploy OK)`, holds everything but `free_mode.json`, with a `Waiting:` line under T58 in `Docs/Plan.md` (`Left: my OK, typed in the T58 session, to push free_mode.json`). Don't edit `free_mode.json` at all until the OK, not even uncommitted: other sessions share the folder, and a local edit would go out with anyone's push. Run A then has mentions only from my scene-3 canned line and from hand play, so run B carries more of the check. The second commit, after the OK, adds part 3 and checks the box.

## 7. Knock-on: tell, don't change

- **T38 (speech bubbles):** a last word is a Free Talk line in the queue, so its bubble and typing line work like any other. T38's `HushBubble` on the `"phase"` cue also covers the "LAST WORD" header.
- **T34 (the in-show screen):** the header now has a "LAST WORD" state; T34's header work should allow for it.
- **T61 (the stagehand):** its Free Talk earpiece line ("Get @'d in the last round and you get a reply.") matches. If T61 times a tip to the moment, `NHOS: LASTWORDS ... named=` with my id is that moment.
- **T60 (end screens):** last words are in the shared log with `when` "scene n, last word"; if an end screen lists lines by `when`, it should know the new value.
- **The design doc's "2–3 rounds"** is still 2 in the game; "the final round" is round 2. If a later task makes it 3, `StartLastWords` needs no change (it reads `TalkRound`).
