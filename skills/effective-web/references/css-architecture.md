# CSS Architecture

> Deep appendix. Start from [css-cascade.md](css-cascade.md), [css-tokens.md](css-tokens.md), or [css-organization.md](css-organization.md); load this file only for migration and feature edge cases.

Structure stylesheets with cascade layers, native nesting, scoped styles, and a custom properties architecture that scales from small projects to large design systems.

## Baseline Styles

Start a new interface with a small, functional baseline in the `reset` layer;
preserve useful native semantics instead of stripping every browser default.
Do not retrofit it into an established product as a mechanical cleanup: verify a
semantic fixture and the affected real pages, because global defaults can create
subtle regressions.

```css
@layer reset {
  *,
  *::before,
  *::after {
    box-sizing: border-box;
  }

  *:not(dialog) {
    margin: 0;
  }

  body {
    line-height: 1.5;
    -webkit-font-smoothing: antialiased;
  }

  img,
  picture,
  video,
  canvas,
  svg {
    display: block;
    max-inline-size: 100%;
  }

  input,
  button,
  textarea,
  select {
    font: inherit;
  }

  p,
  h1,
  h2,
  h3,
  h4,
  h5,
  h6 {
    overflow-wrap: break-word;
  }
}
```

Apply `text-wrap: pretty` to reading text and `text-wrap: balance` to short
headings as progressive enhancements; keep their detailed selection rules in
[Typography rules](typography-rules.md). Enable `interpolate-size:
allow-keywords` only for users without a reduced-motion preference. In a
framework app, add `isolation: isolate` only to the actual application root
when its overlay stacking contract needs it; do not add a global `z-index`.

## Cascade Layers (`@layer`)

Cascade layers give CSS authors explicit control over cascade priority. Layer order determines precedence -- specificity and source order within a layer become irrelevant across layer boundaries.

### Three Ways to Create Layers

```css
/* 1. Declare layer order upfront (statement at-rule) */
@layer reset, base, tokens, layouts, components, utilities;

/* 2. Named block with rules */
@layer components {
  .card { border: 1px solid oklch(92% 0.005 250); }
}

/* 3. Anonymous layer (cannot be appended to later) */
@layer {
  p { margin-block: 1rem; }
}
```

### Importing into Layers

```css
@import url('normalize.css') layer(reset);
@import url('framework.css') layer(components.vendor);
```

`@import` must precede all other rules except `@charset` and `@layer` statements.

### Ordering Rules

- First declared layer = lowest priority
- Last declared layer = highest priority
- Unlayered styles (outside any layer) have the *highest* normal priority
- A simple selector in a higher-priority layer overrides a complex selector in a lower-priority layer, regardless of specificity

```css
@layer base, components;

@layer components {
  .title { color: oklch(25% 0.02 250); }    /* Wins -- later layer */
}

@layer base {
  main .title { color: oklch(45% 0.02 250); } /* Loses -- earlier layer */
}
```

### The `!important` Reversal

When `!important` is applied, layer priority inverts. First-defined layers gain highest `!important` priority; unlayered `!important` declarations rank lower than layered ones.

**Priority order (highest to lowest):**
1. `!important` declarations in earlier layers (e.g. reset)
2. `!important` declarations in later layers (e.g. utilities)
3. `!important` declarations outside layers
4. Normal declarations outside layers
5. Normal declarations in later layers
6. Normal declarations in earlier layers

This means `!important` in a reset layer overrides `!important` in a utilities layer -- the opposite of normal behaviour. Layers make `!important` largely unnecessary; avoid it.

### Nested Layers

```css
@layer components {
  @layer defaults, structures, themes;
}

/* Append rules via dot notation */
@layer components.themes {
  .card { background: oklch(97% 0.003 250); }
}
```

### `revert-layer`

Rolls back to the previous layer's value for a property:

```css
@layer theme {
  a { color: oklch(60% 0.15 250); }
  .no-theme { color: revert-layer; }
}
```

Other global keywords for reference:
- `initial` -- specification initial value
- `inherit` -- parent element value
- `unset` -- `inherit` for inherited properties, otherwise `initial`
- `revert` -- roll back author-origin styling
- `revert-layer` -- roll back to previous layer

