#!/usr/bin/env python3
"""Check which vowel a voice take uses in a word, from its second formant (F2).

usage: pronunciation_check.py <take.wav> <start-seconds> <end-seconds> [--front-min HZ]

Prints the F2 track (every 25 ms; "-" = unvoiced) between start and end and a
verdict. After the consonant release, a front vowel such as /eɪ/ ("Day-lo")
holds F2 near 2,300-2,800 Hz for about 100 ms; a back vowel such as /ɑ/
("Dah-lo") stays near 1,000-1,400 Hz. ASR transcripts cannot make this
distinction. Calibrate --front-min (default 2100) on one accepted and one
rejected take, and place the window on the word itself: the vowel of a
following syllable ("-lo") also has a low F2. Requires praat-parselmouth.
"""
from __future__ import annotations

import sys

STEP = 0.025
SUSTAIN = 3  # consecutive voiced frames above the threshold (~75 ms)


def verdict(track: list[float | None], front_min: float) -> str:
    """'front' when F2 holds above front_min for SUSTAIN voiced frames, else 'back'."""
    run = 0
    for value in track:
        run = run + 1 if value is not None and value >= front_min else 0
        if run >= SUSTAIN:
            return "front"
    return "back"


def f2_track(path: str, start: float, end: float) -> list[tuple[float, float | None]]:
    import math

    import parselmouth

    sound = parselmouth.Sound(path)
    pitch = sound.to_pitch(time_step=0.01)
    formants = sound.to_formant_burg(time_step=0.01, max_number_of_formants=5, maximum_formant=5500)
    points = []
    t = start
    while t < end:
        f0 = pitch.get_value_at_time(t)
        f2 = formants.get_value_at_time(2, t)
        voiced = f0 and not math.isnan(f0) and not math.isnan(f2)
        points.append((round(t, 3), f2 if voiced else None))
        t += STEP
    return points


def main(argv: list[str]) -> int:
    args = argv[1:]
    front_min = 2100.0
    if "--front-min" in args:
        i = args.index("--front-min")
        front_min = float(args[i + 1])
        del args[i : i + 2]
    if len(args) != 3:
        print(__doc__.strip().splitlines()[2], file=sys.stderr)
        return 2
    points = f2_track(args[0], float(args[1]), float(args[2]))
    print(" ".join(f"{t:.3f}:{'-' if f2 is None else int(f2)}" for t, f2 in points))
    print(f"verdict: {verdict([f2 for _, f2 in points], front_min)} vowel (front-min {front_min:.0f} Hz)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
