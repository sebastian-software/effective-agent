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

The hook only checks. It never stages, commits, or pushes. Fix a README failure
with `mise run readme:write`, then review and commit the output. When an
external host is down and blocks a push, skip that job once with
`LEFTHOOK_EXCLUDE=links git push`; CI still checks the pull request.

## Link checks

Every Markdown and site link is checked on every run, not only the links a
change touches.

Both tasks call `scripts/check-links.py`, which maps URLs on
`skills.sebastian-software.com` to the corresponding files in this checkout.
This checks new skill pages before they are deployed, including links from
READMEs. Other domains still receive the same network checks as before.

- **Before a push**, `mise run links:check` applies `lychee.toml` strictly: any
  error fails, including 403, 5xx, and timeouts. Successful results are cached
  for a day in `.lycheecache` (ignored by Git), so repeated pushes take well
  under a second; failures are always rechecked.
- **In CI**, pull requests and a weekly run add `.github/lychee-ci.toml`. Many
  hosts block or slow down GitHub runners while serving contributors normally,
  so CI fails only when a link is gone (404, 410), an anchor is missing, or a
  host cannot be reached at all.

Fix a dead link by finding the source's current URL. Add an entry to
`.lycheeignore` only when no checker can verify the link from any network, and
record the reason and date beside it. A link that fails only in CI does not
belong there. A host that refuses some contributor networks but not CI is
skipped by the local task only, with a comment in `mise.toml`.

The [link-check decision](adr/0007-check-links-strictly-before-push.md) records
why the two levels differ.
