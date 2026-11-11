# Live Search and Release Verification

Use this reference when source files look correct but crawlers receive something
else, or when a release could change public-page discoverability. A local build
proves neither production delivery nor search indexing.

## Inspect what the public endpoint serves

Select representative public URLs: the homepage, affected templates, important
acquisition pages, and relevant host or protocol variants. Keep private,
authenticated, and intentionally excluded pages out of public-indexing checks.

Record the URL, time, request conditions, redirect chain, final status, response
headers, and relevant body evidence. Fetch the deployed `robots.txt`, sitemap,
and page HTML rather than relying on files in the project. Check:

- Expected canonical destinations, including HTTP-to-HTTPS and preferred-host
  redirects. A deliberate redirect is not a failed page merely because the
  first response is not `200`; inspect its destination and detect loops.
- Main text, titles, links, canonical, meta robots, and JSON-LD in the initial
  response, plus the rendered DOM when JavaScript changes them. Missing raw
  HTML text is a risk for non-rendering crawlers, not proof that every engine
  sees an empty page. Check the intended crawler's rendering behavior.
- `X-Robots-Tag` and other response headers alongside HTML directives. An
  apparently successful response can contain a challenge, login page, stale
  cache entry, or soft error instead of the intended content.
- Sitemap URLs against intended canonical, indexable destinations. A sitemap
  submission or successful fetch is not proof of indexing or AI citation.

Interpret status codes for the endpoint and crawler, not with a universal
"anything except 200 fails" rule. The robots-specific handling is maintained
in [AI Search, GEO, and Content Distribution](ai-geo-distribution.md#crawling-recrawling-and-push).
For redirect semantics, use [Google's redirect guidance](https://developers.google.com/search/docs/crawling-indexing/301-redirects).

## Isolate CDN, WAF, and crawler-policy differences

Compare a normal request with relevant crawler user agents as a diagnostic,
retaining headers and body evidence as well as the status. A user-agent spoof
does not authenticate a crawler or prove that real bot traffic can pass.
Where available, corroborate with provider URL inspection, verified crawler
traffic, and CDN/security logs; record unavailable evidence as not checked.

Separate origin behavior from the public edge response. Inspect managed
`robots.txt` additions, cached HTML and headers, redirects, bot challenges,
rate limits, and crawler-specific blocks. For example, Cloudflare can prepend
managed directives depending on configured policies; do not assume it always
does so. Check [Cloudflare's current managed robots behavior](https://developers.cloudflare.com/bots/additional-configurations/managed-robots-txt/)
and the site's actual settings. This provider behavior was last verified on
November 11, 2026.

Keep search, training, and user-directed access policies distinct, using
[LLM and Agent Access](ai-geo-distribution.md#llm-and-agent-access). Repair the
smallest demonstrated delivery failure. Do not disable a WAF, bot protection,
or authentication globally to make a synthetic crawler probe pass.

## Compare the release with its intended baseline

Before an affected deployment, retain a small manifest or existing monitoring
snapshot for the representative URLs: status and destination, canonical,
robots headers and meta directives, meaningful content, and sitemap membership.
Capture the relevant live robots policy separately. Reuse existing release
checks and artifacts; do not require a new monitoring service or full-site
crawl for a small content edit.

Declare intended changes, then compare the same observations after deployment:

| Unexpected change | What to investigate |
| --- | --- |
| Public page gains `noindex` | HTML directive, response header, inherited preview configuration |
| Canonical points elsewhere | Template data, host/environment defaults, conflicting canonicals |
| Useful page becomes missing or inaccessible | Route output, redirects, authentication, CDN/WAF response |
| Relevant crawler loses access | Deployed robots policy, managed additions, verified security events |
| Main content disappears despite a success status | Hydration/rendering failure, challenge, stale cache, soft error |

Return URL-level before/after evidence and distinguish intended exclusions or
moves from regressions. Keep a rollback or focused correction available for
high-impact changes. Act within the user's deployment authority; if only local
implementation is authorized, verify the preview and report production checks
as pending instead of deploying or claiming live success.

Recheck changed delivery behavior after correction. Then use the intended
provider's inspection/reporting when available; recrawling, indexing, and
answer updates can lag. Do not claim a ranking or citation recovery from an
HTTP response alone. Hand findings to `effective-marketing` when they affect
content priorities or interpretation of search outcomes.
