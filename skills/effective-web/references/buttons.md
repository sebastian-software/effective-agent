# Buttons

Learn how to design descriptive and accessible buttons with a clear visual hierarchy.

## Implementation Contract

- Build a shared visual treatment against a real `<button>` first so form,
  keyboard, disabled, focus, and user-agent behavior are visible. Then verify a
  semantically appropriate link variant separately; shared appearance does not
  make the elements interchangeable.
- Keep visible labels as real text and decorative icon geometry out of the
  accessible name. Let variants override an intentional set of semantic custom
  properties rather than duplicate the whole rule set.
- Prototype hover and press behavior in the browser and verify contrast, focus,
  touch, reduced motion, and every theme. Do not retain speculative animation or
  state capability without an identified product or design-system use.

## Define 3 Button Weights

3 weights to indicate importance of actions:

### Primary Button
- Rectangle with rounded corners
- Solid fill of brand colour
- White text
- Most prominent
- Highlights most important action

### Secondary Button
- Unfilled rectangle with border and rounded corners
- Brand colour for text and border (consistency with interactive elements)
- Avoid solid fill of another colour (conflicts with primary)
- Avoid light grey fill/outline (looks disabled)

### Tertiary Button
- Transparent button
- Underlined text (like text link)
- Brand colour for text
- Underline ensures colour blind users know it's interactive

## Common Button Design Mistakes

### Mistake 1: Low contrast fill
Secondary button fill contrast < 3:1 is too low to clearly indicate button shape.

### Mistake 2: Grey secondary button
- Could be mistaken as disabled
- Text/border contrast < 4.5:1 / 3:1

### Mistake 3: Similar primary/secondary styles
- Conflicting visual hierarchy
- Colour blind can't differentiate
- Contrast between buttons < 3:1

### Mistake 4: Similar styles, different colours
- Primary/secondary conflict
- Secondary text contrast too low

### Mistake 5: Too similar contrast
- Buttons too similar for low vision users
- Contrast ratio between buttons < 3:1

### Mistake 6: Low contrast tertiary border
- Border must be 3:1 to identify as interactive

### Mistake 7: Colour-only tertiary indicator
- Colour blind can't distinguish from plain text
- Must have underline

### Mistake 8: Inconsistent button shapes
- If shapes differ, users assume different function
- Elements with same function should look same

### Mistake 9: Unclear hierarchy
- Primary and secondary have similar visual weight
- Secondary background < 3:1 contrast

## Button Design Guidelines

1. Clear visual hierarchy NOT dependent on colour alone
2. Button shape contrast: minimum 3:1
3. Button text contrast: minimum 4.5:1
4. If identical button styles, contrast between them: minimum 3:1
5. Target area: meet the WCAG 2.2 AA minimum of 24 x 24 CSS px (subject to its five exceptions: spacing, equivalent, inline, user-agent, essential), and prefer 44-48 CSS px for primary and touch controls

## Use a Single Primary Button for the Most Important Action

**Guidelines:**
- Primary button = most important action
- Helps people understand what to do next
- If no single most important action, use secondary/tertiary
- AVOID multiple primary buttons (compete for attention, cause confusion)

**Multiple primary buttons cause:**
- Interface clutter
- Confused visual hierarchy
- If everything is important, nothing stands out

## Use Secondary Buttons for Less Important Actions

**Use for:**
- Alternative to primary action
- Multiple actions with equal importance

**When actions have equal importance:**
- Use equal prominence (both secondary)
- Don't bias one over other

**Example:** "Report email as junk?" - Report / Don't report (both secondary)

## Use Tertiary Buttons for the Least Important Actions

**Best for:**
- Displaying multiple actions
- Destructive actions you want less prominent

**Benefits:**
- Low prominence
- Corrects visual hierarchy
- Makes primary action most prominent
- Helps avoid accidental destructive actions

## Try to Avoid Disabled Buttons

**Problems with disabled buttons:**
- Can cause people to get stuck (no feedback on WHY)
- Low contrast - hard for poor eyesight to see
- Not keyboard accessible - confuses keyboard users

### Alternative 1: Enable buttons and validate on submit
- Display error messages when submitted
- Instantly shows what was missed
- Simple, accessible solution

### Alternative 2: Remove unavailable actions
- Remove unavailable actions entirely
- Let people know WHY unavailable
- Reduces confusion, creates clear focus

### Alternative 3: Lock icon on unavailable actions
- Put lock icon on regular buttons
- Indicates unavailable/locked
- Ensures discoverability and sufficient contrast
- Works well for premium features
- Let people know how to get access

### If You Must Use Disabled Buttons
- Include message near button explaining why unavailable
- Add tooltip explaining why unavailable
- Make button keyboard accessible (allows focus for assistive technology)

## Left Align Buttons

Order buttons left to right, most important to least important.

**Reasons:**
- English read left to right, F-pattern
- Right-aligned buttons can be missed on large screens
- Screen magnifier users might miss right-aligned buttons
- Most important button should have lowest interaction cost

### Mobile Screens
- Stack buttons top to bottom
- Most important at top
- Make buttons full-width (both hands can reach)

### Small Dialog Boxes
Both left and right alignment can work if visual hierarchy is clear.

