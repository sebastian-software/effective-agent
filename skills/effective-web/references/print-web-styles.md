# Print Styles

> Deep appendix. Start from [print-web-basics.md](print-web-basics.md), then [print-web-content.md](print-web-content.md) or [print-web-layout.md](print-web-layout.md); load this file only for uncommon output constraints.

Ensure web pages produce clean, readable output when printed on paper or saved as PDF.

## @media print Basics

Print styles let you override screen styles for paged media. They apply when the user triggers Print or Save as PDF.

### Embedding Strategies

**Inline in the main stylesheet (preferred):**

Avoids an extra HTTP request and keeps print rules co-located with the screen rules they override.

```css
/* Inside your main stylesheet */
@media print {
  /* print-only rules */
}
```

**Separate file via `<link>`:**

Useful when the print stylesheet is large or maintained by a different team.

```html
<link rel="stylesheet" href="print.css" media="print">
```

The browser downloads `print.css` at low priority and only applies it when printing, so it does not block rendering.

### Hiding Non-Essential Elements

Hide interactive controls and transient chrome by default, but retain navigation,
sidebars, or footer material when they provide necessary document wayfinding,
offline provenance, legal notices, or task context. Decide from the printed
artifact rather than the HTML element name.

```css
@media print {
  nav:not([data-print-keep]),
  footer:not([data-print-keep]),
  aside:not([data-print-keep]),
  .sidebar:not([data-print-keep]),
  .ads,
  .cookie-banner,
  .share-buttons,
  button,
  .no-print,
  video,
  audio,
  iframe,
  form,
  .modal,
  .tooltip {
    display: none !important;
  }
}
```

### Blacklist vs Whitelist Approach

**Blacklist:** List every element to hide. Simple but fragile -- new elements added to the page need explicit hiding.

**Whitelist:** Hide everything by default, then show only the main content area. More robust for complex pages.

```css
/* Whitelist approach */
@media print {
  body > *:not(main) {
    display: none !important;
  }
}
```

The blacklist approach is more common because it is easier to reason about. The whitelist approach is safer for large sites where the page structure changes frequently.

## @page Rule

The `@page` at-rule controls page dimensions, margins, and orientation for paged media.

### Margins

```css
@page {
  margin: 2cm;
}

/* Different margins per side */
@page {
  margin-top: 2.5cm;
  margin-bottom: 2.5cm;
  margin-left: 2cm;
  margin-right: 2cm;
}
```

A `2cm` margin is a safe default that leaves room for printer hardware margins while giving content enough space.

### Page Size and Orientation

The `size` descriptor accepts named sizes and/or an orientation keyword.

```css
@page {
  size: A4;              /* A4 portrait (default) */
}

@page {
  size: A4 landscape;    /* A4 landscape */
}

@page {
  size: letter;          /* US Letter: 8.5in x 11in */
}

@page {
  size: 210mm 297mm;     /* Explicit dimensions */
}
```

Named size keywords: `A3`, `A4`, `A5`, `B4`, `B5`, `letter`, `legal`, `ledger`.

### Pseudo-Class Selectors

```css
@page :first {
  margin-top: 4cm;       /* Extra top margin on first page for title */
}

@page :left {
  margin-left: 3cm;      /* Wider inner margin for binding */
  margin-right: 2cm;
}

@page :right {
  margin-left: 2cm;
  margin-right: 3cm;
}

@page :blank {
  /* Style intentionally blank pages */
}
```

### Named Pages

Named pages allow different configurations per content type.

```css
@page cover {
  margin: 0;
  size: A4 landscape;
}

@page chapter {
  margin: 2.5cm;
  size: A4;
}

.cover-page {
  page: cover;
}

.chapter-content {
  page: chapter;
}
```

### Margin Boxes (Chromium)

Chromium supports margin at-rules (`@top-center`, `@bottom-center`, `@bottom-right`, etc.) for inserting headers, footers, and page numbers into the page margins.

```css
@page {
  @top-center {
    content: "Document Title";
  }
  @bottom-right {
    content: counter(page) " of " counter(pages);
  }
}
```

