# Route: Locale Typography

Produce typography that belongs to the reader's locale without turning the task
into a grammar, translation, or house-style rewrite. Applies to visible prose in
any medium: Markdown, HTML, JSX, templates, UI copy, documents, and print.

## Workflow

1. Determine the locale from an explicit locale tag, the document's `lang`,
   product configuration, or the stated audience. Never infer one language from
   a multilingual country alone.
2. Preserve an established house style when it intentionally differs from the
   locale default. Preserve punctuation inside verbatim quotations unless the
   user asks to normalize it.
3. Consult [Shared rules](locale-shared-rules.md) when source protection,
   character choices, line breaking, or locale-aware data need guidance. Use the
   [locale matrix](locale-matrix.md) when the language-to-region mapping is unclear.
4. Read only the matching language profile listed below. Load more than one
   profile only for mixed-language content.
5. For web or application code, also read
   [implementation](locale-implementation.md). Delegate dynamic numbers, units,
   currency, dates, times, lists, and plurals to locale-aware APIs.
6. Apply changes only to visible prose. Do not alter code, identifiers, URLs,
   file paths, commands, data keys, attribute values, or copy-paste literals.
7. Review nested quotations, punctuation adjacency, line-breaking hazards, and
   locale tags before finishing.

If the locale remains ambiguous and the choice would visibly change the result,
ask for it. For low-risk work, state the assumed locale briefly and continue.

## Language profiles

- [German](locale-german.md): `de-DE`, `de-AT`, `de-CH`, `de-BE`, `de-LU`
- [English](locale-english.md): `en-US`, `en-GB`, `en-CA`
- [French](locale-french.md): `fr-FR`, `fr-CA`, `fr-CH`, `fr-BE`, `fr-LU`
- [Dutch](locale-dutch.md): `nl-NL`, `nl-BE`
- [Luxembourgish](locale-luxembourgish.md): `lb-LU`
- [Spanish](locale-spanish.md): `es-ES`
- [Italian](locale-italian.md): `it-IT`, `it-CH`
- [Danish](locale-danish.md): `da-DK`
- [Norwegian](locale-norwegian.md): `nb-NO`, `nn-NO`
- [Swedish](locale-swedish.md): `sv-SE`
- [Polish](locale-polish.md): `pl-PL`
- [Czech](locale-czech.md): `cs-CZ`
- [Croatian](locale-croatian.md): `hr-HR`

The language list is for selection. One matching profile normally suffices;
load shared or implementation guidance only for the issues involved.

## Boundaries

- Correct typography and locale-sensitive presentation, not spelling, grammar,
  translation, tone, or general content style unless requested.
- When translation revision is requested, use
  [Revise translated prose](locale-shared-rules.md#revise-translated-prose) for
  language-level choices; this route still owns locale typography.
- Encode durable rules and frequent error cases, not a complete national style
  manual.
- Treat locale defaults as defaults, not universal law. Product terminology,
  legal requirements, quoted source material, and an explicit house style win.
- Do not hand-format dynamic locale data. Use `Intl`, ICU, CLDR-backed
  libraries, or the platform equivalent and test the exact runtime.
- Do not insert manual soft hyphens throughout prose. Prefer correct language
  metadata and automatic hyphenation; add discretionary breaks only for known,
  reviewed exceptions.
- Localization UX — RTL, text expansion, and locale-aware formatting inside a
  browser experience — belongs to `effective-web`. This route owns the
  language-level convention itself in any medium.
