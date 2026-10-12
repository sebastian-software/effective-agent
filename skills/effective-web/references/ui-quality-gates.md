# UI Quality Gates

Use the categories relevant to the changed surface and its reachable user risks.
Reuse existing evidence; a small presentation change may need only required
repository checks and one focused rendered inspection. Mark assessed categories
as `blocked`, `risky`, or `acceptable`, and distinguish unverified claims. These
are severity judgments, not numerical design scores.

## UI Gate

| Category | Blocked | Risky | Acceptable |
|----------|---------|-------|------------|
| Accessibility | WCAG AA blocker, keyboard trap, missing labels on critical controls, unreadable contrast | Minor ARIA gaps, weak focus styling, unclear alt text | Keyboard, semantics, labels, focus, contrast, target size, and announcements are covered |
| Responsive layout | Horizontal overflow, unusable mobile layout, clipped primary action, text that cannot fit | Awkward spacing, density, or ordering at one breakpoint | Continuous resize, short and narrow viewports, zoom, long text, and touch input work |
| Performance | Implementation choice likely breaks LCP, INP, CLS, or interaction responsiveness | Heavy assets, expensive animation, or unbounded rendering need verification | Critical assets, layout stability, and interaction cost are handled |
| Theming | Hard-coded colours break tokens, dark mode, contrast, or semantic state colours | Some one-off values need token consolidation | Tokens and semantic colours are used consistently |
| State coverage | Missing a reachable empty, loading, error, success, disabled, or permission state for the core flow | A consequential secondary state needs clearer copy or interaction detail | States required by the brief and real component contract are implemented |
| Resilience | Supported or observed long text, empty values, permissions, offline/errors, or localisation break the primary task | A reachable secondary failure is known but bounded | Relevant long text, missing data, error recovery, permission, and i18n cases are handled |
| Specificity | Dominant choices omit required subject evidence or contradict an explicit surface contract, preventing the requested outcome | A concrete mismatch with the content, audience, or visual system weakens the intended hierarchy or identity | The dominant choices fit the task, content, audience, and visual system, including familiar or current conventions |

