// No Humans On Set: the relay. Holds the provider keys as Worker secrets, checks
// each request from the game, forwards the body unchanged to the provider and
// returns the provider's reply. The one change it makes to the body is the
// "force" fields in relay.config.json (the cheapest effort). See Relay/README.md.
//
// Request (POST /):  { "provider": "<id>", "session": "<id>", "body": { ... } }
// Reply on success:  the provider's reply, unchanged.
// Reply on failure:  { "type": "error", "error": { "type": <code>, "message": <text the game can show>, "source": "relay" } }
// GET /health:       { "ok": true, "providers": [<ids that can serve calls>], "budget_left": true|false }

import { DurableObject } from "cloudflare:workers";
import CONFIG from "../relay.config.json";

// Text the game may show. No provider or company names here.
const MESSAGES = {
	bad_request: "The game sent a request the AI service can't take.",
	unknown_provider: "The game asked for an AI that the AI service doesn't have.",
	provider_unavailable: "This AI isn't set up on the AI service.",
	session_limit: "This show has used all its free AI calls. Enter your own API keys to keep playing.",
	player_limit: "You have used all of today's free AI calls. Enter your own API keys to keep playing, or come back tomorrow.",
	budget_used_up: "The free AI budget for today is used up. Enter your own API keys to keep playing, or come back tomorrow.",
	provider_error: "The AI didn't answer. Try again in a moment.",
	relay_error: "The AI service had a problem. Try again in a moment.",
	not_found: "The AI service has nothing at this address.",
};

const STATUS = {
	bad_request: 400,
	unknown_provider: 400,
	provider_unavailable: 503,
	session_limit: 429,
	player_limit: 429,
	budget_used_up: 429,
	provider_error: 502,
	relay_error: 500,
	not_found: 404,
};

function json(obj, status = 200) {
	return new Response(JSON.stringify(obj), {
		status,
		headers: { "content-type": "application/json" },
	});
}

// detail is for people reading curl output or logs. It never names a provider.
function fail(code, detail, extra = {}) {
	const error = { type: code, message: MESSAGES[code], source: "relay", ...extra };
	if (detail) error.detail = detail;
	return json({ type: "error", error }, STATUS[code]);
}

function utcDay() {
	return new Date().toISOString().slice(0, 10);
}

function intVar(value, fallback) {
	const n = Number.parseInt(value ?? "", 10);
	return Number.isFinite(n) && n >= 0 ? n : fallback;
}

function limitsFor(env, provider) {
	return {
		session_calls: intVar(env.SESSION_CALLS, CONFIG.limits.session_calls),
		ip_daily_calls: intVar(env.IP_DAILY_CALLS, CONFIG.limits.ip_daily_calls),
		daily_calls: intVar(env.DAILY_CALLS, CONFIG.limits.daily_calls),
		daily_tokens: intVar(env.DAILY_TOKENS, provider ? provider.daily_tokens : 0),
	};
}

function providerReady(env, p) {
	return Boolean(env[p.secret]) && Array.isArray(p.models) && p.models.length > 0;
}

function isObject(v) {
	return v !== null && typeof v === "object" && !Array.isArray(v);
}

// Content is a string, or a list of text parts only (no images, files or tools).
function checkContent(content, where) {
	if (typeof content === "string") return null;
	if (!Array.isArray(content) || content.length === 0) return `${where} must be text`;
	for (const part of content) {
		if (!isObject(part) || part.type !== "text" || typeof part.text !== "string") {
			return `${where} may only hold text parts`;
		}
	}
	return null;
}

