# Realism Review

Shared check for generated, edited, and retouched images. Generative models
drift toward perfection, and viewers read that perfection as fake before they
can name why.

## Typical Symptoms

- **Plastic skin:** no pores, stubble, fine lines, or tonal variation; faces
  read as dolls or wax.
- **Sterile light:** even illumination without direction, falloff, or real
  shadows; subjects look pasted into the scene.
- **Perfect symmetry:** mirrored faces, centered everything, identical
  repeated elements.
- **Untouched surfaces:** in generated scenes, fabric, glass, metal, and wood
  without wear, handling traces, or creases where bodies and hands act on them.
- **Weightless objects:** missing contact shadows, no pressure on cushions,
  hands that do not grip, items that float.
- **Optical cleanliness:** no grain, no depth falloff, uniform sharpness from
  foreground to background, a grain or noise pattern that changes between
  subject and background.

When an image feels wrong, check skin and light first; they cause most of it.

## Added Versus Preserved

In [Photo Generation](route-photo-generation.md), realism cues are added on
purpose: material history (handling marks, worn edges, natural creases),
optical behavior (depth of field, grain, slight lens falloff), and organic
irregularity (asymmetry, uneven ground, atmosphere). Choose the few the scene
would really carry; stacking every cue produces a different artificiality.

In [Photo Editing](route-photo-editing.md) and
[Business Portrait Retouch](route-business-retouch.md), the real photograph
already has its grain, asymmetry, and light. The review checks that the edit
kept them; it never adds generated cues to a real photo. Stylistic film
effects on a real photo are a separate, explicit request. Deliberate retouch
refinements such as pressed clothing or softened lines are intended; check
that they keep soft body shading and real fabric texture instead of looking
flat.

## Inspection

Review at full size and at roughly 200 percent on faces, hands, glasses,
hairlines, fabric edges, and object contact points. Compare the same regions
with the source or reference: identity, finger count and anatomy, eyeglass
frames, patterns, text, and background geometry. Check a series side by side
for consistent grade, grain, and retouch strength. Name each concrete defect
so the next run from the original can address it in the prompt.

## Resolution and Upscaling

Generated and edited output stays below camera resolution; report the actual
dimensions and never imply native detail. Upscale only when the use needs it
or the user asks. Prefer a conservative mode, since creative upscalers invent
skin and fabric texture, repeat this review on faces and edges afterwards, and
state that the image was upscaled.
