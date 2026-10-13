[← Effective Agent](../../README.md)

# Effective Video

**Product films rendered from code, with a voice and an original score.**

The skill produces a finished film along one timing grid shared by picture,
voice and music:

- **Film Plan** turns a product and its message into a brief, a beat sheet
  on musical bars, and checkpoints the requester judges by ear and eye.
- **Remotion Picture** builds the scenes and camera in Remotion. It mixes the
  product's own components with copied [snapcn](https://snapcn.dev)
  components, re-skinned to the brand.
- **Voiceover** uses commercially licensed open TTS models with synthetic
  reference voices and seeded takes. Brand-name pronunciation is checked
  acoustically, not by transcript.
- **Score and Mix** composes an original piece as MIDI, renders it with
  licensed soundfonts, ducks it under the voice and normalises the mix to
  -16 LUFS.
- **Delivery** produces the master, captions and poster. It keeps video out
  of Git, plays the film from a streaming host behind a click-to-load poster,
  and archives the originals.

**[Explore Effective Video →](https://effective-agent.dev/skills/effective-video/)**

Example requests:

- Make a 60-second product film for our homepage with an English voiceover
  and calm piano music.
- Rebuild the promo with snapcn components where they fit, but keep our
  product scenes.
- The voice says "Dahlo" at 0:15. Fix that take without touching the rest.
- Publish the film on Bunny Stream with a click-to-play player and archive
  the originals.

Bundled scripts place voice takes from a cue sheet and write the captions,
mix voice and score with ducking and two-pass loudness normalisation, and
check a name's vowel from its formants.

The skill does not cover live-action shooting, editing camera footage, or
paid media. Messaging and copy belong to
[Effective Marketing](../effective-marketing/README.md). Site embedding and
player UI belong to [Effective Web](../effective-web/README.md). Uploads to
accounts or channels need their own authorization.

## Install

~~~sh
npx skills add sebastian-software/effective-agent --skill effective-video
~~~

For managed installations, see the [DALO setup guide](../../docs/dalo.md):

~~~sh
dalo init
dalo target link codex
dalo source add-catalog sebastian https://github.com/sebastian-software/effective-agent.git
dalo source select sebastian effective-video
dalo approve skill sebastian:effective-video
dalo sync
~~~

## Agent Instructions

[SKILL.md](SKILL.md) routes to:

- [Film Plan](references/route-film-plan.md)
- [Remotion Picture](references/route-remotion-picture.md)
- [Voiceover](references/route-voiceover.md)
- [Score and Mix](references/route-score-mix.md)
- [Delivery](references/route-delivery.md)

Maintained by [Sebastian Software](https://oss.sebastian-software.com/).
We also help teams [design, modernize, and ship software](https://sebastian-consulting.com/en).

## License

MIT OR Apache-2.0 — see the collection [LICENSE-MIT](../../LICENSE-MIT) and [LICENSE-APACHE](../../LICENSE-APACHE).
