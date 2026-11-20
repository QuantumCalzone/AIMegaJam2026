"""The trailer's captions, in the game's style: transparent 1920 x 1080 PNGs that ffmpeg lays over the cut.

The look comes from the design doc's "Palette and type" (Docs/Design/ArtInspiration.md) and UIStyle:
Roboto, the engine's font (Apache 2.0), as the game's F_UI; ink panels #161225 with old-gold trim;
white text on ink; Gold means "act now", teal means "you", curtain red means the vote and the cut; each
bot's name in its seat color. Sizes are for a phone: a phone shows the trailer about 390 px wide, a fifth
of 1080p, so nothing is set under 56 px (11 px on the phone).

Kinds:

    hook   big centred words, white with an ink outline and a soft shadow; {you:...} {gold:...} {red:...}
           {openai:...} {anthropic:...} {spacexai:...} {meta:...} colour a stretch
    quote  a chat-style ink panel at the bottom: the speaker's seat bar and name, then the line, word for
           word as the show logged it ("NHOS:" lines)
    stamp  a tilted curtain-red slab with white letters, for CUT! and the like
    title  the end card's name, in the cover's style (gold gradient, ink outline), with a line under it

    python Docs/ItchMedia/tools/caption.py hook  "One of these robots is human.|{you:It's you.}" out.png
    python Docs/ItchMedia/tools/caption.py quote "Anthropic" "Why is your box sweating?" out.png
    python Docs/ItchMedia/tools/caption.py stamp "CUT!" out.png
    python Docs/ItchMedia/tools/caption.py title "Free on itch.io" out.png
    python Docs/ItchMedia/tools/caption.py sheet out.png [frame.png]   # every kind on a frame, to judge them

hook and title take --veil 0.55 (an ink veil over the whole shot, 0 to 1) when the shot behind is busy.

"|" breaks a line. Needs Pillow. The fonts come from the engine (set UE_ROOT if it isn't E:/Epic Games/UE_5.8).
"""
import os
import re
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

UE_ROOT = os.environ.get("UE_ROOT", "E:/Epic Games/UE_5.8")
FONTS = os.path.join(UE_ROOT, "Engine", "Content", "Slate", "Fonts")
W, H = 1920, 1080

INK = (0x16, 0x12, 0x25)
OLD_GOLD = (0xA9, 0x87, 0x3A)
WHITE = (0xFF, 0xFF, 0xFF)
QUIET = (0xC9, 0xC3, 0xDA)
COLORS = {
    "white": WHITE, "quiet": QUIET,
    "gold": (0xF2, 0xC1, 0x4E), "red": (0xC8, 0x20, 0x2F), "amber": (0xF2, 0x9E, 0x1F),
    "you": (0x3F, 0xD0, 0xC9), "openai": (0xA8, 0xCC, 0xFF), "anthropic": (0xE8, 0x89, 0x4A),
    "spacexai": (0xD8, 0xF0, 0x4A), "meta": (0xC8, 0xAC, 0x12),
}
SEAT = {"OpenAI": "openai", "Anthropic": "anthropic", "SpaceXAI": "spacexai", "Meta": "meta", "You": "you"}
GOLD_RAMP = [(0.0, (0xFF, 0xE7, 0xA0)), (0.5, (0xF2, 0xC1, 0x4E)), (1.0, (0xD3, 0x9A, 0x2E))]


def font(weight, size):
    return ImageFont.truetype(os.path.join(FONTS, f"Roboto-{weight}.ttf"), size)


def runs(line):
    """'a {you:b} c' -> [('a ', white), ('b', teal), (' c', white)]"""
    out, pos = [], 0
    for m in re.finditer(r"\{(\w+):([^}]*)\}", line):
        if m.start() > pos:
            out.append((line[pos:m.start()], WHITE))
        out.append((m.group(2), COLORS[m.group(1)]))
        pos = m.end()
    if pos < len(line):
        out.append((line[pos:], WHITE))
    return out


