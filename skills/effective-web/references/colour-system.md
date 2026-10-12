# Color System and Theming

Use this module to create a palette and token system that can serve brand,
interaction, dark mode, and future components without turning values into
untraceable folklore.

## Build from Roles

1. Define the semantic roles and the contrast relationships they must preserve.
2. Create primitive steps in a perceptually useful space such as OKLCH when the
   browser-support policy permits it.
3. Map semantic tokens to those primitives, then expose only narrow component
   tokens where a consumer needs a real contract.
4. Design dark mode as its own contrast and elevation system; do not simply
   invert the light palette.

- Use relative color syntax, wide-gamut values, and `light-dark()` as progressive
  enhancements with a tested fallback. Keep a stable sRGB path when it is part
  of the product baseline.
- Use translucency and shadows to express elevation sparingly. A surface should
  remain distinguishable when transparency, backdrop effects, or color features
  are unavailable.
- Document semantic ownership and migrate hard-coded values deliberately rather
  than adding another near-duplicate token.

## Choose Coverage by Purpose

Color roles and color coverage are separate decisions. Choose distribution to
support the register, hierarchy, and identity:

| Approach | Useful when | Preserve |
| --- | --- | --- |
| Mostly neutral surfaces with focused accents | Repeated tasks or sustained reading need a quiet field | Distinct action, focus, and status cues |
| A brand-colored header, section, or feature background | Identity or narrative needs a visible region | Tested foreground pairs and recognizable controls inside the region |
| Multiple role colors | Categories, data series, or states need differentiation | Stable meanings and non-color cues |

These approaches can coexist. A broad brand surface is not automatically better
than a small accent, and a single brand hue does not require every semantic role
to share it. Do not impose surface-percentage targets or add colors just to fill
a palette. Keep error, warning, success, and focus meanings distinct from
decorative brand regions.

For tonal-gradient math, palette recipes, and specialized elevation patterns,
consult the [deep color appendix](colour.md).
