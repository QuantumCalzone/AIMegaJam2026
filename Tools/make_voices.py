#!/usr/bin/env python3
"""Make the robots' syllable voices (T72), and cut my own recorded voice into clips.

Usage (from anywhere; Python 3.10+, standard library only, no numpy):

    python Tools/make_voices.py                 # write the four robot sets, print each clip's numbers
    python Tools/make_voices.py --stats         # print the numbers only, write nothing
    python Tools/make_voices.py --me TAKE.wav   # cut my one-take recording into the "Me" set
    python Tools/make_voices.py --measure FILE.wav [...]   # print the numbers of any 16-bit wav

Each robot gets its own set of short gibberish syllables, as in games where a
character "talks" in little sounds while its words type out. T73 plays one per
syllable through BPC_ShowAudio.Syllable. The sets are written to
SourceAssets/Audio/voices/<Provider>/S_Voice<Provider>_NN.wav (44.1 kHz, 16-bit,
mono), and the editor's auto-import turns each into a SoundWave in
Content/NHOS/Audio/Voice/<Provider>/ (see T20's findings).

How a syllable is made: a buzzy source at a pitch (f0) that moves along a short
contour, through a vowel filter (three formant resonators in parallel), with
an optional consonant in front (a noise burst, a hiss or a hum), a quick attack
and a short tail. Each provider has its own source, vowels, contour and effect,
so the four differ in tone and not only in pitch:

  OpenAI    clean, bright chirp: soft sine harmonics, front vowels (ee, eh, a),
            a calm upward glide, a breath of air. Calm hype about the future.
  Anthropic warm, round vowel: a smooth glottal pulse, rounded vowels (oh, oo,
            ah), a low-pass, a small nervous flutter and a falling, sighing end.
  SpaceXAI  crunchy, bit-crushed buzz: a square-and-saw source driven into
            clipping, crushed to a few bits and a low sample rate, with jumpy
            pitch steps. Loud, chaotic, overclocked.
  Meta      low, wobbly drone: a dark saw with a nasal hum, a wide vibrato and
            tremolo (8 Hz, so it wobbles inside one syllable), a flat monotone. Stiff, trying hard to sound human.

T20's pitch order holds (Meta lowest, then Anthropic, then OpenAI, with
SpaceXAI highest): the base pitches are T20's blip pitches times 175 Hz.

Levels: every clip, mine included, is set to the same loudness (an RMS taken
through a rough loudness weighting: a high-pass at 100 Hz and a +4 dB shelf
above 1.5 kHz), with its peak kept under -1 dBFS. The target, -25.5 dB, is what
T20's talk blip file (Kenney's pluck_001) measures with the same weighting, so
the voices take the blip's own settings in the game: wave volume 0.6 under
SC_Voice (0.5), which is 0.3 effective. `--measure` prints any wav's numbers.

The random seed is fixed, so a second run writes the same bytes. The last line
it prints is a hash of all the files, to check that.

--me: give it one take (a 16-bit wav; convert an .m4a or .mp3 first on a Mac
with `afconvert -f WAVE -d LEI16@44100 -c 1 take.m4a take.wav`). It finds the
syllables by the gaps of silence between them, trims each with a short fade,
keeps the breaths and wobble of the voice, sets each to the same loudness as
the robots and writes SourceAssets/Audio/voices/Me/S_VoiceMe_NN.wav. Clips
longer than --max-len seconds (default 0.35) are cut short with a fade.
--first N keeps only the first N syllables found. T72's set is
`--me SourceAssets/Audio/voices/Me/source/recording.wav --first 12 --max-len 0.25`: the take says beep, boop, bzzt,
dee, doo, bop, kshh, blip, zap, bleep, dah, wub, then five more that are not used.
"""

import argparse
import cmath
import hashlib
import math
import os
import random
import struct
import sys
import wave

SR = 44100
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "SourceAssets", "Audio", "voices")
SEED = 7272

TARGET_LOUD_DB = -25.5   # weighted RMS of every clip, in dBFS: T20's talk blip file measures -25.6
PEAK_CAP_DB = -1.0       # no clip peaks above this
BASE_F0 = 175.0          # T20's blip pitch 1.0 (my own lines)

