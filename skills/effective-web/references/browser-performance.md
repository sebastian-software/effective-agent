# Browser Performance

Performance is measured browser behavior, not folklore. Every change should move a
specific metric — LCP, INP, CLS, transferred bytes, or time to first interaction —
and be verifiable in browser tooling or field data. Optimize the bottleneck the
measurement reveals, not the technique that is easiest to apply.

## Measure first, fix the bottleneck

- Establish the measured problem before changing anything: which Core Web Vital
  fails, on which page, on which device class and connection. Distinguish lab
  (Lighthouse, DevTools, WebPageTest, Playwright traces) from field data (CrUX,
  RUM, Search Console Core Web Vitals); ship decisions against field data where it
  exists, because lab numbers hide real device and network variance.
- Hold each Core Web Vital to its current "good" threshold, evaluated at the 75th
  percentile of real users: LCP at or below 2.5 s, INP at or below 200 ms, CLS at
  or below 0.1. A single fast local run is not proof; p75 must pass per device
  class (mobile and desktop) and per page type. Segment field data by geography,
  connection, and logged-in/out state where available, because an aggregate score
  hides the failing cohort.
- Treat Lighthouse as a diagnostic, not ground truth: it measures LCP and CLS in
  lab conditions but cannot measure real INP, because there is no real user input.
  Use Total Blocking Time (TBT) as the lab proxy for interaction cost and confirm
  INP against field data.
- Debug Core Web Vitals locally in the Chrome DevTools Performance panel. The
  standalone Web Vitals extension was retired in 2025 once its live-metrics and
  field-data workflow moved into DevTools; do not depend on it.
- Identify the actual LCP element from a trace before optimizing it. The LCP
  element is frequently not the element a developer assumes; guessing wastes
  effort on the wrong resource.
- Use `Server-Timing` headers or equivalent RUM instrumentation when a frontend
  symptom may originate from backend or rendering latency. Do not optimize the
  client for a slow document response.
- Budget the critical path: count render-blocking requests, their bytes, and
  their round trips. The first-paint cost is dominated by what must arrive and
  execute before the browser can render, not by total page weight.

## LCP and resource discovery

- Keep the LCP resource discoverable in the initial HTML response so the
  preload scanner finds it before the main parser blocks on scripts or CSS. The
  scanner is a separate lightweight parser that fetches resources early; it only
  sees URLs present in the served markup.
- Never lazy-load the LCP image or any above-the-fold image. `loading="lazy"`
  on the LCP element delays its request until layout, which directly inflates
  LCP. Apply `loading="lazy"` only to images below the fold.
- Do not hide startup-critical resources behind JavaScript, `data-src`, CSS
  background images, client-only rendering, or `@import` chains unless a
  deliberate `preload` plan compensates. Each of these is invisible to the
  preload scanner and defers discovery until later in the pipeline.
- Apply `fetchpriority="high"` to the single likely LCP image so the browser
  raises it above other images in the same fetch queue. Do not apply it broadly;
  multiple high-priority fetches compete with CSS, fonts, and scripts and cancel
  the benefit.
- Use `<link rel="preload">` only for a late-discovered critical resource (for
  example a hero image referenced from CSS, or a critical font). Preloading
  resources the scanner already finds, or preloading many resources, steals
  bandwidth from the critical path and regresses LCP.
- Establish early connections to required cross-origin hosts with
  `<link rel="preconnect">` for origins used immediately, and `dns-prefetch`
  for origins used later. Preconnect at most a few origins; each open connection
  has a cost.
- Avoid large base64 / inline data URIs for above-the-fold assets. They bloat the
  HTML the parser must process, cannot be cached separately, and delay discovery
  of everything after them.

## INP and main-thread responsiveness

- Treat INP as the responsiveness metric: it measures the latency from user input
  to the next paint across the worst interactions of a visit. Optimize input
  handlers, not just initial load.
- Decompose a slow interaction into its three parts before fixing it — input delay
  (main thread busy before the handler runs), processing duration (the handler
  itself), and presentation delay (layout and paint of the next frame) — and attack
  the dominant part. Idle-time and load-time main-thread work inflates input delay
  even when the handler is cheap.
- Break up long tasks. Any task over 50 ms blocks the main thread and delays
  input handling. Split work with `await scheduler.yield()` where supported, or
  yield via `setTimeout` / `postMessage`, so the browser can paint and process
  input between chunks.
- Move heavy, non-DOM computation off the main thread into a Web Worker. The main
  thread should be reserved for input handling, layout, and paint.
- Decouple visual feedback from expensive work: paint the input acknowledgement
  first, then run the heavy update in a subsequent frame. INP is measured to the
  next paint, so a fast visual response improves the metric even when total work
  is unchanged.
