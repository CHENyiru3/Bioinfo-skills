---
id: scrna.seurat.workflow.neighbor_graph
schema_version: "0.1.0"
kind: skill
domain: scrna
stage: neighbor_graph
status: filled
state_in: [reduction_key]
state_out: [neighbor_graph]
registered_refs: [scrna.seurat.package.seurat, scrna.seurat.tool.find_neighbors]
validation: [backend_neutral, seurat_object_state_contract]
---
# Seurat Neighbor Graph

## Purpose

Construct a nearest-neighbor graph from a declared reduction for UMAP,
clustering, and graph diagnostics.

## When Required

Before graph clustering or graph-based embeddings when the graph is missing or
stale.

## When Optional

If an approved graph exists for the same reduction, dimensions, and parameters.

## When Forbidden

Do not build a graph from an undeclared reduction or overwrite graph keys
without approval.

## Required Input State

Named reduction, dimensions, graph key policy, metric/backend choices.

## Produced Output State

Neighbor and SNN graph entries under declared graph names.

## User Decision Points

Reduction, dimensions, k, graph names, nearest-neighbor method, and metric.

## Registered Package Refs

- `scrna.seurat.package.seurat`

## Registered Tool Refs

- `scrna.seurat.tool.find_neighbors`

## Expected Artifacts

Updated object, graph summary, and provenance.

## Validation Checks

Confirm reduction exists, dimensions are valid, graphs are square/cell-aligned,
and keys were not overwritten.

## Failure Modes

Missing reduction, wrong dimensions, disconnected graph, batch-driven
neighborhoods, and key collisions.

## Allowed Claims

The graph was built from the declared reduction and parameters.

## Forbidden Claims

Graph neighbors are not independent biological observations.

## Next Stage Routing

Route to embedding visualization or clustering.