# Vowel formants (F1, F2, F3) in Hz for an adult voice; each provider scales them.
VOWELS = {
    "a": (730, 1090, 2440),
    "ae": (660, 1720, 2410),
    "eh": (530, 1840, 2480),
    "ee": (270, 2290, 3010),
    "ih": (390, 1990, 2550),
    "oh": (570, 840, 2410),
    "oo": (300, 870, 2240),
    "uh": (640, 1190, 2390),
    "aw": (590, 920, 2540),
}


# ---------------------------------------------------------------- filters

class Biquad:
    """RBJ cookbook biquad, direct form I."""

    def __init__(self, kind, freq, q=0.707, gain_db=0.0):
        w0 = 2 * math.pi * min(freq, SR * 0.45) / SR
        cw, sw = math.cos(w0), math.sin(w0)
        alpha = sw / (2 * q)
        a_lin = 10 ** (gain_db / 40)
        if kind == "lp":
            b = [(1 - cw) / 2, 1 - cw, (1 - cw) / 2]
            a = [1 + alpha, -2 * cw, 1 - alpha]
        elif kind == "hp":
            b = [(1 + cw) / 2, -(1 + cw), (1 + cw) / 2]
            a = [1 + alpha, -2 * cw, 1 - alpha]
        elif kind == "bp":  # constant 0 dB peak gain
            b = [alpha, 0.0, -alpha]
            a = [1 + alpha, -2 * cw, 1 - alpha]
        elif kind == "hshelf":
            sq = 2 * math.sqrt(a_lin) * alpha
            b = [a_lin * ((a_lin + 1) + (a_lin - 1) * cw + sq),
                 -2 * a_lin * ((a_lin - 1) + (a_lin + 1) * cw),
                 a_lin * ((a_lin + 1) + (a_lin - 1) * cw - sq)]
            a = [(a_lin + 1) - (a_lin - 1) * cw + sq,
                 2 * ((a_lin - 1) - (a_lin + 1) * cw),
                 (a_lin + 1) - (a_lin - 1) * cw - sq]
        else:
            raise ValueError(kind)
        self.b = [x / a[0] for x in b]
        self.a = [1.0, a[1] / a[0], a[2] / a[0]]
        self.x1 = self.x2 = self.y1 = self.y2 = 0.0

    def step(self, x):
        b, a = self.b, self.a
        y = b[0] * x + b[1] * self.x1 + b[2] * self.x2 - a[1] * self.y1 - a[2] * self.y2
        self.x2, self.x1 = self.x1, x
        self.y2, self.y1 = self.y1, y
        return y

    def run(self, xs):
        return [self.step(x) for x in xs]


def formant_filter(src, formant_tracks, gains, qs):
    """Parallel resonators whose centre moves per sample (tracks are lists of Hz).

    Coefficients are recomputed every 32 samples, which is smooth enough for
    glides this short.
    """
    out = [0.0] * len(src)
    for track, g, q in zip(formant_tracks, gains, qs):
        f = Biquad("bp", track[0], q)
        for i, x in enumerate(src):
            if i % 32 == 0 and i:
                nf = Biquad("bp", track[i], q)
                f.b, f.a = nf.b, nf.a
            out[i] += g * f.step(x)
    return out


# ---------------------------------------------------------------- sources

def f0_track(n, f0, contour, rng, vib_hz=0.0, vib_depth=0.0, jitter=0.0):
    """Per-sample pitch. contour is a list of (time 0..1, ratio) points."""
    track = []
    jit = 1.0
    for i in range(n):
        t = i / max(1, n - 1)
        # piecewise-linear contour
        r = contour[-1][1]
        for (t0, r0), (t1, r1) in zip(contour, contour[1:]):
            if t0 <= t <= t1:
                r = r0 + (r1 - r0) * ((t - t0) / max(1e-9, t1 - t0))
                break
        if jitter and i % 220 == 0:
            jit = 1.0 + rng.uniform(-jitter, jitter)
        v = 1.0 + vib_depth * math.sin(2 * math.pi * vib_hz * i / SR) if vib_hz else 1.0
        track.append(f0 * r * v * jit)
    return track


