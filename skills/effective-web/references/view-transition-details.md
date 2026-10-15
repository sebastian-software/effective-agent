# View Transition Details

Use for snapshot identity, clipping, layering, input, or destination-readiness
problems. Ordinary state transitions do not need this machinery. The underlying
DOM update or navigation must work without snapshots and under reduced motion.

## Match identity, not appearance

For same-document changes, wrap the actual DOM update in
`document.startViewTransition(updateCallback)`. For cross-document navigation,
both same-origin documents opt in with `@view-transition { navigation: auto; }`.
Client-side routing usually needs the same-document integration even when the
URL changes. See [the API workflow](https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API/Using).

Give each conceptual item a unique `view-transition-name` within each captured
state; its old and new representations share that name. A `view-transition-class`
groups styles and does not provide identity. Where supported, `match-element`
can generate identity for a continuing element, but is not a shared name joining
different DOM elements or documents. Verify exact features instead of inferring
all capabilities from the presence of `document.startViewTransition`.

Same-document transitions are Baseline 2025; cross-document support remains
Chromium and Safari as of October 2026. Keep normal navigation and an instant
update path. For reduced motion, prefer skipping capture and applying the change
directly, or explicitly substitute a brief non-spatial response. Suppress
generated movement and account for the default crossfade rather than assuming
that disabling a custom animation removes every effect.

## Keep geometry and custom movement separate

The group pseudo-element owns generated position and size animation. Put an
additional enter/exit transform on `::view-transition-old()`,
`::view-transition-new()`, or a suitable image-pair layer instead of replacing
the group's placement transform. Additive composition is another deliberate
option; preserve operation order and verify the actual result.

An independently captured child is painted outside its former DOM ancestry.
Ancestor clipping, radii, or blending may no longer produce the expected image.
Capture the whole clipped unit when that is sufficient, or use supported nested
transition grouping and explicitly restore the required clipping. Keep ordinary
DOM selectors separate from newer pseudo-element selectors so an unsupported
selector cannot discard the static clipping rule.

Changing aspect ratios or text wrapping can distort a snapshot crossfade.
Prefer a regular property transition when it solves the problem, or separate
the image and text treatments. Generated group animations can interpolate
width/height and contend on the main thread; profile before replacing them
with measured transform-based FLIP motion. See the
[rendering model](https://drafts.csswg.org/css-view-transitions-1/).

## Test input while the pixels move

A document-scoped transition overlay can intercept input. Giving that overlay
`pointer-events: none` does not by itself restore hit testing to an element
captured away from its ordinary DOM position. Test pointer and keyboard paths
separately; accessibility-tree presence is not proof of pointer reachability.

Keep frequently used controls outside capture when practical. If a real control
needs a decorative traveling duplicate, keep one semantic button and hide the
duplicate from interaction and assistive technology. Do not reverse DOM reading
order to repair visual stacking; set the intended layer order explicitly.

Keep transitions short and test scroll during capture, top-layer controls,
rapid repeated input, and changing focus. A second transition on the same root
skips the active transition rather than carrying a physical spring's velocity.
Define whether the interface skips, retargets through another mechanism, or
uses live-element layout motion when interruption quality is central.

Retain the returned `ViewTransition`: `ready` exposes the captured pseudo-tree,
`updateCallbackDone` signals update completion, and `finished` supports cleanup.
Handle skipped transitions and rejected readiness without losing the actual
state change. A framework may queue updates differently; use its documented
commit integration rather than treating a scheduled React update as painted DOM.

## Make destination content ready deliberately

For cross-document shared images, ensure the destination element and asset are
ready for capture using an appropriate preload or prerender strategy. An image
that arrives after capture cannot participate retroactively. `blocking="render"`
can wait for parsing, not for image bytes; measure its Core Web Vitals cost
before adopting render blocking.

Use element-scoped transitions when preserving unrelated page interaction or
concurrent component changes warrants them. As of October 2026, this remains a
single-engine feature (Chrome 147+); detect the exact element API and retain
a complete document-scoped or instant fallback. Nested-group behavior also
needs its own detection rather than a generic API-presence check.
