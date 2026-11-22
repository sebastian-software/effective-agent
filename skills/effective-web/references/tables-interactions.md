# Table Interactions

Use this module for sorting, filtering, column controls, pagination, and row
actions in a data-dense view. Make the data state visible before optimizing
interaction density.

## Sorting and Filtering

- State the active sort column and direction in text or an accessible name, not
  only an arrow icon. Preserve the result count and current filters in the
  surrounding context.
- Put filters close to the values they affect. Provide an explicit reset and do
  not silently drop a filter when the layout changes.
- Treat column hiding and reordering as a user preference with a recoverable
  default. Do not remove a required comparison value without an alternative.

## Loading More Data

- Use pagination when users need a stable position, URL-addressable result set,
  or predictable total. Use a visible Load more control for exploratory lists.
- Avoid infinite scroll for analytical tables, footer-dependent flows, or tasks
  where returning to a prior row matters. Preserve scroll position when data
  changes.
- Keep bulk and row actions near their scope, explain destructive effects, and
  prefer undo when a reversible operation can avoid a confirmation dialog.
- For checkbox range selection, use the [direct manipulation studies](control-microinteractions.md#direct-manipulation)
  to define how dragging, backtracking, and cancellation affect existing selections.

## Verify

Exercise keyboard operation, focus after sorting or filtering, empty/partial
results, slow responses, selection state, and the mobile presentation chosen in
[responsive data tables](tables-responsive.md).

For detailed CSS and uncommon interaction patterns, use the [deep table
appendix](tables-data.md).
