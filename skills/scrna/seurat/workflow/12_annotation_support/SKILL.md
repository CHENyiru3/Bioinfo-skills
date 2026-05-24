---
id: scrna.seurat.workflow.annotation_support
schema_version: "0.1.0"
kind: skill
domain: scrna
stage: annotation_support
status: filled
state_in: [labels_markers_or_reference]
state_out: [annotation_candidates]
registered_refs: [scrna.seurat.package.seurat, scrna.seurat.package.azimuth, scrna.seurat.tool.find_transfer_anchors, scrna.seurat.tool.map_query]
validation: [backend_neutral, seurat_object_state_contract]
---
# Seurat Annotation Support

## Purpose

Support label review through markers, references, or transfer mapping while
preserving uncertainty.

## When Required

When clusters need biological interpretation or a reference mapping is requested.

## When Optional

If curated labels with provenance already exist.

## When Forbidden

Do not overwrite final annotations without review and do not treat transferred
labels as definitive.

## Required Input State

Candidate groups, marker evidence, reference provenance, species, feature
overlap, and score fields.

## Produced Output State

Candidate labels, transferred labels/scores, or annotation review tables.

## User Decision Points

Reference source, label fields, confidence thresholds, output columns, and
manual review policy.

## Registered Package Refs

- `scrna.seurat.package.seurat`
- `scrna.seurat.package.azimuth`

## Registered Tool Refs

- `scrna.seurat.tool.find_transfer_anchors`
- `scrna.seurat.tool.map_query`

## Expected Artifacts

Annotation evidence table, transferred-label report, score summaries, and
provenance.

## Validation Checks

Confirm label columns, score columns, reference source, feature overlap, and no
unapproved overwrite.

## Failure Modes

Poor reference match, species mismatch, missing markers, and overconfident
automated labels.

## Allowed Claims

The workflow generated annotation candidates or transferred labels.

## Forbidden Claims

Automated labels are not final without expert/marker review.

## Next Stage Routing

Route to visualization, marker ranking, or reporting.
