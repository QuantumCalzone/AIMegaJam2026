"""T97: Leonardo candidates for one card's props, and its contact sheet. Standard library only.

  python Docs/Art/Props/gen.py card <card id> [--props ID ...] [--count 2] [--force]
      For each prop of the card (or only --props), one lucid-origin generation of --count images at
      1024 x 1024 into Docs/Art/Props/<card>/<prop>/, converted to real PNGs (Leonardo serves JPEG data
      under a .png name). Skips a prop that already has candidates unless --force, which
      renames the old ones r<round>_candidate_N.png. Reads the Leonardo
      API balance before and after each call and logs the difference as its cost in log.json.
  python Docs/Art/Props/gen.py sheet <card id> [--rows N]
      Docs/Art/Props/<card>/sheet.png: the card's candidates, one column per prop.
  python Docs/Art/Props/gen.py approved
      <card>/approved.png: each card's four approved props with their sizes (concept.png where a prop has one,
      else model_view.png), and approved.png: the seven strips stacked, card order as in prompts.json.

Prompts are in prompts.json. The key is read by Tools/art_gen.py from Local/leonardo_key.json, never printed.
"""
import argparse
import json
import subprocess
import sys
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


def candidates(d):
    return sorted(d.glob("candidate_*.png"))


def cmd_card(a):
    card = P["cards"][a.card]
    entries = json.loads(LOG.read_text(encoding="utf-8")) if LOG.exists() else []
    for pid, prop in card.items():
        if a.props and pid not in a.props:
            continue
        d = HERE / a.card / pid
        if candidates(d) and not a.force:
            print(f"{pid}: has candidates, skipped")
            continue
        rnd = 1 + len({f.name.split("_")[0] for f in d.glob("r*_candidate_*.png")})
        for old in candidates(d):
            old.rename(d / f"r{rnd}_{old.name}")  # keep the earlier round's candidates
        prompt = f"{P['style']} {prop['subject']} {P['ref_suffix']}"
        negative = prop.get("negative", P["negative"]) + (", " + prop["extra_negative"] if prop.get("extra_negative") else "")
        before = balance()
        e = art_gen.leonardo(prompt, d, "lucid-origin", 1024, 1024, a.count, negative, label=pid)
        after = balance()
        for f in candidates(d):
            subprocess.run(["sips", "-s", "format", "png", str(f), "--out", str(f)], check=True, capture_output=True)
        e.update({"card": a.card, "prop": pid, "name": prop["name"], "folder": f"{a.card}/{pid}",
                  "balance_before": before, "balance_after": after, "credits": before - after,
                  "negative_prompt": negative})
        entries.append(e)
        LOG.write_text(json.dumps(entries, indent=2), encoding="utf-8")
        print(f"{pid}: {len(candidates(d))} images, {before - after} credits (balance {after})")


def cmd_sheet(a):
    card = P["cards"][a.card]
    args = []
    for pid, prop in card.items():
        imgs = [str(f) for f in candidates(HERE / a.card / pid)][:a.rows]
        args += [prop["name"]] + imgs + ["-"] * (a.rows - len(imgs))
    subprocess.run(["swift", str(HERE / "sheet.swift"), str(HERE / a.card / "sheet.png"), str(a.rows)] + args, check=True)


def cmd_approved(a):
    """Each card's approved props in one strip (<card>/approved.png), and all seven stacked (approved.png)."""
    strips = []
    for cid, card in P["cards"].items():
        args = []
        for n, (pid, prop) in enumerate(card.items()):
            d = HERE / cid / pid
            img = d / "concept.png" if (d / "concept.png").exists() else d / "model_view.png"
            spare = " (spare)" if n == 3 else ""
            args += [f"{prop['name']}{spare}, {prop['size_cm']} cm", str(img)]
        out = HERE / cid / "approved.png"
        subprocess.run(["swift", str(HERE / "sheet.swift"), str(out), "1"] + args, check=True)
        strips.append(str(out))
    subprocess.run(["swift", str(HERE / "stack.swift"), str(HERE / "approved.png")] + strips, check=True)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("card")
    c.add_argument("card")
    c.add_argument("--props", nargs="+")
    c.add_argument("--count", type=int, default=2)
    c.add_argument("--force", action="store_true")
    s = sub.add_parser("sheet")
    s.add_argument("card")
    s.add_argument("--rows", type=int, default=2)
    sub.add_parser("approved")
    a = p.parse_args()
    {"card": cmd_card, "sheet": cmd_sheet, "approved": cmd_approved}[a.cmd](a)


if __name__ == "__main__":
    main()
