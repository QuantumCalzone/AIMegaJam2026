#!/usr/bin/env bash
# Curl tests for the relay.
#   bash test/curl-tests.sh <relay URL>            free mode (default): no provider is called, no tokens
#   bash test/curl-tests.sh <relay URL> --real     real calls: start the relay with low limits first
#                                                  (SESSION_CALLS=2, DAILY_CALLS=8; see README)
# Free mode trips the free session limit (limits.free.session_calls + 1 calls, a few seconds)
# and skips the daily budget test, which only real mode can trip without using up the day.
# A real run makes up to 8 calls of at most 16 tokens each.
#
# Analytics events (POST /event, GET /stats) are tested in both modes. Every test event has
# "test": true. Options after the URL:
#   --events-limit <n>     the relay's IP_DAILY_EVENTS (start it with a low one, e.g. 5); trips
#                          the event limit. Without it that one test is skipped, because the
#                          limit is per address per day and can't be tripped twice in a day.
#   --stats-config <path>  a stats.json with the relay's STATS_KEY (default: Local/stats.json in
#                          the repo). Without it, the tests that read events back are skipped.

URL="${1:-http://127.0.0.1:8787}"
MODE="free"
EVENTS_LIMIT=""
STATS_CONFIG=""
shift
while [ $# -gt 0 ]; do
	case "$1" in
		--real) MODE="real" ;;
		--events-limit) EVENTS_LIMIT="$2"; shift ;;
		--stats-config) STATS_CONFIG="$2"; shift ;;
		*) echo "unknown option: $1"; exit 2 ;;
	esac
	shift
done
# Windows has python, a Mac has python3.
PY=$(command -v python || command -v python3)
FREE=""
[ "$MODE" = "free" ] && FREE=',"free":true'
# What a good reply looks like in each mode.
GOOD='"usage"'
[ "$MODE" = "free" ] && GOOD='"relay_free":true'
echo "mode: $MODE"
PASS=0
FAIL=0
SKIP=0
RUN="t$(date +%s)"

# Models the tiny good call uses, per provider. Keep in step with relay.config.json.
model_for() {
	case "$1" in
		anthropic) echo "claude-haiku-5-5" ;;
		*) "$PY" -c "import json,sys;print(json.load(open('relay.config.json'))['providers'][sys.argv[1]]['models'][0])" "$1" ;;
	esac
}

tiny_body() { # provider model
	local field
	field=$("$PY" -c "import json,sys;print(json.load(open('relay.config.json'))['providers'][sys.argv[1]]['max_tokens_field'])" "$1")
	echo "{\"model\":\"$2\",\"$field\":16,\"messages\":[{\"role\":\"user\",\"content\":\"Reply with the one word: ready\"}]}"
}

post() { # data -> prints body
	curl -s -X POST "$URL/" -H "content-type: application/json" --data-binary "$1"
}

# postx and evx take the request body as a plain argument. (macOS bash 3.2 brace-expands a
# "{...,...}" body nested in "$(...)" inside double quotes, which splits it into pieces.)
postx() { # name, data, pattern
	local r
	r=$(post "$2")
	expect "$1" "$r" "$3"
}

evx() { # name, data, pattern
	local r
	r=$(ev "$2")
	expect "$1" "$r" "$3"
}

expect() { # name, reply, pattern
	if printf '%s' "$2" | grep -q -- "$3"; then
		PASS=$((PASS + 1)); echo "PASS  $1"
	else
		FAIL=$((FAIL + 1)); echo "FAIL  $1"; echo "      got: ${2:0:400}"
	fi
}

[ -n "$STATS_CONFIG" ] && STATS_CONFIG=$(cd "$(dirname "$STATS_CONFIG")" && pwd)/$(basename "$STATS_CONFIG")
cd "$(dirname "$0")/.." || exit 1
[ -z "$STATS_CONFIG" ] && [ -f ../Local/stats.json ] && STATS_CONFIG="$(cd .. && pwd)/Local/stats.json"

skip() { # name, why
	SKIP=$((SKIP + 1)); echo "SKIP  $1 ($2)"
}

absent() { # name, reply, pattern: passes when the pattern is NOT in the reply
	if printf '%s' "$2" | grep -q -- "$3"; then
		FAIL=$((FAIL + 1)); echo "FAIL  $1"; echo "      found: $3"
	else
		PASS=$((PASS + 1)); echo "PASS  $1"
	fi
}

