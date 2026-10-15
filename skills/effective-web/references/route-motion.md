# Motion and Interaction

Use this route for motion that clarifies state, continuity, feedback, and
progress, or adds an earned moment of brand character without slowing users down.

## Workflow

1. Identify the purpose of motion: feedback, state change, orientation,
   hierarchy, continuity, or earned delight.
2. Remove expressive motion that competes with task completion or appears in a
   dense repeated workflow.
3. Choose CSS, Web Animations, per-frame JavaScript, or a library from the
   required capability and execution model.
4. Prefer compositor-friendly properties and verify costly effects.
5. For looping, canvas, WebGL, or long-lived motion, verify that offscreen,
   hidden-document, and unmounted work stops at its owning lifecycle.
6. Keep product transitions short and predictable.
7. Respect `prefers-reduced-motion` and provide equivalent state clarity without animation.

## Rules

- Author the static, reduced-motion experience first; layer motion inside `@media (prefers-reduced-motion: no-preference)` and never lose information when motion is off.
- Prefer `transform` and `opacity` on hot paths; avoid layout properties and
  measure large filters or other paint-heavy effects.
- Keep UI transitions short (≈150–250ms) and make every animation interruptible by user input.
- Motion should never hide latency or force users to wait for choreography.
- Do not make content available only through hover or scroll tricks.
- Use scroll effects only when they improve comprehension or orientation.
- Feature-detect and reduced-motion-guard View Transitions and scroll-driven animations; the content change must work when they are unsupported.
- Preserve focus, scroll position, URL state, and stable layout during transitions.
- Allow restrained expressive motion in earned brand or success moments; make it
  non-blocking, keyboard-equivalent, and absent from the reduced-motion path.
- Adopt an animation library only when it adds a required capability beyond
  basic platform transitions and keyframes.

## References

Select the smallest module for the unresolved behavior; these are alternatives,
not a required reading sequence.

- [expressive-motion.md](expressive-motion.md) - tactile surfaces, transient
  impulses, spring tokens, action-specific exits, and optional sound feedback.
- [procedural-animation.md](procedural-animation.md) - pointer geometry, DOM
  particles, Canvas sizing, time-based simulation, and worker ownership.
- [layout-motion.md](layout-motion.md) - React Motion layout identity,
  measurement groups, scale correction, and preference-aware client boundaries;
  load when the project uses or needs that library capability.
- [scroll-navigation.md](scroll-navigation.md) - anchors, sticky offsets,
  horizontal sequences, and scroll snap; read [scroll-feedback.md](scroll-feedback.md)
  for back-to-top, scroll-driven feedback, and large lists.
- [motion-interaction.md](motion-interaction.md) - motion principles, timing, and reduced-motion rules.
- [animation-runtime-performance.md](animation-runtime-performance.md) -
  offscreen work, RAF and canvas loops, cleanup, route cycles, and runtime
  evidence; load it for sustained load, jank, memory growth, or lifecycle risk.
