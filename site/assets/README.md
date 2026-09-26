# Brand assets

Use the **Sebastian Software** variant of the company brand system.
The checked-in vectors are unchanged assets from the `sebastian-software/`
directory in `sebastian-software/sebastian-brand`, revision
`4985cb83ee450e6bce08081ddd4e760a1f27dfdc`:

- `brand/software-on-light.svg` and `favicon.svg`: `icon-software-light-transparent.svg`
- `brand/software-on-dark.svg`: `icon-software-dark-transparent.svg`
- `brand/logo-software.svg`: `logo-software-transparent.svg`

The local names describe the background on which each icon is used. Keep the
original geometry, proportions, and colors. Use the existing wordmark or icon;
do not invent an initials mark for the Skills site.

The site palette uses Software's Midnight, Teal, Lagoon, Signal, and Frost
colors, with lighter and darker surface/text tones for accessible contrast.
The upstream brand system owns the brand definitions.

Headings use **Sebastian Slab Medium (500)**, the Elena webfont used by the
Consulting site. Body text, navigation, and controls use the platform's system
UI font. The company wordmark retains its original outlined typography, and
the model seals keep their own sans-serif lettering.

The heading font is loaded from the [existing company CDN asset](https://sebastian-consulting.com/assets/slab-serif-Medium-Cq_srit_.woff2).
Its 46 KB WOFF2 is byte-identical to `fonts/slab-serif/slab-serif-Medium.woff2`
in the brand repository at the revision above. Only this normal, medium face
is requested. All pages preload it and use `font-display: swap` with the
Consulting site's metric-matched Georgia fallback.

The commercial font binary stays outside this open-source repository. It
remains subject to the company's font license, not the MIT/Apache licenses
here. The company CDN is an external dependency: if the asset URL changes,
update the CSS, the preload links in every HTML page, and the social-preview renderer together.
The browser checks verify it loads; visitors retain readable fallback text
if the CDN is unavailable.

Keep surfaces calm, with neutral elevation shadows rather than colored glow
or offset sticker shadows on interface controls.

## Model seals

`seals/gpt-6.svg` and `seals/opus-5-5.svg` implement the Precision Seals design.
They have an opaque white substrate, Software Teal upper ring, Signal accent,
sans-serif labels, and unchanged provider artwork. They remain white in dark
mode. Keep the company name visible as issuer and link their homepage caption
to the explanation of what “tuned for” means. These are our tuning labels, not
provider certification, endorsement, benchmark scores, or test grades.

Regenerate both self-contained vectors after changing the shared layout:

```sh
node scripts/render-model-seals.mjs
```

SVG text uses Arial/Helvetica and does not need a web font or runtime script.
The originals below remain separate so the embedded provider paths can be
compared with the source assets. The generator only scales and positions them.

## Third-party marks

These marks identify the models and technologies covered by the skills. They
remain the property of their respective owners and are not relicensed under
the repository's MIT/Apache licenses.

| Local asset | Original source |
| --- | --- |
| `providers/openai-blossom.svg` | `OpenAI-black-monoblossom.svg` from [OpenAI's official asset pack](https://cdn.openai.com/brand/OpenAI-Logos-2025.zip), linked by its [brand guidelines](https://openai.com/brand/) |
| `providers/claude-spark.svg` | `Claude Spark - Clay.svg` from [Anthropic's press kit](https://www.anthropic.com/press-kit) |
| `technology/typescript.svg` | `ts-logo-512.svg` from the [TypeScript branding asset pack](https://www.typescriptlang.org/branding/typescript-design-assets.zip) |
| `technology/rust.svg`, `technology/rust-on-dark.svg` | `rust-logo.svg` and `rust-logo-white-outline.svg` from [Rust's official artwork](https://github.com/rust-lang/rust-artwork/tree/main/logo) |

Retrieved September 26, 2026. Original geometry and colors are unchanged. The
Rust logo is owned by the Rust Foundation and distributed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), as described in its [media guide](https://rust-lang.org/policies/media-guide).
The homepage footer also provides attribution. Technology logos are plain
identifiers, separate from the model seals.

## Raster exports

Generate the PNG and ICO fallbacks and the social preview with the existing
Playwright dependency and Chrome:

```sh
node scripts/render-site-assets.mjs
```

Run from the repository root after installing the development dependencies.
Set `CHROME_BIN` if Chrome is not at a known platform path. The social preview
uses the original wordmark and keeps inventory counts on the homepage.
