# Personal publications: editorial craft

These examples are observations from a small set of individual publications, not templates
or instructions to imitate their authors. Select a structure for the assignment, the
available evidence, and the contributor's own voice. First-person experience requires a
real source. Never invent it. Titles and closing moves below describe the sampled pieces,
not a rule for every piece by an author.

## Labnotes Weekend Reading

[A sourdough finisher](https://labnotes.org/weekend-reading-a-sourdough-finisher/),
[A server raclette](https://labnotes.org/weekend-reading-a-server-raclette/), and
[More time to write](https://labnotes.org/weekend-reading-more-time-to-write/).

The recurring title prefix identifies the series. The changing subtitle can be whimsical,
topical, or a pun, and need not summarize every item. The newsletter format does much of
the work: recognizable sections such as “Tech Stuff” collect independent links,
quotations, images, and short annotations. Within that structure, Assaf Arkin's personal
selection and commentary provide the voice. An annotation can name the use, audience,
concrete feature, personal reaction, or limitation. It does not need all five. In “A
sourdough finisher,” he qualifies a claimed startup-speed advantage by explaining that the
underlying code still runs on Node. “A sourdough finisher” opens directly with the tech
section. “A server raclette” and “More time to write” first offer a separate entertainment
link. “A server raclette” moves from technical tools through design, people, business, AI,
and security to a miscellaneous section whose last entries include a library story and a
friendly sign-off. The items can range from a single sentence to a quoted passage with
context, and the issue ends with subscription material rather than a forced synthesis.

For a curated digest, make each link earn its place: identify what it offers and add the
one judgment or qualification that helps a reader decide whether to open it. Group items
for scanning, and let the sequence move across subjects without pretending they form an
argument. A hypothetical annotation: “The viewer remembers the filter you used last time. You still need a server to run it.” Attribute recommendations and preserve
source context. A novelty subtitle or joke is optional, and a digest's brevity should not
be confused with a reported assessment.

## David Heinemeier Hansson

[Seven years from China](https://world.hey.com/dhh/seven-years-from-china-a63b03cc),
[The malleable computer](https://world.hey.com/dhh/the-malleable-computer-7c187a9b), and
[Setting the pace](https://world.hey.com/dhh/setting-the-pace-03d4539a).

These titles name a time and place, a central idea, or a practical action. Each makes a different promise. “Seven years from China” proceeds from earlier trips to
recent observations, then moves through factory and transport examples to a geopolitical
argument. It acknowledges the limited view of a short visit and the author's unusual
reception, but still draws ambitious conclusions. It ends by returning to the personal
experience of the visit. “The malleable computer” is much shorter: it states a promise,
identifies a barrier, proposes a change, gives an operating-system distinction and an
example, then closes with a broader prediction. “Setting the pace” begins with a
management principle and grounds it in the six-week practice of the author's company.

A recurring authorial choice is a clear position in the first paragraphs, often with
emphatic language and comparisons. The structure and the confidence are separable: strong
rhetoric does not establish the truth of generalizations, and a founder's interest in a
product or policy is relevant context. The travel piece's caveat does not make a brief,
curated visit representative of a whole country.

State a defensible claim, identify the experience or evidence behind it, and show the
reasoning that connects the two. Where an observation supports only a narrower claim, say
so before extending it. For example, a team proposing a shorter release cycle could trace
three actual releases from merged change to customer availability, identify where review
or deployment caused delays, then explain which delay a proposed weekly release train
would address. State that three releases reveal local bottlenecks rather than proving what
cadence another team should adopt. A short essay can end on an implication. A personal
account can return to its opening experience. Neither requires a combative tone.

For a signed opinion, ordinary speech can carry a strong passage. In a
piece about release trains, a sentence such as “The fix was ready on
Tuesday. We shipped it on Friday because Friday was on the calendar.”
lets the reader hear the frustration and see its cause. Use it only
when the dates and the reason are in the author's account.

## Marco Arment

[Ten years after we lost Steve Jobs](https://marco.org/2021/10/05/steve-jobs-ten-years),
[The future of the App Store](https://marco.org/2021/09/13/future-of-the-app-store), and
[Ten years of Overcast: A new foundation](https://marco.org/2024/07/16/overcast-rewrite).

The sampled titles range from a personal anniversary to a broad forecast to an anniversary
with a specific product-change subtitle. Their forms differ as much as their subjects. The
Jobs remembrance is short, unsectioned, and openly personal: it says the writer never met
Jobs, then explains what the loss meant to him and ends with a sense of unrealized work.
The App Store essay opens with a prediction, enumerates expected rules, and walks through
consequences for users and developers, including hypothetical behavior by named companies. It ends by restating the preferred course. Its predictions and interpretations are
arguments from 2021, not present-day facts. The Overcast announcement leads with the
release, then organizes new features, retained features, removals, next steps, and the
reason for the rewrite. It explains the user-visible consequence of removing streaming and
puts technical detail in a footnote before a note of thanks.

The publication carries the same person's perspective across remembrance, analysis, and
product communication. Their structure is driven by the task. Particularly useful is the
product announcement's willingness to name a loss alongside improvements and explain the
practical effect. His role as Overcast's developer is a source of direct knowledge and an
interest to disclose, not independent verification.

In a release note, lead with what changed, explain what users must now do differently, and
give a reason grounded in the actual implementation. If the evidence exists, separate
future plans from shipped behavior. In a personal remembrance, establish the nature of the
relationship and leave the feeling at its proper scale. For example, if a podcast app
removes streaming because stitched ad breaks can make partial downloads repeat audio,
explain that an episode now downloads before playback starts, describe the expected wait,
and identify any offline or storage implications supported by the release. Do not invent
roadmaps, motives, or personal ties.

## Overreacted

[Goodbye, Clean Code](https://overreacted.io/goodbye-clean-code/),
[The Elements of UI Engineering](https://overreacted.io/the-elements-of-ui-engineering/),
and
[A Complete Guide to useEffect](https://overreacted.io/a-complete-guide-to-useeffect/).

The titles include a farewell to an idea, a map of a field, and a comprehensive technical
guide. In “Goodbye, Clean Code,” a late-night refactoring scene and two code organizations
let the reader understand why the change initially seemed attractive. The next morning
supplies the reversal. The essay then identifies both a collaboration failure and a
technical tradeoff before ending with advice to reconsider the goal of cleanliness. “The
Elements of UI Engineering” instead introduces the author's attempt to articulate tacit
knowledge, catalogs distinct UI problems and tradeoffs, and ends by inviting readers to
experiment on a small interface. The `useEffect` guide is much longer: it returns to
examples, common mistaken mental models, and edge cases as it builds an explanation. Its
closing points back to the opening summary and invites feedback. Its 2019 framework advice
and forecasts are historical. Check current documentation before applying them.

The recurring craft is to make the reader's reasoning visible: demonstrate a plausible
approach, test it against a concrete change or edge case, and revise the model. Questions,
personal mistakes, code, and exercises serve that explanation in different combinations.
They are not required features of every technical article, and a reconstructed or
simplified code example should be labeled accordingly.

Choose an example small enough to follow, demonstrate the tempting solution, then
introduce a specific requirement that exposes its tradeoff. Explain what changed in the
reasoning and offer a next step only if it helps the reader practice. For example, show a
cache keyed by user ID, then add a locale-dependent response and explain why the key must
account for locale. Verify the behavior in the relevant system. Don't invent a failure
story to make the lesson dramatic.
