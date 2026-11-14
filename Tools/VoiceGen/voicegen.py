#!/usr/bin/env python3
"""Take 37 voice production flow for ElevenLabs: design the voices, approve them, then batch-generate every bark.

Stage 1  design    Voice Design: generate 3 preview voices per speaker from the description in voices.json.
Stage 1b revise    Change the sound: add notes to the description and regenerate previews.
Stage 2  approve   Save the preview you like as a real ElevenLabs voice. Batch generation refuses speakers without one.
         test      Speak any line with an approved voice to check it before spending on the batch.
Stage 3  batch     Generate takes for every line in Tools/barks/DT_Barks.csv. Shows the cost first; needs --yes.
         pick      Choose the take you like; it is cleaned up and written to Art/Voice/final/<Actor>/<Name>.wav (then Tools/Editor/import_vo.py imports it into Unreal).
         status    What is designed, approved, generated and picked.

Usage (run from the repo root):
  python Tools/VoiceGen/voicegen.py design Brick
  python Tools/VoiceGen/voicegen.py design all
  python Tools/VoiceGen/voicegen.py revise Brick --notes "a bit gruffer, more Southern, less cartoonish"
  python Tools/VoiceGen/voicegen.py approve Brick r001_2
  python Tools/VoiceGen/voicegen.py test Brick "Never fear! Hardcastle's here!"
  python Tools/VoiceGen/voicegen.py batch --dry-run                  # counts lines and characters, spends nothing
  python Tools/VoiceGen/voicegen.py batch --speaker Brick --yes      # generate takes
  python Tools/VoiceGen/voicegen.py batch --tag Notice --yes         # only some tags
  python Tools/VoiceGen/voicegen.py takes                            # build Art/Voice/takes.html to audition
  python Tools/VoiceGen/voicegen.py pick VO_Brick_Notice_01 2        # keep take 2
  python Tools/VoiceGen/voicegen.py pick-all 1                       # keep take 1 everywhere you have not picked

Needs an ElevenLabs API key: environment variable ELEVENLABS_API_KEY, or the file Tools/VoiceGen/.elevenlabs_api_key
(git ignores it). It is never printed. Design previews and batch generation spend ElevenLabs credits.
Output files are 48 kHz mono WAV, trimmed and normalised to -16 LUFS when ffmpeg is installed (see voices.json settings).
Open Art/Voice/review.html to listen to previews and takes.
"""
import argparse
import base64
import csv
import html
import json
import os
import shutil
import struct
import subprocess
import sys
import urllib.error
import urllib.request
import wave
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
API = "https://api.elevenlabs.io"
OUT = REPO / "Art" / "Voice"
VO_DIR = REPO / "Art" / "Voice" / "final"
CSV_PATH = REPO / "Tools" / "barks" / "DT_Barks.csv"
CFG = json.loads((HERE / "voices.json").read_text(encoding="utf-8"))
S = CFG["settings"]


# ----------------------------------------------------------------------------- API plumbing

def api_key():
    key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not key:
        f = HERE / ".elevenlabs_api_key"
        if f.exists():
            key = f.read_text().strip()
    if not key:
        sys.exit("No ElevenLabs API key. Set ELEVENLABS_API_KEY or create Tools/VoiceGen/.elevenlabs_api_key.")
    return key


def call(path, body, binary=False):
    req = urllib.request.Request(API + path, data=json.dumps(body).encode(), method="POST", headers={
        "xi-api-key": api_key(), "Content-Type": "application/json", "User-Agent": "take37-voicegen"})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            data = r.read()
            return data if binary else json.loads(data)
    except urllib.error.HTTPError as e:
        sys.exit(f"ElevenLabs error {e.code}: {e.read().decode(errors='replace')[:800]}")


# ----------------------------------------------------------------------------- state

def state_path():
    return OUT / "state.json"


def load_state():
    p = state_path()
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {"speakers": {}, "picked": {}}


def save_state(st):
    OUT.mkdir(parents=True, exist_ok=True)
    state_path().write_text(json.dumps(st, indent=2), encoding="utf-8")
    write_review(st)


def spk_state(st, name):
    return st["speakers"].setdefault(name, {"rounds": [], "notes": [], "approved": None})


def check_speaker(name):
    if name not in CFG["speakers"]:
        sys.exit(f"Unknown speaker '{name}'. Known: {', '.join(CFG['speakers'])}")


def full_description(name, notes):
    d = CFG["speakers"][name]["description"]
    if notes:
        d += " Adjustments: " + "; ".join(notes) + "."
    return d[:1000]


# ----------------------------------------------------------------------------- stage 1: design

