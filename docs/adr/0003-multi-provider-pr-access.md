# ADR 0003: Put PR Review Behind a Capability-Based Provider Boundary

- Status: Accepted
- Date: 2026-07-28
- Decision issue: [#200](https://github.com/sebastian-software/effective-agent/issues/200)

## Context

`pr-review` coupled its complete review and maintenance workflows to `gh`.
Mode C was provider-neutral, but it only classified review items already
resolved by a caller; it could not inspect a supplied PR and produce an
actual review. Forgejo, Gitea, GitLab, and unattended GitHub App callers
therefore had no complete path.

The coupling also made GitHub access unnecessarily fragile in sandboxed agent
runtimes. `gh` normally reads credentials below its config directory or the
platform credential store. A shell sandbox may expose neither even when the
host already has an authenticated GitHub connector. GitHub documents
`GH_TOKEN` as the headless alternative, but moving a user's long-lived token
into a sandbox would widen credential exposure rather than fix the boundary.

The review judgment itself does not depend on a provider. It needs a bounded set
of facts — PR metadata and intent, diff, history and threads, checks and
mergeability, reviewer identity — and it produces a decision plus review
comments. Provider APIs differ in how those facts and actions are represented.

## Decision

1. `pr-review` defines one capability contract for live provider access. The
   review ladder refers to those capabilities, not to provider commands.
2. Each PR uses one coherent access path: an already authenticated
   host-native provider tool first, a provider CLI or documented API second, or
   complete caller-supplied context when the caller owns provider integration.
3. Caller-supplied full context runs the same Mode A judgment as a live review
   and can return `pr-review-result/v1` for caller-owned publication. Mode C's
   narrower `pr-review-handoff/v1` item classifier remains unchanged.
4. Reviewer identity can be supplied explicitly and is kept separate from the
   provider's delivery actor. App installation tokens are not required to
   impersonate a user or satisfy a user-profile lookup.
5. Provider-specific commands stay at the boundary. Existing `gh` commands
   remain in one GitHub fallback reference; adding another provider must not
   duplicate or fork the review ladder.
6. This repository does not adopt or build a universal PR CLI wrapper now.
   A tool may be used as an adapter when it satisfies the same capabilities,
   but it is not part of the skill's portable contract.

## Alternatives Considered

### Adopt `gcli` as the universal command layer

Rejected for now. `gcli` supports GitHub, GitLab, and Gitea broadly, but its
integrated review action is marked experimental and its current manual states
that review is not implemented for Gitea. It cannot close the Forgejo/Gitea
review gap without another fallback.

### Adopt Magit Forge

Rejected as the portable boundary. Magit Forge provides API-backed support for
GitHub and GitLab, while its current manual lists Forgejo and Gitea as only
partially supported. It also assumes an Emacs/Magit runtime that a standalone
agent skill cannot require.

### Add complete command recipes for every provider

Rejected. This would make the skill own authentication, pagination, review
thread semantics, inline anchors, CI retry behavior, and API drift separately
for each provider. The shared judgment would become scattered across the same
wrappers the change is intended to avoid.

### Support only caller-supplied reviews

Rejected as the sole path. It fits automated multi-provider services, but
removes the useful direct workflow for people whose host already exposes a
capable connected tool or provider CLI.

## Consequences

- Forgejo, Gitea, GitLab, GitHub Apps, and future providers can reuse the full
  review judgment without teaching `pr-review` their command syntax.
- Direct live support is capability-based rather than claimed from a detected
  remote URL. A partial CLI must degrade to an exact caller-owned review result
  instead of silently omitting threads, checks, or publication.
- Sandboxed GitHub runs prefer an authenticated host connector. They do not
  copy local login files or tokens into the shell merely to make `gh` pass an
  upfront authentication gate.
- Provider adapters still own translation into their native concepts and
  provider-specific inline positions. The skill itself consistently says PR.
- The caller-supplied contract adds one stable integration surface and one
  versioned result schema. The review ladder, voice, decision rules, and
  codebase-context pass remain single-source.

## Validation and Review Triggers

The static scenarios must cover a caller-owned Forgejo review, a GitHub
connector fallback when sandboxed `gh` is unavailable, a supplied app identity,
and safe degradation when a partial adapter cannot publish a review.

Revisit the wrapper decision when a maintained multi-provider tool provides
stable read, thread, check, inline-review, approval/request-changes, and reply
support for GitHub, GitLab, Forgejo, and Gitea; or when repeated adapters reveal
a smaller common contract than the one in
`skills/pr-review/references/provider-access.md`.

## References

- [GitHub CLI environment variables](https://cli.github.com/manual/gh_help_environment)
- [GitHub App authentication modes](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/about-authentication-with-a-github-app)
- [Endpoints available to installation access tokens](https://docs.github.com/en/rest/authentication/endpoints-available-for-github-app-installation-access-tokens)
- [GitLab merge request reviews](https://docs.gitlab.com/user/project/merge_requests/reviews/)
- [Forgejo API usage](https://forgejo.org/docs/latest/user/api-usage/)
- [Codeberg documentation for `tea` and `fj`](https://docs.codeberg.org/git/clone-commit-via-cli/)
- [`gcli pulls review` manual](https://manpages.debian.org/unstable/gcli/gcli-pulls-review.1.en.html)
- [Magit Forge support matrix](https://docs.magit.vc/forge/Setup-a-Partially-Supported-Host.html)
