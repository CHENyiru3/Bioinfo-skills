# scrna_graph_clustering_m1 Specification

## Biological Intent

Build a graph-clustering section for an AnnData object that already has a
declared representation. The section constructs neighbors, computes UMAP
coordinates from that graph, and assigns Leiden graph communities.

## Required Input State

- The input is an AnnData `.h5ad` with nonzero observations and variables.
- `obsm["X_pca"]` exists and has one row per observation.
- The section does not compute normalization, feature selection, PCA, or batch
  integration.
- Existing graph, embedding, or cluster keys are not overwritten unless
  `overwrite` is explicitly approved.

## Produced Output State

- `.uns["neighbors_x_pca"]` with neighbor graph metadata.
- `.obsp["neighbors_x_pca_distances"]` and
  `.obsp["neighbors_x_pca_connectivities"]`.
- `.obsm["X_umap_neighbors_x_pca"]`.
- `.obs["leiden_neighbors_x_pca"]`.
- Wrapper provenance and sidecar artifacts for parameters, versions, embedding,
  cluster sizes, and execution log.

## Tool Binding

- Pack: `scrna.scverse.core`
- Workflow: `bioinfo.sdd.workflow.section_default.v0`
- Task: `scrna.scverse.task.graph_clustering.v0`
- Installed bundle: `scrna.scverse.bundle.scanpy_graph_clustering.v0`
- Package: `scrna.scverse.package.scanpy`
- `scrna.scverse.tool.scanpy_neighbors`
- `scrna.scverse.tool.scanpy_umap`
- `scrna.scverse.tool.scanpy_leiden`

## Allowed Claims

- Neighbor graph was constructed from the declared representation.
- UMAP coordinates were computed from the declared graph.
- Leiden graph communities were assigned under recorded parameters.
- Cluster-size summaries correspond to the declared cluster key.

## Forbidden Claims

- Cell type annotation.
- Condition-level inference.
- Normalization, feature selection, or PCA computation.
- Final biological interpretation of the clusters.

## Review Gate

`spec_review` is approved for implementation of this bounded section.
