# Voiceover

Use for creating, replacing, or fixing a synthetic voiceover, including the
pronunciation of product names.

## Choose a Model by Licence First

Check the licence of the **weights**, not only the code, before quality.
Commercial marketing use excludes non-commercial weights even when the code is
MIT.

- **Chatterbox (Resemble AI, MIT).** Expressive and steerable with
  `exaggeration` and `cfg_weight`. It conditions on a short reference clip. It
  runs on Apple Silicon with the MPS fallback. Its output carries an
  imperceptible Perth watermark; keep it.
- **Kokoro-82M (Apache-2.0).** Small, fast, and clean, but less expressive.
  It is useful on its own, and as a synthetic reference voice for Chatterbox.
- **Exclude** weights under non-commercial terms, such as XTTS-v2 (CPML) and
  the F5-TTS checkpoints (CC BY-NC), unless the requester holds a commercial
  licence.
- **Paid APIs** are an option only with the requester's own account and key.

Recheck licences when choosing a newer model; this list reflects October 2026.

## Never Clone a Real Person

Condition a cloning model only on a synthetic reference or on a recording made
with the speaker's consent. Do not imitate a known speaker or keynote voice.
A non-native speaker's own recording carries their accent into the clone. If
the target is a native accent, use a synthetic reference instead.

## Takes

- Offer three to six short samples first: the same hook and claim, with the
  default voice and a few synthetic references across genders. Let the
  requester choose by ear.
- Generate each line separately, with several fixed seeds, at the chosen
  settings. Calm keynote delivery came from about `exaggeration` 0.45,
  `cfg_weight` 0.4 and `temperature` 0.7.
- Very short lines such as "Every version is pinned." or a single name
  produce garbage onsets or dropped words. Merge them with a neighbouring
  sentence and split the result at a pause, or regenerate with more seeds.
- Screen every take with an ASR model (Whisper) for wrong or missing words,
  repeated phrases, and trailing noise. Use a larger model when brand or
  product names are involved: the small model hears "Codex" as "codecs".
- Pick takes by fit as well as correctness: pause positions that match the
  beat sheet, and a total length that fits its bars.
- Archive the chosen takes. Generation is not reproducible bit for bit across
  machines, so a later rebuild needs the files, not only the seeds.

## Pronunciation of Names

Agree on the pronunciation before generating takes, and write it down. To
enforce it, spell the name phonetically in the text sent to the model (for
example "Daylo"). Keep the correct spelling in captions and on screen.

**ASR transcripts cannot verify pronunciation.** Whisper writes the same word
as "Dalo", "Daylo" or "Dallow" regardless of the vowel spoken. Check the vowel
acoustically instead, with
[`scripts/pronunciation_check.py`](../scripts/pronunciation_check.py):

- It tracks the second formant (F2) across the word.
- /eɪ/ ("day") rises to roughly 2,300–2,800 Hz for about 100 ms after the
  consonant release.
- /ɑ/ ("dah") stays near 1,000–1,400 Hz.
- Calibrate against one take the requester accepted and one they rejected.
- Start the window at the name's first consonant, not on the preceding word.
  A front vowel just before it, as in "Meet", also has a high F2 and yields a
  false "front". The low F2 of a following "-lo" does not change the verdict.
- Check every occurrence of the name in the final voice track, not only in the
  replaced take.

## Placement

Place takes with a cue sheet: take, start time, optional trim, and caption
text. [`scripts/cue_sheet.py`](../scripts/cue_sheet.py) does this:

- it levels each take to the same speech loudness;
- it adds short fades at trims;
- it writes the voice track plus SRT and WebVTT captions, using the take's
  real duration.

When replacing a take, regenerate the captions as well, because cue end times
move with the take length.

## Local Setup Pitfalls

- Kokoro's espeak-ng backend truncates long data paths and exits without a
  traceback ("Error processing file …/phontab"). Copy `espeak-ng-data` to a
  short path and point the phonemizer at it.
- Chatterbox's watermarker needs `pkg_resources`. Pin `setuptools<81` in the
  environment (needed as of October 2026).
- Keep the models in an isolated, ignored environment (uv venv). Never commit
  weights or takes to the product repository.
