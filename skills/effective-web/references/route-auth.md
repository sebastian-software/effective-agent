# Auth and Security UX

Use this route for user-facing security flows where clarity, trust, and browser constraints matter.

## Workflow

1. Identify the security goal, user risk, attacker-relevant surface, and recovery path.
2. Make the safe path the easiest path without hiding important consequences.
3. Use browser-native capabilities for credentials, autocomplete, permissions, and secure context requirements.
4. Explain interruptions only when the user needs to decide or recover.
5. Verify accessibility, password manager compatibility, and failure states.

## Rules

- Default to passkeys/WebAuthn for new accounts; design enrollment, fallback, device-sync, and recovery as deliberate states, not an afterthought.
- Do not block password managers or paste unless there is a documented security requirement.
- Always verify origin, challenge, and signature server-side before trusting a WebAuthn assertion.
- Security copy should be precise, calm, and free of vague reassurance.
- Permission prompts need context before the browser prompt appears.
- Avoid leaking sensitive state through overly specific public error messages, including whether an account exists.

For passkey lifecycle, credential forms, recovery, security headers, permission prompts, and copy, read the reference below.

## References

- [auth-web-security.md](auth-web-security.md) - passkey/WebAuthn lifecycle, credential forms, recovery, sessions, security headers, permission prompts, and security copy.
