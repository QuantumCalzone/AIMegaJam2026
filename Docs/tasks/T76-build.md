# T76 build sheet: the bots send an emotion with every reply

Back to [T76](T76.md). A PC prep session wrote this on 2026-11-15, without the editor, against **`noHumansOnSet` at `485a979`**. T76 needs no editor and changes no asset.

**What lands before T76 and moves these places.** T57, T58, T62, T63, T64 to T66, T68 and T69 come first in the plan, and T75 is a dependency. Of those, these change T76's files: T58 (`asks.last_word`, a `last_word` free-mode phase, a free-mode phase guard in the checker), T62 (the actions block, `_readme` lines, free-mode actions: `[0, 1]` in a scene turn and none in a reaction, `look {prop}`), T63 (the `input` prompt, `asks.input`, `_readme`, `input.json`), T68 (`llm.json` `build` and two `_readme` sentences, a paragraph in `Relay/README.md`), T69 (a new `input_schema` for the input ask alone, the reply shape plus `attempt`; the `llm.json` `_readme` sentence about the schemas; `input`, `asks.input` and a `_readme` sentence in `prompts.json`; in the checker, an `input_schema` check, `attempt` in `check_reply`'s `types` for the input ask, and `shape_fails(reply, ask)`; no `free_mode.json` or `Relay/` change), and T75 (`emotes.json`, and `check_files` returns it). This sheet writes each edit **as T69 leaves the files**, from [T57-build.md](T57-build.md), [T58-build.md](T58-build.md), [T62-build.md](T62-build.md), [T63-build.md](T63-build.md), [T64-build.md](T64-build.md) to [T66-build.md](T66-build.md), [T68-build.md](T68-build.md), [T69-build.md](T69-build.md) and [T75-build.md](T75-build.md). T57 is already in `485a979`; T69's sheet landed while this one was written. **T60 comes after T76** in the plan (it adds `tell` to the reply); part 9 tells it what T76 leaves. Each place is named by its text first, then its line at `485a979`. Find each by its text before you change it.

**Sources read:** `T76.md` and its plan entry; `T75.md`, `T75-build.md` (the 12 ids, part 4's checker code, part 7), `T77.md`, `T78.md`, `T69.md`; the T55 and T60 build sheets (the model for this form) and the T57, T58, T62 to T66, T68 and T69 build sheets for the files they change (T69's parts 1, 2, 3c and 4); `Content/NHOS/Data/llm.json`, `prompts.json`, `free_mode.json`; `Relay/src/index.js` (`freePhase`, `weighted`, `freeReplyObject`, `freeResponse`), `Relay/test/curl-tests.sh`, `Relay/test/game_shape.py`, `Relay/README.md`, `Relay/relay.config.json`; `Tools/check_prompts.py`; `Graphs/BPC_LLMClient/ParseReply.txt`. **The design doc, read and not changed:** Rules rev 45, Bot Prompts rev 82, Tech & Build rev 28.

## In short

| T76 step | Where in this sheet |
|---|---|
| 1. The design doc first | Part 1: the Rules tab's new "Emotions" section and the Bot Prompts tab's new base line, as text for my person's OK; question 1 adds three small Tech & Build edits |
| 2. The reply shape | Part 2: `emotion` in `reply_schema` and in T69's `input_schema` (the 12 ids, required in both), and the `llm.json` `_readme`; part 3b: the `prompts.json` `_readme` |
| 3. The prompt | Part 3a: the one rule line at the end of `base`, word for word from part 1b |
| 4. Free mode in the relay | Part 4: a weighted `emotions` list in seven phases of `free_mode.json` (none in `input`), and its `_readme`; part 5a: `freeEmotion` in `Relay/src/index.js` |
| 5. The checker | Part 6: `emotion_problems` (enum = ids, base line, free-mode lists), the known-id check on every reply, the count of each provider's picks, the `types` in `check_reply` and `shape_fails` |
| 6. The relay's tests | Part 5b: three new curl tests; part 5c: the `Relay/README.md` lines |
| Done when | Part 7: `--offline`, then the deploy push, `--relay --free`, the curl tests and `game_shape.py` (all free), then the paid run (about 10 cents) and the Findings |

- **Needs the relay deploy:** `Content/NHOS/Data/free_mode.json` (the relay bundles it) and `Relay/src/index.js`. Every push to `noHumansOnSet` redeploys the relay (`Relay/README.md`, "Deploy"), so the push that carries them is the deploy, and it needs my person's OK, typed in the T76 session (an OK passed on by the dispatcher doesn't clear the permission check). `Relay/test/curl-tests.sh` and `Relay/README.md` change nothing the relay does.
- **Costs money:** only the paid check run (part 7e), about 70 calls on the four providers, about $0.10. Every other run here is free.
- **The game doesn't change.** It reads reply fields by name (`Json|GetField` in `BPC_LLMClient`), so the new field is ignored until T77, and its own Test for Free (`FreeReply`) ignores the new lists until T77 too.

## Questions for my person

One question. My recommendation is first.

