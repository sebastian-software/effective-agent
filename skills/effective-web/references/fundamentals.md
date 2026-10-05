# Fundamentals

> Deep appendix. Start from [fundamentals-core.md](fundamentals-core.md); load this file only for the full historical design and motion treatment.

Overarching UI design principles that form the foundation of all guidelines.

## Minimise Usability Risks

Base design decisions on risk - the risk that someone could have difficulty using an interface.

**Common usability risks:**
- Thin, light grey text - some may find it difficult to read
- Icons without labels - some might not understand what icons mean (especially those with cognitive/vision impairments)
- Coloured headings - could be mistaken for links
- Navigation with only arrows/dots (e.g. carousels) - use descriptive labels instead that tell users what content awaits them

**Guidelines:**
- Consider people with poor eyesight, low computer literacy, reduced dexterity and cognitive ability
- Meet WCAG 2.2 level AA requirements as minimum
- Keep an eye out for potential usability risks
- If anything is slightly vague, confusing or unclear - simplify it

## Have a Logical Reason for Every Design Detail

Every element must have a purpose that improves usability.

- Design using objective logic, rather than subjective opinion
- Be able to articulate the rationale behind each decision
- "That looks nice" or "I don't like it" are NOT logical or constructive feedback
- Focus on HOW it works and WHY it works that way

## Minimise Interaction Cost

Interaction cost = sum of physical and mental effort required to achieve a task.

**Actions that add to interaction cost:**
- Looking, scrolling, searching, reading
- Clicking, waiting, typing
- Thinking, remembering

### How to Minimise Interaction Cost

