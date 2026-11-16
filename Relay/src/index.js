// No Humans On Set: the relay. Holds the provider keys as Worker secrets, checks
// each request from the game, forwards the body unchanged to the provider and
// returns the provider's reply. The one change it makes to the body is the
// "force" fields in relay.config.json (the cheapest effort). See Relay/README.md.
//
// Request (POST /):  { "provider": "<id>", "session": "<id>", "body": { ... }, "free": true (optional) }
// Free mode ("free": true): every check runs, but no provider is called. The reply is a
// canned one in the provider's exact response shape, with "relay_free": true. No tokens.
// Reply on success:  the provider's reply, unchanged.
// Reply on failure:  { "type": "error", "error": { "type": <code>, "message": <text the game can show>, "source": "relay" } }
// GET /health:       { "ok": true, "providers": [<ids that can serve calls>], "budget_left": true|false, "free_mode": true }
// POST /event:       an analytics event, checked against "events" in relay.config.json and stored in the
//                    Stats Durable Object. Answers { "ok": true }. Never calls a provider or counts as a call.
// GET /stats:        the stored events, for Tools/analytics_report.py. Needs "Authorization: Bearer <STATS_KEY>";
//                    without it (or with no STATS_KEY set) it answers not_found, like any unknown path.

import { DurableObject } from "cloudflare:workers";
import CONFIG from "../relay.config.json";
// The game's pre-written free-mode replies (one source for the game and the relay).
import FREE from "../../Content/NHOS/Data/free_mode.json";

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

