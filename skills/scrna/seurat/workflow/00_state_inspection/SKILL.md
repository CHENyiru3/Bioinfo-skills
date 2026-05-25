---
id: scrna.seurat.workflow.state_inspection
schema_version: "0.1.0"
kind: skill
domain: scrna
stage: state_inspection
status: filled
state_in: [seurat_object_path]
state_out: [seurat_state_report]
registered_refs: [scrna.seurat.package.seurat, scrna.seurat.package.seuratobject]
validation: [backend_neutral, seurat_object_state_contract]
---
# Seurat State Inspection

## Purpose

Inspect a Seurat object before selecting methods, so assay, layer, reduction,
graph, identity, metadata, and version state are explicit.

## When Required

- Before mutating an unfamiliar Seurat object.
- Before converting between Seurat, SingleCellExperiment, and AnnData.
- Before using existing reductions, graphs, identities, or labels.

## When Optional

- If the same object and state report were produced in the current approved run.
- If the task only explains a package reference without touching data.

## When Forbidden

- Do not inspect by running preprocessing or modifying the object.
- Do not infer missing metadata from filenames without user confirmation.

## Required Input State

A readable Seurat object path or in-session object with declared source.

## Produced Output State

A report of package versions, object dimensions, assays, layers, reductions,
graphs, metadata columns, identities, images, and warnings. No object mutation.

## User Decision Points

Which object path to inspect, whether to include expensive summaries, and which
metadata columns define sample, batch, condition, and groups.

## Registered Package Refs

- `scrna.seurat.package.seurat`
- `scrna.seurat.package.seuratobject`

## Registered Tool Refs

- None yet; implemented through the state-inspection wrapper contract.

## Expected Artifacts

JSON and Markdown state reports, plus optional TSV summaries.

## Validation Checks

Confirm load success, dimensions, assay/layer names, reduction dimensions,
graph dimensions, metadata length, and package versions.

## Failure Modes

Unreadable object, missing package, moved BPCells backing paths, unsupported
serialized format, or object version mismatch.

## Allowed Claims

The report describes observed Seurat object state.

## Forbidden Claims

Inspection does not prove QC quality, annotation correctness, or biological
validity.

## Next Stage Routing

Route to ingest if no object exists, normalization if counts are available, or
the requested downstream stage once required state is confirmed.
