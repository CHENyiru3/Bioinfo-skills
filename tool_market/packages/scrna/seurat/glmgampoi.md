---
id: scrna.seurat.package.glmgampoi
kind: package_ref
package: glmGamPoi
import_name: glmGamPoi
language: r
ecosystem: seurat
docs_local: seurat_tutorial
source_urls: [https://github.com/const-ae/glmGamPoi, https://bioconductor.org/packages/glmGamPoi/]
source_version: local Seurat install docs recommend glmGamPoi; Bioconductor version needs verification
source_accessed_at: 2026-05-25
source_local_paths: [seurat_tutorial/install_v5.html, seurat_tutorial/articles/sctransform_vignette.html]
distillation_status: needs_version_check
runtime_status: installed
workflow_stages: [04_normalization_transform, 14_aggregation_pseudobulk_de]
install_probe: "R -q -e 'library(glmGamPoi); packageVersion(\"glmGamPoi\")'"
import_probe: "library(glmGamPoi)"
---
# glmGamPoi

## Role In Workflow

glmGamPoi provides efficient Gamma-Poisson model fitting used by Seurat-related
count modeling and SCT workflows.

## Supported Stages

Use it for count-aware normalization or differential-expression support only
when count state and model assumptions are explicit.

## Required Object State

Methods require count-like data, not arbitrary scaled or log-normalized values.

## Produced Object State

Depending on the caller, outputs may be fitted model state, residuals, or
statistics consumed by Seurat functions.

## Major API Families

Gamma-Poisson model fitting and count-model support for Seurat workflows.

## Runtime Availability

The local mirrored tutorial environment contains glmGamPoi.

## Failure Modes

Missing Bioconductor dependency, incompatible input scale, model fit failures,
or large memory use on dense matrices.

## Scientific Caveats

Model speed does not validate the experimental design or count-source policy.

## When To Avoid

Avoid for transformed expression values or when the approved workflow uses a
different statistical model.

## Sources Used

- Public repository: `https://github.com/const-ae/glmGamPoi`.
- Bioconductor page: `https://bioconductor.org/packages/glmGamPoi/`.
- Local archive: `seurat_tutorial/install_v5.html`.
