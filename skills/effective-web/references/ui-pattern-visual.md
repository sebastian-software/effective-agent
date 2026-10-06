# Visual Pattern Review

Use this module for suspected generic choices in type, palette, surfaces, media,
and icons. Apply the context and evidence distinction in
[UI anti-patterns](ui-antipatterns.md).

## Visual and Typographic Reflexes

- Cream, beige, purple gradients, cyan-on-dark, or a dark dashboard are category
  defaults unless the physical context, brand palette, or content demands them.
- Gradient text, decorative glass, neon glow, blurred orbs, generic diffuse
  shadows, grid overlays, or repeating stripes accumulate without an
  information, depth, or interaction role.
- A long sentence is enlarged to display scale until it dominates or overflows
  the first viewport. Match type scale to copy length and available measure.
- Display tracking is crushed until glyph shapes or word recognition suffer.
- An italic serif hero is used as shorthand for premium or editorial quality.
  Keep it when the chosen direction or accepted visual system genuinely owns
  that voice.
- Monospace is used to make an unrelated product appear technical rather than
  for code, identifiers, aligned data, or a documented brand voice.
- One familiar font is blamed for generic output even though hierarchy, role,
  optical sizing, weight, measure, and content are the actual problems.
- Heading, body, label, and data roles differ too little to carry hierarchy, or
  small text, long uppercase passages, tight leading, and extreme tracking make
  the real copy difficult to read. Verify the actual face, language, viewport,
  and content rather than enforcing a universal display-size ceiling.
- Text colour is chosen from a rule against grey rather than the actual
  background and role. A hue-related neutral can fit a palette; sufficiently
  contrasting grey is also valid. Verify the rendered pair in each state.
- Colours and accents compete without assigned roles. Several accents can serve
  data or rich states; a universal one-accent rule would erase those roles.

Do not maintain a blacklist of fonts, colours, or effects. Judge whether the
combination follows the owning system and creates a distinctive, usable result.
Do not default to Inter or Roboto merely because they are convenient; preserve
them when the brand, product system, or reading context deliberately uses them.
Use [Typography Detail](typography-detail.md) for wrapping, measure, tracking,
numeric alignment, and language-appropriate case.

## Media and Icon Reflexes

- Stock photos, Corporate Memphis figures, rockets, abstract 3D objects, or
  decorative terminals replace evidence about the actual product. Select media
  for what it explains or expresses; a coherent abstract brand or a typography-
  led page can be valid, and a real developer tool can use a terminal.
- A primitive illustration or approximate organic mask is accepted because it
  satisfies a request for an asset. Inspect its contours, perspective, lettering,
  anatomy, and intended material. SVG and CSS are media choices, not evidence
  of poor quality; good vectors and deliberate geometric work remain valid.
- An opaque wash hides the image while its file still loads. Preserve enough
  visible image to serve its purpose, use a local contrast treatment, or remove
  an unnecessary asset. A broken image or unintended artifact needs correction.
- Emoji, Unicode substitutes, sparkles, or inconsistent icon families make
  every function look alike. Match meaning, stroke, weight, and style to the
  owning system; an intentional emoji vocabulary can be appropriate.
- A floating browser mockup or invented chart decorates a product section
  without showing a use case. Show a meaningful workflow or clearly mark a
  concept view. A mockup is evidence only for what it actually represents.
