# Typography Detail

Use this module after the type system is sound and the task concerns text
measure, spacing, numeric data, headings, or rich display copy.

## Text Mechanics

- Couple line height to role, font size, and actual measure. Use unitless line
  heights for inherited UI text unless a locally fixed value is intentional.
- Keep letter spacing at zero for normal lowercase body copy. Add tracking only
  for a deliberate uppercase, small-caps, or display treatment, then inspect
  the actual typeface.
- Enable kerning and appropriate OpenType features where the font supports them;
  use tabular figures for data that must align. Never fake bold or italic when a
  real face or a less emphatic treatment is available.
- Prevent heading widows where they materially damage scanning, but do not add
  brittle manual line breaks that fail under translation and resize.

## Paragraph Rhythm

For sustained prose, choose a primary paragraph boundary: interparagraph space
or first-line indentation. Both together usually repeat the same signal; keep
the combination only when it serves a deliberate editorial distinction.

With indentation, the first paragraph after a heading can remain flush left,
since the heading already marks its beginning. Scope the treatment to the prose
component; labels, lists, callouts, and short UI messages need their own spacing.
Judge the result with the actual font and reading measure rather than importing
a fixed print indent or applying a global `p` rule.

## Contrast and Overlays

- Ensure text on an image has a stable contrast mechanism: a tested overlay,
  solid surface, crop choice, or alternate composition. Do not rely on a lucky
  portion of one marketing image.
- Avoid thin, low-contrast, or pure-light-gray interface text. Test zoom, dark
  mode, loading fallback, and long localized strings.

For punctuation and spacing rules of a specific language, route the decision to
`effective-writing`. For editorial and display edge cases, consult the [deep
typography appendix](typography.md).