- Defer or remove third-party scripts that execute on the main thread during
  interaction. Load non-critical scripts with `defer` or `async`, and gate
  analytics and tag managers behind idle time.
- Use CSS `content-visibility: auto` with `contain-intrinsic-size` on large
  offscreen sections to skip their rendering work until they approach the
  viewport, reducing layout and paint cost.

## CLS and layout stability

- Reserve space for every element that arrives or resizes after first paint:
  images, video, ads, embeds, and injected widgets. Unreserved late content
  pushes layout and accumulates layout shift.
- Set explicit `width` and `height` (or a CSS `aspect-ratio`) on all media so the
  browser reserves the correct box before bytes arrive. Intrinsic sizing from
  dimension attributes prevents the reflow that dominates CLS.
- Reserve space with skeletons or fixed containers for asynchronously loaded
  widgets and data regions; a skeleton that matches the final box size prevents
  shift, a smaller placeholder does not.
- Never insert content above existing content unless it is space-reserved or a
  direct response to user interaction. Banners, cookie notices, and late hero
  content injected at the top are common CLS sources.
- Trigger layout-affecting animation with `transform`, not with properties that
  change box geometry (`top`, `height`, `margin`). Geometry changes force layout
  and can register as shift.

## Image delivery

- Choose format by content: AVIF first for photographic content (best
  compression), WebP as the widely supported fallback, and keep JPEG/PNG only for
  compatibility. Use SVG for icons, logos, and line art; it is resolution
  independent and usually smaller than a raster equivalent. Replace animated GIF
  with a muted, looping, autoplay `<video>` (H.264/AV1) — orders of magnitude
  smaller.
- Serve multiple sources with `<picture>` and `type` so the browser picks the
  best format it supports, and fall back gracefully.
- Match the delivered image to the rendered size and device pixel ratio with
  `srcset` (width descriptors) and an accurate `sizes` attribute. A `sizes` value
  that does not match the real layout across breakpoints makes the browser pick
  the wrong candidate and waste bytes.
- For below-the-fold images that already use `loading="lazy"`, consider
  `sizes="auto, <descriptive fallback>"`: supporting browsers can select from
  `srcset` using the computed layout size, while older browsers skip `auto` and
  use the remaining sizes list. Keep explicit `width` and `height` (or a stable
  aspect ratio) so deferred layout has reliable dimensions. Do not use this as
  a reason to lazy-load a hero or likely LCP image; those still need an accurate
  descriptive `sizes` value and early discovery.
- Use `<picture>` with media-conditioned `<source>` only for genuine art
  direction (different crop or aspect ratio per viewport). For pure
  resolution-switching, `srcset` + `sizes` on a single `<img>` is sufficient and
  simpler.
- Keep the responsive variant set pragmatic. Too few variants force oversized
  downloads; too many inflate storage, generation work, and CDN cache
  fragmentation. Pick breakpoints from the actual rendered widths in the layout.
- Automate encoding and variant generation through an image CDN or build pipeline
  (for example Sharp, or a CMS/framework image component) rather than hand-tuning
  files. Derive quality, format negotiation, and sizing from request context.
- Treat placeholder techniques — blur-up, BlurHash, LQIP, dominant-color, traced
  SVG — as perceived-performance tools applied *after* sizing, compression, cache
  behavior, and LCP discovery are correct. A placeholder that delays the real
  image's discovery makes loading slower, not faster. Keep the placeholder
  payload far smaller than the asset it stands in for.

## Fonts

- Set `font-display: swap` plus a metric-matched fallback font
  (`size-adjust`/`ascent-override`/`descent-override`); use `fallback` or
  `optional` when CLS is the measured problem. `swap` renders text immediately
  in the fallback and never blocks paint waiting for the web font — invisible
  text (FOIT) blocks LCP when the LCP element is text.
- `preload` only the one or two font files actually used for above-the-fold text,
  and only the formats actually served. Preloading every weight competes with the
  LCP image for bandwidth.
- Self-host fonts or `preconnect` to the font origin; a third-party font host adds
  connection setup to the critical path.
- Subset fonts to the glyphs the product uses and serve `woff2` (best
  compression, universal modern support). Ship only the weights and styles the
  design actually renders.
- Minimize layout shift from font swap by pairing the web font with a metrics-
  matched fallback using `size-adjust`, `ascent-override`, and
  `descent-override` in `@font-face`, so the fallback occupies nearly the same
  space as the final font.

## JavaScript and the main thread

- Ship less JavaScript before measuring anything else: parse, compile, and
  execution of script is the largest controllable main-thread cost on most pages.
- Split bundles at route and interaction boundaries with dynamic `import()` so the
  initial load ships only what first paint needs; load the rest on navigation or
  on first interaction with a feature.