### Recommended Layer Structure

```css
@layer reset, tokens, base, layouts, components, utilities;
```

| Layer | Purpose |
|-------|---------|
| `reset` | Normalize browser defaults |
| `tokens` | Custom properties (primitive + semantic) |
| `base` | Element-level typography, links, headings |
| `layouts` | Composition primitives (Stack, Sidebar, Grid) |
| `components` | Component-specific styles |
| `utilities` | Single-purpose overrides (highest normal priority) |

## CSS Nesting

Native CSS nesting groups related rules inside a parent selector. Supported in all engines (initial support in Chrome 112, Safari 16.5, Firefox 117; full support without the `&` requirement for type selectors in Chrome 120+ and Safari 17.2+).

### Syntax

```css
.card {
  padding: 1rem;
  background: oklch(100% 0 0);

  .title {
    font-weight: bold;
    color: oklch(25% 0.02 250);
  }

  &:hover {
    box-shadow: 0 2px 8px oklch(0% 0 0 / 0.1);
  }

  &.featured {
    border-color: oklch(60% 0.15 250);
  }
}
```

### The `&` Selector

- Represents the parent selector context
- Required for compound selectors: `&:hover`, `&.active`, `&::before`
- Required for joining: `&.featured` produces `.card.featured`
- Adjacent combinators work: `& + &` targets sibling relationships
- Optional for descendant selectors: `.title` inside `.card {}` is shorthand for `& .title`

### Specificity Behaviour (`:is()` Wrapper)

Nested selectors behave as if the parent is wrapped in `:is()` for specificity calculation. The nested rule takes the specificity of the *highest-specificity selector* in the parent's selector list.

```css
/* This nesting: */
article, .widget {
  p { color: oklch(45% 0.02 250); }
}

/* Behaves like: */
:is(article, .widget) p { color: oklch(45% 0.02 250); }
/* Specificity = (0, 1, 1) for ALL matches
   -- takes .widget's class specificity even when matching article p */
```

This can cause unexpected specificity inflation compared to Sass nesting, where each selector in a comma list expands independently.

### Nesting At-Rules

Media, container, supports, and layer queries nest directly:

```css
.card {
  display: block;

  @media (min-width: 40em) {
    display: grid;
    grid-template-columns: 1fr 2fr;
  }

  @container sidebar (min-width: 300px) {
    grid-template-columns: 1fr 1fr;
  }
}
```

### Depth Limits

Limit nesting to 2-3 levels maximum. Deeper nesting creates:
- Overly specific selectors that are hard to override
- Tight coupling between CSS and DOM structure
- Reduced readability

```css
/* Good: 2 levels */
.card {
  .title { font-weight: bold; }
  .title small { color: oklch(45% 0.02 250); }
}

/* Bad: 4+ levels mirrors DOM structure */
.page {
  .main {
    .section {
      .card {
        .title { font-weight: bold; }
      }
    }
  }
}
```

## Scoped Styles (`@scope`)

`@scope` defines style boundaries so rules apply only within a subtree. Supported in Chrome 118+, Edge 118+, Safari 17.4+, Firefox 146+.

### Basic Syntax

```css
@scope (.card) {
  :scope {
    border: 1px solid oklch(92% 0.005 250);
    border-radius: 0.5rem;
  }
  .title { font-weight: bold; }
  .content { padding: 1rem; }
}
```

### Donut Scope

A donut scope has both an upper and lower boundary. Styles apply inside the upper bound but stop at the lower bound, creating a "hole" for slotted content.

```css
@scope (.card) to (.card-slot) {
  /* Styles apply inside .card but NOT inside .card-slot */
  p { color: oklch(25% 0.02 250); }
  img { border-radius: 0.5rem; }
}
```

The upper bound (`.card`) is inclusive; the lower bound (`.card-slot`) is exclusive.

### Scope Proximity

Scope proximity is a cascade criterion that comes after specificity but before source order. When two selectors have equal specificity, the one with the closer scope root wins:

