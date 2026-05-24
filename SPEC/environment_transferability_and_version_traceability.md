# Environment Transferability And Version Traceability

Status: implemented v0

This SPEC defines how Bioinfo-skills should keep package references, skill
references, environment files, lock snapshots, and runtime reports synchronized
across Python/scverse and R/Seurat support.

The immediate driver is Seurat/R support, but the rule is broader: every package
that a skill can route to must have a traceable installation surface and an
observable runtime status.

## 1. Goals

- Make package environments transferable across machines through explicit,
  checked-in environment specs.
- Keep versions traceable from package reference to documentation source,
  environment spec, lock snapshot, and runtime report.
- Support both Python/scverse and R/Seurat without mixing package managers in a
  way that hides provenance.
- Keep runtime skills independent from local tutorial mirrors and generated
  environments.
- Define implementation tasks before changing package refs, skill refs,
  wrappers, or lock files.

## 2. Non-Goals

- Do not hand-author exact lock files in this planning phase.
- Do not require all optional tutorial packages in the default environment.
- Do not make local folders such as `seurat_tutorial/conda_env` or
  `bioinfo_tutorial/conda_env` runtime dependencies.
- Do not treat article `sessionInfo()` output as a pin by itself. It is useful
  evidence, but package refs need an explicit source, source version, and access
  date.

## 3. Current Baseline

Existing Bioinfo-skills files:

- `envs/scverse-python.yml`
- `envs/scverse-python-extra.txt`
- `envs/r-seurat-placeholder.yml`
- `workflow/envs/scverse.yaml`
- `containers/lockfiles/scverse-python.conda-lock.placeholder.yml`
- `containers/lockfiles/r-seurat.renv.lock.placeholder`
- `reports/runtime/scverse_runtime_status.*`
- `tool_market/packages/scrna/scverse/scanpy.md`
- `skills/scrna/scverse/**/SKILL.md`
- `skills/scrna/seurat/SKILL.md` placeholder

External source material currently visible in the workspace:

- `seurat_tutorial/environment.yml`
- `seurat_tutorial/SETUP.md`
- `seurat_tutorial/install_v5.html`
- `seurat_tutorial/articles/*.html`
- `seurat_tutorial/reference/*.html`

The Seurat tutorial mirror already has a richer R environment than the current
Bioinfo-skills placeholder. That mirror must be treated as source evidence, not
as the installed environment for Bioinfo-skills.

## 4. Traceability Model

Each package should be represented at four levels.

```text
package ref        durable package role, docs source, intended version policy
environment spec   transferable install request, grouped by capability
lock snapshot      generated resolver output for a platform or R source stack
runtime report     observed import/load/version status in a concrete runtime
```

These levels answer different questions:

- Package refs answer "why this package exists in the skill system".
- Environment specs answer "how to request an install".
- Lock snapshots answer "what the resolver produced".
- Runtime reports answer "what is actually importable or loadable now".

No single level should substitute for the others.

## 5. Canonical Package Matrix

Implementation should introduce a canonical matrix, proposed as
`envs/package-matrix.yml`, before adding more generated files. It should be
small enough to review by hand and structured enough to audit.

Required fields per package:

```yaml
- id: scrna.seurat.package.seurat
  package: Seurat
  import_name: Seurat
  language: r
  ecosystem: seurat
  package_ref: tool_market/packages/scrna/seurat/seurat.md
  skill_refs:
    - skills/scrna/seurat/SKILL.md
  env_groups:
    - r_seurat_core
  conda_package: r-seurat
  cran_package: Seurat
  bioconductor_package: null
  source_urls:
    - https://satijalab.org/seurat/
    - https://cran.r-project.org/package=Seurat
  source_version_policy: "match selected Seurat docs series"
  desired_version: null
  lock_version: null
  runtime_version: null
  runtime_probe: "Rscript -e 'library(Seurat); packageVersion(\"Seurat\")'"
  status: planned
```

Recommended optional fields:

- `github_repo`
- `r_universe`
- `platform_notes`
- `system_requirements`
- `docs_local`
- `source_local_paths`
- `distillation_status`
- `runtime_status`
- `last_verified_at`

## 6. Version Sync Rules

