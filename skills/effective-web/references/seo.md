# SEO for Frontend

> Deep appendix. Start from the [Frontend SEO and AI Search route](route-seo.md), which narrows to the crawl, metadata, or structured-data checks in scope; load this file for the full implementation reference.

Search engine optimisation techniques that frontend developers and designers directly control.

This chapter covers the intersection of UI design and SEO — the markup, metadata, and performance decisions made in HTML, CSS, and page structure. Keyword research, backlink strategy, analytics setup, and server configuration (robots.txt, sitemaps) are outside the scope of a UI design system.

For AI search and GEO, entity authority, business data distribution, LLM crawler access, feeds, and source-of-truth decisions, see [references/ai-geo-distribution.md](ai-geo-distribution.md).

## Document Head and Meta Tags

The `<head>` is the first thing search engines parse. Get the basics right on every page.

### Title Tag

The most important on-page SEO element. It appears in search results, browser tabs, and social shares.

```html
<title>Primary keyword — Secondary context | Brand</title>
```

**Guidelines:**
- Unique per page — never duplicate titles across pages
- 50-60 characters (longer titles get truncated in search results)
- Place the primary keyword near the beginning
- Make it click-worthy — it competes with other results and AI-generated summaries
- Put the brand name last, separated by `|` or `—`

### Meta Description

Not a ranking factor, but directly affects click-through rate from search results.

```html
<meta name="description" content="Learn how to optimise your frontend code for search engines. Practical guidelines on meta tags, structured data, and Core Web Vitals.">
```

**Guidelines:**
- Unique per page — duplicates signal low-quality content to crawlers
- 150-160 characters (Google truncates beyond this)
- Include the primary keyword naturally (Google bolds matching terms)
- Include a value proposition — tell users what they will get
- Write it as a call-to-action, not a passive description

### Canonical Tag

Tells search engines which URL is the "official" version when content is accessible at multiple URLs.

```html
<link rel="canonical" href="https://example.com/page">
```

**When to use:**
- Pages accessible with and without trailing slash (`/page` vs `/page/`)
- HTTP and HTTPS versions of the same page
- Pages with query parameters (`?sort=date`, `?ref=twitter`)
- Content syndicated or republished from another source
- Always self-referencing — every page should have a canonical pointing to itself

### Language and Localisation

```html
<html lang="de">
```

- Always set the `lang` attribute on `<html>` — it helps search engines serve the right language version and improves screen reader pronunciation
- For multilingual sites, use `hreflang` to link alternate language versions:

```html
<link rel="alternate" hreflang="en" href="https://example.com/en/page">
<link rel="alternate" hreflang="de" href="https://example.com/de/page">
<link rel="alternate" hreflang="x-default" href="https://example.com/en/page">
```

`x-default` specifies the fallback for users whose language is not covered.

## Favicons

Do not ship a public site without a favicon, but do not generate every legacy
size from an icon generator. Start with the three core assets below; add a
manifest and its three additional PNGs only when the site is installable as a
PWA. Keep `favicon.ico` available at the site root — some clients request that
path directly.

### Core Assets

| File | Size | Purpose |
|------|------|---------|
| `favicon.ico` | 32×32 | Fallback for older browsers |
| `icon.svg` | scalable | Modern browsers — supports dark mode |
| `apple-touch-icon.png` | 180×180 | iOS home screen bookmark |

### HTML Markup

```html
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
```

For Progressive Web Apps, also add a manifest link:

```html
<link rel="manifest" href="/manifest.webmanifest">
```

### SVG Favicon with Dark Mode

