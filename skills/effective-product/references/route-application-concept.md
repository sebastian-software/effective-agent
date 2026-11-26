# Route: Application Concept

Use this route when the requested outcome is a concept for a **new application**
or a deep review of such a concept before implementation planning. A feature
request, research question, or isolated scope decision stays on its narrower
Product route. Do not turn a concept into an implementation plan.

## Read the relevant product guidance

- [Discovery and Evidence Review](route-discovery.md) and
  [Product decision contract](product-decision-contract.md) for the problem,
  audience, evidence, and consequential assumptions.
- [Scope, Quality, and Shipping](route-scope-and-shipping.md) for the smallest
  coherent first version, non-goals, and quality bar.
- [Solution Modeling and Prototyping](route-design-modeling.md) when the
  application needs objects, flows, or interaction alternatives to make its
  solution understandable.
- [Decision Records](route-decisions.md) only to judge whether a durable choice
  merits a later ADR. Creating a concept does not create an ADR.

Load only the links needed for the current concept. Bring in
`effective-engineering` for consequential system or data feasibility and
`effective-web` for browser experience or browser-specific obligations; keep
their detailed designs out of the concept. Bring in `effective-engineering`
as well when the concept adds a second entry point or runtime component that
shares business rules or data; record its runtime and ownership as decided or
open.

## Develop the first concept

Read the user's idea, existing product evidence, and any applicable project
brief or repository context. An empty repository is a valid starting point.
Clarify only missing choices that change the application's purpose, primary
users, central use cases, hard constraints, or explicit exclusions. Label what
remains unknown rather than holding a broad discovery interview or inventing
customer evidence.

A first concept is useful when a reader can decide whether this is the
application they want. That usually needs the problem for a named audience, the
central use cases and the idea connecting them, the smallest coherent first
version with its non-goals, a coarse technical direction, and the risks or open
questions that could change the direction. Keep observations, stakeholder
claims, and assumptions visibly apart; an honest open question beats a
fabricated answer. The technical direction stays at the level of platform,
integration, data, and constraints; interfaces, schemas, and sequencing belong
to later planning. Use the project's concept format if one exists.

## Review the concept in depth

Start with the actual concept and its evidence. Compare its claims **with each
other** before adding new criteria: do the audience, problem, use cases,
solution, first-version scope, non-goals, and technical direction describe the
same application? Then examine product fit, coherent scope and quality,
feasibility, data and trust boundaries, material risks, and the evidence behind
consequential claims. A demanding technical or browser question belongs with
the matching discipline above; name the unresolved dependency in the concept.

Use the verdict vocabulary and correction ranking in
[Evidence Review](evidence-review.md). A choice that changes the product
promise, scope, or risk belongs to the user: present the paths, their
consequences, and a recommendation. A deferred decision cannot appear elsewhere
in the concept as settled, so a concept with an open blocker is not ready for
implementation planning.

When the user asks for a handoff to planning, ordered work packages with a
goal, a completion criterion, and dependencies are enough; name durable choices
that may merit an ADR. Keep small, clear concepts small.
