---
id: scrna.scverse.workflow.dimensionality_reduction
schema_version: "0.1.0"
kind: skill
domain: scrna
stage: dimensionality_reduction
status: filled
state_in: ["feature_mask_key and expression matrix"]
state_out: ["representation_key"]
registered_refs: [scrna.scverse.package.scanpy, scrna.scverse.tool.scanpy_pca]
validation: [backend_neutral, state_contract_checked]
---
# Dimensionality Reduction

## Purpose

Compute a declared low-dimensional representation for graph construction,
diagnostics, integration, and downstream visualization. In the standard Scanpy
path this is PCA stored under a representation key such as `obsm["X_pca"]`,
with loadings and variance metadata recorded in corresponding AnnData slots.

This stage consumes an already approved expression source and feature mask. It
does not normalize, select HVGs, build neighbor graphs, embed cells, cluster
cells, or interpret PCs as biological conclusions.

## When Required

- Before neighbor graph construction when the graph should be built from PCA or
  another declared representation.
- Before batch-integration methods that consume PCA rather than raw expression.
- When a diagnostic representation and explained-variance record are needed for
  review.

## When Optional

- When the downstream method consumes a different declared representation, such
  as a model-derived latent space.
- When graph construction is explicitly approved on another matrix or
  representation.

## When Forbidden

- Do not run PCA if the expression source is missing or the feature mask is
  empty.
- Do not silently fall back from a missing feature mask to all genes.
- Do not overwrite an existing representation key without an explicit
  overwrite decision.
- Do not hide PCA inside neighbor graph, embedding, clustering, or integration
  stages.

## Required Input State

- A declared normalized/log expression source, unless a different PCA input
  state is explicitly approved.
- A declared `feature_mask_key` such as `var["highly_variable"]`, or an
  explicit decision to use all retained genes.
- Enough cells and selected genes to compute the requested number of components.
- A declared `representation_key`, conventionally `X_pca`.
- Existing output keys in `.obsm`, `.varm`, and `.uns` checked for collisions.

## Produced Output State

- A declared representation such as `obsm["X_pca"]`.
- PCA loadings in the matching `.varm` key when applicable.
- PCA variance and parameter metadata in the matching `.uns` key.
- Provenance recording expression source, feature mask, selected feature count,
  `n_comps`, solver/chunking policy, random state, and representation key.

## User Decision Points

- Which expression source to consume.
- Which feature mask to use, or whether to use all retained genes.
- The number of components and any solver or chunking policy needed for the
  data size.
- The output `representation_key`, including whether the default `X_pca` is
  acceptable.
- How to handle existing PCA keys: fail, use a new key, or explicitly overwrite
  with provenance.

## Registered Package Refs

- `scrna.scverse.package.scanpy`

## Registered Tool Refs

- `scrna.scverse.tool.scanpy_pca`

## Expected Artifacts

- Mutated AnnData output with the declared representation key.
- PCA loadings and variance metadata when produced by the selected tool.
- Parameter/provenance entry recording expression source, feature mask,
  `n_comps`, random state, solver/chunking policy, and representation key.
- Validation summary reporting representation shape and selected feature count.

## Validation Checks

- Confirm expression source and feature mask exist before PCA.
- Confirm the feature mask selects at least one feature and no more than the
  number of retained genes.
- Confirm `n_comps` is valid for the number of cells and selected features.
- Confirm the representation key exists after PCA and has one row per cell.
- Confirm matching `.varm` and `.uns` keys are present when expected.
- Confirm no neighbor graph, embedding, cluster labels, or marker output was
  created by this stage.

## Failure Modes

- Empty or missing feature mask.
- Requested `n_comps` exceeds what the data shape can support.
- Existing representation keys are overwritten without approval.
- Sparse or backed matrices trigger unexpected memory use.
- PCs are dominated by QC metrics, library size, cell cycle, mitochondrial
  content, or batch effects.
- Deprecated parameter choices obscure the actual feature mask used.

## Allowed Claims

- A declared low-dimensional representation was produced with the recorded
  expression source, feature mask, and PCA parameters.
- The representation can be offered to neighbor graph or integration stages if
  their state checks pass.
- Explained-variance metadata are available when present in the output.

## Forbidden Claims

- PCA removes batch effects or unwanted biological variation by itself.
- PCs define cell types or clusters without downstream evidence.
- PCA is the only acceptable representation for graph construction.
- A graph, embedding, cluster assignment, or marker result exists unless a later
  approved stage produced it.

## Next Stage Routing

- Route to `08_neighbor_graph` with the declared `representation_key`.
- Route to `07_batch_integration` when the selected integration method consumes
  PCA or another representation.
- Route back to `05_feature_selection` if the feature mask is missing or
  inappropriate.
- Route back to `04_normalization_transform` if the expression source is not in
  the required state.

## Backend-Neutral Rule

Do not place workflow-engine, shell, script, or notebook syntax in this skill.
Execution belongs in wrappers and adapters after the user approves the exact
operation, parameters, and artifacts.
