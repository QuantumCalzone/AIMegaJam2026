#!/usr/bin/env python3
"""ui_shots.py: check UI screenshots without color, and measure their contrast (T34 steps 5 and 6).

Python 3.10 or newer, standard library only, so it runs on the Mac and the PC alike.

What it does for each PNG you give it:

1. Writes two versions next to it (or in --out):
   - <name>_gray.png: the relative luminance of each pixel (WCAG's, from linear sRGB), so a contrast
     ratio measured on the gray version is the same as on the original.
   - <name>_deut.png: deuteranopia at full strength (Machado, Oliveira and Fernandes 2009), applied
     in linear sRGB. This is the common red-green deficiency.
   Files that already end in _gray or _deut are skipped, so a folder glob can be run twice.
2. Prints contrast ratios (WCAG 2.x: (L1 + 0.05) / (L2 + 0.05)):
   - With no --text or --edge, one rough figure for the whole image: its median color as the
     background against its darkest or lightest 1 % (whichever is farther). Use boxes for real figures.
   - --text NAME=X,Y,W,H: a box around one piece of text, in screenshot pixels. The box's median color
     is the background and its 1st or 99th luminance percentile is the text (whichever contrasts more),
     the method T33 used. Keep the box tight on the text and its own background. Needs 4.5:1.
   - --edge NAME=X0,Y0,X1,Y1: a short line that starts outside a button or border and crosses its edge.
     The first pixel is the outside; the pixel on the line that differs most from it is the edge.
     Needs 3:1 (WCAG 1.4.11).
   - --colors HEX HEX: the ratio of two colors, no image needed (for example UIStyle's values).

Run it from the repo root (on the Mac, `python3` in place of `python`). Coordinates are pixels of the PNG
as saved, title bar included (a 1600 x 900 PIE window saves as 1600 x 968 on the Mac). A 1600-wide shot
takes about 3 s.

    python Tools/ui_shots.py Saved/T34/shots/after_vote_p16.png
    python Tools/ui_shots.py Saved/T34/shots/*.png --no-contrast
    python Tools/ui_shots.py shot.png --text header=40,30,600,48 --edge action=900,850,900,880
    python Tools/ui_shots.py --colors F2C14E 161225
    python Tools/ui_shots.py shot.png --no-variants --md --text header=40,30,600,48

--md prints the measurements as Markdown table rows for T34's Findings. The exit code is 0 when every
measured box and edge passes, 1 when one fails, 2 on a bad argument or file. The rough whole-image
figure never fails the run. PNGs with 8 bits per channel (gray, RGB, palette, with or without alpha)
are read; alpha is dropped (screenshots are opaque). Interlaced and 16-bit PNGs are refused.
"""

from __future__ import annotations

import argparse
import os
import struct
import sys
import zlib
from dataclasses import dataclass

PNG_SIG = b"\x89PNG\r\n\x1a\n"
TEXT_MIN = 4.5
EDGE_MIN = 3.0

# Machado et al. 2009, deuteranopia, severity 1.0 (linear RGB).
DEUT = (
    (0.367322, 0.860646, -0.227968),
    (0.280085, 0.672501, 0.047413),
    (-0.011820, 0.042940, 0.968881),
)
LUM = (0.2126, 0.7152, 0.0722)
SCALE = 65535  # fixed-point steps for linear values


@dataclass
class Image:
    width: int
    height: int
    rgb: bytearray  # width * height * 3, row by row


# ---------------------------------------------------------------- sRGB <-> linear


def _to_lin(c: int) -> float:
    s = c / 255.0
    return s / 12.92 if s <= 0.04045 else ((s + 0.055) / 1.055) ** 2.4


LIN = [_to_lin(i) for i in range(256)]


def _build_back() -> bytes:
    """Linear value in 0..SCALE -> sRGB byte."""
    out = bytearray(SCALE + 1)
    for i in range(SCALE + 1):
        v = i / SCALE
        s = 12.92 * v if v <= 0.0031308 else 1.055 * v ** (1 / 2.4) - 0.055
        out[i] = max(0, min(255, int(round(s * 255))))
    return bytes(out)


BACK = _build_back()


def luminance(r: int, g: int, b: int) -> float:
    return LUM[0] * LIN[r] + LUM[1] * LIN[g] + LUM[2] * LIN[b]


