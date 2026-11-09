"""Chiptune preview renderer for the PC.

Renders demo chiptunes to WAV files so they can be auditioned before the
Feather arrives. Uses the same ingredients the Feather's synthio can do:
pulse/triangle/noise waveforms, envelopes, vibrato, arpeggios, a few voices.
Output is 22050 Hz mono, like the Feather.

Usage:  python tools/chiptune_preview.py [output_dir]

Only public-domain carols and original tunes belong in this file.
"""

import os
import sys
import wave
from fractions import Fraction

import numpy as np

SR = 22050
RNG = np.random.default_rng(1225)

# ---------------------------------------------------------------- notes ----
_IDX = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def midi(name):
    """'C#5' -> MIDI number."""
    i, k = _IDX[name[0]], 1
    while k < len(name) and name[k] in "#b":
        i += 1 if name[k] == "#" else -1
        k += 1
    return 12 * (int(name[k:]) + 1) + i


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


DRUMS = {"K", "S", "H", "J"}  # kick, snare, hi-hat, sleigh bells


def parse(seq, beats_per_bar=4):
    """'C5 D5:1/2 E5+G5:2 | R:4' -> [(notes|drum|None, beats)], bar-checked."""
    out = []
    for bar in seq.split("|"):
        toks = bar.split()
        total = Fraction(0)
        for tok in toks:
            n, _, d = tok.partition(":")
            d = Fraction(d) if d else Fraction(1)
            if n == "R":
                item = None
            elif n in DRUMS:
                item = n
            else:
                item = [midi(x) for x in n.split("+")]
            out.append((item, d))
            total += d
        if toks and total != beats_per_bar:
            raise ValueError(f"bar has {total} beats, expected {beats_per_bar}: {bar!r}")
    return out


_QUAL = {"": [0, 4, 7], "m": [0, 3, 7], "7": [0, 4, 7, 10], "m7": [0, 3, 7, 10],
         "maj7": [0, 4, 7, 11], "6": [0, 4, 7, 9], "dim": [0, 3, 6]}


def chord(name, octave):
    k = 2 if len(name) > 1 and name[1] in "#b" else 1
    root = midi(name[:k] + str(octave))
    return [root + i for i in _QUAL[name[k:]]]


def parse_chords(s, beats_per_bar=4):
    out = []
    for bar in s.split("|"):
        names = bar.split()
        for c in names:
            out.append((c, Fraction(beats_per_bar, len(names))))
    return out


def bars(s):
    return len(s.split("|"))


# ---------------------------------------------------------- instruments ----
INST = {
    "lead_nes": dict(kind="pulse", duty=0.25, a=0.004, d=0.25, s=0.6, r=0.08, vib=0.006, gain=0.28, legato=0.88),
    "lead_gb": dict(kind="pulse", duty=0.5, a=0.003, d=0.18, s=0.5, r=0.06, vib=0.004, gain=0.20, legato=0.9),
    "lead_warm": dict(kind="pulse", duty=0.33, a=0.006, d=0.3, s=0.55, r=0.1, vib=0.007, gain=0.26, legato=0.9),
    "arp": dict(kind="pulse", duty=0.125, arp=0.045, a=0.004, d=0.4, s=0.45, r=0.05, gain=0.08, legato=0.98),
    "bass": dict(kind="tri", a=0.002, d=0.2, s=0.8, r=0.03, gain=0.40, legato=0.85),
    "stab": dict(kind="pulse", duty=0.25, a=0.002, d=0.09, s=0.0, r=0.04, gain=0.06, legato=0.9),
    "bell": dict(kind="bell", a=0.001, d=0.35, s=0.0, r=0.25, gain=0.10, legato=1.0),
}


def osc(kind, freqs, n, duty=0.5, vib=0.0):
    t = np.arange(n) / SR
    f = np.asarray(freqs, dtype=float)
    if vib:
        f = f * (1 + vib * np.sin(2 * np.pi * 5.5 * t) * np.clip((t - 0.15) / 0.15, 0, 1))
    ph = np.cumsum(f) / SR % 1.0
    if kind == "pulse":
        return np.where(ph < duty, 1.0, -1.0)
    if kind == "tri":  # 4-bit stepped triangle, NES style
        return np.round((4 * np.abs(ph - 0.5) - 1) * 7.5) / 7.5
    if kind == "bell":
        return np.sin(2 * np.pi * ph) + 0.25 * np.sin(2 * np.pi * ((ph * 3.0) % 1.0))
    raise ValueError(kind)


