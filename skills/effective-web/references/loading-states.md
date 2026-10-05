# Loading States

Communicate system status during wait times without pretending to know a layout
that has not loaded yet. Prefer real component states, honest empty/loading
regions, and accessible progress indicators over skeleton screens that imitate
the final UI poorly.

## Response Time Thresholds

Three response time limits govern which feedback pattern to use (Jakob Nielsen, NNGroup):

| Threshold | User Perception | Required Feedback |
|-----------|----------------|-------------------|
| **< 100ms** | Instantaneous, direct manipulation | None - display result immediately |
| **100ms - 1s** | Noticeable delay, thought flow unbroken | Subtle indicator (cursor change, button state) |
| **1s - 10s** | Conscious waiting, attention held | Real component loading state or local status indicator |
| **> 10s** | Attention lost, user may leave | Determinate progress bar with cancel option |

**Guidelines:**
- Provide visual feedback the moment a user initiates an action (button state change, page transition)
- Showing a loader for waits under 1 second harms perceived performance - delay the indicator by 300ms
- For 2-10 second waits, combine a scoped busy state with inconspicuous progress updates
- For waits over 10 seconds, show estimated completion time and a clear way to cancel

## Real Component Loading States

Do not build a fake version of the future UI. Skeletons often become a second,
inaccurate implementation of the component: wrong row counts, wrong line
lengths, wrong image ratios, wrong density, wrong responsive behavior. Users
learn a layout that changes under them seconds later.

Prefer one of these patterns:

1. **Existing component with pending content:** Render the real component
   shell, labels, controls, and stable layout. Mark the region as busy and show
   a small status indicator where content is unavailable.
2. **Empty-state-shaped loading:** If the component's meaningful state is "no
   content yet", use the real empty-state layout with copy like "Loading
   projects..." and a local indicator.
3. **Neutral loading region:** If the component cannot be rendered yet, show a
   compact status block that does not imply rows, cards, charts, or copy that
   may not exist.
4. **Determinate progress:** For uploads, exports, imports, generation, or
   multi-step work, show measurable progress and cancellation when possible.

### Real Component Example

```html
<section aria-busy="true" aria-live="polite" class="project-list">
  <header class="project-list__header">
    <h2>Projects</h2>
    <button type="button">Create project</button>
  </header>

  <div class="project-list__status" role="status">
    <svg aria-hidden="true" class="spinner" viewBox="0 0 24 24">...</svg>
    <span>Loading projects...</span>
  </div>
</section>
```

This preserves the real component boundary and action area without guessing how
many projects, rows, avatars, or metadata fields will arrive.

### When a Skeleton Is Acceptable

Use a skeleton only when all of these are true:

- The final structure is deterministic before data arrives.
- The skeleton is generated from the same component primitives as the real UI.
- The dimensions, responsive behavior, and density match the real component.
- The skeleton is static by default and respects reduced motion when animated.

If any of these are false, use a real component loading state or neutral status
indicator instead.

## Spinners and Progress Indicators

### Indeterminate Indicators (Spinners)

Use when the wait duration is unknown or between 1-10 seconds:

- Animated spinner or circular indicator showing system activity
- No timeline information - signals "something is happening"
- Place near the content being loaded, not centred on the page
- Include descriptive text: "Loading comments..." or "Updating settings..."

### Determinate Indicators (Progress Bars)

Use for waits over 10 seconds or when processing measurable units:

- Visual bar filling from 0-100%
- Shows current progress, completion status, and remaining work
- Start the animation slower and accelerate toward completion - exceeding expectations creates more satisfaction than disappointing early speed
- Provide approximate timeframes: "About 3 minutes remaining"
- Always provide a cancel option for long processes

### Placement Guidelines

- Place the indicator where the user is already looking
- Full-page loads: stable page shell plus a local status region in the content area
- Button actions: spinner inside the button (see Button Loading States)
- List/feed: spinner at the bottom of existing content
- Modal actions: spinner within the modal

## Button Loading States

When a button triggers an action that takes more than 300ms, show a loading state on the button itself. Users are already looking at the button when they click it.

### Implementation Pattern

```html
<button type="submit" class="btn btn--primary" aria-busy="false">
  <svg class="btn__spinner" aria-hidden="true" viewBox="0 0 24 24"
       fill="none" stroke="currentColor" stroke-width="2">
    <circle cx="12" cy="12" r="10" opacity="0.25" />
    <path d="M12 2a10 10 0 0 1 10 10" stroke-linecap="round" />
  </svg>
  <span class="btn__label">Save post</span>
</button>
```

```css
.btn__spinner {
  display: none;
  width: 1em;
  height: 1em;
  animation: spin 0.6s linear infinite;
}

.btn[aria-busy="true"] .btn__spinner {
  display: inline-block;
}

.btn[aria-busy="true"] .btn__label {
  /* Optionally change label text via JS: "Save post" -> "Saving..." */
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (prefers-reduced-motion: reduce) {
  .btn__spinner {
    animation-duration: 1.5s;
  }
}
```

