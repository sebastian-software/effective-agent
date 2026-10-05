# Forms UX

Design forms around user recovery: clear labels, browser-supported input attributes, tolerant validation, meaningful error messages, and submission flows that preserve native behavior.

## Working Rules

- Reach for native `<form>`, `<label>`, `<input>`, `<select>`, `<textarea>`, `<button>`, `<fieldset>`, and `<legend>` before building custom equivalents.
- Choose `type`, `name`, `autocomplete`, `inputmode`, and `enterkeyhint` intentionally so the browser shows the right keyboard and autofill.
- Validate after useful interaction, not at first keystroke.
- Preserve paste, autofill, password managers, native validation, and submitter semantics unless there is a specific risk.
- Do not apply global `novalidate` or wrap fields in custom validation layers that hide input purpose, mobile keyboards, password managers, or autofill.
- Associate each error message with its field programmatically (for example `aria-describedby`) so assistive tech announces it.
- Keep submit available until a submission is in progress. Do not disable it
  because client-side state says the form is incomplete; submission is the
  reliable opportunity to expose validation and recovery.
- After a failed submission, preserve entered values and move focus to a labelled
  error summary when several fields fail. Link each summary item to its field,
  keep the inline error associated with that field, and explain how to recover.
- Pair custom widgets with precise keyboard, focus, error, and fallback behavior.

### Autocomplete and Autofill

- Set specific `autocomplete` tokens (`email`, `tel`, `street-address`, `cc-number`, `one-time-code`, etc.) so browsers and password managers can fill fields and preserve input-purpose identification for assistive tech.
- Never disable autocomplete globally. Turn it off (`autocomplete="off"`) only for values that must not be stored or reused, such as one-time codes, CVV/CVC, and per-transaction unique identifiers.

### Mobile Forms

- Match the on-screen keyboard to the field with `inputmode` and `type` (`type="email"`, `inputmode="numeric"` for codes, `type="tel"` for phone numbers).
- Keep mobile forms single-column and prefer a visible segmented control or radio set over a dropdown for small option counts to cut taps.
- Mark required and optional fields the same way on mobile as on desktop (see [Forms](forms.md)); a form that asks almost only for required information may mark just the few optional fields with "(optional)".
- Meet the 24x24 CSS px WCAG floor; prefer 44-48px touch targets where space and platform conventions allow.
- Detect coarse pointers with `pointer`/`hover` media queries rather than inferring touch from viewport width, and test hybrid devices that have both.

### Sliders and Range Inputs

- Reserve sliders for exploratory range or filter interaction, not precise data entry.
- Always pair a slider with a text or number input so users needing exact values or with limited motor control have a reliable path.
- Account for non-linear value distributions and make dual-handle (min/max) ranges visually unambiguous about which handle is which.

### Modern Form APIs

- Submit programmatically with `form.requestSubmit()` rather than `form.submit()` so constraint validation runs and a `submit` event fires.
- Read `event.submitter` on the `SubmitEvent` to know which button triggered submission instead of tracking focus or click state.
- Use the `formdata` event to inject or transform entries on the `FormData` without intercepting submission.
- Open native date/color/select pickers from a custom control with `HTMLInputElement.showPicker()`, gated on a user gesture.
- Disable an entire subtree from focus and interaction with the `inert` attribute (for example, the inactive step of a multi-step form) instead of toggling `disabled`/`tabindex` per element.

### Custom Controls

- Do not replace a native select, combobox, date picker, slider, or file input for visual styling alone.
- When a custom control is justified, test the mobile OS picker it replaces and verify the value parses back correctly on every target platform.