For each package ref:

1. `source_version` records the documentation or package-doc version used for
   distillation.
2. `desired_version` records the version or range requested by the environment
   policy.
3. `lock_version` records the generated resolved version.
4. `runtime_version` records the version loaded in a concrete runtime report.
5. A mismatch is allowed only when it is explicit and classified.

Mismatch classes:

- `docs_ahead_of_runtime`: docs are newer than the installed package.
- `runtime_ahead_of_docs`: runtime is newer than the docs used for the ref.
- `optional_missing`: package is intentionally absent from the base env.
- `platform_limited`: package is unavailable or unreliable on a platform.
- `source_only`: package is installed from CRAN, R-universe, or GitHub outside
  conda-lock coverage.

The package ref should not claim `runtime_status: installed` unless a runtime
report or probe backs that claim.

## 7. Environment Grouping

Use environment groups instead of one unbounded environment.

Required groups:

- `scverse_core`: Python/scverse packages needed by approved Python wrappers.
- `scverse_extra`: optional Python packages used by broader tutorials or
  advanced workflows.
- `r_seurat_core`: R packages needed for basic Seurat object creation,
  preprocessing, dimensionality reduction, clustering, visualization, and marker
  ranking.
- `r_seurat_performance`: packages recommended by Seurat docs for speed or
  large data, such as BPCells, presto, and glmGamPoi.
- `r_seurat_modalities`: packages for ATAC, spatial, multimodal, reference
  mapping, sketching, or deconvolution.
- `r_notebook_docs`: packages and tools for notebooks and rendered docs, such
  as IRkernel, rmarkdown, knitr, JupyterLab, and pandoc.
- `r_tutorial_data`: SeuratData and dataset packages. This group should not be
  part of the default runtime because it can trigger large downloads.

Proposed install files:

```text
envs/
  package-matrix.yml
  scverse-python.yml
  scverse-python-extra.txt
  r-seurat.yml
  r-seurat-optional.yml
  r-seurat-notebook.yml
```

The existing `envs/r-seurat-placeholder.yml` should graduate to
`envs/r-seurat.yml` during implementation, with a compatibility note or removal
handled in the same change.

## 8. Locking Strategy

Conda:

- Use conda YAML files as the transferable install surface.
- Generate conda-lock files for supported platforms when resolver access is
  available.
- Keep the human-authored YAML small and capability grouped.
- Pin major compatibility axes first, such as `r-base=4.4` for the current
  Seurat tutorial source.

R:

- Use conda packages for R packages available through conda-forge or bioconda
  when they are part of the base transferable environment.
- Use `renv.lock` only for R source packages that must come from CRAN,
  Bioconductor, R-universe, or GitHub and cannot be represented cleanly through
  conda.
- Do not install the same R package through both conda and renv in the same
  environment without recording which package manager owns it.

Containers:

- Container templates should install from the same environment specs.
- Container build logs may become runtime evidence, but they are not package
  refs.

## 9. Runtime Reports

Python runtime reports already exist for scverse. Implementation should add an
R runtime report with the same intent:

```text
reports/runtime/
  scverse_runtime_status.json
  scverse_runtime_status.md
  scverse_runtime_status.tsv
  seurat_runtime_status.json
  seurat_runtime_status.md
  seurat_runtime_status.tsv
```

Required R probe fields:

- package name
- import/load expression
- observed version
- runtime status
- error message if missing
- environment path
- R version
- platform
- timestamp

## 10. Validation Gates

Before package refs or skill refs claim installed support:

- The package matrix parses.
- Package refs validate against `schemas/package_ref.schema.json`.
- Tool refs validate against `schemas/tool_ref.schema.json`.
- Runtime probes produce a report.
- Environment files resolve or fail with a captured reason.
- Skills only register refs whose package/tool files exist.
- Tests that enforce skill tree structure and package coverage pass.

## 11. Implementation Tasks

### Phase A: Inventory And Matrix

- `ENV-001`: Inventory all package refs and tool refs currently present under
  `tool_market/`.
- `ENV-002`: Inventory all packages declared in `envs/*.yml`,
  `workflow/envs/*.yaml`, and container templates.