def envelope(n, gate, a, d, s, r):
    t = np.arange(n) / SR
    e = np.where(t < a, t / a, s + (1 - s) * np.exp(-(t - a) / d))
    rel = t > gate
    e[rel] *= np.exp(-(t[rel] - gate) / r)
    return e


def render_note(notes, seconds, p):
    gate = seconds * p["legato"]
    n = int((gate + 6 * p["r"]) * SR)
    t = np.arange(n) / SR
    if p.get("arp") and len(notes) > 1:
        idx = (t / p["arp"]).astype(int) % len(notes)
        freqs = np.array([hz(m) for m in notes])[idx]
        wav = osc(p["kind"], freqs, n, p.get("duty", 0.5))
    else:
        wav = sum(osc(p["kind"], np.full(n, hz(m)), n, p.get("duty", 0.5), p.get("vib", 0)) for m in notes)
        wav = wav / max(1, len(notes) ** 0.7)
    return wav * envelope(n, gate, p["a"], p["d"], p["s"], p["r"]) * p["gain"]


def render_drum(kind):
    if kind == "K":
        n = int(0.18 * SR); t = np.arange(n) / SR
        f = 45 + 110 * np.exp(-t / 0.03)
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.08) * 0.55
    if kind == "S":
        n = int(0.16 * SR); t = np.arange(n) / SR
        noise = RNG.uniform(-1, 1, n)
        tone = np.where((t * 190) % 1 < 0.5, 1, -1)
        return (noise * np.exp(-t / 0.06) * 0.30 + tone * np.exp(-t / 0.025) * 0.10)
    if kind == "H":
        n = int(0.05 * SR); t = np.arange(n) / SR
        noise = np.diff(RNG.uniform(-1, 1, n + 1))
        return noise * np.exp(-t / 0.012) * 0.09
    if kind == "J":  # sleigh bells: bright noise with a fast shimmer
        n = int(0.12 * SR); t = np.arange(n) / SR
        noise = np.diff(RNG.uniform(-1, 1, n + 1))
        return noise * np.exp(-t / 0.04) * (0.6 + 0.4 * np.sin(2 * np.pi * 38 * t)) * 0.07
    raise ValueError(kind)


# ---------------------------------------------------------------- mixer ----
class Mix:
    def __init__(self, bpm, total_beats):
        self.spb = 60.0 / bpm
        self.buf = np.zeros(int((total_beats * self.spb + 3) * SR))

    def add(self, seq, inst, start_beat, transpose=0, out=None):
        out = self.buf if out is None else out
        beat = Fraction(start_beat)
        for item, d in seq:
            if item is not None:
                if isinstance(item, str):
                    w = render_drum(item)
                else:
                    w = render_note([m + transpose for m in item], float(d) * self.spb, INST[inst])
                i = int(float(beat) * self.spb * SR)
                j = min(len(out), i + len(w))
                out[i:j] += w[: j - i]
            beat += d


def bass_line(chords, style, octave=3):
    seq = []
    for name, d in chords:
        notes = chord(name, octave)
        root, third, fifth = notes[0], notes[1], notes[2]
        beats = int(d)
        if style == "march":
            for b in range(beats):
                seq.append(([root if b % 2 == 0 else fifth - 12], Fraction(1)))
        elif style == "roots":
            for b in range(beats):
                seq.append(([root if b % 2 == 0 else root + 12], Fraction(1)))
        elif style == "boogie":  # swung rock'n'roll walk: 1 3 5 6 b7 6 5 3
            walk = [0, third - root, 7, 9, 10, 9, 7, third - root]
            for b in range(beats):
                seq.append(([root + walk[(2 * b) % 8]], Fraction(2, 3)))
                seq.append(([root + walk[(2 * b + 1) % 8]], Fraction(1, 3)))
    return seq


def harmony(chords, style, octave=4):
    seq = []
    for name, d in chords:
        notes = chord(name, octave)
        if style == "arp":
            seq.append((notes, d))
        elif style == "stab":  # swung off-beat piano stabs
            for _ in range(int(d)):
                seq += [(None, Fraction(2, 3)), (notes, Fraction(1, 3))]
    return seq


