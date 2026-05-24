---
id: scrna.seurat.package.sctransform
kind: package_ref
package: sctransform
import_name: sctransform
language: r
ecosystem: seurat
docs_local: seurat_tutorial
source_urls: [https://satijalab.org/seurat/articles/sctransform_vignette.html]
source_version: local Seurat docs mirror label 5.4.0; local tutorial runtime observed separately
source_accessed_at: 2026-05-25
source_local_paths: [seurat_tutorial/articles/sctransform_vignette.html, seurat_tutorial/reference/sctransform.html]
distillation_status: needs_version_check
runtime_status: installed
workflow_stages: [04_normalization_transform, 05_feature_selection, 07_batch_integration]
install_probe: "R -q -e 'library(sctransform); packageVersion(\"sctransform\")'"
import_probe: "library(sctransform)"
---
# sctransform

## Role In Workflow

sctransform provides variance-stabilizing transformation used by Seurat's SCT
workflow.

## Supported Stages

Use it for `SCTransform`-based normalization and feature modeling when count
layers and modeling assumptions are explicit.

## Required Object State

The input must preserve suitable counts for the target assay. Wrappers must not
run SCT on log-normalized data.

## Produced Object State

SCT workflows create or update an `SCT` assay, model metadata, transformed
values, variable features, and residual-related state.

## Major API Families

Seurat-facing `SCTransform` usage and lower-level sctransform model functions.

## Runtime Availability

The local mirrored tutorial environment contains sctransform.

## Failure Modes

Missing raw counts, incorrect assay selection, memory pressure, model fit
failures, and incompatible downstream assumptions about counts versus residuals.

## Scientific Caveats

SCT changes the expression scale and should not be mixed silently with
log-normalized RNA workflows or count-based differential testing.

## When To Avoid

Avoid SCT when count state is unavailable, when a count-based method requires
raw counts, or when the analysis plan already approved a different
normalization model.

## Sources Used

- Public vignette: `https://satijalab.org/seurat/articles/sctransform_vignette.html`.
- Local archive: `seurat_tutorial/articles/sctransform_vignette.html`.
- Local reference: `seurat_tutorial/reference/sctransform.html`.