**Browser support:** `margin` and `size` work in all major browsers; `page-orientation` works in Chromium and Firefox but not Safari. Margin at-rules are Chromium-only as of early 2026; named pages (the `page` property) work cross-browser (Chrome 85+, Firefox 110+, Safari).

## Page Breaks

### Modern Properties vs Legacy Properties

The legacy properties `page-break-before`, `page-break-after`, and `page-break-inside` have been replaced by `break-before`, `break-after`, and `break-inside`. The modern properties also handle column and region breaks. For maximum compatibility, declare both.

```css
@media print {
  /* Force a page break before every h1 */
  h1 {
    page-break-before: always;   /* Legacy */
    break-before: page;          /* Modern */
  }

  /* Avoid breaking inside figures, tables, code blocks */
  figure,
  table,
  pre,
  blockquote,
  img {
    page-break-inside: avoid;    /* Legacy */
    break-inside: avoid;         /* Modern */
  }

  /* Avoid a page break immediately after headings */
  h1, h2, h3, h4, h5, h6 {
    page-break-after: avoid;     /* Legacy */
    break-after: avoid;          /* Modern */
  }
}
```

### Orphans and Widows

Orphans are lines left at the bottom of a page before a break. Widows are lines stranded at the top of the next page. Both default to 2 in most browsers. Set them higher for better readability.

```css
@media print {
  p {
    orphans: 3;    /* Minimum 3 lines before a page break */
    widows: 3;     /* Minimum 3 lines after a page break */
  }
}
```

### Practical Combinations

```css
@media print {
  /* Keep headings with their following content */
  h1, h2, h3, h4 {
    break-after: avoid;
    page-break-after: avoid;
  }

  /* Start major sections on new pages */
  .chapter,
  .section-break {
    break-before: page;
    page-break-before: always;
  }

  /* Never split these across pages */
  table, figure, pre, blockquote, ul, ol {
    break-inside: avoid;
    page-break-inside: avoid;
  }
}
```

**Note on Flexbox/Grid:** Page breaks inside flex and grid containers vary by engine. Use them for sections kept whole with `break-inside: avoid`; keep content that may run across pages in simple block flow (see [print layout](print-layout.md)).

## Typography for Print

### Selecting Body Fonts

Serif and sans-serif families can both work in print. Choose a body face by
legibility at the target point size, glyph and language coverage, available
weights/styles, embedding or licensing constraints, and the hierarchy required
by the artifact. Test the actual printer or PDF pipeline; a familiar fallback
such as Times New Roman is acceptable when it meets those criteria, not a font
to ban or prescribe categorically.

### Point-Based Sizing

Print media uses points (pt), not pixels. 1pt = 1/72 inch. Body text is typically 11pt (see [print typography](print-typography.md) for the authoritative scale); 12pt suits generous layouts or audiences needing larger type.

```css
@media print {
  body {
    font-family: Charter, Georgia, "Times New Roman", serif;
    font-size: 11pt;
    line-height: 1.4;
    color: #000;
  }

  h1 { font-size: 24pt; line-height: 1.1; }
  h2 { font-size: 18pt; line-height: 1.15; }
  h3 { font-size: 14pt; line-height: 1.2; }
  h4 { font-size: 11pt; font-weight: 700; line-height: 1.25; }
}
```

### Line Height

Use unitless values for `line-height`. Body text on paper reads well at 1.35–1.4 (tighter than screen; see [print typography](print-typography.md)). Decrease for headings (1.05–1.3, tighter as size grows). Increase for very long lines.

## Making Link Destinations Useful on Paper

Do not append every raw href mechanically. Use a human-readable link label by
default, then expose a destination when a reader needs an offline citation,
provenance trail, or actionable fallback. A short URL, numbered source list,
footnote, printed attribution, or QR code can be clearer than a full URL.

### Basic Technique

```css
@media print {
  a[data-print-url]::after {
    content: " (" attr(href) ")";
    font-size: 90%;
    word-break: break-all;
  }
}
```