function freeLimits() {
	const f = CONFIG.limits.free ?? {};
	return {
		session_calls: f.session_calls ?? CONFIG.limits.session_calls,
		ip_daily_calls: f.ip_daily_calls ?? CONFIG.limits.ip_daily_calls,
		daily_calls: f.daily_calls ?? CONFIG.limits.daily_calls,
		daily_tokens: Number.MAX_SAFE_INTEGER,
	};
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

// The text of the last user message: the state JSON the game sends.
function lastUserText(p, body) {
	const users = body.messages.filter((m) => m.role === "user");
	const content = users.length ? users[users.length - 1].content : "";
	if (typeof content === "string") return content;
	return content.map((part) => part.text).join("");
}

function pick(list) {
	return list.length ? list[Math.floor(Math.random() * list.length)] : "";
}

function names(list) {
	return Array.isArray(list)
		? list.map((x) => (isObject(x) ? x.name : x)).filter((x) => typeof x === "string" && x)
		: [];
}

// Which free_mode.json phase this ask is: a field the state has, or words in its "ask".
function freePhase(state) {
	const ask = typeof state.ask === "string" ? state.ask : "";
	for (const ph of FREE.phases) {
		if (ph.when_field && ph.when_field in state) return ph;
		if ((ph.ask_contains ?? []).some((w) => ask.includes(w))) return ph;
	}
	return FREE.phases.find((ph) => ph.id === "scene_turn") ?? {};
}

function fill(text, ctx) {
	return text
		.replace(/\{actor\}/g, () => pick(ctx.others) || "someone")
		.replace(/\{vote\}/g, ctx.vote || "someone")
		.replace(/\{place\}/g, () => pick(ctx.places) || "Center")
		.replace(/\{prop\}/g, () => pick(ctx.props) || "prop");
}

function weighted(list) {
	const total = list.reduce((n, x) => n + (x.weight ?? 1), 0);
	let r = Math.random() * total;
	for (const x of list) {
		r -= x.weight ?? 1;
		if (r <= 0) return x;
	}
	return list[list.length - 1];
}

// The emotion a free reply shows (T76): a weighted pick from the phase's "emotions"
// in free_mode.json, or "neutral" when the phase has none (the input step).
function freeEmotion(ph) {
	const list = Array.isArray(ph.emotions) ? ph.emotions.filter((x) => isObject(x) && typeof x.id === "string") : [];
	return list.length ? weighted(list).id : "neutral";
}

// The emotion of the player's typed line (T77): the first entry in free_mode.json's "emotion_keywords" with a word
// found in the line, or "neutral". The line gets one space in front and is matched in lower case, so a word that
// starts with a space matches only at the start of a word; a word with "+" needs every part. BPC_LLMClient.KeywordEmotion
// and Tools/check_prompts.py read the table the same way.
function keywordEmotion(text) {
	const line = " " + String(text).toLowerCase();
	const table = Array.isArray(FREE.emotion_keywords) ? FREE.emotion_keywords : [];
	for (const k of table) {
		if (!isObject(k) || typeof k.id !== "string" || !Array.isArray(k.words)) continue;
		for (const w of k.words) {
			const parts = typeof w === "string" ? w.toLowerCase().split("+").filter((p) => p) : [];
			if (parts.length && parts.every((p) => line.includes(p))) return k.id;
		}
	}
	return "neutral";
}

// A reply in the game's one reply shape, made up from free_mode.json without a model.
function freeReplyObject(p, body) {
	let state = {};
	try {
		const parsed = JSON.parse(lastUserText(p, body));
		if (isObject(parsed)) state = parsed;
	} catch {
		// Not JSON: answer as a scene turn with no names.
	}
	const me = isObject(state.you) ? state.you.name : state.actor;
	const ctx = {
		others: names(state.cast).filter((n) => n !== me),
		places: names(isObject(state.set) ? state.set.places : state.places),
		props: names(isObject(state.set) ? state.set.props : state.props),
		vote: "",
	};
	const ph = freePhase(state);
	const reply = { actions: [], speech: "", vote: "", reason: "", pass: false, emotion: freeEmotion(ph), tell: "" };

	if (ph.echo_typed) {
		const typed = typeof state.typed === "string" ? state.typed : "";
		reply.speech = typed.split(/\s+/).filter(Boolean).slice(0, 15).join(" ");
		reply.emotion = keywordEmotion(typed);
		return reply;
	}
	if (ph.vote) {
		const options = names(state.options).filter((n) => n !== me);
		ctx.vote = pick(options.length ? options : names(state.options));
		reply.vote = ctx.vote;
		// A vote's reason comes with its tell (T60): the one at the same index in the phase's "tells", or "".
		const reasons = ph.reasons ?? [];
		const i = Math.floor(Math.random() * reasons.length);
		reply.reason = reasons.length ? fill(reasons[i], ctx) : "";
		reply.tell = Array.isArray(ph.tells) && typeof ph.tells[i] === "string" ? ph.tells[i] : "";
		return reply;
	}
	if (ph.pass_chance && Math.random() < ph.pass_chance) {
		reply.pass = true;
		return reply;
	}
	reply.speech = fill(pick(ph.lines ?? []), ctx);
	const [lo, hi] = ph.actions ?? [0, 0];
	const count = lo + Math.floor(Math.random() * (hi - lo + 1));
	for (let i = 0; i < count && FREE.scene_actions?.length; i++) {
		const a = weighted(FREE.scene_actions);
		const action = { verb: a.verb, target: fill(a.target, ctx), item: fill(a.item, ctx) };
		// Skip an action whose names the state doesn't have.
		if ((a.target.includes("{actor}") && !ctx.others.length) || (a.item.includes("{prop}") && !ctx.props.length)) continue;
		if (a.target.includes("{place}") && !ctx.places.length) continue;
		reply.actions.push(action);
	}
	return reply;
}

function freeResponse(p, body) {
	const text = JSON.stringify(freeReplyObject(p, body));
	const id = crypto.randomUUID().replace(/-/g, "");
	if (p.shape === "anthropic") {
		return json({
			id: `msg_free_${id}`,
			type: "message",
			role: "assistant",
			model: body.model,
			content: [{ type: "text", text }],
			stop_reason: "end_turn",
			stop_sequence: null,
			usage: { input_tokens: 0, output_tokens: 0 },
			relay_free: true,
		});
	}
	return json({
		id: `chatcmpl-free-${id}`,
		object: "chat.completion",
		created: Math.floor(Date.now() / 1000),
		model: body.model,
		choices: [{ index: 0, message: { role: "assistant", content: text, refusal: null }, finish_reason: "stop" }],
		usage: { prompt_tokens: 0, completion_tokens: 0, total_tokens: 0 },
		relay_free: true,
	});
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
		if (!["provider", "session", "body", "free"].includes(key)) {
			return fail("bad_request", `request field "${key}" is not allowed`);
		}
	}

	const { provider: id, session, body } = envelope;
	if ("free" in envelope && typeof envelope.free !== "boolean") return fail("bad_request", "free must be true or false");
	const free = envelope.free === true;
	if (typeof session !== "string" || !/^[A-Za-z0-9_-]{8,64}$/.test(session)) {
		return fail("bad_request", "session must be 8 to 64 letters, digits, - or _");
	}
	if (typeof id !== "string" || !Object.hasOwn(CONFIG.providers, id)) {
		return fail("unknown_provider");
	}
	const p = CONFIG.providers[id];
	// Free mode needs no key, only an allow-list to check the body against.
	if (free ? !(Array.isArray(p.models) && p.models.length) : !providerReady(env, p)) {
		return fail("provider_unavailable");
	}

	const reason = checkBody(p, body);
	if (reason) return fail("bad_request", reason);

	const day = utcDay();
	const ip = request.headers.get("cf-connecting-ip") ?? "unknown";
	const verdict = await limiter(env).reserve({
		day,
		session,
		provider: id,
		ipHash: await hashIp(ip, day),
		limits: free ? freeLimits() : limitsFor(env, p),
		free,
	});
	if (!verdict.ok) return fail(verdict.code);
	if (free) return freeResponse(p, body);

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

// ---- Analytics: POST /event and GET /stats ----

const EVENT_KEYS = ["player", "session", "build", "mode", "event", "fields", "test"];
const EVENT_MODES = ["free", "relay", "keys", ""];

function eventSpec(name) {
	const allowed = CONFIG.events.allowed;
	return typeof name === "string" && !name.startsWith("_") && Object.hasOwn(allowed, name) ? allowed[name] : null;
}

function checkField(spec, value, name) {
	if (spec.type === "string") {
		if (typeof value !== "string") return `field "${name}" must be text`;
		if (value.length > spec.max) return `field "${name}" is over ${spec.max} characters`;
	} else if (spec.type === "int") {
		if (!Number.isInteger(value)) return `field "${name}" must be a whole number`;
		if (value < spec.min || value > spec.max) return `field "${name}" must be ${spec.min} to ${spec.max}`;
	} else if (spec.type === "bool") {
		if (typeof value !== "boolean") return `field "${name}" must be true or false`;
	} else {
		return `field "${name}" has no type in the config`;
	}
	return null;
}

// Returns null when the event is the shape the config allows, or a reason when it isn't.
function checkEvent(ev) {
	if (!isObject(ev)) return "request must be a JSON object";
	for (const key of Object.keys(ev)) {
		if (!EVENT_KEYS.includes(key)) return `request field "${key}" is not allowed`;
	}
	if (typeof ev.player !== "string" || !/^[0-9a-fA-F]{32}$/.test(ev.player)) return "player must be 32 hex digits";
	if (typeof ev.session !== "string" || !/^[A-Za-z0-9_-]{8,64}$/.test(ev.session)) {
		return "session must be 8 to 64 letters, digits, - or _";
	}
	if ("build" in ev && (typeof ev.build !== "string" || ev.build.length > 20)) return "build must be text of up to 20 characters";
	if ("mode" in ev && !EVENT_MODES.includes(ev.mode)) return 'mode must be "free", "relay", "keys" or ""';
	if ("test" in ev && typeof ev.test !== "boolean") return "test must be true or false";
	const spec = eventSpec(ev.event);
	if (!spec) return "event is not on the allow-list";
	if ("fields" in ev) {
		if (!isObject(ev.fields)) return "fields must be an object";
		for (const [name, value] of Object.entries(ev.fields)) {
			if (name.startsWith("_") || !Object.hasOwn(spec, name)) return `field "${name}" is not allowed for ${ev.event}`;
			const err = checkField(spec[name], value, name);
			if (err) return err;
		}
	}
	return null;
}

function stats(env) {
	return env.STATS.get(env.STATS.idFromName("global"));
}

async function handleEvent(request, env) {
	const type = request.headers.get("content-type") ?? "";
	if (!type.toLowerCase().includes("application/json")) {
		return fail("bad_request", "content-type must be application/json");
	}
	const cap = CONFIG.events.max_body_bytes;
	if (Number(request.headers.get("content-length") ?? 0) > cap) return fail("bad_request", "event is too large");
	const text = await request.text();
	if (new TextEncoder().encode(text).length > cap) return fail("bad_request", "event is too large");

	let ev;
	try {
		ev = JSON.parse(text);
	} catch {
		return fail("bad_request", "request is not JSON");
	}
	const reason = checkEvent(ev);
	if (reason) return fail("bad_request", reason);

	const now = new Date().toISOString();
	const day = now.slice(0, 10);
	const ip = request.headers.get("cf-connecting-ip") ?? "unknown";
	const verdict = await stats(env).add({
		day,
		limit: intVar(env.IP_DAILY_EVENTS, CONFIG.limits.ip_daily_events),
		row: {
			ts: now,
			ip: await hashIp(ip, day),
			player: ev.player.toLowerCase(),
			session: ev.session,
			build: ev.build ?? "",
			mode: ev.mode ?? "",
			event: ev.event,
			fields: JSON.stringify(ev.fields ?? {}),
			test: ev.test === true ? 1 : 0,
		},
	});
	if (!verdict.ok) return fail(verdict.code);
	return json({ ok: true });
}

// True only when STATS_KEY is set (16 characters or more) and the request carries it.
async function statsKeyMatches(request, env) {
	const key = env.STATS_KEY ?? "";
	const m = /^Bearer (\S+)$/.exec(request.headers.get("authorization") ?? "");
	if (key.length < 16 || !m) return false;
	const enc = new TextEncoder();
	const [a, b] = await Promise.all([
		crypto.subtle.digest("SHA-256", enc.encode(m[1])),
		crypto.subtle.digest("SHA-256", enc.encode(key)),
	]);
	return crypto.subtle.timingSafeEqual(a, b);
}

// GET /stats?since=YYYY-MM-DD&test=1&after=<id>&limit=<n>: one page of events, oldest first.
// Leaves out "test" events unless test=1. "next" is the after= value for the next page, or null.
async function handleStats(request, env, url) {
	if (!(await statsKeyMatches(request, env))) return fail("not_found");
	const since = url.searchParams.get("since") ?? "";
	if (since && !/^\d{4}-\d{2}-\d{2}$/.test(since)) return fail("bad_request", "since must be YYYY-MM-DD");
	const page = await stats(env).read({
		since,
		test: url.searchParams.get("test") === "1",
		after: intVar(url.searchParams.get("after"), 0),
		limit: Math.min(Math.max(intVar(url.searchParams.get("limit"), 2000), 1), 5000),
	});
	return json({ ok: true, ...page });
}

async function handleHealth(env) {
	const providers = Object.entries(CONFIG.providers)
		.filter(([, p]) => providerReady(env, p))
		.map(([id]) => id);
	const status = await limiter(env).status({ day: utcDay(), limits: limitsFor(env, null) });
	return json({ ok: true, providers, budget_left: status.budget_left, free_mode: true });
}

export default {
	async fetch(request, env, ctx) {
		const url = new URL(request.url);
		try {
			if (url.pathname === "/" && request.method === "POST") return await handleRelay(request, env, ctx);
			if (url.pathname === "/health" && request.method === "GET") return await handleHealth(env);
			if (url.pathname === "/event" && request.method === "POST") return await handleEvent(request, env);
			if (url.pathname === "/stats" && request.method === "GET") return await handleStats(request, env, url);
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

	// Free-mode calls use their own counters ("free:" keys), so tests never use up the real budget.
	async reserve({ day, session, provider, ipHash, limits, free = false }) {
		await this.rollDay(day);
		const s = this.ctx.storage;
		const pre = free ? "free:" : "";
		const keys = {
			calls: `${pre}calls`,
			tokens: `${pre}tokens:${provider}`,
			session: `${pre}session:${session}`,
			ip: `${pre}ip:${ipHash}`,
		};
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

// One global store for analytics events (SQLite). Unlike the Limiter, it keeps every
// event until someone deletes it. The per-address event counts are for one UTC day;
// "test" events are counted apart, so tests never use up a player's real allowance.
export class Stats extends DurableObject {
	constructor(ctx, env) {
		super(ctx, env);
		this.sql = ctx.storage.sql;
		this.sql.exec(`CREATE TABLE IF NOT EXISTS events (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			ts TEXT NOT NULL,
			ip TEXT NOT NULL,
			player TEXT NOT NULL,
			session TEXT NOT NULL,
			build TEXT NOT NULL,
			mode TEXT NOT NULL,
			event TEXT NOT NULL,
			fields TEXT NOT NULL,
			test INTEGER NOT NULL
		)`);
		this.sql.exec(`CREATE TABLE IF NOT EXISTS event_counts (
			day TEXT NOT NULL,
			who TEXT NOT NULL,
			n INTEGER NOT NULL,
			PRIMARY KEY (day, who)
		) WITHOUT ROWID`);
		this.countsDay = "";
	}

	add({ day, limit, row }) {
		if (this.countsDay !== day) {
			this.sql.exec("DELETE FROM event_counts WHERE day < ?", day);
			this.countsDay = day;
		}
		const who = `${row.test ? "test:" : ""}${row.ip}`;
		const got = this.sql.exec("SELECT n FROM event_counts WHERE day = ? AND who = ?", day, who).toArray();
		if ((got.length ? got[0].n : 0) >= limit) return { ok: false, code: "player_limit" };
		this.sql.exec(
			"INSERT INTO event_counts (day, who, n) VALUES (?, ?, 1) ON CONFLICT (day, who) DO UPDATE SET n = n + 1",
			day,
			who,
		);
		this.sql.exec(
			"INSERT INTO events (ts, ip, player, session, build, mode, event, fields, test) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
			row.ts, row.ip, row.player, row.session, row.build, row.mode, row.event, row.fields, row.test,
		);
		return { ok: true };
	}

	// The address hash stays in the store and is never read back out.
	read({ since, test, after, limit }) {
		const rows = this.sql
			.exec(
				`SELECT id, ts, player, session, build, mode, event, fields, test FROM events
				 WHERE id > ? AND ts >= ? AND (? = 1 OR test = 0) ORDER BY id LIMIT ?`,
				after, since, test ? 1 : 0, limit,
			)
			.toArray()
			.map((r) => ({ ...r, fields: JSON.parse(r.fields), test: r.test === 1 }));
		return { events: rows, next: rows.length === limit ? rows[rows.length - 1].id : null };
	}
}
