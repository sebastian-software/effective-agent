# X Strategy Playbook

Use this reference when the assignment is an X or Twitter content strategy,
content program, cadence decision, algorithm-claim review, or update to an
existing X playbook. For a single post whose success does not depend on current
platform mechanics, the lighter guidance in [Platform adaptation](platform-adaptation.md)
is enough.

This playbook provides a starting position, not a promise of reach. Keep durable
strategy separate from the current implementation snapshot so future changes do
not force the whole plan back to zero.

## Strategy Baseline

Start with these bets unless audience, offer, evidence, or observed account data
gives a reason to change them:

- Treat original posts as reach assets. Give each one a useful idea, mechanism,
  proof point, example, resource, or perspective that stands without a prompt to
  engage.
- Give people a real reason to share or quote the post: it helps them explain,
  decide, teach, compare, remember, or start a relevant conversation. Do not
  confuse this with adding "share this" or manufacturing engagement bait.
- Use replies to build context, demonstrate judgment, learn audience language,
  and form real relationships. Reply because there is something useful to add,
  not to hit a quota or attach an unsolicited pitch.
- Build familiarity in the actual niche. Mutual relationships can improve
  distribution under the current implementation, but indiscriminate
  follow-for-follow behavior produces a weak audience and is not the strategy.
- Space strong original posts enough that they are not needlessly competing in
  the same reader sessions. Treat the spacing as an account-level experiment,
  not a universal daily limit.
- Avoid ragebait, repetitive templates, engagement farming, generic AI output,
  and high-volume automated replies. They damage reader trust even when a
  platform classifier does not act on them.
- Judge the program by qualified attention and learning: repeat relevant
  readers, substantive replies, shares and quotes with context, profile visits,
  useful direct conversations, site behavior, leads, opportunities, and
  downstream customer value. Likes and impressions are diagnostic signals, not
  the business result.

## Start a Program Without Starting from Zero

When no account baseline exists, propose a four-week learning cycle rather than
an indefinite calendar:

1. Name the audience, the commercial or professional objective, and the reader
   change each post should create.
2. Select two or three content families from available evidence. Useful
   starting families include a proof-backed lesson, an explained mechanism, a
   reasoned point of view, a build or project observation, and a curated
   resource with original interpretation.
3. Choose a sustainable initial cadence. Two or three strong original posts per
   week is a reasonable experiment for many small teams, not an algorithmic
   optimum. Reduce it when evidence or review capacity cannot support the work.
4. Reserve a small recurring relationship block for reading and adding a few
   substantive replies in relevant conversations. Do not prescribe a reply
   count when usefulness would suffer.
5. Change one meaningful variable at a time where practical: content family,
   opening, evidence form, media role, conversational ending, or distribution
   support. Do not interpret a single post as a controlled experiment.
6. Review weekly and decide what to continue, revise, stop, or investigate.
   Preserve post-level observations and downstream outcomes without declaring
   causality from an uncontrolled feed.

Return the baseline, the first cycle, measurement, assumptions, and review date
as separately reviewable parts. A strategy should remain usable when one
platform parameter changes.

## Evidence Classes

Label consequential platform guidance with one of these classes:

| Class | Meaning | How to use it |
| --- | --- | --- |
| Durable principle | Supported by reader value, editorial quality, or business economics rather than one ranking implementation | Use as the default strategy layer |
| Code-backed snapshot | Present in a named upstream version, with scope and date recorded | Use as a current constraint or directional clue; recheck before consequential use |
| Platform-observed | Seen in account data or product behavior without access to the causal mechanism | Use as local evidence; preserve alternative explanations |
| Tactical hypothesis | A plausible action derived from evidence but not established as a platform law | Test on the account with a decision rule |
| Superseded or disproven | Corrected by stronger or newer evidence | Retain as a warning; do not silently delete the correction history |

Use a compact claim record when platform mechanics materially affect the plan:

```yaml
claim: "Concise, testable statement"
status: code-backed | platform-observed | hypothesis | superseded | disproven
scope: "For You ranking, visibility, account observation, or other boundary"
verified_at: YYYY-MM-DD
source: "Primary URL or local evidence locator"
source_version: "Commit, documentation version, or observation window"
confidence: high | medium | low
recheck_when: "Date, upstream change, product change, or decision trigger"
supersedes: "Previous claim or none"
```

