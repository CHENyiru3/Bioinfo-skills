# Lockfiles

This directory reserves locations for reproducibility lockfiles.

Current v0 status:

- `scverse-python.conda-lock.placeholder.yml` is still a placeholder.
- `r-seurat-linux-64.explicit.txt` is a generated explicit Linux lock snapshot
  exported from the local Seurat tutorial conda environment.
- `r-seurat-source-packages.tsv` records the pinned GitHub archive commits for
  source-route R packages installed outside conda.
- `r-seurat.renv-decision.md` records that the base Seurat stack is conda-owned
  by `envs/r-seurat.yml`; create a real `renv.lock` only when a source-route R
  package needs full recursive R-package dependency ownership outside conda.
- `envs/lock-tools.yml` declares the tool environment for future
  cross-platform `conda-lock` generation.
- generated lockfiles should record tool versions, source package ownership,
  and platform assumptions.
