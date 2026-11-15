# T50 build sheet: only the bots get the director's note

Prep for [T50](T50.md), written on 2026-11-15 without the editor, while T51 was still open. It is written against **T51's result as `T51.md` describes it**: no decoy anywhere, every note in `scenes.json` has a `category`, every seat on stage gets the note, and `NHOS: SETUP ... note=<id> category=<category>` with no `decoy=`. Line numbers are from `noHumansOnSet` at `8ceb55c`, before T51; T51's edits move them, so find each line by its text. Part 7 lists what to check again once T51 is pushed.

Lines marked **doc** are copied word for word from the design doc. Lines marked **my call** are not in the doc: show them to the person before the commit (T50, step 1).

## 1. The four doc lines

From the Bot Prompts tab, "Opening prompt: game rules" (read on 2026-11-15, tab rev 81). The block is a code block, and its apostrophes are straight (`'`), as below.

1. `Every actor sees the director's note category. Only the AI actors see the note itself. The human does not have the note and knows it, so they will watch you and copy.`
2. `Follow the note in every scene, but subtly. Never say it aloud during the scene, and don't act it out so plainly that anyone could copy it after one turn.`
3. `Fitting the category is not proof. An actor who only matches the category, or copies the others a turn late, probably lacks the note.`
4. `In Free Talk the scene is over, so you may name the note when you accuse someone.`

The other lines of that block belong to other tasks: "One actor in this cast is a human..." (already in `game`), "Silence is evidence..." (T57), the two rival lines (T56, already in `game`), "A tied vote cuts nobody..." (T52 and T54). Don't add them in T50.

The Rules tab says the same rule for the player (tab rev 27), for the card text and `ItchPage.md`:

- Scene Prep: "Only the AI actors get the secret director's note. You don't, and you know it. The scene card shows everyone the note's category, such as Props." and "The AIs know you lack the note and can see its category. They follow it subtly so you can't simply copy them, never say it aloud during the scene, and treat anyone who only matches the category, or copies a turn late, as a suspect." The last Scene Prep bullet: the card shows "the note's category".
- The Scene & acting: "During the scene, your screen shows only your own card: your role, your want and the note's category." and "You act blind on turn 1. After that, read the AIs' moves and work out the note. Acting early risks guessing wrong; waiting risks copying late."
- Free Talk: "The scene is over, so actors may name the director's note when they accuse someone."
- Onboarding table, Scene Prep row: "Scene card: story, your role, your want, **Note category: Props**, **Note: ██████ (bots only)**". The stagehand's lines there are T61's, not T50's.

## 2. `Content/NHOS/Data/prompts.json`

Each line is given as it sits in the JSON file (escaped quotes and all). The plan: put each doc line as its own sub-bullet (`"  - "`, the form T56 used for the rival lines) under the rule it belongs to, so the doc text stays whole and the checker can find it (part 4, C). Then reword the old lines around it.

### `game`

**a. "How a show works", Scene Prep (line 23).**

