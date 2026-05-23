---
id: scrna.scverse.tool.scanpy_pca
kind: tool_ref
package_ref: scrna.scverse.package.scanpy
api_entrypoint: scanpy.pp.pca
method_family: dimensionality_reduction
source_urls: [https://scanpy.readthedocs.io/en/stable/generated/scanpy.pp.pca.html]
source_version: scanpy 1.11.5 local runtime; stable generated docs archived locally
source_accessed_at: 2026-05-23
source_local_paths: [BioBrain/reference/scverse_docs/scanpy_docs/scanpy.readthedocs.io/en/stable/generated/scanpy.pp.pca.html]
distillation_status: distilled
state_in: [expression_matrix, feature_mask_key]
state_out: [representation_key]
parameters: [n_comps, layer, obsm, zero_center, svd_solver, chunked, chunk_size, random_state, return_info, mask_var, use_highly_variable, dtype, key_added, copy]
caveats: [do_not_hide_pca_inside_neighbor_graph_stage]
compatible_adapters: [snakemake, python_script, ipython_notebook]
---
# scanpy.pp.pca

## API Entry Point

`scanpy.pp.pca(data, n_comps=None, *, layer=None, obsm=None, zero_center=True, svd_solver=None, chunked=False, chunk_size=None, random_state=0, return_info=False, mask_var=_empty, use_highly_variable=None, dtype='float32', key_added=None, copy=False)`

Use this API to compute a declared low-dimensional representation after
normalization and feature-selection decisions are explicit.

## Method Family

Dimensionality reduction for graph construction, integration inputs, and
diagnostic review.

## Required Object State

- AnnData has a declared expression source, typically normalized/log expression.
- A declared feature mask exists in `.var`, or the user explicitly approves PCA
  over all retained genes.
- The selected feature count and cell count can support the requested
  `n_comps`.
- The output representation key is declared and checked for collisions.

## Output State

- With default output settings, Scanpy stores scores in `obsm["X_pca"]`,
  loadings in `varm["PCs"]`, and variance metadata in `uns["pca"]`.
- With `key_added`, the representation, loadings, and metadata use the declared
  custom key according to Scanpy's output policy.
- Provenance records expression source, `mask_var` or feature-mask decision,
  selected feature count, `n_comps`, solver/chunking parameters, random state,
  and representation key.

## Important Parameters

- `n_comps`: number of components. The default is Scanpy-defined, but this
  repository should record the effective value.
- `layer`: named expression layer to use instead of `.X`; missing layers must
  fail.
- `mask_var`: preferred way to provide a boolean feature mask or `.var` key.
- `use_highly_variable`: deprecated in Scanpy in favor of `mask_var`; if used,
  record why and what mask it resolved to.
- `key_added`: output representation key. `None` means the default `X_pca`,
  `PCs`, and `pca` keys.
- `zero_center`, `svd_solver`, `chunked`, and `chunk_size`: algorithm and memory
  controls that affect performance and sometimes numerical behavior.
- `random_state`: seed-like value for stochastic solver paths; record it for
  reproducibility.
- `dtype`: output dtype, commonly `float32`.

## Minimal Use

The approved operation should follow this semantic sequence:

1. Confirm the expression source exists and is in the intended state.
2. Confirm the feature mask exists or record the decision to use all retained
   genes.
3. Check that `n_comps` is valid for the number of cells and selected features.
4. Compute PCA into the declared `representation_key`.
5. Record expression source, feature mask, selected feature count, `n_comps`,
   random state, solver/chunking policy, and output keys.

This reference intentionally does not define a reusable wrapper.

## Validation Checks

- Expression source exists and has one row per cell.
- Feature mask exists, is boolean-like, and selects at least one gene unless the
  all-genes policy is explicitly recorded.
- Requested `n_comps` is less than or equal to the valid component limit for the
  selected matrix shape.
- Output representation exists in `.obsm` and has shape
  `(adata.n_obs, effective_n_comps)`.
- Loadings and variance metadata exist in the expected keys when produced.
- No neighbor graph, embedding, cluster labels, or marker results were created.
- Provenance records the `representation_key`, feature mask, and PCA
  parameters.

## Failure Modes

- Feature mask missing, empty, or stored under an unexpected key.
- PCA silently uses all genes because the intended mask key was absent.
- `n_comps` is too large for the selected cell/feature dimensions.
- Existing `X_pca`, `PCs`, or `pca` keys are overwritten without approval.
- Large sparse, dense, dask, or backed matrices exceed memory for the chosen
  solver or chunking policy.
- PCs are dominated by QC covariates, library size, batch, or cell-cycle signal.

## Statistical Caveats

- PCA is a linear representation of the selected matrix; it is not biological
  annotation and does not correct batch effects by itself.
- Feature selection, scaling choices, solver settings, and normalization state
  can change PCs and downstream graphs.
- Explained variance is a diagnostic aid, not proof that selected PCs capture
  the biological signal of interest.
- PCA is common for scRNA graph construction, but model-derived or specialized
  representations can be more appropriate for some analyses.

## Adapter Notes

- Adapters should pass explicit expression source, feature-mask key,
  `n_comps`, `random_state`, and `representation_key`.
- Adapters should fail on missing masks or key collisions unless an explicit
  all-genes or overwrite policy exists.
- Reports should include output keys, representation shape, selected feature
  count, explained variance summary, and Scanpy version.
- Keep PCA separate from neighbor graph, embedding, integration, clustering, and
  marker-ranking steps.

## Sources Used

- Public docs: `https://scanpy.readthedocs.io/en/stable/generated/scanpy.pp.pca.html`.
- Local archive: `BioBrain/reference/scverse_docs/scanpy_docs/scanpy.readthedocs.io/en/stable/generated/scanpy.pp.pca.html`.
- Runtime version observed in the scverse tutorial environment: `scanpy 1.11.5`.