ev() { # data -> prints body
	curl -s -X POST "$URL/event" -H "content-type: application/json" --data-binary "$1"
}

event_tests() {
	local player evs base marker long big hdr r i tripped
	player=$("$PY" -c "import secrets;print(secrets.token_hex(16))")
	evs="${RUN}-events"
	base="\"player\":\"$player\",\"session\":\"$evs\",\"build\":\"curl-test\",\"mode\":\"free\",\"test\":true"
	marker="curl test $RUN"
	echo "== analytics events (all \"test\": true; none reach a provider)"
	evx "event: launch is taken" "{$base,\"event\":\"launch\",\"fields\":{\"launches\":2,\"first_seen\":\"2026-11-15\"}}" '"ok":true'
	evx "event: unsupported is taken" "{$base,\"event\":\"unsupported\",\"fields\":{\"words\":\"$marker\",\"source\":\"typed\",\"phase\":\"scene\"}}" '"ok":true'
	evx "event: no fields, upper-case player" "{\"player\":\"$(printf '%s' "$player" | tr a-f A-F)\",\"session\":\"$evs\",\"event\":\"show_start\",\"test\":true}" '"ok":true'
	evx "event: not JSON" 'hello' 'request is not JSON'
	r=$(curl -s -X POST "$URL/event" -H 'content-type: text/plain' --data-binary "{$base,\"event\":\"mode\"}")
	expect "event: wrong content-type" "$r" 'content-type must be application/json'
	evx "event: unknown event" "{$base,\"event\":\"cheat\"}" 'event is not on the allow-list'
	evx "event: extra top-level field" "{$base,\"event\":\"mode\",\"ip\":\"1.2.3.4\"}" 'is not allowed'
	evx "event: extra field" "{$base,\"event\":\"launch\",\"fields\":{\"typed\":\"hello\"}}" 'is not allowed for launch'
	evx "event: wrong type" "{$base,\"event\":\"launch\",\"fields\":{\"launches\":\"two\"}}" 'must be a whole number'
	evx "event: number out of range" "{$base,\"event\":\"phase\",\"fields\":{\"scene\":500}}" 'must be 0 to 99'
	long=$("$PY" -c "print('w' * 81)")
	evx "event: string over its cap" "{$base,\"event\":\"unsupported\",\"fields\":{\"words\":\"$long\"}}" 'is over 80 characters'
	evx "event: fields not an object" "{$base,\"event\":\"launch\",\"fields\":[1]}" 'fields must be an object'
	evx "event: player not 32 hex" "{\"player\":\"not-hex\",\"session\":\"$evs\",\"event\":\"mode\",\"test\":true}" 'player must be 32 hex digits'
	evx "event: no player" "{\"session\":\"$evs\",\"event\":\"mode\",\"test\":true}" 'player must be 32 hex digits'
	evx "event: bad mode" "{\"player\":\"$player\",\"session\":\"$evs\",\"mode\":\"demo\",\"event\":\"mode\",\"test\":true}" 'mode must be'
	evx "event: test not true or false" "{\"player\":\"$player\",\"session\":\"$evs\",\"event\":\"mode\",\"test\":\"yes\"}" 'test must be true or false'
	big=$("$PY" -c "print('x' * 2100)")
	evx "event: over 2 KB" "{$base,\"event\":\"unsupported\",\"fields\":{\"words\":\"$big\"}}" 'too large'
	expect "event: GET is not a route" "$(curl -s "$URL/event")" '"type":"not_found"'

	echo "== reading events back"
	expect "stats: no key is not_found" "$(curl -s "$URL/stats")" '"type":"not_found"'
	expect "stats: wrong key is not_found" "$(curl -s "$URL/stats" -H 'authorization: Bearer wrong-key-wrong-key-wrong-key')" '"type":"not_found"'
	if [ -n "$STATS_CONFIG" ] && [ -f "$STATS_CONFIG" ]; then
		# The key goes to curl in a file (never on a command line or in output), then the file is deleted.
		hdr=$(mktemp)
		chmod 600 "$hdr"
		"$PY" -c "import json,sys;open(sys.argv[2],'w').write('authorization: Bearer '+json.load(open(sys.argv[1]))['stats_key']+'\n')" "$STATS_CONFIG" "$hdr"
		r=$(curl -s "$URL/stats?test=1&since=$(date -u +%Y-%m-%d)&limit=5000" -H @"$hdr")
		expect "stats: the good events are stored" "$(printf '%s' "$r" | grep -o "\"session\":\"$evs\"" | wc -l | tr -d ' ')" '^3$'
		absent "stats: the address is never read back" "$r" '"ip"'
		r=$(curl -s "$URL/stats?since=$(date -u +%Y-%m-%d)&limit=5000" -H @"$hdr")
		absent "stats: test events are left out without test=1" "$r" "\"session\":\"$evs\""
		rm -f "$hdr"
		r=$("$PY" ../Tools/analytics_report.py --config "$STATS_CONFIG" --relay "$URL" --since "$(date -u +%Y-%m-%d)" --test --top 1000 2>&1)
		expect "report --test shows the test event" "$r" "$marker"
		r=$("$PY" ../Tools/analytics_report.py --config "$STATS_CONFIG" --relay "$URL" --since "$(date -u +%Y-%m-%d)" --top 1000 2>&1)
		expect "report without --test answers" "$r" '== unsupported actions'
		absent "report without --test leaves it out" "$r" "$marker"
	else
		skip "stats and report read-back" "no stats.json; pass --stats-config"
	fi

	if [ -n "$EVENTS_LIMIT" ]; then
		echo "== event limit ($EVENTS_LIMIT test events a day from this address, then one more)"
		tripped=""
		for i in $(seq 1 $((EVENTS_LIMIT + 1))); do
			r=$(ev "{$base,\"event\":\"mode\"}")
			if printf '%s' "$r" | grep -q '"type":"player_limit"'; then tripped="$i"; break; fi
		done
		expect "event limit trips with player_limit" "${tripped:+tripped}" 'tripped'
	else
		skip "event limit" "pass --events-limit <the relay's IP_DAILY_EVENTS>"
	fi
}

