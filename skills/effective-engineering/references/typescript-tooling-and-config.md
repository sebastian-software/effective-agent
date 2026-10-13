# Tooling and Config

## Read the `tsconfig` as a Contract

The compiler options define the guarantees the rest of the code relies on. Read
them before changing types, and treat the meaning-bearing options as the
contract rather than defaults to normalize:

- `strict` bundles `strictNullChecks`, `noImplicitAny`, `strictFunctionTypes`,
  and more; whether it is on decides how much the type system already proves;
- `module` and `moduleResolution` (for example `NodeNext`, `Bundler`) decide how
  imports resolve and what the emit looks like — they are runtime-affecting;
- `target` and `lib` decide which syntax and globals are available and must match
  the actual runtime;
- `verbatimModuleSyntax`, `isolatedModules`, and `esModuleInterop` change how
  imports and type-only imports emit, which matters for CJS/ESM interop and for
  single-file transpilers (esbuild, SWC, Babel);
- `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, and
  `noImplicitOverride` are opt-in checks a repository either has or has not
  adopted.

Check the installed TypeScript major version before reading an absent option
as its old default; defaults and deprecated options change between majors.

Do not blanket-enable every strict or opt-in flag against the repository's
convention. Turning on `noUncheckedIndexedAccess` or `exactOptionalPropertyTypes`
across a codebase is a substantive change with real churn; propose it as its own
decision, not as a side effect of a feature change.

## Match Build and Runtime Targets to Reality

Emit and syntax must match where the code runs. Confirm the runtime — a specific
Node LTS line, an edge or worker runtime, or the browser — and set `target`,
`lib`, and module settings to it rather than to a generic default. Do not assume
a global (`fetch`, `structuredClone`, `AbortController`, Web Streams) exists;
check the target runtime's version. Distinguish type-checking (`tsc --noEmit`)
from the actual build tool: many repositories transpile with esbuild, SWC, or a
bundler and use `tsc` only for checking, so a passing `tsc` does not prove the
shipped bundle behaves the same.

## Follow the Repository's Lint and Format Contract

Discover and follow the existing linter (typically ESLint with
`typescript-eslint`) and formatter (Prettier, Biome, or an ESLint style config)
before writing or reformatting code. The rule that changes decisions: adopt the
repository's rule set and formatting; do not introduce a different formatter,
reformat untouched code, or add lint rules as incidental cleanup. When a
type-aware lint rule flags real unsafety (a floating promise, an unsafe `any`
flow), fix the code rather than disabling the rule.

## Stay Package-Manager Agnostic

Detect the package manager from the lockfile (`package-lock.json`,
`pnpm-lock.yaml`, `yarn.lock`, `bun.lock` or `bun.lockb`) and workspace layout, and use it.
Do not switch managers, regenerate a lockfile under a different tool, or assume
npm. Respect an existing workspaces or monorepo layout (pnpm/npm/yarn workspaces,
Turborepo, Nx) and its project-reference or build-graph conventions rather than
flattening it.