SVG favicons can adapt to the user's colour scheme using an embedded media query. This is particularly useful for monochrome logos.

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <style>
    .icon { fill: #1a1a1a }
    @media (prefers-color-scheme: dark) {
      .icon { fill: #ffffff }
    }
  </style>
  <path class="icon" d="..." />
</svg>
```

Serve SVG favicons with the correct MIME type: `image/svg+xml`.
Test icon selection and colour-scheme changes in the project's target
browsers; an already-open tab can retain a cached favicon until it reloads.

### Web Manifest for PWAs

Use `.webmanifest` only for an installable PWA. Its three extra icons are a
192×192 install icon, a 512×512 maskable icon, and a 512×512 standard icon.

```json
{
  "icons": [
    { "src": "/icon-192.png", "type": "image/png", "sizes": "192x192" },
    { "src": "/icon-mask.png", "type": "image/png", "sizes": "512x512", "purpose": "maskable" },
    { "src": "/icon-512.png", "type": "image/png", "sizes": "512x512" }
  ]
}
```

Maskable icons (adaptive icon shapes on Android) should have bigger paddings. The safe zone is a 409×409 circle within the 512×512 canvas. Use [maskable.app](https://maskable.app) to verify your icon.

### What Is Outdated

Do not generate or include these — they add complexity without benefit:

- Multiple PNG sizes (16×16, 24×24, 32×32, 48×48, 64×64) — browsers downscale the SVG or 180px PNG
- Multiple Apple touch icon sizes (57, 72, 76, 114, 120, 144, 152) — 180×180 covers all devices
- `browserconfig.xml` and `mstile-*.png` — Windows tiles are no longer relevant
- `rel="shortcut icon"` — the `shortcut` keyword is non-standard and unnecessary
- `type="image/x-icon"` on `.ico` links — browsers detect the format automatically
- Inline base64-encoded favicons — larger payload, not cacheable

### Generating Favicons

Start from a single SVG source file:

1. **SVG favicon** — use the source SVG directly (add dark mode styles if needed)
2. **ICO file** — export at 32×32 from the SVG (tools: sharp + sharp-ico, ImageMagick, or Inkscape)
3. **Apple touch icon** — export PNG at 180×180 with appropriate padding
4. **PWA only:** export PNGs at 192×192 and 512×512
5. **PWA only:** export the maskable PNG at 512×512 with extra padding so content fits within the 409×409 safe zone

## Open Graph and Social Metadata

When a URL is shared on social media, the platform scrapes Open Graph tags to build the preview card. Without them, platforms guess — and guess poorly.

```html
<meta property="og:title" content="SEO for Frontend Developers">
<meta property="og:description" content="Practical guidelines on meta tags, structured data, and Core Web Vitals.">
<meta property="og:image" content="https://example.com/images/seo-guide-og.jpg">
<meta property="og:url" content="https://example.com/seo-guide">
<meta property="og:type" content="article">
<meta property="og:locale" content="en_GB">
```

**Guidelines:**
- `og:image` — minimum 1200 x 630px, 1.91:1 ratio (works on all platforms)
- `og:title` — can differ from `<title>` (no brand suffix needed, more casual tone)
- `og:description` — can differ from `<meta name="description">` (optimise for social context)
- Twitter/X uses Open Graph as fallback, but for large image cards add:

```html
<meta name="twitter:card" content="summary_large_image">
```

**Test before shipping:** Use the sharing debuggers from Facebook, LinkedIn, and Twitter/X to verify how preview cards render. Cached previews can persist for days.

## Semantic Page Structure

Search engines use HTML structure to understand content hierarchy and relevance. Semantic markup benefits both SEO and accessibility — the same techniques serve both goals.

### One `<h1>` Per Page

The `<h1>` signals the primary topic of the page to search engines.

**Guidelines:**
- Exactly one `<h1>` per page containing the primary keyword (a content convention for clear topic signaling — neither Google nor WCAG requires a single `<h1>`; see [accessibility testing](accessibility-testing.md) before reporting extra `<h1>` elements as failures)
- It should match (or closely reflect) the `<title>` tag content
- Place it early in the `<main>` content area
- Do not use `<h1>` for site names or logos in the header — use styled `<a>` or `<p>` elements instead

### Logical Heading Hierarchy

```html
<h1>Page topic</h1>
  <h2>Major section</h2>
    <h3>Subsection</h3>
    <h3>Subsection</h3>
  <h2>Major section</h2>
    <h3>Subsection</h3>
```

- Never skip heading levels (e.g. `<h1>` directly to `<h3>`)
- Use headings for structure, not for styling — use CSS for visual size
- Headings create an implicit document outline that crawlers follow

### Landmark Elements

Use the correct semantic elements for page regions; the [Accessibility and HTML route](route-accessibility.md) owns landmark markup. The SEO benefit is that search engines can identify and weight content by its structural role.

| Element | SEO Role |
|---------|----------|
| `<main>` | Identifies the primary content (most weight for ranking) |
| `<nav>` | Identifies navigation — crawlers follow nav links to discover site structure |
| `<article>` | Marks self-contained content — helps search engines identify standalone pieces |
| `<aside>` | Signals secondary content — typically de-weighted for primary topic relevance |
| `<header>` / `<footer>` | Structural markers — help crawlers distinguish chrome from content |
| `<search>` | Identifies search functionality — improves site understanding |

### Breadcrumb Navigation

Breadcrumbs improve both usability and SEO. They appear in search results and help crawlers understand site hierarchy.

```html
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li><a href="/products/shoes">Shoes</a></li>
    <li aria-current="page">Running shoes</li>
  </ol>
</nav>
```

Pair with structured data (see below) to display breadcrumbs directly in search results.

## Structured Data (JSON-LD)

Structured data helps search engines understand *what* content is, not just *what it says*. It can enable eligible rich results such as star ratings, breadcrumb paths, and product prices in search results. Eligibility and supported result types change; markup is not a display guarantee.

### Implementation

Use JSON-LD (JavaScript Object Notation for Linked Data) embedded in a `<script>` tag. Google recommends JSON-LD over microdata or RDFa.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "SEO for Frontend Developers",
  "author": {
    "@type": "Person",
    "name": "Jane Smith"
  },
  "datePublished": "2026-01-15",
  "dateModified": "2026-02-01",
  "image": "https://example.com/images/seo-guide.jpg"
}
</script>
```

### Common Schema Types for UI Projects

| Schema Type | Use Case | Rich Result |
|-------------|----------|-------------|
| `Article` | Blog posts, news articles | Headline, image, date in results |
| `Product` | Product pages | Price, availability, ratings |
| `BreadcrumbList` | Breadcrumb navigation | Breadcrumb trail in results |
| `FAQPage` | Visible question-and-answer content | No Google rich result (retired May 2026) |
| `Organization` | Company info | Knowledge panel, logo |
| `LocalBusiness` | Physical business or location pages | Local panels, business facts |
| `Service` | Service pages | Entity clarity for offered services |
| `WebSite` | Homepage | No Google rich result (Sitelinks search box retired 2024); still useful for site-name and entity clarity |
| `HowTo` | Step-by-step guides | No Google rich result (retired) |

Google retired FAQ rich results on May 7, 2026; confirm current feature support
against [Google Search documentation updates](https://developers.google.com/search/updates)
before treating any schema type as a search appearance.

### BreadcrumbList Example

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://example.com/" },
    { "@type": "ListItem", "position": 2, "name": "Products", "item": "https://example.com/products" },
    { "@type": "ListItem", "position": 3, "name": "Running shoes" }
  ]
}
</script>
```

**Guidelines:**
- Place JSON-LD in the `<head>` or at the end of `<body>` — both work
- Only mark up content that is visible on the page — hidden structured data violates Google's guidelines
- Validate eligible markup with Google's Rich Results Test before deploying
- Inspect the rendered DOM when the application injects JSON-LD on the client; a static HTML fetch can miss markup that appears only after JavaScript runs
- One JSON-LD block per distinct entity; multiple blocks per page are fine
- Use stable `@id` values when the same entity appears across pages
- Keep business details, product data, reviews, prices, availability, and opening hours synchronized with the operational source of truth

For AI/GEO, structured data still helps with entity clarity and rich-result eligibility, but Google does not require special AI schema or extra GEO markup. See [references/ai-geo-distribution.md](ai-geo-distribution.md).

## Image SEO

Images are covered for responsive loading in [Web Performance route](route-performance.md) and for alt text in accessibility guidelines. This section adds the SEO-specific considerations.

### File Names

Search engines read file names as content signals.

```
team-meeting-2026.webp        (descriptive)
IMG_4532.webp                  (not useful)
hero-banner-final-v3.webp      (not useful)
```

- Use lowercase, hyphen-separated, descriptive names
- Include relevant keywords naturally — do not stuff
- Name files before uploading — renaming later means updating every reference

### Alt Text for SEO

Alt text serves accessibility first, SEO second. Write for users, not for crawlers.

```html
<!-- Good: descriptive and natural -->
<img src="team-meeting.webp" alt="Five team members reviewing design mockups at a whiteboard">

<!-- Bad: keyword stuffing -->
<img src="team-meeting.webp" alt="team meeting design agency best design agency meeting office">

<!-- Bad: redundant -->
<img src="team-meeting.webp" alt="image of a team meeting">
```

**Guidelines:**
- Describe what the image shows, not what you want to rank for
- Include keywords only where they naturally fit the description
- Keep alt text under 125 characters (screen readers may truncate)
- Decorative images get empty `alt=""` — no SEO value, no screen reader noise

### Image Format and Performance

Image optimisation directly affects Core Web Vitals (LCP in particular).

- Prefer WebP or AVIF — smaller file sizes with equal or better quality than JPEG/PNG
- Use `<picture>` for format negotiation with JPEG/PNG fallback
- Set explicit `width` and `height` or `aspect-ratio` to prevent CLS
- Use `loading="lazy"` for below-the-fold images
- Use `loading="eager"` (or omit the attribute) for the LCP image
- Use `fetchpriority="high"` on the LCP image to prioritise its download

```html
<img
  src="hero.webp"
  alt="Product dashboard showing real-time analytics"
  width="1200"
  height="630"
  fetchpriority="high"
>
```

## Core Web Vitals

Google uses Core Web Vitals as a ranking signal. The three metrics directly correlate with UI design and frontend implementation decisions.

### LCP — Largest Contentful Paint (< 2.5s)

Measures how quickly the main content becomes visible.

**What counts as LCP:** The largest image, video, or text block in the viewport at load time — typically the hero image or main heading.

**Frontend actions:**
- Preload the LCP image only if it is not discoverable in the initial HTML (e.g. a CSS `background-image`): `<link rel="preload" as="image" href="hero.webp">`; for an `<img>` in the markup, use `fetchpriority="high"` instead
- Use `fetchpriority="high"` on the LCP element
- Avoid lazy-loading the LCP image
- Preload one critical web font (see [Typography route](route-typography.md))
- Inline critical CSS
- Minimise render-blocking scripts — use `defer` or `async` on `<script>` tags

### INP — Interaction to Next Paint (< 200ms)

Measures responsiveness — how quickly the page reacts to user input.

**Frontend actions:**
- Keep event handlers fast — avoid synchronous layout calculations in click/input handlers
- Break long tasks (> 50ms) with `scheduler.yield()`, `setTimeout`, or `postMessage` — not `requestAnimationFrame`, which queues work at the head of the next frame (see [browser performance](browser-performance.md))
- Provide immediate visual feedback on interaction (see the 8 interaction states in [Fundamentals](fundamentals.md#clearly-indicate-interaction-states))
- Avoid layout thrashing — batch DOM reads before DOM writes
- Use CSS transitions for state changes rather than JavaScript-driven animation

### CLS — Cumulative Layout Shift (< 0.1)

Measures visual stability — how much content moves unexpectedly during loading.

**Frontend actions:**
- Set explicit `width` and `height` on all images and videos
- Use `aspect-ratio` in CSS for responsive media containers
- Reserve space for ads, embeds, and dynamically injected content
- Use `font-display: swap` plus a metric-matched fallback font (`size-adjust`/`ascent-override`/`descent-override`); use `fallback` or `optional` when CLS is the measured problem (see [Typography route](route-typography.md))
- Place dynamic content (banners, cookie notices) in fixed or reserved space — never push existing content down

## Internal Linking

How pages link to each other affects how search engines discover, crawl, and rank content. Navigation design is an SEO decision.

### Site Architecture

- Important pages should be reachable within 3 clicks from the homepage
- Flat hierarchies are better than deep nesting for SEO
- Every page should be linked from at least one other page — no orphan pages
- Use `<nav>` for primary and secondary navigation (helps crawlers identify site structure)

### Anchor Text

The clickable text of a link tells search engines what the target page is about.

```html
<!-- Good: descriptive -->
<a href="/guides/typography">Typography guidelines</a>

<!-- Bad: generic -->
<a href="/guides/typography">Click here</a>
<a href="/guides/typography">Read more</a>
```

**Guidelines:**
- Use descriptive anchor text that reflects the target page's content
- Vary anchor text naturally — identical anchor text across many links looks manipulative
- Avoid generic phrases: "click here", "read more", "learn more"
- This rule already aligns with accessibility best practices (screen readers announce link text out of context)

### Footer and Sidebar Links

- Keep footer links to genuinely useful pages (legal, contact, top-level categories)
- Do not stuff footers with keyword-rich links — search engines de-weight excessive footer links
- Sidebar links should support the current content context, not serve as a secondary sitemap

## URL Structure

Clean URLs help both users and search engines understand page content before visiting.

**Guidelines:**
- Use lowercase, hyphen-separated words: `/products/running-shoes`
- Keep URLs short and descriptive — remove filler words ("a", "the", "and")
- Include relevant keywords naturally
- Use a consistent trailing slash convention (either always or never — pick one)
- Avoid query parameters for content that should be indexed (`?id=123` is less useful than `/product/shoe-name`)
- Avoid uppercase letters, underscores, and special characters
- Match URL structure to site hierarchy: `/category/subcategory/page`

```
Good: /guides/typography
Good: /products/running-shoes
Bad:  /page?id=42&cat=3
Bad:  /Guides/Typography_Best_Practices
```

## Robots and Crawl Guidance in HTML

While `robots.txt` and sitemaps are server-side concerns, some crawl directives live in HTML and are a frontend responsibility.

### Meta Robots

Control how search engines index individual pages.

```html
<!-- Default (can be omitted): index this page and follow its links -->
<meta name="robots" content="index, follow">

<!-- Don't index this page but follow its links -->
<meta name="robots" content="noindex, follow">

<!-- Don't follow links on this page -->
<meta name="robots" content="index, nofollow">
```

**When to use `noindex`:**
- Thank-you pages after form submission
- Internal search results pages
- Paginated archive pages (page 2, 3, ...) — debatable, but common
- Staging or preview environments (better handled via HTTP headers or robots.txt)

### Link-Level Control

```html
<!-- Tell crawlers not to follow this specific link -->
<a href="/external" rel="nofollow">Sponsored link</a>

<!-- Mark user-generated content links -->
<a href="/user-link" rel="ugc">User comment link</a>

<!-- Mark sponsored/paid links -->
<a href="/sponsor" rel="sponsored">Our sponsor</a>
```

## Performance as SEO

Many performance optimisations are covered across other chapters. This is a cross-reference of the SEO-relevant techniques and where to find them.

| Technique | SEO Impact | Reference |
|-----------|-----------|-----------|
| Font preloading and `font-display` | Reduces LCP and CLS | [Typography route](route-typography.md) |
| `font-size-adjust` for fallback fonts | Reduces CLS during font swap | [Typography route](route-typography.md) |
| Responsive images with `srcset` | Reduces LCP on mobile | [Web Performance route](route-performance.md) |
| `aspect-ratio` on media | Prevents CLS | [Web Performance route](route-performance.md) |
| `loading="lazy"` for off-screen images | Reduces initial page weight | [Web Performance route](route-performance.md) |
| CSS-only animations (`transform`, `opacity`) | Improves INP | [Motion and Interaction route](route-motion.md) |
| Reduced motion preferences | Accessibility and performance | [Motion and Interaction route](route-motion.md) |
