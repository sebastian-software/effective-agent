# Authoring First-Party Agent Guidance

Skills are focused instruction packages. A skill may route a cohesive domain to
multiple workflows, but it must remain understandable from `SKILL.md` without
loading every bundled resource into context. Optional instruction packs hold
standing cross-task conventions and follow a separate activation contract.

## The Discipline Pattern

The six disciplines use `effective-<discipline>` names and one architecture:

- `SKILL.md` is a minimal router: short trigger, task selection, essential
  standalone safeguards, `## Route by Intent`, and `## Routing Boundaries`.
  The 300-line limit is a ceiling, not a target.
- Every route is linked directly as `references/route-<intent>.md`. Keep the
  reference directory flat and choose deeper material by the current task.
- Keep each substantive rule at one owner within a skill. A router selects
  guidance; it should not repeat the leaf's checklist. Shared contracts are
  loaded when their decision is needed, not before every task in the domain.
- Skills remain independently installable without optional instruction packs.
  Keep necessary authority and safety boundaries locally, but state them once
  at the level where they apply.
- Name cross-discipline handoffs in `## Routing Boundaries`; use local links for
  handoffs between routes of the same skill.

Add a discipline only for an independently requestable outcome that does not
fit the six existing owners, and record the choice as an ADR. Do not recreate
pre-consolidation compatibility stubs; [MIGRATION.md](../MIGRATION.md) owns their
mapping.

A description determines activation. Keep it as short as routing permits:
state the outcome, a few discriminating triggers, and the nearest confusable
boundary. Do not enumerate every leaf topic, repeat trigger instructions in
several forms, or use “always use”/“must trigger” language to compete for work.
The 1024-character format limit is not a writing target.

After changing descriptions, run the blind routing review in
[review-scenarios.md](review-scenarios.md) against
`docs/activation-matrix.json`. Static validation checks the contract's shape,
not model behavior. Report unavailable host/model coverage honestly.

### Calibrate Guidance to the Task

Each instruction should change a decision the agent would otherwise get wrong.
Remove generic encouragement, duplicate rules, mandatory full-repository reads,
and fixed output/check sequences that add no task-specific value. Keep detailed
recipes where a tool, protocol, or known failure needs exact steps.

Use conditional doc pointers and proportionate verification. A typo fix does
not need an architecture survey; passing checks need another run only after
changes, failures, or new evidence justify it. Reuse available briefs and
fixtures. Ask for missing information only when it changes the outcome or blocks
work, and respect explicit user checkpoints.

Define completion from the whole request. “Audit, fix, and open a PR” already
includes implementation and publication authority; an audit-only request does
not. Avoid generic review stops that interrupt an authorized workflow.

Skills carry domain knowledge and boundaries, not the machinery of one
particular workflow. Do not import finding taxonomies, status vocabularies,
mandatory recheck loops, fixed artifact templates, standing pre-read
instructions for other agents, or rules that turn a review into an edit. State
what makes an artifact sound and which misreadings to avoid; leave the method
to the agent and the user's request.

