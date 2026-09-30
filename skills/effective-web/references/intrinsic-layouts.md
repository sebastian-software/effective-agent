# Intrinsic Layout Algorithms

Use this reference to choose and compose small layout primitives that adapt to
their content and container before adding viewport breakpoints or bespoke
component CSS. Use the executable
[composition examples](../examples/layout-composition.html) to inspect these
relationships with variable content and container widths.

## Contents

- [Operating Model](#operating-model)
- [Choose the Smallest Primitive](#choose-the-smallest-primitive)
- [Outer Grids and Layout Slots](#outer-grids-and-layout-slots)
- [Core Implementations](#core-implementations)
- [Shared Tracks and Reading Regions](#shared-tracks-and-reading-regions)
- [Composition and API Rules](#composition-and-api-rules)
- [Container Queries](#container-queries)
- [Accessibility and Resilience](#accessibility-and-resilience)
- [Verification](#verification)

## Operating Model

- Treat layout as relationships among boxes, not as fixed screenshots. Let
  content and available space determine dimensions; supply bounds, preferences,
  and thresholds instead of prescribing width and height.
- Compose primitives with one stable responsibility instead of namespacing all
  geometry beneath a finished component such as `.dialog` or `.card`.
- Keep HTML semantics independent from layout. A Stack may be a `section`,
  list, form, or generic wrapper; choose the element from meaning first.
- Prefer intrinsic reconfiguration through wrapping, flexible sizing,
  `minmax()`, and overflow. Add a container query only when the required change
  cannot be expressed intrinsically. Use a viewport query only for a genuinely
  viewport-owned decision.
- Preserve the simplest suitable formatting context. Do not turn document flow
  into Flexbox merely to obtain spacing; the parent-scoped Owl is often the
  smaller and more faithful Stack algorithm.
- Use logical properties and relative units. Default boxes to
  `box-sizing: border-box`; opt a measured Center into `content-box` only when
  its padding must sit outside the readable measure.
- Encode system-wide tolerances as custom properties such as `--measure`,
  `--space`, `--item-min`, and `--threshold`. Keep the full spacing-scale and
  measure guidance in [layout foundations](layout-foundations.md).
- Implement the algorithm in the project's native component model. Custom
  elements are optional; the value lies in the layout contract, not the wrapper
  technology.

## Choose the Smallest Primitive

| Need | Primitive | Stable responsibility |
| --- | --- | --- |
| Vertical flow with owned sibling rhythm | Stack | Use `gap` in a Flex/Grid composition or the Owl in normal block flow; nest another Stack for another rhythm. |
| Symmetric inset and visible grouping | Box | Apply even padding and, when useful, a border or background without deciding external placement. |
| Bounded readable column | Center | Cap inline measure, center the column, and retain minimum inline gutters. |
| Wrapping inline group | Cluster | Arrange variable-width peers such as actions, tags, or navigation with wrapping and gap. |
| Narrow region beside flexible content | Sidebar | Keep one side intrinsic or preferred-width while the main region owns the remainder; stack both when the main region would stop being dominant. |
| Equal peers that must be all-row or all-column | Switcher | Cross one container-based threshold without leaving a cramped intermediate row; optionally cap the supported item count. |
| Principal content between optional top and bottom regions | Cover | Center one child in the available block space while tolerating missing header or footer content. |
| Repeated minimum-size cells | Grid | Add as many tracks as fit while preventing a minimum track from overflowing a narrow container. |
| Media or content at a fixed ratio | Frame | Reserve an aspect ratio and deliberately crop or contain its direct child. |
| Single-row horizontal browsing | Reel | Use native overflow for a discoverable horizontal sequence instead of making JavaScript the scrolling mechanism. |
| Deliberate superimposition | Imposter | Center and bound an overlay inside a positioned ancestor or the viewport; do not use it for ordinary flow. |
| Text-relative inline graphic | Icon | Let an SVG inherit color and scale with nearby text while preserving a reliable accessible name. |
| A component needs explicit size-dependent modes | Container | Establish the nearest or a named inline-size query context; this is a meta-layout utility, not a visual primitive. |

Do not force a named primitive when normal document flow or one declaration is
already sufficient. Likewise, split a primitive when options give it multiple
unrelated jobs or consumers require chains of undo rules.

## Outer Grids and Layout Slots

Build the outer grid before polishing inner components. Outline the page or
section's meaningful boxes, preserve their semantic source order, and make a
small structural prototype that proves the main tracks, wrapping, reordering,
and overlap at continuous widths.

Treat a layout slot as a structural region, not necessarily a framework slot or
Web Component `<slot>`. Give each region a small contract:

- required and optional content;
- minimum, preferred, and maximum useful size;
- placement and mode conditions;
- source, reading, and focus order;
- overflow, absence, and excessive-content behavior.

Keep reusable component markup stable when the same object appears in a hero,
rail, grid, or compact list. Let the host Grid, Flex, or Flow composition own
external placement. Let the component respond internally to its available
space with intrinsic behavior and, when necessary, a container query. When
presentation intent belongs to the host but cannot be inferred from space or
content, expose it on that host through a semantic context hook such as an
inherited custom property or scoped data attribute. Do not pass `featured`,
`compact`, or `hero` props merely to mirror placement. Expose component state
only when the content, interaction, or product meaning actually changes.

Test the structural prototype with representative semantics before adding
decorative details. Include absent optional content, one and many items, long
labels, different media ratios, and a deliberately awkward intermediate width.
If the skeleton already needs repeated resets or DOM duplication, revise the
slot contract or source structure before building the finished component.

## Core Implementations

These are starting contracts, not mandatory class names.

```css
.stack {
  display: flex;
  flex-direction: column;
  gap: var(--space, 1rem);
}

.flow-stack > * {
  margin-block: 0;
}

.flow-stack > * + * {
  margin-block-start: var(--space, 1rem);
}

.box {
  padding: var(--box-space, var(--space, 1rem));
  outline: 0.125rem solid transparent;
  outline-offset: -0.125rem;
}

.center {
  box-sizing: content-box;
  max-inline-size: var(--measure, 60ch);
  margin-inline: auto;
  padding-inline: var(--gutter, 1rem);
}

.cluster {
  display: flex;
  flex-wrap: wrap;
  align-items: var(--cluster-align, center);
  justify-content: var(--cluster-justify, flex-start);
  gap: var(--space, 1rem);
}
```

Both Stack implementations preserve the durable rule: the parent context owns
the relationship and reusable children do not ship default outer margins.
Choose `gap` when Flex/Grid behavior is already required. Choose the Owl when
heterogeneous content should keep normal block formatting. Keep the direct-child
form by default; recursive `.flow-stack * + *` spacing is powerful but can
unexpectedly spread nested lists, forms, and prose. Use nested variants for
different rhythms and keep `margin: auto` for free-space alignment.

Keep Box padding symmetric or absent at the primitive level; asymmetric inset
usually belongs to a more specific composition. Keep Center responsible for the
column's measure and gutters. Centering every child intrinsically is a separate
option that must survive zoom without moving content outside the viewport.

```css
.with-sidebar {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space, 1rem);
}

.with-sidebar > * {
  min-inline-size: 0;
  max-inline-size: 100%;
}

.with-sidebar > .sidebar-rail {
  flex-basis: var(--sidebar-size, 18rem);
  flex-grow: 1;
}

.with-sidebar > .sidebar-main {
  flex-basis: 0;
  flex-grow: 999;
  min-inline-size: var(--content-min, 50%);
}

.switcher {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space, 1rem);
}

.switcher > * {
  min-inline-size: 0;
  flex-basis: calc((var(--threshold, 30rem) - 100%) * 999);
  flex-grow: 1;
  max-inline-size: 100%;
}

.switcher > :nth-last-child(n + 5),
.switcher > :nth-last-child(n + 5) ~ * {
  flex-basis: 100%;
}
```

Use Sidebar when one region should remain meaningfully narrower. Use Switcher
when the children are peers and partial wrapping would imply a false hierarchy.
Change the quantity selector to the documented maximum the composition can
support; do not hide or drop excess content.

Sidebar expects two regions with explicit rail/main roles, so either can come
first in semantic source order. With a zero main basis and a large growth
factor, the main takes almost all spare space; its minimum share decides when
both regions must stack. A plain `3:1` growth ratio with two preferred bases is
a different contract and does not guarantee that minimum share.

Switcher multiplies the difference between its threshold and container width
by a large factor. Above the threshold a negative basis clamps to zero, so
peers share the row; below it a large positive basis makes them stack. `999`
is a steep transition, not a mathematical discontinuity. Choose the threshold
so the supported count, gaps, and real content fit in row mode; check the narrow
transition band and automatic minimum sizes. Five or more children stack in
this example. Allow long text to wrap and bound controls/media separately;
`min-inline-size: 0` alone does not make oversized content fit.

```css
.cover {
  display: flex;
  flex-direction: column;
  min-block-size: var(--cover-min, 100vh);
  padding: var(--cover-space, 1rem);
  gap: var(--space, 1rem);
}

.cover > [data-principal] {
  margin-block: auto;
}

.grid {
  display: grid;
  grid-template-columns:
    repeat(auto-fit, minmax(min(var(--item-min, 16rem), 100%), 1fr));
  gap: var(--space, 1rem);
}

.frame {
  aspect-ratio: var(--frame-ratio, 16 / 9);
  overflow: hidden;
}

.frame > :is(img, video) {
  inline-size: 100%;
  block-size: 100%;
  object-fit: var(--frame-fit, cover);
  object-position: var(--frame-position, 50% 50%);
}
```

Select the Cover's principal child explicitly; do not couple the algorithm to a
heading level. For a viewport Cover, use the project's supported small or
dynamic viewport unit when browser chrome must be accounted for instead of
assuming `100vh` always equals the visible area. Supply real image `width` and
`height` attributes as well as the Frame ratio when the browser must reserve
loading space. Prefer real content images with alternatives over inaccessible
background images.

Use `auto-fit` when empty Grid tracks should collapse and present items should
stretch into the available row. Use `auto-fill` only when retaining the empty
track scaffold is intentional. A shared Grid that needs consumer-specific query
chains or undo rules no longer has one stable responsibility.

```css
.reel {
  display: flex;
  overflow-x: auto;
  gap: var(--space, 1rem);
  scrollbar-gutter: stable;
}

.reel > * {
  flex: 0 0 var(--reel-item-size, auto);
}

.imposter {
  position: var(--imposter-position, absolute);
  inset: 0;
  display: grid;
  grid-template: minmax(0, 1fr) / minmax(0, 1fr);
  place-items: center;
  box-sizing: border-box;
  padding: var(--imposter-gap, 1rem);
}

.imposter > * {
  min-inline-size: 0;
  min-block-size: 0;
  max-inline-size: 100%;
  max-block-size: 100%;
  overflow: auto;
}

.icon {
  inline-size: 0.75em;
  block-size: 0.75em;
  inline-size: 1cap;
  block-size: 1cap;
  fill: currentColor;
  flex: none;
}
```

Keep a Reel's native scrolling as the baseline. Optional controls may advance
the scroll position, but must not become the only way to reach content. Use a
partly visible next item, visible scrollbar, edge treatment, or concise cue to
make overflow discoverable.

Use Imposter only where overlap is intentional. This implementation uses one
content child inside an inset alignment layer; an absolute layer requires a
positioned ancestor with a useful block size. Grid alignment avoids mixing
logical offsets with physical translation, which would miscenter in RTL or
vertical writing. Bound and scroll oversized content within that region.
For an interactive modal, prefer the native dialog/top-layer mechanism and load the
[dialog guidance](dialog-foundation.md); positioning alone does not provide focus
movement, containment, dismissal, background inertness, or an accessible name.
Let source order determine overlapping layers where it remains semantically
correct; add `z-index` only when the intended layer order genuinely differs.
Avoid escalating arbitrary `z-index` values as a substitute for understanding
the positioning context.

For an Icon authored inline with text, an ordinary word space is a legitimate
default: it scales with the font, follows `dir`, and collapses when the label is
absent. Preserve that simple behavior unless the component requires token-exact
spacing. In that case use an `inline-flex` wrapper with `gap`, keep the SVG
decorative when the surrounding control supplies the name, and verify the
icon-only state explicitly.

## Shared Tracks and Reading Regions

Use Subgrid when repeated items need corresponding content slots to align
across a row. Keep an independent nested-Grid baseline:

```css
.product-card {
  display: grid;
  grid-template-rows: auto 1fr auto;
  gap: 0.75rem;
  min-inline-size: 0;
}

@supports (grid-template-rows: subgrid) {
  .product-card {
    grid-row: span 3;
    grid-template-rows: subgrid;
  }
}
```

The card's three direct slots are its heading, body, and actions. Optional media
belongs inside the body, so removing it does not change the row-span contract.
Without Subgrid, each card still lays out these slots independently. With
Subgrid, cards in the same visual row share their slot heights. Do not subgrid
an unbounded set of children without a track-capacity contract: the subgridded
axis cannot create its own implicit tracks.

An outer Grid can constrain prose while allowing selected media to occupy the
full region. This avoids viewport-width escape math and preserves source order.

```css
.article-layout {
  display: grid;
  grid-template-columns:
    [wide-start] minmax(1rem, 1fr)
    [text-start] minmax(0, 65ch)
    [text-end] minmax(1rem, 1fr) [wide-end];
  row-gap: 1.25rem;
}

.article-layout > * {
  grid-column: text-start / text-end;
  min-inline-size: 0;
}

.article-layout > figure {
  grid-column: wide-start / wide-end;
  margin: 0;
}
```

Cap prose where it is actually read; avoid a universal `*` measure cap that also
constrains form controls, data regions, nested grids, and overlays. `ch` is a
font metric, not an exact character count. Check real and fallback fonts, text
zoom, and supported writing directions before choosing a final measure.

## Composition and API Rules

- Keep primitives content-agnostic and target direct children so a parent does
  not unexpectedly restyle nested compositions.
- Give each shared primitive a small contract with useful fallbacks. Expose
  behavior variables, not every underlying CSS property.
- Let components own internal layout only. Their parent composition owns
  external placement and sibling rhythm.
- Compose Box, Stack, Cluster, and a structural primitive rather than creating
  component-specific copies of the same geometry.
- Allow source order to remain meaningful. Visual reordering and overlap must
  not create a conflicting reading or focus order.
- Prefer global, low-specificity defaults for genuine axioms; use layout
  primitives for composition and narrow utilities for true exceptions. Do not
  generate a utility for every CSS declaration.
- Preserve content-based sizing. Fixed dimensions need a content, localization,
  and zoom contract; otherwise use `min-*`, `max-*`, `flex-basis`, and intrinsic
  sizes as tolerances.

## Container Queries

Establish the smallest useful query boundary:

```css
.component-region {
  container-type: inline-size;
}

@container (inline-size < 24rem) {
  .component-region__actions {
    /* Change only the behavior that truly needs an explicit mode. */
  }
}
```

- Prefer the nearest unnamed container. Name a container only when a descendant
  must query a non-nearest ancestor or multiple nested contexts would be
  ambiguous.
- Query the component's available space, not a duplicated viewport assumption.
- Establish containment on a stable owner; inline-size containment changes
  content-based sizing, so check shrink-to-fit contexts before adding it.
- Do not add empty query-only wrappers when the owning region can establish the
  container.
- Keep a coherent no-query baseline. A container query should finesse an
  already usable composition, not rescue hidden or inaccessible content.
- Change properties related to available space. Do not use size queries for
  arbitrary palette, typeface, or brand changes.

## Accessibility and Resilience

- Verify that zoom, larger default fonts, long translations, and user content
  change the layout without obscuring or truncating information.
- Keep Box boundaries perceivable in forced-colors mode; a transparent inset
  outline can preserve a boundary when background colors disappear.
- Give icon-only controls a durable localized name on the owning control and
  hide decorative SVGs from the accessibility tree. Do not rely on an SVG
  `title` being propagated as the control name.
- Keep horizontally scrolling regions one-dimensional and discoverable. Add a
  label and keyboard focus only when the region itself must be operated; if its
  children are focusable, focusing them should bring them into view.
- Do not treat Imposter as a dialog implementation. Load semantics, focus,
  Escape, close affordance, return focus, and inert-background behavior from
  the dedicated dialog guidance.
- Do not use `display: none` merely to make a layout variant fit; it removes
  content from layout and the accessibility tree.

## Verification

1. Resize the owning container continuously, including exactly at and one pixel
   to either side of each threshold; do not test only named device widths.
2. Test absent, minimum, expected, and excessive content plus short, long, and
   unbreakable values. Include dynamic insertion and removal when the UI
   supports it.
3. Remove optional media and vary its aspect ratio, intrinsic size, crop, and
   loading state without changing the component's meaning or reachability.
4. Test narrow, wide, short, and tall containers plus browser zoom and larger
   default text. Confirm readable measure and that no fixed dimension clips
   content.
5. Test translated text, RTL, and the supported writing modes. Confirm logical
   spacing, ordering, scrolling, and centering.
6. Test keyboard focus, visible focus, source order, selection, hash targets,
   and scroll reachability wherever overlap or overflow is involved.
7. Test forced colors and missing images/media. Confirm Box boundaries, Icon
   meaning, and Frame fallbacks remain understandable.
8. Remove JavaScript and optional support-gated enhancements. The intrinsic core
   must still expose all content and core actions.
9. Inspect the API after real use. Split a primitive that accumulates unrelated
   modes, consumer-specific selectors, or repeated undo rules.

The [composition fixture](../examples/layout-composition.html) includes a
Subgrid catalog, a Sidebar checkout, a Switcher comparison, and a reading grid
with wider media. Its controls vary container width, root font size, direction,
item count, and media presence. Check actual browser zoom and the target
project's supported engines separately.

Technical contracts: [CSS Flexbox](https://www.w3.org/TR/css-flexbox-1/),
[CSS Grid](https://www.w3.org/TR/css-grid-2/),
[Subgrid](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout/Subgrid),
and [CSS Containment](https://www.w3.org/TR/css-contain-3/).
