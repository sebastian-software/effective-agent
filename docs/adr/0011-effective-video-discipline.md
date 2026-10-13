# ADR 0011: Produce Rendered Films in a Video Discipline

- Status: Proposed
- Date: 2026-10-13
- Extends: [ADR 0004](0004-effective-disciplines.md), following the precedent of
  [ADR 0010](0010-effective-image-workflows.md)

## Context

A 56-second marketing film for Dalo was produced entirely from code:

- the picture as Remotion scenes, with a few copied snapcn components
- a synthetic English voiceover from open TTS models
- an original piano score written as MIDI and rendered with licensed soundfonts
- a ducked mix at broadcast loudness
- delivery through a streaming host, with captions and a poster

The requested outcome is a finished, publishable film.

None of the seven disciplines owns that outcome:

- `effective-marketing` owns the message, hooks, and video content strategy,
  but not rendering a film.
- `effective-web` owns motion inside web pages, not offline compositions,
  voice synthesis, or audio mixing.
- `effective-image` owns still photographs.

Splitting the work between marketing and web would scatter one pipeline across
two skills. The steps share a single timing grid and a single set of
licensing and pronunciation pitfalls.

The production surfaced failure modes that a capable agent still repeats
without guidance:

- choosing TTS weights with non-commercial licences
- trusting a transcript to confirm a brand name's pronunciation
- shipping demo copy left in copied components
- normalising music loudness in a way that flattens its arc
- committing video binaries to Git
- embedding a third-party player that contradicts the site's privacy promises

## Decision

Add the independently installable discipline `effective-video` for films
rendered from code. Organize it by production stage, with five routes:

1. **Film Plan:** brief, beat sheet on a musical bar grid, and review
   checkpoints.
2. **Remotion Picture:** scenes, camera, own components versus copied snapcn
   components, the brand theme, and frame checks.
3. **Voiceover:** licence-checked open TTS, no cloning of real voices, seeded
   takes, and acoustic pronunciation checks.
4. **Score and Mix:** an original score from MIDI with licensed soundfonts,
   ducking, and loudness.
5. **Delivery:** streaming playback, reach channels, archived originals,
   captions, and the poster.

Ship small deterministic helpers where a step needs exact behaviour: assembling
cue sheets with captions, the ducked loudness mix, and a formant-based
pronunciation check.

Ownership at the edges:

- **`effective-marketing`** keeps positioning, the script's message, and
  channel strategy. The video skill owns timing, beat structure, and production
  wording such as phonetic spelling for synthesis.
- **`effective-web`** keeps the embed code and player UI on a site.
- **Publication** to accounts, storage, or channels needs its own
  authorization. Using the skill does not grant it.

## Alternatives

- **A route in `effective-marketing` plus a route in `effective-web`.**
  Rejected because the pipeline is one artifact with one timing grid; the
  voice, score, and picture decisions depend on each other.
- **A narrow skill named after Remotion.** Rejected for the reason ADR 0010
  rejected naming the image skill after one workflow: other renderers and
  formats, such as vertical social cuts, belong to the same outcome.

## Consequences

The public inventory grows to eight skills. README installation links, website
cards, detail pages, counts, structured data, the routing matrix, and the site
layout test include the video discipline.

The routes name concrete tools that were current in October 2026: Remotion,
snapcn, Chatterbox, Kokoro, fluidsynth, Bunny Stream. Each is presented as a
verified default with its selection criteria, so a successor can be swapped in
when it meets the same licence and quality bar.

Review scenarios are unrun fixtures, not evidence of an independent behavioural
evaluation.

## Review Triggers

- Revisit the tool defaults when a named tool changes its licence, is
  superseded, or stops meeting the quality bar.
- Add a route when real requests establish another reusable workflow, such as
  screen-recording demos or vertical social cuts with burned-in captions.
- Revisit the marketing boundary if script ownership causes repeated handoff
  confusion.
