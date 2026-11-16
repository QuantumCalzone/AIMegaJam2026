# T88 build sheet: the director's note clue changes each scene

Back to [T88](T88.md). A PC prep session wrote this on 2026-11-15, without the editor. It is a plan, not a record: nothing here was written to the editor, the design doc or any data file. When T88 writes a graph, its source goes to `Graphs/` as usual.

## Written against, and what to re-check first

**Written against `noHumansOnSet` at `6ea1aec`** (T86: the design doc's audience sentences). The design doc was read, not changed: Rules tab rev 52, Bot Prompts rev 91, Overview rev 147.

While this sheet was written, the session `t78-chain-chip` was building T78 in the repo folder and held the locks on `BP_Show.uasset` and `WBP_Stage.uasset`. **T78 landed as this sheet was pushed** (`b515048`, "checked"), and its locks are gone. Checked against it: T78 changed none of `ActorState.txt`, `PrepPrompt.txt`, the data files, `Tools/check_prompts.py`, `Docs/switches.example.json` or `Docs/ItchPage.md`; `SetPrepMode.txt` gained only the face chip's row (the input row, not my card). So the re-checks marked (T78) below hold at `b515048`; do check 1 again only for what lands after it. T61's PC part still held `Docs/claims/T61` (so `stagehand.json` and `WBP_HowToPlay` are T61's). Before T88 writes anything:

1. **T78's push.** `git log --oneline 6ea1aec..HEAD -- Graphs/BP_Show Graphs/WBP_Stage Content/NHOS/Data Tools/check_prompts.py`. This sheet takes these from the graphs and files T78 may change; each one is marked **re-check (T78)** where it is used:
   - `Graphs/BP_Show/ActorState.txt` (part 5b edits it by its anchors, not by line numbers).
   - `Graphs/BP_Show/PrepPrompt.txt` (part 5d).
   - `Graphs/WBP_Stage/SetPrepMode.txt` (part 6 doesn't change it, but reads it for what shows in Scene Prep).
   - My card's widgets in `WBP_Stage` (`YouAre`, `MeText`, `RoleText`, `WantText`, `NoteFrame` > `NoteBox` > `NoteTitle`, `NoteText`, `NoteHidden`). T78 changes the input row, not the card, but read the tree before part 6.
   - `Tools/check_prompts.py`: part 7 names functions and constants, not line numbers.
2. **The two graphs with no file.** `ScenePrep` and `ShowPrep` have no source in `Graphs/BP_Show/` (T28, T50 and T51 all edited them node by node; their read-backs are lossy). Part 5a and 5c are node edits. Read both in the editor first, as part 0 says, and check nobody wrote a file for them since.
3. **T61's claim.** `git lfs locks | grep claims/T61`. If T61 is still open on the PC, `stagehand.json` (part 2e) and `WBP_HowToPlay` (part 12) are T61's: send that session the new lines, as T88's step 7 says. If T61 is done, T88 changes `stagehand.json` itself (it is in T88's Touches) and asks the dispatcher who takes `WBP_HowToPlay`.
4. **The data files.** If someone changed `scenes.json`'s notes (a new note, a reworded note) since `6ea1aec`, the 50 fields in part 2b must be re-checked against the new text with part 7's checks before they go in.
5. **The design doc.** Read the Rules, Bot Prompts and Overview tabs again; part 1 quotes each passage it changes. If one changed, put the OKed edit into the new text by meaning and show my person the difference.

## In short

| T88 step | Where in this sheet |
|---|---|
| 1. The design first | Question 1 (answered: the category in scene 1), part 1 (the doc edits, question 4) |
| 2. The data | Part 2a (`clues.json`), part 2b (the 50 note fields, question 2), parts 2c to 2e (`prompts.json`, `tells.json`, `stagehand.json`) |
| 3. The emoji check | Part 3 (question 3: the fallback if the UI font draws no emoji) |
| 4. The builder | Part 4 (`BPC_NoteClue`, every function with a draft source) and part 8 (the two switches) |
| 5. The deal and the state | Part 5a (`ScenePrep`), 5b (`ActorState`), the `SETUP` and `CLUE` lines |
| 6. My card | Part 6 (`ClueText`, `SetClue`), part 5c (`ShowPrep`), part 5d (`PrepPrompt`) |
| 7. Everything else | Parts 2c to 2e, part 7 (the checker), part 8 (`switches.example.json`), part 9 (`ItchPage.md`), part 12 (knock-ons) |
| 8. Check | Part 10 |

- **The draw:** scene 1 always gets the category (my person's answer 1). Each later scene draws, at random, a kind this show hasn't used, so a 4-scene show shows the category and 3 of the other 11 kinds. The `clue` switch forces one kind in every scene, scene 1 too.
- **One new component, `BPC_NoteClue`** (`NoteClue` on `BP_Show`), owns all of it: it reads `clues.json` and the notes, draws, builds the text and keeps this scene's clue (`Kind`, `Label`, `How`, `Text`, `Mono`). `BP_Show` calls it from one node in `ScenePrep` (`Deal`), reads it in `ActorState` (`StateObj`) and `ShowPrep` (the getters), and nowhere else.
- **The bots get `scene_card.note_clue`** = `{kind, how, text}` in place of `note_category`. `text` is word for word what my card shows under the label. The input LLM still gets neither the note nor the clue.
- **My card:** the note box reads "Clue: <label>" (`NoteText`), then the clue's text in a new wrapped `ClueText`, then T50's "Note: ██████ (bots only)" row.
- **Locks:** `Content/NHOS/Core/BP_Show.uasset`, `Content/NHOS/UI/WBP_Stage.uasset`; new assets `Content/NHOS/Core/BPC_NoteClue.uasset` and (answer 3) the emoji font assets.
- **Costs money:** only the one relay show Claude plays by hand (Done when). Every other run is free (`--offline`, `--relay --free`, free autoplay, PIE in Test for Free).
- **Needs the relay deploy?** No. The relay bundles `free_mode.json` and reads no note field; none of T88's files is in the relay's bundle. Check with `grep -rn "scenes.json\|clues.json\|prompts.json" Relay/src` before the push; if a file shows up, the push needs my person's OK, as T58 found.

## Questions for my person

Four questions, each asked on its own with the multiple-choice tool, the recommendation first. **All four are answered**; the answers are copied here word for word. T88's Needs line asks for each of them, so T88 can start without asking again.

1. **Scene 1's clue.** Does scene 1 of every show get the category, which the stagehand's first tip and the How to play bullets teach, or does it draw like the other scenes?
   - Options asked: "Category in scene 1 (Recommended)" (scene 1 always shows the category; scenes 2 on draw from the other 11 kinds with no repeat; `clues.json` marks only `category` as allowed in scene 1), "Scene 1 draws like the rest", "Category on the first show only".
   - **My person's answer (2026-11-15):** "Category in scene 1 (Recommended)".
2. **The 50 note fields** (part 2b). Asked with the whole table, "OK as drafted (Recommended)" or "Change some rows".
   - **My person's answer (2026-11-15):** "OK as drafted (Recommended)".
3. **The emoji fallback** (part 3), if the UI font draws no emoji. Options asked: "Engine's Noto Color Emoji (Recommended)", "Monochrome Noto Emoji", "Twemoji or OpenMoji images".
   - **My person's answer (2026-11-15):** "Engine's Noto Color Emoji (Recommended)".
4. **The design doc edits** (part 1), with the full text. Options asked: "OK all edits (Recommended)", "OK, but not the Overview", "Change some edits".
   - **My person's answer (2026-11-15):** "OK all edits (Recommended)".

Don't ask these again in T88. Copy the four answers under "Findings" in `T88.md`.

## Decisions this sheet makes (open to change)

1. **`clues.json` holds one entry per kind with `id`, `label`, `how`, `from`, `scene_1`, `mono` and `prefix`.** `scene_1` is the task's "whether the kind may come in scene 1"; only `category` has it true (answer 1). `mono` says the card shows the text in the mono font (part 6), so a run of `_` can be counted. `prefix` is text the clue starts with: "Opposite of: " for `opposite`, "" for the rest. The prefix is part of the clue's text, so the card and the bots read the same words.
2. **The draw rule, in general form:** scene 1 draws among unused kinds with `scene_1` true; every later scene draws among all unused kinds. With today's file that gives answer 1 exactly, and a later change to `scene_1` needs no graph change. A forced kind (`clue`) skips the draw in every scene and may repeat (it is a test switch). A `clue` value that isn't a kind id is ignored, with `NHOS: CLUE unknown switch clue=<value>`.
3. **A show's used kinds clear at scene 1** (`Deal` with `Scene` 1), so Restart needs no new call: `SetupShow` → `ScenePrep` with `SceneNum` 1.
4. **`BPC_NoteClue` finds the note by id** (`NoteId`, which `ScenePrep` already sets for the `SETUP` line) and reads `scenes.json`'s notes itself. So `ScenePrep` passes two plain values and `BP_Show` holds no note object for it.
5. **`Build` returns the text exactly as the card shows it**, the prefix included. `ActorState` sends that same text. One source of truth for what I could see.
6. **Pig Latin follows the task's rule strictly:** every leading consonant moves, `y` counts as a consonant, and "qu" is not kept together. So "question." becomes "Uestionqay." and "your" becomes "ouryay". The checker's reference (part 7) does the same.
7. **First letters keep each word's own punctuation**, not only the end's: "turn," becomes "t…,". The task's example has only the end's.
8. **The built kinds work on letters a to z only, in either case** (the notes are plain ASCII). "Contains" in Blueprint ignores case by default, which the vowel test relies on (`PlanChar` does the same).
9. **`tells.json`'s `note` tell changes only its `means`**; its `line` ("They caught you guessing at the director's note.") names no category, so it stays.
10. **The stagehand's Scene Prep line stays true** with answer 1, because the tip shows once per show, in scene 1, when the clue is the category. It gains "this time" so a new player isn't surprised in scene 2 (part 2e, in question 4's doc edit).
11. **`NoteCategory` stays a `BP_Show` variable.** `ScenePrep` still sets it and the `SETUP` line still prints `category=`; only `ActorState` stops sending it.
12. **The emoji clue gets its own font only where it shows** (part 3): `ClueText` switches to the emoji font when the kind is `emoji`, so F_UI and every other text in the game stay as they are.

## Wording that comes from the task or the doc

- The twelve ids, card labels and examples: T88.md's table, word for word.
- The four written fields' limits: T88.md step 2.
- The doc's two note lines in `prompts.json` `game` and the checker's `DOC_NOTE_LINES`: whatever question 4 OKs, word for word (part 1b).
- The stagehand's line: the doc's onboarding table, word for word, straight apostrophes (part 2e).

## 0. Before you start

1. Read "Written against" above and do its five checks.
2. `git lfs locks`: no one else holds `BP_Show.uasset` or `WBP_Stage.uasset`. Claim T88 and lock both, as the plan says.
3. The editor must have today's `BP_Show` and `WBP_Stage` loaded (the memory "Editor stale after a pull": after a pull that changed them, reload the packages before you read or save).
4. **Read `ScenePrep` and `ShowPrep` in the editor** (`find_nodes` and `get_node_infos`; trace from `K2Node_FunctionEntry_0`, as T50 found for `ActorState`'s orphan chains). Record:
   - in `ScenePrep`: the node that sets `NoteId`, the `SetNoteCategory` node, T50's `SetArrayElem` that blanks `SeatNote[HumanSeat]`, the `BuildCast` call, the `ShowPrep` call, the `SETUP` print and its `Append` chain, and the `OpenPrep` call at the end;
   - in `ShowPrep`: the `SetInfoTop` call and the `Append("Note category: ", NoteCategory)` on its `Note` pin (T50).
   Save the list in the task's scratch folder. Reading a Blueprint marks it dirty (T47): check `AssetTools.is_dirty` and reload if you must not save.
5. `BP_Show` reads only `ScenePrep`, `ShowPrep` and `ActorState` for the note (T50 checked all 99 graphs). Confirm with `find_nodes` for `NoteCategory` and `SeatNote` that nothing new reads them.

## 1. The design doc (question 4)

Read at Rules rev 52, Bot Prompts rev 91 and Overview rev 147. Each edit names its node id. The prep session changed nothing in the doc. My person has OKed all of it (1d, which settles T88 step 1's "Show me the edit before you save it"); T88 saves it with the Claude Docs connector.

### 1a. Rules tab

1. **Scene Prep, the note bullet** (`.843`).
   - Old: "Only the AI actors get the secret director’s note. You don’t, and you know it. The scene card shows everyone the note’s category, such as Props."
   - New: "Only the AI actors get the secret director’s note. You don’t, and you know it. Your card shows a clue to it instead: its category in scene 1, such as Props, then a new kind of clue each scene, such as only its vowels or a riddle from the director. No kind of clue comes twice in a show."
2. **Scene Prep, what the AIs know** (`.4947`).
   - Old: "The AIs know you lack the note and can see its category. They follow it subtly so you can’t simply copy them, never say it aloud during the scene, and treat anyone who only matches the category, or copies a turn late, as a suspect."
   - New: "The AIs know you lack the note and see exactly which clue you got. They follow it subtly so you can’t simply copy them, never say it aloud during the scene, and treat anyone who only matches the clue, or copies a turn late, as a suspect."
3. **Scene Prep, a new bullet after `.4947`:** "The twelve kinds of clue: the category, the vowels only, the consonants only, the first letters, the words scrambled, Pig Latin, the key word hidden, only the key word, emoji, the opposite rule, a riddle from the director, and the note autocorrected."
4. **Scene Prep, the pause** (`.8385`): "… your role and your want, the note’s category, the cast …" becomes "… your role and your want, the note’s clue, the cast …".
5. **The Scene & acting, your card** (`.8620`): "During the scene, your screen shows only your own card: your role, your want and the note’s category." becomes "… your role, your want and the note’s clue."
6. **Free Talk** (`.5603`).
   - Old: "The scene is over, so actors may name the director’s note when they accuse someone."
   - New: "The scene is over, so actors may name the director’s note when they accuse someone. They hold you only to what your clue could tell you."
7. **Onboarding table, the Scene Prep row** (`.6880`).
   - On screen, old: "Scene card: story, your role, your want, **Note category: Props**, **Note: ██████ (bots only)**"
   - On screen, new: "Scene card: story, your role, your want, **Clue: Category**, **Props**, **Note: ██████ (bots only)**. From scene 2, a new kind of clue, such as **Clue: Vowels only**, **_e_e_ _o_e _o __e _a__.**"
   - Earpiece line, old: "“I could only get you the category. They have the full note, and they know you don’t. Watch turn 1.”"
   - Earpiece line, new: "“I could only get you the category this time. They have the full note, and they know you don’t. Watch turn 1.”"
8. **Left as they are:** "You act blind on turn 1 …" (`.5180`, still true: a clue is not the note); the stagehand bullet "It explains the category hint inside the fiction: “I could only sneak you the category.”" (`.6397`, still true for scene 1, the only Scene Prep with a tip).

### 1b. Bot Prompts tab, "Opening prompt: game rules" (code block `.9010`, its first text run `.9011`)

These two lines are copied into `prompts.json` `game` and the checker's `DOC_NOTE_LINES` word for word (parts 2c and 7).

1. Old: "- Every actor sees the director's note category. Only the AI actors see the note itself. The human does not have the note and knows it, so they will watch you and copy."
   New: "- Only the AI actors see the director's note. The human sees only a clue to it, a different kind each scene, and you see exactly which clue they got. The human knows they lack the note, so they will watch you and copy."
2. Old: "- Fitting the category is not proof. An actor who only matches the category, or copies the others a turn late, probably lacks the note."
   New: "- Fitting the clue is not proof. An actor who only matches what the clue could tell them, or copies the others a turn late, probably lacks the note."
3. Left as they are: "Follow the note in every scene, but subtly …" and "In Free Talk the scene is over, so you may name the note …" (they name no category). The line above the block ("The “a turn late” clause is a difficulty knob …") stays.

### 1c. Overview tab (outside the task's two tabs; in question 4 so the doc stays true)

- "How a show works", Scene Prep (`.4230`). Old: "Scene Prep: everyone gets a scene card showing the director’s note category. Only the bots get the note itself, and they know you don’t have it." New: "Scene Prep: everyone gets a scene card, and yours shows a clue to the director’s note: its category in scene 1, then a new kind of clue each scene. Only the bots get the note itself, and they know you don’t have it."

### 1d. My person's answer to question 4

**My person's answer (2026-11-15):** "OK all edits (Recommended)". T88 saves every edit in 1a, 1b and 1c word for word with the Claude Docs connector (no need to show them again, unless a tab changed since the revs above: then show the difference), and copies 1b's two lines into `prompts.json` `game` and `DOC_NOTE_LINES`. Save straight edits, not suggestions: my person OKed this text.

## 2. The data

### 2a. `Content/NHOS/Data/clues.json` (new)

```json
{
	"_readme": [
		"The kinds of clue to the director's note that the human's card shows (T88). BPC_NoteClue on BP_Show reads this file once per run. At each Scene Prep it draws one kind this show hasn't used: scene 1 draws only among kinds with scene_1 true (today only category), and every later scene among all unused kinds, so no kind repeats in a show. Local/switches.json's clue forces one kind by its id, in every scene.",
		"id: the kind's id, which the log and the state use. label: the card's name for it ('Clue: <label>'). how: one line, sent to the AI actors as scene_card.note_clue.how, that says how the clue was made from the note. from: 'built' when BPC_NoteClue.Build makes the text from the note's words (and its key), or the name of the note's field in scenes.json that holds the text. prefix: text the clue starts with, on the card and in the state. mono: the card shows the text in the mono font, so a run of blanks can be counted.",
		"The clue's text reaches the AI actors word for word as scene_card.note_clue.text, with kind and how. The input LLM never gets the note or the clue. Tools/check_prompts.py checks that this file holds the twelve kinds, that every 'from' that isn't 'built' is a field every note has, and that only category has scene_1 true."
	],
	"kinds": [
		{"id": "category",      "label": "Category",          "from": "category",    "prefix": "",              "scene_1": true,  "mono": false, "how": "the note's category, one word that says what kind of thing the note is about"},
		{"id": "vowels",        "label": "Vowels only",       "from": "built",       "prefix": "",              "scene_1": false, "mono": true,  "how": "the note with every letter except a, e, i, o and u turned into _; spaces and punctuation kept"},
		{"id": "first_letters", "label": "First letters",     "from": "built",       "prefix": "",              "scene_1": false, "mono": false, "how": "the first letter of each word of the note, then …, with each word's punctuation kept"},
		{"id": "consonants",    "label": "Consonants only",   "from": "built",       "prefix": "",              "scene_1": false, "mono": true,  "how": "the note with a, e, i, o and u turned into _"},
		{"id": "scrambled",     "label": "Scrambled words",   "from": "built",       "prefix": "",              "scene_1": false, "mono": false, "how": "the note with the letters of each word shuffled in place; word order and punctuation kept"},
		{"id": "pig_latin",     "label": "Pig Latin",         "from": "built",       "prefix": "",              "scene_1": false, "mono": false, "how": "the note in Pig Latin: each word's leading consonants moved to its end plus ay, or yay after a word that starts with a vowel"},
		{"id": "key_blank",     "label": "Key word hidden",   "from": "built",       "prefix": "",              "scene_1": false, "mono": false, "how": "the whole note with its one key word blacked out, one block per letter"},
		{"id": "key_only",      "label": "Only the key word", "from": "built",       "prefix": "",              "scene_1": false, "mono": false, "how": "the note with every word blacked out except its one key word, one block per letter"},
		{"id": "emoji",         "label": "Emoji",             "from": "emoji",       "prefix": "",              "scene_1": false, "mono": false, "how": "two to four emoji written to stand for the note"},
		{"id": "opposite",      "label": "Opposite day",      "from": "opposite",    "prefix": "Opposite of: ", "scene_1": false, "mono": false, "how": "the reverse of the note's rule; the human must do the opposite of it"},
		{"id": "riddle",        "label": "Director's riddle", "from": "riddle",      "prefix": "",              "scene_1": false, "mono": false, "how": "a riddle of at most 10 words in the director's voice that hints at the note without its key word"},
		{"id": "autocorrect",   "label": "Autocorrect",       "from": "autocorrect", "prefix": "",              "scene_1": false, "mono": false, "how": "the note with two or three words swapped for words spelled almost the same"}
	]
}
```

- **The `how` lines are for the bots.** Each says what the human could and couldn't learn from the clue, in plain words, with no example from the note itself. None names a provider or a persona (the checker's leak check reads every state, and `how` is in it).
- One entry per line keeps the file readable; the game reads it the same way. Tabs, as in the other data files.

### 2b. `scenes.json`: the 50 note fields (question 2)

Each of the 10 notes keeps `id`, `category` and `note` and gains five fields, in this order: `key`, `emoji`, `opposite`, `riddle`, `autocorrect`. The limits (T88 step 2): `key` is one whole word of the note, as written there; `emoji` is 2 to 4 emoji; `opposite` is no longer than the note (in words); `riddle` is at most 10 words, in the director's voice, without the key word; `autocorrect` is the note with two or three words changed to near-spellings, the same word count, still readable.

Every draft below passes those limits (checked with part 7's rules in a scratch script). Each emoji is one code point from U+1F000 up, except ❓ (U+2753, an emoji by default, no variation selector), and **every one is in the engine's `NotoColorEmoji.ttf`** (Emoji 11, 2018; part 3). One first idea, 🧍 (standing person, Emoji 12) for `stay_center`, is not in that font, so 🗿 (a statue: never move) took its place.

| Note (`id`) | `key` | `emoji` | `opposite` (the card adds "Opposite of: ") | `riddle` | `autocorrect` (changed words in bold) |
|---|---|---|---|---|---|
| `never_back`: Never move to the Back. | Back | 🚫🚶🔙 | Always move to the Back. | Some corners of my stage are cursed. | Never **moose** to the **Bach**. |
| `stay_center`: Move to Center in your first turn, then never move anywhere else. | Center | 🎯📌🗿 | Never go to Center, and keep moving all scene. | Find my spotlight early, then put down roots. | Move to Center in your **thirst** turn, then never move anywhere **elks**. |
| `hold_prop`: Grab a prop in your first turn and hold it all scene. Never throw it or give it away. | hold | 🧸🔒🙅 | Never hold a prop for long. Throw or give away anything you grab. | Whatever you pick up first, love it forever. | Grab a **prawn** in your first turn and hold it all **seen**. Never throw it or give it away. |
| `give_every_turn`: Grab a prop, then give it to another actor on your next turn. | give | 🎁👉🧑 | Grab a prop, then never let another actor have it. | Take something, then make a gift of it. | **Crab** a prop, then give it to another actor on your next **tern**. |
| `throw_once`: Throw something at least once, at the actor you trust least. | Throw | 🤾💥🤨 | Never throw anything at the actor you trust most. | Your least favorite castmate deserves a flying gift. | Throw something at **lest** once, at the actor you **thrust** least. |
| `riser_once`: Climb onto the Riser at least once. | Riser | 🧗📦🔝 | Never climb onto the Riser. | Every actor deserves one moment above the rest. | **Clime** onto the Riser at **yeast** once. |
| `keep_moving`: Move to a different place every turn. | different | 🏃🔀📍 | Stay in the same place every turn. | A rolling robot gathers no suspicion. | **Moo** to a different **palace** every turn. |
| `look_first`: Start every turn by looking at another actor. | looking | 👀🧑🔁 | Never look at another actor on any turn. | Before you act, lock eyes with a castmate. | Start every **churn** by looking at another **factor**. |
| `favorite_prop`: Mention your favorite prop every time you speak. | favorite | 💬💖🎩 | Never mention any prop when you speak. | Every line, gush about the prop you love most. | Mention your favorite **prom** every **thyme** you speak. |
| `ask_question`: End every line with a question. | question | 💬🔚❓ | End no line with a question. | Why end a line any other way? | **Bend** every **lion** with a question. |

What each emoji row says: never_back 🚫 no, 🚶 walking, 🔙 back. stay_center 🎯 the bullseye (the middle), 📌 pinned, 🗿 a statue. hold_prop 🧸 a prop, 🔒 locked, 🙅 no (giving it up). give_every_turn 🎁 a gift, 👉 to, 🧑 a person. throw_once 🤾 a throw, 💥 a hit, 🤨 distrust. riser_once 🧗 climbing, 📦 the box, 🔝 on top. keep_moving 🏃 running, 🔀 shuffling, 📍 places. look_first 👀 looking, 🧑 at a person, 🔁 every time. favorite_prop 💬 speaking, 💖 love, 🎩 a prop. ask_question 💬 a line, 🔚 its end, ❓ a question.

For reference, what the seven built kinds make from these notes (the reference builder in part 7; scrambled differs every run):

| Note | Pig Latin (the longest kind) | Vowels only |
|---|---|---|
| `never_back` | Evernay ovemay otay ethay Ackbay. | `_e_e_ _o_e _o __e _a__.` |
| `hold_prop` (the longest: 19 words, 132 characters) | Abgray ayay oppray inyay ouryay irstfay urntay andyay oldhay ityay allyay enescay. Evernay owthray ityay oryay ivegay ityay awayyay. | `__a_ a __o_ i_ _ou_ _i___ _u__ a__ _o__ i_ a__ __e_e. _e_e_ ___o_ i_ o_ _i_e i_ a_a_.` |
| `ask_question` | Endyay everyyay inelay ithway ayay uestionqay. | `E__ e_e__ _i_e _i__ a _ue__io_.` |

**The new note entries, as they go into `scenes.json`** (one note per line, as today; tabs):

```json
		{ "id": "never_back", "category": "Movement", "note": "Never move to the Back.", "key": "Back", "emoji": "🚫🚶🔙", "opposite": "Always move to the Back.", "riddle": "Some corners of my stage are cursed.", "autocorrect": "Never moose to the Bach." },
		{ "id": "stay_center", "category": "Movement", "note": "Move to Center in your first turn, then never move anywhere else.", "key": "Center", "emoji": "🎯📌🗿", "opposite": "Never go to Center, and keep moving all scene.", "riddle": "Find my spotlight early, then put down roots.", "autocorrect": "Move to Center in your thirst turn, then never move anywhere elks." },
		{ "id": "hold_prop", "category": "Props", "note": "Grab a prop in your first turn and hold it all scene. Never throw it or give it away.", "key": "hold", "emoji": "🧸🔒🙅", "opposite": "Never hold a prop for long. Throw or give away anything you grab.", "riddle": "Whatever you pick up first, love it forever.", "autocorrect": "Grab a prawn in your first turn and hold it all seen. Never throw it or give it away." },
		{ "id": "give_every_turn", "category": "Props", "note": "Grab a prop, then give it to another actor on your next turn.", "key": "give", "emoji": "🎁👉🧑", "opposite": "Grab a prop, then never let another actor have it.", "riddle": "Take something, then make a gift of it.", "autocorrect": "Crab a prop, then give it to another actor on your next tern." },
		{ "id": "throw_once", "category": "Props", "note": "Throw something at least once, at the actor you trust least.", "key": "Throw", "emoji": "🤾💥🤨", "opposite": "Never throw anything at the actor you trust most.", "riddle": "Your least favorite castmate deserves a flying gift.", "autocorrect": "Throw something at lest once, at the actor you thrust least." },
		{ "id": "riser_once", "category": "Movement", "note": "Climb onto the Riser at least once.", "key": "Riser", "emoji": "🧗📦🔝", "opposite": "Never climb onto the Riser.", "riddle": "Every actor deserves one moment above the rest.", "autocorrect": "Clime onto the Riser at yeast once." },
		{ "id": "keep_moving", "category": "Movement", "note": "Move to a different place every turn.", "key": "different", "emoji": "🏃🔀📍", "opposite": "Stay in the same place every turn.", "riddle": "A rolling robot gathers no suspicion.", "autocorrect": "Moo to a different palace every turn." },
		{ "id": "look_first", "category": "Looks", "note": "Start every turn by looking at another actor.", "key": "looking", "emoji": "👀🧑🔁", "opposite": "Never look at another actor on any turn.", "riddle": "Before you act, lock eyes with a castmate.", "autocorrect": "Start every churn by looking at another factor." },
		{ "id": "favorite_prop", "category": "Speech", "note": "Mention your favorite prop every time you speak.", "key": "favorite", "emoji": "💬💖🎩", "opposite": "Never mention any prop when you speak.", "riddle": "Every line, gush about the prop you love most.", "autocorrect": "Mention your favorite prom every thyme you speak." },
		{ "id": "ask_question", "category": "Speech", "note": "End every line with a question.", "key": "question", "emoji": "💬🔚❓", "opposite": "End no line with a question.", "riddle": "Why end a line any other way?", "autocorrect": "Bend every lion with a question." }
```

Write the emoji as the characters themselves (UTF-8), not `\u` escapes: the game reads the file as UTF-8 (T44's file already has curly quotes), and Python's `json.load` reads both.

**`scenes.json` `_readme`, the notes line.** Old: "notes: each scene draws one note, and every AI actor gets it; the human's seat gets none (T50). Its 'category' (Movement, Props, Looks or Speech) says what kind of thing the note is about and never what to do; T50 shows it to everyone. A note applies during the scene's 3 turns. Notes are mostly physical, so the log shows who follows them, and each one must work in every story, with any card's four props. Notes never ask everyone to grab the same single prop."
New: "notes: each scene draws one note, and every AI actor gets it; the human's seat gets none (T50). The human's card shows a clue to it instead, a different kind each scene (T88, clues.json). Its 'category' (Movement, Props, Looks or Speech) says what kind of thing the note is about and never what to do; it is scene 1's clue. The other fields feed the other kinds: 'key' is one word of the note, written as it is there; 'emoji' is 2 to 4 emoji; 'opposite' is the reverse rule, no longer than the note; 'riddle' is at most 10 words in the director's voice, without the key word; 'autocorrect' is the note with two or three words changed to near-spellings. A note applies during the scene's 3 turns. Notes are mostly physical, so the log shows who follows them, and each one must work in every story, with any card's four props. Notes never ask everyone to grab the same single prop."

**My person's answer to question 2 (2026-11-15):** "OK as drafted (Recommended)". All 50 fields go in as in the table above, unchanged.

### 2c. `prompts.json`

Each line is found by its text; line numbers are at `6ea1aec`. **Re-check (T78)**: T78 doesn't name `prompts.json` in its Touches.

1. **`game`, line 14** (the doc's line 1, part 1b, word for word). Old: "  - Every actor sees the director's note category. Only the AI actors see the note itself. The human does not have the note and knows it, so they will watch you and copy." New: "  - Only the AI actors see the director's note. The human sees only a clue to it, a different kind each scene, and you see exactly which clue they got. The human knows they lack the note, so they will watch you and copy."
2. **`game`, line 30, "Reading the state"** (not in the doc). Old: "- \"scene_card\" is the story: its title, its premise and \"note_category\", the category of the director's note. Every actor sees the category, the human too." New: "- \"scene_card\" is the story: its title, its premise and \"note_clue\", the clue to the director's note that the human sees this scene: its \"kind\", \"how\" it was made from the note, and its exact \"text\". It changes every scene. You hold the note itself, so you can tell how much the clue gives away."
3. **`game`, line 40, "Spotting the human".** Old: "- The note: compare what each actor does with what your note asks. The human can only guess from the category and from watching you." New: "- The note: compare what each actor does with what your note asks. The human can only guess from the clue and from watching you."
4. **`game`, line 41** (the doc's line 2, part 1b, word for word). Old: "  - Fitting the category is not proof. An actor who only matches the category, or copies the others a turn late, probably lacks the note." New: "  - Fitting the clue is not proof. An actor who only matches what the clue could tell them, or copies the others a turn late, probably lacks the note."
5. **`game`, line 65, the `tell` line** (it copies `tells.json`'s `note` means, part 2d). Old: "… note (only matched the note's category, or missed the note), …" New: "… note (only matched the note's clue, or missed the note), …". The rest of the line stays.
6. **`_readme`, line 2:** `scene_card {title, premise, note_category}` becomes `scene_card {title, premise, note_clue {kind, how, text}}`.
7. **`_readme`, line 4.** Old: "The director's note (T50): only the AI seats get it. Every actor ask carries its category in scene_card.note_category (the note's 'category' in scenes.json) and the note itself in you.note. The human's seat holds no note and never gets an actor ask, and the input LLM gets neither the note nor its category." New: "The director's note (T50): only the AI seats get it, in you.note. The human's card shows a clue to it, a different kind each scene (T88): every actor ask carries that clue in scene_card.note_clue, with its kind (an id in clues.json), how it was made (the kind's 'how') and its exact text as the card shows it. The human's seat holds no note and never gets an actor ask, and the input LLM gets neither the note nor the clue."
8. `asks`: none names the category (checked at `6ea1aec`), so none changes.

### 2d. `tells.json`

Only the `note` entry's `means` (decision 9). Old: `"means": "only matched the note's category, or missed the note"`. New: `"means": "only matched the note's clue, or missed the note"`. At `6ea1aec` the checker only needs `means` to be filled (`check_files`, the tells block); it doesn't compare it with `prompts.json`'s tell line, but parts 2c.5 and 2d keep the two the same words anyway.

### 2e. `stagehand.json` (T61's file while T61 is open; see "Written against", check 3)

The `scene_prep` moment's `line`, word for word from the doc's onboarding table after question 4 (straight apostrophes). Old: "I could only get you the category. They have the full note, and they know you don't. Watch turn 1." New: "I could only get you the category this time. They have the full note, and they know you don't. Watch turn 1." (20 words; the file's limit is 25.)

**If T61 is still open:** send T61's PC session (the dispatcher knows it) one message with this line and part 12's How to play bullet 2, and don't change the file. Write in `T88.md`'s findings that it was sent.

## 3. The emoji check and the fallback (question 3)

**What the files say today, read without the editor:**

- `F_UI` is the engine's Roboto with Droid Sans Fallback as its fallback typeface (T14). Neither font has a glyph for any emoji in part 2b: their character maps (`<UE_ROOT>/Engine/Content/Slate/Fonts/Roboto-Bold.ttf`, `Roboto-Regular.ttf`, `DroidSansFallback.ttf`) hold no code point from U+1F000 up and not U+2753. So **the card will almost surely draw no emoji**, and T88's PIE check (step 3) is expected to fail. Run it anyway: it is cheap and it shows what the player would see (a box or nothing).
- Slate can draw color emoji: its font renderer loads glyphs with `FT_LOAD_COLOR` and handles BGRA bitmaps (`Engine/Source/Runtime/SlateCore/Private/Fonts/SlateFontRenderer.cpp`). The editor's own default font adds `NotoColorEmoji.ttf` as an emoji sub-font, but only when `GIsEditor` (`LegacySlateFontInfoCache.cpp`, "Emoji (editor-only)"), and only to the engine's default font, not to `F_UI`.
- **The engine already ships Noto Color Emoji:** `<UE_ROOT>/Engine/Content/Editor/Slate/Fonts/NotoColorEmoji.ttf`, 7,792,004 bytes, "Version 2.017; noto-emoji 20180810" (Emoji 11), © 2013 Google Inc., **SIL Open Font License 1.1** (its `name` table says so, and so does `Engine/Source/ThirdParty/Licenses/Noto_License.txt`). It is under `Editor/`, so a packaged game doesn't have it unless the project imports it. Using it needs **no download**.

**Do the PIE check in a game window too.** PIE runs with `GIsEditor` true. To see what a packaged build shows, also look in a `-game` window (the "Play the game in its own window" command), where `GIsEditor` is false.

**The options for question 3** (the task's two, plus the engine's font):

1. **The engine's `NotoColorEmoji.ttf` as the clue's emoji font (Recommended in the question).** Copy it to `SourceAssets/Fonts/NotoColorEmoji.ttf` (`.ttf` is already an LFS type in `.gitattributes`), import it as a font face `Content/NHOS/UI/Fonts/FF_NotoColorEmoji` (loading policy Inline), and make a font `Content/NHOS/UI/Fonts/F_Emoji` with that face as its default typeface. `WBP_Stage.SetClue` sets `ClueText`'s font to `F_Emoji` when the kind is `emoji` (decision 12; part 6). Color emoji, matching the clay cartoon look. Cost: about 7.8 MB in the pak. The license travels inside the font file (OFL allows bundling it with the game; the copyright and license are in its `name` table). An Emoji 11 font, so the checker (part 7) checks every emoji against the TTF's character map.
2. **The monochrome Noto Emoji font (SIL OFL), the task's first option.** A download from Google Fonts (name, source and size to be given before it). Black and white, so it can take the card's ink color; a few hundred KB.
3. **Twemoji (CC BY 4.0) or OpenMoji (CC BY-SA 4.0) as images,** the task's second option. Needs an image per emoji used (28 different ones), a credit line, and a different widget for the emoji clue (an image row, not text); the bots still get the emoji characters. The most work.

**Where the font goes in the editor** (option 1; option 2 is the same with the other file):

1. Copy the TTF into `SourceAssets/Fonts/` (a plain file copy, no download).
2. Import with an editor Python script through Unreal MCP (T14 found MCP has no font import tool; `AssetToolsHelpers.get_asset_tools().import_asset_tasks` with an `AssetImportTask` on the `.ttf`, `automated = True`, destination `/Game/NHOS/UI/Fonts`). Check what it made: a `FontFace`, and maybe a `Font`. Name them as above.
3. If the import makes no `Font`, create one (`unreal.Font` via `AssetTools.create_asset` with `FontFactory`), then set its composite font's default typeface to the face. If Python can't reach the composite font, set it in the font editor by hand and say so in the findings.
4. **LFS:** `.ttf` and `.uasset` already have LFS rules in `.gitattributes` (checked at `6ea1aec`), so no new rule is needed. Run `git check-attr filter SourceAssets/Fonts/NotoColorEmoji.ttf` before the commit; it must say `lfs`.
5. `Docs/Assets.md`: a row for `FF_NotoColorEmoji` / `F_Emoji`: source `<UE_ROOT>/Engine/Content/Editor/Slate/Fonts/NotoColorEmoji.ttf` (UE 5.8.4), Noto Color Emoji 2.017 by Google, SIL OFL 1.1, used for the emoji clue on the card only.

**My person's answer to question 3 (2026-11-15):** "Engine's Noto Color Emoji (Recommended)". So option 1: copy the engine's `NotoColorEmoji.ttf` (no download), import it as `F_Emoji`, and use it only for `ClueText` when the clue is `emoji`. It applies only if step 3's PIE check shows that the card draws no emoji; if the card draws them after all (it shouldn't, see above), add nothing and say so in the findings.

## 4. `BPC_NoteClue` (new component, `Content/NHOS/Core/BPC_NoteClue.uasset`)

Add it to `BP_Show` as a public component named `NoteClue`, as T20 added `Audio` and T61 `Stagehand`. `BP_Show` reads its results with variable getters (`Class|BPCNoteClue|GetKind :self (V NoteClue)`), as `StoreTell` reads `BPC_LLMClient`'s `RTell`; so `Kind`, `Label`, `How`, `Text` and `Mono` must not be private. Write each function's source to `Graphs/BPC_NoteClue/<Function>.txt`.

T30's and T65's DSL rules apply (T77-build, "This update" 5 and 6): no `if` without a `return` inside the else path of an earlier `(if … (return))`; a `bind` of a pure expression is read where it is used, so every value that must not move is copied with `set` first. Blueprint's Select evaluates both inputs, so no `select` below has a `get` that could be out of range.

### 4a. Variables

| Name | Type | What it holds |
|---|---|---|
| `Loaded` | Boolean | Both files read |
| `KindObjs` | JsonObject array | `clues.json` `kinds`, as read (a temp for the loop) |
| `KindIds`, `KindLabels`, `KindHows`, `KindFroms`, `KindPrefixes` | String arrays | One entry per kind, in file order |
| `KindFirst`, `KindMono` | Boolean arrays | `scene_1`, `mono` per kind |
| `NoteObjs` | JsonObject array | `scenes.json` `notes`, as read |
| `NoteIds` | String array | Each note's `id`, same order |
| `NoteObj` | JsonObject | The note being built |
| `Note`, `Key` | String | That note's `note` and `key` |
| `Used` | String array | The kinds this show has shown |
| `Pool` | String array | The kinds `Draw` may pick from |
| `Sw` | JsonObject | `Local/switches.json` |
| `ForceKind` | String | The `clue` switch ("" = draw) |
| `ClueTest` | Boolean | The `clue_test` switch |
| `Kind`, `Label`, `How`, `Text` | String | This scene's clue (public) |
| `Mono` | Boolean | Show `Text` in the mono font (public) |
| `Words`, `Outs`, `SChars` | String arrays | Temps of the word builders |
| `WCore`, `WPunct`, `BOut`, `SOut`, `TmpStr` | String | Temps |
| `PK` | Integer | `PigWord`'s consonant count |
| `PStop`, `SDiff`, `TmpB` | Boolean | Temps |

### 4b. `EventGraph`: BeginPlay

`Event BeginPlay` → `Load`. (So `clue_test` logs its 120 lines as the show loads, before any Scene Prep.)

### 4c. `Load.txt`

```lisp
; BPC_NoteClue.Load (T88): reads clues.json (the kinds of clue) and scenes.json's notes once per run, then the switches.
; A missing file leaves Loaded false, and Deal then gives no clue (the show plays on).
(fn Load ()
  (set Loaded false)
  (clear (V KindIds))
  (clear (V KindLabels))
  (clear (V KindHows))
  (clear (V KindFroms))
  (clear (V KindPrefixes))
  (clear (V KindFirst))
  (clear (V KindMono))
  (clear (V NoteIds))
  (bind _cdir (Utilities|Paths|GetProjectContentDirectory))
  (bind (_c _cok) (Json|LoadJsonfromFile (Utilities|Struct|MakeFilePath (cat _cdir "NHOS/Data/clues.json"))))
  (if (not _cok)
    (print "NHOS: CLUES missing Content/NHOS/Data/clues.json")
    (return))
  (bind _ks (Json|GetField _c "kinds"))
  (set KindObjs _ks)
  (for _k (V KindObjs)
    (bind _id (Json|GetField _k "id"))
    (set TmpStr _id)
    (add (V KindIds) (V TmpStr))
    (bind _lb (Json|GetField _k "label"))
    (set TmpStr _lb)
    (add (V KindLabels) (V TmpStr))
    (bind _hw (Json|GetField _k "how"))
    (set TmpStr _hw)
    (add (V KindHows) (V TmpStr))
    (bind _fr (Json|GetField _k "from"))
    (set TmpStr _fr)
    (add (V KindFroms) (V TmpStr))
    (bind _px (Json|GetField _k "prefix"))
    (set TmpStr _px)
    (add (V KindPrefixes) (V TmpStr))
    (bind _s1 (Json|GetField _k "scene_1"))
    (set TmpB _s1)
    (add (V KindFirst) (V TmpB))
    (bind _mo (Json|GetField _k "mono"))
    (set TmpB _mo)
    (add (V KindMono) (V TmpB)))
  (bind (_s _sok) (Json|LoadJsonfromFile (Utilities|Struct|MakeFilePath (cat _cdir "NHOS/Data/scenes.json"))))
  (if (not _sok)
    (print "NHOS: CLUES missing Content/NHOS/Data/scenes.json")
    (return))
  (bind _ns (Json|GetField _s "notes"))
  (set NoteObjs _ns)
  (for _n (V NoteObjs)
    (bind _nid (Json|GetField _n "id"))
    (set TmpStr _nid)
    (add (V NoteIds) (V TmpStr)))
  (set Loaded true)
  (CallFunction|ReadSwitches)
  (print (cat "NHOS: CLUES loaded kinds=" (str (len (V KindIds))) " notes=" (str (len (V NoteIds)))))
  (if (V ClueTest)
    (CallFunction|TestAll)))
```

### 4d. `ReadSwitches.txt`

```lisp
; BPC_NoteClue.ReadSwitches (T88): ForceKind (clue) and ClueTest (clue_test) from Local/switches.json; "" and false
; if the file or the field is missing. Deal calls it at each Scene Prep, so clue can change between scenes.
(fn ReadSwitches ()
  (set ForceKind "")
  (set ClueTest false)
  (bind (_sw _swok) (Json|LoadJsonfromFile (Utilities|Struct|MakeFilePath (cat (Utilities|Paths|GetProjectDirectory) "Local/switches.json"))))
  (if (not _swok)
    (return))
  (set Sw _sw)
  (if (Json|HasField (V Sw) "clue")
    (bind _f (Json|GetField (V Sw) "clue"))
    (set TmpStr _f)
    (set ForceKind (V TmpStr)))
  (if (Json|HasField (V Sw) "clue_test")
    (bind _t (Json|GetField (V Sw) "clue_test"))
    (set TmpB _t)
    (set ClueTest (V TmpB))))
```

### 4e. `Draw.txt`

```lisp
; BPC_NoteClue.Draw(Scene) -> String (T88): the kind for this scene. The clue switch forces one in every scene.
; Otherwise scene 1 draws among unused kinds with scene_1 true (today only category, my person's answer 1), and
; later scenes among all unused kinds, so no kind repeats in a show (at most 4 scenes, 12 kinds).
(fn Draw (Scene)
  (if (and (not (Utilities|String|IsEmpty (V ForceKind))) (>= (Utilities|Array|FindItem (V KindIds) (V ForceKind)) 0))
    (print (cat "NHOS: CLUE forced " (V ForceKind)))
    (return (V ForceKind)))
  (if (not (Utilities|String|IsEmpty (V ForceKind)))
    (print (cat "NHOS: CLUE unknown switch clue=" (V ForceKind))))
  (clear (V Pool))
  (for _i (range (len (V KindIds)))
    (bind _id (get (V KindIds) _i))
    (if (and (or (> Scene 1) (get (V KindFirst) _i)) (< (Utilities|Array|FindItem (V Used) _id) 0))
      (add (V Pool) _id)))
  (if (== (len (V Pool)) 0)
    (print "NHOS: CLUE pool empty, using category")
    (return "category"))
  (return (get (V Pool) (Math|Random|RandomIntegerinRange 0 (- (len (V Pool)) 1)))))
```

### 4f. `Deal.txt` (the one call from `ScenePrep`)

```lisp
; BPC_NoteClue.Deal(Scene, NoteId) (T88): ScenePrep calls it after the note is dealt and before ShowPrep. Scene 1
; starts a new show's list of used kinds (Restart comes through SetupShow -> ScenePrep with scene 1).
(fn Deal (Scene NoteId)
  (if (not (V Loaded))
    (CallFunction|Load))
  (if (not (V Loaded))
    (set Kind "")
    (set Label "")
    (set How "")
    (set Text "")
    (set Mono false)
    (print "NHOS: CLUE none, a data file is missing")
    (return))
  (CallFunction|ReadSwitches)
  (if (<= Scene 1)
    (clear (V Used)))
  (bind _k (CallFunction|Draw :Scene Scene))
  (set Kind _k)
  (add (V Used) (V Kind))
  (bind _i (Utilities|Array|FindItem (V KindIds) (V Kind)))
  (set Label (get (V KindLabels) _i))
  (set How (get (V KindHows) _i))
  (set Mono (get (V KindMono) _i))
  (bind _t (CallFunction|Build :Kind (V Kind) :NoteId NoteId))
  (set Text _t)
  (print (cat "NHOS: CLUE scene=" (str Scene) " kind=" (V Kind) " text=" (V Text))))
```

### 4g. `Build.txt`

```lisp
; BPC_NoteClue.Build(Kind, NoteId) -> String (T88): the clue's text exactly as the card shows it (and the bots read it),
; the kind's prefix included. The built kinds follow T88 step 4; the others read the note's field named in "from".
(fn Build (Kind NoteId)
  (bind _ni (Utilities|Array|FindItem (V NoteIds) NoteId))
  (bind _fi (Utilities|Array|FindItem (V KindIds) Kind))
  (if (or (< _ni 0) (< _fi 0))
    (print (cat "NHOS: CLUE cannot build " Kind " for " NoteId))
    (return ""))
  (set NoteObj (get (V NoteObjs) _ni))
  (bind _n (Json|GetField (V NoteObj) "note"))
  (set Note _n)
  (bind _key (Json|GetField (V NoteObj) "key"))
  (set Key _key)
  (bind _px (get (V KindPrefixes) _fi))
  (if (streq Kind "vowels")
    (return (cat _px (CallFunction|Blank :Text (V Note) :Vowels false))))
  (if (streq Kind "consonants")
    (return (cat _px (CallFunction|Blank :Text (V Note) :Vowels true))))
  (if (streq Kind "first_letters")
    (return (cat _px (CallFunction|FirstLetters :Text (V Note)))))
  (if (streq Kind "scrambled")
    (return (cat _px (CallFunction|Scramble :Text (V Note)))))
  (if (streq Kind "pig_latin")
    (return (cat _px (CallFunction|PigLatin :Text (V Note)))))
  (if (streq Kind "key_blank")
    (return (cat _px (CallFunction|KeyMask :Text (V Note) :Key (V Key) :Hide true))))
  (if (streq Kind "key_only")
    (return (cat _px (CallFunction|KeyMask :Text (V Note) :Key (V Key) :Hide false))))
  (bind _from (get (V KindFroms) _fi))
  (bind _v (Json|GetField (V NoteObj) _from))
  (set TmpStr _v)
  (return (cat _px (V TmpStr))))
```

- If `Json|GetField` can't take a field name from a pin (it reads its name from the node in some versions), branch on the four written kinds and `category` by name instead, as the built kinds do. Check on the first write.
- A `from` that is `built` but no built branch matches returns the prefix only; the checker (part 7) makes sure every `built` id has a branch here by listing them (`BUILT_KINDS`).

### 4h. The word builders

```lisp
; BPC_NoteClue.SplitWord(W) (T88): WCore = W up to its last letter, WPunct = what follows ("Back." -> "Back", ".").
; The notes have no leading punctuation. A word with no letter is all WPunct.
(fn SplitWord (W)
  (set WCore "")
  (set WPunct W)
  (for _i (range (Utilities|String|Len W))
    (bind _c (Utilities|String|GetSubstring :SourceString W :StartIndex _i :Length 1))
    (if (Utilities|String|Contains :SearchIn "abcdefghijklmnopqrstuvwxyz" :Substring _c)
      (set WCore (Utilities|String|Left W (+ _i 1)))
      (set WPunct (Utilities|String|RightChop W (+ _i 1))))))

; BPC_NoteClue.Blank(Text, Vowels) -> String (T88): Vowels true blanks a, e, i, o and u (the consonants kind); false
; blanks every other letter (the vowels kind). Spaces and punctuation stay. Contains ignores case.
(fn Blank (Text Vowels)
  (set BOut "")
  (for _i (range (Utilities|String|Len Text))
    (bind _c (Utilities|String|GetSubstring :SourceString Text :StartIndex _i :Length 1))
    (bind _l (Utilities|String|Contains :SearchIn "abcdefghijklmnopqrstuvwxyz" :Substring _c))
    (bind _v (Utilities|String|Contains :SearchIn "aeiou" :Substring _c))
    (set BOut (cat (V BOut) (select (and _l (xor _v (not Vowels))) "_" _c))))
  (return (V BOut)))

; BPC_NoteClue.FirstLetters(Text) -> String (T88): each word's first letter, then "…", then its own punctuation.
(fn FirstLetters (Text)
  (set Words (Utilities|String|ParseIntoArray Text " "))
  (clear (V Outs))
  (for _w (V Words)
    (CallFunction|SplitWord :W _w)
    (add (V Outs) (cat (Utilities|String|Left (V WCore) 1) "…" (V WPunct))))
  (return (Utilities|String|JoinStringArray (V Outs) " ")))

; BPC_NoteClue.Bars(N) -> String (T88): N blocks (U+2588), one per letter.
(fn Bars (N)
  (set BOut "")
  (for _i (range N)
    (set BOut (cat (V BOut) "█")))
  (return (V BOut)))

; BPC_NoteClue.KeyMask(Text, Key, Hide) -> String (T88): Hide true blacks out the key word (key_blank); false blacks
; out every other word (key_only). Each word keeps its punctuation. Key is matched exactly, as written in the note.
(fn KeyMask (Text Key Hide)
  (set Words (Utilities|String|ParseIntoArray Text " "))
  (clear (V Outs))
  (for _w (V Words)
    (CallFunction|SplitWord :W _w)
    (set TmpB (Utilities|String|EqualExactly(String) (V WCore) Key))
    (if (xor (V TmpB) (not Hide))
      (bind _bars (CallFunction|Bars :N (Utilities|String|Len (V WCore))))
      (add (V Outs) (cat _bars (V WPunct)))
      (else
        (add (V Outs) _w))))
  (return (Utilities|String|JoinStringArray (V Outs) " ")))

; BPC_NoteClue.PigWord(W) -> String (T88): leading consonants (y counts as one) move to the end plus "ay"; a word that
; starts with a vowel adds "yay". A capital stays on the first letter, and punctuation stays at the end.
(fn PigWord (W)
  (CallFunction|SplitWord :W W)
  (set TmpStr (Utilities|String|ToLower (V WCore)))
  (set TmpB (not (Utilities|String|EqualExactly(String) (Utilities|String|Left (V WCore) 1) (Utilities|String|Left (V TmpStr) 1))))
  (set PK 0)
  (set PStop false)
  (for _i (range (Utilities|String|Len (V TmpStr)))
    (bind _c (Utilities|String|GetSubstring :SourceString (V TmpStr) :StartIndex _i :Length 1))
    (if (or (V PStop) (Utilities|String|Contains :SearchIn "aeiou" :Substring _c))
      (set PStop true)
      (else
        (set PK (+ _i 1)))))
  (set SOut (select (== (V PK) 0) (cat (V TmpStr) "yay") (cat (Utilities|String|RightChop (V TmpStr) (V PK)) (Utilities|String|Left (V TmpStr) (V PK)) "ay")))
  (if (V TmpB)
    (set SOut (cat (Utilities|String|ToUpper (Utilities|String|Left (V SOut) 1)) (Utilities|String|RightChop (V SOut) 1))))
  (return (cat (V SOut) (V WPunct))))

(fn PigLatin (Text)
  (set Words (Utilities|String|ParseIntoArray Text " "))
  (clear (V Outs))
  (for _w (V Words)
    (bind _p (CallFunction|PigWord :W _w))
    (add (V Outs) _p))
  (return (Utilities|String|JoinStringArray (V Outs) " ")))

; BPC_NoteClue.ScrambleWord(W) -> String (T88): the word's letters shuffled in place, its punctuation kept. A word with
; two or more different letters never comes out unchanged (at most 20 shuffles; the chance of 20 misses is nil).
(fn ScrambleWord (W)
  (CallFunction|SplitWord :W W)
  (set SChars (Utilities|String|GetCharacterArrayfromString (V WCore)))
  (set SDiff false)
  (for _c (V SChars)
    (if (not (Utilities|String|EqualExactly(String) _c (get (V SChars) 0)))
      (set SDiff true)))
  (set SOut (V WCore))
  (if (V SDiff)
    (for _t (range 20)
      (if (Utilities|String|EqualExactly(String) (V SOut) (V WCore))
        (Utilities|Array|Shuffle (V SChars))
        (set SOut (Utilities|String|JoinStringArray (V SChars) "")))))
  (return (cat (V SOut) (V WPunct))))

(fn Scramble (Text)
  (set Words (Utilities|String|ParseIntoArray Text " "))
  (clear (V Outs))
  (for _w (V Words)
    (bind _s (CallFunction|ScrambleWord :W _w))
    (add (V Outs) _s))
  (return (Utilities|String|JoinStringArray (V Outs) " ")))
```

- **Node names to confirm on the first write:** `Utilities|String|GetCharacterArrayfromString` (Kismet's "Get Character Array from String"), `Utilities|String|Left`, `Utilities|String|RightChop`, `Utilities|Array|Shuffle` (used in `PlayTurn.txt`), `Utilities|String|JoinStringArray` with a separator pin (used with "" nowhere yet; if the separator can't be "", join with "" by a loop of `cat`).
- `PigWord`, `ScrambleWord` and `KeyMask` call `SplitWord`, which writes `WCore` and `WPunct`; each copies what it needs into its own temps before the next call (`TmpStr`, `SOut`), as T65's pure-node trap asks. `PigLatin` and `Scramble` keep the result in a `bind` of a function call, which is impure and so is read once.
- `Words` and `Outs` are shared temps. No builder calls another builder that uses them, so they don't clash.

### 4i. `StateObj.txt` (for `ActorState`)

```lisp
; BPC_NoteClue.StateObj() -> JsonObject (T88): scene_card.note_clue for every actor state: kind, how, text.
(fn StateObj ()
  (bind _o (Json|LoadJsonfromString "{}"))
  (Json|SetField _o "kind" (V Kind))
  (Json|SetField _o "how" (V How))
  (Json|SetField _o "text" (V Text))
  (return _o))
```

### 4j. `TestAll.txt` (the `clue_test` switch)

```lisp
; BPC_NoteClue.TestAll (T88): with clue_test on, Load logs every kind for every note, so the builders can be checked
; from the log with no show: NHOS: CLUETEST <note id> <kind> <text>. 10 notes x 12 kinds = 120 lines.
(fn TestAll ()
  (for _nid (V NoteIds)
    (for _k (V KindIds)
      (bind _t (CallFunction|Build :Kind _k :NoteId _nid))
      (print (cat "NHOS: CLUETEST " _nid " " _k " " _t))))
  (print (cat "NHOS: CLUETEST done " (str (* (len (V NoteIds)) (len (V KindIds)))))))
```

If a nested `for` in one graph is a problem for the DSL, move the inner loop into `TestNote(NoteId)`.

## 5. `BP_Show`

### 5a. `ScenePrep` (node edits; no file, see "Written against" 2)

1. **The clue deal:** a new `Class|BPCNoteClue|Deal` node with `:self` from `GetNoteClue`, `Scene` from `GetSceneNum`, `NoteId` from `GetNoteId`. Wire its exec **after T50's `SetArrayElem` (the human's blank note) and before `BuildCast`**, so it runs before `ShowPrep` (which `ScenePrep` calls after `BuildCast`) and before the `SETUP` print.
2. **The `SETUP` line** gains ` clue=<id>` at the end: one more `Append` of " clue=" and `NoteClue.Kind` (`Class|BPCNoteClue|GetKind`) after `category=<category>`. It reads `NHOS: SETUP human=<id> scene=<card> note=<id> category=<category> scenes=<n> clue=<id>` (keep whatever comes before; T53 added `scenes=`). At the end, the checker's existing `SETUP` regexes still match.
3. Nothing else changes: `NoteCategory` is still set (decision 11), and the deal loop, `BuildCast`, `ShowPrep` and `OpenPrep` stay.
4. If T88 writes a source for `ScenePrep` after all, write it by hand (T51), not from a read-back.

### 5b. `ActorState.txt` (file edit; **re-check (T78)**)

Replace the `note_category` line by its anchor:

```lisp
  (Json|SetField _card "note_category" (V NoteCategory))
```

with

```lisp
  (bind _clue (Class|BPCNoteClue|StateObj :self (V NoteClue)))
  (Json|SetField _card "note_clue" _clue)
```

and add to the comment block at the top: "; T88: scene_card carries note_clue {kind, how, text} (BPC_NoteClue.StateObj) in place of note_category." The key order stays title, premise, note_clue (the checker's sample states use it). Write the whole graph from the file with `write_graph_dsl` (it has a source since T62) or make the same change by nodes, tracing from `K2Node_FunctionEntry_0` (T50's two orphan chains); either way, `Graphs/BP_Show/ActorState.txt` gets the change.

**The input LLM's state** (`InputState`, no file) reads no note and no clue: T50 checked it, and `find_nodes` for `NoteClue` in part 0 confirms nothing else reads the component.

### 5c. `ShowPrep` (node edits; no file)

1. `SetInfoTop`'s `Note` pin: T50's `Append("Note category: ", NoteCategory)` becomes `Append("Clue: ", NoteClue.Label)` (`Class|BPCNoteClue|GetLabel`). `SetInfoTop` still writes it into `NoteText`, unchanged.
2. A new call after `SetInfoTop`: `Class|WBPStage|SetClue :self (GetStage) :Text (NoteClue.Text) :Mono (NoteClue.Mono) :Emoji (streq NoteClue.Kind "emoji")` (part 6b).
3. `ShowPrep` runs at every Scene Prep (it fills the card), so the card shows the new clue in Scene Prep and keeps it through the scene, as T50's line did.

### 5d. `PrepPrompt.txt` (file edit; **re-check (T78)**, and T84 changes this line after T88)

In the `SetPTurn` string, "the note's category" becomes "the note's clue":

```lisp
    (Variables|Default|SetPTurn "Read the card on the right: the scene, your role, the note's clue, the cast and the stage. Press Start the scene when you are ready.")
```

Set the same text as the pin value in the editor if you don't rewrite the graph (T50 did it that way), and add "; T88: \"the note's clue\"." to the file's comment.

### 5e. The log lines (all from `BPC_NoteClue` but `SETUP`)

- `NHOS: CLUES loaded kinds=12 notes=10` once per run.
- `NHOS: SETUP … clue=<id>` per scene (5a).
- `NHOS: CLUE scene=<n> kind=<id> text=<text>` per scene (`Deal`).
- `NHOS: CLUE forced <id>` / `NHOS: CLUE unknown switch clue=<x>` with the switch.
- `NHOS: CLUETEST <note id> <kind> <text>` ×120 and `NHOS: CLUETEST done 120` with `clue_test`.

## 6. `WBP_Stage`: my card's note box

Read the tree first (**re-check (T78)**). At `6ea1aec` the note box is `NoteFrame` > `NoteBox` (a VerticalBox) with `NoteTitle` ("THE DIRECTOR'S NOTE"), `NoteText` (F_UI Bold 20, set by `SetInfoTop`) and T50's `NoteHidden` row (`NoteHiddenLabel`, `NoteBar`, `NoteBotsOnly`).

### 6a. The widget tree

- A new TextBlock **`ClueText`** in `NoteBox`, between `NoteText` and `NoteHidden`: **Auto Wrap Text on**, F_UI Regular 18 (the card's body size; T34 restyles the card later), the note box's cream ink, top padding 2, justification left. Is Variable on.
- `NoteText` now reads "Clue: <label>" (from `ShowPrep`), so it is the clue's heading. Leave its font.
- `NoteHidden` stays as T50 built it, under `ClueText`.
- The card's width doesn't change: `ClueText` wraps inside `NoteBox`.

### 6b. `SetClue.txt` (new)

```lisp
; T88: the clue's text on my card, under "Clue: <label>" (NoteText, from ShowPrep -> SetInfoTop). The built kinds that
; blank letters show in the mono font, so a run of _ can be counted; the emoji kind shows in the emoji font (part 3).
(fn SetClue (Text Mono Emoji)
  (Class|TextBlock|SetText :self (Variables|WBP_Stage|GetClueText) :InText (Utilities|String|ToText Text))
  (bind _f (select Mono (CallFunction|Mono) (Class|UIStyle|UIFont :Role "Body")))
  (if Emoji
    (Class|TextBlock|SetFont :self (Variables|WBP_Stage|GetClueText) :InFontInfo (V EmojiFont))
    (else
      (Class|TextBlock|SetFont :self (Variables|WBP_Stage|GetClueText) :InFontInfo _f))))
```

- `EmojiFont` is a new SlateFontInfo variable on `WBP_Stage`: font object `F_Emoji`, typeface `Default` (check the name the import gives it), size 28 (emoji read small at 18). With answer 3's option 2 it is the monochrome font; with option 3 `SetClue` shows an image row instead (part 3 says what that needs).
- `Mono()` is T65's mono font (DroidSansMono 18). It has `_` and `…` but no `█`, so the mono kinds are only `vowels` and `consonants` (decision 1); `key_blank` and `key_only` stay in F_UI, whose fallback draws `█` (T50).
- `UIStyle.UIFont "Body"` is the card's body font; if `UIFont` takes a size or the role name differs, read `Graphs/UIStyle/` first and use what `RoleText` uses.
- **Never run the clue through `CleanText`**: it drops everything from U+2190 up (T14), which takes `█`, `…` and every emoji.

### 6c. The layout checks (step 6)

- The longest text is `hold_prop` in Pig Latin: 19 words, 132 characters (part 2b). Force it (`"clue": "pig_latin"`, and a note forced by a scratch edit or by restarting until `hold_prop` comes up; the `SETUP` line names the note).
- At 1600 × 900 and at 1440 × 900, in Scene Prep and in turn 1: it wraps inside the card, and **the scene's card (turn 1) has no scroll**. Scene Prep's card scrolled before T88 at some sizes (T34-build row 13, which T34 and T84 settle); compare with a screenshot of the same scene without the clue (`"clue": "category"`), and make sure T88 adds no scroll where there was none.
- If the long text adds a scroll in the scene, drop `ClueText` to 16 before anything else, and say so in the findings for T34.

## 7. `Tools/check_prompts.py`

**Re-check (T78)**: anchors are names, not line numbers.

### 7a. The docstring, "Director's note (T50)" paragraph

Old: "Director's note (T50): only the AI seats get the note. Every actor state's scene_card carries note_category, the note's 'category' from scenes.json, and 'you' carries the note. …"
New: "Director's note (T50, T88): only the AI seats get the note. Every actor state's scene_card carries note_clue {kind, how, text}, the clue the human's card shows this scene (clues.json), and 'you' carries the note. The human's sample seat (Player 3) has no note, and the input converter's state has neither the note nor the clue. The file check also finds the design doc's four note lines in prompts.json 'game', word for word (DOC_NOTE_LINES). A scene turn whose speech holds the note word for word is a WARN. Clues (T88): clues.json holds the twelve kinds (CLUE_KINDS), only category may come in scene 1, every 'from' that isn't 'built' is a field of every note, and each note's key is a whole word of it and its four written fields are filled and within their limits. --log checks every NHOS: CLUETEST line of a built kind against the reference builders below, and that a show's NHOS: CLUE lines name a different kind in each scene, the category in scene 1 (unless the clue switch forced one)."

### 7b. Constants

```python
# T88: the kinds of clue to the director's note (clues.json), in file order; BUILT_KINDS are made by BPC_NoteClue.Build.
CLUE_KINDS = ["category", "vowels", "first_letters", "consonants", "scrambled", "pig_latin",
              "key_blank", "key_only", "emoji", "opposite", "riddle", "autocorrect"]
BUILT_KINDS = ["vowels", "first_letters", "consonants", "scrambled", "pig_latin", "key_blank", "key_only"]
NOTE_FIELDS = ["id", "category", "note", "key", "emoji", "opposite", "riddle", "autocorrect"]
MAX_RIDDLE_WORDS = 10
# T88 answer 3: the emoji font's source file; when it exists, every note emoji must be in its character map.
EMOJI_FONT = ROOT / "SourceAssets" / "Fonts" / "NotoColorEmoji.ttf"
```

(`ROOT` is the checker's repo-root path, `Path(__file__).resolve().parent.parent`. Add `import struct` and `import unicodedata` to its imports.)

`DOC_NOTE_LINES`: lines 1 and 3 become the two new doc lines from part 1b (without the leading "- "), word for word; lines 2 and 4 stay.

### 7c. The reference builders and the note checks (new)

```python
LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
BAR = "█"


def split_word(w):
    """T88: (letters up to the last letter, the punctuation after), as BPC_NoteClue.SplitWord."""
    i = len(w)
    while i > 0 and w[i - 1] not in LETTERS:
        i -= 1
    return w[:i], w[i:]


def build_clue(kind, note):
    """T88: the reference for BPC_NoteClue.Build's built kinds (not scrambled, which is random). note is the scenes.json entry."""
    text, key = note["note"], note.get("key", "")
    words = text.split(" ")
    if kind == "vowels":
        return "".join("_" if c in LETTERS and c.lower() not in "aeiou" else c for c in text)
    if kind == "consonants":
        return "".join("_" if c.lower() in "aeiou" else c for c in text)
    if kind == "first_letters":
        return " ".join(c[:1] + "…" + p for c, p in map(split_word, words))
    if kind == "pig_latin":
        out = []
        for c, p in map(split_word, words):
            lw = c.lower()
            k = next((i for i, ch in enumerate(lw) if ch in "aeiou"), len(lw))
            r = lw + "yay" if k == 0 else lw[k:] + lw[:k] + "ay"
            out.append((r[:1].upper() + r[1:] if c[:1].isupper() else r) + p)
        return " ".join(out)
    if kind in ("key_blank", "key_only"):
        hide = kind == "key_blank"
        return " ".join((BAR * len(c) + p) if (c == key) == hide else w
                        for w, (c, p) in zip(words, map(split_word, words)))
    raise ValueError(kind)


def scramble_ok(note_text, got):
    """T88: each word of got is its note word's letters shuffled, punctuation kept, and changed if it can change."""
    a, b = note_text.split(" "), got.split(" ")
    if len(a) != len(b):
        return False
    for w, g in zip(a, b):
        (c, p), (gc, gp) = split_word(w), split_word(g)
        if p != gp or sorted(c) != sorted(gc) or (len(set(c)) >= 2 and gc == c):
            return False
    return True


def emoji_list(s):
    """T88: the emoji in a string, one per code point; joiners and variation selectors are not emoji."""
    return [ch for ch in s if ch not in "‍️" and not unicodedata.category(ch).startswith("M")]


def font_cmap(path):
    """T88: the code points a TrueType font maps (format 4 and 12 subtables), or None if the file is missing."""
    try:
        f = path.read_bytes()
    except FileNotFoundError:
        return None
    n = struct.unpack(">H", f[4:6])[0]
    tabs = {f[12 + 16 * i:16 + 16 * i].decode("latin-1"): struct.unpack(">II", f[20 + 16 * i:28 + 16 * i]) for i in range(n)}
    off = tabs["cmap"][0]
    cps = set()
    for i in range(struct.unpack(">H", f[off + 2:off + 4])[0]):
        so = struct.unpack(">I", f[off + 8 + 8 * i:off + 12 + 8 * i])[0]
        t = off + so
        fmt = struct.unpack(">H", f[t:t + 2])[0]
        if fmt == 4:
            sc = struct.unpack(">H", f[t + 6:t + 8])[0] // 2
            ends = struct.unpack(f">{sc}H", f[t + 14:t + 14 + 2 * sc])
            starts = struct.unpack(f">{sc}H", f[t + 16 + 2 * sc:t + 16 + 4 * sc])
            for s, e in zip(starts, ends):
                cps.update(range(s, e + 1))
        elif fmt == 12:
            for g in range(struct.unpack(">I", f[t + 12:t + 16])[0]):
                s, e, _ = struct.unpack(">III", f[t + 16 + 12 * g:t + 28 + 12 * g])
                cps.update(range(s, e + 1))
    return cps


def clue_problems(clues, notes):
    """T88: clues.json against CLUE_KINDS, and each note's five clue fields against their limits."""
    errs = []
    kinds = clues.get("kinds", [])
    ids = [k.get("id") for k in kinds]
    if ids != CLUE_KINDS:
        errs.append(f"clues.json: kinds must be {CLUE_KINDS} in that order, not {ids}")
    for k in kinds:
        for f in ("id", "label", "how", "from"):
            if not isinstance(k.get(f), str) or not k.get(f):
                errs.append(f"clues.json: kind {k.get('id')} needs a non-empty '{f}'")
        if not isinstance(k.get("scene_1"), bool) or not isinstance(k.get("mono"), bool) or not isinstance(k.get("prefix"), str):
            errs.append(f"clues.json: kind {k.get('id')} needs scene_1 and mono (true or false) and prefix (a string)")
        if (k.get("from") == "built") != (k.get("id") in BUILT_KINDS):
            errs.append(f"clues.json: kind {k.get('id')}'s from must be 'built' exactly for {BUILT_KINDS}")
        if k.get("from") not in ("built", None) and k.get("from") not in NOTE_FIELDS:
            errs.append(f"clues.json: kind {k.get('id')}'s from '{k.get('from')}' is not a note field")
    if [k.get("id") for k in kinds if k.get("scene_1")] != ["category"]:
        errs.append("clues.json: only category may come in scene 1 (scene_1 true), my person's answer 1 in T88")
    cmap = font_cmap(EMOJI_FONT)
    for n in notes:
        nid, text = n.get("id"), n.get("note", "")
        words = text.split(" ")
        cores = [split_word(w)[0] for w in words]
        for f in ("key", "emoji", "opposite", "riddle", "autocorrect"):
            if not isinstance(n.get(f), str) or not n.get(f).strip():
                errs.append(f"scenes.json: note {nid} needs '{f}' (T88)")
        key = n.get("key", "")
        if key and key not in cores:
            errs.append(f"scenes.json: note {nid}'s key '{key}' is not a whole word of its note, as written there")
        emo = emoji_list(n.get("emoji", ""))
        if not 2 <= len(emo) <= 4:
            errs.append(f"scenes.json: note {nid} needs 2 to 4 emoji, has {len(emo)}")
        if any(ord(ch) < 0x2190 for ch in emo):
            errs.append(f"scenes.json: note {nid}'s emoji holds a letter or symbol below U+2190")
        if cmap is not None and any(ord(ch) not in cmap for ch in emo):
            errs.append(f"scenes.json: note {nid} has an emoji the emoji font can't draw: "
                        f"{[f'U+{ord(ch):04X}' for ch in emo if ord(ch) not in cmap]}")
        if len(n.get("opposite", "").split()) > len(text.split()):
            errs.append(f"scenes.json: note {nid}'s opposite is longer than the note")
        rid = n.get("riddle", "")
        if len(rid.split()) > MAX_RIDDLE_WORDS:
            errs.append(f"scenes.json: note {nid}'s riddle is over {MAX_RIDDLE_WORDS} words")
        if key and key.lower() in [split_word(w)[0].lower() for w in rid.split()]:
            errs.append(f"scenes.json: note {nid}'s riddle says its key word '{key}'")
        auto = n.get("autocorrect", "").split(" ")
        if len(auto) != len(words):
            errs.append(f"scenes.json: note {nid}'s autocorrect must keep the note's {len(words)} words")
        elif not 2 <= sum(a != b for a, b in zip(words, auto)) <= 3:
            errs.append(f"scenes.json: note {nid}'s autocorrect must change two or three words")
    return errs
```

### 7d. `check_files`

1. Load `clues = load_json("clues.json", errors)` with the others, and add `clues.json` to the "Files OK" line in `main`.
2. In the notes loop, the field check becomes: `if set(n) - set(NOTE_FIELDS): errors.append(f"scenes.json: note {n.get('id')} may hold only {', '.join(NOTE_FIELDS)}; every AI actor gets the same note")`. The `note` and `category` check stays.
3. After the loop: `errors.extend(clue_problems(clues or {}, notes))`.
4. Return `clues` in `data` (`data["clues"]`) for the sample states.

### 7e. The sample states: `note_clue` in place of `note_category`, cycling the kinds

- `Show.__init__`: keep `self.clues = data["clues"]["kinds"]`.
- A helper: `def clue_for(self, note, i)`: kind `CLUE_KINDS[i % 12]`; `text` = `build_clue(kind, note)` for a built kind except `scrambled` (use a fixed shuffle, such as each word reversed, which `scramble_ok` accepts for every note word with two different letters; a word like "a" stays), the note's field plus the kind's prefix for the others; returns `{"kind": kind, "how": <the kind's how>, "text": text}`.
- `actor_state`: `"scene_card": {"title": …, "premise": …, "note_clue": self.clue_for(self.note, <a counter>)}`, where the counter is the actor ask's index in `build_jobs`, so the paid and `--relay --free` runs send every kind across the asks.
- `card_cases`: `"note_clue": self.clue_for(note, i)` for card `i` (7 cards, so kinds 0 to 6; the counter above covers the rest).
- `check_note_deal`: its docstring and messages say clue; the test `'"note_category"' not in text` becomes `'"note_clue"' not in text` ("FAIL note: no scene_card.note_clue in {ask}"); the input branch also fails on `'"note_clue"'` and on the sample clue's text (`if note in text or '"note' in text` already catches `"note_clue"`). `main`'s line becomes "Only the AI seats get the note, and every actor state carries the human's clue."
- `check_leaks` reads every state, `how` and `text` included, so a clue that named a provider would fail there with no new code.

### 7f. `--log`

1. `LOG_RE` gains `CLUE|CLUETEST` (put `CLUETEST` before `CLUE` in the alternation, or rely on `\b`: `CLUE\b` doesn't match `CLUETEST`).
2. **`CLUETEST` lines** (a `clue_test` run has no `LOG` line, so check them before the "no NHOS: LOG lines" return): for each `NHOS: CLUETEST <note id> <kind> <text>`, find the note in `scenes.json`; a built kind other than `scrambled` must equal `build_clue(kind, note)`; `scrambled` must pass `scramble_ok`; `opposite` must be the prefix plus the note's `opposite`; the other written kinds and `category` must equal the note's field. Print `CLUETEST: <n> lines, <bad> wrong` and `[FAIL] CLUETEST <note> <kind> | got <text> | want <text>` per wrong line; a run with fewer than 120 lines prints how many are missing. Fails the exit code.
3. **`CLUE` lines** per show: one per scene; no kind twice in a show unless an `NHOS: CLUE forced` line came first; scene 1's kind is `category` unless forced. Each mismatch is a `[FAIL] show <i> | CLUE | …` and fails the exit code. The show summary line gains `clues = <kinds in order>`.
4. **The `SETUP` line's `clue=`** must equal that scene's `CLUE` kind (a cheap cross-check that `ScenePrep` deals before it prints).

## 8. `Docs/switches.example.json`

Two new fields after `emote_test`: `"clue": ""` and `"clue_test": false`. Append to `_readme`:

" clue (T88): force one kind of clue to the director's note in every scene, scene 1 too, by its id in Content/NHOS/Data/clues.json (category, vowels, first_letters, consonants, scrambled, pig_latin, key_blank, key_only, emoji, opposite, riddle, autocorrect), for screenshots of each kind; a forced kind may repeat. It is read at each Scene Prep. \"\" or missing draws as a show does: the category in scene 1, then a kind not yet used. Set it back to \"\" before a person plays. clue_test (T88): when the show loads, log every kind of clue for every note (NHOS: CLUETEST <note id> <kind> <text>, 120 lines), so the builders can be checked from the log with no show (python Tools/check_prompts.py --log). It is read once when the show loads. Set it back to false before a person plays."

## 9. `Docs/ItchPage.md`

Two lines, found by their text.

1. "How a show works", step 1. Old: "… You don't, and they know it: your card shows only the note's category, such as Props." New: "… You don't, and they know it: your card shows only a clue to it, the note's category in scene 1, then a new kind of clue each scene, such as only its vowels or a riddle from the director."
2. "How to fool them". Old: "On turn 1 you act blind, with only the note's category to go on." New: "On turn 1 you act blind, with only the note's clue to go on."

## 10. The checks (step 8 and Done when)

1. `python Tools/check_prompts.py --offline`: files OK (with `clues.json`), no provider name, "Only the AI seats get the note, and every actor state carries the human's clue.", the action rules.
2. `python Tools/check_prompts.py --relay --free`: every ask passes, no WARN. Free mode spends nothing; the relay doesn't change (see "In short"), so no deploy OK is needed.
3. **`clue_test`:** `"clue_test": true` and `"autoplay": false` in `Local/switches.json`, open a game window (or PIE) on the saved assets, let it reach the title, close it. `python Tools/check_prompts.py --log <that log>` reports 120 `CLUETEST` lines, 0 wrong. This checks every built kind against step 4's rules on all 10 notes, more than the "at least two" the task asks; read two notes' lines by eye too and paste them in the findings.
4. **A free autoplay show** (`"mode": "free"`, `"autoplay": true`, `"fast_lines": true`, `"clue": ""`, `"clue_test": false`): reaches `NHOS: SHOW END`, scene 1's `CLUE` is `category`, every scene's kind differs, each `SETUP` has `clue=`, and `--log` passes. `grep -c "note_category"` in the log's request dumps is 0 (if the run dumps states; otherwise read one `HoldLine` state on turn 2: T62's `HoldLine` prints it).
5. **The emoji check** (step 3), before part 2b's emoji go in: put a few emoji on my card in PIE (force `"clue": "emoji"` once `scenes.json` has them, or set `ClueText` by hand in the PIE world) and take a screenshot; then the same in a `-game` window. If they don't draw, ask question 3's answer into effect (part 3) and shoot again.
6. **Thirteen screenshots** in Scene Prep at 1600 × 900, one per kind (force each with `clue`), and the longest text (`hold_prop`, Pig Latin) at 1440 × 900, in Scene Prep and in turn 1 (part 6c). Keep them in the task's scratch folder, not in git. Check each: the label reads "Clue: <label>", the text wraps in the card, `_` runs are countable in the mono kinds, `█` shows in the key kinds, emoji draw, "Opposite of: " leads the opposite.
7. **Claude plays one show through the relay by hand** (Done when; this is the one paid run), with `clue` off and `"mode": "relay"`, from the title, as a real player: acting blind on turn 1 with only the clue. From the log and the screenshots:
   - in scenes whose clue was not the category, no Free Talk line or vote reason holds me to the category ("only matched the category", "the category was Props");
   - accusations about my turn 1 fit what my clue could tell me (a bot may still catch a wrong guess, but not blame me for missing what the clue hid);
   - no bot says the note aloud during a scene (the checker's WARN for a quoted note, and a read of the scene lines).
8. **Findings:** which kinds look too easy (they give the note away: `key_blank`, `opposite` and `autocorrect` are the suspects) or too hard (`riddle`, `scrambled` on a long note, `emoji`), from the screenshots and the relay show. Write them under "## Findings" in `T88.md`.

## 11. The commit

One commit for T88, as "How to run a task" in the plan lists: `BPC_NoteClue.uasset`, `BP_Show.uasset`, `WBP_Stage.uasset`, the emoji font assets and `SourceAssets/Fonts/NotoColorEmoji.ttf` (answer 3), `clues.json`, `scenes.json`, `prompts.json`, `tells.json`, `stagehand.json` (only if T61 is done), `Tools/check_prompts.py`, `Docs/switches.example.json`, `Docs/ItchPage.md`, `Docs/Assets.md`, `Graphs/BPC_NoteClue/*.txt`, `Graphs/BP_Show/ActorState.txt`, `Graphs/BP_Show/PrepPrompt.txt`, `Graphs/WBP_Stage/SetClue.txt`, `Docs/tasks/T88.md`, `Docs/Plan.md` (the box and the "Next up" line), `Docs/DevLog.md`. Unlock the two Blueprints and the claim after the push.

## 12. For T84 (Scene Prep's middle panel), and other knock-ons

**What T84 gets from T88** (T84 depends on T88 for these two things):

1. **The clue rows in my card's note box.** After T88, `NoteBox` holds, in order: `NoteTitle` ("THE DIRECTOR'S NOTE"), `NoteText` ("Clue: <label>"), **`ClueText`** (the clue's text, wrapped, Regular 18; mono for vowels and consonants; the emoji font for emoji) and `NoteHidden` ("Note: ██████ (bots only)"). The longest `ClueText` is about five lines at the card's width (Pig Latin of `hold_prop`). My card stays outside `PrepBox` (T28), so when T84 moves `PrepBox`'s scene and stage parts into the middle panel, the note box stays on the card and keeps all four rows. T84 should leave `ClueText` and `SetClue` alone and re-take its 1440 × 900 screenshots with that longest clue forced (`"clue": "pig_latin"` on `hold_prop`), since the card's height in Scene Prep is what T84 frees up.
2. **`PrepPrompt`'s turn line.** After T88 it reads: "Read the card on the right: the scene, your role, the note's clue, the cast and the stage. Press Start the scene when you are ready." (`Graphs/BP_Show/PrepPrompt.txt`.) T84 rewrites this line for the middle panel; it should keep "the note's clue" (not "category") in whatever it writes.

**Tell, don't change:**

- **T61 (while open):** the stagehand's `scene_prep` line (part 2e) and How to play's bullet 2 (`WBP_HowToPlay` `Body2`, and `Docs/tasks/T61-build/how_to_play.md`). Old bullet 2: "Everyone gets the same scene card. The AIs also get a secret director's note. You only see its category, and they know it." New: "Everyone gets the same scene card. The AIs also get a secret director's note. You get only a clue: its category in scene 1, then a new kind each scene. They know which." `WBP_HowToPlay` is not in T88's Touches; if T61 is done, ask the dispatcher which task takes it.
- **T34:** `NoteFrame`'s restyle (C2) now has a fourth row, `ClueText`, to put in `PaperText` with the others; and the card body list (`RoleText`, `WantText`, …) gains `ClueText`. Its mono font is T65's `Mono()`.
- **`WBP_UIStyleSheet`'s sample note** ("Secret note: Never move to the Back.") was already out of date (T50); still a sample, not the game.
- **T61's earpiece over Scene Prep:** the card's note box grows by up to five lines in scenes 2 on; the earpiece sits at the bottom center, not over the card, so nothing to do unless T84 moves it.
