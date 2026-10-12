# Guides and READMEs

## Start from the reader's entry point

Identify who arrives, what they already know, and the first useful outcome they
need. A repository README commonly needs to answer what the software is, why a
reader would use it, how to reach a verified first success, where deeper docs
live, and how to get help or contribute. Preserve a different established
structure when it already works for the intended audience.

Do not turn the README into the entire manual. Keep the shortest supported path
near the entry point and link to focused guides for concepts, configuration,
operations, or advanced workflows.

## Structure task guides around completion

A useful procedure normally makes these elements discoverable:

1. the outcome and intended audience;
2. prerequisites, supported versions, permissions, and starting state;
3. ordered steps with exact commands or interface actions;
4. observable success criteria;
5. likely failures and recovery where they materially affect completion; and
6. the next relevant task or reference.

Use headings that describe reader goals rather than internal component names
when the document is task-oriented. Separate explanation from procedure when
mixing them would interrupt the supported path.

## Design a maintainable information architecture

- Give each durable fact one clear owner. Link to API references, configuration
  schemas, generated output, ADRs, or runbooks instead of copying them.
- Put contributor setup near contributor workflows and user setup near user
  workflows. Do not make either audience filter through the other's details.
- Keep navigation and indexes aligned with new, renamed, moved, or removed
  pages. Follow the generator's ordering and metadata conventions.
- Preserve established terminology and heading style. Introduce a glossary only
  when recurring domain terms genuinely block comprehension.
- Remove stale paths and misleading alternatives rather than keeping them for
  historical completeness. Put durable history in release or migration notes.

## Refresh an existing translation

Read the changed source, matching target, and the target project's current
locale settings and terminology. Update only the affected passages, leaving
already-correct sections intact. Translate technical meaning without copying
source-language word order. Preserve code, commands, identifiers, paths,
examples, and placeholders according to their owning format. Check changed
technical claims against their code, schema, or decision owner. Surface
material uncertainty when that context does not settle the wording or claim.

## Review for reader success

Read the result from the documented starting state. Confirm that prerequisites
appear before use, links resolve, commands are copyable, expected output is
recognizable, and the guide does not rely on knowledge found only in the
author's implementation context.
