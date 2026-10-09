[← Effective Agent](README.md)

# Migration: 34 Skills → 6 Effective Disciplines

This collection consolidated its 34 first-party skills into six top-level
discipline skills that share one naming grammar and one internal architecture.
No guidance was deleted during that consolidation. Every absorbed `SKILL.md` body became a route reference
inside its discipline, and every `references/` file moved with it.

The rationale, alternatives, execution outcome, and lasting review triggers are
recorded in [ADR 0004](docs/adr/0004-effective-disciplines.md).

## The six disciplines

| Discipline | One-line story |
| --- | --- |
| [`effective-product`](skills/effective-product/README.md) | Decide what to build and how it should work |
| [`effective-web`](skills/effective-web/README.md) | Build the browser experience as one system |
| [`effective-engineering`](skills/effective-engineering/README.md) | Design and write the software itself |
| [`effective-delivery`](skills/effective-delivery/README.md) | Move repositories and teams forward safely |
| [`effective-writing`](skills/effective-writing/README.md) | Prose that people trust and act on |
| [`effective-marketing`](skills/effective-marketing/README.md) | Take verified value to market |

## Old slug → new home

| Old skill | Discipline | Route |
| --- | --- | --- |
| `codebase-improvement` | `effective-delivery` | Codebase Audit and Plans |
| `consultant-profile` | `effective-marketing` | Consultant Profile (plus Profile Voice and Profile Evidence) |
| `conversion-optimization` | `effective-marketing` | Conversion Optimization |
| `create-social-content` | `effective-marketing` | Social Content |
| `data-systems` | `effective-engineering` | Data Systems |
| `decision-records` | `effective-product` | Decision Records |
| `effective-workflow` | `effective-delivery` | Workflow Orchestration |
| `engineering-management` | `effective-delivery` | Engineering Leadership |
| `issue-autopilot` | `effective-delivery` | Issue Queue Autopilot |
| `linkedin-posts` | `effective-marketing` | LinkedIn Posts |
| `linkedin-social-selling` | `effective-marketing` | LinkedIn Social Selling |
| `locale-typography` | `effective-writing` | Locale Typography |
| `market-research` | `effective-product` | Customer and Market Research |
| `marketing-writing` | `effective-marketing` | Marketing Copywriting |
| `metro-english` | `effective-writing` | Metro English |
| `nonfiction-writing` | `effective-writing` | Structure and Story, Prose and Revision, Human Voice Editing, Persuasive Nonfiction, Technical Subject Matter |
| `originality-review` | `effective-web` | Originality Review |
| `port-codebases` | `effective-delivery` | Behavior-Preserving Ports |
| `pr-review` | `effective-delivery` | PR Review and Upkeep (plus Review Provider Access) |
| `pricing-and-packaging` | `effective-product` | Pricing and Packaging |
| `product-design` | `effective-product` | Design Research, Solution Modeling, Behavioral Design |
| `product-management` | `effective-product` | Discovery and Evidence Review, Strategy and Operating Model, Scope, Quality, and Shipping |
| `product-marketing` | `effective-marketing` | Positioning, Messaging, Launch, Market Learning |
| `product-naming` | `effective-product` | Product and Feature Naming |
| `reference-analysis` | `effective-web` | Reference Analysis |
| `rust-engineering` | `effective-engineering` | Rust Engineering, Rust Architecture, Rust Performance, Rust Unsafe and SIMD |
| `smart-dependency-updater` | `effective-delivery` | Dependency Updates |
| `software-architecture` | `effective-engineering` | Software Architecture |
| `software-testing` | `effective-engineering` | Focused Testing, Benchmark Methodology |
| `software-validation` | `effective-delivery` | Repository Validation |
| `tech-docs` | `effective-delivery` | Technical Documentation |
| `typescript-engineering` | `effective-engineering` | TypeScript Engineering |
| `web-legal-compliance` | `effective-web` | Web Legal Compliance |

`effective-web` kept its name, its 25 existing intent routes, and all of its
references; it absorbed the three skills listed above.

## What changed for you

**If you installed a skill by name**, replace the old selection with its
discipline:

```sh
npx skills add sebastian-software/effective-agent --skill effective-delivery
```

```sh
dalo source select sebastian effective-delivery
dalo approve skill sebastian:effective-delivery
dalo sync
```

**If you did not pin anything**, nothing breaks: new discovery sees the six
disciplines directly.

