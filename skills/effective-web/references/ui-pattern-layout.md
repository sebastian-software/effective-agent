# Layout Pattern Review

Use this module when a suspected generic pattern concerns page structure,
grouping, cards, or the reading path. Apply the context and evidence distinction
in [UI anti-patterns](ui-antipatterns.md).

## Structural and Layout Reflexes

Review these as advisory signals:

- A generic hero, metrics strip, and identical feature-card grid could serve any
  product after replacing the logo and colours.
- Every section becomes a bordered or elevated card; cards are nested inside
  cards instead of grouping through hierarchy, spacing, dividers, or surfaces.
  Keep nesting when the containers represent distinct actionable entities or a
  meaningful relationship in the accepted component system.
- Each feature repeats the same rounded-square icon tile, heading, and paragraph
  with no relationship to the actual content.
- Tiny tracked eyebrow labels or `01 / 02 / 03` markers scaffold every section.
  Keep labels that add a section, version, breadcrumb, or status, and numbers
  whose order carries real meaning, such as a process or timeline.
- A thick coloured side stripe decorates rounded cards, list items, or callouts
  without communicating state or category.
- Identical radii, shadows, borders, and stock component styling flatten the
  roles of unrelated elements. Choose them from the owning system and component
  purpose; a border plus shadow, hard offset shadow, pill, or soft corner can be
  intentional. No fixed radius range fits every brand.
- Every section centres its text or changes alignment for variety. Choose
  alignment for the reading path and content form; a short centred opening can
  still be appropriate.
- Equal three-column or bento grids give unlike content equal weight. Derive
  columns and tile size from content and priority; repeated peers can remain
  equal when comparison or recognition benefits.
- Alternating image/text rows create an automatic left-right zigzag. Use the
  alternation only when it improves reading order; short, clearly grouped
  comparisons can benefit from it.
- A heading sits closer to the previous section than to the content it
  introduces. Bind it to its following content and distinguish within-group
  spacing from between-group spacing. Dense rows still need a visible relation.
- One maximum width governs prose, data, media, and controls despite their
  different space needs. A split first viewport leaves a tall empty column or
  pushes the primary action away from the explanation it belongs to.
- Decorative sparklines and charts imply evidence but do not support a decision.
- Modals become the default container for complex work that deserves inline
  space, a sheet, or a dedicated route. Keep a modal when consequential choice
  or genuinely necessary focus justifies interruption.
- The footer, final CTA, three pricing tiers, recommended-plan badge, or FAQ is
  filled from a page template. Build the close from real destinations and the
  next useful step, pricing from the actual offer, and questions from plausible
  user uncertainty. A real offer may justify a familiar structure.

Ask what information structure would remain if borders, icons, and labels were
removed. If the answer is nothing, redesign the hierarchy rather than replacing
one decoration with another.
