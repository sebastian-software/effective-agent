# Route: Rust Unsafe, FFI, SIMD, and Parallelism

Use this route for every unsafe block, unsafe trait implementation, raw
pointer, foreign call, or ABI boundary, and for auto-vectorization, portable
SIMD, intrinsics, target features, atomics, Rayon, thread pools, or CPU-heavy
async work.

Start from the Rust entry route for the ownership, naming, error, and review
contract; come here for the low-level decision.

## Read

- [Unsafe and FFI](rust-unsafe-and-ffi.md) — required for every unsafe block,
  unsafe trait implementation, raw pointer, foreign call, or ABI boundary.
- [SIMD and parallelism](rust-simd-and-parallelism.md) — a deep CPU, SIMD,
  atomics, and scheduling reference for specialist optimization work; routine profiling and
  unsafe reviews load the focused references first.

## Apply

- Write the safety argument, not just the `unsafe` block. Every unsafe operation
  needs a stated invariant, the reason it holds here, and what would break it.
- Scope suppressions narrowly. Explain why a local `allow`, `expect`, unsafe
  operation, or manual `Send`/`Sync` is sound and when it can be removed.
- Derive atomic ordering from a happens-before argument, not from a table of
  orderings.
- Treat Rayon chunking, async blocking work, queue bounds, and shutdown as
  resource and lifecycle contracts rather than throughput folklore.
- Keep specialized SIMD or target-feature paths behind a safe fallback and a
  documented dispatch contract.

## Cross-links

- Measurement, profiling, and layout decisions are the Rust Performance and
  Memory route.
- Benchmark construction and interpretation are the Benchmarks route.
- Executing an existing Miri, sanitizer, or fuzz command belongs to
  `effective-delivery`.
