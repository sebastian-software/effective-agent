# Shared rules

Apply these rules before a language profile. The profile wins wherever it is
more specific.

## Protect meaning and source text

- Change only rendered prose unless the user explicitly requests source-code
  normalization.
- For markup or templates, use the consuming format to distinguish prose from
  syntax and preserve the escaping semantics it requires.
- Preserve exact quotations, legal names, trademarks, identifiers, URLs,
  commands, and machine-readable values.
- Keep punctuation that belongs to a quotation inside it and punctuation that
  belongs to the surrounding sentence outside it unless the language profile
  or house style uses a conventional exception.
- Preserve a coherent existing house style. Do not create mixed quote or dash
  systems inside one document.

## Revise translated prose

Use the target project's existing locale settings, house style, and terminology.
Preserve intent and register without copying source word order; keep unrelated
target passages unchanged. If the source and local context leave a material
language choice unresolved, surface the uncertainty rather than inventing an
approved term or parallel glossary.

## Use the right character

| Purpose | Character | Rule |
| --- | --- | --- |
| Hyphen or compound | `-` | Keep attached to the joined words. |
| En dash | `–` | Use for ranges or parenthetical dashes only where the profile says so. |
| Em dash | `—` | Use only where the locale or house style calls for it. |
| Minus | `−` | Use for mathematical subtraction and negative values in typeset math. |
| Ellipsis | `…` | Prefer the single glyph in typographic prose when the locale and house style accept it. |
| Apostrophe | `’` | Use for linguistic apostrophes and elisions; do not substitute a prime. |
| Prime | `′` / `″` | Use for measurements such as feet, inches, minutes, and seconds of arc. |
| Multiplication | `×` | Use for dimensions and multiplication, not the letter `x`. |
| Non-breaking space | U+00A0 | Keep inseparable tokens on one line without changing visible width. |
| Narrow no-break space | U+202F | Use only where the locale or publishing system expects narrow spacing. |

Do not replace ASCII punctuation inside code. Do not run blind smart-quote
replacement over Markdown, HTML, JSX, templates, or structured data.

## Line breaking

- Keep a number with its unit or currency marker when the locale places them
  next to each other.
- Keep initials, section symbols, short function words, and other tokens
  together only where the language profile identifies a real convention.
- Use a non-breaking space for semantic binding. Do not use a visual thin space
  when a line break would still be possible.
- Avoid non-breaking spans so long that they overflow narrow layouts.

## Locale data

- Format numbers, percentages, currencies, measurements, dates, times, relative
  time, and lists with locale-aware APIs.
- Do not derive a decimal separator, grouping separator, currency placement, or
  date order from language alone; use the complete locale.
- Keep user-entered values separate from their localized display strings.
- Never parse a localized display string back into business data without a
  locale-aware parser and explicit validation.

## Sources

- [Unicode CLDR: delimiters](https://cldr.unicode.org/translation/core-data/characters)
- [Unicode CLDR: number and currency patterns](https://cldr.unicode.org/translation/number-currency-formats/number-and-currency-patterns)
- [W3C Internationalization: language declarations](https://www.w3.org/International/questions/qa-html-language-declarations)
