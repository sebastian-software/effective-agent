# Design Directions

Choose a direction after selecting the surface register. The register describes
the interface's job; the direction describes how it should feel and behave.
Do not treat product, landing page, minimalist, playful, and premium as competing
values at one level.

If no direction has been accepted yet and the task needs competing experience
concepts rather than a compact implementation brief, use the visual-character
exploration in the `effective-product` skill's structure-and-prototyping reference
(when that skill is installed) first. Translate the chosen evidence and
qualities into the Design Read below; do not invent a separate browser-only
direction.

## Contents

- [Design Read](#design-read)
- [Independent Axes](#independent-axes)
- [Compare the Open Decision](#compare-the-open-decision)
- [Direction Profiles](#direction-profiles)
- [Conflict Resolution](#conflict-resolution)
- [Persistence and Drift](#persistence-and-drift)

## Design Read

Before a net-new or materially redesigned surface, state a compact internal or
user-visible read:

```text
Surface: [operate / persuade / read / experience]
Audience: [specific people and context]
Primary job: [task, decision/action, understanding, or encounter/exploration]
Direction: [one primary direction plus an optional secondary influence]
Expression: [restrained / balanced / expressive]
Density: [sparse / normal / dense / data-heavy]
Motion: [static / functional / expressive]
Depth: [flat / borders / surface shifts / subtle shadows / layered]
Communication: [relationship, form of address, voice, and tone constraints]
Signature: [one product- or subject-specific element]
Avoid: [the category default or wrong direction]
```

Infer this from the prompt, accepted ADRs, existing product, design system,
content, and code. If one missing answer would materially change the direction,
ask one concise question. Do not conduct a design interview when a responsible
assumption is available; state the assumption and proceed.

Useful questions distinguish real branches:

- Is this a repeated operational task for experienced users, or a surface that
  must win trust and interest from occasional visitors?
- Should the relationship feel like an expert peer, a reassuring guide, a
  formal authority, or an energetic host?
- Must users compare and act quickly, or should they explore and absorb a story?

Do not ask empty preference questions such as "modern or clean?".

## Independent Axes

- **Expression:** restrained to expressive. Controls contrast, composition,
  imagery, typography, and the number of memorable moments.
- **Density:** sparse to data-heavy. Follows task frequency, comparison needs,
  content volume, and device constraints rather than prestige.
- **Warmth:** clinical or distant to personal and approachable. Appears in
  colour temperature, shape, imagery, copy, and feedback.
- **Precision:** interpretive to exact. Appears in alignment, terminology,
  numerical presentation, interaction predictability, and state clarity.
- **Motion:** static to functional to expressive. Match motion to purpose and
  usage frequency; always preserve a complete reduced-motion path.
- **Materiality:** flat to layered. Choose one coherent depth strategy instead
  of mixing borders, glass, diffuse shadows, and nested enclosures everywhere.

"High-end" is not the opposite of "minimalist". High-end describes execution
quality and may imply premium materiality or art direction; minimalism describes
restraint. A precise premium-minimalist landing page is coherent. A dense
analytical console with cinematic scroll choreography usually is not.

## Compare the Open Decision

When composition is still open, compare alternatives that change a meaningful
relationship: the leading evidence, navigation structure, grouping, or density.
Keep the task, content, and constraints comparable so a preferred direction is
more than a reaction to different material. Compare task use as well as visual
appeal before refining the strongest ideas.

If the open decision is only a typeface or palette, targeted variants are
appropriate; do not reopen an accepted layout to manufacture difference. There
is no required variant count. Use the `effective-product` exploration described
in the introduction when the alternatives change the broader experience.

## Direction Profiles

Use profiles as starting hypotheses, not fixed palettes or component recipes.
Combine one primary profile with at most one secondary influence.

### Precision and Analysis

Use for finance, analytics, engineering, monitoring, regulated operations, and
decision support where users compare evidence and exceptions.

- Prefer dense but ordered information, strong alignment, tabular numbers,
  explicit states, and restrained semantic colour.
- Let hierarchy, grouping, and data shape create identity; do not decorate the
  surface like a campaign.
- Keep motion brief and functional. Avoid ambiguous metaphors, playful failure
  copy, atmospheric backgrounds, and novelty controls.

### Utility and Operations

Use for admin tools, internal systems, settings, queues, and repeated workflows.

- Prefer familiar controls, predictable navigation, compact spacing, visible
  batch actions, recoverability, and keyboard efficiency.
- Use the product's real objects, verbs, permissions, and process stages instead
  of generic dashboard cards.
- Keep the interface quiet. Earn delight at completion or helpful recovery, not
  on every page load.

### Warmth and Approachability

Use for consumer products, collaboration, onboarding, care, education, and
services where reassurance and relationship matter.

- Use generous but not wasteful spacing, human imagery or illustration, clear
  guidance, forgiving interaction, and supportive feedback.
- Warmth may coexist with professional precision. Avoid forced informality,
  childish shapes, vague reassurance, or humor in high-risk states.
- Align copy with recorded communication decisions: proximity, form of address,
  vocabulary, and channel-specific tone are part of the same direction.

### Editorial Minimalism

Use when hierarchy, reading, product evidence, or a small number of objects can
carry the experience through restraint.

- Let typography, measure, alignment, whitespace, and real content do most of
  the work. Use scarce accents and modest component geometry.
- Treat every visible element as intentional. Minimal does not mean unlabeled,
  undiscoverable, low-contrast, image-free, or incomplete.
- Avoid applying sparse marketing rhythm to dense operational tasks that need
  comparison and scanning.

### Premium and Cinematic

Use for launches, premium consumer brands, portfolios, cultural work, and other
surfaces where perceived craft and atmosphere materially affect the outcome.

- Choose one strong material, media, typographic, spatial, or motion signature;
  keep supporting elements disciplined.
- Vary section rhythm when the narrative earns it. Use real or commissioned
  media rather than fake product screenshots or abstract filler.
- Bound blur, layered effects, continuous motion, and overlapping layouts for
  mobile performance, accessibility, and reduced transparency or motion.
- Do not equate premium with cream, serif type, glass pills, giant whitespace,
  nested borders, or constant animation.

### Bold and Playful

Use for expressive consumer experiences, entertainment, youth-oriented brands,
events, or campaigns where energy and discovery are part of the value.

- Commit to a controlled visual idea through colour, type, shape, interaction,
  illustration, or copy. Make the play specific to the subject.
- Preserve hierarchy, task completion, readable copy, target sizes, and a calm
  fallback. Do not let every element compete or move.
- Remove playfulness from destructive, legal, security, payment, and serious
  error states unless the brief provides a compelling reason.

## Conflict Resolution

When directions pull against each other:

1. Let the primary user job and harm of failure decide the baseline.
2. Let the primary direction own layout, density, interaction, and default tone.
3. Apply the secondary influence locally through colour, imagery, copy, an
   earned moment, or one signature element.
4. Prefer state- or section-specific variation over averaging incompatible
   directions into a vague middle.

Examples:

- A friendly finance app remains precise in tables, money, errors, and approval
  flows; warmth appears in onboarding, guidance, and recovery.
- A premium admin product remains efficient and dense; premium craft appears in
  typography, proportion, surface discipline, and a few transitions rather than
  cinematic page choreography.
- A playful consumer service becomes sober for account recovery, consent,
  payment failure, and irreversible actions.

## Persistence and Drift

Read accepted ADRs before selecting a new direction. When a project establishes
or changes a durable register, audience relationship, direction, density,
motion, depth, or cross-channel communication choice, use `effective-product` to
record the rationale, rejected options, consequences, and review triggers.

Keep exact colours, spacing, radii, durations, component props, phrase libraries,
and campaign copy in their owning systems. During review, compare the rendered
surface, design tokens, components, and language against the accepted decision;
fix accidental drift or explicitly supersede the ADR when the direction changed.
