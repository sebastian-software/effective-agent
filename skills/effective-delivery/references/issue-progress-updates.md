# Progress updates

Make the current target and its importance visible throughout every interactive
run. Before the first action, and whenever the target or stage materially changes,
post a compact progress block in the user's language:

```markdown
### Now: <issue/PR ID> — <short title>
Stage: <triage | claiming | reproducing | implementing | validating | finalizing | CI/reviews | ready | blocked>
What: <one sentence describing the behavior, defect, or change>
Why this matters now: <one concrete sentence based on impact, urgency, risk, blocking value, feedback, or recency>
```

Link the issue or PR in the heading when possible. Add the implementation agent,
worktree, or branch only when it helps the user locate the work.

Derive “Why this matters now” from live evidence: ranking reasons, customer/user
impact, security or data risk, work it unblocks, a failing required check, or new
substantive feedback. When recency changes the order, say that plainly. Do not use
vague filler such as “high priority” without the reason.

Update the block when:

- queue reconciliation selects or preempts a target;
- ownership is claimed and an implementation/repair agent starts;
- work moves between reproduction, implementation, validation, finalization, and
  CI/review;
- a new CI/review problem changes the plan;
- the target becomes ready or blocked;
- the user asks for status.

If a long stage has no result yet, state what is still running or awaited
without inventing progress. Keep unchanged background
monitor wakeups quiet; emit the block when work starts or state materially changes.
