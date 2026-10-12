# Core Interface Decisions

Use this module when choosing interface patterns or conducting a broad design
review before loading a focused layout, component, accessibility, or motion
route. It is the default entry point for general UI judgment, not a checklist to
apply mechanically.

## Decide What Must Become Easier

1. Name the user's primary outcome, the next action, and the highest-cost
   failure.
2. Remove or demote elements that do not improve recognition, orientation,
   trust, comprehension, recovery, or the intended visual character.
3. Make the current state, available action, and consequence understandable
   before adding visual polish.
4. Preserve familiar patterns unless evidence shows they harm the task. A novel
   control must repay its learning cost with a clear benefit.

## Choose Patterns by Role

Use familiar visual patterns when they support content relationships,
interaction, recognition, or the intended visual character. Brand identity,
atmosphere, and editorial rhythm are valid roles; an element need not convey
additional information to earn its place.

For a new surface, derive hierarchy and relationships from the content before
adding labels, accents, or containers. Do not add repeated emphasis or nested
containers without a distinct role. Connect an expressive choice to the actual
composition and direction, rather than a generic claim that it looks polished.

For an existing surface, preserve coherent conventions and purposeful style.
Before recommending removal, identify the concrete mismatch with the content,
task, or visual system and the benefit of the change. Popularity, trendiness,
and resemblance to generated output do not establish a defect. Do not require
novelty or a written justification for every decorative detail; infer intent
from the brief, content, system, and rendered result. Use the
[layout example pairs](ui-pattern-layout.md#contextual-example-pairs) to
distinguish a fitting treatment from its misuse.

## Shape a Coherent System

- Inspect the existing visual language before inventing tokens, controls, or
  page treatments. Diagnose drift by its source: an absent token, a missing
  component contract, a one-off product requirement, or an unreviewed override.
- Define a small set of purposeful choices for type, color, spacing, elevation,
  radius, icon treatment, and interaction states. Reuse them by role rather
  than copying visual values.
- Use grouping, alignment, hierarchy, and generous but intentional space to
  show relationships. Do not default every group to a card or every important
  action to a saturated button.
- Prefer progressive disclosure when extra controls, explanation, or advanced
  options are not needed for the first successful pass.

## Protect the Interaction Contract

- Actions need visible affordance and feedback. Buttons perform actions; links
  navigate; disabled, loading, error, and success states must preserve the
  user's mental model.
- Keep keyboard focus visible, unobscured, and returned predictably after a
  transient surface closes. Never disable zoom or make pointer precision a
  requirement.
- Treat accessibility, localization, slow loading, and narrow layouts as
  normal states of the design rather than exceptions to patch later.
- Use motion only to clarify change, spatial continuity, or completion; the
  static and reduced-motion paths must carry the same information.

## Review Questions

- Can a new user identify the purpose, current state, next action, and risk in
  a quick scan?
- Are repeated patterns genuinely the same job, with the same semantics and
  state behavior?
- Does each visual emphasis correspond to importance, urgency, or a meaningful
  relationship?
- Can keyboard, zoom, long content, errors, and reduced motion complete the
  same primary task?

For rare design-system diagnosis, composite-widget keyboard mechanics, or
platform-animation details, consult the [deep fundamentals appendix](fundamentals.md)
after identifying the exact concern.
