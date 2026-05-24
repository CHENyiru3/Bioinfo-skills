---
id: scrna.scverse.tool.scanpy_umap
kind: tool_ref
package_ref: scrna.scverse.package.scanpy
api_entrypoint: scanpy.tl.umap
method_family: embedding_visualization
state_in: [neighbors_key]
state_out: [embedding_key]
parameters: [min_dist, spread, n_components, maxiter, alpha, gamma, negative_sample_rate, init_pos, random_state, a, b, method, key_added, neighbors_key, copy]
caveats: [embedding_is_diagnostic_not_primary_statistical_evidence]
compatible_adapters: [snakemake, python_script, ipython_notebook]
source_urls: [https://scanpy.readthedocs.io/en/1.11.x/generated/scanpy.tl.umap.html]
source_version: scanpy 1.11.x public docs; local runtime observed scanpy 1.11.5
source_accessed_at: 2026-05-23
source_local_paths: [BioBrain/reference/scverse_docs/scanpy_docs/scanpy.readthedocs.io/en/stable/generated/scanpy.tl.umap.html, BioBrain/reference/scverse_docs/scanpy_docs/scanpy.readthedocs.io/en/stable/_sources/generated/scanpy.tl.umap.rst]
distillation_status: distilled
---
# scanpy.tl.umap

Produce a graph-derived diagnostic embedding. Do not cluster on UMAP unless that
choice is explicitly approved.

## API Entry Point

`scanpy.tl.umap(adata, *, min_dist=0.5, spread=1.0, n_components=2,
maxiter=None, alpha=1.0, gamma=1.0, negative_sample_rate=5,
init_pos="spectral", random_state=0, a=None, b=None, method="umap",
key_added=None, neighbors_key="neighbors", copy=False)`

The function mutates `adata` by default and returns `None`; with `copy=True`
it returns a modified AnnData copy.

## Method Family

Graph-derived manifold embedding for visualization. Scanpy UMAP consumes a
neighbor graph and produces coordinates that summarize graph topology in a
small number of dimensions.

## Required Object State

- AnnData with `.uns[neighbors_key]` produced by an approved neighbor graph
  stage.
- `.uns[neighbors_key]` must identify a connectivity matrix in `.obsp`.
- Cell filtering state must match the graph; stale graphs after subsetting
  should be rebuilt or explicitly validated.
- Optional plot overlays must already exist in `.obs`, `.var`, `.raw`, `.X`,
  or declared layers before plotting is requested.

## Output State

- With `key_added=None`, writes `.obsm["X_umap"]` and `.uns["umap"]`.
- With `key_added="name"`, writes `.obsm["name"]` and `.uns["name"]`.
- Coordinates have shape `n_obs x n_components` and floating dtype.
- No cluster labels or marker statistics are produced by this API.

## Important Parameters

- `neighbors_key`: graph metadata key; keep it explicit to avoid visualizing
  the wrong graph.
- `key_added`: embedding output key. Use a unique key for parameter sweeps or
  graph comparisons.
- `min_dist` and `spread`: control visual compactness. Smaller `min_dist`
  creates tighter visual groups; larger values distribute cells more evenly.
- `n_components`: usually `2` for plots, but higher-dimensional embeddings are
  possible for approved downstream methods.
- `init_pos`: `"spectral"` by default; alternatives such as `"random"` or an
  `.obsm` key affect layout.
- `random_state`: required for reproducible stochastic optimization.
- `method`: `"umap"` is the standard implementation. `"rapids"` is deprecated
  in Scanpy 1.10+; prefer `rapids_singlecell.tl.umap` for GPU workflows.
- `a` and `b`: advanced curve-shape parameters; leave unset unless explicitly
  approved because Scanpy derives them from `min_dist` and `spread`.

## Minimal Use

```python
import scanpy as sc

embedding_key = "X_umap_neighbors_pca_15"
sc.tl.umap(
    adata,
    neighbors_key="neighbors_pca_15",
    min_dist=0.5,
    spread=1.0,
    random_state=0,
    key_added=embedding_key,
)
```

## Validation Checks

- `.uns[neighbors_key]` exists and points to a present `.obsp`
  connectivity matrix.
- Output `embedding_key` is new or overwrite was approved.
- `.obsm[embedding_key]` exists after execution and has shape
  `adata.n_obs x n_components`.
- Embedding values are finite and not all identical.
- Provenance records `neighbors_key`, `key_added`, `min_dist`, `spread`,
  `n_components`, `init_pos`, method, and random seed.

## Failure Modes

- Missing or stale graph key after filtering or concatenation.
- Visual layout changes caused by seed, initialization, implementation, graph,
  or UMAP parameter changes.
- Misleading apparent islands from graph fragmentation, overcorrection, strong
  batch effects, QC gradients, or overplotting.
- Output key collision with prior embeddings from another graph.
- GPU method mismatch or deprecation if Scanpy's `"rapids"` path is requested.

## Statistical Caveats

- UMAP is a visualization of a graph optimization, not a hypothesis test.
- Distances, density, islands, and axis directions in UMAP space should not be
  interpreted as calibrated biological distances or effect sizes.
- Apparent separation by condition, sample, or batch requires follow-up with
  metadata-aware and replicate-aware analyses.
- Clustering should use the neighbor graph unless an explicit method decision
  justifies using embedding coordinates.

## Adapter Notes

- Adapters should require an existing `neighbors_key` and explicit
  `embedding_key`.
- Record UMAP parameters, graph key, seed, package version, and output key in
  provenance.
- Plotting overlays are separate artifacts; adapters should validate requested
  color variables before rendering.
- Preserve previous embeddings during parameter sweeps by varying `key_added`.

## Sources Used

- Public API docs: `https://scanpy.readthedocs.io/en/1.11.x/generated/scanpy.tl.umap.html`.
- Local archive: `BioBrain/reference/scverse_docs/scanpy_docs/scanpy.readthedocs.io/en/stable/generated/scanpy.tl.umap.html`.
- Local source mirror: `BioBrain/reference/scverse_docs/scanpy_docs/scanpy.readthedocs.io/en/stable/_sources/generated/scanpy.tl.umap.rst`.
- Runtime version observed in the scverse tutorial environment: `scanpy 1.11.5`.