def run_design(name):
    check_speaker(name)
    st = load_state()
    ss = spk_state(st, name)
    sp = CFG["speakers"][name]
    idx = len(ss["rounds"]) + 1
    desc = full_description(name, ss["notes"])
    print(f"[{name}] round {idx}: designing previews (spends credits)...")
    res = call("/v1/text-to-voice/design", {
        "voice_description": desc, "model_id": S["design_model"], "text": sp["sample"]})
    files, ids = [], {}
    for k, prev in enumerate(res.get("previews", []), 1):
        fname = f"r{idx:03d}_{k}.mp3"
        p = OUT / "design" / name / fname
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(base64.b64decode(prev["audio_base_64"]))
        files.append(fname)
        ids[fname[:-4]] = prev["generated_voice_id"]
    ss["rounds"].append({"round": idx, "description": desc, "files": files, "voice_ids": ids,
                         "time": datetime.now(timezone.utc).isoformat()})
    save_state(st)
    print(f"[{name}] saved {', '.join(files)}  (listen in {OUT / 'review.html'})")


def cmd_design(a):
    for n in (CFG["speakers"] if a.speaker == "all" else [a.speaker]):
        run_design(n)


def cmd_revise(a):
    check_speaker(a.speaker)
    st = load_state()
    ss = spk_state(st, a.speaker)
    ss["notes"] += [n.strip() for n in a.notes.split(";") if n.strip()]
    save_state(st)
    run_design(a.speaker)


# ----------------------------------------------------------------------------- stage 2: approve and test

def cmd_approve(a):
    check_speaker(a.speaker)
    st = load_state()
    ss = spk_state(st, a.speaker)
    gen_id = None
    for r in ss["rounds"]:
        if a.preview in r["voice_ids"]:
            gen_id, desc = r["voice_ids"][a.preview], r["description"]
    if not gen_id:
        sys.exit(f"No such preview '{a.preview}'. See 'status'.")
    res = call("/v1/text-to-voice", {"voice_name": f"Take37 {a.speaker}", "voice_description": desc[:1000],
                                     "generated_voice_id": gen_id})
    ss["approved"] = {"preview": a.preview, "voice_id": res["voice_id"], "time": datetime.now(timezone.utc).isoformat()}
    save_state(st)
    print(f"Approved {a.speaker} -> voice {res['voice_id']}. Batch generation is now allowed for this speaker.")


def approved_voice(st, name):
    v = st["speakers"].get(name, {}).get("approved")
    if not v:
        sys.exit(f"{name} has no approved voice. Run design, then approve.")
    return v["voice_id"]


def voice_settings(intensity):
    """Louder, more intense lines get a looser, more expressive delivery."""
    intensity = int(intensity)
    stab = {1: 0.55, 2: 0.4, 3: 0.28}.get(intensity, 0.4)
    return {"stability": stab, "similarity_boost": 0.8, "style": 0.35 if intensity >= 2 else 0.15, "use_speaker_boost": True}


def tts_text(text, delivery):
    """eleven_v3 treats [bracketed] text as a performance direction, not speech. Other models would read it aloud."""
    if S.get("use_delivery_tags") and S["tts_model"] == "eleven_v3" and delivery:
        direction = delivery.split(";")[0].strip().lower()
        return f"[{direction}] {text}"
    return text


def speak(voice_id, text, intensity=2):
    body = {"text": text, "model_id": S["tts_model"], "voice_settings": voice_settings(intensity)}
    return call(f"/v1/text-to-speech/{voice_id}?output_format={S['output_format']}", body, binary=True)


def pcm_to_wav(pcm, path, rate):
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(pcm)


def out_rate():
    fmt = S["output_format"]
    return int(fmt.split("_")[1]) if fmt.startswith("pcm_") else 24000


def cmd_test(a):
    check_speaker(a.speaker)
    st = load_state()
    audio = speak(approved_voice(st, a.speaker), tts_text(a.text, a.delivery), a.intensity)
    p = OUT / "tests" / f"{a.speaker}_{datetime.now().strftime('%H%M%S')}.wav"
    pcm_to_wav(audio, p, out_rate())
    print(f"saved {p}")


# ----------------------------------------------------------------------------- stage 3: batch