def drum_bars(n_bars, pattern):
    return parse(" | ".join([pattern] * n_bars))


def write_wav(path, buf):
    buf = np.tanh(buf * 1.2)
    buf = buf / max(1e-9, np.max(np.abs(buf))) * 0.9
    end = len(buf)
    while end > 0 and abs(buf[end - 1]) < 1e-4:
        end -= 1
    data = (buf[: end + SR // 2] * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data.tobytes())
    return len(data) / SR


# ---------------------------------------------------------------- songs ----
def jingle_bells():
    """James Lord Pierpont, 1857 (public domain). NES-style march."""
    v1 = "G4 E5 D5 C5 | G4:3 G4:1/2 G4:1/2 | G4 E5 D5 C5 | A4:4 | A4 F5 E5 D5 | B4:4 | G5 G5 F5 D5 | E5:4"
    v2 = "G4 E5 D5 C5 | G4:4 | G4 E5 D5 C5 | A4:3 A4 | A4 F5 E5 D5 | G5 G5 G5 G5 | A5 G5 F5 D5 | C5:2 G4:2"
    c1 = "E5 E5 E5:2 | E5 E5 E5:2 | E5 G5 C5:3/2 D5:1/2 | E5:4 | F5 F5 F5:3/2 F5:1/2 | F5 E5 E5 E5:1/2 E5:1/2 | E5 D5 D5 E5 | D5:2 G5:2"
    c2 = "E5 E5 E5:2 | E5 E5 E5:2 | E5 G5 C5:3/2 D5:1/2 | E5:4 | F5 F5 F5:3/2 F5:1/2 | F5 E5 E5 E5:1/2 E5:1/2 | G5 G5 F5 D5 | C5:4"
    hv1, hv2 = "C | C | C | F | Dm | G | G | C", "C | C | C | F | F | G | G7 | C G7"
    hc1, hc2 = "C | C | C | C | F | C | D7 | G7", "C | C | C | C | F | C | G7 | C"
    sections = [  # (melody, chords, lead, transpose, bells)
        (None, "C | G7", None, 0, False),
        (v1, hv1, "lead_nes", 0, False), (v2, hv2, "lead_nes", 0, False),
        (c1, hc1, "lead_nes", 0, False), (c2, hc2, "lead_nes", 0, False),
        (c1, hc1, "lead_nes", 12, True), (c2, hc2, "lead_nes", 12, True),
        ("C5+E5+G5+C6:4", "C", "lead_nes", 0, True),
    ]
    return dict(bpm=168, sections=sections, bass="march", harm="arp",
                drums="K S K S", shimmer="J:1/2 J:1/2 J:1/2 J:1/2 J:1/2 J:1/2 J:1/2 J:1/2")


def deck_the_halls():
    """Traditional Welsh carol (public domain). Game Boy style with echo."""
    a = "G5:3/2 F5:1/2 E5 D5 | C5 D5 E5 C5 | D5:1/2 E5:1/2 F5:1/2 D5:1/2 E5:3/2 D5:1/2 | C5 B4 C5:2"
    b = "D5:3/2 E5:1/2 F5 D5 | E5:3/2 F5:1/2 G5 D5 | E5:1/2 F#5:1/2 G5 A5:1/2 B5:1/2 C6 | B5 A5 G5:2"
    a3 = "G5:3/2 F5:1/2 E5 D5 | C5 D5 E5 C5 | A5:1/2 A5:1/2 A5:1/2 A5:1/2 G5:3/2 F5:1/2 | E5 D5 C5:2"
    ha, hb, ha3 = "C | C | G7 C | G7 C", "G7 | C G | Em Am | D G", "C | C | F C | G7 C"
    sections = []
    for bells in (False, True):
        sections += [(a, ha, "lead_gb", 0, bells), (a, ha, "lead_gb", 0, bells),
                     (b, hb, "lead_gb", 0, bells), (a3, ha3, "lead_gb", 0, bells)]
    sections.append(("C5+G5+C6:4", "C", "lead_gb", 0, True))
    return dict(bpm=112, sections=sections, bass="roots", harm="arp", echo=True,
                drums="K:1 S:1 K:1/2 K:1/2 S:1", shimmer="H:1/2 H:1/2 H:1/2 H:1/2 H:1/2 H:1/2 H:1/2 H:1/2")


def snowglobe_shuffle():
    """Original tune written for this project (90s Christmas-pop feel)."""
    v1 = ("A4:2/3 B4:1/3 D5 F#5 E5:2/3 D5:1/3 | D5 B4 R:2/3 F#4:1/3 A4:2/3 B4:1/3 | "
          "D5:3/2 E5:1/2 D5:2/3 B4:1/3 G4 | A4:2 R C#5:2/3 E5:1/3")
    v2 = ("F#5 F#5:2/3 E5:1/3 F#5 A5 | C#5 A#4:2/3 C#5:1/3 E5:2 | "
          "D5 B4:2/3 D5:1/3 G5:3/2 F#5:1/2 | E5 D5 Bb4:2")
    ch = ("B4:2/3 D5:1/3 G5 G5:2/3 F#5:1/3 G5 | E5:2/3 F#5:1/3 A5 A5:2 | "
          "A5:2/3 G5:1/3 F#5 C#5 F#5 | F#5:2/3 E5:1/3 D5 B4:2 | "
          "G5 G5:2/3 F#5:1/3 E5 B4 | C#5 E5 A5 G5 | F#5:3 E5:2/3 D5:1/3 | D5:4")
    hv1, hv2 = "D | Bm | G | A", "D | F#7 | G | Gm"
    hch = "G | A | F#m | Bm | Em | A7 | D | D"
    sections = [
        (None, "D | A7", None, 0, False),
        (v1, hv1, "lead_warm", 0, False), (v2, hv2, "lead_warm", 0, False),
        (ch, hch, "lead_warm", 0, False),
        (v1, hv1, "lead_warm", 0, False), (v2, hv2, "lead_warm", 0, False),
        (ch, hch, "lead_warm", 0, True),
        ("D5+F#5+A5+D6:4", "D", "lead_warm", 0, True),
    ]
    return dict(bpm=104, sections=sections, bass="boogie", harm="stab",
                drums="K S K S", shimmer="J:2/3 J:1/3 J:2/3 J:1/3 J:2/3 J:1/3 J:2/3 J:1/3")


def render(song):
    total = sum(4 * bars(ch) for _, ch, *_ in song["sections"])
    mix = Mix(song["bpm"], total)
    lead_buf = np.zeros_like(mix.buf)
    beat = 0
    for melody, chords, lead, transpose, bells in song["sections"]:
        n = bars(chords)
        ch = parse_chords(chords)
        last = melody is not None and n == 1 and ":4" in melody and "+" in melody
        if melody:
            mel = parse(melody)
            mix.add(mel, lead, beat, transpose, out=lead_buf)
            if bells:
                mix.add(mel, "bell", beat, transpose + 12)
        if last:  # final hit: one big chord, a kick and a crash of bells
            mix.add(parse("K:4"), None, beat)
            mix.add(bass_line(ch, "march")[:1], "bass", beat)
            mix.add(parse("J:1/4 J:1/4 J:1/4 J:1/4 R:3"), None, beat)
        else:
            mix.add(bass_line(ch, song["bass"]), "bass", beat)
            mix.add(harmony(ch, song["harm"]), "arp" if song["harm"] == "arp" else "stab", beat)
            mix.add(drum_bars(n, song["drums"]), None, beat)
            mix.add(drum_bars(n, song["shimmer"]), None, beat)
        beat += 4 * n
    mix.buf += lead_buf
    if song.get("echo"):  # Game Boy style echo on the lead
        for delay, g in ((0.75, 0.35), (1.5, 0.15)):
            k = int(delay * mix.spb * SR)
            mix.buf[k:] += g * lead_buf[:-k]
    return mix.buf


SONGS = [
    ("1_jingle_bells_nes", jingle_bells),
    ("2_deck_the_halls_gameboy", deck_the_halls),
    ("3_snowglobe_shuffle_original", snowglobe_shuffle),
]

if __name__ == "__main__":
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "chiptune-demos"
    os.makedirs(out_dir, exist_ok=True)
    for name, fn in SONGS:
        path = os.path.join(out_dir, name + ".wav")
        secs = write_wav(path, render(fn()))
        print(f"{path}  ({secs:.0f} s)")
