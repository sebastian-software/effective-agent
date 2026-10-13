# Route: Issue Queue Autopilot

Operate a live issue queue without merging. Keep the parent agent responsible for
triage, coordination, and state reconciliation; delegate each implementation to one
separate agent in one fresh worktree.

## Activation gate

Apply this gate before choosing a mode, querying a tracker, reconciling PRs, or
changing repository state. Activate this route only when at least one condition is
true:

- The user delegates target selection from a live set of issues. Repository,
  project, assignee, label, state, or priority constraints may narrow the set, but
  more than one possible target must remain for this route to discover or rank.
- The user requests an ongoing queue or monitor for new, reopened, or changing
  issues without naming the implementation target.
- The current request continues a queue, issue, branch, or PR that this autopilot
  demonstrably claimed in an earlier run. A specific identifier is expected during
  such a continuation; it does not create ownership retroactively.

Treat the request as targeted, and therefore outside this route, when it identifies
the work through an issue or PR number, tracker key, URL, exact title, attached
issue, or finite enumerated list. Phrases such as “this issue,” “fix issue #123,”
“implement LIN-42,” “review PR #9,” and “fix #123 and #124” are targeted requests.
The mere word “issue,” including its plural, is never sufficient to activate
this route.

For a targeted request:

1. Stop applying this route's queue workflow. Do not inspect the broader backlog,
   rank or claim other work, reconcile unrelated PRs, create a monitor, or introduce
   this route's worktree and ready-state conventions.
2. Route a named software change through Workflow Orchestration and standalone PR
   maintenance through PR Review and Upkeep, plus only the domain disciplines the
   target requires.
Do not infer authorization for autopilot from nearby conversation about issues,
from an open issue page, or from repository state. Selection must be delegated in
the current request or inherited from a demonstrable active autopilot run.

## Choose the operating mode

- **Triage:** Discover and rank an unspecified issue set only. Do not assign, edit,
  comment, branch, or create a PR.
- **Run:** Reconcile owned PRs, then process the highest-ranked actionable issue.
  Use this as the default only after the activation gate passes and the user asks
  to take the next issue or work through a backlog or queue.
- **Monitor:** Repeat run cycles for incoming issues and PR state changes. Use the
  environment's automation/recurring-monitor mechanism when available. Create or
  update one non-overlapping automation; do not claim persistent monitoring unless
  it exists. Default to a 15-minute cadence unless the user or repository specifies
  another cadence.

A run/monitor request explicitly authorizes pushing issue branches, opening the
resulting PRs, and making those PRs non-draft for CI/review bots. It does not
authorize merging, changing production data, or broadening an issue's scope.

## Keep current work prominent

Read [issue-progress-updates.md](issue-progress-updates.md) before the
first interactive action. Keep the parent orchestrator responsible for concise,
evidence-based updates even while a separate agent implements.

## Establish repository rules

1. Read the repository instructions and project overview before querying or
   mutating anything. Load all skills and architecture records required by those
   instructions and by the selected issue.
2. Inspect remotes, the current authenticated identities, default branch, worktree
   state, PR conventions, labels, and required checks.
3. Select the authoritative tracker in this order:
   - explicit repository instructions;
   - explicit user direction;
   - established issue links/project metadata in recent PRs;
   - GitHub Issues when the repository clearly uses them and no Linear project is
     authoritative.
4. When both GitHub and Linear contain the same work, deduplicate by links and
   identifiers. Update status only in the authoritative tracker unless repository
   convention requires synchronized updates.
5. Use the repository's mandated Linear project when one is documented.

Prefer installed GitHub/Linear integrations; use authenticated repository CLIs only
when an integration is unavailable. Never guess issue, project, repository, or
account identity.

## Write collaboration text with Metro English

Load `effective-writing` and take its Metro English route, when available, before posting
team-facing GitHub or Linear text.
Use it for:

- PR descriptions, summaries, and handoff notes;
- issue comments for reproduction, ownership, progress, completion, or blockers;
- replies explaining completed fixes or follow-up changes;
- responses to PR review, CI, and review-bot findings;
- concise ready-state and async status updates.

Finalize the technical substance first, then make the language sound like a direct,
natural US teammate. Preserve facts, severity, decisions, links, required PR
templates, preview lines, architecture sections, and repository terminology.
Repository house style and mandated title/commit/documentation formats take
precedence. Use English for these collaboration artifacts unless the user or
repository explicitly requires another language.

Include the `effective-writing` Metro English route in every implementation or
repair agent's assignment so the agent applies it before posting, rather than
leaving the language pass to the orchestrator after publication.

## Reconcile active work before selecting an issue

At the start of every run and monitor wakeup:

1. Refresh every open PR previously created or maintained by this queue.
2. Remove `ready-to-merge` immediately when the invariant in
   [issue-ready-state.md](issue-ready-state.md) is false.
3. Route actionable CI failures or substantive new review/issue feedback back to
   the agent owning that PR's worktree. If the original agent is unavailable,
   launch one repair agent in the same worktree.
4. Commit and push narrow, branch-related fixes; rerun relevant local checks and
   refresh remote checks/reviews.
5. Restore `ready-to-merge` only after the invariant is true again.

Do not start a new issue while an owned PR has an actionable branch-local problem.
External infrastructure failures and product decisions may be documented as
blocked; once safely parked, continue with the next actionable issue.

## Build the live queue

Fetch open and reopened issues from the authoritative tracker immediately before
each selection. Include title, description, labels, project/team, priority,
creation/update time, all assignees, status, dependencies, comments, linked PRs,
and URL.

Apply the ownership gate before scoring:

1. Build the primary pool from issues where the current authenticated user is among
   the assignees and issues that are effectively unassigned.
