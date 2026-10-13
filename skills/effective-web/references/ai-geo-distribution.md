# AI Search, GEO, and Content Distribution

Use this reference when public content must be discoverable, understandable, citable, or actionable across classic search, Google AI features, LLM search, browser agents, local/business surfaces, and partner feeds.

The durable base is the same as classic SEO: crawlable, useful, accurate, well-linked content with clear entities and trustworthy sources. AI/GEO adds entity clarity, source consistency, extractable passages, and intentional crawler policy on top of that base — it does not replace it. Weight official guidance from search and AI providers over vendor or agency claims; treat evolving AI-search tactics as hypotheses to measure, not settled ranking rules.

## Contents

- [Working Rules](#working-rules)
- [Google AI Features](#google-ai-features)
- [Entity Authority](#entity-authority)
- [Editorial Provenance and Freshness](#editorial-provenance-and-freshness)
- [Business Data Distribution](#business-data-distribution)
- [Crawling, Recrawling, and Push](#crawling-recrawling-and-push)
- [LLM and Agent Access](#llm-and-agent-access)
- [Agent-Readable Content](#agent-readable-content)
- [GEO Measurement](#geo-measurement)
- [Tactics Worth Testing](#tactics-worth-testing)
- [AI/GEO Review Checklist](#aigeo-review-checklist)

## Working Rules

- Treat classic SEO and AI/GEO as overlapping disciplines built on the same crawlable, useful, accurate, well-linked content.
- Do not prescribe `llms.txt`, AI text files, Markdown mirrors, content chunking, or special schema.org markup as requirements for Google AI Overviews or AI Mode. Google says these are not required.
- Use structured data to clarify real visible entities and qualify for rich results. Do not add hidden facts, fake reviews, unsupported services, or speculative claims.
- Keep important facts in visible text, not only in images, PDFs, JavaScript state, JSON-LD, or third-party widgets.
- Make the page's primary entity explicit: organization, local business, product, service, person, article, event, place, or dataset.
- Align facts across the visible page, JSON-LD, canonical URL, sitemap, Google Business Profile, Merchant Center, social profiles, review platforms, partner directories, and feeds.
- Make authorship, evidence, publication history, and material updates visible where readers would expect them. Do not simulate freshness by changing dates without changing the content.
- Separate crawler access for search, training, and user-triggered retrieval. Different AI providers expose different user agents and opt-out semantics.
- Favor entity clarity, citation consistency, original information gain, and answer usefulness over manipulative AI recommendation tactics.
- Measure mentions, citations, referrals, outcomes, and factual accuracy separately. Treat vendor visibility scores and share-of-voice reports as sampled observations, not ground truth.

## Google AI Features

For Google AI Overviews and AI Mode, follow the normal Google Search technical requirements:

- Make pages indexable and eligible for snippets.
- Keep content helpful, reliable, and people-first.
- Keep important content in text form, with high-quality images and video where useful.
- Make structured data match visible text.
- Keep Merchant Center and Google Business Profile data current where relevant.
- Use Search Console to diagnose indexability and traffic. Google includes AI
  feature visibility in the overall performance report and is rolling out
  dedicated Generative AI views to a subset of sites; availability is not
  universal and the dedicated report remains a visibility view, not causal
  conversion attribution.

Do not add the following as Google AI ranking requirements:

- `llms.txt`,
- special "AI schema",
- hidden JSON-LD facts,
- content chunking solely for Google AI,
- pages rewritten only for machines instead of users.

Use Google-Extended and preview controls only when the goal is to limit AI use or display. For search appearance, use supported controls such as `noindex`, `nosnippet`, `data-nosnippet`, and `max-snippet`, and expect recrawling to take time.

## Entity Authority

AI search and classic search both need to answer "who or what is this about?" and "why should this source be trusted?"

For organizations and local businesses:

- Create one canonical entity page for the organization, and one canonical page per physical location when locations differ.
- Show visible name, legal or trading name where useful, address, phone, service area, opening hours, contact methods, authors or leadership where relevant, credentials, policies, and unique differentiators.
- Use `Organization`, `LocalBusiness`, more specific local subtypes, `WebSite`, `BreadcrumbList`, `Product`, `Service`, `Article`, `FAQPage`, `Event`, or other schema types only when they match visible content and Google eligibility.
- Use stable `@id` values in JSON-LD to connect entity references across pages.
- Use `sameAs` only for profiles that unambiguously identify the same entity, such as the Google Business Profile or Maps URL, LinkedIn, Wikidata, Crunchbase, GitHub, YouTube, or official social profiles.
- Keep entity facts consistent across citations. Mismatched names, addresses, phone numbers, service lists, categories, and opening hours reduce confidence.

Think in entities and passages, not only keywords. Pages should make it easy to extract the answer, the source entity, the supporting evidence, and the next action.

## Editorial Provenance and Freshness

Make trust cues useful to readers first and machine-readable second:

- Show an accurate byline on editorial content where authorship matters. Link it to a durable author or reviewer profile that explains relevant experience and responsibility.
- Show the original publication date and a last-updated date only when they are useful and true. Record what changed when the update is material or the topic is high-risk.
- Keep visible bylines and dates aligned with `Article` or `BlogPosting` structured data, including `author`, `datePublished`, and `dateModified` where applicable.
- Explain how consequential reviews, comparisons, tests, or recommendations were produced. Include selection criteria, sample size, test conditions, screenshots, data, citations, and limitations as appropriate.
- Disclose substantial automation or AI assistance when a reader would reasonably want to know how the content was produced. Do not use a disclosure as a substitute for accountable review.
- Assign an owner and review cadence to time-sensitive pages such as prices, policies, technical recommendations, availability, and local-business facts. Correct or retire stale pages instead of bulk-bumping dates.

Freshness is claim-specific, not a site-wide ranking trick. Update `dateModified`, sitemap `lastmod`, feeds, and visible copy only after a material change, and keep the content itself consistent across those signals.

## Business Data Distribution

The website is the best editorial source of truth, but not automatically the operational source of truth for every surface.

For local businesses:

- Claim and verify the Google Business Profile. Google uses it directly for Maps, local results, and knowledge panel business facts.
- Verify the official website in Search Console.
- Show business details visibly on the site and mark them up with `LocalBusiness` structured data.
- Keep `openingHoursSpecification`, address, phone, `url`, `geo`, departments, menus, reservations, service areas, and special hours accurate.
- Update the Google Business Profile directly when Maps or knowledge panel facts must change. Use manual updates for small operations and the Business Profile API for multi-location or CMS-driven workflows.
- For products and ecommerce, use Merchant Center feeds in addition to product pages and `Product` structured data.
- For bookings and orders, use official platform integrations such as Reserve with Google or Maps Booking APIs rather than assuming page markup alone creates an action surface.

Source-of-truth model:

| Data type | Preferred source of truth | Distribution |
| --- | --- | --- |
| Editorial pages | CMS/website | Sitemap, internal links, Search Console, canonical URLs, social previews |
| Organization identity | Website entity page | Organization JSON-LD, Search Console, knowledge panel claim, `sameAs` profiles |
| Local hours/address | Business profile/location data system | Website visible content, LocalBusiness JSON-LD, Google Business Profile/API, local citations |
| Product availability/prices | Commerce/PIM | Product pages, Product JSON-LD, Merchant Center feed, partner marketplaces |
| Documentation/API facts | Docs source repo | HTML docs, sitemap, OpenAPI, changelog/RSS, optional Markdown mirrors |

## Crawling, Recrawling, and Push

- Treat `robots.txt` as an explicit crawler policy and operational endpoint,
  not as an indexing requirement or security control. For Google, `2xx` applies
  the returned policy; redirects are followed within limits; all `4xx` except
  `429` are treated as no `robots.txt` and therefore no crawl restrictions;
  `5xx`, DNS, timeout, and network failures are treated as unavailability. An
  unavailable file pauses Google crawling for the first 12 hours, then Google
  uses the last good cached policy for up to 30 days when one exists before its
  longer-term fallback. Serve and monitor an explicit file when policy clarity
  matters, but do not diagnose deindexing from a missing-file `404` alone.
- Use XML sitemaps for canonical URLs with meaningful `lastmod` values. Do not bump `lastmod` when the visible content did not materially change.
- Use Search Console URL Inspection for a few important Google recrawl requests. It is not a bulk indexing API and does not guarantee instant indexing.
- Use IndexNow for participating engines such as Bing when URLs are added, updated, or deleted. IndexNow accepts single-URL submissions and JSON POST batches.
- Use RSS, Atom, or changelog feeds when humans, agents, or downstream systems need to monitor new content.
- For high-change data, provide APIs or feeds rather than expecting crawlers to infer every update from rendered pages.
- Set `Last-Modified`, `ETag`, and cache headers coherently so crawlers and agents can avoid unnecessary fetches.

Google-specific status handling source: [How Google interprets the robots.txt specification](https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec#http-status-codes).

## LLM and Agent Access

Search and AI crawlers serve separate purposes, so set policy per purpose. User-agent names and opt-out behavior change; verify them in each provider's current crawler documentation before writing `robots.txt` rules. The list below was verified in October 2026:

- Googlebot controls Google Search crawling.
- Google-Extended can limit use in some Google AI training and grounding systems without being the same as Search indexing controls.
- OpenAI separates `OAI-SearchBot` for ChatGPT search visibility, `GPTBot` for training, and `ChatGPT-User` for user-triggered retrieval, with `robots.txt` handling that differs by purpose; it also lists further agents such as `OAI-AdsBot`.
- Anthropic separates `ClaudeBot` for training, `Claude-SearchBot` for search, and `Claude-User` for user-triggered retrieval.

Decide crawler policy intentionally:

| Goal | Policy direction |
| --- | --- |
| Appear in AI search answers | Allow search crawlers such as Googlebot, `OAI-SearchBot`, and `Claude-SearchBot` |
| Avoid training use | Disallow training crawlers where supported, such as `GPTBot` or `ClaudeBot`, without necessarily blocking search crawlers |
| Support user-directed agents | Avoid blocking user-triggered agents when users need them to retrieve docs, product details, booking flows, or support content |
| Protect private or paid content | Use authentication, `noindex` where appropriate, and server-side access control; do not rely on `robots.txt` as security |

Monitor crawler traffic, response cost, error rates, and cache effectiveness in server or CDN logs. A claimed user-agent string is not proof of identity; use provider-published IP ranges or verification procedures where available, and rate-limit or block abusive traffic without accidentally closing the intended search path.

## Agent-Readable Content

Agents may inspect rendered pages, DOM structure, the accessibility tree, screenshots, structured data, feeds, and APIs. The most reliable way to make content agent-readable is to make it user-readable.

- Use semantic HTML, headings, tables, lists, labels, captions, and accessible names.
- Keep critical facts in text, not only in images, canvas, carousels, videos, or collapsed widgets.
- Put answer-ready summaries near the relevant detail, not in a disconnected FAQ dump.
- Use comparison tables when users compare options.
- Use stable IDs, canonical URLs, breadcrumbs, and internal links.
- Expose machine interfaces when the task is operational: OpenAPI specs, product feeds, event feeds, booking APIs, downloadable docs, or changelogs.
- Provide Markdown mirrors only when real documentation or API consumers use them. Treat `llms.txt` as optional discovery, not a settled search standard.

Answer engines often need concise passages with enough context to cite. Write sections that can stand alone: claim, scope, evidence, date, entity, and action.

## GEO Measurement

Define success before choosing a monitoring tool. Keep four layers separate:

| Layer | What to observe | Typical evidence |
| --- | --- | --- |
| Visibility | Whether the entity is mentioned and whether the site is cited for the target task | Mention rate, citation rate, cited URL, competitor share of voice |
| Accuracy | Whether the answer names the right entity and states current facts without harmful omissions | Fact checks against the source of truth, citation-to-claim review, brand and product accuracy |
| Acquisition | Whether people or agents reach the owned surface | Referral sessions, server logs, landing pages, engaged visits |
| Outcome | Whether the exposure advances the real goal | Qualified leads, bookings, sales, sign-ups, assisted conversions |

Use a versioned query panel based on real audience tasks, not only brand-name prompts. Record engine or product, locale, account or personalization state where controllable, device, date, query wording, answer, mentions, citations, and cited URLs. Repeat samples over time because model, retrieval, and ranking changes make any single run unstable.

Compare like with like and retain raw snapshots. A vendor score can support
trend analysis, but it cannot prove complete market visibility or causal ROI.
Where the [Generative AI performance report](https://developers.google.com/search/blog/2026/06/gen-ai-performance-reports)
is available, use its impressions, pages, countries, devices, and dates as
dedicated Google visibility evidence while retaining the overall performance
view. Pair either view with analytics, logs, conversions, and periodic manual
accuracy review; neither report proves campaign ROI.

## Tactics Worth Testing

Treat these as experiments and review questions rather than ranking guarantees:

- Relevance coverage: address the user task, related entities, alternatives, constraints, evidence, and next steps instead of repeating one keyword.
- Information gain: add original data, examples, benchmarks, screenshots, prices, policies, expert commentary, or process detail that competitors lack.
- Citation consistency: make the same core facts appear consistently across website, profiles, feeds, PR, docs, reviews, and third-party directories.
- Passage quality: write sections that answer specific questions directly while linking to deeper detail.
- Topical authority: maintain a coherent cluster of pages that demonstrates real experience, not isolated one-off posts.
- Reputation surfaces: monitor reviews, forums, video, industry directories, partner pages, and press mentions, because AI answers may synthesize from off-site evidence.
- Measurement reality: track branded AI answers manually or with tools, but expect incomplete attribution. Do not promise clean ROI from GEO dashboards.

Avoid tactics that create short-lived AI visibility but increase brand, legal, and spam risk:

- fake third-party listicles,
- self-serving "best X" pages posing as neutral,
- spammed Q&A pages,
- prompt-injection text aimed at crawlers,
- hidden entity stuffing,
- auto-generated doorway pages,
- off-site review manipulation.

## AI/GEO Review Checklist

- Is the page indexable, canonical, snippet-eligible, and internally linked?
- Is the primary entity obvious in visible content and structured data?
- Are important facts visible in text and consistent with JSON-LD?
- Are expected authors, reviewers, sources, methods, publication dates, and material-update dates visible and accurate?
- Are Google Business Profile, Merchant Center, Search Console, and local citations up to date where relevant?
- Does each page answer a real user task better than competing generic pages?
- Does the page include original facts or evidence worth citing?
- Are sitemaps, `lastmod`, feeds, and push mechanisms aligned with real content changes?
- Are search, training, and user-agent crawler policies intentional?
- Are crawler identity, traffic volume, cost, and abuse controls observable without relying on the user-agent string alone?
- Is `llms.txt` or a Markdown mirror included only because a real audience or tool uses it?
- Does the measurement plan use a repeatable query panel and separate visibility, accuracy, acquisition, and outcomes without claiming false attribution precision?
