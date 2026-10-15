# Procedural Animation Recipes

Use one of these construction patterns when the requested effect needs it.
The setup, timing, lifecycle, and accessible alternative belong to
[procedural animation](procedural-animation.md); these recipes supply the
geometry and state model, not a mandatory set of embellishments.

## Remap one range into another

Keep remapping, easing, and clamping distinct. This bounded helper handles
reversed input and output ranges and rejects an undefined source range:

```js
function remapClamped(value, inA, inB, outA = 0, outB = 1) {
  if (inA === inB) throw new RangeError("Input range must have a span");
  const t = Math.max(0, Math.min(1, (value - inA) / (inB - inA)));
  return outA + (outB - outA) * t;
}
```

For unbounded extrapolation, omit the progress clamp deliberately. An exponent
on normalized progress can change the falloff or stagger rhythm; it does not
turn an animated score into a measurement of real background progress.

## Reveal a radial band through a field

For each point, compute `distance = hypot(x - originX, y - originY)` in one
coordinate system. Subtract the growing wave radius. With a positive band width,
`max(0, 1 - abs(distance - radius) / bandWidth)` gives a bounded soft ring.
Use the signed difference instead when the inside and outside need different
behavior. Map that weight into brightness, opacity, or displacement.

Begin with a stationary grid and one wave before adding noise, multiple waves,
or glow. On early exit, retain the current field and fade it, retract the wave,
or finish the bounded expansion; switching to a different visibility formula
can expose previously hidden cells in a flash. A reduced-motion version can
show a static meaningful result or omit a purely decorative field.

## Use smooth noise instead of frame-by-frame randomness

Independent random samples create flicker. A coherent noise generator lets
nearby spatial or temporal inputs produce related values. Sample `(x / scale,
y / scale, elapsed * speed)` for an evolving field; moving a spatial input over
time instead produces travel through a pattern. The generator's output range
and seed API must be checked rather than assumed.

Normalize into valid opacity, size, or color ranges. Keep a seed for repeatable
debugging; vary frequency and amplitude independently before combining layers.
Choose a useful sampling density rather than computing invisible detail. Noise
is a visual construction tool, not evidence of natural or physically accurate
behavior.

Constrain particle colors through a palette or bounded color-space parameters
instead of unrelated random RGB channels. A hue parameter is not the same as
the color space used to interpolate endpoints; `hue-rotate()` is also not a
guarantee of constant perceived lightness. Inspect intermediate colors in the
actual effect, not only attractive starting swatches.

## Choose explicit or painted trails

Draw from the previous position to the current one when a fast point otherwise
looks disconnected. Match line width and caps to its shape. Handle zero-length
segments rather than depending on a browser-specific rendering accident.

For controlled per-object trails, retain a bounded history and fade points by
age. A translucent background wash is cheaper to express but affects the whole
canvas, may retain residue, and changes persistence with frame cadence. When a
time-based wash is appropriate, an opacity such as
`1 - Math.exp(-dt / persistenceSeconds)` makes its decay depend on elapsed time;
the persistence must be positive. Profile the scene rather than claiming one
method is universally faster.

## Keep connectors attached to responsive content

Measure both anchors in a shared local space and derive the path from current
endpoints. Reduce a cubic connector's sideways bend as the endpoints align
vertically; account for reversed horizontal order rather than assuming left-to-
right placement. Recalculate after content, font, resize, or other layout
changes that move either anchor.

A fixed viewBox with `preserveAspectRatio="none"` and non-scaling stroke can
stretch a decorative connector; direct local-pixel path coordinates may make
endpoint geometry clearer. Keep stroke thickness and dash behavior intentional.
For an animated normalized path, use the [SVG stroke rules](svg-graphics.md#shapes-and-paths).

## Separate simulation state from drawing

For a grid simulation, compute the next generation from an unchanged previous
generation. Updating cells while reading neighbors makes the result depend on
iteration order. Render cadence and simulation cadence may differ; pausing the
simulation should still allow editing and a correct redraw.

For a paint gesture, choose paint or erase from its initial cell and retain
that mode until release. Repeatedly toggling each revisited cell creates an
unpredictable stroke. For kinetic DOM text, preserve semantic text and use
per-item position/velocity records; guard zero distance before normalizing a
click impulse, and keep base geometry separate from accumulated displacement.

For an explicitly requested typewriter effect, keep one owned schedule and
reset index, rendered fragment, and cursor together on restart. Do not create
parallel writers after repeated activation. Preserve the complete semantic text
and an immediate reduced-motion result rather than making assistive technology
wait through a stream of decorative character updates.