- Audit and remove unused dependencies and dead code; a large utility pulled in
  for one helper inflates parse cost for every visit. Prefer platform APIs over
  libraries where the platform suffices.
- Hydrate selectively. For server-rendered pages, avoid hydrating static regions;
  defer or island-hydrate interactive components so the main thread is not blocked
  re-running the whole tree at load.
- Do not adopt a single client architecture (a specific state library, an
  all-in-one framework) as mandatory. Choose the rendering and state approach from
  the measured bottleneck, not from habit.

## Network and caching

- Set cache lifetimes deliberately per resource class. Fingerprinted static assets
  (hashed filenames) should be `Cache-Control: public, max-age=31536000,
  immutable`; HTML and frequently changing data need short or revalidated
  lifetimes.
- Use `stale-while-revalidate` only where the product tolerates briefly serving
  stale content: it improves perceived speed by returning a cached response
  immediately while revalidating in the background. It is a caching/freshness
  tradeoff, never a correctness or security mechanism — do not apply it to
  authenticated, transactional, or per-user-sensitive responses.
- Distinguish CDN edge caching from browser caching and set both intentionally;
  an asset cached at the edge but `no-store` in the browser still pays a round
  trip on every navigation.
- Serve over HTTP/2 or HTTP/3 so multiple resources share a connection without
  head-of-line blocking; this changes the cost model — many small cacheable files
  can beat one large bundle that invalidates wholesale.
- Compress text responses with Brotli (better ratio than gzip) and serve
  pre-compressed static assets where possible.

## Navigation, bfcache, and speculative loading

- Keep pages eligible for the back/forward cache (bfcache) so back navigation is
  instant. Do not use `unload` handlers (use `pagehide`/`visibilitychange`
  instead), and avoid `Cache-Control: no-store` on the document, which evicts the
  page from bfcache.
- Speculatively prefetch or prerender likely next navigations with the
  Speculation Rules API (`<script type="speculationrules">`), tuned to `moderate`
  or `conservative` eagerness so it does not waste bandwidth on unlikely paths.
  Prefetch loads the document; prerender renders it for an instant transition.
- Restrict prefetch/prerender to same-site, idempotent GET navigations the user is
  likely to take. Never speculatively load destinations with side effects.
- Annotate the LCP image and critical scripts on prerendered pages the same way as
  on the live page; a prerender that still lazy-loads its hero gains nothing.

## Perceived loading and interaction latency

- Show immediate local feedback for every interaction. Perceived speed is driven
  by the time to the first visible response, which can be far shorter than time to
  completion.
- For interaction-heavy tools, reduce real and perceived latency with local reads,
  optimistic writes, durable retry queues, and narrowly subscribed UI updates
  before chasing micro-optimizations. Local-first data and an IndexedDB-backed
  initial load remove the network from the critical interaction path.
- Scope live updates to the components and fields that changed. A broadly
  subscribed update that re-renders a whole list or page on every change is a
  common, invisible INP regression.
- Treat path length as part of perceived performance: keep high-frequency
  workflows keyboard-accessible and command-driven where appropriate, without
  hiding the mouse/touch alternative.
- Animate only when motion clarifies state change or spatial origin. Prefer
  `transform` and `opacity`, keep durations short (150–250 ms for UI feedback),
  and avoid layout-triggering properties in dense or long-list surfaces. Honor
  `prefers-reduced-motion`.

## Review checklist

- Is the failing metric and the offending element known from measurement (lab and,
  where available, field), not guessed, and judged against the p75 "good"
  thresholds (LCP 2.5 s, INP 200 ms, CLS 0.1) rather than one local run?
- Is the LCP resource present in the initial HTML, correctly sized, not
  lazy-loaded, and prioritized with `fetchpriority="high"` only where warranted?
- Do `srcset` and `sizes` match the real rendered widths across breakpoints, and
  are formats negotiated (AVIF/WebP) with a fallback?
- Are explicit dimensions or `aspect-ratio` set on all media, and is space
  reserved for late widgets, ads, and injected content?
- Do fonts use `font-display`, a metrics-matched fallback, subset `woff2`, and
  preload limited to above-the-fold faces?
- Are long tasks broken up, heavy work moved off the main thread or deferred, and
  third-party scripts kept off the interaction path?
- Are cache lifetimes set per resource class, with `immutable` for fingerprinted
  assets and `stale-while-revalidate` only on tolerant, non-sensitive responses?
- Is the page bfcache-eligible (no `unload`, no `no-store` on the document), and
  are likely navigations speculatively loaded with bounded eagerness?
- Do interaction-heavy flows give immediate local feedback, with updates scoped to
  changed fields rather than broad re-renders?
- Is animation limited to composited properties, honoring `prefers-reduced-motion`?
- Is the change verified with before/after evidence from browser tooling or field
  metrics?
