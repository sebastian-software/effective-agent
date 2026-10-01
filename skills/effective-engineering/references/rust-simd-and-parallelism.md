# SIMD and Parallelism

Use this reference when Rust code needs measured CPU, memory, SIMD, atomic,
thread-parallel, or compiler-level optimization. It is a decision and safety
reference, not a catalog of clever micro-optimizations.

## Routing

Use the sections in this order:

1. Establish a representative benchmark and correctness oracle.
2. Inspect layout, aliasing, dispatch, and generated IR/assembly.
3. Reshape scalar code for inlining and auto-vectorization.
4. Add portable SIMD or architecture-specific dispatch only when measurements
   justify it.
5. Add Rayon or another parallel layer only after the single-thread kernel and
   task granularity are understood.
6. For shared mutable state, route through the atomics and memory-ordering
   sections before choosing a lock or an async boundary.

Route other concerns as follows:

- Route public API design, crate boundaries, and workspace layering to
  [Architecture and boundaries](rust-architecture-and-boundaries.md). Keep
  performance kernels behind a stable, safe boundary.
- Route general profiling, allocation, and binary-size investigations to
  [Performance and memory](rust-performance-and-memory.md); use this file for
  CPU/SIMD and parallel interactions.
- Route async runtime choice, cancellation, and I/O scheduling to
  [Errors and concurrency](rust-errors-and-concurrency.md). Use this file to
  decide whether CPU work must leave an async executor.
- Route unsafe-code audits to [Unsafe and FFI](rust-unsafe-and-ffi.md). The rules here state the
  minimum invariants; they do not replace a complete unsafe review.

## Non-negotiable safety rules

- Prove the CPU feature before calling an architecture-specific intrinsic.
- Keep target architecture and feature checks in compile-time configuration.
- Encapsulate intrinsic calls in a small unsafe function with a written safety
  contract and a safe scalar fallback.
- Treat alignment, slice length, pointer provenance, aliasing, and overlap as
  preconditions. Do not infer them from a benchmark input.
- Treat atomic ordering as a happens-before contract, not a speed knob.
- Do not block an async executor thread on a mutex, OS wait, or CPU-heavy loop.
- Benchmark release artifacts with the same target CPU, feature flags, input
  distribution, and deployment constraints as production.

## 1. Build an evidence loop before optimizing

### 1.1 Establish the scalar baseline

Write the simplest correct scalar implementation first. Test the result against
edge cases, empty inputs, tails, aliasing/overlap rules, integer overflow
behavior, floating-point tolerances, and unsupported CPU paths.

Record:

- input sizes and distribution, not only an average;
- wall-clock latency and throughput;
- allocations and peak memory where relevant;
- target triple, compiler version, optimization level, CPU features, and LTO;
- correctness checksum or a reference implementation.

