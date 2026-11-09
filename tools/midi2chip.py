"""Convert a MIDI file you own into a chiptune preview WAV.

Each MIDI part is mapped to a chip instrument by its General MIDI program
(or its track name), drums are mapped to noise drums, and everything is
rendered with the same engine as chiptune_preview.py (22050 Hz mono).

Usage:
    python tools/midi2chip.py song.mid out.wav [--lead "Melody"] [--max-chord 3]

Requires: pip install mido numpy

Do not commit converted copyrighted songs. Keep the MIDI and the output
outside the repository, or in firmware/chiptunes/private/ (git-ignored).
"""

import argparse
import os
import sys

import mido
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from chiptune_preview import INST, SR, RNG, render_drum, render_note, write_wav  # noqa: E402

# extra instruments for MIDI parts
INST.update({
    "keys": dict(kind="pulse", duty=0.125, a=0.002, d=0.25, s=0.3, r=0.08, gain=0.045, legato=1.0),
    "pad": dict(kind="pulse", duty=0.5, a=0.06, d=0.5, s=0.7, r=0.15, gain=0.035, legato=1.0),
    "brass": dict(kind="pulse", duty=0.25, a=0.02, d=0.2, s=0.6, r=0.08, gain=0.05, legato=1.0),
    "midi_lead": dict(kind="pulse", duty=0.33, a=0.006, d=0.3, s=0.6, r=0.08, vib=0.007, gain=0.30, legato=1.0),
    "midi_bass": dict(kind="tri", a=0.002, d=0.2, s=0.85, r=0.03, gain=0.42, legato=1.0),
    "midi_bell": dict(kind="bell", a=0.001, d=0.5, s=0.0, r=0.3, gain=0.12, legato=1.0),
})

# General MIDI drum notes -> chip drums
DRUM_MAP = {35: "K", 36: "K", 37: "S", 38: "S", 39: "S", 40: "S",
            42: "H", 44: "H", 46: "H", 54: "J", 56: "J", 69: "J", 70: "J",
            49: "C", 51: "C", 52: "C", 55: "C", 57: "C", 59: "C"}


def crash():
    n = int(0.6 * SR)
    t = np.arange(n) / SR
    return np.diff(RNG.uniform(-1, 1, n + 1)) * np.exp(-t / 0.25) * 0.06


def role_for(program, name, lead_name):
    if lead_name and lead_name.lower() in name.lower():
        return "midi_lead"
    if 32 <= program <= 39:
        return "midi_bass"
    if 8 <= program <= 15:
        return "midi_bell"
    if program <= 7:
        return "keys"
    if 56 <= program <= 63:
        return "brass"
    if 40 <= program <= 55 or 88 <= program <= 95:
        return "pad"
    if 72 <= program <= 87:
        return "midi_lead" if not lead_name else "keys"
    return None  # sound effects etc. are skipped


def collect(path):
    """Return {channel: {'name', 'program', 'notes': [(start, dur, pitch, vel)]}}."""
    mid = mido.MidiFile(path)
    names = {}
    for tr in mid.tracks:
        for msg in tr:
            if hasattr(msg, "channel"):
                names.setdefault(msg.channel, tr.name)
                break
    parts, active, now = {}, {}, 0.0
    for msg in mid:  # merged, time in seconds, tempo changes applied
        now += msg.time
        if not hasattr(msg, "channel"):
            continue
        p = parts.setdefault(msg.channel, dict(name=names.get(msg.channel, ""), program=0, notes=[]))
        if msg.type == "program_change":
            p["program"] = msg.program
        elif msg.type == "note_on" and msg.velocity > 0:
            active[(msg.channel, msg.note)] = (now, msg.velocity)
        elif msg.type in ("note_off", "note_on"):
            start = active.pop((msg.channel, msg.note), None)
            if start:
                p["notes"].append((start[0], max(0.03, now - start[0]), msg.note, start[1]))
    return parts, now


def thin_chords(notes, max_chord):
    """Keep at most max_chord notes per onset (the highest), like a chip would."""
    notes = sorted(notes)
    out, group = [], []
    for n in notes + [(1e9, 0, 0, 0)]:
        if group and n[0] - group[0][0] > 0.015:
            out += sorted(group, key=lambda x: -x[2])[:max_chord]
            group = []
        group.append(n)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("midi")
    ap.add_argument("out")
    ap.add_argument("--lead", default="melody", help="track name of the melody part")
    ap.add_argument("--max-chord", type=int, default=3)
    args = ap.parse_args()

    parts, length = collect(args.midi)
    buf = np.zeros(int((length + 3) * SR))

    def put(w, t):
        i = int(t * SR)
        j = min(len(buf), i + len(w))
        buf[i:j] += w[: j - i]

    for ch, p in sorted(parts.items()):
        if not p["notes"]:
            continue
        if ch == 9:
            role = "drums"
            for start, _, pitch, vel in p["notes"]:
                d = DRUM_MAP.get(pitch)
                if d:
                    put((crash() if d == "C" else render_drum(d)) * (vel / 100), start)
        else:
            role = role_for(p["program"], p["name"], args.lead)
            if role:
                notes = p["notes"] if role in ("midi_lead", "midi_bass") else thin_chords(p["notes"], args.max_chord)
                for start, dur, pitch, vel in notes:
                    put(render_note([pitch], dur, INST[role]) * (0.5 + vel / 254), start)
        print(f"  ch {ch:2d}  {p['name'] or '-':12s} prog {p['program']:3d}  {len(p['notes']):5d} notes -> {role or 'skipped'}")

    secs = write_wav(args.out, buf)
    print(f"{args.out}  ({secs:.0f} s)")


if __name__ == "__main__":
    main()
