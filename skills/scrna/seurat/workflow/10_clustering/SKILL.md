---
id: scrna.seurat.workflow.clustering
schema_version: "0.1.0"
kind: skill
domain: scrna
stage: clustering
status: filled
state_in: [neighbor_graph]
state_out: [cluster_key]
registered_refs: [scrna.seurat.package.seurat, scrna.seurat.tool.find_clusters]
validation: [backend_neutral, seurat_object_state_contract]
---
# Seurat Clustering

## Purpose

Assign graph community labels from a declared Seurat graph.

## When Required

When new exploratory cluster labels are needed for markers or annotation.

## When Optional

If curated labels or approved clusters already answer the question.

## When Forbidden

Do not cluster without a declared graph or overwrite identities without
approval.

## Required Input State

Graph name, resolution, algorithm, random seed, and output cluster key.

## Produced Output State

Cluster metadata column and identity state according to wrapper policy.

## User Decision Points

Graph, resolution, algorithm, seed, cluster key, and whether identities should
be changed.

## Registered Package Refs

- `scrna.seurat.package.seurat`

## Registered Tool Refs

- `scrna.seurat.tool.find_clusters`

## Expected Artifacts

Updated object, cluster-size table, and provenance.

## Validation Checks

Confirm graph exists, cluster labels cover all cells, sizes are nonzero, and key
replacement was approved.

## Failure Modes

Overclustering, underclustering, batch-driven labels, tiny clusters, and
identity overwrite.

## Allowed Claims

Communities were assigned under recorded graph and resolution settings.

## Forbidden Claims

Clusters are not final cell types or condition effects.

## Next Stage Routing

Route to marker ranking, annotation support, or visualization.
