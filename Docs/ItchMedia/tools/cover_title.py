"""The itch.io cover's name, on the PC: a Python port of cover_art/title.swift (which runs only on a Mac).

It crops a render to itch.io's cover shape (1.26 : 1, 630 x 500), shades the top with ink, and sets the
game's name in the game's display style: Roboto Black, UIStyle's Gold #F2C14E as a light-to-deep gradient,
an InkSolid #161225 outline and a soft drop shadow. Every size is title.swift's at an 896 px tall frame,
scaled to the render's height, so a 2520 x 2000 render gets the same look as the jam's cover.

Needs Python 3.10+ and Pillow (pip install pillow). Run from the repo root:

    python Docs/ItchMedia/tools/cover_title.py <render.png> "<UE_ROOT>/Engine/Content/Slate/Fonts/Roboto-Black.ttf" \
        <cover_full.png> [--crop-x N] [--small Docs/ItchMedia/cover.png] [--grid preview_315.png]

    --crop-x N      left edge of the 1.26 : 1 crop, in the render's pixels (default: centred)
    --small PATH    also write the 630 x 500 cover itch.io shows
    --grid PATH     also write a 315 x 250 copy, the size of itch.io's game grid, to judge it by
    --top F         the first line's cap top, as a share of the height (default 0.038, title.swift's 34 px)
    --size F        the letters' size, as a share of the height (default 0.1674, title.swift's 150 px)
    --shade F       how far down the ink shade reaches, as a share of the height (default 0.40)
    --lines A|B     the name's lines (default "NO HUMANS|ON SET")

Check: run on cover_art/art.png with --crop-x 23 and compare with cover_art/cover_full.png (title.swift's
output). The two match to within a pixel or two of letter placement.
"""
import argparse

from PIL import Image, ImageDraw, ImageFilter, ImageFont

INK = (0x16, 0x12, 0x25)                 # UIStyle InkSolid
GOLD = [(0.0, (0xFF, 0xE7, 0xA0)), (0.5, (0xF2, 0xC1, 0x4E)), (1.0, (0xD3, 0x9A, 0x2E))]  # UIStyle Gold, light to deep
SHAPE = 630 / 500                        # itch.io's cover
CAP = 0.711                              # Roboto's cap height, as a share of the size

# title.swift's numbers, at its 896 px frame.
REF_H = 896
REF_GAP = 26                             # px between the first line's base and the second line's caps
REF_STROKE = 18                          # outline width (CoreGraphics strokes half inside, half outside)
REF_SHADOW_DY = 8
REF_SHADOW_BLUR = 18                     # CoreGraphics shadow blur; about two Gaussian sigmas
TRACKING = [0.02, 0.08]                  # extra space between letters, per line, as a share of the size


def gradient(w, h, stops):
    col = Image.new("RGB", (1, h))
    for y in range(h):
        t = y / max(h - 1, 1)
        for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
            if t0 <= t <= t1:
                k = (t - t0) / (t1 - t0)
                col.putpixel((0, y), tuple(round(a + (b - a) * k) for a, b in zip(c0, c1)))
                break
    return col.resize((w, h))


def ramp(w, h, y0, y1, a0, a1):
    col = Image.new("L", (1, h))
    for y in range(h):
        k = min(max((y - y0) / max(y1 - y0, 1), 0.0), 1.0)
        col.putpixel((0, y), round(255 * (a0 + (a1 - a0) * k)))
    return col.resize((w, h))


def advance(font, text, size, tracking):
    """Each letter's x, with the font's kerning and the extra tracking, and the line's width."""
    xs, x = [], 0.0
    for i, ch in enumerate(text):
        xs.append(x)
        nxt = text[i + 1] if i + 1 < len(text) else ""
        x += font.getlength(ch + nxt) - font.getlength(nxt) + size * tracking
    return xs, x - size * tracking      # no trailing space, as title.swift


def line_masks(canvas, font, text, size, tracking, baseline, stroke):
    xs, width = advance(font, text, size, tracking)
    x0 = (canvas[0] - width) / 2
    fill, outline = Image.new("L", canvas, 0), Image.new("L", canvas, 0)
    df, do = ImageDraw.Draw(fill), ImageDraw.Draw(outline)
    for x, ch in zip(xs, text):
        df.text((x0 + x, baseline), ch, font=font, fill=255, anchor="ls")
        do.text((x0 + x, baseline), ch, font=font, fill=255, anchor="ls", stroke_width=stroke, stroke_fill=255)
    return fill, outline


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("render")
    ap.add_argument("font")
    ap.add_argument("out")
    ap.add_argument("--crop-x", type=int, default=None)
    ap.add_argument("--small")
    ap.add_argument("--grid")
    ap.add_argument("--top", type=float, default=34 / REF_H)
    ap.add_argument("--size", type=float, default=150 / REF_H)
    ap.add_argument("--shade", type=float, default=0.40)
    ap.add_argument("--lines", default="NO HUMANS|ON SET")
    a = ap.parse_args()

    art = Image.open(a.render).convert("RGB")
    H = art.height
    W = round(H * SHAPE)
    if W > art.width:                    # a render wider than tall enough: crop the height instead
        W = art.width
        H = round(W / SHAPE)
    cx = a.crop_x if a.crop_x is not None else (art.width - W) // 2
    cy = (art.height - H) // 2
    img = art.crop((cx, cy, cx + W, cy + H))
    s = H / REF_H

    # Shade the top with ink, strongest at the top edge, so the name stands off the bright stage.
    ink = Image.new("RGB", img.size, INK)
    img = Image.composite(ink, img, ramp(W, H, 0, H * a.shade, 0.55, 0.0))

    size = round(a.size * H)
    font = ImageFont.truetype(a.font, size)
    stroke = max(1, round(REF_STROKE * s / 2))   # Pillow's stroke_width is outside only: half of CG's line width
    lines = a.lines.split("|")
    fills, outlines, caps = [], [], []
    cap_top = a.top * H
    for i, text in enumerate(lines):
        baseline = cap_top + size * CAP
        f, o = line_masks(img.size, font, text, size, TRACKING[min(i, len(TRACKING) - 1)], baseline, stroke)
        fills.append(f)
        outlines.append(o)
        caps.append((round(cap_top), round(size * CAP)))
        cap_top = baseline + REF_GAP * s

    outline = outlines[0]
    for o in outlines[1:]:
        outline = Image.composite(o, outline, o)

    # A soft drop shadow, then the ink outline, then the gold fill (light at the caps, deeper at the base).
    shadow = Image.new("L", img.size, 0)
    shadow.paste(outline.filter(ImageFilter.GaussianBlur(REF_SHADOW_BLUR * s / 2)).point(lambda v: round(v * 0.7)),
                 (0, round(REF_SHADOW_DY * s)))
    img = Image.composite(Image.new("RGB", img.size, (0, 0, 0)), img, shadow)
    img = Image.composite(ink, img, outline)
    for f, (top, cap_h) in zip(fills, caps):
        gold = Image.new("RGB", img.size, GOLD[1][1])
        gold.paste(gradient(W, cap_h, GOLD), (0, top))
        img = Image.composite(gold, img, f)

    img.save(a.out, optimize=True)
    print(f"wrote {a.out} ({W} x {H}, crop x {cx})")
    if a.small:
        img.resize((630, 500), Image.LANCZOS).save(a.small, optimize=True)
        print(f"wrote {a.small} (630 x 500)")
    if a.grid:
        img.resize((315, 250), Image.LANCZOS).save(a.grid, optimize=True)
        print(f"wrote {a.grid} (315 x 250, itch.io's grid size)")


if __name__ == "__main__":
    main()
