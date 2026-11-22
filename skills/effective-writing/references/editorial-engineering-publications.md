# Editorial approaches from engineering publications

Use this reference when planning or revising a technical article. It describes observed
editorial choices, not a recipe for copying a writer's voice. Choose a structure for the
reader's problem and use evidence from the actual work. The sources below were read in
November 2026. Product capabilities, browser support, and specifications may have changed
since publication.

## Josh W. Comeau

Comeau's individually authored articles often make a broad CSS question tangible before
introducing an explanation. In
[A Framework for Evaluating Browser Support](https://www.joshwcomeau.com/css/browser-support/),
an apparently reassuring support percentage becomes a decision about the fallback
experience, the audience, and the harm of failure. A cosmetic wrapping enhancement and an
overflowing image that obscures text give the reader two different outcomes to compare. He
then applies the framework to his own blog, labels an audience estimate as rough, shows
the fallback, and ends by acknowledging that judgment remains necessary.

[The Undeniable Utility Of CSS `:has`](https://www.joshwcomeau.com/css/has/) develops
several uses of a feature, including a keyboard-focus problem from his own site. It also
flags browser support before the demonstrations.
[A Modern CSS Reset](https://www.joshwcomeau.com/css/custom-css-reset/) works differently:
it assembles a reusable starting point and explains individual rules through examples,
including box-model arithmetic and an interactive editor. Its changelog records
corrections and changes over time.

Titles in this small sample range from a named decision framework to an enthusiastic
feature claim and a practical reusable artifact. They signal the reader's payoff without
requiring one fixed title pattern. Interactive examples, diagrams, and accessible
fallbacks are part of the explanation where available. Prose should still explain the
outcome if a demo is unavailable.

For a caching article, start with two concrete failures: an outdated decorative badge and
an outdated account balance. Explain why the same cache age has different consequences,
then give readers a way to choose an invalidation strategy. If the numbers are estimates,
say how they were obtained and where they may mislead.

A useful change of pace in a tutorial is to let the reader make a choice
before supplying the vocabulary. For example, ask which of two buttons
a keyboard user would reach next, then show what receives focus. The
answer gives the term in the next paragraph a job.

## Kent C. Dodds

[Introducing Kody: Your Personal Software Factory](https://kentcdodds.com/blog/introducing-kody-your-personal-software-factory)
is a product launch, not an independent review. It opens with social posts and a poll
about recurring problems, groups those problems into a product rationale, explains the
offering and personal use, and ends with an invitation to try it. Its strong safety and
performance claims are the creator's claims. The article itself is not a substitute for
independent validation.

[The Testing Trophy and Testing Classifications](https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications)
traces a teaching model through earlier posts and discussions.
[Static vs Unit vs Integration vs E2E Testing for Frontend Apps](https://kentcdodds.com/blog/static-vs-unit-vs-integration-vs-e2e-tests)
uses a painting-tool analogy, describes the categories, and weighs confidence, speed, and
cost with examples. It supplies text for a visual model for readers using assistive
technology or missing the image. The launch's problem-to-invitation arc differs from the
testing articles' explanation and comparison.

The titles include a product introduction, a named conceptual model, and a direct
comparison. The byline and site establish a personal teaching perspective. The product
announcement also carries a direct commercial interest. A model can organize a discussion
without making its categories universal or its recommendations automatically right for
every project.

In an article about deployment checks, introduce a small model with three costs: time to
detect a problem, cost to run the check, and cost to investigate a failure. Walk one
change through each option. Explain where the model stops helping, such as when a
regulatory requirement determines the check.

## Piccalilli

Piccalilli publishes named contributors with different voices. Mat Marquis's
[Understanding CSS random()](https://piccalil.li/blog/understanding-css-random/) starts
with the practical and visual reason for adding variation to margin notes, then moves into
syntax, seed sharing, scope, and progressively more complicated examples. The ending
returns to the original experiment. Its playful personal narrative is specific to that
author and article.

Andy Bell's
[Building a breakout element with container units](https://piccalil.li/blog/building-a-breakout-element-with-container-units/)
begins with a site layout constraint, explains why viewport units are insufficient, and
builds the solution around a container. His
[If it works, it’s right](https://piccalil.li/blog/if-it-works-its-right/) is an opinion
piece responding respectfully to another author: it explains his own flexible-layout
preference while allowing for different team needs. Saleh Mubashar's
[Native masonry layouts with CSS grid lanes](https://piccalil.li/blog/native-masonry-layouts-with-css-grid-lanes/)
instead gives standards history, compares proposals, explains the layout algorithm with
examples, and discusses accessibility and evolving support.

These titles range from an explanatory feature name to a building task and a position. The
publication's shared subject does not imply a single authorial voice, level of formality,
or narrative length. New CSS features and standards histories are time-sensitive: date
claims and recheck current specifications before reuse.

Explain a log viewer's layout by showing the actual constraint first: a long request ID
must remain readable beside a narrow filter panel. Show a minimal layout, explain the rule
that controls overflow, then show what happens when the panel is resized. An opinion piece
about layout philosophy would need a different structure and explicit reasons for its
recommendation.

A feature explainer and an opinion column can use the same CSS declaration
in different ways. The explainer can pause and ask the reader to change
one value. The columnist can show the one layout that made a once-favorite
rule hard to defend. In both, spend a sentence on what someone actually
sees when the viewport shrinks.

## Evil Martians

Martian Chronicles uses named, sometimes multiple bylines, including engineers and a
technical editor.
[We stopped a Railway migration 3 weeks out. How to know to stop or go?](https://evilmartians.com/chronicles/we-stopped-a-railway-migration-3-weeks-out-how-to-know-to-stop-or-go)
by Ilya Cherepanov, Kirill Kuznetsov, Kirill Yakovenko, and Travis Turner opens with the
decision and its stakes. It reports that the same database import took 71 minutes on one
service and 382 on another. The table names the infrastructure used for each run:
one ran on a VM and the other on physical hardware. That detail limits what the
timings can prove and explains why the team cared about predictability. The authors
also identify workloads for which they would recommend the platform.

[The Whop chop: how we cut a Rails test suite and CI time in half](https://evilmartians.com/chronicles/the-whop-chop-how-we-cut-a-rails-test-suite-and-ci-time-in-half),
by Igor Platonov and Travis Turner, leads with a client result and follows the
investigation: profiling a sample surfaced database activity, external calls, and logging.
The article then shows the configuration changes and other work.
[Don't bet on SELECT's order: shuffle your rows and see what folds](https://evilmartians.com/chronicles/dont-bet-on-select-order-shuffle-your-rows-see-what-folds),
by Yaroslav Kurbatov and Travis Turner, starts with a specific hidden assumption, explains
why physical row order can change, and describes experiments and a tool for exposing
dependencies.

The titles use a consequential decision, a measured outcome, or a technical risk and
action. Case studies and tool articles have different evidence and endings. The firm's
service promotion is part of the publication context. A reported result belongs to its
workload and measurement method, not every reader's system.

For a migration post, state the scheduled decision and the constraint first. Show a small
table of test runs, environment, data size, and duration. Explain what was measured and
what remained uncertain. End with the decision, the conditions that would change it, and
the operational consequences. Do not invent measurements to make the story more dramatic.

## Apply the craft

- Choose an opening that earns the reader's attention: a decision, an observed failure, a
  real constraint, or a question the article can answer.
- Develop the argument with a sequence of examples that changes one relevant variable at a
  time. Explain why the result matters before adding more detail.
- Make judgments attributable and proportionate: separate a measurement, a person's
  observation, a vendor claim, and the author's recommendation. Include the cases where
  the recommendation changes.
- End according to the assignment: a decision and its conditions, a usable technique and
  limits, an open question, or a product invitation. A launch's call to action is not a
  requirement for a tutorial.
- Use original examples and the contributor's own experience. Do not copy signature
  phrases, humor, personal anecdotes, sentence rhythms, or a publication's branding. Test
  code and technical claims against current primary documentation.
