# Editorial approaches from engineering publications

A tutorial can turn on one button. A migration report may need the whole
maintenance window. These readings follow the technical detail that makes
each story worth the reader's time.

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

Comeau gives readers something they can decide before giving them the
vocabulary to defend the decision. Try that with a cache. Show two stale
values of exactly the same age: a decorative badge and an account balance.
Which one would the reader ship? Having chosen, they now have a reason to
care how the application invalidates a value.

In a keyboard tutorial, ask which button the reader expects to reach next.
Show which button actually receives focus. The outcome gives the term in
the next paragraph a job even if the reader cannot run the demo.

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

For an article about deployment checks, take one change through a unit
test and an integration test. How long before the failure appears? How
much work does it take to find its cause? A small model becomes useful at
the moment it gives two competent engineers a reason to choose differently.

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

Give a layout article a request ID long enough to push the filter panel
off screen. A feature explainer can invite the reader to resize the panel
and watch the point where the rule gives way. A columnist can use that
same screenshot to explain why a once-favorite rule has lost its appeal.
The visible consequence earns either piece its claim.

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

The interesting number in the migration is the distance between two runs.
The team needed to schedule a window. A reader can grant both that the
faster machine was fast and that booking the maintenance window would
have been a poor bet. Carry the comparison that far in your own story.
Supply the workload and the machines, then name the decision that depended
on the spread. A team choosing to stay put has a perfectly good ending.
