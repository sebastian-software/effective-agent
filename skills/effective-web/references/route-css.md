# CSS Architecture

Use this route for making CSS maintainable, predictable, and compatible with the project's browser-support promise.

## Workflow

1. Identify styling ownership: global reset, tokens, layout primitives, components, utilities, overrides.
2. Define cascade order explicitly with layers or local conventions.
3. Identify the canonical token source and the reference, semantic, and narrow
   component-token boundaries; use custom properties for the web-facing
   semantic contract and runtime theming.
4. Choose progressive enhancement boundaries based on the supported baseline.
   Check the dated feature radar when the model may not know the current
   platform, and promote useful Newly available features with an honest fallback.
5. Keep build tooling simple enough that generated CSS remains debuggable.

## Rules

- Avoid specificity arms races; solve ordering and scope instead.
- Do not encode semantic state only in class names when native state or attributes fit better.
- Gate modern CSS with feature queries when unsupported behavior would break the UI.
- Prefer readable source CSS over clever generated output.
- Document exceptions in the local component or token contract, not as global folklore.

## References

- Choose one primary concern: [css-cascade.md](css-cascade.md) for layers,
  selectors, and scope; [css-tokens.md](css-tokens.md) for semantic tokens and
  theming; or [css-organization.md](css-organization.md) for ownership, entry
  points, and generated output. Each links the deep appendix only for an
  identified edge case.
- [baseline-support.md](baseline-support.md) - browser baseline and support decisions.
- [platform-feature-radar.md](platform-feature-radar.md) - dated leads for recent
  Baseline features that older model knowledge may miss.
- [css-build-tooling.md](css-build-tooling.md) - CSS build tooling and generated output rules.
- [design-system-rules.md](design-system-rules.md) - token architecture,
  consumer boundaries, theming, governance, and system-wide review checks.

If the primary concern becomes responsive layout, typography, component
behavior, visibility semantics, accessibility, or final UI review, switch
through [Route by Intent](../SKILL.md#route-by-intent). Add this CSS route only
when cascade, token, ownership, support, or tooling decisions are also in scope.
