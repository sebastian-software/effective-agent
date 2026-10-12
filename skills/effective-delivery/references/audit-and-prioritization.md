# Audit and Prioritization

Use this reference to inspect a codebase for improvement opportunities without
padding the result with generic advice.

## Contents

- [Reconnaissance](#reconnaissance)
- [Patterns Across Completed Deliveries](#patterns-across-completed-deliveries)
- [Audit Lenses](#audit-lenses)
- [Finding Contract](#finding-contract)
- [Verification and Rejection](#verification-and-rejection)
- [Prioritization](#prioritization)
- [Report Shape](#report-shape)

## Reconnaissance

Establish the repository's actual operating model before evaluating it:

- Read scoped `AGENTS.md`, `CLAUDE.md`, contributing guidance, README files,
  manifests, workspace configuration, and CI workflows.
- Identify languages, frameworks, package managers, deploy targets, generated
  areas, and exact build, lint, typecheck, and test commands.
- Read accepted ADRs and relevant product, architecture, security, design, and
  domain documents. A documented tradeoff is not automatically a defect; drift
  between the decision and reality may be.
- Inspect representative implementation and tests before inferring conventions.
- Use Git history and churn only as supporting signal. Old code is not wrong
  merely because it is old, and frequently changed code is not automatically
  unhealthy.
- Note missing or broken verification early. A trustworthy baseline may need to
  precede a risky refactor.

State the audit boundary. On large repositories, name packages and categories
not inspected instead of implying exhaustive coverage.

## Patterns Across Completed Deliveries

When asked to analyze patterns across delivered work, compare relevant
evidence in existing project artifacts and describe gaps in their coverage:

- Work without a review has unknown review status. A review with no findings
  shows only that none were recorded within its scope.
- Failures reproduced independently across changes can indicate recurrence;
  repeated reports or tools describing one cause remain one observation.
- An action landing shows that it was implemented. Evidence that it helped
  requires observing the relevant outcome; timing alone is not enough.
- Assess decisions against the requirements and information available when
  they were made, not with hindsight.
- Missing evidence is unknown, not evidence of failure.

Churn, commit volume, and finding counts can guide follow-up investigation; they
do not measure delivery quality or individual contribution.

## Audit Lenses

Choose lenses that fit the request; do not force every audit through every
category.

### Correctness and resilience

Trace error paths, async work, shared state, nullability, boundary conditions,
state transitions, retries, transactions, cleanup, idempotency, and recovery.
Distinguish a reachable failure from a theoretical possibility.

### Security and privacy

Inspect trust boundaries, authentication and authorization, input contracts,
interpreter and filesystem sinks, credential handling, production configuration,
and sensitive logging. Keep reports defensive and omit exploit payloads and
secret values.

### Performance and capacity

Prioritize waterfalls, repeated I/O, N+1 access, wrong algorithmic complexity,
unbounded work, payload and bundle size, cache boundaries, and resource leaks
before micro-optimizing cheap local operations. Measure when cost is uncertain.

### Tests and verification

Map high-risk and high-churn paths to meaningful coverage. Look for missing
regression tests, assertions that prove little, brittle snapshots, over-mocking,
uncontrolled time or network, and the absence of a dependable one-command
baseline.

### Architecture and complexity

Look for duplicated policy, divergent implementations, inappropriate coupling,
cycles, single-implementation abstractions, pass-through layers, dead
flexibility, inconsistent patterns, and shared concepts represented differently.
Use the [Complexity lens](complexity-lens.md) before recommending new structure.

### Dependencies and migrations

Check support status, reachable advisories, deprecated APIs, duplicate tools,
abandoned critical dependencies, lockfile drift, and the actual blast radius of
an upgrade. Route a full update portfolio through the dependencies route.

### Developer experience and operations

Inspect setup accuracy, feedback-loop speed, local/CI parity, configuration
discovery, error messages, logs, runbooks, and whether routine work has one
discoverable path.

### Agent divergence as repository evidence

When several agents repeatedly implement the same bounded task differently,
compare their decisions with code, tests, examples, ADRs, terminology, ownership,
and module boundaries before merely tuning prompts. Concrete divergence can
expose a missing or conflicting contract, undocumented standard, weak
observation point, or architecture that relies on tacit knowledge.

Report this only when the divergence creates a verified cost or behavior risk.
One poor generation does not prove the repository is at fault. Correct the
source that should own the truth—code, test, accepted decision, documentation,
or boundary—rather than accumulating a large agent-only instruction manual.

### Documentation and decision drift

Report documentation only when absence or staleness creates a concrete cost.
Check whether accepted ADRs still match code, design, copy, or operational
behavior and whether current decisions are discoverable.

### Product direction

Ground options in unfinished intent, documented product goals, real user
friction, asymmetrical feature surfaces, or capabilities the architecture makes
unusually cheap. Present direction separately from defects; strategy remains a
maintainer choice.

## Finding Contract

Use this shape for each finding:

```md
### Short outcome-oriented title

- Evidence: `path/file.ext:123` and the verified behavior
- Reachability: supported trigger, affected surface, and relevant exposure or lifetime without invented probabilities
- Impact: concrete consequence, recovery, reversibility, risk, cost, or blocked capability
- Effort: S, M, or L, including tests and migration work
- Fix risk: LOW, MEDIUM, or HIGH, with the main regression surface
- Confidence: HIGH, MEDIUM, or LOW, based on inspected evidence
- Direction: the smallest credible correction and why its total ownership cost is proportionate, not a complete implementation plan
```

Use exact locations and symbols. Explain why the issue matters and what a safe
direction looks like; do not bury the actionable point in a long preamble.

For code-review-style output, compress the contract to location, problem,
consequence, and concrete correction while retaining the non-obvious rationale.

## Verification and Rejection

Before presenting a finding:

1. Open the cited implementation and its callers, configuration, and tests.
2. Reproduce or logically trace the claimed behavior far enough to establish
   reachability.
3. Check accepted decisions and current repository conventions.
4. Deduplicate findings that share one root cause.
5. Downgrade uncertainty to an investigation item instead of prescribing a fix.

When a finding may overlap existing work, search the relevant issue and PR
trackers for a distinctive error fragment, affected symbol or contract, or
intended outcome. If a title search misses the work, try alternate wording for
the symptom or outcome. Compare candidates by symptom, error text, affected
contract, and intended outcome rather than title. Check the item's state,
rationale, and changed evidence, including closed items when their history may
contain a completed fix or rejected direction. Treat only the same underlying
problem as a duplicate; keep related work and competing solutions distinct.

Reject candidates that are by design, already fixed, based on stale line
numbers, unsupported by evidence, or whose avoided harm does not justify the
implementation, cognitive, test, maintenance, and regression cost. Do not use
invented percentages to force a decision. In a recurring
audit or saved backlog, retain a concise rejected rationale so the same weak
finding is not rediscovered repeatedly.

## Prioritization

Rank by leverage rather than severity labels alone:

1. Concrete user, security, data, or operational harm.
2. Work that establishes verification or unblocks several later fixes.
3. High-confidence improvements with small effort and low regression risk.
4. Repeated costs at shared boundaries rather than isolated aesthetic cleanup.
5. Direction or modernization work whose timing is supported by repository
   intent and current external facts.

Do not manufacture a fixed number of findings. A short audit with two important
items is better than a complete-looking list with speculative filler.

## Report Shape

Return:

1. Scope and important exclusions.
2. Vetted findings in priority order.
3. Direction options in a separate section when requested.
4. Dependency order and the recommended next item.
5. Rejected or uncertain candidates only when they prevent repeated confusion.

If the user asked only for an audit, stop there. Do not silently create files,
issues, branches, or fixes.
