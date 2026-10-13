# Route: Software Architecture

Turn a product and delivery problem into a system direction that can be built,
operated, and changed safely. Prefer a small, evidenced design over named
patterns, diagrams, or distributed components without a clear driver.

## Choose the Mode

- **Assess:** map an existing system and report verified architectural risks,
  strengths, and unknowns without editing it.
- **Design:** compare viable options and recommend the smallest architecture
  that meets stated quality attributes and constraints.
- **Review:** test an architecture proposal or ADR against the current system,
  operational reality, and delivery path. Route implementation-plan review to
  `effective-delivery`.
- **Evolve:** define an incremental migration, compatibility period, rollback
  conditions, and evidence gates for an approved direction.

Respect the user's authority. Do not change source, infrastructure, cloud
resources, secrets, deployments, or decision records during an assessment or
design request unless explicitly asked.

## Read

- [Architecture foundations](architecture-foundations.md) to map
  responsibilities, boundaries, interfaces, data ownership, quality scenarios,
  and viable options.
- [Operability and Twelve-Factor practices](operability-and-twelve-factor.md)
  when the system is a service, API, worker, scheduled process, or deployment
  change. Treat the factors as operational design prompts, not a checklist that
  mandates containers, microservices, or a cloud vendor.
- [Source-verified external contracts](source-verified-external-contracts.md)
  when a framework, dependency, platform, or provider contract materially
  affects the recommended architecture or its public behavior, including a
  technology choice that rests on current support, licensing, availability, or
  limits.

## Workflow

1. Discover the product goal, users, critical flows, scale or latency needs,
   compliance and data constraints, team ownership, delivery constraints, and
   the consequences of failure. Read scoped instructions, repository docs,
   manifests, deployment and CI configuration, runbooks, observability setup,
   representative entry points, tests, and accepted ADRs before judging.
2. State the decision scope and evidence limits. Separate facts observed in the
   system from assumptions, forecasts, and open questions. Do not invent load,
   availability, recovery, regulatory, budget, or ownership requirements.
3. Map responsibilities, boundaries, interfaces, data ownership, quality
   scenarios, and viable options. Keep diagrams proportional: a concise
   component map or sequence may clarify a consequential relationship; it is not
   a deliverable by default.
4. For each serious option, name the changed boundaries and contracts, the
   operational model, benefits, costs, failure modes, security implications,
   migration path, and how the important claims will be verified. Reject an
   option that solves an imagined scale problem while increasing actual
   coupling, latency, cost, or support burden.
5. Recommend one direction with explicit tradeoffs, deferred choices, and the
   next smallest reversible step. Create or update an ADR only when the choice
   is durable and the user authorizes that artifact; use `effective-product` for
   its repository convention and lifecycle.
6. For an approved evolution, sequence delivery around stable seams: establish
   observability and tests, introduce compatible contracts, migrate one flow or
   consumer at a time, measure, remove the old path, and verify the intended
   quality attributes. Set a removal owner and gate for every temporary bridge.

## Deliverables

Return the smallest artifact that makes the next decision or delivery step
clear. A useful architecture recommendation normally contains:

- context, constraints, observed system shape, and open questions;
- the recommended boundaries, responsibilities, data ownership, and contracts;
- quality scenarios and operational expectations that drove the choice;
- considered alternatives and concrete tradeoffs;
- a migration or delivery sequence, compatibility and rollback conditions; and
- verification signals, including what would cause the direction to be revised.

Keep exact topology, ports, endpoint values, environment values, credentials,
and runbook commands in their owning code, configuration, or runbooks. Never
place secrets or personal data in an architecture artifact.

## Operating Rules

- Start from the simplest deployable shape. A modular monolith is a valid
  default when it meets the product and operational needs; introduce a service
  boundary only for a concrete independent scaling, reliability, security,
  ownership, lifecycle, or technology reason.
- Make ownership singular. One component or service owns each mutable business
  fact; other components receive a contract, projection, or explicit write
  protocol rather than sharing its storage by accident.
- At every process or network boundary, assess failure contracts: timeouts,
  retry safety, idempotency, ordering, partial completion, degraded behavior,
  and compatibility. Define only the contracts warranted by the dependency
  contract, observed behavior, or consequence; do not encode every imaginable
  undocumented combination.
- Distinguish architecture from implementation preference. A framework, queue,
  database, or pattern is a means, not the decision unless its properties are
  the durable tradeoff.
- Keep security architecture specific to a threat and trust boundary. Escalate
  specialist security, privacy, compliance, capacity, cost, or incident
  decisions when the available evidence cannot establish a safe direction.
- Treat observability, deployment, data recovery, and rollback as design
  concerns for consequential flows, not post-launch chores.

## Testing-Strategy Design

This route owns non-frontend testing-strategy design: the test-pyramid shape,
coverage goals, and which risks deserve which test types, derived from the
system's quality scenarios, contracts, and failure consequences rather than from
a generic pyramid ratio. Hand the agreed strategy to the Testing route for
focused test design and implementation, and route frontend testing strategy to
`effective-web`. Load, soak, and stress work stays split: the objectives,
workload scenarios, and capacity decisions are owned here; execution
methodology is outside this collection (see the
[load, soak, stress, and capacity boundary](benchmark-methodology.md#load-soak-stress-and-capacity-boundary)).

## Cross-links

- Data models, datastore choice, transactions, consistency guarantees,
  replication, partitioning, batch or streaming semantics, and safe data
  evolution within agreed boundaries are the Data route. Overall service
  boundaries, quality attributes, ownership, and deployment direction stay here.
- Rust and TypeScript implementation depth within an agreed boundary are the
  Rust and TypeScript routes.
- Benchmark design and interpretation against a named performance question is
  the Benchmarks route, after the performance question, workload scenario, and
  target are agreed here.
- Repository-wide audit findings, prioritization, implementation plans,
  behavior-preserving ports, pull-request review, and execution of an existing
  repository benchmark, load, soak, or stress command belong to
  `effective-delivery`. Team boundaries, ownership, delegation, decision paths,
  and cognitive load belong there too when the organization around a boundary,
  not the boundary itself, is what has to change.
- Frontend CSS, React, rendering, component, and interface architecture belong
  to `effective-web`.
- Durable choices, ADR format, supersession, and drift control belong to
  `effective-product`.

Use this route when the system-level direction itself needs reasoning; use the
narrower route once the question becomes its specialized execution work.
