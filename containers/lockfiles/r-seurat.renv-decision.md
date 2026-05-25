# R/Seurat renv Decision

Status: decision recorded
Date: 2026-05-25

The base R/Seurat runtime is conda-owned through `envs/r-seurat.yml`.

No `renv.lock` is generated for the base stack because the selected base
packages are available from conda-forge or bioconda and should be resolved by
the conda environment and future conda-lock output.

Use a dedicated `renv.lock` only when source-route packages need full recursive
R-package dependency ownership outside conda. For the current v0 runtime, conda
owns the base and dependency stack, while
`containers/lockfiles/r-seurat-source-packages.tsv` records the exact GitHub
archive commits installed by `scripts/install_seurat_source_packages.R`.

Current source-route packages installed in the local runtime:

- `Azimuth`
- `SeuratDisk`
- `SeuratData`
- `SeuratWrappers`

Current source-route optional packages still pending verification:

- specialized spatial packages pending verification
- specialized ATAC annotation packages pending verification
