# Animation Composition

Use when several effects compete for the same property, a reusable keyframe
needs different starting states, or motion snaps when classes change. First
identify which element and animation owns each property.

## Separate independent responsibilities

Multiple animations on one element do not automatically add their transforms
or opacities. The default composition replaces values; list order matters when
effects target the same property. See [animation composition](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/animation-composition).

| Combination | Useful separation | Failure to avoid |
| --- | --- | --- |
| Centering, travel, and spin | Stable anchor outside a moving child; rotation on another part or independent property | A travel animation overwrites the centering transform |
| Batch fade and particle twinkle | Fade a wrapper while its children twinkle | Two independent opacity animations unexpectedly replace one another |
| Hinged object and loose attachment | Parent movement plus child motion around its own pivot | One origin makes every part behave like a rigid plate |
| Hover displacement and action exit | Separate properties or wrappers with explicit reset ownership | An old hover transform leaks into the next entrance |

Independent `translate`, `rotate`, and `scale` properties reduce contention,
but compose in a fixed order before the `transform` list. Reordering CSS
declarations does not change that geometry. A transform list or parent/child
structure is appropriate when a different order is required; translation after
rotation can describe an orbit rather than a spin in place. See
[independent translation](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/translate).

Additive composition can be useful when supported, but is an intentional effect
stack, not a substitute for understanding the underlying value and operation
order. Prefer the clearer ownership model when additive behavior is hard to
predict or maintain.

## Reuse underlying values deliberately

A keyframe omitting `from` can begin from the underlying opacity or transform;
omitting `to` lets the underlying destination participate. For example, one
fade-out ending at zero can serve both a muted and an opaque particle instead
of forcing both to start at opacity one.

When partial keyframes are intended to layer over a second changing animation,
verify the effect ordering in the supported browsers. An outer fade and inner
twinkle give simpler ownership when that interaction is fragile. The combined
opacity is then the result of nested painting, rather than two competing values
on the same node.

## Treat timing and retained styles as state

- Delay and iteration are different: `animation-delay` postpones the first
  iteration only. Put an unchanged segment into the keyframe timeline for a
  pause on every loop. A blink should spend most of its cycle at rest.
- A negative delay starts partway through the animation. Use it to distribute
  phases in a continuous field rather than making every particle begin in sync.
  It does not create a queue or delay each repetition.
- `backwards` applies the appropriate initial keyframe during a delay;
  `forwards` retains the ending value afterward; `both` combines those effects.
  Choose only the retention the component needs. Retained animation values can
  override later ordinary styles and make a new hover or theme state appear
  broken. See [fill modes](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/animation-fill-mode)
  and [animation delay](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/animation-delay).
- For parameterized keyframes, keep a shared definition and supply local custom
  properties for distance, angle, amplitude, lifetime, or phase. Include the units
  required by the consuming property and a valid fallback where absence is valid.
- An animation's visual completion is not an ownership boundary by itself.
  Handle cancellation, removal, preference changes, and multiple named animation
  events when choosing event-based or deadline-based cleanup.

Verify rapid class changes, partial progress, and the final rest state. Inspect
the computed property and active animations before adding specificity or
another wrapper to compensate for an unexplained override.
