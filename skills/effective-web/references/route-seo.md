# Frontend SEO and AI Search

Use this route for the frontend details that make public pages understandable to search engines, AI search systems, link previews, agents, and users before they click.

## Workflow

1. Identify page intent, canonical URL, primary entity, search surface, and target preview text.
2. Set title, description, canonical, robots behavior, and social metadata.
3. Add structured data only when it accurately represents visible page content.
4. Verify crawlable rendered content, heading structure, image alt text, internal links, and entity consistency.
5. For local or business facts, define the source of truth and sync it across website, structured data, Google Business Profile, Merchant Center, feeds, and citations.
6. For editorial content, verify authorship, evidence, publication history, and material updates in visible content and matching structured data.
7. Define GEO sampling and instrumentation across visibility, factual accuracy,
   acquisition, and outcomes; use repeatable samples instead of a single tool snapshot.
8. Read [Live Search and Release Verification](seo-release-verification.md) for
   production crawler/CDN diagnosis, deployment baselines, and indexability
   regressions. Check previews, business profiles, and instrumentation as relevant.

Search opportunity selection, decision-page priorities, distribution strategy,
AI answer-accuracy review, and interpretation of business outcomes belong to
`effective-marketing` through **SEO and AI Search Visibility**. Return technical
findings and measured evidence to that route; implement the authorized fixes
without requiring a separate approval for each routine change.

## Rules

- Metadata must describe the actual page, not a generic product promise.
- Avoid duplicate titles and descriptions across important pages.
- Structured data must not invent claims or hidden content.
- Public pages need meaningful server-rendered or reliably rendered content.
- Performance, accessibility, and content clarity are SEO inputs.
- Google generative search does not require `llms.txt`, AI text files, special Markdown, or special schema.org markup; do not prescribe them as Google ranking requirements.
- AI/GEO work should improve extractable facts, entity clarity, and crawler access policy, not chase prompt-injection or keyword-stuffing tactics.
- Distinguish an absent `robots.txt` from an unreachable one. For Google, most
  `4xx` responses mean no crawl restrictions, while `5xx`, DNS, and network
  failures can pause crawling temporarily; do not claim that a missing file by
  itself removes a site from the index.
- Keep business facts consistent across the visible page, JSON-LD, Search Console, Google Business Profile, Merchant Center, social profiles, review sites, and local citations.
- Do not manufacture authority or freshness with generic bylines, unsupported biographies, fake citations, or unchanged `dateModified` and sitemap `lastmod` values.
- Keep mentions, citations, referrals, conversions, and answer accuracy as separate measurements; no single GEO visibility score proves traffic or ROI.

## References

- [seo.md](seo.md) - frontend SEO metadata, structured data, and implementation checks.
- [seo-release-verification.md](seo-release-verification.md) - live delivery,
  CDN/WAF differences, redirect and indexability checks, and release comparison.
- [ai-geo-distribution.md](ai-geo-distribution.md) - AI search/GEO, entity authority, editorial provenance, business data distribution, LLM crawler access, agent-readable content, and measurement.
