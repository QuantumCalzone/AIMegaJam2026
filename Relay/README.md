# Relay

The relay lets a judge play **No Humans On Set** without their own API keys. It is a Cloudflare Worker. It holds our provider keys as Worker secrets, checks each request from the game, forwards the request body unchanged to the provider and returns the provider's reply. It is the server half of T21 in [Docs/MVPPlan.md](../Docs/MVPPlan.md). The game half (calling the relay, the key-entry screen) is still to do.

There are no keys in this folder, and none may ever go in git. Players who enter their own keys call the providers directly. Their keys never go to the relay.

## Files

| File | What it is |
|---|---|
| `src/index.js` | The Worker: the checks, the forwarding and the `Limiter` Durable Object that counts calls. |
| `relay.config.json` | The allow-list: providers, endpoints, auth style, secret names, models, `max_tokens` caps and limits. |
| `wrangler.toml` | The Worker's name, entry point and Durable Object binding. No keys. |
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

**Free mode** costs nothing, for local testing. Add `"free": true` to the request. The relay runs every check (the request shape, the model allow-list, `max_tokens`, the limits) but calls no provider and needs no key. It answers with a canned reply in that provider's exact response shape (a Messages reply or a Chat Completions reply), with `"relay_free": true` at the top and zero usage. The reply text is a valid game reply: `actions` empty, `speech` a short canned line (or, for the input step, the player's `typed` text cut to 25 words), `vote` a random name from the ask's `options` when it has any, `reason` "Free mode reply.", `pass` false. Free calls are counted apart from real ones (`limits.free`), so they never use up the real budget. `GET /health` says `"free_mode": true`. The reply text comes from `Content/NHOS/Data/free_mode.json` (lines, vote reasons and stage actions per phase; the relay bundles it at build time). **In the game,** the title screen's **Test for Free** button (or `"free_mode": true` in `Local/switches.json`, for autoplay runs) sends every ask this way, with no key needed; **Play with LLMs** calls the providers directly with the player's key.

**On failure** the reply is always this shape (which matches Anthropic's error shape, so the existing `type: "error"` check in `BPC_LLMClient` already catches it):

```json
{ "type": "error", "error": { "type": "budget_used_up", "message": "The free AI budget for today is used up. ...", "source": "relay" } }
```

`error.message` is safe to show to the player: it never names a provider or company. `error.detail`, when present, says which check failed, for logs. Provider errors are never passed through, because their text names the provider; the relay sends `provider_error` with `upstream_status` instead.

| `error.type` | When | HTTP status |
|---|---|---|
| `bad_request` | Not JSON, wrong content type, too large, an extra field, a model not on the allow-list, `max_tokens` missing or over the cap, streaming, non-text content (images, tools) | 400 |
| `unknown_provider` | A provider id that isn't in the config | 400 |
| `provider_unavailable` | The provider has no secret set, or no models listed | 503 |
| `session_limit` | This session id has used its calls for the day | 429 |
| `player_limit` | This player's address has used its calls for the day | 429 |
| `budget_used_up` | Everyone together used the day's calls, or this provider used its tokens for the day | 429 |
| `provider_error` | The provider answered with an error or didn't answer | 502 |
| `relay_error` | A bug in the relay | 500 |
| `not_found` | Any other path or method | 404 |

The game can't read HTTP status codes (the `HttpBlueprint` nodes don't give them), so it must branch on `error.type`. The statuses are for curl and logs.

**`GET /health`** returns `{ "ok": true, "providers": ["anthropic"], "budget_left": true }`. `providers` lists the providers that can serve calls right now, so the game knows which personas can take AI seats through the relay. Use it for the pre-show check; it costs no tokens. If it doesn't answer, or `budget_left` is false, show the "AI service unavailable" screen with key entry.

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

These limits are not a spending cap. **Set a hard monthly spending limit at every provider's console too.** That is the real cap if something goes wrong.

To change a limit without editing the config, add a Text var in the dashboard (**Settings > Variables and Secrets**): `SESSION_CALLS`, `IP_DAILY_CALLS`, `DAILY_CALLS` or `DAILY_TOKENS` (one value for every provider). Delete the var to go back to the config value. Locally, pass the same names to `wrangler dev` with `--var NAME:value`.

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
| `anthropic` | `claude-haiku-5-5` | see Findings in `Docs/MVPPlan.md` | `https://api.anthropic.com/v1/messages` | `max_tokens` | JSON through `output_config.format` |
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
6. The address is on the Worker's page, `https://nhos-relay.<account subdomain>.workers.dev`. Put it in `Content/NHOS/Data/llm.json` (T21's game side).

**Every push to the production branch redeploys** (the build watch path is `*`). That is harmless, because the code only changes when `Relay/` does. The build log shows a warning that the local config differs from the dashboard (vars, compatibility date); with `keep_vars = true` the dashboard vars and secrets stay, as the limit tests showed.

`wrangler.toml` has `keep_vars = true`, so vars and secrets set in the dashboard survive every deploy. `.node-version` asks the build for Node 22, which wrangler 4.162 needs.

**Before you submit:** set a hard spending limit at every provider's console, and decide the daily limits for judging week.

**To take it down fast** (for example if the bill climbs): delete a secret in the dashboard, which turns that provider off at once, or delete the Worker. **Logs:** the Worker's **Logs** tab (observability is on).

## Test it

**Free mode, the default: no tokens.** From the repo root (Git Bash, or any shell with curl, bash and Python):

```bash
bash Relay/test/curl-tests.sh https://nhos-relay.<account subdomain>.workers.dev
```

```bash
python Relay/test/game_shape.py https://nhos-relay.<account subdomain>.workers.dev
```

The curl tests check `/health`, one free call per provider in the config, eleven bad request shapes, an unknown provider, that no error text names a provider, the free session limit (151 calls, a few seconds) and that a free vote picks a name from `options`. `game_shape.py` sends a request shaped like the game's to every provider and checks that the reply parses with every schema field.

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

Paste the keys you have into `Relay/.dev.vars` (git ignores it), then start it with low limits and run the tests in a second terminal:

```bash
npm run dev:limits
```

```bash
npm test
```

The local relay is at `http://127.0.0.1:8787`. Local counts are kept in `Relay/.wrangler/` (git ignores it). Delete that folder to reset them.

You can also deploy from your own machine instead of Workers Builds: `npx wrangler login`, then `npx wrangler secret put ANTHROPIC_API_KEY` (it asks for the value), then `npx wrangler deploy`.
