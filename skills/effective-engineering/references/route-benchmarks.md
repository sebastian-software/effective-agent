# Route: Benchmark Methodology

Use this route to design, repair, or interpret a repository-native
microbenchmark, comparative benchmark, or bounded end-to-end workflow
benchmark, and before making a publishable performance claim.

## Read

[Benchmark methodology](benchmark-methodology.md) — construction, warmup,
variance, comparison discipline, environment control, and how to report a
result honestly.

## Apply

- Name the performance question before choosing a harness. A benchmark without
  a decision attached measures nothing anyone will act on.
- Record workload, platform, toolchain, build profile, baseline, and metric with
  every result. A number without its environment is not evidence.
- Prefer a trend or relative threshold on shared CI when an absolute number
  would be brittle.
- Report variance and the comparison's limits. Do not convert a noisy
  improvement into a headline ratio.
- Do not claim load, soak, stress, or capacity methodology; that is a different
  discipline of measurement and no first-party route currently claims its
  execution.

## Cross-links

- The performance question, workload scenario, target, and capacity decision
  are the Architecture route.
- A focused performance-regression guard for one function or service path is
  the Testing route.
- Rust-specific profiling, layout, and SIMD work are the Rust Performance and
  Rust Unsafe routes.
- Executing an established benchmark command belongs to `effective-delivery`.
- Browser performance measurement belongs to `effective-web`.
