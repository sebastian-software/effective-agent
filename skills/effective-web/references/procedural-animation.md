# Procedural Animation

Use for pointer-reactive geometry, transient particles, or Canvas scenes. Keep
labels and controls semantic; a decorative drawing surface does not replace
accessible content. For measured jank or leaks, use
[animation runtime performance](animation-runtime-performance.md).

For range-mapping code, ripple and noise fields, trails, responsive connectors,
or simultaneous grid updates, select [construction recipes](procedural-animation-recipes.md).

## Choose the representation

| Need | Starting point | Responsibility |
| --- | --- | --- |
| Small transient burst | DOM nodes and shared parameterized keyframes | Bound node count and batch lifetime |
| Editable vector parts or meaningful diagram | Inline SVG | Maintain coordinates, identity, and semantics |
| Many primitives updated together | Canvas | Own drawing, timing, resize, and accessible alternatives |
| Measured main-thread drawing contention | Worker and OffscreenCanvas | Transfer ownership, inputs, dimensions, and teardown |

There is no universal particle-count crossover. Profile the intended scene and
device, including allocation and paint; a small amount of trigonometry is not
automatically the bottleneck. Prefer fresh short-lived records until measured
allocation pressure justifies a pool. Reset and dispose a pool when no longer
useful instead of retaining an unbounded supply of invisible objects.

## Keep coordinates and targets stable

- Measure a stable wrapper and animate its child. Measuring a target whose
  transform changes from that measurement creates a feedback loop.
- `clientX/Y` and `getBoundingClientRect()` share viewport coordinates. Subtract
  the wrapper's origin for local offsets; do not mix those values with document
  offsets after scrolling. Refresh cached geometry when scroll, resize, or
  surrounding layout changes can invalidate it.
- Convert screen coordinates to the intended SVG element's local space before
  comparing them with its geometry. An inverse `getScreenCTM()` handles nested
  transforms and viewBox mapping; guard an unavailable or noninvertible matrix.
  A simple width ratio is insufficient when letterboxing or transforms apply.
  See [SVG coordinate transforms](https://developer.mozilla.org/en-US/docs/Web/API/SVGGraphicsElement/getScreenCTM).
- Clamp proximity mappings to meaningful bounds and give the center a tolerance
  region. A pupil can point toward a distant cursor while its displacement
  remains within the eye. Set new spring targets instead of starting an
  independent animation on every pointer event.
- Attach a clipped reveal's trigger to a stable, reachable parent: fully
  clipped pixels cannot provide their own pointer hit area. Preserve a
  focus/tap path for meaningful content; see [clip-path](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/clip-path).

For a radial burst, `x = cos(angle) * radius` and
`y = sin(angle) * radius` use radians. Distribute `n` directions with
`index / n * 2π`, then add bounded jitter to avoid both clumping and exact
symmetry. A full circle must not duplicate its first point at the final angle.
Uniformly choosing radius is not uniform sampling of disk area; choose the
distribution for the desired ring or field.

## Own every emitted batch

Emit on the meaningful state change, such as adding a favorite, rather than
every click including reversal. Keep particles outside normal layout,
decorative to assistive technology, nonselectable, and unable to intercept input
or create scrollbars. Use shared keyframes with per-particle parameters instead
of generating a stylesheet per particle.

Fading is not removal. Retire a batch after delay plus active duration, and also
handle cancellation and owner teardown. If using `animationend`, select the
relevant animation and cover cases where it never completes. Stop a continuous
emitter separately from retiring particles already in flight. Under reduced
motion, skip nonessential generation and simulation rather than hiding a live
effect. Preserve any meaningful result without the burst.

In React, render DOM particles from records with stable keys and functional
updates so a new batch preserves older live batches. Keep Canvas simulation in
refs or another mutable model instead of setting React state every frame.

## Size Canvas and simulate elapsed time

Separate displayed CSS size from bitmap size. Measure the CSS box, choose an
appropriate device-pixel ratio, and size the backing bitmap from both. A
resolution cap can be a measured quality/performance tradeoff, not a hardcoded
assumption that every display is 2×. Recheck dimensions and effective DPR when
zoom or the display changes. After assigning `canvas.width/height`, restore
the transform and drawing styles because assignment resets the context, even
when assigning the same value. Avoid repeatedly multiplying an existing scale.
See [Canvas resizing](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/width)
and [device pixel ratio](https://developer.mozilla.org/en-US/docs/Web/API/Window/devicePixelRatio).

Use frame timestamps and seconds: `x += velocity * dt`. Apply the same time
basis to acceleration, drag, and emission, not just position. Continuous drag
can use `velocity *= Math.exp(-drag * dt)`; accumulate fractional emissions
between frames. Per-frame constants make a scene behave differently at 60Hz
and 120Hz. Test equivalent elapsed time at different cadences.

Reset or cap elapsed time after a decorative scene resumes; choose the bound
for the effect instead of copying a universal value. Reconcile out-of-bounds
positions after resize and direct velocity inward instead of flipping it on
every frame. Save/restore drawing state around per-object transforms, and load
image assets before the frame that needs them. See [frame timing](https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame).

## Move work to a worker only when needed

Transfer control before obtaining a context on the HTML canvas, then transfer
the OffscreenCanvas to the worker. Keep one drawing owner. Send measured sizes,
DPR, pointer input, and configuration from the main thread; the worker cannot
read the DOM. Feature-detect the required path and retain a simpler fallback.
Terminate the worker and its subscriptions at owner teardown; off-thread work
still needs pause, resize, and cancellation semantics. See
[canvas transfer](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/transferControlToOffscreen).
