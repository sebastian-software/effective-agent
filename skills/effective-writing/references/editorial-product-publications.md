# Editorial product publications

Read these nine pieces as accounts from people close to the product. Look for
the information a maker can give a reader firsthand, especially a discarded
design, a customer question, or a trace from the old implementation.

## iA

- [It Takes Two to Duo](https://ia.net/topics/it-takes-two-to-duo) is a short, playful
  product announcement. Its title makes a pun on the device name. The subtitle supplies
  the missing subject. It opens with the hardware change and the apps' adaptation, recalls
  Writer's original typewriter concept, then shows presenting from a pocket and controls
  moving within a thumb's reach. Images carry much of the demonstration. It closes with an
  invitation to try the products. The page speaks as the company, without a named
  individual byline.
- [Search to Navigate](https://ia.net/topics/search-to-navigate) names an action and
  explains the feature in its subtitle. It begins with a release fact, then reframes
  search and navigation as questions a writer asks while working. Screenshots, keyboard
  shortcuts, and three selected changes make the claim tangible. Footnotes preserve design
  qualifications. Its ending gives an immediate action and platform availability. It is a
  company-voice release, not an independent evaluation.
- [Making Icons Fresh](https://ia.net/topics/making-icons-fresh) uses a short evocative
  title and a subtitle that states the tension. It begins by acknowledging attachment to
  familiar icons. A visual history, discarded variants, and the difficulty of reconciling
  two app icons show decisions over time. This longer design narrative can dwell on
  uncertainty and the team's own attachment because the process itself is the story.

A control moving within reach of a thumb says what a small screen changes
for the person holding it. In a design story, let a short sentence direct
the eye before explaining the geometry. For a hypothetical screenshot
pair: “Try closing the drawer with your thumb. In the first version the
button is on the far side of the phone.” Now the second image gets a chance
to answer. A rejected layout can do the same job in a longer design essay.

## Tailwind CSS

- Adam Wathan's
  [Tailwind UI is now Tailwind Plus](https://tailwindcss.com/blog/tailwind-plus) states
  the change in the title and opening. It immediately addresses existing customers' likely
  concerns: pricing, upgrade costs, and access. Only then does it explain why the name
  changed and list possible additions, explicitly noting that some ideas may never ship.
  It ends in a personal expression of excitement rather than a technical recap.
- Wathan's [Tailwind CSS v4.0](https://tailwindcss.com/blog/tailwindcss-v4) opens with a
  candid, emphatic release announcement, then gives a feature inventory and upgrade paths.
  The performance section supplies a benchmark table and distinguishes full builds,
  rebuilds with new CSS, and rebuilds without new CSS. Code examples explain features in
  use. Its breadth and long list serve a major-version release. They are not a model for
  every article.
- Philipp Spiess and Wathan's
  [Vanilla JavaScript support for Tailwind Plus](https://tailwindcss.com/blog/vanilla-js-support-for-tailwind-plus)
  starts with a specific gap for users outside React and Vue. It introduces the new
  Elements library, shows substantial HTML and framework examples, identifies native
  platform primitives and polyfills, and closes with links to try the components. The
  named authors and conversational enthusiasm are part of a maker's release note.

The rebrand has an unusually satisfying first question. Does someone who
already paid have to pay again? For a fictional product with a new name
and the same lifetime license, a single sentence would do: “If you already
own the old edition, you own this one too.” The brand history can wait.

The version announcement earns a longer middle. A full build and a rebuild
that generates no new CSS ask different things of the tool. Keep the
workload beside the time so the reader can find the case they run daily.

## Vercel

- [Introducing eve 1.0](https://vercel.com/blog/eve-is-now-generally-available), credited
  to Andrew Barba and eight colleagues, opens with general availability and a compact
  account of the changes. Task-oriented sections explain the agent harness, collaboration,
  tracing, performance, and setup. It mixes customer examples and testimonials with code,
  a benchmark table, workload assumptions, an upgrade guide, and first-run commands. Its
  ending offers several concrete ways to start. The mock model replies
  immediately in the turn-latency test. That detail explains which part
  of the wait the benchmark can measure.
- Matthew Stanciu and Tim Caswell's
  [How we made global routing faster with Bloom filters](https://vercel.com/blog/how-we-made-global-routing-faster-with-bloom-filters)
  titles the mechanism and outcome, then leads with memory and tail-latency improvements.
  It follows a request through path lookup, explains why large JSON files block the event
  loop, and introduces the filter's false-positive/false-negative tradeoff. Diagrams and
  measurements make the mechanism inspectable. Its engineering byline and
  problem-to-solution sequence support a narrower technical explanation than the launch
  post.
- Tim Caswell, Steven Salat, and Luba Kravchenko's
  [How we cut CDN metadata lookup latency by 91%](https://vercel.com/blog/how-we-cut-cdn-metadata-lookup-latency-by-91-percent)
  puts a numerical result in the title, then establishes the request and metadata context.
  Concrete route examples, cache behavior, and diagrams explain why grouping metadata into
  bounded shards changes lookup behavior. It builds on the prior Bloom-filter work rather
  than treating the new optimization as an isolated trick.

Trace one request in a performance story. Which process opens the file,
which lookup waits, and what can the new index skip? Once a reader can
follow the request, the result in the headline has a mechanism behind it.
A customer describing the wait supplies another kind of evidence. The two
can sit happily in the same article when readers know which is which.

## Apply this to an engineering blog

For a hypothetical article about reducing a build cache's repeated downloads,
begin with the actual developer symptom: a rebuild downloads unchanged
dependencies after a branch switch. Explain the previous cache key with one
small example, show why the branch name invalidated otherwise reusable
entries, then show the revised key and its correctness boundary. Include a
before-and-after trace and a measured workload if available. State what was
measured, the comparison, and any regressions. Close with what readers can
do, or with the unresolved tradeoff if this is an investigation rather than a
release. The example is illustrative, not a claim about an existing system.

Choose the title to match the evidence: a plain change announcement for a release, a
mechanism-and-result title for a verified engineering result, or a question for an
unresolved investigation. Give the reader a concrete action or decision early, let the
amount of explanation follow the difficulty, and distinguish observation, attribution,
inference, and future intent. Do not manufacture usage numbers, quotes, screenshots,
measurements, or certainty to reproduce a publication's effect.