### Button Loading Guidelines

- The spinner must not change the button dimensions - reserve space or replace the icon
- Change the label to describe the ongoing process: "Save post" becomes "Saving..."
- Prevent double submission: set `aria-disabled="true"` during loading
- Prefer `aria-disabled="true"` over `disabled` - `aria-disabled` keeps the button focusable and discoverable by screen readers, but it does not block activation: guard the click or submit handler while loading, and keep the server tolerant of duplicates
- Set `aria-busy="true"` on the button to indicate processing
- On success, briefly show a check icon or "Saved" before restoring the default state

### `aria-disabled` vs `disabled`

```css
/* aria-disabled: stays focusable, screen readers can still reach it */
.btn[aria-disabled="true"] {
  opacity: 0.6;
  cursor: not-allowed;
  pointer-events: none;
}

/* disabled: removed from tab order, invisible to some screen readers */
.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
```

Use `aria-disabled="true"` for loading states. Use the native `disabled` attribute only when a button is permanently unavailable (and provide an explanation why).

## Optimistic UI

Optimistic UI shows the result of an action before the server confirms it, making the interface feel instant. The UI assumes success and rolls back only if the server returns an error.

### When to Use Optimistic UI

**Good candidates:**
- Like/favourite toggles
- Adding items to a list
- Marking items as read/unread
- Simple state changes with high success rates (> 99%)
- Server response time under 2 seconds

**Avoid for:**
- Payment processing
- Account deletion or other destructive actions
- Actions with complex server-side validation
- Operations that depend on external services with unreliable availability
- Anything where showing a false success state causes real harm

### Implementation Pattern

```javascript
async function toggleFavourite(itemId) {
  // 1. Store previous state for rollback
  const previousState = getItemState(itemId);

  // 2. Apply optimistic update immediately
  updateUI(itemId, { isFavourite: !previousState.isFavourite });

  try {
    // 3. Send request to server in background
    await api.toggleFavourite(itemId);
  } catch (error) {
    // 4. Rollback on failure
    updateUI(itemId, previousState);
    showToast("Could not update. Please try again.");
  }
}
```

### Rollback Strategy

- Always store the previous state before applying the optimistic update
- On failure, revert to the stored state and show a non-intrusive error (toast notification)
- Never silently fail - the user must know the action did not complete
- Keep rollback animations subtle: a quick fade is enough, avoid dramatic reversals

## Accessibility

### `aria-busy` for Loading Regions

Set `aria-busy="true"` on a container while its content is being updated. This tells assistive technology to wait before announcing the new content:

```html
<section aria-busy="true" aria-live="polite">
  <!-- Real component loading state or local status indicator -->
</section>
```

When loading completes:
1. Replace unavailable content with real content
2. Set `aria-busy="false"`
3. The `aria-live="polite"` region will then announce the update

**Caveats:**
- Support for `aria-busy` varies across browser/screen reader combinations
- Pair `aria-busy` with a visible or visually hidden status message
- Include a visually hidden "Loading" text that screen readers can announce

### Visually Hidden Loading Text

```css
.visually-hidden {
  position: absolute;
  overflow: hidden;
  clip: rect(1px, 1px, 1px, 1px);
  width: 1px;
  height: 1px;
  white-space: nowrap;
}
```

```html
<div aria-busy="true">
  <span class="visually-hidden">Loading content</span>
</div>
```

### `aria-live` Regions for Status Updates

Use `aria-live="polite"` for loading completion announcements. Use `aria-live="assertive"` only for errors that require immediate attention:

```html
<div role="status" aria-live="polite">
  <!-- Empty initially, populated on completion -->
</div>
```

### Screen Reader Announcements

- Announce the start of loading: "Loading articles"
- Announce completion: "5 articles loaded"
- Announce errors: "Failed to load articles. Try again."
- Do not announce decorative loading graphics or animation frames

### Reduced Motion

Always respect `prefers-reduced-motion`. Slow or disable spinner animation when
the motion itself is not essential:

```css
@media (prefers-reduced-motion: reduce) {
  .spinner {
    animation-duration: 1.5s;
  }
}
```

### Cursor Feedback

Set `cursor: progress` on loading regions so mouse users see visual feedback:

```css
[aria-busy="true"] {
  cursor: progress;
}
```

## Perceived Performance

Perceived performance is how fast the interface feels, regardless of actual load time. Improving perceived performance often has a greater impact on user satisfaction than improving actual speed.

### Progressive Loading

Load and display content in stages, most important first:

1. Render the page shell (navigation, layout structure) immediately
2. Render real component boundaries and local status regions for unavailable content
3. Load primary content (headings, first paragraph, hero image)
4. Load secondary content (comments, recommendations, sidebar)

### LCP Optimisation

Largest Contentful Paint should be under 2.5 seconds for 75% of page visits:

- Never lazy-load the LCP element - set `fetchpriority="high"` on it
- Inline critical CSS or keep stylesheets smaller than the LCP resource
- Avoid third-party domains for the LCP image (reuse existing connections)
- Use responsive images with `srcset` and modern formats (AVIF, WebP)
- Implement server-side rendering so images are discoverable from HTML source

