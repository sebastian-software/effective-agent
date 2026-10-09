---
name: effective-web
description: >-
  Design, build, review, and test browser experiences: UI, CSS, React,
  accessibility, performance, and print. Use also for reference-site analysis,
  originality reviews, and web legal/consent disclosures. General browsing,
  backend work, and repository audits are outside this skill.
---

# Effective Web

Choose the route for the browser outcome and load only the references needed
for the affected behavior. Use Design Planning for a new direction and Design
Review and Modernization for a broad redesign; add focused routes as needed.

Work within the product language, supported browsers, and existing contracts.
Preserve accessibility, privacy, authentication, and user data. Add states,
fallbacks, fixtures, and tests for reachable behavior with meaningful user
consequences; avoid speculative combinations.

Verify what the change can affect. Use browser evidence when rendering or
interaction matters, and reuse existing fixtures and checks where sufficient.
Complete authorized implementation and verification before handing back the
result; report material evidence gaps.

## Route by Intent

| User intent | Read |
| --- | --- |
| Plan a new experience or AI-assisted feature: register, hierarchy, direction, and interaction model | [Design Planning](references/route-design-planning.md) |
| Critique, redesign, modernize, polish, or quality-gate an existing experience | [Design Review and Modernization](references/route-design.md) |
| Fix hierarchy, grids, spacing, responsive layout, or safe areas | [Layout and Spacing](references/route-layout.md) |
| Improve type hierarchy, measure, rhythm, fallbacks, or font loading | [Typography](references/route-typography.md) |
| Build palettes, semantic tokens, contrast, dark mode, or themes | [Color and Theming](references/route-color.md) |
| Design buttons, navigation, dialogs, menus, or reusable primitives | [Component Primitives](references/route-components.md) |
| Build field layouts, validation, completion, or multi-step forms | [Forms UX](references/route-forms.md) |
| Design dense data, sorting, filtering, row actions, or responsive tables | [Data Tables](references/route-tables.md) |
| Review HTML semantics, accessible names, ARIA, focus, or keyboard use | [Accessibility and HTML](references/route-accessibility.md) |
| Add transitions, scrolling behavior, feedback, or reduced-motion support | [Motion and Interaction](references/route-motion.md) |
| Support localization, RTL, text expansion, or locale-aware formatting | [Internationalization UX](references/route-i18n.md) |
| Write labels, microcopy, empty states, errors, or product language | [Interface Copy](references/route-copy.md) |
| Design loading, empty, success, failure, retry, or not-found states | [Error and Loading States](references/route-states.md) |
| Build login, passkeys, recovery, sessions, permissions, or security UX | [Auth and Security UX](references/route-auth.md) |
| Organize cascade layers, tokens, scoping, browser support, or CSS tooling | [CSS Architecture](references/route-css.md) |
| Improve metadata, structured data, crawlability, previews, or AI search | [Frontend SEO and AI Search](references/route-seo.md) |
| Choose unit, component, visual, browser, or E2E coverage and CI strategy | [Frontend Testing](references/route-testing.md) |
| Show what a branch or pull request changes on rendered pages with annotated before/after screenshots | [Change Screenshots](references/route-change-screenshots.md) |
| Diagnose Core Web Vitals, images, caching, resource loading, animation cost, memory growth, or perceived speed | [Web Performance](references/route-performance.md) |
| Decide React server/client boundaries, state placement, hydration, or rendering | [React Architecture](references/route-react-architecture.md) |
| Design reusable React APIs, composition, state ownership, refs, or interop | [React Components](references/route-react-components.md) |
| Build, style, animate, optimize, or make accessible SVG icons and illustrations | [SVG Graphics](references/route-svg.md) |
| Create SVG noise, grain, paper, clouds, organic surfaces, or filter effects | [SVG Textures](references/route-textures.md) |
| Build print stylesheets, paged media, printable documents, or web-to-print output | [Print Design](references/route-print.md) |
| Turn a supplied website, screenshot, recording, prototype, or reference pack into an evidence-backed visual and interaction specification | [Reference Analysis](references/route-reference-analysis.md) |
| Compare produced work with its references for source overlap, distinctive combination, and asset provenance, and decide release risk | [Originality Review](references/route-originality.md) |
| Scope Impressum and operator disclosures, privacy and cookie notices, consent and tracking, or online-sales information across jurisdictions | [Web Legal Compliance](references/route-compliance.md) |

## Routing Boundaries

- `effective-product`: research, product direction, scope, interaction models,
  information architecture, decision-grade prototypes, release decisions, and
  durable design decisions recorded as ADRs.
- `effective-marketing`: positioning, commercial page/campaign copy, funnel
  diagnosis, and experiment decisions. Build and verify the chosen variants here;
  interface labels, errors, and states stay here.
- `effective-writing`: editorial articles and public prose, plus locale-level
  punctuation and formatting. Layout and localization UX stay here.
- `effective-engineering`: non-frontend system/data contracts, Rust, shared-library
  TypeScript, focused non-frontend tests, and benchmark methodology.
- `effective-delivery`: repository audits, ports, PR upkeep including publishing
  screenshots in a description, dependencies, technical documentation, and
  execution-only requests for established checks.

General browsing or research does not belong here merely because it uses a URL.
Backend infrastructure, deployment, load testing, dedicated security audits,
and non-web publishing need other expertise. Legal and originality work here
supports implementation; it does not establish legal clearance.
