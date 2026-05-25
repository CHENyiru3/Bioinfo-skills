---
id: scrna.seurat.workflow.specialized_ecosystem
schema_version: "0.1.0"
kind: skill
domain: scrna
stage: specialized_ecosystem
status: filled
state_in: [specialized_seurat_request]
state_out: [specialized_stage_route]
registered_refs: [scrna.seurat.package.bpcells, scrna.seurat.package.signac, scrna.seurat.package.azimuth, scrna.seurat.package.seuratdisk, scrna.seurat.tool.bpcells_open_matrix_dir, scrna.seurat.tool.bpcells_open_matrix_10x_hdf5, scrna.seurat.tool.bpcells_open_matrix_anndata_hdf5, scrna.seurat.tool.bpcells_write_matrix_dir, scrna.seurat.tool.sketch_data, scrna.seurat.tool.signac_gene_activity]
validation: [backend_neutral, seurat_object_state_contract]
---
# Seurat Specialized Ecosystem

## Purpose

Route Seurat extensions such as BPCells, Signac, sketching, spatial workflows,
reference mapping, conversion, and SeuratWrappers methods.

## When Required

When the request uses a specialized package or modality beyond core scRNA.

## When Optional

If a narrower Seurat stage already owns the requested method.

## When Forbidden

Do not load optional packages or source-route methods without runtime evidence
and method-specific state checks.

## Required Input State

Modality, package, method, object state, optional dependency status, and output
key policy.

## Produced Output State

Specialized objects, assays, reductions, matrices, or conversion artifacts
declared by method-specific refs.

## User Decision Points

Capability group, package source, runtime availability, method parameters, and
accepted state-loss or approximation limits.

## Registered Package Refs

- `scrna.seurat.package.bpcells`
- `scrna.seurat.package.signac`
- `scrna.seurat.package.azimuth`
- `scrna.seurat.package.seuratdisk`

## Registered Tool Refs

- `scrna.seurat.tool.bpcells_open_matrix_dir`
- `scrna.seurat.tool.bpcells_open_matrix_10x_hdf5`
- `scrna.seurat.tool.bpcells_open_matrix_anndata_hdf5`
- `scrna.seurat.tool.bpcells_write_matrix_dir`
- `scrna.seurat.tool.sketch_data`
- `scrna.seurat.tool.signac_gene_activity`

## Expected Artifacts

Method-specific reports, output objects or matrices, and dependency/runtime
evidence.

## Validation Checks

Confirm optional package status, required object state, output keys, and method
provenance.

## Failure Modes

Missing optional packages, source install failure, genome/reference mismatch,
lost state during conversion, and unsupported backed matrix operations.

## Allowed Claims

The specialized method ran under declared package and state assumptions.

## Forbidden Claims

Do not generalize specialized outputs beyond their package-specific assumptions.

## Next Stage Routing

Route back to core stages after specialized state is produced, or to
interoperability/reporting when conversion is the goal.
