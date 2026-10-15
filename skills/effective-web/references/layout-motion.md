# Layout Motion

Use when Motion for React layout or shared-layout behavior is already chosen or
needed for interruptible movement of live interface elements. Reuse the
installed package and verify its API; this is not a requirement to adopt a
library for ordinary CSS transitions. The following API examples were checked
against Motion's documentation in October 2026.

## Commit layout, animate the difference

Put the final arrangement in normal CSS and React data. Let `layout` animate
the measured difference instead of keeping a second animated position model.
Use `layout="position"` when size interpolation would stretch content. For size
changes, direct children may need their own `layout` correction; expose radius
and supported shadow values through Motion styles/props when correction is
needed. Measure the actual box: a full-width text wrapper can stay fixed while
the glyphs move inside it. See [layout animation](https://motion.dev/docs/react-layout-animations).

## Preserve object identity and scope

- Derive React keys and `layoutId` from stable item identity, never the current
  array index or freshly generated randomness. Keep ordered collections in
  data so adding, removing, and restoring items have predictable destinations.
- Share a `layoutId` only between representations of the same conceptual
  object. Namespace independent component instances through `LayoutGroup id`
  or a shared instance prefix. Generating separate prefixes at each end of an
  intended connection prevents the match.
- Use a common `LayoutGroup` when related components affect one another's
  geometry without rendering together. Fix identity and measurement ownership
  before compensating for teleports with arbitrary transform offsets.
- For fixed or scrollable containers, inspect `layoutRoot` or `layoutScroll`
  rather than guessing page-offset corrections. Preserve reading order, focus,
  and labels independently of the visual travel.

See [layout grouping and namespaces](https://motion.dev/docs/react-layout-group).
For React-generated instance prefixes, [useId](https://react.dev/reference/react/useId)
is suitable; item data must still supply list keys.

## Preserve preferences and rendering boundaries

Set `MotionConfig reducedMotion="user"` when using that library's layout and
transform animation. Review opacity, custom loops, CSS, and sound separately;
the provider does not stop unrelated effects. In a Server Component framework,
keep the preference-aware provider in a small client wrapper that accepts
server-rendered children rather than moving the root's whole module graph to
the client. See [MotionConfig](https://motion.dev/docs/react-motion-config).

Use `initial={false}` when stable initial content should appear directly at its
target. Check repeated input and reverse travel in the real component, including
rapid transfers between collections, removal of the focused item, and reduced
motion. A successful uninterrupted demonstration does not prove correct
identity, focus, or interruption behavior.

## Distinguish framework and browser transitions

React scheduling transitions are not the browser View Transition API. When
integrating snapshots manually, coordinate capture with the actual DOM commit;
scheduling a state update alone does not establish that the destination DOM is
ready. Follow the installed framework's documented integration. For snapshot
overlay, clipping, and hit-testing behavior, use the
[View Transition details](view-transition-details.md).
