# Motion Interaction

Use motion to explain state change, spatial continuity, feedback, and progress,
or to create an earned moment of brand character. Functional motion must clarify
the interface. Expressive motion must be restrained, optional, and unable to
delay or obscure the user's task.

## Plan Coordinated Motion

When several elements move together or an expressive sequence carries the
story, decide what the motion communicates before choosing effects:

- Which change needs attention, and which supporting elements should stay quiet?
- Which shared objects or spatial relationships explain continuity?
- Which repeated actions should share motion because they share meaning?

Use these answers to remove competing movement and keep the sequence's total
delay and rendering cost bounded. Preserve the same information and task access
in the static version. A routine control transition does not need a separate
motion concept, and a sequence does not justify animating stable page content.

## Reduced Motion First

- Treat `prefers-reduced-motion: reduce` as the baseline, not an afterthought. Author the static, non-animated experience first, then add motion inside `@media (prefers-reduced-motion: no-preference)`.
- Never remove information when motion is disabled. A reduced-motion fallback must still show the final state, the new content, and any feedback — replace movement with an instant change or a subtle opacity cross-fade, not with nothing.
- Mirror the CSS check in JavaScript with `window.matchMedia('(prefers-reduced-motion: reduce)').matches` before triggering `scrollIntoView`, `animate()`, or library-driven motion, and listen for changes so the preference can flip at runtime.
- Distinguish essential from non-essential motion. Motion that conveys state (a spinner, a progress bar) may continue under reduced motion; large translational, parallax, zoom, and auto-playing motion must be suppressed because it triggers vestibular discomfort.

## Performance-Safe Properties

- Prefer `transform` and `opacity` for movement, scaling, and fades because they
  can avoid layout and paint. Some `filter` animations can also be composited,
  but large blur/filter regions are expensive; verify them in the Performance
  panel on representative hardware rather than assuming GPU promotion is free.
- Avoid animating layout-affecting properties (`width`, `height`, `top`, `left`, `margin`, `padding`) on hot paths in task surfaces — they trigger repeated layout and can drop frames. Use `transform: translate()` / `scale()` when the visual result and hit-testing remain correct.
- Promote an element to its own layer with `will-change: transform` only for the duration of an animation, then remove it; leaving `will-change` set permanently wastes memory.
- Read layout values (`offsetWidth`, `getBoundingClientRect`) before writing styles within a frame, never interleaved, to avoid forced reflow. Batch reads and writes (or use `requestAnimationFrame`) when measuring for JS-driven motion.
- Keep product UI transitions short — roughly 150–250ms for state changes and micro-interactions; reserve longer durations only for large spatial moves. Motion must never make the user wait for choreography or hide real latency.
- Use ease-out curves for elements entering and responding to user input (fast start, gentle settle) and ease-in for elements leaving. Reserve spring or overshoot easing for playful, non-blocking accents; never apply bouncy springs to functional, frequently repeated transitions.

## Transitions vs Animations

- Prefer CSS `transition` for simple, reversible state changes driven by a class, attribute, or pseudo-class (`:hover`, `[data-open]`, `[aria-expanded]`). Transitions are naturally interruptible — the browser retargets smoothly when the state flips mid-flight.
- If entry and exit intentionally behave differently — for example, a brief
  eased entrance with an immediate reset — name that interaction contract and
  keep the asymmetric transition at the state that owns it. Mirror the meaningful
  cue for keyboard activation and keep the static result under reduced motion.
- Use CSS `@keyframes` animations for multi-step, looping, or self-starting motion (loaders, attention pulses, entry sequences). Omit intermediate keyframes you do not need — partial keyframes (only `from`/`to`, or a single `50%`) keep motion bounded and let the browser interpolate the rest.
- Make every animation interruptible. User input must be able to cancel, reverse, or retarget an in-progress animation; never block interaction while motion plays. For JS-driven motion, hold the `Animation` object so it can be `cancel()`ed or reversed.

## Entry and Exit Animations

- Do not replay an entrance merely because stable default content mounted. Tabs,
  toggles, icons, and persistent chrome should normally render directly in their
  initial state and animate only after a user- or system-driven state change.
  Preserve an intentional first entrance for earned editorial, onboarding, or
  loading moments; verify a full refresh separately from subsequent transitions
  instead of applying one library flag indiscriminately.
