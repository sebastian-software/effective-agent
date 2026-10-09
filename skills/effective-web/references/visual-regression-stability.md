# Visual Regression Stability

A visual test is only worth keeping if every diff means a real product change. If the
environment is not pinned, diffs come from font hinting, animation timing, anti-aliasing,
or live data — and the team learns to rubber-stamp updates, which defeats the test.

## Scope the screenshot

- Screenshot a component or a single element, not the full page, unless page composition
  is the actual subject. Smaller surfaces produce smaller, attributable diffs.
- Prefer driving the target through a Storybook story or a focused component mount so the
  state is deterministic and reproducible outside the test.

## Pin the rendering environment

- Fix viewport size, device scale factor, browser engine, and the OS/container image.
  Run visual tests in the same container locally and in CI; a different OS renders fonts
  differently and every baseline will mismatch.
- Self-host and preload web fonts; block the test from starting until `document.fonts.ready`
  resolves. Never depend on a network font CDN — a slow or missing font swaps glyphs and
  shifts layout.
- Pin locale, timezone, and `Date`/`Math.random` so dates, numbers, and shuffled content
  render identically on every run.

## Neutralize motion and dynamic content

- Disable animations and transitions before capture. Inject CSS that sets
  `animation: none !important; transition: none !important; caret-color: transparent`,
  and pause CSS animations and video; with Playwright pass `animations: 'disabled'` to
  `toHaveScreenshot`. Stop skeleton shimmer, canvas noise, live clocks, and rotating
  content unless that motion is the subject of the test.
- Wait for the deterministic end state (web-first assertion or `expect(locator)
  .toBeVisible()`), not a fixed timeout, so capture happens after content settles.
- Mask regions that are legitimately non-deterministic — timestamps, avatars, ads,
  randomized IDs, user-generated content, maps, analytics banners, and third-party embeds
  — via the runner's mask option (Playwright `mask: [locator]`) or by overlaying a fixed
  placeholder. Mask the smallest region possible; do not mask away the thing under test.

## Thresholds and baselines

- Fixed-coordinate comparison tools such as odiff or pixelmatch fit these baselines,
  where layout must not move. Before/after evidence for a change, where content
  shifts, needs row alignment instead: see [Change Screenshots](route-change-screenshots.md).
- Start with a near-zero pixel threshold and only raise it with a written reason
  (documented sub-pixel anti-aliasing on one engine). A loose blanket threshold hides real
  regressions. Before raising a threshold to make a test pass, first narrow the screenshot,
  stabilize the fixture, or split the assertion.
- Keep dark mode, high-contrast, locale, and RTL screenshots only for states where that
  appearance is part of the risk being guarded; do not snapshot every theme by default.
- Generate baselines in CI (or the shared container), never from a developer laptop, so the
  reference matches the comparison environment.
- Treat a baseline update as a product/design decision, not routine test maintenance: review
  the actual/expected/diff images in the PR and require sign-off, the same as any UI change.
- When using a hosted visual service (e.g. Chromatic) for Storybook coverage, the same rules
  apply — pin fonts and motion, mask dynamic regions, and gate baseline approval on review.

## Review checklist

- Is the capture scoped to the smallest meaningful element?
- Are viewport, DPR, browser, container image, fonts, locale, and timezone all pinned?
- Are animations disabled and fonts confirmed loaded before capture?
- Are only the genuinely dynamic regions masked, with the subject still visible?
- Is the threshold near zero, with any increase justified in writing?
- Were baselines generated in CI and approved through PR review?
