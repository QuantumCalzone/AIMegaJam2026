"""T96: Leonardo candidates and edits for the costumes, with each call's cost logged. Standard library only.

  python Docs/Art/Costumes/gen.py cand <costume id> [...] [--count 2] [--force]
      One lucid-origin generation of --count images at 1024 x 1024 per costume, into
      Docs/Art/Costumes/<costume>/candidate_N.png, converted to real PNGs (Leonardo serves JPEG data
      under a .png name). --force renames earlier candidates r<round>_candidate_N.png first.
  python Docs/Art/Costumes/gen.py edit --out DIR --image SRC.png --prompt "..." [--ref R.png ...] [--count 1]
      Tools/art_gen.py edit (gemini-2.5-flash-image), then the takes converted to real PNGs.
  python Docs/Art/Costumes/gen.py sheet <costume id> [...] --out OUT.png
      A contact sheet of the costumes' candidates, one column per costume (Docs/Art/Props/sheet.swift).

Every paid call reads the Leonardo API balance before and after and logs both in log.json, with the
nominal cost (8.5 per lucid-origin image at 1024 x 1024, 26 per edited image). Other tasks spend from the
same balance at the same time, so the README counts the nominal cost. The key is read by
Tools/art_gen.py from Local/leonardo_key.json and never printed.
"""
import argparse
import fcntl
import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "Tools"))
import art_gen  # noqa: E402

P = json.loads((HERE / "prompts.json").read_text(encoding="utf-8"))
LOG = HERE / "log.json"


def balance():
    r = art_gen.call("GET", f"{art_gen.LEO}/v1/me", art_gen.key("leonardo"))
    return ((r.get("user_details") or [{}])[0]).get("apiPaidTokens")


def to_png(files):
    for f in files:
        subprocess.run(["sips", "-s", "format", "png", str(f), "--out", str(f)], check=True, capture_output=True)


def add_log(entry):
    with open(HERE / ".log.lock", "w") as lock:   # several edits run at once (fit.py)
        fcntl.flock(lock, fcntl.LOCK_EX)
        entries = json.loads(LOG.read_text(encoding="utf-8")) if LOG.exists() else []
        entries.append(entry)
        LOG.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def rel(p):
    return str(Path(p).resolve().relative_to(ROOT))


def cmd_cand(a):
    for cid in a.ids:
        c = P["costumes"][cid]
        d = HERE / cid
        d.mkdir(exist_ok=True)
        old = sorted(d.glob("candidate_*.png"))
        if old and not a.force:
            print(f"{cid}: has candidates, skipped")
            continue
        rnd = 1 + len({f.name.split("_")[0] for f in d.glob("r*_candidate_*.png")})
        for f in old:
            f.rename(d / f"r{rnd}_{f.name}")
        prompt = f"{P['style']} {c['subject']} {P['ref_suffix']}"
        neg = [w.strip() for w in P["negative"].split(",") if w.strip() not in c.get("drop", [])]
        negative = ", ".join(neg + ([c["extra_negative"]] if c.get("extra_negative") else []))
        before = balance()
        e = art_gen.leonardo(prompt, d, "lucid-origin", 1024, 1024, a.count, negative, label=cid)
        after = balance()
        files = sorted(d.glob("candidate_*.png"))
        to_png(files)
        add_log({"time": art_gen.now(), "kind": "candidates", "costume": cid, "round": rnd,
                 "generation": e.get("generation") or e.get("generationId"), "seed": e.get("seed"),
                 "model": "lucid-origin", "size": [1024, 1024], "count": a.count, "prompt": prompt,
                 "negative": negative, "files": [rel(f) for f in files], "nominal_cost": 8.5 * a.count,
                 "balance_before": before, "balance_after": after})
        print(f"{cid}: {len(files)} candidates, balance {before} -> {after}")


def cmd_edit(a):
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    before = balance()
    cmd = [sys.executable, str(ROOT / "Tools/art_gen.py"), "edit", "--out", str(out), "--image", a.image,
           "--prompt", a.prompt, "--count", str(a.count)]
    for r in a.ref:
        cmd += ["--ref", r]
    subprocess.run(cmd, check=True)
    after = balance()
    files = sorted(out.glob("edit_*.png"))
    to_png(files)
    gen = json.loads((out / "edit.json").read_text(encoding="utf-8"))
    last = gen[-1] if isinstance(gen, list) else gen
    add_log({"time": art_gen.now(), "kind": "edit", "out": rel(out), "generation": last.get("generation"),
             "source": rel(a.image), "refs": [rel(r) for r in a.ref], "count": a.count, "prompt": a.prompt,
             "files": [rel(f) for f in files], "nominal_cost": 26 * a.count,
             "balance_before": before, "balance_after": after})
    print(f"edit: {len(files)} takes in {rel(out)}, balance {before} -> {after}")


def cmd_sheet(a):
    rows = max(len(list((HERE / cid).glob("candidate_*.png"))) for cid in a.ids)
    args = []
    for cid in a.ids:
        files = sorted((HERE / cid).glob("candidate_*.png"))
        args += [P["costumes"][cid]["name"]] + [str(f) for f in files] + ["-"] * (rows - len(files))
    subprocess.run(["swift", str(ROOT / "Docs/Art/Props/sheet.swift"), a.out, str(rows)] + args, check=True)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("cand")
    c.add_argument("ids", nargs="+")
    c.add_argument("--count", type=int, default=2)
    c.add_argument("--force", action="store_true")
    e = sub.add_parser("edit")
    e.add_argument("--out", required=True)
    e.add_argument("--image", required=True)
    e.add_argument("--prompt", required=True)
    e.add_argument("--ref", action="append", default=[])
    e.add_argument("--count", type=int, default=1)
    s = sub.add_parser("sheet")
    s.add_argument("ids", nargs="+")
    s.add_argument("--out", required=True)
    a = ap.parse_args()
    {"cand": cmd_cand, "edit": cmd_edit, "sheet": cmd_sheet}[a.cmd](a)


if __name__ == "__main__":
    main()
