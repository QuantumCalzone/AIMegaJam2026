#!/usr/bin/env python3
"""Measure the loudness of audio files: integrated LUFS (ITU-R BS.1770-4), peak and clipped samples.

Written for T102 (the audio import and the mix). Python 3.10+, no packages.

    python Tools/measure_loudness.py SourceAssets/Audio/music/t100
    python Tools/measure_loudness.py --md out.md --json out.json <file or folder> ...

- 16-bit and 24-bit PCM `.wav` files are read directly. Every other format (`.flac`, `.ogg`, `.mp3`,
  float `.wav`) is first decoded to a 16-bit WAV in a temp folder, with `afconvert` (on every Mac)
  or `ffmpeg` (if it is on PATH). A file neither tool can decode is reported and skipped.
- Folders are searched recursively for .wav, .flac, .ogg, .mp3, .aif and .aiff files.
- The work is spread over the CPU's cores, since the K-weighting filter runs in plain Python.

Columns:
- `LUFS`: integrated loudness, BS.1770-4 (K-weighting, 400 ms blocks with 75% overlap, an absolute
  gate at -70 LUFS and a relative gate 10 LU under the ungated mean). Needs at least 400 ms of audio;
  shorter files print "-".
- `ungated`: the K-weighted loudness of the whole file with no gate. For a short sound (a syllable,
  a click) this is the number to compare; for a loop it is close to `LUFS`.
- `M max`: the loudest 400 ms block (momentary loudness), in LUFS.
- `peak`: the highest sample, in dBFS (sample peak, not true peak; a true peak can be up to about
  0.5 dB higher).
- `clip`: samples at full scale (|x| >= 32767 on the 16-bit scale).

Sum of the channel powers with weight 1.0 each (the stereo and mono case of BS.1770). A mono file is
measured as one channel, so a mono and a stereo file with the same samples in each channel differ
by 3 dB, as BS.1770 says they should.
"""

from __future__ import annotations

import argparse
import array
import concurrent.futures
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import wave

AUDIO_EXT = {".wav", ".flac", ".ogg", ".mp3", ".aif", ".aiff"}


# ---------- decoding ----------

def _read_pcm_wav(path: str):
    """Returns (rate, [channel arrays of floats in -1..1]) for a 16/24-bit PCM WAV, or None."""
    try:
        with wave.open(path, "rb") as w:
            ch, width, rate, n = w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
            raw = w.readframes(n)
    except (wave.Error, EOFError):
        return None  # float or extensible formats the wave module refuses
    if width == 2:
        a = array.array("h")
        a.frombytes(raw)
        if sys.byteorder == "big":
            a.byteswap()
        scale = 1.0 / 32768.0
        data = a
    elif width == 3:
        # 24-bit little-endian: widen to 32-bit by hand
        count = len(raw) // 3
        data = array.array("i", [0]) * count
        for i in range(count):
            b = raw[3 * i:3 * i + 3]
            v = b[0] | (b[1] << 8) | (b[2] << 16)
            data[i] = v - (1 << 24) if v & 0x800000 else v
        scale = 1.0 / 8388608.0
    else:
        return None
    chans = [[s * scale for s in data[c::ch]] for c in range(ch)]
    return rate, chans


def _decode_to_wav(path: str, tmpdir: str) -> str | None:
    out = os.path.join(tmpdir, os.path.basename(path) + ".wav")
    if shutil.which("afconvert"):
        cmd = ["afconvert", "-f", "WAVE", "-d", "LEI16", path, out]
    elif shutil.which("ffmpeg"):
        cmd = ["ffmpeg", "-v", "error", "-y", "-i", path, "-c:a", "pcm_s16le", out]
    else:
        return None
    r = subprocess.run(cmd, capture_output=True, text=True)
    return out if r.returncode == 0 and os.path.exists(out) else None


def load(path: str):
    if path.lower().endswith(".wav"):
        got = _read_pcm_wav(path)
        if got:
            return got
    with tempfile.TemporaryDirectory() as tmp:
        wav = _decode_to_wav(path, tmp)
        if not wav:
            return None
        return _read_pcm_wav(wav)


# ---------- BS.1770-4 ----------

def k_weight_coeffs(rate: float):
    """The two biquads of the K-weighting filter for any sample rate (the BS.1770 analog prototypes,
    bilinear-transformed; at 48 kHz they match the coefficients printed in the standard)."""
    # Stage 1: high shelf (+4 dB above about 1.5 kHz)
    f0, G, Q = 1681.974450955533, 3.999843853973347, 0.7071752369554196
    K = math.tan(math.pi * f0 / rate)
    Vh = 10 ** (G / 20)
    Vb = Vh ** 0.4996667741545416
    a0 = 1 + K / Q + K * K
    b = ((Vh + Vb * K / Q + K * K) / a0, 2 * (K * K - Vh) / a0, (Vh - Vb * K / Q + K * K) / a0)
    a = (2 * (K * K - 1) / a0, (1 - K / Q + K * K) / a0)
    # Stage 2: high pass (RLB, about 38 Hz)
    f0, Q = 38.13547087602444, 0.5003270373238773
    K = math.tan(math.pi * f0 / rate)
    a0 = 1 + K / Q + K * K
    b2 = (1.0, -2.0, 1.0)
    a2 = (2 * (K * K - 1) / a0, (1 - K / Q + K * K) / a0)
    return b, a, b2, a2


