# Route: Behavior-Preserving Ports

Treat a port as a controlled behavior migration. Preserve observable contracts
first; improve architecture and idioms after parity unless the user explicitly
accepts combined migration risk.

## Establish Authority and Feasibility

1. Determine whether the user asked for assessment, a plan, a pilot, or the
   complete port. Do not turn analysis into a rewrite without authorization.
2. Inspect repository instructions, dirty state, build graph, supported
   platforms, tests, benchmarks, public APIs, foreign-function boundaries,
   generated code, and release constraints.
3. Compare porting with credible alternatives: targeted hardening, adapters,
   incremental replacement, or retaining the current implementation. State the
   failure class or strategic benefit that justifies the port.
4. Identify the equivalence oracle. Prefer a language-independent test suite,
   protocol fixtures, golden files, compatibility corpus, differential tests,
   or production traces. If no trustworthy oracle exists, build a bounded one
   before scaling implementation.
5. Read [Migration contract](migration-contract.md) and record the preserved
   behavior, allowed differences, exclusions, invariants, and gates.

Stop and request direction when the source behavior is disputed, the target
changes product semantics, or no affordable verification can distinguish a
correct port from plausible-looking code.

## Choose a Resource Profile

Read [Execution profiles](execution-profiles.md), then select the smallest
profile that can satisfy the migration contract:

- **Solo:** one working agent, sequential batches, cold self-review or fresh
  passes, narrow checks after every batch, and scheduled full-suite checkpoints.
- **Paired:** an implementer plus one independent semantic reviewer for a named
  high-risk question or measured review benefit; deterministic checks remain
  the default evidence path.
- **Parallel:** independent shards with explicit ownership, isolated worktrees
  or directories, bounded concurrency, and a single integration queue.

State the chosen profile and why. More agents reduce wall-clock time only when the work can be
partitioned and verification keeps pace.

When any profile creates, adopts, writes in, stages from, integrates from, or
removes a worktree, read [worktree safety](worktree-safety.md). Record its
repository, absolute root, branch or commit, base, shard ownership, checkout
class, and cleanup ownership in run context; re-verify before the first write
and after every resume or handoff. Reuse a suitable harness-managed worktree
without nesting or claiming cleanup ownership.

Treat concurrency and model capability as separate controls. Read
[Model-tiered orchestration](model-tiering.md) when multiple model tiers are
available. Default to a strong architect at planning and milestone boundaries,
an efficient builder for bounded slices, deterministic evidence owned by the
builder or integrator, and risk-based specialist review instead of assigning a
second model to recheck every change.

## Build the Porting System

1. Map source concepts to target concepts: types, ownership, lifetimes, errors,
   cleanup, concurrency, reflection, compile-time behavior, FFI, numeric rules,
   text encodings, and platform APIs.
2. Store durable cross-cutting choices in the repository's accepted ADR system
   when they need lasting rationale. Keep temporary work queues in the existing
   issue or plan convention; do not invent a private agent-state directory.
3. Partition by dependency boundary and reviewer question, not raw line count.
   Mark high-risk seams such as async cleanup, callbacks, aliasing, GC/native
   ownership, serialization, and platform-specific code.
4. Port a representative vertical slice first. Include at least one hard
   lifetime or state boundary and one end-to-end behavior, not merely easy
   utility files.
5. Review the pilot against source, migration contract, tests, and performance.
   Update the mapping rules before expanding the same mistake across the tree.
6. Decide big-bang versus incremental delivery from coupling and deployability.
   Prefer one mechanical code conversion when a long-lived dual architecture
   would create more risk; prefer incremental replacement when components have
   stable seams and can ship independently.

## Run Evidence-Driven Loops

Advance through these queues in order, returning to earlier gates after broad
changes:

1. structural translation and dependency graph
2. parser, type-checker, or compiler failures
3. link and startup failures
4. narrow smoke paths and CLI or API entry points
5. focused unit and differential tests
6. full local suite
7. CI across supported platforms and configurations
8. leak, sanitizer, race, fuzz, benchmark, and production-canary evidence where
   relevant

For every batch:

1. Give the implementer the source slice, mapping rules, migration contract,
   owned files, and exact validation target.
2. Produce the smallest behavior-preserving change that advances one queue.
3. Run cheap deterministic verification and diff-hygiene checks.
4. Review the diff adversarially in a cold pass without relying on the
   implementer's explanation. Ask how it can compile and still be wrong.
   Escalate to an independent specialist only for the named risks or measured
   review benefits defined in the model-tiering guidance.
5. Apply verified review findings, then rerun the narrowest decisive check.
6. Record the result and remaining uncertainty in the existing work artifact.
7. When a failure pattern repeats, improve the shared rule or workflow before
   continuing. Do not hand-fix the same generator error indefinitely.

Read [Review and verification](review-and-verification.md) before running port
batches or declaring parity.

## Protect the Correctness Signal

Reject shortcuts that make dashboards greener without making the port correct:

- stubs, dummy returns, silent fallbacks, or broad exception swallowing
- deleting, weakening, quarantining, or skipping pre-existing tests
- changing golden outputs without an approved semantic difference
- blanket lint, type, sanitizer, or warning suppressions
- replacing ownership analysis with indiscriminate leaks or unsafe operations
- changing public behavior merely because the target language prefers it
- mixing unrelated redesigns into mechanical batches
- accepting compilation as evidence of behavioral equivalence

Permit a temporary compatibility shim only when it has a named owner, a removal
gate, focused coverage, and lower total risk than immediate replacement.

## Integrate and Ship

1. Integrate in dependency order and rerun affected downstream checks after
   every merge or shard combination.
2. Verify that tests actually executed and that counts, fixtures, platforms,
   sanitizers, and coverage did not silently shrink.
3. Compare behavior, performance, memory, binary or artifact size, and startup
   characteristics against the recorded baseline. Explain regressions; do not
   hide them inside aggregate claims.
4. Separate merge confidence from release confidence. Use canaries, shadow
   traffic, staged rollout, or rollback switches when the blast radius warrants
   them.
5. Report completed slices, verified gates, approved differences, unresolved
   risks, resource profile, and the next queue item. Claim completion only when
   every migration-contract gate passes or the user explicitly accepts an
   exception.

## Cross-links

- Ordinary dependency bumps — a version upgrade plus scoped local adaptation,
  even a major with migration work — are the Dependencies route. This route owns
  migrations dominated by mechanical repository-wide translation with their own
  parity evidence.
- Discovery and execution of established repository-native checks are the
  Validation route; this route owns migration-specific parity gates.
- Review and upkeep of the resulting pull requests are the Review route.
- Unresolved target-architecture direction, system-boundary tradeoffs, focused
  non-frontend test design beyond parity and differential evidence, and a
  post-parity Rust or TypeScript idiom and quality pass belong to
  `effective-engineering`.
- Durable migration decisions are recorded through `effective-product`.
