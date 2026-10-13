# ADR 0012: Date Volatile Claims and Re-check Them on a Schedule

- Status: Accepted
- Date: 2026-10-14

## Context

The skills state facts that change without any change to this repository:
browser support, vendor behavior, crawler names, platform limits, and tool
pins. A freshness pass on 2026-10-14 checked about 25 web-platform claims
against webstatus.dev, MDN browser-compat-data, and release notes. Thirteen
were stale or wrong. `ariaNotify()` and the tree-counting functions had
reached Baseline, Firefox 154 had shipped `text-box-trim`,
`overscroll-behavior` had dropped back to Limited availability, and Playwright
component testing had become stable. Most of the stale claims were bare
version lists without a date, so nothing showed that they needed a second look.

The effective-web feature radar already used a dated snapshot with a refresh
workflow, and `validate-site.py` already enforced a 90-day freshness limit on
the comparison page's review date.

## Decision

1. Volatile claims carry the date they were last verified, either inline as
   `as of <Month YYYY>` or through a `Snapshot date` header in a file with a
   refresh workflow. Baseline Widely available features need no date.
2. `scripts/check-claim-freshness.py` reports dated claims older than 180
   days and, with `--undated`, support-status claims that name an engine or
   version without a date.
3. A scheduled workflow runs the check monthly and fails when a claim is due.
   Pull requests do not run it, so an unrelated stale claim never blocks a
   change.
4. Re-verification stays manual or agent-assisted against primary sources.
   The check does not fetch sources or rewrite guidance.

## Consequences

- Every volatile claim either gets re-checked within roughly six months or
  produces a visible failed run.
- Authors spend a sentence on a date, and reviewers can ask for one.
- The undated check only covers support-status phrases next to a browser name
  or version; other volatile facts depend on authors following the convention.
- A failed monthly run needs someone to do the verification; the workflow
  itself does not open issues or edit files.
