# DALO Setup

DALO can install a reviewed selection from this first-party source and link it
into one or more agent targets. The source contains independently installable
skills and optional instruction packs. Composition with other repositories,
team-wide precedence, cross-catalog routing, and the final active set belong in
a separate downstream agent stack.

## Install Selected Skills

Register this repository as a catalog:

```sh
curl -fsSL https://dalo.sh/install.sh | sh
dalo init
dalo target link codex
dalo source add-catalog sebastian https://github.com/sebastian-software/effective-agent.git
dalo source inspect sebastian
dalo source select sebastian effective-web
dalo approve skill sebastian:effective-web
dalo sync
dalo doctor
```

Replace `effective-web` with another discipline name — `effective-product`,
`effective-engineering`, `effective-delivery`, `effective-writing`, or
`effective-marketing` — or select several names in one command. Catalog
selections are pinned. New skills in the repository remain inactive until
explicitly selected and approved. Review selected skills before granting the
source-qualified approval.

If you pinned a pre-consolidation slug such as `pr-review` or
`nonfiction-writing`, it no longer exists upstream. DALO preserves the current
catalog pin during `sync`; `dalo source refresh sebastian --check` reports the
selection as `selected_removed` instead of silently advancing it. Re-pin the
selection to the discipline that absorbed it using
[MIGRATION.md](../MIGRATION.md), then sync again.

## Sync and Review

```sh
dalo status
dalo sync
dalo doctor
dalo source refresh sebastian
```

`source refresh` reports upstream drift without advancing catalog pins or
activating new skills. Review changed selections before accepting a future pin.

## Enable Optional Instruction Packs

Instruction packs are standing guidance, not skills. DALO discovers them from
the source but does not activate them during source registration, skill
selection, approval, sync, or refresh.

With a DALO version that supports source-backed instruction packs, inspect the
available packs and explicitly enable the ones that should apply to each
verified target:

```sh
dalo instructions enable sebastian:request-and-completion --target codex --target claude
dalo instructions enable sebastian:documentation-truth --target codex --target claude
dalo instructions list
dalo doctor
```

`request-and-completion` governs authority, autonomy, and terminal-state
behavior. `documentation-truth` prevents prose shadows of code while preserving
the distinct authority of requirements, decisions, domain language, runbooks,
and verification evidence. Each enabled pack becomes a separate DALO-owned
managed block in Codex's and Claude's user-level instruction files. Content
outside those blocks remains user-owned. Activation is source- and commit-bound;
source drift requires review and explicit re-enablement rather than silently
changing standing behavior.

Use an explicit file target when a DALO release or another agent does not yet
provide a verified logical target mapping. Do not copy the pack into a project
instruction file merely to bypass that capability boundary.
