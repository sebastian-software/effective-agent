# Typography

> Deep appendix. Start from [typography-system.md](typography-system.md) and [typography-detail.md](typography-detail.md); load this file only for exceptional editorial and display treatments.

Learn a system of logical guidelines to make text beautiful and easy to read.

## Typeface Classifications

**Serif** - Decorative tails/feet at ends of letters. Traditional, classic, formal mood. Some legible at small sizes, others better for large.

**Sans Serif** - No decorative tails. Modern, simple. Highly legible at all sizes. Safe, neutral option for most interfaces.

**Script** - Based on handwriting. Low legibility - not suitable for small sizes. Can convey formal or casual mood at large sizes.

**Display** - Wide range of decorative styles. Designed for large sizes only. Strong character, good for conveying different moods.

**Monospaced** - Every character takes same horizontal space. Good for code and numbers (easier to compare).

## Decide Typography Roles First

Do not choose fonts by mood alone. Decide the text roles before selecting or
changing type.

| Role | Needs |
|------|-------|
| Functional UI | Legible at small sizes, sturdy weights, clear forms, predictable metrics |
| Body prose | Comfortable measure, line height, paragraph rhythm, strong fallback behaviour |
| Display text | Distinct voice, large-size quality, controlled line breaks |
| Data and code | Tabular numbers or monospaced alignment where comparison matters |

Product UI often works best with one well-tuned sans-serif family and a tight
scale. Brand surfaces may need a stronger display voice. Content-heavy surfaces
need reading rhythm more than personality.

Before implementation, decide:

- Which roles exist on this surface.
- Whether one family can serve all roles.
- Which scale ratio fits the register.
- Which weights are genuinely distinct.
- How fallback fonts, long text, and localisation affect layout.

## Use a Single Sans Serif Typeface

Safest for most interface designs.

### Reasons

**1. Legibility**
- Sans serif most legible
- Main purpose of interface text: clearly communicate information
- If not legible = harder to read, understand, use

**2. Neutrality**
- Don't convey strong mood/personality
- Fits most brand personalities
- Content is focal point, not typeface
- Less chance of unsuitable choice

**3. Simplicity**
- Less character and detail
- Complicated typefaces = distracting, increased cognitive load
- Less is more with typography

### Choosing Functional Text Typefaces

For UI/functional text (labels, captions, navigation, data), prioritise:
- Open, distinct letterforms — capital I, lowercase l, and number 1 must be easily distinguishable
- Large x-height for legibility at small sizes (but not so large that n and h become hard to tell apart)
- Generous default letterspacing — don't compensate with `letter-spacing`; choose a correctly designed font
- Sturdy weights — avoid light weights for UI text; thin strokes blur or dissolve at small sizes
- Look for typefaces designed for signage or interfaces (e.g. Fira Sans, Source Sans, Roboto, Inter)

## Evoke Emotion Using a Second Typeface for Headings

If a second typeface is used, reserve it for headings; keep body and UI text in the primary family.

**Typeface Moods:**
- **Sans serif** - neutral, minimal, modern
- **Serif** - traditional, established, classic
- **Rounded sans serif** - fun, soft, playful
- **Casual script** - personal, handmade
- **Formal script** - formal, feminine, elegant
- **Light sans serif** - chic, modern, luxurious

### Combining Typefaces

Limit to 2-3 typefaces maximum. Every typeface must serve a clear, distinct purpose (body, display, functional).

**How to find good pairings:**
1. **Start with an anchor** — choose your body text typeface first, then find companions that complement it
2. **Match underlying structure** — pair typefaces with similar skeletons (e.g. both rational, both dynamic) but different expression
3. **Use contrast for distinction** — pair serif with sans-serif, or light with heavy, to create clear hierarchy
4. **Check similar metrics** — look for comparable x-heights, cap heights, and overall colour (density)
5. **Try superfamilies first** — families with serif + sans-serif siblings (e.g. Questa Sans + Questa Serif) are guaranteed to harmonise
6. **Consider same designer** — type designers leave personal stylistic thumbprints across their work

**Avoid:** Pairing typefaces that are too similar (e.g. two geometric sans-serifs) — they create uncomfortable "almost the same" tension without clear distinction.

### Workhorses vs Personalities

**Workhorses** (Helvetica, Futura, Proxima Nova) are versatile but need skill to make distinctive. Look to display styles within their superfamily for variety.

**Personalities** (typefaces with strong inherent character) do most of the work for you but suit fewer contexts. Favour personalities for display text — they make it easier to create distinctive designs.

## Tips for Choosing a Sans Serif Typeface