// Returns null when the body is the shape the game sends, or a reason when it isn't.
function checkBody(p, body) {
	if (!isObject(body)) return "body must be a JSON object";

	for (const key of Object.keys(body)) {
		if (!p.body_keys.includes(key)) return `body field "${key}" is not allowed`;
	}
	if ("stream" in body && body.stream !== false) return "streaming is not supported";

	if (typeof body.model !== "string" || !p.models.includes(body.model)) {
		return "model is not on the allow-list";
	}

	const mt = body[p.max_tokens_field];
	if (!Number.isInteger(mt) || mt < 1) return `${p.max_tokens_field} must be a whole number of 1 or more`;
	if (mt > p.max_tokens_cap) return `${p.max_tokens_field} is over the cap of ${p.max_tokens_cap}`;

	if (!Array.isArray(body.messages) || body.messages.length === 0 || body.messages.length > 64) {
		return "messages must be a list of 1 to 64 messages";
	}
	for (let i = 0; i < body.messages.length; i++) {
		const m = body.messages[i];
		if (!isObject(m)) return `messages[${i}] must be an object`;
		for (const key of Object.keys(m)) {
			if (key !== "role" && key !== "content") return `messages[${i}] field "${key}" is not allowed`;
		}
		if (!p.roles.includes(m.role)) return `messages[${i}] has a role that is not allowed`;
		const err = checkContent(m.content, `messages[${i}].content`);
		if (err) return err;
	}

	if (p.shape === "anthropic" && "system" in body) {
		const err = checkContent(body.system, "system");
		if (err) return err;
	}
	if ("output_config" in body && !isObject(body.output_config)) return "output_config must be an object";
	if ("response_format" in body && !isObject(body.response_format)) return "response_format must be an object";
	if ("temperature" in body && typeof body.temperature !== "number") return "temperature must be a number";
	if ("reasoning_effort" in body && typeof body.reasoning_effort !== "string") return "reasoning_effort must be text";
	return null;
}

// Set each "force" field from the config (a dotted path, e.g. "output_config.effort"),
// so calls through our keys always run at the cheapest effort, whatever the game sends.
function applyForce(p, body) {
	for (const [path, value] of Object.entries(p.force ?? {})) {
		const keys = path.split(".");
		let o = body;
		for (const k of keys.slice(0, -1)) {
			if (!isObject(o[k])) o[k] = {};
			o = o[k];
		}
		o[keys[keys.length - 1]] = value;
	}
}

function providerHeaders(env, p) {
	const headers = { "content-type": "application/json" };
	if (p.auth === "x-api-key") {
		headers["x-api-key"] = env[p.secret];
		headers["anthropic-version"] = p.api_version;
	} else if (p.auth === "bearer") {
		headers["authorization"] = `Bearer ${env[p.secret]}`;
	}
	return headers;
}

// Tokens a reply used, for the daily token budget. Without usage in the reply,
// count the request's own size and its max_tokens, so a provider can't go uncounted.
function tokensUsed(p, replyText, body, bodyText) {
	try {
		const u = JSON.parse(replyText).usage;
		if (isObject(u)) {
			const n =
				p.shape === "anthropic"
					? (u.input_tokens ?? 0) + (u.output_tokens ?? 0) +
					  (u.cache_creation_input_tokens ?? 0) + (u.cache_read_input_tokens ?? 0)
					: u.total_tokens ?? (u.prompt_tokens ?? 0) + (u.completion_tokens ?? 0);
			if (Number.isFinite(n) && n > 0) return n;
		}
	} catch {
		// Not JSON: fall through to the estimate.
	}
	return Math.ceil(bodyText.length / 4) + body[p.max_tokens_field];
}

