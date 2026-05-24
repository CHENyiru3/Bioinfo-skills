---
id: scrna.scverse.tool.scanpy_neighbors
kind: tool_ref
package_ref: scrna.scverse.package.scanpy
api_entrypoint: scanpy.pp.neighbors
method_family: neighbor_graph
state_in: [representation_key]
state_out: [neighbors_key]
parameters: [n_neighbors, n_pcs, use_rep, knn, method, transformer, metric, metric_kwds, random_state, key_added, copy]
caveats: [avoid_accidental_X_fallback, key_multiple_graphs]
compatible_adapters: [snakemake, python_script, ipython_notebook]
source_urls: [https://scanpy.readthedocs.io/en/1.11.x/api/generated/scanpy.pp.neighbors.html]
source_version: scanpy 1.11.x public docs; local runtime observed scanpy 1.11.5
source_accessed_at: 2026-05-23
source_local_paths: [BioBrain/reference/scverse_docs/scanpy_docs/scanpy.readthedocs.io/en/stable/api/generated/scanpy.pp.neighbors.html, BioBrain/reference/scverse_docs/scanpy_docs/scanpy.readthedocs.io/en/stable/_sources/api/generated/scanpy.pp.neighbors.rst]
distillation_status: distilled
---
# scanpy.pp.neighbors

Construct a kNN/connectivity graph for UMAP, graph clustering, and graph-based
downstream methods.

## API Entry Point

`scanpy.pp.neighbors(adata, n_neighbors=15, n_pcs=None, *, use_rep=None,
knn=True, method="umap", transformer=None, metric="euclidean",
metric_kwds=mappingproxy({}), random_state=0, key_added=None, copy=False)`

The function mutates `adata` by default and returns `None`; with `copy=True`
it returns a modified AnnData copy.

## Method Family

Neighbor graph construction from cells in a declared representation. The graph
contains distances and weighted connectivities used by UMAP, Leiden/Louvain,
PAGA-like summaries, and other graph-aware methods.

## Required Object State

- AnnData with `n_obs` cells.
- Declared representation in `.obsm[use_rep]` or explicit approval to use
  `.X`.
- If `use_rep` is a PCA key and `n_pcs` is set, the representation must have
  enough dimensions.
- Upstream normalization, HVG selection, PCA, or integration must already be
  complete when those choices are intended; this API should not be used to
  hide those stages.

## Output State

- With `key_added=None`, writes `.uns["neighbors"]`,
  `.obsp["distances"]`, and `.obsp["connectivities"]`.
- With `key_added="name"`, writes `.uns["name"]`,
  `.obsp["name_distances"]`, and `.obsp["name_connectivities"]`.
- The `.uns` metadata stores keys for the produced matrices and parameters
  needed by downstream tools.

## Important Parameters

- `use_rep`: required by this skill system unless the user explicitly approves
  `.X`; valid values include `"X"` or a key in `.obsm`.
- `n_pcs`: number of PCs to consume. Use only with a compatible PCA-like
  representation; `0` means use `.X` when `use_rep` is not set.
- `n_neighbors`: controls local versus broader graph structure. Very small
  values can fragment the graph; larger values can smooth rare states.
- `metric` and `metric_kwds`: distance definition. Keep consistent across
  compared graphs.
- `method`: connectivity model, usually `"umap"`; `"gauss"` is available for a
  diffusion-map style kernel.
- `transformer`: optional nearest-neighbor implementation. Fix the choice for
  reproducibility and document GPU or approximate search use.
- `random_state`: seed for stochastic approximate neighbor search paths.
- `key_added`: required when preserving multiple graphs or avoiding overwrite
  of default neighbor keys.

## Minimal Use

```python
import scanpy as sc

neighbors_key = "neighbors_pca_15"
sc.pp.neighbors(
    adata,
    use_rep="X_pca",
    n_neighbors=15,
    n_pcs=30,
    metric="euclidean",
    random_state=0,
    key_added=neighbors_key,
)
```

## Validation Checks

- `use_rep` exists in `adata.obsm` unless explicitly set to `"X"`.
- `adata.obsm[use_rep].shape[0] == adata.n_obs`.
- `n_pcs` is absent or no greater than the available representation
  dimensions.
- `.uns[neighbors_key]` exists and includes `connectivities_key` and
  `distances_key`.
- Referenced `.obsp` matrices exist, are square `n_obs x n_obs`, sparse,
  finite, and nonempty.
- Existing graph keys were not overwritten unless that was approved.

## Failure Modes

- Silent automatic representation choice can compute PCA or use `.X` when
  `use_rep` is omitted; wrappers should refuse this unless approved.
- Graph fragmentation or isolated cells from too few neighbors, over-filtered
  data, or poor representation quality.
- Batch-driven neighborhoods when upstream integration or design review was
  skipped.
- Memory or runtime pressure on large datasets with exact search.
- Incomparable downstream results when graph key, metric, seed, or backend
  differs between runs.

## Statistical Caveats

- The graph is a modeling choice, not observed biology.
- Neighbor edges are not independent samples and should not be treated as
  replicate-level evidence.
- Batch mixing or separation on a graph is diagnostic and must be interpreted
  with metadata and experimental design.
- Downstream clusters and embeddings inherit this graph's representation,
  metric, and parameter biases.

## Adapter Notes

- Adapters should pass an existing AnnData path and explicit parameter values;
  they should not add upstream preprocessing.
- Record `use_rep`, `n_pcs`, `n_neighbors`, `metric`, `method`,
  `random_state`, `key_added`, package version, and output matrix keys.
- Refuse to overwrite `.uns[neighbors_key]` or referenced `.obsp` keys unless
  the approved task says replacement is intended.
- For GPU or approximate search, record the implementation and runtime
  dependency because results and performance may differ.

## Sources Used

- Public API docs: `https://scanpy.readthedocs.io/en/1.11.x/api/generated/scanpy.pp.neighbors.html`.
- Local archive: `BioBrain/reference/scverse_docs/scanpy_docs/scanpy.readthedocs.io/en/stable/api/generated/scanpy.pp.neighbors.html`.
- Local source mirror: `BioBrain/reference/scverse_docs/scanpy_docs/scanpy.readthedocs.io/en/stable/_sources/api/generated/scanpy.pp.neighbors.rst`.
- Runtime version observed in the scverse tutorial environment: `scanpy 1.11.5`.