def phases(track):
    ph, out = 0.0, []
    for f in track:
        out.append(ph)
        ph += f / SR
        ph -= math.floor(ph)
    return out


def src_harmonics(track, rolloff=2.0, top=4500.0):
    """Sum of sine harmonics up to `top` Hz, amplitude 1/n^rolloff. Clean."""
    out = []
    ph = 0.0
    for f in track:
        ph += 2 * math.pi * f / SR
        nmax = max(1, int(top / max(f, 1.0)))
        s = 0.0
        for k in range(1, nmax + 1):
            s += math.sin(k * ph) / (k ** rolloff)
        out.append(s)
    return out


def src_glottal(track, open_q=0.6):
    """Rosenberg glottal pulse, differentiated: a smooth, warm buzz."""
    raw = []
    for p in phases(track):
        if p < open_q * 0.66:
            g = 0.5 * (1 - math.cos(math.pi * p / (open_q * 0.66)))
        elif p < open_q:
            g = math.cos(0.5 * math.pi * (p - open_q * 0.66) / (open_q * 0.34))
        else:
            g = 0.0
        raw.append(g)
    return [raw[i] - raw[i - 1] if i else 0.0 for i in range(len(raw))]


def src_saw(track):
    return [2 * p - 1 for p in phases(track)]


def src_square(track, duty=0.5):
    return [1.0 if p < duty else -1.0 for p in phases(track)]


def noise(n, rng):
    return [rng.uniform(-1, 1) for _ in range(n)]


# ---------------------------------------------------------------- shaping

def envelope(n, attack_s, tail_s, hold_curve=1.0):
    a = max(1, int(attack_s * SR))
    tl = max(1, int(tail_s * SR))
    env = []
    for i in range(n):
        if i < a:
            e = math.sin(0.5 * math.pi * i / a)
        else:
            e = 1.0
        rem = n - 1 - i
        if rem < tl:
            e *= (rem / tl) ** 1.6
        env.append(e)
    return env


def bitcrush(xs, bits, hold):
    levels = 2 ** (bits - 1)
    out, cur = [], 0.0
    for i, x in enumerate(xs):
        if i % hold == 0:
            cur = round(max(-1.0, min(1.0, x)) * levels) / levels
        out.append(cur)
    return out


def softclip(xs, drive):
    k = math.tanh(drive)
    return [math.tanh(drive * x) / k for x in xs]


def norm_peak(xs):
    m = max(1e-9, max(abs(x) for x in xs))
    return [x / m for x in xs]


def consonant(kind, rng, f0_hz):
    """A short onset sound. Returns samples (already enveloped)."""
    if kind == "":
        return []
    if kind in ("b", "d", "g", "p", "t", "k"):
        centre = {"b": 700, "p": 900, "d": 3200, "t": 4200, "g": 1800, "k": 2400}[kind]
        n = int(SR * (0.008 if kind in "bdg" else 0.014))
        nz = Biquad("bp", centre, 1.2).run(noise(n, rng))
        env = [math.exp(-5 * i / n) for i in range(n)]
        return [0.9 * x * e for x, e in zip(nz, env)]
    if kind in ("s", "sh", "z", "ks"):
        centre = {"s": 6500, "sh": 3000, "z": 5500, "ks": 4500}[kind]
        n = int(SR * (0.028 if kind != "ks" else 0.036))
        nz = Biquad("hp", centre * 0.6, 0.7).run(Biquad("bp", centre, 0.9).run(noise(n, rng)))
        if kind == "z":
            buzz = src_saw([f0_hz] * n)
            nz = [0.7 * a + 0.25 * b for a, b in zip(nz, buzz)]
        env = envelope(n, 0.006, 0.010)
        return [0.6 * x * e for x, e in zip(nz, env)]
    if kind in ("m", "n"):
        n = int(SR * 0.022)
        hum = Biquad("lp", 400 if kind == "m" else 550, 1.0).run(src_glottal([f0_hz] * n))
        hum = norm_peak(hum)
        env = envelope(n, 0.004, 0.004)
        return [0.45 * x * e for x, e in zip(hum, env)]
    raise ValueError(kind)


