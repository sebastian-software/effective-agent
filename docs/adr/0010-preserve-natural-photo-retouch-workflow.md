# ADR 0010: Preserve Natural Photo Retouch as a Focused Skill

- Status: Accepted
- Date: 2026-10-08
- Extends: [ADR 0004](0004-effective-disciplines.md)

## Context

A business photo-shoot workflow established a reusable Imagegen prompt for
smoother clothing, clearer glasses, rested eyes, facial light balancing, and
consistent warm color treatment. The requested outcome is an edited photograph
or coherent series. Commercial messaging, browser work, and prose guidance
do not own that outcome.

## Decision

Add one independently installable skill, `effective-photo-retouch`, with a
single natural-retouch route. Preserve the reusable prompt in that route,
separate from project-specific filenames and private photographs.

Keep activation focused on editing existing portraits and shoot series.
Do not expand it into general photography advice, new scene generation, body
reshaping, commercial copy, CDN administration, or implicit publication.

The six broad disciplines retain their existing responsibilities. This
addition is a focused image-editing capability, not a reopening of the former
compatibility-skill inventory.

## Consequences

The public inventory grows to seven skills. README installation links, website
cards, detail pages, filter counts, structured data, and the routing matrix
must include the new capability.

Review scenarios distinguish color references from identity references, retain
authentic expressions, require comparison against originals before artifact
removal, and expose output-resolution limitations. These scenarios are unrun
fixtures, not evidence of an independent behavioral evaluation.

## Review Triggers

Revisit the boundary if actual requests require broader photographic work or
overlap with another skill. Revise the prompt for demonstrated defects rather
than accumulating rules from unverified artifacts.
