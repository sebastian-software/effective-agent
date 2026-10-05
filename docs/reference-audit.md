# Reference Audit

This is the prompt that `scripts/reference-audit.py` sends to a coding harness
before a push. It reviews changed skill and instruction-pack Markdown for
defects that a deterministic validator cannot see. The script appends the
changed files, the files they link to or are linked from, and the diff.

## Task

You are reviewing a change to agent guidance in this repository. Agents load
these files on demand, so a wrong pointer or two rules that disagree send an
agent the wrong way without any error. Review only what the diff changes or
what the changed text depends on. Read and search the files you need before
you judge them; reading and searching commands are fine. Do not modify
anything.

Report a finding only when the repository itself shows the defect:

- **Stale pointer.** A changed sentence sends the reader to a file, section,
  route, skill, script, or command for something the target does not contain,
  or a pointer elsewhere in the same skill now promises content that the change
  removed or moved. Read the target before reporting.
- **Contradiction.** A changed rule gives the opposite guidance to another rule
  on the same point in the same skill, or in the `SKILL.md` router. Search the
  skill for the topic, not only the listed neighbors. A narrower rule whose
  scope explains the difference (a different medium, platform, or task) is an
  override, not a contradiction.
- **Model- or history-relative phrasing.** The changed text describes model
  behavior instead of the requirement ("models tend to…", "models with stale
  training…"), or is written as a diff against an earlier version the reader
  never saw ("keeps its name", "now works differently", "no longer" about a
  rule rather than about the domain).

Do not report domain judgment you disagree with, external facts you cannot
verify in this repository, style preferences, or duplicated text that agrees.
A clean change is a valid result: return an empty list.

## Confidence

- `high`: you read both sides and the repository contradicts the text: the
  target lacks the promised content, or two rules give opposite instructions.
  Quote both locations. A high finding blocks the push.
- `medium`: likely, but it depends on reading intent or scope.
- `low`: worth a look; it does not meet the bar above.

## Output

Return only the JSON object the schema describes. For each finding give the
changed `file` and `line`, the exact `quote`, the `kind`, the `confidence`, the
other location in `related` (`file:line`, or an empty string), a short
`explanation`, and a concrete `suggestion` for the fix.
