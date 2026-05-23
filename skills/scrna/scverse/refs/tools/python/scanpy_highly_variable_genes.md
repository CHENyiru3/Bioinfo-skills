---
id: scrna.scverse.tool.scanpy_highly_variable_genes
kind: tool_ref
package_ref: scrna.scverse.package.scanpy
api_entrypoint: scanpy.pp.highly_variable_genes
method_family: feature_selection
source_urls: [https://scanpy.readthedocs.io/en/stable/generated/scanpy.pp.highly_variable_genes.html]
source_version: scanpy 1.11.5 local runtime; stable generated docs archived locally
source_accessed_at: 2026-05-23
source_local_paths: [BioBrain/reference/scverse_docs/scanpy_docs/scanpy.readthedocs.io/en/stable/generated/scanpy.pp.highly_variable_genes.html]
distillation_status: distilled
state_in: [normalized_or_count_expression]
state_out: [feature_mask_key]
parameters: [layer, n_top_genes, min_disp, max_disp, min_mean, max_mean, span, n_bins, flavor, subset, inplace, batch_key, filter_unexpressed_genes, check_values]
caveats: [flavor_requires_correct_count_or_log_state]
compatible_adapters: [snakemake, python_script, ipython_notebook]
---
# scanpy.pp.highly_variable_genes

## API Entry Point

`scanpy.pp.highly_variable_genes(adata, *, layer=None, n_top_genes=None, min_disp=0.5, max_disp=inf, min_mean=0.0125, max_mean=3, span=0.3, n_bins=20, flavor='seurat', subset=False, inplace=True, batch_key=None, filter_unexpressed_genes=None, check_values=True)`

Use this API to compute highly variable gene metrics and a declared feature
mask. The default behavior writes metrics into `.var`; physical subsetting is
controlled by `subset` and should remain disabled unless explicitly approved.

## Method Family

Feature selection before PCA, graph construction, and related dimensionality
reduction steps.

## Required Object State

- For `flavor="seurat"` and `flavor="cell_ranger"`, the selected expression
  source is logarithmized normalized data.
- For `flavor="seurat_v3"` and `flavor="seurat_v3_paper"`, the selected
  expression source is raw counts and `n_top_genes` is required.
- If `batch_key` is provided, that key exists in `.obs` and represents an
  approved batch or sample grouping for HVG merging.
- The gene axis is nonempty and contains enough expressed genes for the chosen
  thresholds.

## Output State

- With `inplace=True`, Scanpy writes a boolean `adata.var["highly_variable"]`
  mask and flavor-dependent metrics.
- Dispersion-based flavors can write means, dispersions, and normalized
  dispersions.
- `seurat_v3`-style flavors can write variances, normalized variances, ranks,
  and batch-aware fields when `batch_key` is used.
- This repository treats the resulting mask as the declared
  `feature_mask_key`; if a nondefault semantic key is needed, the implementation
  must record how the mask was mapped.

## Important Parameters

- `flavor`: one of `seurat`, `cell_ranger`, `seurat_v3`, or
  `seurat_v3_paper`; record the value because it controls count/log
  expectations and ranking behavior.
- `layer`: expression layer to use instead of `.X`; missing layers must fail.
- `n_top_genes`: number of HVGs to select; mandatory for `seurat_v3` flavors and
  often preferred for reproducibility.
- `batch_key`: optional `.obs` column for selecting HVGs per batch and merging
  results; record the key even when `None`.
- `subset`: default `False`; setting it to `True` physically drops non-HVGs and
  requires explicit approval.
- `min_mean`, `max_mean`, `min_disp`, and `max_disp`: threshold controls for
  dispersion-based selection when `n_top_genes` is not used.
- `check_values`: integer-count warning check used for `seurat_v3` flavors.

## Minimal Use

The approved operation should follow this semantic sequence:

1. Confirm the chosen expression source matches the selected flavor.
2. Confirm `batch_key` exists when requested.
3. Run HVG selection with `subset=False` unless feature dropping is separately
   approved.
4. Treat the produced mask as the declared `feature_mask_key`.
5. Record flavor, expression source, `n_top_genes` or thresholds, `batch_key`,
   selected-gene count, and subsetting policy.

This reference intentionally does not define a reusable wrapper.

## Validation Checks

- Expression source exists and satisfies the flavor-specific count/log
  requirement.
- `batch_key` is either absent by design or present in `.obs`.
- `adata.var["highly_variable"]` or the declared mapped mask exists after
  selection and is boolean-like.
- Selected HVG count is greater than zero and no larger than `adata.n_vars`.
- `subset=False` unless a provenance record explicitly authorizes physical gene
  dropping.
- Provenance records flavor, `batch_key`, expression source, thresholds or
  `n_top_genes`, and output mask key.

## Failure Modes

- Log-normalized data are used with a count-based `seurat_v3` flavor.
- Raw counts are used with a dispersion-based flavor that expects log data.
- `scikit-misc` is missing for `seurat_v3`-style flavors.
- `batch_key` is missing, confounded with condition, or contains undersized
  groups.
- Thresholds select zero or too many genes for the intended PCA.
- Existing HVG metrics are overwritten without an explicit policy.

## Statistical Caveats

- HVG selection is not marker discovery and does not assign cell identity.
- Batch-aware HVG merging is not batch correction or integration.
- HVGs can be dominated by QC effects, cell cycle, dissociation stress,
  mitochondrial content, ribosomal genes, or technical batch.
- Removing non-HVGs can discard genes needed for marker ranking, signature
  scoring, or targeted biology.
- The selected flavor changes the scientific and computational assumptions;
  comparisons across flavors should be interpreted cautiously.

## Adapter Notes

- Adapters should require explicit `flavor`, expression source, `batch_key`, and
  output mask policy.
- Adapters should fail rather than silently switching between count and log
  layers.
- Reports should include selected-gene count, flavor, `batch_key`, expression
  source, and whether physical subsetting occurred.
- Keep this operation separate from normalization, PCA, graph construction, and
  clustering.

## Sources Used

- Public docs: `https://scanpy.readthedocs.io/en/stable/generated/scanpy.pp.highly_variable_genes.html`.
- Local archive: `BioBrain/reference/scverse_docs/scanpy_docs/scanpy.readthedocs.io/en/stable/generated/scanpy.pp.highly_variable_genes.html`.
- Runtime version observed in the scverse tutorial environment: `scanpy 1.11.5`.
