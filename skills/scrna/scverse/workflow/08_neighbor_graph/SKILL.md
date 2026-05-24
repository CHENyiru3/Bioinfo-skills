---
id: scrna.scverse.workflow.neighbor_graph
schema_version: "0.1.0"
kind: skill
domain: scrna
stage: neighbor_graph
status: filled
state_in: ["declared representation_key or approved graph-producing integration output"]
state_out: ["neighbors_key, distances_key, connectivities_key"]
registered_refs: [scrna.scverse.package.scanpy, scrna.scverse.package.rapids_singlecell, scrna.scverse.tool.scanpy_neighbors]
validation: [backend_neutral, state_contract_checked]
---
# Neighbor Graph

## Purpose

Construct a declared nearest-neighbor graph from an existing representation so
embedding, graph clustering, and graph diagnostics operate on the same
approved cell-cell relationship model.

## When Required

- Before UMAP, Leiden, Louvain, diffusion graph diagnostics, or graph-based
  trajectory methods that consume a neighbor graph.
- When changing the representation, distance metric, number of neighbors, or
  integration-derived graph used by downstream graph steps.
- When an existing graph key is missing, stale, overwritten, or derived from
  an unapproved representation.

## When Optional

- If a previous approved graph-producing integration step already wrote a
  named neighbor graph with usable connectivities and recorded provenance.
- If the requested downstream task only inspects existing embeddings or labels
  and does not claim they should be recomputed.
- If using a package-specific graph object outside AnnData, provided the
  next stage can consume that object explicitly.

## When Forbidden

- Do not run this stage to hide missing PCA, normalization, HVG selection, or
  batch integration decisions.
- Do not silently fall back to high-dimensional `.X` when a declared
  `representation_key` such as `X_pca` is expected.
- Do not overwrite an existing graph unless the user explicitly approves the
  same key; prefer a new `neighbors_key` for parameter comparisons.

## Required Input State

- AnnData object with observations representing cells and a declared
  `representation_key`, usually `obsm["X_pca"]`, or an approved integrated
  representation such as `obsm["X_scVI"]` or `obsm["X_pca_harmony"]`.
- Representation dimensions must be compatible with the requested `n_pcs`
  or explicitly set to use all dimensions of the chosen representation.
- Cell order, filtering state, and upstream provenance must be current for
  the AnnData object being mutated.
- If reusing an integration graph, the graph metadata must identify the
  connectivities and distances keys it owns.

## Produced Output State

- A declared `neighbors_key` in `.uns`, for example `.uns["neighbors"]` or
  `.uns["neighbors_pca_15"]`.
- Sparse distance and connectivity matrices in `.obsp`, keyed by the
  neighbor metadata, for example `.obsp["distances"]` and
  `.obsp["connectivities"]` or key-prefixed variants.
- Provenance recording representation, `n_neighbors`, `n_pcs` or dimensions
  used, metric, random state, graph method, package, and runtime version.
- No normalization, HVG selection, PCA, clustering, annotation, or marker
  ranking output should be produced by this stage.

## User Decision Points

- Which representation to use (`X_pca`, integrated embedding, or other named
  `.obsm` key).
- `neighbors_key`, especially when comparing graphs from multiple
  representations or parameter sets.
- `n_neighbors`, where smaller values emphasize local neighborhoods and
  larger values smooth toward broader manifold structure.
- `n_pcs` or dimensional span, and whether a non-PCA representation should
  ignore `n_pcs`.
- Distance metric and graph connectivity method.
- Random seed and approximate-neighbor backend when reproducibility or scale
  matters.

## Registered Package Refs

- `scrna.scverse.package.scanpy`
- `scrna.scverse.package.rapids_singlecell`

## Registered Tool Refs

- `scrna.scverse.tool.scanpy_neighbors`

## Expected Artifacts

- Updated AnnData object with declared neighbor graph keys.
- Parameter/provenance record stating the representation and graph settings.
- Optional graph diagnostics such as cell count, matrix shape, nonzero counts,
  component count, and warnings for isolated cells or disconnected components.

## Validation Checks

- Confirm `representation_key` exists and has one row per cell.
- Confirm requested `n_pcs` does not exceed available representation
  dimensions.
- Confirm the produced `.uns[neighbors_key]` points to existing `.obsp`
  distance and connectivity matrices.
- Confirm graph matrices are square with shape `n_obs x n_obs`, sparse, finite,
  and nonempty.
- Confirm existing graph keys are not overwritten unless approved.
- Confirm provenance records representation, metric, `n_neighbors`, seed, and
  output keys.

## Failure Modes

- Missing representation or accidental fallback to `.X`.
- `n_pcs` exceeds available components or mismatches non-PCA embeddings.
- Disconnected graphs, isolated cells, or very small components from overly
  strict neighborhood settings.
- Batch-, donor-, or library-size-driven neighborhoods caused by inadequate
  upstream correction or confounded design.
- Non-reproducible approximate-neighbor output when seed and implementation
  are not fixed.
- Memory or runtime failures on large datasets without a scalable backend.

## Allowed Claims

- The declared graph was constructed from the named representation with stated
  parameters.
- Downstream embedding and clustering can use this graph key.
- Graph diagnostics can flag connectivity, isolation, or gross batch-mixing
  concerns for review.

## Forbidden Claims

- The graph proves true biological lineages, cell types, or condition effects.
- Neighbor relationships are statistically independent observations.
- UMAP or clustering results are valid if they were produced from an
  undeclared or stale graph.
- Batch mixing is solved merely because a graph exists.

## Next Stage Routing

- Route to `09_embedding_visualization` to compute or refresh diagnostic
  embeddings from this `neighbors_key`.
- Route to `10_clustering` to assign graph communities from this
  `neighbors_key`.
- Route to `15_trajectory_fate_velocity` only after confirming trajectory
  assumptions and any package-specific graph requirements.
- Route back to `06_dimensionality_reduction` or `07_batch_integration` if the
  representation is missing, unsuitable, or biologically confounded.