```css
@scope (.light-theme) {
  p { color: oklch(25% 0.02 250); }
}
@scope (.dark-theme) {
  p { color: oklch(95% 0.01 250); }
}
/* If .dark-theme is nested inside .light-theme,
   elements inside .dark-theme get white text
   because that scope root is closer */
```

### `@scope` vs Nesting Comparison

| Feature | `@scope` | Nesting |
|---------|----------|---------|
| **Purpose** | Define component boundaries | Organize related selectors |
| **Lower boundary** | Yes (donut scope) | No |
| **Proximity in cascade** | Yes (closer scope wins) | No |
| **Specificity** | Does not add root specificity to scoped selectors | Parent specificity wraps via `:is()` |
| **Best for** | Component isolation, slots, theming | Pseudo-classes, states, media queries |

**Use `@scope` when:**
- Styles should not leak in or out of a component
- You need slots for nested content (donut scope)
- Themes are nested and proximity should resolve conflicts

**Use nesting when:**
- Grouping pseudo-classes, states, and media queries within a selector
- Expressing modifier relationships
- Improving readability of related rules

## Custom Properties Architecture

### Three-Tier System: Primitive, Semantic, Component

```css
/* Tier 1: Primitives -- raw values, global, never used directly in components */
:root {
  --blue-1: oklch(98% 0.008 250);
  --blue-5: oklch(55% 0.15 250);
  --blue-9: oklch(10% 0.014 250);
  --gray-1: oklch(97% 0.003 250);
  --gray-5: oklch(58% 0.02 250);
  --gray-9: oklch(20% 0.01 250);
  --space-xs: 0.5rem;
  --space-s: 1rem;
  --space-m: 1.5rem;
  --space-l: 2rem;
  --radius-s: 0.25rem;
  --radius-m: 0.5rem;
}

/* Tier 2: Semantic -- contextual meaning, themeable */
:root {
  --color-text: var(--gray-9);
  --color-text-muted: var(--gray-5);
  --color-interactive: var(--blue-5);
  --color-surface: var(--gray-1);
  --color-background: oklch(100% 0 0);
  --color-border: oklch(92% 0.005 250);
}

/* Tier 3: Component -- scoped, prefixed with underscore */
.card {
  --_padding: var(--space-m);
  --_radius: var(--radius-m);
  --_border: var(--color-border);

  padding: var(--_padding);
  border-radius: var(--_radius);
  border: 1px solid var(--_border);
}
```

**Key principles:**
- Never use primitive tokens directly in component styles -- always go through semantic tokens
- Semantic tokens reference primitives; component tokens reference semantics
- This one-directional chain enables theming: change semantic tokens and all components update
- Component tokens use a leading underscore (`--_color`) to signal "private" scope
- Keep primitives to a curated set -- not every possible value

### Theming via `light-dark()`

```css
:root {
  color-scheme: light dark;

  --color-text: light-dark(oklch(25% 0.02 250), oklch(95% 0.01 250));
  --color-surface: light-dark(oklch(97% 0.003 250), oklch(15% 0.01 250));
  --color-interactive: light-dark(oklch(60% 0.15 250), oklch(70% 0.12 250));
  --color-border: light-dark(oklch(92% 0.005 250), oklch(30% 0.01 250));
}
```

`light-dark()` requires `color-scheme: light dark` on the element or an ancestor. The first value applies in light mode, the second in dark mode.

### Anti-Patterns

- **Hundreds of unused primitives** -- curate only the values the design system actually uses
- **All tokens on `:root`** -- scope component tokens to component selectors
- **Skipping the semantic layer** -- going straight from primitive to component makes theming impossible
- **Custom properties for static values** -- if a value never changes and is never shared, just use the value directly

## CSS Methodologies

### BEM (Block Element Modifier)

```css
.card { }
.card__title { }
.card__title--highlighted { }
```

- Forces flat specificity (almost all selectors are single-class)
- Predictable, explicit naming scales well in teams
- Verbose naming can feel heavy
- Still relevant for design systems needing strict conventions

### Utility-First (Tailwind)

