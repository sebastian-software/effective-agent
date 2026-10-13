<!-- Shared contract for every Effective Delivery route that uses Git worktrees. -->

# Worktree Safety

Read this reference before the workflow creates, adopts, writes in, stages
from, commits in, pushes from, integrates from, or removes a Git worktree.

## Establish a Run-Local Receipt

Use Git metadata rather than similar-looking paths. Record in the current run:

- canonical repository identity from `git rev-parse --path-format=absolute
  --git-common-dir` and the absolute worktree root from `git rev-parse
  --path-format=absolute --show-toplevel`;
- the registered worktree entry, expected branch or detached commit, base
  reference, and the work unit this checkout serves (PR head, dependency
  group, or port shard) plus its exclusively owned files;
- the checkout class: primary checkout, user-created worktree, harness-managed
  worktree, or worktree created by this run;
- cleanup ownership. Only a worktree created by this run is workflow-owned.

Keep the receipt in run context; do not create a private ledger, hidden state
directory, or mandatory receipt file. Treat a pre-existing linked worktree as
foreign unless the host identifies it as managed for the current task.

## Preflight and Revalidation

1. Inspect `git worktree list --porcelain`, relevant local and remote branch
   refs, the proposed absolute path, and dirty and staged state before creating
   or adopting a worktree. Refuse branch, path, or file-ownership collisions;
   never overwrite or reuse a checkout by name resemblance.
2. Preserve dirty and staged state. Never stash, reset, overwrite, discard,
   commit, or absorb foreign changes. Use a clean isolated worktree when
   possible; stop when unrelated state cannot be separated safely.
3. Reuse a suitable linked or harness-managed worktree instead of nesting a new
   one. Never claim cleanup ownership for a checkout the workflow did not
   create.
4. Immediately before the first write and after any resume, delegation, or
   handoff, compare the repository identity, absolute root, registered worktree
   entry, and expected branch or detached commit with the receipt. Stop on any
   mismatch before editing, install or generation commands, validation that
   writes, staging, commit, integration, push, or cleanup.
5. Run Git commands with `git -C <absolute-root>` and every other command with
   an explicit tool working directory. Do not rely on a previous `cd` or on
   shell variables surviving another tool call; carry the recorded absolute
   values into each command.

## Stage and Deliver One Unit

- Scope the worktree to the one work unit named in the receipt.
- Stage explicit paths with `git -C <root> add -- <paths>`. Avoid `git add .`,
  `git add -A`, and `git commit -a` whenever other changes could exist.
- Inspect both `git -C <root> diff --cached --name-only` and `git -C <root>
  diff --cached` before every commit or checkpoint. Foreign staged work blocks
  delivery until it is isolated.
- Treat a shared lockfile, manifest, or generated file as owned only when the
  repository-native command for the current unit produced it in the verified
  root and the complete diff belongs to that unit's declared purpose. If
  another unit appears in the diff, narrow and rerun the owning command,
  serialize after the earlier unit, or split the work; never hand-delete
  unrelated entries.
- Immediately before a run-owned commit, revalidate that `HEAD` still equals
  the receipt's expected commit and that detached-versus-branch state still
  matches. Record the full staged tree ID after inspecting the staged diff.
  After the commit succeeds, advance the receipt to the new commit only when
  its parent is that expected commit and its complete tree equals the recorded
  staged tree. This explicit transition is the only way the workflow may change
  the receipt's expected commit; an arbitrary HEAD move remains foreign and
  blocks push, integration, and cleanup. Propagate the latest expected commit
  through handoff and integration; never bless an arbitrary observed HEAD as a
  checkpoint.
- Do not rewrite remote history unless the exact operation is documented by the
  calling route and authorized for the current unit. Revalidate review and
  branch state after any push.

## Clean Up Conservatively

Remove a worktree automatically only when the receipt says this run created it
for the recorded work unit. Immediately before removal, verify the same
repository identity, registered absolute path, latest run-owned expected branch
or detached commit, and a clean status. For a detached receipt, also prove that
`HEAD` has not become attached to a branch even when the commit OID is
unchanged.

Never use force removal for automatic cleanup. Leave a dirty, moved,
mismatched, user-created, or harness-managed worktree and its branch intact;
report the exact path, observed state, expected state, and safest next action.
Require separate user authority for destructive cleanup or branch deletion.
