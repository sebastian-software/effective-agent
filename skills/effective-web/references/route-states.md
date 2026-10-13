# Error and Loading States

Use this route for the states users see while work is pending, unavailable, failed, empty, partial, or complete.

For the words inside those states — labels, messages, button text — use
**Interface Copy** ([route-copy.md](route-copy.md)) instead. This route owns
which states exist, their structure, and their behavior.

## Workflow

1. List every state: initial, loading, empty, partial, success, validation error, network error, permission error, not found, fatal.
2. Preserve layout stability across states.
3. Give users honest progress and a recovery path when recovery is possible.
4. Keep state copy specific and close to the affected region.
5. Verify retry, refresh, back navigation, and offline behavior where relevant.

## Rules

- Skeletons must match final layout closely enough to prevent reorientation.
- Spinners are acceptable only for short, uncertain waits or compact controls.
- Errors need cause, impact, and next step at the right level of detail.
- Empty states should not blame the user or over-explain the product.
- Success states should confirm meaningful completion, not celebrate routine clicks.

## References

- [loading-states.md](loading-states.md) - loading, progress, and skeleton patterns.
- [error-pages.md](error-pages.md) - error page and recovery patterns.
