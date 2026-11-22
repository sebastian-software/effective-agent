# Technical Subject-Matter Writing

Use this reference for engineering blog posts, technical articles, explainers,
technical case studies, and public technical project pages. Preserve technical
integrity without making editorial prose sound like a manual.

## Select the writing contract

Choose the narrowest contract that fits the artifact:

| Contract | Use |
| --- | --- |
| Technical editorial prose | Explain, argue, teach, or demonstrate through an article, blog post, case study, or public project page. |
| Technical marketing prose | Explain a verified capability, mechanism, constraint, or differentiator through `effective-marketing`. |
| Technical documentation | Help a user operate, configure, integrate, migrate, or troubleshoot a product through `effective-delivery`. |
| Controlled technical language | Apply ASD-STE100, a tekom-based project profile, or another named standard through `effective-delivery` only when it governs the artifact. |

Do not infer a controlled-language requirement from a general request for
clarity. For public German prose, prefer precise, natural technical German
rather than Einfache Sprache. For public English prose, prefer natural
editorial English rather than internal-team Metro English.

An explicit user request establishes the desired style, including short
sentences, no metaphors, or a controlled-language profile. Apply it on the first
pass; do not require a second request because another register might suit the
channel better. Briefly explain a material tradeoff when useful, then complete
the requested version while preserving facts, qualifications, and technical
meaning.

Use `effective-delivery` for authoring or verification against a named
controlled-language standard. Distinguish requested stylistic features from
verified compliance: the request alone does not prove that the result meets a
standard. Resolve a genuine conflict with another governing requirement at that
specific boundary, rather than treating a stylistic preference as a blocker.

Do not describe German prose as ASD-STE100 compliant: ASD-STE100 controls
English. State that mismatch before drafting when the requested assurance is
invalid. Do not describe prose as universally tekom-compliant: a project adopts
specific rules from a named guide and editorial profile.

## Establish the source and ownership chain

Keep these layers separately reviewable:

```text
engineering truth -> approved terminology -> claim and proof
                  -> editorial explanation -> channel presentation
```

- Derive product behavior, values, limits, compatibility, and failure modes
  from current engineering or approved product sources.
- Use `effective-delivery` when repository inspection, executable examples, a public
  interface, or a controlled-language contract owns correctness.
- Use `effective-marketing` to establish market position, supported claims,
  proof, audience, and desired action.
- Keep articles, editorial explanations, narratives, and public project prose
  in this skill.
- Use `effective-marketing` for commercial homepages, landing pages, product or
  service pages, pricing pages, campaigns, launches, and sales assets.
- Use `effective-web` for page hierarchy, interface copy, accessibility,
  implementation, and browser verification.

Do not use polished prose as evidence that a technical or commercial claim is
true. Mark unresolved behavior, measurements, permissions, and comparisons
before drafting around them.

## Preserve the technical proposition

Extract the proposition before revising its language:

- actor or owning system
- action or mechanism
- object or affected surface
- prerequisites and conditions
- limits, versions, scale, or environment
- result, side effect, and likely failure
- evidence and uncertainty

Keep qualifications next to the claim they constrain. Do not turn `can`,
`supports`, `typically`, or `under these conditions` into an unconditional
promise for a cleaner sentence or stronger hook.

Preserve literal code, commands, API names, configuration keys, UI labels,
protocol names, identifiers, and quoted output. Route uncertain implementation
details back to their technical source instead of smoothing over them.

## Control terminology without flattening the prose

- Use one preferred term for each important technical concept.
- Preserve official product, protocol, framework, and interface names.
- Define an unfamiliar term at its first useful occurrence when the audience
  needs it; do not interrupt specialists with definitions of shared basics.
- Expand an abbreviation on first use unless the audience and channel make it
  reliably familiar.
- Vary surrounding language, examples, and sentence construction rather than
  rotating synonyms for a core concept.
- Distinguish adjacent concepts that readers may otherwise collapse, such as
  authentication and authorization, latency and throughput, or backup and
  replication.
- Reuse an accepted glossary, terminology database, or editorial decision
  instead of creating a parallel vocabulary inside one article.

Treat stable terminology as a comprehension aid, not as a ban on voice,
metaphor, or normal lexical variety.

## Explain for the selected audience

Start from what the reader already recognizes, then add only the technical
depth needed for the piece's governing idea.

- Connect mechanism to consequence: explain what the system does, why that
  behavior matters, and under which conditions.
