[← Sebastian Software Skills](../../README.md)

# Effective Image

**Focused workflows for image assets.**

The first route, **Business Portrait Retouch**, refines existing shoots with
a restrained editorial finish:
smooth distracting shirt folds, reduce eyeglass glare, balance facial shadows,
and keep the approved color treatment consistent across a series. Preserve
recognizable faces, authentic expressions, and the setting.

**[Explore Effective Image →](https://skills.sebastian-software.com/skills/effective-image/)**

Example requests:

- Show before/after proposals for this business shoot with smoother clothing
  and natural skin texture.
- Apply the approved warm look across the remaining portraits. Reduce glare
  and tired-looking shadows without changing the smiles.

The current route uses Imagegen editing. Further image workflows can be added
as separate routes. It does not cover new scenes, photo publication, storage
configuration, or commercial copy. Output resolution
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

[SKILL.md](SKILL.md) routes to [Business Portrait Retouch](references/route-business-retouch.md),
with the reusable prompt and instructions for
references, series consistency, before/after comparison, and artifact review.

Maintained by [Sebastian Software](https://oss.sebastian-software.com/).
We also help teams [design, modernize, and ship software](https://sebastian-consulting.com/en).

## License

MIT OR Apache-2.0 — see the collection [LICENSE-MIT](../../LICENSE-MIT) and [LICENSE-APACHE](../../LICENSE-APACHE).