def outlined(canvas, xy, text, f, fill, stroke, anchor="ls", shadow=True):
    """Text with an ink outline and a soft shadow, drawn onto an RGBA canvas."""
    if shadow:
        sh = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((xy[0], xy[1] + stroke), text, font=f, fill=(0, 0, 0, 170), anchor=anchor,
                                stroke_width=stroke, stroke_fill=(0, 0, 0, 170))
        canvas.alpha_composite(sh.filter(ImageFilter.GaussianBlur(stroke * 1.2)))
    ImageDraw.Draw(canvas).text(xy, text, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=INK)


def veiled(veil):
    """A blank caption frame, or one with an ink veil (0..1) over the whole shot, to quiet a busy background."""
    return Image.new("RGBA", (W, H), INK + (round(255 * veil),) if veil else (0, 0, 0, 0))


def hook(text, size=104, y_center=None, veil=0.0):
    img = veiled(veil)
    f = font("Black", size)
    lines = text.split("|")
    lead = round(size * 1.18)
    y0 = (y_center if y_center is not None else H / 2) - lead * (len(lines) - 1) / 2 + size * 0.36
    for i, line in enumerate(lines):
        parts = runs(line)
        width = sum(f.getlength(t) for t, _ in parts)
        x = (W - width) / 2
        for t, col in parts:
            outlined(img, (x, y0 + i * lead), t, f, col, stroke=max(4, size // 14))
            x += f.getlength(t)
    return img


def wrap(text, f, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if f.getlength(trial) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def quote(speaker, line, size=58, max_w=1500):
    """A chat line, big: the seat bar, the name in its seat color, the words in white, on an ink panel."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    name_f, line_f = font("Black", round(size * 0.8)), font("Bold", size)
    body = wrap(f"\u201c{line}\u201d", line_f, max_w)
    pad, bar, gap = 32, 12, 12
    lead = round(size * 1.25)
    name_h = round(size * 0.8)
    text_w = max([line_f.getlength(b) for b in body] + [name_f.getlength(speaker)])
    pw = round(text_w + pad * 2 + bar + 24)
    ph = round(pad * 2 + name_h + gap + lead * len(body) - (lead - size))
    x0, y0 = (W - pw) // 2, H - 48 - ph            # 48 from the bottom: clear of a phone's player bar
    d = ImageDraw.Draw(img)
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((x0, y0 + 8, x0 + pw, y0 + ph + 8), 24, fill=(0, 0, 0, 150))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
    d.rounded_rectangle((x0, y0, x0 + pw, y0 + ph), 24, fill=INK + (240,), outline=OLD_GOLD, width=4)
    seat = COLORS[SEAT.get(speaker, "white")]
    d.rounded_rectangle((x0 + pad, y0 + pad, x0 + pad + bar, y0 + ph - pad), 6, fill=seat)
    tx = x0 + pad + bar + 24
    d.text((tx, y0 + pad + name_h * 0.86), speaker, font=name_f, fill=seat, anchor="ls")
    for i, b in enumerate(body):
        d.text((tx, y0 + pad + name_h + gap + size * 0.86 + i * lead), b, font=line_f, fill=WHITE, anchor="ls")
    return img


def stamp(text, size=200, angle=-8):
    f = font("Black", size)
    tw = f.getlength(text)
    slab = Image.new("RGBA", (round(tw + 120), round(size * 1.35)), (0, 0, 0, 0))
    d = ImageDraw.Draw(slab)
    d.rounded_rectangle((6, 6, slab.width - 6, slab.height - 6), 24, fill=COLORS["red"], outline=WHITE, width=10)
    d.text((slab.width / 2, slab.height / 2), text, font=f, fill=WHITE, anchor="mm")
    slab = slab.rotate(-angle, expand=True, resample=Image.BICUBIC)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    pos = ((W - slab.width) // 2, (H - slab.height) // 2)
    sh.paste((0, 0, 0, 160), (pos[0] + 10, pos[1] + 16), slab)
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
    img.alpha_composite(slab, pos)
    return img


def title(sub, size=190, veil=0.0):
    """NO HUMANS / ON SET in the cover's style, and one white line under it (for "Free on itch.io")."""
    img = veiled(veil)
    f = font("Black", size)
    cap = 0.711 * size
    lines = [("NO HUMANS", 0.02), ("ON SET", 0.08)]
    top = H * 0.24
    stroke = round(size * 0.06)
    fills, outline = [], Image.new("L", img.size, 0)
    for text, track in lines:
        xs, x = [], 0.0
        for i, ch in enumerate(text):
            xs.append(x)
            nxt = text[i + 1] if i + 1 < len(text) else ""
            x += f.getlength(ch + nxt) - f.getlength(nxt) + size * track
        x0 = (W - (x - size * track)) / 2
        m = Image.new("L", img.size, 0)
        dm, do = ImageDraw.Draw(m), ImageDraw.Draw(outline)
        for xx, ch in zip(xs, text):
            dm.text((x0 + xx, top + cap), ch, font=f, fill=255, anchor="ls")
            do.text((x0 + xx, top + cap), ch, font=f, fill=255, anchor="ls", stroke_width=stroke, stroke_fill=255)
        fills.append((m, round(top), round(cap)))
        top += cap + size * 0.17
    sh = outline.filter(ImageFilter.GaussianBlur(stroke)).point(lambda v: round(v * 0.7))
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    shadow.paste((0, 0, 0, 255), (0, stroke // 2), sh)
    img.alpha_composite(shadow)
    img.paste(INK + (255,), (0, 0), outline)
    for m, t, ch in fills:
        col = Image.new("RGB", (1, ch))
        for y in range(ch):
            k = y / max(ch - 1, 1)
            (a0, c0), (a1, c1) = (GOLD_RAMP[0], GOLD_RAMP[1]) if k <= 0.5 else (GOLD_RAMP[1], GOLD_RAMP[2])
            u = (k - a0) / (a1 - a0)
            col.putpixel((0, y), tuple(round(p + (q - p) * u) for p, q in zip(c0, c1)))
        gold = Image.new("RGB", img.size, GOLD_RAMP[1][1])
        gold.paste(col.resize((W, ch)), (0, t))
        img.paste(gold, (0, 0), m)
    sub_img = hook(sub, size=84, y_center=top + 90)
    img.alpha_composite(sub_img)
    return img


def sheet(out, background=None):
    """Every kind on one frame, plus the same frame at a phone's width, to judge the sizes."""
    bg = Image.open(background).convert("RGBA").resize((W, H)) if background else Image.new("RGBA", (W, H), (60, 20, 24, 255))
    frames = [
        hook("One of these robots is human.|{you:It's you.}", veil=0.55),
        quote("Anthropic", "A real line from a show on Play goes here, word for word, as the NHOS: log has it."),
        stamp("CUT!"),
        title("Free on itch.io", veil=0.7),
    ]
    tiles = []
    for fr in frames:
        t = bg.copy()
        t.alpha_composite(fr)
        tiles.append(t.convert("RGB"))
    big = Image.new("RGB", (W, H * len(tiles)))
    for i, t in enumerate(tiles):
        big.paste(t, (0, H * i))
    big.resize((W // 2, H * len(tiles) // 2), Image.LANCZOS).save(out)
    phone = Image.new("RGB", (390 * 2 + 10, 219 * 2 + 10), (255, 255, 255))
    for i, t in enumerate(tiles):
        phone.paste(t.resize((390, 219), Image.LANCZOS), ((i % 2) * 400, (i // 2) * 229))
    root, ext = os.path.splitext(out)
    phone.save(f"{root}_phone{ext}")
    print(f"wrote {out} and {root}_phone{ext} (each frame at 390 px wide, a phone's width)")


def main(argv):
    kind = argv[0]
    if kind == "sheet":
        sheet(argv[1], argv[2] if len(argv) > 2 else None)
        return
    veil = 0.0
    if "--veil" in argv:
        i = argv.index("--veil")
        veil = float(argv[i + 1])
        argv = argv[:i] + argv[i + 2:]
    if kind == "hook":
        img, out = hook(argv[1], veil=veil), argv[2]
    elif kind == "quote":
        img, out = quote(argv[1], argv[2]), argv[3]
    elif kind == "stamp":
        img, out = stamp(argv[1]), argv[2]
    elif kind == "title":
        img, out = title(argv[1], veil=veil), argv[2]
    else:
        raise SystemExit(__doc__)
    img.save(out)
    print(f"wrote {out}")


if __name__ == "__main__":
    main(sys.argv[1:])
