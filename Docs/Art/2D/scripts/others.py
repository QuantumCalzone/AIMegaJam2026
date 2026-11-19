"""T99 round 1: the portrait, the bill and the flame sheet, four candidates each, in parallel."""
import subprocess, sys, concurrent.futures
STYLE = ("Stop-motion claymation style: hand-sculpted from matte modeling clay with faint thumbprints, soft rounded "
         "chunky forms, bold simple shapes and a clean readable silhouette, saturated slightly chalky colors, from the "
         "same world as a gold, crimson and cream 19th-century clay opera house. ")
NEG = ("text, letters, words, numbers, logo, watermark, brand mark, realistic human face, hair, fur, thin wires, "
       "glossy plastic, chrome, photorealistic, ink outlines, flat 2D illustration, scary, gore, extra characters")
JOBS = {
 "portrait": (1024, 1024, STYLE + "Head-and-shoulders portrait of a friendly AI robot stagehand who whispers tips "
   "backstage. A big round cream clay head, about a third of the image wide, centered in the upper middle, with a dark "
   "rounded screen face (#14121C) showing two big soft rose-pink glowing LED eyes and a warm rose-pink LED smile. A "
   "chunky black backstage headset with round ear cups and a short thick microphone boom, a dark plum knit beanie, a "
   "black stagehand t-shirt with one small gold clay wrench pin, cream clay shoulders. Facing the viewer, kind, helpful "
   "and a little conspiratorial. Soft warm frontal stage light, plain flat deep plum background. Cute, never creepy.",
   NEG + ", human, skin, nose, teeth, red eyes, angry, multiple characters, frame, border, hands"),
 "bill": (2048, 1024, STYLE + "One play-money banknote sculpted from matte modeling clay, seen flat and straight on "
   "from the front, filling almost the whole frame with a thin even margin of plain dark background around it. A "
   "muted sage-green bill with softly rounded corners, a raised clay double border, a large round medallion in the exact "
   "center with a simple cute round robot head in relief (two square eyes and an antenna), one round rosette left of "
   "the medallion and one right of it, thin wavy relief lines across the paper, and the four corners left plain and "
   "empty. No real currency's design, no portrait of a person, no currency symbol.",
   NEG + ", dollar sign, currency symbol, president, portrait of a person, coins, stack of bills, hand, wallet, "
   "perspective, tilted, curled"),
 "flames": (1920, 1080, STYLE + "A sprite sheet of eight separate small sculpted clay flames, arranged in two neat rows "
   "of four, evenly spaced, each flame standing upright on its own with clear empty space around it, all the same size. "
   "Each flame is a chunky rounded teardrop tongue of matte clay in layers: deep red outer edge, tangerine orange, "
   "golden yellow, and a pale cream hot core near the base, with one to three rounded tips. Every flame has a slightly "
   "different flicker shape, leaning a little left or right. Plain flat pure black background, no smoke, no floor, no "
   "shadow.",
   NEG + ", smoke, candle, wick, torch, logs, wood, floor, ground, shadow, sparks, explosion, overlapping flames"),
}
def run(k):
    w, h, p, n = JOBS[k]
    r = subprocess.run([sys.executable, "Tools/art_gen.py", "image", "--out", f"Local/art/T99/{k}/r1",
                        "--prompt", p, "--negative", n, "--width", str(w), "--height", str(h), "--count", "4"],
                       capture_output=True, text=True)
    return k, r.returncode, (r.stdout + r.stderr).strip()[-300:]
with concurrent.futures.ThreadPoolExecutor(3) as ex:
    for k, code, out in ex.map(run, sys.argv[1:] or list(JOBS)):
        print(k, code, out, flush=True)
