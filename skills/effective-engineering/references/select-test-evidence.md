# Select Test Evidence

Choose an evidence layer from the claim, not from a preferred test taxonomy.
The useful question is: *what must remain real for this test to distinguish the
failure we care about?*

## Make the Claim Testable

Write a compact behavior model before building fixtures:

| Element | Question |
| --- | --- |
| Rule or invariant | What must always, never, or eventually be true? |
| Trigger | Which input, prior state, event, or environment exposes it? |
| Observable result | What can a caller, collaborator, datastore, process, or user observe? |
| Failure distinction | Which plausible wrong implementation should fail this test? |
| Real boundary | Which auth, schema, serialization, transaction, clock, process, or protocol behavior makes the claim meaningful? |
| Risk and test value | Why is this failure worth guarding, and will this evidence reduce more expected harm or uncertainty than it costs to own? |

Keep the model small enough to guide one focused change. A vague request such
as “increase coverage” is not a claim; inspect the uncovered risk or ask for a
concrete behavior. Conversely, do not split one coherent claim into isolated
assertions merely to satisfy an assertion-count rule.

A mock can support a claim about a collaborator call, but it cannot establish
behavior hidden behind that mock. For example, asserting one repository write
can show that retry logic issues one write; it cannot prove that a database
uniqueness constraint rejects duplicates when the database is mocked out.

Use qualitative, evidence-backed calibration when exact probability or cost is
unavailable. Consider reachability under supported behavior, consequence,
affected users or data, repetition, relevant lifetime, detectability, recovery,
and reversibility. Compare those with test setup, runtime, flake potential,
maintenance, and the production complexity needed to create the seam. Do not
invent percentages to make the comparison look precise.

## Select the Narrowest Honest Layer

Start close to the decision, then widen only to preserve a real boundary.

For a broader testing or review request, first decide whether a new durable test
is warranted at all. Existing type, compiler, contract, focused manual, or
integration evidence can be sufficient for a trivial low-risk change; record a
material residual risk instead of adding ceremonial coverage. When the user
explicitly requests a test, honor that outcome with the smallest discriminating
evidence and explain if the originally proposed layer would add more machinery
than value.

- **Direct mechanism test:** a calculation, validation, parser, policy, state
  transition, or protocol decision can receive explicit inputs and return an
  observable result. Prefer this after extracting the cohesive mechanism.
- **Component or service integration:** persistence, serialization, routing,
  authorization, transaction, migration, queue, or retry semantics make the
  claim true. Use the repository's local harness and preserve that boundary.
- **Contract test:** an agreed provider or consumer contract needs executable
  evidence. Test the agreed shape and behavior; do not silently redesign the
  contract in a test task.
- **Process or smoke test:** command-line startup, a public binary, environment
  parsing, filesystem behavior, or the thin wiring itself is the claim. Keep
  the case minimal and make live dependencies opt-in.

An in-memory test of a rule and a database-backed test of the same invariant
can both be useful when they protect different failure modes. Do not retain a
slower layer just because it resembles a pyramid, and do not erase a real
boundary behind a mock only because a unit test is easier to write.

## Techniques That Change the Evidence

### Properties

Use a property when a family of inputs should preserve a law, not merely when
random data looks sophisticated. State the generator's domain and oracle:

- round trips preserve a normalized value;
- parsing then rendering never produces an invalid representation;
- an operation is idempotent for a given request identity;
- a state transition keeps balances, ordering, ownership, or uniqueness true.

Bound or seed generated inputs according to repository convention so failures
can be reproduced. Keep the generator valid enough to test the intended law,
but include invalid domains when rejection behavior is the claim. Minimize the
reported counterexample when the available tooling supports it.

### Snapshots

Snapshot only a stable, reviewable contract such as a normalized document,
structured response, diagnostic format, or generated configuration. Normalize
irrelevant timestamps, paths, IDs, ordering, and volatile metadata before
snapshotting. Keep the assertion close enough to explain why a deliberate
update is correct; a large opaque snapshot is not evidence that a reviewer can
judge.

### Replays

Use a recorded exchange, event sequence, message trace, or failure fixture
when order and timing matter but a live dependency is unsuitable. Make the
recording safe to store, explicit about its protocol version and semantics, and
small enough to reveal the behavior under test. A replay should reproduce a
known contract, not become a stale substitute for understanding it.

## Prove the Test Can Fail

When practical, obtain focused negative proof:

- run the test against the pre-fix behavior;
- reproduce the reported regression with its smallest fixture;
- temporarily reverse a branch, condition, validation, retry identity, or
  output mapping that the test is meant to protect; or
- use a small targeted mutation or equivalent demonstration.

For an existing implementation, add the regression test without deleting
sound code. Record the negative proof in the change summary when it is not
obvious from the test alone. If reversal would be unsafe, expensive, or too
disruptive, say so and explain the evidence that remains.

## Verify More Than Green

Run the focused test first so its failure is legible, then the relevant broader
suite. Check that the test has isolated setup and cleanup, deterministic inputs,
and an assertion on the behavior rather than incidental implementation shape.
Report skipped live, credentialed, platform-specific, or timing-sensitive
coverage instead of presenting a local green result as stronger evidence than
it is.