def filtered_power_segments(x, rate: int, seg: int):
    """K-weights one channel and returns the sum of squares of each `seg`-sample segment."""
    (b0, b1, b2), (a1, a2), (c0, c1, c2), (d1, d2) = k_weight_coeffs(rate)
    x1 = x2 = y1 = y2 = z1 = z2 = 0.0
    out = []
    acc = 0.0
    k = 0
    for s in x:
        y = b0 * s + b1 * x1 + b2 * x2 - a1 * y1 - a2 * y2
        x2, x1 = x1, s
        z = c0 * y + c1 * y1 + c2 * y2 - d1 * z1 - d2 * z2
        y2, y1 = y1, y
        z2, z1 = z1, z
        acc += z * z
        k += 1
        if k == seg:
            out.append(acc)
            acc = 0.0
            k = 0
    tail = (acc, k)
    return out, tail


def lufs(ms: float) -> float:
    return -0.691 + 10 * math.log10(ms) if ms > 0 else float("-inf")


def measure(path: str) -> dict:
    got = load(path)
    if not got:
        return {"file": path, "error": "can't decode (no afconvert or ffmpeg, or an odd format)"}
    rate, chans = got
    n = len(chans[0])
    seg = int(round(rate * 0.1))  # 100 ms; a 400 ms block is 4 segments
    per_ch = [filtered_power_segments(c, rate, seg) for c in chans]
    nseg = len(per_ch[0][0])
    segs = [sum(pc[0][i] for pc in per_ch) for i in range(nseg)]
    total = sum(segs) + sum(pc[1][0] for pc in per_ch)
    ungated = lufs(total / n) if n else float("-inf")
    blocks = [sum(segs[i:i + 4]) / (4 * seg) for i in range(0, max(0, nseg - 3))]
    integrated = None
    mmax = None
    if blocks:
        mmax = lufs(max(blocks))
        abs_gated = [z for z in blocks if lufs(z) > -70.0]
        if abs_gated:
            rel = lufs(sum(abs_gated) / len(abs_gated)) - 10.0
            rel_gated = [z for z in abs_gated if lufs(z) > rel]
            if rel_gated:
                integrated = lufs(sum(rel_gated) / len(rel_gated))
    peak = max(max(abs(min(c)), abs(max(c))) for c in chans)
    clip_level = 32767 / 32768
    clipped = sum(1 for c in chans for s in c if abs(s) >= clip_level)
    return {
        "file": path,
        "rate": rate,
        "channels": len(chans),
        "seconds": round(n / rate, 3),
        "lufs": None if integrated is None else round(integrated, 2),
        "ungated": None if ungated == float("-inf") else round(ungated, 2),
        "m_max": None if mmax is None else round(mmax, 2),
        "peak_dbfs": None if peak <= 0 else round(20 * math.log10(peak), 2),
        "clipped": clipped,
    }


# ---------- CLI ----------

def gather(paths):
    files = []
    for p in paths:
        if os.path.isdir(p):
            for root, _, names in os.walk(p):
                for nm in sorted(names):
                    if os.path.splitext(nm)[1].lower() in AUDIO_EXT:
                        files.append(os.path.join(root, nm))
        elif os.path.isfile(p):
            files.append(p)
        else:
            print(f"not found: {p}", file=sys.stderr)
    return sorted(set(files))


def fmt(v, nd=1):
    return "-" if v is None else f"{v:.{nd}f}"


def table(rows):
    out = ["| File | s | ch | LUFS | ungated | M max | peak dBFS | clip |", "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        if "error" in r:
            out.append(f"| `{r['file']}` | {r['error']} | | | | | | |")
            continue
        out.append(
            f"| `{r['file']}` | {r['seconds']:.1f} | {r['channels']} | {fmt(r['lufs'])} | {fmt(r['ungated'])} "
            f"| {fmt(r['m_max'])} | {fmt(r['peak_dbfs'])} | {r['clipped']} |"
        )
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+", help="files or folders")
    ap.add_argument("--json", help="write every result to this JSON file")
    ap.add_argument("--md", help="write the table to this Markdown file")
    ap.add_argument("--jobs", type=int, default=os.cpu_count() or 2)
    args = ap.parse_args()
    files = gather(args.paths)
    if not files:
        sys.exit("no audio files found")
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.jobs) as ex:
        rows = list(ex.map(measure, files))
    md = table(rows)
    print(md)
    if args.md:
        with open(args.md, "w", encoding="utf-8") as f:
            f.write(md + "\n")
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(rows, f, indent=1)


if __name__ == "__main__":
    main()
