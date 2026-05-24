---
id: scrna.seurat.workflow.marker_ranking
schema_version: "0.1.0"
kind: skill
domain: scrna
stage: marker_ranking
status: filled
state_in: [group_key, expression_source]
state_out: [marker_table]
registered_refs: [scrna.seurat.package.seurat, scrna.seurat.package.presto, scrna.seurat.tool.find_markers, scrna.seurat.tool.find_all_markers]
validation: [backend_neutral, seurat_object_state_contract]
---
# Seurat Marker Ranking

## Purpose

Rank marker genes for declared groups using explicit assay, layer, and test
choices.

## When Required

When clusters or groups need descriptive markers for review.

## When Optional

If existing marker tables already match the group and expression source.

## When Forbidden

Do not use cell-level marker ranking as replicate-aware condition DE.

## Required Input State

Group key, assay, slot/layer, test method, thresholds, and group counts.

## Produced Output State

Marker table and provenance; object mutation is not required.

## User Decision Points

FindMarkers versus FindAllMarkers, grouping, comparison, assay/slot, test, and
thresholds.

## Registered Package Refs

- `scrna.seurat.package.seurat`
- `scrna.seurat.package.presto`

## Registered Tool Refs

- `scrna.seurat.tool.find_markers`
- `scrna.seurat.tool.find_all_markers`

## Expected Artifacts

Marker tables, group counts, method metadata, and warnings.

## Validation Checks

Confirm group labels, group sizes, assay/layer state, output columns, and method
metadata.

## Failure Modes

Tiny groups, wrong identities, incompatible expression scale, and condition
overclaims.

## Allowed Claims

Markers were ranked for declared groups under stated settings.

## Forbidden Claims

Marker tables do not prove cell type or condition causality.

## Next Stage Routing

Route to annotation support or pseudobulk DE planning.