def ratio(l1: float, l2: float) -> float:
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


# ---------------------------------------------------------------- PNG in and out


def read_png(path: str) -> Image:
    with open(path, "rb") as f:
        data = f.read()
    if data[:8] != PNG_SIG:
        hint = " (it is a JPEG with a .png name)" if data[:3] == b"\xff\xd8\xff" else ""
        raise ValueError("not a PNG file" + hint)
    pos, idat, palette = 8, [], None
    width = height = depth = ctype = interlace = 0
    while pos < len(data):
        (length,) = struct.unpack(">I", data[pos:pos + 4])
        kind = data[pos + 4:pos + 8]
        body = data[pos + 8:pos + 8 + length]
        pos += 12 + length
        if kind == b"IHDR":
            width, height, depth, ctype, _, _, interlace = struct.unpack(">IIBBBBB", body)
        elif kind == b"PLTE":
            palette = body
        elif kind == b"IDAT":
            idat.append(body)
        elif kind == b"IEND":
            break
    if depth != 8:
        raise ValueError(f"bit depth {depth} is not supported (8 only)")
    if interlace:
        raise ValueError("interlaced PNGs are not supported")
    channels = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}.get(ctype)
    if channels is None:
        raise ValueError(f"color type {ctype} is not supported")
    if ctype == 3 and palette is None:
        raise ValueError("palette PNG without a PLTE chunk")
    raw = zlib.decompress(b"".join(idat))
    bpp = channels
    stride = width * bpp
    rows = _unfilter(raw, height, stride, bpp)
    rgb = bytearray(width * height * 3)
    if ctype == 2:
        rgb[:] = rows
    elif ctype == 6:
        rgb[0::3] = rows[0::4]
        rgb[1::3] = rows[1::4]
        rgb[2::3] = rows[2::4]
    elif ctype == 0:
        rgb[0::3] = rows
        rgb[1::3] = rows
        rgb[2::3] = rows
    elif ctype == 4:
        rgb[0::3] = rows[0::2]
        rgb[1::3] = rows[0::2]
        rgb[2::3] = rows[0::2]
    else:  # palette
        pr, pg, pb = palette[0::3], palette[1::3], palette[2::3]
        rgb[0::3] = bytes(pr[i] for i in rows)
        rgb[1::3] = bytes(pg[i] for i in rows)
        rgb[2::3] = bytes(pb[i] for i in rows)
    return Image(width, height, rgb)


def _unfilter(raw: bytes, height: int, stride: int, bpp: int) -> bytearray:
    out = bytearray(height * stride)
    prev = bytearray(stride)
    pos = 0
    for y in range(height):
        ftype = raw[pos]
        line = bytearray(raw[pos + 1:pos + 1 + stride])
        pos += 1 + stride
        if ftype == 1:  # Sub
            for i in range(bpp, stride):
                line[i] = (line[i] + line[i - bpp]) & 0xFF
        elif ftype == 2:  # Up
            line = bytearray((a + b) & 0xFF for a, b in zip(line, prev))
        elif ftype == 3:  # Average
            for i in range(stride):
                left = line[i - bpp] if i >= bpp else 0
                line[i] = (line[i] + ((left + prev[i]) >> 1)) & 0xFF
        elif ftype == 4:  # Paeth
            for i in range(stride):
                a = line[i - bpp] if i >= bpp else 0
                b = prev[i]
                c = prev[i - bpp] if i >= bpp else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                if pa <= pb and pa <= pc:
                    pred = a
                elif pb <= pc:
                    pred = b
                else:
                    pred = c
                line[i] = (line[i] + pred) & 0xFF
        elif ftype != 0:
            raise ValueError(f"bad PNG filter type {ftype} on row {y}")
        out[y * stride:(y + 1) * stride] = line
        prev = line
    return out


def write_png(path: str, img: Image) -> None:
    stride = img.width * 3
    raw = bytearray()
    for y in range(img.height):
        raw.append(0)
        raw += img.rgb[y * stride:(y + 1) * stride]

    def chunk(kind: bytes, body: bytes) -> bytes:
        return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", img.width, img.height, 8, 2, 0, 0, 0)
    with open(path, "wb") as f:
        f.write(PNG_SIG + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(bytes(raw), 6)) + chunk(b"IEND", b""))