def read_lines():
    with open(CSV_PATH, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def take_dir(name):
    return OUT / "takes" / name


def cmd_batch(a):
    st = load_state()
    rows = read_lines()
    if a.speaker:
        rows = [r for r in rows if r["Actor"] == a.speaker]
    if a.tag:
        rows = [r for r in rows if r["Tag"] == a.tag]
    todo = []
    for r in rows:
        have = len(list(take_dir(r["Name"]).glob("take_*.wav"))) if take_dir(r["Name"]).exists() else 0
        if have < a.takes:
            todo.append((r, a.takes - have))
    chars = sum(len(tts_text(r["Subtitle"], r["Delivery"])) * n for r, n in todo)
    speakers = sorted({r["Actor"] for r, _ in todo})
    print(f"{len(todo)} lines need takes, {sum(n for _, n in todo)} generations, about {chars:,} characters of credits.")
    print("speakers:", ", ".join(f"{s} ({'approved' if st['speakers'].get(s, {}).get('approved') else 'NOT APPROVED'})" for s in speakers))
    if a.dry_run or not todo:
        return
    if not a.yes:
        sys.exit("This spends ElevenLabs credits. Re-run with --yes.")
    for s in speakers:
        approved_voice(st, s)
    for r, n in todo:
        d = take_dir(r["Name"])
        start = len(list(d.glob("take_*.wav"))) + 1 if d.exists() else 1
        for k in range(start, start + n):
            audio = speak(approved_voice(st, r["Actor"]), tts_text(r["Subtitle"], r["Delivery"]), r["Intensity"])
            pcm_to_wav(audio, d / f"take_{k}.wav", out_rate())
            print(f"  {r['Name']} take {k}")
    write_review(st)
    print("Done. Listen in", OUT / "review.html", "then 'pick' or 'pick-all'.")


def clean_to(src, dst):
    """Trim silence, normalise loudness and write 48 kHz mono WAV. Needs ffmpeg for loudness; otherwise just copies."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    ff = shutil.which("ffmpeg")
    if not ff:
        shutil.copy2(src, dst)
        return False
    pad = S["trim_silence_ms"] / 1000.0
    filt = (f"silenceremove=start_periods=1:start_threshold=-50dB:start_silence={pad},"
            f"areverse,silenceremove=start_periods=1:start_threshold=-50dB:start_silence={pad},areverse,"
            f"loudnorm=I={S['target_lufs']}:TP=-1.5:LRA=11")
    r = subprocess.run([ff, "-y", "-loglevel", "error", "-i", str(src), "-af", filt, "-ar", "48000", "-ac", "1", str(dst)])
    if r.returncode != 0:
        shutil.copy2(src, dst)
        return False
    return True


def pick(name, take, st):
    row = next((r for r in read_lines() if r["Name"] == name), None)
    if not row:
        sys.exit(f"No such line {name}")
    src = take_dir(name) / f"take_{take}.wav"
    if not src.exists():
        sys.exit(f"No such take: {src}")
    dst = VO_DIR / row["Actor"] / f"{name}.wav"
    ok = clean_to(src, dst)
    st["picked"][name] = take
    return ok


def cmd_pick(a):
    st = load_state()
    ok = pick(a.name, a.take, st)
    save_state(st)
    print(f"{a.name}: take {a.take} -> Art/Voice/final/ ({'normalised' if ok else 'copied; install ffmpeg to normalise'})")


def cmd_pick_all(a):
    st = load_state()
    n = 0
    for r in read_lines():
        if r["Name"] in st["picked"] or not (take_dir(r["Name"]) / f"take_{a.take}.wav").exists():
            continue
        pick(r["Name"], a.take, st)
        n += 1
    save_state(st)
    print(f"picked take {a.take} for {n} lines. Import them into Unreal with Tools/Editor/import_vo.py.")


def cmd_status(a):
    st = load_state()
    rows = read_lines()
    for name, sp in CFG["speakers"].items():
        ss = st["speakers"].get(name, {})
        mine = [r for r in rows if r["Actor"] == name]
        gen = sum(1 for r in mine if take_dir(r["Name"]).exists())
        picked = sum(1 for r in mine if r["Name"] in st["picked"])
        appr = ss.get("approved", {}).get("preview", "-") if ss.get("approved") else "-"
        print(f"{name:9s} rounds={len(ss.get('rounds', [])):2d} approved={appr:8s} lines={len(mine):3d} generated={gen:3d} picked={picked:3d}")
    print("\nreview page:", OUT / "review.html")


# ----------------------------------------------------------------------------- review page

def audio_tag(path):
    return f"<audio controls preload='none' src='data:audio/{'mpeg' if path.suffix == '.mp3' else 'wav'};base64," \
           + base64.b64encode(path.read_bytes()).decode() + "'></audio>"


def write_review(st):
    parts = []
    for name, sp in CFG["speakers"].items():
        ss = st["speakers"].get(name)
        if not ss or not ss["rounds"]:
            continue
        parts.append(f"<h2>{html.escape(sp['label'])}</h2><p class='d'>{html.escape(ss['rounds'][-1]['description'])}</p>")
        if ss.get("approved"):
            parts.append(f"<p class='ok'>Approved: {ss['approved']['preview']}</p>")
        for r in ss["rounds"]:
            parts.append(f"<h3>Round {r['round']}</h3><div class='row'>")
            for f in r["files"]:
                stem = f[:-4]
                parts.append(f"<figure><b>{stem}</b>{audio_tag(OUT / 'design' / name / f)}"
                             f"<code>voicegen.py approve {name} {stem}</code></figure>")
            parts.append("</div>")
    page = ("<!doctype html><meta charset='utf-8'><title>Take 37 voices</title><style>"
            "body{font-family:Georgia,serif;background:#fbf4de;color:#1c1a1f;margin:24px}"
            ".row{display:flex;gap:14px;flex-wrap:wrap}figure{margin:0;background:#fff;padding:10px;border:3px solid #1c1a1f;"
            "box-shadow:6px 6px 0 #1c1a1f;display:flex;flex-direction:column;gap:6px}.d{color:#6b6150;max-width:900px}"
            ".ok{color:#1a9b4d;font-weight:bold}code{font-size:.8em}</style><h1>Take 37 voice review</h1>" + "\n".join(parts))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "review.html").write_text(page, encoding="utf-8")


def write_takes_page():
    """Audition page for generated takes, grouped by speaker, with the text, delivery note and pick commands."""
    rows = [r for r in read_lines() if take_dir(r["Name"]).exists()]
    parts = []
    for name in CFG["speakers"]:
        mine = [r for r in rows if r["Actor"] == name]
        if not mine:
            continue
        parts.append(f"<h2>{html.escape(CFG['speakers'][name]['label'])}</h2>")
        for r in mine:
            takes = sorted(take_dir(r["Name"]).glob("take_*.wav"))
            players = "".join(f"<div><small>take {t.stem.split('_')[1]}</small>{audio_tag(t)}</div>" for t in takes)
            parts.append(f"<div class='line'><b>{html.escape(r['Subtitle'])}</b> <small>{r['Name']} | {html.escape(r['Delivery'])}</small>"
                         f"<div class='row'>{players}</div><code>voicegen.py pick {r['Name']} N</code></div>")
    page = ("<!doctype html><meta charset='utf-8'><title>Take 37 takes</title><style>"
            "body{font-family:Georgia,serif;background:#fbf4de;color:#1c1a1f;margin:24px}.line{background:#fff;border:3px solid #1c1a1f;"
            "padding:8px 12px;margin:10px 0;max-width:900px}.row{display:flex;gap:16px;flex-wrap:wrap;margin:4px 0}"
            "small{color:#7a6f55}code{font-size:.75em}</style><h1>Take 37 takes</h1>" + "".join(parts))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "takes.html").write_text(page, encoding="utf-8")
    return OUT / "takes.html"


def cmd_takes(a):
    print("saved", write_takes_page())


# ----------------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sp = sub.add_parser("design"); sp.add_argument("speaker"); sp.set_defaults(fn=cmd_design)
    sp = sub.add_parser("revise"); sp.add_argument("speaker"); sp.add_argument("--notes", required=True); sp.set_defaults(fn=cmd_revise)
    sp = sub.add_parser("approve"); sp.add_argument("speaker"); sp.add_argument("preview"); sp.set_defaults(fn=cmd_approve)
    sp = sub.add_parser("test"); sp.add_argument("speaker"); sp.add_argument("text"); sp.add_argument("--intensity", type=int, default=2)
    sp.add_argument("--delivery", default="", help="performance note, as in the CSV Delivery column")
    sp.set_defaults(fn=cmd_test)
    sp = sub.add_parser("batch"); sp.add_argument("--speaker"); sp.add_argument("--tag"); sp.add_argument("--takes", type=int, default=S["takes_per_line"])
    sp.add_argument("--dry-run", action="store_true"); sp.add_argument("--yes", action="store_true"); sp.set_defaults(fn=cmd_batch)
    sp = sub.add_parser("pick"); sp.add_argument("name"); sp.add_argument("take", type=int); sp.set_defaults(fn=cmd_pick)
    sp = sub.add_parser("pick-all"); sp.add_argument("take", type=int); sp.set_defaults(fn=cmd_pick_all)
    sp = sub.add_parser("takes"); sp.set_defaults(fn=cmd_takes)
    sp = sub.add_parser("status"); sp.set_defaults(fn=cmd_status)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
