[← Sebastian Software Skills](../../README.md)

# Effective Image

**Focused workflows for image assets.**

Routing starts from the source:

- **Photo Editing** changes existing photos (cleanup, backgrounds, objects,
  real product insertion) with short single-change edits, keeping the
  original's people, light, and grain as the measure of truth.
- **Business Portrait Retouch** is the portrait preset: tailored-looking
  clothing, reduced eyeglass glare, balanced facial shadows, a subtly fresher
  and fitter look, and an approved color treatment consistent across a shoot.
- **Photo Generation** directs new photoreal scenes and brand visuals with a
  fixed series brief, concrete photographic language, and deliberate realism
  cues instead of plastic skin and sterile light.

**[Explore Effective Image →](https://skills.sebastian-software.com/skills/effective-image/)**

Example requests:

- Show before/after proposals for this business shoot with smoother clothing
  and natural skin texture.
- Apply the approved warm look across the remaining portraits. Reduce glare
  and tired-looking shadows without changing the smiles.
- Remove the cables from this office photo without changing the people.
- Create a warm travertine bathroom scene for our serum bottle that looks like
  an actual photograph, not an AI render.

All routes use Imagegen; a batch script runs the retouch through the
Images API at higher resolution. The skill does not cover illustration, photo
publication, storage configuration, or commercial copy. Output resolution
depends on the available tool and is reported with the delivery.

## Install

~~~sh
npx skills add sebastian-software/skills.sebastian-software.com --skill effective-image
~~~

For managed installations, see the [DALO setup guide](../../docs/dalo.md):

~~~sh
dalo init
dalo target link codex
dalo source add-catalog sebastian https://github.com/sebastian-software/skills.sebastian-software.com.git
dalo source select sebastian effective-image
dalo approve skill sebastian:effective-image
dalo sync
~~~

## Agent Instructions

[SKILL.md](SKILL.md) routes to [Photo Editing](references/route-photo-editing.md),
its portrait preset [Business Portrait Retouch](references/route-business-retouch.md)
with the reusable prompt and batch script, and
[Photo Generation](references/route-photo-generation.md). All share the
[Realism Review](references/realism-review.md).

Maintained by [Sebastian Software](https://oss.sebastian-software.com/).
We also help teams [design, modernize, and ship software](https://sebastian-consulting.com/en).

## License

MIT OR Apache-2.0 — see the collection [LICENSE-MIT](../../LICENSE-MIT) and [LICENSE-APACHE](../../LICENSE-APACHE).
