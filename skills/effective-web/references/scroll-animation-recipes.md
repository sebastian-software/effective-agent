# Scroll Animation Recipes

Use for an intentional scroll-linked scene, threshold-triggered entrance, or
section-dependent visual treatment. Keep static content available and retain
native scroll input. These are techniques to choose from, not a reason to add
reveals to every section.

## Choose the playhead

| Behavior | Mechanism | Check |
| --- | --- | --- |
| Motion reverses when scrolling reverses | Scroll/view progress timeline | Stop and reverse at intermediate positions |
| Crossing a boundary starts a timed response | IntersectionObserver plus a time-based animation | Stop scrolling immediately after crossing |
| One section supplies another element's progress | Named view timeline with a suitable common scope | Nested scrollers and sibling scope |

An observer is not a continuous scroll playhead. A scroll timeline is not a
one-time event. Choose replay, one-shot, and return behavior explicitly.

## Trigger on the visibility you actually require

- Observation delivers an initial result; a callback does not prove that the
  person just scrolled. Handle an already visible target deliberately.
- Process every relevant entry in a callback. `isIntersecting` indicates
  overlap; if the effect needs a visibility fraction, compare `intersectionRatio`
  with that fraction and configure the matching threshold.
- Choose a fraction the target can reach. A large section may never fit enough
  of its area into the viewport; use a smaller sentinel or a different boundary
  rather than waiting forever for an impossible ratio.
- Use `root` and `rootMargin` for the actual scrollport and desired boundary.
  A sentinel often describes a document-level trigger better than observing a
  whole long section. Unobserve a completed one-shot trigger; disconnect the
  owner on teardown.

Keep content visible when observation or animation is unavailable. If reduced
motion changes while open, show the final meaningful state and stop obsolete
trigger work. See the [Intersection Observer specification](https://www.w3.org/TR/intersection-observer/).

## Define ranges and out-of-range states

Declare `animation-timeline` and `animation-range` after an `animation` shorthand
that would reset them. `scroll(root block)` follows root block-axis scrolling;
the default nearest scroller can accidentally bind the effect to an inner panel.

For a target shorter than the scrollport, `cover` spans its full passage,
`contain` the interval fully inside, and `entry`/`exit` isolate the respective
edge crossings. Taller targets have different alignment boundaries; inspect the
range against real content instead of assuming full visibility occurs. See
[animation ranges](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/animation-range).

Specify what should be painted before and after the range, including reverse
scrolling. Entry and exit may use different ranges, but two opacity animations
still require deliberate [property composition](animation-composition.md).
An absent fill state can flash content during reversal; an unnecessary retained
state can suppress ordinary styling. Neither is solved by adding `both` blindly.

## Let sections supply header backgrounds

For a transparent header crossing sections with different surfaces, a
header-height sticky background inside each section can follow the viewport
only while that section contains it. Keep the real header and navigation
separate from these decorative blockers so gaps can stay transparent.

Share the header-height value, account for whether the actual header reserves
layout space, and ensure short sections have room for a blocker to behave as
intended. Check stacking, pointer interception, focus visibility, and theme
changes. When that geometry does not fit, a section observer or timeline may be
clearer; do not force the blocker technique onto every header.

For long parallax scenes, parameterize layer depth through shared keyframes.
Do not replace native wheel or touch inertia to make the demonstration look
smoother. An active scroll animation can own a background value that an ordinary
theme transition also wants; choose an owner or a separate decorative layer.
