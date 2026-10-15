# SVG Graphics

Build SVG as semantic, scalable interface content rather than opaque path data.
Choose its delivery, coordinate system, accessibility contract, styling surface,
and motion model deliberately.

## Delivery

- Choose CSS geometry for simple, parameterized shapes when the rules remain
  shorter and clearer than an asset. Prefer an exported SVG when CSS recreation
  would require opaque clipping, gradients, pseudo-elements, or hours of tuning.
  Prototype borderline cases and compare maintenance cost, not technical novelty.
- Use `<img src="…svg" alt="…">` for static, cacheable graphics whose internal
  nodes do not need CSS or JavaScript. It behaves like other replaced images and
  keeps the SVG out of the document DOM.
- Use inline `<svg>` when internal shapes need `currentColor`, theme tokens,
  state styling, animation, internal DOM access, or per-instance labels.
- Use an icon component or an intentional `<symbol>`/`<use>` sprite when many
  instances share geometry. Verify styling, accessible naming, external-resource
  policy, and duplicate-ID behavior before standardizing the system.
- Reuse one path definition for a background track and a drawn foreground
  instead of copying long geometry. Keep clone-specific paint inheritable;
  `<use>` is not a general merge-and-override mechanism for template geometry.
- Do not inline large static illustrations by default. Repetition bloats HTML,
  delays parsing, and forfeits independent asset caching.

## Coordinate System and Sizing

- Preserve a correct `viewBox="min-x min-y width height"`. It selects and scales
  an internal coordinate region; CSS `width`/`height` or intrinsic dimensions
  control the rendered box.
- Give content images intrinsic `width` and `height` attributes to reserve their
  aspect ratio, then constrain them responsively with `max-inline-size: 100%` and
  `block-size: auto` where appropriate.
- Keep the artwork inside its viewBox with intentional optical padding. Fix
  off-center icon geometry at the source before compensating with arbitrary CSS.
- Collaborate on asset boundaries. Well-prepared SVG parts with intentional
  intrinsic geometry, viewBoxes, and grouping can remove breakpoint logic and
  absolute-positioning compensation from the consuming component.
- Set `preserveAspectRatio` deliberately when the artwork should crop, meet, or
  stretch inside a differently shaped viewport. Do not accept clipping or
  distortion as an accidental default.
- Use `vector-effect="non-scaling-stroke"` only when stroke weight should remain
  visually constant while geometry scales; ordinary icons usually benefit from
  strokes scaling with the artwork.
- Test icons at the smallest size they actually render. Prefer the icon set's
  native 16, 20, or 24px grid over fractional scaling that softens strokes, and
  simplify artwork whose counters or interior lines collapse at that size.

## Shapes and Paths

- Prefer `<circle>`, `<rect>`, `<line>`, `<polyline>`, and `<polygon>` when they
  express the geometry. Use `<path>` for curves, arcs, or compound forms that
  simpler shapes cannot represent cleanly.
- Format authored path commands with useful whitespace and line breaks. Optimize
  bytes in the build pipeline; do not sacrifice maintainability for negligible
  pre-compression savings.
- Treat uppercase commands as absolute coordinates and lowercase commands as
  offsets from the previous point. Remember that most drawing commands inherit
  their starting point from the command before them.
- Normalize progress-based stroke effects with `pathLength="100"` when useful,
  then express dash lengths and offsets in that shared scale instead of measuring
  each path in JavaScript.
- For a self-drawing line, offset a full-length dash and animate the offset to
  zero. Growing a zero-length dash can leave a visible dot with round caps.
  Keep dash values numeric in the normalized scale; percentage dash values are
  not percentages of path length. See [pathLength](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/pathLength).
- Morph only between compatible path topologies, and verify the target browser
  set. If morphing is decorative, allow unsupported browsers to keep the static
  start or end state; add a library only when broad morphing support is required.

## Styling and Accessibility

- Use `fill="currentColor"` or `stroke="currentColor"` for monochrome icons and
  semantic custom properties for multi-color graphics. Keep component state on
  the containing control and let the SVG inherit it.
- Match an icon's optical weight to adjacent text without rewriting a coherent
  icon family ad hoc. Use a supported stroke variant when the family provides
  one; otherwise preserve its native stroke and adjust size, color, or emphasis.
  Verify the pair at its real rendered size rather than deriving a universal
  stroke width from font weight alone.
- Reuse one geometry asset across ordinary color states and let `currentColor`
  inherit hover, focus, disabled, and selected treatment. When the icon family
  provides a deliberate outline/filled pair, a filled selected state can add a
  useful cue; it must remain consistent across the surface and cannot be the
  only indication of state.
- Hide decorative inline SVG with `aria-hidden="true"`. For decorative `<img>`,
  use `alt=""`; do not repeat adjacent visible text through the accessibility tree.
- Name an informative inline SVG with `role="img"` and `aria-labelledby` pointing
  to a concise `<title>` and, when needed, `<desc>`. Prefer existing visible text
  as the label when it already describes the graphic. Generate unique title,
  description, gradient, mask, clip-path, and filter IDs per component instance
  so repeated SVGs do not reference one another accidentally.
- Give complex charts and diagrams a nearby textual summary and access to the
  underlying values or relationships. A title alone cannot communicate a dense
  visualization non-visually.
- Put control-like click, keyboard, focus, disabled, and link semantics on a
  surrounding `<button>` or `<a>`. Use direct interaction on SVG nodes only for
  genuinely graphical behavior a native control cannot express, and then supply
  an equivalent keyboard path, focus treatment, semantics, and textual access.
- Verify `currentColor`, focus indication, and meaningful shapes in forced-colors
  mode; do not let fills, masks, or gradients become the only carrier of state.

## Motion and Performance

- Match pointer-triggered SVG motion with `:focus-visible` or activation and
  author it inside the reduced-motion enhancement path. Preserve the final state
  and accessible outcome when motion is absent.
- Prefer transforms and opacity for hot-path motion. Stroke dash animations and
  path morphs can be appropriate for small graphics, but repeated complex paths,
  filters, and large paint regions require profiling.
- Set `transform-box` and `transform-origin` explicitly when SVG transforms pivot
  around the wrong box. For squash/stretch, keep the effect subtle and preserve
  perceived mass by scaling one axis inversely to the other.
- To move artwork through a stationary mask, mask a parent group and transform
  the child; transforming the already masked shape moves the composite. Separate
  mask, geometry, and motion ownership before attempting a complex path morph.
- Choose luminance versus alpha masking deliberately. Opaque gray partially
  reveals in a luminance mask but fully reveals in an alpha mask; check the
  chosen mask mode instead of treating every opaque fill as equivalent.
- For cursor-reactive artwork, use the coordinate and stable-measurement rules
  in [procedural animation](procedural-animation.md#keep-coordinates-and-targets-stable).
- Optimize exported SVG deterministically, but inspect the result. Never allow an
  optimizer to remove a required `viewBox`, accessible title/description, IDs,
  or precision that visibly changes the artwork.

## Review Checklist

- Is the chosen delivery mode justified by caching, styling, interaction, and reuse?
- Does the SVG scale without clipping, distortion, layout shift, or optical drift?
- Does each icon remain crisp and recognizable at its smallest real size, with
  optical weight coherent with nearby text and the rest of its icon family?
- Is it correctly hidden, concisely named, or accompanied by a fuller text alternative?
- Do theme, hover, focus, selected, disabled, reduced-motion, and forced-colors
  states work without duplicated state assets or a visual-only state cue?
- Are paths readable and effects support-gated, maintainable, and measured?
