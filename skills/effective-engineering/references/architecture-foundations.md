# Architecture Foundations

Use this reference to reason about system direction without treating a diagram
or a named pattern as proof of a good design.

## Contents

- [Establish the Decision Frame](#establish-the-decision-frame)
- [Map Boundaries and Contracts](#map-boundaries-and-contracts)
- [Make a New Entry Point Explicit](#make-a-new-entry-point-explicit)
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

## Make a New Entry Point Explicit

Use this when a concept gives the same business rules or data more than one
entry point (for example a browser product and an agent channel), or adds a
runtime component beside existing ones that shares them. A single-component
concept, or a single-channel one that adds no runtime component, needs none of
it. Record, reusing the boundary list above:

- **Runtime:** same process, separate process, or not decided, recorded
  separately from repository layout and deployment.
- **Call path, contract, and failure:** who calls whom, through which interface
  and existing contract, and how the path fails.
- **Owning component:** which component owns the Responsibility, Data ownership,
  and Trust boundary items above, including authorization and audit.
- **First-increment evidence:** what each planned check actually proves.

“Not decided” is valid when the concept records the consequence and the
decision needed before implementation; never invent an identity protocol or
permission model to fill the gap. A shared repository does not imply a shared
process, and two channels do not imply two copies of business rules. Call out a
constraint that exists only in one channel and decide whether the shared
contract enforces it; do not copy it into the new entry point.

Example: a browser product with a backend HTTP API adds a Model Context Protocol
(MCP) entry point so that a customer agent can start a document review.

| Variant | Runtime and call path | Owner and enforcement | Tradeoff |
| --- | --- | --- | --- |
| In-process adapter | API process; the MCP module calls application services | Services own rules; authorization and audit apply only where enforced below the HTTP layer | No extra hop; shares failure and load with the API and couples to its internals |
| Separate service | Own process, even in the same repository; calls the HTTP API, with no backend imports or database access | Backend API, as for the browser | Clear contract; another service to operate, an unavailable backend to handle, identity across a network hop |

Neither variant is the default; see [Compare Options](#compare-options). In
both, how an agent request acts for an authorized user is open until decided,
and an API description such as OpenAPI does not settle it. Until then, the first
increment can prove the lower evidence rungs below while business tools stay
unavailable.

Keep evidence rungs separate, naming caller and hop for each:

- **Availability:** a health check proves the component runs, with no identity.
- **Protocol:** a client call through the new entry point proves the protocol.
- **Connectivity:** a round trip with the component's own credential proves
  that hop and credential, not user authorization.
- **Business boundary:** a denial at a real protected operation of the owning
  component proves that an identity cannot cross there; without such an
  operation the denial is unproven, and a missing tool is no proof.

See [Select Test Evidence](select-test-evidence.md) for what must stay real.

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
