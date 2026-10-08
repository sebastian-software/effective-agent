# ADR 0010: Organize Image Work in a Routed Discipline

- Status: Accepted
- Date: 2026-10-08
- Extends: [ADR 0004](0004-effective-disciplines.md)

## Context

A business photo-shoot workflow established a reusable Imagegen prompt for
smoother clothing, clearer glasses, rested eyes, facial light balancing, and
consistent warm color treatment. The requested outcome is an edited photograph
or coherent series. Commercial messaging, browser work, and prose guidance
do not own that outcome.

The collection organizes domain workflows under broad skills with focused
routes. Naming the skill after one retouch workflow would make future image
work unnecessarily fragmented.

## Decision

Add the independently installable image discipline `effective-image`.
Business Portrait Retouch is its first route. Preserve the reusable prompt
there, separate from project-specific filenames and private photographs.

Route by the actual image task and keep workflow-specific constraints in that
route. Do not apply identity-preserving business retouch to every image task.
Further image workflows belong in their own routes when introduced; the
initial release does not claim general image-generation coverage.

The existing six disciplines retain their responsibilities. Commercial copy,
browser implementation, CDN administration, and publication authorization
remain outside the image skill.

## Consequences

The public inventory grows to seven skills. README installation links, website
cards, detail pages, filter counts, structured data, and the routing matrix
must include the image discipline.

Review scenarios for the first route distinguish color references from identity
references, retain authentic expressions, check originals before artifact
removal, and expose output-resolution limitations. These scenarios are unrun
fixtures, not evidence of an independent behavioral evaluation.

## Review Triggers

Add a route when actual requests establish another reusable image workflow.
Revisit domain boundaries when image work overlaps with another skill. Revise
retouch instructions for demonstrated defects rather than accumulating rules
from unverified artifacts.