Judge specificity through [pattern roles](fundamentals-core.md#choose-patterns-by-role).
Common styling or resemblance to generated output does not establish severity.
Name the actual mismatch and consequence; a coherent conventional interface can
be acceptable without a unique visual signature.

## Interpretation

- Any `blocked`: do not call the UI done.
- Any `risky`: either fix now or explicitly name the follow-up risk.
- All `acceptable`: the implementation can ship within the assessed quality
  scope.

## Accessibility as an operating capability

When improving the delivery system, build accessibility into the cheapest
useful layer instead of treating it solely as a release audit:

- Put semantic, keyboard, focus, contrast, motion, target-size, and naming
  requirements in component acceptance criteria and design-system contracts.
- Give accessibility defects owners and severity. A blocked primary task cannot
  become acceptable because an automated scan is green or the release is late.
- Run static and component-level checks during development, browser checks in CI,
  and manual keyboard and assistive-technology review for consequential flows.
- Include disabled people and representative assistive setups in usability work
  when the product risk or audience warrants it.
- Track regressions and recurring root causes across releases. Fix the shared
  primitive or process when the same defect appears in multiple features.
- Keep a release-time audit as a verification layer, not the first time the team
  considers accessibility.

## Core and Enhancement Gate

Build and verify the semantic, usable core before adding decorative overlap,
sticky behavior, advanced typography, motion, or another optional enhancement.
The core must preserve the primary task, content, source order, focus order, and
readable fallback when the enhancement is removed or unsupported.

For changes that introduce or alter these behaviors, verify the affected core
with the relevant probes:

- Feature erasure and delayed or unavailable JavaScript where relevant.
- Continuous resizing instead of a few named breakpoints, including shallow
  landscape viewports and mobile browser chrome.
- Keyboard navigation, visible and unobscured focus, zoom, touch, pointer, text
  selection, and hash-target navigation.
- Minimum, typical, maximum, empty, long, and localized content.
- Representative browsers from the project's support policy.

Keep flair optional. Suspend sticky, overlapping, clipped, or animated treatment
when it obscures focused content or blocks the primary task. If the enhancement
requires compound conditions, undo chains, duplicated content, opaque math, or
repeated exception selectors, revisit the underlying design and layout model
before adding another patch.

## Reusable UI Fixtures

Reuse existing stories, fixtures, or the real page to expose the changed
behavior. Add or extend a fixture only when it makes a consequential regression
reproducible and its maintenance cost is justified:

- For global CSS, maintain a semantic kitchen sink with headings, prose, lists,
  forms, tables, media, selection, focus, hash targets, and uncommon elements.
- For reusable components, use the project's Storybook or pattern library and
  cover representative content, states, themes, locale, and interaction.
- For sticky, overlapping, scrolling, focus-dependent, or container-dependent
  behavior, provide enough surrounding height, width, items, and controls to
  reproduce the behavior while resizing and navigating by keyboard.
- If no component workshop exists, use a small isolated local route or example.
  Keep fixture-only styles and data out of production behavior.
- For a simple one-off page region, verify the real page instead of creating a
  parallel fixture without reuse value.

## Final Execution Pass

Inspect the rendered change against the brief and existing system. Combine the
relevant viewport, content, state, keyboard, theme, and motion checks in one
evidence round. Source review alone cannot establish layout or interaction
quality; use the real page or an existing fixture where possible.

Fix observed defects and verify the fixes. Stop when the requested outcome and
required checks pass; continue only for a new failure, change, or unresolved
material risk. Reopen the direction only if the evidence contradicts the brief,
and use existing user authorization for any resulting work within scope.

Report actionable findings at clickable `file:line` locations, with the user
consequence and evidence. State any verification limit without replacing concrete
findings with a general score.

## Pattern Fit Gate

Use this gate when a suspected default may conflict with the surface's task or
visual character. Apply [pattern roles](fundamentals-core.md#choose-patterns-by-role)
and classify findings with [UI anti-patterns](ui-antipatterns.md): objective
defects can block, unexamined defaults are advisory, and a cluster sharing a
concrete mismatch points to an owning direction or structure decision.

Ask:

- Does the structure support the actual workflow, data shapes, and reading or
  browsing needs? A familiar shell can fit when its content and actions do.
- Do labels, accents, and container boundaries serve distinguishable content,
  interaction, or expressive roles without competing with the intended hierarchy?
- Does the interface show real evidence when users need to inspect a product,
  place, person, object, state, screenshot, diagram, or outcome?
- Does the expressive treatment fit the direction while preserving task access,
  clear content, and proportionate attention and rendering cost?

Operate UI can pass by reflecting the real workflow through familiar controls.
Persuade UI can pass by making the offer, evidence, and action credible in the
intended voice. Read UI can pass by being readable and trustworthy. Experience
UI can pass when the work leads and the interface supplies orientation and
control. Judge fit and consequence rather than uniqueness or intensity.

## Performance Design Check

Performance is part of the user experience. Do not optimise random details, but
do make performance-sensitive design choices explicit before shipping.

Check:

- The LCP element is known, not lazy-loaded, and has appropriate priority.
- Images are sized for their display context and have width/height or
  `aspect-ratio` to prevent layout shift.
- Heavy visual effects are bounded to small areas and do not animate layout
  properties.
- Long lists, large tables, feeds, and search results have a pagination,
  virtualisation, or progressive loading strategy.
- Non-critical media, scripts, and visual flourishes are lazy-loaded or omitted
  when they do not serve the primary action.
- Font choices do not require unnecessary weights, families, or blocking loads.
- The interface remains usable on slower mobile devices and weaker connections.

If performance risk is visible in the design itself, fix the design decision.
If performance risk depends on implementation details, measure before and after
the change.

## Code-Level Web Checks

Check the implementation details affected by the change:

- Use `<button>` for actions and `<a>`/router links for navigation. Do not use
  clickable `<div>`/`span` elements for primary interaction.
- Icon-only controls have accessible names; decorative icons are hidden from
  assistive technology.
- Form inputs have `label`, meaningful `name`, appropriate `type`,
  `autocomplete`, and `inputmode`. Do not block paste.
- Global form and prose fixtures include wrapped labels, disabled explanations,
  hidden or generated fields, long localized words, URLs, code overflow,
  selection contrast, disclosure widgets, and real fragment navigation beneath
  persistent UI.
- Disable spellcheck for email addresses, usernames, invitation codes, and
  machine identifiers when spelling suggestions would corrupt or distract from
  the value. Do not disable it for normal prose fields.
- Async validation, save status, background work, and toast messages use local
  feedback and `aria-live` when screen reader users need the update.
- Text containers handle long content with wrapping, `min-width: 0` in flex/grid
  children, or deliberate truncation with a path to the full value.
- Dates, times, numbers, and currencies use `Intl.*` APIs rather than hardcoded
  formatting.
- Animations list properties explicitly; avoid `transition: all`, layout
  animation, and non-interruptible effects.
- URL state reflects tabs, filters, pagination, selected records, and expanded
  panels when users need shareable or restorable UI state.
- Warn before route change, reload, or close only when users would lose genuine
  unsaved work; remove the guard immediately after save or discard.
- Dark themes set `color-scheme`; browser UI such as form controls and
  scrollbars should not fight the theme.
- Keep browser chrome coherent by updating `theme-color` when the top-level
  surface changes materially, including supported light and dark modes.
- Mark stable brand names, code tokens, product identifiers, and commands with
  `translate="no"` when automatic translation would corrupt them; keep surrounding
  explanatory prose translatable.

## Use With Judgment

These gates cover the assessed scope and combine implementation evidence with
design judgment. They do not establish quality beyond that scope. If the real
surface exposes a wrong register, weak hierarchy, or unclear primary action,
revisit the owning decision; a link to planning guidance does not require another
planning cycle.