These principles follow [Eric Provencher's guidance on skills and prompts](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra).
Keep them model-neutral and verify behavior on the runtimes that use the skills.

## Required Structure

First-party skills live directly under `skills/`:

```text
skills/skill-name/
  README.md
  SKILL.md
  evals/
    evals.json
  agents/
    openai.yaml
  references/  # optional focused guidance
  scripts/     # optional deterministic helpers
```

Every public skill requires `README.md`, `SKILL.md`, `evals/evals.json`, and
`agents/openai.yaml`. Add the other directories when they serve a clear purpose.
Do not add external snapshots or generated copies.

## Instruction Packs

Use an instruction pack instead of a skill when all of these are true:

- the rule should remain active across otherwise unrelated tasks;
- it has no independently requestable outcome or useful activation trigger;
- it governs agent conduct such as authority, completion, communication, or
  orchestration rather than one professional discipline; and
- it can be expressed provider-neutrally without assuming one model, tool name,
  target path, or downstream catalog.

First-party packs live directly under `instructions/` and use DALO's compact
source format:

```text
version: 1.0.0
topics: authority, completion

# Request Contract
```

The filename stem is the stable pack ID. Declare one semantic `version:` entry
in the first five lines and one comma-separated `topics:` or `tags:` entry in
the first eight. Topics use unique lowercase tokens and make potential overlap
visible; they do not establish precedence. Keep a pack at or below 200 lines so
standing context remains cheaper than the task guidance it coordinates.

Every pack requires matching unrun scenarios at
`instructions/evals/<id>.json`. The file contains exactly one non-empty `evals`
array whose entries have `name`, `prompt`, and `expected`. Cover the dangerous
nearby behavior, not only the happy path: missing authority, silent partial
completion, unsafe concurrency, unjustified external action, or a rule that
overrides a more specific artifact contract.

Packs contain canonical Markdown only. Never include DALO managed-block markers
in the source. Discovery and source refresh are passive; activation must remain
an explicit DALO or host action. A skill must stay complete without the pack and
must not assume it is active. Put cross-catalog routing, target selection,
precedence, and stack-specific exceptions in the downstream agent stack.

The asset boundary is recorded in
[ADR 0005](adr/0005-first-party-instruction-packs.md).

### Language Depth Is a Route, Not a Skill

Language-specific depth belongs to `effective-engineering` as a route, not to a
standalone skill. Add one only where the generic architecture and testing routes
demonstrably miss agent failure modes specific to that language — for example
borrow-checker workarounds and written unsafe-proof discipline in Rust, which
the Rust routes own, or casting away type errors, defensive `any`, floating
promises, and cargo-cult strictness in TypeScript.

Frontend and browser-facing TypeScript stays with `effective-web`, and test
evidence stays with the Focused Testing route; a language route does not absorb
those. Give every new language route reciprocal cross-links with the
architecture and testing routes so a review, test, or port hands the
language-depth findings in and keeps lifecycle, merge, and delivery ownership
with `effective-delivery`.

Naming note: language routes deliberately avoid the `effective-<language>` form.
It would collide with the well-known "Effective TypeScript" and "Effective C++"
book titles that are the cultural source of the naming pattern.

## Human-Facing `README.md`

Each skill README helps people choose and install that skill. Include:

- an outcome-led value proposition, representative capabilities and prompts;
- links to the collection README and local `SKILL.md`;
- selective skills CLI and DALO installation commands;
- honest scope and useful handoffs to other first-party skills;
- [Sebastian Software open source](https://oss.sebastian-software.com/) and
  [English consulting](https://sebastian-consulting.com/en);
- `MIT OR Apache-2.0 — see the collection [LICENSE-MIT](../../LICENSE-MIT) and [LICENSE-APACHE](../../LICENSE-APACHE).`

Do not repeat the agent workflow or build generic cross-promotion lists. Name
sibling skills inline in runtime guidance: selective installs do not include
sibling files. Human-facing READMEs can link between skills.

After README edits, run `python3 scripts/validate-readmes.py`. Skill inventory
changes also require matching cards/metadata in `site/index.html` and
`python3 scripts/validate-site.py`.

## `SKILL.md` Frontmatter

Every new skill starts with valid YAML frontmatter containing only `name` and
`description`:

```yaml
---
name: effective-web
description: >-
  Design, build, review, and improve user-facing web experiences. Use for UI/UX,
  CSS, React, accessibility, frontend SEO, performance, or frontend testing.
---
```

DALO parses standard YAML, including literal and folded block scalars. It still
tolerates legacy metadata on existing skills, but do not add new fields unless
the repository contract changes.

### Writing the description

The description is what an agent sees before deciding whether to load a skill.

- State what the skill covers and name concrete trigger situations.
- Prefer terms users actually mention over abstract goals.
- Keep the trigger concise; details belong in the body and references.
- Keep the frontmatter name portable: lowercase ASCII letters, digits, `.`, `_`,
  and `-` only.

## `SKILL.md` Body Conventions

- Name the boundary section exactly `## Routing Boundaries`. It states what the
  skill must not invent and where it hands work to another skill; keep that
  canonical heading so agents and reviewers find the section in every skill.
- Cross-reference other skills by their frontmatter name in inline code, for
  example: route frontend work through `effective-web`. Do not use prose names,
  quotes, or bare links for skill-name cross references.
- Name only first-party skills that exist directly below `skills/`. Describe an
  unowned or external capability as outside the current skill's scope without
  inventing a downstream skill slot. The validator treats backticked
  identifiers in `## Routing Boundaries` and explicit phrases such as
  `` `example` skill `` as first-party skill references.
- Keep `SKILL.md` at or below 300 lines. The body owns the trigger, workflow,
  routing, and boundaries; detailed tables, policy text, and examples belong in
  `references/`. `scripts/validate-readmes.py` enforces this limit and the
  canonical boundary heading in CI.

## Resource Directories

- Use `agents/openai.yaml` for the required product-facing display name, short
  description, and `$skill-name` invocation prompt; never store project
  decisions or agent memory there.
- Use `references/` for detailed guidance loaded only when needed.
- Use `scripts/` for deterministic helpers agents can run.
- Use `assets/` or `examples/` only when a skill genuinely needs reusable output
  resources or complete examples; neither directory is part of the default
  first-party anatomy.

Keep `SKILL.md` lean. For a routed skill, link every route directly from
`SKILL.md` and keep references one level deep. Move long tables, examples,
policy text, and API details into references so agents load only the context
needed for the current task.

## Prove Behavior, Not Packaging

Use the smallest proof that discriminates the failure mode:

- Existing app surfaces, fixtures, or component stories for visual,
  interactive, responsive, stateful, or timing-dependent behavior. Add a
  reusable fixture only when existing evidence cannot expose the contract.
- Representative input/output for a nonvisual transformation.
- A review scenario for consequential routing or judgment changes.
- A deterministic script for mechanical contracts.

A screenshot proves appearance at one moment, not focus, interruption, cleanup,
or a workflow. Record browser/runtime evidence when rendering matters. Keep
examples self-contained where practical and exclude private material, copied
branding, and dependencies added only for a decorative demo.

Small visual recipes and tool techniques belong in focused references or
examples. A new route needs a distinct task; a new discipline needs its own
outcome and activation boundary.

## Runtime Context Budgets

References are runtime context, not an archive. A task-level reference should
normally stay at or below 500 lines; prefer a 150–350 line module when a task
needs only one decision area. A route must name the smallest matching reference
set and make a choice explicit when it offers alternatives. Do not present every
link in a route as required reading.

Routes should normally expose no more than 900 direct-reference lines. That is
a review threshold rather than permission to load every linked file: agents
still select the one or two references that match the task. The README validator
prints route-level totals in CI so a growing reference surface is visible in a
PR. This structural check does not measure the actual task path: it excludes the
router body, transitive reads, and cross-skill loading, and includes optional
direct links. For context changes, record the files actually read in a few
representative runs using the [comparison workflow](review-scenarios.md).
Optimize those paths before imposing additional file-size targets.

An unusually large deep reference is allowed only when it is a genuine
edge-case appendix and its normal route points to smaller task modules first.
Register it with a concrete reason and existing default modules in
`docs/reference-context-exceptions.json`. The validator rejects an unregistered
reference above 500 lines. Review every exception when the route or its modules
change; splitting a chapter must reduce the default load, not create copies of
the same baseline advice.

## Distill, Don't Archive

Ship actionable guidance, not article archives, intake logs, external snapshots,
or source-review commentary. Preserve useful knowledge as a decision rule or
short example. Verify changing platform contracts against primary sources;
experimental or single-source claims remain conditional rather than becoming
universal defaults.

Synthesize knowledge from books, courses, documentation, and practice around
the user's task. Preserve precise algorithms, decision criteria, constraints,
and failure modes; independently written examples should demonstrate the same
technical depth. Change structure when it improves selection or comprehension,
not merely to make a source less recognizable. Routine knowledge synthesis does
not need an itemized reading list in the runtime guidance. Omit optional book
and author credits when they distract from the task, while retaining required
attribution and license notices for reused material. Keep technical links that
verify platform contracts. Do not package source text, illustrations, or worked
examples as a substitute for the original publication.

## Calibrate Findings and Verification by Decision Value

A finding or permanent test needs evidence of reachable behavior, consequential
impact, and a remedy worth its implementation and maintenance cost. Do not
invent probabilities or reward finding count, coverage, reviewer count, or
exhaustive state enumeration.

Allow a clean audit, no new test, or unchanged code when speculative, recoverable
risk does not justify more machinery. Lower the evidence threshold at security,
authorization, privacy, money, data integrity, destructive actions, required
accessibility, and regulated boundaries.

Add a specialist or review pass for a distinct unresolved risk. Deduplicate
shared root causes; repeated agreement is not independent evidence.

## Persist Decisions in Shared ADRs

Follow the project's ADR convention for lasting rationale, alternatives,
tradeoffs, and review triggers. Use plain Markdown under `docs/adr/` only when
there is no convention and the decision merits a record. Accepted history is
superseded, not silently rewritten.

Keep exact values and behavior in their owning code, configuration, tokens,
guides, or tests. After executing a temporary RFC or plan, retain only lasting
decisions and deviations in the accepted ADR. Keep raw model output and dated
review logs with the PR, not as permanent source files. The decision-records
route in `effective-product` owns ADR lifecycle details.

## Keep Findings, Plans, and Decisions Distinct

Findings own evidence, impact, confidence, and possible corrections. Plans or
issues own scope, sequencing, dependencies, and temporary status. ADRs own
durable choices and rationale.

Discover existing trackers and plan directories. Do not create private ledgers
or mandatory `plans/` hierarchies. If a user asks to save a plan and no convention
exists, use `docs/plans/` and add an index only when several plans need ordering.
The audit route in `effective-delivery` owns plan creation and reconciliation.

## Review Scenarios (Unrun)

For consequential workflow or judgment changes, add a review scenario that
tests the failure mode the new rule is meant to prevent. The historical
`evals/evals.json` path is retained as a portable fixture format, but it is not
an executed behavioral-evaluation harness.

Store review scenarios in `skills/<name>/evals/evals.json`. Use `evals` for
output-quality cases. Add `activation` when the skill has adjacent owners,
high-cost behavior, or a description change that needs trigger evidence:

```json
{
  "evals": [
    {
      "name": "reject-shortcut",
      "prompt": "A realistic request containing the tempting shortcut.",
      "expected": "The decision, evidence, and tradeoff a strong response must surface."
    }
  ],
  "activation": [
    {
      "name": "direct-request",
      "prompt": "A realistic request that should load this skill.",
      "should_trigger": true
    },
    {
      "name": "adjacent-owner",
      "prompt": "A realistic nearby request that should not invoke this skill's full instructions.",
      "should_trigger": false
    }
  ]
}
```

Keep `name` stable and descriptive. Treat `prompt` as the user input and
`expected` as manual review criteria, not a golden response string. CI validates
only the fixture's JSON shape, non-empty fields, and unique names; it does not
submit prompts to a model, score responses, or claim behavioral correctness.
An `activation` set must include both should-trigger and should-not-trigger
cases. Put the most confusable natural-language requests in that set rather
than testing only explicit `$skill-name` invocation. A negative case means that
the host should not invoke this skill's full instructions; merely exposing its
name and description in the catalog does not count as activation. Use a request
owned by another skill or one that needs no skill, and avoid cases where
co-activation would be legitimate.

When a change needs behavior evidence, follow the documented [manual
review-scenario workflow](review-scenarios.md). It generates a report template
and validates that a human-recorded review identifies the skill, case, agent,
model, sampling settings, response, pass/fail result, and grading evidence. The
report validator checks traceability, not whether the human's grade is correct.

Use its fresh-session comparison template when deciding whether a skill or
prompt revision earns its context, latency, and token cost. Run each case once
with the skill available and once with it disabled, without sharing conversation
history between conditions. Record response quality, duration, token usage when
available, and the evidence for the comparison.

- Use a realistic prompt containing a plausible misconception, incomplete fix,
  or tempting shortcut; do not merely ask the agent to repeat the rule.
- State the expected decision and the evidence or tradeoff it must surface,
  without prescribing incidental wording or one exact implementation.
- Include fallback and degraded-state scenarios for progressive enhancements.
- Prefer a few discriminating cases over broad happy-path coverage that a
  baseline model would already pass.

For procedural guidance, give each consequential step an observable completion
condition so an agent can tell whether to continue, stop, or escalate. Review
new wording sentence by sentence: remove a rule when it does not change a
decision, action, or verification outcome. Replace stale or duplicated guidance
at its owner instead of adding another exception to an already layered rule set.

## First-Party Boundary

Everything below `skills/` is maintained here as Sebastian Software source.
Do not copy external skills, rename their frontmatter, add `SOURCE.md`
snapshots, or maintain external source selections and pins in this repository.

State a skill's boundary in capability terms that remain useful when the skill
is installed alone. Exact external slot names, catalog provenance, selections,
version pins, precedence, and cross-source routing belong in a downstream agent
stack.

Named runtime references are closed over this repository: every named skill
must match an existing first-party skill directory. Do not leave a dead named
handoff for an external or formerly installed skill. When no first-party owner
exists, state what the current skill does and does not cover, then stop.

## Delivery Worktree Inventory

Worktree mutation belongs to `effective-delivery`. Its review, issue queue,
dependency, porting, and orchestration routes apply one standalone
[worktree safety contract](../skills/effective-delivery/references/worktree-safety.md).
Keep creation, adoption, staging, integration, and cleanup rules there rather
than copying them into every router.

## Review

Before merging a change:

1. Confirm the trigger description still selects the skill for the right tasks.
2. Confirm links to bundled references, scripts, and any optional resources resolve.
3. When adding a skill, create `agents/openai.yaml` and `evals/evals.json`; add
   or update unrun output and activation scenarios for consequential changes,
   and record a fresh-session activation or with/without-skill review when
   behavior evidence is needed.
4. When adding a skill, add its `site/index.html` card and inventory metadata.
5. Run `python3 scripts/validate-readmes.py`,
   `python3 scripts/validate-site.py`,
   `python3 scripts/validate-activation-matrix.py`, and
   `python3 -m unittest discover -s scripts/tests -p 'test_*.py'`.
6. Run the repository's DALO CI smoke test.
7. Check that `dalo status` reports no inventory warnings or duplicate slots.
8. For routed skills, confirm every reference is reachable from its matching
   route, the default load is explicit and narrow, and old public skill names no
   longer appear in internal links.
9. When a skill claims visual, interactive, responsive, stateful, or
   time-dependent behavior, confirm that an appropriate rendered or executable
   proof exists or that the real product surface is the deliberate proof target.
10. Confirm useful micro-patterns sit at the smallest durable level instead of
    being discarded or promoted automatically.
11. For an instruction pack, confirm its metadata and matching scenarios pass
    `validate-readmes.py`, its rules remain provider-neutral, no skill depends on
    it, and installation docs preserve explicit activation.
