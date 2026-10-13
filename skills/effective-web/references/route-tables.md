# Data Tables

Use this route when the primary UI problem is understanding, comparing, filtering, or acting on structured data.

## Workflow

1. Identify the user's comparison task and the few columns that matter most.
2. Decide whether the data should be a table, list, card set, matrix, or chart.
3. Set column priority, alignment, sorting, filtering, pagination, and row actions.
4. Design empty, loading, partial, overflow, and error states with stable dimensions.
5. Verify keyboard navigation and small-screen behavior.

## Rules

- Align numbers by decimal or right edge; align text by left edge.
- Keep actions close to the row or selection they affect.
- Do not hide essential data behind hover.
- Sticky headers and columns are useful only when they preserve orientation without covering content.
- Responsive tables need an explicit strategy, not horizontal overflow by default.
- Stacked-card patterns that set `display: block` on table elements destroy
  table semantics for screen readers; restore roles
  (`role="table"`/`"row"`/`"cell"`) or prefer keeping table `display` — see
  [html-accessibility.md](html-accessibility.md).

## References

Choose the one primary concern before reading another module:

- [tables-semantics.md](tables-semantics.md) - native structure, headers,
  captions, accessible comparison, and dense-value scanning.
- [tables-responsive.md](tables-responsive.md) - constrained widths, overflow,
  cards, priority columns, and sticky orientation.
- [tables-interactions.md](tables-interactions.md) - sorting, filters, column
  controls, pagination, and row or bulk actions.
