# Interop and Accessibility

Libraries and platform interop are implementation tools, not permission to skip
semantic DOM and accessibility. A headless library gives behavior and ARIA
wiring; the component still owns names, states, focus order, and the correct
rendered element. Verify accessibility against rendered DOM, keyboard, and a
screen reader — not against the library's reputation.

## Working Rules

### Accessible names, roles, and states

- Give every interactive element an accessible name. Prefer visible text;
  otherwise pass an explicit `aria-label`/`aria-labelledby` through the API.
  Icon-only controls without a name are invisible to screen readers.
- Use the native element for its role before reaching for `role`: `<button>`,
  `<a href>`, `<nav>`, `<ul>`, `<dialog>`. Add `role` only when no native
  element fits, and then supply every state that role requires
  (`aria-expanded`, `aria-selected`, `aria-checked`, `aria-current`).
- Reflect dynamic state in ARIA as it changes, and announce out-of-band updates
  (validation results, async completion) through an `aria-live` region or a
  status role so non-visual users are not stranded.
- Express disabled state with the native `disabled` attribute on real form
  controls; for composite widgets that must stay focusable, use `aria-disabled`
  plus suppressed activation. Convey required, invalid, and described-by via
  `required`/`aria-required`, `aria-invalid`, and `aria-describedby` pointing at
  the error text.

### Focus and keyboard

- Implement the keyboard interaction the widget's role mandates (WAI-ARIA
  Authoring Practices): arrow-key navigation and roving `tabindex` for menus,
  tabs, listboxes, and radio groups; `Enter`/`Space` activation; `Escape` to
  dismiss. A reused interactive component without keyboard support is broken.
- Manage focus deliberately on transitions: move focus into an opened
  dialog/menu, restore it to the trigger on close, and never leave focus on a
  hidden or removed element. Keep a visible focus indicator; never remove the
  outline without an equivalent replacement.
- Make focus order follow DOM order. Avoid positive `tabindex`; use `tabindex={0}`
  to add an element to the tab order and `tabindex={-1}` for programmatic focus
  targets only.

### Headless libraries (React Aria, Radix)

- Treat React Aria, Radix, and similar as accessibility infrastructure for
  focus management, ARIA wiring, and keyboard behavior — then still supply
  product-specific labels, descriptions, empty/loading/error states, and layout.
  The library does not know your copy.
- Pick per primitive on accessibility coverage and styling model, not as an
  all-or-nothing bet: Radix ships unstyled behavior with `asChild` for merging
  onto your element; React Aria offers hooks plus styled-agnostic components and
  strong i18n/collection support. Mixing per-component is fine when each carries
  its own correct semantics.
- Do not override the library's ARIA attributes or focus management unless a real
  bug requires it; if you must, re-verify the affected keyboard and
  screen-reader flow.

### Portals and dialogs

- Render overlays (modals, popovers, toasts, tooltips) through a portal so they
  escape `overflow`/`z-index`/`transform` stacking contexts, but keep the React
  tree relationship: events still bubble through the React parent, so wire
  handlers on the component, not on the portal container.
- For a modal dialog, trap focus inside while open, render an
  `aria-modal="true"` dialog with an accessible name, make the rest of the page
  inert (the `inert` attribute or `aria-hidden` on siblings), close on `Escape`
  and on backdrop click, and restore focus to the opener. Prefer a vetted
  primitive (`<dialog>`, Radix Dialog, React Aria) over hand-rolling these.
- Position popovers with awareness of the viewport (flip/shift) and ensure the
  trigger's `aria-expanded`/`aria-controls` reference the portal content by `id`.

### Refs and imperative handles

- Use refs only for genuine imperative needs: focus, scroll, measurement,
  media/animation control, and third-party/DOM library integration. Express
  everything else declaratively through props and state.
- In React 19+, accept `ref` as a normal prop on function components and forward
  it to the underlying DOM node; the old `forwardRef` wrapper is no longer
  required (and React plans to deprecate it in a future release). In React 18 codebases, keep using
  `forwardRef`. Match the codebase's React version before changing a public ref
  API — it is a breaking change for consumers.
- When exposing imperative methods, use `useImperativeHandle` to publish a
  minimal, named API (`{ focus, scrollIntoView }`) instead of leaking the raw DOM
  node, so the contract is intentional and stable.

### Custom elements and framework interop

- In React 19+, rely on its full Custom Elements support: React passes primitive
  props as HTML attributes and object/function props as DOM properties, and
  routes `on*` props to native events. Verify each custom element's expected
  attribute-vs-property contract; for non-standard events, attach listeners via a
  ref with `addEventListener` and clean them up.
- Test interop across attributes, properties, events, refs, SSR, and hydration —
  custom elements often need client-side definition and can mismatch during
  server render. Define or guard them so the first client render reconciles
  cleanly.

### Server and client boundaries

- Default components to Server Components in an RSC setup; add `"use client"`
  only at the leaf that needs interactivity (state, effects, event handlers,
  browser APIs, refs to DOM). Pushing the boundary down keeps more of the tree
  off the client bundle.
- Pass only serializable props across the server/client boundary — no functions
  or class instances; `Date` is serializable, though a primitive may be clearer
  when it matches the consumer's needs. Pass children as
  already-rendered server content into a client wrapper to keep static parts on
  the server.
- Gate browser-only code (`window`, `localStorage`, `matchMedia`, measuring DOM)
  behind effects or client components so it never runs during SSR, and ensure the
  server and first client render produce identical markup to avoid hydration
  mismatches (read environment-specific values after mount, not during render).

## Review checklist

- Does every interactive element have an accessible name, the correct native
  role/element, and accurate dynamic ARIA state?
- Is the role's required keyboard interaction implemented, with focus moved on
  open, restored on close, and a visible focus indicator?
- Do headless primitives keep their ARIA/keyboard wiring intact while the product
  supplies labels and states?
- Do dialogs trap focus, set `aria-modal`, inert the background, close on
  `Escape`, and restore focus — preferably via a vetted primitive?
- Are refs limited to real imperative needs, forwarded per the codebase's React
  version, and exposed as a minimal imperative handle?
- Are custom elements verified for attribute/property/event/ref behavior across
  SSR and hydration?
- Is `"use client"` at the smallest leaf, with serializable props across the
  boundary and browser APIs guarded against SSR/hydration mismatch?
