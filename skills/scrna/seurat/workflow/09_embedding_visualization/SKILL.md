---
id: scrna.seurat.workflow.embedding_visualization
schema_version: "0.1.0"
kind: skill
domain: scrna
stage: embedding_visualization
status: filled
state_in: [reduction_or_graph]
state_out: [embedding_key, plots]
registered_refs: [scrna.seurat.package.seurat, scrna.seurat.tool.run_umap]
validation: [backend_neutral, seurat_object_state_contract]
---
# Seurat Embedding Visualization

## Purpose

Compute or display embeddings for diagnostic visualization.

## When Required

When a requested visualization needs a missing or stale embedding.

## When Optional

If an existing embedding is current and only plotting is requested.

## When Forbidden

Do not use UMAP as quantitative evidence for distances or trajectories.

## Required Input State

Declared reduction or graph, dimensions, output embedding key, and labels to
display.

## Produced Output State

Named embedding reduction and optional plot artifacts.

## User Decision Points

Input representation, dimensions, seed, method, output key, and plot groupings.

## Registered Package Refs

- `scrna.seurat.package.seurat`

## Registered Tool Refs

- `scrna.seurat.tool.run_umap`

## Expected Artifacts

Updated object, embedding summary, and plots.

## Validation Checks

Confirm finite coordinates, one row per cell, output key, and plot labels.

## Failure Modes

Missing input reduction, non-reproducibility, overwritten embedding, and visual
overinterpretation.

## Allowed Claims

Embedding coordinates were produced under recorded parameters.

## Forbidden Claims

Embedding geometry alone does not prove biological continuity or separation.

## Next Stage Routing

Route to clustering, annotation support, or marker ranking as needed.
