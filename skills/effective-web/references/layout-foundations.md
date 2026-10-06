# Layout Foundations

Use this module to establish a page or component's structural geometry before
choosing an implementation primitive. Read only the follow-up module named by
the unresolved constraint.

## Model Relationships Before CSS

1. List the content groups, their importance, and whether they are peers,
   sequence, supporting detail, or an owned action group.
2. Choose the outer page structure separately from each component's internal
   layout. The page owns placement; a component owns its response to its own
   available space.
3. Set a readable measure, alignment anchors, and a spacing scale based on
   relationship: closer means more related; larger gaps indicate a boundary.
4. Prefer ordinary flow, wrapping, bounded columns, and intrinsic grid or flex
   algorithms before fixed widths, breakpoints, or clipping.

## Baseline Rules

- Use full-width bands and clear page regions for large structure. Use a card
  only when it represents a repeated item, distinct tool, or real boundary.
- Apply `box-sizing: border-box` globally and use logical properties so writing
  direction does not require a second layout.
- Let the parent own a repeated gap with `gap`; use a one-off spacer only when
  it is a real, locally owned element of the composition.
- Bind headings to the content they introduce. A heading closer to the previous
  block reads as that block's caption; check proximity with the real copy at
  narrow and wide widths. Dense layouts still need an identifiable group.
- Choose image/text alternation for a better reading path, not automatic
  left-right variety. Short comparisons may benefit; preserve logical source
  and focus order when the layout changes.
- Test empty, long, unbreakable, and translated content. A break is evidence of
  a missing constraint or wrong ownership, not an automatic reason for another
  media query.
- Make fixed and sticky controls safe-area aware and preserve reachable touch
  targets for coarse pointers.

## Choose the Next Module

- For intrinsic grids, stable component slots, and container-driven changes,
  read [intrinsic layouts](intrinsic-layouts.md).
- For image sizing, continuous resize, content thresholds, and page-level
  breakpoints, read [responsive design](responsive-design.md).
- For CSS algorithms, container queries, and resilient implementation details,
  read [CSS layout and responsive design](css-layout-responsive.md).

Use the [deep layout appendix](layout-spacing.md) only for an unusual spacing
system, visual-density diagnosis, safe-area edge case, or a detailed CSS
pattern not covered by those focused modules.
