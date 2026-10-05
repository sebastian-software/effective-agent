# Component Development

Build components as durable interface primitives: semantic DOM first, clear state surfaces, predictable layout ownership, resilient focus behavior, and configurable CSS APIs.

## Working Rules

- Preserve native controls and semantics whenever possible.
- Do not put default outer margins on reusable components. Separate component
  internals from parent layout: the parent owns spacing between components,
  using `gap` in Flex/Grid compositions or a parent-scoped flow rule such as
  the Owl (`> * + *`) when normal block flow should remain intact. Components
  own their internal rhythm. Make the narrow exception explicit: a
  token-backed, inert spacer may own one deliberate discontinuity when neither
  sibling should own it; do not use it to replace a repeated parent-owned rule.
- Expose state through real DOM state, attributes, data attributes, and custom properties instead of hidden implementation details.
- Define disabled, loading, empty, error, success, hover, focus, active, reduced-motion, high-contrast, and translated-text behavior.
- Keep component APIs portable across plain HTML/CSS, React, and Web Components unless framework specifics are required.
- Use low-level primitives for behavior and composition; keep visual styling and app-specific policy layered above them.
- Prefer configurable CSS APIs over prop explosions: custom properties, data attributes, parts/slots, and semantic child structure scale better than many one-off visual props.
- Derive parent/container styling from real child state with `:has()`, `:focus-visible`, `:checked`, `aria-expanded`, data attributes, or form validity instead of replacing semantic children with fake wrappers. Guard `:has()` usage with `@supports selector(:has(*))` where a fallback matters.
- Treat ARIA as support for missing semantics, not a replacement for it. Reach for `button` triggers, real option lists, and native controls first; add `aria-expanded`, `aria-controls`, and `aria-describedby` to convey state that the markup cannot, and keep keyboard, focus, and screen-reader behavior part of the component API and its review checklist.
- For floating UI, separate three decisions: trigger semantics, positioning/collision strategy, and dismissal/focus behavior. Anchor positioning can solve placement, but it does not solve accessibility by itself.
- Before building custom select, switch, accordion, dialog, tooltip, menu, tabs, or navigation, check whether current native elements plus progressive enhancement meet the requirement. Ship a usable baseline (semantic markup, reachable links, skip links, sensible focus flow) that works before JavaScript loads, and let JavaScript enhance organization rather than create the only path.
- Reach for native platform primitives that preserve semantics and replace hand-written state code, but never treat a native visual API as an accessibility shortcut. Use command/invoker attributes (`command`/`commandfor`) to cut glue JavaScript only where target browsers support them, and keep the same actions reachable through ordinary controls where support is mixed. Treat experimental primitives such as interest-triggered popovers and CSS carousels as not-yet-shippable unless the product is explicitly browser-gated; build critical hovercards and carousels with tested input, focus, and fallback behavior.
- Meet the 24x24 CSS px WCAG floor for interactive controls, and prefer 44-48px touch targets with adequate spacing where space allows. Extend the hit area past small visual bounds (icon buttons, pagination, toggles), make the whole label or row part of the target, and apply Fitts's law by placing frequent actions where they are easy to reach. Expanded targets must not overlap adjacent interactive targets. Verify target sizes under touch and pointer input.
- Never nest a button, link, or other interactive control inside another
  interactive element. For a clickable card or row with secondary actions, keep
  the controls as semantic siblings; when the primary action should cover the
  surface, expand it with a positioned pseudo-element and raise the secondary
  controls above that layer. Verify non-overlapping hit areas, DOM/focus order,
  visible focus rings, text selection, and screen-reader names.
- Treat focus as a state that may invalidate decorative positioning. When
  sticky, overlapping, clipped, or docked treatment can obscure the focused
  item, suspend the treatment while focus is within the affected collection and
  verify the full keyboard path in a suitably tall and resizable fixture.
- Require a visible focus indicator on every interactive component. Standardize it through custom properties for size, color, and style; draw it with `outline` plus `outline-offset` in an explicit focus color token (two-tone with a `box-shadow` where the ring crosses varied backgrounds; see [HTML Accessibility](html-accessibility.md)) and a minimum thickness such as `max(2px, 0.08em)`; key it on `:focus-visible` with a `:focus` fallback; and verify it holds up in dark mode and forced-colors mode, adjusting per control type (button, link, input, textarea, `summary`).
- Make components adapt to content count, container width, and language length using container queries, quantity queries (`:has()` over child counts), Grid, and logical properties, adding `@supports` fallbacks only where the project's support target predates them. Prefer these over hard-coded breakpoints, and document any remaining magic numbers as deliberate.
- Keep layout stable when overlays or state changes appear: reserve space with `scrollbar-gutter`, prevent scroll chaining with `overscroll-behavior`, and avoid layout shift from appearing/disappearing chrome rather than relying on fixed pixel offsets.
- Preserve structural affordances in high contrast mode. Hide optional borders with transparent colors (`border-color: transparent`, `outline-color: transparent`) rather than `border: none` or `outline: none`, so forced-colors mode, control recognizability, layout stability, and focus/hover states survive.
- Keep tightly nested rounded surfaces concentric when they visually form one
  shell: derive the outer radius from the inner radius plus the intervening
  inset. Apply the geometry only when spacing is even and the curves are meant
  to share a center; choose radii independently for asymmetric or clearly
  separate surfaces.
