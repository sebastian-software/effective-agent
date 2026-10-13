# Web Performance

Use this route for browser-facing performance work where implementation choices
affect loading, rendering, network discovery, perceived speed, Core Web Vitals,
or sustained animation and media runtime cost.

## Workflow

1. Identify the measured problem first: LCP, CLS, INP, blocking resources,
   image bytes, caching, resource discovery, perceived loading state, dropped
   frames, sustained CPU or GPU use, memory growth, or lifecycle leaks.
2. Inspect the app stack, rendering mode, image pipeline, CDN/cache behavior,
   framework defaults, animation execution models, and current measurement tools.
3. Apply the narrowest useful fix: image markup, preload/resource discovery,
   cache freshness, layout reservation, dynamic import boundaries, font
   loading, interaction work, or lifecycle-local animation control.
4. Verify with local browser tools and project checks. Prefer measured before/after evidence over theoretical optimization.
5. Explain tradeoffs: freshness vs cache reuse, bytes vs variants, above-the-fold priority vs preload overuse, visual polish vs rendering stability.

## Reference Files

- [browser-performance.md](browser-performance.md) - Browser performance rules for images, LCP, preload behavior, caching, and perceived loading.
- [animation-runtime-performance.md](animation-runtime-performance.md) -
  browser baselines, offscreen work, RAF and canvas loops, cleanup, route
  cycles, and honest before/after claims.

## Boundaries

Do not use this route as a marketing SEO audit. Cross-reference SEO only when performance affects crawlable content, Core Web Vitals, metadata delivery, or social/media assets.

Do not treat security headers as performance work unless transport, caching, or policy choices directly affect loading behavior.
