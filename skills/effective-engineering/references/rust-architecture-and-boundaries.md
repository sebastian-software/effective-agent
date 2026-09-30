# Architecture and Boundaries

Use this reference when designing, implementing, or reviewing a Rust crate or
workspace whose ownership, API, failure, concurrency, or operational boundaries
matter. Apply the rules as engineering constraints, not as a mandatory pattern
catalogue. Prefer repository evidence over generic thresholds.

## Contents

1. [Establish the architecture contract](#1-establish-the-architecture-contract)
2. [Use ownership as an architecture tool](#2-use-ownership-as-an-architecture-tool)
3. [Model domain invariants in types](#3-model-domain-invariants-in-types)
4. [Design stable APIs and trait boundaries](#4-design-stable-apis-and-trait-boundaries)
5. [Choose generics versus `dyn Trait`](#5-choose-generics-versus-dyn-trait)
6. [Design error and IO boundaries](#6-design-error-and-io-boundaries)
7. [Structure crates and workspaces](#7-structure-crates-and-workspaces)
8. [Document negative invariants](#8-document-negative-invariants)
9. [Apply the rust-analyzer case study](#9-apply-the-rust-analyzer-case-study)
10. [Build testing and observability boundaries](#10-build-testing-and-observability-boundaries)
11. [Design production workflows](#11-design-production-workflows)
12. [Run the architecture review](#12-run-the-architecture-review)
13. [Source map](#13-source-map)

## 1. Establish the architecture contract

### 1.1 Read the repository contract before editing

Inspect the workspace root, scoped `AGENTS.md`/contributor instructions,
`Cargo.toml` files, `Cargo.lock`, edition, MSRV, feature resolver, CI, lint and
format configuration, supported targets, async runtime, public crates, and
nearby tests before changing a boundary. Record what is stable, what is
internal, and which commands validate the changed surface.

Do not invent a stronger MSRV, a new runtime, a new crate, a target guarantee,
or a performance budget because a design article used one. Tie each decision to
the repository's actual contract.

**Source:** [Rust modules and packages](https://doc.rust-lang.org/stable/book/ch07-00-managing-growing-projects-with-packages-crates-and-modules.html) and [Quality and Review](rust-quality-and-review.md).

### 1.2 State the boundary in one paragraph

Before implementation, write down:

- accepted input and ownership of each input;
- output ownership and lifetime;
- mutation and side effects;
- expected errors and programmer-invariant failures;
- cancellation, ordering, backpressure, and concurrency;
- resource limits (memory, handles, tasks, retries);
- unsafe, FFI, serialization, persistence, and protocol obligations;
- the tests and measurements that would disprove the design.

If the paragraph cannot be written without hand-waving, the boundary is not
ready for implementation.

### 1.3 Separate the problem map from the implementation map

Start architecture documentation with a bird's-eye view of the problem and
the major data/control flows. Follow with a code map that answers both “where is
the code that does X?” and “what does this module do?”. Keep volatile algorithm
details in local rustdoc or design notes rather than in the top-level map.

**Source:** [matklad – `ARCHITECTURE.md`](https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html).

### 1.4 Treat API boundaries as stability decisions

Mark every crate or module that is consumed outside its implementation team.
Rules at a boundary differ from rules in a private helper: names, visibility,
serialization, semver, error shape, auto traits, and MSRV become compatibility
contracts. Make a public facade small enough that its maintenance burden is
visible.

**Source:** [rust-analyzer Architecture – Code Map and API Boundaries](https://rust-analyzer.github.io/book/contributing/architecture.html), [Rust API Guidelines – About](https://rust-lang.github.io/api-guidelines/).

## 2. Use ownership as an architecture tool

### 2.1 Encode the data-flow verb in the signature

Use a shared borrow when the callee only observes a value, a mutable borrow for
in-place mutation, and ownership when the callee stores, consumes, transforms,
or transfers the value.

```rust
fn inspect(config: &Config) -> Report { /* read only */ }
fn normalize(config: &mut Config) { /* mutate in place */ }
fn persist(config: Config, db: &Database) -> Result<Id, StoreError> { /* consume */ }
```

Do not accept `&mut T` merely because interior mutability makes it convenient;
make mutation part of the contract. Do not consume `T` if the operation only
needs a short read.

**Source:** [Rust ownership guide](https://doc.rust-lang.org/stable/book/ch04-00-understanding-ownership.html) and [Rust API flexibility guidelines](https://rust-lang.github.io/api-guidelines/flexibility.html).

### 2.2 Accept the borrowed type, not the owned wrapper

Prefer `&str` over `&String`, `&[T]` over `&Vec<T>`, and `&T` over `&Box<T>`
when ownership is not needed. This accepts more callers through deref coercion
and avoids an unnecessary level of indirection.

```rust
fn contains_marker(text: &str, marker: &str) -> bool { /* ... */ }

let owned = String::from("rust");
assert!(contains_marker(&owned, "us"));
assert!(contains_marker("rust", "us"));
```

Keep an owned parameter when the operation must retain it beyond the call or
when moving it avoids a copy at a meaningful boundary.

**Source:** [Rust Design Patterns – Use borrowed types for arguments](https://rust-unofficial.github.io/patterns/idioms/coercion-arguments.html).

### 2.3 Use `Cow` when ownership depends on runtime content

Return `Cow<'a, T>` when valid inputs can be returned borrowed but exceptional
inputs require an owned representation. Document when allocation occurs.

```rust
use std::borrow::Cow;

fn display_label(input: &str) -> Cow<'_, str> {
    if input.contains('_') {
        Cow::Owned(input.replace('_', " "))
    } else {
        Cow::Borrowed(input)
    }
}
```

Do not use `Cow` merely to avoid deciding a clear ownership contract; its value
comes from a real borrowed/owned runtime split.

**Source:** [`std::borrow::Cow`](https://doc.rust-lang.org/std/borrow/enum.Cow.html).

### 2.4 Return owned values across durable boundaries

Return owned data when it crosses a task, thread, cache, queue, persistence,
FFI, or protocol boundary. Do not force a caller to extend a borrow to keep a
worker alive. If the result can remain tied to an input and this is useful,
make that relationship explicit with a lifetime or `Cow`.

### 2.5 Use lifetimes to express relationships, not to extend storage

Treat a lifetime parameter as a relationship between borrows. It does not make
data live longer and it does not justify leaking, global storage, `Arc` cloning,
or unsafe lifetime extension.

```rust
fn header_value<'a>(headers: &'a [(String, String)], name: &str) -> Option<&'a str> {
    headers.iter()
        .find(|(key, _)| key.eq_ignore_ascii_case(name))
        .map(|(_, value)| value.as_str())
}
```

Prefer elided lifetimes when they express the same contract. Add explicit
lifetimes when the relationship is part of the API a caller must understand.

**Source:** [Rust lifetime guide](https://doc.rust-lang.org/stable/book/ch10-03-lifetime-syntax.html).

### 2.6 Diagnose `clone` before writing it

When a borrow-checker error suggests `clone`, first ask:

1. Which component should own the value?
2. Does the callee really need ownership, or only `&T`?
3. Can `mem::take`/`mem::replace` move the value while leaving a valid state?
4. Can the struct be split so two independent fields borrow independently?
5. Is duplicate ownership intentional and documented?

Clone only when the duplicate ownership is part of the contract or is proven
cheaper/safer than a redesign.

**Source:** [`std::mem::take`](https://doc.rust-lang.org/std/mem/fn.take.html) and [Rust ownership guide](https://doc.rust-lang.org/stable/book/ch04-00-understanding-ownership.html).

### 2.7 Use RAII for resource lifetime, not for fallible shutdown

Represent a resource lease with a guard whose borrow prevents use after the
resource is finalized. Use `Drop` for infallible cleanup (unlocking, releasing,
restoring state). Add an explicit `close`, `flush`, or `shutdown` method for
operations that can fail or block; never hide required error handling in
`Drop::drop`.

**Source:** [`Drop`](https://doc.rust-lang.org/std/ops/trait.Drop.html) and [Rust API dependability guidelines](https://rust-lang.github.io/api-guidelines/dependability.html).

## 3. Model domain invariants in types

### 3.1 Parse directly into a validated domain type

Make the constructor or parser the validation boundary, then pass the validated
domain type through downstream layers instead of repeatedly checking a raw
string or number. Keep its representation private so ordinary code cannot bypass
the invariant. This example applies that rule to a capacity of 1 through 4096;
choose a bound from the actual workload.

```rust
use std::num::NonZeroUsize;

pub struct BatchLimit(NonZeroUsize);

#[derive(Debug)]
pub struct InvalidBatchLimit;

impl TryFrom<usize> for BatchLimit {
    type Error = InvalidBatchLimit;

    fn try_from(value: usize) -> Result<Self, Self::Error> {
        NonZeroUsize::new(value)
            .filter(|limit| limit.get() <= 4096)
            .map(Self)
            .ok_or(InvalidBatchLimit)
    }
}
```

After construction, downstream code may rely on the invariant. Preserve the
raw input separately only when error reporting or auditing genuinely needs it.

**Source:** [`TryFrom`](https://doc.rust-lang.org/std/convert/trait.TryFrom.html), [`NonZeroUsize`](https://doc.rust-lang.org/std/num/type.NonZeroUsize.html), and [Rust API type-safety guidelines](https://rust-lang.github.io/api-guidelines/type-safety.html).

### 3.2 Use newtypes for stable semantic distinctions

Wrap equal representations when confusing them would be a correctness or
security defect: `UserId(Uuid)`, `OrderId(Uuid)`, `Meters(f64)`,
`UntrustedPath(PathBuf)`, or a capability token. Keep the field private and
provide only the conversions/operations that preserve the distinction.

Do not wrap every primitive. Add a newtype when it supplies an invariant,
meaning, trait behavior, or a future-compatible boundary.

**Source:** [Rust API newtype guidelines](https://rust-lang.github.io/api-guidelines/type-safety.html).

### 3.3 Use enums for lifecycle states

Replace a boolean plus undocumented side conditions with an enum that makes
states and transitions explicit.

```rust
enum Connection {
    Connecting { attempt: u32 },
    Ready { socket: TcpStream },
    Closed { reason: CloseReason },
}
```

Make transitions consume or mutably transform the state so impossible
operations are rejected at compile time or returned as an explicit error.

### 3.4 Use builders for multi-policy construction

Use a builder when a type has multiple optional policies, defaults, or validation
steps. Keep the final type immutable where possible and let `build` return a
structured error that identifies invalid combinations.

Use `Default` for a meaningful safe baseline and keep a `new` constructor when
an empty/default value is a conventional, useful starting point.

**Source:** [Rust API Guidelines – C-BUILDER/C-COMMON-TRAITS](https://rust-lang.github.io/api-guidelines/type-safety.html), [Rust Design Patterns – Constructors and Default](https://rust-unofficial.github.io/patterns/rust-design-patterns.pdf).

### 3.5 Choose `#[non_exhaustive]` for extensible public enums/structs

Apply `#[non_exhaustive]` when adding variants or fields is a planned
compatible evolution. Document the wildcard handling consumers need. Leave a
public enum exhaustive only when the set is deliberately closed and changing it
is a planned breaking release.

**Source:** [Rust Design Patterns – `#[non_exhaustive]`](https://rust-unofficial.github.io/patterns/rust-design-patterns.pdf); [Rust API Guidelines – Future proofing](https://rust-lang.github.io/api-guidelines/future-proofing.html).

### 3.6 Use `bitflags` for independent flags

Use a bitflag type when multiple options can be active simultaneously. Use an
enum when exactly one alternative is valid. Avoid a growing list of boolean
parameters that hides the state space.

**Source:** [Rust API Guidelines – C-BITFLAG](https://rust-lang.github.io/api-guidelines/type-safety.html).

## 4. Design stable APIs and trait boundaries

### 4.1 Minimize visibility

Start all modules, fields, helpers, and constructors private. Promote only the
symbols that are part of a stable consumer contract. Use `pub(crate)`,
`pub(super)`, or `pub(in path)` for narrower collaboration.

```rust
pub struct Parser { cache: Cache }

impl Parser {
    pub fn parse(&self, input: &str) -> Result<Ast, ParseError> { /* ... */ }
    pub(crate) fn cache_stats(&self) -> Stats { /* internal */ }
}
```

Treat every additional `pub` as a future compatibility obligation: it can
freeze storage, algorithm choices, auto-traits, or error details.

**Source:** [Rust visibility and privacy](https://doc.rust-lang.org/reference/visibility-and-privacy.html).

### 4.2 Make names predict cost and ownership

Follow the Rust conversion vocabulary:

- `as_*`: normally a cheap borrowed view;
- `to_*`: representation change that may do work or allocate;
- `into_*`: consumes ownership and returns an owned representation.

Name getters as `field()`/`field_mut()` unless `get` communicates a checked
lookup. Name collection iterators `iter`, `iter_mut`, and `into_iter`; name
their iterator types accordingly.

**Source:** [Rust API Guidelines – Naming](https://rust-lang.github.io/api-guidelines/naming.html).

### 4.3 Implement common traits at the defining crate

Implement applicable `Debug`, `Display`, `Default`, `Clone`, `Eq`, `Ord`, and
`Hash` traits when you define a type. Orphan rules prevent downstream crates
from filling every omission. Avoid deriving a trait whose semantics would lie;
write a deliberate implementation or omit it.

Implement `From`/`TryFrom`, `AsRef`, and `AsMut` where the conversion is
natural. Implement `FromIterator` and `Extend` for collection-like types.

**Source:** [Rust API Guidelines – Interoperability](https://rust-lang.github.io/api-guidelines/interoperability.html).

### 4.4 Keep smart pointers unsurprising

Use `Deref` to expose the natural borrowed view of a smart pointer or collection.
Do not use it to simulate class inheritance or to leak a large hidden method
surface. Prefer explicit facade methods or a trait when the relationship is
semantic rather than pointer-like.

**Source:** [Rust API Guidelines – C-DEREF](https://rust-lang.github.io/api-guidelines/predictability.html); [Rust Design Patterns – Deref polymorphism](https://rust-unofficial.github.io/patterns/rust-design-patterns.pdf), pp. 68–70.

### 4.5 Keep public dependency coupling intentional

If a third-party type appears in your public API, either re-export it as part of
your contract or wrap it in your own type. Otherwise, consumers must depend on
your dependency directly and its version becomes an accidental API constraint.

Avoid wildcard imports from dependencies you do not control; a minor release
can add a trait or method that creates ambiguity.

**Source:** [Rust API necessity guidelines](https://rust-lang.github.io/api-guidelines/necessities.html).

### 4.6 Make documentation part of the API

Document error conditions, panic conditions, safety requirements, ownership
effects, blocking behavior, cancellation, and feature requirements for every
public operation. Add a rustdoc example that uses the public interface. Do not
expose implementation details that are not a compatibility promise.

**Source:** [Rust API Guidelines – Documentation](https://rust-lang.github.io/api-guidelines/documentation.html); [Rust API Guidelines – C-FAILURE](https://rust-lang.github.io/api-guidelines/documentation.html).

### 4.7 Seal extension points deliberately

Use a private supertrait to seal a trait when downstream implementations would
prevent future methods or variants. Leave a trait open when external
implementations are the purpose. Document which side owns the exhaustive list.

```rust
mod private { pub trait Sealed {} }
pub trait Transport: private::Sealed {
    fn send(&self, bytes: &[u8]) -> Result<(), SendError>;
}
```

**Source:** [Rust API Guidelines – C-SEALED](https://rust-lang.github.io/api-guidelines/future-proofing.html), [Rust Design Patterns – Single Choice principle](https://rust-unofficial.github.io/patterns/additional_resources/design-principles.html).

## 5. Choose generics versus `dyn Trait`

### 5.1 Start with the concrete need

Use a concrete type when there is one implementation and no evidence of
substitution. Add a generic parameter when callers choose a type and static
dispatch is useful. Add a trait when substitution is a real boundary, not merely
to mock a private one-method helper.

**Source:** [Rust trait-object guide](https://doc.rust-lang.org/stable/book/ch18-02-trait-objects.html) and [Rust API flexibility guidelines](https://rust-lang.github.io/api-guidelines/flexibility.html).

### 5.2 Use generics for static dispatch and caller-selected types

Use `T: Trait` when the implementation benefits from inlining/monomorphization,
the set of types is chosen by the caller, or the API should preserve associated
types and compile-time guarantees.

```rust
fn encode<W: Write>(value: &Value, mut out: W) -> Result<(), EncodeError> {
    /* W is selected at the call site; no heap object is required. */
    Ok(())
}
```

Keep generic bounds at the method that needs them rather than duplicating them
on the entire struct or deriving unnecessary bounds on data containers.

### 5.3 Use `dyn Trait` at a small heterogeneous boundary

Use `Box<dyn Trait>`, `&dyn Trait`, or `Arc<dyn Trait>` when the runtime must
hold different implementations in one collection, load plugins, or cross an
explicit application boundary. Isolate the dynamic dispatch in an adapter and
keep the computation-heavy core generic or concrete when appropriate.

```rust
pub struct PluginHost {
    plugins: Vec<Box<dyn Plugin + Send + Sync>>,
}
```

Document object-safety, thread-safety, allocation, and dispatch costs. Do not
turn every internal function into a trait object just to make tests convenient.

**Source:** [Rust trait-object guide](https://doc.rust-lang.org/stable/book/ch18-02-trait-objects.html) and [Rust dyn compatibility](https://doc.rust-lang.org/reference/items/traits.html#dyn-compatibility).

### 5.4 Check object safety before publishing a trait

If a trait is intended for `dyn Trait`, keep dispatchable methods object-safe.
Move constructors, generic methods, or methods returning unconstrained `Self`
behind `where Self: Sized`, or split the trait into an object-safe runtime
interface and a construction/configuration interface.

### 5.5 Use closures as lightweight policies

For one-shot or local algorithm substitution, pass a closure or generic
function rather than introducing a named strategy hierarchy. Promote it to a
trait only when the policy is a stable reusable boundary or needs associated
types/stateful behavior.

**Source:** [Rust Design Patterns – Strategy/Policy](https://rust-unofficial.github.io/patterns/rust-design-patterns.pdf).

## 6. Design error and IO boundaries

### 6.1 Separate domain, adapter, operator, and protocol errors

Define error layers with different consumers:

1. **Domain/control-flow:** matchable variants such as `InvalidBatchLimit` or
   `AlreadyExists`.
2. **Adapter:** source errors from SQL, HTTP, filesystem, or queues, preserving
   the cause and adding operation context.
3. **Operator:** logs/telemetry with root cause and correlation fields.
4. **Protocol edge:** stable HTTP/LSP/CLI status and sanitized message.

Do not make a single error enum carry every dependency's entire API or expose
internal database details through a public protocol.

**Source:** [`std::error::Error`](https://doc.rust-lang.org/std/error/trait.Error.html) and [Errors and Concurrency](rust-errors-and-concurrency.md).

### 6.2 Choose `thiserror` versus opaque application errors by consumer

Use a structured enum for a library or domain boundary whose callers need to
match variants. Use an opaque error with context at an application composition
root when callers only need to report or terminate. Do not erase errors before
the layer that must make a control-flow decision.

### 6.3 Preserve root cause and log once at the useful boundary

Attach context at each operation boundary (`read config`, `insert subscriber`,
`send confirmation email`) while retaining the source chain. Log when the
system can choose a response, retry, rollback, or alert. Propagate otherwise;
do not log the same failure at every stack layer.

### 6.4 Treat broken input as a data result in tooling

For parsers, IDEs, linters, and configuration editors, return partial output
plus diagnostics where possible. Reserve `Result::Err` for inability to produce
the promised model or for infrastructure failures.

```rust
fn parse_file(text: &str) -> (SyntaxTree, Vec<Diagnostic>) { /* resilient */ }
```

**Source:** [rust-analyzer Architecture – parser and Error Handling](https://rust-analyzer.github.io/book/contributing/architecture.html).

### 6.5 Keep IO at the outside of the core

Make core domain, syntax, and query modules deterministic and free of filesystem,
network, LSP, and environment reads. Pass snapshots or abstract inputs inward;
perform IO in adapters and convert results at the boundary.

This keeps unit tests reproducible, allows parallel or incremental computation,
and prevents a server's working directory or global environment from leaking
into semantics.

**Source:** [rust-analyzer Architecture – `base-db`, `syntax`, `toolchain`, and Error Handling](https://rust-analyzer.github.io/book/contributing/architecture.html).

### 6.6 Make destructors infallible and non-blocking

Never depend on `Drop` to report a required failure. Expose explicit shutdown
for flushing, network close, joining, or remote cleanup. Document whether the
explicit method is idempotent and what happens if callers omit it.

**Source:** [`Drop`](https://doc.rust-lang.org/std/ops/trait.Drop.html) and [Rust API dependability guidelines](https://rust-lang.github.io/api-guidelines/dependability.html).

### 6.7 Keep serialization at the protocol boundary

Do not derive `Serialize`/`Deserialize` on every internal type. Treat every
serialized type as a compatibility contract. Define DTOs at the client/protocol
edge and convert explicitly to/from internal types.

**Source:** [rust-analyzer Architecture – Serialization](https://rust-analyzer.github.io/book/contributing/architecture.html); [Rust API Guidelines – Documentation/Future proofing](https://rust-lang.github.io/api-guidelines/).

## 7. Structure crates and workspaces

### 7.1 Let crates form an intentional dependency DAG

Create a crate when a component needs an independently reviewable API, test
surface, build unit, or dependency policy. Keep the dependency direction
acyclic and document which crates are API boundaries. Keep purely local details
in modules rather than creating crates for every file.

**Source:** [The Rust Programming Language – Packages, Crates, and Modules](https://doc.rust-lang.org/stable/book/ch07-00-managing-growing-projects-with-packages-crates-and-modules.html); [rust-analyzer Architecture – Code Map](https://rust-analyzer.github.io/book/contributing/architecture.html).

### 7.2 Use a flat `crates/` workspace layout when it improves navigation

For a medium-to-large multi-crate repository, start with a virtual root
manifest and one level of named crates:

```toml
[workspace]
members = ["crates/*"]
```

Keep directory names equal to crate names. Adopt nested folders only when they
encode a real ownership or dependency boundary and remain easier to navigate.

Centralize shared dependency versions in the root `[workspace.dependencies]`
table and shared lint policy in `[workspace.lints]`, with member crates
inheriting through `workspace = true`; this removes version drift between
member crates without changing the flat layout.

**Source:** [matklad – Large Rust Workspaces](https://matklad.github.io/2021/08/22/large-rust-workspaces.html);
[Cargo Reference – Workspaces](https://doc.rust-lang.org/cargo/reference/workspaces.html).

### 7.3 Separate internal and publishable crates

Mark internal crates as non-publishable and keep their versioning policy simple.
Place semver-stable libraries in a clearly named public area and prevent them
from depending on application-internal crates. Review public dependencies for
license, MSRV, feature, and stability guarantees.

### 7.4 Centralize automation in `cargo xtask`

Put release preparation, code generation, installation, fixture updates, and
repository checks in a typed `xtask` crate. Keep shell scripts as thin launchers
when the repository needs them. Give generated outputs an explicit owner and
validation command.

**Source:** [matklad – Large Rust Workspaces](https://matklad.github.io/2021/08/22/large-rust-workspaces.html), [rust-analyzer Architecture – `xtask` and Code generation](https://rust-analyzer.github.io/book/contributing/architecture.html).

### 7.5 Keep a stable source layout even for small crates

Keep `src/lib.rs`/`src/main.rs` in `src/` even when the crate currently has one
file. Avoid layout exceptions that make later extraction, tooling, and codegen
harder.

### 7.6 Control features and dependency graph growth

Name Cargo features after the capability they enable; do not use placeholder
names such as `use-std` or negative features. Keep features additive and inspect
the graph for accidental transitive coupling. Treat a dependency appearing in a
public type as a deliberate design decision.

**Source:** [Cargo features](https://doc.rust-lang.org/cargo/reference/features.html) and [Rust API feature naming](https://rust-lang.github.io/api-guidelines/naming.html).

## 8. Document negative invariants

### 8.1 Maintain a concise `ARCHITECTURE.md`

Write a short document with:

1. product/problem bird's-eye view;
2. crate/module code map;
3. public API boundaries;
4. dependency direction;
5. negative invariants (what must not happen);
6. cross-cutting concerns and ownership.

Name important files, modules, and types without linking to fragile line
numbers. Revisit the document periodically, not on every implementation edit.

**Source:** [matklad – `ARCHITECTURE.md`](https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html).

### 8.2 Write invariants as enforceable rules

Replace vague prose such as “keep layers clean” with rules a reviewer or test
can check:

- `syntax` does not depend on LSP or query database crates.
- Domain crates do not read environment variables or open sockets.
- Only the protocol crate serializes LSP/HTTP DTOs.
- Internal query crates do not become public API boundaries.
- A changed function body must not invalidate unrelated global summaries.

If an invariant cannot be checked, state what evidence would establish it and
add a test, dependency check, or code review gate.

### 8.3 Keep generated code and bootstrapping boundaries explicit

Record which files are generated, the command that regenerates them, and why
the generator does not depend on the generated binary. Avoid bootstrapping when
it would make clean builds circular or fragile.

**Source:** [rust-analyzer Architecture – Code generation](https://rust-analyzer.github.io/book/contributing/architecture.html).

## 9. Apply the rust-analyzer case study

Use rust-analyzer as a reference architecture for large, long-running,
incremental Rust systems. Do not copy its crates mechanically; copy the
invariants and boundary discipline.

### 9.1 Separate ground state from derived state

Keep source files and an abstract crate graph as input state. Compute syntax,
HIR, type inference, and IDE features lazily through queries. Keep build-system
details and file paths behind adapters rather than embedding them in semantic
types.

### 9.2 Give each abstraction layer a deliberate API shape

- Parser: flat events and diagnostics; no dependence on a particular tree.
- Syntax: value-type tree per file; no semantic context.
- Query internals: raw IDs and incremental data; no public facade promise.
- HIR: resolved facade for semantic consumers.
- IDE: serializable-in-concept POD/view-model types using editor vocabulary.
- Binary/protocol: LSP and JSON conversion only at the edge.

**Source:** [rust-analyzer Architecture – Bird's Eye View and Code Map](https://rust-analyzer.github.io/book/contributing/architecture.html).

### 9.3 Isolate hostile or unstable extensions

Run untrusted proc macros in a separate process. Keep path resolution explicit
for multi-project or remote servers. Convert cancellation into a typed result at
the first stable boundary. Keep a broken project partially usable.

### 9.4 Use snapshots and fixtures to protect semantics

Centralize the API call in a small helper, represent input as fixtures, and
compare stable snapshots. Avoid tests that bind to private API shape when the
behavior can be tested through a boundary.

### 9.5 Build observability into the event loop

Prefer an explicit event enum and request loop when all triggers and costs need
to be visible. Add hierarchical profiles and object counts behind controlled
configuration. Keep profiling cheap enough for representative production-like
diagnostics, but document its overhead.

## 10. Build testing and observability boundaries

### 10.1 Place tests at three intentional levels

Use fast unit/property/snapshot tests for pure domain and syntax rules. Use
boundary tests for a public Rust API or service composition. Use a small number
of heavy tests for real files, Cargo, databases, network adapters, or LSP/HTTP
protocols.

Avoid duplicating the same contract at every level. Make the cheapest test the
one that catches the defect.

**Source:** [rust-analyzer testing architecture](https://rust-analyzer.github.io/book/contributing/architecture.html).

### 10.2 Keep test input deterministic

Do not let core tests depend on real time, network, process environment, current
directory, or an external database. Inject clocks, clients, paths, and stores at
the boundary. Reserve side-effect tests for explicit adapters and isolate their
state.

### 10.3 Use property tests for invariants, not for every function

Generate representative invalid and valid values for parsers, validators,
serialization round trips, and state transitions. State the property first:

- successful `TryFrom` values satisfy the invariant;
- parsing then rendering preserves the intended semantic model;
- replaying an idempotent request returns the same committed result;
- a cancellation leaves no partially visible state.

### 10.4 Instrument operations with structured context

Use `tracing` spans or the repository's equivalent to carry request ID,
operation name, entity identifiers, retry count, and duration across async
boundaries. Redact secrets and avoid making `Debug` output a data-exfiltration
path.

**Source:** [`tracing`](https://docs.rs/tracing/latest/tracing/) and [Rust API debuggability guidelines](https://rust-lang.github.io/api-guidelines/debuggability.html).

### 10.5 Profile before changing architecture for speed

State the workload and boundary, measure representative behavior, and identify
whether cost comes from algorithm, IO, synchronization, allocation, copying,
cache locality, dispatch, or build configuration. Apply the smallest change and
retain a benchmark or regression check.

Do not select `Arc`, boxing, smaller integer widths, `inline`, LTO, or a new
collection solely from object size or a generic blog rule.

**Source:** [rust-analyzer performance diagnostics](https://rust-analyzer.github.io/book/contributing/architecture.html) and [Benchmark Methodology](benchmark-methodology.md).

## 11. Design production workflows

### 11.1 Build dependencies at the composition root

Construct configuration, database pools, HTTP clients, telemetry, and task
supervision once at startup. Pass them explicitly to handlers/services. Keep
domain code free of hidden global state, direct environment reads, and implicit
runtime initialization.

**Source:** [Services, Data, and Async](services-data-and-async.md).

### 11.2 Test services through the public boundary

Make an integration test start the application through the same composition
path as production and call its public HTTP/API boundary. Keep private handler
tests for local transformations; use boundary tests to verify wiring, state,
serialization, and error mapping.

### 11.3 Keep database transactions explicit

Group changes that must be atomic in a transaction. Define which layer owns the
transaction and which errors trigger rollback. Do not spread transaction
ownership across unrelated handlers or adapters.

**Source:** [`sqlx::Transaction`](https://docs.rs/sqlx/latest/sqlx/struct.Transaction.html) and [Transactions and Consistency](transactions-and-consistency.md).

### 11.4 Make SQL/build validation reproducible

Use the repository's supported SQLx offline metadata or equivalent query
validation so a production build does not require a developer database. Check
that CI regenerates or validates metadata intentionally.

**Source:** [SQLx query validation and offline mode](https://docs.rs/sqlx/latest/sqlx/macro.query.html).

### 11.5 Keep blocking work away from async executors

Identify password hashing, compression, filesystem work, CPU-heavy parsing, and
blocking FFI calls. Run them through an explicit blocking pool or worker
boundary, size the pool, and expose cancellation/timeout behavior. Do not hide
blocking work inside an async function merely because it has an `.await` later.

**Source:** [Tokio blocking-task boundary](https://docs.rs/tokio/latest/tokio/task/fn.spawn_blocking.html).

### 11.6 Specify retry and idempotency before adding retries

For every retried side effect, define:

1. idempotency key scope and lifetime;
2. atomic reservation/uniqueness mechanism;
3. response/result persistence;
4. concurrent duplicate behavior;
5. timeout and retry budget;
6. compensation or recovery after partial failure.

Use save-and-replay for stateful idempotency or a deterministic key only when
the operation and time semantics support it. Never add an unbounded retry loop.

**Source:** [Transactions and Consistency](transactions-and-consistency.md) and [API and Interface Contracts](api-and-interface-contracts.md).

### 11.7 Choose recovery explicitly

For a distributed workflow, choose backward recovery (compensating action),
forward recovery (retry/continue), or asynchronous processing. Document what a
crash between two external effects leaves behind and how the next attempt
repairs or observes it.

**Source:** [Transactions and Consistency](transactions-and-consistency.md).

### 11.8 Keep security at both domain and operational boundaries

Model authentication/session states explicitly. Hash passwords without blocking
the async executor. Prevent user enumeration, protect secrets from logs and
debug output, define TLS/session-store policies, and test the failure paths.

**Source:** [API and Interface Contracts](api-and-interface-contracts.md) and [Rust API debuggability guidelines](https://rust-lang.github.io/api-guidelines/debuggability.html).

## 12. Run the architecture review

### 12.1 Ownership review

- Does every signature state observe, mutate, consume, or return ownership?
- Does any `clone` exist only to silence a compiler error?
- Does data cross a task/thread/cache/persistence boundary with the correct
  ownership and lifetime?
- Can RAII cleanup fail or block? If so, where is explicit shutdown?

### 12.2 Domain and API review

- Are stable distinctions represented by private newtypes/enums?
- Can invalid values be constructed outside the validating module?
- Are `pub` fields, enum variants, error variants, features, and auto traits
  intentional compatibility promises?
- Are conversion/getter/iterator names predictable?
- Are common traits and `From`/`TryFrom` implementations present where needed?
- Is third-party coupling in the public API deliberate?

### 12.3 Trait and dispatch review

- Is a trait required by demonstrated substitution or only by a test mock?
- Is the implementation statically dispatched where that matters?
- Is `dyn Trait` isolated to a small heterogeneous boundary?
- Is object safety documented and tested?
- Would a closure, enum, or concrete type be clearer?

### 12.4 Error and boundary review

- Are domain, adapter, operator, and protocol errors distinct?
- Is root cause retained and logged once at the useful boundary?
- Does broken user input produce diagnostics/partial results where possible?
- Are IO, environment, serialization, and protocol types kept at the edge?
- Are cancellation and partial failure represented in the contract?

### 12.5 Workspace and invariant review

- Does the crate graph remain acyclic and readable?
- Are internal and publishable crates separated?
- Are features additive, named after capabilities, and tested in combinations?
- Is automation owned by a typed `xtask` or equivalent?
- Are negative invariants documented and enforced by dependencies/tests?
- Can a broken build leave useful tooling functionality available?

### 12.6 Production and evidence review

- Are composition-root dependencies explicit and testable?
- Are transactions, retries, idempotency, and recovery specified before code?
- Is blocking work excluded from async executors?
- Are tests deterministic and placed at the cheapest useful boundary?
- Are logs structured, correlated, and secret-safe?
- Was every performance claim measured on the representative workload and
  build/target configuration?

### 12.7 Capture the boundary decision

For a durable boundary choice, name what an ADR would record; create the record
only when the user authorizes that artifact, using `effective-product`'s
convention:

1. problem and constraints;
2. chosen ownership and API shape;
3. alternative (concrete/generic/`dyn`, enum/newtype, sync/async);
4. failure, cancellation, and recovery contract;
5. dependency direction and negative invariants;
6. tests, telemetry, and performance evidence;
7. migration and compatibility plan.

Keep the record stable and link it from the architecture map; do not turn the
map into a changelog.

## 13. Source map

- [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)
- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)
- [Rust Design Patterns](https://rust-unofficial.github.io/patterns/) and [PDF](https://rust-unofficial.github.io/patterns/rust-design-patterns.pdf)
- [rust-analyzer Architecture](https://rust-analyzer.github.io/book/contributing/architecture.html)
- [Large Rust Workspaces](https://matklad.github.io/2021/08/22/large-rust-workspaces.html)
- [ARCHITECTURE.md](https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html)
