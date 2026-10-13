# Contributor Checks

Pinned contributor tools and Git hooks catch a broken README or link before a
push. CI runs the same checks on every pull request and remains the gate for
changes pushed without the hooks.

## Project language

US English (`en-US`) is required for all Effective Agent project content,
whether written by a person, agent, or bot. This includes:

- Issue and pull request titles and descriptions, comments, and reviews.
- Project posts, discussions, announcements, and other shared communication.
- Documentation, ADRs, skill guidance, website copy, and code comments.
- Commit messages, changelogs, and release notes.

Use US spelling, such as "behavior," "color," and "organize." Before publishing
or editing an artifact, check its title and entire body for language and
spelling. Translate content drafted in another language before sharing it.
When correcting an existing issue or pull request, preserve its meaning,
links, technical identifiers, acceptance criteria, and decision status.

Keep quoted source text, proper names, exact technical identifiers, and
locale-specific examples or fixtures intact when their original language
matters; write the surrounding explanation in US English. Private conversations
may use the participants' preferred language. This repository policy does not
override the language requested by users of the installable skills.

The [project language decision](adr/0011-use-us-english-for-project-content.md)
records the rationale and scope. Reviewers check language alongside content;
the existing automated checks do not establish language compliance.

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
`lychee.toml`, as for `www.ftc.gov`. When such a host still answers GitHub
runners with a false 404, exclude it in `.github/lychee-ci.toml` only. Add an
entry to `.lycheeignore` only when no checker can verify the link from any
network, and record the reason and date beside it. A link that fails only in CI
does not belong there. A host that refuses some contributor networks but not CI
is skipped by the local task only, with a comment in `mise.toml`.

The [link-check decision](adr/0007-check-links-strictly-before-push.md) records
why the two levels differ.

## Claim freshness

`scripts/check-claim-freshness.py` finds verification dates in skill guidance
and instruction packs (`as of October 2026`, `Snapshot date: **2026-10-14**`,
`Last verified 2026-07-22`) and reports every one older than 180 days. With
`--undated` it also lists support-status claims, such as "Limited
availability" or "Chromium-only" next to a browser name or version, that carry
no date. Run it locally with `mise run claims:freshness`.

A scheduled workflow runs the check on the first of each month and fails when a
claim is due, so the failure reaches the maintainers. To resolve it, re-check
each reported claim against its primary source, then update the claim and its
date together. See [Date Volatile Claims](authoring-skills.md#date-volatile-claims)
for the convention and the [claim-freshness decision](adr/0012-date-and-recheck-volatile-claims.md)
for the rationale. The check reads files only; deciding whether a claim is
still true remains review work.

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