## Current X Implementation Snapshot

Snapshot metadata:

| Field | Value |
| --- | --- |
| Verified | 2026-08-17 |
| Primary source | [xai-org/x-algorithm](https://github.com/xai-org/x-algorithm) |
| Source version | [`c65aa179db7bdd61e2c2821eac87f208a105c053`](https://github.com/xai-org/x-algorithm/tree/c65aa179db7bdd61e2c2821eac87f208a105c053) |
| Covered surface | Published For You retrieval, ranking, diversity, filtering, and abuse-enforcement excerpts |
| Known omissions | Grox prompts and some Botmaker rules are not published; deployment flags and experiments may differ from defaults |

Treat every item below as a code-backed snapshot, not a universal promise about
all X surfaces or future deployment.

### Ranking weights express predicted behavior

The published defaults assign more weight to predicted replies and shares than
to predicted favorites. For example, the snapshot contains favorite `0.5`,
reply `5`, share `2`, DM share `5`, copy-link share `20`, quote `5`, and author
follow `4`. The current mutual-follow reply boost adds `15` to an eligible
original post's reply weight.

These values multiply the predicted probability that a particular viewer will
take an action. They do not multiply raw engagement counts. Therefore statements
such as "one copied link equals 40 actual likes" or "one report cancels 468
likes" are false count conversions. X added explicit comments warning against
that interpretation in the
[ranking parameters](https://github.com/xai-org/x-algorithm/blob/c65aa179db7bdd61e2c2821eac87f208a105c053/home-mixer/params/param.rs#L279-L355)
and [README](https://github.com/xai-org/x-algorithm/blob/c65aa179db7bdd61e2c2821eac87f208a105c053/README.md#scoring-and-ranking).

Strategic implication: make posts worth sharing and discussing, but do not
optimize to a fictional exchange rate or manufacture predicted actions.

### Mutual-follow boost is narrower than the slogan

The current bidirectional boost applies to predicted replies on eligible
original posts when viewer and author follow each other. It does not turn every
reply, repost, or mutual follow into the same reach multiplier. The published
[change note](https://github.com/xai-org/x-algorithm/blob/c65aa179db7bdd61e2c2821eac87f208a105c053/docs/BIDIRECTIONAL_BOOST_CHANGE.md)
also records prior experiment values, so the default itself has already changed.

Strategic implication: build genuine reciprocal relationships around original
work. Treat the numeric boost as volatile.

### Author diversity is per feed slate, not a daily post counter

The default author-diversity multiplier decays when several candidates from the
same author appear in one ranked feed slate. With decay `0.5` and floor `0.25`,
the first candidate keeps `1.0`, the second receives `0.625`, the third
`0.4375`, and later candidates approach the floor. This is not evidence that
each additional post made during a calendar day receives a permanent daily
penalty. See the
[parameters](https://github.com/xai-org/x-algorithm/blob/c65aa179db7bdd61e2c2821eac87f208a105c053/home-mixer/params/param.rs#L221-L246)
and [scorer](https://github.com/xai-org/x-algorithm/blob/c65aa179db7bdd61e2c2821eac87f208a105c053/home-mixer/scorers/ranking_scorer.rs#L680-L706).

Strategic implication: avoid flooding the same reader session and test spacing;
do not present a universal posts-per-day rule.

### Candidate windows and sources have scope

The Phoenix For You pipeline currently filters candidates older than 48 hours.
That cutoff describes a candidate source, not deletion or invisibility across
all X surfaces. Published retrieval defaults also include Phoenix `1000` and
Thunder `1200`, with additional candidate sources; the simplified claim that
the system always takes "1200 in-network plus 1200 out-of-network" is not the
current published architecture. See the
[age configuration](https://github.com/xai-org/x-algorithm/blob/c65aa179db7bdd61e2c2821eac87f208a105c053/home-mixer/params/config.rs)
and [candidate parameters](https://github.com/xai-org/x-algorithm/blob/c65aa179db7bdd61e2c2821eac87f208a105c053/home-mixer/params/param.rs).

Strategic implication: an original post has a time-bounded For You discovery
window, while replies, profiles, links, and other surfaces may keep it useful.

### A cold-start mechanism exists, but is not an entitlement

The snapshot enables an author cold-start mechanism whose defaults consider an
original post from an author with no more than `1000` followers and fewer than
`1000` impressions. For a treatment viewer, freshness defaults to 24 hours, and
one eligible candidate can be lifted toward slots 15–16. Corpus assignments,
viewer arms, flags, and ranking context limit the mechanism. See
[author cold start](https://github.com/xai-org/x-algorithm/blob/c65aa179db7bdd61e2c2821eac87f208a105c053/home-mixer/scorers/author_cold_start.rs)
and its [parameters](https://github.com/xai-org/x-algorithm/blob/c65aa179db7bdd61e2c2821eac87f208a105c053/home-mixer/params/param.rs#L647-L724).

Strategic implication: small accounts should publish worthwhile original work
instead of assuming they have no distribution chance. Do not promise a slot or
reverse-engineer content around the threshold.

### Ranking, filtering, and enforcement are different layers

Some visibility rules remove labeled posts only from out-of-network
recommendations; other labels have broader effects. Do not collapse every reach
change into "shadowbanning" or infer a label from impression counts alone. The
repository explains the distinction between
[scoring and filtering](https://github.com/xai-org/x-algorithm/blob/c65aa179db7bdd61e2c2821eac87f208a105c053/README.md#filtering).

The published enforcement rules include 30-day labels for detected
`llm_slop_post` and `llm_slop_user` conditions. The post rule applies
`RiskyHighVizReply`; the user rule applies `SpamHighRecall`. Because the
classifier prompts and some rules are omitted, the code does not justify a
complete checklist of what X will classify as AI slop. See the
[post rules](https://github.com/xai-org/x-algorithm/blob/c65aa179db7bdd61e2c2821eac87f208a105c053/abuse-enforcement-service/service-lib/rules/enforcement_post.yaml#L39-L45),
[user rules](https://github.com/xai-org/x-algorithm/blob/c65aa179db7bdd61e2c2821eac87f208a105c053/abuse-enforcement-service/service-lib/rules/enforcement_user.yaml#L45-L57),
and [repository omissions](https://github.com/xai-org/x-algorithm/blob/c65aa179db7bdd61e2c2821eac87f208a105c053/README.md#whats-not-in-this-repo).

Strategic implication: use AI to research, structure, challenge, and edit, but
keep a real source, specific judgment, and human editorial control. Avoid
high-volume template production and automated engagement.

## Mine Threads and Comments as Research

A viral explainer is a lead, not an authority. When a thread influences the
strategy:

1. Capture the original claims and links without accepting the framing.
2. Read the Community Note, substantive replies, quote posts, counter-threads,
   and later posts from the same authors.
3. Classify each useful item as source, interpretation, correction, question,
   anecdote, or unsupported repetition.
4. Follow file paths and citations back to the current official repository or
   documentation. Prefer exact versions over screenshots of code.
5. Search for later corrections and upstream commits. A correction should
   supersede the original claim in the record rather than disappear from the
   history.
6. Turn unresolved audience questions into research or content ideas, not facts.

Public explainers and counter-threads often correct themselves after upstream
documentation changes. Treat such a correction as evidence for this update
method, not as a reason to discard platform research.

## Update Workflow

Recheck the snapshot when a consequential X strategy is created, when X ships a
recommendation or policy change, when observed behavior materially conflicts
with the playbook, or at least quarterly while the playbook is actively used.

1. Record the newest official commit or documentation version and verification
   date.
2. Diff ranking parameters, scorer semantics, filters, enforcement rules, and
   the repository's stated omissions against the recorded version.
3. Revisit secondary explainers, Community Notes, counter-threads, and author
   corrections only after checking primary sources.
4. Update the snapshot and implications separately. Do not rewrite a durable
   principle merely because one coefficient changed.
5. Mark replaced claims as superseded with the replacement source.
6. Reopen cadence, format, or relationship tactics only when the change affects
   the current account objective or observed results.

If current primary evidence cannot be checked, say which snapshot is being used
and lower confidence instead of presenting it as current fact.
