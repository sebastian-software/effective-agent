# Solution Modeling

Translate supported opportunities into competing product systems before
committing to a page inventory. Explore what the product enables, the concepts
it exposes, and how people move through meaningful moments.

## Explore systems, not feature piles

Begin with prioritized problem and empowerment statements, opportunity
questions, design factors, constraints, and non-goals. Generate several ways to
change the situation. A direction may alter information, coordination, timing,
automation, environment, policy, service, or product behavior; it does not need
to begin as a new screen.

For each direction state:

- target situation and desired real-world outcome
- product promise and essential capability
- actors served, underserved, and affected
- system model and important expectation changes
- autonomy, safety, accessibility, privacy, and failure implications
- evidence supporting it and assumptions introduced by it
- smallest prototype or operational test that could disprove it

Compare directions before combining them. A large concept containing every
idea prevents the team from learning which model is understandable or valuable.

## Use a feature canvas as a decision surface

Use a lightweight feature canvas when collaborators need one shared overview of
who the direction serves, why it matters, the benefits expected, the capability
being explored, and how the team will begin. Link each summary back to the
deeper research and problem artifacts rather than duplicating them. Skip the
canvas when the same information is already clear to everyone and it would not
improve a decision or handoff.

When a feature-level concept deserves deeper exploration, document more than
its headline:

1. opportunity, actors, and intended progress
2. evidence and design principles it responds to
3. objects, actions, state, rules, and dependencies involved
4. entry conditions, trigger, and expected result
5. variations, interruptions, empty states, errors, and recovery
6. user control, permissions, privacy, and accessibility implications
7. success and harm signals
8. open questions, exclusions, and prototype plan

Do not treat the canvas as approval. Use it to reveal the cost and consequences
of an idea so the team can narrow, reject, combine, or test it.

## Model objects before pages

Use object-oriented UX for products whose value depends on people creating,
organizing, connecting, viewing, or changing persistent things.

Begin with a noun hunt across the brief, research language, existing product,
and opportunity work. Treat the first list as provisional: merge synonyms,
separate an object from an attribute or view, and add a concept only when it has
recognizable identity, data, behavior, or relationships. When the method is
unfamiliar, reverse-engineer one comparable product first to distinguish its
objects from its screens.

For every core object identify:

- recognizable name and purpose in the user's language
- attributes people need to identify, compare, or act on it
- relationships and cardinality to other objects
- lifecycle and important states
- actions, including who may perform them and under which conditions
- ownership, visibility, permissions, and collaboration rules
- creation paths, defaults, validation, deletion, restoration, and history
- representations at different densities and in different contexts

Separate an object from a view of that object. A project may appear in a list,
calendar, search result, notification, relationship panel, and detail view
without becoming six unrelated concepts. Derive navigation and components from
the object and relationship model rather than letting the first screen sketch
define the domain.

Also distinguish a reusable definition or template from its concrete instances:
a recurring inspection plan from a completed inspection, or an appointment
series from one occurrence. Before designing edit and delete controls, clarify
whether an action changes the definition, one instance, future instances, or
existing records. Make propagation, exceptions, and historical meaning explicit
instead of letting a shared label imply that these are the same object.

Probe relationships pairwise: how could object A appear meaningfully within B,
and how could B appear within A? Also test an object against itself, such as
related items, versions, dependencies, or collections. Keep only relationships
that support a real decision or action; the exercise is a way to discover
organic capability, not a requirement to connect everything.

## Map moments

A moment is a situated interaction with a purpose, entry condition, relevant
objects, and consequence. List moments before arranging an end-to-end flow:

- orient or resume
- capture or create
- inspect or compare
- organize or connect
- collaborate, hand off, or request input
- decide, commit, publish, or submit
- notice change or receive feedback
- correct, undo, restore, or recover
- reflect, learn, or adapt the environment

Classify important moments as one-off or rare setup, repeated core activity, and
first-time versions of repeated activity. The same action may need contextual
teaching on first use and become a compact expert interaction later. Compare
moments by user impact and expected intuitiveness: keep high-impact familiar
work fluid, plan guidance or exploration for high-impact unfamiliar work,
minimize low-impact administration, and challenge moments that are both hard to
understand and low value.

For each moment specify context, motivation, attention available, object state,
actions, feedback, exit, and likely interruption. This exposes important
nonlinear access points that a single happy-path journey hides.

## Turn moments into flows

Connect moments only where order or causality matters. A moment flow should
show:

```text
entry and preconditions -> decision or action -> state change and feedback
                        -> branch, recovery, exit, or next meaningful moment
```

Include permission failures, concurrency, empty data, cancellation, return
after interruption, undo, and downstream effects. Preserve context and a way
back when a focused subtask opens from an exploratory environment.

For a complex moment, block out a few purposeful stages before individual
screens or decisions. Define the triggering action and the materially changed
ending state. The flow should hand people back to an understandable environment
with renewed choice, not silently extend one constrained funnel into the rest
of the product. Make optional setup genuinely skippable and available later.

Use a linear path for a known outcome whose order protects correctness, safety,
or speed. Use a network of moments when people may validly begin, organize, and
progress in different ways.

## Use journeys to check the whole experience

A journey connects product moments with the wider situation over time. Include
the trigger before product contact, current alternative, expectations, access,
core activity, interruptions, support, result, and later reflection. Show what
the person is doing outside the interface and how responsibility moves between
people or systems.

Annotate confidence and source evidence. Journeys based only on imagined future
use are scenario hypotheses, not research findings. Use them to plan a
prototype, service handoff, or further study—not as proof that the experience
works.

## Solution-model deliverable

Provide:

- two or more directions and their tradeoffs
- chosen promise, design factors, and non-goals
- feature decisions and unresolved hypotheses
- actor, object, relationship, permission, and state model
- moment inventory and critical moment flows
- end-to-end journey in real-world context
- failure, recovery, accessibility, and autonomy review
- prototype questions and decision criteria
