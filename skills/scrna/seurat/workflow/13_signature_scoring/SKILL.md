---
id: scrna.seurat.workflow.signature_scoring
schema_version: "0.1.0"
kind: skill
domain: scrna
stage: signature_scoring
status: filled
state_in: [gene_sets, expression_source]
state_out: [score_columns]
registered_refs: [scrna.seurat.package.seurat, scrna.seurat.tool.add_module_score]
validation: [backend_neutral, seurat_object_state_contract]
---
# Seurat Signature Scoring

## Purpose

Score declared gene sets in a Seurat object.

## When Required

When the user requests per-cell module or program scores.

## When Optional

If matching score columns already exist with gene-set provenance.

## When Forbidden

Do not score unidentified gene sets or ignore poor gene-symbol overlap.

## Required Input State

Gene sets, assay, expression layer, feature naming scheme, and output names.

## Produced Output State

Metadata score columns and gene-overlap report.

## User Decision Points

Gene set source, assay, score prefix, control settings, seed, and replacement
policy.

## Registered Package Refs

- `scrna.seurat.package.seurat`

## Registered Tool Refs

- `scrna.seurat.tool.add_module_score`

## Expected Artifacts

Updated object, score summary, matched/missing gene report.

## Validation Checks

Confirm gene overlap, finite scores, metadata columns, and seed.

## Failure Modes

Gene name mismatch, weak overlap, overwritten scores, and unstable control gene
sampling.

## Allowed Claims

Scores were computed for declared gene sets.

## Forbidden Claims

Scores alone do not prove pathway activity.

## Next Stage Routing

Route to visualization, group summaries, or downstream modeling.
