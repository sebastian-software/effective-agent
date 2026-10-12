# Design Planning Core

Decision rules for planning UI before writing code, so the first implementation
is specific instead of a generic first draft. Load the deep
[design-planning.md](design-planning.md) appendix for the full treatment:
design-intent/browser-evidence protocol, bounded-prototype lifecycle, the
complete pre-code question bank, each adjustment lens in detail, earned delight,
review/change contracts, and the full brief and readiness templates.

Plan when the request is net-new, ambiguous, high-stakes, or visually important.
Skip planning for a small change inside an existing, well-understood component.
The goal is not an iterative polishing loop — it is choosing the right register,
structure, and interaction model from the start.

## Use Existing Context

Reuse the brief and project evidence already available. Inspect relevant
decisions, tokens, components, content, or rendered screens to resolve an actual
gap. Preserve accepted constraints unless the user has authorized changing them.
A design artifact still needs validation against the content, viewports, inputs,
and settings affected by implementation.

Resolve three layers without depending on particular filenames:

- **Product truth:** users, facts, content, capability, constraints, and success.
- **Shared visual system:** reusable tokens, components, type, colour, material,
  motion, interaction, and the accepted rationale behind them.
- **Surface contract:** local register, hierarchy, composition, evidence,
  interaction, states, and anti-goals.

Visual authority is evidence, not a filename: missing design documentation does
not make an existing product greenfield. Inspect tokens, components, rendered
screens, and code. Keep product truth and global tokens out of the surface
contract; promote local strategy only with evidence of cross-surface reuse.

Use [design-directions.md](design-directions.md) when choosing a direction and
[redesign-preservation.md](redesign-preservation.md) when an existing contract
may change. A visual refresh alone does not authorize a content rewrite or
framework migration. Use `effective-product` when the experience model needs
exploration, then bring the chosen qualities back.

If a missing answer would materially change layout, interaction, or
communication, ask **one** concise discriminating question; otherwise state a
responsible assumption and proceed. Do not ask users to choose between vague
adjectives or re-answer preserved decisions.

## Pre-Code Questions

Answer from the prompt, product context, or existing code; ask only what cannot
be inferred. Cover: purpose, primary user and context, the one primary action,
register (operate / persuade / read / experience), product domain or brand point
of view, required content (min/typical/max cases), states (default, empty,
loading, error, success, permission-limited), existing constraints (design
system, framework, a11y, i18n, performance), device/input context, competing
attention, user mental model, and anti-goals. The full annotated list is in the
appendix.

## Decide Before Styling

Before colours, spacing, shadows, or type, decide:

- Information hierarchy — what is dominant, secondary, and quiet.
- Layout topology: single column, split pane, table, master-detail, dashboard
  grid, wizard, timeline, canvas, or article.
- Interaction model: inline edit, explicit submit, autosave, modal, popover,
  route change, optimistic update, or background task. For AI-assisted work pick
  the modality deliberately — do not choose chat merely because an LLM is used.
- Surface density: sparse, normal, dense, or data-heavy.
- Primary (and optional secondary) direction from
  [design-directions.md](design-directions.md), not a fixed style preset.
- Tone and the role of structural devices such as numbers, eyebrows, badges,
  and dividers. Apply [Choose Patterns by Role](fundamentals-core.md#choose-patterns-by-role)
  when selecting repeated visual treatments.

Do not start with card grids, hero templates, gradients, or animation before the
surface has a clear job.

## Specificity

- **Operate surfaces:** specificity comes from the product's world — name domain
  concepts, data shapes (compare rows / monitor exceptions / approve batches /
  debug incidents), and useful actions. Familiar navigation, cards, and metrics
  can fit when they reflect the real workflow; do not invent a unique signature
  merely to distinguish an otherwise effective tool.
- **Persuade surfaces:** decide the point of view first — audience and promise,
  concrete voice, the category reflex to avoid, primary credibility evidence,
  and one memorable signal. Let the first viewport express the thesis through
  real evidence, not a headline-stat-gradient default.
- **Read surfaces:** name the reader's question, source material, comprehension
  path, and wayfinding need. Let hierarchy, measure, examples, and evidence make
  sustained reading unusually clear and trustworthy.
- **Experience surfaces:** name the artifact or interaction that leads, how
  exploration unfolds, and which controls remain available while the interface
  recedes. Do not delay the work behind a persuasion template.
- If the only claim is "it looks polished", the direction is still too generic.

## Context Adaptation

Adaptation is not scaling. Moving desktop→mobile, product→print, or
pointer→touch may need a different structure while preserving the same
information architecture. Decide device/viewport, input, use case, connection,
and platform expectations up front. Do not hide core functionality on small
screens — change the interaction model. Use content-driven breakpoints,
container queries for components, media queries for page layout, and
`pointer`/`hover` queries to detect input capability.

## Adjustment Lenses

Pick the lens that prevents the wrong first draft (details in the appendix):

- **Bolder** — a persuade or experience surface needs a clearer point of view:
  make one thing unmistakably dominant. In narrow work, preserve neighbours,
  content, behavior, and system contracts; amplify vocabulary the system already
  owns. Use the appendix's scope and copy-free structure checks.
- **Quieter** — too loud for repeated/high-stakes use: cut decorative colour,
  motion, and shadows; let structure and states carry confidence.
- **Distill** — complexity is the risk: remove duplicate actions and ornamental
  containers; preserve capability, remove decision noise.
- **Minimalist** — a context lens (editorial/utilitarian/premium), not a
  default: let type, measure, whitespace, and content carry hierarchy. Do not
  apply to dense operational tools or bolder brand pages.

## Anti-Pattern and Readiness Checks

For generic or agent-generated output read
[ui-antipatterns.md](ui-antipatterns.md): separate objective defects from
context-dependent advisories, look for clusters, and preserve patterns justified
by task, register, or accepted decision. If a cluster appears, change the owning
brief decision rather than polishing around it.

Write a **compact design brief** for ambiguous or net-new UI (surface, register,
direction, primary user/action, register-specific signature, layout strategy,
interaction model, required states, content, context adaptation, browser
evidence, constraints, anti-goals) in concrete nouns — the full template is in
the appendix. Record durable register/direction/communication decisions through
`effective-product`.

Implement when the direction and consequential constraints are clear. Resolve
remaining gaps from available evidence or reasonable assumptions; ask only when
a missing answer would materially change the result and cannot be inferred.
Revise a contradictory brief before styling. Do not score the design numerically.
