# Brand assets

## Effective Agent: Field Guide

The product has an independent book-and-compass identity, selected from
[the Field Guide direction](../../design/field-guide/README.md).
It represents inspectable guidance and a useful direction, without encoding
the number of skills. The SVGs are native vectors:

- `brand/field-guide.svg`: forest and terracotta on a light surface.
- `brand/field-guide-reverse.svg`: reversed for dark surfaces.
- `brand/field-guide-mono.svg`: a single-color version using `currentColor`.
- `favicon.svg`: the light product mark.

Use the product mark with the live-text name **Effective Agent**, without an
issuer subtitle. It can sit inside an Effective Agent feature on the Sebastian
Software OSS site; it does not replace that site's masthead.

The product palette uses warm ivory, forest green, and terracotta, with explicit
light and dark surface/text tokens in `styles.css`. The editorial layout lives
in `field-guide.css`; shared interactions and accessibility remain in the base
stylesheet. Inventory and skill names stay in HTML, separate from the artwork.

## Sebastian Software master identity

The About section retains the unchanged corporate mark from the
`sebastian-software/` directory in `sebastian-software/sebastian-brand`, revision
`4985cb83ee450e6bce08081ddd4e760a1f27dfdc`:

- `brand/software-on-light.svg`: `icon-software-light-transparent.svg`.
- `brand/software-on-dark.svg`: `icon-software-dark-transparent.svg`.
- `brand/logo-software.svg`: `logo-software-transparent.svg`.

Keep the original corporate geometry, proportions, and colors. The product
identity is a separate asset, not a recolored company icon.

## Typography

Headings use **Sebastian Slab Medium (500)**, the Elena webfont used by the
Consulting site. Body text, navigation, and controls use the platform's system
UI font. The company wordmark retains its original outlined typography, and
the archived model seals keep their own sans-serif lettering.

The heading font is loaded from the official [company asset CDN](https://assets.sebastian-software.com/fonts/Elena/Elena-Medium-latin-f0e984d3e709.woff2).
The Latin and extended Elena Medium subsets follow the definitions in the
[shared font stylesheet](https://assets.sebastian-software.com/fonts/fonts.css).
Only this normal, medium face is requested. All pages preload the Latin subset;
the extended subset loads for matching characters. Both use `font-display: swap`
with the Consulting site's metric-matched Georgia fallback.

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
mode. They are retained as historical assets and are not used in the Field Guide
hero or social preview. If reused, preserve the issuer and explain what
“tuned for” means. These are our tuning labels, not
provider certification, endorsement, benchmark scores, or test grades.

Regenerate both self-contained vectors after changing the shared layout:

```sh
node scripts/render-model-seals.mjs
```

SVG text uses Arial/Helvetica and does not need a web font or runtime script.
The originals below remain separate so the embedded provider paths can be
compared with the source assets. The generator only scales and positions them.

## Third-party marks

These retained marks identify models and technologies covered by the skills. They
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
The Field Guide pages do not display these retained third-party marks.
If reused, provide the applicable attribution on the surface where they appear.

## Desk illustration

`illustrations/field-guide-desk.png` is original Imagegen artwork with a transparent
background. The overlapping guides do not encode the collection size or assign
one volume per skill. Miniature type and technical diagrams are decorative;
readable names, inventory, and claims stay in HTML. Desk details use coffee,
glasses, notes, a compass, and a pen rather than botanical decorations.

The [implementation notes and exact prompts](../../design/field-guide/README.md)
record the generation and targeted edits. Keep the original alpha channel when
exporting the scene. Generated detail is not source-authoritative instruction.

## Raster exports

Generate the PNG and ICO fallbacks and the social preview with the existing
Playwright dependency and Chrome:

```sh
node scripts/render-site-assets.mjs
```

Run from the repository root after installing the development dependencies.
Set `CHROME_BIN` if Chrome is not at a known platform path. The social preview
uses the product mark and reusable desk illustration. Inventory counts remain
in HTML rather than being baked into the art.
