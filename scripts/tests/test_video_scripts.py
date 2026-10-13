from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "skills/effective-video/scripts"


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


cue_sheet = load("cue_sheet")
pronunciation = load("pronunciation_check")


class CueSheetTests(unittest.TestCase):
    def test_srt_timestamp_rolls_over_units(self) -> None:
        self.assertEqual(cue_sheet.srt_timestamp(0.0), "00:00:00,000")
        self.assertEqual(cue_sheet.srt_timestamp(75.5), "00:01:15,500")
        self.assertEqual(cue_sheet.srt_timestamp(3725.0004), "01:02:05,000")

    def test_srt_timestamp_never_writes_a_thousand_milliseconds(self) -> None:
        self.assertEqual(cue_sheet.srt_timestamp(1.9996), "00:00:02,000")

    def test_caption_follows_the_take_length(self) -> None:
        start, end = cue_sheet.caption_span({"at": 15.25}, 4.68)
        self.assertAlmostEqual(start, 15.47)
        self.assertAlmostEqual(end, 19.78)

    def test_caption_honours_onset_and_minimum_length(self) -> None:
        start, end = cue_sheet.caption_span({"at": 10.0, "on": 0.5}, 0.4)
        self.assertAlmostEqual(start, 10.5)
        self.assertAlmostEqual(end, 11.0)

    def test_srt_numbers_blocks_and_separates_them(self) -> None:
        text = cue_sheet.srt([(0.42, 2.0, "One."), (3.0, 4.5, "Two.")])
        self.assertEqual(
            text,
            "1\n00:00:00,420 --> 00:00:02,000\nOne.\n\n2\n00:00:03,000 --> 00:00:04,500\nTwo.\n\n",
        )

    def test_vtt_uses_dots_and_a_header(self) -> None:
        self.assertEqual(
            cue_sheet.vtt([(0.42, 2.0, "One.")]),
            "WEBVTT\n\n00:00:00.420 --> 00:00:02.000\nOne.\n\n",
        )


class PronunciationVerdictTests(unittest.TestCase):
    def test_sustained_high_f2_is_a_front_vowel(self) -> None:
        track = [None, 650, 1400, None, 2330, 2490, 2670, 2500, 2180, 1360, 1100]
        self.assertEqual(pronunciation.verdict(track, 2100), "front")

    def test_release_spike_alone_is_not_a_front_vowel(self) -> None:
        # The consonant release can flash a high F2 before a back vowel.
        track = [None, 2040, 2060, 1940, 1420, 1270, 1200, 1060, 1210]
        self.assertEqual(pronunciation.verdict(track, 2100), "back")

    def test_unvoiced_frames_break_a_run(self) -> None:
        track = [2300, 2400, None, 2500, None, 2600]
        self.assertEqual(pronunciation.verdict(track, 2100), "back")


if __name__ == "__main__":
    unittest.main()