### Lazy Loading

Defer off-screen content to prioritise visible content:

```html
<!-- LCP image: never lazy-load, high priority -->
<img src="hero.avif" alt="..." fetchpriority="high" width="800" height="450">

<!-- Below-fold images: lazy-load -->
<img src="feature.avif" alt="..." loading="lazy" width="400" height="300">
```

### Prevent Layout Shift with `aspect-ratio`

Images and embeds without dimensions cause content to jump when they load. Always set `aspect-ratio` or explicit `width`/`height`:

```css
.card__image {
  width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: cover;
  background: oklch(92% 0.005 0); /* Placeholder colour while loading */
}
```

This reserves space in the layout before the image arrives, preventing Cumulative Layout Shift (CLS target: < 0.1).

## Decision Matrix: When to Use Which Pattern

| Scenario | Wait Time | Pattern | Why |
|----------|-----------|---------|-----|
| Button form submit | 0.3-2s | Button spinner + label change | User already looking at button |
| Like/toggle action | < 2s | Optimistic UI | High success rate, instant feel |
| Full page load | 1-10s | Stable shell + local status region | Honest feedback without fake layout |
| Single component load | 1-5s | Inline spinner with text | Localised feedback |
| File upload | 5-60s | Determinate progress bar | User needs progress and cancel option |
| Background save | < 2s | No indicator (or subtle) | Don't interrupt workflow |
| Search results | 1-3s | Existing results stay visible, status near filters | Avoids blanking the page during refetch |
| Infinite scroll | 0.5-3s | Spinner at list bottom | Contextual, non-blocking |
| Data export | 10s+ | Progress bar + cancel | Long process needs completion estimate |

## Common Loading State Mistakes

### Mistake 1: Layout shift when loading state appears or disappears
- Loading indicator insertion pushes surrounding elements
- Spinner insertion pushes surrounding elements
- Fix: Reserve exact space with `aspect-ratio`, fixed heights, and `min-height`

### Mistake 2: Blocking all interaction during loading
- Disabling the entire page when only one section is loading
- Fix: Scope the loading indicator and `aria-busy` to the specific region being updated

### Mistake 3: No feedback at all for 1-2 second waits
- Users assume their click did not register and click again
- Fix: Provide instant visual feedback (button state change) within 100ms, show spinner after 300ms

### Mistake 4: Showing a spinner for under 300ms
- A flash of spinner creates visual noise and feels broken
- Fix: Delay showing the spinner by 300ms - if the action completes before then, skip it

### Mistake 5: No rollback for optimistic UI
- Silently swallowing server errors after showing optimistic success
- Fix: Always store previous state and revert on failure with a clear error message

### Mistake 6: Fake skeleton that does not match the loaded layout
- Users build incorrect mental models from misleading placeholders
- Fix: Prefer a real component loading state or neutral status block; use skeletons only when generated from the same primitives as the final component

### Mistake 7: Animated loading effect with no reduced motion support
- Can trigger vestibular disorders in users with motion sensitivity
- Fix: Wrap non-essential loading animation in `@media (prefers-reduced-motion: no-preference)` or slow it down under `reduce`

### Mistake 8: Blank content area with only global chrome visible
- Header and footer with empty content area looks broken, not loading
- Fix: Put status feedback in the content area that is actually waiting

### Mistake 9: No screen reader announcements
- Sighted users see the spinner, but screen reader users get no feedback
- Fix: Use `aria-busy`, `aria-live`, visually hidden loading text, and announce completion

### Mistake 10: Progress bar that stalls or jumps backward
- Destroys user trust in the estimated completion
- Fix: Start slower and accelerate toward completion - never move backward

## Chapter Summary

1. Use response time thresholds to pick the right feedback pattern: no indicator under 100ms, subtle change up to 1s, real component loading state or local status for 1-10s, progress bar over 10s
2. Avoid fake skeleton UIs by default; use real component states, empty-state-shaped loading, or neutral status blocks
3. Delay showing spinners by 300ms to avoid flashing indicators on fast responses
4. Button loading states belong on the button itself: inline spinner, label change ("Saving..."), `aria-busy="true"`, and `aria-disabled="true"` to prevent double submission
5. Use optimistic UI for simple, high-success-rate actions (likes, toggles) - always store previous state and roll back on failure
6. Announce loading to screen readers with `aria-busy`, `aria-live="polite"`, and visually hidden status text - announce both start and completion
7. Respect `prefers-reduced-motion` for spinners, progress indicators, and any optional loading animation
8. Prevent layout shift with `aspect-ratio` on images and embeds, and ensure loading indicators do not resize their containers
9. Optimise LCP by never lazy-loading the largest content element and setting `fetchpriority="high"`
10. Use determinate progress bars for waits over 10 seconds - start slow, accelerate toward completion, and always provide a cancel option
11. Scope loading indicators to the specific region being updated - never block the entire page when only one section is loading