- Choose popular, tried and tested typefaces
- Look for variety of weights (light, regular, medium, semibold, bold)
- Look for taller lowercase letters (x-height) and greater letter spacing = more legible at small sizes
- Get inspiration from companies known for good design
- Ensure multi-language support if needed
- Look for OpenType features
- When in doubt, use default system typeface

## Normalize Font Sizes with font-size-adjust

Different fonts at the same `font-size` can appear vastly different in visual size due to varying x-heights (the height of lowercase letters). `font-size-adjust` normalizes this.

**Use cases:**
- **Fallback fonts:** Prevent layout shift when web fonts load
- **Mixing fonts:** Make a serif heading font and sans-serif body font work together with one type scale

```css
/* The value is the x-height ratio (x-height / font-size) */
body {
  font-family: "Custom Font", Arial, sans-serif;
  font-size-adjust: 0.5;  /* Normalize based on x-height */
}
```

**How to find the value:**
1. Measure your primary font's x-height ratio
2. Apply it - fallback fonts will scale to match visually

**Browser support:** Baseline Newly available (Chrome 127+, Firefox 118+, Safari 17+) — treat as a progressive enhancement

## Limit Font Weights and Ensure Clear Distinction

Don't use all available weights - adds noise and clutter. More importantly: avoid weights that are too similar to distinguish.

**Problematic combinations (too close together):**
- Light vs Thin
- Book vs Regular
- Semibold vs Bold

**Guidelines:**
- Typically 2, max 3 weights with clear visual distinction
- Common useful set: Regular (400), Medium (500), Bold (700)
- Very thin or thick weights - headings/large text only (difficult at small sizes)
- Each weight should serve a clear purpose in your hierarchy

## Use a Type Scale to Set Font Sizes

Logical way to create balanced font sizes that work together.

### How to Create

1. Start with base font size (body text)
2. Multiply by scale factor for larger sizes

### Popular Type Scales (smallest to largest)
- 1.067 – Minor Second
- 1.125 – Major Second
- 1.200 – Minor Third
- 1.250 – Major Third
- 1.333 – Perfect Fourth
- 1.414 – Augmented Fourth
- 1.500 – Perfect Fifth
- 1.618 – Golden Ratio

### Example (1.200 Minor Third, base 16px)
```
Heading 1: 40px / 48px line-height / bold
Heading 2: 32px / 40px line-height / bold
Heading 3: 24px / 32px line-height / bold
Heading 4: 20px / 28px line-height / bold
Body:      16px / 24px line-height / regular
Small:     14px / 20px line-height / regular
```

**Tips:**
- Round to nearest whole number
- Try to make line-heights divisible by 4 (aligns to 4pt grid)
- Adjust as needed once confident

### Small vs Large Type Scales

**Small scales (e.g., Major Second):**
- Less difference between sizes
- Better for complex apps, tools, dashboards

**Large scales (e.g., Perfect Fifth):**
- Larger differences between sizes
- Better for simpler interfaces, marketing sites

### Responsive Type Scales

Instead of just scaling individual font sizes, scale the **type scale ratio itself** based on viewport width:

| Viewport | Scale Ratio | H1 | H2 | H3 | Body |
|----------|-------------|----|----|-----|------|
| 320px | 1.2 (Minor Third) | 35px | 29px | 24px | 17px |
| 1024px | (interpolated) | 50px | 39px | 31px | 19px |
| 1500px | 1.33 (Perfect Fourth) | 63px | 47px | 36px | 20px |

**Why this works:**
- Headings can be dramatically larger on desktop (63px H1) without being too big on mobile (35px)
- The hierarchy stays proportional at all sizes
- Smooth fluid interpolation - no breakpoint jumps

Build the scale as one system rather than a collection of unrelated formulas.
Choose the small- and large-context base sizes and ratios, derive corresponding
steps at both ends, and interpolate each pair. A smaller ratio at the narrow end
and a larger ratio at the wide end can preserve readable hierarchy without
making display text dominate small containers. Keep deliberate outliers explicit
instead of distorting the entire ratio to accommodate one heading.

Export the result through stable semantic custom properties. Components should
consume the properties, not depend on the calculator, token generator, or build
tool that produced them. Verify the complete scale at continuous widths and at
browser zoom, not only at its two configured endpoints.

### Fluid Typography with clamp()

Use `clamp()` for font sizes that scale smoothly:

```css
/* clamp(minimum, preferred, maximum) — matches the 320px → 1500px scale above */
h1 {
  font-size: clamp(2.1875rem, 2.4vw + 1.7rem, 3.9375rem); /* 35px → 63px */
}

h2 {
  font-size: clamp(1.8125rem, 1.5vw + 1.5rem, 2.9375rem); /* 29px → 47px */
}

.prose {
  font-size: clamp(1.0625rem, 0.25vw + 1rem, 1.25rem); /* 17px → 20px */
}
```

