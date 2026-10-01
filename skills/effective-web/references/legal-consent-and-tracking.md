# Consent and Tracking

Use this reference for cookies, pixels, SDKs, browser storage, session replay,
analytics, advertising, profiling, universal opt-out signals, consent banners,
or preference centers. Establish legal applicability with the regional route;
use this reference to turn that decision into coherent product behavior.

## Classify Before Designing

### Surface

- Public content, landing page, store, or checkout
- Authenticated app shell or account area
- Embedded widget, mobile webview, or companion app
- Privacy or cookie page and durable preference center

### Service

Classify each browser and server integration by actual behavior, not vendor
label:

- Strictly necessary for a user-requested service
- Functional or personalization
- Audience measurement, product analytics, experimentation, or performance
- Advertising, sale or sharing, cross-context targeting, or profiling
- Sensitive-data, child-directed, biometric, health, financial, or other
  regulated processing

Inventory cookies, local and session storage, cache or identifier access,
pixels, tag managers, SDK persistence, fingerprinting, request headers, and
server-side events. "Cookieless" does not prove that a service is exempt.

### Legal and policy tier

Define named behavior tiers only after regional research. A useful internal
model may distinguish:

| Tier | Behavior |
| --- | --- |
| Prior opt-in required | Keep every optional service off until a valid choice; offer accept, reject optional, and manage choices without deceptive pressure. |
| Notice and opt-out permitted | Start only the verified services, disclose them, and provide a durable and effective opt-out. Do not assume this tier from `US` alone. |
| Recognized opt-out signal | Apply the signal to the rights and services covered by current law and policy; explain the resulting state. |
| Necessary only | Run only services proven necessary for the requested function. Do not hide analytics inside this label. |
| Unresolved | Apply the fallback explicitly approved by Product/Legal; log the reason without collecting unnecessary location data. |

Geo-tiering can reduce friction, but it is an implementation strategy rather
than an applicability rule. Combine current device location, place of
establishment, intentional targeting, known account or transaction facts, and
recognized privacy signals as the applicable law requires. Document which
signal wins when they disagree.

## State and Runtime Architecture

- Make app-owned consent or privacy state authoritative. Treat tag managers and
  vendor consent APIs as downstream adapters.
- Define a versioned schema for categories, choice source, policy version,
  timestamp, and the minimum routing evidence needed. Avoid retaining raw IP or
  precise location merely to prove a tier.
- Migrate stored choices deliberately. Bump the policy or schema version when a
  prior choice would gain a new purpose, service, or meaning; do not reinterpret
  it silently.
- Resolve rules early enough to prevent optional capture during hydration or a
  client-side routing flash. Test edge, server, and browser signals together.
- Keep explicit opt-out or rejection effective across sessions, locales,
  devices where promised, and downstream services.
- Separate browser-side storage and capture from server-side operational events.
  Document their purpose, legal basis, retention, and controls independently.
- Verify each SDK's real persistence, anonymous or memory-only modes, replay,
  feature flags, automatic events, and shutdown behavior. Disable it when the
  approved tier cannot be implemented reliably.

## Interface Integrity

Choose the least intrusive interface that satisfies the verified tier:

- Use no banner when only necessary services run and no special notice is
  required; keep the relevant legal information reachable.
- Use an in-flow notice, compact non-obscuring card, or banner when a choice can
  coexist with the page. Mark a non-modal surface as a labelled region.
- Use a real modal only when the product intentionally blocks background use
  pending a valid decision. Move focus inside, keep the background inert, trap
  focus, provide an accessible name, and return focus logically.
- Keep a persistent privacy or cookie-settings entry point after dismissal so
  withdrawal and later choices are as usable as the initial action.

For a prior opt-in tier:

- Put accept, reject optional or necessary-only, and manage-preferences actions
  on the first layer when current law or guidance requires refusal parity.
- Keep optional categories off until selected.
- Do not use continued browsing, scrolling, inactivity, a preselected toggle,
  or a disguised "Continue" action as consent.
- Do not require optional processing to access the service unless qualified
  counsel has approved the exact conditional-access model.

Across all tiers, do not let the surface cover navigation, account controls,
forms, primary actions, or keyboard focus. A compact fixed card is acceptable
only after mobile, zoom, scrolling, and focus tests show it does not obscure the
application. Prefer direct labels such as "Accept all", "Reject optional",
"Manage preferences", and "Save preferences" over vague or coercive copy.

## GPC and Similar Signals

Check both `Sec-GPC: 1` and `navigator.globalPrivacyControl === true` when the
recognized signal and product architecture require it. A signal is not blanket
consent and does not have identical legal effect in every jurisdiction.

- Map it to the current statutory right, covered services, and precedence rule.
- Never infer that it disables all first-party analytics unless current law or
  approved policy says so.
- Do not let "Accept all" reverse a binding signal silently.
- Show a plain status in the preference center when the signal changes product
  behavior.
- Keep the server and browser interpretations consistent.

## Verification Matrix

Test at least:

- First visit with no stored choice
- Every legal or policy tier and the unresolved fallback
- Accept, reject optional, category customization, save, reopen, and withdrawal
- Recognized signal on and off, including conflicts with stored state
- Policy or schema migration from each supported prior version
- Failure or late arrival of geo, account, tag-manager, and SDK configuration
- Optional network and storage activity before and after each transition
- Mobile, 200 percent zoom, keyboard traversal, screen reader names, focus
  visibility, and reduced motion
- App navigation, forms, account controls, and task actions while a non-modal
  surface is visible
- Cross-locale text expansion and links to current legal pages

Capture network, storage, UI, and downstream SDK evidence. A correct banner
without correct runtime gating is not a correct implementation.

## Starting Sources

Verify current versions and regional applicability:

- [EDPB Cookie Banner Taskforce report](https://www.edpb.europa.eu/documents/task-force-report/report-of-the-work-undertaken-by-the-cookie-banner-taskforce_en)
- [EDPB consent guidelines (05/2020)](https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-052020-consent-under-regulation-2016679_en)
- [ICO cookies and similar technologies](https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/guide-to-pecr/cookies-and-similar-technologies/)
- [CNIL cookies and trackers guidance hub](https://www.cnil.fr/fr/cookies-et-autres-traceurs)
- [W3C Global Privacy Control](https://w3c.github.io/gpc/)
- [WCAG 2.2 Focus Not Obscured](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html)
- [WAI-ARIA modal dialog pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/)
