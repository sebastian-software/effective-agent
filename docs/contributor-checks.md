# Contributor Checks

Pinned contributor tools and Git hooks catch a broken README or link before a
push. CI runs the same checks on every pull request and remains the gate for
changes pushed without the hooks.

## Set up once per clone

Install [mise](https://mise.jdx.dev/getting-started.html) and Git. From a trusted
checkout, run:

```sh
mise trust
mise install --locked
```

`mise.toml` pins mdtheme, lychee, and Lefthook; `mise.lock` records their
release checksums. After installing, mise runs `lefthook install`, which adds
the pre-push hook from `lefthook.yml` to this clone. Run `mise install --locked`
again after pulling a tooling change. Linked worktrees share the clone's hooks.

## What runs before a push

| Job | Runs when the push changes | Command |
| --- | --- | --- |
| `readme` | `README.md.src`, `README.md`, or `mdtheme.yaml` | `mise run readme:check` |
| `links` | Markdown, site HTML, `.lycheeignore`, or `lychee.toml` | `mise run links:check` |
| `reference-audit` | Markdown under `skills/` or `instructions/`, or the audit prompt or script | `mise run references:audit` |

The hook only checks. It never stages, commits, or pushes. Fix a README failure
with `mise run readme:write`, then review and commit the output. When an
external host is down and blocks a push, skip that job once with
`LEFTHOOK_EXCLUDE=links git push`; CI still checks the pull request.

## Link checks

Every Markdown and site link is checked on every run, not only the links a
change touches.

Both tasks call `scripts/check-links.py`, which maps URLs on
`effective-agent.dev` to the corresponding files in this checkout.
It also maps this repository's GitHub `blob/main/` links to files in the
checkout. New skill pages and agent-instruction links are checked before
deployment or merge, including links from READMEs. Missing files and anchors
still fail; other repositories, branches, and external domains keep their
normal network checks.

- **Before a push**, `mise run links:check` applies `lychee.toml` strictly: any
  error fails, including 403, 5xx, and timeouts. Successful results are cached
  for a day in `.lycheecache` (ignored by Git), so repeated pushes take well
  under a second; failures are always rechecked.
- **In CI**, pull requests and a weekly run add `.github/lychee-ci.toml`. Many
  hosts block or slow down GitHub runners while serving contributors normally,
  so CI fails only when a link is gone (404, 410), an anchor is missing, or a
  host cannot be reached at all.

Fix a dead link by finding the source's current URL. Confirm in a browser that
it is really gone first: some hosts answer scripted requests with a false 404 or
403. When browser navigation headers get through, add them for that host in
`lychee.toml`, as for `www.ftc.gov`. Add an entry to `.lycheeignore` only when
no checker can verify the link from any network, and record the reason and date
beside it. A link that fails only in CI does not
belong there. A host that refuses some contributor networks but not CI is
skipped by the local task only, with a comment in `mise.toml`.

The [link-check decision](adr/0007-check-links-strictly-before-push.md) records
why the two levels differ.

## Reference audit

`scripts/validate-readmes.py` checks that every local link, anchor, and quoted
section name resolves, and that "the X section above/below" points the right
way. It cannot tell whether a pointer's target still contains what the
sentence promises, or whether a changed rule now contradicts another rule in
the same skill. The reference audit covers that before a push.

`mise run references:audit` sends the prompt in
[reference-audit.md](reference-audit.md) to a local coding harness: `claude`
when it is installed, otherwise `codex`. The harness can only read the
repository. It reviews the commits being pushed (the diff against the branch's
upstream, or against `main` for a new branch), plus the router, link targets,
and linking files of each changed Markdown file.

- A **high-confidence** finding fails the push. Medium and low findings are
  printed as advice.
- When a finding is wrong, push once with `git push --no-verify`, or skip only
  this job with `LEFTHOOK_EXCLUDE=reference-audit git push`.
- A missing harness, a login problem, or a timeout prints a warning and never
  blocks.
- Results are cached per change in `.reference-audit-cache/` (ignored by Git),
  so pushing the same commits again costs nothing.
- Choose the harness or model with `REFERENCE_AUDIT_HARNESS=claude|codex` and
  `REFERENCE_AUDIT_MODEL=<model>`. `python3 scripts/reference-audit.py
  --print-prompt` shows exactly what would be sent.

CI does not run the audit: CI never executes model behavior. The
[reference-audit decision](adr/0009-audit-changed-guidance-before-push.md)
records why.
