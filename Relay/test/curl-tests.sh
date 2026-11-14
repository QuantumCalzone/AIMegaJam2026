#!/usr/bin/env bash
# Curl tests for the relay. Start it first with low limits:
#   npx wrangler dev --var SESSION_CALLS:2 --var DAILY_CALLS:8
# then run:  bash test/curl-tests.sh [relay URL, default http://127.0.0.1:8787]
# Each good call asks for at most 16 tokens. A run makes up to 8 real calls.
# Restart wrangler dev (or wait for the next UTC day) before running it again,
# because the daily count carries over.

URL="${1:-http://127.0.0.1:8787}"
PASS=0
FAIL=0
RUN="t$(date +%s)"

# Models the tiny good call uses, per provider. Keep in step with relay.config.json.
model_for() {
	case "$1" in
		anthropic) echo "claude-haiku-5-5" ;;
		*) python -c "import json,sys;print(json.load(open('relay.config.json'))['providers'][sys.argv[1]]['models'][0])" "$1" ;;
	esac
}

tiny_body() { # provider model
	local field
	field=$(python -c "import json,sys;print(json.load(open('relay.config.json'))['providers'][sys.argv[1]]['max_tokens_field'])" "$1")
	echo "{\"model\":\"$2\",\"$field\":16,\"messages\":[{\"role\":\"user\",\"content\":\"Reply with the one word: ready\"}]}"
}

post() { # data -> prints body
	curl -s -X POST "$URL/" -H "content-type: application/json" --data-binary "$1"
}

expect() { # name, reply, pattern
	if printf '%s' "$2" | grep -q -- "$3"; then
		PASS=$((PASS + 1)); echo "PASS  $1"
	else
		FAIL=$((FAIL + 1)); echo "FAIL  $1"; echo "      got: ${2:0:400}"
	fi
}

cd "$(dirname "$0")/.." || exit 1

echo "== health"
HEALTH=$(curl -s "$URL/health")
echo "      $HEALTH"
expect "health answers" "$HEALTH" '"ok":true'
READY=$(printf '%s' "$HEALTH" | python -c "import json,sys;print(' '.join(json.load(sys.stdin)['providers']))")
[ -n "$READY" ] || echo "      no provider has a key; put keys in .dev.vars"

echo "== one good call per provider with a key"
for P in $READY; do
	M=$(model_for "$P")
	R=$(post "{\"provider\":\"$P\",\"session\":\"${RUN}-good-$P\",\"body\":$(tiny_body "$P" "$M")}")
	expect "good call: $P" "$R" '"usage"'
done

FIRST=$(echo "$READY" | cut -d' ' -f1)
FIRST=${FIRST:-anthropic}
FM=$(model_for "$FIRST")
GOOD_BODY=$(tiny_body "$FIRST" "$FM")

echo "== bad requests (none of these reach a provider or count)"
expect "not JSON" "$(post 'hello')" '"type":"bad_request"'
expect "wrong content-type" "$(curl -s -X POST "$URL/" -H 'content-type: text/plain' --data-binary '{}')" '"type":"bad_request"'
expect "extra top-level field" "$(post "{\"provider\":\"$FIRST\",\"session\":\"${RUN}-bad\",\"body\":$GOOD_BODY,\"key\":\"x\"}")" '"type":"bad_request"'
expect "missing session" "$(post "{\"provider\":\"$FIRST\",\"body\":$GOOD_BODY}")" '"type":"bad_request"'
expect "streaming" "$(post "{\"provider\":\"anthropic\",\"session\":\"${RUN}-bad\",\"body\":{\"model\":\"claude-haiku-5-5\",\"max_tokens\":16,\"stream\":true,\"messages\":[{\"role\":\"user\",\"content\":\"hi\"}]}}")" '"type":"bad_request"'
expect "max_tokens over cap" "$(post "{\"provider\":\"anthropic\",\"session\":\"${RUN}-bad\",\"body\":{\"model\":\"claude-haiku-5-5\",\"max_tokens\":64000,\"messages\":[{\"role\":\"user\",\"content\":\"hi\"}]}}")" '"type":"bad_request"'
expect "no max_tokens" "$(post "{\"provider\":\"anthropic\",\"session\":\"${RUN}-bad\",\"body\":{\"model\":\"claude-haiku-5-5\",\"messages\":[{\"role\":\"user\",\"content\":\"hi\"}]}}")" '"type":"bad_request"'
expect "model not allowed" "$(post "{\"provider\":\"anthropic\",\"session\":\"${RUN}-bad\",\"body\":{\"model\":\"some-big-model\",\"max_tokens\":16,\"messages\":[{\"role\":\"user\",\"content\":\"hi\"}]}}")" '"type":"bad_request"'
expect "image content" "$(post "{\"provider\":\"anthropic\",\"session\":\"${RUN}-bad\",\"body\":{\"model\":\"claude-haiku-5-5\",\"max_tokens\":16,\"messages\":[{\"role\":\"user\",\"content\":[{\"type\":\"image\",\"source\":{}}]}]}}")" '"type":"bad_request"'
expect "tools field" "$(post "{\"provider\":\"anthropic\",\"session\":\"${RUN}-bad\",\"body\":{\"model\":\"claude-haiku-5-5\",\"max_tokens\":16,\"tools\":[],\"messages\":[{\"role\":\"user\",\"content\":\"hi\"}]}}")" '"type":"bad_request"'
expect "unknown provider" "$(post "{\"provider\":\"nobody\",\"session\":\"${RUN}-bad\",\"body\":$GOOD_BODY}")" '"type":"unknown_provider"'
expect "unknown path" "$(curl -s "$URL/v2/anything")" '"type":"not_found"'
for P in anthropic openai xai meta; do
	case " $READY " in *" $P "*) ;; *)
		expect "provider with no key: $P" "$(post "{\"provider\":\"$P\",\"session\":\"${RUN}-bad\",\"body\":$GOOD_BODY}")" '"type":"provider_unavailable"' ;;
	esac
done
ALL=$(post 'hello')
if printf '%s' "$ALL" | grep -qiE 'anthropic|openai|xai|meta|claude|grok|llama'; then
	FAIL=$((FAIL + 1)); echo "FAIL  error text names a provider: $ALL"
else
	PASS=$((PASS + 1)); echo "PASS  error text names no provider"
fi

echo "== session limit (needs SESSION_CALLS:2)"
S="${RUN}-limit"
expect "session call 1" "$(post "{\"provider\":\"$FIRST\",\"session\":\"$S\",\"body\":$GOOD_BODY}")" '"usage"'
expect "session call 2" "$(post "{\"provider\":\"$FIRST\",\"session\":\"$S\",\"body\":$GOOD_BODY}")" '"usage"'
expect "session call 3 trips the limit" "$(post "{\"provider\":\"$FIRST\",\"session\":\"$S\",\"body\":$GOOD_BODY}")" '"type":"session_limit"'

echo "== daily budget (needs DAILY_CALLS:8)"
TRIPPED=""
for i in 1 2 3 4 5 6 7 8 9; do
	R=$(post "{\"provider\":\"$FIRST\",\"session\":\"${RUN}-day-$i\",\"body\":$GOOD_BODY}")
	if printf '%s' "$R" | grep -q '"type":"budget_used_up"'; then TRIPPED="$i"; break; fi
done
expect "daily budget trips" "${TRIPPED:+tripped}" 'tripped'
[ -n "$TRIPPED" ] && echo "      tripped on day call $i: ${R:0:300}"
expect "health says the budget is used up" "$(curl -s "$URL/health")" '"budget_left":false'

echo
echo "$PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
