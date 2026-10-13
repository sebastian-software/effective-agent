# Performance Engineering for Rust

Use this reference for measurement-driven runtime optimization, profiling,
compiler and build optimization, and the choice of measurement tools. For
concrete memory layouts, containers, and binary-size details additionally read
[Memory and data layout](rust-memory-and-data-layout.md).

## Contents

- [Working contract and measurement workflow](#working-contract-and-measurement-workflow)
- [Benchmark design with Criterion](#benchmark-design-with-criterion)
- [Profiling and flamegraphs](#profiling-and-flamegraphs)
- [Heap and allocation profiling](#heap-and-allocation-profiling)
- [Build profiles and codegen](#build-profiles-and-codegen)
- [LTO, linkers, and debug information](#lto-linkers-and-debug-information)
- [Profile-guided optimization](#profile-guided-optimization)
- [Hot-path optimization](#hot-path-optimization)
- [I/O, iterators, and bounds checks](#io-iterators-and-bounds-checks)
- [Portability and safety boundaries](#portability-and-safety-boundaries)
- [Diagnostic checklist](#diagnostic-checklist)
- [Sources and currency](#sources-and-currency)

## Working contract and measurement workflow

1. **Define the target metric.** Decide whether you must improve wall time,
   CPU cycles, instructions, peak bytes, allocation rate, binary size, or
   compile time. Avoid an imprecise goal such as "faster".
   [Rust Performance Book – Benchmarking](https://nnethercote.github.io/perf-book/benchmarking.html)
2. **Capture a baseline.** Build with the same toolchain, the same features,
   the same target, and realistic input data. Store benchmark, profiler, and
   binary-size artifacts before changing code.
   [Rust Performance Book – Benchmarking](https://nnethercote.github.io/perf-book/benchmarking.html)
3. **Profile first.** Use sampling and flamegraphs to find hotspots; treat
   flamegraph width only as relative on-CPU share and confirm every candidate
   with a focused measurement.
   [flamegraph – Flamegraphs Are the Beginning, Not the End](https://github.com/flamegraph-rs/flamegraph#flamegraphs-are-the-beginning-not-the-end)
4. **Change one cause.** Separate algorithm, data-layout, allocator, compiler,
   and CPU-feature changes so it stays visible which change produced the
   effect.
5. **Repeat the baseline measurement.** Accept an optimization only when the
   effect size, confidence interval, and cost (complexity, portability,
   debuggability, compile time) fit the contract.
6. **Document the rationale.** Record workload, hardware, toolchain,
   measurement command, and observed metric directly at the optimized code.

Use realistic workloads and several size classes. Microbenchmarks are useful
for tight hotspots but must not replace a production-shaped measurement.
[Rust Performance Book – Benchmarking](https://nnethercote.github.io/perf-book/benchmarking.html)

Keep the machine quiet and warm for measurements, but not thermally
throttled. Control the CPU power mode, background processes, VM or CI load,
and memory activity. [Criterion – A Note of Caution](https://criterion-rs.github.io/book/user_guide/command_line_output.html#a-note-of-caution),
[flamegraph – Performance Theory 101](https://github.com/flamegraph-rs/flamegraph#performance-theory-101-basics-of-quantitative-engineering)

## Benchmark design with Criterion

Use a current Criterion release from the `criterion-rs` organization and its
book. [Criterion.rs repository](https://github.com/criterion-rs/criterion.rs)

Set up Criterion as its own benchmark target:

```toml
[dev-dependencies]
criterion = "..."

[[bench]]
name = "hot_path"
harness = false
```

```rust
use criterion::{criterion_group, criterion_main, Criterion};
use std::hint::black_box;

fn bench_hot_path(c: &mut Criterion) {
    c.bench_function("hot path", |b| {
        b.iter(|| hot_path(black_box(input())))
    });
}

criterion_group!(benches, bench_hot_path);
criterion_main!(benches);
```

Keep setup outside the measured closure when you only want to evaluate the hot
path. Use `std::hint::black_box` so inputs and results are not constant-folded or removed
as unused. [Criterion – Getting Started](https://criterion-rs.github.io/book/getting_started.html)

Account for the Criterion measurement model:

- Let the warm-up phase warm CPU and OS caches and, where present, JIT layers.
- Measure several samples with several iterations; Criterion estimates time
  per iteration from the whole sample.
- Use the bootstrap confidence intervals and the stored comparison data.
- Investigate many outliers and a low R² instead of reading only the mean.

[Criterion – Analysis Process](https://criterion-rs.github.io/book/analysis.html),
[Criterion – Command-Line Output](https://criterion-rs.github.io/book/user_guide/command_line_output.html)

Use these commands for focused runs and reproducible baselines:

```sh
cargo bench
cargo bench -- --verbose
cargo bench -- hot_path
cargo bench -- --profile-time 10
cargo bench -- --save-baseline before
cargo bench -- --baseline before
cargo test --benches
```

`--profile-time` suppresses the regular analysis and plot generation, which
makes it suitable for external profilers. [Criterion – Command-Line Options](https://criterion-rs.github.io/book/user_guide/command_line_options.html)

Use `BenchmarkGroup::throughput` only when you correctly know the bytes or
elements processed per iteration. Use `bench_with_input`/`BenchmarkId` for
input sizes, and implement `size_hint` or `ExactSizeIterator::len` for your
own iterators when the length is known.
[Criterion – Advanced Configuration](https://criterion-rs.github.io/book/user_guide/advanced_configuration.html),
[Criterion – Benchmarking With Inputs](https://criterion-rs.github.io/book/user_guide/benchmarking_with_inputs.html)

Note that external Criterion benchmarks in a separate target rely on `pub`
functions. Put compute-heavy logic into a library and keep a binary as a thin
adapter. [Criterion – Known Limitations](https://criterion-rs.github.io/book/user_guide/known_limitations.html)

## Profiling and flamegraphs

Build at least line-level debug information into release builds for readable
stacks:

```toml
[profile.release]
debug = "line-tables-only"
```

For `cargo-flamegraph`, `debug = true` can be useful; for benchmarks set
`[profile.bench] debug = true` when needed. [Rust Performance Book – Profiling](https://nnethercote.github.io/perf-book/profiling.html),
[flamegraph – Improving output](https://github.com/flamegraph-rs/flamegraph#improving-output-when-running-with---release)

Install and start flamegraphs like this:

```sh
cargo install flamegraph
cargo flamegraph --bin app -- --input workload.dat
cargo flamegraph --bench hot_path -- --bench
flamegraph --pid 1337
```

On Linux the tool uses `perf`, on macOS `xctrace`, and on Windows Blondie by
default. With a current lld or mold on Linux, `-Wl,--no-rosegment` may be
required for accurate stacks.
[flamegraph – Quick Start](https://github.com/flamegraph-rs/flamegraph#quick-start),
[flamegraph – Linux](https://github.com/flamegraph-rs/flamegraph#linux)

[samply](https://github.com/mstange/samply) is an actively maintained
cross-platform sampling alternative with an interactive profiler UI; the
flamegraph project itself recommends trying it. Choose one primary sampling
tool per investigation and keep its version in the measurement record.

Interpret a flamegraph element as the share of samples in which the function
was active or on the call stack. The x-axis is not a timeline; a narrower box
does not prove an absolute speedup. Confirm the effect with Criterion or
instruction counting. [flamegraph – Systems Performance](https://github.com/flamegraph-rs/flamegraph#systems-performance-work-guided-by-flamegraphs),
[flamegraph – Flamegraphs Are the Beginning, Not the End](https://github.com/flamegraph-rs/flamegraph#flamegraphs-are-the-beginning-not-the-end)

Extend sampling with Cachegrind/Callgrind for instruction, cache, and branch
data where needed; use `perf`, Instruments, VTune, uProf, or samply depending
on the platform. Do not expect on-CPU sampling to provide a complete I/O or
off-CPU latency analysis. [Rust Performance Book – Profiling](https://nnethercote.github.io/perf-book/profiling.html)

Use Criterion profiling hooks when you need an in-process profiler. Implement
`criterion::profiler::Profiler` and enable it through `with_profiler`; the
hooks run only with `--profile-time`.
[Criterion – Profiling](https://criterion-rs.github.io/book/user_guide/profiling.html)

## Heap and allocation profiling

Choose DHAT or `dhat-rs` when `malloc`/`free`, peak heap, `memcpy`, or
allocation rates appear hot in the profile. [Rust Performance Book – Heap Allocations](https://nnethercote.github.io/perf-book/heap-allocations.html#profiling)

For Rust heap tests, feature-gate the allocator as shown in
[DHAT for heap regressions](rust-memory-and-data-layout.md#dhat-for-heap-regressions)
and use release builds:

```sh
cargo run --release --features dhat-heap
```

Enable `dhat::Alloc` exclusively during profiling; the wrapper can slow the
program substantially and is experimental per the crate documentation.
[DHAT-rs – Configuration and setup](https://docs.rs/dhat/latest/dhat/#configuration-profiling-and-testing),
[DHAT-rs – crate warning](https://docs.rs/dhat/latest/dhat/)

Use `Profiler::builder().testing().build()` and `HeapStats::get()` to check
`total_*`, `max_*`, and `curr_*` bytes and blocks as regressions.
[DHAT-rs – Heap usage testing](https://docs.rs/dhat/latest/dhat/#heap-usage-testing)

For ad-hoc frequencies mark code points with `dhat::ad_hoc_event(weight)`.
Keep the profiler lifetime across the whole relevant `main` scope, because
allocations outside the lifetime can be ignored or treated as new allocations.
[DHAT-rs – Ad hoc profiling](https://docs.rs/dhat/latest/dhat/#setup-ad-hoc-profiling),
[DHAT-rs – Running](https://docs.rs/dhat/latest/dhat/#running)

When an allocation profile points at the allocator itself, an alternative
global allocator such as jemalloc (via `tikv-jemallocator`) or mimalloc is one
of the highest-leverage single changes for allocation-heavy workloads; treat
it as a system boundary and measure it per platform as described in
[Memory and data layout](rust-memory-and-data-layout.md).
[Rust Performance Book – Build Configuration](https://nnethercote.github.io/perf-book/build-configuration.html)

Apply the detailed container and layout rules in
[Memory and data layout](rust-memory-and-data-layout.md) before introducing `Box`,
`SmallVec`, `Cow`, `clone_from`, or an alternative allocator because of an
allocation profile.

## Build profiles and codegen

Use an explicit release profile for runtime measurements. Adjust
`codegen-units` only with a measurement: `1` often improves cross-unit
optimization but increases compile time. [rustc Codegen – codegen-units](https://doc.rust-lang.org/rustc/codegen-options/index.html#codegen-units)

Set `opt-level` deliberately:

- `3` optimizes for runtime;
- `s` optimizes for size with somewhat more inlining and vectorization;
- `z` optimizes for size more aggressively but is not guaranteed smaller than `s`.

[rustc Codegen – opt-level](https://doc.rust-lang.org/rustc/codegen-options/index.html#opt-level),
[min-sized-rust – Optimize For Size](https://github.com/johnthagen/min-sized-rust#optimize-for-size)

Use `target-cpu=native` or individual `target-feature` flags only when you
know the CPU contract of the deployment. Check available values with
`rustc --print target-cpus` and `rustc --print target-features`; a wrong
target can cause runtime faults or lost portability.
[rustc Codegen – target-cpu](https://doc.rust-lang.org/rustc/codegen-options/index.html#target-cpu),
[rustc Codegen – target-feature](https://doc.rust-lang.org/rustc/codegen-options/index.html#target-feature)

Disable LLVM vectorization (`no-vectorize-loops`, `no-vectorize-slp`) only for
diagnostics or A/B comparisons. Do not use these flags as a blanket
optimization setting. [rustc Codegen – vectorization flags](https://doc.rust-lang.org/rustc/codegen-options/index.html#no-vectorize-loops)

## LTO, linkers, and debug information

Compare `lto = "thin"` and `lto = "fat"` with the same workload. Thin LTO
reduces link time and often reaches similar runtime gains; fat LTO can deliver
additional cross-crate optimization but costs more time and is not always
better. [rustc Codegen – lto](https://doc.rust-lang.org/rustc/codegen-options/index.html#lto)

Use `embed-bitcode=no` when no LTO is needed; do not combine it with `-C lto`.
Use `linker-plugin-lto` only with a compatible native linker.
[rustc Codegen – embed-bitcode](https://doc.rust-lang.org/rustc/codegen-options/index.html#embed-bitcode),
[rustc Codegen – linker-plugin-lto](https://doc.rust-lang.org/rustc/codegen-options/index.html#linker-plugin-lto)

Rust uses lld as the default linker on `x86_64-unknown-linux-gnu` since
Rust 1.90; on other targets, adopt lld, mold, or wild for link-time reduction
only after a successful link and CI run for every supported target.
[Rust 1.90 lld announcement](https://blog.rust-lang.org/2025/09/01/rust-lld-on-1.90.0-stable/),
[Rust Performance Book – Linking](https://nnethercote.github.io/perf-book/build-configuration.html#linking)

Keep debug lines for profilers even when you strip symbols from the shipped
binary. `strip=debuginfo` or `strip=symbols` reduces size but can weaken
backtraces, debuggers, and profilers. [rustc Codegen – strip](https://doc.rust-lang.org/rustc/codegen-options/index.html#strip)

## Profile-guided optimization

Run PGO as a reproducible four-step process:

1. Instrument with `-Cprofile-generate=/absolute/path`.
2. Run the instrumented binary several times with typical workloads.
3. Run `llvm-profdata merge` on all `.profraw` files.
4. Rebuild with `-Cprofile-use=/absolute/path/merged.profdata` and identical
   compiler flags.

```sh
rustup component add llvm-tools
rm -rf /tmp/pgo-data
RUSTFLAGS="-Cprofile-generate=/tmp/pgo-data" \
  cargo build --release --target=x86_64-unknown-linux-gnu
./target/x86_64-unknown-linux-gnu/release/app typical-input
llvm-profdata merge -o /tmp/pgo-data/merged.profdata /tmp/pgo-data
RUSTFLAGS="-Cprofile-use=/tmp/pgo-data/merged.profdata" \
  cargo build --release --target=x86_64-unknown-linux-gnu
```

Pass `RUSTFLAGS` through Cargo to all crates, use `--target` so build scripts
do not generate profiles, and delete old profile data before training. Use
`-Cllvm-args=-pgo-warn-missing-function` to report missing profiles.
[rustc PGO – Complete Cargo Workflow](https://doc.rust-lang.org/nightly/rustc/profile-guided-optimization.html#a-complete-cargo-workflow),
[rustc PGO – Troubleshooting](https://doc.rust-lang.org/nightly/rustc/profile-guided-optimization.html#troubleshooting)

Use `cargo-pgo` when the manual profile sequence is too error-prone in your
build system; still verify training data, toolchain binding, and distribution.
Its BOLT post-link optimization support is explicitly experimental.
[rustc PGO – Community Maintained Tools](https://doc.rust-lang.org/nightly/rustc/profile-guided-optimization.html#community-maintained-tools),
[cargo-pgo](https://github.com/Kobzol/cargo-pgo)

## Hot-path optimization

Profile before `#[inline]`, `#[inline(always)]`, or `#[inline(never)]`.
Inlining can remove call overhead and enable further optimization, but it can
also increase code size, compile time, and instruction-cache pressure.
Inlining is not transitive; measure after every annotation. [Rust Performance Book – Inlining](https://nnethercote.github.io/perf-book/inlining.html)

Move rare error and special-case paths into a separate `#[cold]` function when
the profile shows they bloat the hot path. [Rust Performance Book – Outlining](https://nnethercote.github.io/perf-book/inlining.html#outlining)

Inspect generated code only for small, genuinely hot functions with Compiler
Explorer or `cargo-show-asm`; verify bounds checks, unrolling, inlining, and
SIMD in the assembly instead of assuming their presence.
[Rust Performance Book – Machine Code](https://nnethercote.github.io/perf-book/machine-code.html)

Use Rayon/Crossbeam and SIMD for data parallelism as separate levers; thread
parallelism and vectorization solve different bottlenecks.
[Rust Performance Book – Parallelism](https://nnethercote.github.io/perf-book/parallelism.html)

## I/O, iterators, and bounds checks

Lock stdout/stderr once manually for many outputs and buffer file and socket
I/O with `BufReader`/`BufWriter` to reduce syscalls. For byte-oriented
protocols use `read_until` when UTF-8 validation is unnecessary.
[Rust Performance Book – I/O](https://nnethercote.github.io/perf-book/io.html)

Avoid `collect` when you immediately iterate the result again. Prefer
returning `impl Iterator`, use `extend` for existing collections, and provide
`size_hint` when the output length is known. [Rust Performance Book – Iterators](https://nnethercote.github.io/perf-book/iterators.html)

In hot loops use `chunks_exact` when the block size fits, and check whether
`iter().copied()` produces better LLVM code. [Rust Performance Book – Iterators](https://nnethercote.github.io/perf-book/iterators.html#chunks)

Reduce bounds checks safely first through iteration, pre-formed slices, or
explicit range assertions. Use `get_unchecked` only with a local, documented
safety proof and only after measured relevance.
[Rust Performance Book – Bounds Checks](https://nnethercote.github.io/perf-book/bounds-checks.html),
[Rustonomicon – Working with Unsafe](https://doc.rust-lang.org/stable/nomicon/working-with-unsafe.html)

## Portability and safety boundaries

- **CPU contract:** do not ship `target-cpu=native` code when older or
  heterogeneous CPUs must be supported. Use feature detection or multiple
  implementations.
- **Layout:** rely only on documented `repr(C)`/alignment guarantees;
  `repr(Rust)` field order and concrete DST sizes are not stable optimization
  contracts. [Rust Reference – Type layout](https://doc.rust-lang.org/stable/reference/type-layout.html)
- **Unsafe:** treat `get_unchecked`, `repr(packed)`, transmute, and custom
  containers as proof obligations, not performance labels. Document
  provenance, bounds, alignment, aliasing, lifetimes, drop, and unwind
  behavior. [Rustonomicon](https://doc.rust-lang.org/stable/nomicon/),
  [Rust Engineering – Unsafe and FFI](rust-unsafe-and-ffi.md)
- **Panic semantics:** `panic = "abort"` saves unwind code but changes
  behavior and can break library and FFI contracts. [rustc Codegen – panic](https://doc.rust-lang.org/rustc/codegen-options/index.html#panic)
- **Profiling overhead:** the DHAT allocator, instrumentation PGO, and debug
  info influence the measurement. Use them only for the diagnostic run and
  measure the final build separately.
- **Experimental:** `dhat` and several nightly flags can crash, hang, be
  subject to ABI or toolchain changes, or deliver incomplete results. Mark
  these dependencies in CI and re-check them on toolchain upgrades.

## Diagnostic checklist

### Runtime

- Am I actually measuring the release build with the production target?
- Are CPU power, temperature, VM/CI, and background load controlled?
- Is the hotspot on-CPU, off-CPU/I/O, allocation, cache/branch, or dispatch?
- Have I confirmed a flamegraph candidate with Criterion or instruction
  counting?

### Memory

- Which call site produces how many bytes and blocks, with what lifetime and
  peak usage?
- Is a `Vec` under-reserved, oversized, or better represented through
  `SmallVec`/`Cow`/reuse?
- Are `clone`, `to_owned`, `format!`, `lines()`, or reallocations in the hot
  path?
- Which hot types contain padding, large enum variants, or unnecessary
  pointers?

### Codegen/distribution

- Are `codegen-units`, LTO, allocator, linker, and `target-cpu` measured
  individually?
- Are PGO workloads representative, profiles current, and flags identical?
- Is debug information kept for profiling and stripped only in the artifact
  step?
- Have `panic=abort`, `no_std`, `no_main`, `repr(packed)`, or nightly flags
  changed the safety or portability contract?

## Sources and currency

Use the [Rust Reference](https://doc.rust-lang.org/stable/reference/type-layout.html)
for guarantees and the current [rustc codegen reference](https://doc.rust-lang.org/rustc/codegen-options/index.html).
Treat the [Rustonomicon](https://doc.rust-lang.org/stable/nomicon/) as an
advanced, explicitly incomplete companion; the Reference wins on conflicts.

Verify version, platform, and toolchain before adopting any number or flag.
The [Criterion book](https://criterion-rs.github.io/book/),
[cargo-flamegraph](https://github.com/flamegraph-rs/flamegraph),
[samply](https://github.com/mstange/samply),
[`dhat`](https://docs.rs/dhat/latest/dhat/), and
[min-sized-rust](https://github.com/johnthagen/min-sized-rust) keep evolving;
current CLI and nightly details can deviate from the examples.