# ---------------------------------------------------------------- the two versions


def _channel_lut(k: float) -> list[int]:
    return [int(round(k * LIN[i] * SCALE)) for i in range(256)]


def to_gray(img: Image) -> Image:
    lr, lg, lb = (_channel_lut(k) for k in LUM)
    src = img.rgb
    n = img.width * img.height
    out = bytearray(n * 3)
    back = BACK
    vals = bytes(back[min(SCALE, lr[r] + lg[g] + lb[b])] for r, g, b in zip(src[0::3], src[1::3], src[2::3]))
    out[0::3] = vals
    out[1::3] = vals
    out[2::3] = vals
    return Image(img.width, img.height, out)


def to_deut(img: Image) -> Image:
    luts = [[_channel_lut(k) for k in row] for row in DEUT]
    src = img.rgb
    rs, gs, bs = src[0::3], src[1::3], src[2::3]
    out = bytearray(len(src))
    back = BACK
    for ch, (lr, lg, lb) in enumerate(luts):
        out[ch::3] = bytes(
            back[max(0, min(SCALE, lr[r] + lg[g] + lb[b]))] for r, g, b in zip(rs, gs, bs)
        )
    return Image(img.width, img.height, out)


# ---------------------------------------------------------------- contrast


@dataclass
class Result:
    kind: str  # text, edge, image, colors
    name: str
    fg: tuple[int, int, int]
    bg: tuple[int, int, int]
    value: float
    need: float | None  # None: informational only

    @property
    def ok(self) -> bool:
        return self.need is None or self.value >= self.need


def _hex(c: tuple[int, int, int]) -> str:
    return "#%02X%02X%02X" % c


def _pixel(img: Image, x: int, y: int) -> tuple[int, int, int]:
    i = (y * img.width + x) * 3
    return img.rgb[i], img.rgb[i + 1], img.rgb[i + 2]


def _box_pixels(img: Image, x: int, y: int, w: int, h: int) -> list[tuple[float, tuple[int, int, int]]]:
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(img.width, x + w), min(img.height, y + h)
    if x1 <= x0 or y1 <= y0:
        raise ValueError(f"box {x},{y},{w},{h} is outside the {img.width}x{img.height} image")
    px = []
    step = max(1, int(((x1 - x0) * (y1 - y0) / 400_000) ** 0.5))  # sample big boxes
    for yy in range(y0, y1, step):
        for xx in range(x0, x1, step):
            c = _pixel(img, xx, yy)
            px.append((luminance(*c), c))
    px.sort(key=lambda t: t[0])
    return px


def measure_box(img: Image, name: str, box: tuple[int, int, int, int], kind: str, need: float | None) -> Result:
    px = _box_pixels(img, *box)
    n = len(px)
    bg_l, bg_c = px[n // 2]
    lo_l, lo_c = px[min(n - 1, int(n * 0.01))]
    hi_l, hi_c = px[max(0, int(n * 0.99) - 1)]
    lo_r, hi_r = ratio(bg_l, lo_l), ratio(bg_l, hi_l)
    fg_c, val = (lo_c, lo_r) if lo_r >= hi_r else (hi_c, hi_r)
    return Result(kind, name, fg_c, bg_c, val, need)


def measure_edge(img: Image, name: str, line: tuple[int, int, int, int]) -> Result:
    x0, y0, x1, y1 = line
    for x, y in ((x0, y0), (x1, y1)):
        if not (0 <= x < img.width and 0 <= y < img.height):
            raise ValueError(f"edge point {x},{y} is outside the {img.width}x{img.height} image")
    steps = max(abs(x1 - x0), abs(y1 - y0), 1)
    out_c = _pixel(img, x0, y0)
    out_l = luminance(*out_c)
    best_c, best = out_c, 1.0
    for s in range(1, steps + 1):
        x = round(x0 + (x1 - x0) * s / steps)
        y = round(y0 + (y1 - y0) * s / steps)
        c = _pixel(img, x, y)
        r = ratio(out_l, luminance(*c))
        if r > best:
            best_c, best = c, r
    return Result("edge", name, best_c, out_c, best, EDGE_MIN)


def parse_color(s: str) -> tuple[int, int, int]:
    s = s.strip().lstrip("#")
    if len(s) != 6:
        raise ValueError(f"color {s!r} is not RRGGBB")
    return int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16)


