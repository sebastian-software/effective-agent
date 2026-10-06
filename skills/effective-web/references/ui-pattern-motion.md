# Motion Pattern Review

Use this module for repeated effects, false activity, hidden content, or
unjustified changes to familiar interaction. Apply the context and evidence
distinction in [UI anti-patterns](ui-antipatterns.md).

## Motion and Interaction Reflexes

- Every section receives the same reveal animation regardless of content.
- Images scale, rotate, or drift on every card hover without indicating an
  action or revealing information. An interactive gallery can justify image
  motion; keyboard and touch users need equivalent access to its information.
- Bounce, spring, glow, or continuous motion is applied to frequent task UI.
  Reserve expressive motion for an earned, non-blocking moment and keep the
  reduced-motion path complete.
- Pulsing dots, blinking cursors, and loops imply activity that the product does
  not have. Tie them to real state or clearly intentional presentation, and
  choose timing and easing for response, distance, and character.
- Important content starts hidden until a reveal script runs, or reading waits
  on scroll progress, pinning, or parallax. Preserve a readable fallback and
  orientation; a deliberate controlled experience can still use those devices.
- Marquees make readers wait for moving content. Keep the content understandable
  and controllable through pause or a static alternative.
- Cursor followers and magnetic buttons alter familiar pointer or target
  behaviour without a useful interaction benefit. A deliberate experiment needs precise targets,
  a conventional fallback, and usable keyboard and touch paths.
- Width, height, margin, or padding animation causes avoidable layout work.
  Measure expensive filters and layout transitions on the target device;
  transform/opacity is a useful starting point, not the entire motion palette.
- Every action is styled as primary, so the interface has no decision hierarchy.
- Mobile removes important actions because the desktop layout does not fit.

Distinguish style from behavior. A playful spring can be an accepted exception;
hidden functionality, inaccessible motion, or layout jank remains a defect.