**1. Keep related actions close (Fitts's Law)**
- The closer and larger a target, the faster it is to click
- Keep actions close to the element they relate to
- Ensure sufficient target area: treat 24x24 CSS px as the WCAG 2.2 AA floor (subject to its five exceptions: spacing, equivalent, inline, user-agent, essential) and prefer 44-48 CSS px for frequently used touch controls

**2. Reduce distractions**
- Avoid animated banners, pop-ups, unnecessary visuals
- Remove attention-grabbing elements that pull focus from tasks

**3. Minimise choice (Hick's Law)**
- Time to make a decision increases with number and complexity of choices
- Reduce choices to speed up decisions
- Highlight recommended or popular items

## Minimise Cognitive Load

Cognitive load = amount of brain power required to use an interface.

**Quick ways to reduce cognitive load:**
- Remove unnecessary styles, information, and decisions
- Break up information into smaller groups
- Use conventional design patterns (Jakob's Law)
- Maintain consistency - similar elements look and work similarly
- Create clear visual hierarchy

### Replace Borders with Subtler Alternatives

Borders add visual noise. When separating elements, try less prominent alternatives first:

- **Background colours** — give input fields and section footers a subtle background colour instead of a border
- **Spacing** — replace divider lines between list rows with increased padding; the whitespace provides enough separation
- **Box shadows** — give elevated elements (modals, dropdowns, cards) a subtle shadow instead of a border; mimics real-world depth

**Keep borders when:** form fields need visible boundaries for accessibility (3:1 contrast), background colours aren't distinct enough, or you need to indicate interactive boundaries.

### Use Progressive Disclosure

Reveal information gradually as needed — show only what the current task requires. Use expandable sections for secondary details, and opt-in controls to reveal dependent inputs (e.g. a "Receive updates via text message" checkbox that reveals a required mobile-number field, instead of an always-present optional field).

### Don't Confuse Minimalism with Simplicity

Minimal interfaces can be vague — unlabelled navigation, overly subtle selected states, hidden actions, insufficient icon contrast. Simplify by removing what carries no meaning, never by hiding what users need. People don't use what they can't see: if there is space, keep important content and actions visible, and make hidden content discoverable (e.g. expose the edge of off-screen cards). Don't let aesthetics hinder usability or exclude people — trendy effects (glassmorphic, neumorphic) age poorly and often cause accessibility and hierarchy issues.

## Create a Design System

A system of predefined options and guidelines for efficient design decisions.

### Discover the Existing System First

Before adding or changing UI, inspect the project for existing decisions:

- Design tokens: colour, typography, spacing, radius, elevation, motion
- Shared components: buttons, inputs, dialogs, navigation, tables, empty states
- CSS architecture: cascade layers, utility conventions, component boundaries
- Interaction patterns: inline edit vs modal, explicit save vs autosave, toast vs
  inline feedback
- Comparable screens: how neighbouring product areas solve the same problem

When a design system exists, extend it deliberately. Do not create a local
one-off value when a token already exists. Do not rebuild a component that is
already available. If the system is missing a needed token or component, name
that gap and add the smallest reusable piece that fits the existing structure.

### Diagnose Design Drift by Root Cause

Before normalising an inconsistency, identify why the drift exists. Different
causes need different fixes:

| Drift cause | Typical symptom | Better fix |
|-------------|-----------------|------------|
| Missing token | The same semantic value is repeated with local numbers or colours | Add or extend the token, then use it everywhere that meaning appears |
| One-off component | A local button, card, form row, or empty state duplicates a shared pattern | Replace it with the shared component or extract the smallest reusable component |
| Pattern mismatch | The screen uses a different save, error, filter, navigation, or disclosure pattern from comparable screens | Align with the established product pattern unless the brief names a deliberate exception |
| Conceptual flow mismatch | The UI exposes a different mental model, sequence, or level of detail than the user expects | Rework information architecture or interaction model before adjusting styles |

Do not fix drift by repainting symptoms. A spacing patch will not solve a
missing component. A new component will not solve the wrong product flow. Name
the cause first, then change the smallest system-level decision that prevents
the same drift from reappearing.

### 1. Set Predefined Style Options

**Colour Options (Colour Palette):**
```
Brand       - Interactive elements (buttons, links)
Text strong - Headings, primary text
Text weak   - Secondary text
Stroke strong - Form borders, icons
Stroke weak - Decorative borders
Fill        - Secondary backgrounds
Background  - White or near-white
```

**Typography Options:** See [Typography](typography.md) for the type scale (1.200 Minor Third, base 16px).

**Spacing Options:** See [Layout and Spacing](layout-spacing.md) for the 8pt grid (XS–XXL).

**Shadow Options:** See [Colour](colour.md) for the two shadow levels (Raised, Overlay).

**Border Radius Options:**
- Small: 8pt
- Medium: 16pt
- Large: 32pt

**Icon Options:**
- Use SVG icons exclusively — never emoji, bitmap icons, or icon fonts
- Pick one icon set and use it consistently (e.g. Lucide, Heroicons, Phosphor)
- Default size: `1.5rem` (24px) for UI icons, `1rem` (16px) for inline icons
- Use `currentColor` so icons inherit the parent's text colour
- Match stroke width to the surrounding font weight (2px stroke ≈ regular weight, 2.5px ≈ bold)

```html
<!-- Decorative icon (label provides meaning) -->
<button>
  <svg aria-hidden="true" width="24" height="24" viewBox="0 0 24 24"
       fill="none" stroke="currentColor" stroke-width="2">
    <path d="..."/>
  </svg>
  Save post
</button>

<!-- Standalone icon (icon IS the label) -->
<button aria-label="Close dialog">
  <svg aria-hidden="true" width="24" height="24" viewBox="0 0 24 24"
       fill="none" stroke="currentColor" stroke-width="2">
    <path d="..."/>
  </svg>
</button>
```

**Icon accessibility rules:**
- Icons next to text: add `aria-hidden="true"` to the SVG (the text is the label)
- Icon-only buttons: add `aria-label` to the button (not to the SVG)
- Never use icons without a visible text label unless space is extremely limited — always prefer icon + text over icon alone

### 2. Create Reusable Modules

- Start with smallest components (buttons, avatars, form inputs)
- Combine small components to create larger ones
- Arrange components in specific layouts for reusable page templates
- Create a component library / UI kit

### Extract Patterns Deliberately

Extract a pattern when it appears three or more times with the same intent, or
when a shared token/component would prevent immediate drift.

Good extraction candidates:

- Repeated component structures: cards, rows, toolbars, empty states, form
  groups.
- Repeated semantic values: colour roles, spacing, elevation, radius, type styles,
  motion timing.
- Repeated interaction patterns: inline edit, confirmation/undo, filter bars,
  status messages.

Do not extract one-off UI just because it looks similar. Two elements that look
alike but serve different mental models may need separate implementations. Keep
the component API as specific as the product concept allows; components that are
too generic become hard to use correctly.

### 3. Define Usage Guidelines

- How to use components and visual styles
- How to write clear interface text
- Examples of useful interface conventions:
  - Indicate interactive elements using brand colour
  - Use sentence case
  - Left align buttons and text
  - Avoid disabled buttons
  - Front-load text
  - Be concise, use plain language

## Ensure an Interface is Accessible

Design interfaces that can be used by everyone, regardless of disability.

**Consider:**
- Blindness, low vision, colour blindness
- Motor impairment
- Mental disabilities

**Key principles:**
- Provide comparable experience for all
- Meet WCAG 2.2 level AA as minimum
- Include people with disabilities in usability testing

### Use Semantic HTML

Use meaningful HTML elements instead of generic `<div>` everywhere:

```html
<!-- Don't: ambiguous structure -->
<div>
  <div>Logo + Nav</div>
  <div>
    <div>Main content</div>
    <div>Sidebar</div>
  </div>
  <div>Footer</div>
</div>

<!-- Do: clear structure -->
<header>Logo + Nav</header>
<nav>Navigation</nav>
<main>
  <section>Main content</section>
  <aside>Sidebar</aside>
</main>
<footer>Footer</footer>
```

**Why it matters:**
- Screen readers use semantic elements to navigate (jump to `<nav>`, skip to `<main>`)
- Improves SEO and machine readability
- Makes code self-documenting

**Key elements:** `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<aside>`, `<footer>`, `<figure>`, `<figcaption>`, `<search>`

The `<search>` element (Baseline 2023) wraps any search or filtering interface — not just site search, but also filter controls on a results page:

```html
<search>
  <form action="/search">
    <label for="q">Search</label>
    <input id="q" type="search" name="q">
    <button type="submit">Search</button>
  </form>
</search>
```

It provides a semantic landmark that screen readers expose as a "search" role, letting users jump directly to it.

### Provide Skip Links

Skip links let keyboard users bypass repeated navigation and jump directly to the main content. They are the most common way to satisfy WCAG 2.4.1 Bypass Blocks (Level A), which requires some mechanism to skip repeated blocks (landmarks or a heading structure can also satisfy it).

```html
<body>
  <a href="#main-content" class="skip-link">Skip to main content</a>
  <header><!-- navigation --></header>
  <main id="main-content" tabindex="-1">
    <!-- page content -->
  </main>
</body>
```

The `tabindex="-1"` on the target element ensures browsers move focus there when the skip link is activated. Without it, some browsers scroll to the element but leave focus on the link.

```css
.skip-link {
  position: absolute;
  transform: translateY(-100%);
  transition: transform 0.2s ease-out;
  z-index: 9999;
  background: var(--bg, #fff);
  padding: 8px 16px;
}

.skip-link:focus-visible {
  transform: translateY(0);
}
```

**Guidelines:**
- Make the skip link the first focusable element on the page
- Hide it visually but keep it accessible (no `display: none`)
- Reveal it on focus so sighted keyboard users can see it
- Point to the `<main>` element (or equivalent primary content container)

### Assistive Technology

**Screen Readers:**
- Software that describes interface using speech or braille
- Users use keyboard to step through elements
- Mobile users swipe or drag finger across screen

**Screen Magnifiers:**
- Enlarges part of interface for people with low vision
- Users have limited view - can only see small part at a time
- Important: Keep this in mind when designing

### Good Accessibility Benefits Everyone

- Anyone could get temporary disability (eye/arm injury)
- Situational disabilities (bright sunny day affecting screen visibility)
- Good accessibility = great usability

### Never Disable Zoom

Setting `user-scalable=no` or `maximum-scale=1` on the viewport meta tag prevents users from zooming in. This violates WCAG Success Criterion 1.4.4 (Resize Text, Level AA) and makes the interface unusable for people with low vision.

```html
<!-- Never do this -->
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">

<!-- Correct -->
<meta name="viewport" content="width=device-width, initial-scale=1">
```

**If zoom is disabled to prevent double-tap-to-zoom delay on mobile:** Use `touch-action: manipulation` on interactive elements instead. This disables double-tap zoom on those elements while keeping pinch-to-zoom available everywhere:

```css
button, a, input, select, textarea {
  touch-action: manipulation;
}
```

## Design for Affordance

Affordance is an object's ability to convey its function through its appearance. A raised button suggests pressing; a handle suggests pulling; text that flows off the edge suggests scrolling.

**In digital design:**
- Buttons should look tappable (depth, fill colour, hover states)
- Scrollable areas should show partial content at the edges to hint at more
- Draggable items should have grab handles or visual weight
- Input fields should look like containers that accept text

**The risk of flat design:** Removing all depth cues can make interfaces ambiguous. Ensure interactive elements are still distinguishable from static content through colour, weight, or shape.

## Use Common Design Patterns (Jakob's Law)

Stick with conventional design patterns that people are already familiar with.

- Building on existing mental models means less learning time
- Reduces usability issues, cognitive load, and interaction cost
- Example: Accordion components for expandable content

**Play it safe:**
- Use conventional form field styles
- Save time on usability testing
- Focus creativity on unique selling points

## Use the 80/20 Rule (Pareto Principle)

Roughly 80% of effects come from 20% of causes.

**In product design:**
- ~80% of users use 20% of features
- ~80% of complaints come from 20% of issues
- ~80% of attention is spent on 20% of a page

**Application:**
- Prioritise the small number of things with largest impact
- Optimise for tasks most people will be doing
- Don't over-invest in edge cases

## Keep Costs in Mind

Every minute spent costs money.

**Ways to improve efficiency:**
- Use existing design systems, templates, icon sets
- Outsource time-intensive tasks
- Stick with familiar UI patterns
- Learn technical constraints of implementation
- Talk to developers early and often
- Simple approach is usually cheaper and easier

## Be Consistent

Similar elements look and work in a similar way.

### Within Your Product
- Create design system with guidelines for components, templates, visual styles, language
- Predictable functionality improves usability and reduces errors

### With Other Products
- Maintain consistency with well-established products
- Follow platform guidelines (iOS, Android) unless they test poorly
- Follow well-established, accessible UI patterns

**Conventional patterns:**
- Text links are underlined
- Checkboxes are small squares with tick icon
- Input fields are rectangles with label on top

## Clearly Indicate Interaction States

Interactive elements must change appearance when interacted with.

An interactive component is not complete until all relevant states are designed
and implemented. State completeness matters most for shared components because
every missing state repeats across the product.

**8 Interaction States Checklist:**

| State | When | Design Treatment |
|-------|------|------------------|
| **Default** | At rest | Base styling |
| **Hover** | Pointer over (not touch) | Subtle lift, colour shift |
| **Focus** | Keyboard/programmatic focus | Visible focus ring |
| **Active/Press** | Being clicked/tapped | Pressed in, darker |
| **Disabled** | Not interactive | Reduced opacity, no pointer |
| **Loading** | Processing | Busy indicator, status text |
| **Error** | Invalid state | Red border, icon, message |
| **Success** | Completed | Green check, confirmation |

**Common miss:** Designing hover without focus. Keyboard users never see hover states - they need visible focus indicators.

### Focus Rings with :focus-visible

Never remove focus indicators without replacement - it's an accessibility violation.

```css
/* Show focus ring only for keyboard navigation (:focus-visible is Baseline Widely available) */
:focus-visible {
  outline: 2px solid var(--brand);
  outline-offset: 2px;
}
```

Browsers that support `:focus-visible` automatically suppress focus rings on mouse/touch clicks. No need for a separate `:focus { outline: none }` rule.

**Focus ring requirements:**
- High contrast (3:1 minimum against adjacent colours)
- 2-3px thick
- Offset from element (not inside it)
- Consistent across all interactive elements

### Keep Focus Visible and Unobscured

WCAG 2.2 adds explicit focus visibility expectations. When keyboard focus moves
to an element, sticky headers, bottom bars, drawers, popovers, or floating
toolbars must not fully cover it.

Use `scroll-margin-*` on headings, form fields, and interactive targets that can
receive focus via skip links, validation jumps, deep links, or route changes:

```css
:target,
:focus {
  scroll-margin-block-start: var(--sticky-header-offset, 80px);
  scroll-margin-block-end: var(--sticky-footer-offset, 64px);
}
```

If a component opens an overlay, focus must move into it and return to the
trigger when it closes. If a component scrolls to an error, move focus to the
first actionable error field, not only to a summary message.

### Provide Alternatives for Dragging

Any critical action that can be performed by dragging must also have a visible
single-pointer or keyboard alternative:

- Sortable rows: provide move up/down controls or a reorder menu.
- Sliders: provide an input field or stepper when exact values matter.
- Swipe actions: provide a visible button, menu item, or inline action.
- Canvas interactions: provide a panel, list, or keyboard commands for the same
  operation.

Drag can be a convenience, but it must not be the only path to complete the
task.

### Keyboard Navigation in Composite Widgets

Composite widgets — tab bars, toolbars, menu bars, listboxes, tree views — should act as a single Tab stop. Users press Tab to reach the widget, then use arrow keys to move between items within it. This is the roving tabindex pattern defined in the WAI-ARIA Authoring Practices Guide (APG).

**The pattern:**
1. The focused item gets `tabindex="0"`, all other items get `tabindex="-1"`
2. Arrow keys move focus and update `tabindex` values
3. Tab moves focus out of the widget entirely

```html
<div role="tablist">
  <button role="tab" tabindex="0" aria-selected="true">Tab 1</button>
  <button role="tab" tabindex="-1">Tab 2</button>
  <button role="tab" tabindex="-1">Tab 3</button>
</div>
```

```javascript
tablist.addEventListener('keydown', (e) => {
  const tabs = [...tablist.querySelectorAll('[role="tab"]')];
  const current = tabs.indexOf(document.activeElement);
  let next;

  if (e.key === 'ArrowRight') next = (current + 1) % tabs.length;
  else if (e.key === 'ArrowLeft') next = (current - 1 + tabs.length) % tabs.length;
  else return;

  tabs[current].tabIndex = -1;
  tabs[next].tabIndex = 0;
  tabs[next].focus();
});
```

**When to use roving tabindex:**
- Tab bars, toolbars, menu bars (horizontal: Left/Right arrows)
- Listboxes, tree views (vertical: Up/Down arrows)
- Grids and data tables (all four arrow keys)

**When NOT needed:**
- A simple list of links or buttons — each is an independent Tab stop
- Form fields in sequence — standard Tab order is correct

## Animation and Motion

Animation adds context that static interfaces can't provide. It offloads spatial reasoning to the brain's visual cortex, reducing cognitive load and increasing perceived speed. But animation is a powerful tool that must be used purposefully — decorative animation wears on users after the fiftieth viewing.

**The test for good animation:** If users notice your animation, it may be doing too much. Good microinteraction animations are seamless — users don't consciously register them, they just feel the interface is responsive and clear.

### Animation Patterns

Use these categories to identify and communicate the purpose of an animation:

| Pattern | Purpose | Example |
|---------|---------|---------|
| **Transition** | Move users between places/tasks in the information space | Page-to-page slide, tab switching |
| **Supplement** | Bring info on/off page without changing location or task | Tooltip appearing, dropdown opening |
| **Feedback** | Connect user action to interface reaction | Button press ripple, form validation |
| **Demonstration** | Show how something works instead of telling | Onboarding walkthrough, feature tour |
| **Decoration** | Purely aesthetic, no new information | Background particle effects |

**Prioritisation:** Transitions and feedback provide the most cognitive benefit. Decorations provide the least and risk annoying users. When resources are limited, prioritise animations that answer "What just happened?" for the user.

### Product Motion Discipline

In product UI, motion serves the task. Use it for:

- State change: a panel opens, a row moves, a filter applies.
- Feedback: a button acknowledges press, validation appears, a save completes.
- Progress: a background operation is running or finishing.
- Spatial continuity: users understand where an object went.

Keep product transitions short, usually 150-250ms. Avoid orchestrated page-load
sequences, decorative loops, bounce, elastic easing, and motion that delays
work. The interface should feel responsive, not performed.

Brand and campaign surfaces can use more expressive motion when motion carries
the story. Product surfaces need restraint because users repeat the same actions
many times.

### CSS Keyframe Motion Discipline

CSS keyframes are best for simple, local motion: a one-element entrance, a
finite shimmer, a mask reveal, a subtle glow, or a background motif. Use a
timeline library or View Transitions when the motion coordinates multiple
elements, depends on gestures, or needs interruption control.

Rules:

- Prefer finite durations and iteration counts. Avoid infinite loops in product
  UI unless the animation communicates ongoing progress and respects reduced
  motion.
- Use `animation-fill-mode: both` when an element must hold its before/after
  state.
- Do not make critical state depend on hover-triggered animations, delayed class
  toggles, or wall-clock JavaScript.
- List animated properties explicitly. Never use `transition: all`.
- Keep render-critical motion deterministic: the element should have a valid
  default state even if animation does not run.

**Questions to justify an animation:**
- Does it show the user where information came from or went to?
- Does it indicate progress?
- Does it move the user through an information space?
- Does it explain something faster than words could?

### The Cone of Vision

The eye is most sensitive to colour and detail at the centre (foveal region). Peripheral vision is blurry but highly sensitive to motion.

**Practical implications:**
- **Centre of vision:** Colour fades and small movements are sufficient to draw attention
- **Peripheral vision:** Use motion to attract attention — colour changes alone may go unnoticed
- Two independently moving objects on opposite sides of the screen cannot both be tracked
- Overusing motion causes "banner blindness" — the brain learns to ignore excessive animacy

### Easing (Timing Functions)

Easing describes the rate of change over time. Different easings suit different situations:

| Easing | CSS | Best For |
|--------|-----|----------|
| **Ease-out** (deceleration) | `ease-out` | User-initiated actions (clicks, taps). Feels snappy and responsive |
| **Ease-in** (acceleration) | `ease-in` | System-initiated animations (alerts, pop-ups). Starts slowly, less startling |
| **Ease-in-out** | `ease-in-out` | Moving elements toward each other |
| **Linear** | `linear` | Fades and colour changes only. Motion with linear easing looks mechanical |

For unique brand feel, use custom `cubic-bezier()` curves. Keep a chart of your project's easings to maintain consistency.

### Duration (Timing Scale)

Use a predefined set of durations for consistency, similar to a typographic scale:

```
Immediate:  100ms     — Fades, colour changes under cursor/finger
Fast:       150–250ms — Button presses, toggles, responsive interactions
Slower:     400ms     — Elements moving on page, dropdowns, tooltips
Deliberate: 700ms     — Large movements across screen, demonstrations
```

Keep interaction feedback inside the 150–250ms band (consistent with the Product Motion Discipline section above); reserve the longer steps for spatial movement.

**Guidelines:**
- Colour/opacity changes under the cursor feel slow above 100ms
- Moving elements across the page needs 300ms+ to track
- Centre-of-vision animations need shorter durations (70-200ms)
- Peripheral animations benefit from longer durations (300-700ms)
- When in doubt, halve your duration — developers consistently overestimate how long animations should run

### Spring Easing with linear()

The `linear()` easing function (Baseline 2023) accepts a list of output values that the browser interpolates between, enabling easing curves that `cubic-bezier()` cannot express — including spring physics.

Spring-based motion feels more natural than cubic-bezier because it models physical deceleration. Apple (iOS 17+), Framer Motion, and the animations.dev community have converged on two parameters: **duration** and **bounce** (0 = critically damped, no overshoot; positive = elastic overshoot).

**Default to critically damped springs (bounce = 0)** — they feel responsive without being playful. Reserve bouncy springs for confirmations, celebrations, or deliberately playful interfaces.

```css
:root {
  /* Critically damped spring — natural deceleration, no overshoot */
  --ease-spring: linear(
    0, 0.009, 0.035, 0.078, 0.136, 0.206, 0.286, 0.373,
    0.464, 0.557, 0.65, 0.738, 0.819, 0.891, 0.951,
    0.998, 1.029, 1.047, 1.051, 1.044, 1.029, 1.01,
    0.99, 0.974, 0.965, 0.961, 0.963, 0.969, 0.978,
    0.988, 0.997, 1.003, 1.005, 1.003, 1
  );

  /* Gentle bounce — for playful/confirming interactions */
  --ease-spring-bouncy: linear(
    0, 0.004, 0.016, 0.035, 0.063, 0.098, 0.141, 0.191,
    0.25, 0.316, 0.391, 0.474, 0.566, 0.666, 0.775,
    0.893, 1.02, 1.086, 1.125, 1.139, 1.131, 1.106,
    1.067, 1.019, 0.968, 0.921, 0.882, 0.855, 0.843,
    0.849, 0.871, 0.905, 0.946, 0.989, 1.027, 1.054,
    1.067, 1.063, 1.044, 1.015, 0.983, 0.956, 0.94,
    0.939, 0.953, 0.977, 1.005, 1.026, 1.035, 1.029,
    1.012, 0.993, 0.98, 0.977, 0.984, 0.997, 1.009,
    1.014, 1.009, 0.999, 0.992, 0.99, 0.994, 1.001, 1
  );
}
```

Generate these values from spring parameters using tools like [linear-easing-generator](https://linear-easing-generator.netlify.app/).

**When CSS springs are enough:**
- Hover effects, button presses, entry/exit transitions, layout shifts

**When a JS animation library is needed (Framer Motion, React Spring, Motion One):**
- Gesture-driven animation (drag, swipe, pinch) — the animation must respond to ongoing input
- Interruptible animations — a new trigger mid-animation must redirect smoothly, not restart
- Complex orchestrated sequences with stagger, layout animations, or shared element transitions

### Only Animate Transform and Opacity

For smooth 60fps animations, only animate `transform` and `opacity`. Other properties (width, height, margin, padding) trigger expensive layout recalculations.

```css
/* Good - GPU accelerated */
.card:hover {
  transform: translateY(-2px);
  opacity: 0.9;
}

/* Avoid - triggers layout */
.card:hover {
  margin-top: -2px;
  height: 102%;
}
```

A consistent frame rate matters more than a high one — a steady 30fps looks smoother than 60fps with dips.

### Animate Height with grid-template-rows

The one exception to "only animate transform and opacity": `grid-template-rows` can animate between `0fr` and `1fr`, enabling smooth accordion-style height transitions without JavaScript height calculations (animating grid tracks is Baseline Widely available, so it needs no feature gate):

```css
.collapsible {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows 300ms ease-out;
}

.collapsible.is-open {
  grid-template-rows: 1fr;
}

.collapsible__inner {
  overflow: hidden;
  min-height: 0;
}
```

```html
<div class="collapsible">
  <div class="collapsible__inner">
    Content that collapses smoothly
  </div>
</div>
```

**Accessibility caveat:** When collapsed (`0fr`), the content is visually hidden but still in the accessibility tree. Add `visibility: hidden` to the inner element when collapsed so screen readers skip it, and transition visibility alongside:

```css
.collapsible__inner {
  overflow: hidden;
  min-height: 0;
  visibility: hidden;
  transition: visibility 300ms;
}

.collapsible.is-open .collapsible__inner {
  visibility: visible;
}
```

**Future alternative:** `interpolate-size: allow-keywords` (Chrome 129+) allows direct `height: 0` to `height: auto` transitions — but it is Baseline Limited availability, so keep the grid technique as the default until support widens.

### Every Entrance Needs an Exit

When something animates onto the screen, it must also animate as it leaves. Alerts that beautifully slide in but instantly vanish on dismissal make the interface feel unfinished. Invest in a system that waits for exit animations to complete before removing elements.

**Exit animations should be faster than entrances.** Users have already processed the element — the exit just needs to confirm it's gone. Use 75-85% of the entrance duration for the exit:

| | Entrance | Exit |
|---|---|---|
| **Duration** | 300ms | 225-250ms |
| **Easing** | `ease-out` (decelerate in) | `ease-in` (accelerate out) |
| **Perception** | "Here I am" — arrives confidently | "Done" — leaves quickly |

The asymmetry is subtle but noticeable. Symmetric enter/exit feels sluggish because the exit draws too much attention to something the user already dismissed.

### Use @starting-style for Entry Animations

`@starting-style` (Baseline 2024) defines the initial state for CSS transitions when an element first appears — enabling entry animations without JavaScript. Previously, animating an element "from hidden to visible" required JS to add a class after insertion.

```css
dialog[open] {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 300ms ease-out, transform 300ms ease-out;

  @starting-style {
    opacity: 0;
    transform: translateY(-8px);
  }
}
```

This is particularly useful for elements that toggle visibility: dialogs, popovers, tooltips, and notification toasts. Combine with `allow-discrete` to also transition `display: none`:

```css
.tooltip {
  transition: opacity 200ms ease-out, display 200ms allow-discrete;
  opacity: 1;

  @starting-style { opacity: 0; }
}
.tooltip[hidden] {
  opacity: 0;
  display: none;
}
```

### Use the Popover API for Non-Modal Tooltips, Dropdowns, and Menus

The Popover API provides native behaviour for non-modal floating UI elements — no JavaScript libraries needed for the basics:

```html
<button popovertarget="actions-menu">Actions</button>
<div id="actions-menu" popover>
  <ul>
    <li><button>Edit</button></li>
    <li><button>Duplicate</button></li>
    <li><button>Delete</button></li>
  </ul>
</div>
```

**What the browser handles automatically:**
- Renders in the **top layer** (no z-index wars)
- **Dismisses on outside click** or Escape key

**What you must still handle:**
- Initial focus placement and focus trapping when the interaction requires them (`auto`/`hint` popovers restore focus on hide when focus is inside; `manual` popovers never restore focus automatically)
- Scroll locking or making background content inert; popovers leave the page interactive

**When to use popover:**
- Dropdown menus and action menus
- Non-modal information panels
- Notification toasts (combine with `popover="manual"` for persistent display)

**When to use `<dialog>` instead:**
- Modal dialogs that require focus trapping and background inertness
- Confirmation prompts and form overlays that require user action before continuing

Combine with `@starting-style` for animated entry/exit — the Popover API and `@starting-style` were designed to work together.

### Use the `inert` Attribute for Non-Modal Content

The `inert` attribute (Baseline 2023) makes an element and all its descendants non-interactive and invisible to assistive technology. It is the correct way to trap focus inside a custom overlay, off-canvas drawer, or wizard step.

```html
<nav class="drawer" id="drawer">
  <!-- Drawer content -->
</nav>
<main id="main-content" inert>
  <!-- Main content is unreachable while drawer is open -->
</main>
```

**When `inert` is set:**
- Click/tap events are ignored
- The element is removed from the tab order
- Screen readers skip the entire subtree
- `find-in-page` does not match text inside `inert` content

**You do NOT need `inert` when using:**
- `<dialog>.showModal()` — the browser automatically makes everything outside the dialog inert

Popover API surfaces remain non-modal: automatic popovers provide light dismissal,
but do not manage focus or make the page inert.

**Use `inert` when:**
- Building a custom drawer/sidebar that overlays the page
- Implementing a step-by-step wizard where only the current step should be interactive
- Creating a custom modal without `<dialog>` (though `<dialog>` is preferred)

Style inert regions to reinforce their inactive state:

```css
[inert] {
  opacity: 0.5;
  pointer-events: none;
}
```

### Avoid Flashes of Unloaded States (FOULS)

When loading content dynamically, ensure users never see empty/unloaded pages:

1. Start in a real component loading state or local status region.
2. Preserve stable component boundaries so loading feedback does not shift the
   page.
3. Transition loaded content in smoothly when the transition clarifies what
   changed.
4. Never show an unexplained blank area. If content is unavailable, say what is
   loading or what action can recover.

### Signal Oncoming Animations

Anticipatory animation helps users mentally prepare. For example, hovering over a collapsible sidebar can cause it to slightly shift in the direction it will expand if clicked.

### Respect Reduced Motion Preferences

Vestibular disorders affect ~35% of adults over 40. Seizure-triggering animations can be dangerous — never flash elements more than twice per second.

**Static-first is the standard approach:** author the non-animated state as the default, and gate all motion inside `@media (prefers-reduced-motion: no-preference)` (see [motion and interaction](motion-interaction.md) and [Motion route](route-motion.md)). Motion then never reaches users who opted out, and there is nothing to undo.

**Retrofit fallback only:** when adding reduced-motion support to an existing codebase where motion was not gated, a global kill-switch limits the damage until the animations are migrated:

```css
/* Retrofit safety net for ungated legacy animations */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation: none;
    transition: none;
  }
}
```

No `!important` — this allows more specific selectors (dialogs, view transitions, popovers) to override with safe opacity fades. WCAG 2.3.3 explicitly excludes opacity changes from "motion animation", so fades do not trigger vestibular disorders.

Replace motion-based animations with fades where a visual signal is still needed:

```css
@media (prefers-reduced-motion: reduce) {
  .toast[data-state="open"] {
    animation: fade-in 150ms ease-out;
  }
}

@keyframes fade-in {
  from { opacity: 0; }
}
```

### View Transitions API

The View Transition API provides native browser support for animated transitions between UI states — both within a single page (SPA) and across page navigations (MPA). It answers the question "what just happened?" by showing spatial relationships between states, reducing cognitive load.

**Browser support:** Same-document transitions are Baseline 2025 (Chrome 111+, Safari 18+, Firefox 144+). Cross-document (MPA) transitions have no Firefox support — use as progressive enhancement only.

#### Same-Document Transitions (SPA)

Wrap DOM updates in `document.startViewTransition()`:

```javascript
function navigate(item) {
  if (!document.startViewTransition) {
    updateDOM(item);
    return;
  }

  document.startViewTransition(() => updateDOM(item));
}
```

The browser snapshots the old state, runs the callback, then cross-fades between the old snapshot and a live projection of the new DOM over 250ms by default. The old state is static and the new projection can keep media playing, but a document-scoped transition overlay sits above the page and can prevent normal pointer interaction until the transition finishes.

#### Cross-Document Transitions (MPA)

Opt in with CSS on both pages — no JavaScript needed:

```css
@view-transition {
  navigation: auto;
}
```

Both pages must be on the same origin and both must opt in. Navigations taking longer than 4 seconds are automatically skipped.

#### Shared Element Transitions

Give matching elements the same `view-transition-name` on both pages (or both states). The browser automatically morphs position, size, and content between them:

```css
/* List page */
.product-thumbnail { view-transition-name: product-image; }

/* Detail page */
.product-hero { view-transition-name: product-image; }
```

Each name must be unique across all rendered elements at the same time. Use `view-transition-name: match-element` (Baseline 2025) for lists where items reorder but don't change identity. Use `view-transition-class` to apply shared animation styles to groups of named elements.

#### Custom Animations

Override the default cross-fade by targeting the pseudo-elements:

```css
::view-transition-old(root) {
  animation: 300ms ease-in slide-out-left;
}
::view-transition-new(root) {
  animation: 300ms ease-out slide-in-right;
}
```

Use `:active-view-transition-type()` for directional animations (forward vs backward navigation).

#### When to Use View Transitions vs @starting-style

| | View Transitions | `@starting-style` |
|---|---|---|
| **Purpose** | Animate between two complete UI states | Animate an element's first appearance |
| **Scope** | Full page or named elements | Individual elements |
| **Trigger** | `startViewTransition()` or navigation | Element insertion, `display: none` → visible |
| **Best for** | Page transitions, list reordering, shared elements | Dialogs, popovers, tooltips, toasts |

#### Performance and Accessibility

- Keep transitions under 500ms and verify pointer, keyboard, focus, popover, and dialog behavior while the overlay exists; do not rely on choreography that blocks the next task
- Use `view-transition-name` sparingly — each named element creates a bitmap snapshot
- Profile automatically generated group animations when snapshot dimensions change; `width` and `height` interpolation can run on the main thread, so do not assume View Transitions are compositor-only
- Keep the returned `ViewTransition` when cleanup or custom playback matters; use its lifecycle promises and test rapid repeated input because starting another transition on the same root skips the active one
- Make critical destination content and shared images ready before an MPA transition where practical. An expected element being parsed does not prove its image has loaded; prefer bounded preload or prerender work, and use render blocking only with measured Core Web Vitals evidence
- Prefer a feature-detected element-scoped transition when only one component should pause or overlay and the rest of the page must remain interactive; retain a document-scoped or instant fallback for other engines

**Always respect `prefers-reduced-motion`.** For MPA transitions, only enable when motion is acceptable:

```css
@media (prefers-reduced-motion: no-preference) {
  @view-transition {
    navigation: auto;
  }
}
```

For SPA transitions, substitute a quick cross-fade instead of disabling entirely — fades do not trigger vestibular disorders:

```css
@media (prefers-reduced-motion: reduce) {
  ::view-transition-group(*) {
    animation: none;
  }
  ::view-transition-old(*) {
    animation: 150ms ease-out fade-out;
  }
  ::view-transition-new(*) {
    animation: 150ms ease-in fade-in;
  }
}
```
