#!/usr/bin/env python3
"""Report the game's analytics events, read from the relay's GET /stats (T67).

Python 3.10+, no packages. The key comes from Local/stats.json (an example is in
Docs/stats.example.json). It never goes in Local/llm_key.json, which ships next to the
packaged game. The relay address comes from stats.json's "relay", or else from
"relay" in Content/NHOS/Data/llm.json.

    python Tools/analytics_report.py                    every real event
    python Tools/analytics_report.py --since 2026-11-20 events from that UTC day on
    python Tools/analytics_report.py --test             real and "test" events together
    python Tools/analytics_report.py --build 2026-11-20-10f8540
                                                        one build's events alone
    python Tools/analytics_report.py --new-key          write Local/stats.json with a fresh
                                                        key (prints no key; paste it into
                                                        the Worker's STATS_KEY secret)

Other options: --config <path to stats.json>, --relay <address>, --top <n> (rows in the
long lists, 15 by default). Player ids listed in stats.json's "ignore_players" (our own
machines) are always left out.

Builds (T111): every event carries the build that sent it. A build that Tools/deploy_itch.py
makes reports its version label, <commit date>-<short sha>, the label of its file on
itch.io; the editor and builds packaged by hand report "local", and builds from before T111
"2026-11-15". The builds table lists players, shows and events per build, newest first (by
the build's first event). It marks the releases: labels of the form YYYY-MM-DD-<sha> whose
commit is on main (git merge-base --is-ancestor against origin/main as last fetched, or
main, when the script runs in the repo). It says "?" when git can't tell (no repo, or a
commit this clone hasn't fetched). Everything else is not a release.
"""

from __future__ import annotations

import argparse
import json
import re
import secrets
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = ROOT / "Local" / "stats.json"
LLM_JSON = ROOT / "Content" / "NHOS" / "Data" / "llm.json"
# Cloudflare answers 403 to Python's default User-Agent.
USER_AGENT = "nhos-analytics-report/1"
PAGE = 5000
# A build that Tools/deploy_itch.py made: <commit date (UTC)>-<short sha> (T111).
VERSION_LABEL = re.compile(r"^\d{4}-\d{2}-\d{2}-(?P<sha>[0-9a-f]{7,40})$")


def fail(text: str) -> None:
    print(f"analytics_report: {text}", file=sys.stderr)
    sys.exit(1)


def new_key(path: Path) -> None:
    if path.exists():
        fail(f"{path} already exists; delete it first if you want a new key")
    path.parent.mkdir(parents=True, exist_ok=True)
    body = {
        "_readme": "The key for GET /stats on the relay (Tools/analytics_report.py). Paste stats_key into the Worker's STATS_KEY secret. Never commit this file.",
        "relay": "",
        "stats_key": secrets.token_hex(32),
        "ignore_players": [],
    }
    path.write_text(json.dumps(body, indent="\t") + "\n", encoding="utf-8")
    try:
        path.chmod(0o600)
    except OSError:
        pass
    print(f"Wrote a new key to {path}. Open the file, copy stats_key and add it as the")
    print("Worker secret STATS_KEY (Settings > Variables and secrets > Add variable, tick")
    print('Secret, then "Add variable and deploy").')


def load_config(path: Path, relay_arg: str | None) -> tuple[str, str, set[str]]:
    if not path.exists():
        fail(f"no {path}; copy Docs/stats.example.json there, or run with --new-key")
    try:
        cfg = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        fail(f"can't read {path}: {e}")
    key = str(cfg.get("stats_key") or "")
    if len(key) < 16:
        fail(f"stats_key in {path} is missing or shorter than 16 characters")
    relay = relay_arg or str(cfg.get("relay") or "")
    if not relay:
        try:
            relay = json.loads(LLM_JSON.read_text(encoding="utf-8")).get("relay", "")
        except (OSError, json.JSONDecodeError):
            relay = ""
    if not relay:
        fail(f'no relay address: set "relay" in {path} or pass --relay')
    ignore = {str(p).strip().lower() for p in cfg.get("ignore_players") or [] if str(p).strip()}
    return relay.rstrip("/"), key, ignore


