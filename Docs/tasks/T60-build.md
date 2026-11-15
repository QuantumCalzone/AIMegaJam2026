# T60 build sheet: the win and lose screens

Back to [T60](T60.md). A PC prep session wrote this on 2026-11-15, without the editor. It is written against **`noHumansOnSet` at `d2d4cdc` (T52)**, with `BP_Show`, `prompts.json`, `llm.json` and `Tools/check_prompts.py` **as T54 and T55 leave them** ([T54-build.md](T54-build.md), [T55-build.md](T55-build.md)). T37 (`1d8f9ed`, on `origin` as this sheet was pushed) changed `BPC_LLMClient` and its `Graphs/` files; part 2 was checked against it. T57, T58, T62 to T66, T38 and T34 also land before T60 and change `prompts.json`, `check_prompts.py` and `BP_Show`. So every place below is named by its text first; line numbers are "at `d2d4cdc`". Find each line by its text before you change it.

The design doc was read, not changed: Rules tab rev 42 (the paragraph after The Cut: "The win screen shows every AI's reasoning, then reveals their rivals. If you're cut, you lose: ... the lose screen shows every AI's reasoning about you, names the reason that got the most votes, and offers an instant restart."; the Onboarding table's Lose screen row, on screen "'YOU: HUMAN', then each AI's reason", and its Win screen row; "The lose screen does the most teaching"), Bot Prompts rev 82 (the opening-prompt block already says "Silence is evidence, and so is a line that sounds too polished"; the Rivals table) and Tech & Build rev 25 (build list: "Win and lose screens with the AIs' reasoning (the top reason on a loss, the rivals on a win), plus instant restart"). The reply format ("How to reply" in `prompts.json` `game`) is not in the doc, so the new `tell` field needs **no doc edit**. Question 3 may change the lose screen's title to the doc's words; that is a game change, not a doc change.

## In short

- **The top reason** (my person's answer to T60's question: each vote names its tell):
  - **`llm.json` `reply_schema`** gets a `tell` field: a string whose enum is `""` and eight tell ids. It is required, like every field (strict schemas need that), so every ask fills it; only a vote fills it with a tell.
  - **`Content/NHOS/Data/tells.json`** (new) lists the tells in priority order, with what each means and its lose-screen line ("They caught you copying late.").
  - **`prompts.json`:** one new `"tell"` line under How to reply in `game`, the vote ask asks for it, the input converter leaves it empty, `_readme` names it.
  - **The tell reaches `BP_Show`** through the LLM client (question 1): the client keeps the reply's `tell` in a new `RTell`, free mode pairs a tell with each pre-written vote reason, and `BP_Show` stores each vote's tell when it stores the vote (`StoreTell`).
  - **`BP_Show.TopReason`** (new) counts the tells of the votes that cut me and sets `TopLine`; it prints `NHOS: TELL <voter> tell=<tell> | <reason>` per counted vote and `NHOS: TOP REASON <tell> votes=<n>`.
- **The rivals:** `BP_Show.RevealRivals` (new) reads `rival` from `personas.json` for each AI seat, puts the rival's provider name on that AI's card ("Rival: Anthropic") and prints `NHOS: RIVALS <id>=<id> ...`.
- **`BP_Show.EndReveal(Screen)`** (new) runs one or the other; `ShowEndScreen` calls it with one node after its cards are in. `ShowEndScreen` keeps T54's `reason=` in `SHOW END` and T54's win subtitle.
- **`WBP_EndScreen`:** a `ReasonText` line (UIStyle `Header`, `Gold`) between the cards and Play Again; `SetReason(Reason)` and `SetRival(Name, Rival)`; `AddCard` keeps each card. **`WBP_EndCard`:** a `RivalTitle` and `RivalText` at the bottom of the card, collapsed until `SetRival(Rival)`.
- **`Tools/check_prompts.py`:** the files agree on the tells; a vote reply must name a tell; `--log` checks `TOP REASON` against the `TELL` lines on a loss and `RIVALS` against `personas.json` on a win.
- **Runs:** `--offline`, `--relay --free` and a paid run of every ask (**it needs my person's OK, asked in the T60 session**); free autoplay shows for a loss, a win and a 4-actor win; PIE screenshots and Restart from each screen; Claude plays one loss and one win by hand.

## Questions for my person

Ask each with the multiple-choice tool, one at a time, before part 1. The recommended answer is first.

1. **How the tell gets from the reply to `BP_Show`.** The reply reaches `BP_Show` through `BPC_LLMClient`'s `OnAnswer`, which passes only speech, vote, reason, pass and the actions. T60's Touches don't name the client.
   - **Widen T60's Touches to `BPC_LLMClient` and `free_mode.json` (Recommended).** The client reads `tell` into a new `RTell` (two node edits, `ParseFields` and `ClearReply`); free mode's vote phase gets a `tells` list, one per pre-written reason, and `FreeReply` sets `RTell` from it. `BP_Show` reads `LLMClient.RTell` when it stores a vote. Test for Free then names a top reason that fits the reasons on screen. Costs: the `BPC_LLMClient` lock (the Mac's T37 held it and pushed `1d8f9ed`; check `git lfs locks`), the PC's editor must have T37's `BPC_LLMClient` loaded (closed, pulled and reopened, as the dispatcher's ledger says), and the push of `free_mode.json` redeploys the relay, so it needs my person's OK typed in the T60 session (T58 found the same). The relay's code doesn't change and its free mode sends no `tell`, which the checker allows for `--free`.
   - No client change: `BP_Show` parses the client's raw reply text (`HText`) for `tell` itself. No new lock and no relay push, but Test for Free has no tells, so every free show's lose screen says the `other` line ("They caught you, each for a reason of their own."). The free autoplay loss would show the line but couldn't show a real top reason.
2. **The tells and their lines.** T60's task lists `note`, `late_copy`, `silence`, `polish`, `human_slip`, `no_persona` and `other` ("such as"). The game prompt's "Spotting the human" also names the scene card (playing your role and want), so the sheet adds `role`.
   - **These eight, in this priority order, with these lines (Recommended):** `late_copy` "They caught you copying late." (the doc's example), `note` "They caught you guessing at the director's note.", `silence` "They caught you going quiet.", `polish` "They caught you sounding too polished.", `human_slip` "They caught you sounding a little too human.", `no_persona` "They caught you without a persona of your own.", `role` "They caught you drifting out of your role.", `other` "They caught you, each for a reason of their own." A tie for the top goes to the one listed first.
   - The task's seven (no `role`), with the same lines; a vote about the role or the want becomes `other`.
3. **The lose screen's title.** T33 built "YOU'RE CUT" on the red plate. The doc's Lose screen row says the screen shows "YOU: HUMAN", then each AI's reason.
   - **"YOU: HUMAN", as the doc says (Recommended).** It is the reveal stamp's own words, seconds earlier, so the end screen picks up where the cut left off. The plate stays red with white letters.
   - Keep "YOU'RE CUT".
4. **Where the rivals show on the win screen.**
   - **On each AI's card, under its reasons: a "Rival" heading and the rival's name, such as "Anthropic" (Recommended).** The card already holds that AI's reasoning, so each card reads reasoning first, then its rival, and no new block competes with the result plate. T33's cards already scroll at 1280 × 720.
   - One block under the cards: "OpenAI and Anthropic were rivals. SpaceXAI and Meta were rivals."

## Decisions this sheet makes (open to change)

The T60 session shows this list to my person when it closes the task.

1. **The votes that count** are the votes for my seat in the scene I was cut: `HistScene` = `CutScene[HumanSeat]` and `HistTarget` = `HumanSeat` (T60 step 1: "the votes that cut me"). My own vote never counts (I can't vote for myself).
2. **A tie for the top tell goes to the tell listed first in `tells.json`.** `other` is last, so it wins only when nothing else has as many votes. A vote with an empty or unknown tell (a failed reply) counts as `other`.
3. **No top reason when nothing is counted** (for example every vote failed): `NHOS: TOP REASON none votes=0`, and the line stays hidden.
4. **The top reason shows on every loss, not only the first show.** The doc puts it in the earpiece column too; T61's earpiece line says it again on a first show (T61-build, decision 5).
5. **A bot whose rival isn't in this show** (a 4-actor show) still shows its rival, as "SpaceXAI (not in this show)". The doc: "If the rival isn't on stage, the bot simply has no one to lean toward." Only the bots in this show get a line (T60 step 3).
6. **The rivals show at once,** with the cards. A timed reveal (the rival lines fading in after a beat) is polish for later.
7. **Each vote's tell is printed** (`NHOS: TELL ...`) next to its reason, so the check can compare the two, and `--log` can recount the top reason.
8. **`StoreClosing` doesn't change.** The closing vote also carries `tell` (the schema requires it), but nothing reads it.

## Wording that comes from the task or the doc

- **The lose line** is one of `tells.json`'s lines (question 2); "They caught you copying late." is the doc's example, word for word.
- **The `game` tell line** (part 1c) is new wording; its tells paraphrase "Spotting the human" and the doc's opening-prompt lines (copying a turn late, matching only the category, silence, too polished, human slips, no persona, role and want).
- **The rival line** on a card: the heading "Rival" and the rival's provider name, the name I see (`personas.json` `name`).

## 0. Before you start (after T54 and T55 are pushed)

1. `git log --oneline -15` shows T54, T55 and the chain tasks the plan puts before T60. `git lfs locks` shows no lock on `BP_Show.uasset`, `WBP_EndScreen.uasset` or `WBP_EndCard.uasset` (and, with question 1's first answer, `BPC_LLMClient.uasset`). Claim T60 and lock those assets.
2. **Ask the four questions** above. With question 1's first answer, change T60's **Touches** in `Docs/Plan.md` in a `Plan: T60 touches the LLM client and free mode` commit: add `Content/NHOS/Core/BPC_LLMClient.uasset` (`ParseFields`, `ClearReply`, `FreeReply`), `Content/NHOS/Data/free_mode.json` (the vote phase's `tells`) and `Content/NHOS/Data/tells.json` (new). With the second answer, add only `tells.json`. Then ask for the `free_mode.json` OK now, with the multiple-choice tool: "Push free_mode.json with T60 (Recommended)": the push redeploys the relay, but no reply the relay sends changes; or "Not now" (then T60 pushes without `free_mode.json` and waits, as T55 did).
3. **Read the findings** of `T54.md` (the `ShowEndScreen` edits: the win subtitle from `WinLine`, `reason=` in `SHOW END`), `T55.md` (`ShowEndScreen`'s ", after the Director broke a tie." removed; any branch on how a cut happened) and of T57, T58, T34 for anything they changed in `ShowEndScreen`, `StoreVote`, `RecordVotes` or the end screen widgets. T58: last words are in the shared log with `when` "scene n, last word"; the cards list votes, not log lines, so nothing changes.
4. `python Tools/check_prompts.py --offline` passes before you start.
5. **Survey, in this order** (each a separate `call_tool`; tool calls stop at about 120 s; read only, never write a read-back):
   1. `BlueprintTools.read_graph_dsl` of **`ShowEndScreen`**, saved to `Saved/T60/ShowEndScreen.read.txt` (big: T10's write took 34 s). Record: the `Create Widget` node of `WBP_EndScreen` and where its return value goes (a variable such as `EndScreen`, which `RestartShow` removes, or only pins); the loop that calls `AddCard` and the exec node after its `Completed` pin; the `Name` source of `AddCard` (expected `SeatLabel[s]`, the provider name; `RevealRivals` must pass the same); the `Setup` call's `Title` source (expected a `Select` on `ShowWin` between "YOU WIN" and "YOU'RE CUT"); the `NHOS: SHOW END` print. Expected order: cards, `Setup`, `Add to Viewport`, the print.
   2. `read_graph_dsl` of **`StoreVote`** (`Saved/T60/StoreVote.read.txt`). Record: how it finds the voter's seat (from the ask's `Tag`, `vote-<seat>`?), and the node that stores the reason by seat (a `Set Array Elem` on an array such as `VoteReasons`, or an `Add`). Check whether the human's ballot goes through `StoreVote` too (search `find_nodes` for `K2Node_CallFunction` titled `StoreVote`), or through its own function. **Check that `StoreVote` runs inside `OnAnswer`'s call** (`OnAnswer` → `HandleReply` → `StoreVote`, T09), not later from a timer or `BPC_LinePlayer`'s queue: `StoreTell` reads the client's `RTell`, which the next reply overwrites. If it runs later, read `RTell` in the `OnAnswer` handler, where `Vote` and `Reason` are stored, into a new `BP_Show` variable `ReplyTell`, and have `StoreTell` read `ReplyTell`.
   3. `read_graph_dsl` of **`RecordVotes`** (`Saved/T60/RecordVotes.read.txt`). Record the element types of `HistScene`, `HistVoter`, `HistTarget` (Integer seats, as T10's "a vote for my seat is marked (you)" suggests, or ids or names) and `HistReason`. Part 2e's DSL assumes Integer seats; if they hold ids, compare with `(get (V SeatId) (V HumanSeat))` by `streq` instead.
   4. `read_graph_dsl` of **`StoreClosing`** (`Saved/T60/StoreClosing.read.txt`): it must not add to the `Hist*` arrays (if it does, `TopReason` would count closing votes in the last scene; then also filter on an index below the closing's first entry). Expected (T10): it stores the closing vote and reason in arrays of its own and calls `ShowEndScreen` once, after the last answer.
   5. `find_nodes` in `BP_Show` for `K2Node_VariableGet` titled `Get ShowNum`, `Get CutScene`, `Get SeatLabel`, `Get AllPersonas`, `Get LLMClient` (all exist at `d2d4cdc`: `RestartShow`, T10; `DrawCast.txt`; `ShowLine.txt`). `ObjectTools.list_properties` on `BP_Show` for the type name of `AllPersonas`' elements (a JSON object); part 2's `TellObjs` uses the same type.
   6. **`WBP_EndScreen` and `WBP_EndCard` widget trees** (the UMG toolset from `list_toolsets`; T33 built them with it): the root `VerticalBox` of the end screen, the slot that holds `CardsGrid` (and its `ScrollBox`, if any) and the button row; the card's `VerticalBox` and the slot paddings of `ClosingTitle` and `ClosingText`; the designer text of `VotesTitle` and `ClosingTitle` (so "Rival" matches their form).
   7. With question 1's first answer: `read_graph_dsl` of `BPC_LLMClient`'s **`ParseFields`** and **`ClearReply`** (no files): where `reason` is read from the reply object into `RReason`, and where `ClearReply` empties `RReason`.

## 1. The data files

### 1a. `Content/NHOS/Data/tells.json` (new)

With question 2's first answer. With the second, drop the `role` entry, and `role` from 1b's enum and 1c's line.

```json
{
	"_readme": [
		"The tells (T60): the kinds of evidence a vote can name. Every vote reply fills 'tell' with one of these ids: llm.json reply_schema 'tell', whose enum is \"\" and then these ids, in this order. prompts.json 'game' explains each one to the AIs in its '\"tell\"' line under How to reply.",
		"When the human is cut, the lose screen counts the tells of the votes that cut them and shows the top one's 'line' (BP_Show.TopReason). A tie for the top goes to the tell listed first here, so 'other' is last. 'means' is for people reading this file; no AI reads this file.",
		"Each line follows the game's legibility rules: one plain sentence, 15 words at most, no brackets, emoji or all-caps words. Tools/check_prompts.py checks this file against llm.json, prompts.json and free_mode.json."
	],
	"tells": [
		{"id": "late_copy", "means": "copied the others a turn late", "line": "They caught you copying late."},
		{"id": "note", "means": "only matched the note's category, or missed the note", "line": "They caught you guessing at the director's note."},
		{"id": "silence", "means": "passed or went quiet", "line": "They caught you going quiet."},
		{"id": "polish", "means": "lines too smooth or polished for a bot", "line": "They caught you sounding too polished."},
		{"id": "human_slip", "means": "hunger, sleep, feelings or family as their own, or a dodged question", "line": "They caught you sounding a little too human."},
		{"id": "no_persona", "means": "no clear persona of their own, or a flat copy of another's", "line": "They caught you without a persona of your own."},
		{"id": "role", "means": "didn't play their role or chase their want", "line": "They caught you drifting out of your role."},
		{"id": "other", "means": "anything else", "line": "They caught you, each for a reason of their own."}
	]
}
```

`DefaultGame.ini` stages all of `Content/NHOS/Data` as loose files, so a build carries the new file with no config change.

### 1b. `llm.json`

**a. `reply_schema`, lines 40 to 44.** Add `tell` after `pass`, and to `required`:

```json
			"pass": {
				"type": "boolean"
			},
			"tell": {
				"type": "string",
				"enum": ["", "late_copy", "note", "silence", "polish", "human_slip", "no_persona", "role", "other"]
			}
		},
		"required": ["actions", "speech", "vote", "reason", "pass", "tell"],
```

If T62 to T66 changed `actions` (Look around, No action), keep their change; `tell` is only added.

**b. `_readme`, line 2.** After `unused fields come back empty.` add: ` A vote also fills 'tell', one id from tells.json: the kind of evidence its reason gives (T60). Every other ask leaves it "".` (escape the quotes as `\"\"` in the file). T55 removed the Director and "tiebreak" from the same sentence's list; keep its words.

### 1c. `prompts.json`

Each line as it sits in the file (two tabs before it).

**a. `game`, How to reply: a new line after the `"reason"` line** (line 70, `"- \"reason\": one sentence, in character, in plain words, when the ask wants a reason: ..."`), before the line that starts `"- Call actors by their Player names`:

```
		"- \"tell\": with a vote, the kind of evidence your reason gives, one of: late_copy (copied the others a turn late), note (only matched the note's category, or missed the note), silence (passed or went quiet), polish (sounded too smooth for a bot), human_slip (a human slip, such as hunger, sleep or feelings), no_persona (no clear persona of its own), role (ignored its role or want), other (anything else). Leave it \"\" for every other ask.",
```

The line above How to reply's list ("Fill only the fields the ask names, and leave the others empty ...") already covers `tell` for the other asks.

**b. `asks.vote`, line 126.** Now: `"vote": "The Cut. Vote in secret for the actor you think is the human. Fill: vote (one name from options) and reason (why, in one sentence, in character). Everyone sees your reason after the vote.",`. New:

```
		"vote": "The Cut. Vote in secret for the actor you think is the human. Fill: vote (one name from options), reason (why, in one sentence, in character) and tell (the kind of evidence your reason gives). Everyone sees your reason after the vote.",
```

"The Cut" stays first, so free mode's vote phase (`ask_contains` "The Cut") still finds it. If T57 or T58 changed this ask, add only ", ... and tell (the kind of evidence your reason gives)" to its Fill list.

**c. `input`, line 109.** Now: `"- \"vote\" and \"reason\" are always \"\". \"pass\" is false unless the free talk rule says otherwise."`. New: `"- \"vote\", \"reason\" and \"tell\" are always \"\". \"pass\" is false unless the free talk rule says otherwise."`. If T63 or T64 rewrote the input prompt (spelling only), add `tell` to whichever rule says which fields stay empty.

**d. `_readme`, line 9.** Now: `"Every reply matches llm.json 'reply_schema': actions [{verb, target, item}], speech, pass, vote, reason. Unused fields come back empty. ..."`. Make its start `"Every reply matches llm.json 'reply_schema': actions [{verb, target, item}], speech, pass, vote, reason, tell. Unused fields come back empty. A vote's tell is one id from tells.json (T60)."` and keep the rest of the line.

**`asks.closing` doesn't change:** the closing vote fills `tell` or leaves it empty, and nothing reads it (decision 8).

### 1d. `free_mode.json` (question 1's first answer; pushed only with the OK)

**a. The `vote` phase, lines 39 to 49.** After its `reasons` list, add `tells`, one per reason at the same index:

```json
			"reasons": [
				"{vote} paused before every line, like someone thinking for real.",
				"{vote} picked up the {prop} like it had feelings about it.",
				"{vote} never mentioned an upgrade once. No robot does that.",
				"{vote} laughed at the wrong moment. Very human of them.",
				"{vote} wandered to the {place} for no reason at all."
			],
			"tells": ["silence", "human_slip", "no_persona", "human_slip", "role"]
```

If an earlier task changed the reasons, pair each new reason with the tell it names. `closing` and `tiebreak` (gone after T55) get none.

**b. `_readme`, line 6.** After `'echo_typed' (the input step: speech = the player's typed text, cut to 15 words).` add ` 'tells' (vote only, T60): the tell of each reason, at the same index, from tells.json.`

**The relay:** no file in `Relay/` changes. `freeReplyObject` ignores `tells`, and its replies have no `tell`; the checker allows that for `--free` (part 5c). A later task that touches the relay with a deploy OK can add `tell` to its free replies (a follow-up, part 8).

## 2. `BPC_LLMClient` (question 1's first answer)

| Graph | File | T60 changes | How |
|---|---|---|---|
| `ParseFields` | none | reads `tell` into `RTell` | Node edit (2b) |
| `ClearReply` | none | empties `RTell` | Node edit (2b) |
| `FreeReply` | `Graphs/BPC_LLMClient/FreeReply.txt` | sets `RTell` from the vote phase's `tells` | DSL write (2c) |
| `Deliver`, `OnAnswer` | `Deliver.txt` | nothing: `OnAnswer` keeps its pins | — |

### 2a. Variables

`RTell` (String), `FreeIdx` (Integer, 0). `OnAnswer` keeps its signature: changing a dispatcher's pins leaves `BP_Show`'s bound event stale (T18). `BP_Show` reads `RTell` instead, while `OnAnswer` runs: `Deliver` calls it right after the reply is parsed (T37's `BackstageNote` runs just before it and doesn't touch the reply fields), and `BP_Show`'s handler runs `StoreVote` before it returns (T09), so `RTell` is still this reply's.

### 2b. `ParseFields` and `ClearReply`: node edits

Write each under "Findings" in `T60.md`, since neither graph has a file.

- **`ParseFields`:** next to the nodes that read `reason` from the reply object into `RReason` (a `HasField`/`GetField` pair on "reason", survey 7), add the same for "tell": `Json|HasField <obj> "tell"`, a `Branch` on it, `Json|GetField <obj> "tell"`, `Set RTell`. With no `tell` field (an old reply, the relay's free mode), `RTell` stays "" from `ClearReply`. Don't fail the parse on a missing `tell`.
- **`ClearReply`:** after `Set RReason ""`, add `Set RTell ""`.

### 2c. `FreeReply` (file)

In `Graphs/BPC_LLMClient/FreeReply.txt`, replace the vote branch's reason pick (from `    (bind _rs (Json|GetField (V FreePhase) "reasons"))` through `      (set RReason _rf))`) with:

```lisp
    (bind _rs (Json|GetField (V FreePhase) "reasons"))
    (set TmpArr2 _rs)
    (if (> (len (V TmpArr2)) 0)
      (set FreeIdx (Math|Random|RandomIntegerinRange 0 (- (len (V TmpArr2)) 1)))
      (set TmpStr (get (V TmpArr2) (V FreeIdx)))
      (bind _rf (CallFunction|FreeFill :Text (V TmpStr)))
      (set RReason _rf)
      ; T60: the vote's tell, from the phase's 'tells' at the same index (free_mode.json). The closing phase has none.
      (bind _ht (Json|HasField (V FreePhase) "tells"))
      (if _ht
        (bind _ts (Json|GetField (V FreePhase) "tells"))
        (set TmpArr _ts)
        (if (> (len (V TmpArr)) (V FreeIdx))
          (set RTell (get (V TmpArr) (V FreeIdx))))))
```

The `(return)` after it stays. `TmpArr` held the options a few lines up; they are used by then. Since T37 (`1d8f9ed`), `FlushLocal` calls `ClearReply` before each `FlushOne`, which calls `FreeReply` and then `Deliver`, so a phase without `tells` leaves `RTell` "". T37's `error_test` failure path (`ErrorTestFail`) delivers a failed reply, and `Deliver` clears it first. Expand with `Tools/dslpp.py` (a `;;; GRAPH FreeReply` line first) and write it with `write_graph_dsl`. Compile, save, and unlock `BPC_LLMClient.uasset` after the push.

### 2d. With question 1's second answer instead

No client change. `StoreTell` (part 3c) reads the raw reply instead of `RTell`; replace its `_t` bind with:

```lisp
  (set TellNow "")
  (bind (_o _ok) (Json|LoadJsonfromString (Class|BPCLLMClient|GetHText :self (Variables|Default|GetLLMClient))))
  (if _ok
    (bind _h (Json|HasField _o "tell"))
    (if _h
      (bind _tv (Json|GetField _o "tell"))
      (set TellNow _tv)))
```

and store `(V TellNow)`. `HandleHttp` sets `HText` to "" before each parse and to the reply text on success, so a failed or free reply gives "" (counted as `other`). Skip part 1d and 5b's free-mode check.

## 3. `BP_Show`

### 3a. Which graphs, which have files

| Graph | File in `Graphs/BP_Show/` | T60 changes | How |
|---|---|---|---|
| `StoreTell(Seat)` | new | — | DSL write (3c) |
| `LoadTells` | new | — | DSL write (3d) |
| `TopReason` | new | — | DSL write (3e) |
| `RevealRivals(Screen)` | new | — | DSL write (3f) |
| `EndReveal(Screen)` | new | — | DSL write (3g) |
| `StoreVote` | none | one `StoreTell` call | Node edit (3h) |
| `ShowEndScreen` | none (T54, T55 edited nodes) | one `EndReveal` call; the lose title (question 3) | Node edits (3i) |
| `StoreClosing`, `RecordVotes` | none | nothing (survey only) | — |
| `RunCue` | `RunCue.txt` | nothing: the `"end"` cue runs `EndCheer` and `ShowEndScreen` | — |
| `RestartShow` | none | nothing: it removes the end screen and starts a new show; `StoreTell` clears on a new `ShowNum` | — |

Create the five functions with `add_function_graph` and their inputs with `add_function_param` (no `container_type` for a single value, T33), compile, then write each file. Create them callee first (`LoadTells`, `StoreTell`, `TopReason`, `RevealRivals`, then `EndReveal`), and compile `WBP_EndScreen` with its new functions (part 4) before writing `RevealRivals` and `EndReveal`, which call them. Write the call nodes in `StoreVote` and `ShowEndScreen` last (T18: a call node goes stale when its function gets a new parameter).

### 3b. New variables

| Variable | Type | Default | Used by |
|---|---|---|---|
| `TellScene`, `TellVoter` | Integer array | empty | `StoreTell`, `TopReason` |
| `TellText` | String array | empty | `StoreTell`, `TopReason` |
| `TellShow` | Integer | -1 | `StoreTell` (clears the three at a new show) |
| `TellIds`, `TellLines` | String array | empty | `LoadTells`, `TopReason` |
| `TellObjs` | array of the JSON object type `AllPersonas` holds (survey 5) | empty | `LoadTells` |
| `TellCounts` | Integer array | empty | `TopReason` |
| `TellTmp`, `TellNow`, `TopTell`, `TopLine` | String | "" | `LoadTells`, `TopReason`, `EndReveal` |
| `TellIdx`, `TopCount`, `TopScene` | Integer | 0 | `TopReason` |
| `RivalId`, `RivalName`, `RivalShown`, `PersonaTmp` | String | "" | `RevealRivals` |
| `RivalSeat` | Integer | 0 | `RevealRivals` |
| `RivalPairs` | String array | empty | `RevealRivals` |

`TopLine` stays set after the end screen: T61's earpiece reads it for its lose line (T61-build part 0 step 4).

### 3c. `StoreTell` (new)

`Graphs/BP_Show/StoreTell.txt`:

```lisp
; T60: keeps each vote's tell, the kind of evidence its reason gives (llm.json reply_schema 'tell'), with its
; scene and voter seat. StoreVote calls it where it stores the vote's reason. OnAnswer runs StoreVote at once,
; so the LLM client still holds this reply's tell (RTell). A new show (ShowNum) starts the lists again.
; TopReason matches these entries to the vote history (HistScene, HistVoter), which RecordVotes fills at the cut.
(fn StoreTell (Seat)
  (if (not (== (V TellShow) (V ShowNum)))
    (clear (V TellScene))
    (clear (V TellVoter))
    (clear (V TellText))
    (set TellShow (V ShowNum)))
  (bind _t (Class|BPCLLMClient|GetRTell :self (Variables|Default|GetLLMClient)))
  (add (V TellScene) (V SceneNum))
  (add (V TellVoter) Seat)
  (add (V TellText) (select (== Seat (V HumanSeat)) "" _t)))
```

- It keeps its own lists instead of adding a `HistTell` to `RecordVotes` and `StartScene` (no files), so only `StoreVote` gets a node.
- `Class|BPCLLMClient|GetRTell` reads another Blueprint's variable, as `WBP_EndScreen` reads `Class|BPShow|GetStage` (T33). If the DSL can't resolve it, place a `Get RTell` node on the `LLMClient` reference by hand and note it under "Findings".
- The `select` keeps the human's ballot empty if it runs through `StoreVote` (survey 2). My votes never count anyway.

### 3d. `LoadTells` (new)

`Graphs/BP_Show/LoadTells.txt`:

```lisp
; T60: the tells a vote can name, in priority order, with the lose screen's line for each
; (Content/NHOS/Data/tells.json). TopReason calls it at the end of a show the human lost.
(fn LoadTells ()
  (clear (V TellIds))
  (clear (V TellLines))
  (bind _cdir (Utilities|Paths|GetProjectContentDirectory))
  (bind (_o _ok) (Json|LoadJsonfromFile (Utilities|Struct|MakeFilePath (cat _cdir "NHOS/Data/tells.json"))))
  (if (not _ok)
    (print "NHOS: TELLS missing Content/NHOS/Data/tells.json")
    (return))
  (bind _ts (Json|GetField _o "tells"))
  (set TellObjs _ts)
  (for _t (V TellObjs)
    (bind _id (Json|GetField _t "id"))
    (set TellTmp _id)
    (add (V TellIds) (V TellTmp))
    (bind _ln (Json|GetField _t "line"))
    (set TellTmp _ln)
    (add (V TellLines) (V TellTmp))))
```

The load follows `BPC_LinePlayer/LoadPacing.txt` (path) and `BPC_LLMClient/FreeReply.txt` (an object array from `GetField`, then `for`). Only a `for` follows the `if ... (return)`, so T30's join problem doesn't arise.

### 3e. `TopReason` (new)

`Graphs/BP_Show/TopReason.txt`:

```lisp
; T60: the lose screen's top reason. Counts the tells of the votes that cut the human (the votes for HumanSeat
; in the scene it was cut, from the vote history), and sets TopLine to the line of the most common one
; (tells.json). A tie goes to the tell listed first; an empty or unknown tell counts as other. Prints one TELL line
; per counted vote, then TOP REASON. None of these ifs has a return, so each one joins the next (T30).
(fn TopReason ()
  (CallFunction|LoadTells)
  (clear (V TellCounts))
  (for _k (range (len (V TellIds)))
    (add (V TellCounts) 0))
  (set TopTell "none")
  (set TopCount 0)
  (set TopLine "")
  (set TopScene (get (V CutScene) (V HumanSeat)))
  (for _i (range (len (V HistTarget)))
    (if (and (== (get (V HistScene) _i) (V TopScene)) (== (get (V HistTarget) _i) (V HumanSeat)))
      (set TellNow "other")
      (for _j (range (len (V TellText)))
        (if (and (== (get (V TellScene) _j) (V TopScene)) (== (get (V TellVoter) _j) (get (V HistVoter) _i)))
          (set TellNow (get (V TellText) _j))))
      (set TellIdx (Utilities|Array|FindItem (V TellIds) (V TellNow)))
      (if (< (V TellIdx) 0)
        (set TellNow "other")
        (set TellIdx (Utilities|Array|FindItem (V TellIds) "other")))
      (if (>= (V TellIdx) 0)
        (Utilities|Array|SetArrayElem (Variables|Default|GetTellCounts) (V TellIdx) (+ (get (V TellCounts) (V TellIdx)) 1)))
      (print (cat "NHOS: TELL " (get (V SeatId) (get (V HistVoter) _i)) " tell=" (V TellNow) " | " (get (V HistReason) _i)))))
  (for _k (range (len (V TellIds)))
    (if (> (get (V TellCounts) _k) (V TopCount))
      (set TopCount (get (V TellCounts) _k))
      (set TopTell (get (V TellIds) _k))
      (set TopLine (get (V TellLines) _k))))
  (print (cat "NHOS: TOP REASON " (V TopTell) " votes=" (str (V TopCount)))))
```

- `(Utilities|Array|SetArrayElem (Variables|Default|GetTellCounts) ...)` is the form `StagePrep.txt` uses. `FindItem` is in `HandleHttp.txt`. Nested `if`s inside a `for` are in `FreeReply.txt`.
- `>` (not `>=`) keeps the first tell on a tie (decision 2).
- If survey 3 found `HistVoter` and `HistTarget` hold ids, not seats: compare `(streq (get (V HistTarget) _i) (get (V SeatId) (V HumanSeat)))`, store `(get (V SeatId) Seat)` in `StoreTell` (make `TellVoter` a String array) and compare voters with `streq`; the `TELL` print then uses `(get (V HistVoter) _i)` as it is.
- `CutScene[HumanSeat]` is set by `CutActor` (T10). If T52's `TieCut` or anything else changed that, use `SceneNum` instead: the show ends in the scene I was cut.

### 3f. `RevealRivals` (new)

`Graphs/BP_Show/RevealRivals.txt`:

```lisp
; T60: the win screen's rivals (the Rules tab: "The rivals are revealed at the end"). For each AI seat, its persona's
; 'rival' (personas.json, T56) goes on that AI's card by the name the player sees: the rival's provider name,
; with "(not in this show)" when the rival has no seat. Prints NHOS: RIVALS <id>=<rival id> for each AI seat.
(fn RevealRivals (Screen)
  (clear (V RivalPairs))
  (for _s (range (V SeatCount))
    (if (not (== _s (V HumanSeat)))
      (set RivalId "")
      (set RivalName "")
      (for _p (V AllPersonas)
        (bind _pid (Json|GetField _p "id"))
        (set PersonaTmp _pid)
        (if (streq (V PersonaTmp) (get (V SeatId) _s))
          (bind _rv (Json|GetField _p "rival"))
          (set RivalId _rv)))
      (for _q (V AllPersonas)
        (bind _qid (Json|GetField _q "id"))
        (set PersonaTmp _qid)
        (if (streq (V PersonaTmp) (V RivalId))
          (bind _qn (Json|GetField _q "name"))
          (set RivalName _qn)))
      (set RivalSeat (Utilities|Array|FindItem (V SeatId) (V RivalId)))
      (set RivalShown (select (>= (V RivalSeat) 0) (V RivalName) (cat (V RivalName) " (not in this show)")))
      (if (not (Utilities|String|IsEmpty (V RivalName)))
        (Class|WBPEndScreen|SetRival :self Screen :Name (get (V SeatLabel) _s) :Rival (V RivalShown))
        (add (V RivalPairs) (cat (get (V SeatId) _s) "=" (V RivalId))))))
  (print (cat "NHOS: RIVALS " (Utilities|String|JoinStringArray (V RivalPairs) " "))))
```

- `AllPersonas` holds every persona from `personas.json` (`DrawCast` fills it once, before the draw filters `PersonaArr`), so a rival with no seat still has its name.
- `Name` must be what `ShowEndScreen` passes to `AddCard` (survey 1; expected `SeatLabel[s]`). If it passes something else, pass the same here.
- `SeatCount` is the seat count T54's `SetWinReason` loops over. `Screen` is an object reference to `WBP_EndScreen`.

### 3g. `EndReveal` (new)

`Graphs/BP_Show/EndReveal.txt`:

```lisp
; T60: the end screen's reveal, after its cards are in. A loss names the top reason (TopReason, from the votes that
; cut the human) in one large line; a win reveals each AI's rival (RevealRivals). ShowEndScreen calls it once.
(fn EndReveal (Screen)
  (set TopLine "")
  (if (V ShowWin)
    (CallFunction|RevealRivals :Screen Screen)
    (else
      (CallFunction|TopReason)
      (Class|WBPEndScreen|SetReason :self Screen :Reason (V TopLine)))))
```

### 3h. `StoreVote`: one call

Node edit, no file. Put a `CallFunction|StoreTell` node in the exec chain right after the node that stores the vote's reason by seat (survey 2), with `Seat` from the same pin that gives that node its index. If the reason is stored on two paths (a good reply and a failed one), call it on both; a failed reply's `RTell` is "" (`Deliver` calls `ClearReply` first). Write the edit under "Findings".

### 3i. `ShowEndScreen`: node edits

T54 and T55 edited it; read their findings first. Keep every edit small.

1. **The reveal call.** Put a `CallFunction|EndReveal` node in the exec chain after the `AddCard` loop's `Completed` and before the `NHOS: SHOW END` print, so `TOP REASON` and `RIVALS` print first. Its `Screen` pin takes the end screen: the variable the `Create Widget` result is stored in, or the `Create Widget` node's return value (survey 1). It may go before or after `Add to Viewport`; the widget is built either way.
2. **The lose title** (question 3, first answer): the literal "YOU'RE CUT" in the `Setup` call's `Title` source becomes "YOU: HUMAN". "YOU WIN" stays (T54's answer 1).
3. **Keep:** T54's win subtitle (`WinLine`), the lose subtitle, ` reason=` in the `SHOW END` line (the checker reads it), and `Phase` = "end". If a branch on how a cut happened is still there (T55's knock-on), it can go.

Write each edit under "Findings", with the old and new title.

Compile `BP_Show` with warnings as errors; the editor log after the compile has no `LogBlueprint: Error`. Close every game window before you save (T53).

## 4. `WBP_EndScreen`

### 4a. The widget tree

Add one `TextBlock`, **`ReasonText`**, to the root `VerticalBox` (survey 6), between the slot that holds the cards (`CardsGrid`, or the `ScrollBox` around it) and the button row:

- Slot: auto size (not fill), horizontal alignment Center, padding top 24 (`S5`), bottom 16 (`S4`), left and right 0.
- Text "", `AutoWrapText` on, justification Center, visibility **Collapsed**, `bIsVariable` on.
- Font and color come from the graph (4b), not the designer.

The cards' slot keeps Fill, so at 1280 × 720 the cards shrink and scroll and the reason line keeps its height. **No other widget changes.**

### 4b. Graphs

**`Graphs/WBP_EndScreen/EventGraph.txt`:** in `EventPreConstruct`, after the two `AisTitle` lines (`(Class|Text|SetColorandOpacity :self (Variables|WBP_EndScreen|GetAisTitle) ...)`), add:

```lisp
  (Class|Text|SetFont :self (Variables|WBP_EndScreen|GetReasonText) :Font (Class|UIStyle|UIFont :Role "Header"))
  (Class|Text|SetColorandOpacity :self (Variables|WBP_EndScreen|GetReasonText) :ColorAndOpacity (Utilities|Struct|MakeSlateColor :SpecifiedColor (Class|UIStyle|UIColor :Role "Gold")))
```

`Header` is 32 pt bold with the ink outline (larger than the 24 pt card titles, smaller than the 72 pt result); gold on ink measured 10.2:1 in T33 ("Needs a key"). Add `; T60: the top reason on a loss is one large gold line under the cards.` to the file's header comment. Nothing else in the file changes.

**`Graphs/WBP_EndScreen/AddCard.txt`:** after `(set CardCount (+ (V CardCount) 1))`, inside the `fn`, add:

```lisp
  ; T60: keep each card and its name, so SetRival can find an AI's card.
  (add (V Cards) _card)
  (add (V CardNames) Name))
```

(moving the final `)` of the `fn` to the last line). New variables: `Cards` (array of `WBP_EndCard` object references), `CardNames` (String array).

**`Graphs/WBP_EndScreen/SetReason.txt`** (new; input `Reason`, String):

```lisp
; WBP_EndScreen.SetReason(Reason), called by BP_Show.EndReveal on a loss (T60): the top reason, the kind of
; evidence most of the votes that cut the human named ("They caught you copying late."), as one large gold line
; under the cards, right above Play Again. An empty reason leaves the line collapsed.
(fn SetReason (Reason)
  (Widget|SetText(Text) :self (Variables|WBP_EndScreen|GetReasonText) :InText (Utilities|Text|ToText(String) Reason))
  (if (not (Utilities|String|IsEmpty Reason))
    (Widget|SetVisibility :self (Variables|WBP_EndScreen|GetReasonText) :InVisibility "SelfHitTestInvisible")))
```

**`Graphs/WBP_EndScreen/SetRival.txt`** (new; inputs `Name` and `Rival`, String):

```lisp
; WBP_EndScreen.SetRival(Name, Rival), called by BP_Show.RevealRivals on a win (T60): the rival line on the
; card of the AI called Name (the card's title, as AddCard got it).
(fn SetRival (Name Rival)
  (bind _i (Utilities|Array|FindItem (V CardNames) Name))
  (if (>= _i 0)
    (Class|WBPEndCard|SetRival :self (get (V Cards) _i) :Rival Rival)))
```

Order: compile `WBP_EndCard` with its `SetRival` (part 5) first, then write `AddCard`, `SetReason`, `SetRival` and the event graph here, then compile `WBP_EndScreen` with warnings as errors (T33 did). `Setup`, `ShowRing` and the Restart and Quit clicks don't change: Restart still calls `BP_Show.RestartShow` in one click, and Play Again keeps the keyboard focus.

## 5. `WBP_EndCard`

### 5a. The widget tree

Add two `TextBlock`s at the end of the card's `VerticalBox` (survey 6), after `ClosingText`:

- **`RivalTitle`:** text "Rival" (match the form of `VotesTitle` and `ClosingTitle`'s designer text, survey 6), slot padding the same as `ClosingTitle`'s.
- **`RivalText`:** text "", `AutoWrapText` on, slot padding the same as `ClosingText`'s.
- Both visibility **Collapsed**, `bIsVariable` on.

### 5b. Graphs

**`Graphs/WBP_EndCard/EventGraph.txt`:** in `EventPreConstruct`, after the two `ClosingText` lines, add:

```lisp
  (Class|Text|SetFont :self (Variables|WBP_EndCard|GetRivalTitle) :Font (Class|UIStyle|UIFont :Role "Name"))
  (Class|Text|SetColorandOpacity :self (Variables|WBP_EndCard|GetRivalTitle) :ColorAndOpacity cText)
  (Class|Text|SetFont :self (Variables|WBP_EndCard|GetRivalText) :Font (Class|UIStyle|UIFont :Role "Caption"))
  (Class|Text|SetColorandOpacity :self (Variables|WBP_EndCard|GetRivalText) :ColorAndOpacity cText)
```

The same roles as the other two sections: `Name` 20 pt bold headings and `Caption` 18 pt body, both `PaperText` (12.7:1 on paper in T33). In the `IsDesignTime` block, after the `Setup` sample, add `(CallFunction|SetRival :Rival "Meta")`, so the designer shows the new rows.

**`Graphs/WBP_EndCard/SetRival.txt`** (new; input `Rival`, String):

```lisp
; WBP_EndCard.SetRival(Rival), called by WBP_EndScreen.SetRival on a win (T60): the AI's rival, by the name the
; player sees, under its reasons. The two rows stay collapsed on a loss.
(fn SetRival (Rival)
  (Widget|SetText(Text) :self (Variables|WBP_EndCard|GetRivalText) :InText (Utilities|Text|ToText(String) Rival))
  (Widget|SetVisibility :self (Variables|WBP_EndCard|GetRivalTitle) :InVisibility "SelfHitTestInvisible")
  (Widget|SetVisibility :self (Variables|WBP_EndCard|GetRivalText) :InVisibility "SelfHitTestInvisible"))
```

`Setup` doesn't change, so `AddCard`'s call to it stays valid. Compile with warnings as errors.

## 6. `Tools/check_prompts.py`

Each block with the text it goes after or replaces. Line numbers are at `d2d4cdc`; T54, T55, T57 and T58 add lines, so search by text.

**a. The docstring.** Before `Exit code 0 means the files are valid and every reply passed its checks.`, after the last task paragraph (T52's "A tie", then T54's, T55's, T57's and T58's):

```
Tells (T60): every vote names its tell, the one kind of evidence its reason
gives (reply_schema 'tell'; the list, and each tell's lose-screen line, are in
tells.json). The file check fails a reply_schema whose 'tell' enum isn't ""
then the tells.json ids, a 'game' prompt whose "tell" line doesn't name every
tell, and a free_mode.json vote phase whose 'tells' don't pair with its
reasons. A vote reply must name a tell from the list; the other asks leave it
empty. A --free reply may leave 'tell' out: the relay's free mode builds its
replies without it. --log checks a lost show's NHOS: TOP REASON against its
NHOS: TELL lines, and a won show's NHOS: RIVALS against personas.json 'rival'.
```

Also line 13: `It reads Content/NHOS/Data/{llm,prompts,personas,scenes,errors}.json` → `{llm,prompts,personas,scenes,errors,tells}.json`.

**b. `check_files`: load and check the tells.**

- After `    error_lines = load_json("errors.json", errors)` (line 540): `    tells = load_json("tells.json", errors)`.
- Replace the required-fields check (lines 546 to 547):

  ```python
      if sorted(schema.get("required", [])) != sorted(["actions", "speech", "pass", "vote", "reason", "tell"]):
          errors.append("llm.json: reply_schema must require actions, speech, pass, vote, reason and tell")
  ```

- After T54's goal-1 block (it ends `"or still on stage when the last scene ends (T54)")`), add:

  ```python
      # T60: the tells a vote can name (tells.json), the reply field (reply_schema 'tell') and the prompt agree.
      tlist = tells.get("tells", []) if isinstance(tells, dict) else []
      tell_ids = [t.get("id") for t in tlist if isinstance(t, dict)]
      if not tell_ids or len(set(tell_ids)) != len(tell_ids) or tell_ids[-1] != "other":
          errors.append("tells.json: 'tells' needs unique ids, with 'other' last (T60)")
      for t in tlist:
          line = t.get("line", "") if isinstance(t, dict) else ""
          if not isinstance(t, dict) or not t.get("means") or not line:
              errors.append(f"tells.json: tell {t.get('id') if isinstance(t, dict) else t!r} needs 'means' and 'line'")
          elif words(line) > MAX_WORDS or legibility(line):
              errors.append(f"tells.json: tell {t['id']}'s line must be one plain line of {MAX_WORDS} words at most")
      tell_prop = schema.get("properties", {}).get("tell", {})
      if tell_prop.get("type") != "string" or tell_prop.get("enum") != [""] + tell_ids:
          errors.append('llm.json: reply_schema.tell must be a string whose enum is "" and then the tells.json ids, in order (T60)')
      tell_line = next((g for g in game if g.lstrip().startswith('- "tell"')), "")
      missing = [t for t in tell_ids if not re.search(r"\b" + re.escape(t) + r"\b", tell_line)]
      if not tell_line or missing:
          errors.append(f"prompts.json: 'game' needs a '- \"tell\"' line under How to reply that names every tell "
                        f"(missing: {', '.join(missing) if tell_line else 'the line'}) (T60)")
  ```

- After `    errors.extend(prewritten_problems(scenes, errors))` (line 680), with question 1's first answer:

  ```python
      # T60: free mode pairs one tell with each pre-written vote reason, so Test for Free names a top reason.
      free = load_json("free_mode.json", errors) or {}
      for ph in free.get("phases", []):
          if ph.get("id") == "vote" and "tells" not in ph:
              errors.append("free_mode.json: the vote phase needs 'tells', one per reason (T60)")
          if "tells" in ph and (len(ph["tells"]) != len(ph.get("reasons", [])) or any(t not in tell_ids for t in ph["tells"])):
              errors.append(f"free_mode.json: {ph.get('id')} 'tells' must pair one tells.json id with each reason (T60)")
  ```

- The return (line 685): `    return {"llm": llm, "prompts": prompts, "personas": plist, "scenes": scenes, "tells": tell_ids}`.
- `main`'s "Files OK" line (line 1509): add `tells.json, ` after `errors.json, `.

**c. `check_reply` and `shape_fails`.**

- `check_reply`, line 1179: `    types = {"actions": list, "speech": str, "pass": bool, "vote": str, "reason": str, "tell": str}`. The "unexpected fields" check then accepts `tell`, and a reply without it fails.
- Right before `    # Legibility: every AI line reads like a normal chat.` (line 1254), add:

  ```python
      # T60: a vote names its tell; the other asks leave it empty. The closing vote may name one: nothing reads it.
      tell = reply["tell"]
      if ask == "vote":
          need(tell in ctx.get("tells", []), f"tell {tell!r} is not one of tells.json's ids")
      elif ask == "input":
          need(not tell, "the input LLM set tell")
      elif ask != "closing":
          unused(not tell, f"tell filled in {ask}")
  ```

- `build_jobs`: add `"tells": data["tells"]` to the `ctx` of the actor asks (the dict that starts `ctx = {"places": places, "props": props, "actors": actors, "me": show.name(pid), "options": st["options"],`). Only the vote reads it.
- `shape_fails` (line 1474), whole function:

  ```python
  def shape_fails(reply):
      """Only the reply's shape: every schema field with the right type (for --free replies). 'tell' (T60) may be
      missing, because the relay's free mode builds its replies without it."""
      types = {"actions": list, "speech": str, "pass": bool, "vote": str, "reason": str}
      fails = [f"{k} is missing or not a {t.__name__}" for k, t in types.items() if not isinstance(reply.get(k), t)]
      if "tell" in reply and not isinstance(reply["tell"], str):
          fails.append("tell is not a str")
      return fails
  ```

**d. `LOG_RE`** (line 1272): add `TOP REASON|TELL|RIVALS`. With T52's, T54's, T55's, T57's and T58's kinds:

```python
LOG_RE = re.compile(r"NHOS: (SHOW READY|SHOW END|RESTART|SEATS|SETUP|LOG|CLOSING|CUT|TIE|REACTIONS DONE|PASSED|LASTWORDS|TOP REASON|TELL|RIVALS)\b ?(.*)$")
```

`TELL\b` doesn't match `LoadTells`' `NHOS: TELLS missing ...`, which is fine: the file check catches a missing `tells.json`.

**e. `check_log`: collect.** Its signature becomes `def check_log(path: Path, personas, all_shows: bool, tell_ids=()) -> int:`, and `main` calls `check_log(Path(args.log), data["personas"], args.all_shows, data["tells"])`.

- After `    names = {p["id"]: p["name"] for p in personas}` (line 1277): `    rival_of = {p["id"]: p.get("rival") for p in personas}  # T60`
- After T54's `    end_bad = 0`: `    top_bad = 0  # T60: lost shows whose TOP REASON is missing or miscounted, won shows whose RIVALS are wrong`
- After T54's `        cuts, end = 0, None  # T54`: `        told, top, rivals, cast = [], None, None, []  # T60`
- Right before `            if kind == "SEATS":`:

  ```python
              if kind == "TELL":
                  # T60: "NHOS: TELL <voter id> tell=<tell> | <reason>", one per vote that cut the human.
                  m = re.search(r"tell=(\S+)", rest)
                  told.append(m.group(1) if m else "?")
                  continue
              if kind == "TOP REASON":
                  top = rest  # "<tell> votes=<n>"
                  continue
              if kind == "RIVALS":
                  rivals = dict(p.split("=", 1) for p in rest.split() if "=" in p)
                  continue
  ```

- In the `SEATS` branch, after its `seats=` block: `                m = re.search(r"cast=(\S+)", rest)` / `                if m:` / `                    cast = [c for c in m.group(1).split(",") if c in rival_of]`. Check the separator in a fresh log's `NHOS: SEATS` line (T26: "cast=<ids in seat order>"); the code assumes commas.

**f. `check_log`: the check.** After T54's reason check (it ends with its `[FAIL] show {i} | SHOW END |` print), add:

```python
        # T60: a lost show names one top reason, the most common tell of the votes that cut the human
        # (a tie may name any of the tied tells); a won show reveals each AI's rival.
        result = end.get("result") if end else None
        if result == "lose":
            m = re.match(r"(\S+) votes=(\d+)$", top or "")
            counts = {t: told.count(t) for t in told}
            best = max(counts.values(), default=0)
            if not m:
                top_bad += 1
                print(f"[FAIL] show {i} | TOP REASON | {'missing' if top is None else repr(top)}; "
                      f"one 'NHOS: TOP REASON <tell> votes=<n>' expected on a loss")
            elif int(m.group(2)) != best or (told and counts.get(m.group(1), 0) != best) \
                    or (m.group(1) != "none" and tell_ids and m.group(1) not in tell_ids):
                top_bad += 1
                print(f"[FAIL] show {i} | TOP REASON | {top}, but the TELL lines count {counts}")
        elif result == "win":
            want = {pid: rival_of[pid] for pid in cast}
            if top is not None:
                top_bad += 1
                print(f"[FAIL] show {i} | TOP REASON | a top reason on a win: {top}")
            if rivals is None:
                top_bad += 1
                print(f"[FAIL] show {i} | RIVALS | missing; one 'NHOS: RIVALS <id>=<id> ...' expected on a win")
            elif cast and rivals != want:
                top_bad += 1
                print(f"[FAIL] show {i} | RIVALS | {rivals}, expected {want} (personas.json 'rival')")
```

- The summary line: after T54's `ending = ...` part, add `, top reason = {top or 'none'}` before its closing `.`.
- The return: `    return 1 if bad or clock_bad or vote_bad or end_bad or top_bad else 0` (keep any counter T57 or T58 added).

**Tried on a scratch copy** (the prep session, at `d2d4cdc` with parts 1a to 1d and part 6 applied, and a stand-in for T54's `SHOW END` parsing): `--offline` passes. It fails, each with its own message, when `role` is taken out of the `llm.json` enum, when the `game` tell line is gone, when the `free_mode.json` vote phase has six tells for five reasons, and when a `tells.json` line has an all-caps word and a bracket. `check_reply`: a vote with a known tell passes; `"vibes"`, `""` or no `tell` fail; a closing vote with a tell passes; a reaction with a tell is a `WARN`. `shape_fails` passes a reply without `tell` and fails `tell: 1`. Synthetic logs (5 seats):

| Log | Result |
|---|---|
| a loss, `TELL` late_copy, late_copy, silence; `TOP REASON late_copy votes=2` | pass, `top reason = late_copy votes=2` |
| the same with `TOP REASON silence votes=1` | exit 1: `silence votes=1, but the TELL lines count {'late_copy': 2, 'silence': 1}` |
| a loss with no `TOP REASON` | exit 1: `missing` |
| a loss, `TELL` late_copy, silence (a 1–1 tie); `TOP REASON silence votes=1` | pass (any tied tell) |
| a win, `RIVALS` right, in another order than the seats | pass |
| a win, `overclocker=worrier` | exit 1, with the expected pairs |
| a win with no `RIVALS` | exit 1: `missing` |

Run the same after T54 and T55's edits are in, since their blocks are the anchors.

## 7. The check

The Done-when: a free autoplay show that I lose shows the reasoning and one top reason; a show with `spare_human` on shows the reasoning and the rivals; screenshots of both; `NHOS: TOP REASON <tell> votes=<n>` on a loss and `NHOS: RIVALS <id>=<id> ...` on a win; Restart from each screen reaches a second `NHOS: SHOW END`; Claude plays one win and one loss by hand and checks that the top reason matches what the AIs said.

The brief's editor rule applies: you drive the editor; say so in your status file, and tell my person before PIE if the brief asks for it.

### Files

```bash
python Tools/check_prompts.py --offline
```

```bash
python Tools/check_prompts.py --relay --free
```

Both pass. `--relay --free` spends no tokens; its replies have no `tell`, which `shape_fails` allows.

**The paid run needs my person's OK** (T60's task: the schema change reaches all four providers). Ask with the multiple-choice tool once the data edits are in: "Run the paid check (Recommended)": every ask once on each provider with the keys in `Local/llm_key.json`, about 60 to 70 asks, a few cents (T5x runs: $0.03 to $0.11 per show's worth of calls), then `--ask vote --repeat 3` (12 asks); or "Skip it" (then write under "Findings" that no provider has answered with a `tell` yet, and that the Done-when's tell-matches-reason check rests on free mode only).

```bash
python Tools/check_prompts.py
```

```bash
python Tools/check_prompts.py --ask vote --repeat 3
```

- Every ask passes: each provider accepts the new enum under its strict schema, every vote names a tell, and no other ask fills one (a `WARN` if it does).
- **The tell matches the reason:** the run prints each reply as JSON. For each of the 12 votes of the second run, read `reason` and `tell` and judge whether the tell is the kind of evidence the reason gives. Write the pairs, and any provider that picks `other` for a clear tell, under "Findings". If one provider gets most of them wrong, the `game` tell line (part 1c) needs clearer words; change it and run the 12 again (another few cents, same OK).

### Run A: a loss, in a game window on the saved assets

`Local/switches.json`: `"autoplay": true`, `"mode": "free"`, `"force_tie": false`, `"spare_human": false`, `"fast_lines": true`, `"burn_test": false`, `"ai_seats": 0`. Close every game window before you save an asset (T53).

```bash
"<UE_ROOT>/Engine/Binaries/Win64/UnrealEditor.exe" "<PROJECT>" -game -windowed -ResX=1600 -ResY=900 -log=T60lose.log
```

```bash
grep -E "NHOS: (SETUP|CUT |TIE|TELL|TOP REASON|RIVALS|CLOSING|SHOW END)" Saved/Logs/T60lose.log
```

Expected at the end, in order (`<…>` varies):

```
NHOS: CUT human votes=<n> reveal=HUMAN
NHOS: CLOSING <id> vote=<id> | <reason>          (4 lines)
NHOS: TELL <id> tell=<tell> | <reason>            (n lines, one per vote that cut me)
NHOS: TOP REASON <tell> votes=<k>
NHOS: SHOW END result=lose reason=caught scenes=<s> human=human show=1
```

- No `NHOS: RIVALS`, no `NHOS: TELLS missing`, no `LogScript` warning, no `Accessed None`.
- With question 1's first answer, each `TELL` line's tell is the one free mode pairs with its reason (part 1d: "paused before every line" is `silence`, and so on). With the second, every tell is `other`.
- `python Tools/check_prompts.py --log Saved/Logs/T60lose.log` passes, with `ending = lose caught, top reason = <tell> votes=<k>`.
- Free-mode votes are random, so a show may end in a win instead (a tie, or an AI cut each scene). Run it again until it ends `result=lose`; each run takes a few minutes with `fast_lines`.

### Run B: a win (`spare_human` on)

The same switches with `"spare_human": true` and `-log=T60win.log`.

- Expected at the end: `NHOS: RIVALS visionary=worrier worrier=visionary overclocker=copycat copycat=overclocker` (in the AIs' seat order), no `TELL` or `TOP REASON`, `NHOS: SHOW END result=win reason=<final_two|last_scene> ...`.
- `--log Saved/Logs/T60win.log` passes.

### Run C: a 4-actor win (`ai_seats` 3)

Run B with `"ai_seats": 3` and `-log=T60four.log`: `RIVALS` names only the three seated AIs; the one whose rival wasn't drawn shows "(not in this show)" on its card (decision 5; seen in the screenshots below). `--log` passes.

### The screenshots and Restart: PIE autoplay

PIE in a 1600 × 900 floating window, `Local/switches.json` as in run A, then as in run B (autoplay skips the title; `mode` free is Test for Free). Wait for `NHOS: SHOW END` in the log, then `SlateInspectorToolset.Screenshot` (T33). If the stage waits on **See the results** (the gold `ContinueButton`, T14), click it through the Slate inspector and wait for `NHOS: END screen shown`. Save them in `Saved/T60/shots/` (not in git):

1. `lose_p16.png`: the red plate with the title (question 3), the subtitle, the four cards with each AI's votes and reasons, the top reason in gold under the cards, Play Again and Quit. No "Rival" row on any card.
2. `win_p16.png`: the gold plate, T54's subtitle, each card with its "Rival" row at the bottom, no reason line.
3. `lose_p12.png` and `win_p12.png`: the same at 1280 × 720. The reason line wraps inside the screen, Play Again stays on screen, and the cards scroll if they must; nothing clips or overlaps.
4. `win_four_p16.png` (run C's switches): three cards, one rival with "(not in this show)".

**Restart from each:** with the screenshot taken, press Enter (Play Again has the keyboard focus, T33) with `SlateInspectorToolset.PressKey`. Expected: `NHOS: RESTART show=2`, the stage widgets back, and show 2 playing by itself to a second `NHOS: SHOW END ... show=2`. Do it once from the lose screen and once from the win screen. `--log --all-shows` on each PIE log passes.

**Without color:** a grayscale and a deuteranopia version of `lose_p16.png` and `win_p16.png` (as T33 did). The reason line must still stand out from the body text by size, and the "Rival" rows by their bold heading.

As a first-time player, judge: does the lose screen tell me in one glance why I was caught, and would I know what to do differently next show? Does the win screen's rival row read as a reveal, not clutter? Write what you saw under "Findings", with the contrast of the reason line (gold on ink, expected about 10:1) measured as T33 did.

### Claude plays by hand

PIE, Test for Free, autoplay off, a 1600 × 900 floating window, clicks and typing through the Slate inspector (the build note "Claude does the playing").

- **One loss:** play until the AIs cut me (free-mode votes are random, so it may take more than one show; Restart between shows is the one-click path the lose screen offers). On the lose screen, read each AI's reasons about me on the cards and the `TELL` lines in the log, and check that the top reason is the most common tell among them.
- **One win:** with `spare_human` on in `Local/switches.json` (it applies with autoplay off too), play to the end; check each card's rival against `personas.json`.
- **"Matches what the AIs said":** Test for Free pairs each reason with its tell by construction, so it checks the counting and the screen. Real AIs' reasons are checked by the paid run's 12 votes above. If my person wants to see it in a show too, one Play via Relay show by hand costs about $0.03 to $0.11 and needs their OK; offer it, don't run it unasked.

**Afterward:** set `autoplay`, `spare_human` and `fast_lines` back to false and `ai_seats` to 0, and close each game window.

## 8. The commit

**One commit** (`T60: Win and lose screens: the reasoning, the top reason and the rivals`), if my person OK'd the `free_mode.json` push in part 0:

- `Content/NHOS/Core/BP_Show.uasset`, `Content/NHOS/UI/WBP_EndScreen.uasset`, `Content/NHOS/UI/WBP_EndCard.uasset`, `Content/NHOS/Data/tells.json` (new), `Content/NHOS/Data/llm.json`, `Content/NHOS/Data/prompts.json`, `Tools/check_prompts.py`, `Graphs/BP_Show/StoreTell.txt`, `LoadTells.txt`, `TopReason.txt`, `RevealRivals.txt`, `EndReveal.txt` (new), `Graphs/WBP_EndScreen/EventGraph.txt`, `AddCard.txt`, `SetReason.txt` (new), `SetRival.txt` (new), `Graphs/WBP_EndCard/EventGraph.txt`, `SetRival.txt` (new), `Docs/tasks/T60.md`, `Docs/Plan.md` (the box, "Next up"), `Docs/DevLog.md`.
- With question 1's first answer, also `Content/NHOS/Core/BPC_LLMClient.uasset`, `Graphs/BPC_LLMClient/FreeReply.txt` and `Content/NHOS/Data/free_mode.json`.
- Under "Findings" in `T60.md`: my person's four answers, every node edit (`StoreVote`, `ShowEndScreen`, and `ParseFields` and `ClearReply`), the checker's synthetic-log results, the paid run's tell pairs, and the screenshots' judgement.
- Unlock every asset after the push.

**If the `free_mode.json` OK wasn't given,** push the rest as `T60: ... (waits for the free_mode.json push OK)` with a `Waiting:` line under T60 (`Left: my OK to push free_mode.json, typed in the T60 session.`), and keep `free_mode.json` uncommitted and unedited until then (T55 part 5: a local commit of it would go out with anyone's push). Until it lands, Test for Free votes have no tell and the lose screen says the `other` line; the `--offline` free-mode check fails, so add the `free_mode.json` check (part 6b) in the second commit.

**DevLog line:** `T60: The end screens teach. Each vote now names its tell (a new reply field), and the lose screen names the top one in a large line ("They caught you copying late."); the win screen reveals each AI's rival on its card.`

**"Next up" sentence:** `T60 (the end screens) is done: every vote names its tell (llm.json reply_schema 'tell', tells.json), the lose screen shows the top reason under the cards (BP_Show.TopLine, which T61's earpiece can say), and the win screen shows each AI's rival on its card.`

## 9. Knock-on: tell, don't change

- **T61 (the stagehand):** `BP_Show.TopLine` holds the top reason's line after a loss ("" on a win), and `NHOS: TOP REASON <tell>` names the tell; T61-build part 7a's `end` row passes `TopLine` to `EndShow` as `Reason`. `EndReveal` runs inside `ShowEndScreen`, so `TopLine` is set by the time `RunCue`'s `"end"` branch reaches T61's node after `(CallFunction|ShowEndScreen)`.
- **The relay's free mode** sends no `tell` (part 1d). A later task that pushes `Relay/` with a deploy OK can add `tell: ""` to `freeReplyObject` and, in its vote branch, `FREE`'s `tells` at the reason's index; then `shape_fails` can require `tell` again.
- **`Docs/ItchPage.md`** (T54's line): "Either way, the end screen shows how each AI voted and why." It could add "and, if you're caught, the main reason they caught you". Not in T60's Touches; tell my person.
- **`Docs/Submission.md`'s trailer shot list** names the ending shot; a lose screen with its top reason, or a win with the rivals, is a stronger last shot. Tell my person.
- **The design doc** needs nothing. If my person keeps "YOU'RE CUT" (question 3), the doc's Lose screen row still says "YOU: HUMAN"; show my person that difference rather than editing the doc.
