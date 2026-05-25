---
id: scrna.seurat.workflow.aggregation_pseudobulk_de
schema_version: "0.1.0"
kind: skill
domain: scrna
stage: aggregation_pseudobulk_de
status: filled
state_in: [sample_id, group_key, condition]
state_out: [aggregate_counts_or_de_plan]
registered_refs: [scrna.seurat.package.seurat, scrna.seurat.package.glmgampoi, scrna.seurat.package.seuratwrappers]
validation: [backend_neutral, seurat_object_state_contract]
---
# Seurat Aggregation Pseudobulk DE

## Purpose

Plan or produce sample-level aggregates for replicate-aware differential
expression workflows.

## When Required

When the biological question compares conditions and biological replicates
exist.

## When Optional

If the task is descriptive cluster marker ranking rather than condition testing.

## When Forbidden

Do not use cell-level markers as condition-level DE when replicate design is
required.

## Required Input State

Sample ID, condition, group/cell type, count assay/layer, and replicate counts.

## Produced Output State

Aggregated count matrices, design tables, or DE plan artifacts.

## User Decision Points

Aggregation groups, count source, design formula, contrasts, and DE backend.

## Registered Package Refs

- `scrna.seurat.package.seurat`
- `scrna.seurat.package.glmgampoi`
- `scrna.seurat.package.seuratwrappers`

## Registered Tool Refs

- `scrna.seurat.tool.find_markers` only for documented Seurat count tests, not
  as a substitute for full replicate-aware DE wrappers.

## Expected Artifacts

Pseudobulk matrix, sample metadata, design table, and method decision log.

## Validation Checks

Confirm sample/condition columns, replicate counts, group sizes, and count-like
input.

## Failure Modes

No replicates, confounded design, low counts, wrong expression scale, and
condition overclaims.

## Allowed Claims

Aggregates and design inputs were produced or validated.

## Forbidden Claims

Do not claim replicate-aware DE unless an approved DE backend was run.

## Next Stage Routing

Route to a DE-specific wrapper plan or reporting.
