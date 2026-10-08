# Business Portrait Retouch

Use the reusable prompt below for a warm, open, professional result that still
looks like a photograph from the same shoot. It supports more visible shirt
smoothing while keeping facial corrections restrained. This route is a preset
of [Photo Editing](route-photo-editing.md); its source and review rules apply.

## Source and Reference Roles

Inspect the original and any previous edits before editing. Image 1 is always
the actual target. An optional Image 2 has exactly one declared role:

- **Color reference:** transfer only the approved color treatment. Do not copy
  people, poses, clothing, objects, composition, or light direction.
- **Identity reference:** when refining an already approved edit, use the
  original to check identity, anatomy, expression, and scene. Keep Image 1's
  approved color treatment.

Use the original for a first pass and the approved edit for a requested
refinement. Do not keep reprocessing successful outputs without a concrete
reason.

## Adapt the Brief

Keep the target's specific pose, gaze, mouth, smile, hands, clothing pattern,
and visible objects explicit in a short photo-specific instruction. Preserve
quiet or side-looking expressions; an open professional appearance does not
mean inventing a smile or camera eye contact.

The template's warm neutral grading is the established default for this
retouch style. Substitute a different user-approved treatment when supplied.
The navy-clothing phrase applies to navy garments; preserve other real garment
colors. The approximate eye-opening limit is a restraint on the edit, not a
measurable tool setting or a requirement to open every eye.

If the user requests initial proposals, show a few representative before/after
pairs first. Once a look is approved, apply it consistently to the authorized
series while respecting indoor/outdoor lighting differences. Do not require
another approval for each photograph.

## Reusable Imagegen Prompt

Declare the reference role and append the photo-specific instruction after
this prompt. Omit the Image 2 sentence when no second reference is supplied.

~~~text
Use case: identity-preserve.
Asset type: polished, welcoming and professional business photo shoot retouch.
Edit ONLY Image 1. Preserve its original people, identity, anatomy, age, facial structure, exact mouth/teeth/smile, eyeglass frame, hairstyle, beard, body proportions, pose, hands and finger anatomy, gaze direction, clothing design, jewelry, watch, all objects, architecture, background geometry, perspective, camera position, original crop and depth of field.
Input role of Image 2, if described as style reference: use ONLY its restrained warm natural color treatment as a loose series reference, never copy its people, clothing, scene, light direction, framing or objects.
Retouch brief:
1. Local face light balancing: softly lift unnecessarily deep under-eye and mouth-adjacent shadows and reduce excessive forehead/nose shine, giving a rested open appearance with believable facial volume. Use subtle photographic dodge/burn, not new lighting or face sculpting.
2. Eyes/glasses: gently reduce the appearance of eyelid puffiness using local shadow corrections; only when visibly squinting ease it very slightly, maximum roughly 5 percent, preserving natural smiling eye crinkles, actual eye shape, iris size, asymmetry and gaze. Substantially reduce distracting bright/tinted lens glare over eyes, leaving faint realistic glass reflections. Preserve existing catchlights; no new highlights, whitening or enlarged eyes.
3. Skin: remove isolated transient blemishes only and balance small patches of excessive orange/red on cheeks, ears, nose, neck or hands to their original natural skin tones. Preserve pores, beard stubble and age/smile lines. Maintain different complexions of different people.
4. Clothes: make shirts visibly smooth and freshly pressed, especially chest, shoulders and sleeves. Remove distracting tight/random creases and accordion wrinkles, keeping only broad soft folds physically needed by the pose. Neaten obvious collar or placket irregularities and isolated visible lint without changing garment cut, seams, buttons, lapels, pockets, stripes/checks, fabric weave or sheen. Preserve exact body/garment outline. Keep tailored jackets naturally dimensional.
5. Background: subtly dim competing bright windows, lamps or wall patches and reduce distracting background color intensity where necessary, directing attention to the people. Keep every real background object and detail in its original place and retain the actual shoot setting and authentic depth of field. No background replacement, artificial blur or obvious vignette.
6. Series finishing: coherent warm neutral editorial color treatment, soft highlight rolloff, natural balanced skin, rich navy clothes and gentle clean contrast. Retain real indoor/outdoor light differences. Selective crispness on actual eyes, hair and fabric only, no fake detail or skin sharpening. Keep the photograph's own fine grain uniform across skin, clothing and background.
Overall result should be an improved real photo from the same shoot: warm, open, professional, natural. No plastic skin, glamour beauty filter, whitening of teeth/eyes, age changes, face/body reshaping, saturation boost, HDR, added objects, changed logos/text, border or watermark.
Return exactly one full original composition retouched photograph, matching Image 1's portrait/landscape orientation and original aspect ratio. Use the largest supported native output resolution.
Strict preservation: never add a laptop, cup, phone, props or any other item absent from Image 1. Do not introduce objects from related shoot scenes. Do not manufacture etched or squiggly skin texture.
~~~

Reference-role examples:

~~~text
Image 2 is only a color treatment reference. Image 1 is the original edit target.
~~~

~~~text
Image 2 is an identity/anatomy reference only. Preserve Image 1's approved grade.
~~~

Photo-specific example:

~~~text
The subject is smiling while seated at a wooden table. Preserve the exact
smile, gaze, hands, watch, cup, and table. Smooth the shirt sleeves and
shoulders substantially; keep broad elbow folds physically needed by the pose.
~~~

## Batch Through the Images API

When built-in Imagegen returns too little resolution, or a whole folder needs
the approved look, run `scripts/retouch_batch.py` with `OPENAI_API_KEY` set.
It reads the prompt above, sends each source as Image 1 to
`gpt-image-2.5-sunburst` at the largest supported size for its aspect ratio
(about 8.3 megapixels; sizes above 2560 × 1440 are experimental), and saves
each result as
`<source>-retouched.png` with a `.prompt.json` record of the prompt, size,
and reference role. Existing outputs are skipped unless `--force` is passed.

~~~sh
scripts/retouch_batch.py SOURCE_DIR --reference APPROVED_EDITS_DIR --notes notes.json --dry-run
~~~

`--reference` adds Image 2 for every source, or by matching source stem when
it is a folder; `--reference-role` selects `color` (default) or `identity`.
`--notes` maps source stems to the photo-specific instruction. Run
`--dry-run` first to check the plan and prompt without calling the API.

## Review and Delivery

Deliver as in [Photo Editing](route-photo-editing.md#review-and-delivery).
For portraits, check expression drift, clothing patterns, and added or missing
objects against each result's own original.

Show comparable framing in before/after views. Resizing for a contact sheet or
comparison is presentation work, not additional retouch. Report actual output
dimensions and any material detail changes, following the
[Realism Review](realism-review.md#resolution-and-upscaling). An optional
curated selection should favor relaxed expressions and useful variety, not
maximum retouch strength.

If Imagegen is unavailable, preserve the prompt and explain the limitation
rather than silently changing tools. Uploading, publication, or optimizer
configuration remains a separate authorized task.