- Animate elements entering the top layer (dialogs, popovers, `[popover]`, `details`) from a hidden or `display: none` state using `@starting-style` together with `transition`, which defines the styles to transition *from* on first render. Support is recent (Chrome/Edge 117+, Safari 17.5+, Firefox 129+); the transition is simply skipped where unsupported, so treat it as progressive enhancement.
- Transition an element to or from `display: none` by including `display` and `overlay` in the `transition-property` list and using `transition-behavior: allow-discrete`, so the element stays visible through its exit animation before being removed.
- Animate height to or from `auto` only with the modern intrinsic-size sizing keywords (`interpolate-size: allow-keywords` on a root, or `calc-size()`); this is Chromium-only at present, so provide a fixed-height or cross-fade fallback elsewhere. Do not fake auto-height growth by animating `max-height` to a guessed pixel value — it produces eased delays and clipping.

## View Transitions

- Use the View Transitions API for spatial continuity across state changes: list-to-detail, filtering and reordering, and persistent UI that should appear to stay put. For same-document (SPA) transitions, wrap the DOM update in `document.startViewTransition(updateCallback)`; for cross-document (MPA) transitions, opt in with `@view-transition { navigation: auto; }` in CSS on both pages.
- Tag elements that should animate between states with a unique `view-transition-name` (or `view-transition-class` for groups). Two elements sharing a name in the old and new state are matched and tweened as one — this is how a thumbnail expands into a hero image.
- Always guard view transitions with reduced motion: wrap the snapshot pseudo-element animations in `@media (prefers-reduced-motion: no-preference)`, or skip `startViewTransition` and apply the DOM change directly when the user prefers reduced motion. Without a guard the default cross-fade still animates.
- View Transitions support is uneven (same-document is Baseline 2025 across Chromium, Safari, and Firefox; cross-document remains Chromium- and Safari-only). Feature-detect with `if (document.startViewTransition)` and fall back to an instant, un-animated update — the content change must work without the transition.
- Customise the snapshot animation via the `::view-transition-group()`, `::view-transition-old()`, and `::view-transition-new()` pseudo-elements rather than animating real DOM nodes. Treat the old snapshot as static and the new snapshot as a live projection, but do not equate "live" with interactive: a document-scoped transition overlay renders above the page and may intercept pointer input until the transition finishes.
- Keep document-scoped transitions short and test controls, focus, top-layer content, and rapid repeated input while they run. A second transition on the same root skips the active one, so retain the returned `ViewTransition`; use `ready` when the pseudo-tree can be customised, `updateCallbackDone` for update completion, and `finished` for cleanup. Define whether repeated input should skip, reverse, or retarget motion while always leaving the final DOM state correct.
- Do not assume generated View Transition keyframes are compositor-only. The browser may interpolate `width` and `height` on `::view-transition-group()`, which can compete on the main thread when snapshot sizes change. Profile the actual transition in the Animations and Performance panels under representative main-thread load; if measured frame drops justify it, simplify the effect or replace the size interpolation with measured `translate`/`scale` keyframes in a FLIP-style transform.
- Use element-scoped transitions when a bounded component change must leave the rest of the page interactive or when concurrent or nested transitions materially improve the interaction, but only behind exact feature detection and a complete fallback because support is still single-engine. For cross-document shared images, make the destination state ready through appropriate preload or prerender strategy; `blocking="render"` can wait for an element to be parsed, not for its image bytes to finish loading, so adopt render blocking only after measuring its Core Web Vitals impact.

## Scroll-Driven and Spatial Motion

- Prefer native CSS scroll-driven animations (`animation-timeline: scroll()` / `view()`) over per-scroll JavaScript updates because the browser can synchronize them with scrolling without a listener loop. Still profile the animated properties and paint cost instead of assuming any timeline makes an effect jank-free. See [scroll feedback](scroll-feedback.md) for reduced-motion, virtual-list, and progressive-enhancement constraints; load its deep appendix only for ranges and animation-shorthand edge cases.
- Choose by execution model and capability, not by the label "CSS" or
  "JavaScript": CSS transitions/keyframes fit declarative states; the Web
  Animations API adds imperative playback control over the browser animation
  engine; `requestAnimationFrame` fits per-frame logic but competes on the main
  thread. Measure dropped frames and main-thread contention for the actual effect.
