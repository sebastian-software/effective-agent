---
name: effective-image
description: >-
  Edit real photos and generate new photoreal images with Imagegen: cleanup,
  backgrounds, product composites, natural business portrait retouch across a
  shoot, and new scenes or brand visuals that look like real photographs.
  Commercial copy belongs to effective-marketing; browser implementation to
  effective-web.
---

# Effective Image

Choose the route that matches the image task. Read only its relevant
references and keep the requested outcome, source roles, and delivery format
explicit.

## Route by Intent

| User intent | Read |
| --- | --- |
| Change an existing photo: clean up, remove or replace objects, change the background, correct color or light, or insert a real product | [Photo Editing](references/route-photo-editing.md) |
| Retouch business portraits, prepare before/after proposals, or apply an approved natural look across a shoot | [Business Portrait Retouch](references/route-business-retouch.md) |
| Create a new photoreal image or series: scenes, brand and lifestyle visuals, product settings, or a less artificial-looking AI image | [Photo Generation](references/route-photo-generation.md) |

## Routing Boundaries

Route by the starting point: an existing photograph is edited and stays the
measure of truth; a new image is generated and gets realism deliberately.
Business retouch is the portrait preset of editing; do not turn its prompt
into a default for other edits. A generated scene that receives a real product
or person moves to editing for that insertion. All routes share the
[Realism Review](references/realism-review.md). Illustration, graphic design,
and stylized art are not covered.

Commercial messaging and image placement strategy belong to
`effective-marketing`; browser implementation belongs to `effective-web`.
Publishing images to storage or enabling a CDN optimizer requires its own
destination and task authorization; using this skill alone does not authorize
either action.
