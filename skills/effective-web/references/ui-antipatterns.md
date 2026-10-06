# UI Anti-Patterns

Use anti-patterns to expose an unexamined design reflex, not to turn current
taste into permanent law. Read the brief, accepted ADRs, design system,
representative screens, content, and surface register before judging a pattern.
The client's chosen style and the user's task take precedence over style
advisories. Preserve an existing identity during refinement; an anti-pattern
review does not authorize replacing its fonts, palette, copy, or components.

## Classify Before Correcting

| Class | Meaning | Response |
| --- | --- | --- |
| Defect | Observable user harm or broken implementation, such as unreadable contrast, overflow, lost functionality, or an inaccessible control | Treat as blocked or risky according to impact; verify and fix |
| Advisory | A current generated-output tell or weak default that may still be valid in context | Name the reflex and ask what product, audience, or brand decision justifies it |
| Cluster | Several advisory tells reinforce the same generic template or aesthetic | Change the owning direction, hierarchy, media, copy, or interaction decision instead of polishing each symptom |
| Accepted exception | The pattern follows a real task, sequence, brand system, content form, or recorded decision | Keep it, verify execution, and avoid inventing a second system to satisfy the checklist |

Do not escalate an advisory to a defect merely because it is easy to detect.
One familiar font, card, glow, serif headline, or numbered label is not evidence
of generic design. Repetition without purpose and clusters across independent
choices are stronger signals.
An accepted visual choice still needs working behavior and accessible execution.
For a suspected cluster, name the missing product relationship and the change
that would restore it. Replacing cream with purple, cards with rows, or one
popular font with another without that explanation creates another house style.

## Separate Evidence From Judgment

Use deterministic checks only for claims the implementation can establish:

- broken or placeholder image references;
- contrast against the rendered background;
- text, content, and viewport overflow;
- positioned overlays clipped by an overflow ancestor;
- heading structure, accessible names, focus behavior, and target size;
- long lines, unreadably small text, or destructive tracking and leading;
- values drifting from the owning design tokens or component system;
- core functionality removed rather than adapted for a smaller context.

Separate measured values from their interpretation. A small type size, narrow
target, long line, or unusual token value is a reason to inspect its role and
use, not proof of harm by itself. Test the affected behavior and report the
actual consequence. Use [UI quality gates](ui-quality-gates.md) for functional,
state, accessibility, responsive, localization, and performance coverage rather
than repeating that checklist in every style review.

Use rendered inspection and design judgment for category reflex, specificity,
materiality, typography personality, copy cadence, and whether decoration earns
its cost. A clean static scan cannot prove that the direction fits the brief.
When an automated rule is added, test a true positive, an intentional exception,
and a plausible false positive. Prefer an advisory finding with evidence over a
confident but context-free prohibition.

## Select the Relevant Pattern Module

Load only the module matching the suspected cause. Add another when the actual
finding spans decision areas; a broad review still need not enumerate every tell.

| Suspected cause | Read |
| --- | --- |
| Page templates, cards, grouping, alternation, columns, or the close | [Layout pattern review](ui-pattern-layout.md) |
| Type, palette, surfaces, imagery, or icons | [Visual pattern review](ui-pattern-visual.md) |
| Reveals, loops, scroll effects, hover, cursor behavior, or animation cost | [Motion pattern review](ui-pattern-motion.md) |
| Generic phrasing, redundant text, unsupported proof, offers, or urgency | [Copy pattern review](ui-pattern-copy.md) |

## Review Sequence

1. Identify the surface register, primary job, audience, and accepted decisions.
2. Verify objective defects first and classify their user impact.
3. Mark advisory tells without treating them as failures.
4. Look for a cluster across structure, type, colour, material, motion, and copy.
5. Trace a cluster to its owning brief decision and revise that decision.
6. Preserve justified exceptions and verify their execution.
7. Recheck the rendered surface with real content, long text, responsive states,
   keyboard input, reduced motion, and the owning design system.

Report a small number of actionable findings. State the evidence, class, user or
brand impact, and the owning decision to change. Do not return a taste score or
a list of every detectable stylistic feature.
