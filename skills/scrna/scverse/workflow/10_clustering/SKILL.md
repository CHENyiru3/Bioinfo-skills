---
id: scrna.scverse.workflow.clustering
schema_version: "0.1.0"
kind: skill
domain: scrna
stage: clustering
status: filled
state_in: ["declared neighbors_key"]
state_out: ["cluster_key and cluster-size metadata"]
registered_refs: [scrna.scverse.package.scanpy, scrna.scverse.tool.scanpy_leiden]
validation: [backend_neutral, state_contract_checked]
---
# Clustering

## Purpose

Assign graph communities from a declared neighbor graph for downstream marker
ranking, annotation support, composition summaries, and exploratory review.
Clustering is a decision-centered analysis step: method, graph, resolution,
seed, and output key must be explicit.

## When Required

- When the user needs new graph-based group labels for marker ranking,
  annotation support, or exploratory cell-state summaries.
- When changing `neighbors_key`, clustering method, resolution, weights, or
  random seed should produce a new `cluster_key`.
- When existing labels are absent, stale after filtering, or derived from an
  unapproved graph.

## When Optional

- If curated annotations, imported labels, or externally computed clusters
  already satisfy the question and are documented.
- If the task is replicate-aware condition testing or pseudobulk DE; those
  should use sample-level design rather than create clusters by default.
- If the user only asks to visualize existing labels.

## When Forbidden

- Do not run clustering without a declared `neighbors_key`.
- Do not overwrite existing `.obs` labels without explicit approval; use a new
  `cluster_key` for resolution sweeps.
- Do not treat clusters as cell types without marker, reference, and expert
  review.
- Do not normalize, select HVGs, compute PCA, build a graph, annotate cells, or
  rank markers inside this stage.

## Required Input State

- AnnData object with `.uns[neighbors_key]` and valid graph connectivities in
  `.obsp`.
- The graph must have provenance identifying the representation, metric,
  `n_neighbors`, and any integration method used upstream.
- The intended `cluster_key` must be absent or explicitly approved for
  replacement.
- Optional stratification or restricted-clustering metadata must exist in
  `.obs` before use.

## Produced Output State

- Cluster labels in `.obs[cluster_key]`, stored as categorical labels.
- Clustering parameter metadata in `.uns[cluster_key]` or project provenance,
  including method, graph key, resolution, seed, package/flavor, weights, and
  iteration settings.
- Cluster-size table for the full object and, when relevant, by sample, batch,
  or condition.
- No marker table, annotation column, pseudobulk result, or embedding should be
  produced by this stage.

## User Decision Points

- Which `neighbors_key` to cluster.
- Clustering method and implementation flavor, usually Leiden for new work.
- `cluster_key` naming convention, especially for resolution sweeps.
- Resolution value or sweep range, with a plan for selecting among outputs.
- Random seed, weighted versus unweighted graph use, and iteration settings.
- Whether to report cluster sizes overall and by sample or batch to detect
  confounding.

## Registered Package Refs

- `scrna.scverse.package.scanpy`

## Registered Tool Refs

- `scrna.scverse.tool.scanpy_leiden`

## Expected Artifacts

- Updated AnnData object with declared `.obs[cluster_key]`.
- Parameter/provenance record linking labels to `neighbors_key`.
- Cluster-size table and optional sample/batch/condition cross-tabulations.
- Optional diagnostic plots from `09_embedding_visualization` that display the
  cluster labels, if an embedding already exists or is separately approved.

## Validation Checks

- Confirm `.uns[neighbors_key]` exists and points to a valid connectivity
  matrix.
- Confirm `.obs[cluster_key]` is new or replacement is approved.
- Confirm labels have one value per cell and are categorical or safely
  castable to categorical.
- Confirm every cluster has a nonzero cell count; flag very small clusters for
  review.
- Confirm cluster counts, resolution, random seed, graph key, and method flavor
  are recorded.
- Confirm rerunning a resolution comparison changes only approved cluster keys
  and associated metadata.

## Failure Modes

- Overclustering that splits continuous states, sample-specific artifacts, or
  tiny unstable groups.
- Underclustering that merges distinct cell types or states.
- Batch-, donor-, chemistry-, or QC-driven clusters caused by the graph rather
  than biology.
- Non-reproducible labels from changed random seed, implementation, or graph.
- Key collisions that overwrite curated labels or previous parameter sweeps.
- Missing Leiden dependencies in the runtime environment.

## Allowed Claims

- The specified graph clustering method assigned community labels under the
  recorded parameters.
- Cluster counts and metadata cross-tabs describe the label distribution.
- Clusters can be used as groups for downstream marker ranking and annotation
  support after caveats are retained.

## Forbidden Claims

- Clusters are final cell types, disease states, lineages, or treatment effects
  without independent marker/reference/design evidence.
- Resolution optimization is objective without a declared criterion.
- Small clusters are biologically meaningful without stability and QC review.
- Cluster-level marker ranking is replicate-aware condition-level differential
  expression.

## Next Stage Routing

- Route to `11_marker_ranking` for descriptive marker ranking with declared
  expression source and group key.
- Route to `12_annotation_support` to compare clusters against marker genes,
  references, and expert labels.
- Route to `09_embedding_visualization` to display labels on an existing or
  separately approved embedding.
- Route back to `08_neighbor_graph`, `07_batch_integration`, or upstream state
  inspection if clusters are driven by unsuitable graph state or confounders.
