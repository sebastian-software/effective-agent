# ADR 0009: Audit Changed Guidance with a Coding Harness Before Push

- Status: Accepted
- Date: 2026-10-05

## Context

A prompt audit of the skills on 2026-10-05 found about 26 defects that every
existing check had passed. Twelve were pointers to a route or file that no
longer held the promised content after the consolidation, and the rest were
older passages that contradicted newer rules in the same skill. The link
validator confirmed that each target file existed; it could not tell whether
the target still said what the sentence promised.

Only about three of those defects were mechanical: a quoted section name
missing from its target, and a "section below" that pointed up. The others
needed someone to read both locations and judge whether they agree.

## Decision

1. `validate-readmes.py` checks the mechanical cases in CI: quoted section
   names after a link must name a heading in the target, and "the X section
   above/below" must point the right way.
2. A pre-push job runs `scripts/reference-audit.py`. It sends the diff of the
   pushed commits, with each changed file's router, link targets, and linking
   files, to a local `claude` or `codex` CLI in read-only mode. The prompt is
   kept in `docs/reference-audit.md` so both harnesses get the same review.
3. High-confidence findings block the push; `git push --no-verify` overrides a
   wrong one. Medium and low findings are advice.
4. A missing harness or a harness failure does not block. Results are cached
   per change.
5. CI does not run the audit, because CI never executes model behavior.

## Consequences

- Stale pointers and contradicting rules are caught by contributors who
  installed the hooks and have a harness, before review.
- Each push that changes guidance costs one harness run, roughly 15 to 40
  seconds on a small change. Re-pushing the same commits is free.
- Model findings vary between runs and harnesses. A false high finding costs a
  `--no-verify`; a missed one is still caught only by review.
- Pushes without the hook or a harness rely on review and the deterministic
  checks.

See [contributor checks](../contributor-checks.md#reference-audit) for the
workflow.
