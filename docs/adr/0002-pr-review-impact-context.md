# ADR 0002: Resolve Pull-Request Impact Context on Demand

- Status: Accepted
- Date: 2026-07-27
- Decision issue: [#190](https://github.com/sebastian-software/effective-agent/issues/190)

## Context

`pr-review` judged a pull request from the diff, the linked ticket, CI status,
and existing review threads. It had no way to ask what the diff touches beyond
itself. A search for `caller`, `call site`, `codebase`, and `pattern` across
`skills/pr-review/SKILL.md` and its six references returned only Mode C's
unrelated "caller" wording: the capability was absent rather than thin.

Commercial machine reviewers close that gap with a persistent repository graph —
entities plus call, import, and usage edges — queried per changed function. A
skill cannot host an index service. The open question was whether the same
relationships can be resolved on demand, for the few symbols a pull request
actually changes, at a cost the review can carry.

## Evidence

A corpus study ran on 2026-07-27 against public pull requests reviewed by an
established commercial machine reviewer. That reviewer embeds a severity badge
image in each inline comment, so severity extracts mechanically; the corpus held
443,557 such pull requests at sampling time.

**Method.** Twenty-five merged pull requests were sampled per primary language
across ten languages (TypeScript, JavaScript, Python, Go, Rust, Java, Ruby, PHP,
C#, Kotlin), sorted by last update. Repositories were bucketed by stars — small
below 100, medium 100 to 999, large 1000 and above. For each pull request the
inline review comments and the changed-file list were fetched, and every comment
carrying a severity badge was recorded. The raw study is deliberately not
committed; this section is its auditable summary.

**Sample.** 250 pull requests across 111 distinct repositories. 211 carried at
least one badged finding, for 389 findings in total — 1.85 findings per pull
request that had any. Severity split 272 P1 (69.9 percent) and 117 P2 (30.1
percent). By repository size: 197 findings small, 76 medium, 116 large.

**Headline result.** Findings that reference code outside the diff are a small
minority. Two detectors bound the rate:

- A permissive detector — any relational phrase, or any backticked file path not
  in the diff — flagged 54 of 389 findings (13.9 percent).
- A strict detector — a named peer symbol, an explicit plural or definite "call
  sites", "sibling", "every other", or "the rest of the codebase" — flagged 10
  of 389 (2.6 percent).

A manual audit of twelve permissively flagged findings found four clear true
positives, five clear false positives, and three uncertain. The defensible rate
is therefore roughly **3 to 8 percent**, not the dominant share the issue
assumed. The two dominant false-positive shapes became rules in the reference:
a hypothetical caller ("when a caller supplies an empty list") is not a call
site, and a file path named in prose is not a resolved relationship.

**Categories.** Classification is a keyword heuristic over each finding's bolded
title and body, with a residual bucket; it is indicative, not exact.

| Category | Findings | Share | Strict out-of-diff | Example |
| --- | ---: | ---: | ---: | --- |
| Other in-diff defect (residual) | 246 | 63.2% | 0 | — |
| Removed behaviour | 44 | 11.3% | 0 | [better-auth#10507](https://github.com/better-auth/better-auth/pull/10507#discussion_r3642032033) |
| Broken call site or contract | 44 | 11.3% | 6 | [celestia-app#7598](https://github.com/celestiaorg/celestia-app/pull/7598#discussion_r3656086630) |
| Cross-layer mismatch | 42 | 10.8% | 0 | [kube-router#2064](https://github.com/cloudnativelabs/kube-router/pull/2064#discussion_r3388810220) |
| Pattern divergence | 13 | 3.3% | 4 | [gumbo#13](https://github.com/CajunSystems/gumbo/pull/13#discussion_r3652051302) |

Two consequences follow directly. Broken call sites are the class that actually
needs resolution — 6 of the 10 strict out-of-diff findings, at an 80 percent
out-of-diff rate under the permissive detector. And the cross-layer default
mismatch, which the issue named as a motivating class, produced **no** strict
out-of-diff finding in this sample. The reference keeps it in scope but is
explicitly forbidden from manufacturing one.

**Whether authors act.** GitHub nulls an inline comment's `line` once the
commented line no longer exists in the diff, a mechanical proxy for the author
having changed that code afterwards. It held for 179 of 389 findings (46
percent). The proxy cannot distinguish a targeted fix from an unrelated edit and
is reported only as a coarse engagement signal.

## Decision

Resolve impact context **on demand**, per review, for the symbols the diff
changes. No index, no persistent graph, no background service.

The mechanism lives in `skills/pr-review/references/codebase-context.md` and is
reached from ladder rung 2 in `SKILL.md`. It is bounded:

- depth one, with no transitive closure;
- at most ten resolved symbols per review, exported and cross-module first;
- when the cap binds, the review says so; a silent fall back to a diff-only pass
  is prohibited;
- "cap reached" and "resolution not possible" are separate disclosures.

The step sits in the ladder rather than in the per-PR picture. The per-PR
picture runs before the rung-1 intent gate and before the "nothing new since
your last review" early exit, so placing resolution there would spend it on
pull requests the review abandons or skips.

A symbol qualifies when its declaration changed, or when a body change alters an
observable default, a thrown error, or the returned shape. A declaration-only
trigger was rejected because it cannot reach the cross-layer class at all.

## Alternatives Considered

### Build or vendor a repository index

A persistent entity-and-edge graph is what the commercial tools use, and it
answers richer questions than on-demand search. It also needs storage, an
invalidation strategy, and a build step in every repository the skill is
installed into. A skill that ships as Markdown cannot own that lifecycle, and a
per-machine index would make reviews non-reproducible between reviewers.

### Adopt severity badges and a confidence score

The sampled reviewer labels every finding P1 or P2 and the labels are genuinely
useful for triage. `skills/pr-review/SKILL.md` states that its output "is a
content contract, not a one-line format or severity-label system". Adding badges
would replace prose judgment with a taxonomy the rest of the skill is built to
avoid. Rejected on that ground alone; the measured 70/30 P1/P2 split is recorded
above for anyone revisiting the question.

### Adaptive noise suppression from ignored comments

Learning which findings authors ignore is the natural way to tune the pass. It
requires shared team state. A per-machine store would make two reviewers produce
different reviews of the same pull request. Revisit only if the collection ever
gains a committed, reviewable location for such state.

### Ground the taxonomy in this repository's own history

Cheaper and fully re-verifiable, but this repository's pull requests are almost
entirely Markdown and site work. It cannot supply call-site evidence at all.

## Consequences

- The context pass produces no comment on most pull requests. That is the
  measured expectation, not a failure; a pass that comments every time is
  misconfigured.
- The cap of ten is generous against a measured 1.85 findings per pull request.
  It bounds the worst case rather than the common one.
- Out-of-diff findings cannot be anchored inline, because GitHub will not attach
  a review comment to a line the diff does not contain. They go in the review
  body under a plain heading, naming the file and symbol in prose.
- Code resolved from outside the diff is untrusted evidence in the same way
  preview content and browser diagnostics already are.
- The evidence here is a sample, not a census, and its category labels are
  heuristic. Re-run the study before treating any figure as a trend.
- Revisit when the harness exposes reliable cross-repository symbol resolution,
  or when the cap is observed to bind on ordinary pull requests rather than
  large refactors.
