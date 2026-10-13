# Typography Rules

Use this reference for typography decisions: readable measure, wrapping, fluid sizing, local units, editorial rhythm, and text rendering details.

## Working Rules

- Keep body text readable before applying decorative type behavior.
- Use modern wrapping tools on short headings and compact labels only when they improve scannability.
- Use fluid sizing with zoom and user preferences in mind.
- Align icons, decoration, and local spacing to the type context rather than to arbitrary pixels.
- Name shared type tokens by role (`text-body-sm`, `text-label`,
  `text-display`) when a team needs usage rules; use size-only names only when
  their intended roles are already unambiguous. Keep the number of roles,
  families, sizes, and weights deliberately small.
- Prefer the high-level CSS property for registered variable-font axes and
  OpenType features: use `font-weight`, `font-stretch`, `font-style`,
  `font-optical-sizing`, and `font-variant-*`. Reserve
  `font-variation-settings` and `font-feature-settings` for custom axes and
  features that have no dedicated property, so fallbacks retain the intended
  behavior.
- Set `font-synthesis: none` at the root as a deliberate quality default, then
  load every weight and style the interface uses. Treat missing bold or italic
  as an asset/configuration defect to fix rather than silently accepting faux
  glyphs; verify fallback and failure states so hierarchy remains legible while
  fonts load or fail.
- Let link underlines use the font's metrics where available with
  `text-underline-position: from-font` and
  `text-decoration-thickness: from-font`; retain
  `text-decoration-skip-ink: auto`, and tune offset or thickness only when the
  typeface or interaction treatment needs it.
- Use `rem` for global scale decisions and `em`/font-relative units for local component relationships such as icon size, padding, inline gaps, badges, and decorations.
- Prefer `clamp()`-based fluid type within bounded ranges; avoid unbounded viewport-unit type that ignores zoom, user preferences, or narrow/large extremes. Keep at least one term of a fluid `font-size` in a zoom-respecting unit (`rem`/`em`) so text still scales with the browser zoom and default-size settings; never express it in `vw` alone.
- Use `text-wrap: balance` for short headings, card titles, tooltips, modal headings, and FAQs. Do not apply it blindly to long body text or performance-sensitive large blocks; many engines stop balancing after a small number of lines (around 6 in Chromium) and it must not be relied on to change an element's width.
- Use `text-wrap: pretty` for long-form paragraphs to suppress orphans and improve last-line breaks. Treat it as progressive enhancement (support is still uneven across engines and absent in Firefox as of October 2026), and let it degrade to normal wrapping where unsupported.
- Use `cap` and `rcap` units to size and align type-relative decoration — icons, leading bullets, spacers, and inline buttons — to the cap height of the surrounding text instead of guessing pixels. Provide a pixel or `em` fallback for older engines, since `cap`/`rcap` are recent additions.
- Use `font-size-adjust` to hold perceived text size constant across a webfont swap or a serif/sans mix by pinning the x-height ratio, which removes the size jump and reflow when the fallback is replaced.
- Treat text-box trimming (`text-box-trim` / `text-box-edge`, formerly proposed as `leading-trim`) as the precise way to remove the half-leading above cap height and below the baseline so headings and buttons align to their glyphs rather than their line box. Support now spans all three engines (Safari 18.2, Chromium 133, Firefox 154), but Baseline still lists it as Limited availability as of October 2026; gate it behind `@supports` and keep manual optical padding as the fallback.
- For editorial or CMS content, define vertical rhythm from semantic structure rather than arbitrary spacing after every element. Express rhythm with low-specificity selectors — e.g. `:where(h2, h3, p, ul, ol, blockquote, figure)` for the base step and `:has()` for context-sensitive gaps (a heading immediately followed by a paragraph, or a figure between paragraphs) — and reset the first/last child edges so sections do not accumulate stray margins.
- Set measure by content role: paragraphs, lists, captions, and quotations often
  need a narrower readable measure than display headings, tables, code, or media.
  Do not apply one `max-inline-size` indiscriminately to every prose child.
- Treat typeface, text role, font size, actual measure, and line height as one
  system. Longer reading lines often need more leading, while larger display
  sizes usually need a smaller unitless ratio. Prefer role-specific unitless
  values or measure-aware unitless steps; use a smooth length-based formula only
  with its container-unit and inheritance tradeoffs understood. Read
  [line-height-and-measure.md](line-height-and-measure.md).
- For user-authored, translated, or CMS text, combine the correct document
  language with `hyphens: auto` where appropriate and an emergency
  `overflow-wrap` strategy for URLs, identifiers, and long unbroken words. Test
  the longest supported locales; hyphenation without the correct `lang` is not a
  reliable overflow solution.
- Stress-test unusually tight display leading with real ascenders, descenders,
  multiple lines, fallback fonts, zoom, and narrow containers. A visually flat
  line-height is acceptable only when glyphs never collide or clip.
- When inline code, highlights, or badges can wrap, use
  `box-decoration-break: clone` where each line fragment needs its own padding,
  background, and border. Keep a readable no-clone fallback and test copied text
  and selection rather than forcing the inline content onto one line.

## Typography Review Checklist

- Are type sizes bounded at minimum and maximum values, and do they still work at browser zoom?
- Is the line length readable for the content type, especially when media or full-bleed layouts are present?
- Do icons, counters, badges, and inline controls align to the font metrics rather than arbitrary pixel centers?
- Are heading wraps intentional, balanced, and still searchable/copyable text?
- Do shared type tokens express their role, and do standard axes/features use
  resilient high-level properties instead of unnecessary raw tags?
- Are all requested weights and styles loaded under the root
  `font-synthesis: none` policy, including fallback and font-failure states?
- Do link underlines follow the font metrics without cutting through glyphs or
  weakening the link affordance?
- Does long-form content keep rhythm across headings, paragraphs, lists, quotes, figures, and first/last child edges?
- Do prose measures reflect content roles, and do long localized words, URLs,
  and identifiers wrap without breaking the layout?
- Was line height tuned after the real typeface, role, font size, and measure,
  and does any dynamic formula use valid CSS types plus the intended ancestor
  query container?
- Does tight display leading survive glyph, fallback-font, zoom, and multiline
  stress cases?
- Are newer text metrics features guarded or treated as progressive enhancement?
