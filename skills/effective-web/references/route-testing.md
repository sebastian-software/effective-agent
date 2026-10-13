# Frontend Testing

Use this route to choose, implement, or review frontend tests for browser-facing applications.

Test the user-facing risk, not the available state space. A new test should
either distinguish a consequential regression, protect a supported contract, or
provide decision evidence worth its fixture, runtime, flake, and maintenance
cost. Do not create a browser/theme/viewport/state Cartesian product or a test
merely because a reviewer named an imaginable edge case. A trivial presentation
change may need only the existing checks and one focused rendered inspection;
rare failures in checkout, authentication, destructive actions, accessibility,
or unrecoverable work can justify deeper coverage.

## Workflow

1. Inspect the project stack: framework, package manager, existing test runners, Storybook, browser automation, CI, and current scripts.
2. State the reachable behavior, user consequence, and failure the evidence
   must distinguish; do not invent probability or traffic estimates.
3. Choose the narrowest useful test layer:
   - pure logic: unit test,
   - component state or interaction: Storybook/Vitest/component test,
   - visible UI drift: visual regression,
   - integrated route or workflow: Playwright-style E2E,
   - static guarantees: linting, type checking, accessibility checks.
4. Reuse existing fixtures and stories before inventing parallel setup.
5. Stabilize browser tests before adding baselines: fixed viewport, deterministic data, mocked time/randomness, loaded fonts, disabled animations, and masked dynamic regions.
6. Treat generated tests as drafts. Review locators, assertions, waits, and scope before committing.
7. Make baseline updates explicit, reviewed, and tied to an intentional UI change.

## Reference Files

- [testing-layer-decision.md](testing-layer-decision.md) - Choose unit, component, visual, E2E, or static checks.
- [storybook-component-testing.md](storybook-component-testing.md) - Use stories as component state fixtures.
- [visual-regression-stability.md](visual-regression-stability.md) - Stabilize screenshots and visual baselines.
- [playwright-e2e-workflows.md](playwright-e2e-workflows.md) - Keep Playwright tests user-centered and maintainable.
- [ci-and-baseline-review.md](ci-and-baseline-review.md) - Define CI ordering and baseline update review.
- [vendor-tool-notes.md](vendor-tool-notes.md) - Treat vendor tools as implementation options, not defaults.

## Boundaries

Do not use this route for backend-only tests, load tests, security testing, vendor procurement, or simply running an existing test command without changing or interpreting the test strategy.
