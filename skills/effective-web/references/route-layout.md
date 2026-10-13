# Layout and Spacing

Use this route for the structural geometry of an interface: where things sit, how they align, how relationships are expressed through space, and how the layout adapts across containers and viewports.

## Workflow

1. Identify the content groups and rank them by relationship, frequency, and importance.
2. Outline the meaningful boxes and separate the page or section's outer grid
   from the internal layout of its components.
3. State each region's layout behavior before naming a component: flow,
   wrapping group, bounded column, narrow-plus-flexible pair, equal peers,
   repeated cells, overflow sequence, or deliberate overlay.
4. For repeated or context-sensitive content, define layout slots with
   required and optional content, sizing bounds, placement conditions, source
   order, and overflow behavior.
5. For a complex composition, inventory each layout zone's conditions: content
   presence or count, available component space, viewport-owned page state,
   ancestor-provided presentation intent, capabilities, and user preferences.
   Assign every condition to the element or context that owns it.
6. Prototype the outer grid and slot placement with semantic mock markup and
   representative content before styling component details.
7. Choose and compose the smallest intrinsic primitives that express those
   behaviors. Prefer content- and container-driven reconfiguration before
   queries.
8. Establish a spacing scale and apply it by relationship: closer means more related, farther means separated.
9. Define stable dimensions only for genuinely fixed-format UI such as boards, toolbars, tiles, counters, and grids.
10. Add a container query for an explicit component mode only after intrinsic
   sizing cannot express it; reserve media queries for viewport-owned changes.
11. Check continuous container widths, content absence and excess, image-ratio
    changes, zoom, long and unbreakable content, keyboard reachability, and
    supported writing directions before shipping.

## Rules

- Avoid layout shifts caused by hover states, labels, loading text, or dynamic content.
- Preserve readable line lengths; do not let wide screens stretch dense content indefinitely.
- Use full-width bands or unframed layouts for page structure. Reserve cards for repeated items, modals, and genuinely framed tools.
- Treat the layout-zone condition inventory as a behavioral contract, not as a
  request for exhaustive device mockups. Validate the in-between states in a
  resizable browser fixture with realistic zero, one, and many content cases.
- Keep semantic component markup stable across layout contexts. Let the host
  composition own external placement and let the component own its internal
  response to available space.
- Keep presentation intent that exists only because of host placement on the
  host through a semantic custom property or scoped data attribute. Do not pass
  `featured`, `compact`, or `presentation` props through the component API
  merely to repeat that layout context.
- Treat breakage as evidence of a missing constraint or misassigned owner.
  Diagnose that relationship before adding another breakpoint, fixed size, or
  overflow clip.
- Account for safe-area insets on fixed and sticky UI.
- Keep touch targets large enough and spacing generous enough for coarse pointers.

## References

- [layout-foundations.md](layout-foundations.md) - start here for structural
  geometry, grouping, spacing, and primitive selection. It names the one
  follow-up reference to load only when the remaining constraint is intrinsic,
  responsive, or CSS-implementation specific.
