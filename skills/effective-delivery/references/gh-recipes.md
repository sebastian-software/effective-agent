# GitHub CLI fallback recipes

Use this reference only after [Provider access](provider-access.md) selects `gh` as
the adapter. Prefer a capable connected GitHub tool when the shell sandbox
cannot reach the network or local CLI credentials. Never copy credential files,
keychain values, or tokens into the sandbox to make these commands work.

Placeholders: `<N>` = PR number, `<head>`/`<base>` = the PR's head/base branch
names.

Set up once per run:

```bash
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
# Use a caller-supplied reviewer identity when available. Only otherwise:
ME=$(gh api user -q .login)
```

For headless automation, `gh` supports an already injected `GH_TOKEN` (or
`GH_ENTERPRISE_TOKEN` for GitHub Enterprise). Do not extract a host login into
one. An installation token may not expose a user identity; use the supplied app
or bot identity instead of requiring `gh api user`.

## 1. Discover the relevant PRs

Current repo only. Mode A = to review; Mode B = your own.

```bash
# Mode A: assigned to me for review, OR I reviewed it before (but I'm not the author)
gh pr list --repo "$REPO" --state open -S "review-requested:@me" \
  --json number,title,headRefName,baseRefName,author,updatedAt,isDraft
gh pr list --repo "$REPO" --state open -S "reviewed-by:@me -author:@me" \
  --json number,title,headRefName,baseRefName,author,updatedAt,isDraft

# Mode B: my own PRs (author, plus anything assigned to me)
gh pr list --repo "$REPO" --state open -S "author:@me" \
  --json number,title,headRefName,baseRefName,updatedAt,isDraft
gh pr list --repo "$REPO" --state open -S "assignee:@me -author:@me" \
  --json number,title,headRefName,baseRefName,updatedAt,isDraft
```

Merge the Mode A sets and dedupe by `number`. Skip drafts unless the user asked
for them.

## 2. Build the per-PR picture

```bash
FIELDS=number,title,body,headRefName,baseRefName,author,isDraft,mergeable,mergeStateStatus,reviewDecision,updatedAt,commits,comments,reviews,statusCheckRollup,labels,url,closingIssuesReferences
gh pr view <N> --repo "$REPO" --json "$FIELDS"
```

Read it like this:

- **Since my last action**: find my latest entry in `reviews[]` where
  `author.login == $ME` and note `submittedAt`. New `commits[].committedDate` or
  `comments[].createdAt` after that timestamp = something to look at. Nothing
  after it and no new comments → nothing to do.
- **mergeStateStatus**: `BEHIND` = branch is behind base (needs rebase);
  `DIRTY`/`mergeable == CONFLICTING` = merge conflict; `BLOCKED` = checks/review
  gating; `CLEAN` = good.
- **statusCheckRollup**: mixed objects — status contexts carry `state`
  (`SUCCESS`, `FAILURE`, `PENDING`); check runs carry `status` plus
  `conclusion` (`conclusion` is null while running, never `PENDING`). This is
  your CI view; provider preview checks (e.g. a database preview like Supabase)
  show up here too.
- **closingIssuesReferences**: the linked issue(s) — the intent source and your
  scope yardstick. If empty, also scan `body` for `Closes #` / `Fixes #` and the
  branch name. To actually read the ticket content, see section 2b.

Full diff:

```bash
gh pr diff <N> --repo "$REPO"
```

For just the new commits since your last review, list commits from the JSON and
diff them in the worktree (section 6): `git diff <last-reviewed-sha>..HEAD`.
If the author force-pushed and that SHA is unreachable, inspect the full current
PR diff, re-read your earlier review, and explicitly revalidate every previously
reviewed behavior or fix. A full current diff alone cannot reveal a change that
was dropped during the rewrite.

## 2b. Resolve intent and linked acceptance criteria

The review starts from intent, so get the ticket content — adaptively:

```bash
# 1) GitHub issue linked? (preferred — gh reads it directly)
gh pr view <N> --repo "$REPO" --json closingIssuesReferences \
  -q '.closingIssuesReferences[].number'
gh issue view <ISSUE> --repo "$REPO" --json title,body,labels,state
```

If there's no linked GitHub issue **and** the repo clearly doesn't use GitHub
issues (`gh issue list -L 5` is empty, or Issues are disabled), the source is
probably elsewhere — look for a Linear ticket: a `https://linear.app/...` link in
the PR body, or a Linear-style branch name (`name/abc-123-...`). Read it through a
Linear MCP **if one is connected** — discover its tools at runtime (e.g.
`ToolSearch "linear issue"`) and, if Linear tools come back, use them to fetch the
ticket.

If no Linear MCP is connected and the content isn't reachable, don't stall:
use the PR title, description, diff, and available requirements. A missing link
does not stop independent technical review. Note an established ticket-linking
requirement as an unresolved process condition, and ask only for acceptance
context needed to resolve a specific judgment. Publish a question only when PR
communication is authorized; otherwise include it in the returned review.

## 3. Human vs. bot author

