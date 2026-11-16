# Relay

The relay lets a judge play **No Humans On Set** without their own API keys. It is a Cloudflare Worker. It holds our provider keys as Worker secrets, checks each request from the game, forwards the request body unchanged to the provider and returns the provider's reply. It is the server half of T21 in [Docs/Plan.md](../Docs/Plan.md) (details in [Docs/tasks/T21.md](../Docs/tasks/T21.md)). The game half (calling the relay, the key-entry screen) was built in T18.

There are no keys in this folder, and none may ever go in git. Players who enter their own keys call the providers directly. Their keys never go to the relay.

## Files

| File | What it is |
|---|---|
| `src/index.js` | The Worker: the checks, the forwarding, the `Limiter` Durable Object that counts calls, and the `Stats` Durable Object that stores analytics events. |
| `relay.config.json` | The allow-list: providers, endpoints, auth style, secret names, models, `max_tokens` caps, limits, and the analytics events and their fields. |
| `wrangler.toml` | The Worker's name, entry point and Durable Object bindings. No keys. |
| `.dev.vars.example` | The secret names, for running it locally. Copy it to `.dev.vars`. Git ignores `.dev.vars`. |
| `package.json`, `.node-version` | Pin wrangler (4.162.0) and Node 22 for the Cloudflare build. |
| `test/curl-tests.sh` | The curl tests. |

## How the game calls it

**`POST /`** with `content-type: application/json` and this body:

```json
{
	"provider": "anthropic",
	"session": "3f2a9c0e8b7d4e1fa6c5b2d9e0f1a2b3",
	"body": { "model": "claude-haiku-5-5", "max_tokens": 2000, "system": "...", "messages": [ ... ], "output_config": { ... } }
}
```

- `provider` is a provider id from `relay.config.json`. The game keeps the persona-to-provider map in its own data files. These ids never show on screen.
- `session` is 8 to 64 letters, digits, `-` or `_`. Make one per show, for example with the `New Guid` node.
- `body` is exactly the request body the game would send to the provider directly. The relay adds the auth headers (and `anthropic-version` for Anthropic). The game sends no keys and no provider headers.

**On success** the reply is the provider's reply, unchanged, so the game parses it the same way as a direct call.

**Free mode** costs nothing, for local testing. Add `"free": true` to the request. The relay runs every check (the request shape, the model allow-list, `max_tokens`, the limits) but calls no provider and needs no key. It answers with a canned reply in that provider's exact response shape (a Messages reply or a Chat Completions reply), with `"relay_free": true` at the top and zero usage. The reply text is a valid game reply: `actions` empty, `speech` a short canned line (or, for the input step, the player's `typed` text cut to 15 words), `vote` a random name from the ask's `options` when it has any, `reason` "Free mode reply.", `pass` false. Free calls are counted apart from real ones (`limits.free`), so they never use up the real budget. `GET /health` says `"free_mode": true`. The reply text comes from `Content/NHOS/Data/free_mode.json` (lines, vote reasons and stage actions per phase; the relay bundles it at build time). **In the game** (since T18), **Test for Free** no longer calls the relay: `BPC_LLMClient` builds the same kind of reply from `free_mode.json` itself, with no LLM call. **Play via Relay** sends every ask here for real, as `{provider, session, body}` with one session id per show. **Play with my own API keys** calls the providers directly with the player's keys. The relay's free mode stays for `Tools/check_prompts.py --relay --free` and `test/curl-tests.sh`.

The game's own **Test for Free** doesn't use this flag: it builds its replies itself and makes no LLM call. A packaged build still sends analytics events to `/event` in Test for Free, as in every mode, unless the player turns Play stats off or `Local/switches.json` has `"analytics": "off"` (T68).

