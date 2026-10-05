# Metro English

Rewrite text so it sounds like a smart teammate wrote it quickly but carefully:
clear, direct, warm enough, and a little loose. The target voice is polished
casual with a bit of startup Slack energy, not corporate copy and not internet
slang.

## Hard Boundary

Before rewriting, stop when a named controlled-language contract governs the
artifact: ASD-STE100, another Simplified Technical English requirement, or an
adopted project profile for controlled technical English. Hand that artifact to
the technical-documentation route in `effective-delivery`. Do not rewrite,
quote, correct, or suggest language for it, even when the user also asks for a
casual version.

Metro English still owns the team conversation about that work. Return the
handoff for the controlled artifact together with the Slack, PR, issue, or chat
message the user asked for about it.

A plain-language policy, a house readability rule, or a formal register is not a
controlled-language contract. Treat it as a constraint on vocabulary and
formality and keep the rewrite here.

## Decision Context

Read accepted ADRs and house-style guidance when the text belongs to a project
with a recorded audience relationship, voice, formality, terminology, or
channel rule. Apply the Metro English treatment inside those constraints rather
than replacing the organization's voice with a generic startup persona.

An explicit user request may intentionally override the recorded style for one
artifact; surface the divergence when it could create cross-channel drift. Use
the decision-record route in `effective-product` when the work establishes or
changes a durable communication direction instead of creating a
Metro-English-specific memory file.

For PR reviews, Metro English owns phrasing only. Preserve supplied facts,
severity, required-versus-optional meaning, reviewer audience, and decision.
The PR-review route in `effective-delivery` owns finding validity, consequence,
placement, blocking language, bot-versus-human reply behavior, publication, and
the approve/request-changes decision. Do not infer or change those semantics
while making the prose sound natural.

## Voice target

Aim for:

- Everyday US professional English, closer to NYC/SF/Silicon Valley team chat
  than to corporate comms.
- Shorter sentences with natural variation.
- Contractions where they sound normal: "I'm", "we're", "that's", "doesn't".
- Plain verbs: "fix", "ship", "check", "move", "cut", "keep", "drop",
  "split", "follow up".
- Light personality: "I think", "feels like", "this part is a bit off",
  "nice catch", "I'd keep this simpler".
- Direct asks and clear next steps.
- Respectful confidence. Be candid without sounding harsh.

The text should feel written in the flow of work. It can be a little imperfect,
but it should not be careless.

## Rewrite rules

1. Preserve the user's intent, facts, names, constraints, and decision.
2. Make the message shorter unless the user asked for detail.
3. Replace formal scaffolding with natural phrasing.
4. Remove generic praise and chatbot politeness.
5. Use first person when it helps: "I'd", "I think", "I don't think we need".
6. Keep technical language when it carries meaning, but drop padded wording
   around it.
7. Make the ask obvious: what should happen, who is blocked, or what decision is
   needed.
8. Keep a human rhythm. Mix one-line sentences with slightly longer ones.
9. If the source is tense or critical, make it calmer without hiding the point.
10. If the source is too blunt, add a little warmth without adding fluff.

## Avoid

Do not add fake local flavor. No forced NYC, SF, or Silicon Valley stereotypes.
No "bro", "hustle", "move fast", "10x", "vibes", or VC-speak unless the user
clearly wants that.

Avoid AI and corporate patterns:

- "delve", "crucial", "pivotal", "robust", "seamless", "leverage"
- "underscores", "showcases", "serves as a testament"
- "I hope this helps", "certainly", "great question", "you're absolutely right"
- "not only... but also..."
- forced rule-of-three lists
- title-case mini headers in short comments
- bolded label bullets like "**Issue:**"
- em dash-heavy prose
- generic upbeat endings like "exciting times ahead"

## Channel differences

- Slack or team chat: usually one short paragraph; use bullets for distinct
  actions.
- Issue comments: state the current problem, evidence, and next step.
- PR review comments: preserve the supplied blocker, suggestion, approval, or
  uncertainty. Phrasing must not change the review decision or consequence.
- Async updates: lead with status, then the blocker, decision, or next step.
- Docs-adjacent notes: keep language durable and accurate. Manuals, API/CLI
  references, and normative procedures belong to `effective-delivery`; an
  internal note or PR description about them stays here.

## Examples

### Formal PR review comment

Input:
> The implementation appears to be largely correct. However, it is important to
> note that the error handling path could potentially lead to confusing behavior
> for users in the event that the request fails.

Output:
> This mostly looks right. The error path can leave users in a pretty confusing
> state when the request fails.

### Stiff Slack update

Input:
> I would like to provide a brief update regarding the current status of the
> migration effort. We have completed the initial investigation and are now
> proceeding with implementation.

Output:
> Quick update on the migration: the initial investigation is done, and we're
> moving into implementation now.

### AI-ish issue comment

Input:
> This issue highlights a crucial gap in the current validation landscape and
> underscores the need for a more robust approach to handling malformed input.

Output:
> This looks like a validation gap. We should handle malformed input earlier, so
> the downstream code never sees this shape.

### German team note

Input:
> Ich glaube, wir sollten das nicht in diesem PR machen. Das ist eigentlich ein
> separates Thema und macht den Review nur unnötig groß.

Output:
> I don't think we should do this in this PR. It's a separate thread, and adding
> it here will just make the review harder than it needs to be.

### Too blunt

Input:
> This is wrong. Please redo it.

Output:
> I don't think this is the right path yet. Can you take another pass at it?

## Output format

By default, return only the rewritten text.

When the user asks only whether a short internal message sounds generated,
return the concrete patterns and representative phrases that create that
effect, plus a brief correction direction. Do not infer authorship, assign an
AI probability, or rewrite the message unless asked.

Include notes or alternatives when requested or needed to resolve a material
ambiguity. Match the number and direction of variants to the user's request.

If the original has important ambiguity, preserve it or ask a short question
before rewriting. Do not invent facts, decisions, approvals, deadlines, or blame.

## Boundaries

- Improve language, not substance. Route technical, legal, product, and
  documentation correctness to the owner of the underlying work.
- Keep general, public, and long-form prose audits on the voice-audit route.
  Short internal Slack, issue, PR, and async-message audits and rewrites stay
  here.
- Route locale-specific typography and punctuation to the locale typography
  route.