```html
<div class="p-4 rounded-md border border-gray-200 bg-white">
  <h2 class="font-bold text-lg">Title</h2>
</div>
```

- All utilities at (0,1,0) specificity -- very flat
- Fast prototyping, consistent design tokens
- Trades CSS file readability for HTML-centric styling
- Requires purging to remove unused CSS

### CUBE CSS (Composition Utility Block Exception)

Separate composition, utilities, component styles, and state exceptions while preserving the cascade.

**Four layers:**
- **Composition:** Layout primitives (Stack, Sidebar, Cluster)
- **Utility:** Single-purpose classes (`.text-center`, `.flow`)
- **Block:** Component-specific styles (minimal by the time you reach this layer)
- **Exception:** State deviations via data attributes

```css
/* Block */
.card {
  padding: var(--space-m);
  background: oklch(100% 0 0);
}

/* Exception via data attribute */
.card[data-state="reversed"] {
  display: flex;
  flex-direction: column-reverse;
}
```

Exceptions use `data-*` attributes instead of BEM modifiers, providing a hook for both CSS and JavaScript.

### Composable Layout Primitives

Keep single-purpose geometry in the layout layer: Stack for sibling rhythm,
Box for inset, Center for a measured column, Cluster for wrapping peers,
Sidebar for unequal regions, Switcher for equal peers that change mode together,
Cover for a principal region, Grid for repeated tracks, Frame for a ratio,
Reel for native scrolling, Imposter for overlap, and Icon for text-relative
media. Container establishes a query context when an explicit local mode is
needed; it does not supply a visual composition itself.

Each primitive composes as a parent, child, or sibling. Read
[intrinsic-layouts.md](intrinsic-layouts.md) for selection, exact algorithms,
parameter contracts, and verification. Keep external placement with the parent
and internal response with the component; do not duplicate the algorithms in
component namespaces. A Stack may use Flex/Grid `gap` or normal block flow with
a direct-child Owl selector. Choose from the formatting behavior required.

### Recommended Combination

Use cascade layers as the orchestration layer -- they work with any methodology:

```css
@layer reset, tokens, base, layouts, components, utilities;
```

- **Layouts layer:** Composable layout primitives for composition
- **Components layer:** CUBE CSS or BEM for component naming
- **Utilities layer:** Sparingly, for one-off overrides at highest priority
- **Tokens layer:** Three-tier custom properties architecture

Cascade layers + low-specificity methodology = the strongest combination.

## Anchor Positioning

CSS anchor positioning connects an absolutely positioned element to one or more anchor elements. Treat it as progressive enhancement unless current project support data confirms the target browsers all implement the required properties; do not assume in-app webviews and pinned enterprise browsers match the latest engine.

Use anchor positioning for dropdowns, tooltips, popovers, and context menus when
browser support allows it. The overlay should still escape ancestor clipping by
living in the top layer (`popover`) or using `position: fixed`.

Do not solve clipped overlays with larger z-index values. If an ancestor clips
overflow, the overlay must move out of that clipping context or use a native
top-layer primitive.

Anchor positioning solves placement and collision strategy only. It does not
solve trigger semantics, accessible names and descriptions, dismissal, focus
movement, touch behavior, or screen-reader expectations; supply those
separately.

Choose the adoption path by support level:

- Broad support: prefer anchor positioning for suitable floating UI to remove
  fragile JavaScript geometry code.
- Mixed support: keep the component usable with a simpler position,
  fixed/top-layer placement, or an existing floating-positioning library.
- Task-critical floating UI: do not rely on anchor positioning without a tested
  fallback.

### `anchor-name` and `position-anchor`

```css
/* Define an anchor */
.trigger {
  anchor-name: --tooltip-anchor;
}

/* Position relative to anchor */
.tooltip {
  position: absolute;
  position-anchor: --tooltip-anchor;
}
```

### `position-area`

A shorthand that places the positioned element in a region of the anchor's grid:

```css
.tooltip {
  position: absolute;
  position-anchor: --tooltip-anchor;
  position-area: block-start center;
  margin-block-end: 0.5rem;
}
```

### `position-try-fallbacks`

