# T69 build sheet: the actions players try that the game can't do

Back to [T69](T69.md). It is a plan, not a record: nothing here was written to the editor, the data files or the checker.

## This version (2026-11-16)

**Written against `noHumansOnSet` at `0adc4bc`**, by a PC prep session without the editor. A Mac prep session wrote the first version on 2026-11-15 against `2e3e5c8`, from the T63, T64 and T68 build sheets, before any of the three was built. They are built now (T63 and T64 done; T68's two lanes pushed, its chain part still running), and T60 changed the same files. Every graph, widget, variable, function, data field and line below was checked against today's sources: `Graphs/`, the data files, `Tools/check_prompts.py`, `Relay/`, the task files and the design doc (Bot Prompts, rev 84).

**What changed in this sheet, and why:**

1. **T60 added `tell` to the one reply shape** (`reply_schema`, required, an enum of "" and the eight `tells.json` ids). So `input_schema` (part 2a) is now `reply_schema` with `tell` *and* `attempt`, the input LLM keeps returning `tell` "" as it does today, and T63's last `input` rule line now reads `- "vote", "reason" and "tell" are always "". ...` (part 1a's anchor). T60's paid run showed all four providers take the full shape under strict mode, so the new schema is safe on all four. Decision 1 now weighs T60's choice too (it put a vote-only field in the shared shape).
2. **`ParseFields` and `ClearReply` now have source files** (T60 rewrote both), so part 3c edits their files instead of making node edits, and part 0's surveys 1 and 2 are gone. `ParseFields` already reads `tell` under `Json|HasField`; `attempt` is read the same way.
3. **The analytics component may be missing.** T68's lane added `Stats` and `HaveStats` to `BPC_LLMClient` (`FindStats`), and every call into `Stats` is guarded by `(if (V HaveStats) ...)`. `NoteAttempt` (part 3d) keeps that guard.
4. **`Class|BPShow|GetAnalytics` doesn't exist** (T68's `WBP_Title` finds the component by class, with `IsValid`). The builder does the same in a new `SendBlocked` (part 5b), so it doesn't depend on how T68's chain names the component.
5. **The builder's hook is now an `OnPreviewMouseButtonDown` override,** with `OnMouseButtonDown` as the fallback (part 5a, new decision 10). T61 found how to make an override through MCP (`add_function_graph` with the engine function's name), so that survey is answered. T64 found that a disabled button shows its tooltip under a real cursor, so a greyed button is on the pointer's widget path. The root's visibility is set in `OpenTurn` on the builder itself (`SelfHitTestInvisible`), not on `BuilderBox` as the first version said.
6. **T64's names are confirmed** (`ActBtns`, `ActVerbs`, `ActOk`, `ActTip`, `Show`, `Armed`, `Sent`, `Live`, `OpenTurn`'s `(set Sent false)`, the six tips in `WhyNot`). Throw and Give stay disabled buttons; T64 needed no `Border` around them for the tooltip. **No chip is ever greyed:** a chip is shown only when it's a valid choice. So step 3's "greyed-out action or chip" means the seven action buttons only.
7. **The plan already took the first version's knock-on:** T69's entry says "Not a chain task (my call, 2026-11-15)", its Touches list no `BP_Show` and now name `BPC_Analytics.uasset` (`Unsupported`), `Docs/switches.example.json` (`attempt_test`) and `Docs/ItchPage.md`. So the "outside the Touches" notes in decisions 3, 6 and 9 and in part 8 are moot, and part 10's first bullet is gone.
8. **The design doc's input prompt is one line behind `prompts.json`** (T60 changed the file, not the doc). Part 6 now also fixes that line, inside the same OK.
9. **Smaller fixes:** the `Docs/ItchPage.md` sentence now uses the words T68's and T70's sheets expect (part 8); `Unsupported` drops words holding "player", as the checker does (decision 5); the paid run costs under 1 cent, not 3 (T63's 13 cases cost $0.0026); `shape_fails` already takes the ask (T62), so part 4g only adds a check; `Unsupported` doesn't call `Init` itself (`Send` does); the commit lists no file as outside the Touches.

**My person's answers already in this sheet:** "Not a chain task" (the plan, 2026-11-15). The first version's other choices were made by the prep session on my person's standing word (prep sessions take their own recommendation on design calls); they are listed under "Decisions made for my person", open to change. This version needs no new decision.

**What T69 must still check again, in the editor or after these land:**

- **T68's chain part** (session `t68-show-calls`, running now on the PC): it adds `BPC_Analytics` to `BP_Show` as the `Analytics` component and its calls (`CueHeader`, `RunCue`'s `"stat"` branch, `OpenPrep`, `DrawCast`, `ShowTitle`), finishes the checker (`build`) and writes what T69 gets into `T68.md`. Check that `CurPhase` follows the phases on screen (`SendPhase`, from `RunCue`'s `"stat"` branch), that the load log no longer prints `NHOS: CLIENT no analytics component`, and that `check_prompts.py`'s anchors in part 4 still hold.
- **T65** (running now on the Mac, its sheet `T65-build.md` part 6b): it rewrites `WBP_ActionBuilder`'s `Refresh` (last line), `SetLine`, `StyleAll` and `EventGraph` and swaps `PreviewText` for `PreviewWrap`. T69 touches none of those, but it locks `WBP_ActionBuilder` only after T65 has pushed and unlocked it, and starts from T65's files. T65 also adds an `OnPreviewKeyDown` override to `WBP_Stage`: read its Findings on overrides before part 5a.
- **T66** (the timer, before T69 in the chain): it adds `timers` to `input.json` and checks to `check_prompts.py`, and calls `HandleSend` from a timeout. Re-find part 4's anchors after it.
- **In the editor:** the variable type of `ReplySchema` (part 0, survey 1), the node names of part 5 (survey 2), and part 5a's click test, which decides whether step 3 is built.

**Sources read for this version:** `T69.md` and its plan entry; `T63.md`, `T64.md`, `T68.md`, `T60.md`, `T61.md` (the override rule), `T65-build.md` (parts 0, 5 and 6b), `T66-build.md` (its knock-on), the T76, T77 and T70 build sheets (where they quote this one); `Graphs/BP_Show/` (`SpellAsk`, `SpellIn`, `SpellSkip`, `InputState`, `HandleReply`), `Graphs/BPC_LLMClient/` (`LoadConfig`, `BuildBody`, `ParseFields`, `ClearReply`, `Deliver`, `CountCall`, `FindStats`, `FreeReply`, `FlushLocal`, `FlushOne`, `HandleHttp`), `Graphs/BPC_Analytics/` (`Send`, `Init`, `IsOn`, `Error`, `CuePhase`, `PhaseKey`, `SendPhase`, `OnSent`), `Graphs/WBP_ActionBuilder/` (`EventGraph`, `OpenTurn`, `ReadOk`, `WhyNot`, `Refresh`, `FillLists`, `PickVerb`, `IsOn`, `SetLive`), `Graphs/WBP_Title/` (`ShowStats`), `Graphs/WBP_HowToPlay/OnKeyDown.txt`, `Graphs/WBP_SpeechBubble/Place.txt` (geometry nodes); `llm.json`, `prompts.json`, `input.json`, `free_mode.json`; `Tools/check_prompts.py`, `Tools/analytics_report.py`; `Relay/src/index.js` (`checkEvent`, `freeReplyObject`), `Relay/relay.config.json`; `Docs/switches.example.json`, `Docs/ItchPage.md`; `git lfs locks`. **The design doc**, read and not changed: Bot Prompts rev 84.

## In short

- **The reply field is `attempt`** (step 1): at most 6 lowercase words naming a physical action the typed line describes or asks for that the player can't click ("backflip", "climb the chandelier"), `""` for plain speech, a pass or one of the five clickable actions. Never a name: any actor is "someone". It never changes the line or the turn.
- **The input ask gets its own schema** (decision 1): a new `input_schema` in `llm.json`, `reply_schema`'s shape (with T60's `tell`) plus `attempt`. The actors' `reply_schema` doesn't change, so no actor prompt changes and the AIs never see the field. Only the input ask's provider (Anthropic, `roles.input`) reads it; the schema stays valid under all four providers' strict rules in case that role moves.
- **No `BP_Show` change** (decision 2). The reply is read where it arrives, in `BPC_LLMClient`: `ParseFields` reads `attempt` into a new `RAttempt`, and `Deliver` hands a filled one from a `spell-` ask to a new `NoteAttempt`, which calls a new `BPC_Analytics.Unsupported(Words, Source)` with `source` `typed` when `HaveStats` is true. T69 locks `BPC_LLMClient`, `BPC_Analytics` and `WBP_ActionBuilder`, not `BP_Show` or `WBP_Stage`.
- **`BPC_Analytics.Unsupported`** (new, decision 3): lower case, cut to 6 words and 80 characters, dropped if it holds "@" or "player", sent at most once per phase for the same words and source, with `phase` = `CurPhase`. T68's `Send` then decides whether anything goes out: builds only, the switch, autoplay, Play stats.
- **The builder's blocked clicks** (step 3): T64's greyed buttons are disabled, so they fire no click. A new **`OnPreviewMouseButtonDown` override on `WBP_ActionBuilder`** sees every mouse-down inside the builder before any button does, hit-tests the greyed buttons under the pointer and sends `unsupported` with `source` `builder` and words like `throw, holding nothing`, at most once per verb per turn. It returns Unhandled, so every click works as before. **It must be tried first (part 5a);** if no mouse event reaches the widget, step 3 is left out, as the task allows.
- **Free mode leaves `attempt` empty**: the game's free echo and the relay's free reply never set it, and a missing field reads as `""`. For the PIE check, a new switch **`attempt_test`** (decision 6) gives every free input reply that attempt, the way `error_test` fakes failures.
- **Prompts:** one new rule line at the end of `input`, a sentence in `asks.input`, one in `_readme` (part 1). **Checker:** `input_schema` kept in step with `reply_schema`, the input ask's body uses it, `attempt` checked in every input reply, three new cases and one changed (part 4).
- **Checks:** `--offline` and `--relay --free` cost nothing; the one paid `--ask input` run is 16 cases on Anthropic's Haiku, **under 1 cent** (part 7).
- **No `Relay/` change and no deploy:** the relay takes `unsupported` already (`words` 80, `source` 10, `phase` 40), and its free reply needs no `attempt`.