Mark only links whose destination a paper reader must use. Keep the visible
label human-readable, and use `data-print-keep` on navigation, footer, or
sidebar elements that provide necessary document context:

```html
<a href="https://example.com/source" data-print-url>Source study</a>
<nav data-print-keep aria-label="Document sections">…</nav>
```

### Filtering: Only External Links

Internal anchors, `javascript:` links, `mailto:` links, and `tel:` links should not print their href.

```css
@media print {
  /* Mark only the selected external destinations that need a printed fallback. */
  a[data-print-url][href^="http"]::after,
  a[data-print-url][href^="//"]::after {
    content: " (" attr(href) ")";
    font-size: 90%;
    word-break: break-all;
  }

  /* Suppress for internal, mailto, tel, and JavaScript links */
  a[data-print-url][href^="#"]::after,
  a[data-print-url][href^="mailto:"]::after,
  a[data-print-url][href^="tel:"]::after,
  a[data-print-url][href^="javascript:"]::after {
    content: none;
  }
}
```

### Abbreviation Expansion

The same technique works for `<abbr>` elements so readers see the full term on paper.

```css
@media print {
  abbr[title]::after {
    content: " (" attr(title) ")";
  }
}
```

### Handling Long URLs

Long URLs can break layouts. Use `overflow-wrap` and `word-break` to allow wrapping.

```css
@media print {
  a[data-print-url][href^="http"]::after {
    content: " (" attr(href) ")";
    overflow-wrap: break-word;
    word-break: break-all;
  }
}
```

## Colour Adjustments

### Removing Backgrounds

Browsers strip background colours and images by default when printing to save ink. Design with this in mind.

```css
@media print {
  * {
    background: transparent !important;
    color: #000 !important;
    box-shadow: none !important;
    text-shadow: none !important;
  }
}
```

The aggressive `*` selector above comes from the HTML5 Boilerplate. A more targeted approach is preferable when some backgrounds carry meaning (table header shading, status badges, syntax highlighting).

### print-color-adjust: exact

When colours are meaningful, use `print-color-adjust: exact` to request that the browser preserves them.

```css
@media print {
  .status-badge,
  .chart,
  .syntax-highlight {
    print-color-adjust: exact;
    -webkit-print-color-adjust: exact;  /* Safari */
  }
}
```

**Values:**
- `economy` (default) -- browser may remove backgrounds and adjust colours to optimise for paper
- `exact` -- content has been specifically designed with colours that matter; preserve them

The user can always override this via the "Background graphics" checkbox in the print dialog. No CSS can override a user preference.

### forced-color-adjust

Related but distinct: `forced-color-adjust` controls whether elements are affected by forced colours mode (Windows High Contrast). Set `forced-color-adjust: none` on elements where colour is essential to meaning (charts, heatmaps), but use sparingly.

```css
.heatmap-cell {
  forced-color-adjust: none;
}
```

### Link Styling for Print

Remove coloured underlines and make links black text so they blend with body copy while remaining identifiable.

```css
@media print {
  a, a:visited {
    color: #000;
    text-decoration: underline;
  }
}
```

## Image Handling

### Prevent Overflow

Images must not exceed the printable area.

```css
@media print {
  img {
    max-width: 100% !important;
    height: auto;
    break-inside: avoid;
    page-break-inside: avoid;
  }
}
```

### Background Images Are Stripped

Browsers remove `background-image` by default when printing. Do not rely on CSS background images for meaningful content. If a background image is essential, use `print-color-adjust: exact`, but understand users may still override this. Use `<img>` elements for content images.

### Responsive Images in Print

When printing, browsers select from `srcset` based on device pixel ratio, not viewport width. This means the browser may select a small image variant. For critical print content, ensure the `src` fallback points to a sufficiently high-resolution source.

### Decorative Image Hiding

Hide purely decorative images to save ink.

```css
@media print {
  .decorative-image,
  [role="presentation"] {
    display: none;
  }
}
```

### Constrain Image Size

Prevent oversized images from wasting ink and paper.

```css
@media print {
  img {
    max-width: 100%;
    max-height: 3.5in;
  }
}
```

