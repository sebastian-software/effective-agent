# ADR 0011: Use US English for All Project Content

- Status: Accepted
- Date: 2026-10-12

## Context

Several open issues were created with German titles and descriptions, while the
repository's documentation and skill guidance are in English. Without a
documented project language, contributors and agents can carry the language of a private
conversation into shared artifacts. Readers then need multiple languages to
follow the backlog and its decisions.

## Decision

US English (`en-US`) is the project language for Effective Agent. Use it for
all project content: issue and pull request titles and descriptions, comments,
reviews, discussions, posts, documentation, website copy, code comments,
commit messages, changelogs, and release notes. The rule applies equally to
human, agent, and bot contributions.

The [contributor language policy](../contributor-checks.md#project-language)
owns the practical rules for publishing, editing, and translating content.
[Repository instructions](../../AGENTS.md) and GitHub issue and pull request
templates make the policy discoverable at the point of contribution.

Quoted source text, proper names, exact technical identifiers, and examples or
fixtures that demonstrate another locale may retain their original language;
surrounding explanations use US English. This does not authorize German project
prose. Private conversations can use the participants' preferred language.

This decision governs contributions to Effective Agent. The installable
skills continue to follow the language requirements of the projects and users
that invoke them.

## Consequences

Contributors can read, search, and review the project in one language with a
consistent spelling convention. Contributors working in another language must
translate shared content before publishing it.

Translate active German issue titles and descriptions while preserving their
scope, links, technical identifiers, acceptance criteria, and proposal status.
Check new and edited content during review. A language detector alone cannot
distinguish unwanted project prose from valid quotations or locale examples.

## Review Triggers

Revisit this decision if the project adopts supported localized documentation
or communication channels. Record that change explicitly before introducing
another project language.