**On failure** the reply is always this shape (which matches Anthropic's error shape, so the existing `type: "error"` check in `BPC_LLMClient` already catches it):

```json
{ "type": "error", "error": { "type": "budget_used_up", "message": "The free AI budget for today is used up. ...", "source": "relay" } }
```

`error.message` is safe to show to the player: it never names a provider or company. `error.detail`, when present, says which check failed, for logs. Provider errors are never passed through, because their text names the provider; the relay sends `provider_error` with `upstream_status` instead.

| `error.type` | When | HTTP status |
|---|---|---|
| `bad_request` | Not JSON, wrong content type, too large, an extra field, a model not on the allow-list, `max_tokens` missing or over the cap, streaming, non-text content (images, tools); for `/event`, an event or field not on its allow-list | 400 |
| `unknown_provider` | A provider id that isn't in the config | 400 |
| `provider_unavailable` | The provider has no secret set, or no models listed | 503 |
| `session_limit` | This session id has used its calls for the day | 429 |
| `player_limit` | This player's address has used its calls (or, for `/event`, its events) for the day | 429 |
| `budget_used_up` | Everyone together used the day's calls, or this provider used its tokens for the day | 429 |
| `provider_error` | The provider answered with an error or didn't answer | 502 |
| `relay_error` | A bug in the relay | 500 |
| `not_found` | Any other path or method | 404 |

The game can't read HTTP status codes (the `HttpBlueprint` nodes don't give them), so it must branch on `error.type`. The statuses are for curl and logs.

**`GET /health`** returns `{ "ok": true, "providers": ["anthropic"], "budget_left": true }`. `providers` lists the providers that can serve calls right now, so the game knows which personas can take AI seats through the relay. It costs no tokens. Since T21 the game calls it when the player clicks **Play via Relay**: if it doesn't answer, `budget_left` is false or fewer than 3 providers are listed, the game shows its "AI service unavailable" screen, which offers key entry and Test for Free. In the middle of a show, `session_limit`, `player_limit`, `budget_used_up` and `provider_unavailable` (and a relay that stops answering) bring up the same screen with `error.message`.

## Analytics events (`POST /event`, `GET /stats`)

Since T67 the relay also collects the game's play stats, because it is the one server we run. The relay itself only sees Play via Relay: Test for Free makes no network call to it for asks, and Play with my own API keys calls the providers directly. So the game reports for itself, in every mode (T68 and T69 add the sending).

**`POST /event`** with `content-type: application/json` and this body (2 KB at most):

```json
{
	"player": "9f1c2a7e4b3d4e6fa0b1c2d3e4f5a6b7",
	"session": "3f2a9c0e8b7d4e1fa6c5b2d9e0f1a2b3",
	"build": "2026-11-15",
	"mode": "free",
	"event": "phase",
	"fields": { "phase": "free_talk_1", "scene": 2 },
	"test": false
}
```

- `player`: 32 hex digits, an anonymous id the game makes on its first launch. Stored lower case.
- `session`: 8 to 64 letters, digits, `-` or `_`. The show's session id, or one made at launch for events before a show.
- `build` (up to 20 characters), `mode` (`free`, `relay`, `keys` or `""`), `fields` and `test` (true or false) may be left out.
- `event` and its `fields` must be on the allow-list in `relay.config.json` (`events.allowed`). Each field has a type and a cap (a string's length, a number's range), and every field may be left out. Anything else is a `bad_request` in the usual error shape: an unknown event, an extra field, a wrong type, a number out of range, a string over its cap, a body over 2 KB.

| Event | Fields |
|---|---|
| `launch` | `launches` (1 to 1,000,000), `first_seen` (up to 10 characters, the UTC date) |
| `mode`, `show_start`, `analytics_off` | none |
| `phase` | `phase` (40), `scene` (0 to 99) |
| `show_end` | `result` (20), `reason` (40) |
| `calls` | `provider` (20), `model` (60), `calls`, `failed` (0 to 100,000), `tokens_in`, `tokens_out` (0 to 100,000,000) |
| `error` | `kind` (40) |
| `unsupported` | `words` (80), `source` (10), `phase` (40) |

The answer is `{"ok": true}`. An event never calls a provider and never counts against the call limits. A show's drop-off point is the last `phase` it sent, so there is no quit event (the game can't send anything when its window closes).