**If you pinned an old slug**, re-pin it now. The 33 compatibility stubs and
their registry were removed on 2026-08-16 after the six-discipline release had
settled. New installs cannot select an old name. DALO preserves an existing
catalog pin and reports the removed selection as `selected_removed` during
`source refresh --check`; use the table above to choose the successor, update
the selection, and run the manager's sync command again.

## Renamed reference files

Files kept their names except where pooling made them ambiguous:

- `rust-engineering/references/*.md` → `rust-*.md`
- `typescript-engineering/references/*.md` → `typescript-*.md`
- `linkedin-posts` and `linkedin-social-selling` references → `linkedin-*.md`
- `locale-typography/references/*.md` → `locale-*.md`
- `web-legal-compliance/references/*.md` → `legal-*.md`
- `pr-review/references/voice.md` → `review-voice.md`
- `pr-review/references/voice-examples.md` → `review-voice-examples.md`
- `smart-dependency-updater/references/workflow.md` → `dependency-workflow.md`
- `issue-autopilot/references/*.md` → `issue-*.md`
- `issue-autopilot/scripts/rank_issues.py` → `effective-delivery/scripts/rank_issues.py`

The four byte-identical copies of `worktree-safety.md` in `issue-autopilot`,
`port-codebases`, `pr-review`, and `smart-dependency-updater` merged into one
shared file in `effective-delivery`.

## Routes that were split

Four absorbed skills exposed more than the 900-line route context budget once
their references pooled, so their route was split rather than registered as an
exception:

- `consultant-profile` → Consultant Profile, Profile Voice and Localization,
  Profile Evidence and Interviews
- `rust-engineering` → Rust Engineering, Rust Architecture, Rust Performance and
  Memory, Rust Unsafe and SIMD
- `pr-review` → PR Review and Upkeep, Review Provider Access
- `software-testing` → Focused Testing, Benchmark Methodology (per
  [ADR 0001](docs/adr/0001-performance-testing-ownership.md))

## Service Growth System

The former standalone `service-growth-system` skill (Apache-2.0) was merged in
after the consolidation. Its optional commands map to these routes; see
[ADR 0008](docs/adr/0008-merge-service-growth-system.md) for the rationale.

| Command | Discipline | Route |
| --- | --- | --- |
| `offer` | `effective-marketing` / `effective-product` | Positioning (service offer) / Pricing and Packaging (service pricing) |
| `validate` | `effective-product` | Discovery and Evidence Review (service pilots) |
| `message` | `effective-marketing` | Messaging and Proof (positioning thesis) |
| `content` | `effective-marketing` | Social Content (video and audio, content journey) |
| `outbound` | `effective-marketing` | Outbound Prospecting |
| `conversation`, `sales` | `effective-marketing` | Consultative Sales |
| `funnel` | `effective-marketing` | Marketing Copywriting (service landing page) and CRM (intake and events) |
| `ads` | `effective-marketing` | Paid Campaigns |
| `crm` | `effective-marketing` | CRM and Sales Operations |
| `operations` | `effective-marketing` | Service Business Growth |

Reference files moved as follows:

- `outbound/*.md` → `outbound-*.md`; `sales/*.md` → `sales-*.md`;
  `paid-media/*.md` → `paid-*.md`; `crm/*.md` → `crm-*.md`
- `conversations/*.md` → `sales-conversations-to-meetings.md`
- `funnels/forms-and-measurement.md` → `crm-intake-and-events.md`;
  `funnels/landing-page.md` → `service-landing-page.md`
- `offer-positioning/offer.md` → `service-offer.md`; its pricing reference →
  `effective-product` `service-pricing.md`, with the price conversation moved
  into `sales-conversation.md`
- `offer-validation/*.md` → `effective-product` `service-pilots.md`
- `market-messaging/*.md` → `positioning-thesis.md`; generic copy review folded
  into the existing copywriting references
- `content-system/*.md` → `video-and-audio-content.md` and
  `content-journey-and-topics.md`; text-post guidance folded into the existing
  social references
- `operations/*.md` → `service-growth-operations.md`

The intermediate `routes/*.md` layer was dropped: each discipline links its
routes directly from `SKILL.md`.

## License

MIT OR Apache-2.0 — see the collection [LICENSE-MIT](LICENSE-MIT) and [LICENSE-APACHE](LICENSE-APACHE).