When the preferred position overflows the viewport, the browser tries fallback positions:

```css
.tooltip {
  position: absolute;
  position-anchor: --tooltip-anchor;
  position-area: block-start center;
  position-try-fallbacks: flip-block, flip-inline, flip-block flip-inline;
}
```

**Flip keywords:**
- `flip-block` -- mirrors across the block axis (top/bottom)
- `flip-inline` -- mirrors across the inline axis (left/right)
- Combined: `flip-block flip-inline`

### `@position-try`

Define named custom fallback positions:

```css
@position-try --below-end {
  position-area: block-end span-inline-end;
  margin-block-start: 0.5rem;
}

.dropdown {
  position: absolute;
  position-anchor: --menu-trigger;
  position-area: block-end span-inline-start;
  position-try-fallbacks: --below-end, flip-block;
}
```

## Evolve Abstractions from Evidence

- Establish a resilient semantic baseline before component styling: ordinary
  headings, prose, lists, links, media, code, tables, forms, focus, selection,
  fragment targets, disclosures, and disabled controls should remain usable
  without a component class. Let named patterns own specialized presentation
  instead of turning the global layer into a hidden component system.
- Start a new component need locally. Promote a token, utility, composition, or
  public custom property only after multiple concrete uses or an established
  system decision proves that the abstraction has one stable job.
- Give utilities a useful default, one portable responsibility, and only the
  token-backed inputs needed for intentional variation. Do not turn one local
  exception into a global capability "just in case."
- Treat growing utility clusters, arbitrary values, compound queries, undo
  rules, duplicated content, opaque math, and repeated exception selectors as
  signals to revisit ownership or the layout model before patching further.
- Document the derivation, inputs, valid range, fallback, and ownership of
  generated geometry or advanced CSS math. Comments that merely call the result
  "magic" do not make an `@property`, trigonometric, clipping, or container-fit
  implementation maintainable.
- Refactor existing rules when requirements change. CSS that only accumulates
  new selectors and overrides is becoming append-only even if every individual
  addition appears harmless.
- Remove superseded experiments, selectors, and component options when Git
  already preserves their history. Retain temporary debt only with a documented
  current state, desired state, owner, and follow-up trigger.

## CSS File Organisation

### Layer-Based File Structure

```
styles/
  main.css                /* Layer order + @import statements */
  reset.css               /* @layer reset */
  tokens/
    primitives.css        /* @layer tokens */
    semantic.css          /* @layer tokens */
  base/
    typography.css        /* @layer base */
    elements.css          /* @layer base */
  layouts/
    stack.css             /* @layer layouts */
    sidebar.css           /* @layer layouts */
    grid.css              /* @layer layouts */
  components/
    card.css              /* @layer components */
    button.css            /* @layer components */
    dialog.css            /* @layer components */
  utilities/
    spacing.css           /* @layer utilities */
    visibility.css        /* @layer utilities */
```

### Entry Point Pattern

The single entry point declares layer order and imports everything:

```css
/* main.css -- single source of truth for cascade order */
@layer reset, tokens, base, layouts, components, utilities;

@import url('reset.css') layer(reset);
@import url('tokens/primitives.css') layer(tokens);
@import url('tokens/semantic.css') layer(tokens);
@import url('base/typography.css') layer(base);
@import url('base/elements.css') layer(base);
@import url('layouts/stack.css') layer(layouts);
@import url('layouts/sidebar.css') layer(layouts);
@import url('components/card.css') layer(components);
@import url('components/button.css') layer(components);
@import url('utilities/spacing.css') layer(utilities);
```

**Key principles:**
- Declare layer order at the very top, once
- Each file goes into exactly one layer
- One component per file, named after the component
- Third-party CSS goes into its own layer or a sub-layer: `@import url('vendor.css') layer(components.vendor);`
- Build tools should bundle `@import` statements for production to avoid sequential loading

## When to Use Which Approach

### Small Project (marketing page, blog)

- Cascade layers: `@layer reset, base, components, utilities`
- Simple naming -- `.card`, `.card-title` (no BEM needed)
- Minimal custom properties (semantic layer only)
- Nesting for pseudo-classes and media queries
- Composable layout primitives for composition

