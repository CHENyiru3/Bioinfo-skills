---
id: scrna.scverse.tool.scanpy_get_aggregate
kind: tool_ref
package_ref: scrna.scverse.package.scanpy
api_entrypoint: scanpy.get.aggregate
method_family: aggregation
source_urls: [https://scanpy.readthedocs.io/en/stable/generated/scanpy.get.aggregate.html]
source_version: scanpy stable docs with viewcode 1.12.1; local runtime records scanpy 1.11.5
source_accessed_at: 2026-05-23
source_local_paths: [BioBrain/reference/scverse_docs/scanpy_docs/scanpy.readthedocs.io/en/stable/generated/scanpy.get.aggregate.html, BioBrain/reference/scverse_docs/scanpy_docs/scanpy.readthedocs.io/en/stable/_sources/generated/scanpy.get.aggregate.rst]
distillation_status: distilled
state_in: [AnnData, grouping_columns, declared_matrix_source]
state_out: [aggregated_AnnData]
parameters: [by, func, axis, mask, dof, layer, obsm, varm]
caveats: [aggregation_is_not_a_de_model_by_itself, pseudobulk_requires_sample_level_replicates, condition_only_grouping_invalid_for_de]
compatible_adapters: [snakemake, python_script, ipython_notebook]
---
# scanpy.get.aggregate

## API Entry Point

`scanpy.get.aggregate(adata, by, func, *, axis=None, mask=None, dof=1,
layer=None, obsm=None, varm=None)`

## Method Family

Aggregation and pseudobulk preparation. The function groups an AnnData matrix
by categorical metadata and computes summary metrics into a new AnnData object.
It can prepare pseudobulk counts when used with raw counts and sample-level
grouping, but it is not a differential expression model.

## Required Object State

- `adata` is an AnnData object with grouping columns in `.obs` when aggregating
  observations.
- `by` names one or more existing categorical or safely castable grouping
  columns.
- For pseudobulk DE preparation, `by` includes `sample_id` and, when relevant,
  a cell group key such as annotation or cluster. Aggregating by condition alone
  is not valid for replicate-aware DE.
- A matrix source is declared. If `layer`, `obsm`, and `varm` are all omitted,
  Scanpy aggregates `.X`.
- For count-based DE, the selected source must contain raw non-negative counts
  and `func="sum"` should be used for the count matrix.
- Sample-level condition and covariate metadata are available for downstream
  modeling.

## Output State

- Returns a new aggregated AnnData object.
- Grouping columns are represented in the aggregated `.obs`.
- The aggregated `.obs` includes `n_obs_aggregated`, the number of original
  observations in each group.
- Each requested metric in `func` is written as a layer of the output object,
  such as `layers["sum"]`, `layers["mean"]`, or `layers["count_nonzero"]`.
- Combinations of grouping levels absent from the original data are not
  represented in the output.
- No DE statistics, p-values, model coefficients, or contrasts are produced by
  this function.

## Important Parameters

- `by`: grouping column name or collection of names.
- `func`: aggregation metric or metrics. Documented metrics include `sum`,
  `mean`, `median`, `var`, and `count_nonzero`.
- `axis`: axis on which to find the grouping column; for standard cell
  aggregation use observation grouping.
- `mask`: optional boolean mask or key to apply along the selected axis.
- `dof`: degrees of freedom used for variance aggregation.
- `layer`: named layer to aggregate instead of `.X`.
- `obsm` and `varm`: named multidimensional annotations to aggregate instead of
  the main matrix source.

## Minimal Use

```python
import scanpy as sc

pseudobulk = sc.get.aggregate(
    adata,
    by=["sample_id", "cell_type"],
    func="sum",
    layer="counts",
)
```

For condition-level DE, wrappers should align `pseudobulk.obs` to a separate
sample/design table and then route the count matrix to an approved
replicate-aware DE model.

## Validation Checks

- Confirm every `by` column exists and has no unhandled missing values.
- Confirm `sample_id` is included when the output is intended for pseudobulk
  condition-level DE.
- Reject condition-only aggregation for DE because it removes biological
  replicate variation.
- Confirm the requested `layer`, `obsm`, or `varm` key exists; otherwise record
  explicit `.X` use.
- Confirm the selected count source is raw, non-negative, and count-like when
  the output will feed a count-based DE engine.
- Confirm `func="sum"` is used for count-based pseudobulk matrices.
- Report `n_obs_aggregated`, dropped group combinations, library sizes, and
  replicate counts per condition.
- Confirm the aggregated object can be joined unambiguously to sample-level
  condition and covariate metadata.

## Failure Modes

- Aggregating log-normalized expression and treating it as raw counts in a DE
  model.
- Grouping by condition instead of sample, which destroys replicate-level
  variance.
- Missing or inconsistent sample metadata prevents design alignment.
- Sparse groups with too few cells produce unstable pseudobulk profiles.
- Absent grouping combinations are silently unavailable unless reported.
- Layer or matrix-source ambiguity causes the wrong expression values to be
  aggregated.
- Duplicate sample-condition mappings or many-to-many joins corrupt the design
  table.

## Statistical Caveats

- Aggregation summarizes observations; it does not test a hypothesis.
- Pseudobulk condition-level DE requires biological replicates, raw counts,
  design metadata, and a downstream statistical model.
- Sample, donor, batch, chemistry, and condition confounding cannot be repaired
  by aggregation.
- Within-cell-type pseudobulk results inherit uncertainty from the annotation or
  clustering used as the group key.
- Aggregated expression changes can reflect composition, quality, or capture
  differences unless the design and QC checks address them.

## Adapter Notes

- Execution adapters should call an approved wrapper that validates grouping,
  matrix source, and design alignment before aggregation.
- The wrapper should produce pseudobulk counts, aggregation metadata, cell-count
  summaries, and sample/design tables, but should not invent a DE model.
- Keep aggregation artifacts separate from DE result artifacts.
- Record grouping columns, `func`, matrix source, dropped combinations, and
  Scanpy version.
- For downstream DE, adapters should pass the `sum` count layer and aligned
  design table to the approved replicate-aware DE tool.

## Sources Used

- Public Scanpy docs for `scanpy.get.aggregate`:
  `https://scanpy.readthedocs.io/en/stable/generated/scanpy.get.aggregate.html`.
- Local archive paths listed in frontmatter were used as supporting source
  material; this ref is intended to remain usable without those folders.