## Common Elements to Hide

| Element / Selector | Reason |
|---|---|
| `nav` | Hide interactive site navigation; retain concise document wayfinding when it helps the reader |
| `footer` (site footer) | Hide social or secondary navigation; retain provenance, legal notices, or page context when needed |
| `aside`, `.sidebar` | Hide incidental promotion; retain task instructions, annotations, or essential reference material |
| `button`, `input[type="submit"]` | Interactive -- no function on paper |
| `form` | Cannot submit from paper |
| `video`, `audio`, `iframe` | Cannot play media on paper |
| `.cookie-banner`, `.modal` | Overlay UI irrelevant |
| `.share-buttons`, `.social-links` | Interactive sharing impossible |
| `.ads`, `.advertisement` | No value on paper, wastes ink |
| `.back-to-top` | No scrolling on paper |
| `.search-bar`, `[role="search"]` | No search on paper |
| `.pagination` | Page navigation irrelevant |
| `.tooltip`, `.popover` | Hover-dependent UI |
| `.skip-link` | Keyboard navigation aid, not needed on paper |
| `.breadcrumb` (optional) | May keep for context, or hide to save space |

### Print-Only Content

Some content is useful on paper but hidden on screen.

```css
.print-only {
  display: none;
}

@media print {
  .print-only {
    display: block;
  }
}
```

**Use cases:** QR codes linking back to the page, "Printed from [URL]" attribution, expanded table of contents, legal disclaimers.

## Layout Adjustments

### Linearise to Single Column

Multi-column grid and flex layouts should collapse to a single column for reliable printing. Fragmentation inside flex and grid containers is unreliable across browsers.

```css
@media print {
  body {
    width: 100%;
    margin: 0;
    padding: 0;
  }

  main {
    width: 100%;
    max-width: none;
    margin: 0;
    padding: 0;
    float: none;
  }

  .grid-layout {
    display: block;
  }
}
```

### Full-Width Content

Remove `max-width` constraints so text fills the printable area.

```css
@media print {
  .container,
  .wrapper,
  .content {
    max-width: 100%;
    width: 100%;
    padding: 0;
    margin: 0;
  }
}
```

### Table Printing

Wide tables are problematic on paper. Ensure header rows repeat on each page and rows do not split.

```css
@media print {
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 10pt;
  }

  thead {
    display: table-header-group;  /* Repeat header on each page */
  }

  tfoot {
    display: table-footer-group;
  }

  tr {
    break-inside: avoid;
    page-break-inside: avoid;
  }
}
```

## When Print Styles Matter Most

Print styles are especially important for content that people routinely print or save as PDF:

- **Articles and blog posts** -- long-form content printed for offline reading or annotation
- **Recipes** -- commonly printed for kitchen use
- **Invoices and receipts** -- business documents printed for records
- **Documentation and manuals** -- technical docs, API references, user guides
- **Legal documents** -- terms, contracts, policies
- **Academic content** -- research papers, course materials
- **Real estate listings** -- property details printed for viewings
- **Contact pages** -- addresses, phone numbers, directions
- **Event tickets and confirmations** -- booking confirmations, itineraries
- **Government forms** -- applications, declarations
- **Maps and directions** -- still printed despite mobile devices

Even if analytics suggest few users print, the ones who do expect a usable result. A broken print layout reflects poorly on the site.

## Complete Starter Print Stylesheet

Copy-paste this into your main stylesheet as a starting point. Adjust selectors to match your markup.