### Design System / Component Library

- Full layer architecture with nested sub-layers
- CUBE CSS or BEM naming for explicit component structure
- Three-tier custom properties (primitive, semantic, component)
- `@scope` for component encapsulation where supported
- Composable layout primitives as composition building blocks
- Strict nesting depth limits (max 2 levels)

### Large Application with Third-Party CSS

- Cascade layers essential -- layer vendor CSS below your own
- `@import url('framework.css') layer(vendor)` with vendor declared before components
- BEM or CUBE naming to avoid collisions with third-party selectors
- `@scope` for component isolation
- Utility layer at highest priority for overrides
- Aggressive unused CSS removal (PurgeCSS or similar)

## Common Mistakes

### Over-Nesting

Mirroring DOM structure in CSS (`.page .main .section .card .title`) creates brittle, overly specific selectors. Every nesting level inflates specificity via the `:is()` wrapper.

**Rule of thumb:** If you need to nest more than 2-3 levels, restructure.

### Specificity Wars

Overriding styles with ever-more-specific selectors instead of refactoring. Cascading `!important` declarations that become impossible to override. Using IDs in selectors (`#header .nav`) when classes suffice.

**Solution:** Use cascade layers to manage priority; keep selectors flat.

### Unused CSS

Shipping CSS that applies to no elements on the page increases file size and slows parsing. Common in utility-first frameworks without purging. Average web page ships 50-80% unused CSS.

**Tools:** Chrome DevTools Coverage panel, PurgeCSS, Lightning CSS.

### Too Many Custom Properties

Defining primitive tokens for every possible value ("just in case"). Putting all tokens on `:root` when many are only used in one component. Skipping the semantic layer, making theming impossible.

**Rule:** If a value never changes and is never shared, just use the value directly.

### Misunderstanding Nesting Specificity

Native CSS nesting wraps parents in `:is()`, which differs from Sass output. A parent list like `article, .widget` gives all nested selectors the specificity of `.widget` (0,1,0) even when matching via `article` (0,0,1).

```css
/* Developers expect (0, 0, 2) for article p but get (0, 1, 1): */
article, .widget {
  p { color: oklch(45% 0.02 250); }
}
```

### Ignoring `!important` Reversal in Layers

`!important` in an early layer (e.g. reset) overrides `!important` in a later layer (e.g. utilities) -- the opposite of normal cascade behaviour. This catches developers who place `!important` in utility layers expecting highest priority.

## Performance Considerations

### Selector Efficiency

Modern browsers match selectors in microseconds. The difference between `.card .title` and `.card-title` is negligible. Optimise for developer experience and maintainability, not selector speed.

**Exception:** Extremely large DOMs (10,000+ elements) with deeply nested descendant selectors may show measurable impact.

### File Size

Every byte of CSS is render-blocking -- the browser cannot paint until CSSOM is built.
- Remove unused CSS (biggest win for most projects)
- Use shorthand properties where appropriate (`margin` instead of four `margin-*` declarations)
- Minify and compress (gzip/brotli)
- Avoid duplicating declarations across files

### Unused CSS

Average web page ships 50-80% unused CSS, especially with frameworks. Use the Chrome DevTools Coverage panel to identify unused rules. PurgeCSS or Lightning CSS can strip unused selectors at build time.

### Render-Blocking

All `<link rel="stylesheet">` in `<head>` is render-blocking by default.
- Inline critical CSS (above-the-fold styles) to improve LCP
- Use `media` attribute on `<link>` to defer non-matching stylesheets: `<link rel="stylesheet" href="print.css" media="print">`
- Avoid `@import` in production without build tools (causes sequential loading)

### Custom Properties Performance

Custom property inheritance is cheap -- browsers handle it efficiently.
- Avoid setting custom properties on every element; prefer `:root` or component roots
- `@property` registration with `inherits: false` prevents unnecessary recalculation down the tree
- Cascade layers add minimal parsing overhead -- the benefit of eliminating `!important` chains outweighs any cost
