# I18n UX

Design global interfaces so language, country, currency, units, timezone, direction, and shipping/payment context can differ. Inferred locale is a starting point, not a command.

## Working Rules

- Separate language choice from country, region, currency, units, timezone, tax, legal region, and fulfilment context; keep them independent unless the product domain explicitly ties them together.
- Treat an inferred locale (from `Accept-Language` or IP geolocation) as a default, never a lock. Never force a redirect based on it, and always expose an override the user can set and that persists.
- Preserve the user's current task and in-progress state when they switch language or region; do not reset the page, form, or position.
- Identify every locale with a BCP 47 language tag and drive all formatting from it through `Intl` (dates, numbers, currency, lists, relative time).
- Make locale controls discoverable, reversible, keyboard-accessible, and screen-reader-friendly. Label languages in their own endonym (`Deutsch`, not `German`) and set `lang` plus `dir` on the option so each name renders in its own script.
- Support translated text expansion, RTL, and changed reading order; test forms, navigation, tables, and component labels with long translated strings.
- Build messages from placeholders that translators can reorder; never assemble a sentence by concatenating translated fragments in a fixed source order.
- Never let truncation remove the only part of a label or option that distinguishes it from its siblings.
- Keep data-grid headers able to identify their cells after responsive transformation (stacked or card layouts), alongside locale-aware alignment and number formatting.
- Localize form input examples, placeholders, address structure, name and phone-number fields, postal codes, and validation copy per locale.
- Delegate the choice of quotation marks and other locale-specific punctuation to the `effective-writing` skill; implement the chosen marks with CSS rather than literal characters in copy — declare `quotes` per language with `:lang()` and emit `<q>` or `quotes`-aware content so the browser inserts the correct marks for each locale.

## Update existing UI messages

Read the changed source and matching target alongside the target project's
existing locale settings and terminology. Update only the affected message.
Identify the message's syntax and how the project processes it. Text can contain
custom placeholders, formats such as ICU, HTML markup, entities, or escape
sequences. Separate translatable prose from syntax and functional values.
Preserve variable identities and meaning. Where the format supports plural or
select branches, provide the cases required by the message contract and target
locale. Preserve HTML and other structural markup, and functional attributes or
URLs according to the consumer. Translate human-facing text,
including intended values in attributes such as `alt`, `title`, or
`aria-label`. Reorder variables only when the format supports it. Preserve
entity and escaping semantics for the consumer: equivalent entity and literal
spellings are fine when they render the same meaning, but blindly decoding
escaped literal markup can turn displayed text into active structure. Use
existing tooling or inspect the rendered message when proportionate to check
changed meaning, formatting, text expansion, plural, direction, markup, or
attribute behavior.
