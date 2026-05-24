---
id: scrna.scverse.tool.scanpy_leiden
kind: tool_ref
package_ref: scrna.scverse.package.scanpy
api_entrypoint: scanpy.tl.leiden
method_family: clustering
state_in: [neighbors_key]
state_out: [cluster_key]
parameters: [resolution, restrict_to, random_state, key_added, adjacency, directed, use_weights, n_iterations, partition_type, neighbors_key, obsp, copy, flavor, clustering_args]
caveats: [clusters_are_not_cell_types_without_marker_or_reference_evidence]
compatible_adapters: [snakemake, python_script, ipython_notebook]
source_urls: [https://scanpy.readthedocs.io/en/1.11.x/generated/scanpy.tl.leiden.html]
source_version: scanpy 1.11.x public docs; local runtime observed scanpy 1.11.5
source_accessed_at: 2026-05-23
source_local_paths: [BioBrain/reference/scverse_docs/scanpy_docs/scanpy.readthedocs.io/en/stable/generated/scanpy.tl.leiden.html, BioBrain/reference/scverse_docs/scanpy_docs/scanpy.readthedocs.io/en/stable/_sources/generated/scanpy.tl.leiden.rst]
distillation_status: distilled
---
# scanpy.tl.leiden

Assign graph communities for marker ranking and annotation support.

## API Entry Point

`scanpy.tl.leiden(adata, resolution=1, *, restrict_to=None, random_state=0,
key_added="leiden", adjacency=None, directed=None, use_weights=True,
n_iterations=-1, partition_type=None, neighbors_key=None, obsp=None,
copy=False, flavor="leidenalg", **clustering_args)`

The function mutates `adata` by default and returns `None`; with `copy=True`
it returns a modified AnnData copy.

## Method Family

Graph community detection using the Leiden algorithm. In the scRNA workflow it
assigns exploratory cell communities from a declared neighbor graph for later
marker ranking and annotation support.

## Required Object State

- AnnData with a valid graph connectivity matrix.
- Prefer explicit `neighbors_key`; when omitted, Scanpy uses the default
  `.obsp["connectivities"]` path from default neighbors.
- If using `obsp`, the named adjacency matrix must exist and cannot be
  provided together with `neighbors_key`.
- The intended `.obs[key_added]` cluster key must be new or explicitly
  approved for replacement.
- Runtime must provide the requested Leiden implementation dependencies,
  typically `leidenalg` or `igraph`.

## Output State

- Writes cluster labels to `.obs[key_added]` as a categorical series.
- Writes parameter metadata to `.uns[key_added]["params"]`, including
  resolution, random state, and iteration count.
- Does not compute markers, annotations, UMAP coordinates, or pseudobulk
  statistics.

## Important Parameters

- `neighbors_key`: graph metadata key. Keep explicit so labels can be traced to
  one graph.
- `key_added`: cluster label column. Use names such as
  `leiden_neighbors_pca_15_r1_0` for resolution comparisons.
- `resolution`: controls cluster granularity; higher values generally create
  more clusters, lower values fewer clusters.
- `random_state`: affects stochastic optimization and must be recorded.
- `use_weights`: uses graph edge weights by default; disabling changes the
  model and should be justified.
- `n_iterations`: `-1` runs until convergence; positive values cap iterations.
- `restrict_to`: reclusters a subset of categories from an existing `.obs`
  annotation and requires careful key naming.
- `flavor` and `partition_type`: choose implementation and partition model;
  changing them makes results non-comparable unless documented.

## Minimal Use

```python
import scanpy as sc

cluster_key = "leiden_neighbors_pca_15_r1_0"
sc.tl.leiden(
    adata,
    neighbors_key="neighbors_pca_15",
    resolution=1.0,
    random_state=0,
    key_added=cluster_key,
    flavor="leidenalg",
)
```

## Validation Checks

- `.uns[neighbors_key]` exists and points to a present connectivity matrix, or
  the approved `obsp`/`adjacency` input exists.
- `key_added` is absent from `.obs` or replacement was approved.
- `.obs[key_added]` exists after execution, has one value per cell, and is
  categorical or safely castable to categorical.
- Cluster-size table has nonzero counts and flags very small clusters for
  review.
- Provenance records graph key, resolution, seed, flavor, weights,
  iterations, package version, and output key.

## Failure Modes

- Missing neighbor graph or dependency packages.
- Labels written from the default graph when `neighbors_key` was omitted.
- Overclustering from high resolution or graph fragmentation.
- Underclustering from low resolution or over-smoothed graphs.
- Batch-, donor-, chemistry-, or QC-driven clusters inherited from the graph.
- Non-reproducible labels when graph, seed, Leiden flavor, or dependency
  versions change.
- Accidental overwrite of curated annotations or previous resolution sweeps.

## Statistical Caveats

- Leiden clusters are algorithmic graph communities, not automatically cell
  types or biological states.
- Resolution selection is subjective unless a criterion is declared in
  advance.
- Cluster marker ranking is descriptive and is not replicate-aware
  condition-level differential expression.
- Very small clusters need stability, QC, doublet, and metadata review before
  interpretation.

## Adapter Notes

- Adapters should require explicit `neighbors_key`, `key_added`, `resolution`,
  and `random_state`.
- Record cluster counts overall and, when metadata exists, by sample, batch,
  and condition.
- Preserve existing labels by writing new keys for resolution sweeps.
- Do not call graph construction, UMAP, marker ranking, or annotation inside a
  clustering adapter step.

## Sources Used

- Public API docs: `https://scanpy.readthedocs.io/en/1.11.x/generated/scanpy.tl.leiden.html`.
- Local archive: `BioBrain/reference/scverse_docs/scanpy_docs/scanpy.readthedocs.io/en/stable/generated/scanpy.tl.leiden.html`.
- Local source mirror: `BioBrain/reference/scverse_docs/scanpy_docs/scanpy.readthedocs.io/en/stable/_sources/generated/scanpy.tl.leiden.rst`.
- Runtime version observed in the scverse tutorial environment: `scanpy 1.11.5`.