def _named(spec: str, count: int) -> tuple[str, tuple[int, ...]]:
    if "=" in spec:
        name, nums = spec.split("=", 1)
    else:
        name, nums = "", spec
    parts = [int(float(v)) for v in nums.replace(" ", "").split(",")]
    if len(parts) != count:
        raise ValueError(f"{spec!r} needs {count} numbers")
    return name or nums, tuple(parts)


# ---------------------------------------------------------------- main


def _line(r: Result, md: bool, shot: str) -> str:
    need = "" if r.need is None else f"{r.need:g}:1"
    verdict = "info" if r.need is None else ("ok" if r.ok else "FAIL")
    if md:
        return f"| {shot} | {r.kind} | {r.name} | {_hex(r.fg)} on {_hex(r.bg)} | {r.value:.1f}:1 | {need or '-'} | {verdict} |"
    return f"  {r.kind:<6} {r.name:<22} {_hex(r.fg)} on {_hex(r.bg)}  {r.value:5.1f}:1  {verdict}{' (needs ' + need + ')' if need else ''}"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0], formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("png", nargs="*", help="screenshots (PNG)")
    ap.add_argument("--out", help="folder for the _gray and _deut versions (default: next to each PNG)")
    ap.add_argument("--no-variants", action="store_true", help="don't write the _gray and _deut versions")
    ap.add_argument("--no-contrast", action="store_true", help="don't print the rough whole-image figure")
    ap.add_argument("--text", action="append", default=[], metavar="NAME=X,Y,W,H", help="a text box (needs 4.5:1)")
    ap.add_argument("--edge", action="append", default=[], metavar="NAME=X0,Y0,X1,Y1", help="a line across an edge (needs 3:1)")
    ap.add_argument("--colors", nargs=2, metavar="HEX", help="the ratio of two colors")
    ap.add_argument("--md", action="store_true", help="print measurements as Markdown table rows")
    args = ap.parse_args(argv)

    if not args.png and not args.colors:
        ap.print_help()
        return 2

    failed = False
    bad_file = False
    if args.md:
        print("| Shot | Kind | What | Colors | Contrast | Needs | |")
        print("|---|---|---|---|---|---|---|")

    if args.colors:
        try:
            a, b = (parse_color(c) for c in args.colors)
        except ValueError as e:
            print(f"error: {e}", file=sys.stderr)
            return 2
        r = Result("colors", "pair", a, b, ratio(luminance(*a), luminance(*b)), None)
        print(_line(r, args.md, "-"))

    try:
        texts = [_named(s, 4) for s in args.text]
        edges = [_named(s, 4) for s in args.edge]
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    if args.out:
        os.makedirs(args.out, exist_ok=True)

    for path in args.png:
        stem, _ = os.path.splitext(os.path.basename(path))
        if stem.endswith("_gray") or stem.endswith("_deut"):
            continue
        try:
            img = read_png(path)
        except (OSError, ValueError, zlib.error) as e:
            print(f"{path}: error: {e}", file=sys.stderr)
            bad_file = True
            continue
        if not args.md:
            print(f"{path}  {img.width}x{img.height}")
        if not args.no_variants:
            folder = args.out or os.path.dirname(path) or "."
            for suffix, fn in (("_gray", to_gray), ("_deut", to_deut)):
                dest = os.path.join(folder, stem + suffix + ".png")
                write_png(dest, fn(img))
                if not args.md:
                    print(f"  wrote  {dest}")
        results: list[Result] = []
        try:
            for name, box in texts:
                results.append(measure_box(img, name, box, "text", TEXT_MIN))
            for name, line in edges:
                results.append(measure_edge(img, name, line))
        except ValueError as e:
            print(f"{path}: error: {e}", file=sys.stderr)
            bad_file = True
            continue
        if not results and not args.no_contrast:
            results.append(measure_box(img, "whole image (rough)", (0, 0, img.width, img.height), "image", None))
        for r in results:
            print(_line(r, args.md, stem))
            failed = failed or not r.ok
    if bad_file:
        return 2
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
