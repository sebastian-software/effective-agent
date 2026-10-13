# React Components

Use this route for reusable React component work. Keep React-specific API
decisions connected to semantic HTML, accessibility, forms UX, responsive
layout, and motion rules from the related Effective Web routes.

## Workflow

1. Inspect the existing component conventions: prop naming, state ownership, styling API, accessibility patterns, form library, refs, portals, and test setup.
2. Choose the component boundary: primitive, composed widget, app-specific component, or thin adapter around a headless library.
3. Define state ownership: controlled, uncontrolled, externally managed, form-managed, or derived.
4. Preserve semantic DOM and accessible names. Read the accessibility, forms,
   component, layout, and motion routes when the component renders those concerns.
5. Expose stable extension points: slots/children, `as`/polymorphism only when justified, data attributes, CSS custom properties, refs, and event callbacks.
6. Harden states: loading, empty, error, disabled, success, focus, hover, reduced motion, translated text, SSR/hydration, and async transitions.

## Reference Files

- [component-api-design.md](component-api-design.md) - Composition, polymorphism, slots, and reusable APIs.
- [forms-and-state.md](forms-and-state.md) - React forms, data binding, controlled state, and state ownership.
- [interop-and-accessibility.md](interop-and-accessibility.md) - React Aria, Radix, custom elements, refs, and accessibility pass-through.

## Boundaries

Read [React Architecture](route-react-architecture.md) for React Server
Components, hydration, rendering boundaries, and app-level performance
architecture. Read [Design Review and Modernization](route-design.md) for visual design and
framework-agnostic quality rules.