## Decisions made for my person

My person asked prep sessions to take their own recommendation on design calls. Each is open to change. The T69 session shows this list to my person when it closes the task.

1. **The input ask gets its own schema (`input_schema`), not a field in the shared `reply_schema`.** The task asks T69 to weigh the two and write the pick under "Findings"; this is the pick and why:
   - **Strict-schema rules, all four providers.** OpenAI's strict mode (and the two OpenAI-shaped providers, xAI and Meta, which `llm.json` sends with `strict: true`) wants every property in `required` and `additionalProperties: false`; Anthropic's structured outputs take the same schema. So a new field must be required wherever it is, and every reply under that schema must carry it. A shared field means every actor reply on all four providers returns `"attempt": ""`; its own schema means only the input reply does. T60's paid run showed all four take the full shape, `tell`'s enum included, so a plain `attempt` string adds no risk to either schema.
   - **Tokens.** About 135 actor calls a show (`CALLS_PER_SHOW`) would each write about 5 more output tokens (`,"attempt":""`), and each request carries the bigger schema. Small in money, but spent on a field the actors must never fill.
   - **Behaviour.** A field named `attempt` in the actors' schema invites them to write stage directions into it, and the actors' prompts would need a line telling them to leave it empty (`game` or `base`, outside T69's Touches, and a Bot Prompts edit of the opening or base prompt). With its own schema, no actor prompt changes.
   - **T60's `tell` went the other way, for a reason that doesn't hold here.** `tell` is filled by actors (the vote), so it had to be in their schema; the input LLM returns it "" because the shape is shared, and T63's `input` rule line says so. `attempt` is filled only by the input LLM. `input_schema` keeps `tell` so that it stays exactly `reply_schema` plus one field: one rule for the checker (part 4c) and for T76.
   - **The cost of its own schema:** one new key in `llm.json`, two small edits in `BPC_LLMClient` (`LoadConfig` reads it; `BuildBody` picks it for the input role) and one in the checker's `request_body`. A schema change makes Anthropic compile the new grammar once (it caches it after that), so the first input call after the change can be slower; with T63's 4-second `spelling_wait` that line may go as typed once (`NHOS: SPELLING skipped late`), and its `attempt` is still counted (decision 2).
   - **For T76 and T77:** T76 adds `emotion` to `reply_schema`; T77 has the input LLM pick my emotion, so `input_schema` needs it too. The checker's new check (part 4c) fails if the two schemas drift apart, so T76 can't miss it.
2. **The game reads `attempt` in `BPC_LLMClient`, not `BP_Show`.** The client parses every reply (`ParseFields`), and `Deliver` sees each one before `BP_Show` does, so one new function there (`NoteAttempt`) and one call in `Deliver` send it. `BP_Show` and T63's line path (`SpellAsk` → `HandleReply` → `SpellIn`) don't change, and T69 needs no lock on `BP_Show`. A reply that comes after `spelling_wait` (dropped by `BP_Show.HandleReply` as `STALE`) still has its `attempt` counted: the player did type it.
3. **A wrapper, `BPC_Analytics.Unsupported(Words, Source)`.** Two callers (the client and the builder) need the same cleanup, so it lives in one function next to `Send`, in T68's style (`Error(Kind)` is one such wrapper). T69's plan entry names it in the Touches.
4. **The five clickable actions don't count.** "I throw the rose" says those words (T63) and leaves `attempt` `""`, because the builder can do it; the event is for what the game can't do, and the report's heading says so. Players typing clickable actions would be a builder problem for T64's hints, not a missing verb.
5. **The privacy guard is in three places:** the prompt says "someone" for any actor and never a name; `Unsupported` drops any words holding "@" or "player" (a Player name) and prints why; the checker fails an input reply whose `attempt` holds a provider name, "@" or "player". See "What a row holds".
6. **The PIE check fakes the field with a new switch, `attempt_test`** (in `Local/switches.json`, read with `error_test` in `LoadConfig`), not a paid relay turn. In Test for Free every input reply then carries that text as its `attempt`. It adds `"attempt_test": ""` and one sentence to `Docs/switches.example.json` (in the Touches). The other way (one turn in Play via Relay) costs real tokens and needs my person's OK each time.
7. **Every phase counts, not only scene turns.** The input ask runs for scene lines, Free Talk, last words, reactions and vote reasons; a "*does a backflip*" in Free Talk is as telling. `phase` says where.
8. **The builder's words** are the verb and a short reason, mapped from T64's tips (`WhyNot`, as built): Throw or Give with nothing held ("Grab something first.") → `throw, holding nothing` / `give, holding nothing`; Grab with nothing free ("Nothing free to grab.") → `grab, nothing free`; Grab with full hands ("Your hands are full.") → `grab, hands full`; Give when nobody has a free hand ("Nobody has a free hand.") → `give, no free hand`; nothing to pick ("Nothing to pick.") → `<verb>, no target`. "The stage isn't ready." is the game's state, not a player's try, and sends nothing.
9. **The `Docs/ItchPage.md` privacy bullet gets T69's words in T69,** as T68's sheet asks (its parts 12 and 13): the page must say what is sent from the day T69 sends it. The words are the ones T68's and T70's sheets expect (part 8).
10. **(New in this version.) The builder catches the click in `OnPreviewMouseButtonDown`, with `OnMouseButtonDown` as the fallback.** The preview event tunnels from the root down before any child sees the click, so it doesn't depend on whether a disabled button passes its mouse-down on to its parents; it only needs the builder on the pointer's widget path, which a greyed button's tooltip shows it is. And the builder finds `BPC_Analytics` on `BP_Show` by class, as `WBP_Title.ShowStats` does, so it doesn't depend on T68 making the component readable as a variable.

## What a row of this event holds (privacy)

T67 step 6 lists what may be stored: "an anonymous player id, the mode, the phases, call counts and tokens, error kinds and a few words for an unsupported action. Never typed text, keys or the address." T68's itch-page bullet says the same to players, with the Play stats switch as the opt-out. One `unsupported` row, as `BPC_Analytics.Send` builds it and the relay stores it:

```json
{"player": "3f9c0d2e…(32 hex)", "session": "8b1e…", "build": "2026-11-15", "mode": "relay",
 "event": "unsupported", "fields": {"words": "backflip", "source": "typed", "phase": "turn_2"}, "test": false}
```

plus what the relay adds: the UTC time and the day-salted hash of the address (`hashIp`), never the address.

- **`words`:** at most 6 lowercase words and 80 characters (the relay's cap), written by the input LLM from the typed line (`typed`) or by the game from the greyed button (`builder`). **Never the typed line itself:** the line goes to the AIs as speech, as before, and never to the relay's store. No names: the prompt asks for "someone", `Unsupported` drops "@" and "player", the checker tests it. A player who types a real person's name into a stage direction is the one gap the game can't see ("hug Taylor"); the prompt's "never write a name" covers it, and the paid run's name case (part 4d) checks that the model follows it.
- **`source`:** `typed` or `builder` (the relay caps it at 10 characters). **`phase`:** T68's phase key, from `BPC_Analytics.PhaseKey` (`turn_2`, `free_talk_1`, `last_word`, `vote`, `reactions`, `closing`, and `scene_prep` from `OpenPrep`). No scene number: the allow-list has no `scene` field for this event, and adding one would change `Relay/`.
- **Who sends:** exactly as every T68 event (`Send` checks `Active`, which `Init` sets): only a packaged build, never the editor unless the `analytics` switch is `test` (then `"test": true`); never with the switch `off`, in autoplay without `test`, or when the player turned Play stats off on the title screen.
- **How many:** at most one per phase for the same words and source, and one per verb per turn for the builder. A player who types a stage direction in every line sends about 20 a show, well inside T67's 500 a day per address.
- **Test for Free never sends a `typed` row:** free mode makes no LLM call, so `attempt` stays empty there (except under `attempt_test`). `builder` rows come from every mode.

## 0. Before you start (after T63, T64, T65, T66 and T68 are pushed)

1. `git log --oneline -20` shows T65, T66 and T68's chain commit (T63 and T64 are in already). `Docs/claims/T65` and `Docs/claims/T68` are released. `git lfs locks` shows no lock on `Content/NHOS/Core/BPC_LLMClient.uasset`, `Content/NHOS/Core/BPC_Analytics.uasset` or `Content/NHOS/UI/WBP_ActionBuilder.uasset` (at `0adc4bc` the Mac's T65 holds `WBP_ActionBuilder` and `WBP_Stage`). Claim T69 and lock all three. **`BP_Show` and `WBP_Stage` need no lock** (decision 2).
2. **Read what changed since this sheet:** the Findings of `T65.md`, `T66.md` and `T68.md` (T68's "What T69 gets", written by its chain part), and `git log --oneline 0adc4bc.. -- Graphs/BPC_LLMClient Graphs/BPC_Analytics Graphs/WBP_ActionBuilder Content/NHOS/Data/llm.json Content/NHOS/Data/prompts.json Tools/check_prompts.py`. In particular:
   - **T68:** `BP_Show` has the `Analytics` component, and `FindStats` finds it (`NHOS: CLIENT no analytics component` is gone from the load log). `BPC_Analytics` still has `Ready`, `Init`, `Send(Event, Fields)`, `CurPhase` and `TmpStr`; `Send` prints `NHOS: ANALYTICS <event> <fields>`; `Deliver` still starts with `CountCall`. If T68 renamed anything, use its names below.
   - **T65:** `WBP_ActionBuilder`'s `OpenTurn` still has `(set Sent false)`; T65's new variables (`Words`, `Toks`, `Tok`, `Found`, `WordUsed`, `TmpK`) don't clash with part 5b's `BlockSent`. If T65's Findings say how its `OnPreviewKeyDown` override was made, make part 5a's override the same way.
   - **T66:** part 4's anchors in `check_prompts.py` (`INPUT_RULES`, the `input.json` block, `INPUT_CASES`, `request_body`, `check_reply`, `shape_fails`).
3. `python Tools/check_prompts.py --offline` passes before you start, so any failure afterward is T69's.
4. **Ask my person for the OK on part 6's doc text** at the start, with the multiple-choice tool. The paid run (part 7c) needs its own OK later.
5. **Survey, one `call_tool` each** (calls stop at about 120 s; save each read to `Saved/T69/<name>.read.txt`; read graphs from their `Graphs/` files, not with `read_graph_dsl`, which marks the Blueprint changed (T64)):
   1. **`ObjectTools.list_properties` on `BPC_LLMClient`:** the type of `ReplySchema` (expected the JSON object type, `JsonObjectWrapper`, like `TmpObj`; `InputSchema` and `BSchema` get the same), and that `RAttempt`, `InputSchema`, `BSchema` and `AttemptTest` don't exist yet.
   2. **Node names** (`find_node_types`, `context_pins: []`), each expected from a pushed source's family: the pointer's position, `Input|PointerEvent|GetScreenSpacePosition` (as `Input|KeyEvent|GetKey` in `WBP_HowToPlay.OnKeyDown`); the hit test, `UserInterface|Geometry|IsUnderLocation` (as `UserInterface|Geometry|GetLocalSize` and `LocaltoViewport` in `WBP_SpeechBubble.Place`); `Widget|GetCachedGeometry` (in `Place`); `Widget|EventReply|Unhandled` (in `OnKeyDown`). Use the names the survey returns.
   3. **The override** (part 5a): T61 made `WBP_HowToPlay.OnKeyDown` with `add_function_graph` named after the engine function, which "makes the override, with its inputs and its `EventReply` result already in place" (`T61.md`). Do the same with `OnPreviewMouseButtonDown` on `WBP_ActionBuilder`, then read its entry's pin names (expected `MyGeometry` and `MouseEvent`) for part 5b's file.

## 1. `prompts.json` (step 1)

As T63 and T60 leave the file. Each line as it sits in the file, two tabs before it, quotes escaped as written.

**a. `input`.** Its last line, as T60 left it, is `		"- \"vote\", \"reason\" and \"tell\" are always \"\". \"pass\" is false unless the free talk rule says otherwise."` with no comma. Give it a comma and add one line after it, so the key ends:

```json
		"- \"vote\", \"reason\" and \"tell\" are always \"\". \"pass\" is false unless the free talk rule says otherwise.",
		"- \"attempt\": the player can click only five actions: move to a place, look, and grab, throw or give a prop. If typed describes or asks for any other physical action, such as \"*does a backflip*\" or \"I climb the chandelier\", name it in \"attempt\" in at most 6 lowercase words (\"backflip\", \"climb the chandelier\"). Write \"someone\" for any actor and never write a name. Otherwise \"attempt\" is \"\": for plain speech, for a pass, and for the five clickable actions. \"attempt\" never changes speech."
	],
```

- **Why one line:** T63's rules are one line each; the field is one rule. Its two halves are what the checker pins (part 4b).
- **It never changes speech:** the stage direction stays in the line as typed, with its spelling fixed (T63's "Keep the player's words, word order, ... punctuation"), so "*does a backflip* hello" is still spoken as "*does a backflip* hello". The task: "the line is still sent as typed and fixed".
- T63's `"typed" is only speech, even when it describes an action` rule stays true: `attempt` isn't an action, `actions` stays `[]`.

**b. `asks.input`.** T63 left `		"input": "Fix the spelling of typed, the line the player's robot (named in actor) says. It is speech only: no actions."` (the last key in `asks`, no comma). Make it:

```json
		"input": "Fix the spelling of typed, the line the player's robot (named in actor) says. It is speech only: no actions. If it describes a physical action the player can't click, name it in attempt."
```

It keeps T63's "no actions" (the checker requires it) and stays the last key in `asks`, with no comma.

**c. `_readme`.** In the string (index 2, the "User message" line) that ends with T63's sentence ` Since T63 it only fixes the spelling of typed (and turns names into Player names): its speech becomes the player's line, and its actions are ignored.`, add right after it:

` Since T69 its reply (llm.json input_schema) also has attempt: at most 6 words naming a physical action typed describes that the player can't click, or \"\". The game only counts them (BPC_LLMClient.NoteAttempt sends an unsupported analytics event) and never uses them in play.`

(T77's sheet finds its own edit by this sentence; keep its words.)

**d. Nothing else** in `prompts.json` changes: `game`, `base` and the actors' asks never see `attempt`.

## 2. `llm.json` (decision 1)

**a. `input_schema`** (new), right after the `reply_schema` block's closing `},`, same indent. `reply_schema`'s shape as T60 left it, plus `attempt` last:

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
			"tell": {
				"type": "string",
				"enum": ["", "late_copy", "note", "silence", "polish", "human_slip", "no_persona", "role", "other"]
			},
			"attempt": {
				"type": "string"
			}
		},
		"required": ["actions", "speech", "vote", "reason", "pass", "tell", "attempt"],
		"additionalProperties": false
	},
```

- **Copy `reply_schema`'s blocks as they are on the day,** in the file's own layout (`reply_schema` writes each enum one item per line); only `attempt` is new. The checker (part 4c) compares the property objects, so `tell`'s enum must match `reply_schema`'s exactly, order included.
- **Why the whole reply shape, not just `speech`, `pass` and `attempt`:** `ParseFields` reads `actions`, `vote`, `reason` and `tell` too, and the checker's shape check wants them; a smaller schema would need edits to both for no gain (the input LLM already returns them empty: T63's rule line).
- **No `maxLength` on `attempt`:** strict mode on the OpenAI-shaped providers refuses some string keywords, and the schema must stay valid if `roles.input.provider` ever moves there. `Unsupported` cuts to 6 words and 80 characters.

**b. `_readme`** (the top-level one). Find `reply_schema is the one reply shape for every ask (scene turn, Free Talk line, vote, reaction, closing line, input conversion); unused fields come back empty.` and make it:

`reply_schema is the reply shape for every actor ask (scene turn, Free Talk line, vote, reaction, closing line); input_schema is the same shape plus attempt, for the input ask alone (T69: a few words naming an action the player typed that the game can't do, for analytics); unused fields come back empty.`

T60's next sentence (`A vote also fills 'tell' ... Every other ask leaves it "".`) stays as it is; the input ask leaves `tell` "" too. The same paragraph's `and uses at most 2 actions` is stale (T62, T63's finding); T76's sheet fixes it (its decision 10) if T69 doesn't, so leave it unless my person asks.

**c. The body shapes.** In the top-level `_readme`, `output_config {effort, format {type: json_schema, schema: reply_schema}}` → `output_config {effort, format {type: json_schema, schema: reply_schema (input_schema for the input ask)}}`. In `providers._readme`, the same Anthropic phrase → the same words, and `json_schema {name: reply, schema: reply_schema, strict: true}` → `json_schema {name: reply, schema: reply_schema (input_schema for the input ask), strict: true}`.

## 3. `BPC_LLMClient`

### 3a. Graphs and files

Every graph T69 changes here has a source file now (T60 wrote `ParseFields` and `ClearReply`; T68's lane wrote `LoadConfig`, `Deliver` and the rest). Edit each file and write it with `write_graph_dsl`.

| Graph | T69 | Part |
|---|---|---|
| `LoadConfig` | reads `input_schema` and `attempt_test` | 3b |
| `BuildBody` | the schema by role | 3b |
| `ParseFields` | reads `attempt` | 3c |
| `ClearReply` | clears `RAttempt` | 3c |
| `FreeReply` | `attempt_test` in the echo branch | 3c |
| `NoteAttempt` | new: the event | 3d |
| `Deliver` | one call | 3d |

**New variables:** `InputSchema`, `BSchema` (the type of `ReplySchema`, survey 1), `RAttempt`, `AttemptTest` (String, ""). Order (T18, T54, T63: a call node goes stale when its function gets a new parameter): first `BPC_Analytics.Unsupported` (part 5d) with its inputs and body, compile `BPC_Analytics`; then the client's variables and `NoteAttempt` with its `Tag` input, compile; then the graphs, callee first (`NoteAttempt`, then `Deliver`). Compile with warnings as errors and save after each group.

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

- These are `if`s without `return`, the form `LoadConfig` already uses for `relay` (`_hr`) and for each switch. If a read-back shows the new lines landing in a then branch, T30's rule applies: move them before the first `if` that returns.

**`BuildBody.txt`.** Right after `  (set TokCap _mt)` (before the `(if (not (streq Role "actor"))` block):

```lisp
  (set BSchema (V ReplySchema))
  (if (streq Role "input")
    (set BSchema (V InputSchema)))
```

and replace both `(V ReplySchema)` further down with `(V BSchema)`: `(Json|SetField _js "schema" (V ReplySchema))` (the `openai_chat` branch) and `(Json|SetField _fm "schema" (V ReplySchema))` (the Anthropic branch). Add a top comment line (the file has none): `; T69: the input ask uses input_schema (reply_schema plus attempt); every actor ask keeps reply_schema.`

- The relay checks the body's keys (`body_keys`), not the schema inside `output_config` or `response_format`, so it takes the new schema as it is (the 64 KB body cap is far off).

### 3c. Reading the field, and free mode

**`ParseFields.txt`.** Right after T60's `tell` read (inside the `else`, after `        (set RTell _te))`), the same form:

```lisp
      (bind _hat (Json|HasField _o "attempt"))
      (if _hat
        (bind _at (Json|GetField _o "attempt"))
        (set RAttempt _at))
```

A missing field leaves `RAttempt` as `ClearReply` set it, `""`. `ParseFields` reads only the fields it names, so an actor reply (no `attempt`) parses as before. Top comment line: `; T69: also 'attempt', the input reply's few words naming an action the player can't click, into RAttempt (only input_schema has it).`

**`ClearReply.txt`.** After `  (set RTell "")`: `  (set RAttempt "")`. Comment line: `; T69: also RAttempt.` `HandleHttp`, `FlushLocal`, `Deliver`'s fail branch and `Ask`'s early fails call it before each reply, so an old `attempt` never rides on the next reply.

**`FreeReply.txt`.** In the `echo_typed` branch, right before its `(return)`, after `    (set RSpeech (Utilities|String|JoinStringArray (V TmpArr2) " "))`:

```lisp
    (set RAttempt (V AttemptTest))
```

Add a top comment line (the file has none): `; T69: free mode leaves attempt empty; the attempt_test switch fills it on every input reply (the echo), for the PIE check.` With the switch empty (always, outside a test), free mode leaves `attempt` empty, as the task says. The input ask reaches `FreeReply` through `FlushLocal` → `FlushOne`, and `error_test` never fails it (`ErrorTestPick` picks an actor ask).

- **The relay's free mode** (`Relay/src/index.js`, `freeReplyObject`) returns `{actions, speech, vote, reason, pass}`, with no `tell` and no `attempt`; `ParseFields` reads a missing field as `""`. So Play via Relay in free mode (the checker's `--relay --free`) also leaves it empty, and `Relay/` doesn't change.

### 3d. Sending it

**`Graphs/BPC_LLMClient/NoteAttempt.txt`** (new):

```lisp
; T69: the input LLM's attempt field: a few words naming a physical action the player typed that the game can't do.
; Deliver calls this for every reply to a spelling ask (spell-<n>, T63's SpellAsk), in time or late. It never changes
; the line or the turn: BP_Show never sees it. BPC_Analytics.Unsupported cleans it and decides whether it goes out;
; HaveStats is false while BP_Show has no analytics component (T68's FindStats).
(fn NoteAttempt (Tag)
  (bind _a (Utilities|String|Trim (V RAttempt)))
  (if (Utilities|String|IsEmpty _a)
    (return))
  (print (cat "NHOS: ATTEMPT " Tag " " _a))
  (if (V HaveStats)
    (Class|BPCAnalytics|Unsupported :self (V Stats) :Words _a :Source "typed")))
```

- `NHOS: ATTEMPT` prints in every run, analytics on or off, so a check can see the field arrive without the relay (part 7d).

**`Deliver.txt`.** As T68's lane left it: `CountCall`, `(set TmpStr2 ...)`, the `(if Ok (print ...) (else (print ...) (CallFunction|ClearReply)))` block, `BackstageNote`, `CallOnAnswer`. Between the `if Ok` block and `  (CallFunction|BackstageNote :Tag Tag :Ok Ok :Error Error)`:

```lisp
  (if (and Ok (Utilities|String|StartsWith :SourceString Tag :InPrefix "spell-"))
    (CallFunction|NoteAttempt :Tag Tag))
```

Top comment line: `; T69: a spelling reply's attempt goes to NoteAttempt (analytics) before BP_Show hears of it.`

- **Before `CallOnAnswer`,** because `BP_Show.HandleReply` → `SpellIn` → `HumanSay` can start the next ask at once, and `RAttempt` must still be this reply's.
- **By tag, not role:** `Deliver` doesn't know the role, and only `SpellAsk` uses `spell-` (`Graphs/BP_Show/SpellAsk.txt`; the line's pending slot is `input-<n>`, which never reaches the input LLM). A failed ask (`Ok` false) is skipped; `ClearReply` has emptied `RAttempt` anyway. `StartsWith` is the form `HandleHttp` uses for `event-` and `keytest-`.
- Neither `if` has a `return`, so both join the next line (T30).

## 4. `Tools/check_prompts.py`

As T63, T60 and T68's chain leave it (re-find every anchor after T66 and T68; the line numbers below are at `0adc4bc`). Find each line by its text.

**a. The docstring.** After T63's "Spelling only (T63)" paragraph (line 142), add:

```
The attempt field (T69): the input ask has its own schema in llm.json,
input_schema, which is reply_schema plus "attempt", so no actor ask carries
it. Every input reply must hold "attempt": at most 6 words naming a physical
action the typed line describes that the player can't click, or "". It never
holds a provider or Player name or an "@". Free mode leaves it empty (the
relay's free reply has no attempt at all, which reads as ""). The file check
keeps input_schema in step with reply_schema and pins the prompt's attempt rule.
```

**b. Constants.** After T63's `INPUT_RULES = [...]` (line 227):

```python
# T69: the input LLM names an action the player can't click in "attempt" (at most 6 words); prompts.json 'input' keeps this rule.
INPUT_ATTEMPT_RULES = ['- "attempt": the player can click only five actions', '"attempt" never changes speech.']
MAX_ATTEMPT_WORDS = 6
```

**c. `check_files`.** In the `# llm.json` block, right after `errors.append("llm.json: reply_schema must require actions, speech, pass, vote, reason and tell")` (line 853):

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

(`want_props` copies T60's `tell` with its enum, so a `tell` change in one schema only fails here too.) And right after T63's `for rule in INPUT_RULES:` loop (line 1077, before its `for old in (...)` loop):

```python
    # T69: the attempt rule.
    for rule in INPUT_ATTEMPT_RULES:
        if not any(rule in line for line in prompts.get("input", [])):
            errors.append(f"prompts.json: 'input' lost a T69 rule: {rule!r}")
    if "attempt" not in prompts.get("asks", {}).get("input", ""):
        errors.append("prompts.json: asks.input must name attempt (T69)")
```

**d. The input cases.** Add three cases at the end of T63's `INPUT_CASES` (after `{"phase": "reaction", "typed": "asdf qwerty zxcv", "speech": "asdf qwerty zxcv"},`, line 1201) and an `attempt` key on one of T63's:

```python
    # T69: the attempt field. True = it must name an action (at most 6 words), False = it must be "".
    {"phase": "scene", "typed": "*does a backflip* hello", "contains": ["backflip", "hello"], "attempt": True},
    {"phase": "scene", "typed": "hello there", "speech": "hello there", "attempt": False},
    # A stage direction about an actor: "someone", never a name.
    {"phase": "free talk", "typed": "i climb onto @OpenAI's shoulders", "contains": ["@Player 1"], "attempt": True},
```

and on T63's `{"phase": "scene", "typed": "I throw the rose at @Anthropic", "speech": "I throw the rose at @Player 2"}`, add `"attempt": False` (a clickable action, decision 4). The first two are the task's Done-when cases. 16 input cases, so the job count grows by 3. T63's two stage-direction cases (`walk to the front and say ...`, `grab teh sword and thorw it at meta ...`) describe clickable actions too, but stay unmarked: T69 adds one clickable case, not three, until the paid run shows how the model treats them. (`build_jobs` turns each `@OpenAI` into `@Player 1` before the state is sent, as for T63's cases.)

**e. `request_body`** (line 1503). The schema by role, in both formats. After the `model, effort, max_tokens = ...` line:

```python
    schema = llm["input_schema"] if role == "input" else llm["reply_schema"]  # T69: only the input ask has attempt
```

and replace both `llm["reply_schema"]` in the two bodies with `schema`. Update the docstring's last sentence: `'input' takes its role's (llm.json _readmes), and input_schema (T69).`

**f. `check_reply`** (line 1634). At the top, T60's types by ask:

```python
    types = {"actions": list, "speech": str, "pass": bool, "vote": str, "reason": str, "tell": str}
    if ask == "input":
        types["attempt"] = str  # T69: input_schema
```

(the `extra = set(reply) - set(types)` check then refuses `attempt` in an actor reply and accepts it in an input reply). In T63's `elif ask == "input":` branch, after its `need(passed == case.get("pass", False), f"pass is {passed}")` line:

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

T60's `tell` block right after the branch (`elif ask == "input": need(not tell, "the input LLM set tell")`) stays as it is.

**g. `shape_fails`** (line 2120) already takes the ask (T62) and lets `tell` be missing (T60); its one caller already passes it (`fails, warns = shape_fails(reply, ask), []`). Add, after T60's `tell` check:

```python
    # T69: an input reply may leave out attempt (the relay's free reply has none), but a free reply never fills it.
    if ask == "input" and reply.get("attempt", "") != "":
        fails.append(f"free mode filled attempt: {reply.get('attempt')!r}")
```

and add to its docstring: `T69: an input reply may leave out 'attempt', but free mode never fills it.`

**h. What doesn't change:** `ALL_ASKS`, `ACTOR_ASKS`, `CALLS_PER_SHOW`, `build_jobs` (it loops over `INPUT_CASES`), `check_log` and its `LOG_RE` (the `NHOS: ATTEMPT` and `NHOS: ANALYTICS` lines aren't AI lines), `Tools/analytics_report.py` (its "unsupported actions" heading already lists `words` and `source`).

**i. Break each new check once on purpose** and see one clear line each, then put it back: remove `attempt` from `input_schema.required`; add `attempt` to `reply_schema`; change one id in `input_schema`'s `tell` enum; drop the rule line from `input`.

## 5. `WBP_ActionBuilder`: the blocked clicks (step 3)

Start from T65's files (it rewrites `Refresh`, `SetLine`, `StyleAll` and `EventGraph`); T69 changes only `OpenTurn` and adds functions.

### 5a. Try it first (decides whether step 3 is built)

T64 greys an action by disabling its button (`Refresh`: `SetIsEnabled` false, with the tip as its tooltip), and a disabled `Button` fires no `OnClicked`. But the button is still on the pointer's widget path: T64's check saw its tooltip under a real cursor. A preview mouse event tunnels from the root down that path before any widget handles it, so an `OnPreviewMouseButtonDown` override on `WBP_ActionBuilder` sees the mouse-down whatever the button does with it. The hit test (part 5b) then tells which greyed button is under the pointer.

1. Make the override (survey 3) with only `(print "NHOS: BUILDER mouse down")` and `(return (Widget|EventReply|Unhandled))`. Compile, save.
2. PIE (Test for Free, autoplay off, 1600 × 900, `spare_human` on): at scene 1, turn 1, Throw and Give are greyed (`NHOS: BUILDER open turn=1 ... greyed=throw,give`). Click Throw **with a real mouse click**, through desktop control on the play window as T64's check did (grant `UnrealEditor.exe`; drag the PIE window clear of other windows first). The Slate inspector's clicks skip the routing.
3. **The log prints `NHOS: BUILDER mouse down`:** build 5b and 5c. **It doesn't** (and a click on an open button doesn't print it either, so the widget sees no mouse at all): in `OpenTurn`, change `(Widget|SetVisibility :self self :InVisibility "SelfHitTestInvisible")` to `"Visible"` and try again (the builder's empty space then takes clicks, which only the panel behind it would have had). Still nothing: make the same test with an `OnMouseButtonDown` override instead. Still nothing: **leave step 3 out**, delete the override, put `OpenTurn` back, and write under "## Findings": "T64's greyed actions are disabled buttons, and the builder gets no mouse event from a click on one; telling those clicks apart needs enabled buttons styled as greyed (a rework of `Refresh`, `StyleAll` and `PickVerb`), so step 3 is left out." The task allows it.
4. Write which override and which visibility worked under "## Findings". If `OpenTurn` had to set `"Visible"`, keep it and say so in `OpenTurn`'s comment.

### 5b. Variables and functions

New variable: `BlockSent` (String array). New functions, in this order (inputs first, compile, then the graphs callee first, T18):

| Function | Inputs | Outputs |
|---|---|---|
| `BlockWords` | `Act`, `Tip` (String) | String |
| `SendBlocked` | `Words` (String) | — |
| `BlockedClick` | `K` (Integer) | — |
| `GreyClickAt` | `Pos` (Vector2D) | — |
| `OnPreviewMouseButtonDown` | the override's own (`MyGeometry`, `MouseEvent`; survey 3) | `EventReply` |

`Graphs/WBP_ActionBuilder/BlockWords.txt`:

```lisp
; T69: the few words a click on a greyed action sends (decision 8): the verb and why it's greyed, from T64's tip (WhyNot).
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

- The tips are `WhyNot.txt`'s as built. **If a later task changes a tip's words, change them here too;** a tip this map doesn't know sends nothing, so a missed one is quiet, not wrong. Part 7d checks the Throw one.

`Graphs/WBP_ActionBuilder/SendBlocked.txt`:

```lisp
; T69: hands a greyed click's words to BP_Show's analytics component (T68's BPC_Analytics), found by class as
; WBP_Title.ShowStats does it. Its own function because IsValid ends the flow in the DSL (T45).
(fn SendBlocked (Words)
  (bind _an (Actor|GetComponentbyClass :self (V Show) :ComponentClass "/Game/NHOS/Core/BPC_Analytics.BPC_Analytics_C"))
  (Utilities|IsValid _an
    (:"Is Valid"
      (Class|BPCAnalytics|Unsupported :self _an :Words Words :Source "builder"))
    (:"Is Not Valid"
      (print "NHOS: BUILDER no analytics component"))))
```

- `Show` is the `BP_Show` actor `OpenTurn` finds at each turn, and `GreyClickAt` runs only while `Armed`, so it is set. If T68's chain made `Analytics` readable from outside and T69 prefers `Class|BPShow|GetAnalytics :self (V Show)`, that works too; the class lookup is the form that's proven today.

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
  (CallFunction|SendBlocked :Words _w))
```

`Graphs/WBP_ActionBuilder/GreyClickAt.txt`:

```lisp
; T69: which greyed action button, if any, is under the pointer (Pos, in absolute/screen space). Only while my turn is
; live and before I send (Refresh's own test): at any other time every button is off, and a click on one says nothing
; about a missing action.
(fn GreyClickAt (Pos)
  (bind _on (and (V Armed) (and (not (V Sent)) (V Live))))
  (if _on
    (for _k (range (len (V ActBtns)))
      (if (not (get (V ActOk) _k))
        (bind _g (Widget|GetCachedGeometry :self (get (V ActBtns) _k)))
        (if (UserInterface|Geometry|IsUnderLocation _g Pos)
          (CallFunction|BlockedClick :K _k))))))
```

`Graphs/WBP_ActionBuilder/OnPreviewMouseButtonDown.txt` (the override, made the way survey 3 found; use its pin names):

```lisp
; T69: every mouse-down inside the builder passes here first (part 5a), a greyed (disabled) action button's too.
; GreyClickAt finds whether it was one. Always Unhandled, so every click works as before.
(fn OnPreviewMouseButtonDown (MyGeometry MouseEvent)
  (bind _pos (Input|PointerEvent|GetScreenSpacePosition MouseEvent))
  (CallFunction|GreyClickAt :Pos _pos)
  (return (Widget|EventReply|Unhandled)))
```

- **No `return` before the loop** in `GreyClickAt` and none in the override until the end, so T30's rule can't bite.
- **Absolute space on both sides:** the pointer's screen-space position and each button's cached geometry. `IsUnderLocation` takes an absolute coordinate. If survey 2 names the nodes differently, use its names.
- **An open button's click** runs `GreyClickAt` too (the preview comes first), but `ActOk` is true for it, so nothing is sent, and the button then handles the click as before (`OnClicked` → `PickVerb`). Clicks on chips, gaps and the preview send nothing either. Only a greyed button under the pointer sends.
- If part 5a fell back to `OnMouseButtonDown`, the file has that name and the same body; an open button then handles its own click and the builder never sees it.

### 5c. `OpenTurn.txt`: one line

After T64's `  (set Sent false)`:

```lisp
  (clear (V BlockSent))
```

and a comment line at the top: `; T69: a new turn clears BlockSent, so each greyed action reports once per turn.`

### 5d. `BPC_Analytics.Unsupported` (new; decision 3)

New variables on `BPC_Analytics`: `UWords`, `UKeep`, `USent` (String arrays), `UPhase` (String, ""). `TmpStr` is T68's. `Graphs/BPC_Analytics/Unsupported.txt`:

```lisp
; T69: an action the player tried that the game can't do (T67's unsupported event). Source "typed" is the input LLM's
; attempt field (BPC_LLMClient.NoteAttempt); "builder" is a click on a greyed action (WBP_ActionBuilder.BlockedClick).
; Only these few words go out, never the typed line: lower case, at most 6 words and 80 characters (the relay's cap),
; and never a name. The same words from the same source go out once per phase (CurPhase, set by SendPhase).
; Send decides whether anything goes out (Active: builds only, the switch, autoplay, Play stats).
(fn Unsupported (Words Source)
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
  (if (or (Utilities|String|Contains :SearchIn (V TmpStr) :Substring "@") (Utilities|String|Contains :SearchIn (V TmpStr) :Substring "player"))
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

- **The one `if` without `return` comes first** (T30). Every later `if` returns.
- **No `Init` call:** `Send` calls it when `Ready` is false, and the dedupe needs only `CurPhase`.
- Every node's form is in a pushed source: `Json|LoadJsonfromString "{}"` and `Json|SetField` with a typed String (`BPC_Analytics/Error.txt`, `SendPhase.txt`; T68: no `select` or literal straight into `SetField`, so `words` goes through `TmpStr`); `ParseIntoArray` with `:CullEmptyStrings`, `Math|Integer|Min(Integer)` and `JoinStringArray` (`BPC_LLMClient/FreeReply.txt`); `GetSubstring` (`BPC_Analytics/OnSent.txt`); `Contains` (`BPC_Analytics/PhaseKey.txt`); `FindItem` (`BPC_LLMClient/CountCall.txt`); `ToLower` (`BPC_Analytics/Init.txt`); `Trim` (`BP_Show/SpellAsk.txt`).
- **`CurPhase` before the first phase** is `""` (T68's default); the input ask first runs in scene 1's turn 1, after `SendPhase` has set `turn_1`, so in practice it is always set. An empty `phase` would still pass the relay.
- The dedupe runs whether or not analytics is on, so an off run prints nothing and costs one array.
- Compile order: this function first (it calls only `Send`), then T69's client graphs (part 3), then the widget (part 5b). `BPC_Analytics` and the client already reference each other (T68).

## 6. The design doc (step 4): waiting for my person's OK in T69

**Proposed, not made.** Read the Bot Prompts tab again on the day. At rev 84 (read 2026-11-16) it has T63's "Input LLM prompt" section: a heading, one paragraph ending `... it never makes an action: the player builds every action by clicking.` and a `text` code block with the `input` lines. **That block is one line behind `prompts.json`:** its last line still reads `- "vote" and "reason" are always "". "pass" is false unless the free talk rule says otherwise.`, while T60 made the file's `- "vote", "reason" and "tell" are always "". ...` and left the doc. Show my person this text with the multiple-choice tool ("Make this Bot Prompts edit (Recommended)" / "Change the wording" / "No doc edit"), and edit with the Claude Docs connector only after the OK:

- **The section's paragraph:** after its last sentence, add: `Its reply also names, in a few words, any physical action the typed line describes that the player can’t click, such as a backflip. The game only counts those words for its play stats and never uses them in play.`
- **The code block:** its last line becomes the file's (`- "vote", "reason" and "tell" are always "". "pass" is false unless the free talk rule says otherwise.`, catching up with T60), then part 1a's new line, as one line, each `\"` written as a plain `"`:

  `- "attempt": the player can click only five actions: move to a place, look, and grab, throw or give a prop. If typed describes or asks for any other physical action, such as "*does a backflip*" or "I climb the chandelier", name it in "attempt" in at most 6 lowercase words ("backflip", "climb the chandelier"). Write "someone" for any actor and never write a name. Otherwise "attempt" is "": for plain speech, for a pass, and for the five clickable actions. "attempt" never changes speech.`

  The block and `prompts.json`'s `input` must then match word for word; compare them line by line after the edit.
- **Checked and left:** Turn Input (the spelling-only rule and "Typing 'I throw the rose' only says those words" stay true: `attempt` never makes an action), Rules, Tech & Build (says nothing about analytics; T68 leaves it too). The doc's "Changes from the original prompts" list needs nothing.

## 7. The checks (Done-when)

### 7a. `--offline` (free)

`python Tools/check_prompts.py --offline`: `Files OK: ...`, and the job count is the day's plus 3 (the three new input cases). Then the broken-on-purpose runs from 4i, each one clear line, and back.

### 7b. `--relay --free` (free, no deploy)

`python Tools/check_prompts.py --relay --free`: every ask passes (T63 had 67 of 67). The relay's free input reply has no `attempt`, which `shape_fails` accepts; a filled one would fail. No relay deploy: T69 changes nothing the relay reads (`free_mode.json`, `relay.config.json`) or runs, and the relay passes the new schema through.

### 7c. The paid input run (after my person's OK; under 1 cent)

Ask with the multiple-choice tool: "Run the 16 input cases on Anthropic (under 1 cent) (Recommended)" or "Not now". Cost: T63's 13 input cases cost $0.0026 on Anthropic's `claude-haiku-5-5` (`roles.input`); three more cases with a slightly bigger schema make about $0.003 to $0.004. The checker's summary prints the real figure; write it under "Findings".

In the repo folder (a worktree has no `Local/`): `python Tools/check_prompts.py --ask input`. If `Local/llm_key.json` has no Anthropic key, `python Tools/check_prompts.py --relay --ask input` (relay credit, the same cost). Expect 16 of 16, and in particular (the Done-when): `attempt` filled for `*does a backflip* hello` (such as `"backflip"` or `"does a backflip"`) and `""` for `hello there`. **The name case** (`i climb onto @OpenAI's shoulders`) should give something like `"climb onto someone's shoulders"`; a "player 1" or "@" there fails the check and means the prompt needs a word, not the check. A case that fails on wording alone: run it again with `--repeat 3`; a steady failure gets a prompt fix (and the same fix in the doc after my person's OK). Note what the model put in `attempt` for T63's two unmarked stage-direction cases. The first call after the schema change may take a second longer (decision 1); that doesn't fail the checker.

### 7d. PIE (Test for Free, autoplay off, 1600 × 900, `"analytics": "test"`)

`Local/switches.json` in the repo folder: `"mode": "free"`, `"autoplay": false`, `"spare_human": true`, `"analytics": "test"`, `"attempt_test": "backflip"`. Set the play window to 1600 × 900 (`LevelEditorPlaySettings`' `newWindowWidth`/`newWindowHeight`, T63's note; put them back after), start PIE floating, pick **Test for Free**. Expect `NHOS: CLIENT ready ... attempt_test=backflip` and T68's `NHOS: ANALYTICS player <id> test=true build=... relay=true packaged=false`.

1. **Typed (step 2).** At scene 1, turn 1, type `*does a backflip* hello` and press Action! with No action. Look for, in order: `NHOS: LLM spell-<n> ok`, `NHOS: ATTEMPT spell-<n> backflip`, `NHOS: ANALYTICS unsupported {"words":"backflip","source":"typed","phase":"turn_1"}` (key order as `GetJsonString` writes it), later `NHOS: ANALYTICS ok unsupported`; T63's `NHOS: HUMAN none - - says=*does a backflip* hello` (the line unchanged: free mode echoes it). At turn 2, type any line: with `attempt_test` still set, a second `unsupported` goes out with `"phase":"turn_2"` (a new phase). I send one typed line per phase, so the once-per-phase rule for typed words can't show in play; call `Unsupported("backflip", "typed")` twice through MCP during one phase instead and see one `NHOS: ANALYTICS unsupported` line.
2. **Free mode leaves it empty.** Set `"attempt_test": ""`, stop and start PIE (the client reads switches at load). Type a stage direction: no `NHOS: ATTEMPT`, no `unsupported`.
3. **The builder (step 3, if 5a passed).** At turn 1, Throw is greyed (nothing held). Click Throw twice with a real click. Look for one `NHOS: BUILDER greyed click throw` and one `NHOS: ANALYTICS unsupported {"words":"throw, holding nothing","source":"builder","phase":"turn_1"}`; the second click prints nothing. Click Look around (open): T64's `NHOS: BUILDER pick around ...` and no `unsupported`. Screenshot: `Saved/T69/shots/greyed-throw.png`.
4. **Analytics off.** `"analytics": "off"`, restart PIE, repeat 1 with `attempt_test` set: `NHOS: ATTEMPT` prints, `NHOS: ANALYTICS unsupported` doesn't (`Send` returns at `Active` false; only T68's `NHOS: ANALYTICS off why=switch ...` load line shows).
5. **The report.** `python Tools/analytics_report.py --test --since <today>` lists `backflip` (`typed`) and `throw, holding nothing` (`builder`) under "unsupported actions". Without `--test` neither shows.

Then set `analytics` back to `off`, `attempt_test` back to `""`, `spare_human` back to false, and close PIE.

### 7e. A free autoplay show (nothing broke)

Optional, one run: `"autoplay": true`, `"mode": "free"`, `"fast_lines": true`, `"analytics": "off"`, in a game window (`-game -windowed -ResX=1600 -ResY=900`), until `NHOS: SHOW END`: no `LogScript` line, no `NHOS: ATTEMPT` (free mode, `attempt_test` empty), every `NHOS: LLM spell-` ok. `python Tools/check_prompts.py --log` passes on that log. Set `autoplay` and `fast_lines` back to false, close the window.

## 8. The commit

One commit, `T69: Analytics, part 3: the actions players try that the game can't do`: `Content/NHOS/Data/prompts.json`, `Content/NHOS/Data/llm.json`, `Tools/check_prompts.py`, `Content/NHOS/Core/BPC_LLMClient.uasset`, `Content/NHOS/Core/BPC_Analytics.uasset`, `Content/NHOS/UI/WBP_ActionBuilder.uasset` (if step 3 was built); `Graphs/BPC_LLMClient/` (`LoadConfig`, `BuildBody`, `ParseFields`, `ClearReply`, `FreeReply`, `Deliver`; new `NoteAttempt`), `Graphs/BPC_Analytics/Unsupported.txt` (new), `Graphs/WBP_ActionBuilder/` (`OpenTurn`; new `BlockWords`, `SendBlocked`, `BlockedClick`, `GreyClickAt`, `OnPreviewMouseButtonDown` or `OnMouseButtonDown`); `Docs/switches.example.json`, `Docs/ItchPage.md`; `Docs/tasks/T69.md` (Result; Findings with the schema pick from decision 1, part 5a's result and the paid run's cost), `Docs/Plan.md` (the box), `Docs/DevLog.md`. Every file is in T69's Touches. Stage by path. Unlock every asset after the push. If my person hasn't given the paid run's OK, follow "When only my check is left": push with a `Waiting:` line under T69 (`Left: my OK for the paid --ask input run (under 1 cent)`).

**`Docs/switches.example.json`:** add `"attempt_test": ""` after `"error_test": ""` (with its comma; `"analytics": "off"` follows), and at the end of `_readme`, after T75's `emote_test` sentence: ` attempt_test (T69): in Test for Free, every input reply carries this text as its attempt field (the few words naming an action the player typed that the game can't do), so the unsupported analytics event can be checked without spending tokens. It is read once when the show loads. Set it back to empty before a person plays.`

**`Docs/ItchPage.md`:** in T68's "Play stats" bullet, `... how many AI calls went to each lab with their token counts, and the kind of any error. Never your typed lines, ...` becomes `... how many AI calls went to each lab with their token counts, the kind of any error, and a few words naming an action you tried that the game can't do yet (never your typed line). Never your typed lines, ...`. These are the words T68's sheet (part 13) and T70's sheet (its "What gets sent where") expect. If T68's chain changed the bullet, add the same clause at the end of its list of what is sent.

## 9. The task's steps and checks, and where this sheet covers them

| `T69.md` | Here |
|---|---|
| Step 1, the field in the input ask's reply (name, 6 words, `""` for speech, never changes the line or turn) | Part 1a, 1b, 1c; decisions 4, 5 |
| Step 1, shared schema or its own: token cost and the four providers' strict rules, written under Findings | Decision 1; part 2 |
| Step 1, the checker checks the field; free mode leaves it empty | Part 4; 3c (free mode, the relay's free reply) |
| Step 2, send `unsupported` with `words` (cut to 6), `source` `typed`, `phase`; never the typed line | Parts 3c, 3d, 5d; "What a row holds" |
| Step 3, blocked clicks in `WBP_ActionBuilder`, once per verb per turn, or say why not | Parts 5a to 5c; decisions 8, 10 |
| Step 4, the Bot Prompts edit, after my OK | Part 6 |
| Done-when: `--offline`; the paid `--ask input` with the two cases | 7a, 7c |
| Done-when: PIE prints `NHOS: ANALYTICS unsupported` for a typed stage direction (faked reply) and once for Throw with nothing held | 7d (1, 3); decision 6 |
| Done-when: `analytics_report.py --test` lists the words | 7d (5) |
| Done-when: `analytics` back to `off` | 7d, last line |

## 10. Knock-on: tell, don't change

- **T76 (the emotion field):** add `emotion` to **both** `reply_schema` and `input_schema` (T77 needs it in the input reply too); part 4c's check fails if only one has it. `request_body` and `BuildBody` already pick the schema by role. T76's sheet says `input_schema` "ends with the same `pass` property, then `attempt`"; since T60 both schemas have `tell` after `pass`, so `emotion` goes after `tell` in `reply_schema` and between `tell` and `attempt` in `input_schema` (the check compares property objects, not their order).
- **T77 (my emotion from the input LLM):** `ParseFields` and `ClearReply` now hold `RAttempt` next to T60's `RTell`; T77's field goes next to them. T77's `FreeReply` change sits next to T69's `attempt_test` line in the echo branch, and its `prompts.json` `_readme` edit finds T69's sentence (part 1c).
- **T70 (the itch page):** the privacy bullet holds T69's clause (part 8), as T70's sheet expects. Test a package with `"analytics": "test"` as T68 says; `attempt_test` must be empty in any `switches.json` that ships (none should ship).
- **T66's suggested `timeout` event** (`T66-build.md`'s knock-on) is not T69's: the relay allows nine events, and a new one needs a relay change and a deploy.
- **Test for Free never reports typed attempts** (free mode makes no LLM call). If my person wants those counted too, a cheap rule in free mode (the words between `*` asterisks) could fill `attempt`, but the task says free mode leaves it empty, so it's left out.
- **`Relay/README.md`** lists what is stored, already including "a few words for an unsupported action" (T67 step 6). Nothing to change.
