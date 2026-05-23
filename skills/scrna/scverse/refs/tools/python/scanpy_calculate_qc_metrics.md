---
id: scrna.scverse.tool.scanpy_calculate_qc_metrics
kind: tool_ref
package_ref: scrna.scverse.package.scanpy
api_entrypoint: scanpy.pp.calculate_qc_metrics
method_family: qc_metrics
source_urls: [https://scanpy.readthedocs.io/en/stable/generated/scanpy.pp.calculate_qc_metrics.html]
source_version: scanpy 1.11.5 local runtime; stable generated docs accessed 2026-05-23
source_accessed_at: 2026-05-23
source_local_paths: [BioBrain/reference/scverse_docs/scanpy_docs/scanpy.readthedocs.io/en/stable/generated/scanpy.pp.calculate_qc_metrics.html, BioBrain/reference/scverse_docs/scanpy_docs/scanpy.readthedocs.io/en/stable/_sources/generated/scanpy.pp.calculate_qc_metrics.rst, bioinfo_tutorial/conda_env/lib/python3.11/site-packages/scanpy/preprocessing/_qc.py]
distillation_status: distilled
state_in: [raw_count_AnnData, declared_qc_var_masks]
state_out: [obs_qc_metrics, var_qc_metrics]
parameters: [expr_type, var_type, qc_vars, percent_top, layer, use_raw, inplace, log1p, parallel]
caveats: [organism_specific_qc_masks_required, percent_top_must_fit_feature_count, parallel_deprecated_no_effect]
compatible_adapters: [snakemake, python_script, ipython_notebook]
---
# scanpy.pp.calculate_qc_metrics

## API Entry Point

`scanpy.pp.calculate_qc_metrics(adata, *, expr_type='counts', var_type='genes', qc_vars=(), percent_top=(50, 100, 200, 500), layer=None, use_raw=False, inplace=False, log1p=True, parallel=None)`

Use this API to compute observation-level and variable-level QC metrics from a
declared matrix source. With `inplace=False`, it returns two tables. With
`inplace=True`, it writes metrics into `adata.obs` and `adata.var`.

## Method Family

Raw-count quality-control metric calculation before approved filtering.

## Required Object State

- AnnData has a declared count source for QC, usually `layers["counts"]` or an
  explicitly approved `.X`.
- The selected matrix has observations in rows and features in columns.
- Requested `qc_vars` already exist as boolean-like columns in `.var`.
- `percent_top` values are positive and no larger than the number of retained
  features.
- `layer` and `use_raw` are not both selected; the implementation raises an
  error if both are requested.
- Existing `.obs` and `.var` QC columns are checked before using
  `inplace=True`.

## Output State

- Observation-level metrics include detected-feature counts, total counts,
  optional log-transformed metric annotations, top-feature count percentages,
  and totals or percentages for requested QC variable masks.
- Variable-level metrics include detected-cell counts, mean counts, dropout
  percentage, total counts, and optional log-transformed metric annotations.
- Returned tables or in-place columns use names derived from `expr_type`,
  `var_type`, `qc_vars`, and `percent_top`.
- The expression matrix itself is not normalized, log-transformed, filtered, or
  subset by this function.

## Important Parameters

- `expr_type`: label embedded in metric names, defaulting to `counts`; use a
  value that matches the declared matrix state.
- `var_type`: label embedded in feature-count metric names, defaulting to
  `genes`.
- `qc_vars`: one mask key or a collection of `.var` mask keys used to compute
  per-cell totals and percentages for feature groups such as mitochondrial
  genes.
- `percent_top`: ranks of most highly expressed features used for cumulative
  percentage metrics; set to `None` or an empty collection to skip those
  metrics.
- `layer`: named `adata.layers[...]` source to use instead of `.X`; missing
  layers must fail rather than falling back silently.
- `use_raw`: use `adata.raw.X` instead of `.X`; do not combine with `layer`.
- `inplace`: if `True`, writes metrics to `.obs` and `.var`; if `False`,
  returns observation and variable metric tables.
- `log1p`: controls whether log-transformed metric annotations are computed; it
  does not apply `log1p` to the expression matrix.
- `parallel`: present in the API but deprecated in the observed local source
  and currently has no effect.

## Minimal Use

The approved operation should follow this semantic sequence:

1. Confirm the object has a declared raw-count source for QC.
2. Create or verify organism- and namespace-specific `.var` QC masks.
3. Choose exactly one matrix source: `.X`, `.raw`, or a named layer.
4. Choose `expr_type`, `var_type`, `qc_vars`, `percent_top`, and output policy.
5. Calculate metrics and write or export only the approved metric fields.
6. Record source key, mask keys, metric parameters, software version, and
   whether metrics were written in place.

This reference intentionally does not define threshold values or a reusable
wrapper.

## Validation Checks

- Confirm the selected matrix source exists and matches the declared count
  state.
- Confirm all `qc_vars` are present in `.var` and are boolean-like.
- Confirm each `percent_top` rank is greater than zero and less than or equal to
  the number of features.
- Confirm expected observation metrics are present after execution, such as
  total counts, detected-feature counts, and requested QC percentages.
- Confirm expected variable metrics are present after execution, such as
  detected-cell counts, mean counts, dropout percentage, and total counts.
- Confirm `log1p` metric columns, when present, are metric annotations only and
  not evidence that the expression matrix was transformed.
- Confirm raw counts remain present after metric calculation.
- Confirm no filtering occurred unless a separate filtering operation was
  approved and recorded.

## Failure Modes

- QC is calculated from normalized, log-transformed, scaled, or integrated data.
- Requested `qc_vars` are missing, non-boolean, or derived from the wrong
  organism or feature namespace.
- `percent_top` includes a rank outside the feature range, which can raise an
  index error.
- `layer` and `use_raw` are both requested.
- Existing `.obs` or `.var` metric columns are overwritten with `inplace=True`.
- Zero-count cells can produce undefined percentages for QC feature masks or
  top-feature proportions.
- Sparse or dense matrix shape and dtype choices can affect memory use; first
  calls may pay compilation overhead in the observed implementation.
- `parallel` is supplied with an expectation of speedup, but the observed local
  source treats it as deprecated and ineffective.

## Statistical Caveats

- QC metrics summarize technical properties; they do not define universal
  filtering thresholds.
- Mitochondrial, ribosomal, hemoglobin, ERCC, antibody, or other QC masks depend
  on organism, assay, chemistry, and feature identifiers.
- High mitochondrial percentage, low gene count, or high total counts can
  indicate multiple biological or technical states and require sample-aware
  review.
- Cell-level QC thresholds are not replicate-aware statistical tests and should
  not be interpreted as condition-level inference.
- QC metrics do not detect all doublets, ambient RNA effects, damaged cells, or
  batch effects.

## Adapter Notes

- Adapters should require explicit count source, `qc_vars`, `percent_top`, and
  output policy; they should not infer a count source from `.X`.
- Adapters should fail when a requested layer, `.raw`, or QC mask is missing.
- Reports should include Scanpy version, object shape, source key, mask keys,
  metric names, `percent_top`, and collision/overwrite decisions.
- Keep metric calculation separate from threshold selection and physical
  filtering so review artifacts can be inspected before subsetting.
- Threshold decisions should be recorded in the workflow-stage provenance, not
  hidden inside this tool reference.

## Sources Used

- Public docs: `https://scanpy.readthedocs.io/en/stable/generated/scanpy.pp.calculate_qc_metrics.html`.
- Local archive: `BioBrain/reference/scverse_docs/scanpy_docs/scanpy.readthedocs.io/en/stable/generated/scanpy.pp.calculate_qc_metrics.html`.
- Local source stub: `BioBrain/reference/scverse_docs/scanpy_docs/scanpy.readthedocs.io/en/stable/_sources/generated/scanpy.pp.calculate_qc_metrics.rst`.
- Local runtime source inspected for `layer`/`use_raw`, `percent_top`, and
  `parallel` behavior: `bioinfo_tutorial/conda_env/lib/python3.11/site-packages/scanpy/preprocessing/_qc.py`.
- Runtime version observed in the scverse tutorial environment: `scanpy 1.11.5`.
