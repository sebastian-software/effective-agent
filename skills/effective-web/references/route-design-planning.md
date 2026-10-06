# Design Planning

Use this route before implementing a greenfield, ambiguous, high-stakes, or
visually important experience. Establish a specific design intent, structure,
interaction model, and evidence boundary without loading the review and
modernization corpus.

## Use First For

- Planning a new product, brand, content, or marketing surface.
- Choosing the design register, hierarchy, layout topology, density, and
  interaction model before styling.
- Designing AI-assisted features where modality, uncertainty, user control,
  recovery, and handoff matter.
- Turning an ambiguous request into a compact implementation-ready design brief.

For an existing experience that needs critique, preservation-aware
modernization, polish, or final quality gates, switch through [Route by
Intent](../SKILL.md#route-by-intent) to Design Review and Modernization.

## Planning Workflow

1. Reuse the supplied brief and established project context. Inspect relevant
   decisions, screens, content, or system constraints where direction is unclear.
2. Identify the primary user, job, action, failure modes, required states, and
   anti-goals. Ask one discriminating question only when the answer materially
   changes the direction.
3. Use [Design registers](design-registers.md) when the surface purpose is
   unresolved, or [Design directions](design-directions.md) when its visual
   direction needs exploration. Preserve an established direction.
4. Use [Cognitive UX](cognitive-ux.md) when attention, learnability, complex
   modes, unfamiliar concepts, or mental-model mismatch shape the experience.
5. Use [Design planning core](design-planning-core.md) for unresolved hierarchy,
   layout, interaction, density, states, or adaptation decisions.
   If a proposed structure follows a generic page template rather than the
   brief, use [UI anti-patterns](ui-antipatterns.md) to examine that choice and
   retain any justified exception. This is conditional, not a pre-read for
   every new surface.
6. For an AI-assisted feature, use [AI interface
   design](ai-interface-design.md) to choose the smallest fitting modality and
   specify uncertainty, review, cancellation, recovery, and a non-AI path.
7. Produce a compact brief and route implementation details through the focused
   Effective Web routes. Record durable design decisions through
   `effective-product`.

## Rules

- Start from the user's task and product evidence, not a fashionable visual
  preset or chat surface.
- Preserve accepted constraints until they are explicitly superseded.
- Prefer concrete nouns, real content, and required states over adjective-only
  direction.
- Make deterministic work deterministic, especially inside AI-assisted
  experiences.
- Stop planning when the direction is implementation-ready; do not turn the
  route into an iterative polish loop.
