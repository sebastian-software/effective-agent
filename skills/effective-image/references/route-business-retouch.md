# Business Portrait Retouch

Use the reusable prompt below for a warm, open, professional result that still
looks like a photograph from the same shoot: clothing that looks tailored and
crisply ironed, and people who look like themselves on a very good day:
rested, lightly sun-kissed, slightly fitter, and at most about five years
younger. This route is a preset of [Photo Editing](route-photo-editing.md);
its source and review rules apply, except that this subtle, consented
refinement of the subjects' appearance is the purpose of the edit.

## Source and Reference

Image 1 is always the untouched original, as described in
[Photo Editing](route-photo-editing.md#the-source-stays-the-measure). A new
version of a photo, including one that fixes a missed detail, is a fresh run
from the original with an adjusted photo-specific instruction.

An optional Image 2 is a color reference only, typically an approved edit
whose color treatment the series should match. Transfer only that treatment;
do not copy people, poses, clothing, objects, composition, or light
direction.

## Adapt the Brief

Keep the target's specific pose, gaze, mouth, smile, hands, clothing pattern,
and visible objects explicit in a short photo-specific instruction. Preserve
quiet or side-looking expressions; an open professional appearance does not
mean inventing a smile or camera eye contact.

The template's warm neutral grading is the established default for this
retouch style. Substitute a different user-approved treatment when supplied.
The navy-clothing phrase applies to navy garments; preserve other real garment
colors. Percentages in the brief express relative strength for the model, not
measurable tool settings; the eye-opening limit does not require opening every
eye.

Name in the photo-specific instruction where refinement matters, such as a
beginning double chin, a shirt pulling at the waist, or an unflattering
forehead line, and where it must not touch, such as a characteristic smile
line. Retouch only people who agreed to it; the refinement stays subtle enough
that colleagues would not notice a change, only a good photo.

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
Edit ONLY Image 1. Preserve its original people and their immediately recognizable identity, bone structure, eyes, nose, exact smile and mouth shape, every tooth's shape and position, eyeglass frame, hairstyle, beard, overall build apart from the subtle refinement in point 4, pose, hands and finger anatomy, gaze direction, clothing design, jewelry, watch, all objects, architecture, background geometry, perspective, camera position, original crop and depth of field.
Fabric wrinkles and creases are not part of the clothing design or the pose; they are retouching targets. Preserving the pose means keeping the arm and body positions, not the folds in the fabric.
Most visible change: every shirt, including both sleeves from shoulder to cuff, looks brand new and crisply ironed.
Input role of Image 2, if described as style reference: use ONLY its restrained warm natural color treatment as a loose series reference, never copy its people, clothing, scene, light direction, framing or objects.
Retouch brief:
1. Local face light balancing: softly lift unnecessarily deep under-eye and mouth-adjacent shadows and reduce excessive forehead/nose shine, giving a rested open appearance with believable facial volume. Use subtle photographic dodge/burn, not new lighting or face sculpting.
2. Eyes/glasses: gently reduce the appearance of eyelid puffiness using local shadow corrections; only when visibly squinting ease it very slightly, maximum roughly 5 percent, preserving natural smiling eye crinkles, actual eye shape, iris size, asymmetry and gaze. Substantially reduce distracting bright/tinted lens glare over eyes, leaving faint realistic glass reflections. Preserve existing catchlights; no new highlights, whitening or enlarged eyes.
3. Skin and grooming: remove blemishes, small spots, razor irritation and broken capillaries, and balance excessive orange/red patches on cheeks, ears, nose, neck or hands to natural skin tones. Give the skin a fresh, rested glow as after a few relaxed days outdoors: a slightly warmer, healthy tone with a faint sun-kissed warmth on cheeks, nose and forehead, evenly blended into neck and hands; never orange, bronzed, red or visibly tanned. Give the effect of light professional grooming makeup that nobody would notice: even complexion, matte forehead and nose, softened dark circles. Soften deep or unflattering wrinkles such as heavy forehead furrows, deep nasolabial folds and neck lines by about half; keep the smile lines and eye crinkles that carry warmth. Preserve pores, beard stubble, natural skin texture and different complexions of different people.
4. Subtle fitness refinement: make each person look slightly fresher, fitter and at most about five years younger, as on a very good day. Brighten teeth very slightly to a natural, clean ivory by removing yellow or grey tint only, never bright white, and keep every tooth's shape, size and position. Gently tighten the under-chin and jawline to remove the beginning of a double chin, and very slightly slim cheeks, neck, waist and torso, as if a few kilograms lighter, never more than about 5 percent in width. Keep face shape, head size, bone structure, hands and posture recognizably the same; no visible reshaping, warping or bent background lines.
5. Clothes: shirts must look brand new, crisply ironed and tailored. Remove about 90 percent of all shirt creases, including pull lines at the waist and stomach, button-strain folds, wrinkles on sleeves and forearms and fabric bunching at the cuffs, so shirt surfaces are smooth with only soft, gradual shading that shows the body underneath. Each sleeve becomes a smooth, slightly fitted tube of pressed fabric that follows the arm with soft, continuous shading, as freshly ironed as the shirt front: smooth upper arms, smooth forearms and a clean transition into the cuff. Even when both arms are bent, allow at most one soft, shallow fold at each inner elbow; everything else on the sleeve is smooth. Smooth excess fabric billowing at the waist and sleeves so clothing follows the body cleanly. Jackets get the same pressed look with about three quarters of their creases removed. Neaten collar or placket irregularities and visible lint without changing garment design, seams, buttons, lapels, pockets, stripes/checks, fabric weave or sheen. Keep tailored jackets naturally dimensional.
6. Background: subtly dim competing bright windows, lamps or wall patches and reduce distracting background color intensity where necessary, directing attention to the people. Keep every real background object and detail in its original place and retain the actual shoot setting and authentic depth of field. No background replacement, artificial blur or obvious vignette.
7. Series finishing: coherent warm neutral editorial color treatment, soft highlight rolloff, natural balanced skin, rich navy clothes and gentle clean contrast. Retain real indoor/outdoor light differences. Selective crispness on actual eyes, hair and fabric only, no fake detail or skin sharpening. Keep the photograph's own fine grain uniform across skin, clothing and background.
Overall result should be an improved real photo from the same shoot: warm, open, professional, natural, with the same people looking at their best. No plastic skin, glamour beauty filter, visible makeup, bright white teeth, whitened eyes, fake tan, obvious rejuvenation or slimming, changed face shape, saturation boost, HDR, added objects, changed logos/text, border or watermark.
Return exactly one full original composition retouched photograph, matching Image 1's portrait/landscape orientation and original aspect ratio. Use the largest supported native output resolution.
Strict preservation: never add a laptop, cup, phone, props or any other item absent from Image 1. Do not introduce objects from related shoot scenes. Do not manufacture etched or squiggly skin texture.
~~~

Reference-role sentence, added when Image 2 is supplied:

~~~text
Image 2 is only a color treatment reference. Image 1 is the original edit target.
~~~

Photo-specific example:

~~~text
The subject is smiling while seated at a wooden table. Preserve the exact
smile, gaze, hands, watch, cup, and table. Make the shirt and both sleeves
crisply ironed from shoulder to cuff; allow at most one soft, shallow fold at
each inner elbow.
~~~

## Batch Through the Images API

When built-in Imagegen returns too little resolution, or a whole folder needs
the approved look, run `scripts/retouch_batch.py` with `OPENAI_API_KEY` set.
It reads the prompt above, sends each original as Image 1 to the script's
default image model (`--model` overrides it) at the largest size the script
computes for the aspect ratio, using the limits documented for `gpt-image-2`
(about 8.3 megapixels, partly experimental), and saves each result as
`<source>-retouched.png` with a `.prompt.json` record of the prompt, size,
and color reference. Existing outputs are skipped unless `--force` is passed.

~~~sh
scripts/retouch_batch.py ORIGINALS_DIR --reference APPROVED_EDITS_DIR --notes notes.json --dry-run
~~~

`--reference` adds the color reference for every source, or by matching
source stem when it is a folder. `--notes` maps source stems to the photo-specific instruction. Run
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
