# Design Review and Modernization

Use this route to critique, modernize, polish, or quality-gate an existing
experience. Evaluate hierarchy, clarity, coherence, interaction cost, cognitive
load, preservation constraints, and whether the result is good enough to ship.

## Use First For

- Overall UI reviews, product surface critiques, redesign direction, and visual polish.
- Modernization under brand, content, route, analytics, and accessibility
  preservation constraints.
- Quality gates before shipping a frontend experience.
- Deciding which focused Effective Web route should handle a specific problem.
- Specialist interface judgment for a pull-request or branch delta whose Git
  scope has already been resolved by `effective-delivery`.

## Route Specific Work

Use Design Planning from the **Route by Intent** table in
[SKILL.md](../SKILL.md) for a greenfield direction or AI-assisted feature. When
a narrow problem (layout, typography, color, components, forms, tables,
accessibility, motion, SEO, CSS, i18n, copy, states, auth, print, performance,
React, or testing) becomes the primary task, hand off to the matching focused
route instead of expanding this one.

When `effective-delivery` supplies a resolved change scope, read
[Change-scoped interface review](change-scoped-interface-review.md) first. Keep
Git/provider state and the final PR decision with that discipline; return
browser-facing findings and verification rather than starting a second general
code review.

## Review Workflow

1. Reuse the accepted direction and project context; inspect design, content,
   brand, or component evidence needed to judge the requested change.
2. Use [Redesign preservation](redesign-preservation.md) when the work changes
   an existing visual or behavioral contract. Follow the authorized scope.
3. Identify the job-to-be-done, primary user, primary action, and failure modes.
4. Read [Cognitive UX](cognitive-ux.md) when the task involves attention,
   learnability, complex modes, unfamiliar concepts, or a mismatch between the
   system and what users expect. Check whether the UI has one clear information
   hierarchy and one clear next action per state. Remove elements that do not
   clarify, accelerate, reassure, express the intended relationship, or prevent
   mistakes.
5. For generic or agent-generated output, classify findings with
   [UI anti-patterns](ui-antipatterns.md). Fix objective defects first and treat
   stylistic tells as context-dependent advisories or clusters, not taste laws.
6. Route narrow issues through the **Route by Intent** table in
   [SKILL.md](../SKILL.md#route-by-intent) instead of expanding this route.
   Record new durable direction or communication decisions through
   `effective-product` rather than a tool-specific memory file.
7. Verify the rendered result and implementation against the accepted direction,
   redesign baseline when applicable, and quality gates before considering the
   UI done.

## Combine observations and measurements

For a broad critique, record your own observations before reading automated
style advisories when practical. This reduces anchoring on the detector's
vocabulary. Urgent defect evidence can still guide the investigation immediately.
Use the actual surface, accepted decisions, and task to form the assessment;
a screenshot or source file supports only the claims it can show.

Then reconcile observations with measurements and any other review: merge
duplicates, identify agreement, examine findings present in only one source,
and name false positives or unresolved contradictions. A detector-only signal
needs contextual evaluation; an observation without a detector match can still
be a material problem. Explain impact and the appropriate change rather than
combining unlike findings into an aggregate quality score. A second independent
review is useful when uncertainty or consequence warrants it; it is not a
mandatory role or fixed process for every refinement.

## Baseline Rules

- Every visible element needs a job. Decoration is acceptable only when it improves recognition, trust, orientation, or comprehension.
- Optimize for scanning first, then reading. Users should understand state, next action, and risk without decoding the layout.
- Keep interaction cost low: related controls belong near the content they affect, destructive actions need recoverability, and repeated workflows need density.
- Treat attention as a user resource. Interrupt only when urgency or otherwise
  missed consequential state justifies taking focus.
- Preserve autonomy when emphasizing a likely action, and prefer recognition
  over recall for routine, infrequent, or high-stress work.
- Do not make accessibility, responsive behavior, localization, or loading/error states late-stage patches.
- Prefer fewer stronger patterns over many local exceptions.

## References

Select by the primary concern of the current step; load one module, then add
another only when the work genuinely shifts concern.

| Primary concern | Reference |
|-----------------|-----------|
| Broad UI design decisions, quality heuristics, reduction, and restraint (load the deep appendix only for an identified edge case) | [fundamentals-core.md](fundamentals-core.md) |
| Modernizing an existing experience under preserve/overhaul contracts (brand, IA, copy, analytics, accessibility) | [redesign-preservation.md](redesign-preservation.md) |
| Reviewing generated UI and copy for defects, advisories, clusters, and accepted exceptions | [ui-antipatterns.md](ui-antipatterns.md) |
| Running the final review gates before shipping | [ui-quality-gates.md](ui-quality-gates.md) |
| Reviewing the interface effect of an already resolved pull-request or branch delta | [change-scoped-interface-review.md](change-scoped-interface-review.md) |
| Attention budgets, satisficing, task grouping, perceptual hierarchy, conventions, mental models, and learnability | [cognitive-ux.md](cognitive-ux.md) |
