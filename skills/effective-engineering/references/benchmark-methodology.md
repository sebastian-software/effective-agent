# Benchmark Methodology

Use a benchmark to answer one named performance question with repeatable
evidence. Do not turn a fast local run into a universal product claim, and do
not import a preferred benchmark framework when the repository already has a
harness or no demonstrated need for one.

## Classify the Claim

Name the decision before designing the measurement:

- **Characterization:** establish how one implementation behaves across a
  representative input range. This is evidence for investigation, not a gate.
- **Regression guard:** detect a material change in a concrete path against an
  agreed baseline or target. Prefer a stable relative or historical signal on
  heterogeneous CI runners.
- **Comparison:** compare implementations, versions, or configurations that
  perform the same relevant work under equivalent conditions.
- **Publication:** support a user-visible performance statement with retained,
  independently inspectable evidence and explicit limits.

Keep these lanes separate. A quick diagnostic run is not publication evidence;
a microbenchmark cannot establish service capacity; and a comparison cannot
answer a product question when the candidates perform different semantics.

## Discover the Repository Contract

Read scoped instructions, manifests, task runners, CI, benchmark directories,
nearby reports, and recent accepted evidence. Identify:

- the established command, harness, build profile, and dependency versions;
- the question each existing lane answers and any correctness gate it requires;
- checked-in or generated corpora, fixture provenance, and input-size ranges;
- warmup, sampling, repetition, ordering, and result-retention conventions;
- machine, runtime, compiler, feature, CPU, and optimization metadata already
  captured; and
- whether the benchmark is diagnostic, a regression gate, or publication
  evidence.

Do not silently install Criterion, Tinybench, Benchmark.js, a profiler, or any
other runner. If the repository has no harness, add one only when the requested
decision needs durable benchmark evidence and the chosen mechanism fits the
existing ecosystem and maintenance model.

Route execution-only requests for an established command to
`effective-delivery`. Return here when the harness, experiment, comparison,
interpretation, or claim itself needs design or repair.

## Preserve Semantic Parity

Correctness is a prerequisite to timing. Define the observable semantics each
candidate must preserve and run the relevant correctness or differential gate
before drawing a performance conclusion.

For comparisons, hold constant every dimension that affects the claim:

- input corpus and input order;
- enabled features, validation, escaping, security, and error handling;
- setup state, caches, output allocation or reuse, and concurrency;
- build mode, compiler/runtime version, architecture, and optimization flags;
- measured boundary and included I/O; and
- result validation.

When equivalent semantics are impossible, separate the configurations and
describe the extra work. Never merge secure and trusted modes, cold and warm
runs, isolated hot paths and end-to-end workflows, or native and portable
builds into one headline number.

## Design the Measurement

1. Choose representative, deterministic inputs. Cover the size or complexity
   range that could change the conclusion instead of optimizing for one tiny
   fixture. Record generated-input seeds and parameters.
2. Define the measured boundary. Keep fixture generation, environment probing,
   result serialization, and unrelated setup outside the timed region unless
   the claim explicitly concerns the end-to-end workflow.
3. Make the result observable so the compiler, runtime, or cache cannot remove
   the work. Validate output outside the timed region when that preserves the
   claim.
4. Separate warmup from measurement when the runtime, allocator, caches, JIT,
   or device needs it. If cold-start behavior is the question, reset state in a
   controlled way and label that lane as cold.
5. Use enough samples and elapsed time to distinguish a material effect from
   timer granularity and normal machine noise. Follow the repository's
   established statistical model rather than inventing a universal sample
   count or percentage threshold.
6. Repeat promising or surprising comparisons. Alternate or randomize
   baseline/candidate order when thermal drift, cache state, or background load
   could bias one side consistently.
7. Bound runtime and storage. A comprehensive matrix still needs an explicit
   lane set, stop condition, and retained-output policy.

Do not hide noise by reporting only the fastest run. Preserve the harness's raw
estimates or per-run summaries and report the central estimate, spread or
confidence signal it supports, and any unresolved instability.

## Control and Record the Environment

Capture enough provenance for another run to explain a disagreement:

- repository commit and dirty state;
- benchmark and comparator versions;
- runtime, compiler, build profile, features, and relevant flags;
- operating system, architecture, hardware class, and CPU mode when material;
- input corpus identity and generated-input parameters;
- warmup, samples, repetitions, measurement window, and order policy; and
- known background load, power, thermal, virtualization, or shared-runner
  limits.

Do not erase a dirty worktree to make a benchmark publishable. Use an isolated
clean checkout when the repository's publication protocol requires one, or
label the result diagnostic and preserve the user's state.

## Interpret and Report

Report the question, exact command and scope, semantic gate, environment,
measured lanes, retained artifact, and result limits. Distinguish:

- a measured difference from noise;
- a repeatable difference from its practical importance;
- throughput from latency, memory, allocation, startup, or end-to-end cost;
- a local machine result from a portable expectation; and
- an observed benchmark from a capacity or production forecast.

Do not generalize beyond the measured corpus, features, machine class, or
workflow. If evidence conflicts, inspect semantics, lane configuration,
ordering, machine stability, and raw estimates before averaging it away.

For publication evidence, require a durable artifact another checkout or
reviewer can inspect. An ignored local directory, screenshot, or copied
headline without the underlying estimates is not sufficient.

## Load, Soak, Stress, and Capacity Boundary

This reference does not define running-system load, soak, or stress
methodology. Route performance objectives, workload scenarios, service-level
tradeoffs, and capacity planning to the architecture route. Use
`effective-delivery` to run an established repository-native load or soak
command without redesigning it.

When asked to create a new load or soak program, state that its methodology is
outside this collection. Do not invent a traffic model, user
mix, target environment, credential path, destructive-data policy, or k6,
Locust, JMeter, or Autocannon stack. Ask for an approved workload and target,
preserve any repository-local runbook, and recommend explicit specialist
ownership for the experiment.
