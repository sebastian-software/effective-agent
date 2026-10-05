# Web Fonts

Loading and performance guidelines for using custom fonts on the web.

## @font-face Basics

Link to font files using `@font-face`, specifying weight and style for each file:

```css
@font-face {
  font-family: 'MyFont';
  src: url('myfont-regular.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'MyFont';
  src: url('myfont-bold.woff2') format('woff2');
  font-weight: 700;
  font-style: normal;
  font-display: swap;
}
```

**WOFF2 only.** With 97%+ browser support, WOFF2 is the only format you need. WOFF (without the "2") and older formats like EOT and TTF are no longer necessary — IE11, the last browser that needed them, has been discontinued.

Fonts are only downloaded when needed — if no element on the page uses a declared `@font-face`, it won't be fetched.

## FOIT vs FOUT

When a web font hasn't loaded yet, browsers face a dilemma:

- **FOIT** (Flash of Invisible Text) — hide text while the font loads. Most browsers default to a short block period (~3 s) and then swap to a fallback — not indefinitely invisible text, but still seconds of blank space where text should be.
- **FOUT** (Flash of Unstyled Text) — show text in a fallback font immediately, swap when the web font loads. Text reflows but content is accessible immediately.

**FOUT is the lesser evil.** Content should be readable as soon as it loads. A usable page within one second is the goal.

## Use font-display to Control Loading Behaviour

Add `font-display` to each `@font-face` rule:

| Value | Behaviour | Best For |
|-------|-----------|----------|
| `auto` | Browser decides (usually FOIT) | Avoid using |
| `block` | FOIT — invisible text until font loads | Icon fonts only |
| `swap` | FOUT — immediate fallback, swap when ready | **Most fonts (recommended default)** |
| `fallback` | Brief FOIT (~100ms), then FOUT, but gives up if too slow | When font swap causes measured CLS |
| `optional` | Uses font only if already cached, never blocks | Low-priority fonts; slow connections; measured CLS |

**Default to `swap` plus a metric-matched fallback font (`size-adjust`/`ascent-override`/`descent-override`); use `fallback` or `optional` when CLS is the measured problem.** `swap` shows content immediately, and the metric overrides (see below) make the swap nearly invisible. Only when layout shift from the swap remains a measured problem should you trade font fidelity for stability with `fallback` or `optional`.

## Preload the Most Critical Font

Tell the browser to start downloading a font immediately, before CSS is parsed:

```html
<link rel="preload" href="/fonts/myfont-regular.woff2"
      as="font" type="font/woff2" crossorigin>
```

**Rules:**
- Only preload **one** font — the most important one (usually body text regular)
- Preloading delays initial page render, so don't overdo it
- Until their files load, bold and italic text lacks its real face; under the root `font-synthesis: none` policy it is not faux-synthesised, so check that the interim hierarchy stays legible
- The `crossorigin` attribute is required even for same-origin fonts

## Choose Fallback Fonts Carefully

With a FOUT strategy, users see the fallback font first. Choose fallbacks that closely match your web font:

**Matching priorities (in order):**
1. **Similar x-height** — ensures text appears the same size
2. **Similar horizontal metrics** — minimises reflow when fonts swap
3. **Similar style** — match the general feel (humanist, geometric, etc.)

**Build a cross-platform fallback stack:**

```css
body {
  font-family: "MyWebFont", "Calibri", "PT Sans", "Roboto", sans-serif;
}
```

Order by best match. Include fonts from Windows (Calibri, Segoe UI), macOS/iOS (system-ui, -apple-system), and Android (Roboto).

### Use font-size-adjust for Fallback Matching

`font-size-adjust` normalises the visual size of fallback fonts to match your web font's x-height:

```css
body {
  font-family: "MyWebFont", "Arial", sans-serif;
  font-size-adjust: 0.52;  /* x-height ratio of MyWebFont */
}
```

This prevents the size jump when fonts swap, without needing JavaScript font event classes.

## Reduce Font Payload

### Limit the Number of Fonts

Each WOFF2 file is typically 15–70 KB. A typical page might load 4-6 files (regular, bold, italic, bold-italic for body + display). Keep the total reasonable — every file is a network request.

### Subset Your Fonts

Remove glyphs you don't need (unused languages, ornamental alternates):

```css
/* Load Latin subset only when Latin characters are on the page */
@font-face {
  font-family: 'MyFont';
  src: url('myfont-latin.woff2') format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+2000-206F;
}

/* Load extended Latin on demand */
@font-face {
  font-family: 'MyFont';
  src: url('myfont-latin-ext.woff2') format('woff2');
  unicode-range: U+0100-024F, U+0259, U+1E00-1EFF;
}
```

The `unicode-range` descriptor makes the browser only download a font file when characters from that range appear on the page. This enables efficient lazy-loading of language subsets.

**Subsetting tools:** pyftsubset (from fonttools), glyphhanger.

**Don't subset too aggressively** — missing glyphs cause the browser to fall back to a different font for those characters, creating an ugly mix.

## Variable Fonts

A single variable font file can replace multiple static font files by defining variation axes:

```css
@font-face {
  font-family: 'MyVariable';
  src: url('myvariable.woff2') format('woff2');
  font-weight: 100 900;  /* Range of supported weights */
}

/* Use any weight value, not just multiples of 100 */
h1 { font-weight: 650; }
h2 { font-weight: 550; }
body { font-weight: 380; }
```

### Standard Axes

| Axis | Tag | CSS Property |
|------|-----|-------------|
| Weight | `wght` | `font-weight: 100-900` |
| Width | `wdth` | `font-stretch: 50%-200%` |
| Italic | `ital` | `font-style: italic` |
| Slant | `slnt` | `font-style: oblique Xdeg` |
| Optical size | `opsz` | `font-optical-sizing: auto` |

### Custom Axes

Type designers can define custom axes (x-height, contrast, serif shape, etc.) accessed via the low-level property:

```css
h2 {
  font-variation-settings: "wdth" 600, "wght" 200, "opsz" 48;
}
```

**Benefits of variable fonts:**
- One file replaces many — significant bandwidth savings
- Access to precise intermediate weights (not just 100, 200, ... 900)
- Responsive typography — smoothly adjust weight/width based on viewport
- Optical sizing — automatic adjustment for rendered size

## Metric-Matched Fallback Fonts

Instead of JavaScript class-swapping, use `@font-face` metric overrides to make the fallback font occupy nearly the same space as the web font — the swap becomes almost invisible:

```css
@font-face {
  font-family: "MyWebFont-fallback";
  src: local("Arial");
  size-adjust: 104%;        /* scale glyphs to match the web font's widths */
  ascent-override: 92%;     /* match vertical metrics */
  descent-override: 24%;
}

body {
  font-family: "MyWebFont", "MyWebFont-fallback", sans-serif;
}
```

The adjusted local font renders immediately; when the web font arrives, text barely reflows. Tools like Fontaine or Capsize compute the override values for a given font pairing — don't hand-tune them.

**Edge case:** the Font Loading API (`document.fonts.load()`, `document.fonts.ready`) remains useful when you genuinely need to know *when* a font is available — e.g. before measuring text in `<canvas>` or SVG. It is no longer needed for FOUT control.

## Webfonts as Progressive Enhancement

Treat web fonts as an enhancement, not a requirement:

1. **Start with a good fallback** — the page must be usable and readable in system fonts
2. **Load web fonts** — swap them in when available
3. **Respect connectivity** — use `font-display: optional` for non-critical fonts on slow connections

The content is always more important than the typeface rendering it.