**What the game sends (T68).** A show's events are `mode` (when no mode was picked on the title), `show_start`, a `phase` as each phase shows on screen, `calls` and `show_end`. The phases, in show order, are `scene_prep`, `turn_1` to `turn_3`, `free_talk_1` and `free_talk_2`, `last_word` (only when someone was named in Free Talk's final round), `vote` and `reactions` for each scene, then `closing`, each with its `scene`. A show with a `show_start` and no `show_end` stopped at its last `phase`. `calls` events come at each Scene Prep and at the end screen, one per provider and model, so a show that stops mid-scene still has the counts of every scene before it. `launch` uses the session id the game made at launch; every other event uses the show's.

**What is stored:** the UTC time, the anonymous player id, the session id, the build, the mode, the event and its fields (phases, call counts and tokens per provider and model, error kinds, a few words naming an unsupported action), the `test` flag, and the relay's day-salted hash of the address (`hashIp`, the same one the call limits use), which never leaves the store. Never the address, typed text, keys, names or anything from the player's accounts or machine.

**The store** is a SQLite Durable Object, `Stats` (binding `STATS`, migration `v2`), apart from the `Limiter`, which clears itself every UTC day. `Stats` keeps every event until someone deletes it. It fits the free Workers plan: each event writes about two rows (the event and the address's count), against 100,000 rows written a day, and the 5 GB of storage holds millions of events. Why this store and not Workers Analytics Engine is in `Docs/tasks/T67.md`, under "Findings".

**The limit:** `limits.ip_daily_events` (500 a day per address, about 20 shows), apart from the call counts. Events with `"test": true` are counted apart from real ones, so tests never use up a player's allowance. A refused event answers `player_limit`, like a call. Override the limit with the var `IP_DAILY_EVENTS`, the same way as the call limits.

**`GET /stats`** answers the stored events, oldest first, a page at a time: `{"ok": true, "events": [{"id", "ts", "player", "session", "build", "mode", "event", "fields", "test"}], "next": <id or null>}`. Parameters: `since=YYYY-MM-DD`, `test=1` (include test events; they are left out without it), `after=<id>` (the `next` of the page before) and `limit` (1 to 5,000, 2,000 by default). It needs `Authorization: Bearer <STATS_KEY>`. Without the right key, or when the Worker has no `STATS_KEY` of 16 characters or more, it answers `not_found`, like any unknown path.

### The report

`Tools/analytics_report.py` (Python 3.10+, no packages) reads `/stats` and prints the players (and how many came back: `launches` over 1, or seen on two or more days), players and shows per mode, the drop-off (shows that reached each phase, the `show_end` results, and the last phase of shows that never ended), calls per provider and model with failures and tokens, errors by kind, and the most common unsupported actions.

```bash
python Tools/analytics_report.py
```

```bash
python Tools/analytics_report.py --since 2026-11-20 --test
```

`--since` starts at that UTC day. `--test` adds the test events, which are left out otherwise. It reads the key from `Local/stats.json` (an example is in `Docs/stats.example.json`), never from `Local/llm_key.json`, which ships next to the packaged game. The relay address comes from that file's `relay`, or else from `relay` in `Content/NHOS/Data/llm.json`.

**Leaving out our own machines:** list their player ids in `Local/stats.json` under `ignore_players`. The report always leaves those players out and says how many events it left out; the events stay on the relay. The game prints its player id in the log (T68). The game sends events only from packaged builds, never from the Unreal Editor, except test-marked events for checks (T68).

**Setting up the key (once):**

1. `python Tools/analytics_report.py --new-key` writes `Local/stats.json` with a fresh 64-character key. It prints no key.
2. Open `Local/stats.json`, copy `stats_key`, and in the Worker's **Settings > Variables and secrets > Add variable**, name it `STATS_KEY`, tick **Secret**, paste the key and click **Add variable and deploy**.
3. Copy the same `Local/stats.json` to each machine that runs the report. Never commit it or paste the key in chat.

## Limits

All counts are for one UTC day, and a new day clears them. They live in one Durable Object, so they are exact.

| Limit | Config key | Default | Why |
|---|---|---|---|
| Calls per session id | `limits.session_calls` | 150 | A show is about 55 calls, so this is two or three shows. |
| Calls per player address | `limits.ip_daily_calls` | 600 | About 10 shows. Stops one person from making new session ids to use the whole budget. The address is stored only as a hash salted with the day. |
| Calls for everyone | `limits.daily_calls` | 5000 | About 90 shows a day. |
| Tokens per provider | `providers.<id>.daily_tokens` | 8,000,000 | A show is about 300,000 tokens across all seats. Input and output count the same. |
| `max_tokens` per call | `providers.<id>.max_tokens_cap` | 2000 | The game asks for 2000 (`Content/NHOS/Data/llm.json`). |
| Request size | `max_body_bytes` | 64 KB | The largest ask is about 22 KB. |
| Analytics events per player address | `limits.ip_daily_events` | 500 | About 20 shows. Test events are counted apart. See "Analytics events". |
| Event size | `events.max_body_bytes` | 2 KB | An event is a few hundred bytes. |

These limits are not a spending cap. **Set a hard monthly spending limit at every provider's console too.** That is the real cap if something goes wrong.

To change a limit without editing the config, add a Text var in the dashboard (**Settings > Variables and Secrets**): `SESSION_CALLS`, `IP_DAILY_CALLS`, `DAILY_CALLS`, `DAILY_TOKENS` (one value for every provider) or `IP_DAILY_EVENTS`. Delete the var to go back to the config value. Locally, pass the same names to `wrangler dev` with `--var NAME:value`.

## The allow-list (`relay.config.json`)

Each provider entry has:

- `shape`: `anthropic` (the Messages API) or `chat` (the Chat Completions shape).
- `endpoint`: the URL the relay posts to.
- `auth`: `x-api-key` (sends `x-api-key` and `anthropic-version: <api_version>`) or `bearer` (sends `Authorization: Bearer <key>`).
- `secret`: the name of the Worker secret that holds the key.
- `models`: the model ids the game may ask for. Any other model is a `bad_request`. An empty list turns the provider off.
- `max_tokens_field`: `max_tokens` or `max_completion_tokens`, whichever that provider uses. The field is required.
- `max_tokens_cap`, `daily_tokens`: see Limits.
- `body_keys`: the only top-level body fields allowed. `stream` is allowed only as `false`.
- `roles`: the message roles allowed.

### The models (checked against each provider's own docs on 2026-11-14)

Each is the cheapest current model that its provider documents as supporting Structured Outputs (a strict JSON schema) through Chat Completions or the Messages API. T16 may change the picks; keep `models` in step with the model ids in the game's data files, or the relay refuses the game's calls.

| Provider id | Model | Price per 1M tokens (in / out) | Endpoint | Token field | Notes |
|---|---|---|---|---|---|
| `anthropic` | `claude-haiku-5-5` | see the price table in `Docs/tasks/T16.md` | `https://api.anthropic.com/v1/messages` | `max_tokens` | JSON through `output_config.format` |
| `openai` | `gpt-6-luna` | $0.10 / $0.50 | `https://api.openai.com/v1/chat/completions` | `max_completion_tokens` | Reasoning model, default effort `medium`; send `reasoning_effort: "none"` (also `low` … `max`). The token cap includes reasoning tokens. |
| `xai` | `grok-4.3` | $1.25 / $2.50 | `https://api.x.ai/v1/chat/completions` | `max_tokens` (not stated in the docs; the test confirms it) | Reasoning, default effort `low`; values `none`, `low`, `medium`, `high`, `xhigh`. The company now brands itself SpaceXAI; keys come from `console.x.ai`. The console's only cheaper chat model, `grok-build-0.1` ($1.00 / $2.00), rejects `reasoning_effort` (400) and spent 967 reasoning tokens and 8.4 s on a one-line reply ($0.0023, against $0.00036 for `grok-4.3` at `none`), so it costs more in practice. |
| `meta` | `muse-ember-1.0` | $0.10 / $0.50 | `https://api.meta.ai/v1/chat/completions` | `max_completion_tokens` (`max_tokens` is a deprecated alias) | Reasons by default (583 reasoning tokens on a one-line reply); send `reasoning_effort: "minimal"` (63 tokens). `"none"` returns 400. Meta's hosted API is now the "Meta Model API" with Muse models, not Llama (`llama.developer.meta.com` redirects to `dev.meta.ai`). Keys come from `dev.meta.ai`. |

**The relay forces the cheapest effort.** Each provider's `force` fields in `relay.config.json` are set on every request, whatever the game sends: Anthropic `output_config.effort: "low"`, OpenAI and SpaceXAI `reasoning_effort: "none"`, Meta `reasoning_effort: "minimal"`. This is the only change the relay makes to a body.

All three Chat Completions providers take structured output as `response_format: {"type": "json_schema", "json_schema": {"name": "reply", "schema": <reply_schema>, "strict": true}}`. The game's `reply_schema` already meets their strict rules (every property required, `additionalProperties: false`, enums allowed). The reply text is `choices[0].message.content`; `finish_reason` is `stop` or `length`; usage is `prompt_tokens` / `completion_tokens` / `total_tokens`.

`test/game_shape.py` sends one request shaped like the game's (system and user messages, the reply schema, the effort above) to every provider the relay has a key for, and checks that the reply parses with every schema field: `python Relay/test/game_shape.py <relay address>`.

Cloudflare answers 403 to Python's default `Python-urllib` User-Agent, so the script sends its own. curl and an Unreal-style User-Agent get through.

## Deploy (Workers Builds: nothing to install)

Cloudflare builds and deploys the relay from GitHub on its own machines, so nobody needs Node.js or wrangler on their computer. You need a Cloudflare account (the free Workers plan is enough: it includes Durable Objects with SQLite storage). Each deploy needs the person's OK, because every push to the connected branch deploys.

**Status:** deployed on 2026-11-14 as `nhos-relay` in our Cloudflare account, built from `noHumansOnSet`, with all four secrets set. The curl tests passed against it (23 of 23), and `test/game_shape.py` passes for all four providers with the efforts in the table: `anthropic` 1.6 s, `openai` 1.8 s, `xai` 2.2 s, `meta` 2.3 s (one short reply each; times vary from run to run). The address is on the Worker's page in the dashboard.

Since 2026-11-15 (T67) it also takes analytics events (`POST /event`) and keeps them in the `Stats` Durable Object; `STATS_KEY` is set, and the curl tests passed 49 of 49 against it.

**Adding a secret in the dashboard:** use **Add variable and deploy**, not **Save**. Save only makes a new version; the live one keeps the old secrets until you promote the new version under **Deployments > (version) > Promote version**.

**How it was set up (to do it again, for example in another account):**

1. **Workers & Pages > Create > Connect GitHub.** Authorize the "Cloudflare Workers and Pages" GitHub app and install it on **Only select repositories**: `QuantumCalzone/AIMegaJam2026`.
2. Pick the repository, then set:
   - **Project name:** `nhos-relay` (it must match `name` in `wrangler.toml`).
   - **Build command:** empty. **Deploy command:** `npx wrangler deploy` (the default).
   - **Enable Preview builds:** off.
   - **Advanced settings > Path:** `Relay`
3. Click Deploy. The create form has no branch choice, so this first build runs on `main` and fails if `main` has no `Relay/` folder yet. That is fine.
4. **Settings > Builds > Production branch:** pick the branch the relay is on (`noHumansOnSet` now, `main` after the merge) and save. "Retry build" rebuilds the old commit, so start a new build with a push to that branch, or add a **Deploy Hook** for the branch, `curl -X POST` its URL once, and delete the hook.
5. **Settings > Variables and secrets > Add variable:** `ANTHROPIC_API_KEY`, tick **Secret**, paste the key, "Add variable and deploy". Do the same for `OPENAI_API_KEY`, `XAI_API_KEY` and `META_API_KEY` when T16 adds those providers. Keys never go in chat, git or a command line.
6. The address is on the Worker's page, `https://nhos-relay.<account subdomain>.workers.dev`. Put it in `relay` in `Content/NHOS/Data/llm.json`.

**Every push to the production branch redeploys** (the build watch path is `*`). That is harmless, because the code only changes when `Relay/` does. The build log shows a warning that the local config differs from the dashboard (vars, compatibility date); with `keep_vars = true` the dashboard vars and secrets stay, as the limit tests showed.

`wrangler.toml` has `keep_vars = true`, so vars and secrets set in the dashboard survive every deploy. `.node-version` asks the build for Node 22, which wrangler 4.162 needs.

**Before you submit:** set a hard spending limit at every provider's console, and decide the daily limits for judging week. Both were settled on 2026-11-15 (T21): the limits are set at all four providers, and judging keeps the default limits above.

**To take it down fast** (for example if the bill climbs): delete a secret in the dashboard, which turns that provider off at once, or delete the Worker. **Logs:** the Worker's **Logs** tab (observability is on).

## Test it

**Free mode, the default: no tokens.** From the repo root (Git Bash, or any shell with curl, bash and Python):

```bash
bash Relay/test/curl-tests.sh https://nhos-relay.<account subdomain>.workers.dev
```

```bash
python Relay/test/game_shape.py https://nhos-relay.<account subdomain>.workers.dev
```

The curl tests check `/health`, one free call per provider in the config, eleven bad request shapes, an unknown provider, that no error text names a provider, the free session limit (151 calls, a few seconds) and that a free vote picks a name from `options`. Since T67 they also check analytics events, every one with `"test": true`: three good events are taken, fourteen bad shapes are refused with the right reason, `GET /event` is not a route, and `/stats` answers `not_found` without the key or with a wrong one.

- **Reading events back** needs the key: the script reads `Local/stats.json` from the repo, or the file you name with `--stats-config <path>`. It then checks that the good events are stored, that the address hash is never read back, that test events are left out without `test=1`, and that `Tools/analytics_report.py` shows the test event with `--test` and not without. With no key file, those checks are skipped (the summary line counts them).
- **The event limit** is per address per UTC day, so a test that trips it can run only once a day. It runs only with `--events-limit <n>`, where `n` is the relay's `IP_DAILY_EVENTS`. Against the deployed relay: add a Text var `IP_DAILY_EVENTS` = `3` with **Add variable and deploy**, run `bash Relay/test/curl-tests.sh <address> --events-limit 3`, then delete the var. That trips only this address's count of test events for the day. Locally: `npx wrangler dev --var IP_DAILY_EVENTS:5`, then `--events-limit 5`. `game_shape.py` sends a request shaped like the game's to every provider and checks that the reply parses with every schema field.

**Real mode: spends tokens.** Add `--real` to either script. `game_shape.py --real` makes one call per provider that has a key. `curl-tests.sh --real` also trips the real limits, so first lower them:

1. In **Settings > Variables and Secrets**, add two **Text** vars: `SESSION_CALLS` = `2` and `DAILY_CALLS` = `8`, with **Add variable and deploy**.
2. Run `bash Relay/test/curl-tests.sh <address> --real`. It makes up to 8 real calls of at most 16 tokens each.
3. Delete the two vars, so the limits in `relay.config.json` apply again. To run it again on the same UTC day, raise `DAILY_CALLS` above the day's count plus 8 first.

## Run it locally (optional)

Only if you want to test changes before you push. You need Node.js 22 or later.

```bash
cd Relay
npm install
cp .dev.vars.example .dev.vars
```

Paste the keys you have into `Relay/.dev.vars` (git ignores it). For the analytics tests, also add a line `STATS_KEY=` with any local key of 16 characters or more, and put the same key in a stats.json whose `relay` is `http://127.0.0.1:8787` (pass it with `--stats-config`). Then start it with low limits and run the tests in a second terminal:

```bash
npm run dev:limits
```

```bash
npm test
```

The local relay is at `http://127.0.0.1:8787`. Local counts are kept in `Relay/.wrangler/` (git ignores it). Delete that folder to reset them.

You can also deploy from your own machine instead of Workers Builds: `npx wrangler login`, then `npx wrangler secret put ANTHROPIC_API_KEY` (it asks for the value), then `npx wrangler deploy`.
