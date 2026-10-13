# Review Judgment

Use for a full PR review or an unresolved technical question during upkeep.
The [Review route](route-review.md) owns scope and authority. Mode C uses only
its supplied evidence and separate handoff contract.

## Establish the Change Boundary

Review the provider's PR delta. Record base and head refs or SHAs, the merge
base when working locally, and material exclusions. Do not blend dirty or
unpushed checkout changes into the submitted PR. If the user asks for both,
identify each evidence surface separately.

Inspect additions, modifications, renames, and deletions. Compare removed
safeguards, states, validation, compatibility paths, and side effects with the
base and their current replacements before calling a regression. Deletion by
itself proves neither loss nor preservation.

Distinguish findings introduced by the change, regressions from demonstrated
base behavior, and pre-existing issues. Only the first two determine the PR
decision. Mention consequential existing issues separately without making
unrelated repairs a merge condition. When origin is uncertain, obtain the
smallest decisive base evidence or state the uncertainty.

## Understand and Inspect the Change

Establish intent from the description, linked ticket, diff, and other available
requirements. A missing ticket link does not prevent review when intent is
clear. Keep any genuinely missing acceptance evidence visible, and continue
the judgments it does not affect.

Use these questions where they apply; their order is not a gate sequence:

- Does the change deliver its stated outcome without unnecessary scope? New
  variants, themes, controls, or flows need the states required by their
  contracts, including relevant focus, loading, failure, localized, or narrow
  states. Missing requested behavior is incomplete delivery.
- Does a changed signature or contract affect actual consumers? Use
  [codebase context](codebase-context.md) when relationship resolution is
  needed. Resolve real call sites rather than inventing hypothetical callers.
- Are the implementation and abstractions proportionate? A little duplication
  can be cheaper than an abstraction with no demonstrated reuse.
- Do documentation, tests, and the PR description explain or protect the
  consequential behavior? Missing docs or tests block only when their absence
  leaves a concrete risk or makes intent impossible to assess.
- Do affected accessibility, performance, operability, observability, and
  recovery boundaries remain sound? An inaccessible core flow, unbounded hot
  query, or silent data loss is consequential regardless of category.

If product direction is questionable, identify the unresolved decision and its
effect. Do not invent acceptance criteria or withhold unrelated technical
findings while waiting for that decision.

For specialist browser judgment, use `effective-web` when available and needed.
Pass the resolved base/head delta, affected components, removed signals,
relevant code relationships, UI intent, preview availability, and candidate
evidence. Keep publication and the final PR recommendation here. When specialist
depth is unavailable, disclose a material gap and use a bounded repository-led
fallback where sufficient.

## Find, Then Filter

Inspect relevant behavior before filtering findings for publication. Establish
the supported trigger, affected behavior, consequence, recovery, and, where
evidence permits, exposure or lifetime. Compare avoided harm with the smallest
credible fix's implementation, cognitive, test, maintenance, and regression
cost. A technically possible sequence is not automatically worth changing.
Do not invent probabilities.

Money, authorization, security, privacy, data integrity, destructive operations,
required accessibility, and regulated behavior justify a lower evidence
threshold. Resolve material uncertainty at those boundaries before recommending
approval. Several reviewers repeating one suspicion are not independent proof.

Consolidate shared root causes. Omit taste and speculative cleanup or mark them
clearly optional. A clean review can have no findings. Do not impose a finding
quota or suppress a blocker to keep a report short. State inspected scope and
material exclusions when the review is partial.

## Recommend a Decision

- Recommend approval when no material merge risk remains. Optional suggestions
  do not become conditions for approval.
- Recommend changes for a concrete, reachable merge risk, such as a tenant
  bypass, billing error, unsafe migration, severe regression, or inaccessible
  primary flow. Require only what closes that risk.
- When consequential evidence is missing, name the affected judgment and the
  smallest proof or decision needed. Preserve useful findings from the rest of
  the review.
- An independent second look can help with a distinct unresolved risk or broad
  scope. Do not treat reviewer count as a quality gate.

A recommendation is not permission to submit a provider review. Apply the
Review route's authority boundary before publishing it.

## Communicate the Finding

For each actionable comment, make the location or symbol, concrete defect,
consequence when non-obvious, and smallest useful correction recoverable.
Anchor to a changed line where supported; explain consequential unchanged
callers in the review body when an inline anchor is unavailable. Expand enough
for security, data-loss, architectural, irreversible, or onboarding-sensitive
advice to remain unambiguous.

Lead with the material findings and decision evidence. Recognize a concrete
strength when useful without manufacturing praise or hiding a blocker. For
prose addressed to an author, apply the [review route's Metro English
default](route-review.md#voice). Use [review voice](review-voice.md) only when
PR-specific wording or placement needs calibration. Keep the report in the
requested format.
