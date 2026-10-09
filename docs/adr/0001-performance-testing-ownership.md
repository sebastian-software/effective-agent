# ADR 0001: Split Benchmark Methodology from Load and Capacity Ownership

- Status: Accepted
- Date: 2026-07-22
- Decision issue: [#112](https://github.com/sebastian-software/effective-agent/issues/112)

## Context

`software-testing` already owns focused performance-regression evidence for a
concrete function or service path. It deliberately did not claim broader
benchmark, load, soak, stress, or capacity methodology. Leaving all of those
areas unassigned would hide a real ownership gap; assigning them together
without repository demand would make the collection promise guidance it has
not earned.

This decision separates the related but operationally different needs:

- repeatable microbenchmarks, comparative benchmarks, and bounded end-to-end
  workflow benchmarks;
- load, soak, and stress experiments against running systems; and
- performance targets, workload scenarios, and capacity decisions.

## Evidence

The evaluation inspected active Sebastian Software repositories at exact
`main` commits on 2026-07-22. It searched their recursive trees and the
organization code index for benchmark harnesses and for `k6`, Locust, JMeter,
Autocannon, load-test, soak, stress-test, and capacity-planning evidence.

### Repeated benchmark demand

- [`ferromark` at `055cc729`](https://github.com/sebastian-software/ferromark/blob/055cc72921eeb547e5cc32d99fa36ba92feffff0/benchmarks/pulldown-comparison/README.md)
  has Criterion suites, semantic parity gates, fixed feature intersections,
  corpus-size lanes, warmup and sampling rules, alternating baseline order,
  environment capture, raw estimate retention, and publication safeguards.
- [`palamedes` at `c2bb14e0`](https://github.com/sebastian-software/palamedes/blob/c2bb14e04c08d7119b95a885c5a4add1504ebf45/docs/proof-and-benchmarks.md)
  has reproducible isolated and end-to-end workflow benchmarks, checked-in
  corpora, warmups, repeated runs, medians, memory observations, comparison
  lanes, and explicit exclusions from each claim.
- [`pofile-ts` at `af6d6569`](https://github.com/sebastian-software/pofile-ts/blob/af6d65693ffb8aaa31282dc079f29ab1de50d004/benchmark/package.json)
  maintains a dedicated benchmark workspace with fixture generation and a
  repository-native runner.
- `parakeet-coreml` at `3a29d6f8` (source no longer publicly reachable)
  exposes a product-specific benchmark command for its native inference path.

The demand is not one framework recipe. It is a recurring need to make a
performance claim reproducible, comparable, semantically fair, and honest
about its environment.

### Thin load and soak demand

Three active running-system repositories were checked as representative
service shapes:

- `stellara` at internal snapshot `43cf48c5`, a Fastify REST and MCP gateway;
- `relanto` at internal snapshot `3ed351f2`, an email-delivery service; and
- `terminaro` at internal snapshot `2b588d18`, an appointment-booking
  application.

Their repository trees contain no maintained load, soak, or stress harness.
The organization-wide searches found no intentional k6, Locust, JMeter, or
Autocannon setup and no load-test, soak-test, stress-test, or capacity-planning
workflow. Lockfile substrings and unrelated prose were discarded as false
positives. Current evidence therefore does not support a tool-specific
first-party load-testing workflow or a separate performance-testing skill.

## Decision

1. `software-testing` owns repository-native benchmark methodology for
   microbenchmarks, comparative benchmarks, and bounded end-to-end workflow
   benchmarks. The detailed workflow is conditionally loaded only when the
   requested outcome is a benchmark design, repair, interpretation, or
   publishable performance claim.
2. `software-testing` continues to own focused performance-regression guards
   against an explicit, already agreed target.
3. `software-architecture` owns performance objectives, workload scenarios,
   service-level tradeoffs, capacity planning, and the decision that a load or
   soak experiment is needed. It does not silently become the implementation
   owner for a load-testing toolchain.
4. `software-validation` runs an existing repository-native benchmark, load,
   soak, or stress command and reports its evidence without redesigning the
   methodology.
5. No first-party skill currently claims new load, soak, or stress methodology.
   Agents must say so, preserve any repository-local runbook or established
   harness, and request an explicit workload and target instead of inventing a
   tool, traffic model, environment, or capacity claim.

## Alternatives Considered

### Add one broad reference to `software-testing`

Rejected. It would turn strong benchmark demand into an unsupported promise
about running-system load methodology and make a conditionally loaded resource
too heterogeneous.

### Add a separate performance-testing skill

Rejected for now. The observed benchmark cases fit the existing test-evidence
workflow, while maintained load and soak demand is absent. A separate skill
would add routing and maintenance cost without a coherent demonstrated scope.

### Route every performance test elsewhere

Rejected. It would ignore repeated benchmark practice already present in
several active repositories and keep a real methodology gap silent.

## Consequences

- Benchmark guidance must remain tool-agnostic and start from repository-native
  harnesses; it must not prescribe Criterion, Tinybench, or a new dependency.
- Comparative claims require semantic parity, explicit inclusions and
  exclusions, reproducible inputs, environment provenance, repeated evidence,
  and retained inspectable results.
- Load and soak requests receive an honest boundary rather than generic k6 or
  capacity advice disguised as repository-specific evidence.
- Revisit this decision when at least two maintained repositories have real
  load or soak harnesses, when repeated user work exposes a shared execution
  workflow, or when a single running-system case has enough operational depth
  to justify a focused first-party owner.