**Benefits:**
- No hard jumps at breakpoints
- Smooth scaling between screen sizes
- Headings get proportionally bigger with more space

Keep a root-relative term in the preferred value and use relative units for the
bounds. A viewport-only formula can appear fluid while weakening browser zoom
and user font-size preferences.

**Note:** For UI elements like buttons and labels, fixed sizes (14px) often work better for consistency.

## Distinguish UI Text from Body Text

**UI text** (buttons, labels, navigation, table cells) and **body text** (articles, descriptions, long-form content) have different requirements.

### UI Text: 14px is Fine

For compact UI components, 14px works well and is common practice (Tailwind's base size):

- Buttons, labels, navigation items
- Table cells, form labels, badges
- Sidebar content, metadata

14px keeps UI components compact - important when combined with padding.

### Body Text: Scale Responsively

For long-form reading content, don't leave text hard at 16px - scale it:

- **Mobile (360-440px):** 16-18px — scales across phone viewports
- **Desktop (640px+):** 16-20px — scales with viewport; smaller screens (11-13") stay closer to 16px

```css
.prose {
  font-size: clamp(1rem, 0.4rem + 2.5vw, 1.125rem);        /* 16→18px across 360–440px */
}

@media (min-width: 640px) {
  .prose {
    font-size: clamp(1.125rem, 0.95rem + 0.25vw, 1.25rem);  /* 18→20px across 1120–1920px */
  }
}
```

### Input Fields: 16px Minimum on Mobile

iOS Safari auto-zooms inputs below 16px. See Forms chapter for details.

The key insight: avoid *both* tiny text that strains eyes *and* oversized text that wastes mobile screen space.

## Couple Line Height to Role, Size, and Measure

Choose the typeface, text role, font size, and actual line length before tuning
line height. Longer reading lines often benefit from more leading; larger
display sizes usually need a smaller unitless ratio. A body value near `1.5` is
a useful fallback when only one value is available, not a universal optimum or
an authored WCAG AA minimum.

Prefer unitless values for inherited defaults and role tokens. Use stepped
container-query changes when line height should follow measure. Smooth `cqi`
interpolation returns a length and therefore inherits differently; it needs a
real ancestor query container and role-level redeclaration wherever font size
changes.

Bound prose by role, commonly somewhere around `45–80ch`, but treat `ch` as an
approximation based on the zero glyph rather than a literal character counter.
Narrow an excessive reading measure before using very loose leading to rescue
it. Set paragraph spacing from the semantic rhythm system rather than an
incorrect conversion from unitless `line-height` to `em`.

Read [line-height-and-measure.md](line-height-and-measure.md) for starting
ranges, valid dynamic CSS patterns, font-metric formulas, WCAG distinctions,
and verification.

## Left Align Text

English read left to right, downwards in F-pattern.

**Left-aligned = easiest to read:**
- Each line starts at same left edge
- Consistent anchor for eyes

### Don't Centre Align Long Body Text
- Starting point changes each line
- Eyes work harder to find start
- OK for headings and short text

### Don't Justify Without Hyphenation

Plain justified text creates uneven word spacing and "rivers" of white space. If you must justify:

```css
.justified-prose {
  text-align: justify;
  hyphens: auto;                   /* Baseline Widely available — set lang attribute on <html> */
  hyphenate-limit-chars: 6 3 2;    /* Min 6 chars, 3 before break, 2 after */
}
```

**Fine-grained hyphenation controls** (`hyphenate-limit-lines`, `hyphenate-limit-zone`, `hyphenate-limit-last`) have uneven engine support. Safari supports specific legacy controls such as `-webkit-hyphenate-limit-lines` and `-webkit-hyphenate-limit-before`/`-webkit-hyphenate-limit-after`, while Chromium support is limited; use them as progressive enhancement:

```css
.justified-prose {
  /* Progressive enhancement — ignored by browsers that don't support them */
  hyphenate-limit-lines: 2;
  hyphenate-limit-zone: 8%;
  hyphenate-limit-last: always;
}
```

**When justification can work:** Long-form content with generous measure (60+ characters), combined with hyphenation. Still not recommended for short lines or narrow columns.

**When to avoid entirely:** Short text, narrow columns, dyslexia-sensitive contexts. Left-aligned text is always the safer default.

### Avoid Multiple Text Alignments
Harder to follow, looks messy.

## Kerning and Letter Spacing

### Enable Kerning

Kerning adjusts spacing between specific character pairs (e.g. AV, To, Wa). Always enable it:

```css
body {
  font-kerning: normal;  /* Enable OpenType kerning */
}
```

### Letter Spacing (Tracking) Guidelines

**Decrease for large, bold, or wide text:**
```css
.display-heading {
  letter-spacing: -0.02em;  /* Tighten large/bold text ~2-3% */
}
```

**Increase for ALL CAPS and long digit strings:**
```css
.uppercase-label {
  text-transform: uppercase;
  letter-spacing: 0.05em;  /* Open up ~5% for caps */
}
```

**Turn off ligatures when letterspacing:**
```css
.spaced-text {
  letter-spacing: 0.05em;
  font-variant-ligatures: no-common-ligatures;  /* Ligatures look wrong when spaced */
}
```

**Never letterspace lowercase** body text without good cause — it damages word shapes and reduces readability.

## Use OpenType Features for Polished Typography

Modern fonts contain advanced features that improve readability and professional appearance. Use CSS `font-variant` and `font-feature-settings` to activate them.

### Small Caps

Use for abbreviations and words set in uppercase inside body text so they blend in better. Always use real small caps - never fake them by scaling down capitals.

```css
/* Real small caps */
.abbreviation {
  font-variant-caps: all-small-caps;
  font-feature-settings: "c2sc", "smcp";
}
```

Fake small caps (scaled-down capitals) have thinner strokes and look out of place next to regular text.

### Figure Styles

Figure styles split into two groups:

**Old-style vs Lining figures:**
- **Old-style figures** have varying heights (some descend below baseline) - better for body text as they blend in
- **Lining figures** are all the same height - better for headings and UI elements

```css
.body-text { font-variant-numeric: oldstyle-nums; }
.ui-numbers { font-variant-numeric: lining-nums; }
```

**Proportional vs Tabular figures:**
- **Proportional figures** have varying widths (natural spacing) - good for running text
- **Tabular figures** all take the same horizontal space - essential for tables, prices, and anywhere numbers need to align vertically

```css
.price-table { font-variant-numeric: tabular-nums; }
.prose       { font-variant-numeric: proportional-nums; }
```

### Ligatures

**Common ligatures** (fi, fl, ff, ffl, ffi) improve legibility in body text. Enabled by default in most browsers - don't disable them.

**Discretionary ligatures** are more ornamental. Use sparingly and only for decorative headings:
```css
.decorative-heading {
  font-variant-ligatures: discretionary-ligatures;
  font-feature-settings: "dlig";
}
```

### Proper Punctuation and Typographic Marks

Use the correct typographic marks:
- **Hyphen** (-) connects words: "five-dollar"
- **En dash** (\u2013) replaces "to": "6\u20135 p.m."
- **Em dash** (\u2014) can indicate a break in thought; route its use and spacing to `effective-writing` for the target locale while preserving an established house style
- **Quotation marks** \u2014 mark selection is locale-specific and belongs to the `effective-writing` skill (English curly \u201c \u201d \u2018 \u2019, German \u201e \u201c \u00bb \u00ab, French \u00ab \u00bb, and others differ); implement the chosen marks with CSS `quotes` and `:lang()` rather than hardcoding one language's glyphs. Straight marks (' ") remain for code only.

**Additional typographic marks:**
- **Proper minus** (`&minus;` / −) for negative numbers — not a hyphen
- **Proper ellipsis** (`&hellip;` / …) — one character, not three dots
- **Multiplication** (`&times;` / ×) — not the letter x
- **Non-breaking space** (`&nbsp;`) — between values and units (100 km), initials (J. K. Rowling), and between last two words of headings (prevents widows)
- **Dash and quotation spacing** — use `effective-writing` for the target locale, preserve an established house style, and do not add breaking thin spaces for visual effect

## Prevent Faux Bold and Italic

Browsers synthesise bold/italic when the required font file isn't loaded. Faux bold smears outlines; faux italic mechanically slants the roman. Both look wrong.

Set `font-synthesis: none` at the root so missing assets fail visibly instead of
quietly changing the letterforms. Then load and declare every weight and style
the interface uses, and verify that fallback and font-failure states preserve a
legible hierarchy.

```css
:root {
  font-synthesis: none;
}

@font-face {
  font-family: 'MyFont';
  src: url('myfont-regular.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
}
```

If the interface requests `font-weight: 700` or italic, provide the matching
face or variable-font range. Do not rely on browser synthesis as the normal
rendering path.

## Table Typography

Tables are text to be read — apply typographic care.

**Number formatting:**
- Use **tabular lining numerals** in data tables (equal-width digits that align vertically)
- **Right-align numbers** so decimal points and digit places line up
- **Left-align text** columns
- Align column headings with their data (right-align headers above number columns)

**Reduce visual clutter:**
- Minimise borders, fills, and rules — use white space to separate rows and columns
- Alternating row colours are rarely needed if spacing is adequate
- Horizontal rules between rows are often sufficient; vertical rules almost never needed

```css
.data-table {
  font-variant-numeric: tabular-nums lining-nums;
  border-collapse: collapse;
}

.data-table td.number {
  text-align: right;
  font-variant-numeric: tabular-nums lining-nums;
}
```

## Display Text and Headlines

### Sizing Display Text

For display text that scales with the viewport, use `vmin` units for consistent sizing across portrait and landscape orientations:

```css
.hero-heading {
  font-size: clamp(2rem, 1rem + 6vmin, 5rem);
}
```

### Optical Sizing

Different sizes of text benefit from different font characteristics. Enable automatic optical sizing when available:

```css
body {
  font-optical-sizing: auto;  /* Browser adjusts for rendered size */
}
```

At small sizes: increased x-height, wider spacing, thicker strokes for legibility. At large sizes: finer details, tighter spacing, higher contrast for elegance.

### Hanging Punctuation for Display Text

For large quoted text, pull punctuation into the margin so the text edge aligns visually. The CSS `hanging-punctuation` property exists but is Baseline Limited availability (Safari only). Use a negative `text-indent` instead:

```css
blockquote.display {
  text-indent: -0.4em;  /* Hang opening quote mark — works everywhere */
}
```

### Drop Caps

Use `initial-letter` for drop caps (Baseline Limited availability: Chrome 110+, no Firefox; Safari only via the `-webkit-` prefix, which an unprefixed `@supports` check misses). Provide a fallback for unsupported browsers:

```css
.article > p:first-of-type::first-letter {
  /* Fallback for browsers without initial-letter */
  float: left;
  font-size: 3.2em;
  line-height: 0.8;
  margin-right: 0.1em;
  font-weight: bold;
}

@supports (initial-letter: 3) {
  .article > p:first-of-type::first-letter {
    float: none;
    font-size: inherit;
    line-height: inherit;
    initial-letter: 3;  /* Span 3 lines */
  }
}
```

### Prevent Widows in Headings

A single word on the last line of a heading looks orphaned. Use CSS `text-wrap: balance` (Baseline Newly available: Chrome 114+, Firefox 121+, Safari 17.5+) for headings and `text-wrap: pretty` (Limited availability: Chrome 117+, Safari 26+, not Firefox) for paragraphs — both are safe progressive enhancements:

```css
h1, h2, h3, h4, h5, h6 {
  text-wrap: balance;  /* Equalises line lengths in headings */
}

p {
  text-wrap: pretty;   /* Avoids orphan words on last line */
}
```

For browsers without support, these properties degrade gracefully to normal wrapping. As an additional safeguard, insert `&nbsp;` between the last two words of critical headings.

## Vertical Rhythm

Use the body text line-height as the fundamental spacing unit. All vertical spacing — paragraph margins, heading spacing, padding — should be multiples of this base unit.

```css
:root {
  --baseline: 1.5rem;  /* 24px if root is 16px */
}

h2 { margin-block: calc(var(--baseline) * 2) var(--baseline); }
h3 { margin-block: calc(var(--baseline) * 1.5) calc(var(--baseline) * 0.5); }
p  { margin-block: 0 var(--baseline); }
```

This creates a predictable, harmonious rhythm throughout the page. Embedded media (images, videos) may break the rhythm — that's acceptable; resume the rhythm after.

## Ensure Text on Photos is Legible

Common mistake: placing text directly on photos.

**Contrast requirements:**
- Small text (below 18.66px bold or below 24px regular): 4.5:1 minimum
- Large text (at least 18.66px bold OR at least 24px regular): 3:1 minimum

### Solutions

**Linear gradient overlay:**
- Dark grey, 90% opacity at bottom, 0% halfway up
- Add text shadow

**Semi-transparent overlay:**
- Dark grey, 50% opacity over entire photo
- Add text shadow

**Blurred semi-transparent overlay:**
- Add blur effect for easier reading

**Solid text background:**
- Popular for video captions
- White text on dark grey background

## Avoid Light Grey and Pure Black Text

**Light grey text:**
- Accessibility issue - many can't read or find difficult
- Always aim for 4.5:1 contrast minimum

**Pure black text:**
- Too high contrast causes eye strain and fatigue
- Black: 0% brightness, White: 100%
- Large difference makes eyes work harder
- Use accessible dark grey instead
