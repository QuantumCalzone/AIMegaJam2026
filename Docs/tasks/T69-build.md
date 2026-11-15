# T69 build sheet: the actions players try that the game can't do

Back to [T69](T69.md). A Mac prep session wrote this on 2026-11-15, without the editor, against **`noHumansOnSet` at `2e3e5c8`** (T67 done; the T63, T64 and T68 sheets in, with my person's answers to each). It is a plan, not a record: nothing here was written to the editor, the data files or the checker.

**T69 sits on work that isn't built yet.** This sheet writes the game as these sheets leave it:

- [T63-build.md](T63-build.md) (all): the input ask fixes spelling only. Every line of mine goes through `BP_Show.SpellAsk`, which asks the input LLM under the tag **`spell-<n>`** (decision 2 there), with T63's new `input` lines, `asks.input` and the checker's 13 spelling-only `INPUT_CASES`.
- [T64-build.md](T64-build.md) (parts 2 and 7): `WBP_ActionBuilder`, with its seven action buttons (`MoveBtn` … `NoneBtn`), the arrays `ActBtns`, `ActVerbs`, `ActOk` and `ActTip`, the `Show` reference, `Armed`, `Sent`, `Live`, and the greyed buttons as **disabled** buttons (`Refresh`: `SetIsEnabled` false, with the tip as tooltip).
- [T65-build.md](T65-build.md) (part 6b): T65 adds the preview's words to `WBP_ActionBuilder` and rewrites `Refresh`, `SetLine`, `StyleAll` and its event graph. Nothing T69 touches.
- [T68-build.md](T68-build.md) (all, with my person's two answers in `6dcfc25`): `BPC_Analytics` on `BP_Show` as `Analytics`, with `Send(Event, Fields)`, `Ready`, `Init`, `Active` and `CurPhase`; `BPC_LLMClient.Stats` (the analytics component, set in `LoadConfig`); `CountCall` as `Deliver`'s first line; `Class|BPShow|GetAnalytics` for widgets.
- [T67.md](T67.md) and the relay as pushed: the allow-list in `Relay/relay.config.json` takes `unsupported` with `words` (string, up to 80 characters), `source` (up to 10) and `phase` (up to 40), all optional; `Tools/analytics_report.py` already prints the "unsupported actions" heading (words, source, count).

Each place is named by its text first. Find each line by its text before you change it.

**Re-check against the `Graphs/` sources of your day** (none of these exists in the form below yet): `Graphs/BPC_LLMClient/Deliver.txt`, `LoadConfig.txt` and `HandleHttp.txt` (T68 edits all three), `FreeReply.txt` (T77 will change it later, not before T69); `Graphs/BPC_Analytics/Send.txt` and `Init.txt` (new in T68); `Graphs/WBP_ActionBuilder/OpenTurn.txt`, `Refresh.txt`, `FillLists.txt` and `WhyNot.txt` (new in T64, `Refresh` rewritten in T65); `Graphs/BP_Show/SpellAsk.txt` (T63: the `spell-` tag). Also `Content/NHOS/Data/prompts.json` `input` and `asks.input` and `Tools/check_prompts.py`'s `INPUT_CASES`, `check_reply` and `shape_fails` as T63 leaves them.

**Sources read:** `T69.md` and its plan entry; `T67.md`, `T63.md`, `T64.md`, `T68.md`, the T76 and T77 entries in the plan (they build on T69's reply shape); the T63, T64, T65 and T68 build sheets; `T61-build.md` part 6 and `T65-build.md` part 5d (how a widget override is made through MCP); `T38-build.md` (`GetCachedGeometry` forms); `T30.md` (the `if`/`return` rule); `Graphs/BPC_LLMClient/` (`Ask`, `BuildBody`, `LoadConfig`, `HandleHttp`, `ParseReply`, `Deliver`, `FlushLocal`, `FlushOne`, `FreeReply`, `ErrorTestPick`); `Content/NHOS/Data/llm.json`, `prompts.json`, `free_mode.json`; `Relay/src/index.js` (`checkEvent`, the free reply), `Relay/relay.config.json`; `Tools/check_prompts.py` (`check_files`, `request_body`, `check_reply`, `shape_fails`, the input cases), `Tools/analytics_report.py`; `Docs/switches.example.json`. **The design doc, read and not changed:** Bot Prompts rev 82.

## In short

- **The reply field is `attempt`** (step 1): at most 6 lowercase words naming a physical action the typed line describes or asks for that the player can't click ("backflip", "climb the chandelier"), `""` for plain speech, a pass or one of the five clickable actions. Never a name: any actor is "someone". It never changes the line or the turn.
- **The input ask gets its own schema** (decision 1): a new `input_schema` in `llm.json`, the reply shape plus `attempt`. The actors' `reply_schema` doesn't change, so no actor prompt changes and the AIs never see the field. Only the input ask's provider (Anthropic, `roles.input`) reads it; the schema stays valid under all four providers' strict rules in case that role moves.
- **No `BP_Show` change** (decision 2). The reply is read where it arrives, in `BPC_LLMClient`: `ParseFields` reads `attempt` into a new `RAttempt`, and `Deliver` hands a filled one from a `spell-` ask to a new `BPC_Analytics.Unsupported(Words, Source)` with `source` `typed`. T69 locks `BPC_LLMClient`, `BPC_Analytics` and `WBP_ActionBuilder`, not `BP_Show` or `WBP_Stage`.
- **`BPC_Analytics.Unsupported`** (new, decision 3): lower case, cut to 6 words and 80 characters, dropped if it holds "@" or "player ", sent at most once per phase for the same words and source, with `phase` = `CurPhase`. `Send` (T68) then decides whether anything goes out: builds only, the switch, autoplay, Play stats.
- **The builder's blocked clicks** (step 3): T64's greyed buttons are disabled, so they fire no click. A disabled button lets the mouse event pass to its parents, so a new **`OnMouseButtonDown` override on `WBP_ActionBuilder`** hit-tests the greyed buttons under the pointer and sends `unsupported` with `source` `builder` and words like `throw, holding nothing`, at most once per verb per turn. It returns Unhandled, so nothing else changes. **It must be tried first (part 5a);** if the event doesn't reach the widget, step 3 is left out, as the task allows.
- **Free mode leaves `attempt` empty**: the game's free echo and the relay's free reply never set it, and a missing field reads as `""`. For the PIE check, a new switch **`attempt_test`** (decision 6) gives every free input reply that attempt, the way `error_test` fakes failures.
- **Prompts:** one new rule line at the end of T63's `input`, a sentence in `asks.input`, one in `_readme` (part 1). **Checker:** `input_schema` kept in step with `reply_schema`, the input ask's body uses it, `attempt` checked in every input reply, three new cases and one changed (part 4).
- **Checks:** `--offline` and `--relay --free` cost nothing; the one paid `--ask input` run is 16 cases on Anthropic, **about 3 cents** (part 7).
- **No `Relay/` change and no deploy:** the relay takes `unsupported` already, and its free reply needs no `attempt`.

## Decisions made for my person

My person asked prep sessions to take their own recommendation on design calls. Each is open to change. The T69 session shows this list to my person when it closes the task.

1. **The input ask gets its own schema (`input_schema`), not a field in the shared `reply_schema`.** The task asks T69 to weigh the two and write the pick under "Findings"; this is the pick and why:
   - **Strict-schema rules, all four providers.** OpenAI's strict mode (and the two OpenAI-shaped providers, xAI and Meta, which `llm.json` sends with `strict: true`) wants every property in `required` and `additionalProperties: false`; Anthropic's structured outputs take the same schema. So a new field must be required wherever it is, and every reply under that schema must carry it. A shared field means every actor reply on all four providers returns `"attempt": ""`; its own schema means only the input reply does.
   - **Tokens.** About 125 actor calls a show (`CALLS_PER_SHOW`) would each write about 5 more output tokens (`,"attempt":""`), and each request carries the bigger schema. That is small in money, but it is spent on a field the actors must never fill.
   - **Behaviour.** A field named `attempt` in the actors' schema invites them to write stage directions into it, and the actors' prompts would need a line telling them to leave it empty (`base` or `game`, outside T69's Touches, and a Bot Prompts edit for the opening or base prompt). With its own schema, no actor prompt changes.
   - **The cost of its own schema:** one new key in `llm.json`, two small edits in `BPC_LLMClient` (`LoadConfig` reads it; `BuildBody` picks it for the input role) and one in the checker's `request_body`. And a schema change makes Anthropic compile the new grammar once (it caches it after that), so the first input call after the change can be slower; with T63's 4-second `spelling_wait` that line may go as typed once (`NHOS: SPELLING skipped late`), and its `attempt` is still counted (decision 2).
   - **For T76 and T77:** T76 adds `emotion` to `reply_schema`; T77 has the input LLM pick my emotion, so `input_schema` needs it too. The checker's new check (part 4c) fails if the two schemas drift apart, so T76 can't miss it.
2. **The game reads `attempt` in `BPC_LLMClient`, not `BP_Show`.** The client parses every reply (`ParseFields`), and `Deliver` sees each one before `BP_Show` does, so one new function there (`NoteAttempt`) and one call in `Deliver` send it. `BP_Show` and the line path T63 builds don't change, and T69 needs no lock on `BP_Show` (see "Knock-on" for what that means for the two machines). A reply that comes after `spelling_wait` (dropped by `BP_Show` as `STALE`) still has its `attempt` counted: the player did type it.
3. **A wrapper, `BPC_Analytics.Unsupported(Words, Source)`, outside T69's Touches.** T68's sheet says T69 calls `Send` itself, but two callers (the client and the builder) need the same cleanup, so it lives in one function next to `Send`, in T68's style ("named wrappers keep each caller to one node"). The commit message names `BPC_Analytics.uasset` and `Graphs/BPC_Analytics/Unsupported.txt` as outside the Touches.
4. **The five clickable actions don't count.** "I throw the rose" says those words (T63) and leaves `attempt` `""`, because the builder can do it; the event is for what the game can't do, and the report's heading says so. Players typing clickable actions would be a builder problem for T64's hints, not a missing verb.
5. **The privacy guard is in three places:** the prompt says "someone" for any actor and never a name; `Unsupported` drops any words holding "@" or "player " (a Player name) and prints why; the checker fails an input reply whose `attempt` holds a provider name, "@" or "player". See "What a row holds".
6. **The PIE check fakes the field with a new switch, `attempt_test`** (in `Local/switches.json`, read with `error_test` in `LoadConfig`), not a paid relay turn. In Test for Free every input reply then carries that text as its `attempt`. It adds `"attempt_test": ""` and one sentence to `Docs/switches.example.json`, outside the Touches; the commit message names it. The other way (one turn in Play via Relay) costs real tokens and needs my person's OK each time.
7. **Every phase counts, not only scene turns.** The input ask runs for scene lines, Free Talk, last words, reactions and vote reasons; a "*does a backflip*" in Free Talk is as telling. `phase` says where.
8. **The builder's words** are the verb and a short reason, mapped from T64's tips: Throw or Give with nothing held → `throw, holding nothing` / `give, holding nothing`; Grab with nothing free → `grab, nothing free`; Grab with full hands → `grab, hands full`; Give when nobody has a free hand → `give, no free hand`; nothing to pick → `<verb>, no target`. "The stage isn't ready." is the game's state, not a player's try, and sends nothing.
9. **The `Docs/ItchPage.md` privacy bullet gets T69's words in T69** (outside the Touches; the commit names it), as T68's sheet asks (its part 9c and 13): the page must say what is sent from the day T69 sends it.

## What a row of this event holds (privacy)

T67 step 6 lists what may be stored: "an anonymous player id, the mode, the phases, call counts and tokens, error kinds and a few words for an unsupported action. Never typed text, keys or the address." T68's itch-page bullet says the same to players, with the Play stats switch as the opt-out. One `unsupported` row, as `BPC_Analytics.Send` builds it and the relay stores it:

```json
{"player": "3f9c0d2e…(32 hex)", "session": "8b1e…", "build": "2026-11-15", "mode": "relay",
 "event": "unsupported", "fields": {"words": "backflip", "source": "typed", "phase": "turn_2"}, "test": false}
```

plus what the relay adds: the UTC time and the day-salted hash of the address (`hashIp`), never the address.

- **`words`:** at most 6 lowercase words and 80 characters (the relay's cap), written by the input LLM from the typed line (`typed`) or by the game from the greyed button (`builder`). **Never the typed line itself:** the line goes to the AIs as speech, as before, and never to the relay's store. No names: the prompt asks for "someone", `Unsupported` drops "@" and "player ", the checker tests it. A player who types a real person's name into a stage direction is the one gap the game can't see ("hug Taylor"); the prompt's "never write a name" covers it, and the paid run's name case (part 4d) checks that the model follows it.
- **`source`:** `typed` or `builder`. **`phase`:** T68's phase key (`turn_2`, `free_talk_1`, `last_word`, `vote`, `reactions` …). No scene number: the allow-list has no `scene` field for this event, and adding one would change `Relay/`.
- **Who sends:** exactly as every T68 event (`Send` checks `Active`): only a packaged build, never the editor unless the `analytics` switch is `test` (then `"test": true`); never with the switch `off`, in autoplay without `test`, or when the player turned Play stats off on the title screen.
- **How many:** at most one per phase for the same words and source, and one per verb per turn for the builder. A player who types a stage direction in every line sends about 20 a show, well inside T67's 500 a day per address (T68's sheet counts about 60 events a show without T69).
- **Test for Free never sends a `typed` row:** free mode makes no LLM call, so `attempt` stays empty there (except under `attempt_test`). `builder` rows come from every mode.

## 0. Before you start (after T63, T64 and T68 are pushed)

1. `git log --oneline -20` shows T63, T64, T65 and T68 (and T66, which comes before T68). `Docs/claims/T68` is released. `git lfs locks` shows no lock on `Content/NHOS/Core/BPC_LLMClient.uasset`, `Content/NHOS/Core/BPC_Analytics.uasset` or `Content/NHOS/UI/WBP_ActionBuilder.uasset`. Claim T69 and lock all three. **`BP_Show` and `WBP_Stage` need no lock** (decision 2).
2. **Read what changed since this sheet:** the files under "Re-check" above, and the Findings of `T63.md`, `T64.md`, `T65.md` and `T68.md`. In particular:
   - **T63:** the spelling ask's tag is still `spell-<n>` (`Graphs/BP_Show/SpellAsk.txt`). If T63 renamed it, use its prefix in part 3d. The `input` lines and `INPUT_CASES` are T63's (its parts 3b and 6c); part 1 and part 4 add to them.
   - **T64:** the greyed buttons are disabled (`Refresh`), `ActVerbs` holds `move, look, grab, throw, give, around, none` in the buttons' order (`FillLists`), `ActTip` holds T64's tips (`WhyNot`), and the widget keeps `Show`, `Armed`, `Sent` and `Live`. If T64 wrapped each button in a `Border` for the tooltip (its note under `Refresh`), the hit test in part 5 uses the `Border`s instead of the buttons; nothing else changes.
   - **T68:** `BPC_Analytics` has `Ready`, `Init`, `Send(Event, Fields)` and `CurPhase`; the client has `Stats`; `Deliver` starts with `CountCall`; `WBP_Title` reads the component with `Class|BPShow|GetAnalytics`. The `NHOS: ANALYTICS <event> <fields>` print is T68's `Send`.
3. `python Tools/check_prompts.py --offline` passes before you start, so any failure afterward is T69's.
4. **Ask my person for the OK on part 6's doc text** at the start, with the multiple-choice tool. The paid run (part 7c) needs its own OK later.
5. **Survey, one `call_tool` each** (calls stop at about 120 s; save each read to `Saved/T69/<graph>.read.txt`; never write a read-back to the editor):
   1. **`BPC_LLMClient.ParseFields`** (no file; `read_graph_dsl`). Record how it reads `speech` and `pass` (the JSON object, the `HasField` / `GetField` forms), its last node before `return true`, and **whether it fails a reply with a field it doesn't know** (expected: no, it reads only the fields it wants). Part 3c adds to it.
   2. **`BPC_LLMClient.ClearReply`** (no file): the `Set` nodes it holds (`RSpeech`, `RVote`, `RReason`, `RPass`, `RVerbs`, `RTargets`, `RItems`). Part 3c adds one.
   3. **`ObjectTools.list_properties` on `BPC_LLMClient`:** the type of `ReplySchema` (the JSON object type; `InputSchema` gets the same) and that `RAttempt`, `InputSchema`, `BSchema` and `AttemptTest` don't exist yet.
   4. **The override:** how T65 made `WBP_Stage.OnPreviewKeyDown` (its Findings, survey 5 there). Make `OnMouseButtonDown` the same way (part 5a). If T65 found no way, try `UserInterface|OnMouseButtonDown` with `find_node_types` (`context_pins: []`), then `write_graph_dsl` with `(fn OnMouseButtonDown (MyGeometry MouseEvent) ...)` on a scratch widget (`/Game/Scratch/WBP_ClickTest`, deleted after), and check that the entry has the parent's pins and that it compiles.
   5. **Node names** (`find_node_types`, `context_pins: []`): `PointerEvent_GetScreenSpacePosition` (Kismet Input Library; expected `Utilities|Input|PointerEvent|GetScreenSpacePosition` or similar), `IsUnderLocation` (Slate Blueprint Library; expected `Utilities|Geometry|IsUnderLocation`), `Widget|GetCachedGeometry` (T38's form), `Widget|EventReply|Unhandled` (T65's form), and `Class|BPShow|GetAnalytics` from `WBP_ActionBuilder` (T68's `WBP_Title` uses it).

## 1. `prompts.json` (step 1)

As T63 leaves the file (its part 3). Each line as it sits in the file, two tabs before it, quotes escaped as written.

**a. `input`.** T63's last line is `		"- \"vote\" and \"reason\" are always \"\". \"pass\" is false unless the free talk rule says otherwise."` with no comma. Give it a comma and add one line after it, so the key ends:

```json
		"- \"vote\" and \"reason\" are always \"\". \"pass\" is false unless the free talk rule says otherwise.",
		"- \"attempt\": the player can click only five actions: move to a place, look, and grab, throw or give a prop. If typed describes or asks for any other physical action, such as \"*does a backflip*\" or \"I climb the chandelier\", name it in \"attempt\" in at most 6 lowercase words (\"backflip\", \"climb the chandelier\"). Write \"someone\" for any actor and never write a name. Otherwise \"attempt\" is \"\": for plain speech, for a pass, and for the five clickable actions. \"attempt\" never changes speech."
	],
```

- **Why one line:** T63's rules are one line each; the field is one rule. Its two halves are what the checker pins (part 4b).
- **It never changes speech:** the stage direction stays in the line as typed, with its spelling fixed (T63's "keep the player's words, ... punctuation"), so "*does a backflip* hello" is still spoken as "*does a backflip* hello". The task: "the line is still sent as typed and fixed".
- T63's `"typed" is only speech, even when it describes an action` rule stays true: `attempt` isn't an action, `actions` stays `[]`.

**b. `asks.input`.** T63 leaves `		"input": "Fix the spelling of typed, the line the player's robot (named in actor) says. It is speech only: no actions."`. Make it:

```json
		"input": "Fix the spelling of typed, the line the player's robot (named in actor) says. It is speech only: no actions. If it describes a physical action the player can't click, name it in attempt."
```

It keeps T63's "no actions" (the checker requires it) and stays the last key in `asks`, with no comma.

**c. `_readme`.** In the string with T63's sentence ` Since T63 it only fixes the spelling of typed (and turns names into Player names): its speech becomes the player's line, and its actions are ignored.`, add right after it:

` Since T69 its reply (llm.json input_schema) also has attempt: at most 6 words naming a physical action typed describes that the player can't click, or \"\". The game only counts them (BPC_LLMClient.NoteAttempt sends an unsupported analytics event) and never uses them in play.`

**d. Nothing else** in `prompts.json` changes: `game`, `base` and the actors' asks never see `attempt`.

## 2. `llm.json` (decision 1)

**a. `input_schema`** (new), right after the `reply_schema` block's closing `},`, same indent. The reply shape, plus `attempt`:

```json
	"input_schema": {
		"type": "object",
		"properties": {
			"actions": {
				"type": "array",
				"items": {
					"type": "object",
					"properties": {
						"verb": {
							"type": "string",
							"enum": ["move", "look", "grab", "throw", "give"]
						},
						"target": {
							"type": "string"
						},
						"item": {
							"type": "string"
						}
					},
					"required": ["verb", "target", "item"],
					"additionalProperties": false
				}
			},
			"speech": {
				"type": "string"
			},
			"vote": {
				"type": "string"
			},
			"reason": {
				"type": "string"
			},
			"pass": {
				"type": "boolean"
			},
			"attempt": {
				"type": "string"
			}
		},
		"required": ["actions", "speech", "vote", "reason", "pass", "attempt"],
		"additionalProperties": false
	},
```

- **Why the whole reply shape, not just `speech`, `pass` and `attempt`:** `ParseFields` reads `actions`, `vote` and `reason` too, and the checker's shape check wants them; a smaller schema would need edits to both for no gain (T63's input LLM already returns them empty).
- **No `maxLength` on `attempt`:** strict mode on the OpenAI-shaped providers refuses some string keywords, and the schema must stay valid if `roles.input.provider` ever moves there. `Unsupported` cuts to 6 words and 80 characters.

**b. `_readme`** (the top-level one). Find `reply_schema is the one reply shape for every ask (scene turn, Free Talk line, vote, reaction, closing line, input conversion); unused fields come back empty.` and make it:

`reply_schema is the reply shape for every actor ask (scene turn, Free Talk line, vote, reaction, closing line); input_schema is the same shape plus attempt, for the input ask alone (T69: a few words naming an action the player typed that the game can't do, for analytics); unused fields come back empty.`

T62 already flagged the same paragraph's `and uses at most 2 actions`; if T62 or T63 changed it, leave their words.

**c. `providers._readme`.** Find `json_schema {name: reply, schema: reply_schema, strict: true}` and make it `json_schema {name: reply, schema: reply_schema (input_schema for the input ask), strict: true}`; and in the Anthropic sentence of the same string, `format {type: json_schema, schema: reply_schema}` → `format {type: json_schema, schema: reply_schema (input_schema for the input ask)}`.

## 3. `BPC_LLMClient`

### 3a. Graphs and files

| Graph | File in `Graphs/BPC_LLMClient/` | T69 | How |
|---|---|---|---|
| `LoadConfig` | yes (T68 edits it) | reads `input_schema` and `attempt_test` | edit the file, write it (3b) |
| `BuildBody` | yes | the schema by role | edit the file, write it (3b) |
| `ParseFields` | **none** | reads `attempt` | node edit (3c), after survey 1 |
| `ClearReply` | **none** | clears `RAttempt` | node edit (3c), after survey 2 |
| `FreeReply` | yes | `attempt_test` in the echo branch | edit the file, write it (3c) |
| `NoteAttempt` | new | the event | new file (3d) |
| `Deliver` | yes (T68 edits it) | one call | edit the file, write it (3d) |

**New variables:** `InputSchema`, `BSchema` (the JSON object type of `ReplySchema`, survey 3), `RAttempt`, `AttemptTest` (String, ""). Order (T18, T54: a call node goes stale when its function gets a new parameter): the variables; `NoteAttempt` empty with its `Tag` input; compile; then `BPC_Analytics.Unsupported` (part 5c) must exist before `NoteAttempt`'s body is written; then the graphs. Compile and save after each group.

### 3b. The schema

**`LoadConfig.txt`.** Right after `  (set ReplySchema _f4)`:

```lisp
  (set InputSchema (V ReplySchema))
  (bind _his (Json|HasField _o "input_schema"))
  (if _his
    (bind _fis (Json|GetField _o "input_schema"))
    (set InputSchema _fis))
```

A missing `input_schema` falls back to `reply_schema`, so an old `llm.json` still works (with no `attempt`). Then, with the switches: after `  (set ErrTest "")` add `  (set AttemptTest "")`, and inside the `(if _sok ...)` block, after the `error_test` read (its last line ends `(set ErrTest _set)))`; move the block's closing parenthesis to the new last line):

```lisp
    (bind _hat (Json|HasField _so "attempt_test"))
    (if _hat
      (bind _sat (Json|GetField _so "attempt_test"))
      (set AttemptTest _sat)))
```

and on the `NHOS: CLIENT ready` print, after `" error_test=" (V ErrTest)` add `" attempt_test=" (V AttemptTest)`. Top comment line: `; T69: also input_schema (the input ask's reply shape) and the attempt_test switch.`

- These are top-level `if`s without `return` after the file's `(if (not _ok) (return ...))`, the form `LoadConfig` already uses for `relay` (`_hr`). If a read-back shows the new lines landing in a then branch, T30's rule applies: move them before the first `if` that returns.

**`BuildBody.txt`.** Right after `  (set TokCap _mt)` (before the `(if (not (streq Role "actor"))` block):

```lisp
  (set BSchema (V ReplySchema))
  (if (streq Role "input")
    (set BSchema (V InputSchema)))
```

and replace both `(V ReplySchema)` further down with `(V BSchema)`: `(Json|SetField _js "schema" (V ReplySchema))` (the `openai_chat` branch) and `(Json|SetField _fm "schema" (V ReplySchema))` (the Anthropic branch). Top comment line: `; T69: the input ask uses input_schema (reply_schema plus attempt); every actor ask keeps reply_schema.`

- The relay checks the body's keys (`body_keys`), not the schema inside `output_config` or `response_format`, so it takes the new schema as it is (`Relay/src/index.js`; the 64 KB body cap is far off).

### 3c. Reading the field, and free mode

**`ParseFields`** (node edit, no file). After the nodes that read `pass` (survey 1), before its `return true`: a `HasField` on the reply object with `"attempt"`, a `Branch`; True → `GetField "attempt"` → `Set RAttempt`; both branches join the old return. A missing field leaves `RAttempt` as `ClearReply` set it, `""`. Write the old and new nodes under "Findings" in `T69.md` (no file to update). If survey 1 found that `ParseFields` fails on an unknown field, that would already break T69's input replies: fix it to ignore extras and say so.

**`ClearReply`** (node edit, no file): one `Set RAttempt ""` after its last `Set`. `HandleHttp` and `FlushLocal` call it before each reply, so an old `attempt` never rides on the next reply.

**`FreeReply.txt`.** In the `echo_typed` branch, right before its `(return)`, after `(set RSpeech (Utilities|String|JoinStringArray (V TmpArr2) " "))`:

```lisp
    (set RAttempt (V AttemptTest))
```

Top comment line: `; T69: free mode leaves attempt empty; the attempt_test switch fills it on every input reply (the echo), for the PIE check.` With the switch empty (always, outside a test), free mode leaves `attempt` empty, as the task says.

- **The relay's free mode** (`Relay/src/index.js`, the free reply) returns `{actions, speech, vote, reason, pass}` with no `attempt`; `ParseFields` reads a missing field as `""`. So Play via Relay in free mode (the checker's `--relay --free`) also leaves it empty, and `Relay/` doesn't change. T76 touches the relay's free reply anyway; it may add `"attempt": ""` to input replies, which changes nothing here.

### 3d. Sending it

**`Graphs/BPC_LLMClient/NoteAttempt.txt`** (new):

```lisp
; T69: the input LLM's attempt field: a few words naming a physical action the player typed that the game can't do.
; Deliver calls this for every reply to a spelling ask (spell-<n>, T63), in time or late. It never changes the line or
; the turn: BP_Show never sees it. BPC_Analytics.Unsupported cleans it and decides whether it goes out.
(fn NoteAttempt (Tag)
  (bind _a (Utilities|String|Trim (V RAttempt)))
  (if (Utilities|String|IsEmpty _a)
    (return))
  (print (cat "NHOS: ATTEMPT " Tag " " _a))
  (Class|BPCAnalytics|Unsupported :self (V Stats) :Words _a :Source "typed"))
```

- `NHOS: ATTEMPT` prints in every run, analytics on or off, so a check can see the field arrive without the relay (part 7d).

**`Deliver.txt`.** As T68 leaves it, `Deliver` is: `CountCall` (T68), `(set TmpStr2 ...)`, the `(if Ok (print ...) (else (print ...) (CallFunction|ClearReply)))` block, `BackstageNote`, `CallOnAnswer`. Between the `if Ok` block and `(CallFunction|BackstageNote :Tag Tag :Ok Ok :Error Error)`:

```lisp
  (if (and Ok (Utilities|String|StartsWith :SourceString Tag :InPrefix "spell-"))
    (CallFunction|NoteAttempt :Tag Tag))
```

Top comment line: `; T69: a spelling reply's attempt goes to NoteAttempt (analytics) before BP_Show hears of it.`

- **Before `CallOnAnswer`,** because `BP_Show.HandleReply` can start the next turn at once (T63's `HumanSay` note), and `RAttempt` must still be this reply's.
- **By tag, not role:** `Deliver` doesn't know the role, and only T63's spelling ask uses `spell-`. A failed ask (`Ok` false) is skipped; `ClearReply` has emptied `RAttempt` anyway.
- Neither `if` has a `return`, so both join the next line (T30).

## 4. `Tools/check_prompts.py`

As T63 leaves it (its part 6). Find each line by its text.

**a. The docstring.** After T63's "Spelling only (T63)" paragraph, add:

```
The attempt field (T69): the input ask has its own schema in llm.json,
input_schema, which is reply_schema plus "attempt", so no actor ask carries
it. Every input reply must hold "attempt": at most 6 words naming a physical
action the typed line describes that the player can't click, or "". It never
holds a provider or Player name or an "@". Free mode leaves it empty (the
relay's free reply has no attempt at all, which reads as ""). The file check
keeps input_schema in step with reply_schema and pins the prompt's attempt rule.
```

**b. Constants.** After T63's `INPUT_RULES = [...]`:

```python
# T69: the input LLM names an action the player can't click in "attempt" (at most 6 words); prompts.json 'input' keeps this rule.
INPUT_ATTEMPT_RULES = ['- "attempt": the player can click only five actions', '"attempt" never changes speech.']
MAX_ATTEMPT_WORDS = 6
```

**c. `check_files`.** In the `# llm.json` block, right after the `reply_schema must require ...` check:

```python
    # T69: the input ask's own schema is reply_schema plus "attempt", so the two can't drift apart (T76 adds emotion to both).
    ischema = llm.get("input_schema", {})
    want_props = dict(schema.get("properties", {}), attempt={"type": "string"})
    if ischema.get("properties") != want_props:
        errors.append("llm.json: input_schema must be reply_schema's properties plus attempt (a string)")
    if sorted(ischema.get("required", [])) != sorted(schema.get("required", []) + ["attempt"]):
        errors.append("llm.json: input_schema must require reply_schema's fields plus attempt")
    if ischema.get("additionalProperties") is not False or ischema.get("type") != "object":
        errors.append("llm.json: input_schema must be an object with additionalProperties false (strict mode)")
    if "attempt" in schema.get("properties", {}):
        errors.append("llm.json: reply_schema has attempt; since T69 only input_schema does")
```

and next to T63's `INPUT_RULES` loop (after it):

```python
    # T69: the attempt rule.
    for rule in INPUT_ATTEMPT_RULES:
        if not any(rule in line for line in prompts.get("input", [])):
            errors.append(f"prompts.json: 'input' lost a T69 rule: {rule!r}")
    if "attempt" not in prompts.get("asks", {}).get("input", ""):
        errors.append("prompts.json: asks.input must name attempt (T69)")
```

**d. The input cases.** Add three cases at the end of T63's `INPUT_CASES` (after its `asdf qwerty zxcv` case) and an `attempt` key on one of T63's:

```python
    # T69: the attempt field. True = it must name an action (at most 6 words), False = it must be "".
    {"phase": "scene", "typed": "*does a backflip* hello", "contains": ["backflip", "hello"], "attempt": True},
    {"phase": "scene", "typed": "hello there", "speech": "hello there", "attempt": False},
    # A stage direction about an actor: "someone", never a name.
    {"phase": "free talk", "typed": "i climb onto @OpenAI's shoulders", "contains": ["@Player 1"], "attempt": True},
```

and on T63's `{"phase": "scene", "typed": "I throw the rose at @Anthropic", "speech": "I throw the rose at @Player 2"}`, add `"attempt": False` (a clickable action, decision 4). The first two are the task's Done-when cases. 16 cases, so the job count grows by 3.

**e. `request_body`.** The schema by role, in both formats. After the `model, effort, max_tokens = ...` line:

```python
    schema = llm["input_schema"] if role == "input" else llm["reply_schema"]  # T69: only the input ask has attempt
```

and replace both `llm["reply_schema"]` in the two bodies with `schema`. Update the docstring's last sentence: `'input' takes its role's (llm.json _readmes), and input_schema (T69).`

**f. `check_reply`.** At the top, the types by ask:

```python
    types = {"actions": list, "speech": str, "pass": bool, "vote": str, "reason": str}
    if ask == "input":
        types["attempt"] = str  # T69: input_schema
```

(the `extra = set(reply) - set(types)` check then refuses `attempt` in an actor reply and accepts it in an input reply). In T63's `elif ask == "input":` branch, after its `need(passed == case.get("pass", False), ...)` line:

```python
        # T69: the attempt field.
        att = reply["attempt"].strip()
        need(words(att) <= MAX_ATTEMPT_WORDS, f"attempt has {words(att)} words: {att!r}")
        for leak in provider_leaks(att, ctx["providers"]) + [w for w, r in BANNED_RES if r.search(att)]:
            fails.append(f"attempt names a provider or model: {leak!r}")
        need("@" not in att and "player" not in att.lower(), f"attempt names an actor: {att!r}")
        if case.get("attempt") is True:
            need(att, "attempt is empty; the line describes an action the player can't click")
        elif case.get("attempt") is False:
            need(not att, f"attempt is {att!r}; expected \"\"")
```

**g. `shape_fails`** takes the ask, and free mode leaves `attempt` empty or out:

```python
def shape_fails(reply, ask=None):
    """Only the reply's shape: every schema field with the right type (for --free replies). T69: an input reply may
    leave out attempt (the relay's free reply has none), but a free reply never fills it."""
    types = {"actions": list, "speech": str, "pass": bool, "vote": str, "reason": str}
    fails = [f"{k} is missing or not a {t.__name__}" for k, t in types.items() if not isinstance(reply.get(k), t)]
    if ask == "input" and reply.get("attempt", "") != "":
        fails.append(f"free mode filled attempt: {reply.get('attempt')!r}")
    return fails
```

and its one caller, `fails, warns = shape_fails(reply), []`, becomes `fails, warns = shape_fails(reply, ask), []`.

**h. What doesn't change:** `ALL_ASKS`, `ACTOR_ASKS`, `CALLS_PER_SHOW`, `build_jobs` (it loops over `INPUT_CASES`), `check_log` (the `NHOS: ATTEMPT` and `NHOS: ANALYTICS` lines aren't AI lines; T68 leaves `--log` alone too), `Tools/analytics_report.py` (its "unsupported actions" heading already lists `words` and `source`).

**i. Not tried on a scratch copy.** T63's checker edits (which these build on) aren't in the tree yet, so this part was checked by reading only. When T69 runs, break each new check once on purpose and see one clear line: remove `attempt` from `input_schema.required`; add `attempt` to `reply_schema`; drop the rule line from `input`.

## 5. `WBP_ActionBuilder`: the blocked clicks (step 3)

### 5a. Try it first (decides whether step 3 is built)

T64 greys an action by disabling its button, and a disabled `Button` fires no `OnClicked`. Slate still routes the mouse-down along the widget path: a disabled button doesn't handle it, so it bubbles to the enabled parents, `WBP_ActionBuilder` among them, whose `OnMouseButtonDown` override sees it. The hit test then tells which greyed button is under the pointer.

1. Make the override (survey 4) with only `(print "NHOS: BUILDER mouse down")` and `(return (Widget|EventReply|Unhandled))`. Compile, save.
2. PIE (Test for Free, autoplay off, 1600 × 900): at scene 1, turn 1, Throw and Give are greyed (T64's `turn1_open.png`). Click Throw **with a real mouse click** (the Slate inspector may call `OnClicked` directly and skip the routing; if it can't send a real click, ask my person's OK for computer use on the editor, or ask them to click once).
3. **The log prints `NHOS: BUILDER mouse down`:** build 5b and 5c. **It doesn't** (and a click on an open button doesn't print it either, so the widget sees no mouse at all): try the same override with the root `BuilderBox` set to `Visible` instead of `SelfHitTestInvisible` (T64's `OpenTurn` sets the root visibility). Still nothing: **leave step 3 out**, delete the override, and write under "## Findings": "T64's greyed actions are disabled buttons, which swallow the click and pass no mouse event to the builder; telling those clicks apart needs enabled buttons styled as greyed (a rework of `Refresh`, `StyleAll` and `PickVerb`), so step 3 is left out." The task allows it.

### 5b. Variables and functions

New variable: `BlockSent` (String array). New functions, in this order (inputs first, compile, then the graphs callee first, T18):

| Function | Inputs | Outputs |
|---|---|---|
| `BlockWords` | `Act`, `Tip` (String) | String |
| `BlockedClick` | `K` (Integer) | — |
| `GreyClickAt` | `Pos` (Vector2D) | — |
| `OnMouseButtonDown` | the override's own (`MyGeometry`, `MouseEvent`) | `EventReply` |

`Graphs/WBP_ActionBuilder/BlockWords.txt`:

```lisp
; T69: the few words a click on a greyed action sends (decision 8): the verb and why it's greyed, from T64's tip.
; "" for a tip that is about the game, not the player ("The stage isn't ready."), which sends nothing.
(fn BlockWords (Act Tip)
  (if (streq Tip "Grab something first.")
    (return (cat Act ", holding nothing")))
  (if (streq Tip "Nothing free to grab.")
    (return (cat Act ", nothing free")))
  (if (streq Tip "Your hands are full.")
    (return (cat Act ", hands full")))
  (if (streq Tip "Nobody has a free hand.")
    (return (cat Act ", no free hand")))
  (if (streq Tip "Nothing to pick.")
    (return (cat Act ", no target")))
  (return ""))
```

- The tips are T64's decision 10 and its `WhyNot.txt`. **If T64 changed a tip's words, use its words here**; a tip this map doesn't know sends nothing, so a missed one is quiet, not wrong. Part 7d checks the Throw one.

`Graphs/WBP_ActionBuilder/BlockedClick.txt`:

```lisp
; T69: a click on the greyed action K: one unsupported event per verb per turn (OpenTurn clears BlockSent).
; BPC_Analytics.Unsupported adds the phase and decides whether it goes out (T68's Send).
(fn BlockedClick (K)
  (bind _v (get (V ActVerbs) K))
  (bind _w (CallFunction|BlockWords :Act _v :Tip (get (V ActTip) K)))
  (if (Utilities|String|IsEmpty _w)
    (return))
  (if (>= (Utilities|Array|FindItem (V BlockSent) _v) 0)
    (return))
  (add (V BlockSent) _v)
  (print (cat "NHOS: BUILDER greyed click " _v))
  (bind _an (Class|BPShow|GetAnalytics :self (V Show)))
  (Class|BPCAnalytics|Unsupported :self _an :Words _w :Source "builder"))
```

`Graphs/WBP_ActionBuilder/GreyClickAt.txt`:

```lisp
; T69: which greyed action button, if any, is under the pointer (Pos, in screen space). Only while my turn is live,
; before I send: at any other time every button is off, and a click on one says nothing about a missing action.
(fn GreyClickAt (Pos)
  (bind _on (and (V Armed) (and (not (V Sent)) (V Live))))
  (if _on
    (for _k (range (len (V ActBtns)))
      (if (not (get (V ActOk) _k))
        (bind _g (Widget|GetCachedGeometry :self (get (V ActBtns) _k)))
        (if (Utilities|Geometry|IsUnderLocation _g Pos)
          (CallFunction|BlockedClick :K _k))))))
```

`Graphs/WBP_ActionBuilder/OnMouseButtonDown.txt` (the override, made the way survey 4 found):

```lisp
; T69: a disabled (greyed) action button passes its mouse-down up to the builder (part 5a). GreyClickAt finds which
; one it was. Always Unhandled, so every other click works as before.
(fn OnMouseButtonDown (MyGeometry MouseEvent)
  (bind _pos (Utilities|Input|PointerEvent|GetScreenSpacePosition MouseEvent))
  (CallFunction|GreyClickAt :Pos _pos)
  (return (Widget|EventReply|Unhandled)))
```

- **No `return` before the loop** in `GreyClickAt` and none in the override until the end, so T30's rule can't bite.
- **Screen space on both sides:** the pointer's screen-space position and each button's cached geometry (absolute). `IsUnderLocation` takes an absolute coordinate. If survey 5 names the nodes differently, use its names.
- **An open button's own click** (`OnClicked` → `PickVerb`) is handled by the button and never reaches the builder, so `GreyClickAt` runs only for clicks the buttons didn't take: greyed buttons, gaps, the preview, the chips' gaps. Only a greyed button under the pointer sends anything.
- If T64 wrapped the buttons in `Border`s for the tooltips, loop over those (the hit areas are the same).

### 5c. `OpenTurn.txt`: one line

After T64's `  (set Sent false)`:

```lisp
  (clear (V BlockSent))
```

and a comment line at the top: `; T69: a new turn clears BlockSent, so each greyed action reports once per turn.`

### 5d. `BPC_Analytics.Unsupported` (new, outside the Touches; decision 3)

New variables on `BPC_Analytics`: `UWords`, `UKeep`, `USent` (String arrays), `UPhase` (String, ""). `Graphs/BPC_Analytics/Unsupported.txt`:

```lisp
; T69: an action the player tried that the game can't do (T67's unsupported event). Source "typed" is the input LLM's
; attempt field (BPC_LLMClient.NoteAttempt); "builder" is a click on a greyed action (WBP_ActionBuilder.BlockedClick).
; Only these few words go out, never the typed line: lower case, at most 6 words and 80 characters (the relay's cap),
; and never a name. The same words from the same source go out once per phase. Send decides whether anything goes out.
(fn Unsupported (Words Source)
  (if (not (V Ready))
    (CallFunction|Init))
  (if (not (streq (V UPhase) (V CurPhase)))
    (set UPhase (V CurPhase))
    (clear (V USent)))
  (set UWords (Utilities|String|ParseIntoArray :SourceString (Utilities|String|ToLower (Utilities|String|Trim Words)) :Delimiter " " :CullEmptyStrings true))
  (clear (V UKeep))
  (for _i (range (Math|Integer|Min(Integer) (len (V UWords)) 6))
    (add (V UKeep) (get (V UWords) _i)))
  (set TmpStr (Utilities|String|GetSubstring :SourceString (Utilities|String|JoinStringArray (V UKeep) " ") :StartIndex 0 :Length 80))
  (bind _key (cat Source "|" (V TmpStr)))
  (if (Utilities|String|IsEmpty (V TmpStr))
    (return))
  (if (or (Utilities|String|Contains :SearchIn (V TmpStr) :Substring "@") (Utilities|String|Contains :SearchIn (V TmpStr) :Substring "player "))
    (print (cat "NHOS: ANALYTICS unsupported dropped (a name) source=" Source))
    (return))
  (if (>= (Utilities|Array|FindItem (V USent) _key) 0)
    (return))
  (add (V USent) _key)
  (bind _f (Json|LoadJsonfromString "{}"))
  (Json|SetField _f "words" (V TmpStr))
  (Json|SetField _f "source" Source)
  (Json|SetField _f "phase" (V CurPhase))
  (CallFunction|Send :Event "unsupported" :Fields _f))
```

- **The two `if`s without `return` come first** (T30). Every later `if` returns.
- The form of each node is in T68's sheet (`Send`: `Json|LoadJsonfromString "{}"`, `Json|SetField`) or in a pushed source (`ParseIntoArray`, `Math|Integer|Min(Integer)` and `JoinStringArray` in `BPC_LLMClient/FreeReply.txt`; `GetSubstring` in `ParseReply.txt`; `Contains` in `HandleHttp.txt`; `FindItem` in `HandleHttp.txt`).
- **`CurPhase` before the first phase** is `""` (T68's default); an attempt that early (none can be: the input ask first runs in scene 1's turn 1) would go out with an empty `phase`, which the relay allows.
- The dedupe runs whether or not analytics is on, so an off run prints nothing and costs one array.
- Compile order: this function, then T69's client graphs (part 3), then the widget (part 5b). `BPC_Analytics` and the client already reference each other (T68 part 2c).

## 6. The design doc (step 4): waiting for my person's OK in T69

**Proposed, not made.** Read the Bot Prompts tab again on the day. At rev 82 (2026-11-15) the tab has no input prompt yet: **T63 adds an "Input LLM prompt" section** (a heading, one paragraph and a `text` code block with T63's `input` lines word for word, after "Shared base prompt" and before "Persona prompts"; T63-build part 1a, my person's answer 1 there). T69 adds to that section. Show my person this text with the multiple-choice tool ("Make this Bot Prompts edit (Recommended)" / "Change the wording" / "No doc edit"), and edit with the Claude Docs connector only after the OK:

- **The section's paragraph:** after its last sentence (T63's `... the player builds every action by clicking.`), add: `Its reply also names, in a few words, any physical action the typed line describes that the player can’t click, such as a backflip. The game only counts those words for its play stats and never uses them in play.`
- **The code block:** add part 1a's new line at the end, as one line, each `\"` written as a plain `"`:

  `- "attempt": the player can click only five actions: move to a place, look, and grab, throw or give a prop. If typed describes or asks for any other physical action, such as "*does a backflip*" or "I climb the chandelier", name it in "attempt" in at most 6 lowercase words ("backflip", "climb the chandelier"). Write "someone" for any actor and never write a name. Otherwise "attempt" is "": for plain speech, for a pass, and for the five clickable actions. "attempt" never changes speech.`

  The block and `prompts.json`'s `input` must match word for word.
- **If T63 made no such section** (my person changed answer 1), add only the paragraph sentence above, as a new paragraph at the end of the "Shared base prompt" section, and say so under "Findings".
- **Checked and left:** Turn Input (the spelling-only rule and "Typing 'I throw the rose' only says those words" stay true: `attempt` never makes an action), Rules, Tech & Build (says nothing about analytics; T68 leaves it too). The doc's "Changes from the original prompts" list needs nothing.

## 7. The checks (Done-when)

### 7a. `--offline` (free)

`python Tools/check_prompts.py --offline`: `Files OK: ...`, and the job count is T63's plus 3 (the three new input cases). Then the three broken-on-purpose runs from 4i, each one clear line, and back.

### 7b. `--relay --free` (free, no deploy)

`python Tools/check_prompts.py --relay --free`: every ask passes. The relay's free input reply has no `attempt`, which `shape_fails` accepts; a filled one would fail. No relay deploy: T69 changes nothing the relay reads (`free_mode.json`, `relay.config.json`) or runs, and the relay passes the new schema through.

### 7c. The paid input run (after my person's OK; about 3 cents)

Ask with the multiple-choice tool: "Run the 16 input cases on Anthropic (about 3 cents) (Recommended)" or "Not now". Cost: T63 put its 13 input cases at about 2 cents on Anthropic's `claude-haiku-5-5` (`roles.input`); three more cases with a slightly bigger schema make about 3 cents. The checker's summary prints the real figure; write it under "Findings".

In the repo folder (a worktree has no `Local/`): `python Tools/check_prompts.py --ask input`. If `Local/llm_key.json` has no Anthropic key, `python Tools/check_prompts.py --relay --ask input` (relay credit, the same cost). Expect 16 of 16, and in particular (the Done-when): `attempt` filled for `*does a backflip* hello` (such as `"backflip"` or `"does a backflip"`) and `""` for `hello there`. **The name case** (`i climb onto @OpenAI's shoulders`) should give something like `"climb onto someone's shoulders"`; a "player 1" or "@" there fails the check and means the prompt needs a word, not the check. A case that fails on wording alone: run it again with `--repeat 3`; a steady failure gets a prompt fix (and the same fix in the doc after my person's OK). The first call after the schema change may take a second longer (decision 1); that doesn't fail the checker.

### 7d. PIE (Test for Free, autoplay off, 1600 × 900, `"analytics": "test"`)

`Local/switches.json` in the repo folder: `"mode": "free"`, `"autoplay": false`, `"spare_human": true`, `"analytics": "test"`, `"attempt_test": "backflip"`. Start PIE in a 1600 × 900 floating window, pick **Test for Free**. Expect `NHOS: CLIENT ready ... attempt_test=backflip` and T68's `NHOS: ANALYTICS player <id> test=true ...`.

1. **Typed (step 2).** At scene 1, turn 1, type `*does a backflip* hello` and send (Action! with No action). Look for, in order: `NHOS: LLM spell-<n> ok`, `NHOS: ATTEMPT spell-<n> backflip`, `NHOS: ANALYTICS unsupported {"words":"backflip","source":"typed","phase":"turn_1"}` (key order as `GetJsonString` writes it), later `NHOS: ANALYTICS ok unsupported`; T63's `NHOS: HUMAN none - - says=*does a backflip* hello` (the line unchanged: free mode echoes it). At turn 2, type any line: with `attempt_test` still set, a second `unsupported` goes out with `"phase":"turn_2"` (a new phase). I send one typed line per phase, so the once-per-phase rule for typed words can't show in play; call `Unsupported("backflip", "typed")` twice through MCP during one phase instead and see one `NHOS: ANALYTICS unsupported` line.
2. **Free mode leaves it empty.** Set `"attempt_test": ""`, restart the show (the client reads switches at load: stop and start PIE). Type a stage direction: no `NHOS: ATTEMPT`, no `unsupported`.
3. **The builder (step 3, if 5a passed).** At turn 1, Throw is greyed (nothing held). Click Throw twice with a real click. Look for one `NHOS: BUILDER greyed click throw` and one `NHOS: ANALYTICS unsupported {"words":"throw, holding nothing","source":"builder","phase":"turn_1"}`; the second click prints nothing. Click Look around (open): `NHOS: BUILDER pick around ...` (T64) and no `unsupported`. Screenshot: `Saved/T69/shots/greyed-throw.png`.
4. **Analytics off.** `"analytics": "off"`, restart PIE, repeat 1 with `attempt_test` set: `NHOS: ATTEMPT` prints, `NHOS: ANALYTICS unsupported` doesn't (T68's `Send` drops it; only T68's `NHOS: ANALYTICS off ...` load line shows).
5. **The report.** `python Tools/analytics_report.py --test --since <today>` lists `backflip` (`typed`) and `throw, holding nothing` (`builder`) under "unsupported actions". Without `--test` neither shows.

Then set `analytics` back to `off`, `attempt_test` back to `""`, `spare_human` back to false, and close PIE.

### 7e. A free autoplay show (nothing broke)

Optional, one run: `"autoplay": true`, `"mode": "free"`, `"fast_lines": true`, `"analytics": "off"`, in a game window (`-game -windowed -ResX=1600 -ResY=900`), until `NHOS: SHOW END`: no `LogScript` line, no `NHOS: ATTEMPT` (free mode, `attempt_test` empty), every `NHOS: LLM spell-` ok. Set `autoplay` and `fast_lines` back to false, close the window.

## 8. The commit

One commit, `T69: Analytics, part 3: the actions players try that the game can't do`: `Content/NHOS/Data/prompts.json`, `Content/NHOS/Data/llm.json`, `Tools/check_prompts.py`, `Content/NHOS/Core/BPC_LLMClient.uasset`, `Content/NHOS/UI/WBP_ActionBuilder.uasset` (if step 3 was built); `Graphs/BPC_LLMClient/` (`LoadConfig`, `BuildBody`, `FreeReply`, `Deliver`; new `NoteAttempt`), `Graphs/WBP_ActionBuilder/` (`OpenTurn`; new `BlockWords`, `BlockedClick`, `GreyClickAt`, `OnMouseButtonDown`); `Docs/tasks/T69.md` (Result; Findings with the schema pick from decision 1, the `ParseFields` and `ClearReply` node edits, part 5a's result and the paid run's cost), `Docs/Plan.md` (the box), `Docs/DevLog.md`. **Outside the Touches, named in the message:** `Content/NHOS/Core/BPC_Analytics.uasset` and `Graphs/BPC_Analytics/Unsupported.txt` (decision 3), `Docs/switches.example.json` (decision 6), `Docs/ItchPage.md` (decision 9). Stage by path. Unlock every asset after the push. If my person hasn't given the paid run's OK, follow "When only my check is left": push with a `Waiting:` line under T69 (`Left: my OK for the paid --ask input run (about 3 cents)`).

**`Docs/switches.example.json`:** add `"attempt_test": ""` after `"error_test": ""` (and the comma), and at the end of `_readme`: ` attempt_test (T69): in Test for Free, every input reply carries this text as its attempt field (the few words naming an action the player typed that the game can't do), so the unsupported analytics event can be checked without spending tokens. It is read once when the show loads. Set it back to empty before a person plays.` T68 adds `analytics` to the same file first; keep both.

**`Docs/ItchPage.md`:** in T68's "Play stats" bullet (its part 9c), after `and the kind of any error.` add ` If you try an action the game can't do yet, it sends a few words naming it (like "backflip"), never your typed line.` If T68's wording changed, add the same sentence after its list of what is sent.

## 9. The task's steps and checks, and where this sheet covers them

| `T69.md` | Here |
|---|---|
| Step 1, the field in the input ask's reply (name, 6 words, `""` for speech, never changes the line or turn) | Part 1a, 1b, 1c; decisions 4, 5 |
| Step 1, shared schema or its own: token cost and the four providers' strict rules, written under Findings | Decision 1; part 2 |
| Step 1, the checker checks the field; free mode leaves it empty | Part 4; 3c (free mode, the relay's free reply) |
| Step 2, send `unsupported` with `words` (cut to 6), `source` `typed`, `phase`; never the typed line | Parts 3c, 3d, 5d; "What a row holds" |
| Step 3, blocked clicks in `WBP_ActionBuilder`, once per verb per turn, or say why not | Parts 5a to 5c; decision 8 |
| Step 4, the Bot Prompts edit, after my OK | Part 6 |
| Done-when: `--offline`; the paid `--ask input` with the two cases | 7a, 7c |
| Done-when: PIE prints `NHOS: ANALYTICS unsupported` for a typed stage direction (faked reply) and once for Throw with nothing held | 7d (1, 3); decision 6 |
| Done-when: `analytics_report.py --test` lists the words | 7d (5) |
| Done-when: `analytics` back to `off` | 7d, last line |

## 10. Knock-on: tell, don't change

- **The two machines.** T69 no longer touches `BP_Show` or `WBP_Stage` (decision 2), so by the split in `CLAUDE.md` it is not a chain task: it can run on either machine once T63, T64 and T68 are pushed. T69's plan entry still names `BP_Show.uasset` in its Touches ("or `BPC_LLMClient`"), and T77's entry says it depends on T69 for "the lock on `BP_Show`". Tell my person; the plan changes only on their word.
- **T76 (the emotion field):** add `emotion` to **both** `reply_schema` and `input_schema` (T77 needs it in the input reply too); part 4c's check fails if only one has it. `request_body` and `BuildBody` already pick the schema by role.
- **T77 (my emotion from the input LLM):** the input reply's `ParseFields` read and `ClearReply` now hold `RAttempt`; T77's `RMood` (or whatever it names it) goes next to it. T77's `FreeReply` change sits next to T69's `attempt_test` line in the echo branch.
- **T70 (the itch page):** the privacy bullet holds T69's sentence (section 8). Test a package with `"analytics": "test"` as T68 says; `attempt_test` must be empty in any `switches.json` that ships (none should ship).
- **Test for Free never reports typed attempts** (free mode makes no LLM call). If my person wants those counted too, a cheap rule in free mode (the words between `*` asterisks) could fill `attempt`, but the task says free mode leaves it empty, so it's left out.
- **`Relay/README.md`** lists what is stored, already including "a few words for an unsupported action" (T67 step 6). Nothing to change.
