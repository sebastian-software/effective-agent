# Expressive Motion

Use for a chosen playful or tactile detail. Ordinary feedback needs no particles,
sound, or spring library. Reuse the purpose and reduced-motion contract in
[motion principles](motion-interaction.md); select only the technique needed.

## Build a small vocabulary

Derive motion from the product's visual idea: a few related impulses, materials,
curves, and response rhythms are more coherent than an unrelated effect on every
control. Judge an enlarged or slowed study again at its real display size and
normal speed. First-visit character does not justify an artificial wait.

## Separate surface, target, and response

- Enlarge a button's decorative surface or pseudo-element while keeping its
  label, focus ring, and hit target stable. Scaling the entire long label also
  stretches its horizontal travel. Equal expansion per edge is a different
  geometry from proportional scale; measure any layout-based alternative.
- Keep tactile hover cues on actionable elements. A decorative card that lifts
  like a button can falsely promise interaction.
- A brief icon impulse can return to neutral while hover remains. Separate its
  trigger/reset deadline from its spring's settling time. A hover-only keyframe
  can disappear abruptly on pointer exit; use an owned animation or transient
  state when it should finish independently. Repeated input may retarget or
  restart that bounded response, without queuing copies.
- For squash/stretch, place the pivot at the contact point. Animate an arrow's
  shaft geometry when it should grow without enlarging its arrowhead. Nested
  parts can have different pivots and settling behavior without a full simulation.

## Choose sampled easing or a live spring

Use a time-based curve for a known journey and a continuously updated spring
value when changing targets need physical continuity. A CSS `linear()` easing
can approximate a spring from sampled output values; it is not a simulation that
carries velocity into each interruption. Test rapid reversals rather than only
the uninterrupted demo.

Keep a small set of curve/duration pairs as tokens. For generated samples,
retain the originating spring parameters so the curve can be regenerated.
Tune response speed with stiffness, then settling character with damping while
holding other parameters stable; values depend on the implementation and effect.
Bound overshoot so shrinking controls cannot invert or obscure their state.

For a legacy-target fallback, declare conventional easing first and override
the token inside `@supports (transition-timing-function: linear(0, 1))`.
An unregistered custom property accepting the token text does not prove that
the consuming timing function supports it. See [CSS linear()](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/easing-function/linear)
and [custom-property validity](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascading_variables/Using_custom_properties).
For continuously retargeted React values, see [Motion useSpring](https://motion.dev/docs/react-use-spring);
reuse the installed library before adding another for a stylistic preference.

## Sequence and reset deliberately

- Let parts overlap in time when that communicates one response; waiting for
  every decorative stage to finish needlessly extends the sequence. Keep the
  action and result available independently of the choreography.
- An entrance and return can use different curves. Define the transition on
  the destination state and test quick movement across neighboring controls so
  a long exit does not leave a trail of stale highlights.
- Confirmation and cancellation may have distinct exits when the distinction
  helps explain the action. Clear action-specific transforms before reopening.
  Cancel obsolete reset timers or use an interaction generation token so a
  previous close cannot erase a newly opened dialog.
- Retain a leaving element only as needed for its visual exit; focus,
  interaction, and accessible visibility must follow the actual dialog or menu
  state. Motion never extends an invisible control's interactive lifetime.
- Use animation fill modes deliberately: retained keyframe values can override
  later ordinary styles. Give a settled component an explicit rest state rather
  than relying on indefinite animation ownership.

## Coordinate optional sound

Sound can add tactile feedback when it fits the experience. Keep samples short
and subtle, with a visible, independent site mute control. The action and all
meaningful feedback must also work silently. Reduced motion and mute are
separate preferences. Avoid decorative loops and unbounded overlapping playback
during rapid input.

Prepare a small licensed asset before the interaction where practical. Attempt
playback from a deliberate activation and handle a rejected `play()` promise
without delaying or failing the underlying action. Hover is not a reliable
first playback permission. See [media playback](https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/play).
For variation, choose from a restrained family of samples. If using an installed
sound-sprite library, check whether its segment pair means start/duration or
start/end; do not infer units or licensing from an example download.