async function hashIp(ip, day) {
	const data = new TextEncoder().encode(`${day}|${ip}`);
	const digest = await crypto.subtle.digest("SHA-256", data);
	return [...new Uint8Array(digest).slice(0, 8)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

function limiter(env) {
	return env.LIMITER.get(env.LIMITER.idFromName("global"));
}

async function handleRelay(request, env, ctx) {
	const type = request.headers.get("content-type") ?? "";
	if (!type.toLowerCase().includes("application/json")) {
		return fail("bad_request", "content-type must be application/json");
	}
	const declared = Number(request.headers.get("content-length") ?? 0);
	if (declared > CONFIG.max_body_bytes) return fail("bad_request", "request is too large");

	const text = await request.text();
	if (text.length > CONFIG.max_body_bytes) return fail("bad_request", "request is too large");

	let envelope;
	try {
		envelope = JSON.parse(text);
	} catch {
		return fail("bad_request", "request is not JSON");
	}
	if (!isObject(envelope)) return fail("bad_request", "request must be a JSON object");
	for (const key of Object.keys(envelope)) {
		if (!["provider", "session", "body"].includes(key)) {
			return fail("bad_request", `request field "${key}" is not allowed`);
		}
	}

	const { provider: id, session, body } = envelope;
	if (typeof session !== "string" || !/^[A-Za-z0-9_-]{8,64}$/.test(session)) {
		return fail("bad_request", "session must be 8 to 64 letters, digits, - or _");
	}
	if (typeof id !== "string" || !Object.hasOwn(CONFIG.providers, id)) {
		return fail("unknown_provider");
	}
	const p = CONFIG.providers[id];
	if (!providerReady(env, p)) return fail("provider_unavailable");

	const reason = checkBody(p, body);
	if (reason) return fail("bad_request", reason);

	const day = utcDay();
	const ip = request.headers.get("cf-connecting-ip") ?? "unknown";
	const verdict = await limiter(env).reserve({
		day,
		session,
		provider: id,
		ipHash: await hashIp(ip, day),
		limits: limitsFor(env, p),
	});
	if (!verdict.ok) return fail(verdict.code);

	applyForce(p, body);
	const bodyText = JSON.stringify(body);
	let upstream;
	let replyText;
	try {
		upstream = await fetch(p.endpoint, {
			method: "POST",
			headers: providerHeaders(env, p),
			body: bodyText,
			signal: AbortSignal.timeout(CONFIG.upstream_timeout_ms),
		});
		replyText = await upstream.text();
	} catch (e) {
		console.log(`relay: ${id} fetch failed: ${e}`);
		return fail("provider_error", "no reply", { upstream_status: 0 });
	}

	ctx.waitUntil(
		limiter(env).record({ day, provider: id, tokens: tokensUsed(p, replyText, body, bodyText) }),
	);

	if (!upstream.ok) {
		console.log(`relay: ${id} returned ${upstream.status}: ${replyText.slice(0, 500)}`);
		return fail("provider_error", `upstream status ${upstream.status}`, { upstream_status: upstream.status });
	}
	return new Response(replyText, {
		status: upstream.status,
		headers: { "content-type": upstream.headers.get("content-type") ?? "application/json" },
	});
}

async function handleHealth(env) {
	const providers = Object.entries(CONFIG.providers)
		.filter(([, p]) => providerReady(env, p))
		.map(([id]) => id);
	const status = await limiter(env).status({ day: utcDay(), limits: limitsFor(env, null) });
	return json({ ok: true, providers, budget_left: status.budget_left });
}

export default {
	async fetch(request, env, ctx) {
		const url = new URL(request.url);
		try {
			if (url.pathname === "/" && request.method === "POST") return await handleRelay(request, env, ctx);
			if (url.pathname === "/health" && request.method === "GET") return await handleHealth(env);
			return fail("not_found");
		} catch (e) {
			console.log(`relay: unexpected error: ${e && e.stack ? e.stack : e}`);
			return fail("relay_error");
		}
	},
};

// One global counter object. All state is for one UTC day; a new day clears it.
export class Limiter extends DurableObject {
	async rollDay(day) {
		const s = this.ctx.storage;
		if ((await s.get("day")) !== day) {
			await s.deleteAll();
			await s.put("day", day);
		}
	}

	async reserve({ day, session, provider, ipHash, limits }) {
		await this.rollDay(day);
		const s = this.ctx.storage;
		const keys = { calls: "calls", tokens: `tokens:${provider}`, session: `session:${session}`, ip: `ip:${ipHash}` };
		const got = await s.get(Object.values(keys));
		const n = (k) => got.get(keys[k]) ?? 0;

		if (n("tokens") >= limits.daily_tokens) return { ok: false, code: "budget_used_up" };
		if (n("calls") >= limits.daily_calls) return { ok: false, code: "budget_used_up" };
		if (n("ip") >= limits.ip_daily_calls) return { ok: false, code: "player_limit" };
		if (n("session") >= limits.session_calls) return { ok: false, code: "session_limit" };

		await s.put({
			[keys.calls]: n("calls") + 1,
			[keys.session]: n("session") + 1,
			[keys.ip]: n("ip") + 1,
		});
		return { ok: true };
	}

	async record({ day, provider, tokens }) {
		await this.rollDay(day);
		const key = `tokens:${provider}`;
		await this.ctx.storage.put(key, ((await this.ctx.storage.get(key)) ?? 0) + tokens);
	}

	async status({ day, limits }) {
		await this.rollDay(day);
		const calls = (await this.ctx.storage.get("calls")) ?? 0;
		return { budget_left: calls < limits.daily_calls };
	}
}
