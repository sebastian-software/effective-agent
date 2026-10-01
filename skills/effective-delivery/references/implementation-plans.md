# Implementation Plans

Use this reference to create, review, save, or reconcile plans that another
human or agent can execute without relying on the planning conversation.

## Contents

- [Plan Ownership](#plan-ownership)
- [Synthesize Settled Requirements](#synthesize-settled-requirements)
- [Plan Contract](#plan-contract)
- [Work Packages and Dependencies](#work-packages-and-dependencies)
- [Wide Migration Sequences](#wide-migration-sequences)
- [Drift and Working State](#drift-and-working-state)
- [Plan Template](#plan-template)
- [Review and Reconciliation](#review-and-reconciliation)

## Plan Ownership

Discover the repository's existing planning surface before writing:

- Use the established issue tracker when delivery work already lives there.
- Use an existing `docs/plans/`, `plans/`, roadmap, RFC, or project convention
  when present.
- Use an ADR only for the durable decision and rationale, never as a task-status
  ledger.
- Return the plan in chat when the user did not ask to persist it.

When the user asks to save a plan and no convention exists, use plain Markdown
under `docs/plans/`. Add an index only when several plans require dependency or
status tracking. Do not introduce a hidden directory or tool-specific schema.

## Synthesize Settled Requirements

When asked to turn a discussion or approved brief into a delivery specification,
reuse the decisions already made and the project's terminology. Capture the
problem, intended behavior, accepted constraints, non-goals, and observable
acceptance criteria. Link the authoritative brief or ADR when one exists.

Separate agreed requirements from assumptions and unresolved choices. Ask only
about missing decisions that change the outcome, scope, contract, or safety;
mark affected work blocked while keeping independent work executable. A minor
open detail does not justify repeating discovery or holding the whole plan.

Keep the feature contract understandable without speculative file names or an
exhaustive story list. Add verified paths and symbols when the artifact becomes
an execution plan and they help the executor locate the change. Product
direction belongs to `effective-product`; unresolved system or data contracts
belong to `effective-engineering`.

## Plan Contract

A useful plan is:

- **Self-contained:** include intent, current evidence, relevant decisions,
  exact paths and symbols, and repository conventions needed for judgment.
- **Scoped:** name files or areas in scope and tempting adjacent work that is
  explicitly out of scope.
- **Ordered:** make prerequisites and safe migration order visible.
- **Verifiable:** pair each step with an actual repository command and expected
  result where feasible.
- **Drift-aware:** record the code state used for planning and explain how to
  detect invalidated assumptions before execution.
- **Bounded under uncertainty:** add specific stop conditions where improvising
  would materially change risk, behavior, public API, data, or scope.
- **Maintainable:** identify the enduring contract and what reviewers should
  scrutinize after the immediate change.

Do not assume the executor is cheaper, less capable, or a subagent. Write for a
competent collaborator who lacks the planning session's hidden context.

## Work Packages and Dependencies

For feature work, prefer bounded packages that deliver a complete observable
behavior across the affected layers. Include only the layers the behavior
actually needs. For example, "a member can revoke an invitation and the revoked
link is rejected" is an outcome with its own proof; separate database, API, and
interface tickets may leave no usable behavior until all three are finished.

For each package, state:

- the behavior or invariant it delivers;
- the acceptance evidence that proves that outcome;
- the prerequisites that genuinely prevent it from starting, or none.

Use the repository's existing issue identifiers and dependency relationships
when publishing is requested and authorized. For a plan returned in chat or
Markdown, short package names or numbers are enough. Drafting a breakdown does
not authorize issue creation, new labels, or a new tracker scheme.

A blocker is a required decision, contract, capability, or migration state,
not merely an earlier item in the list. Independent packages remain eligible
to start when their own prerequisites are met. Remove accidental ordering
edges; resolve cycles by exposing the missing shared prerequisite or keeping
inseparable work in one package. Keep each package small enough for coherent
implementation, review, and decisive verification rather than targeting a
fixed file count or context-window size.

Make preparation a separate prerequisite only when it enables the named change.
Use [Legacy change strategy](legacy-change-strategy.md) for consequential work
in weakly tested code; unrelated cleanup is not a prerequisite.

## Wide Migration Sequences

An interface or representation change can affect too many callers for a feature
slice to remain valid on its own. When old and new forms can coexist safely,
plan a compatibility sequence:

1. **Expand:** introduce the new form while preserving the accepted old
   contract. Name the evidence that both forms work during coexistence.
2. **Migrate:** move coherent caller groups onto the new form. Each batch
   depends on expansion, plus any real prerequisite, and proves its behavior
   while remaining compatible with callers still on the old form.
3. **Contract:** remove the old form after every required migration batch and
   evidence that consumers no longer rely on it. Include external consumers,
   rollout windows, and recovery obligations when they are part of the contract;
   a repository search or green tests alone do not establish their migration.

List unresolved compatibility, data conversion, or recovery decisions in the
plan with `effective-engineering` as the decision owner, the affected stages,
and the evidence needed to settle them. Label candidate rules as proposals;
dependent stages are not release-ready until their contract is settled. Do not
invent dual writes or a compatibility promise merely to make the ticket graph
fit.

If intermediate batches cannot be safely verified independently, keep the
coupled work in one integration unit and name its final proof point. Do not
claim that each partial ticket is independently releasable or green. The plan
must make clear where compatibility is established and when removal is safe.

## Drift and Working State

For a Git repository, record the short HEAD SHA and planning date. Check whether
in-scope files have uncommitted changes; do not describe HEAD as the complete
current state when the plan was based on a dirty worktree.

At execution time:

1. Compare current in-scope files with the recorded state.
2. Re-read excerpts and assumptions when those files changed.
3. Continue when changes are compatible and the plan still describes reality.
4. Stop or revise the plan when public contracts, chosen architecture, required
   scope, or verification commands no longer match.

Drift detection protects intent; it should not reject harmless line movement or
force a new plan for every unrelated commit.

## Plan Template

Adapt this to the project's format rather than copying empty sections.

```md
# <Outcome-oriented plan title>

## Status

- Priority: P1 / P2 / P3
- Effort: S / M / L
- Risk: LOW / MEDIUM / HIGH
- Depends on: <items or none>
- Planned at: <short SHA>, <date>
- Working state: <clean or relevant uncommitted paths>

## Why this matters

Describe the verified problem, concrete cost, intended outcome, and relevant
ADR or product constraint.

## Current state

- `path/file.ext:line`: role and verified behavior
- Existing convention to follow, with a representative location
- Relevant decision, interface, data, or compatibility constraint

## Scope

In scope:
- Exact files, packages, public contracts, or behaviors

Out of scope:
- Adjacent work that must not be folded into this change

## Verification commands

| Purpose | Command | Expected result |
| --- | --- | --- |
| Focused tests | `<real command>` | exit 0 and named cases pass |
| Type or build check | `<real command>` | exit 0 |

## Steps

### 1. <Safe first outcome>

Blocked by: <actual prerequisites or none>

Describe exact files, symbols, behavior, migration order, and test additions.

Verify: `<command>` -> <expected result>

### 2. <Next outcome>

Blocked by: <actual prerequisites or none>

Continue with the smallest independently verifiable step.

## Done criteria

- [ ] Observable behavior or invariant
- [ ] Named regression cases pass
- [ ] Required repository checks pass
- [ ] No unintended scope changes
- [ ] Related decision, issue, docs, or generated artifacts are consistent

## Stop conditions

- Stop when a named assumption is false.
- Stop when the change requires a public API, schema, security boundary, or
  out-of-scope file not covered by the plan.
- Stop when the verification baseline is already failing in a way that prevents
  attributing results to this work.

## Maintenance and review focus

Name future interactions, deliberately deferred work, and the riskiest review
questions.
```

Use excerpts only when they anchor a fragile contract or help detect drift. Do
not duplicate large source files inside the plan.

## Review and Reconciliation

When reviewing a plan, check:

- Does the current code still contain the claimed problem?
- Does the plan respect accepted ADRs and project terminology?
- Are scope and exclusions sufficient to prevent attractive side quests?
- Do work packages have their own completion evidence and only genuine blockers?
- Can migration stages coexist safely, and is old-form removal gated by actual
  consumer migration and any rollout or recovery obligations?
- Do commands exist, run from the stated directory, and test the intended
  behavior rather than merely exit successfully?
- Do new tests prove the regression and meaningful edge cases?
- Are stop conditions specific to actual uncertainty?
- Are secrets omitted and external requirements current?
- Do requirement, approach, steps, done criteria, and verification describe
  the same change? A deferred decision cannot appear elsewhere in the plan as
  the chosen approach; the steps that depend on it are blocked, not ready.

A dirty worktree, a newer ADR, or a renamed check usually invalidates one claim
or step, not the plan's objective. A plan is executable when its open decisions
no longer affect the remaining steps and each step's proof actually runs.

When reconciling a backlog:

- **Done:** verify cheap, decisive criteria and link the implementation.
- **Blocked:** investigate the blocker; revise, split, or reject the plan.
- **In progress:** confirm ownership and current branch or worktree state.
- **Todo:** rerun drift checks and verify the finding still exists.
- **Superseded or duplicate:** preserve a short rationale and point to the
  successor.
- **No longer valuable:** reject explicitly instead of leaving permanent stale
  work.

Finish with the next executable item and its prerequisites. Do not confuse a
large backlog with progress.
