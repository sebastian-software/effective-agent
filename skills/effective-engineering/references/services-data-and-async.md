# Services, Data, and Async

Service behavior is often true because of a real boundary. Preserve the
specific boundary that gives the claim meaning instead of replacing it with a
fully mocked handler.

## APIs and Service Contracts

Test the observable contract: authorized and unauthorized outcomes, validation,
serialization, errors, idempotency identity, and side effects. Use the
repository's established auth and transport harness where access rules,
middleware, request parsing, or response mapping are part of the risk.

For an agreed provider or consumer contract, test the agreed request, response,
error, compatibility, and version behavior. Contract design and ownership are
not invented by the test; raise an unresolved shape or responsibility question
to the architecture route.

## Databases, Migrations, and Isolation

Use the repository's real database harness when constraints, query semantics,
RLS, transaction behavior, migrations, locking, or tenant isolation make the
claim true. Give each case explicit setup, identity, and cleanup.

- Create at least the actors and records needed to distinguish allowed from
  disallowed access; a same-tenant happy path does not prove isolation.
- Test migrations against the actual before-and-after schema state where the
  project supports it. Verify the changed invariant, not merely that a file
  exists or the migration command exits successfully.
- Make transaction boundaries deliberate. Assert commit, rollback, visibility,
  uniqueness, or conflict behavior that callers depend on.
- Avoid shared test fixtures with implicit tenant, time, or cleanup state; they
  make authorization and ordering defects appear flaky.

## Retries, Timeouts, and Cancellation

Model the timeline. Name the initiating request, side effect, acknowledgement,
timeout, retry, cancellation, and observable final state. A timeout after a
side effect is not proof that the side effect failed.

Control time and scheduling with the repository's established seam. Advance a
clock or resolve a controlled operation rather than sleeping. Use a stable
request or idempotency identity and assert the resulting side effect occurs at
most once when that is the contract. Include the uncertain-acknowledgement path
and recovery or reconciliation behavior; do not only test a failure before any
work starts.

For callbacks, queues, streams, and concurrent workers, make event order and
ownership explicit. Use a bounded deterministic event sequence or replay when
that expresses the protocol. Check duplicate delivery, ordering assumptions,
visibility, cancellation, cleanup, and terminal error behavior that the system
promises.

## Failure Paths and Flakes

Classify an intermittent failure before changing it:

- real time or arbitrary timeout;
- uncontrolled order or race;
- shared global, database, filesystem, port, or environment state;
- incomplete cleanup or teardown;
- a live external system, credential, network, or nondeterministic response;
- a hidden retry or background task that outlives the assertion.

Replace the uncontrolled cause with explicit state, a local harness, controlled
clock, bounded event coordination, isolated resource, or replay. Never make a
test “stable” by adding retries, sleeps, broad catch blocks, or weaker
assertions that conceal the contract.

## Focused Performance Guards

Use a performance-regression guard only for a concrete function or service path
with an explicit target and a controlled enough environment to make the signal
useful. Fix the input corpus, setup, warm-up policy, operation, and reported
metric. On shared CI, a relative or historical-trend threshold is often more
honest than one brittle absolute latency number.

Measure the path that matters and report environment limits. Read
[Benchmark methodology](benchmark-methodology.md) when the outcome is a wider
microbenchmark, comparison, bounded workflow benchmark, or publishable claim.
Route performance targets and capacity planning that need architecture
tradeoffs to the architecture route; route browser performance to
`effective-web`. New load, soak, and stress methodology is outside this
collection.
