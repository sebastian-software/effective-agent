# React Architecture

Use this route for React architecture decisions that affect rendering, server/client boundaries, data flow, hydration, streaming, or performance.

## Workflow

1. Identify the runtime and framework: React version, Next.js/Remix/React Router/Vite, server rendering mode, RSC support, and deployment target.
2. Separate architecture work from component craft. Read [React Components](route-react-components.md) when the task becomes reusable UI implementation.
3. Choose data and state placement deliberately: server, client, URL, cache, form, external store, or component local state.
4. Define server/client boundaries by data access, interactivity, serialization, bundle cost, and ownership.
5. Read [React performance priorities](react-performance-priorities.md) and
   inspect waterfalls, bundle boundaries, request isolation, cache scope, and
   client ownership before optimizing re-renders or JavaScript loops.
6. Diagnose rendering work before optimizing: re-render source, expensive child, context churn, memoization cost, hydration mismatch, or network waterfall.
7. Prefer clear architecture over premature memoization or framework-specific cleverness.

## Reference Files

- [react-performance-priorities.md](react-performance-priorities.md) - impact
  order, async dependency graphs, bundle discovery, server state, caches, and
  client persistence.
- [server-components.md](server-components.md) - RSC mental model, boundaries, and framework caveats.
- [rendering-performance.md](rendering-performance.md) - Re-renders, memoization, hooks, and UI responsiveness.
- [framework-boundaries.md](framework-boundaries.md) - Next.js, Vite, React Router, Server-Timing, and CSS/runtime boundaries.

## Boundaries

Do not use this route for visual design or generic component APIs unless
rendering architecture is the primary issue. Cross-reference
[Design Review and Modernization](route-design.md), [React Components](route-react-components.md),
[Web Performance](route-performance.md), and [Frontend Testing](route-testing.md)
as needed.
