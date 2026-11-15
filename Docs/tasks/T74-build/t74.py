"""T74: drive the T74 editor (its own MCP port, 8011) to dress the stage and capture the doc's shots.

Written by the T74 prep; the editor parts are NOT RUN. `python t74.py selftest` runs without an editor
(it checks the camera math on a made-up dress.json) and was run by the prep.

Python 3.10+, standard library only. Run it from Git Bash in the T74 worktree:
    python Docs/tasks/T74-build/t74.py check              # MCP answers on the port; console box found
    python Docs/tasks/T74-build/t74.py dress space_plans  # dress only, print dress.json
    python Docs/tasks/T74-build/t74.py house space_plans  # dress + the house shot of one card
    python Docs/tasks/T74-build/t74.py cast space_plans   # dress + five close-ups + the labeled strip
    python Docs/tasks/T74-build/t74.py details            # dress + the two stage close-ups, side by side
    python Docs/tasks/T74-build/t74.py all                # the seven house shots, then the cast and details
Options: --port 8011 (never 8000: that is the other session's editor), --no-warm (one render per shot),
--pie (with `dress` only: dress the running PIE world, for the sheet's fallback B).

Everything lands in <worktree>/Saved/T74/ (not in git): raw/ (the viewport captures as they came),
shots/ (cropped: house_<card>.png 1920x1080, bot_<seat>.png 900x1200, cast_<card>.png,
proscenium.png, chandelier.png, stage_details_<card>.png) and
shots/manifest.json (card, roles, cameras, for the doc's alt text).
"""
import base64
import json
import math
import os
import re
import struct
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
WORK = ROOT / "Saved" / "T74"
RAW, SHOTS = WORK / "raw", WORK / "shots"
SCENES = ROOT / "Content" / "NHOS" / "Data" / "scenes.json"
T47_SEATS = ROOT / "Docs" / "tasks" / "T47-build" / "scenes_seats.json"
CAST_CARD = "space_plans"  # my person's pick (2026-11-15): the Space saga on both Art Inspiration pictures
SEAT_KEYS = {"visionary": "openai", "worrier": "anthropic", "overclocker": "spacexai", "copycat": "meta", "human": "you"}
HOUSE_DEFAULT = {"loc": [-1050.0, 0.0, 330.0], "rot": [-20.0, 0.0, 0.0], "fov": 90.0}
CLOSE_HFOV = 34.0  # the 2026-11-15 close-ups' horizontal FOV, for a 3:4 tile
ANNOT = {"gridSpacing": 0, "gridExtent": 0, "gridHeight": 0, "maxLabelDistance": 0,
         "classFilter": {"refPath": "/Script/Engine.StaticMeshActor"}, "maxLabels": 0}  # T43, T46: required even unused

PORT = 8011
WARM = True
PIE = False  # --pie: dress the running PIE world (the sheet's fallback B); captures then come from the PIE window