```css
@media print {
  /* ---- Page setup ---- */
  @page {
    margin: 2cm;
    size: A4;
  }

  @page :first {
    margin-top: 3cm;
  }

  /* ---- Reset colours ---- */
  body {
    background: #fff;
    color: #000;
    font-family: Charter, Georgia, "Times New Roman", serif;
    font-size: 11pt;
    line-height: 1.4;
  }

  /* ---- Hide non-print elements ---- */
  nav:not([data-print-keep]),
  footer:not([data-print-keep]),
  aside:not([data-print-keep]),
  .sidebar:not([data-print-keep]),
  .ads,
  .cookie-banner,
  .share-buttons,
  .pagination,
  .back-to-top,
  .skip-link,
  button:not(.print-visible),
  video,
  audio,
  iframe,
  form,
  .modal,
  .tooltip,
  .no-print {
    display: none !important;
  }

  /* ---- Show print-only content ---- */
  .print-only {
    display: block !important;
  }

  /* ---- Links: expose only selected printed fallbacks ---- */
  a[data-print-url][href^="http"]::after,
  a[data-print-url][href^="//"]::after {
    content: " (" attr(href) ")";
    font-size: 90%;
    word-break: break-all;
  }

  a[data-print-url][href^="#"]::after,
  a[data-print-url][href^="mailto:"]::after,
  a[data-print-url][href^="tel:"]::after,
  a[data-print-url][href^="javascript:"]::after {
    content: none;
  }

  /* ---- Abbreviations: show expansion ---- */
  abbr[title]::after {
    content: " (" attr(title) ")";
  }

  /* ---- Link styling ---- */
  a, a:visited {
    color: #000;
    text-decoration: underline;
  }

  /* ---- Remove decorative effects ---- */
  * {
    box-shadow: none !important;
    text-shadow: none !important;
  }

  /* ---- Images ---- */
  img {
    max-width: 100% !important;
    height: auto;
    break-inside: avoid;
    page-break-inside: avoid;
  }

  /* ---- Page breaks ---- */
  h1, h2, h3, h4, h5, h6 {
    break-after: avoid;
    page-break-after: avoid;
  }

  figure, table, pre, blockquote, ul, ol {
    break-inside: avoid;
    page-break-inside: avoid;
  }

  p {
    orphans: 3;
    widows: 3;
  }

  /* ---- Tables ---- */
  table {
    width: 100%;
    border-collapse: collapse;
  }

  thead {
    display: table-header-group;
  }

  tr {
    break-inside: avoid;
    page-break-inside: avoid;
  }

  /* ---- Layout: linearise ---- */
  body, main, .container, .wrapper, .content {
    width: 100%;
    max-width: none;
    margin: 0;
    padding: 0;
    float: none;
  }

  /* ---- Preserve meaningful colours ---- */
  .status-badge,
  .chart,
  .syntax-highlight {
    print-color-adjust: exact;
    -webkit-print-color-adjust: exact;
  }
}
```

## Common Print Style Mistakes

### Mistake 1: Forgetting print styles entirely
The most common problem. Developers test on screen and never open Print Preview. Add print style testing to your QA checklist.

### Mistake 2: Not testing across browsers
Print rendering varies significantly between Chrome, Firefox, and Safari. Test in at least Chrome and Firefox. Safari handles page breaks differently.

### Mistake 3: Letting flex or grid content run across pages
Page breaks inside flex and grid containers vary by engine. Keep such sections whole with `break-inside: avoid`, or switch content that spans pages to `display: block` for print.

### Mistake 4: Long URLs breaking layouts
Appending `attr(href)` without `overflow-wrap: break-word` or `word-break: break-all` lets long URLs overflow the page and push content off the right edge.

### Mistake 5: Relying on background images for content
Background images are stripped by default. Use `<img>` for meaningful images, reserve `background-image` for decoration.

### Mistake 6: External font dependencies failing
Web fonts may not load during print. Always provide system font fallbacks in your `font-family` stack.

### Mistake 7: Ignoring orphans and widows
The default of 2 lines is too few. A single line stranded at the top of a page looks unprofessional. Set `orphans: 3` and `widows: 3`.

### Mistake 8: Not hiding interactive elements
Buttons, forms, modals, and video embeds printed on paper waste space and confuse users.

### Mistake 9: Printing irrelevant chrome without reviewing context
Ads, transient controls, and social-navigation chrome usually waste paper and
attention. Hide them by default, but retain concise breadcrumbs, document
navigation, citations, or task context when the printed artifact needs them.

### Mistake 10: Not linearising multi-column layouts
Columns that work on screen can produce bizarre results on paper -- content split across pages in an unreadable order. Collapse to a single column.
