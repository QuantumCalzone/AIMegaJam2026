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

**T16 fills in the other providers.** Only Anthropic has a model today. When T16 picks a model for a persona's provider, add the model id to that provider's `models` and check its `endpoint`, `max_tokens_field` and `body_keys` against the provider's docs (the Meta endpoint here is a guess at its Chat Completions URL). Keep `models` in step with the model ids in the game's data files, or the relay will refuse the game's calls.

## Deploy (Workers Builds: nothing to install)

Cloudflare builds and deploys the relay from GitHub on its own machines, so nobody needs Node.js or wrangler on their computer. You need a Cloudflare account (the free Workers plan is enough: it includes Durable Objects with SQLite storage). Each deploy needs the person's OK, because every push to the connected branch deploys.

**Once, in the Cloudflare dashboard:**

1. **Workers & Pages > Create > Import a repository.** Connect GitHub and pick `QuantumCalzone/AIMegaJam2026`.
2. Set:
   - **Project name:** `nhos-relay` (it must match `name` in `wrangler.toml`).
   - **Production branch:** the branch the relay is on (`noHumansOnSet` now, `main` after the merge).
   - **Root directory:** `Relay`
   - **Build command:** empty. **Deploy command:** `npx wrangler deploy` (the default).
   - Under **Build watch paths**, include `Relay/*` only, so pushes that touch only the game don't redeploy.
3. Save and deploy. The first build fails or the relay answers `provider_unavailable` until a key is set; that is fine.
4. **Settings > Variables and Secrets:** add `ANTHROPIC_API_KEY` as a **Secret** (type Secret, not Text) and paste the key there. Do the same for `OPENAI_API_KEY`, `XAI_API_KEY` and `META_API_KEY` when T16 adds those providers. Keys never go in chat, git or a command line.
5. The address is on the Worker's page, something like `https://nhos-relay.<your-subdomain>.workers.dev`. Put it in `Content/NHOS/Data/llm.json` (T21's game side).

`wrangler.toml` has `keep_vars = true`, so vars and secrets set in the dashboard survive every deploy. `.node-version` asks the build for Node 22, which wrangler 4.162 needs.

**Before you submit:** set a hard spending limit at every provider's console, and decide the daily limits for judging week.

**To take it down fast** (for example if the bill climbs): delete a secret in the dashboard, which turns that provider off at once, or delete the Worker. **Logs:** the Worker's **Logs** tab (observability is on).

## Test it

Test a deploy with low limits so the tests can trip them:

1. In **Settings > Variables and Secrets**, add two **Text** vars: `SESSION_CALLS` = `2` and `DAILY_CALLS` = `8`. Saving them makes a new version at once.
2. From the repo, run the tests against the address (Git Bash, or any shell with curl, bash and Python):

   ```bash
   bash Relay/test/curl-tests.sh https://nhos-relay.<your-subdomain>.workers.dev
   ```

3. Delete the two vars, so the limits in `relay.config.json` apply again. The day's count stays (8 calls), which is nothing against 5000.

The tests check `/health`, one tiny call (16 tokens at most) for each provider that has a key, ten bad request shapes, an unknown provider, providers with no key, that no error text names a provider, the session limit and the daily limit. A run makes up to 8 real calls. To run them again on the same UTC day, raise `DAILY_CALLS` above the day's count plus 8 first.

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