# ---------------------------------------------------------------- MCP (JSON-RPC over HTTP, port 8011 only)
def _post(payload, sid=None):
    req = urllib.request.Request("http://127.0.0.1:%d/mcp" % PORT, data=json.dumps(payload).encode(), method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json, text/event-stream")
    if sid:
        req.add_header("Mcp-Session-Id", sid)
    with urllib.request.urlopen(req, timeout=600) as r:
        body, new_sid = r.read().decode("utf-8", "replace"), r.headers.get("Mcp-Session-Id")
    if body.startswith(("event:", "data:")):
        lines = [l[5:].strip() for l in body.splitlines() if l.startswith("data:")]
        body = lines[-1] if lines else ""
    return (json.loads(body) if body.strip() else None), new_sid


def _session(fresh=False):
    f = WORK / ("sid_%d.txt" % PORT)
    if f.exists() and not fresh:
        return f.read_text().strip()
    _, sid = _post({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
        "protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "t74-capture", "version": "1"}}})
    _post({"jsonrpc": "2.0", "method": "notifications/initialized"}, sid)
    f.write_text(sid or "")
    return sid


def call_tool(toolset, tool, args):
    """call_tool, the server's one tool that runs others. Toolset names are the full ones
    (SlateInspectorToolset.SlateInspectorToolset, EditorToolset.EditorAppToolset)."""
    payload = {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {
        "name": "call_tool", "arguments": {"toolset_name": toolset, "tool_name": tool, "arguments": args}}}
    try:
        res, _ = _post(payload, _session())
    except urllib.error.HTTPError:  # an old session id after an editor restart
        res, _ = _post(payload, _session(fresh=True))
    if res is None or "error" in res:
        raise SystemExit("%s.%s failed: %s" % (toolset, tool, json.dumps(res)[:800]))
    return res["result"]


def _text(result):
    return "".join(c.get("text", "") for c in result.get("content", []) if c.get("type") == "text")


# ---------------------------------------------------------------- editor Python through the console box (T46's way)
def console_ref():
    t = _text(call_tool("SlateInspectorToolset.SlateInspectorToolset", "Snapshot", {"ref": "", "maxDepth": 60}))
    try:
        t = json.loads(t)["returnValue"]
    except Exception:
        pass
    lines = t.split("\n")
    for k, l in enumerate(lines):
        if 'text "Cmd"' in l:
            for l2 in lines[k + 1:k + 6]:
                m = re.search(r"textbox .*\[ref=(\w+)\]", l2)
                if m:
                    return m.group(1)
    raise SystemExit('console box not found: no textbox after text "Cmd" in the Snapshot')


def pyrun(script, done, timeout=180):
    """Type `py "<script>"` into the console box and wait for the script's done file."""
    done = Path(done)
    if done.exists():
        done.unlink()
    call_tool("SlateInspectorToolset.SlateInspectorToolset", "Type",
              {"ref": console_ref(), "text": 'py "%s"' % str(script).replace("\\", "/"), "submit": True})
    t0 = time.time()
    while not done.exists():
        if time.time() - t0 > timeout:
            raise SystemExit("timed out waiting for %s (read the T74 editor's log)" % done)
        time.sleep(0.5)
    time.sleep(0.3)
    return json.loads(done.read_text(encoding="utf-8"))


# ---------------------------------------------------------------- images
def png_size(data):
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("the capture is not a PNG")
    return struct.unpack(">II", data[16:24])


def _image_b64(result):
    for c in result.get("content", []):
        if c.get("type") == "image" and c.get("data"):
            return c["data"]
    sc = result.get("structuredContent") or {}
    try:
        return sc["returnValue"]["image"]["data"]
    except Exception:
        pass
    m = re.search(r'"data"\s*:\s*"([A-Za-z0-9+/=]{1000,})"', _text(result))
    if m:
        return m.group(1)
    raise SystemExit("no image in the CaptureViewport result: " + _text(result)[:500])


def full_fov(hfov, aspect, w, h):
    """The viewport FOV that gives the centered w:h crop a horizontal FOV of hfov.
    The viewport is wider than the frame (2.4:1 to 2.9:1 on this PC), so the crop is its full height."""
    a = w / h
    frac = a / aspect if aspect > a else 1.0  # the crop's share of the viewport's width
    return 2 * math.degrees(math.atan(math.tan(math.radians(hfov / 2)) / frac))


def crop(raw, out, w, h):
    subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(HERE / "crop.ps1"),
                    "-In", str(raw), "-Out", str(out), "-W", str(w), "-H", str(h)], check=True)


def viewport_aspect():
    f = WORK / "viewport.json"
    if f.exists():
        return json.loads(f.read_text())["aspect"]
    data = base64.b64decode(_image_b64(call_tool("EditorToolset.EditorAppToolset", "CaptureViewport", {"annotations": ANNOT, "bShowUI": False})))
    W, H = png_size(data)
    f.write_text(json.dumps({"w": W, "h": H, "aspect": W / H}))
    print("viewport capture %dx%d" % (W, H))
    return W / H


def capture(name, loc, rot, hfov, w, h):
    aspect = viewport_aspect()
    json.dump({"fov": full_fov(hfov, aspect, w, h)}, open(WORK / "fov.json", "w"))
    pyrun(HERE / "setfov.py", WORK / "fov.done", timeout=30)
    args = {"captureTransform": {"location": dict(zip("xyz", loc)), "rotation": {"pitch": rot[0], "yaw": rot[1], "roll": 0},
                                 "scale": {"x": 1, "y": 1, "z": 1}}, "annotations": ANNOT, "bShowUI": False}
    for _ in range(2 if WARM else 1):  # the first render can come out before Lumen settles
        data = base64.b64decode(_image_b64(call_tool("EditorToolset.EditorAppToolset", "CaptureViewport", args)))
    W, H = png_size(data)
    if abs(W / H - aspect) > 0.01:
        raise SystemExit("the viewport changed shape (%dx%d); delete %s and run again" % (W, H, WORK / "viewport.json"))
    raw = RAW / (name + ".png")
    raw.write_bytes(data)
    out = SHOTS / (name + ".png")
    crop(raw, out, w, h)
    return out


# ---------------------------------------------------------------- dressing and shots
def dress(card):
    seats = json.loads(T47_SEATS.read_text(encoding="utf-8")) if T47_SEATS.exists() else {}
    json.dump({"card": card, "seats": seats, "world": "pie" if PIE else "editor"}, open(WORK / "spec.json", "w", encoding="utf-8"), indent=1)
    d = pyrun(HERE / "dress.py", WORK / "dress.json", timeout=120)
    print("dress %s: ok=%s" % (card, d["ok"]))
    for e in d["errors"]:
        print("  !", e.strip()[:400])
    for c in d.get("cast", []):
        print("  %-9s %-36s %-20s %s hat=%s" % (c["provider"], c["role"], c["headpiece"], c["color"], c["hat_ok"]))
    if any("Traceback" in e for e in d["errors"]):
        raise SystemExit("dress.py failed: read the error above")
    return d


def house(card, d=None):
    d = d or dress(card)
    cam = d.get("camera") or HOUSE_DEFAULT
    out = capture("house_" + card, cam["loc"], cam["rot"], cam["fov"], 1920, 1080)
    print("house", card, "->", out)
    return {"card": card, "file": str(out), "camera": cam, "cast": d.get("cast", []), "props": d.get("props", [])}


def close_cams(robots, hfov=CLOSE_HFOV, w=900, h=1200, floor=-8.0, headroom=12.0, side=20.0):
    """One camera per robot, all at the same distance and height so the five share one scale:
    front on (along the robot's own forward vector), pitch 0, framing the floor to the tallest
    visible part (a topper over a hat) plus headroom."""
    top = max(r["top"] for r in robots) + headroom
    half = max(r["half_width"] for r in robots) + side
    vf = 2 * math.atan(math.tan(math.radians(hfov / 2)) * h / w)
    dist = max((top - floor) / 2 / math.tan(vf / 2), half / math.tan(math.radians(hfov / 2)), 250.0)
    z = (top + floor) / 2
    cams = []
    for r in robots:
        fx, fy = r["fwd"]
        n = math.hypot(fx, fy) or 1.0
        fx, fy = fx / n, fy / n
        yaw = math.degrees(math.atan2(-fy, -fx))
        cams.append({"persona": r["persona"], "provider": r["provider"],
                     "loc": [r["loc"][0] + fx * dist, r["loc"][1] + fy * dist, z], "rot": [0.0, yaw, 0.0], "fov": hfov})
    return cams, dist


def cast(card=CAST_CARD, d=None):
    d = d or dress(card)
    cams, dist = close_cams(d["robots"])
    print("close-ups from %.0f cm, at z %.0f" % (dist, cams[0]["loc"][2]))
    for c in cams:
        capture("bot_" + SEAT_KEYS[c["persona"]], c["loc"], c["rot"], c["fov"], 900, 1200)
    roles = {c["persona"]: re.sub(r"^(A|An|The) ", "", c["role"]) for c in d.get("cast", [])}
    order = ["visionary", "worrier", "overclocker", "copycat", "human"]
    out = SHOTS / ("cast_%s.png" % card)
    subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(HERE / "cast.ps1"),
                    "-Dir", str(SHOTS), "-Out", str(out), "-Roles", ",".join(roles.get(p, "") for p in order)], check=True)
    print("cast ->", out)
    return {"card": card, "file": str(out), "cameras": cams, "cast": d.get("cast", [])}


