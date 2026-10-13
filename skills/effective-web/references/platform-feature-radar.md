# Web-Platform Feature Radar

This is a dated discovery aid for models whose knowledge may predate the current
web platform. Snapshot date: **2026-10-14**. Before shipping, verify each lead
against current Baseline/MDN data and the project's support target; status can
only move forward after this snapshot.

## Promote: recently Newly available

Propose these when they remove brittle workarounds or improve the result. State
that they target current browser versions and preserve a coherent older-browser
path when the project supports older devices, WebViews, or enterprise browsers.

- **CSS Anchor Positioning:** the core subset (`anchor-name`, `position-area`,
  `anchor()`, `anchor-size()`, `anchor-scope`, `@position-try`) became
  interoperable in January 2026 and can replace JavaScript geometry for many
  anchored overlays. The feature family is still Limited availability overall:
  BCD marks `position-anchor` complete in Chrome 151+, Firefox 151+, and Safari
  27+ (earlier versions use the wrong initial value), while the
  `position-visibility` keywords `anchor-valid`/`anchor-visible` ship only in
  Safari 27 — so verify current support per property, not per family. Keep trigger
  semantics, top-layer behavior, dismissal, focus, and collision testing as
  separate responsibilities.
- **`:open`:** style the open state of `details`, `dialog`, picker-bearing
  `select`, and supported `input` controls without mirrored classes. A missing
  style must not hide the actual open/closed state.
- **Container style and name-only queries:** let components respond to inherited
  custom-property context or named containment without variant prop plumbing.
  Keep a normal cascade/default style outside the query.
- **`contrast-color()`:** choose the higher-contrast black or white foreground
  from a dynamic background without duplicating color-selection logic. It became
  Baseline Newly available in April 2026, but it is not a perceptual-accessibility
  guarantee: keep a declared fallback for older targets and verify the resulting
  pair, especially on mid-tone backgrounds.
- **`field-sizing: content`:** allow text inputs and textareas to grow with
  content without JavaScript measurement. Bound inline/block size, test empty
  values and placeholders, and preserve manual resizing where users need it.
- **`shape()`:** author responsive `clip-path` and `offset-path` geometry with
  readable commands and CSS math instead of fixed SVG path strings when that
  improves maintainability.
- **Typed/active View Transitions and `animation-composition`:** distinguish
  transition classes and combine effects without ad hoc animation bookkeeping.
  Treat motion as optional and keep navigation/state correct without it.
  (`animation-composition` itself is older — Baseline 2023, widely available
  since January 2026.)
- **Custom Highlights:** style ranges such as search matches or diagnostics
  without wrapping and mutating document text nodes. Do not rely on highlight
  color alone to convey state.
- **`ToggleEvent.source`:** identify the invoker that changed a popover's state
  instead of maintaining duplicate trigger state where the native event fits.
- **`ariaNotify()`:** became Baseline Newly available in September 2026 (Safari
  27 was last). Prefer native semantics, state, and live content first; use it
  only for announcements not already conveyed by the DOM, coalesce messages,
  localize them, and retain a tested live-region fallback for older targets
  where announcements are essential. VoiceOver can drop announcements that
  collide with other speech events.
- **Tree-counting functions:** [`sibling-index()`](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/sibling-index)
  and `sibling-count()` became Baseline Newly available in August 2026
  (Firefox 154 was last). They can simplify position-based calculations and
  staggered effects, but keep a readable fallback for older targets and do not
  replace semantic order or explicit application data with DOM-position
  inference.
- **Invoker commands (`command`/`commandfor`):** Baseline 2025, Newly available
  since December 2025. Let a `button` open, close, or toggle a dialog or popover
  without glue JavaScript; keep the same actions reachable through ordinary
  controls for older targets.

## Prefer as established defaults

These reached Baseline Widely available by 2026 and should no longer be rejected
merely as "too new" when the project has no older-browser exception:

- CSS subgrid for aligning nested content to parent tracks.
- `:user-invalid` for post-interaction form styling instead of showing errors on
  initial load.
- `clip-path` for bounded clipping, with semantic content left intact.
- `image-set()` for resolution- or format-aware CSS images.
- `contain-intrinsic-size` with containment/content visibility to reserve space.
- `lh` and `rlh` units for line-height-relative rhythm.
- `hyphens` and `hyphenate-character` for language-aware text layout, with the
  correct `lang` and locale review.

## Watch, demonstrate, or project-gate

Release notes are discovery feeds, not support policy. As of this snapshot:

- Customizable `select` ships in Chrome 135+ and Safari 27 but not Firefox, so
  it remains Limited availability. Use it as an enhancement over complete text options, not as the
  only usable control.
- `sizes="auto"` can let a lazy-loaded responsive image use its computed layout
  size when selecting from `srcset`. Use `sizes="auto, <legacy sizes>"` so an
  older browser can continue with the descriptive fallback, retain explicit
  dimensions/aspect ratio, and never lazy-load an LCP or above-the-fold image.
- Anchor Positioning level 2 anchored container queries (`container-type:
  anchored`, `@container anchored(...)`) and `border-shape` remain distinct,
  limited subfeatures. Do not infer their support from base Anchor Positioning
  or from the Baseline status of `shape()`; prefer interoperable position
  fallbacks such as `flip-block` where they meet the design.
- Element-scoped View Transitions (`Element.startViewTransition()`) ship in
  Chrome 147 at this snapshot and remain single-engine. Use them only as a
  feature-detected enhancement when a subtree transition should leave the rest
  of the page interactive, preserve external top-layer ordering, or allow
  concurrent or nested transitions. Do not infer support from
  `Document.startViewTransition()`; retain a document-scoped or instant path.
- Browser-generated carousel controls and markers such as
  [`::scroll-button()`](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/::scroll-button),
  `::scroll-marker`, and `:target-current` remain Limited availability. Keep a
  native overflow/scroll-snap baseline with clear reachability, then add them as
  a feature-detected enhancement and re-test keyboard, focus, names, disabled
  states, touch, reduced motion, and screen readers instead of assuming the
  generated accessibility model is sufficient.
- `closedby`, CSS `random()`, `text-fit`, gap
  decorations, Grid Lanes, `corner-shape`, and other newly shipped primitives
  require a fresh feature-level support check; do not inherit the Baseline badge
  of their containing element or related feature family.
- Beta, flag-only, single-engine, and specification proposals may inspire an
  architecture, demo, or test. They must not become an unconditional shared
  component default.

## Refresh workflow

1. Check the current Baseline year page and the latest monthly platform update.
2. Verify the exact subfeature on MDN; families often contain members with
   different support status.
3. Compare the product's Baseline/Browserslist target and real audience data.
4. Classify the feature as default, promoted progressive enhancement,
   project-gated, or watch-only.
5. Update this snapshot when a status change would alter agent decisions.
