---
name: effective-delivery
description: >-
  Audit, diagnose, and deliver repository changes: plans, ports, PR reviews,
  issue queues, dependencies, existing checks, technical documentation, and
  engineering leadership. Use for repository lifecycle work; system design
  belongs to effective-engineering, browser implementation to effective-web.
---

# Effective Delivery

Choose the route that matches the requested repository outcome. Load its
references only for the decisions at hand; routine edits do not need a full
repository survey.

Carry authorized implementation through relevant checks and the requested
handoff. An audit-only or diagnosis-only request stays read-only; a combined
audit-and-fix request already authorizes the fix. Ask only for a consequential
missing decision or authority not already granted.

Preserve unrelated work, discover repository-native commands, and report
material evidence gaps. Rank findings by demonstrated impact and remedy cost;
a clean audit is a valid result. Keep scrutiny high at security, privacy, money,
data-loss, and irreversible boundaries. Never expose secret values.

## Route by Intent

| User intent | Read |
| --- | --- |
| Coordinate multi-stage or mixed-domain work from an unclear request to a review-ready handoff | [Workflow Orchestration](references/route-orchestration.md) |
| Audit a repository, explain a defect or surprising behavior, prioritize improvements, simplify code, or create, review, or reconcile delivery specifications, work packages, or implementation plans | [Codebase Audit and Plans](references/route-audit.md) |
| Plan or execute a behavior-preserving port across languages, runtimes, frameworks, platforms, storage engines, or major APIs | [Behavior-Preserving Ports](references/route-porting.md) |
| Review a pull request, act on review feedback, fix findings, recover CI, or keep a branch current | [PR Review and Upkeep](references/route-review.md) |
| Select a provider adapter, use the GitHub CLI recipes, or return a caller-owned review handoff | [Review Provider Access](references/route-review-access.md) |
| Discover, rank, process, reconcile, or monitor an unspecified live issue queue when the user delegates target selection | [Issue Queue Autopilot](references/route-issue-autopilot.md) |
| Add, choose, update, or group external dependencies; assess changelog impact; create dependency PRs | [Dependency Updates](references/route-dependencies.md) |
| Discover and run the repository's established typecheck, lint, format, test, build, benchmark, or documentation checks and report the evidence | [Repository Validation](references/route-validation.md) |
| Write or verify READMEs, guides, API and CLI references, migration notes, JSDoc, TSDoc, rustdoc, examples, or controlled-language documentation | [Technical Documentation](references/route-docs.md) |
| Resolve unclear ownership, overloaded leaders, weak one-to-ones, coordination drag, decision stalls, or a proposed reorganization | [Engineering Leadership](references/route-leadership.md) |

Any route that creates, adopts, writes in, integrates from, or removes a Git
worktree uses the shared [worktree safety](references/worktree-safety.md) contract.

## Routing Boundaries

- `effective-engineering`: system and data contracts, Rust and server/shared
  TypeScript depth, focused non-frontend test design, and benchmark methodology.
- `effective-web`: browser design, implementation, frontend diagnosis and tests,
  annotated screenshots of rendered changes, interface copy, and web compliance.
- `effective-product`: product direction, research, scope, and durable decisions
  recorded as ADRs.
- `effective-writing`: editorial prose, natural team English, and locale
  typography. Repository-derived or controlled-language documentation stays here.
- `effective-marketing`: positioning and commercial copy, including the
  marketing portions of a README.

A named issue, PR, URL, or finite issue list is targeted work. Select an open
backlog only when queue selection is delegated. Do not invent repository policy,
delivery authority, private plan stores, or organizational evidence. Seek
qualified support when People/HR, employment-law, health, security, or crisis
judgment exceeds the available competence.
