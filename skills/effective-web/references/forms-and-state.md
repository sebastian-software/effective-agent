# Forms and State

State decisions determine whether a component is reusable or a source of bugs.
Decide who owns each piece of state, keep the browser's native form behavior
intact, and never let a re-render or an async transition silently discard what
the user typed.

## Working Rules

### State ownership

- Classify every value before implementing: server state (cache it with a query
  library, do not mirror it into `useState`), URL state (search params, for
  shareable/back-button state), form state (owned by the form layer), local UI
  state (`useState`/`useReducer`), and derived state (computed, never stored).
- Lift state only as high as the lowest common ancestor that needs it. Pushing
  state to the top "just in case" forces wide re-renders and couples unrelated
  components.
- Reach for `useReducer` over multiple `useState` calls when updates are
  interdependent (a wizard step plus its validation plus its dirty flag), so
  transitions are atomic and testable.

### Derived vs stored state

- Compute during render whatever can be computed from props or existing state
  (filtered lists, totals, `isValid`, formatted labels). Storing derived values
  in state guarantees they drift out of sync.
- Do not use an effect to "sync" one state value to another. Either compute it
  inline, or — if it is genuinely expensive — wrap it in `useMemo`. An effect for
  derivation runs after paint and causes a second render with stale UI in
  between.
- When state must reset on a prop change, prefer remounting via a `key` prop over
  an effect that clears state; the `key` change is synchronous and intent is
  obvious.

### Controlled, uncontrolled, and native inputs

- Default to uncontrolled inputs with `defaultValue`/`defaultChecked` for simple
  forms; let the DOM hold the value and read it on submit. Controlled inputs are
  for when render must react to every keystroke (live validation, formatting,
  dependent fields).
- An input is controlled or uncontrolled for its lifetime. Never pass
  `value={x}` where `x` can become `undefined`; use `value={x ?? ''}` to keep it
  controlled.
- Keep native semantics even behind a custom widget: render a real labeled
  `<input>`/`<select>`, preserve `name`, the correct `type`, `autocomplete`,
  `inputMode`, `required`, and `disabled`, and let the browser participate in
  autofill, validation, and password-manager flows. A custom dropdown that drops
  `name` and `autocomplete` breaks autofill and form submission.
- Associate every control with a `<label>` (wrapping or `htmlFor`/`id`); do not
  substitute `placeholder` for a label.

### Form library integration

- Treat the form library (React Hook Form, TanStack Form) as the owner of field
  state and submission. Expose reusable inputs that accept the field's
  `value`/`onChange`/`onBlur`/`name`/`ref` (or integrate via a controller) rather
  than holding their own competing copy.
- Forward the field `ref` to the real DOM input so the library can focus the
  first invalid field on a failed submit and report uncontrolled values.
- Validate with a schema (Zod) resolved by the form library so a single source
  defines types and validation; for when to validate, follow the
  validation-timing rules in [Forms UX](forms-ux.md).
- Drive conditional fields from watched values, and unregister/unmount fields
  that no longer apply (or exclude them from the schema branch) so hidden fields
  do not submit stale data or block validation. Keep what the user sees, what is
  registered, and what the schema expects in agreement.
- Set `defaultValues` for every field up front (including empty strings/`false`)
  so fields start controlled and `reset()` returns to a known state; reset from
  fetched data once it loads rather than seeding state in an effect on each
  render.

### Async, submission, and recovery

- Model submission state explicitly (`idle | submitting | error | success`) and
  while `submitting` mark the submit control `aria-disabled="true"` and
  `aria-busy="true"`, show progress, and ignore further submits in the handler,
  so a double-click cannot fire two requests while the button keeps focus. The
  server still has to tolerate a duplicate submit.
- Never clear user input on error. On a failed submit keep all entered values,
  surface field-level and form-level messages, and move focus to the first error
  or the summary so keyboard and screen-reader users find it.
- For optimistic updates (`useOptimistic` or manual), keep the pre-update value
  and roll back on failure with a visible message. Optimistic UI without a
  rollback path corrupts what the user sees.
- Use transitions (`useTransition`/`startTransition`) for non-urgent updates like
  filtering a large list so typing stays responsive and a pending flag is
  available for UI.

### Effects discipline

- Use `useEffect` only to synchronize with something outside React:
  subscriptions, timers, manual DOM, network when not handled by a data library.
  Do not use it for derivation or for logic that belongs in an event handler.
- Make every effect cleanly cancellable: abort fetches with `AbortController`,
  clear timers, and unsubscribe in the cleanup function, so unmount and
  dependency changes do not leak or set state on a gone component.
- List exhaustive dependencies. If a dependency causes loops, fix the source
  (memoize the value, move it into the effect, or lift it) rather than omitting
  it from the array.

## Review checklist

- Is each value categorized (server / URL / form / local / derived) and owned in
  exactly one place, at the lowest sufficient level?
- Is derived data computed in render or `useMemo`, never stored or synced via an
  effect?
- Is every input controlled-or-uncontrolled for its lifetime, with native
  `label`, `name`, `type`, and `autocomplete` preserved?
- Does the form library own field state, with refs forwarded and a schema as the
  single validation source?
- Do conditional fields stay aligned across UI, registration, and schema, with
  `defaultValues` set and `reset()` working?
- Is submission state explicit, repeat submits guarded while pending, and user input
  preserved on error with focus moved to the first problem?
- Is every effect a real external sync, cancellable in cleanup, with exhaustive
  dependencies?