# ---------------------------------------------------------------- voices

def body_len(total_s, onset):
    """Samples left for the vowel once the onset is in, so a clip stays total_s long."""
    return max(int(0.05 * SR), int(total_s * SR) - len(onset))


def vowel_tracks(n, v_from, v_to, scale):
    a, b = VOWELS[v_from], VOWELS[v_to]
    tracks = []
    for k in range(3):
        tracks.append([scale * (a[k] + (b[k] - a[k]) * (i / max(1, n - 1)) ** 1.5) for i in range(n)])
    return tracks


def syl_openai(rng, i):
    f0 = BASE_F0 * 1.15
    dur = rng.uniform(0.075, 0.12)
    vowels = ["ee", "ih", "eh", "ae", "a", "ee", "eh", "ih", "ae", "ee"]
    onsets = ["", "b", "d", "", "t", "m", "", "d", "b", "n"]
    on = consonant(onsets[i % len(onsets)], rng, f0)
    n = body_len(dur, on)
    v = vowels[i % len(vowels)]
    v2 = rng.choice(["ee", "ih", "eh"])
    # calm upward glide: "vibing about the future"
    rise = rng.uniform(1.12, 1.30)
    contour = [(0, rng.uniform(0.94, 1.0)), (0.7, rise), (1, rise * 1.02)]
    tr = f0_track(n, f0 * rng.uniform(0.96, 1.05), contour, rng, vib_hz=5.0, vib_depth=0.006)
    src = src_harmonics(tr, rolloff=0.7, top=7000)   # many soft sine harmonics: clean, no buzz
    air = Biquad("hp", 4000, 0.7).run(noise(n, rng))
    src = [s + 0.03 * a for s, a in zip(src, air)]
    out = formant_filter(src, vowel_tracks(n, v, v2, 1.15), [0.6, 1.0, 0.9], [6, 8, 9])
    out = [0.15 * s + 0.85 * o for s, o in zip(norm_peak(src), norm_peak(out))]
    out = Biquad("hshelf", 2000, 0.7, 6.0).run(Biquad("hp", 350, 0.7).run(out))  # bright, no boom
    # a faint 23 ms echo for air
    d = int(0.023 * SR)
    out = [x + (0.18 * out[k - d] if k >= d else 0.0) for k, x in enumerate(out)]
    env = envelope(n, 0.005, rng.uniform(0.025, 0.035))
    body = [x * e for x, e in zip(norm_peak(out), env)]
    return on + body


def syl_anthropic(rng, i):
    f0 = BASE_F0 * 0.85
    dur = rng.uniform(0.085, 0.135)
    vowels = ["oh", "oo", "a", "aw", "uh", "oh", "oo", "a", "aw", "oh"]
    onsets = ["m", "", "b", "n", "", "d", "m", "w", "", "b"]
    v = vowels[i % len(vowels)]
    v2 = rng.choice(["oo", "oh", "uh"])
    onset = onsets[i % len(onsets)]
    v_from, v_to = v, v2
    if onset == "w":  # a w is a quick oo-glide into the vowel, with no noise in front
        onset, v_from, v_to = "", "oo", v
    on = consonant(onset, rng, f0)
    n = body_len(dur, on)
    # earnest, a little anxious: a small rise, then a falling, sighing end
    contour = [(0, 1.0), (0.3, rng.uniform(1.04, 1.10)), (1, rng.uniform(0.86, 0.93))]
    tr = f0_track(n, f0 * rng.uniform(0.96, 1.04), contour, rng, vib_hz=9.0, vib_depth=0.018, jitter=0.012)
    src = src_glottal(tr, open_q=0.65)
    out = formant_filter(src, vowel_tracks(n, v_from, v_to, 1.0), [1.0, 0.55, 0.22], [6, 8, 9])
    out = Biquad("lp", 2200, 0.8).run(Biquad("hp", 90, 0.7).run(out))
    env = envelope(n, 0.007, rng.uniform(0.030, 0.040))
    body = [x * e for x, e in zip(norm_peak(out), env)]
    return on + body