- Reach for a JavaScript animation library only when it adds a needed capability
  such as coordinated timelines, physics, FLIP measurement, gesture tracking, or
  SVG morphing. Prefer a platform-native solution for basic transitions; reject
  a library that merely wraps CSS behavior while adding bundle and main-thread cost.
- When animating color (state, theme, or accent shifts), keep text and its background within contrast requirements at every frame, not only at the endpoints, and suppress purely decorative color cycling under reduced motion.

## Theme Changes

- Treat a user- or system-selected theme change as one atomic state update unless
  a deliberate transition has been designed and verified. Letting every
  inherited `color`, background, border, shadow, and SVG transition at once
  creates a smeared page and can pass through unreadable intermediate pairs.
- When ordinary component transitions would animate the swap, prefer the theme
  system's supported transition-suppression option. Otherwise apply a temporary
  root state that disables only theme-sensitive transition properties, commit
  the new token set, and remove that state immediately after the new styles have
  painted. Verify cleanup after rapid toggles, OS-theme changes, hydration, and
  exceptions that intentionally animate.
- Avoid making a permanent universal `* { transition: none !important }` rule
  part of the theme architecture. A temporary broad override is a last resort:
  keep its lifetime bounded, include pseudo-elements, respect CSP, and prove it
  cannot survive an exception or interrupted update.

## State Continuity

- Preserve focus, scroll position, URL state, and semantic navigation when adding page or component transitions. A transition must never strand keyboard focus, reset the scroll position unexpectedly, or replace a real navigation with a non-semantic animation.
- Do not gate content behind hover or scroll: information must be reachable without a pointer hover and without triggering a scroll effect, so keyboard, touch, and assistive-technology users get the same content.

## Earned Delight

- Permit expressive motion on brand, editorial, onboarding, success, and other
  memorable surfaces when it reinforces the product's point of view. Do not use
  delight to compensate for a weak flow or add it to dense repeated task surfaces.
- Keep playful micro-interactions brief, subtle, and non-blocking. Preserve the
  object's visual mass when squashing or stretching, use a deliberate transform
  origin, and avoid exaggerated bounce on frequently used controls.
- Choose state-driven motion when the visual state should persist for as long as
  the condition does. Choose event-driven motion for a short acknowledgement or
  playful impulse that should return immediately even while hover/focus remains.
- Trigger equivalent feedback from keyboard focus/activation, not pointer hover
  alone. Suppress non-essential expressive motion for reduced-motion users while
  preserving the same control, label, state, and outcome.

## Review Checklist

- Does functional motion clarify feedback, state, orientation, or continuity?
  If motion is expressive, is the moment earned, restrained, and non-blocking?
- Is there a `prefers-reduced-motion: reduce` path that still shows the final state and all feedback without large or translational motion?
- Are compositor-friendly properties preferred on hot paths, with filter cost
  measured and no unnecessary layout-property animation causing reflow?
- Are durations short (≈150–250ms for UI state) and the easing appropriate (ease-out in, ease-in out)?
- Can every in-progress animation be interrupted, reversed, or cancelled by user input?
- Does stable default content avoid an accidental first-load entrance, while
  intentional initial choreography still runs?
- Does a theme change commit coherently without a page-wide color smear, stale
  suppression state, or unreadable intermediate contrast?
- Are View Transitions and scroll-driven animations feature-detected, reduced-motion-guarded, and functional when unsupported?
- Do transitions preserve focus, scroll position, URL state, and semantic navigation?
- Does any animation library add a capability the platform does not already
  provide, and has its execution model been verified under main-thread load?
- When timing or easing remains hard to judge, inspect the transition with
  DevTools slow-animation controls or a recorded timeline, then confirm the
  correction again at normal speed and under reduced motion. Slow playback is
  diagnostic evidence, not the shipped timing.
