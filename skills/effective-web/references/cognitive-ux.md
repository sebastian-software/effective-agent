# Cognitive UX

Design for the attention, prior knowledge, and decision capacity people actually
bring to a task. Do not treat cognitive load as a synonym for visual minimalism.
Reduce unnecessary interpretation and switching while preserving the capability,
context, and choice required to complete the job.

## Start with the user's available attention

- Assume attention may already be reduced by the environment, device
  notifications, worry, pain, fatigue, time pressure, or unfamiliarity.
- Identify what the person must notice now, what may wait, and what must remain
  available without competing for focus.
- Interrupt only for time-sensitive risk, irreversible loss, or a result the
  person would otherwise miss. Let routine software complete its job and recede.
- Keep the primary task stable across loading, validation, and recovery. Avoid
  layout shifts, focus jumps, surprise dialogs, and decorative motion that force
  people to rebuild their place.
- Test consequential flows in distracting, narrow, zoomed, slow, and interrupted
  conditions instead of assuming quiet desktop focus.

Do not demand sustained attention merely because the interface can capture it.
Attention is a user resource, not a product metric to maximize.

## Design for satisficing without manipulating it

People often choose the first option that appears suitable, especially when the
task is routine or their attention is depleted.

- Make the most useful likely action easy to recognize, not merely the most
  profitable action or the outcome the business wants to force.
- Keep viable alternatives legible and reachable. A strong primary action must
  not turn secondary choices into hidden or low-contrast traps.
- Prefer recognition over recall: expose relevant objects, labels, recent values,
  examples, and next actions rather than requiring memory of commands or prior
  screens.
- Provide enough information for a safe decision at the point of action. Move
  optional explanation behind progressive disclosure, not essential risk or cost.
- Increase deliberation deliberately for destructive, expensive, legal, or
  safety-relevant decisions. Do not optimize high-consequence work for reflexive
  completion.

## Group around the task

Categorize information and capability through the user's current goal, not only
through the backend taxonomy or team structure.

- Group objects that serve the same task even when their implementation differs.
- Use modes when a complex product has genuinely different task environments,
  tools, or attention needs. Give each mode a clear name, purpose, entry, exit,
  and current-state indicator.
- Let people create or adapt categories when their repeated work does not fit a
  stable product taxonomy. Preserve useful defaults without forcing every user
  into the team's information architecture.
- Preserve shared objects, global actions, undo, navigation, and terminology
  across modes so categorization does not fragment the product.
- Avoid modes for minor filters or presentation choices. Prefer local controls
  when the underlying task and action set stay the same.
- Validate categories with observation, search behavior, support questions, and
  sorting exercises. Do not assume the team's categories match user expectations.

## Build visual relationships before containers

Establish grouping with the lightest effective signal.

1. Use proximity to place related labels, controls, feedback, and content closer
   together than unrelated material.
2. Use continuity and alignment to preserve a predictable scan and reading path,
   including when errors or helper text appear.
3. Use similarity for elements with the same role or behavior.
4. Break similarity or alignment only to communicate a real semantic exception,
   such as a destructive action or changed state.
5. Add a common region, divider, elevation, or card boundary only when spacing
   and alignment cannot make the relationship clear.

Treat contrast as magnitude, not an on/off property. First establish an
accessible, readable baseline for the least prominent useful content. Add size,
weight, color, shape, position, depth, or motion to express stronger hierarchy;
never reduce essential content below the baseline to make something else stand
out. Remember that motion is unusually forceful contrast and use it sparingly.

## Make the interface speak a shared language

Use conventions as the grammar of interaction, then apply signifiers that answer
three questions for every important element:

1. What is this?
2. What can I do with it?
3. What is happening now?

- Preserve native semantics and familiar behavior before styling a novel visual
  expression.
- Keep labels when an icon, gesture, or metaphor is not reliably recognized by
  the target audience.
- Make hover, focus, pressed, selected, loading, success, disabled, and error
  states perceptibly different without relying on one sensory channel.
- Do not style non-interactive content like a control or hide interaction behind
  an unexplained visual treatment.
- Use real-world metaphor only when it clarifies the system for this audience.
  Do not stretch a metaphor once it hides important capability or creates false
  expectations.

Convention does not require visual sameness. Keep the recognizable identity,
behavior, and state cues, then vary shape, material, or composition within those
constraints.

## Use surprise deliberately

Surprise is a mismatch between prediction and result, so it consumes attention
whether it feels pleasant or frustrating. Treat it as salience, not a default
ingredient for delight.

- Keep costs, privacy effects, destructive consequences, navigation, saved
  state, and the outcome of routine actions unsurprising.
- Put novelty in expression, character, or a low-risk moment after the result is
  understood; preserve conventional identity, action, and recovery.
- Match magnitude to context. A small visual variation may add character while
  a novel interaction can force someone to stop and rebuild their model.
- Do not depend on novelty for repeated motivation. It fades with exposure and
  escalating it creates distraction rather than durable value.
- Validate surprising moments with the relevant audience. Preference for
  predictability varies with task, familiarity, attention, and individual
  experience.

