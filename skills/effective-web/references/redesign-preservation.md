# Redesign Preservation

Use this reference when changing an existing web experience materially. A
redesign is a migration of user, brand, content, and operational contracts, not
permission to replace everything that looks old.

## Contents

- [Choose the Redesign Mode](#choose-the-redesign-mode)
- [Capture the Baseline](#capture-the-baseline)
- [Preservation Contract](#preservation-contract)
- [Design-System Provenance](#design-system-provenance)
- [Modernization Order](#modernization-order)
- [Approval and Decisions](#approval-and-decisions)
- [Verification](#verification)

## Choose the Redesign Mode

Name the mode before proposing changes:

- **Greenfield:** no meaningful existing experience or an explicitly approved
  replacement of product, content, and visual foundations.
- **Preserve:** modernize while retaining recognizable brand, information
  architecture, content intent, user habits, and operational contracts.
- **Overhaul:** establish a new visual language while preserving the existing
  product behavior, content, information architecture, and integration
  contracts unless separately authorized.

Do not infer an overhaul from words such as "modern," "premium," or "clean."
If the requested mode remains genuinely ambiguous and would materially change
scope, ask one question: whether the work should preserve the existing identity
or start a new visual direction.

## Capture the Baseline

Inspect and record only what is needed to detect regressions:

- **Purpose and audiences:** primary tasks, conversion paths, repeated workflows,
  and high-risk states.
- **Brand:** logo and wordmark treatment, palette, typography, imagery,
  illustration, shape, motion, and recognizable signatures.
- **Communication:** voice, form of address, terminology, claims, and channel or
  state exceptions from ADRs and editorial guidance.
- **Information architecture:** routes, URLs, navigation labels, headings,
  anchors, internal links, search, and content relationships.
- **Behavior:** forms, validation, field names, state transitions, permissions,
  keyboard paths, recovery, and browser contracts.
- **Learned orientation:** familiar control locations, action sequences,
  shortcuts, and contextual cues in frequent workflows. Capture only the
  patterns whose movement could impose meaningful relearning.
- **Design system:** tokens, components, icon family, supported variants, and
  documented exceptions.
- **Acquisition and discovery:** meaningful metadata, structured data, canonical
  URLs, redirects, indexable content, social previews, and ranking pages when
  SEO is in scope.
- **Operations:** analytics events, experiment hooks, consent behavior, legal
  copy, localization keys, support references, and automation selectors.
- **Quality:** current accessibility wins, known defects, browser target,
  performance measurements, and representative screenshots or visual tests.

Treat this as a focused migration baseline, not a request to document the whole
site.

## Preservation Contract

Do not change these silently:

- route paths, public URLs, anchor IDs, redirects, or canonical relationships;
- primary navigation labels, page hierarchy, or task order;
- form field names, submission contracts, autocomplete semantics, or validation
  expectations;
- analytics events, experiment identifiers, automation hooks, or stable test
  selectors;
- logo, wordmark, owned brand assets, or established product terminology;
- form of address, copy voice, claims policy, or legal and consent language;
- accessibility semantics, keyboard behavior, focus order, reduced-motion
  support, or text alternatives;
- localization keys and content needed for indexed or shared pages.

Preserve behavior deliberately, not pixel-for-pixel. Responsive structure,
component composition, typography, spacing, and visual hierarchy may evolve
when the mode allows it and the user contract remains intact.

## Design-System Provenance

- Extend the repository's existing design system before introducing a parallel
  local vocabulary.
- When the product context requires an official system or platform library,
  verify and use its current official package, tokens, components, and guidance
  rather than approximating its appearance by hand.
- Distinguish an official design system from an aesthetic influence. "Material,"
  "Polaris," or "Fluent" may name a maintained system; "editorial," "bento,"
  "glass," or "brutalist" describes a direction, not a package.
- Do not mix complete design systems to collect preferred components. Use one
  owning system and bridge isolated gaps explicitly.
- Verify installed packages and versions before importing. Do not migrate a
  framework or styling stack merely to achieve a visual refresh.
- Record durable adoption or replacement of an owning design system through
  `effective-product`; keep exact tokens and component APIs in the system itself.

## Modernization Order

Apply the least disruptive lever that satisfies the brief:

1. Correct hierarchy, content grouping, broken states, and accessibility.
2. Align typography, measure, spacing, and rhythm with the intended direction.
3. Consolidate palette, tokens, iconography, radii, and surface strategy.
4. Improve interaction feedback and functional motion.
5. Recompose high-value sections or workflows whose current structure is the
   problem.
6. Replace whole blocks only when smaller changes cannot meet the user and
   design goals.

Stop when the requested outcome is achieved. A redesign should not grow into an
unrequested content rewrite, framework migration, analytics migration, or route
restructure.

## Approval and Decisions

If the proposed design requires changing a protected contract:

1. Name the conflict and affected users or downstream systems.
2. Explain the smallest compatible option and the broader change option.
3. Use existing user authorization for the broader scope. Ask only when the
   change materially exceeds that scope or the intended outcome is unresolved.
4. Use `effective-product` when the change establishes a durable new direction,
   audience relationship, information architecture, design-system ownership,
   or cross-channel communication rule.
5. Track migration tasks, owners, rollout, and status in the project's issue or
   plan system rather than the ADR.

## Verification

Compare the redesigned implementation with both the approved direction and the
captured baseline:

- Run the primary task and conversion paths in representative viewports.
- Compare first-time discovery with returning users' ability to find and
  perform familiar actions. An easier introduction does not prove that moving
  a toolbar preserves repeated-use efficiency. When a move is justified, check
  whether familiar labels, shortcuts, or contextual guidance bridge the change.
- Verify URLs, redirects, navigation, anchors, metadata, structured data, and
  social previews affected by the change.
- Confirm forms, analytics, consent, localization, automation, and integration
  contracts still emit or submit the expected values.
- Test keyboard, focus, zoom, contrast, text alternatives, reduced motion, long
  text, loading, empty, error, success, and permission states.
- Compare current performance and visual evidence with the baseline where risk
  warrants measurement.
- Review copy and terminology against accepted communication decisions.

When a protected contract changed intentionally, verify the migration and update
its owning artifact. Do not hide the change as visual polish.
