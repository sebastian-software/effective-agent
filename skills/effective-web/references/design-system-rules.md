# Design System Rules

Use this reference for reusable design-system decisions that cut across colour, tokens, SVG, visual effects, media, and component clarity. Keep durable rules here only when they affect reusable UI quality, not one-off decoration.

## Working Rules

### Color spaces and token derivation

- Author palettes and ramps in a perceptual color space such as OKLCH or LCH
  because its coordinates are a more useful starting point for visual spacing
  than HSL. Do not treat equal numeric steps as a guarantee of equal perceived
  steps: inspect every ramp, gamut-mapped result, and foreground/background
  pair. Reduce chroma as colors approach white or black to avoid garish
  extremes.
- Define color pairs, not isolated colors. Every brand, surface, status, and accent token needs known foreground, border, focus, hover, active, disabled, and forced-colors behavior.
- Derive related tokens (hover, active, disabled, tints, alpha variants) with relative color syntax (`oklch(from …)`) and `color-mix()` instead of hand-tuned hex or preprocessor math, so one base change cascades. `color-mix()` is Baseline Widely available; relative color syntax is Baseline 2024 (Newly available), so ship a static fallback ahead of relative-color values unless the project's support target already includes them.
- Pick the interpolation color space deliberately for gradients, transitions, and `color-mix()`. Interpolate in OKLCH or another perceptual space to avoid muddy or desaturated midpoints; sRGB interpolation through gray is the common cause of dead-looking gradients.
- Treat the color format itself as a token decision. Define when the system uses `hex`, `rgb()`, `hsl()`, `oklch()`, `color-mix()`, and relative color syntax, and keep raw values out of components — reference semantic tokens only.
- Treat a color-format migration as a representation change, not an implicit
  redesign: preserve selectors, token roles, gradient structure, alpha, and
  formatting unless the task explicitly changes the palette. Leave CSS
  keywords and third-party configuration formats alone when they require hex or
  another specific syntax. Convert with a tested color implementation, inspect
  out-of-gamut results, and verify every foreground/background pair after the
  migration.

### Contrast and accessibility

- Meet applicable WCAG 2.2 AA contrast requirements (4.5:1 text, 3:1 large
  text and non-text/UI) as the compliance baseline. Design beyond the minimum
  where needed: perceived contrast can still be weak at the ratio, especially
  for borders, icons, and underlines that carry meaning. Verify state
  visibility for buttons, inputs, and filters, not just static text.
- Use APCA as a supplementary design and review check: its contrast value is
  polarity-aware, and its evolving guidance varies with use case, text size,
  weight, and font characteristics. Preserve the actual foreground/background
  order: positive Lc represents dark text on a light background; negative Lc
  represents light text on a dark background. It does not replace applicable
  WCAG 2.x conformance requirements.
- Treat `contrast-color()` as a Baseline-2026 convenience for picking black or
  white foregrounds, not an accessibility guarantee. Declare an explicit color
  before it when older targets matter, and verify the selected pair because
  mathematical preference between black and white can still leave mid-tone
  backgrounds perceptually weak. Plan `prefers-contrast` and light/dark
  alternatives rather than relying on automatic foreground selection.

### Token architecture and ownership

- Treat the token set as a versioned API for the visual language, not as a bag
  of variables or an unreviewed export from a design tool. Co-own naming,
  semantics, lifecycle, and release decisions across design and engineering;
  include product, accessibility, QA, and platform owners when their contracts
  depend on the tokens.
- Keep component and token responsibilities separate. Components own markup,
  semantics, behavior, state transitions, accessibility, and structural layout
  relationships. Tokens own stable named design decisions such as color roles,
  type roles, spacing choices, radii, borders, and elevation. A token may
  configure a component, but it must not substitute for the component contract.
- Use three consumption levels with explicit boundaries:
  - **Reference or primitive tokens** store direct values and scales. Keep them
    internal to system authors by default so product code cannot couple itself
    to a palette step or raw measurement accidentally.
  - **Semantic tokens** name jobs such as text, surface, border, action, focus,
    and status roles. Make these the normal public contract for components and
    product code, and alias them to reference tokens per theme.
  - **Component tokens** expose a narrow hook only when a component genuinely
    needs to diverge from the shared semantic role across brands, products, or
    modes. Alias a semantic token by default and reject a token-per-property
    mirror of every component stylesheet.
- Publish reference tokens only for an intentional system-authoring or escape-
  hatch use case with documented stability and migration expectations. Do not
  expose every internal value merely because the build tool can emit it.
- Define a theme as a complete, coherent mapping of one shared semantic contract
  for a brand, product, mode, or supported combination. Override only the token
  domains that actually vary, retain explicit defaults for the rest, and test
  every supported theme for missing aliases, interaction states, contrast pairs,
  typography, density, and platform-specific representation.
- Choose one canonical, reviewable token source and make the direction of sync
  explicit. Treat design libraries, documentation, generated CSS, and native
  artifacts as synchronized consumers unless the project deliberately assigns
  one of them canonical ownership; never let independent edits create several
  competing sources of truth.
- Roll the architecture out through a representative product pilot, then feed
  proven needs back into the token and component systems. Avoid a year-long
  big-bang retrofit and speculative token inventory; version releases, provide
  migration mappings, deprecate before removal, and expand only after real
  products validate the abstraction.
- Treat accessibility as a system-wide verification responsibility. Tokens can
  encode reviewed pairs and constraints, but they cannot guarantee semantic
  markup, focus behavior, readable states, or assistive-technology support.

### Theming architecture