# The 2026-11-15 close-up cameras (that session's list2.json): a cherub and the left boxes, and the chandelier.
DETAIL_CAMS = [
    {"name": "proscenium", "loc": [-820.0, -150.0, 230.0], "rot": [-5.495, -41.0995, 0.0], "fov": 58.0, "w": 1600, "h": 1000},
    {"name": "chandelier", "loc": [-820.0, 60.0, 300.0], "rot": [17.8748, -10.6197, 0.0], "fov": 42.0, "w": 1200, "h": 1000},
]


def details(card=CAST_CARD, d=None):
    """The stage close-ups, on the cast card's stage (my person's call, 2026-11-15: re-shoot them too)."""
    d = d or dress(card)
    for c in DETAIL_CAMS:
        capture(c["name"], c["loc"], c["rot"], c["fov"], c["w"], c["h"])
    out = SHOTS / ("stage_details_%s.png" % card)
    subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(HERE / "details.ps1"),
                    "-A", str(SHOTS / "proscenium.png"), "-B", str(SHOTS / "chandelier.png"), "-Out", str(out)], check=True)
    print("details ->", out)
    return {"card": card, "file": str(out), "cameras": DETAIL_CAMS}


def selftest():
    """No editor: the camera math on the robots' 2026-11-15 places (T79-build part 5)."""
    places = [("visionary", -50, -330, 161.7), ("worrier", -12, -165, 171.0), ("overclocker", -12, 165, -171.0),
              ("copycat", -50, 330, -161.7), ("human", 0, 0, 180.0)]
    robots = [{"persona": p, "provider": SEAT_KEYS[p], "loc": [x, y, 0], "yaw": yw,
               "fwd": [math.cos(math.radians(yw)), math.sin(math.radians(yw))], "top": 262.0 if p == "visionary" else 215.0,
               "half_width": 48.0} for p, x, y, yw in places]
    cams, dist = close_cams(robots)
    for c in cams:
        print("%-12s loc (%.1f, %.1f, %.1f) yaw %.1f" % (c["persona"], *c["loc"], c["rot"][1]))
    print("distance %.1f" % dist)
    for vw, vh in ((3376, 1166), (2799, 1166), (1600, 900)):
        print("viewport %dx%d: house fov %.1f, close-up fov %.1f" % (vw, vh, full_fov(90, vw / vh, 1920, 1080), full_fov(CLOSE_HFOV, vw / vh, 900, 1200)))
    # the 2026-11-15 run: viewport 3376x1166, house 16:9 at 90 -> 116.9 (vcap.py did the same sum)
    assert abs(full_fov(90, 3376 / 1166, 1920, 1080) - 116.9) < 0.1
    # Robot0's camera faces it: yaw 161.7 - 180 = -18.3 (the 2026-11-15 bot_openai shot)
    assert abs(cams[0]["rot"][1] - (-18.3)) < 0.01
    print("selftest ok")