- `ENV-003`: Inventory R packages declared in `seurat_tutorial/environment.yml`
  and packages loaded in `seurat_tutorial/articles/*.html`.
- `ENV-004`: Create `envs/package-matrix.yml` with package ids, package refs,
  skill refs, install sources, environment groups, source URLs, and probes.
- `ENV-005`: Add a structural test that every package ref listed in the matrix
  points to an existing package ref file or is marked `planned`.

### Phase B: Environment Specs

- `ENV-006`: Replace `envs/r-seurat-placeholder.yml` with
  `envs/r-seurat.yml` after the Seurat package matrix entries exist.
- `ENV-007`: Add `envs/r-seurat-optional.yml` for modality, spatial, ATAC,
  reference mapping, and tutorial extension packages.
- `ENV-008`: Add `envs/r-seurat-notebook.yml` for IRkernel, rmarkdown, knitr,
  JupyterLab, pandoc, and rendered tutorial support.
- `ENV-009`: Check that workflow env files either reuse the canonical envs or
  explicitly document why a smaller execution env is needed.
- `ENV-010`: Update container templates to consume the canonical env specs,
  not ad hoc package lists.

### Phase C: Lock And Runtime Evidence

- `ENV-011`: Generate conda-lock files for supported platforms when network and
  resolver access are available.
- `ENV-012`: Replace `containers/lockfiles/r-seurat.renv.lock.placeholder` with
  either a real `renv.lock` or a documented decision that the base R stack is
  conda-owned.
- `ENV-013`: Add `scripts/check_seurat_runtime.R` or an equivalent probe runner.
- `ENV-014`: Emit `reports/runtime/seurat_runtime_status.{json,md,tsv}`.
- `ENV-015`: Add tests that prevent `runtime_status: installed` when no runtime
  report or probe evidence exists.

### Phase D: Version Traceability

- `ENV-016`: Extend package refs with `desired_version`, `lock_version`, and
  `runtime_version` fields where useful.
- `ENV-017`: Add a traceability audit that flags docs/runtime/env mismatches
  unless classified.
- `ENV-018`: Require `source_urls`, `source_version`, `source_accessed_at`, and
  `source_local_paths` for distilled package refs.
- `ENV-019`: Document mismatch classes in `reports/runtime/README.md`.
- `ENV-020`: Add a summary table linking skill ids to package refs, tool refs,
  environment groups, and runtime status.

## 12. Acceptance Criteria

This SPEC is implemented when:

- A reviewer can answer which environment installs a package from its package
  ref alone.
- A reviewer can trace a package version from docs source to env spec, lock
  snapshot, and runtime report.
- The base Seurat environment is installable without tutorial data packages.
- Optional R packages are grouped by capability and do not silently enlarge the
  base environment.
- Missing packages are recorded as missing or optional, not implied as
  installed.
- Existing scverse package refs keep working under the same traceability model.

## 13. v0 Implementation Notes

Implemented in v0:

- `envs/package-matrix.yml`
- `envs/r-seurat.yml`
- `envs/r-seurat-optional.yml`
- `envs/r-seurat-notebook.yml`
- `scripts/check_seurat_runtime.py`
- `scripts/install_seurat_source_packages.R`
- `scripts/repair_relocated_r_runtime.py`
- `reports/runtime/seurat_runtime_status.*`
- `containers/lockfiles/r-seurat-linux-64.explicit.txt`
- `containers/lockfiles/r-seurat-source-packages.tsv`
- `envs/lock-tools.yml`
- Seurat package refs and tool refs under `tool_market/`
- Seurat workflow skills and object-state contract
- multi-ecosystem runtime-report validation

Handled with explicit decisions:

- cross-platform conda-lock generation remains tool-dependent, but
  `envs/lock-tools.yml` now declares the required lock tooling and
  `containers/lockfiles/r-seurat-linux-64.explicit.txt` records the current
  Linux runtime snapshot.
- source-route R packages are pinned separately in
  `containers/lockfiles/r-seurat-source-packages.tsv` and installed by
  `scripts/install_seurat_source_packages.R`.
- base-stack `renv.lock`, because the base Seurat stack is conda-owned; see
  `containers/lockfiles/r-seurat.renv-decision.md`.
