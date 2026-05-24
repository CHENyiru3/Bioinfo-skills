---
id: scrna.seurat.workflow.dimensionality_reduction
schema_version: "0.1.0"
kind: skill
domain: scrna
stage: dimensionality_reduction
status: filled
state_in: [scaled_assay_or_sct_assay]
state_out: [reduction_key]
registered_refs: [scrna.seurat.package.seurat, scrna.seurat.tool.scale_data, scrna.seurat.tool.run_pca]
validation: [backend_neutral, seurat_object_state_contract]
---
# Seurat Dimensionality Reduction

## Purpose

Compute a declared reduction, usually PCA, for graph construction,
visualization, and integration.

## When Required

Before neighbor graph construction from a PCA-like representation.

## When Optional

If a current reduction exists with matching assay, features, dimensions, and
provenance.

## When Forbidden

Do not recompute reductions while hiding changes to feature scope or assay.

## Required Input State

Selected assay, feature set, scaled or SCT-compatible data, and output key.

## Produced Output State

Named reduction with embeddings/loadings and provenance.

## User Decision Points

Scaling covariates, feature scope, number of components, seed, and reduction
name.

## Registered Package Refs

- `scrna.seurat.package.seurat`

## Registered Tool Refs

- `scrna.seurat.tool.scale_data`
- `scrna.seurat.tool.run_pca`

## Expected Artifacts

Updated object, reduction summary, and explained-variance diagnostics when
available.

## Validation Checks

Confirm reduction rows match cells, dimensions are sufficient, and key
replacement was approved.

## Failure Modes

Missing scaled data, dense memory pressure, stale features, and batch-driven
components.

## Allowed Claims

The named reduction was computed from declared assay/features.

## Forbidden Claims

PCA dimensions do not prove biological axes.

## Next Stage Routing

Route to integration, neighbor graph, or embedding visualization.
