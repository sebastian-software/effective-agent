# Forms UX

Use this route for forms as task flows: helping users enter correct information quickly, recover from mistakes, and understand what happens next.

## Workflow

1. Identify the user's intent, required data, optional data, and irreversible consequences.
2. Remove fields that are not needed at this step.
3. Group fields by meaning and keep the primary path single-column unless data density requires otherwise.
4. Choose validation timing by cost: immediate for format guidance, submit-time for complex business rules.
5. Make errors specific, local, recoverable, and persistent until resolved.

## Rules

- Labels belong above fields for predictable scanning.
- Field width should reflect expected input where that helps comprehension.
- Required and optional states must be clear; do not make users infer them.
- Disabled controls need explanation or an alternate path when users expect availability.
- Preserve entered data across errors, navigation, and refresh where possible.
- Consider Baseline 2026 `field-sizing: content` for auto-growing text fields;
  bound the size and keep the fixed-size behavior as a coherent older-browser path.

## References

- [forms.md](forms.md) - baseline form layout and field rules.
- [forms-ux.md](forms-ux.md) - validation, completion, and edge cases.
- [platform-feature-radar.md](platform-feature-radar.md) - recent interoperable
  form and control capabilities an older model may not know.
