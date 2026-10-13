# Route: Dependency Research and Updates

Perform dependency updates as engineering work, not as mechanical version bumps:
treat each update as a small migration and delivery unit. The default outcome is
a portfolio of focused, review-ready dependency groups. For each group,
reviewers and automation can see why the versions belong together, what changed
upstream, what local risk was checked, which validation ran, and whether newly
useful capabilities (new APIs, fixed limitations, changed defaults) were adopted
where they improve the local code.

## New Dependency Introduction

Treat a new external dependency as a focused compatibility decision, not as a
repository-wide update portfolio:

1. Establish the missing capability and check whether the repository, platform,
   or an existing direct dependency already provides it adequately.
2. Identify the owning ecosystem, package manager, runtime and framework
   constraints, peer requirements, supported toolchain, and lockfile boundary.
3. Verify the current stable release through registry metadata or an official
   upstream source. Avoid prereleases, release candidates, canaries, and
   nightlies unless the task or existing project explicitly requires them.
4. If compatibility requires an older release, select the highest supported
   stable version and record the concrete constraint rather than guessing from
   remembered version numbers.
5. Add the dependency with the repository's native package tool so the manifest
   and lockfile remain consistent. Do not hand-edit generated lock state.
6. Inspect the complete dependency diff, adapt only the agreed call sites, and
   run checks that exercise installation, types, build, tests, packaging, and
   runtime behavior as applicable.

Do not inventory or update unrelated dependencies unless the user requested
broader maintenance.

## Default Delivery Contract

Full delivery — pushing branches and opening ready-for-review PRs — applies
only when the request includes publishing or PR creation, or when an
orchestrating caller's handoff explicitly grants that delivery authority.
Otherwise stop at local branches plus a delivery proposal: the prepared groups,
their validation status, and the PRs that would be opened. A caller's narrower
delivery authority overrides this default.

When full delivery is authorized for dependency updates without a narrower
scope, execute the complete portfolio:

1. Discover all direct dependency candidates.
2. Group them into coherent PR units.
3. Create one branch or worktree per viable group.
4. Research, update, validate, commit, push, and open a ready-for-review PR for
   each viable group.
5. Put the reviewer-grade explanation in the PR title and body, not primarily in
   the chat response.
6. Defer only groups that are blocked, require human product/security decisions,
   are too risky for the current run, or conflict with already-open PR
   sequencing. Record the reason.

Final chat responses should be operational: list PR links (or prepared local
branches), validation status, deferred groups, and any blockers. Avoid pasting
full PR bodies into chat unless the user asks for them.

## Operating Model

1. **Load repository context first.**
   - Read local instructions such as `AGENTS.md`, `CLAUDE.md`, contribution
     docs, PR templates, CI workflows, package manifests, lockfiles, and release
     notes.
   - Run [the dependency-context helper](../scripts/discover_dependency_context.py)
     when a quick dependency map is useful.
   - Identify package managers, workspaces, generated lockfiles, supported
     runtime versions, and test/build commands before changing versions.
2. **Build an update inventory.**
   - List currently used dependency versions from manifests and lockfiles.
   - Find candidate latest versions using the project's package manager
     commands, registry metadata, or official release sources.
   - Run the repository's available security audit or a source scan such as
     `osv-scanner scan source -r .`; record advisory IDs, severity, affected and
     fixed ranges, and dependency paths before grouping security work.
   - Separate runtime, dev/tooling, test, type, lint, framework,
     adapter/plugin, and transitive-only updates.
3. **Group dependencies by real coupling.** Use the smallest group that
   preserves meaning and compatibility: packages belong together when they
   answer the same reviewer question and share the same validation surface
   (framework core plus adapters, types plus runtime, one vendor SDK surface,
   one test-runner stack, one migration guide). Keep unrelated packages
   separate even when they are individually small or all look like “tooling”, and split a package into its
   own PR when it has a major version change, migration guide, broad API
   surface, runtime behavior changes, security implications, or unclear
   compatibility. The authoritative grouping table, good grouping reasons, and
   split criteria live in [the detailed workflow](dependency-workflow.md).
4. **Plan the PR portfolio before editing, then execute it.**
   - Produce one row per proposed PR group with package names, old/new versions,
     grouping reason, risk, validation surface, and worktree/branch name
     (portfolio table format in [the detailed workflow](dependency-workflow.md)).
   - Do not finish at the portfolio table when the user asked for dependency
     updates. Use the table as the execution plan for the groups.
5. **Research upstream changes before editing code.**
   - Read changelogs, release notes, migration guides, GitHub releases, compare
     views, and issue links for the exact old-to-new version range.
   - Prefer primary sources. If release notes are incomplete, inspect git tags,
     commits, package diff, type definitions, docs, and tests.
   - Capture gaps explicitly instead of pretending the upstream history is
     complete.