Tone depends on this (see "Voice" in the [Review route](route-review.md#voice)). Bots: anything ending in `[bot]`,
plus known names. The REST API also exposes `user.type == "Bot"`.

```bash
is_bot() {
  case "$1" in
    *"[bot]") return 0 ;;
    vercel|cursor|Copilot|copilot*|github-actions|coderabbitai|sentry*) return 0 ;;
    *) return 1 ;;
  esac
}
# Extend the known-names list with the bots actually active in this repo —
# check the authors of recent PR comments and reviews.
```

Bot findings still deserve real triage: judge each one valid / out of scope /
wrong exactly like a human comment (see [review upkeep](review-upkeep.md#resolve-feedback)), just reply in the short
technical tone from "Voice".

## 3b. Automated PRs

Automated PRs need no linked ticket — their intent is self-evident. Detect by
author login, branch prefix, or labels (not author alone — release-please often
runs under a human token):

- **release-please**: branch `release-please--*`, title `chore: release...`,
  label `autorelease: *`
- **dependabot**: author `dependabot[bot]`, branch `dependabot/*`
- **renovate**: author `renovate[bot]`, branch `renovate/*`

## 4. Post a review

Simple cases (no line-anchored comments) — use the porcelain command:

```bash
gh pr review <N> --repo "$REPO" --approve         --body "$BODY"
gh pr review <N> --repo "$REPO" --request-changes --body "$BODY"
gh pr review <N> --repo "$REPO" --comment         --body "$BODY"
```

Inline (line-anchored) comments — POST the reviews API with a JSON payload. This
is the fiddly part: validate the JSON payload and confirm every `line` falls
inside a diff hunk before posting.

```bash
cat > /tmp/review-<N>.json <<'JSON'
{
  "event": "REQUEST_CHANGES",
  "body": "Short overall note. Specifics are on the lines below.",
  "comments": [
    { "path": "src/foo.ts", "line": 42, "side": "RIGHT", "body": "..." },
    { "path": "src/bar.ts", "start_line": 10, "line": 14, "side": "RIGHT", "body": "..." }
  ]
}
JSON
gh api repos/"$REPO"/pulls/<N>/reviews --method POST --input /tmp/review-<N>.json
```

Notes:
- `event`: `APPROVE` | `REQUEST_CHANGES` | `COMMENT`.
- `line` is the line number in the file's **new** version (`side: RIGHT`); it
  must fall inside the diff hunks or the API rejects it. Multi-line: add
  `start_line` (and `start_side`).
- Don't prefix bodies with `nit:`/`issue:` — severity goes in the sentence.

## 5. Reply to existing comments / threads

```bash
# List review (line) comments with their ids
gh api repos/"$REPO"/pulls/<N>/comments \
  --jq '.[] | {id, path, line, user: .user.login, in_reply_to: .in_reply_to_id, body}'

# Reply inside a review thread
gh api repos/"$REPO"/pulls/<N>/comments/<comment_id>/replies \
  --method POST -f body="..."

# PR-level (conversation) comment
gh pr comment <N> --repo "$REPO" --body "..."
```

Bot findings (from review bots like vercel, cursor, or Copilot) usually live as
review-thread comments —
reply in-thread so the conversation stays attached to the line. Optionally
resolve a thread you've handled via the GraphQL `resolveReviewThread` mutation
(nice-to-have, skip if it slows you down).

## 6. Worktree flow (Mode B fixes)

Read [worktree safety](worktree-safety.md) first. Never edit a
dirty primary checkout. Reuse a suitable verified linked or harness-managed
worktree without taking cleanup ownership, or create a workflow-owned worktree
after checking registered worktrees, branch refs, path collisions, and dirty and
staged state. Record the repository identity, absolute root, detached commit,
head/base refs, checkout class, and cleanup ownership in run context.

```bash
SOURCE_ROOT="$(git rev-parse --path-format=absolute --show-toplevel)"
WT_PARENT="$(mktemp -d)"
WT="$WT_PARENT/pr-<N>"

# inspect before creation; refuse any unexpected registration or collision
git -C "$SOURCE_ROOT" worktree list --porcelain
git -C "$SOURCE_ROOT" status --short

# fetch the current PR head and avoid any local branch checked out elsewhere
git -C "$SOURCE_ROOT" fetch origin "<head>"
git -C "$SOURCE_ROOT" worktree add --detach "$WT" "origin/<head>"

# capture and verify the run-local receipt before the first write
git -C "$WT" rev-parse --path-format=absolute --git-common-dir
git -C "$WT" rev-parse --path-format=absolute --show-toplevel
git -C "$WT" rev-parse HEAD
git -C "$WT" status --short

# ... make the fix with every tool call using workdir="$WT" ...
git -C "$WT" add -- <owned-path> [<owned-path>...]
git -C "$WT" diff --cached --name-only
git -C "$WT" diff --cached
# record `git write-tree` as <expected-tree>, then revalidate the receipt
git -C "$WT" write-tree
test "$(git -C "$WT" rev-parse HEAD)" = "<expected-head>"
test -z "$(git -C "$WT" symbolic-ref -q HEAD)"
git -C "$WT" commit -m "fix: <what and why>"
# record <post-commit-head> and advance the run-local receipt only after proving
# its parent is <expected-head> and its complete tree is the staged tree above
git -C "$WT" rev-parse HEAD
test "$(git -C "$WT" rev-parse HEAD^)" = "<expected-head>"
test "$(git -C "$WT" rev-parse HEAD^{tree})" = "<expected-tree>"
test -z "$(git -C "$WT" symbolic-ref -q HEAD)"
git -C "$WT" push origin HEAD:"<head>"

# only after registration, the updated expected HEAD, and clean status match
test "$(git -C "$WT" rev-parse HEAD)" = "<post-commit-head>"
test -z "$(git -C "$WT" symbolic-ref -q HEAD)"
git -C "$WT" status --short
git -C "$SOURCE_ROOT" worktree remove "$WT"
```

The placeholders above are run-context receipt values, not ambient assumptions.
Advance `<expected-head>` to `<post-commit-head>` only for the successful commit
whose parent and full `<expected-tree>` prove that the run created the
transition. The detached-state checks also reject a branch attachment at the
same commit OID. If the final status is dirty or any other receipt field
changed, do not remove the worktree. Leave it and its branch intact with the
exact discrepancy.

Fork PRs: the head branch lives in the contributor's fork, so a normal push
won't work — that's a Mode A situation anyway. For your own PRs the branch is in
this repo, so the explicit push above is correct.

## 7. Keep the branch current

Pick the update strategy from the repository's convention, not from preference.
Check branch protection and history first: does the repo use squash or merge
commits (`gh pr list --state merged` titles, merge strategy in settings), does
CONTRIBUTING mandate rebasing, do PRs show "Update branch" merges?

**Default-safe: merge from base.** Works everywhere, never rewrites history,
never dismisses approvals:

```bash
gh pr update-branch <N> --repo "$REPO"
# or manually:
git -C "$WT" fetch origin "<base>"
git -C "$WT" merge "origin/<base>"
git -C "$WT" push origin HEAD:"<head>"
```

**Rebase — only where the repo prefers linear history.** Always end with
`--force-with-lease` (refuses to clobber if someone else pushed). A force-push
can dismiss stale approvals and mark inline review threads outdated when
repository settings enable those effects. Rebase only when needed, and re-check
the review state before asking authors or reviewers to repeat work:

```bash
git -C "$WT" fetch origin "<base>"
git -C "$WT" rebase "origin/<base>"
# resolve real conflicts normally, THEN:
git -C "$WT" push --force-with-lease origin HEAD:"<head>"
```

**Lockfile conflicts** — don't hand-merge them, regenerate. Detect the package
manager from the conflicting lockfile: `pnpm-lock.yaml` → `pnpm install`;
`package-lock.json` → `npm install`; `yarn.lock` → `yarn install`;
`bun.lockb`/`bun.lock` → `bun install`. Resolve any `package.json` conflict
first, then rebuild the lockfile so it matches:

```bash
# example for pnpm-lock.yaml; substitute the detected manager and lockfile
# run with the tool working directory set explicitly to "$WT"
pnpm install
git -C "$WT" add -- pnpm-lock.yaml
git -C "$WT" diff --cached --name-only
git -C "$WT" diff --cached
git -C "$WT" rebase --continue   # (merge flow: commit the merge instead)
```

## 8. CI recovery

For a completed GitHub Actions run that appears transiently flaky, first rerun
only failed jobs and their dependencies once:

```bash
gh run rerun <run-id> --failed --repo "$REPO"
```

Inspect the new result before escalating. Do not rerun a deterministic code or
configuration failure; fix the cause instead.

### Stuck provider preview check

Some provider preview checks (e.g. a database preview like Supabase) re-trigger
on PR close/reopen — check the provider's docs for its documented recovery
before assuming this. Use such a re-trigger only after the branch is genuinely
up to date (section 7). At most once or twice; never loop.

```bash
gh pr close  <N> --repo "$REPO"
gh pr reopen <N> --repo "$REPO"
# then re-poll checks:
gh pr view <N> --repo "$REPO" --json statusCheckRollup,mergeStateStatus
```

If it's still stuck after a reopen, stop and report it in the summary — don't
keep cycling.

## 9. Verifying via preview deployment

Pull the preview URL from checks/deployments (no local server, ever):

```bash
gh pr view <N> --repo "$REPO" --json statusCheckRollup \
  --jq '.statusCheckRollup[] | select(.targetUrl != null) | {context, targetUrl}'
# status contexts (e.g. Vercel) use context/targetUrl; check runs use name/detailsUrl
gh api repos/"$REPO"/deployments --jq '.[0].statuses_url'   # fallback
```

Then drive that URL with an available, suitable browser tool. The optional,
separately installed `agent-browser` CLI
([vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser)) is
one option, not a prerequisite. If no browser tool is available, keep the
verification static and report that the preview could not be exercised.
