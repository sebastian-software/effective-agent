# Route: Pull Request Review and Upkeep

Review the submitted change, help its author move forward, and carry authorized
follow-up work through verification and the requested handoff.

## Outcome and Authority

A review-only request authorizes inspection and findings. Return the review to
the user unless publishing it to the named PR is already authorized. A request
to fix findings authorizes implementation and relevant checks; commit, push,
reply, approve, request changes, merge, or deploy only within the authority and
target established by the whole conversation or calling workflow. Skill
selection, PR authorship, and a mode label do not grant that authority.

Honor earlier authorization without asking again. When one external action is
not authorized, complete the review or other authorized work and return the
prepared result. Ask only for a consequential missing decision or permission
needed to fulfill the request.

## Select the Work

| Requested outcome | Read |
| --- | --- |
| **Mode A:** review someone else's PR, including a complete caller-supplied PR | [Review judgment](review-judgment.md) |
| **Mode B:** maintain a PR, resolve feedback, repair CI, or update its branch | [Review upkeep](review-upkeep.md); add judgment for unresolved findings |
| **Mode C:** classify caller-supplied review items while the caller retains all execution | [Mode C contract](mode-c-contract.md), which defines the exact handoff schema and prohibits repository/provider discovery |

Load only the selected mode and references needed for the current decision.
For live PR access or a caller-owned full review result, use
[Review provider access](route-review-access.md). Mode C needs no live adapter.

When someone asks to understand a substantial change, use [Explain a Change to
a Human](review-judgment.md#explain-a-change-to-a-human). That request alone
does not call for a PR decision.

## Establish Scope

Use the current repository unless the user names specific PRs. Operate on the
named targets; discover a review queue only when selection is delegated.
Resolve identity once from caller input or the selected adapter. An app or bot
delivery actor does not require a logged-in human identity.

For live reviews and upkeep, inspect the current PR delta, relevant comments,
previous review state, CI, and mergeability. Read a linked ticket when it
clarifies intent or acceptance criteria. If it is absent or inaccessible, use
the description, diff, and other authoritative context. Continue independent
technical review; identify the specific judgment that missing context prevents.
A repository's ticket-link requirement can remain an unresolved process
condition without stopping code inspection. Do not invent that requirement
from a preference. If nothing changed since the last review and there is no new
evidence or request to reassess, report that briefly instead of repeating work.

## Dry Run

For `--dry-run`, "trockenlauf", or "don't post anything", inspect the same
evidence but make no outward provider changes: no review, approval, comment,
reply, push, or PR close/reopen. Return the concrete proposed decision, comment
text and anchors, or CI action as applicable. Prepare a local fix or throwaway
diff only when the request includes that preparation; a review alone does not
authorize implementation. Report any local changes honestly.

## Verification

Use [review verification](review-verification.md) when behavior needs execution
or rendered evidence. A safe local preview is an option when no deployment
exists. Choose checks from the changed contract and stop repeating them when
the evidence is sufficient. Missing tools or evidence must not become a claim
that a behavior was verified.

Before adopting, creating, or writing in a worktree, apply
[worktree safety](worktree-safety.md). Preserve unrelated changes and never
force-push without the required authority and `--force-with-lease` protection.

## Voice

Match repository language and communication conventions. Make blocking impact
and optional suggestions distinguishable; write compact, concrete comments.
Use [PR review voice](review-voice.md) only when wording or placement needs
calibration. Its examples and a separate writing skill are optional aids, not
prerequisites for an ordinary comment.

## Handoff

Lead with the outcome and decisive evidence in the user's language. Distinguish
a recommendation from a review actually published, local edits from pushed
changes, and completed checks from gaps. Name what remains blocked and why.
Record durable architectural decisions through `effective-product` only when
the rationale needs to outlive the PR.