def syl_spacex(rng, i):
    f0 = BASE_F0 * 1.30
    dur = rng.uniform(0.07, 0.12)
    vowels = ["a", "ee", "ae", "ih", "a", "eh", "ee", "uh", "a", "ae", "ih"]
    onsets = ["z", "k", "t", "ks", "b", "z", "d", "k", "", "t", "z"]
    on = consonant(onsets[i % len(onsets)], rng, f0)
    n = body_len(dur, on)
    v = vowels[i % len(vowels)]
    v2 = rng.choice(["a", "ee", "ae"])
    # jumpy: steps between two pitch levels, or a fast zip
    if rng.random() < 0.5:
        hi = rng.uniform(1.15, 1.35)
        contour = [(0, 1.0), (0.45, 1.0), (0.46, hi), (1, hi)]
    else:
        contour = [(0, rng.uniform(1.25, 1.45)), (1, rng.uniform(0.85, 0.95))]
    tr = f0_track(n, f0 * rng.uniform(0.95, 1.06), contour, rng)
    sq, sw = src_square(tr, duty=rng.uniform(0.3, 0.5)), src_saw(tr)
    src = [0.6 * a + 0.4 * b for a, b in zip(sq, sw)]
    out = formant_filter(src, vowel_tracks(n, v, v2, 1.2), [1.0, 0.8, 0.5], [5, 7, 8])
    out = softclip(norm_peak(out), 4.0)
    out = bitcrush(out, bits=3, hold=6)            # 7.35 kHz, 3 bits: the steps buzz and alias
    out = Biquad("lp", 10000, 0.7).run(Biquad("hp", 250, 0.7).run(out))
    env = envelope(n, 0.003, rng.uniform(0.018, 0.026))
    body = [x * e for x, e in zip(norm_peak(out), env)]
    return on + body


def syl_meta(rng, i):
    f0 = BASE_F0 * 0.70
    dur = rng.uniform(0.10, 0.145)
    vowels = ["uh", "a", "oh", "eh", "uh", "aw", "a", "oh", "uh", "eh"]
    onsets = ["m", "n", "d", "m", "", "b", "n", "", "d", "m"]
    on = consonant(onsets[i % len(onsets)], rng, f0)
    n = body_len(dur, on)
    v = vowels[i % len(vowels)]
    # stiff and flat: a monotone, made wobbly by a wide slow vibrato
    contour = [(0, 1.0), (1, rng.uniform(0.98, 1.02))]
    vib = rng.uniform(7.5, 8.5)
    tr = f0_track(n, f0 * rng.uniform(0.98, 1.02), contour, rng, vib_hz=vib, vib_depth=0.07)
    src = src_saw(tr)
    out = formant_filter(src, vowel_tracks(n, v, v, 0.9), [1.0, 0.45, 0.18], [6, 7, 8])
    hum = Biquad("bp", 260, 3.0).run(src)  # nasal hum
    out = [o + 0.6 * h for o, h in zip(norm_peak(out), norm_peak(hum))]
    out = Biquad("lp", 1600, 0.9).run(Biquad("hp", 70, 0.7).run(out))
    trem = [1.0 - 0.28 * (0.5 + 0.5 * math.sin(2 * math.pi * vib * k / SR)) for k in range(n)]
    env = envelope(n, 0.008, rng.uniform(0.032, 0.042))
    body = [x * t * e for x, t, e in zip(norm_peak(out), trem, env)]
    return on + body


PROVIDERS = [
    # (folder and asset name, seed offset, maker, clip count)
    ("OpenAI", 1, syl_openai, 10),
    ("Anthropic", 2, syl_anthropic, 10),
    ("SpaceXAI", 3, syl_spacex, 11),
    ("Meta", 4, syl_meta, 10),
]


# ---------------------------------------------------------------- levels and analysis

def db(x):
    return 20 * math.log10(max(x, 1e-9))


def rms(xs):
    return math.sqrt(sum(x * x for x in xs) / max(1, len(xs)))


