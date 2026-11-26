# Architecture Foundations

Use this reference to reason about system direction without treating a diagram
or a named pattern as proof of a good design.

## Contents

- [Establish the Decision Frame](#establish-the-decision-frame)
- [Map Boundaries and Contracts](#map-boundaries-and-contracts)
- [Evaluate Module Depth](#evaluate-module-depth)
- [Compare Options](#compare-options)
- [Plan Evolution](#plan-evolution)
- [Evidence and Communication](#evidence-and-communication)

## Establish the Decision Frame

Write the smallest useful frame before proposing a structure:

| Area | Establish |
| --- | --- |
| Outcome | User or business outcome, critical flows, and failure impact |
| Constraints | Existing contracts, data residency, budget, deadline, team skills, supported platforms, and accepted ADRs |
| Quality attributes | Concrete scenarios for latency, availability, recovery, consistency, throughput, security, privacy, operability, and changeability |
| Current shape | Entry points, deployable units, dependencies, data stores, external systems, and ownership |
| Unknowns | Missing load, incident, cost, compliance, or ownership evidence that could change the recommendation |

Phrase quality attributes as observable scenarios. Prefer “a payment submission
does not create a second charge when the caller retries after a timeout” over
“the system should be reliable.” Identify the signal, target, and tradeoff;
do not manufacture a number when none is known.

## Map Boundaries and Contracts

Describe only the boundaries that affect the decision:

- **Responsibility:** name the capability or business rule the boundary owns.
- **Runtime:** state whether the parts share a process, run separately, or are
  not decided yet. Record this separately from repository layout and
  deployment; a shared repository does not imply a shared process.
- **Data ownership:** name the authoritative writer and the replication,
  projection, or synchronization method used by others.
- **Interface:** define inputs, outputs, errors, versioning, and whether the
  caller expects synchronous completion, eventual completion, or a durable
  acknowledgement.
- **Failure behavior:** decide timeouts, retry safety, idempotency, ordering,
  deduplication, dead-letter or compensation paths, and the user-visible
  degraded state where relevant.
- **Trust boundary:** identify where identity, authorization, validation,
  encryption, or audit evidence must be enforced. Do not call a network zone a
  security control without a concrete policy and enforcement point.
- **Ownership:** identify the team or role responsible for operating and
  changing the boundary. An unowned service or queue is a risk, not autonomy.

Avoid a database shared directly by multiple independently deployed services.
If a temporary exception is necessary, state its owner, permitted access,
replacement path, and removal gate.

### Additional Entry Points

When a concept gives the same business rules or data a second entry point (for
example a browser product and an agent channel) or adds a runtime component
that shares them, record the items above for the new path: runtime, call path
through which existing contract, failure behavior, and the component that
enforces authorization and audit. Concepts with one component and one channel
need nothing extra.

- Two channels do not imply two copies of business rules. Name any constraint
  that exists only in one channel and decide whether the shared contract
  enforces it instead of copying it into the new path.
- “Not decided” is valid when the concept records its consequence and the
  decision needed before implementation. Do not invent an identity protocol or
  permission model to fill the gap; an API description such as OpenAPI does not
  settle how a request acts for an authorized user.
- Choose between an in-process adapter and a separate service with
  [Compare Options](#compare-options); neither is the default.
- Name what each first-increment check proves; see
  [Select Test Evidence](select-test-evidence.md#name-what-a-boundary-check-proves).

## Evaluate Module Depth

Prefer a small interface that removes meaningful complexity from its callers.
Before adding or preserving a layer, ask:

- What behavior, invariant, failure handling, or coordination does the
  interface make callers no longer need to understand?
- If the module disappeared, would complexity vanish with it, or spread back
  into several callers?
- Can callers and tests exercise the contract through the same stable
  interface, or must they reach through it to verify useful behavior?
- Does the seam represent demonstrated variation or multiple justified
  implementations, rather than a hypothetical adapter around one path?

A pass-through wrapper, one-to-one method mirror, or single-implementation
interface can still own compatibility, policy, observability, or a genuine
boundary. Keep it only when that leverage is concrete and explainable. Do not
measure depth by implementation-line count or hide a broad, surprising
interface behind the word “module.”

## Compare Options

### Choose the strategic control surface

For build, buy, open-source, managed-service, or vertically integrated options,
decide what the organization must control rather than assuming it must own every
implementation. Inspect:

- whether the capability differentiates the product or merely supports it;
- failure impact, diagnosis and recovery authority, and supplier response;
- data ownership, portability, interface stability, and switching path;
- security, privacy, compliance, availability, and jurisdiction constraints;
- total acquisition, integration, operation, support, migration, and exit cost;
- internal expertise, attention, opportunity cost, and time to useful evidence;
- concentration risk, roadmap dependence, and credible substitutes.

Control may mean owning the implementation, or instead owning the contract,
data, observability, fallback, and tested exit path. Prefer open source or
in-house work when its concrete control properties justify their lifecycle
cost; prefer a supplier when it preserves the required control more cheaply.
Do not equate proprietary with unsafe, open source with maintainable, or
vertical integration with advantage without project-specific evidence.

Compare only realistic options, often including retaining or simplifying the
current shape. Use decision drivers rather than a generic scorecard:

| Option | Meets | Costs or risks | Delivery and reversal |
| --- | --- | --- | --- |
| Modular monolith | In-process boundaries, simple deployment, transactional work | Coupled release and common scaling | Refactor modules; extract only proven seams |
| Separate service | Independent lifecycle, ownership, security, or scaling where evidenced | Network failure, observability, distributed data, deployment overhead | Introduce a compatible contract; migrate consumers; remove bridge |
| Async workflow | Decoupled throughput or long-running work | Event contracts, ordering, duplication, eventual consistency | Add idempotent consumer and replay plan before moving the flow |

These are prompts, not defaults. A service does not become independently
scalable merely because it runs in another process, and a modular monolith is
not an anti-pattern when its module boundaries remain enforceable.

## Plan Evolution

Prefer an evolutionary path when a stable seam exists:

1. Record the current contract and baseline behavior, including metrics and
   known failure modes.
2. Add the new path behind a compatible interface, feature flag, adapter, or
   explicit version boundary.
3. Migrate a narrow flow or consumer. Compare outputs, latency, errors, and
   operational load with the baseline.
4. Expand only after the hypothesis holds. Keep rollback viable while both
   paths exist.
5. Remove compatibility code, old storage access, flags, and documentation at
   a named gate. Temporary dual writes, sync jobs, and adapters need ownership
   and an expiry; they are not a permanent architecture.

Use a one-time cutover only when compatibility is unsafe, dual operation costs
more than a short outage, or the boundary cannot be meaningfully isolated.

## Evidence and Communication

Use repository code, production telemetry, incident history, contracts,
deployment configuration, experiments, and stakeholder constraints as evidence.
Mark predictions as predictions. Link a durable direction to an ADR; keep the
implementation plan, runbook, dashboard, and exact configuration in their
respective owner artifacts.
