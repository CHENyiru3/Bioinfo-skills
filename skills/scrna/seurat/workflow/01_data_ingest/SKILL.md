---
id: scrna.seurat.workflow.data_ingest
schema_version: "0.1.0"
kind: skill
domain: scrna
stage: data_ingest
status: filled
state_in: [raw_matrix_or_tutorial_data]
state_out: [seurat_object_counts]
registered_refs: [scrna.seurat.package.seurat, scrna.seurat.package.bpcells, scrna.seurat.package.seuratdata, scrna.seurat.tool.read10x, scrna.seurat.tool.read10x_h5, scrna.seurat.tool.create_seurat_object]
validation: [backend_neutral, seurat_object_state_contract]
---
# Seurat Data Ingest

## Purpose

Create or load a Seurat object while preserving count source, feature/cell
identifiers, metadata alignment, and optional on-disk backing.

## When Required

- When starting from 10x directories, 10x HDF5, BPCells matrices, or tutorial
  datasets.
- When converting external matrix input into a Seurat object.

## When Optional

- If an approved Seurat object already exists and has a current state report.

## When Forbidden

- Do not download large tutorial datasets without explicit approval.
- Do not filter, normalize, cluster, or annotate inside ingest.

## Required Input State

Declared input files, matrix format, metadata table, feature ID policy, and
expected modalities.

## Produced Output State

A Seurat object with counts in declared assays and aligned metadata.

## User Decision Points

Feature-name policy, assay names, initial minimum cell/feature filters, and
whether BPCells on-disk backing is required.

## Registered Package Refs

- `scrna.seurat.package.seurat`
- `scrna.seurat.package.bpcells`
- `scrna.seurat.package.seuratdata`

## Registered Tool Refs

- `scrna.seurat.tool.read10x`
- `scrna.seurat.tool.read10x_h5`
- `scrna.seurat.tool.create_seurat_object`
- `scrna.seurat.tool.bpcells_open_matrix_10x_hdf5`

## Expected Artifacts

Seurat object file, ingest summary, metadata alignment report, and provenance.

## Validation Checks

Check dimensions, unique identifiers, assay/layer names, metadata row alignment,
and count sparsity.

## Failure Modes

Malformed input, duplicate names, metadata mismatch, large downloads, and moved
on-disk matrix paths.

## Allowed Claims

The object was created from the declared input with recorded identifier policy.

## Forbidden Claims

Ingest does not prove QC, normalization, or biological labels.

## Next Stage Routing

Route to state inspection or QC metrics.
