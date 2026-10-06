# Interface Copy

Use this skill for words inside product UI: labels, helper text, empty states, headings, button text, status messages, and short-form explanation.

For which states exist and how they behave — what appears while work is
pending, failed, or empty, and how recovery works — use
**Error and Loading States** ([route-states.md](route-states.md)) instead.
This route owns the words inside those states.

## Workflow

1. Read accepted ADRs and editorial guidance for audience relationship, form of
   address, stable voice, vocabulary, claim boundaries, and channel exceptions.
2. Identify the user's question at that moment: what is this, why does it matter, what happens next?
3. Remove copy that explains the interface instead of making the interface clearer.
4. Make labels concrete and action text outcome-oriented.
5. Match tone to consequence without changing the recorded voice: calm for
   errors, direct for actions, sparse for repeated workflows.
6. When copy feels generic or generated, use [Copy pattern review](ui-pattern-copy.md)
   to check repeated cadence, manufactured contrast, unsupported claims, and
   redundant language without banning individual words or punctuation. Use
   [UI anti-patterns](ui-antipatterns.md) to classify the finding against context.
7. Check text expansion, localization, accessibility names, and cross-channel
   consistency. Use `effective-product` when the work changes a durable
   communication direction.

## Rules

- Button labels should usually be verb plus object.
- Error copy should name the problem and the recovery path.
- Empty states should help users take the next useful action.
- Avoid marketing language inside task surfaces.
- Prefer specific nouns over clever phrasing.

## References

- [interface-copy.md](interface-copy.md) - concise interface and product copy rules.
- [editorial-ux.md](editorial-ux.md) - editorial UX patterns and wording checks.
- [ui-pattern-copy.md](ui-pattern-copy.md) - generated-copy and marketing tells
  with contextual exceptions.
- [ui-antipatterns.md](ui-antipatterns.md) - defect, advisory, and pattern-cluster
  classification.