1. **The Tech & Build tab.** T76 puts the emotion feature in the Rules and Bot Prompts tabs. The Tech & Build tab (rev 28) then disagrees in two places: "AI actors reply in that format: actions as tool calls, plus speech." (no emotion), and "Cut for the jam: voice acting, extra sets, animations beyond Move, Look, Grab, Throw and Give, ..." (T75's gestures are such animations). Its build list has no line for the emotions either.
   - **(Recommended) Make the three small edits in part 1c too,** with the same OK as the other doc edits. The doc is the only source of truth, and T70's itch page and the judges' read come from it.
   - **Or leave Tech & Build as it is,** and T76 edits only the two tabs its step 1 names.

## Decisions made for my person

My person asked prep sessions to take their own recommendation on calls that are theirs, and list them here. Each is open to change. The T76 session shows this list to my person when it closes the task.

1. **The rule line overrides `game`'s "Fill only the fields the ask names".** `game`'s How to reply says "Fill only the fields the ask names, and leave the others empty", and no ask names `emotion`. The new `base` line starts "Every reply, whatever the ask, fills "emotion"", and `base` comes after `game` in the system text, so the narrower rule wins. The schema forces a value from the enum anyway. `game` stays as it is, inside T76's Touches.
2. **`emotion` goes after `pass`** in `reply_schema`'s `properties` and `required`, and between `pass` and `attempt` in T69's `input_schema` (T69's check compares the two schemas without regard to order), and its enum lists the ids in `emotes.json` file order, `neutral` first. The checker allows any order (the task: "in any order"). If the paid run shows a provider always sending `neutral`, the enum's order is a second knob to try after the rule line.
3. **The free-mode lists are `{id, weight}` objects,** one line per phase, as `scene_actions` are `{verb, target, item, weight}`. Every phase but `input` has one; all 12 ids appear somewhere, so a free show in T77 shows every face. The leans are the task's examples, plus a list for the phases it doesn't name: `last_word` leans worried and angry (a bot defending itself), `reaction_cut` sad and angry (the cut bot's last words), `closing` smug and happy (the end screen's vote).
4. **A free pass shows a face:** the relay picks the emotion before it decides a pass, so a Free Talk pass carries one from `free_talk`'s list (the rule line: "A pass shows a face too").
5. **The design doc's base line is wrapped like the rest of the block** (78 columns, two spaces before each continued line), and `prompts.json` holds it as one line. The checker finds it in `base` word for word (`DOC_EMOTION_LINE`), as it finds the note lines in `game` (`DOC_NOTE_LINES`).
6. **The Rules tab gets its own H2, "Emotions",** after the win and lose paragraph and before "Onboarding", because the faces run through every part of a show. It names the emotions with "such as", so a new emotion in `emotes.json` doesn't make it wrong.
7. **The input ask gets no new instruction.** `input` and `asks.input` are T77's (it tells the input LLM to pick my emotion). Until then the input LLM fills `emotion` with whatever the schema allows, and the checker only checks it is a known id. The count prints the input LLM apart (`input (anthropic)`) and never notes it as stuck.
8. **The checker notes, never fails, a provider that sticks to one emotion:** `STUCK_SHARE = 0.6` of its replies, with 5 or more replies, in a paid run only (free picks are random). The Done-when asks Claude to judge it.
9. **The known-id check runs on every reply, `--free` too,** so "`--relay --free` passes with an emotion on every reply" is a checker result, not a reading of the output.
10. **Two one-word fixes in `llm.json`'s `_readme` while T76 holds it,** if T68 or T69 didn't make them: T62-build part 9's "uses at most 2 actions" (now 1, none in a reaction) and T58's last word in the list of asks.

## 0. Before you start (after T69 is pushed)

1. `git pull` (or, in a worktree, move onto `noHumansOnSet` as `CLAUDE.md` says), read `Agents/`, `git lfs locks`. T76 needs no editor and no lock, so it can run in a worktree (the plan's "Worktrees" build note); claim T76 with `Docs/claims/T76` as the plan says. `git log --oneline -15 -- Content/NHOS/Data/llm.json Content/NHOS/Data/prompts.json Content/NHOS/Data/free_mode.json Relay/ Tools/check_prompts.py` should show T55, T58, T62, T63, T67, T68, T69 and T75.
2. **What T69 built.** [T69-build.md](T69-build.md) gives the input ask its own `input_schema` (decision 1 there): `reply_schema`'s properties plus `attempt`, with the checker failing the two if they drift apart ("T76 adds emotion to both"). Read `T69.md`'s Findings ("the pick", step 1) and `git show <T69 commit> -- Content/NHOS/Data/llm.json Tools/check_prompts.py Relay/src/index.js` to confirm it was built that way:
   - **`input_schema`, as its sheet says** (the usual case): part 2a adds `emotion` to both schemas. T77 needs the input ask's `emotion`.
   - **`attempt` in `reply_schema` instead** (T69 changed its mind): `emotion` goes after `attempt` there, there is no second schema, and the checker's lists keep `attempt` (part 6).
   - **Another name than `input_schema`:** `emotion_problems` (part 6b) checks every `llm.json` key that ends in `_schema`; add T69's key to that loop by name if it doesn't.
3. **T75's ids.** `python -c "import json;print([e['id'] for e in json.load(open('Content/NHOS/Data/emotes.json',encoding='utf-8'))['emotes']])"` prints the ids in order. Expected: `['neutral', 'happy', 'sad', 'angry', 'worried', 'scared', 'surprised', 'confused', 'disgusted', 'suspicious', 'smug', 'embarrassed']`. If T75's rework changed them, use its list in part 2a's enum and part 4's lists (every id in part 4 must still exist; the checker says which doesn't). Check that `check_files` returns `"emotes": emotes` (T75-build part 4c).
4. `python Tools/check_prompts.py --offline` passes before you start.
5. **Ask my person, one question per call, with the multiple-choice tool** (CLAUDE.md, "Asking for input"):
   1. Question 1 above, if my person hasn't answered it in this sheet.
   2. **The doc edits:** show part 1's text (1a, 1b, and 1c with question 1's first answer). "Make these edits (Recommended)" or "Change the wording" (then take theirs, and use it word for word in part 3a and `DOC_EMOTION_LINE`).
   3. **The deploy push:** "Push free_mode.json and the relay with T76 (Recommended)": the push redeploys the relay, whose free replies gain an `emotion`; no paid call and no game behavior changes. Or "Not now" (part 8's two-commit path).
   4. **The paid run:** "Run every ask on the four providers, about 70 calls, about $0.10 (Recommended)" or "Not now" (then the task waits with a `Waiting:` line after its first commit).
6. Status file `Agents/status/task-T76.md` in the repo folder's `Agents/status/`, with `- Editor: not using`.

## 1. The design doc (step 1): show my person, edit after the OK

Edit the doc with the Claude Docs connector (`Docs/GameDesign.md` has the link) only after the OK in part 0. Read each tab again first: if its rev moved past the one named here, check the anchors still say what this part quotes.

### 1a. Rules tab (rev 45): a new section

Insert after the paragraph that starts "You win if you make the final two, or if you're still on stage when the last scene ends." (id `.2859`, the last paragraph of "The Cut") and before the "Onboarding" heading (id `.6133`):

> **Emotions** (heading 2, like "Free Talk" and "The Cut")
>
> - Every robot shows an emotion while its line plays: a face and a small gesture, such as happy, angry, worried, confused, suspicious or smug, or a calm neutral face.
> - Each AI picks its emotion with every reply, a pass included. It's the emotion it acts, not always what it feels: a bot may keep a calm face while it accuses someone, or fake confusion when it's under suspicion.
> - Everyone on stage sees every face. The AIs can't see the stage, so the shared log tells them what each face showed, and a face can be evidence.
> - Your robot shows emotions too, or one blank face would give you away. The game picks yours from your line, unless you pick it yourself before you send.
> - Emotions never show up in the words: no tags or stage directions in any line.

- Bullets 1 and 2 are T76's and T75's. Bullet 3 is T77's (the log's `feels`). Bullet 4 is T77's (the input LLM, or the keyword table) and T78's (the Face chip). Bullet 5 is the legibility rule. T76 step 1 asks for all of them at once.
- T77 checks that this section still matches what it builds; T78 checks bullet 4.

### 1b. Bot Prompts tab (rev 82): the base prompt's last line

In "Shared base prompt", the code block (id `.4986`), after its last line `- Keep every line short: about 10 words, never more than 15.`, add a new line:

```
- Every reply, whatever the ask, fills "emotion": the face your robot shows
  while its line plays. It is the face you act, not always what you feel: a
  bot that suspects someone may keep a neutral face, and a bot under suspicion
  may fake confusion. Use "neutral" when nothing moves you, but don't stick to
  one face. A pass shows a face too: you can say nothing and still look
  worried. Never put the emotion in your speech as a tag or a stage direction.
```

- It covers every point of T76 step 3: the emotion its robot shows while its line plays; acted, not always felt, with the task's two examples; `neutral` when nothing moves it, but not stuck on one; a pass shows its emotion; never in the speech (the base's second line already bans tags).
- The doc wraps it; `prompts.json` holds it as one line, with one space where each break is (part 3a). If my person changes the wording, change part 3a and `DOC_EMOTION_LINE` (part 6b) to match, word for word.

### 1c. Tech & Build tab (rev 28), only with question 1's first answer

1. **"Game state & logs"**, the bullet "AI actors reply in that format: actions as tool calls, plus speech." (id `.264`) becomes "AI actors reply in that format: actions as tool calls, plus speech and the emotion their robot shows."
2. **"Build list"**, a new item after "Cut reveal and reaction round" (id `.1820`): "Emotions: every robot shows a face and a gesture while its line plays, picked by each AI's reply, and from your line or by you".
3. **"Cut for the jam"** (paragraph id `.1947`): "animations beyond Move, Look, Grab, Throw and Give" becomes "animations beyond Move, Look, Grab, Throw, Give and the emotion gestures".

### 1d. Checked and left

- **Turn Input** tab: the Face chip is T78's (part 9 tells T78; its Touches don't name the doc).
- **Art Inspiration:** T75 found it needs no edit for the faces (T75-build, top).
- **Overview, Stories:** describe no reply field.

## 2. `llm.json` (step 2)

### 2a. `reply_schema`

At `485a979`, lines 40 to 44 (T68 adds `"build"` after `"relay"`, one line lower):

```json
			"pass": {
				"type": "boolean"
			}
		},
		"required": ["actions", "speech", "vote", "reason", "pass"],
```

becomes

```json
			"pass": {
				"type": "boolean"
			},
			"emotion": {
				"type": "string",
				"enum": ["neutral", "happy", "sad", "angry", "worried", "scared", "surprised", "confused", "disgusted", "suspicious", "smug", "embarrassed"]
			}
		},
		"required": ["actions", "speech", "vote", "reason", "pass", "emotion"],
```

**T69's `input_schema`**, right after `reply_schema` (T69-build part 2a), ends with the same `pass` property, then `attempt`:

```json
			"pass": {
				"type": "boolean"
			},
			"attempt": {
				"type": "string"
			}
		},
		"required": ["actions", "speech", "vote", "reason", "pass", "attempt"],
```

becomes

```json
			"pass": {
				"type": "boolean"
			},
			"emotion": {
				"type": "string",
				"enum": ["neutral", "happy", "sad", "angry", "worried", "scared", "surprised", "confused", "disgusted", "suspicious", "smug", "embarrassed"]
			},
			"attempt": {
				"type": "string"
			}
		},
		"required": ["actions", "speech", "vote", "reason", "pass", "emotion", "attempt"],
```

- **Both or neither:** T69's check (`input_schema must be reply_schema's properties plus attempt`, part 6c) fails if `emotion` is in only one of them, and the two `emotion` blocks must be identical, the enum's order included (it compares the property objects). Only the match with `emotes.json` is free of order.
- **If T69 put `attempt` in `reply_schema` instead** (part 0 step 2), put `emotion` after `attempt` there, and add `"emotion"` at the end of `required`.
- **Strict schemas:** all four providers already take an `enum` here (`verb`'s, since T16) and need every property in `required` with `additionalProperties: false`, which this keeps (`Relay/README.md`, "All three Chat Completions providers take structured output ...").
- **Size:** the enum adds about 200 bytes to every request. The largest request at `485a979` is 18.6 KB (a closing ask), far under the relay's `max_body_bytes` of 65536.

### 2b. `_readme` (line 2, one string)

T69 rewrites this sentence (T69-build part 2b). Find its version, `reply_schema is the reply shape for every actor ask (scene turn, Free Talk line, vote, reaction, closing line); input_schema is the same shape plus attempt, for the input ask alone (T69: a few words naming an action the player typed that the game can't do, for analytics); unused fields come back empty.`, and make it:

`reply_schema is the reply shape for every actor ask (scene turn, Free Talk line, last word, vote, reaction, closing line); input_schema is the same shape plus attempt, for the input ask alone (T69: a few words naming an action the player typed that the game can't do, for analytics); unused fields come back empty, except 'emotion' (T76), which every reply in both shapes fills with one id from emotes.json: the face the robot shows while its line plays. Both enums list every id in emotes.json, so a new emotion goes in all three places.`

- "last word" is T58's ask (decision 10). If T69's sentence came out different, keep its words, add "last word" to the list of actor asks if it's missing, and add the `except 'emotion' ...` part after `unused fields come back empty`.
- If T69 put `attempt` in `reply_schema` instead (no `input_schema`), write "every reply fills" and "The enum lists every id in emotes.json, so a new emotion goes in both files."
- **Decision 10's other fix:** if the same string still says `uses at most 2 actions`, make it `uses at most 1 action (none in a reaction)` (T62-build part 9).
- T68's two changes to this string ("no LLM call", and the sentence about `build` at its end) sit elsewhere in it; keep them.

## 3. `prompts.json` (steps 2 and 3)

Each line as it sits in the file (two tabs before it, quotes escaped as the file writes them).

### 3a. `base`: the rule line (step 3)

At `485a979` `base` is lines 76 to 85, and its last line is line 84: `		"- Keep every line short: about 10 words, never more than 15."`. Nothing before T76 changes `base` (T62 and T63 change `game`, `input` and `asks`), so it is still the last line; only its line number moves. Give it a comma, and add the new line after it:

```
		"- Keep every line short: about 10 words, never more than 15.",
		"- Every reply, whatever the ask, fills \"emotion\": the face your robot shows while its line plays. It is the face you act, not always what you feel: a bot that suspects someone may keep a neutral face, and a bot under suspicion may fake confusion. Use \"neutral\" when nothing moves you, but don't stick to one face. A pass shows a face too: you can say nothing and still look worried. Never put the emotion in your speech as a tag or a stage direction."
```

It is part 1b's line, unwrapped. The `]` and the `,` after it stay as they are.

### 3b. `_readme`: the reply's fields (step 2)

At `485a979` the last `_readme` line (line 9): `"Every reply matches llm.json 'reply_schema': actions [{verb, target, item}], speech, pass, vote, reason. Unused fields come back empty. Tools/check_prompts.py sends every ask with the same request body as the game."`

- After `speech, pass, vote, reason` (and after T69's field, if it listed one there) add `, emotion`.
- After `Unused fields come back empty.` add: ` Every reply fills emotion, though: one id from emotes.json, the face its robot shows while its line plays (T76; the rule is the last line of 'base'). The game reads it from T77 on.`

Nothing else in `prompts.json` changes. `game`, `input`, `asks` and `does_templates` stay (decisions 1 and 7).

## 4. `free_mode.json` (step 4; pushed only with the deploy OK)

As T62 leaves it (T55 dropped `tiebreak`, T58 added `last_word` before `free_talk`, T62 changed the actions). T63 and T69 leave it alone (T63-build: "No `free_mode.json` or `Relay/` change"; T69: "Free mode leaves it empty", which may add nothing here). Until the deploy OK, don't edit the file at all, not even uncommitted (T55-build part 5).

### 4a. The lists

Add one line to each phase but `input`, **right after its `"ask_contains": [...]` line** (every one of these phases has one):

| Phase | Line to add |
|---|---|
| `closing` | `			"emotions": [{ "id": "smug", "weight": 3 }, { "id": "happy", "weight": 2 }, { "id": "suspicious", "weight": 2 }, { "id": "neutral", "weight": 1 }, { "id": "surprised", "weight": 1 }],` |
| `vote` | `			"emotions": [{ "id": "suspicious", "weight": 4 }, { "id": "smug", "weight": 3 }, { "id": "neutral", "weight": 2 }, { "id": "confused", "weight": 1 }],` |
| `reaction_cut` | `			"emotions": [{ "id": "sad", "weight": 3 }, { "id": "angry", "weight": 3 }, { "id": "embarrassed", "weight": 2 }, { "id": "surprised", "weight": 1 }, { "id": "disgusted", "weight": 1 }],` |
| `reaction` | `			"emotions": [{ "id": "surprised", "weight": 4 }, { "id": "sad", "weight": 3 }, { "id": "smug", "weight": 3 }, { "id": "worried", "weight": 1 }, { "id": "confused", "weight": 1 }, { "id": "happy", "weight": 1 }, { "id": "neutral", "weight": 1 }],` |
| `last_word` | `			"emotions": [{ "id": "worried", "weight": 3 }, { "id": "angry", "weight": 3 }, { "id": "suspicious", "weight": 2 }, { "id": "embarrassed", "weight": 2 }, { "id": "scared", "weight": 1 }, { "id": "neutral", "weight": 1 }],` |
| `free_talk` | `			"emotions": [{ "id": "suspicious", "weight": 4 }, { "id": "worried", "weight": 3 }, { "id": "neutral", "weight": 2 }, { "id": "angry", "weight": 2 }, { "id": "smug", "weight": 1 }, { "id": "confused", "weight": 1 }, { "id": "embarrassed", "weight": 1 }],` |
| `scene_turn` | `			"emotions": [{ "id": "neutral", "weight": 4 }, { "id": "happy", "weight": 3 }, { "id": "confused", "weight": 3 }, { "id": "surprised", "weight": 2 }, { "id": "smug", "weight": 1 }, { "id": "worried", "weight": 1 }, { "id": "angry", "weight": 1 }, { "id": "scared", "weight": 1 }, { "id": "disgusted", "weight": 1 }, { "id": "embarrassed", "weight": 1 }],` |

- Three tabs before each line, as the phase's other keys. Each line ends with a comma, because a key always follows.
- The leans: scene lines neutral, happy and confused; Free Talk suspicious and worried; votes suspicious and smug; reactions surprised, sad and smug (the task's examples); the rest are decision 3's. All 12 ids appear.
- **The `input` phase gets none** (T77 adds my keyword table), so free input replies show `neutral`.
- If T58 or T62 came out with other phase ids, every phase that has `ask_contains` gets a list; the checker fails one that doesn't (part 6b).

### 4b. `_readme`

After T62's `scene_actions` line (it starts `"scene_actions: the actions a free actor may take, with weights.`), add a line:

```
		"emotions (T76): the emotion a free reply shows, picked at random by weight from its phase's list, in the same form as scene_actions ({id, weight}); each id is one in emotes.json. A phase with no list (the input step) shows neutral. The relay fills every free reply's emotion from these lists; the game's own FreeReply reads them from T77 on.",
```

Line 9 (the legibility line) stays last. Line 4 ("... (BPC_LLMClient.FreeReply, no network). The relay also uses it ...; a change here needs a push to reach the relay.") stays true.

## 5. The relay (steps 4 and 6)

### 5a. `Relay/src/index.js`: `freeReplyObject` (the task's `freeReply`)

Two edits.

**1. A new function**, right after `weighted` (lines 201 to 209 at `485a979`, the function that ends `return list[list.length - 1];` and `}`), with one blank line before it:

```js
// The emotion a free reply shows (T76): a weighted pick from the phase's "emotions"
// in free_mode.json, or "neutral" when the phase has none (the input step).
function freeEmotion(ph) {
	const list = Array.isArray(ph.emotions) ? ph.emotions.filter((x) => isObject(x) && typeof x.id === "string") : [];
	return list.length ? weighted(list).id : "neutral";
}
```

`isObject` and `weighted` are the file's own (`weighted` reads `x.weight ?? 1`).

**2. The reply literal** in `freeReplyObject` (line 228 at `485a979`):

- Now: `	const reply = { actions: [], speech: "", vote: "", reason: "", pass: false };`
- New: `	const reply = { actions: [], speech: "", vote: "", reason: "", pass: false, emotion: freeEmotion(ph) };`

T69 leaves this literal alone (T69-build part 3c: the free reply has no `attempt`, which the game and T69's `shape_fails` read as `""`), and T76 doesn't add `attempt` either. If T69 did add a field here, keep it and put `emotion: freeEmotion(ph)` last. The line is right after `const ph = freePhase(state);`, so `ph` is set, and every return path after it (the input echo, the vote, the pass, the scene line) sends the same `reply`, so every free reply carries an emotion. Nothing else in `Relay/src/index.js` changes. `freeResponse` stringifies the object as it is.

There is no Node.js on this PC, so the change can't run locally. The curl tests (part 7c) check it on the deployed relay.

### 5b. `Relay/test/curl-tests.sh`

**1. A helper,** right after the `absent()` function (lines 93 to 99 at `485a979`, it ends with `}`), with one blank line before it:

```bash
emotion_of() { # a relay reply on stdin -> "known <id>" (an id in emotes.json, T76) or "unknown <what>"
	"$PY" -c "import json,sys;r=json.load(sys.stdin);t=r['content'][0]['text'] if 'content' in r else r['choices'][0]['message']['content'];e=json.loads(t).get('emotion');ids=[x['id'] for x in json.load(open('../Content/NHOS/Data/emotes.json',encoding='utf-8'))['emotes']];print('known '+e if e in ids else 'unknown '+repr(e))"
}
```

It runs after the script's `cd "$(dirname "$0")/.."` (line 86), so the working folder is `Relay/` and `../Content/...` is the repo's data. It reads a Messages reply or a Chat Completions reply, whichever `$FIRST`'s provider sends.

**2. Three tests,** in the free branch, right after `expect "free vote picks a name from options" "$free_reply" 'vote\\":\\"Robot [AB]'` (line 236) and before its `echo`:

```bash
	# T76: every free reply carries an emotion, an id in emotes.json; the input step has no list, so it shows neutral.
	expect "free reply carries an emotion" "$free_reply" 'emotion\\":\\"[a-z]'
	expect "free vote's emotion is an id in emotes.json" "$(printf '%s' "$free_reply" | emotion_of)" '^known '
	INPUT_REQ=$("$PY" -c "import json,sys;c=json.load(open('relay.config.json'))['providers'][sys.argv[1]];b={'model':c['models'][0],c['max_tokens_field']:16,'messages':[{'role':'user','content':json.dumps({'actor':'Robot A','phase':'scene','typed':'hello there'})}]};print(json.dumps({'provider':sys.argv[1],'session':sys.argv[2],'body':b,'free':True}))" "$FIRST" "${RUN}-input")
	expect "free input reply's emotion is neutral" "$(post "$INPUT_REQ" | emotion_of)" '^known neutral$'
```

- `INPUT_REQ` is built the way `VOTE_REQ` is (line 234), with a state that has `typed`, so the relay answers from the `input` phase (`when_field`). Its own session (`${RUN}-input`) keeps it clear of the session limit the test before it trips.
- **T77 changes the third test:** with my keyword table, "hello there" still has no keyword, so `neutral` stays right; if T77's table gives it one, T77 changes the test.
- The header comment needs no change.

### 5c. `Relay/README.md`

**1. The free mode paragraph** (line 36 at `485a979`, starts `**Free mode** costs nothing, for local testing.`). Its sentence `The reply text is a valid game reply: ... pass false.` is out of date (it says `actions` empty and `reason` "Free mode reply."). Replace that whole sentence with:

`The reply text is a valid game reply, made from free_mode.json: speech a canned line for the ask's phase (or, for the input step, the player's typed text cut to 15 words), at most one stage action in a scene turn, vote a random name from the ask's options with a canned reason, now and then a pass in Free Talk, and emotion (T76) a weighted pick from the phase's emotions list, or neutral for a phase with none (the input step).`

Wrap each field name in backticks as the paragraph does (`speech`, `typed`, `vote`, `options`, `reason`, `pass`, `emotion`, `emotions`, `neutral`, `free_mode.json`). The rest of the paragraph stays, and so does T68's new paragraph after it.

**2. The curl tests' list** (line 216, starts `The curl tests check /health, ...`): `... the free session limit (151 calls, a few seconds) and that a free vote picks a name from options.` becomes `... the free session limit (151 calls, a few seconds), that a free vote picks a name from options, and that free replies carry an emotion from emotes.json (neutral for the input step, T76).` (backticks as the line has them).

**3. `test/game_shape.py` needs no change:** it reads `required` from `llm.json`'s `reply_schema` (its line 24 and line 106), so it checks `emotion` on its own once part 2a is in. The README's sentences about it stay true.

## 6. `Tools/check_prompts.py` (step 5)

Line numbers are at `485a979`; T57, T58, T62, T63, T66, T68, T69 and T75 all move them (T75 alone adds about 130 lines before `check_files`). Find each place by its text.

### 6a. The docstring

Before `Exit code 0 means the files are valid and every reply passed its checks.` (line 117), after T75's "Emotions (T75)" paragraph:

```
Emotions in replies (T76): every reply carries 'emotion', the face its robot
shows while its line plays. The file check fails a reply_schema (or any other
*_schema in llm.json) whose emotion enum isn't exactly the emotes.json ids, in
any order; a 'base' without the design doc's rule line (DOC_EMOTION_LINE); and
a free_mode.json phase whose 'emotions' ({id, weight}) name an unknown id, or a
phase other than the input step with none. Every reply's emotion must be a
known id, --free runs too, since a provider may not enforce enum. The summary
counts each provider's picks and, in a paid run, notes a provider that sticks
to one emotion (STUCK_SHARE of 5 or more replies).
```

### 6b. `emotion_problems` and its constants (new)

Right after T75's `emote_problems` function (it ends `    return errs` after the "is used by no emotion" check), before `def check_files(errors: list[str]):`, with two blank lines before and after:

```python
# T76: every reply carries "emotion", the face its robot shows while its line plays. This is the
# design doc's rule line (Bot Prompts, the shared base prompt's last line), word for word.
DOC_EMOTION_LINE = ("- Every reply, whatever the ask, fills \"emotion\": the face your robot shows while its line "
                    "plays. It is the face you act, not always what you feel: a bot that suspects someone may "
                    "keep a neutral face, and a bot under suspicion may fake confusion. Use \"neutral\" when nothing "
                    "moves you, but don't stick to one face. A pass shows a face too: you can say nothing and still "
                    "look worried. Never put the emotion in your speech as a tag or a stage direction.")
STUCK_SHARE = 0.6  # T76: a provider whose top emotion is this share of its replies (5 or more) gets a NOTE


def emotion_problems(llm, prompts, emotes, free) -> list[str]:
    """T76: the reply's emotion enum is exactly the emotes.json ids, 'base' has the doc's rule line,
    and every free_mode.json phase but the input step picks known ids by weight."""
    elist = emotes.get("emotes") if isinstance(emotes, dict) else None
    ids = [e.get("id") for e in elist if isinstance(e, dict)] if isinstance(elist, list) else []
    if not ids:
        return []  # emote_problems has already failed emotes.json
    errs = []
    for name, schema in llm.items():
        if not name.endswith("_schema") or not isinstance(schema, dict):
            continue
        emo = schema.get("properties", {}).get("emotion")
        enum = emo.get("enum") if isinstance(emo, dict) else None
        if not isinstance(emo, dict) or emo.get("type") != "string" or not isinstance(enum, list):
            errs.append(f"llm.json: {name} needs 'emotion', a string whose enum is the emotes.json ids (T76)")
            continue
        missing, extra = [i for i in ids if i not in enum], [i for i in enum if i not in ids]
        if missing or extra or len(enum) != len(set(enum)):
            errs.append(f"llm.json: {name}.emotion's enum must hold exactly the emotes.json ids, each once (T76)"
                        + (f"; missing {missing}" if missing else "") + (f"; not in emotes.json {extra}" if extra else ""))
        if "emotion" not in schema.get("required", []):
            errs.append(f"llm.json: {name} must require emotion (strict schemas need every field required)")
    if DOC_EMOTION_LINE not in prompts.get("base", []):
        errs.append("prompts.json: 'base' lost the design doc's emotion line (DOC_EMOTION_LINE, T76)")
    for ph in free.get("phases", []):
        pid, em = ph.get("id"), ph.get("emotions")
        if em is None:
            if not ph.get("echo_typed"):
                errs.append(f"free_mode.json: phase {pid} needs 'emotions', the faces its free replies show (T76)")
            continue
        if not isinstance(em, list) or not em:
            errs.append(f"free_mode.json: phase {pid}: emotions must be a list of {{id, weight}}")
            continue
        seen = []
        for x in em:
            if not isinstance(x, dict) or set(x) != {"id", "weight"}:
                errs.append(f"free_mode.json: phase {pid}: each emotion is {{id, weight}} and nothing else, not {x!r}")
                continue
            if x["id"] not in ids:
                errs.append(f"free_mode.json: phase {pid}: emotion {x['id']!r} is not an id in emotes.json")
            elif x["id"] in seen:
                errs.append(f"free_mode.json: phase {pid}: emotion {x['id']!r} is listed twice")
            seen.append(x["id"])
            if not _num(x["weight"]) or x["weight"] <= 0:
                errs.append(f"free_mode.json: phase {pid}: emotion {x['id']!r} needs a weight above 0")
    return errs
```

- `_num` is T75's (T75-build part 4b). `DOC_EMOTION_LINE` must match part 3a's line exactly; if my person changed the wording, change both.
- The `*_schema` loop covers T69's own input schema, if it made one with a name that ends in `_schema`.
- The free-mode part reads the lists only; T58's phase guard (`free_mode.json: asks.<k> would get a '<hit>' reply`) still decides which phase answers which ask.

### 6c. `check_files`

**1. The required list** (line 614): add `"emotion"`.

- Now: `    if sorted(schema.get("required", [])) != sorted(["actions", "speech", "pass", "vote", "reason"]):` and `        errors.append("llm.json: reply_schema must require actions, speech, pass, vote and reason")`
- New: `    if sorted(schema.get("required", [])) != sorted(["actions", "speech", "pass", "vote", "reason", "emotion"]):` and `        errors.append("llm.json: reply_schema must require actions, speech, pass, vote, reason and emotion")`
- T69's `input_schema` check sits right after it (T69-build part 4c: `# T69: the input ask's own schema is reply_schema plus "attempt" ...`). It needs no change: with `emotion` in both schemas (part 2a) it passes, and with `emotion` in only one it fails `llm.json: input_schema must be reply_schema's properties plus attempt (a string)` and `... must require reply_schema's fields plus attempt`.
- If T69 put `attempt` in `reply_schema` instead, keep it in this list and in the message.

**2. The call,** right after T75's `    errors.extend(emote_problems(emotes))` (T75-build part 4c, after `errors.extend(prewritten_problems(scenes, errors))`):

```python

    # The reply's emotion: the enum, the base line and free mode's lists (T76).
    errors.extend(emotion_problems(llm, prompts, emotes, load_json("free_mode.json", errors) or {}))
```

It loads `free_mode.json` itself (as `prewritten_problems` does), so it doesn't depend on the name T58 gave its own copy. The return stays T75's (`... "emotes": emotes}`).

### 6d. The reply's types: `check_reply` and `shape_fails`

- **`check_reply`** (line 1268): `    types = {"actions": list, "speech": str, "pass": bool, "vote": str, "reason": str}` becomes `    types = {"actions": list, "speech": str, "pass": bool, "vote": str, "reason": str, "emotion": str}`. Without it, every reply fails with `unexpected fields ['emotion']` (the `extra` check right after). The unpack line after it (`actions, speech, passed, vote, reason = ...`) stays.
- **`shape_fails`** (line 1607): the same `types` line gets `"emotion": str` too, so a `--free` reply without one fails.
- **As T69 leaves them** (T69-build parts 4f and 4g): `check_reply` adds `types["attempt"] = str` under `if ask == "input":` right after the dict, and `shape_fails` becomes `shape_fails(reply, ask=None)` with its own dict and an `attempt` check for input replies. Change only the two dict lines; T69's lines around them stay. The relay's free input replies have `emotion` and no `attempt`, which T69's `shape_fails` allows.

### 6e. `main`: the known-id check and the count

**1. The import** (line 123): add `import collections` after `import argparse`.

**2. Before the loop,** after `    mentions = {}  # provider -> [AI lines with speech or a reason, lines with an "@Player N" mention]` (line 1683):

```python
    picks = {}  # T76: provider (the input LLM apart) -> collections.Counter of the emotions its replies picked
    emotion_ids = [e.get("id") for e in data["emotes"].get("emotes", [])]
```

**3. In the loop,** right after the `if reply is None: ... elif args.free: ... else: fails, warns = check_reply(reply, ask, ctx)` block (lines 1694 to 1699) and before `        n_fail += bool(fails)`:

```python
        # T76: every reply's emotion is an id in emotes.json. The schema's enum should force it, but a
        # provider may not enforce enum, so check it, --free replies too. Then count the pick.
        if reply is not None and isinstance(reply.get("emotion"), str):
            emo = reply["emotion"]
            if emo not in emotion_ids:
                fails.append(f"emotion {emo!r} is not an id in emotes.json")
            picks.setdefault(f"input ({pv})" if ask == "input" else pv, collections.Counter())[emo] += 1
```

A missing or non-string `emotion` is already a fail from 6d's `types`, so this skips it.

**4. The summary,** right after the `@ mentions` print (`    if mentions:` and its `print`, lines 1721 to 1722), before `    if n:`:

```python
    if picks:
        print("\nEmotions picked (T76), most picked first:")
        for who, c in sorted(picks.items()):
            n_who = sum(c.values())
            top, top_n = c.most_common(1)[0]
            print(f"  {who:<18} {n_who:>3} replies: " + ", ".join(f"{e} {k}" for e, k in c.most_common()))
            if not args.free and not who.startswith("input") and n_who >= 5 and top_n >= STUCK_SHARE * n_who:
                print(f"    NOTE: {who} sticks to {top} ({top_n} of {n_who} replies); see T76's Done-when")
```

- The input LLM is counted apart (`input (anthropic)`) and never noted (decision 7): until T77 it has no instruction for `emotion`.
- The NOTE never fails the run (decision 8).

### 6f. Tried on a scratch copy

This session tried parts 2 to 4 and 6 on a scratch copy of `485a979` (`Tools/`, `Relay/`, `Content/NHOS`; T57 is in it). Put in first, because none of them had pushed: T75-build's `emotes.json` (part 1) and checker code (parts 4b and 4c), T58-build's `last_word` phase (part 3a), and T69-build's `input_schema` (part 2a), its `_readme` sentence (part 2b, as part 2b here quotes it) and its `input_schema` check (part 4c). A script took each block from this sheet and stopped if an anchor wasn't found exactly once. T62's and T63's edits weren't in the copy, so their anchors weren't exercised.

- `python -I Tools/check_prompts.py --offline` exits 0. Part 1b's text unwrapped, part 3a's line and `DOC_EMOTION_LINE` are the same string, and 1b's widest line is 78 characters.
- **Each break fails with exactly these lines** (exit 1), and the copy passes again after each. A break to `reply_schema`'s `emotion` alone also prints T69's `llm.json: input_schema must be reply_schema's properties plus attempt (a string)`, because the two schemas no longer match; that line is left out of the table.

  | Break | FAIL line (besides T69's) |
  |---|---|
  | `smug` left out of the enum | `llm.json: reply_schema.emotion's enum must hold exactly the emotes.json ids, each once (T76); missing ['smug']` |
  | `bored` added to the enum | `... each once (T76); not in emotes.json ['bored']` |
  | `happy` twice in the enum | `... each once (T76)` |
  | `reply_schema`'s enum reversed, `input_schema`'s not | only T69's line: the two blocks must be identical |
  | `sad` left out of `input_schema`'s enum | `llm.json: input_schema.emotion's enum must hold exactly the emotes.json ids, each once (T76); missing ['sad']` |
  | `emotion` out of `input_schema` | `llm.json: input_schema needs 'emotion', a string whose enum is the emotes.json ids (T76)`, and T69's `... must require reply_schema's fields plus attempt` |
  | `emotion` out of `reply_schema`'s `required` | `llm.json: reply_schema must require actions, speech, pass, vote, reason and emotion`, `llm.json: reply_schema must require emotion (strict schemas need every field required)`, and T69's `... must require reply_schema's fields plus attempt` |
  | no `emotion` property in `reply_schema` | `llm.json: reply_schema needs 'emotion', a string whose enum is the emotes.json ids (T76)` |
  | one word of `base`'s line changed | `prompts.json: 'base' lost the design doc's emotion line (DOC_EMOTION_LINE, T76)` |
  | `scene_turn` without `emotions` | `free_mode.json: phase scene_turn needs 'emotions', the faces its free replies show (T76)` |
  | `bored` in `vote`'s list | `free_mode.json: phase vote: emotion 'bored' is not an id in emotes.json` |
  | `sad` twice in `reaction`'s list | `free_mode.json: phase reaction: emotion 'sad' is listed twice` |
  | a weight of 0 in `closing` | `free_mode.json: phase closing: emotion 'smug' needs a weight above 0` |
  | an extra key in a `free_talk` entry | `free_mode.json: phase free_talk: each emotion is {id, weight} and nothing else, not {...}` |
  | `last_word`'s list empty | `free_mode.json: phase last_word: emotions must be a list of {id, weight}` |

  Both enums reversed together pass, and so does a list on the `input` phase (allowed, not required).
- **`main`, with the send patched out (no network), 63 asks:** in `--relay --free`, a reply with `"emotion": "bored"` fails `emotion 'bored' is not an id in emotes.json`, one with no `emotion` fails `emotion is missing or not a str`, and the rest pass; the table prints one line per provider plus `input (anthropic)`, with no NOTE. In a paid-mode run where Meta always sent `neutral`, the table adds `    NOTE: meta sticks to neutral (13 of 13 replies); see T76's Done-when`. No reply failed with `unexpected fields`.
- **Part 5b's `emotion_of`** printed `known smug` for a Messages reply, `known neutral` for a Chat Completions reply and `unknown None` for a reply with no `emotion`; the two new `expect` patterns match the first two. The relay's JavaScript (part 5a) couldn't run here (no Node.js); part 7c tests it on the deployed relay.

## 7. The check (Done when)

### 7a. `--offline` (free)

```bash
python Tools/check_prompts.py --offline
```

Look for `Files OK: llm.json, prompts.json, personas.json, scenes.json, errors.json, free_mode.json, autoplay.json, props.json, emotes.json and the relay's allow-list` (with T63's `input.json` in it), then `No provider name in what the actors read.` and the note line, exit code 0 (`echo $?` prints `0`). With 6b's free-mode loop in and part 4 not yet made, it fails with one line per phase, `free_mode.json: phase <id> needs 'emotions' ...`. That is why part 8's first commit without the deploy OK leaves the loop out.

### 7b. The deploy push, then `--relay --free` (free: no tokens)

After the OK, commit and push (part 8). Wait about 90 s for the Workers build (T59), then:

```bash
python Tools/check_prompts.py --relay --free
```

Look for: every job `[ok]`, each printed reply ending `"emotion": "<id>"}`; the line `<n> asks: <n> passed, 0 failed, 0 with warnings.`; and the new table, one line per provider plus `input (anthropic)`, for example `  anthropic           17 replies: suspicious 5, neutral 3, ...` and `  input (anthropic)   <n> replies: neutral <n>` (the input step has no list). No NOTE lines in a free run. **If every reply fails with `emotion is missing or not a str`,** the build hasn't finished, or failed: check the Worker's **Deployments** in the dashboard, wait, and run it again.

### 7c. The relay's tests (free)

From the repo root, with the relay address from `llm.json` (never paste it into chat or a doc outside the repo):

```bash
bash Relay/test/curl-tests.sh "$(python -c "import json;print(json.load(open('Content/NHOS/Data/llm.json'))['relay'])")"
```

Look for `PASS  free reply carries an emotion`, `PASS  free vote's emotion is an id in emotes.json` and `PASS  free input reply's emotion is neutral`, and a last line `<n> passed, 0 failed, <m> skipped` with three more passes than before T76 (the skips are T67's read-back and event-limit tests, which need `--stats-config` and `--events-limit`).

```bash
python Relay/test/game_shape.py "$(python -c "import json;print(json.load(open('Content/NHOS/Data/llm.json'))['relay'])")"
```

Free by default (no `--real`). Every provider passes: it checks the free reply has every field in `required`, `emotion` now among them.

### 7d. The doc

Read the Rules, Bot Prompts (and with question 1's first answer, Tech & Build) tabs back after the edits, and check `base`'s last line in `prompts.json` against the doc's, word for word: `--offline` already compares it with `DOC_EMOTION_LINE`, so check that constant against the doc's block once.

### 7e. The paid run (about $0.10, after my person's OK)

```bash
python Tools/check_prompts.py
```

- In the repo folder, after the merge (a worktree has no `Local/llm_key.json`). Or, from the worktree, `python Tools/check_prompts.py --relay`: the same asks on our relay's keys, the same models and about the same cost.
- About 70 calls (every ask once per persona, the card sweep and the input cases). T16 measured about $0.11 for a 90-call show; the summary's last line prints the real cost.
- Look for `<n> asks: <n> passed, 0 failed` (warnings are fine; a FAIL `emotion '<x>' is not an id in emotes.json` means a provider ignored the enum: say which under "## Findings"), the by-provider cost lines, and the emotions table with one line per provider and one for the input LLM.
- **Under "## Findings" in `T76.md`:** copy the table; say for each of the four providers whether it sticks to one emotion or always sends `neutral` (a `NOTE:` line, or your own reading of a narrow spread), and whether the picks fit their lines (read a few replies: a suspicious vote, a worried defense, a pass with a face). Say what the input LLM sent with no instruction (expected: mostly `neutral`; T77 tells it what to pick).
- **If a provider sticks:** propose a reworded rule line to my person (a doc edit, so their OK first), change the doc, part 3a and `DOC_EMOTION_LINE` together, and run that provider's asks again with my person's OK for the extra cost (`python Tools/check_prompts.py --persona <id>`, about a quarter of the run). A second knob is the enum's order (decision 2).

## 8. The commits

**With the deploy OK (the usual path): one commit and one push** after 7a passes: `T76: The bots send an emotion with every reply`, holding `Content/NHOS/Data/llm.json`, `Content/NHOS/Data/prompts.json`, `Content/NHOS/Data/free_mode.json`, `Relay/src/index.js`, `Relay/test/curl-tests.sh`, `Relay/README.md`, `Tools/check_prompts.py`, `Docs/tasks/T76.md` (Result so far, Findings: the doc edits made and their revs, question 1's answer, the decisions above as built), `Docs/Plan.md` (a `Waiting:` line under T76 if the paid run hasn't run yet), `Docs/DevLog.md`. Stage each by path. Then 7b and 7c, then the paid run (7e), then a second commit with the Findings, the box checked and the entry moved to Done (`T76: findings from the paid run`). If the paid run came before the first push, one commit holds it all.

**Without the deploy OK: two commits,** as T55-build part 10 does. The first holds everything but `free_mode.json` and the three `Relay/` files, with 6b's free-mode loop (from `    for ph in free.get("phases", []):` to the end of the function, before `return errs`) left out, so `--offline` passes; `--relay --free` fails until the second commit (every free reply lacks `emotion`). It has a `Waiting:` line under T76 in `Docs/Plan.md`: `Waiting: the relay deploy (free_mode.json and Relay/). Left: my OK, typed in the T76 session.` The second, after the OK, adds those four files and the loop, and the push is the deploy; then 7b and 7c.

Release `Docs/claims/T76` and delete the status file after the last push. Worktree: merge `noHumansOnSet` into the branch first, then into the repo folder (the plan's "Worktrees" note).

## 9. Knock-on: tell, don't change

- **T77:** every reply has `emotion`, an id from `emotes.json` (part 2a); `HandleReply` can read it with `Json|GetField`, like `speech`. Free mode's lists are `emotions: [{id, weight}]` on each phase but `input` (part 4a), and the relay picks with `freeEmotion(ph)` (part 5a); `BPC_LLMClient.FreeReply` should pick the same way (`FreeAction` already does a weighted pick from `scene_actions`). Its keyword table for my line is new: the relay's input path is `if (ph.echo_typed) { ... return reply; }` in `freeReplyObject`, where the table's pick replaces `reply.emotion`. The checker counts the input LLM apart (`input (<provider>)`); T77's input checks can reuse `emotion_ids` from `main`. The curl test "free input reply's emotion is neutral" sends "hello there". `emotion_problems` doesn't require a list on the `input` phase and doesn't forbid one. The Rules tab's "Emotions" section (part 1a) already says the log tells the AIs each face and that my emotion comes from my line.
- **T78:** reads the ids from `emotes.json` (T75), not from `llm.json`. The Rules tab's bullet 4 says I can pick my face before I send. The Turn Input tab has no Face chip yet, and T78's Touches don't name the design doc: T78 should propose that edit.
- **T60 (after T76 in the plan):** its sheet's `reply_schema` (part 1b) and its checker's required list (part 5) are written without `emotion`. Keep T76's: `required` becomes `["actions", "speech", "vote", "reason", "pass", "emotion", "tell"]` (with `tell` after `emotion` in `properties`), the checker's required check and message name both, `check_reply`'s and `shape_fails`'s `types` get `"tell": str` beside `"emotion": str`, and its `prompts.json` `_readme` edit ("... speech, pass, vote, reason, tell.") keeps `emotion` too. **And `input_schema`:** since T69 the checker fails unless `input_schema` is `reply_schema`'s properties plus `attempt`, so T60's `tell` goes in `input_schema` as well (the input converter leaves it `""`, as T60's sheet says). The relay's free replies now carry `emotion` and still no `tell`, which T60's `--free` allowance covers.
- **T69:** nothing to change. Its sheet already says T76 adds `emotion` to both schemas, which part 2a does. Its `attempt_test` switch and `NoteAttempt` don't read `emotion`.
- **T68:** its `llm.json` `_readme` edits sit in other sentences than part 2b's; its `Relay/README.md` paragraph follows the paragraph part 5c changes.
- **T70 (the itch page):** "What gets sent where" doesn't change: the emotion is part of each AI's reply, not new data about the player.
