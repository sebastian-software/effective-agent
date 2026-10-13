#!/usr/bin/env python3
"""Place voiceover takes from a cue sheet on a timeline; write the voice track and SRT captions.

usage: cue_sheet.py <takes-dir> <cues.json> <out-dir>

The cue sheet is JSON:

    {
      "total": 55.81,
      "cues": [
        {"take": "l01_s5", "at": 0.20, "text": "First line."},
        {"take": "l09_s3", "at": 44.68, "trim": [0, 0.90], "text": "Dalo."},
        {"take": "l09_s3", "at": 45.50, "trim": [0.90, null], "text": "Just ask."}
      ]
    }

`take` names `<takes-dir>/<take>.wav`; `at` is the start in seconds; `trim`
cuts the take (seconds, `null` = to the end); `on` (default 0.22) is the
speech onset inside the take, used for the caption start. Every take is
levelled to the same speech loudness and faded at its edges, so trims never
click. Writes `<out-dir>/vo.wav` (48 kHz mono) and `<out-dir>/captions.srt`.
Requires numpy, scipy, and soundfile.
"""
from __future__ import annotations

import json
import os
import sys

SAMPLE_RATE = 48000
SPEECH_RMS_DBFS = -19.0
FADE_SECONDS = 0.012
DEFAULT_ONSET = 0.22
CAPTION_TAIL = 0.15


def srt_timestamp(seconds: float) -> str:
    """Format seconds as an SRT timestamp, e.g. 75.5 -> 00:01:15,500."""
    millis = int(round(max(0.0, seconds) * 1000))
    hours, rest = divmod(millis, 3_600_000)
    minutes, rest = divmod(rest, 60_000)
    secs, millis = divmod(rest, 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"


def caption_span(cue: dict, duration: float) -> tuple[float, float]:
    """Caption start and end for a cue whose placed take lasts `duration` seconds."""
    start = cue["at"] + cue.get("on", DEFAULT_ONSET)
    end = cue["at"] + duration - CAPTION_TAIL
    return start, max(start + 0.5, end)


def srt(captions: list[tuple[float, float, str]]) -> str:
    return "".join(f"{i}\n{srt_timestamp(s)} --> {srt_timestamp(e)}\n{t}\n\n" for i, (s, e, t) in enumerate(captions, 1))


def render(takes_dir: str, sheet: dict, out_dir: str) -> None:
    import numpy as np
    import soundfile as sf
    from scipy.signal import resample_poly

    total = float(sheet["total"])
    track = np.zeros(int(total * SAMPLE_RATE) + SAMPLE_RATE, dtype=np.float32)
    captions = []
    for cue in sheet["cues"]:
        audio, rate = sf.read(os.path.join(takes_dir, cue["take"] + ".wav"), dtype="float32")
        if audio.ndim > 1:
            audio = audio.mean(axis=1)
        start, stop = cue.get("trim", [0, None])
        audio = audio[int(start * rate) : (int(stop * rate) if stop else None)]
        audio = resample_poly(audio, SAMPLE_RATE, rate).astype(np.float32)
        voiced = audio[np.abs(audio) > 0.01]
        if voiced.size:
            audio *= 10 ** (SPEECH_RMS_DBFS / 20) / float(np.sqrt(np.mean(voiced**2)))
        fade = int(FADE_SECONDS * SAMPLE_RATE)
        audio[:fade] *= np.linspace(0, 1, fade)
        audio[-fade:] *= np.linspace(1, 0, fade)
        at = int(cue["at"] * SAMPLE_RATE)
        track[at : at + len(audio)] += audio * cue.get("gain", 1.0)
        if cue.get("text"):
            captions.append((*caption_span(cue, len(audio) / SAMPLE_RATE), cue["text"]))
    os.makedirs(out_dir, exist_ok=True)
    sf.write(os.path.join(out_dir, "vo.wav"), track[: int(total * SAMPLE_RATE)], SAMPLE_RATE)
    with open(os.path.join(out_dir, "captions.srt"), "w", encoding="utf-8") as handle:
        handle.write(srt(captions))


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print(__doc__.strip().splitlines()[2], file=sys.stderr)
        return 2
    with open(argv[2], encoding="utf-8") as handle:
        render(argv[1], json.load(handle), argv[3])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
