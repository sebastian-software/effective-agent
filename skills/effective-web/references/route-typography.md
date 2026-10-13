# Typography

Use this route for typography in digital interfaces. It covers type choice, hierarchy, rhythm, readable measure, webfont behavior, and the small text decisions that make UI feel professional.

## Workflow

1. Identify the reading mode: scanning UI, dense data, long-form content, marketing copy, or form completion.
2. Choose a restrained type system: usually one family, two or three weights, and a predictable scale.
3. Set body size, line-height, and line length before tuning headings.
4. Ensure labels, buttons, captions, and helper text remain readable at real device sizes.
5. Check fallback fonts, loading behavior, and layout shift.

## Rules

- Do not scale font size directly with viewport width.
- Keep letter spacing at `0` unless using uppercase, small caps, or a deliberate display treatment.
- Avoid thin low-contrast text in UI.
- Reserve hero-scale type for true heroes; compact panels need compact headings.
- Use typographic hierarchy to reduce explanation, not to add decoration.

## References

- [typography-system.md](typography-system.md) - roles, scale, readable text,
  fallback behavior, and loading; read [typography-detail.md](typography-detail.md)
  only for measure, numeric, display, or overlay concerns.
- [webfonts.md](webfonts.md) - webfont loading, fallbacks, and performance.
- [typography-rules.md](typography-rules.md) - practical typography implementation rules.
- [line-height-and-measure.md](line-height-and-measure.md) - couple leading to
  typeface, text role, font size, actual measure, CSS inheritance, and WCAG.