def fetch_events(relay: str, key: str, since: str, test: bool) -> list[dict]:
    events: list[dict] = []
    after = 0
    while True:
        query = {"after": after, "limit": PAGE, "test": "1" if test else "0"}
        if since:
            query["since"] = since
        req = urllib.request.Request(
            f"{relay}/stats?{urllib.parse.urlencode(query)}",
            headers={"authorization": f"Bearer {key}", "user-agent": USER_AGENT},
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                page = json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                fail("the relay answered not_found: the key is wrong, STATS_KEY isn't set on the relay, or the relay has no /stats yet")
            fail(f"the relay answered HTTP {e.code}: {e.read()[:300]!r}")
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            fail(f"can't read {relay}/stats: {e}")
        events.extend(page.get("events", []))
        if page.get("next") is None:
            return events
        after = page["next"]


def release_ref() -> str | None:
    """origin/main (as last fetched), else main, when the script runs in the repo; None when git can't say."""
    for ref in ("origin/main", "main"):
        try:
            proc = subprocess.run(["git", "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}"],
                                  cwd=ROOT, capture_output=True, text=True)
        except OSError:
            return None
        if proc.returncode == 0:
            return ref
    return None


def is_release(label: str, ref: str | None) -> str:
    """"yes" for a version label whose commit is on ref, "no" for any other label, "?" when git can't tell."""
    m = VERSION_LABEL.match(label)
    if not m:
        return "no"
    if ref is None:
        return "?"
    try:
        proc = subprocess.run(["git", "merge-base", "--is-ancestor", m.group("sha"), ref],
                              cwd=ROOT, capture_output=True, text=True)
    except OSError:
        return "?"
    # 0: an ancestor; 1: not one; anything else: git doesn't know the commit.
    return {0: "yes", 1: "no"}.get(proc.returncode, "?")


def build_of(e: dict) -> str:
    return str(e.get("build") or "")


def heading(text: str) -> None:
    print()
    print(f"== {text}")


def table(rows: list[list], header: list[str]) -> None:
    if not rows:
        print("  (none)")
        return
    # Numbers line up on the right, text on the left.
    right = [all(isinstance(r[i], int) for r in rows) for i in range(len(header))]
    cells = [[str(c) for c in header]] + [[str(c) for c in r] for r in rows]
    widths = [max(len(r[i]) for r in cells) for i in range(len(header))]
    for n, r in enumerate(cells):
        print("  " + "  ".join(c.rjust(widths[i]) if right[i] else c.ljust(widths[i]) for i, c in enumerate(r)).rstrip())
        if n == 0:
            print("  " + "  ".join("-" * w for w in widths))


def builds_table(events: list[dict]) -> None:
    """Players, shows and events per build, newest first (by the build's first event), with the releases marked."""
    players: dict[str, set] = defaultdict(set)
    shows: dict[str, set] = defaultdict(set)
    count: Counter = Counter()
    first: dict[str, dict] = {}
    last: dict[str, dict] = {}
    for e in sorted(events, key=lambda e: e["id"]):
        b = build_of(e)
        players[b].add(e["player"])
        if e["event"] == "show_start":
            shows[b].add(e["session"])
        count[b] += 1
        first.setdefault(b, e)
        last[b] = e
    ref = release_ref()
    heading("builds" + (f" (release: its commit is on {ref})" if ref else " (release: ? = not in the repo, so git can't tell)"))
    names = sorted(count, key=lambda b: -first[b]["id"])
    table(
        [[b or "(none)", is_release(b, ref), len(players[b]), len(shows[b]), count[b], first[b]["ts"][:10], last[b]["ts"][:10]]
         for b in names],
        ["build", "release", "players", "shows", "events", "first seen", "last seen"],
    )


def report(events: list[dict], top: int) -> None:
    def f(e: dict, name: str, default=None):
        return (e.get("fields") or {}).get(name, default)

    days = sorted({e["ts"][:10] for e in events})
    print(f"{len(events)} events" + (f", {days[0]} to {days[-1]} (UTC)" if days else ""))

    # players
    seen_days: dict[str, set] = defaultdict(set)
    launches: dict[str, int] = defaultdict(int)
    for e in events:
        seen_days[e["player"]].add(e["ts"][:10])
        if e["event"] == "launch":
            launches[e["player"]] = max(launches[e["player"]], int(f(e, "launches", 1) or 1))
    back = [p for p in seen_days if launches[p] > 1 or len(seen_days[p]) > 1]
    heading("players")
    table(
        [["players", len(seen_days)], ["came back (launches over 1, or seen on 2+ days)", len(back)]],
        ["", "count"],
    )

    builds_table(events)

    # modes
    starts = [e for e in events if e["event"] == "show_start"]
    mode_players: dict[str, set] = defaultdict(set)
    for e in events:
        # launch comes before a mode is picked, so it says nothing about the mode played.
        if e.get("mode") and e["event"] != "launch":
            mode_players[e["mode"]].add(e["player"])
    mode_shows = Counter(e.get("mode") or "(none)" for e in starts)
    heading("modes")
    names = sorted(set(mode_players) | set(mode_shows), key=lambda m: (-mode_shows.get(m, 0), m))
    table([[m, len(mode_players.get(m, ())), mode_shows.get(m, 0)] for m in names], ["mode", "players", "shows"])

    # drop-off: a show is a session with a show_start; its drop-off point is the last phase it sent.
    shows = {e["session"] for e in starts}
    by_show: dict[str, list[dict]] = defaultdict(list)
    for e in events:
        if e["session"] in shows:
            by_show[e["session"]].append(e)
    reached: dict[tuple, set] = defaultdict(set)
    order: dict[str, list[int]] = defaultdict(list)
    ended: set = set()
    last_phase: Counter = Counter()
    for s, evs in by_show.items():
        evs.sort(key=lambda e: e["id"])
        phases = [e for e in evs if e["event"] == "phase"]
        for i, e in enumerate(phases):
            name = str(f(e, "phase", "") or "(none)")
            reached[(int(f(e, "scene", 0) or 0), name)].add(s)
            order[name].append(i)
        if any(e["event"] == "show_end" for e in evs):
            ended.add(s)
        elif phases:
            p = phases[-1]
            last_phase[f"scene {f(p, 'scene', 0)}, {f(p, 'phase', '(none)')}"] += 1
        else:
            last_phase["(no phase)"] += 1
    mean = {n: sum(v) / len(v) for n, v in order.items()}
    heading(f"drop-off ({len(shows)} shows, {len(ended)} ended)")
    keys = sorted(reached, key=lambda k: (k[0], mean.get(k[1], 0), k[1]))
    table([[f"scene {sc}, {ph}", len(reached[(sc, ph)])] for sc, ph in keys], ["phase reached", "shows"])
    print()
    results = Counter((str(f(e, "result", "") or "(none)"), str(f(e, "reason", "") or "(none)")) for e in events if e["event"] == "show_end")
    table([[r, why, n] for (r, why), n in results.most_common()], ["show_end result", "reason", "shows"])
    print()
    table([[k, n] for k, n in last_phase.most_common()], ["no show_end: last phase", "shows"])

    # calls
    calls: dict[tuple, list[int]] = defaultdict(lambda: [0, 0, 0, 0])
    for e in events:
        if e["event"] == "calls":
            c = calls[(str(f(e, "provider", "") or "(none)"), str(f(e, "model", "") or "(none)"))]
            for i, name in enumerate(["calls", "failed", "tokens_in", "tokens_out"]):
                c[i] += int(f(e, name, 0) or 0)
    heading("calls")
    table(
        [[p, m, *v] for (p, m), v in sorted(calls.items(), key=lambda kv: -kv[1][0])],
        ["provider", "model", "calls", "failed", "tokens in", "tokens out"],
    )

    # errors
    heading("errors")
    errors = Counter(str(f(e, "kind", "") or "(none)") for e in events if e["event"] == "error")
    table([[k, n] for k, n in errors.most_common()], ["kind", "count"])

    # unsupported actions: the most common words, newest first among ties
    heading("unsupported actions")
    words: Counter = Counter()
    latest: dict[tuple, int] = {}
    for e in events:
        if e["event"] == "unsupported":
            k = (str(f(e, "words", "") or "").strip().lower(), str(f(e, "source", "") or ""))
            words[k] += 1
            latest[k] = e["id"]
    rows = sorted(words.items(), key=lambda kv: (-kv[1], -latest[kv[0]]))[:top]
    table([[w or "(empty)", src, n] for (w, src), n in rows], ["words", "source", "count"])
    if len(words) > top:
        print(f"  ... and {len(words) - top} more (--top)")

    off = {e["player"] for e in events if e["event"] == "analytics_off"}
    if off:
        heading("turned off")
        table([["players who turned analytics off", len(off)]], ["", "count"])


def main() -> None:
    ap = argparse.ArgumentParser(description="Report the game's analytics events from the relay.")
    ap.add_argument("--since", default="", help="only events from this UTC day on (YYYY-MM-DD)")
    ap.add_argument("--test", action="store_true", help='include "test" events')
    ap.add_argument("--build", default=None,
                    help='only events from this build (a version label such as 2026-11-20-10f8540, or "local")')
    ap.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="path to stats.json")
    ap.add_argument("--relay", default=None, help="relay address (overrides stats.json)")
    ap.add_argument("--top", type=int, default=15, help="rows in the long lists")
    ap.add_argument("--new-key", action="store_true", help="write a stats.json with a fresh key")
    args = ap.parse_args()

    if args.new_key:
        new_key(args.config)
        return
    if args.since and not (len(args.since) == 10 and args.since[4] == "-" and args.since[7] == "-"):
        fail("--since must be YYYY-MM-DD")
    if args.build is not None and not 1 <= len(args.build) <= 20:
        fail("--build must be 1 to 20 characters (a build's label, as the builds table lists it)")
    relay, key, ignore = load_config(args.config, args.relay)
    events = fetch_events(relay, key, args.since, args.test)
    # Our own machines' player ids (ignore_players in stats.json) never count.
    kept = [e for e in events if e["player"] not in ignore]
    print(f"relay: {relay}" + ("  (test events included)" if args.test else ""))
    if len(kept) < len(events):
        print(f"left out {len(events) - len(kept)} events from the {len(ignore)} ignored players in {args.config.name}")
    events = kept
    if args.build is not None:
        one = [e for e in events if build_of(e) == args.build]
        if not one:
            builds = sorted({build_of(e) or "(none)" for e in events})
            print(f"no events from build {args.build}; the builds with events are: {', '.join(builds) or 'none'}")
            return
        print(f"build: {args.build} alone ({len(one)} of {len(events)} events)")
        events = one
    report(events, args.top)


if __name__ == "__main__":
    main()