- Prefer optical alignment when mathematically centered text or icons still
  look unbalanced. Correct the source SVG `viewBox` or path when possible;
  otherwise use a small, documented local adjustment and verify it across icon
  variants, writing directions, and zoom levels.
- Inventory every observed use before extracting a visual primitive. Confirm
  size, color, placement, states, content, and context independence; one repeated
  shape in a design file is not yet proof of one reusable contract.
- Treat repeated authored CSS inside a component as an ownership diagnostic.
  Shared behavior should normally remain in globals, compositions, utilities,
  or tokens, while the component owns its distinctive internal relationship.
  Do not optimize for a low line count, but investigate unexplained restatement.
- Give fixed geometry around text — circular badges, clipped labels, fixed-height
  headings — only when content length and localization are contractually bounded.
  Otherwise let content size the element or provide explicit wrapping and
  overflow behavior.
- When a component clips or masks media, verify that focus indicators and
  meaningful content are not clipped with it. Keep overlay layers inside a local
  stacking context and derive coupled offsets from one exposed value instead of
  repeating matching constants.

## Component Pattern Rules

- **Buttons and links:** choose by outcome, not appearance. Buttons mutate state; links navigate. Keep `type="button"` explicit for non-submit buttons inside forms.
- **Switches and checkboxes:** keep the real input in the DOM, associate a visible label, and style from checked/focus/disabled state.
- **Accordions/disclosures:** use `details`/`summary` where the interaction model fits, and prefer this native disclosure behavior over custom open/close state. Use the shared `name` attribute on `details` for exclusive (one-open) sections, but avoid exclusive accordions when users need to compare panels. Make the whole `summary` row a target, and do not force the page to auto-scroll when a panel opens. Native disclosure plus `::details-content` and Grid can organize tab-like content without JavaScript, but it is not an ARIA tabs pattern; only add `role="tablist"` with full roving-focus keyboard behavior when those tab semantics are actually required.
- **Dialogs:** prefer native `dialog.showModal()` when suitable and rely on its built-in inertness and focus handling instead of building reflexive custom focus traps. This does not make focus management optional: still specify initial focus, focus return, Escape/close affordance, scroll locking, and the fact that background content must not receive focus, and test iframe and browser edge cases.
- **Tooltips/popovers:** use `aria-describedby` or popover semantics intentionally; support keyboard/touch dismissal and test collision, overflow, reduced motion, and viewport edges. For placement, prefer CSS Anchor Positioning (`anchor-name`, `position-anchor`, `position-area`, `position-try-fallbacks`, `anchor()`) where browser support allows, with a fallback positioning strategy; positioning is a separate concern from the trigger, dismissal, and accessibility semantics, which still must be specified.
- **Non-modal top-layer UI:** reach for the native Popover API (`popover`, `popovertarget`) for menus, teaching bubbles, and lightweight disclosures whose semantics fit, rather than hand-built top-layer state; pair it with a `button` trigger, explicit dismissal rules, and keyboard/touch checks. Use it for non-modal surfaces and keep `dialog.showModal()` for modal ones.
- **Selects/comboboxes:** evaluate the customizable native `select` (`appearance: base-select`, `::picker(select)`, rich option content) before building a custom combobox, keeping the existing form semantics and JS interface. Treat it as Limited availability until current Baseline data says otherwise, and opt in with a support-gated enhancement. Keep real text in every option; icons, swatches, and images may add meaning but must not replace the label, because unsupported browsers reduce the control to its standard text options. Test mobile OS picker behavior, fallback parsing, accessible value, width behavior, option content, hydration, and form submission.
- **Navigation:** keep a semantic nav baseline with reachable links before adding disclosure, priority-plus, or burger behavior. JS enhances organization; it should not create the only path.
- **Treeviews and nested lists:** reserve affordance space, calculate indentation through CSS variables/logical properties, and support LTR/RTL without fragile selector chains.

## Review Checklist

- Does the component still work with no JavaScript or with delayed JavaScript where that is reasonable?
- Are visual states connected to real semantic state rather than duplicate hidden state?
- Can the component be translated, zoomed, used with touch, used with keyboard, and used in forced-colors mode?
- Does the parent layout control external spacing while the component controls only its internal rhythm?
- Are default outer margins absent from reusable components, with each remaining
  margin owned by a parent-scoped flow relationship, prose context, `auto`
  alignment, or a documented optical correction?
- If an explicit spacer is present, is it a one-off composition concern with a logical axis, stable flex dimension, token-backed size, and no semantic or focus impact?
- Do tightly nested radii remain concentric where the surfaces form one shell,
  and are asymmetric surfaces allowed to use independent geometry?
- Are visibly asymmetric icons optically aligned at the source or through a
  small documented adjustment that survives variants and RTL?
- Are optional visual effects, animation, and masking removable without losing meaning?
- Does the component have a representative story, pattern-library example, or
  isolated fixture when its state or layout behavior cannot be verified on a
  simple static page?
- Do interactive targets meet the 24x24 CSS px floor, use 44-48px touch targets where practical, avoid overlap, and show a visible `:focus-visible` indicator in light, dark, and forced-colors modes?
- Are the component's escape hatches documented: slots, `className`, CSS variables, data attributes, refs, and event callbacks?
