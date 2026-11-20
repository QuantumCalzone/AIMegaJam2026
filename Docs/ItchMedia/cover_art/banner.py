"""The itch.io page banner: the cover's art, cut to a wide strip, with the name on one line.

It crops the cover's repainted art (art.png) to the curtain and the five robots' heads, scales it to the
page column's width (960 px), shades the top with ink, fades the bottom into the page's BG 2 color, and
sets NO HUMANS ON SET in the cover's style: Roboto Black, Gold #F2C14E as a light-to-deep gradient, an
InkSolid #161225 outline and a soft shadow (see title.swift, which makes the cover the same way).

Needs Python 3.10+ and Pillow (pip install pillow). Run from the repo root:

    python Docs/ItchMedia/cover_art/banner.py Docs/ItchMedia/cover_art/art.png \
        "<UE_ROOT>/Engine/Content/Slate/Fonts/Roboto-Black.ttf" Docs/ItchMedia/banner.png
"""

import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT_W = 960            # itch.io's game page column
CROP_TOP = 150        # in art.png's pixels: the strip runs from the curtain above the antenna...
CROP_BOTTOM = 610      # ...down to the robots' necks
INK = (0x16, 0x12, 0x25)
GOLD = [(0.0, (0xFF, 0xE7, 0xA0)), (0.5, (0xF2, 0xC1, 0x4E)), (1.0, (0xD3, 0x9A, 0x2E))]

TITLE = "NO HUMANS ON SET"
SIZE = 84              # px, at the output size
TRACKING = 0.04        # extra space between letters, as a share of SIZE
TITLE_TOP = 26         # px from the top edge to the caps
STROKE = 9             # outline, in px at the output size (the cover's 18 px at 150 px, scaled)
CAP = 0.711            # Roboto's cap height, as a share of the size


def vertical_gradient(w, h, stops):
    """An RGB image, w x h, that runs through `stops` [(position 0..1, (r, g, b)), ...] from top to bottom."""
    img = Image.new("RGB", (1, h))
    for y in range(h):
        t = y / max(h - 1, 1)
        for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
            if t0 <= t <= t1:
                k = (t - t0) / (t1 - t0)
                img.putpixel((0, y), tuple(round(a + (b - a) * k) for a, b in zip(c0, c1)))
                break
    return img.resize((w, h))


def alpha_ramp(w, h, y0, y1, a0, a1):
    """An L mask, w x h: a0 above y0, a1 below y1, a straight ramp between."""
    m = Image.new("L", (1, h))
    for y in range(h):
        k = min(max((y - y0) / (y1 - y0), 0.0), 1.0)
        m.putpixel((0, y), round(255 * (a0 + (a1 - a0) * k)))
    return m.resize((w, h))


def text_masks(size_wh, font, x0, y_top):
    """The title as two L masks, fill and fill-plus-outline, laid out letter by letter with tracking."""
    fill = Image.new("L", size_wh, 0)
    stroke = Image.new("L", size_wh, 0)
    df, ds = ImageDraw.Draw(fill), ImageDraw.Draw(stroke)
    x = x0
    for i, ch in enumerate(TITLE):
        df.text((x, y_top), ch, font=font, fill=255, anchor="ls")
        ds.text((x, y_top), ch, font=font, fill=255, anchor="ls", stroke_width=STROKE, stroke_fill=255)
        nxt = TITLE[i + 1] if i + 1 < len(TITLE) else ""
        # The advance with kerning: the pair's length less the next letter's.
        x += font.getlength(ch + nxt) - font.getlength(nxt) + SIZE * TRACKING
    return fill, stroke


def title_width(font):
    w = 0.0
    for i, ch in enumerate(TITLE):
        nxt = TITLE[i + 1] if i + 1 < len(TITLE) else ""
        w += font.getlength(ch + nxt) - font.getlength(nxt) + SIZE * TRACKING
    return w - SIZE * TRACKING


def main():
    if len(sys.argv) != 4:
        sys.exit("usage: banner.py <art.png> <Roboto-Black.ttf> <out.png>")
    art_path, font_path, out_path = sys.argv[1:]

    art = Image.open(art_path).convert("RGB")
    strip = art.crop((0, CROP_TOP, art.width, CROP_BOTTOM))
    out_h = round(strip.height * OUT_W / strip.width)
    img = strip.resize((OUT_W, out_h), Image.LANCZOS)

    # Shade the top 45% with ink, strongest at the top edge, so the name stands off the curtain.
    ink = Image.new("RGB", img.size, INK)
    img = Image.composite(ink, img, alpha_ramp(OUT_W, out_h, 0, out_h * 0.45, 0.55, 0.0))
    # Fade the bottom 30% into the page's BG 2 (the ink panel color), so the banner meets the column.
    img = Image.composite(ink, img, alpha_ramp(OUT_W, out_h, out_h * 0.70, out_h, 0.0, 1.0))

    font = ImageFont.truetype(font_path, SIZE)
    x0 = (OUT_W - title_width(font)) / 2
    baseline = TITLE_TOP + SIZE * CAP
    fill, stroke = text_masks(img.size, font, x0, baseline)

    # A soft drop shadow, then the ink outline, then the gold fill (light at the caps, deeper at the base).
    shadow = Image.new("L", img.size, 0)
    shadow.paste(stroke.filter(ImageFilter.GaussianBlur(9)).point(lambda v: round(v * 0.7)), (0, 4))
    img = Image.composite(Image.new("RGB", img.size, (0, 0, 0)), img, shadow)
    img = Image.composite(ink, img, stroke)
    gold = Image.new("RGB", img.size, GOLD[1][1])
    cap_top = round(baseline - SIZE * CAP)
    gold.paste(vertical_gradient(OUT_W, round(SIZE * CAP), GOLD), (0, cap_top))
    img = Image.composite(gold, img, fill)

    img.save(out_path, optimize=True)
    print(f"wrote {out_path} ({OUT_W} x {out_h})")


if __name__ == "__main__":
    main()
