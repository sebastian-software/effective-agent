# Internationalization UX

Use this route when UI must survive translation, locale changes, longer strings, bidirectional text, or different formatting conventions.

## Workflow

1. Identify supported locales, scripts, directionality, and formatting requirements.
2. Replace layout assumptions based on English string length.
3. Use locale-aware formatting for dates, numbers, currency, addresses, and names.
4. Check RTL mirroring for layout, icons, navigation, and directional language.
5. Verify truncation, wrapping, pluralization, sorting, and search behavior.

## Rules

- Do not concatenate translated strings from fragments with fixed order.
- Avoid text embedded in images or icons when it must be localized.
- Use logical CSS properties where direction can vary.
- Let translated strings wrap; containers must not depend on exact wording.
- Keep source copy clear enough for translators to preserve intent.

## References

- [i18n-rtl.md](i18n-rtl.md) - RTL and international layout concerns.
- [i18n-ux.md](i18n-ux.md) - localization, formatting, and translation-safe UX rules.
