---
id: scrna.seurat.workflow.qc_metrics_filtering
schema_version: "0.1.0"
kind: skill
domain: scrna
stage: qc_metrics_filtering
status: filled
state_in: [seurat_object_counts]
state_out: [qc_metrics, optionally_filtered_seurat_object]
registered_refs: [scrna.seurat.package.seurat]
validation: [backend_neutral, seurat_object_state_contract]
---
# Seurat QC Metrics Filtering

## Purpose

Compute and review QC metrics, then apply explicit filtering thresholds only
after approval.

## When Required

Before normalization when QC state is unknown or input data are newly ingested.

## When Optional

If upstream QC was already documented and no filtering changes are requested.

## When Forbidden

Do not silently filter cells or features as a side effect of downstream steps.

## Required Input State

Counts assay, species/mitochondrial feature naming policy, and metadata needed
to stratify QC by sample or batch.

## Produced Output State

QC columns and, if approved, a filtered Seurat object with retained cell/feature
counts.

## User Decision Points

QC metrics, thresholds, stratification columns, and whether filtering is only a
report or object mutation.

## Registered Package Refs

- `scrna.seurat.package.seurat`

## Registered Tool Refs

- `scrna.seurat.tool.add_module_score` only for explicit signature-like QC
  scoring, not basic QC.

## Expected Artifacts

QC summary tables, threshold decisions, and object retention report.

## Validation Checks

Confirm QC columns are one value per cell and filtered object dimensions match
the retention report.

## Failure Modes

Wrong mitochondrial pattern, sample-specific threshold bias, and unrecorded
filtering.

## Allowed Claims

Reported metrics and filters were applied as documented.

## Forbidden Claims

QC thresholds do not validate cell types or remove all artifacts.

## Next Stage Routing

Route to normalization or back to ingest/state inspection if count state is
invalid.
