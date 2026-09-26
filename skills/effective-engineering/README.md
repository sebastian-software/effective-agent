[← Sebastian Software Skills](../../README.md)

# Effective Engineering

**Design the system. Make its contracts hold.**

Effective Engineering works on the software itself: architecture, APIs, data
behavior, TypeScript, Rust, and the tests that protect them. It starts from the
repository and the actual failure consequences, then makes the technical choice
explicit enough for the next maintainer to understand.

**[Explore Effective Engineering →](https://skills.sebastian-software.com/skills/effective-engineering/)**

The website covers use cases, capabilities, example prompts, and how this skill
connects with the other disciplines.

## Install

```sh
npx skills add sebastian-software/skills.sebastian-software.com --skill effective-engineering
```

For pinned selections and multiple agent targets, follow the
[DALO setup guide](../../docs/dalo.md):

```sh
dalo init
dalo target link codex
dalo source add-catalog sebastian https://github.com/sebastian-software/skills.sebastian-software.com.git
dalo source select sebastian effective-engineering
dalo approve skill sebastian:effective-engineering
dalo sync
```

## Agent Instructions

[SKILL.md](SKILL.md) contains the workflow, routing rules, and links to the
focused references loaded by the agent. For former skill names, see the
[migration guide](../../MIGRATION.md).

Maintained by [Sebastian Software](https://oss.sebastian-software.com/).
We also help teams [design, modernize, and ship software](https://sebastian-consulting.com/en).

## License

MIT OR Apache-2.0 — see the collection [LICENSE-MIT](../../LICENSE-MIT) and [LICENSE-APACHE](../../LICENSE-APACHE).
