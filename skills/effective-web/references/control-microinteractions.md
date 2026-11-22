# Control Microinteractions

Use the study that matches the interaction under design or review. Juan Di
Nella's collection documents the mechanics and timings behind each demo. The
values below describe those examples. Choose product timings according to what
the user is controlling. A value under the pointer should track input directly,
a hold indicator measures elapsed time, and a tab underline can settle after
selection has already changed. [Microinteractions collection](https://microinteractions.dev/)

## Actions and choices

**Swapping button labels.** When a short action label reveals a detail such as
download size, stack both labels in one grid cell. Both contribute their
intrinsic width even when one is transparent. Clip the moving text inside the
button and keep the focus outline outside the clip. A reversible CSS
transition lets the pointer leave halfway through the demo's 220 ms swap.
Give the action one accessible name that includes the visible wording. Show
essential details before activation on touch. Try the longest translation and
check that the neighboring control stays under the pointer. [Text swap study](https://microinteractions.dev/text-swap/)

**Holding to confirm.** For an action that warrants deliberate confirmation,
drive the threshold and the progress fill from the same duration. The study's
1,200 ms linear fill makes half the bar mean half the hold. Early release,
Escape, lost pointer capture, and loss of focus cancel the pending action. A
fresh press starts at zero even while the old fill is retracting. Offer an
untimed confirmation path with Cancel initially focused. Both paths should
dispatch the action once. If the operation is asynchronous, distinguish
confirmation from success. Try releasing just before the threshold, pressing
again immediately, and activating without a sustained press. [Hold to confirm study](https://microinteractions.dev/hold-confirm/)

**Moving a radio selection.** Let labeled native radios own the checked value,
keyboard behavior, and submission. The study draws the moving dot in a separate
layer. Overlapping circles with a delayed tail pass through a blur and alpha
threshold to form a continuous shape. Keep text, rings, and focus outlines
outside that filter. On a second choice mid-flight, sample the current head
and tail positions and redirect them. With motion reduced, draw the dot at the
checked input immediately. Arrow through several options quickly and submit
before the effect settles. [Radio group study](https://microinteractions.dev/gooey-radio-group/)

## Navigation and disclosure

**Directional buttons.** A chevron already identifies direction at rest. To
emphasize it on hover, draw a separate shaft and grow it from the tail as the
chevron moves outward. Anchoring the shaft's transform to its own SVG bounds
keeps the far end still. The demo uses a 190 ms transition that reverses on
exit. Keep the hit area stationary, show the focus ring immediately, and let
the first tap navigate. Verify previous and next each have an action name and
still read correctly with all movement disabled. [Chevron study](https://microinteractions.dev/chevron-morph/)

**Expressive link underlines.** On a short editorial navigation row, the
pointer's entry position can set the bend of an SVG underline. Flatten the
curve with a damped vertical scale and preserve stroke thickness. The demo
scales settling time with link width, bounded at 400–1,200 ms. Remeasure when
fonts load or labels resize. This long tail is decorative and can finish after
the link has been activated. Cross two links rapidly, then return from the
opposite side. The new bend should originate at the new entry point. Keyboard
focus and reduced motion can use a static line. [Plucked underline study](https://microinteractions.dev/plucked-underline/)

**Tab selection.** Change the selected tab, panel, and text weight on
activation. Reserve the bold label's width with an invisible sizing copy
excluded from the accessible name. Move one decorative underline using a
translation and horizontal scale derived from the selected tab's bounds in
the list. Recalculate after font or container changes. Select A, C, then B
within the demo's 250 ms travel time. B's panel should already be readable
while the underline turns from its current position. Repeat with arrow keys
and a horizontally scrolled tab list. [Tab indicator study](https://microinteractions.dev/tab-indicator/)

**Carousel position.** Use the track's fractional scroll position to derive
the active dot, counter, and indicator geometry. Advancing the leading edge
first and the trailing edge second makes a swipe visible even between slides.
A tap chooses a slide, while dragging across the dot strip scrubs the track.
Suspend snapping while the strip drives scrolling and restore it on release
or cancellation. Interrupt a programmed jump with a swipe and then reverse
direction. The counter and marker should agree with the visible slide. Keep
individual slide buttons usable with a tap or keyboard when travel and stretch
are disabled. [Carousel dots study](https://microinteractions.dev/worm-dots/)

**Switching FAQ answers.** Give each question a disclosure button associated
with its answer. One decorative background can follow the open item. Measure
the currently rendered panel, switch the expanded state, then measure the new
position and height. These two boxes let an interrupted transition start
where the panel is visible. If switching answers would move the content below
the FAQ, reserve space for the tallest open configuration inside the group,
while fitting the background to the actual answer. Test long–short–long at a
narrow width. Focus should stay on the activated question and the expanded
answer should remain readable with motion disabled. [FAQ panel study](https://microinteractions.dev/faq-panel/)

**Section previews.** Start with named fragment links to real headings. The
study gives each link a full row as its target and varies tick length by
continuous distance from the pointer. One preview card follows hover or focus.
A short opening delay suppresses flashes when crossing the rail, and a closing
delay lets the pointer reach the card. Keep the section currently in view
marked independently of the preview. For a touch preview, the first tap names
the destination and a second tap on it follows the link. Test Escape, crossing
from a link into its card, and following an anchor with scripting disabled.
[Tick rail study](https://microinteractions.dev/tick-rail/)

## Direct manipulation

**Slider value at the edges.** Normalize the native range value between its
minimum and maximum. Use the thumb's actual travel, inset by half its width,
to place the fill and pointer tip. Center the value label there until it
reaches the container edge, then clamp only the label. The tip stays aligned
with the thumb. Apply each input change immediately. A scoped CSS anchor or a
clamped offset can express the same geometry. Try Home and End with the
longest formatted value and two sliders on the page. Each should point to its
own thumb and expose the value and unit once. [Range label study](https://microinteractions.dev/edge-aware-tooltip/)

**Reordering a list.** Lift the item from a dedicated touch grip so the rest of
the row still scrolls. Let it follow the pointer directly. Close its old slot
and mark the proposed insertion point with a line. In the study, neighbors
nudge apart by 8 px at the gap, then by 70% of the previous displacement per
row. Retarget moving neighbors immediately when the user crosses another slot.
On drop, commit the DOM order and keep focus on the moved item. Offer keyboard
pickup, arrow movement, drop, and Escape, plus a click or tap move action for
people who cannot drag. Reverse direction quickly, then cancel and verify the
original order. [List reorder study](https://microinteractions.dev/drag-reorder/)

**Selecting a range of rows.** Snapshot the checkbox states at press time.
The first box's new state determines whether this gesture selects or clears.
On each move, apply it to the inclusive range between the anchor and current
row. Restore rows outside that range from the snapshot. This handles skipped
pointer events and preserves a mixed selection when users backtrack. Commit
on release and restore the snapshot on Escape or pointer cancellation. Keep
ordinary checkbox clicks, Shift+click, and Shift+arrow extension available.
Drag past a previously selected row and back, then cancel. Verify the boxes,
count, and mixed-state header all reflect the restored selection. [Drag selection study](https://microinteractions.dev/drag-select/)

**Resizing a split pane.** Give the narrow visual divider a wider hit area.
Place its grip at pointer entry and track the pointer directly. The study
delays revealing the grip by 60 ms to avoid flashing on a crossing, while the
resize cursor appears immediately. Center the grip for keyboard focus. During
a drag, use one clamped width for the pane and divider, preserving usable
space in the other pane. Expose a named, focusable separator with its current
value, arrow-key adjustment, and Enter to collapse or restore. Provide a
single-pointer sizing option for users who cannot drag. Collapse the pane,
narrow the container, and restore it. Check that the grip remains reachable
and the announced width matches the layout. [Resize handle study](https://microinteractions.dev/resize-handle/)
