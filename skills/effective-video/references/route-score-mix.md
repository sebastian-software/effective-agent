# Score and Mix

Use for writing an original score, placing it under the voice, and fixing the
balance or loudness of a film's soundtrack.

## Original, Not Imitated

"In the style of" a composer means an original piece with the same traits,
not the composer's melodies, chord progressions quoted bar for bar, or
recognisable motifs. Say so when a requester names a famous piece.

One illustrative arc for a minimalist modern-classical promo score; derive
instrumentation, key, and arc from the brief:

- solo piano;
- arpeggiated eighths in a minor key that brighten to the relative major at
  the product reveal;
- a slow string pad entering for the team or scale beat;
- sixteenths and an octave-doubled motif for the build;
- one sustained chord for the claim, and a rising arpeggio that rings out
  under the end card.

Drive tension with density and dynamics rather than tempo, so cuts stay on the
grid.

## Compose as Data

Write the score as MIDI from code (for example `mido`). The bar plan of the
[Film Plan](route-film-plan.md) then becomes the piece's structure, and changing
a scene's length means editing one list.

- Give each bar a chord and a section, and derive the layers from the section:
  left-hand broken chords, right-hand arpeggios, melody, strings.
- Key melodic fragments to the chord they sound over. A motif indexed by bar
  number lands on the wrong harmony after a section changes length.
- Split chords per half bar in every layer, strings included, or a pad sustains
  against a changing piano harmony.
- Humanise timing and velocity by a few ticks or steps with a fixed random
  seed, so renders stay reproducible.
- Pedal per chord. Fade the strings in with expression (CC 11) ramps instead
  of a hard entry.

## Render

Render with fluidsynth from soundfonts whose licence allows the use, and record
the credit:

- **Salamander Grand Piano V3 (CC BY 3.0):** attribution is required wherever
  the film is published.
- **Upright Piano KW (CC0):** a softer, more intimate piano.
- **MuseScore General (MIT):** usable strings and cello, as `.sf3`.

Disable fluidsynth's own reverb and chorus. Add a hall with a convolution
reverb: a synthetic impulse response of decaying, low-passed noise with a short
pre-delay is enough.

Normalise the music by a **static** gain to its peak, with at most gentle
compression. A single-pass `loudnorm` on the music flattens the arc you
composed. Measure section loudness: the build should be clearly louder than the
hook, by about 10 dB of mean level rather than 20.

## Mix Under the Voice

[`scripts/mix.sh`](../scripts/mix.sh) does the final mix:

- It gives the voice a high-pass, light presence EQ, moderate compression, and
  a trace of the same hall.
- It ducks the music under the voice with sidechain compression keyed by the
  voice: a low threshold, a ratio around 8, about 40 ms attack and 500 ms
  release.
- It normalises the whole mix with **two-pass** `loudnorm` in linear mode to
  -16 LUFS integrated with a -1.5 dBTP ceiling, a sensible web and streaming
  target.

Level every take to the same speech loudness before mixing (the cue sheet does
this). Check that speech sits about 10–12 dB above the ducked music during
lines.

You cannot hear the mix. Report measured values, such as integrated loudness,
true peak, and section levels. Ask the requester to judge balance and tone by
ear at the animatic checkpoint.