- Use semantic tokens with explicit cascade ownership: define theme values at a single owning scope and let local overrides flow through custom properties, so component code never hard-codes a theme.
- Use `light-dark()` with `color-scheme` for simple per-property system-theme switching, but keep an explicit theme architecture (data attribute or class plus token sets) when products need user-selected themes, local theme overrides, or cross-brand variants.
- Gate wide-gamut/P3 colors and modern color functions on the product's browser
  baseline. Provide an intentional sRGB semantic token first, use `@supports`
  for colour-notation support, and combine it with `@media (color-gamut: p3)`
  before overriding the token with a P3 value. A successful feature query does
  not prove that the output device can render P3. Derive and gamut-map each
  variant for its target gamut, and verify contrast in both branches.

### Agent-readable system contracts

- Map measurements from design artifacts to the nearest approved token first.
  Record and review meaningful deviations instead of importing raw pixels as new
  component values; preserve the intended hierarchy, not accidental measurement
  noise from one frame.
- When coupled geometry depends on part of a composite token, expose that stable
  sub-value once and derive the dependent offset from it. Do not duplicate a
  border width, inset, or radius as a second magic constant that can drift.
- Treat design decisions as maintained infrastructure. Record component purpose,
  allowed variants, token roles, states, accessibility constraints, examples,
  and anti-examples in versioned text next to the implementation.
- Document the full reuse ladder: tokens, utilities, layout compositions, and
  patterns. For every configurable unit, state its purpose, suitable use,
  inputs, defaults, variants, exceptions, representative example, and important
  semantic, content, or layout limits.
- Give both engineers and agents a small closed vocabulary: semantic tokens,
  approved components, explicit usage rules, and migration mappings. Do not ask
  them to infer the system from screenshots or a large set of near-duplicates.
- Keep the executable component, its stories, and its guidance synchronized.
  When a reusable API changes, update its examples and configuration guidance in
  the same task; identify stale rules instead of leaving old instructions to
  drift silently.
- Keep short explanations of intent, constraints, surprising math, and coupling
  near the source. Keep fuller rendered examples in the pattern library or
  design-system documentation, and link the two rather than duplicating them.
- Audit for raw values, detached variants, competing icon/type/color systems,
  undefined tokens, and duplicate interaction patterns. Use deterministic
  inventory and linting before asking an LLM to interpret ambiguous findings.
- Treat an append-only system as a health warning: if contributors repeatedly
  add selectors or components instead of discovering and adapting existing
  ones, improve ownership, naming, documentation, and removal practices before
  expanding the catalog again.
- Preserve room for documented product-specific components. A closed token set
  should prevent accidental drift, not force every legitimate exception into a
  generic primitive.
- Document supported component-plus-utility and composition combinations. A
  flexible API whose valid recipes live only in contributor memory is not a
  reusable system contract.

### SVG, icons, and visual effects

- Prefer inline SVG, or a deliberate SVG delivery system (sprite or component), for icons that need `currentColor`, CSS state styling, accessibility control, or design-system theming. Author SVG with a correct `viewBox`, presentational attributes, and shape primitives so it scales cleanly and stays readable by hand.
- Treat masks, clipping, backdrop filters, glass, grain, and SVG filters as interface-clarity tools, not default decoration, and choose the right primitive: `clip-path` for hard geometric cutouts, CSS or SVG masks for soft/gradient fades (text and image fades, avatar cutouts, rounded tabs). Reserve `feColorMatrix` for specialized image/color math.
- When a composition needs the actual contour of a photographed subject, use a suitable cutout asset or alpha matte rather than approximating the subject with a geometric clip.
- Check contrast, forced-colors behavior, reduced visual complexity, and performance before adopting any effect. Keep effects optional layers with fallbacks; never let meaning depend on translucency, filtering, or an unknown backdrop, and never let an effect drop text contrast.
- Control stacking with `isolation: isolate` and explicit stacking contexts so blend modes, filters, and backdrop effects do not leak into unintended backgrounds.

## Token Review Checklist

- Are reference, semantic, and component tokens separated by a documented
  consumer boundary, with semantic roles as the normal product-facing API?
- Does each component token represent a necessary cross-theme exception rather
  than duplicating one CSS property mechanically?
- Does every semantic token have a role, not just a visual name?
- Is there one canonical, versioned source with a defined sync direction, or can
  design files and generated platform artifacts drift independently?
- Does every supported brand, product, and mode implement the same semantic
  contract without missing aliases, states, or unreviewed fallbacks?
- Does a format-only color migration preserve token meaning, CSS structure,
  third-party format contracts, and foreground/background relationships?
- Are derived colors checked in light mode, dark mode, hover/focus/active states, disabled states, and forced-colors mode?
- Do colors meet applicable WCAG 2.2 AA ratios, with APCA used as a
  supplementary perceptual check?
- Do gradients, transitions, and `color-mix()` operations use a color space that avoids muddy interpolation?
- Can the icon system inherit text color, align to type, expose labels, and avoid duplicated sprite/runtime complexity?
- Are visual effects optional layers with fallbacks, or does meaning depend on masking/filtering/translucency?
- Do wide-gamut/P3 tokens have intentional sRGB fallbacks, separate syntax and
  output-gamut gates, and verified foreground/background pairs in both branches?
- Can a contributor discover the approved component, variant, and token without
  reverse-engineering screenshots or copying a nearby implementation?
- Do tokens, utilities, compositions, and patterns expose their purpose,
  defaults, inputs, variants, limits, and representative examples?
- Did a reusable API change update its source-adjacent guidance, rendered
  examples, and stories in the same task?
- Do deterministic checks catch raw values, undefined tokens, duplicates, and
  stale system guidance before generated code can amplify them?
- Is adoption grounded in representative pilots, with explicit versioning,
  migration, deprecation, and removal rules instead of a speculative big bang?
