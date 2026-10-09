# Route: Change Screenshots

Use this route to show what a branch or pull request changes on rendered pages:
before/after captures, the changed areas found by comparison, and annotations a
reviewer can read at a glance. This route produces the images and captions;
publishing them in a pull request description belongs to `effective-delivery`.

## Decide Whether Screenshots Earn Their Place

Screenshots help only when the change can alter rendered output: components,
styles, tokens, assets, copy, routes, or a build or dependency change that
reaches the page. Documentation, tests, tooling, and backend-only changes get
no screenshots; say so instead of publishing an empty section.

Choose pages from the change. Changed routes and the direct renderers of changed
components come first; for shared tokens and primitives, follow the bounded
consumer expansion in [change-scoped review](change-scoped-interface-review.md).
When every page of a static or prerendered site can be captured cheaply, compare
them all and show only the pages that differ: the comparison filters better than
a guess.

Capture a desktop width and a narrow mobile width. Add an interaction state, such
as an open menu or a validation error, only when the change is about that state.

## Capture Both Revisions Comparably

- Capture the merge base, not a stale default branch, and the head with the same
  browser, viewport, device scale factor, locale, theme, data, and origin. Pages
  that print their own URL or build absolute links differ on another origin.
- Stabilize as for visual tests: follow the motion, font, and dynamic-content
  rules in [visual regression stability](visual-regression-stability.md). Scroll
  through the page once so lazy content loads, then decode images.
- Bound every wait, for example to ten seconds. One hanging third-party request
  must not abort the run; a capture after a timeout is still evidence, and the
  confirmation below catches what it got wrong.
- Assets that are uploaded only on deployment, such as images on an asset CDN,
  appear broken in the head capture. Serve those new files from the build for
  that capture instead of reporting a broken image as the change.
- Take full-page captures and keep them until the comparison is done.

## Find What Changed

Pixel comparison at fixed coordinates, as in odiff, pixelmatch, or ImageMagick,
suits baselines whose layout must not move. It is wrong for a change: inserted
or removed content shifts everything below it, and the whole rest of the page
reads as changed. Use the bundled dependency-free script instead (the path is
relative to this skill):

```sh
node scripts/visual-change-boxes.mjs before.png after.png --scale 2
```

`--scale` is the device scale factor of the captures. The script aligns rows the
way a text diff aligns lines and reports each change as `added`, `changed`, or
`removed` (where content used to be). Inside content that only moved, it
tolerates the anti-aliasing differences of a fractional pixel offset; content
that kept its position is compared exactly. Its JSON output holds the changes in
device pixels, numbered annotations in CSS pixels, a caption legend, and an
`overlayScript`.

- Count a change only when a second pair of captures reports it too. A change
  that disappears was timing or loading; content that differs on every load,
  such as clocks, random order, live data, or ads, needs fixed data or masking.
- Rows are compared across the full width. Content that moves within one column
  next to a static column is framed as one `changed` block.
- Inside moved content, a replacement with nearly the same outline and density,
  such as one digit in a dense table, can stay below the tolerance. When such a
  detail is the point of the change, compare that region directly.
- The comparison says what differs, not whether it improved.

## Annotate on the Page

Evaluate `overlayScript` in the settled head page, for example with Playwright's
`page.evaluate(script)` or a browser tool's evaluate command, then capture again.
Drawn in the page, labels stay sharp at every scale, and the overlay is clipped
to the page so its size does not change.

The overlay follows a convention reviewers cannot mistake for product UI: dashed
frames with a white halo and white bold labels outside the marked content,
numbered in reading order per capture. Green `NEW` marks added content, violet
`CHANGED` changed content, and a red `REMOVED` line marks where content was
removed. Do not use the product's own colors or control shapes for annotations,
and never change product content, data, or styling to make a capture look
better.

## Crop and Caption

- Crop a tall capture to the band holding its annotations plus some context,
  about 300 CSS pixels above and below; keep short captures whole.
- Give each changed page one heading, desktop and mobile side by side, and a
  legend row such as `NEW 1, REMOVED 2`. State once that frames and labels are
  review annotations, not product UI. Add a sentence per number when its meaning
  is not obvious from the image.
- List removed pages, and the compared pages without changes in a collapsed
  list, so reviewers see the coverage.
- Inspect every image before handing it on: synthetic or demo data only, and no
  secrets, personal data, private documents, or internal URLs.

Hand the images and the section to `effective-delivery` for publication. Keep
image files out of the repository.
