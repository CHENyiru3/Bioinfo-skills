---
id: scrna.seurat.workflow.normalization_transform
schema_version: "0.1.0"
kind: skill
domain: scrna
stage: normalization_transform
status: filled
state_in: [seurat_object_counts]
state_out: [normalized_or_sct_assay]
registered_refs: [scrna.seurat.package.seurat, scrna.seurat.package.sctransform, scrna.seurat.package.glmgampoi, scrna.seurat.tool.normalize_data, scrna.seurat.tool.sctransform]
validation: [backend_neutral, seurat_object_state_contract]
---
# Seurat Normalization Transform

## Purpose

Create declared normalized expression state through log normalization or SCT.

## When Required

Before feature selection, PCA, graph analysis, scoring, or marker ranking that
requires normalized data.

## When Optional

If an approved normalized or SCT assay already exists and matches the task.

## When Forbidden

Do not normalize transformed data as if it were counts. Do not mix RNA log data
and SCT residuals without declaring the scale.

## Required Input State

Counts layer, assay name, and selected normalization method.

## Produced Output State

Assay `data` layer for log normalization or an SCT assay with model metadata.

## User Decision Points

LogNormalize versus SCT, assay names, scale factor, regression variables, and
new assay name.

## Registered Package Refs

- `scrna.seurat.package.seurat`
- `scrna.seurat.package.sctransform`
- `scrna.seurat.package.glmgampoi`

## Registered Tool Refs

- `scrna.seurat.tool.normalize_data`
- `scrna.seurat.tool.sctransform`

## Expected Artifacts

Updated Seurat object and normalization provenance.

## Validation Checks

Confirm input counts exist, output assay/layer exists, dimensions are unchanged,
and method parameters are recorded.

## Failure Modes

Wrong assay, missing counts, memory pressure, invalid regression covariates, and
renormalization without approval.

## Allowed Claims

The object has the declared normalized or SCT state.

## Forbidden Claims

Normalization alone does not remove batch effects or prove biological signal.

## Next Stage Routing

Route to feature selection, dimensionality reduction, scoring, or integration.