- Now: `"- Scene Prep: everyone sees the same scene card: the story, who each actor plays and what each one wants. Each actor also gets a secret director's note. Everyone gets the same note, except one random actor, who gets a decoy note instead. Nobody is told who has the decoy, not even that actor. It could be you. It could be the human. A note applies during the scene's 3 turns."`
- After T51 (expected; T51's step 2 takes the decoy out): something like `"- Scene Prep: everyone sees the same scene card: the story, who each actor plays and what each one wants. Each actor also gets the same secret director's note. A note applies during the scene's 3 turns."` Replace whatever T51 left.
- New (**my call**): `"- Scene Prep: everyone sees the same scene card: the story, who each actor plays and what each one wants. The AI actors also get a secret director's note, the same for all of them. A note applies during the scene's 3 turns."`
- New line right after it (**doc**, line 1): `"  - Every actor sees the director's note category. Only the AI actors see the note itself. The human does not have the note and knows it, so they will watch you and copy."`

**b. "How a show works", The Scene (line 24).** The line stays as it is. New line right after it (**doc**, line 2):

`"  - Follow the note in every scene, but subtly. Never say it aloud during the scene, and don't act it out so plainly that anyone could copy it after one turn."`

**c. "How a show works", Free Talk (line 25).** The line stays as it is. New line right after it (**doc**, line 4):

`"  - In Free Talk the scene is over, so you may name the note when you accuse someone."`

**d. "Reading the state", a new line for `scene_card`** (**my call**), right after line 34 (the Player names line), before the `"you"` line:

`"- \"scene_card\" is the story: its title, its premise and \"note_category\", the category of the director's note. Every actor sees the category, the human too."`

**e. "Reading the state", the `you` line (line 35).**

- Now: `"- \"you\" is your seat: your Player name, your role, your want and your secret note. Only you can see your note."`
- New (**my call**): `"- \"you\" is your seat: your Player name, your role, your want and the director's note (\"note\"). Only the AI actors have the note. The human's seat has none."`

**f. "Spotting the human", the note bullet (line 43).**

- Now: `"- The note: compare what each actor does with what your note asks. An actor who breaks the pattern may be the human, or may just hold the decoy. If most actors break your note, maybe you hold the decoy."`
- After T51 (expected): `"- The note: compare what each actor does with what your note asks. An actor who breaks the pattern may be the human."` or close to it. Replace whatever T51 left.
- New (**my call**): `"- The note: compare what each actor does with what your note asks. The human can only guess from the category and from watching you."`
- New line right after it (**doc**, line 3): `"  - Fitting the category is not proof. An actor who only matches the category, or copies the others a turn late, probably lacks the note."`

**g. The last line (line 64).**

- Now: `"Never quote your note word for word. You may hint at it."`
- New (**my call**, the doc's rule from lines 2 and 4 restated as the closing reminder, since the old line sat last for a reason): `"Never say the note aloud during the scene, not even a hint. In Free Talk you may name it."`
- If the person would rather not repeat the rule, delete the line instead: line 2 and line 4 already say it.

**Lines that stay as they are** (checked against the new rule):

- Line 17: `"2. Don't get cut yourself. Play your persona, play your role, chase your want and follow your secret note, so nobody mistakes you for the human. ..."` is read only by the AIs, who have the note, so it still holds.
- Line 22 (the scene count) is T53's; lines 26 (the tie and the Director) and 39 (25 words) are T52, T55 and T59's.

### `asks`

**h. `asks.scene_turn` (line 116).**

- Now: `"scene_turn": "The scene, your turn. Play your role, chase your want, follow your note, and react to what just happened in the log. Fill: actions (1 or 2) and speech.",`
- New (**my call**): `"scene_turn": "The scene, your turn. Play your role, chase your want, follow your note subtly without saying it, and react to what just happened in the log. Fill: actions (1 or 2) and speech.",`
- The ask is the last thing the model reads before it answers, so a short reminder here costs little. If the person says `game` is enough, leave it.

**i. `asks.free_talk` (line 117).**

- Now: `"free_talk": "Free Talk, your line. Say one short line, about 10 words, to the cast about who the human is: accuse one actor, defend yourself, or ask or answer a pointed question, with one piece of evidence from the log. Talk about one actor, not a list. Pass only if you truly have nothing to add. Fill: speech, or pass. No actions.",`
- New (**my call**): `"free_talk": "Free Talk, your line. Say one short line, about 10 words, to the cast about who the human is: accuse one actor, defend yourself, or ask or answer a pointed question, with one piece of evidence from the log. The scene is over, so you may name the note. Talk about one actor, not a list. Pass only if you truly have nothing to add. Fill: speech, or pass. No actions.",`
- T57 (silence is evidence) and T58 (the last word) change this ask later, so keep the edit to the one sentence.

### `_readme`

**j. The state line (line 5).** Two changes: `scene_card` gains `note_category`, and a sentence says who gets the note.

- Now: `"User message: one JSON object, the state of the show, written by the game with Set Field and sent as the message's text. Actor asks use: show {scene, scenes, now}, set {name, places [{name, what}], props}, scene_card {title, premise}, cast [{name, role, want, status}], you {name, role, want, note}, log [{when, actor, does, says}], game_messages [text], options [names], ask (text from 'asks'). The Director gets show, cast, log, game_messages, options and ask. The input LLM gets actor, phase ('scene', 'free talk' or 'reaction'), places [names], props, cast [names], screen_names ['OpenAI is Player 1', ...], typed and ask."`
- New: `"User message: one JSON object, the state of the show, written by the game with Set Field and sent as the message's text. Actor asks use: show {scene, scenes, now}, set {name, places [{name, what}], props}, scene_card {title, premise, note_category}, cast [{name, role, want, status}], you {name, role, want, note}, log [{when, actor, does, says}], game_messages [text], options [names], ask (text from 'asks'). The Director gets show, cast, log, game_messages, options and ask. The input LLM gets actor, phase ('scene', 'free talk' or 'reaction'), places [names], props, cast [names], screen_names ['OpenAI is Player 1', ...], typed and ask."`
- New line right after it: `"The director's note (T50): only the AI seats get it. Every actor ask carries its category in scene_card.note_category (the note's 'category' in scenes.json) and the note itself in you.note. The human's seat holds no note and never gets an actor ask, and the input LLM gets neither the note nor its category."`

**k. The log line (line 6),** `"The log never holds raw input, times, errors, notes or who has the decoy. ..."`: T51 takes out "or who has the decoy". T50 changes nothing more.

## 3. The state the AIs read

| Field | AI seat | My seat (the human) | Input LLM |
|---|---|---|---|
| `scene_card.note_category` (new) | the note's `category` from `scenes.json`, as written, for example `"Props"` | not sent (my seat never gets an actor ask), but my card shows it | not sent |
| `you.note` | the note's `note` text, the same for every AI seat | `SeatNote[HumanSeat]` is `""`; never sent | not sent |
| everything else | as now | as now | as now: `actor`, `phase`, `places`, `props`, `cast`, `screen_names`, `typed`, `ask` |

- **Why `scene_card`:** the category is public, like the title and premise, and everyone sees the same card. `show`, `cast` and `you` are the wrong places: `you` is the seat's own, and `show` holds only counters.
- **Key order:** `ActorState` writes the fields in `check_prompts.py`'s order (T06), so `scene_card` is `{title, premise, note_category}` in both.
- **Only AI seats get `ActorState`:** turns, Free Talk, votes and reactions ask only AI seats with it. My seat goes through `InputState` (typed lines) or the canned autoplay lines (`autoplay.json`), which also go through the input LLM. The free-mode replies (`free_mode.json`) read no note.
- **`SETUP` line:** T51 makes it `NHOS: SETUP ... note=<id> category=<category>`. T50 keeps it as it is, so the check ("its `SETUP` line names the note and its category") passes from T51's line.

## 4. `Tools/check_prompts.py`

Line numbers are from before T51. T51 removes `SAMPLE_DECOY` (line 469), the decoy in `you()` (632) and in `card_cases` (722, 737), changes the note check (432 to 434) and the docstring of `card_cases` (711), and takes "decoy" out of `TALK` (504) and `INPUT_CASES` (552). Build on T51's version.

**A. Module docstring (lines 1 to 74).** Add a paragraph after "Rivals (T56)" (ends at line 69), before "Exit code 0":

```
Director's note (T50): only the AI seats get the note. Every actor state's
scene_card carries note_category, the note's 'category' from scenes.json, and
'you' carries the note. The human's sample seat (Player 3) has no note, and the
input converter's state has neither. The file check also finds the design
doc's four note lines in prompts.json 'game', word for word (DOC_NOTE_LINES).
```

**B. A new constant `DOC_NOTE_LINES`**, after `MAX_WORDS = 25` (line 110). Not in T50's steps, but it keeps the four doc lines safe while T57, T58 and T59 edit `game` after T50 (**my call**: ask the person; drop C too if they say no):

```python
# T50: the design doc's note rules (Bot Prompts, "Opening prompt: game rules"), word for word.
DOC_NOTE_LINES = [
    "Every actor sees the director's note category. Only the AI actors see the note itself. The human does not have the note and knows it, so they will watch you and copy.",
    "Follow the note in every scene, but subtly. Never say it aloud during the scene, and don't act it out so plainly that anyone could copy it after one turn.",
    "Fitting the category is not proof. An actor who only matches the category, or copies the others a turn late, probably lacks the note.",
    "In Free Talk the scene is over, so you may name the note when you accuse someone.",
]
```

**C. `check_files` (lines 317 to 455),** after the notes loop (now lines 432 to 434; T51 makes it check `note` and `category`):

```python
    game = prompts.get("game", [])
    for line in DOC_NOTE_LINES:
        if not any(line in g for g in game):
            errors.append(f"prompts.json: 'game' lost a note rule from the design doc: {line[:60]!r}")
```

**D. The sample show's comment (lines 462 to 465).** After T51 it no longer names a decoy. Add one sentence: `# The human has no note (T50): it grabs the rose in turn 1 by luck and gives it away in turn 3.` (`TURNS` already plays it that way.)

**E. `Show.you` (lines 627 to 633).** The note line (632) becomes:

```python
            "note": "" if pid == HUMAN else self.note["note"],
```

Before T51 it reads `self.note["decoy"] if pid == SAMPLE_DECOY else self.note["note"]`; after T51, expected `self.note["note"]`.

**F. `Show.actor_state` (line 639).**

- Now: `"scene_card": {"title": self.card["title"], "premise": self.card["premise"]},`
- New: `"scene_card": {"title": self.card["title"], "premise": self.card["premise"], "note_category": self.note["category"]},`

**G. `Show.card_cases` (lines 705 to 744).**

- Line 734, now: `"scene_card": {"title": card["title"], "premise": card["premise"]},`
- New: `"scene_card": {"title": card["title"], "premise": card["premise"], "note_category": note["category"]},`
- Line 737: after T51, expected `"note": note["note"]},`. No T50 change: the loop already skips the human (`if pid == HUMAN: continue`, line 729).
- Docstring (711, after T51's edit): add `Every state's scene_card carries the note's category.`

**H. A new check, `check_note_deal(show, jobs) -> int`,** after `check_leaks` (line 1152), called in `main` right after `leaks = check_leaks(data, jobs)` (line 1214), so it runs with `--offline` too. Fail the same way as `leaks` (`return 1` when it is not 0):

```python
def check_note_deal(show, jobs) -> int:
    """T50: only the AI seats get the director's note; every actor state carries its category;
    the input converter gets neither. Returns the number of problems."""
    bad = 0
    if show.you(HUMAN)["note"]:
        bad += 1
        print("FAIL note: the human's sample seat has a director's note")
    note = show.note["note"]
    for ask, label, _, body, _ in jobs:
        text = body_text(body)
        if ask == "input":
            if note in text or '"note' in text:
                bad += 1
                print(f"FAIL note: the input converter got the note or its category | {label}")
        elif ask != "tiebreak" and '"note_category"' not in text:
            bad += 1
            print(f"FAIL note: no scene_card.note_category in {ask} | {label}")
    return bad
```

- `body_text` (line 829) returns the system text and the state as one string, so the search covers both. The `input` prompt never says "note", so `'"note'` matches only a `note` or `note_category` key.
- The tiebreak (the Director's ask) has no `scene_card`; T55 removes it anyway.
- Don't search the input state for the category word itself: it is a common word ("Props") that a prop name or typed line can hold. The key check covers it.
- If it passes, print `Only the AI seats get the note, and every actor state carries its category.` next to the "No provider name..." line (1217).

**I. Optional WARN, a note said aloud (my call).** In `check_reply` (line 931), for `ask == "scene_turn"`, warn when the speech holds the note word for word: `unused(ctx.get("note", "").lower().rstrip(".") not in speech.lower(), "said the note aloud during the scene")`, with `"note": st["you"]["note"]` added to the two scene-turn `ctx` dicts in `build_jobs` (lines 1125 and 1131). It catches only a word-for-word quote, so the hand-played relay show stays the real check.

**Messages:** C, H and I add the FAIL and WARN texts shown above. Nothing else prints differently.

## 5. `Docs/ItchPage.md`

**Line 48** (under "Director's Cut"):

- Now: `Every scene comes with a secret note from the director, and every scene ends with a cut: the cast votes, and one actor leaves the show. When the vote ties, the Director, a tired AI who isn't acting, makes the final cut. The reveal stamp says who it really was: an AI, or the human.`
- New: `Every scene comes with a secret note from the director, which only the AIs get, and every scene ends with a cut: the cast votes, and one actor leaves the show. When the vote ties, the Director, a tired AI who isn't acting, makes the final cut. The reveal stamp says who it really was: an AI, or the human.`
- T50 changes only the first clause. The tie sentence is wrong after T52 and T55 (a tie cuts nobody, no Director), but it is theirs to change.

**Line 54** ("How a show works", step 1):

- Now: `1. **Scene Prep.** Everyone gets the same scene card: a comedy take on a famous story, like Romeo and Juliet, the Sword in the Stone, or a Sherlock Holmes mystery about a stolen rubber chicken. You get a role, a want and a secret director's note, such as "climb onto the Riser at least once". Everyone has the same note, except one actor, who has a decoy. It might be you. Nobody is told who.`
- New: `1. **Scene Prep.** Everyone gets the same scene card: a comedy take on a famous story, like Romeo and Juliet, the Sword in the Stone, or a Sherlock Holmes mystery about a stolen rubber chicken. You get a role and a want. The AIs also get a secret director's note, such as "climb onto the Riser at least once". You don't, and they know it: your card shows only the note's category, such as Props.`

**Line 56** ("The Scene"): no change in T50.

**Line 62** ("How to fool them"):

- Now: `**How to fool them:** play your role and chase your want. Follow the director's note, but remember that someone's note is a decoy. Don't stand still for a whole scene. Watch what the AIs accuse each other of, because they're looking for the same things in you.`
- New: `**How to fool them:** play your role and chase your want. On turn 1 you act blind, with only the note's category to go on. Then watch what the AIs do and work out the note, but copy too late and they'll notice. Don't stand still for a whole scene. Watch what the AIs accuse each other of, because they're looking for the same things in you.`

**Line 29** ("The prompts, scene cards and director's notes were written with Claude."): no change.

## 6. The graphs

Sources in `Graphs/` cover only part of what T50 changes. Where a graph has no file, T50's session reads it in the editor first (one graph at a time, never a full `BP_Show` dump), and changes it by node edits as T28 and T29 did, or writes a new source from its own reading, never from a read-back.

### `BP_Show`

| Graph | Source in `Graphs/` | What T50 changes |
|---|---|---|
| `ScenePrep` | **None today.** T51 means to write `Graphs/BP_Show/ScenePrep.txt` (its status file says so). If T51 pushed it, start from it; if not, read the graph in the editor first. T26 found that the old `Saved/t08` source of this graph doesn't round-trip, and T28 edited it by nodes. | **The deal:** the loop that sets `SeatNote[s]` for each seat on stage (T06: "Every seat on stage gets the note"; after T51, with no decoy draw) sets `""` for `s == HumanSeat`: a `select` on `(== s (V HumanSeat))` between `""` and the note text, into the `SetArrayElem` item pin. Keep the variable that holds the note's category (T51 adds it to print `category=` on the `SETUP` line; check its name). `SETUP` line: no change. |
| `ActorState(Seat, AskKey, Now)` | **None.** Read it in the editor. | Add `note_category` to the `scene_card` object after `premise`: one more `Json|SetField` (or `Set Field`) with the key `"note_category"` and the category variable. `you.note` still reads `SeatNote[Seat]`; no change, since only AI seats come here. |
| `InputState(Line, Phase)` | **None.** Read it in the editor. | **Nothing, but check it:** it must not read `SeatNote`, `NoteText` or the category. T07 and T26 list its fields (`actor`, `phase`, `places`, `props`, `cast`, `screen_names`, `typed`, `ask`), none of them a note. |
| `ShowPrep` | **None.** Read it in the editor. | It fills my card through `WBP_Stage.SetInfoTop` (T14), and after T29 starts the scene-title banner (node 14). Change the note it passes to `SetInfoTop`: today my note (`SeatNote[HumanSeat]` or `NoteText`; find which), after T50 the category. If `SetInfoTop` gets a new pin for the category (see `WBP_Stage` below), wire the category variable to it. |
| `PrepPrompt` | `Graphs/BP_Show/PrepPrompt.txt` | The turn line names my secret note. Now: `"Read the card on the right: the scene, your role and secret note, the cast and the stage. Press Start the scene when you are ready."` New (**my call**): `"Read the card on the right: the scene, your role, the note's category, the cast and the stage. Press Start the scene when you are ready."` Change the file and write it back with `write_graph_dsl`. |
| `RunCue`, `CuePrep`, `OpenPrep`, `StartFromPrep`, `StagePrep` | yes | No change. `RunCue`'s `"prep"` cue calls `ScenePrep`; the card is filled from there. |

### `WBP_Stage`

My card sits outside `PrepBox` (T28), so it shows in Scene Prep and in the scene with no change to the prep switch. Its widgets: `YouAre`, `MeText`, `RoleText`, `WantText`, `NoteFrame` (the gold note box; T14 calls it "the director's note in an amber box").

| Graph or widget | Source in `Graphs/` | What T50 changes |
|---|---|---|
| `SetInfoTop` | **None.** Read it in the editor. | It sets my card's texts, the note among them (T32's style-sheet sample reads `"Secret note: Never move to the Back."`, so the card likely shows `Secret note: <text>`; check). New text, from the Rules tab's onboarding table: `Note category: <category>` on one line and `Note: ██████ (bots only)` on the next. Two ways: (1) keep the one note text and set it to both lines, joined with a newline; (2) add a second text (`NoteCatText`) in `NoteFrame` above the note text, with its own pin on `SetInfoTop`. (1) is the smaller change; (2) lets T34 style the two lines apart. |
| `NoteFrame` and the note text | widgets, no graph | If (2), add `NoteCatText` with `UIStyle` (T32): `UIFont("Name")` and the `"Note"` look's ink text, like the note text. |
| `CleanText` | **None.** | **Check first:** T14 says `CleanText` drops everything from U+2190 up except CJK and full-width forms. The blackout `█` is U+2588, so if the card's text runs through `CleanText`, the bar disappears. Also check that `F_UI` (Roboto with Droid Sans Fallback) draws U+2588. If either fails, draw the bar as a small black `Border` (or a run of a character that both keep), and keep the text `Note:` and `(bots only)` around it. Screenshot it. |
| `SetPrepMode` | `Graphs/WBP_Stage/SetPrepMode.txt` | No change: it shows and hides `PrepBox`, the Start button, Send and Pass. My card isn't in `PrepBox`. |
| `DecoyText` | none | T51 removes it. If it is still there, stop: T51 isn't done. |

### Not in T50's Touches, but look

- `WBP_UIStyleSheet`'s sample note text (`Graphs/WBP_UIStyleSheet/EventGraph.txt`, line 49: `"Secret note: Never move to the Back."`) shows the old card. It is a style sample, not the game. Leave it, and tell the person it is out of date.
- `WBP_Title`'s How to play text (`HowText`, set in the designer, not a graph) may still describe the old note. T61 replaces How to play. Read it; if it names the decoy or "your secret note", tell the person.
- `WBP_Stage` in T34 restyles the card (T32's rows 13 and C2 say T50 changes what the card holds), so keep T50's card change plain.

## 7. Check again once T51 is pushed

1. `git log` has T51's commit, `Docs/claims/T51` is released, and `git lfs locks` shows no lock on `BP_Show.uasset` or `WBP_Stage.uasset`.
2. `grep -ri decoy Content/NHOS/Data Tools Graphs Docs/switches.example.json` finds nothing (T51's own done-when).
3. The ten categories T51's person approved: the exact words (part 6's card shows them as written) and the field name (`category`, as `T51.md` says).
4. `prompts.json`: T51's new text of `game` lines 23 and 43 (part 2, a and f), so T50 replaces the right lines; whether T51 touched `_readme` line 5.
5. `check_prompts.py`: T51's versions of `you()`, `card_cases`, the notes check, `TURNS`, `TALK` and `INPUT_CASES`, and the new line numbers for part 4. Whether the overclocker's `TURNS` still break `hold_prop` without a decoy to explain it (T51's call; T50 doesn't change `TURNS`).
6. `Graphs/BP_Show/ScenePrep.txt`: whether T51 wrote it, the name of the category variable, and how the deal loop sets `SeatNote` now.
7. T51's findings in `T51.md`: anything it learned about `ScenePrep`, `ShowPrep` or the card, and whether `WBP_Stage`'s card text changed when `DecoyText` went.
8. `python Tools/check_prompts.py --offline` passes on T51's files before T50 starts, so any failure after is T50's.
