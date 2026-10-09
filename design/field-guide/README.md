# Field Guide implementation

The selected direction is Concept 02, **The Field Guide**. The website is
implemented in `site/`, with reusable identity assets and an OSS application
study in this directory.

## Identity and composition

Use warm ivory, forest ink, and terracotta actions. The book-and-compass mark
represents guidance and direction; it contains no skill count. Product lockups
use **Effective Agent** without an issuer subtitle. Corporate attribution lives
in the About copy and legal footer. On the Sebastian Software OSS site, place
this mark inside the product feature and preserve the corporate masthead.

The collection is intentionally open-ended. No illustration assigns a named
volume to every current skill or depends on having exactly seven volumes.
Tiny print, code-like passages, checklists, and diagrams make the books feel
used. These details are decorative texture, not product instructions or content
visitors need to read. Primary content and current inventory stay in HTML.

The final desk scene replaces decorative plants and botanical drawings with
coffee, glasses, index cards, paper clips, and technical diagrams. Books remain
the primary subject; the compass and fountain pen keep the Field Guide theme.

## Asset provenance

Generated with the built-in Imagegen tool using the selected board as a style
reference, followed by targeted edits. The final asset is
[`field-guide-desk.png`](../../site/assets/illustrations/field-guide-desk.png),
a 1536 × 1024 PNG with alpha transparency. The scene uses overlapping books and incidental miniature content rather than
a fixed set of labeled skill volumes.

- [Miniature typography prompt](hero-prompt.txt)
- [Desk refinement prompt](desk-edit-prompt.txt)

The prompts use actual skill principles as inspiration. Generated fine print
is not a verbatim rendering of source references and does not need translation
for the surrounding interface to work.

The SVG product marks are native vector artwork derived from the chosen
book-and-compass concept. The Sebastian Software corporate marks remain
unchanged. See [asset documentation](../../site/assets/README.md) for variants,
font licensing, and repeatable favicon/social-preview rendering.

## Review surfaces

- [`site/index.html`](../../site/index.html): implemented homepage.
- [`index.html`](index.html): identity variants and an OSS feature application.
- All seven skill detail pages and the comparison page use the same product
  identity, typography, light/dark palettes, and simplified navigation.

The existing browser suite covers nine pages at seven widths in both color
schemes, including skill filters, keyboard-operated use-case tabs, copy
commands, optional instruction disclosure, and skill-detail navigation.

## Detail pages

Skill pages extend the editorial direction with numbered chapters, a margin
index, source-derived reference counts, an unboxed first-task panel, quotation
style examples, and a focused install section. Existing URLs, section anchors,
copy-button targets, instructions, and related-skill links are preserved. The
comparison page uses the same type, rules, and restrained surfaces; its pinned
source review remains dated July 23, 2026.
