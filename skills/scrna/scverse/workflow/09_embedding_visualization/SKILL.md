---
id: scrna.scverse.workflow.embedding_visualization
schema_version: "0.1.0"
kind: skill
domain: scrna
stage: embedding_visualization
status: filled
state_in: ["declared neighbors_key"]
state_out: ["embedding_key and diagnostic plots"]
registered_refs: [scrna.scverse.package.scanpy, scrna.scverse.tool.scanpy_umap]
validation: [backend_neutral, state_contract_checked]
---
# Embedding And Visualization

## Purpose

Produce graph-derived low-dimensional coordinates and diagnostic visualizations
from a declared neighbor graph. The embedding is a visual summary for review,
not the source of clustering or primary statistical evidence unless a separate
method explicitly requires it and the user approves that choice.

## When Required

- When the user asks for UMAP or similar visual diagnostics from an approved
  graph.
- Before reporting visual summaries of clusters, samples, batches, QC metrics,
  annotations, signatures, or marker expression on an embedding.
- When a new graph or changed UMAP parameter set should create a new
  `embedding_key`.

## When Optional

- If the downstream task is clustering, marker ranking, pseudobulk DE, or
  tabular reporting and no visual diagnostic is needed.
- If a valid embedding from the same `neighbors_key` and parameters already
  exists and the user only asks to inspect or plot it.
- If an alternative visualization method is chosen and documented separately.

## When Forbidden

- Do not compute UMAP to replace missing graph construction.
- Do not cluster on UMAP coordinates without explicit user approval and a
  method-specific caveat.
- Do not compare biological distances or effect sizes directly from visual
  distances on the embedding.
- Do not overwrite existing embeddings during parameter exploration; write a
  new `embedding_key`.

## Required Input State

- AnnData object with `.uns[neighbors_key]` describing the neighbor graph.
- The neighbor metadata must point to a valid connectivity matrix in `.obsp`.
- Optional color/group keys in `.obs` or gene features must be declared before
  plotting so missing metadata can fail clearly.
- The graph provenance should identify the representation and parameters used
  to create the graph.

## Produced Output State

- A declared embedding in `.obsm`, commonly `obsm["X_umap"]` or a custom
  key such as `obsm["X_umap_neighbors_pca_15"]`.
- Embedding parameter metadata in `.uns`, keyed consistently with the
  embedding.
- Plot artifacts or report-ready figures only when requested, with plotted
  color variables and data source recorded.
- No cluster labels, cell-type labels, marker tables, normalization, or graph
  recomputation should be produced by this stage.

## User Decision Points

- Which `neighbors_key` to visualize.
- `embedding_key` and whether to preserve an existing embedding for comparison.
- UMAP parameters such as `min_dist`, `spread`, `n_components`, initialization,
  and random seed.
- Which metadata, cluster labels, QC metrics, batches, samples, or genes to
  overlay on plots.
- Whether the goal is qualitative diagnostic review, publication-ready figures,
  or input for another approved method.

## Registered Package Refs

- `scrna.scverse.package.scanpy`

## Registered Tool Refs

- `scrna.scverse.tool.scanpy_umap`

## Expected Artifacts

- Updated AnnData object with declared `.obsm[embedding_key]`.
- Parameter/provenance record linking the embedding to `neighbors_key`.
- Optional figure files or figure manifest with color variables, palette, point
  size policy, and expression source for gene overlays.
- Diagnostic summary noting cell count, embedding dimensions, seed, and any
  missing plot variables.

## Validation Checks

- Confirm `.uns[neighbors_key]` exists and references a present connectivity
  matrix.
- Confirm embedding shape is `n_obs x n_components` and values are finite.
- Confirm `embedding_key` does not overwrite an existing embedding unless
  approved.
- Confirm plotted `.obs` keys or genes exist before generating figures.
- Confirm the output provenance records `neighbors_key`, UMAP parameters,
  random seed, and embedding key.

## Failure Modes

- Stale or missing graph key, especially after filtering cells.
- Stochastic layout differences caused by changed seed, initialization, or
  implementation.
- Misleading apparent separation from overcorrection, undercorrection, strong
  QC gradients, donor effects, or cell-cycle effects.
- Overinterpretation of visual proximity or islands as discrete biology.
- Plot failures from missing metadata, too many categories, or mismatched gene
  identifiers.

## Allowed Claims

- The embedding visualizes the declared graph under stated UMAP parameters.
- Visual overlays can reveal patterns that should be checked with tabular,
  marker, metadata, or replicate-aware analyses.
- Repeated embeddings with recorded parameters can support qualitative
  sensitivity review.

## Forbidden Claims

- UMAP axis distances are primary statistical evidence.
- UMAP islands are validated cell types without marker or reference support.
- Batch mixing, trajectory, condition separation, or annotation quality is
  proven solely by visual appearance.
- Clusters should be computed from the embedding by default.

## Next Stage Routing

- Route to `10_clustering` when graph community labels are needed; use the
  `neighbors_key`, not the UMAP coordinates, unless explicitly approved.
- Route to `11_marker_ranking` only after valid group labels exist.
- Route to `12_annotation_support` when visualized clusters need biological
  interpretation with marker/reference evidence.
- Route back to `08_neighbor_graph` if the graph is stale or from the wrong
  representation.
