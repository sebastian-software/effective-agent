# Route: Rust Architecture and Boundaries

Use this route when the task changes crate or module structure, public
interfaces, services, domain types, persistence, async boundaries, or project
organization in a Rust workspace.

Start from the Rust entry route for the ownership, naming, error, and review
contract; come here for the structural decision.

## Read

[Architecture and boundaries](rust-architecture-and-boundaries.md) — the
comprehensive Rust architecture casebook. For an ordinary API or failure task,
load the focused ownership and error references from the Rust entry route first;
come here only for cross-cutting workspace and production-boundary work.

## Apply

- Make crate and module boundaries carry dependency direction, stability
  promises, and explicit negative invariants.
- Keep I/O and serialization at the boundary when a pure core improves testing
  or incremental computation.
- Make invalid states difficult to represent when the domain distinction is
  stable and valuable — not as a reflex.
- Add a trait, generic, macro, or adapter only for demonstrated variation or
  reuse.

## Cross-links

- System-level service boundaries, quality attributes, ownership, and deployment
  direction — above the workspace — are the Architecture route.
- Data models, transactions, consistency, and migration semantics are the Data
  route.
- Behavior-preserving ports and repository-wide audits belong to
  `effective-delivery`.
