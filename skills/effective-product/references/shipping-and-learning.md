# Shipping and Learning

Treat a release as a controlled learning event, not as proof that the product
decision was correct or as the end of product work.

## Write the release decision

Before shipping, state:

- target user, situation, and expected progress
- release scope, non-goals, and exposure boundary
- riskiest assumption and evidence already available
- quality bar and unresolved known issues
- expected user and business signals
- guardrails, rollback conditions, and accountable owner
- learning window and next decision date

Use staged exposure when uncertainty or blast radius is high. Do not hide a
trust-critical failure behind an experiment label.

## Instrument the value path

Measure the transitions that support the product thesis:

```text
qualified arrival -> meaningful start -> first value -> repeated value -> retained outcome
```

Define each event in customer terms and verify that it is captured correctly.
Pair behavioral data with support, sales, interview, and operational evidence.
Traffic, impressions, downloads, and sign-ups are inputs; they do not establish
activation, retention, or value on their own.

Minimize collection and route tracking or consent requirements to
`effective-web`'s web legal-compliance route before implementation.

## Design a decision-grade experiment

For each experiment record:

1. decision it informs
2. hypothesis and strongest alternative explanation
3. target segment and eligibility
4. intervention and comparison
5. primary signal and guardrails
6. duration or evidence threshold
7. keep, change, stop, or escalate rule

Use qualitative tests for comprehension, motivation, and failure modes. Use
quantitative tests when the sample and instrumentation can distinguish a
meaningful change. Do not manufacture precision from a small or biased sample.

## Run the post-launch review

Compare expected and observed behavior without rewriting the original thesis.
Ask:

- Who adopted, who did not, and in what situations?
- Where did users fail to reach or repeat value?
- Did behavior differ by segment, channel, device, or touch model?
- What new support, reliability, privacy, or delivery burden appeared?
- Which result is causal evidence and which is only correlated?
- What should be kept, changed, stopped, or investigated next?

A launch spike from press, an influencer, or a platform does not establish a
repeatable distribution system. Separate qualified conversion and retention
from temporary attention.

## Iterate coherently

Prefer one deliberate follow-up that addresses the largest supported bottleneck.
Do not respond to weak launch results by simultaneously changing product,
audience, price, message, and channel; the team will not know what it learned.

## Quality Check

- Is the release attached to a decision and learning window?
- Are core quality, trust, rollback, and ownership explicit?
- Does instrumentation cover first and repeated value rather than vanity only?
- Are thresholds and stop rules defined before results arrive?
- Did the review include failures, non-adopters, and operational consequences?
- Is the next iteration small enough to preserve what was learned?