def loud_weighted(xs):
    w = Biquad("hshelf", 1500, 0.7, 4.0).run(Biquad("hp", 100, 0.5).run(xs))
    return rms(w)


def level(xs):
    """Set the weighted loudness to the target, and keep the peak under the cap."""
    g = (10 ** (TARGET_LOUD_DB / 20)) / max(1e-9, loud_weighted(xs))
    pk = max(abs(x) for x in xs) * g
    cap = 10 ** (PEAK_CAP_DB / 20)
    if pk > cap:
        g *= cap / pk
    return [x * g for x in xs]


def fft(a):
    n = len(a)
    if n == 1:
        return a
    ev, od = fft(a[0::2]), fft(a[1::2])
    t = [cmath.exp(-2j * math.pi * k / n) * od[k] for k in range(n // 2)]
    return [ev[k] + t[k] for k in range(n // 2)] + [ev[k] - t[k] for k in range(n // 2)]


BANDS = [(0, 300), (300, 1000), (1000, 3000), (3000, 8000), (8000, 22050)]


def spectrum_stats(xs):
    """Centroid, flatness and band shares, averaged over 1024-sample Hann frames."""
    N = 1024
    hann = [0.5 - 0.5 * math.cos(2 * math.pi * k / (N - 1)) for k in range(N)]
    frames = []
    pos = 0
    while pos + N <= len(xs) or not frames:
        fr = xs[pos:pos + N]
        fr = fr + [0.0] * (N - len(fr))
        frames.append(fr)
        pos += N // 2
        if pos + N > len(xs):
            break
    power = [0.0] * (N // 2)
    for fr in frames:
        sp = fft([x * h for x, h in zip(fr, hann)])
        for k in range(1, N // 2):
            power[k] += abs(sp[k]) ** 2
    tot = sum(power) or 1e-12
    freqs = [k * SR / N for k in range(N // 2)]
    centroid = sum(f * p for f, p in zip(freqs, power)) / tot
    nz = [p for p in power[1:] if p > 0]
    geo = math.exp(sum(math.log(p) for p in nz) / len(nz)) if nz else 0
    flat = geo / (sum(nz) / len(nz)) if nz else 0
    bands = [sum(p for f, p in zip(freqs, power) if lo <= f < hi) / tot for lo, hi in BANDS]
    return centroid, flat, bands


def f0_estimate(xs):
    """Autocorrelation pitch over the loudest 2048 samples, 60 to 600 Hz."""
    n = min(2048, len(xs))
    best_i, best_e = 0, -1
    for s in range(0, max(1, len(xs) - n), 256):
        e = sum(x * x for x in xs[s:s + n])
        if e > best_e:
            best_i, best_e = s, e
    seg = xs[best_i:best_i + n]
    lo, hi = int(SR / 600), int(SR / 60)
    best_lag, best_r = 0, 0.0
    r0 = sum(x * x for x in seg) or 1e-12
    for lag in range(lo, min(hi, len(seg) - 1)):
        r = sum(seg[k] * seg[k + lag] for k in range(0, len(seg) - lag, 2)) * 2 / r0
        if r > best_r:
            best_lag, best_r = lag, r
    return (SR / best_lag if best_lag else 0.0), best_r


def pitch_spread(xs, f0):
    """How far the pitch moves inside a clip: the range of per-frame pitches, in % of f0.

    Frames are 1024 samples, every 256, searched within 30% of the clip's pitch.
    Quiet frames (under a fifth of the loudest) are skipped.
    """
    if f0 <= 0:
        return 0.0
    N, hop = 1024, 256
    lo, hi = int(SR / (f0 * 1.45)), int(SR / (f0 * 0.7))
    frames = [xs[s:s + N] for s in range(0, len(xs) - N, hop)]
    if not frames:
        return 0.0
    loud = max(sum(x * x for x in fr) for fr in frames)
    found = []
    for fr in frames:
        e = sum(x * x for x in fr)
        if e < loud * 0.2:
            continue
        best_lag, best_r = 0, 0.0
        for lag in range(lo, min(hi, N - 1)):
            r = sum(fr[k] * fr[k + lag] for k in range(0, N - lag, 2))
            if r > best_r:
                best_lag, best_r = lag, r
        if best_lag:
            found.append(SR / best_lag)
    if len(found) < 2:
        return 0.0
    return 100 * (max(found) - min(found)) / f0


def clip_stats(xs):
    c, fl, bands = spectrum_stats(xs)
    f0, conf = f0_estimate(xs)
    return {
        "len": len(xs) / SR,
        "peak": db(max(abs(x) for x in xs)),
        "rms": db(rms(xs)),
        "loud": db(loud_weighted(xs)),
        "centroid": c,
        "flat": fl,
        "bands": bands,
        "f0": f0,
        "voiced": conf,
        "wobble": pitch_spread(xs, f0),
    }


def print_set(name, stats):
    print(f"\n== {name}: {len(stats)} clips")
    print("   clip   len s  peak dB  rms dB  loud dB  centroid Hz  flatness   f0 Hz  pitch moves %")
    for i, s in enumerate(stats):
        print(f"   {i:02d}    {s['len']:.3f}  {s['peak']:7.1f}  {s['rms']:6.1f}  {s['loud']:7.1f}"
              f"  {s['centroid']:11.0f}  {s['flat']:8.3f}  {s['f0']:6.0f}  {s['wobble']:12.0f}")
    k = len(stats)
    avg = {key: sum(s[key] for s in stats) / k for key in ("len", "peak", "rms", "loud", "centroid", "flat", "f0", "wobble")}
    bands = [sum(s["bands"][b] for s in stats) / k for b in range(len(BANDS))]
    lens = [s["len"] for s in stats]
    print(f"   mean   {avg['len']:.3f}  {avg['peak']:7.1f}  {avg['rms']:6.1f}  {avg['loud']:7.1f}"
          f"  {avg['centroid']:11.0f}  {avg['flat']:8.3f}  {avg['f0']:6.0f}  {avg['wobble']:12.0f}"
          f"   (len {min(lens):.3f} to {max(lens):.3f} s)")
    print("   energy by band: " + "  ".join(f"{lo}-{hi} Hz {100 * b:4.1f}%" for (lo, hi), b in zip(BANDS, bands)))
    return avg, bands


# ---------------------------------------------------------------- files

def write_wav(path, xs):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = b"".join(struct.pack("<h", max(-32767, min(32767, int(round(x * 32767))))) for x in xs)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data)


def read_wav(path):
    with wave.open(path, "rb") as w:
        ch, sw, sr, n = w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
        raw = w.readframes(n)
    if sw != 2:
        sys.exit(f"{path}: need 16-bit samples (got {8 * sw}-bit); convert it with afconvert -d LEI16")
    vals = struct.unpack("<" + "h" * (len(raw) // 2), raw)
    xs = [sum(vals[i:i + ch]) / (ch * 32768.0) for i in range(0, len(vals), ch)]
    if sr != SR:  # linear resample
        ratio = sr / SR
        m = int(len(xs) / ratio)
        xs = [xs[min(len(xs) - 1, int(k * ratio))] for k in range(m)]
    return xs


def make_robots(write):
    all_bytes = hashlib.sha256()
    summary = []
    for name, off, maker, count in PROVIDERS:
        rng = random.Random(SEED * 10 + off)
        clips = [level(maker(rng, i)) for i in range(count)]
        stats = [clip_stats(c) for c in clips]
        avg, bands = print_set(name, stats)
        summary.append((name, avg, bands))
        for i, c in enumerate(clips):
            path = os.path.join(OUT, name, f"S_Voice{name}_{i:02d}.wav")
            if write:
                write_wav(path, c)
                with open(path, "rb") as f:
                    all_bytes.update(f.read())
    print("\n== The four sets side by side (means)")
    print("   set         f0 Hz  moves %  centroid Hz  flatness  <300 Hz  300-1k  1k-3k  3k-8k  >8k")
    for name, avg, b in summary:
        print(f"   {name:10s}  {avg['f0']:5.0f}  {avg['wobble']:7.0f}  {avg['centroid']:11.0f}  {avg['flat']:8.3f}"
              f"  {100 * b[0]:6.1f}%  {100 * b[1]:5.1f}%  {100 * b[2]:4.1f}%  {100 * b[3]:4.1f}%  {100 * b[4]:4.1f}%")
    if write:
        print(f"\nwrote {sum(p[3] for p in PROVIDERS)} files under {os.path.relpath(OUT, ROOT)}/")
        print(f"hash of all files: {all_bytes.hexdigest()}")


def cut_me(take, max_len, first):
    xs = read_wav(take)
    # remove DC, then find syllables by a 10 ms RMS envelope against a threshold
    mean = sum(xs) / len(xs)
    xs = [x - mean for x in xs]
    hop = int(0.010 * SR)
    env = [rms(xs[k:k + hop]) for k in range(0, len(xs), hop)]
    floor_ = sorted(env)[len(env) // 10]
    loudest = max(env)
    thr = max(floor_ * 3, loudest * 0.04)
    regions, start, quiet = [], None, 0
    for k, e in enumerate(env):
        if e >= thr:
            if start is None:
                start = k
            quiet = 0
        elif start is not None:
            quiet += 1
            if quiet >= 15:  # 150 ms of quiet ends a syllable
                regions.append((start, k - quiet + 1))
                start, quiet = None, 0
    if start is not None:
        regions.append((start, len(env)))
    # drop clicks and breaths: pieces under 60 ms, or 20 dB below the loudest syllable
    regions = [(a, b) for a, b in regions if (b - a) >= 6 and max(env[a:b]) >= loudest * 0.1]
    found = len(regions)
    if first:
        regions = regions[:first]
    print(f"{take}: {len(xs) / SR:.2f} s, threshold {db(thr):.1f} dBFS, found {found} syllables, keeping {len(regions)}")
    for i, (a, b) in enumerate(regions):
        print(f"   {i:02d}  {a * hop / SR:6.2f} to {b * hop / SR:6.2f} s")
    out_dir = os.path.join(OUT, "Me")
    os.makedirs(out_dir, exist_ok=True)
    for f in os.listdir(out_dir):
        if f.startswith("S_VoiceMe_") and f.endswith(".wav"):
            os.remove(os.path.join(out_dir, f))
    stats = []
    for i, (a, b) in enumerate(regions):
        s0 = max(0, a * hop - int(0.015 * SR))     # keep a breath of lead-in
        s1 = min(len(xs), b * hop + int(0.060 * SR))  # and the natural tail
        clip = xs[s0:s1]
        if len(clip) > int(max_len * SR):
            clip = clip[:int(max_len * SR)]
        n = len(clip)
        fade_in, fade_out = int(0.006 * SR), min(int(0.040 * SR), n // 3)
        clip = [x * min(1.0, k / fade_in) * min(1.0, (n - 1 - k) / fade_out) for k, x in enumerate(clip)]
        clip = level(Biquad("hp", 80, 0.7).run(clip))
        write_wav(os.path.join(out_dir, f"S_VoiceMe_{i:02d}.wav"), clip)
        stats.append(clip_stats(clip))
    print_set("Me", stats)
    print(f"\nwrote {len(regions)} files under {os.path.relpath(out_dir, ROOT)}/")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--stats", action="store_true", help="print the numbers, write nothing")
    ap.add_argument("--me", metavar="TAKE.wav", help="cut my one-take recording into the Me set")
    ap.add_argument("--max-len", type=float, default=0.35, help="longest clip in the Me set, seconds")
    ap.add_argument("--first", type=int, default=0, help="keep only the first N syllables of the take")
    ap.add_argument("--measure", nargs="+", metavar="FILE.wav", help="print the numbers of these wavs")
    args = ap.parse_args()
    if args.measure:
        print_set("measured", [clip_stats(read_wav(p)) for p in args.measure])
        for p in args.measure:
            print("  ", p)
    elif args.me:
        cut_me(args.me, args.max_len, args.first)
    else:
        make_robots(write=not args.stats)


if __name__ == "__main__":
    main()
