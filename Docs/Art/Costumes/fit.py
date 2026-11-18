"""T96: the fit sheets. One edit per costume and character (the edit model dresses one character per call
reliably), then a sheet of the five fits side by side. Standard library only; run from anywhere.

  python Docs/Art/Costumes/fit.py run <costume> [--chars openai anthropic ...] [--parallel 5] [--force]
      For each character, Docs/Art/Costumes/<costume>/fit/<char>/edit_1.png: the costume from pick.png on the
      character's lineup panel (left), and that head shape's version of the costume alone on gray (right).
      Prompts are built from fits.json. Skips a character that already has a fit unless --force, which keeps
      the old take as fit/<char>/r<N>_edit_1.png. Each call is logged in log.json by gen.py.
  python Docs/Art/Costumes/fit.py sheet <costume>
      Docs/Art/Costumes/<costume>/fit_sheet.png: the left half of each character's fit, in seat order, labeled.
"""
import argparse
import concurrent.futures
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
F = json.loads((HERE / "fits.json").read_text(encoding="utf-8"))
CANVAS = HERE / "_canvas"
ORDER = ["openai", "anthropic", "spacexai", "meta", "you"]
LABEL = {"openai": "OpenAI", "anthropic": "Anthropic", "spacexai": "SpaceXAI", "meta": "Meta", "you": "You"}


def swift(*args):
    subprocess.run(["swift", str(HERE / "canvas.swift"), *map(str, args)], check=True)


def panel(char):
    """The character's panel of the lineup with headroom, on the left of a 614 x 864 canvas."""
    out = CANVAS / f"panel_{char}.png"
    if not out.exists():
        tall = CANVAS / "lineup_tall.png"
        if not tall.exists():
            swift("pad", ROOT / "Docs/Art/Cast/lineup.png", tall, 1536, 864)
        i = F["characters"][char]["panel"]
        crop = CANVAS / f"crop_{char}.png"
        swift("crop", tall, crop, round(i * 307.2), 0, 307, 864)
        swift("tile", out, 614, 864, crop, "-")
        crop.unlink()
    return out


def ref(costume):
    out = CANVAS / f"ref_{costume}.png"
    swift("tile", out, 614, 864, HERE / costume / "pick.png")
    return out


def prompt(costume, char):
    c, ch = F["costumes"][costume], F["characters"][char]
    shape = ch["shape"]
    fit = c[shape] + (" " + c[char] if char in c else "")
    return (f"Put the {c['name']} from the second image on the character in the first image, {ch['desc']}, "
            f"fitted to its head like a stop-motion costume fitting. {fit} "
            f"On the right, on the plain light gray background: {F['standalone'][shape]} {F['keep']}")


def run_one(costume, char, r, force):
    d = HERE / costume / "fit" / char
    if (d / "edit_1.png").exists():
        if not force:
            print(f"{costume}/{char}: has a fit, skipped")
            return
        n = 1 + len(list(d.glob("r*_edit_1.png")))
        (d / "edit_1.png").rename(d / f"r{n}_edit_1.png")
    subprocess.run([sys.executable, str(HERE / "gen.py"), "edit", "--out", str(d), "--image", str(panel(char)),
                    "--ref", str(r), "--count", "1", "--prompt", prompt(costume, char)], check=True)


def cmd_run(a):
    r = ref(a.costume)
    for ch in a.chars:
        panel(ch)   # build the canvases before the parallel calls
    with concurrent.futures.ThreadPoolExecutor(a.parallel) as ex:
        for f in [ex.submit(run_one, a.costume, ch, r, a.force) for ch in a.chars]:
            f.result()


def cmd_sheet(a):
    args, tmp = [], []
    for ch in ORDER:
        src = HERE / a.costume / "fit" / ch / "edit_1.png"
        if not src.exists():
            continue
        w, h = [int(x) for x in subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(src)],
                capture_output=True, text=True).stdout.split()[-3::2]]
        half = CANVAS / f"half_{a.costume}_{ch}.png"
        swift("crop", src, half, 0, 0, w // 2, h)
        tmp.append(half)
        args += [LABEL[ch], half]
    swift("sheet", HERE / a.costume / "fit_sheet.png", 360, 900, *args)
    for t in tmp:
        t.unlink()
    print(f"saved {a.costume}/fit_sheet.png")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("costume")
    r.add_argument("--chars", nargs="+", default=ORDER)
    r.add_argument("--parallel", type=int, default=5)
    r.add_argument("--force", action="store_true")
    s = sub.add_parser("sheet")
    s.add_argument("costume")
    a = ap.parse_args()
    {"run": cmd_run, "sheet": cmd_sheet}[a.cmd](a)


if __name__ == "__main__":
    main()
