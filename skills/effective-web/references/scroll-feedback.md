# Scroll Feedback and Large Lists

Use this module when scrolling itself communicates progress, returns a user to a
known place, or carries a large collection. Prefer predictable navigation over
spectacle.

## Feedback Without Hijacking

- Show a back-to-top control only after it saves meaningful effort; make it a
  labelled button, keep it out of content and focus paths, and respect reduced
  motion when returning to the top.
- Use overscroll containment only to stop a real nested-scroll or pull-to-refresh
  problem. Do not prevent users from leaving a short inner region naturally.
- Scroll-driven animation must be optional, reduced-motion guarded, and
  implemented so the same state change remains understandable without it.

## Large Collections

- Virtualize only when measured item count, rendering cost, or memory requires
  it. Preserve item semantics, keyboard navigation, find-in-page expectations,
  and a stable way to reach a known item.
- Prefer pagination or Load more when task completion requires position,
  results totals, bookmarking, or returning to prior content. Infinite scroll
  is an exploratory pattern, not a default list implementation.

For driven versus triggered motion, observer thresholds, ranges, or sticky
header backgrounds, use [scroll animation recipes](scroll-animation-recipes.md).
For virtualizer library details and broader scroll failure patterns, consult
the [deep scroll appendix](scroll-patterns.md).