6. **Assess local impact.**
   - Search the codebase for imported APIs, config keys, CLI usage, environment
     variables, generated code, peer dependency assumptions, and documented
     workarounds tied to the packages.
   - Classify each upstream change as `irrelevant`,
     `covered-by-existing-usage`, `requires-local-change`,
     `enables-local-improvement`, or `needs-human-decision`.
   - Update local code when the new version provides a clearly better API, fixes
     a workaround, removes a local shim, improves types, closes a bug, or
     changes recommended configuration.
7. **Implement, validate, and deliver one PR group at a time.**
   - Update manifests and lockfiles with the package manager that owns them.
   - Make local code migrations in the same PR only when they directly benefit
     from or are required by the grouped dependency update.
   - Run the repository's narrow checks first, then broader suites that match
     the changed dependency surface. If a check cannot be run, record the reason
     and the most relevant substitute validation.
   - Use Conventional Commits unless the repository has its own convention.
   - Complete one group to the authorized delivery point (local branch, or
     committed-pushed-published PR) before moving to the next unrelated group.
     The authoritative branch, commit, publishing, and PR-body rules live in
     [the detailed workflow](dependency-workflow.md).

## Multi-PR Worktree Orchestration

Use worktrees when the user asks for multiple dependency PRs, when several
groups can proceed independently, when the default dependency portfolio contains
more than one viable group, or when the repo has a branch guard that blocks
edits on the main branch.

1. Read [worktree safety](worktree-safety.md). Inspect the canonical repository,
   registered worktrees, refs, proposed absolute paths, and dirty and staged
   state before choosing a location.
2. Reuse a clean suitable harness-managed worktree without cleanup ownership,
   or start from a clean refreshed base and create one collision-free worktree
   per proposed PR group.
3. Record the repository, absolute root, expected branch/commit, base, group,
   checkout class, and cleanup ownership in run context. Re-verify it before the
   first write and after resume or handoff; use an explicit working directory
   for every command.
4. Apply only that group's manifest, lockfile, generated output, migrations, and
   local adoption changes in that worktree.
5. Run validation matching that group's surface. Prefer narrow checks first,
   then the repo's broad quality gate when the group affects shared tooling or
   lockfiles.
6. Stage explicit group files, inspect staged names and diff, then complete the
   group to the authorized delivery point before starting the next unrelated
   group.
7. Automatically clean up only a matching clean worktree created by this run.
   Leave foreign, harness-managed, dirty, moved, or mismatched worktrees intact.
8. Record deferred groups and reasons, especially major upgrades split out
   because they need migration research or human decisions.

When a shared lockfile makes multiple worktrees conflict, keep the PR group
boundaries anyway. Rebase each worktree on the latest default branch after the
prior dependency PR lands, or regenerate the lockfile in the active PR group and
document that it intentionally contains only that group's dependency story. Own
the lockfile only when the current group's package-manager command produced a
coherent diff; never absorb foreign staged changes or hand-delete unrelated
entries.

## Source Research Requirements

For each grouped update, collect enough evidence to answer these questions:

- What exact version range is changing?
- Which upstream changes can affect this repository's runtime behavior,
  generated output, public API, build/test pipeline, or deployment?
- Which changes are irrelevant because the project does not use that feature?
- Which migration notes, deprecations, peer dependency changes, or changed
  defaults require local action?
- Which new fixes or features make an existing local workaround unnecessary?
- Where are the gaps in upstream documentation or changelogs?

Use [ecosystem notes](ecosystem-notes.md) for the non-obvious ecosystem-specific
commands and checks.

## Local Code Adoption

Prefer adopting new dependency capabilities when the improvement is directly
supported by the update research and local usage evidence.

Good adoption candidates:

- Replace local compatibility code after the upstream package gained
  first-class support.
- Remove comments or workarounds tied to a bug fixed in the new version.
- Use improved types, safer options, or stricter defaults when they reduce local
  risk.
- Update configuration to recommended names or defaults before old forms become
  deprecated.
- Simplify code paths made unnecessary by new APIs.

Avoid opportunistic refactors that are merely adjacent. If an improvement is
appealing but not clearly part of the dependency update, mention it as a
follow-up rather than expanding the PR.

## PR Bodies and Writing Style

The PR body is the review artifact: it must explain the group, old and new
versions, the upstream changes that matter locally, required migrations and
beneficial adoption, validation results, and remaining risk. Write for a busy
reviewer, translate upstream changes into local consequences, and avoid vague
modernization claims and AI-sounding filler. The authoritative PR-body template,
review-package checklist, and writing-quality guidance live in
[the detailed workflow](dependency-workflow.md).

## Cross-links

- Migrations dominated by mechanical repository-wide translation — a language,
  runtime, framework, or platform port with its own parity evidence — are the
  Porting route. A version bump plus scoped local adaptation stays here, even
  for a major upgrade with migration work.
- Review and upkeep of the resulting pull requests are the Review route.
- Repository-wide modernization that is not dependency work is the Audit route.
- Discovery and execution of established repository checks is the Validation
  route; this route owns dependency-specific compatibility research and its
  validation scope.
- Durable dependency or platform choices are recorded through
  `effective-product` when the rationale must survive the update.
