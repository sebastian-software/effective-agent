# Color and Theming

Use this route for color decisions that affect usability, brand expression, accessibility, and maintainability.

## Workflow

1. Separate semantic roles from raw colors: text, surface, border, accent, danger, success, warning, focus.
2. Verify contrast for text, icons, borders that carry meaning, and focus states.
3. Build palette steps in a perceptually sane space such as OKLCH when supported by the project.
4. Test light mode, dark mode, high contrast, and forced-colors behavior.
5. Keep color usage purposeful: hierarchy, affordance, status, grouping, or brand signal.

## Rules

- Never rely on color alone to convey state or meaning.
- Keep semantic roles distinguishable even when the brand palette centers on one hue.
- Match brand-color coverage to the surface's register and hierarchy; use the distribution guidance in [colour-system.md](colour-system.md#choose-coverage-by-purpose).
- Dark mode is a separate contrast and elevation system, not an inverted light palette.
- Tokens should describe intent, not appearance.

## References

- [colour-accessibility.md](colour-accessibility.md) - contrast, status,
  interaction, and forced-colors evidence; read [colour-system.md](colour-system.md)
  for palette construction, tokens, and theming.
- [dark-mode.md](dark-mode.md) - dark mode implementation and pitfalls.
- [design-system-rules.md](design-system-rules.md) - token and design-system rules.
