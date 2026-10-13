# Playwright E2E Workflows

Reserve E2E tests for high-value integrated paths and keep each one user-centered,
deterministic, and small enough to debug from its trace alone. Flaky or sprawling E2E
suites get disabled, so stability is the primary design goal, not coverage breadth.

## Locators

- Select elements the way a user finds them: prefer `getByRole` (with an accessible
  `name`), then `getByLabel`, `getByPlaceholder`, and `getByText`. Reach for
  `getByTestId` only when no accessible handle exists.
- Avoid CSS and XPath selectors tied to DOM structure or generated class names; they break
  on refactors that do not change behavior. A role/label locator that fails usually means
  a real accessibility or UX regression worth knowing about.
- Scope queries to a container (`page.getByRole('dialog').getByRole('button', { name: 'Save' })`)
  instead of relying on global uniqueness.

## Waiting and assertions

- Rely on web-first assertions, which auto-wait and retry: `await expect(locator)
  .toBeVisible()`, `.toHaveText()`, `.toHaveURL()`. Let actions like `click` and `fill`
  auto-wait for actionability rather than asserting readiness manually.
- Never use `page.waitForTimeout` / fixed sleeps to "let things settle" — they are the
  primary source of flake and slowness. Wait for a concrete condition: a visible element,
  a URL, or a specific response.
- Do not assert on internal implementation detail (class toggles, internal state). Assert
  on what the user perceives — visible text, navigation, enabled/disabled controls.

## Determinism and network

- Control network boundaries that would otherwise make a test flaky. Use `page.route` to
  stub or modify responses for third-party and non-deterministic endpoints, and prefer
  asserting against seeded backend state for first-party data.
- When the app uses a service worker, account for it explicitly: requests served from the
  worker bypass `page.route`, so register routing before the worker activates or disable the
  worker in the test environment.
- Reset state between tests via fixtures or API setup; do not let one test's data leak into
  the next. Run tests isolated and in parallel by default.

## Codegen and component testing

- Treat `playwright codegen` output as a rough draft only. Before committing, replace brittle
  locators with role/label queries, delete incidental waits and redundant assertions, extract
  shared steps into fixtures, and narrow scope to the behavior under test.
- Since Playwright 1.62 (July 2026), component testing uses a stable stories-and-gallery model
  (`fixtures.mount()` from `@playwright/test`); the old `@playwright/experimental-ct-*` packages
  are no longer published. Confirm the installed version before relying on it, and keep the
  project's existing Storybook or Browser Mode setup when it already covers component-level tests.

## Debugging artifacts

- Enable trace, screenshot, and video capture on first retry/failure in CI; the trace viewer
  replays the run with DOM snapshots and network. Inspect the artifact before re-running a
  failed test, so flake is diagnosed instead of masked.

## Review checklist

- Does every locator use role/label/text (or a deliberate testid), never structural CSS/XPath?
- Are all waits expressed as web-first assertions, with zero fixed timeouts?
- Are non-deterministic and third-party requests routed/stubbed, with service-worker handled?
- Is state reset between tests so they pass in isolation and in parallel?
- Is the suite scoped to critical journeys, not component permutations?
- Are trace/screenshot/video enabled so CI failures are debuggable from artifacts?