**Left alignment reasons:**
- Consistent with left-aligned form fields above
- Avoids confusion from mixed alignment

**Right alignment reasons:**
- Indicates direction/momentum (forward = right, back = left)
- Familiar dialog pattern on desktop platforms (both Windows and macOS place the commit-button group at the bottom right)

### Multi-Step Forms
**Problem with right-aligned primary button:**
- Back button in prominent left position = accidental clicks
- Primary button further from form fields = higher interaction cost
- Right-aligned buttons missed on large screens

**Solution:**
- Keep primary button left-aligned
- Put tertiary "Back" button at top left:
  - Common position (mobile, browsers, breadcrumbs)
  - Allows going back without scrolling
  - Less chance of accidental data loss

### Exception: Single Form Fields
For search/email subscription:
- Primary button on right of field saves space
- Connection reinforces relationship
- Ensures button isn't missed

## Ensure Button Text Describes the Action

Button text = meaningful when read out of context.

**Rule:** Verb (action) + Noun (thing)

**Examples:**
- "Save post"
- "Discard message"
- "Edit article"

**Why descriptive:**
- Prominent buttons viewed first
- Allows quick action without reading supporting text
- Screen reader users jump to buttons/links

**Bad:** "Ok", "Submit", "Yes"
**Good:** "Save post", "Update payment details", "Delete article"

## Ensure Buttons Have a Sufficient Target Size

Small targets = harder to click/touch (especially motor impairments or one-handed use).

**Guidelines:**
- Meet the WCAG 2.2 AA target size: at least 24 x 24 CSS px, or use sufficient spacing or an equivalent larger control for smaller inline targets
- Prefer 44-48 CSS px targets for common touch, coarse-pointer, and high-frequency controls
- Frequently used buttons: even larger

**Small interactive elements:**
- Extend target area beyond visual bounds
- Indicate target area to reduce interaction cost

## Balance Icon and Text Pairs

Ensure same visual prominence for cohesive look.

### Use Similar Weight
Match icon and text thickness - groups them together, creates balance.

### Use Similar Size
Match icon size to text size.

### Vary Contrast
If weight/size hard to match, use contrast for balance.
- Large/thick icons: use "Stroke strong" colour
- Text: use "Text weak" colour

## Add Friction to Destructive Actions

**Destructive action:** Causes harm or can't be undone.

**Friction:** Increases interaction cost to perform action.

**Apply increasing friction based on severity:**

### Initial Friction (Before action)
- Make action less prominent
- Move further away
- Progressively disclose
- DON'T use a red outline/border button (draws attention through colour but looks like a primary action)

### Styling Destructive Buttons Correctly

When a destructive button must be visible, use a filled background with muted tones - not a red outline:

```css
/* Don't: red outline/border draws attention wrong */
.delete-btn-bad {
  border: 1px solid red;
  color: red;
  background: white;
}

/* Do: muted filled background, same hue */
.delete-btn {
  background: hsl(0, 50%, 95%);  /* Light red - reduced saturation, high lightness */
  color: hsl(0, 91%, 38%);       /* Dark red text */
  border: none;
}
```

**The principle:** Keep the same hue (red) but reduce saturation and increase lightness for the background. This makes the button clearly destructive without competing with the primary action.

### Light Friction (Less serious)
Simple confirmation message.
"Delete message? Are you sure you want to delete this message?"

### Moderate Friction
Highlight confirmation in red to warn of destructive action.
"Delete article? You won't be able to recover it."

### Heavy Friction (Very destructive)
Red + checkbox that must be selected before action can occur.
"Delete account? [checkbox] I confirm I want to delete my account"

### Prefer Undo Over Confirmation Dialogs

UX research shows confirmation dialogs are ineffective - users click through them automatically without reading. Undo is almost always better.

Make undo the default for reversible destructive actions. It keeps users in
flow, makes the result visible immediately, and gives them a real recovery path
instead of asking them to predict whether they made a mistake.

**Undo pattern:**
1. Execute action immediately
2. Show toast: "Email deleted. [Undo]"
3. Actually delete after the toast expires; give an Undo toast substantially longer than an informational one and a persistent alternative (see [Dialog and Modal](dialog-modal.md))

**Benefits:**
- Doesn't interrupt workflow
- Users don't have to think before acting
- Mistakes are easily recoverable
- Feels faster and more responsive

**Use confirmation dialogs ONLY for:**
- Truly irreversible actions (account deletion)
- High-cost actions (payments)
- Batch operations affecting many items

For anything else, first ask whether the system can delay the final operation,
soft-delete, archive, or retain a short recovery window. A reversible operation
with undo is usually safer than a modal confirmation that users dismiss from
muscle memory.

**Example - Gmail style:**
```
"Message deleted. [Undo]"  ← Toast with undo option
```

Even with friction, mistakes happen. Undo removes a lot of risk while maintaining flow.

## Chapter Summary

1. Define 3 button weights with clear visual hierarchy not dependent on colour alone
2. Avoid disabled buttons - enable and validate on submit instead
3. Order buttons left to right, most important to least important
4. Button text: verb + noun, meaningful out of context
5. Meet the WCAG 2.2 AA target size (24 x 24 CSS px minimum); prefer 44-48 CSS px targets with 8px+ separation for comfortable touch use
