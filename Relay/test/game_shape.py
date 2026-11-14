"""Send one request shaped like the game's to each provider the relay has a key for.

Usage:  python Relay/test/game_shape.py <relay URL> [--real]

Free mode (the default) costs nothing: the relay runs every check and answers with a
canned reply in the provider's shape, for every provider in the config. --real calls the
providers that have a key (listed by /health) and spends tokens.

It sends a system prompt, one user message and
the game's reply schema (from Content/NHOS/Data/llm.json) as strict JSON output,
then checks that the reply text parses as JSON with the schema's fields.
Exit code 0 when every provider passes. Each call asks for at most 2000 tokens.
"""
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LLM = json.loads((ROOT / "Content/NHOS/Data/llm.json").read_text(encoding="utf-8"))
CONFIG = json.loads((ROOT / "Relay/relay.config.json").read_text(encoding="utf-8"))
SCHEMA = LLM["reply_schema"]
SYSTEM = "You are a robot actor in an improv show. Reply only in the given JSON shape."
USER = '{"ask": "Say one short friendly line to the audience. No actions, no vote."}'

# Reasoning effort to send per provider, from each provider's docs. None = don't send it.
EFFORT = {"openai": "none", "xai": "none", "meta": "minimal"}  # meta rejects "none" (400)


def body_for(pid):
    p = CONFIG["providers"][pid]
    if p["shape"] == "anthropic":
        role = LLM["roles"]["actor"]
        return {
            "model": p["models"][0],
            "max_tokens": 2000,
            "system": SYSTEM,
            "messages": [{"role": "user", "content": USER}],
            "output_config": {"effort": role["effort"], "format": {"type": "json_schema", "schema": SCHEMA}},
        }
    body = {
        "model": p["models"][0],
        p["max_tokens_field"]: 2000,
        "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": USER}],
        "response_format": {
            "type": "json_schema",
            "json_schema": {"name": "reply", "schema": SCHEMA, "strict": True},
        },
    }
    if EFFORT.get(pid):
        body["reasoning_effort"] = EFFORT[pid]
    return body


def text_of(pid, reply):
    if CONFIG["providers"][pid]["shape"] == "anthropic":
        for block in reply.get("content", []):
            if block.get("type") == "text":
                return block["text"], reply.get("stop_reason"), reply.get("usage", {})
        return None, reply.get("stop_reason"), reply.get("usage", {})
    choice = (reply.get("choices") or [{}])[0]
    return choice.get("message", {}).get("content"), choice.get("finish_reason"), reply.get("usage", {})


# Cloudflare answers 403 to Python's default User-Agent, so send our own.
UA = {"user-agent": "nhos-relay-test/1.0"}


def post(url, payload):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), method="POST",
                                 headers={"content-type": "application/json", **UA})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read() or b"{}")


def main():
    url = sys.argv[1].rstrip("/")
    real = "--real" in sys.argv[2:]
    if real:
        with urllib.request.urlopen(urllib.request.Request(url + "/health", headers=UA), timeout=30) as r:
            ready = json.loads(r.read())["providers"]
        print("real mode, providers with a key:", ", ".join(ready) or "none")
    else:
        ready = list(CONFIG["providers"])
        print("free mode (no tokens), providers:", ", ".join(ready))
    failed = 0
    for pid in ready:
        start = time.time()
        envelope = {"provider": pid, "session": f"gameshape-{pid}-{int(start)}", "body": body_for(pid)}
        if not real:
            envelope["free"] = True
        reply = post(url + "/", envelope)
        secs = time.time() - start
        if reply.get("type") == "error":
            failed += 1
            print(f"FAIL  {pid}: {json.dumps(reply.get('error'))}")
            continue
        text, stop, usage = text_of(pid, reply)
        try:
            data = json.loads(text or "")
            missing = [k for k in SCHEMA["required"] if k not in data]
        except json.JSONDecodeError:
            data, missing = None, ["(not JSON)"]
        ok = data is not None and not missing and (real or reply.get("relay_free") is True)
        failed += 0 if ok else 1
        print(f"{'PASS' if ok else 'FAIL'}  {pid} ({CONFIG['providers'][pid]['models'][0]}): {secs:.1f} s, stop={stop}, usage={json.dumps(usage)}")
        print(f"      {text}")
        if missing:
            print(f"      missing: {missing}")
    print(f"\n{len(ready) - failed} passed, {failed} failed")
    sys.exit(1 if failed or not ready else 0)


if __name__ == "__main__":
    main()