echo "== health"
HEALTH=$(curl -s "$URL/health")
echo "      $HEALTH"
expect "health answers" "$HEALTH" '"ok":true'
READY=$(printf '%s' "$HEALTH" | "$PY" -c "import json,sys;print(' '.join(json.load(sys.stdin)['providers']))")
[ -n "$READY" ] || echo "      no provider has a key; put keys in .dev.vars"

if [ "$MODE" = "free" ]; then
	# Free mode needs no key, so test every provider in the config.
	READY=$("$PY" -c "import json;print(' '.join(json.load(open('relay.config.json'))['providers']))")
	echo "== one free call per provider"
else
	echo "== one good call per provider with a key"
fi
for P in $READY; do
	M=$(model_for "$P")
	R=$(post "{\"provider\":\"$P\",\"session\":\"${RUN}-good-$P\",\"body\":$(tiny_body "$P" "$M")$FREE}")
	expect "good call: $P" "$R" "$GOOD"
done

FIRST=$(echo "$READY" | cut -d' ' -f1)
FIRST=${FIRST:-anthropic}
FM=$(model_for "$FIRST")
GOOD_BODY=$(tiny_body "$FIRST" "$FM")

echo "== bad requests (none of these reach a provider or count)"
postx "not JSON" 'hello' '"type":"bad_request"'
expect "wrong content-type" "$(curl -s -X POST "$URL/" -H 'content-type: text/plain' --data-binary '{}')" '"type":"bad_request"'
postx "extra top-level field" "{\"provider\":\"$FIRST\",\"session\":\"${RUN}-bad\",\"body\":$GOOD_BODY,\"key\":\"x\"}" '"type":"bad_request"'
postx "missing session" "{\"provider\":\"$FIRST\",\"body\":$GOOD_BODY}" '"type":"bad_request"'
postx "streaming" "{\"provider\":\"anthropic\",\"session\":\"${RUN}-bad\",\"body\":{\"model\":\"claude-haiku-5-5\",\"max_tokens\":16,\"stream\":true,\"messages\":[{\"role\":\"user\",\"content\":\"hi\"}]}$FREE}" '"type":"bad_request"'
postx "max_tokens over cap" "{\"provider\":\"anthropic\",\"session\":\"${RUN}-bad\",\"body\":{\"model\":\"claude-haiku-5-5\",\"max_tokens\":64000,\"messages\":[{\"role\":\"user\",\"content\":\"hi\"}]}$FREE}" '"type":"bad_request"'
postx "no max_tokens" "{\"provider\":\"anthropic\",\"session\":\"${RUN}-bad\",\"body\":{\"model\":\"claude-haiku-5-5\",\"messages\":[{\"role\":\"user\",\"content\":\"hi\"}]}$FREE}" '"type":"bad_request"'
postx "model not allowed" "{\"provider\":\"anthropic\",\"session\":\"${RUN}-bad\",\"body\":{\"model\":\"some-big-model\",\"max_tokens\":16,\"messages\":[{\"role\":\"user\",\"content\":\"hi\"}]}$FREE}" '"type":"bad_request"'
postx "image content" "{\"provider\":\"anthropic\",\"session\":\"${RUN}-bad\",\"body\":{\"model\":\"claude-haiku-5-5\",\"max_tokens\":16,\"messages\":[{\"role\":\"user\",\"content\":[{\"type\":\"image\",\"source\":{}}]}]}$FREE}" '"type":"bad_request"'
postx "tools field" "{\"provider\":\"anthropic\",\"session\":\"${RUN}-bad\",\"body\":{\"model\":\"claude-haiku-5-5\",\"max_tokens\":16,\"tools\":[],\"messages\":[{\"role\":\"user\",\"content\":\"hi\"}]}$FREE}" '"type":"bad_request"'
postx "unknown provider" "{\"provider\":\"nobody\",\"session\":\"${RUN}-bad\",\"body\":$GOOD_BODY}" '"type":"unknown_provider"'
expect "unknown path" "$(curl -s "$URL/v2/anything")" '"type":"not_found"'
postx "free is not true or false" "{\"provider\":\"$FIRST\",\"session\":\"${RUN}-bad\",\"body\":$GOOD_BODY,\"free\":\"yes\"}" '"type":"bad_request"'
[ "$MODE" = "real" ] && for P in anthropic openai xai meta; do
	case " $READY " in *" $P "*) ;; *)
		postx "provider with no key: $P" "{\"provider\":\"$P\",\"session\":\"${RUN}-bad\",\"body\":$GOOD_BODY}" '"type":"provider_unavailable"' ;;
	esac
