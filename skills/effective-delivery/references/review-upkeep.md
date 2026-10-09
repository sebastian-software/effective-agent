# Review Upkeep

Use for requested PR maintenance: resolve feedback, repair CI, or bring a branch
current. The [Review route](route-review.md) owns authority; authorship alone
does not authorize implementation, pushes, replies, or provider changes.

Inspect what changed since the last action, current human and bot feedback,
CI, mergeability, and the PR's stated outcome. Use
[review judgment](review-judgment.md) for an unresolved finding or a requested
full review, rather than repeating an entire review before every small fix.
Repair missing intent or ticket information when the maintenance request and
repository convention call for it; do not fabricate requirements.

## Resolve Feedback

- Fix supported, consequential, in-scope findings through relevant checks and
  the already authorized handoff. Apply [worktree safety](worktree-safety.md)
  before the first write and after a resume or handoff.
- Decline practically negligible or counterproductive changes with evidence
  and the maintenance tradeoff. Do not add a fallback, state machine,
  abstraction, or ceremonial test merely to satisfy a bot.
- Keep worthwhile out-of-scope work separate. Propose a follow-up only when the
  residual risk earns ownership; do not create backlog filler.
- Correct misunderstandings respectfully. Prepare replies when publication is
  not authorized; send them when it is.

Keep the PR description aligned with the final implementation and its evidence.
When the change alters rendered pages, keep its screenshot section current after
pushes that change them: `effective-web` produces the annotated captures, and
the selected provider adapter publishes them (with `gh`, see recipe 10 in
[GitHub CLI fallback recipes](gh-recipes.md)).
Resolve consequential architectural choices or developing reviewer conflicts
with the smallest necessary human decision, while completing independent work.

## CI and Branch State

For an apparently transient completed CI failure, rerun failed jobs once when
CI maintenance is authorized. Investigate recurring failures rather than
looping unchanged retries. A relevant correction justifies rerunning affected
checks; retain the failure and recovery evidence.

When branch upkeep is authorized, follow repository convention. Merging the
base is the default-safe choice; rebase and `git push --force-with-lease` need
the repository's linear-history convention and authority to rewrite the
affected owned branch. Never rewrite someone else's work by assumption.

For a stuck provider preview check, use a documented re-trigger only after the
bounded retry and a current branch, at most once or twice. Close/reopen is a
provider mutation, not a generic retry: use it only when documented and within
granted authority. If still stuck, report the evidence and stop that retry flow.

Use [review verification](review-verification.md) for execution or browser
evidence and [review voice](review-voice.md) only when response wording needs
calibration. Distinguish local, committed, pushed, and published outcomes in
the final handoff.
