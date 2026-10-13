# Release Notes

Release notes explain what a release changes for its intended audience. Follow
the project's release format, attribution policy, tooling, and audience.
Launch announcements and promotional copy belong to `effective-marketing`.

## Verify the change and its effect

- Establish the release range and intended audience from the request and the
  repository's release conventions. Use commit subjects to locate changes, not
  as evidence of their effect.
- Inspect the changes in the range and trace each proposed claim to the released
  implementation or another authoritative source. Describe the observed effect
  for readers who use, operate, or integrate with the product.
- Include an internal change when it affects the release's audience, such as an
  operator or integrator. Do not include or exclude a change solely because it
  is code, tests, documentation, or infrastructure.
- Attribute an indirect fix through a dependency only when the relevant
  upstream change and its effect in this repository are supported by evidence.
  Use the [upstream research](dependency-workflow.md#5-upstream-research) and
  [local impact](dependency-workflow.md#6-local-impact-analysis) steps of the
  dependency workflow. A version bump or a nearby upstream note alone does not
  establish that the release fixes a local problem.

## Write and review

State the supported outcome in concise, audience-relevant language. Keep the
project's established grouping and release tooling when they apply; add
structure only when the project expects it or readers need it to scan the
changes.

Review every claim against the full range and its evidence. Remove claims based
only on a commit subject, label, or unsupported causal link. If the range has no
notable effect for the intended audience, use the project's no-change wording,
such as “No notable changes.”