2. Treat an issue as effectively unassigned when it has no human assignee and no
   active implementation owner, branch, linked PR, agent, or repository-specific
   in-progress signal. On GitHub, the reporter, commenters, code owners, or a bot
   assignee alone do not prove active human ownership; verify the live work signals.
3. Exclude issues assigned only to another active human, even when their score would
   be higher. Include them only after an explicit user handoff/direction or an
   unambiguous repository ownership rule permits takeover.
4. Rank self-assigned and effectively unassigned issues together by the normal
   relevance/urgency rubric. If neither category contains an actionable issue,
   report the queue as idle instead of silently taking another person's work.

Exclude:

- done, canceled, duplicate, invalid, or explicitly deferred work;
- issues with an active implementation owner or linked open implementation PR,
  unless this queue owns that work;
- issues that require a product/security/legal decision before safe implementation;
- issues outside the selected repository or project.

For every remaining issue, assess `impact`, `urgency`, and repository `relevance`
from 0–5. Normalize the result as described in
[issue-ranking.md](issue-ranking.md), then run:

```bash
python3 <skill-dir>/scripts/rank_issues.py issues.json --format markdown
```

Honor explicit human priorities first. Otherwise select the first actionable item
from the ranked result. Recency is a meaningful boost, not an override: a new
cosmetic request must not outrank an older outage, security defect, data-loss risk,
or customer blocker.

Show a compact grouped queue when starting, when ordering materially changes, or
when the user asks. Follow the progress-update contract for the selected item.
Avoid noisy reports for unchanged monitor cycles.

## Claim exactly one issue

Re-read the selected issue immediately before mutation. Confirm it remains open,
inside the primary ownership pool, relevant, and free of a newly linked
implementation PR.

Read [worktree-safety.md](worktree-safety.md) before creating,
adopting, resuming, writing in, delivering from, or cleaning up a worktree.

1. Apply the repository's existing ownership/in-progress convention. Do not invent
   a new status scheme when one already exists.
2. Record a concise implementation intent on the issue only when repository
   practice expects it.
3. Fetch the latest default branch.
4. Create a fresh worktree and feature branch from that base using the
   environment-native worktree mechanism. Otherwise use an explicit safe worktree
   path and a branch such as `<prefix>/<issue-id>-<short-slug>`, using the repository's or harness's branch prefix.
5. Never implement in the orchestration checkout. Never reuse a worktree from a
   different issue or touch unrelated dirty changes.
6. Keep the worktree until the PR is terminal or repository tooling safely cleans
   it. Never force-remove a dirty or unpushed worktree.

If the branch or worktree already exists, verify provenance and resume it only when
it belongs to the same issue and no other agent is active there.

## Delegate implementation

Launch one separate implementation agent with the absolute worktree path and only
the context it needs:

- issue identifier, authoritative URL, full current description, acceptance
  criteria, and relevant discussion;
- repository instructions and required domain skills/architecture records;
- branch/worktree path and the explicit prohibition on unrelated changes;
- required TDD, validation, documentation, and PR/finalization workflow;
- an explicit instruction to load `effective-writing` and its Metro English route
  for PR descriptions, issue
  comments, review replies, fix confirmations, and handoff notes;
- permission to push and make this issue's PR non-draft, but not to merge;
- a definition of done matching the ready-state invariant.

The implementation agent must:

1. Reproduce or verify the issue before changing code. If it is invalid,
   duplicate, already fixed, or materially underspecified, return evidence instead
   of guessing.
2. Write a failing behavioral test first when it protects real behavior; follow
   repository-approved reasons for skipping low-value tests and document the skip.
3. Make the smallest complete change that satisfies the issue and repository
   architecture/security rules.
4. Run focused tests first, then all proportionate repository checks.
5. Update required docs and work logs. Link the PR to the issue using native closing
   syntax for GitHub or the authoritative Linear identifier/link.
6. Commit with repository conventions, push, and use the repository's required
   finalization workflow.
7. Move the PR out of draft to trigger full CI/review-bot coverage. In repositories
   with explicit ready-finalize modes, use that mode because a run/monitor
   invocation is the user's explicit authorization for this queue's PR.
8. Resolve actionable CI and review-bot findings, pushing each narrow fix and
   rechecking the latest head.

Do not close the issue before merge unless the repository's workflow explicitly
does so. Do not merge the PR.

## Mark and maintain readiness

Use `ready-to-merge` as a reversible machine-readable flag on the implementation PR.
Prefer an existing equivalent only when repository conventions define one. If no
equivalent exists, create the exact label with a clear description when mutation
mode and permissions allow.

Read [issue-ready-state.md](issue-ready-state.md) before adding or
removing the flag. Re-read the latest head, checks, review threads, conflicts, and
linked issue activity immediately before each transition.

After adding the flag, update the authoritative issue to its existing review/ready
state when applicable and post at most one concise completion note with the PR
link. A later push, red CI result, conflict, or substantive new problem removes the
flag until the invariant is restored.

## Monitor safely

Read [issue-monitoring.md](issue-monitoring.md) before creating or waking
a monitor. Reconcile queue-owned work before every selection and prevent
overlapping implementations.

## Completion report

Report:

- authoritative tracker and project;
- grouped ranking and selected issue;
- agent/worktree/branch;
- tests and validation performed;
- issue and PR links;
- current CI/review status;
- whether `ready-to-merge` is present and why;
- blockers or the next queued issue;
- monitor automation status when applicable.

Never report “ready to merge” merely because code was pushed or CI once passed.

## Routing Boundaries

Use Workflow Orchestration for a newly named software change and PR Review and
Upkeep for a standalone named PR. This route owns only
delegated queue selection, queue-owned implementation coordination, and ongoing
queue reconciliation; it does not merge PRs or absorb targeted work.