- Introduce a concrete example before a large abstraction when it reduces the
  reader's cognitive load.
- Use an analogy only when its mapping is accurate. Name where it stops being
  accurate when readers could otherwise carry the wrong model forward.
- Separate the supported path from alternatives and edge cases.
- Use diagrams, code, or tables only when they explain a relationship more
  efficiently than prose.
- Let specialist readers keep useful complexity. Do not replace precise domain
  language with broad everyday words that change the meaning.

Write for competent readers who may lack this specific context. Do not confuse
accessibility with condescension or remove the qualification that makes an
expert statement true.

## Draft from the material

For a bylined blog post, start with the piece brief, the author's notes or
interview, and the evidence behind the claim. A neighboring article for the
same audience can help you hear how the author explains a difficult point.
Use the publication's source language even when the interview took place in
another language.

Find the detail that made the subject worth writing about. It might be a
choice the author used to make differently, a result that upset an assumption,
or something a reader can try with a few lines of code. Put enough of it in
the opening for the reader to see the point. In an explainer, the behavior
itself can supply all the interest.

Suppose a bug report shows a white code sample after the preview switches to
dark mode, and the fix adds the theme to the cache key. You can open with the
symptom and go straight to the explanation. “Switch the preview to dark mode
and the code sample stays white. The highlighter has already rendered that
snippet once, and its cache key says nothing about the theme.” Now the change
to the cache key answers a question the reader already has.

Keep going where the example leads. Show the old behavior, a plausible
alternative, or the part of the implementation that explains the surprise,
whichever the reader needs next. In a signed review, let readers see what
the author values. Suppose their notes say, “I admire the optimism of a
backup tool that prints ‘Success’ before it writes the file.” That line gives
the reader both the behavior and the author's verdict. Check when the message
appears and keep the joke if the sequence holds. If the author calls a change
groundbreaking, show what they can do now that used to be out of reach.
An opinion can be emphatic while its factual basis stays precise.

Read the piece on its own. A new reader should have enough context to
understand the observation and enough room to reach a different verdict.

An unsigned explainer or project page has room for humor, varied sentence
length, and a firsthand observation when its source is clear.

Do not add one action per sentence, one sentence per paragraph, an approved-word
dictionary, imperative syntax, or other controlled-language constraints merely
because the subject is technical. Apply the stylistic constraints the user
requests or the named documentation contract requires, while preserving meaning
and distinguishing style from verified standards compliance.

For a tutorial embedded in an article, separate the editorial frame from the
operational instructions. Apply documentation discipline to commands,
prerequisites, steps, expected results, and recovery while allowing the
surrounding article to retain its voice.

## Adapt without losing the contract

### German

- Prefer natural, precise technical German with useful subordinate clauses and
  normal paragraph rhythm.
- Reduce heavy nominal constructions, ambiguous references, and unnecessary
  internal jargon.
- Keep established Fachbegriffe when they are accurate and useful.
- Treat tekom-derived clarity rules as an editorial influence unless a
  project-specific rule set explicitly governs the artifact.
- Do not default to Einfache Sprache or Leichte Sprache.

### English

- Prefer direct, idiomatic editorial English appropriate to the audience and
  author.
- Keep technical terms stable while allowing contractions, narrative rhythm,
  and personality when the channel supports them.
- Do not claim ASD-STE100 conformance or apply its dictionary and rule set
  unless the artifact is explicitly governed by it.
- Use the Metro English route for internal team communication about the work, not as
  the default voice for a public technical article or project page.

## Review an article

Use these checks where the draft needs attention. For an article request,
deliver the article itself in the publication's format.

1. **Technical integrity** - Verify behavior, conditions, limits, examples, and
   comparisons against their owning sources.
2. **Terminology** - Check preferred terms, literal identifiers, abbreviations,
   and distinctions between adjacent concepts.
3. **Audience path** - Confirm that context, mechanism, consequence, and depth
   arrive in the order the selected reader needs.
4. **Claim and proof** - Keep every consequential technical and commercial
   claim within the supplied evidence.
5. **Voice and movement** - Restore rhythm, personality, examples, and
   transitions where precision editing made the prose mechanical.
6. **Channel fit** - Check the title, lead, editorial hierarchy, call to action,
   and handoffs without changing the technical proposition.

Report a controlled-language conformance level only through the governing
technical-documentation workflow. For editorial prose, describe the result as
technically reviewed, terminology-aligned, or informed by rule-based technical
writing only when the performed review supports that statement.