When a new capability must violate an expectation, make the benefit legible,
preview what will happen, provide safe practice or undo, and use the result to
teach a reusable model.

## Map system, designed, and mental models

Before simplifying a complex product, distinguish three layers:

- **System model:** the objects, rules, states, data flow, permissions,
  constraints, and consequences that actually exist.
- **Designed model:** the interface and interaction layer through which people
  inspect and change that system.
- **Mental model:** the beliefs and expectations a person forms from the designed
  model plus prior experience.

Do not hide system capability merely to make the first screen look simple. Match
the designed model to the depth of control the audience needs. When novice and
expert work differ, consider compatible views, direct manipulation plus
shortcuts, or progressive disclosure over one compromised interface.

Audit whose experience defines the team's supposedly typical user, object, or
workflow. Prototypes and conventions are learned from repeated exposure; they
can encode stereotypes, exclude legitimate variants, and make familiar team
assumptions look universal. Test category boundaries and important expectations
across relevant differences in experience, identity, ability, and context.

For every important mismatch, document:

```text
current expectation -> unfamiliar concept or interaction -> attainable benefit
```

Name whether the gap comes from the underlying system, the designed interface,
or both. Preserve a conventional path when possible, then teach the more capable
path in context. Do not require people to cross a learning gap whose benefit is
unclear or marginal.

## Make exploration safe

People learn an interface by acting, observing the result, and adjusting their
mental model. Protect that loop instead of punishing imperfect actions.

- Prefer undo, soft deletion, history, drafts, and reversible state changes over
  repeated confirmation dialogs. Reserve irreversible deletion for cases where
  the underlying data truly cannot be retained.
- Communicate the current state, accepted action, result, and available recovery
  immediately. Do not make people guess whether they are viewing or editing,
  whether work is saved, or whether an action succeeded.
- Keep a person anchored to the originating context when they inspect or edit a
  related object. Use an adjacent panel, preview, or reversible drill-in when a
  full navigation would make them reconstruct their place.
- Add friction in proportion to the user's potential harm. Slow an irreversible,
  expensive, or high-risk action with consequence-specific confirmation; keep
  routine and reversible work fluid.
- Never add protective-looking friction to prevent cancellation, unsubscribe,
  removal, export, or another outcome that only harms the business. Friction is
  justified by user risk, not retention pressure.
- Offer focus modes or collapsible chrome when the person signals a narrow task.
  Do not remove context or capability by default merely to make the screen look
  simpler.

## Decide what deserves learning

Make routine, infrequent, or high-stress actions recognizable without training.
Reserve learnability for capability whose repeated value justifies practice.

- Capture attention without distraction, organize the new concept into existing
  knowledge, and give it a meaningful context.
- Chunk related steps and expose stable landmarks rather than presenting a long
  tour or an arbitrary sequence of tips.
- Teach at the moment of need with examples, previews, safe practice, and undo.
- Use first-run onboarding to establish capability and expectations, not to
  teach detailed actions before the surrounding interface and user intent exist.
- Split guidance into small, contextual modules that appear when behavior
  indicates relevant intent. Keep guidance dismissible, replayable, and
  discoverable after the first session.
- Repeat the same pattern for the same action. Do not create a unique interaction
  for each surface and then call the product learnable.
- Support retrieval with visible cues, recent history, command discovery,
  shortcuts shown beside actions, and contextual help.
- Do not require memorization for tasks people perform rarely. Automaticity only
  develops through meaningful repetition.
- Let onboarding be skipped, resumed, and rediscovered. Measure successful task
  completion and later independent use, not tour completion.

Choose the teaching pattern from the learning need:

| Need | Pattern | Boundary |
| --- | --- | --- |
| A local, unfamiliar action | A contextual hint or example beside that action | Avoid interrupting an unrelated task |
| A worthwhile multi-step capability | An optional, retrievable guide through a real task | Explain actions as people use them, rather than requiring recall of a launch tour |
| A novel interaction or consequential workflow needs practice | A clearly identified sandbox, preview, or reversible rehearsal | Make practice effects distinct from live changes |

Repair unclear labels, affordances, and flow before adding instruction. A
screen-by-screen introduction is not evidence that users can perform the task;
some genuinely novel capabilities need teaching, while familiar ones do not.

## Review checklist

- What is already competing for attention in the real use context?
- Which interruption, choice, or state change forces the user to rebuild context?
- Does salience point to the user's likely best action while preserving autonomy?
- Can people recognize the required object, action, and state without recalling
  another screen?
- Do groups follow the current task and user vocabulary?
- Are proximity, alignment, and similarity doing work that extra containers or
  decoration currently duplicate?
- Does each important control communicate identity, possibility, and state?
- Which system detail is abstracted, and does the abstraction hide capability or
  consequences the audience needs?
- What mental-model gap must be crossed, and is its benefit worth learning?
- Can people see the result of an action, reverse it, and remain oriented to the
  context where they initiated it?
- Is added friction protecting the user from proportional harm or protecting a
  business metric from the user's stated choice?
- Can a distracted first-time user recover while an experienced user remains
  efficient?
