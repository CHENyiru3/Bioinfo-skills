# Runtime Reports

Generated runtime availability reports belong here.

Current report files:

- `scverse_runtime_status.*`: Python/scverse package import probes.
- `seurat_runtime_status.*`: R/Seurat package load probes.

Runtime/package mismatch classes:

- `docs_ahead_of_runtime`: docs are newer than the installed package.
- `runtime_ahead_of_docs`: runtime is newer than the docs used for the ref.
- `optional_missing`: package is intentionally absent from the base env.
- `platform_limited`: package is unavailable or unreliable on a platform.
- `source_only`: package is installed from CRAN, R-universe, or GitHub outside
  conda-lock coverage.

Missing optional source-route R packages should carry `waiver_reason` in the
JSON/TSV report and point to `scripts/install_seurat_source_packages.R`.