def main(argv):
    global PORT, WARM, PIE
    if "--pie" in argv:
        PIE = True
        argv.remove("--pie")
    if "--port" in argv:
        i = argv.index("--port")
        PORT = int(argv[i + 1])
        del argv[i:i + 2]
    if "--no-warm" in argv:
        WARM = False
        argv.remove("--no-warm")
    if PORT == 8000:
        raise SystemExit("port 8000 is the editor another session drives; T74 uses its own (8011)")
    if not argv or argv[0] == "selftest":
        return selftest()
    for p in (WORK, RAW, SHOTS):
        p.mkdir(parents=True, exist_ok=True)
    cmd, rest = argv[0], argv[1:]
    if cmd == "check":
        print("console box:", console_ref())
        print("viewport aspect: %.3f" % viewport_aspect())
    elif cmd == "dress":
        print(json.dumps(dress(rest[0]), indent=1)[:4000])
    elif cmd == "house":
        print(json.dumps(house(rest[0]), indent=1)[:2000])
    elif cmd == "cast":
        print(json.dumps(cast(rest[0] if rest else CAST_CARD), indent=1)[:2000])
    elif cmd == "details":
        print(json.dumps(details(rest[0] if rest else CAST_CARD), indent=1)[:2000])
    elif cmd == "all":
        cards = [c["id"] for c in json.loads(SCENES.read_text(encoding="utf-8"))["cards"]]
        man = {"houses": [house(c) for c in cards if c != CAST_CARD]}
        d = dress(CAST_CARD)  # the cast card last, so its house shot, close-ups and cast share one dressing
        man["houses"].append(house(CAST_CARD, d))
        man["cast"] = cast(CAST_CARD, d)
        man["details"] = details(CAST_CARD, d)
        (SHOTS / "manifest.json").write_text(json.dumps(man, indent=1), encoding="utf-8")
        print("manifest ->", SHOTS / "manifest.json")
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