done
ALL=$(post 'hello')
if printf '%s' "$ALL" | grep -qiE 'anthropic|openai|xai|meta|claude|grok|llama'; then
	FAIL=$((FAIL + 1)); echo "FAIL  error text names a provider: $ALL"
else
	PASS=$((PASS + 1)); echo "PASS  error text names no provider"
fi

event_tests

S="${RUN}-limit"
if [ "$MODE" = "free" ]; then
	N=$("$PY" -c "import json;l=json.load(open('relay.config.json'))['limits'];print(l.get('free',{}).get('session_calls',l['session_calls']))")
	echo "== free session limit ($N calls, then one more)"
	OKS=0
	for i in $(seq 1 "$N"); do
		R=$(post "{\"provider\":\"$FIRST\",\"session\":\"$S\",\"body\":$GOOD_BODY$FREE}")
		printf '%s' "$R" | grep -q '"relay_free":true' && OKS=$((OKS + 1))
	done
	expect "the first $N free calls pass" "$OKS" "^$N\$"
	postx "free call $((N + 1)) trips the limit" "{\"provider\":\"$FIRST\",\"session\":\"$S\",\"body\":$GOOD_BODY$FREE}" '"type":"session_limit"'
	VOTE_REQ=$("$PY" -c "import json,sys;c=json.load(open('relay.config.json'))['providers'][sys.argv[1]];b={'model':c['models'][0],c['max_tokens_field']:16,'messages':[{'role':'user','content':json.dumps({'options':['Robot A','Robot B'],'ask':'The Cut: vote.'})}]};print(json.dumps({'provider':sys.argv[1],'session':sys.argv[2],'body':b,'free':True}))" "$FIRST" "${RUN}-vote")
	free_reply=$(post "$VOTE_REQ")
	expect "free vote picks a name from options" "$free_reply" 'vote\\":\\"Robot [AB]'
	echo
	echo "$PASS passed, $FAIL failed, $SKIP skipped"
	[ "$FAIL" -eq 0 ]
	exit $?
fi

echo "== session limit (needs SESSION_CALLS:2)"
postx "session call 1" "{\"provider\":\"$FIRST\",\"session\":\"$S\",\"body\":$GOOD_BODY}" '"usage"'
postx "session call 2" "{\"provider\":\"$FIRST\",\"session\":\"$S\",\"body\":$GOOD_BODY}" '"usage"'
postx "session call 3 trips the limit" "{\"provider\":\"$FIRST\",\"session\":\"$S\",\"body\":$GOOD_BODY}" '"type":"session_limit"'

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
echo "$PASS passed, $FAIL failed, $SKIP skipped"
[ "$FAIL" -eq 0 ]