Source: [Matklad, Conclusion](https://matklad.github.io/2023/04/09/can-you-trust-a-compiler-to-optimize-your-code.html#Conclusion);
[SIMD Performance Guide, profiling](https://rust-lang.github.io/packed_simd/perf-guide/prof/profiling.html).

### 1.2 Separate codegen evidence from hardware evidence

Use Compiler Explorer or local IR/assembly tools to answer “what code was
generated?” Use Criterion, perf, cache counters, and real workloads to answer
“what did this CPU actually spend time doing?” Neither answer subsumes the
other.

Source: [Compiler Explorer Rust](https://rust.godbolt.org/);
[SIMD Performance Guide, Linux profiling](https://rust-lang.github.io/packed_simd/perf-guide/prof/linux.html).

### 1.3 Optimize the bottleneck, then retain a regression test

Profile an average representative workload, change one structural property,
inspect codegen, benchmark again, and preserve the result as a benchmark or
test. Stop when the measured bottleneck moves or the improvement is below the
project’s noise floor.

## 2. Compiler mental model

### 2.1 Treat a function as the primary optimization boundary

Compilers reason best about typed local values and control flow inside one
function. They reason less reliably about bytes behind shared pointers and
about facts split across function or crate boundaries.

Prefer a small, visible kernel:

    fn dot(xs: &[f32], ys: &[f32]) -> f32 {
        xs.iter().zip(ys).map(|(x, y)| x * y).sum()
    }

Then inspect whether the abstraction disappears; do not assume that a shorter
source expression is faster.

Source: [Matklad, Seeing Like a Compiler](https://matklad.github.io/2023/04/09/can-you-trust-a-compiler-to-optimize-your-code.html#Seeing-Like-a-Compiler).

### 2.2 Prefer statically resolvable calls in hot kernels

Use generics and concrete closure types when a call is part of a hot loop.
Treat function pointers and dynamic dispatch as deliberate boundaries because
they may prevent inlining. Do not remove dynamic dispatch merely for style:
measure the boundary and keep it where runtime extensibility is required.

Source: [Matklad, Impossible and Possible](https://matklad.github.io/2023/04/09/can-you-trust-a-compiler-to-optimize-your-code.html#Impossible-and-Possible).

### 2.3 Understand inlining as context propagation

Inlining exposes caller and callee locals to the same optimizer. It can make
index relationships, constant arguments, and dead branches visible. The
benefit is generally larger than eliminating the call instruction itself.

Do not blanket-apply inline(always). It can increase code size, instruction
cache pressure, compile time, and monomorphization cost. Confirm the effect in
IR/assembly and benchmarks.

Source: [Matklad, Bringing Code Closer to the Compiler’s Nose](https://matklad.github.io/2023/04/09/can-you-trust-a-compiler-to-optimize-your-code.html#Bringing-Code-Closer-to-Compiler's-Nose).

### 2.4 Recognize scalar replacement of aggregates

SROA can temporarily split an aggregate such as a vector header into scalar
locals, enabling better dataflow reasoning. It does not grant permission to
change a public memory layout or an FFI representation.

Keep aggregate mutation localized and avoid needless address-taking in a hot
path. Inspect LLVM IR if a value unexpectedly spills to memory.

Source: [Matklad, SROA discussion](https://matklad.github.io/2023/04/09/can-you-trust-a-compiler-to-optimize-your-code.html#Bringing-Code-Closer-to-Compiler's-Nose).

### 2.5 Treat aliases and indirection as optimization costs

An embedded field is easier to reason about than a separately allocated
Box/handle. Unique ownership may let LLVM see through a Box, but that is not a
portable guarantee. Reduce pointer chasing in data-parallel loops and reserve
indirection for ownership, lifetime, or API boundaries that need it.

Source: [Matklad, Indirection and layout](https://matklad.github.io/2023/04/09/can-you-trust-a-compiler-to-optimize-your-code.html#Impossible-and-Possible).

### 2.6 Design layout and cache behavior explicitly

The compiler generally cannot redesign shared data layout on behalf of all
functions. Choose compact fields, reduce padding only when it does not violate
alignment/ABI contracts, group fields with common access patterns, and compare
array-of-structs with struct-of-arrays for the measured workload.

Source: [Matklad, baseline performance rules](https://matklad.github.io/2023/04/09/can-you-trust-a-compiler-to-optimize-your-code.html#Impossible-and-Possible).

## 3. Auto-vectorization and branch shape

### 3.1 Make vectorizable work independent across lanes

Express one operation per element with a predictable access pattern. Avoid
inner-loop branches whose outcome determines whether later elements execute.
Move a decision outside a fixed-size chunk when semantics allow.

Source: [Matklad, SIMD](https://matklad.github.io/2023/04/09/can-you-trust-a-compiler-to-optimize-your-code.html#SIMD).

### 3.2 Process explicit chunks and handle the tail separately

Use chunks that match the intended vector width or a multiple of it, and retain
a scalar tail path:

    for (left, right) in xs.chunks_exact(16).zip(ys.chunks_exact(16)) {
        // same operation for every lane in the chunk
    }
    // process chunks_exact remainder scalar

Do not hard-code 16 as a universal best width. Benchmark widths on the target
CPU and leave room for the compiler’s chosen vector width.

Source: [Matklad, common-prefix SIMD example](https://matklad.github.io/2023/04/09/can-you-trust-a-compiler-to-optimize-your-code.html#SIMD).

### 3.3 Replace short-circuit reduction inside a chunk

When checking whether all lanes match, accumulate a chunk predicate without
short-circuiting:

    let mut equal = true;
    for (x, y) in left.iter().zip(right) {
        equal = equal & (x == y);
    }
    if !equal { break; }

The bitwise and is intentional: logical and would introduce a dependency on
the first false lane. Preserve the original semantics by locating the first
mismatch in a scalar tail or a second pass when the API requires its position.

Source: [Matklad, branchless chunk comparison](https://matklad.github.io/2023/04/09/can-you-trust-a-compiler-to-optimize-your-code.html#SIMD).

### 3.4 Verify vectorization, do not infer it from iterators

Iterators and generics can be zero-cost after inlining, but they can also leave
an unexpected call, bounds check, or alias barrier. Check LLVM IR, assembly,
and optimization remarks for vector loads, lane operations, and the intended
reduction.

Source: [Matklad, Conclusion](https://matklad.github.io/2023/04/09/can-you-trust-a-compiler-to-optimize-your-code.html#Conclusion);
[Compiler Explorer](https://rust.godbolt.org/).

## 4. Portable SIMD

### 4.1 Route by stability requirement

Use std::simd only when the project accepts a nightly, experimental API and can
track its feature gate. For a stable crate, choose a scalar implementation,
stable core::arch wrappers, or an established portable-SIMD crate such as
`wide` unless the project has a separately approved nightly policy.

Source: [std::simd module status](https://doc.rust-lang.org/std/simd/index.html);
[portable-simd repository README](https://github.com/rust-lang/portable-simd);
[portable_simd tracking issue](https://github.com/rust-lang/rust/issues/86656).

### 4.2 Keep portable SIMD’s semantic contract

Model Simd<T, N> as an elementwise, array-like value with vector operations.
Use Mask for per-lane predicates and Select for lane-wise choice. Do not assume
that one source operation maps to one vendor instruction.

Portable SIMD may compile to scalar code where the target lacks suitable SIMD.
That is a correctness/portability feature; test it as an expected fallback.

Source: [std::simd, “What is portable?”](https://doc.rust-lang.org/std/simd/index.html#what-is-portable).

### 4.3 Record floating-point target exceptions

Some older architectures flush subnormal f32 values to zero. If a numerical
contract includes subnormals, document the allowed behavior and test each
supported target. Do not silently compare bit patterns across all CPUs.

Source: [std::simd, consistency between targets](https://doc.rust-lang.org/std/simd/index.html#portable-simd-is-consistent-between-targets).

### 4.4 Keep lane and mask assumptions local

The portable-simd repository documents up to 64 lanes, aliases up to 512 bits,
and primitive integer/float/pointer element types. Treat those facts as the
current project state, not as a stable ABI or a promise for future releases.
Mask layout is intentionally architecture-dependent.

Source: [portable-simd, supported vectors](https://github.com/rust-lang/portable-simd#supported-vectors).

## 5. core::arch and CPU feature dispatch

### 5.1 Isolate architecture-specific code

Use target_arch configuration to select the x86, x86_64, aarch64, wasm, RISC-V,
or other module. Keep architecture modules behind a stable portable facade.
Do not import x86 intrinsics into a crate path that must compile for ARM.

The stable intrinsic surface keeps growing: AVX-512 intrinsics and their
target features stabilized in Rust 1.89, and since Rust 1.87 many intrinsics
are callable without an unsafe block inside a function that already enables
the matching target feature. Verify the exact stabilization state of an
intrinsic against the current core::arch documentation instead of assuming
either nightly-only or stable status.

Source: [core::arch overview](https://doc.rust-lang.org/stable/core/arch/index.html#overview);
[other architectures](https://doc.rust-lang.org/stable/core/arch/index.html#other-architectures);
[AVX-512 stabilization tracking issue](https://github.com/rust-lang/rust/issues/111137).

### 5.2 Choose static features only with a deployment contract

Use target_feature configuration or compiler flags when every deployed CPU
meets the feature requirement. Document the minimum CPU and reject incompatible
deployment rather than allowing an illegal instruction.

    RUSTFLAGS='-C target-feature=+avx2' cargo build

Source: [core::arch static detection](https://doc.rust-lang.org/stable/core/arch/index.html#static-cpu-feature-detection).

### 5.3 Use runtime dispatch for portable binaries

Make a safe entry point perform platform-gated feature detection, then call a
small target_feature-enabled unsafe kernel:

    fn process(input: &[u8], output: &mut [u8]) {
        #[cfg(any(target_arch = "x86", target_arch = "x86_64"))]
        if is_x86_feature_detected!("avx2") {
            return unsafe { process_avx2(input, output) };
        }
        process_scalar(input, output);
    }

The feature-detection macro itself is platform-specific, so guard its use with
cfg. Keep the fallback functionally equivalent and test both paths.

Source: [core::arch dynamic detection](https://doc.rust-lang.org/stable/core/arch/index.html#dynamic-cpu-feature-detection);
[core::arch examples](https://doc.rust-lang.org/stable/core/arch/index.html#examples).

### 5.4 Make the unsafe contract explicit

For each target kernel document:

- the CPU feature proven by the caller;
- required alignment and minimum length;
- pointer provenance and non-overlap assumptions;
- integer overflow or floating-point behavior;
- why the fallback and optimized path have equivalent observable semantics.

Do not let a target_feature attribute become an unreviewed unsafe escape hatch.

Source: [core::arch overview](https://doc.rust-lang.org/stable/core/arch/index.html#overview).

## 6. Target flags, alignment, and bounds

### 6.1 Treat target features as independent switches

Enabling avx2 does not automatically enable fma in the SIMD guide’s model.
List required features explicitly and verify target-feature output with rustc.
Feature dependencies such as ARM v7 plus NEON require their prerequisite
features.

Source: [SIMD guide, RUSTFLAGS](https://rust-lang.github.io/packed_simd/perf-guide/target-feature/rustflags.html).

### 6.2 Restrict target-cpu=native to local artifacts

Use native CPU optimization for local experiments or a controlled fleet. Do
not use it for generic release artifacts, cross-compilation, or packages whose
users have unknown CPUs. Prefer a defined baseline plus runtime dispatch.

Source: [SIMD guide, target-cpu](https://rust-lang.github.io/packed_simd/perf-guide/target-feature/rustflags.html#target-cpu).

### 6.3 Preserve safe load/store checks unless measured

Aligned SIMD slice operations check length and SIMD alignment. SIMD alignment
can exceed the element type’s alignment. Keep the safe path until profiling
shows checks are material and the unsafe preconditions can be proven.

Source: [SIMD guide, bounds checking](https://rust-lang.github.io/packed_simd/perf-guide/bound_checks.html).

### 6.4 Distinguish unaligned from unchecked access

Use an unaligned API when the data is valid but not suitably aligned. Use an
unchecked API only with a narrow, reviewed proof of length and alignment, and
account for debug assertions and build profile behavior.

Source: [SIMD guide, bounds checking](https://rust-lang.github.io/packed_simd/perf-guide/bound_checks.html).

### 6.5 Delay horizontal reductions

Keep vertical lane-wise operations in the inner loop and reduce once at the
end. Horizontal operations combine lane information and are commonly slower.
Measure reduction order for floating-point reproducibility and error tolerance.

Source: [SIMD guide, vertical and horizontal operations](https://rust-lang.github.io/packed_simd/perf-guide/vert-hor-ops.html).

### 6.6 Profile at two levels

On Linux, build an optimized benchmark with debug information, use perf record
with DWARF or LBR call graphs, inspect perf report, and request cache events
when relevant. Use llvm-mca or another microarchitecture analyzer to interpret
latency, throughput, register pressure, and µ-op behavior.

Source: [SIMD guide, Linux profiling](https://rust-lang.github.io/packed_simd/perf-guide/prof/linux.html);
[machine-code analysis](https://rust-lang.github.io/packed_simd/perf-guide/prof/mca.html).

## 7. Compiler Explorer and IR/assembly workflow

### 7.1 Keep the function visible

Export a small diagnostic kernel with a stable name, or use inline(never) for
inspection. Current Rust/Compiler Explorer examples note that small optimized
functions may otherwise disappear into their callers.

Source: [Compiler Explorer Rust](https://rust.godbolt.org/);
[Rust noscript examples](https://rust.godbolt.org/noscript/rust).

### 7.2 Inspect the whole lowering path

Read Rust HIR and macro expansion for desugaring, Rust MIR for control flow and
borrow/bounds structure, LLVM IR for vectorizer/inlining visibility, and
assembly for actual loads, stores, branches, and instructions. Use optimization
remarks to distinguish an applied transformation from a missed opportunity.

Source: [Compiler Explorer tool list](https://rust.godbolt.org/);
[Rustc intermediate representations](https://rustc-dev-guide.rust-lang.org/overview.html#intermediate-representations).

### 7.3 Make comparisons reproducible

Save compiler version, target triple, optimization level, target CPU/features,
codegen options, source, and share URL. Re-run a promising result locally,
because Compiler Explorer’s runners and installed libraries can change.

### 7.4 Protect confidential source

Do not use optional third-party AI explanation features with confidential
source or output. Treat public share URLs as public artifacts.

Source: [Compiler Explorer UI](https://rust.godbolt.org/), consent and sharing
controls.

## 8. Atomics and memory ordering

### 8.1 Start with ownership and borrowing

Use shared references for read-only access and exclusive mutable references for
mutation. Use Arc for shared ownership, not as a mutation or synchronization
primitive. Establish Send and Sync constraints before introducing atomics.

Source: [Rust shared ownership](https://doc.rust-lang.org/std/sync/struct.Arc.html) and [Send/Sync contracts](https://doc.rust-lang.org/std/marker/trait.Sync.html).

### 8.2 Prefer scoped threads for bounded borrows

Use std::thread::scope when worker threads cannot outlive a lexical region.
This permits borrowing local slices without forcing static ownership or Arc
allocation, and the scope joins outstanding threads before returning.

Source: [`std::thread::scope`](https://doc.rust-lang.org/std/thread/fn.scope.html).

### 8.3 Use Relaxed only for the contract it satisfies

Relaxed operations provide atomic access and a per-variable modification order,
but they do not publish arbitrary writes to other variables. Stop flags and
independent counters are common uses; composite snapshots need stronger
ordering or a lock.

Source: [Rust atomic memory model](https://doc.rust-lang.org/std/sync/atomic/index.html) and [`Ordering`](https://doc.rust-lang.org/std/sync/atomic/enum.Ordering.html).

### 8.4 Use Release/Acquire for publication

Write data, then publish a flag or pointer with Release. Read the flag or
pointer with Acquire before consuming the data. Document the synchronizes-with
edge and test the protocol on weakly ordered targets.

    writer: data = value; ready.store(true, Release)
    reader: if ready.load(Acquire) { use(data) }

Source: [`Ordering::Release` and `Ordering::Acquire`](https://doc.rust-lang.org/std/sync/atomic/enum.Ordering.html).

### 8.5 Treat CAS failure and reclamation as first-class paths

For lazy pointer initialization, allocate privately, publish with
compare_exchange, and reclaim the losing allocation on CAS failure. Prove that
an acquired non-null pointer refers to initialized, live storage before
constructing a reference.

Source: [`AtomicPtr::compare_exchange`](https://doc.rust-lang.org/std/sync/atomic/struct.Atomic.html#method.compare_exchange-1) and [Rust atomic memory model](https://doc.rust-lang.org/std/sync/atomic/index.html).

### 8.6 Use fences only with a written synchronization proof

A conditional Acquire fence after a Relaxed load can avoid acquire cost on a
frequent null path, but fence correctness depends on the matching release and
the exact control flow. Do not replace Acquire/Release with fences by intuition.

Source: [`std::sync::atomic::fence`](https://doc.rust-lang.org/std/sync/atomic/fn.fence.html).

### 8.7 Test x86 and ARM assumptions separately

A passing x86-only test cannot establish portable ordering. Check the
language-level synchronization contract and generated instructions separately
on the supported architectures; hardware behavior cannot substitute for the
required ordering in the source program.

Source: [Rust atomic portability](https://doc.rust-lang.org/std/sync/atomic/index.html#portability).

## 9. Locks, blocking, and async boundaries

### 9.1 Prefer established primitives for production

Use std locks, well-reviewed channels, or a runtime’s synchronization primitives
unless implementing a primitive is itself the requirement. A custom primitive
needs its own ownership, synchronization, liveness, reclamation, and unsafe
proof; familiarity with a teaching implementation is insufficient.

Source: [Rust synchronization primitives](https://doc.rust-lang.org/std/sync/index.html).

### 9.2 Keep blocking work off async executor threads

Do not call blocking mutex waits, futexes, thread joins, synchronous file I/O,
or long CPU/SIMD loops directly from an async executor worker. Use the runtime’s
blocking pool, a dedicated thread pool, or Rayon and return the result through
an async-aware boundary.

Use a synchronous lock inside an async task only when the critical section is
provably short, non-blocking, and compatible with the runtime. Otherwise use an
async-aware lock and preserve cancellation/ownership semantics.

Source: [Tokio blocking-task behavior](https://docs.rs/tokio/latest/tokio/task/fn.spawn_blocking.html)
and [Tokio mutex guidance](https://docs.rs/tokio/latest/tokio/sync/struct.Mutex.html).

### 9.3 Account for contention and cache lines

Benchmark lock hold time, queueing, cache-line bouncing, false sharing, and
reader/writer skew. A lock-free algorithm can still be slower under contention,
and a store that appears slow in a profile may be the point where a pipeline
stall becomes visible.

Source: [Rust atomic portability](https://doc.rust-lang.org/std/sync/atomic/index.html#portability) and [SIMD machine-code analysis](https://rust-lang.github.io/packed_simd/perf-guide/prof/mca.html).

## 10. Rayon and task granularity

### 10.1 Start with parallel iterators

Use par_iter, par_iter_mut, or into_par_iter for ordinary data-parallel work.
Import the Rayon prelude in the module that uses those traits.

Source: [Rayon crate overview](https://docs.rs/rayon/latest/rayon/);
[Rayon iterator module](https://docs.rs/rayon/latest/rayon/iter/index.html).

### 10.2 Use join and scopes for explicit fork/join work

Use join for two independent branches, scope for multiple borrowed tasks, and
ThreadPoolBuilder for an explicit pool or global pool configuration. Ensure
each task is large enough to amortize scheduling and synchronization.

Source: [Rayon, custom tasks](https://docs.rs/rayon/latest/rayon/#how-to-use-rayon).

### 10.3 Tune splitting instead of forcing one task per element

Use IndexedParallelIterator for arbitrary index splits. Use with_min_len,
with_max_len, uniform_blocks, or domain-specific split functions when default
grain size causes overhead, imbalance, or cache loss. Measure on skewed inputs,
not only balanced inputs.

Source: [Rayon iterator adapters](https://docs.rs/rayon/latest/rayon/iter/index.html).

### 10.4 Keep SIMD inside the Rayon task

Structure the outer layer as cache-sized or workload-sized Rayon chunks, and
the inner layer as a scalar or SIMD kernel. Avoid tiny Rayon tasks around a
single vector operation; avoid nested pools that oversubscribe CPUs.

Source: [Rayon parallel iterators](https://docs.rs/rayon/latest/rayon/iter/index.html);
[Matklad SIMD chunking](https://matklad.github.io/2023/04/09/can-you-trust-a-compiler-to-optimize-your-code.html#SIMD).

### 10.5 Respect non-threaded targets and dyn limitations

Rayon has limited support on targets without std threading implementations.
ParallelIterator is not dyn-compatible by design, so represent runtime
polymorphism outside the parallel iterator pipeline.

Source: [Rayon targets without threading](https://docs.rs/rayon/latest/rayon/#targets-without-threading);
[dyn compatibility](https://docs.rs/rayon/latest/rayon/iter/trait.ParallelIterator.html#dyn-compatibility).

## 11. Rustc IR, monomorphization, and queries

### 11.1 Locate the problem at an IR stage

Use HIR for desugaring and types, THIR for fully typed patterns, MIR for
borrow-checking/control-flow/dataflow and generic optimization, LLVM IR for
monomorphized optimization, and assembly for target instructions.

Source: [Rustc Guide, intermediate representations](https://rustc-dev-guide.rust-lang.org/overview.html#intermediate-representations).

### 11.2 Expect MIR optimizations before LLVM

Rust performs many optimizations on generic MIR because some patterns are easier
to express there than in LLVM. Inspect optimized MIR when a source construct
behaves unexpectedly before blaming LLVM vectorization.

Source: [Rustc Guide, MIR lowering](https://rustc-dev-guide.rust-lang.org/overview.html#mir-lowering).

### 11.3 Balance monomorphization against code size

Generics are copied for concrete type parameters during code generation. This
enables static dispatch and inlining, but can increase code size and compile
time. Use dynamic dispatch where the boundary is truly dynamic and measure
LTO/codegen-unit trade-offs.

Source: [Rustc Guide, code generation](https://rustc-dev-guide.rust-lang.org/overview.html#code-generation);
[Matklad, static calls](https://matklad.github.io/2023/04/09/can-you-trust-a-compiler-to-optimize-your-code.html#Impossible-and-Possible).

### 11.4 Model compiler caches as queries, not a linear pass list

Rustc’s query system tracks dependencies, caches many results, and redoes only
affected work for incremental compilation. Not every phase is query-fied or
disk-cached, and some checks still visit unreachable items for diagnostics.

Source: [Rustc Guide, queries](https://rustc-dev-guide.rust-lang.org/overview.html#queries).

### 11.5 Use interning/arenas with explicit lifetime ownership

Intern immutable values in an arena when deduplication and cheap identity
comparisons matter. Tie references to the arena lifetime and provide a clear
rebuild/drop boundary; do not leak an arena merely to avoid an allocation.

Source: [Rustc Guide, interning](https://rustc-dev-guide.rust-lang.org/overview.html#intermediate-representations).

### 11.6 Keep compile-time and runtime goals separate

When changing generic structure, record runtime speed, binary size, compile
time, incremental rebuild time, and compiler memory. Rustc documentation treats
all of these as competing constraints.

Source: [Rustc Guide, compiler goals](https://rustc-dev-guide.rust-lang.org/overview.html#how-it-does-it).

### 11.7 Do not assume rustc itself is fully parallel

At the documented point, code generation is parallel by default while much of
the rest of rustc is not. Parallel compiler work must handle lock contention,
query invariants, and complexity; bootstrap.toml experiments are not ordinary
stable project settings.

Source: [Rustc Guide, parallelism](https://rustc-dev-guide.rust-lang.org/overview.html#parallelism).

## 12. Review checklists

### 12.1 SIMD/CPU checklist

- Is there a representative scalar baseline?
- Is the hot loop visible to the compiler?
- Are calls statically resolvable where inlining matters?
- Are layout and indirections measured?
- Are chunks independent and branch shape vectorizable?
- Is the tail path correct?
- Is std::simd’s nightly status accepted?
- Does core::arch dispatch prove architecture and CPU feature?
- Are alignment, length, overlap, and provenance preconditions documented?
- Are target flags reproducible and deployment-safe?
- Did assembly/IR and hardware profiling both confirm the result?

### 12.2 Atomics/locks checklist

- Is ownership/borrowing documented before atomics?
- Does each Atomic ordering have a specific happens-before reason?
- Is Relaxed being used only for independent state or per-variable facts?
- Are Release/Acquire edges explicit for publication?
- Are CAS failure and reclamation paths correct?
- Are weak-ordering ARM tests included?
- Is a lock-free design actually better under measured contention?
- Is blocking kept off async executor workers?

### 12.3 Rayon checklist

- Is the unit of work large enough to amortize scheduling?
- Are splits balanced for skewed inputs?
- Are min/max grain controls measured?
- Is the inner kernel scalar or SIMD and separately benchmarked?
- Is there only the intended number of thread pools?
- Does the target provide std threading?
- Is runtime polymorphism outside the non-dyn-compatible iterator pipeline?

## Source map

- [std::simd](https://doc.rust-lang.org/std/simd/index.html)
- [portable-simd README](https://github.com/rust-lang/portable-simd)
- [core::arch](https://doc.rust-lang.org/stable/core/arch/index.html)
- [Matklad compiler optimization article](https://matklad.github.io/2023/04/09/can-you-trust-a-compiler-to-optimize-your-code.html)
- [Rust SIMD Performance Guide](https://rust-lang.github.io/packed_simd/perf-guide/)
  — published by the archived `packed_simd` project; its profiling, target
  flag, and bounds-check guidance remains sound, but check crate and flag
  details against the current toolchain
- [Rust atomic memory model](https://doc.rust-lang.org/std/sync/atomic/index.html)
- [Rayon API](https://docs.rs/rayon/latest/rayon/)
- [Rust Compiler Development Guide](https://rustc-dev-guide.rust-lang.org/overview.html)
- [Compiler Explorer Rust](https://rust.godbolt.org/)
