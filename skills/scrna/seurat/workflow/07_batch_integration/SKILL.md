---
id: scrna.seurat.workflow.batch_integration
schema_version: "0.1.0"
kind: skill
domain: scrna
stage: batch_integration
status: filled
state_in: [batch_metadata, normalized_or_reduced_state]
state_out: [integrated_assay_or_reduction]
registered_refs: [scrna.seurat.package.seurat, scrna.seurat.package.harmony, scrna.seurat.package.seuratwrappers, scrna.seurat.tool.integrate_layers, scrna.seurat.tool.find_integration_anchors, scrna.seurat.tool.integrate_data]
validation: [backend_neutral, seurat_object_state_contract]
---
# Seurat Batch Integration

## Purpose

Integrate batches, samples, technologies, or modalities only after reviewing
design, confounding, and downstream interpretation.

## When Required

When the approved analysis needs an integrated reduction or assay for graph and
embedding steps.

## When Optional

If unintegrated analysis is the intended comparison or existing integrated state
is valid.

## When Forbidden

Do not integrate when batch is fully confounded with the biological condition
unless interpretation limits are explicit.

## Required Input State

Batch/sample metadata, assay/layer state, source reduction or object list, and
selected method.

## Produced Output State

Integrated assay, reduction, or anchor set under declared output keys.

## User Decision Points

Method, batch variable, feature set, dimensions, output key, and whether to keep
unintegrated results for comparison.

## Registered Package Refs

- `scrna.seurat.package.seurat`
- `scrna.seurat.package.harmony`
- `scrna.seurat.package.seuratwrappers`

## Registered Tool Refs

- `scrna.seurat.tool.integrate_layers`
- `scrna.seurat.tool.find_integration_anchors`
- `scrna.seurat.tool.integrate_data`

## Expected Artifacts

Updated object, integration provenance, and comparison diagnostics.

## Validation Checks

Confirm batch columns, source state, output key, dimensions, and no unapproved
overwrites.

## Failure Modes

Overcorrection, failed anchors, missing method dependencies, and confounded
design.

## Allowed Claims

An integrated representation was produced under stated assumptions.

## Forbidden Claims

Integration does not prove batch effects are solved or biology is preserved.

## Next Stage Routing

Route to neighbor graph, embedding, clustering, or marker ranking with scale
limits documented.
