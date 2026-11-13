# Route: Worktree Cleanup

Inventory the linked Git worktrees below a folder and remove the ones that are
provably finished. This is the user-requested cleanup that
[Worktree safety](worktree-safety.md) reserves for separate authority: most of
the worktrees found here were created by other runs, sessions, or people.

## Core Contract

- A request to list or size worktrees is read-only. A request to clean up,
  delete, or reclaim space authorizes removing the `done` and `missing` classes
  below, and nothing else.
- Let [the worktree cleanup helper](../scripts/worktree_cleanup.py) decide and
  act. It rechecks every worktree immediately before removal and has no option
  to remove a `dirty` or `busy` one. Do not reach around it with
  `git worktree remove --force` or `rm -rf`.
- Removal must lose nothing: no uncommitted file, no commit that only the
  removed branch held, no unique ignored file the user has not been told about.

## Classes

| Class | Meaning | Action |
| --- | --- | --- |
| `done` | Clean, idle, and every commit is already in the base branch | Remove the worktree and delete its local branch |
| `unmerged` | Clean and idle, but the branch has commits the base branch lacks | Only on request: remove the worktree, keep the branch |
| `dirty` | Uncommitted or untracked changes, an operation in progress, or local work in a submodule | Never removed |
| `busy` | A process works in it, it is locked, protected, active within `--min-idle-hours`, or unreadable | Never removed |
| `missing` | Registered, but the folder is gone | `git worktree prune` |

The base is the repository's default branch, on `origin` and locally. A branch
counts as contained when it is an ancestor, when `git cherry` finds the same
patches, when merging it would not change the base (this covers squash merges),
or when the provider reports a merged pull request whose head is exactly the
local tip.

## Workflow

1. **Protect work in progress.** The worktree the agent runs in and every
   worktree that is some process's working directory are `busy` automatically.
   An idle session has no process to detect: when the host can list sessions,
   pass the working folder of each running or recently active one as
   `--protect <path>`. When it cannot, add `--min-idle-hours <N>` to the scan
   so a worktree with Git activity in the last N hours counts as `busy`.
2. **Scan.** From the directory that holds this skill:
   ```sh
   python3 scripts/worktree_cleanup.py scan --root <folder> --out <report.json>
   ```
   Use the folder the user named; the default is the current directory. The scan
   fetches `origin` for each repository that has linked worktrees and measures
   sizes. Offline, add `--no-fetch --no-gh`. Write the report to a scratch
   location, not into a repository.
3. **Report.** Give the count and size per class, then each repository. Name
   every `unmerged`, `dirty`, and `busy` worktree with its reason. For
   `unmerged`, say whether the branch is pushed and how many of its commit
   subjects already exist on the base. Call out `ignored files only here`: those
   ignored files do not exist in the main checkout (a local `.env`, for example)
   and disappear with the worktree.
4. **Remove.** Preview with `--dry-run` when more than one repository is
   affected, then:
   ```sh
   python3 scripts/worktree_cleanup.py remove --report <report.json> --classes done,missing
   ```
   Add `--include <path>` only for a worktree the user named or approved: an
   `unmerged` one, whose branch then stays, or a `done` one with ignored files
   found nowhere else.
5. **Verify.** Read every `removed`, `skip`, and `FAILED` line. Report what was
   removed, what stayed and why, and the freed space. Pass on the `restore:`
   command printed for each deleted branch; the same data is in the removal
   record next to the report.

## Boundaries of the Helper

- **Recheck.** A worktree whose class or tip changed since the scan is skipped.
  Scan again; do not work around the skip.
- **Locks.** Some harnesses lock the worktrees of their agents with the process
  ID of the creating session. A lock whose process has ended is stale. A lock
  held by the calling session is reported as `locked by the calling session`;
  pass `--own-locks-finished` only when no subagent or background task of this
  session is still running. Locks of other running processes and locks set by
  hand are respected.
- **Force.** Git refuses to remove a worktree that has submodules or untracked
  files. The helper passes `--force` in exactly two cases, after its own check:
  initialized submodules with no changes, stash, or local commits, and
  untracked dependency or cache folders such as `node_modules` or `.venv`.
  This is the only force removal the delivery routes permit.
- **Branches.** The default branch and long-lived names such as `main` or
  `develop` are never deleted, even when their worktree is removed.
- **Leftover folders.** A folder below a worktree parent that is not a
  registered worktree is reported as `orphan` and left alone. Inspect it and
  ask before deleting it.
- **Unreadable worktrees.** `git cannot read this worktree` usually means the
  repository folder was renamed or moved. `git worktree repair` in the
  repository fixes the link; run it only on request, then scan again.

## Limits

- Repositories are found up to four levels below the root where `.git` is a
  directory. A bare repository with a worktree layout is not detected.
- A squash merge after which the base changed the same lines again cannot be
  proven locally. Without a matching merged pull request the branch stays
  `unmerged`. The pull-request check uses the GitHub CLI; on another provider,
  confirm the merge through [Review provider access](route-review-access.md)
  and remove the worktree with `--include`.
- The stash belongs to the repository, not to a worktree, and is not touched.
- Freed space can appear late when the file system keeps snapshots. Say so when
  the number does not match the removed size.

## Cross-links

- Creating, adopting, or cleaning up a worktree as part of another route stays
  with that route and [Worktree safety](worktree-safety.md).
- Archiving sessions, clearing build caches, or freeing disk space outside Git
  worktrees is outside this route.
