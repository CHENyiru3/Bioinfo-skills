---
id: scrna.seurat.workflow.feature_selection
schema_version: "0.1.0"
kind: skill
domain: scrna
stage: feature_selection
status: filled
state_in: [normalized_or_sct_assay]
state_out: [variable_features]
registered_refs: [scrna.seurat.package.seurat, scrna.seurat.tool.find_variable_features]
validation: [backend_neutral, seurat_object_state_contract]
---
# Seurat Feature Selection

## Purpose

Select variable features for dimensionality reduction and integration.

## When Required

Before PCA or integration workflows that rely on variable features.

## When Optional

If variable features already exist and match the approved assay/method.

## When Forbidden

Do not overwrite variable features without recording the previous state.

## Required Input State

Selected assay and normalized or transformed expression state.

## Produced Output State

Variable features stored on the selected assay.

## User Decision Points

Assay, method, number of features, and whether to replace existing features.

## Registered Package Refs

- `scrna.seurat.package.seurat`

## Registered Tool Refs

- `scrna.seurat.tool.find_variable_features`

## Expected Artifacts

Updated object, selected feature count, and feature list.

## Validation Checks

Confirm features are present, unique, nonempty, and tied to the selected assay.

## Failure Modes

Wrong assay scale, too few features, stale features after filtering, and
overwriting previous selections.

## Allowed Claims

Variable features were selected under recorded parameters.

## Forbidden Claims

Feature selection alone does not identify markers or cell types.

## Next Stage Routing

Route to scaling, PCA, or integration.
