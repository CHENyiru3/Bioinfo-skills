---
id: scrna.scverse.tool.scanpy_rank_genes_groups
kind: tool_ref
package_ref: scrna.scverse.package.scanpy
api_entrypoint: scanpy.tl.rank_genes_groups
method_family: marker_ranking
source_urls: [https://scanpy.readthedocs.io/en/stable/generated/scanpy.tl.rank_genes_groups.html, https://scanpy.readthedocs.io/en/stable/generated/scanpy.get.rank_genes_groups_df.html, https://scanpy.readthedocs.io/en/stable/generated/scanpy.tl.filter_rank_genes_groups.html]
source_version: scanpy stable docs, copyright 2026; local runtime records scanpy 1.11.5
source_accessed_at: 2026-05-23
source_local_paths: [BioBrain/reference/scverse_docs/scanpy_docs/scanpy.readthedocs.io/en/stable/generated/scanpy.tl.rank_genes_groups.html, BioBrain/reference/scverse_docs/scanpy_docs/scanpy.readthedocs.io/en/stable/generated/scanpy.get.rank_genes_groups_df.html, BioBrain/reference/scverse_docs/scanpy_docs/scanpy.readthedocs.io/en/stable/generated/scanpy.tl.filter_rank_genes_groups.html]
distillation_status: distilled
state_in: [AnnData, groupby_obs_key, declared_expression_source, logarithmized_expression]
state_out: [adata_uns_marker_result_key, marker_dataframe]
parameters: [groupby, method, use_raw, layer, groups, reference, n_genes, rankby_abs, pts, key_added, corr_method, tie_correct, mask_var]
caveats: [descriptive_cluster_marker_ranking_not_condition_de, cells_are_not_independent_replicates, expects_logarithmized_data]
compatible_adapters: [snakemake, python_script, ipython_notebook]
---
# scanpy.tl.rank_genes_groups

## API Entry Point

`scanpy.tl.rank_genes_groups(adata, groupby, *, mask_var=None, use_raw=None,
groups='all', reference='rest', n_genes=None, rankby_abs=False, pts=False,
key_added=None, copy=False, method=None, corr_method='benjamini-hochberg',
tie_correct=False, layer=None, **kwds)`

Companion accessors:

- `scanpy.get.rank_genes_groups_df(adata, group, *, key='rank_genes_groups',
  pval_cutoff=None, log2fc_min=None, log2fc_max=None, gene_symbols=None)`
- `scanpy.tl.filter_rank_genes_groups(adata, *, key=None, groupby=None,
  use_raw=None, key_added='rank_genes_groups_filtered',
  min_in_group_fraction=0.25, min_fold_change=1,
  max_out_group_fraction=0.5, compare_abs=False)`

## Method Family

Cluster marker ranking for already-defined groups in `adata.obs`. This is a
descriptive marker discovery step, not replicate-aware condition-level
differential expression.

## Required Object State

- `adata` is an AnnData object with a declared `groupby` column in `adata.obs`.
- The selected groups contain cells and at least two groups are available for
  comparison.
- Expression source is declared as one of:
  - `use_raw=True` to use `adata.raw`.
  - `layer="..."` to use a named `adata.layers` matrix.
  - `use_raw=False` and `layer=None` to use `adata.X`.
- The selected expression source is expected to contain logarithmized data for
  Scanpy ranking.
- Gene IDs are in the selected matrix namespace. If display symbols are needed,
  pass a `.var` column name through `gene_symbols` when extracting tables.

## Output State

- With `copy=False`, Scanpy mutates `adata` in place and returns `None`.
- Results are stored under `adata.uns[key_added]` when `key_added` is supplied,
  otherwise under `adata.uns["rank_genes_groups"]`.
- Expected result fields include `names`, `scores`, `pvals`, and `pvals_adj`.
- `logfoldchanges` is available for t-test-like methods and is an approximation
  from mean log values.
- `pts` and, for `reference="rest"`, `pts_rest` are added when `pts=True`.
- `scanpy.get.rank_genes_groups_df` converts stored results to a pandas
  DataFrame for one group, a list of groups, or all groups with `group=None`.
- `scanpy.tl.filter_rank_genes_groups` writes a filtered result key and keeps
  the original result shape while setting filtered gene names to missing values.

## Important Parameters

- `groupby`: required `.obs` key defining groups to characterize.
- `method`: `None` defaults to `t-test`; allowed documented methods are
  `t-test`, `t-test_overestim_var`, `wilcoxon`, and `logreg`.
- `use_raw`: `None` uses `adata.raw` when present. For reproducible wrappers,
  prefer explicit `True` or `False` and record the expression source.
- `layer`: named `adata.layers` key to use. Do not combine an absent layer with
  silent fallback to `.X`.
- `groups`: `'all'` or a subset of group names. With `reference='rest'`, the
  reference still uses all remaining groups, not only the requested subset.
- `reference`: `'rest'` compares each group against all other cells; a specific
  group compares against that group.
- `n_genes`: number of ranked genes retained; `None` returns all genes.
- `corr_method`: `benjamini-hochberg` or `bonferroni`, used for t-test-like and
  Wilcoxon methods.
- `tie_correct`: applies Wilcoxon tie correction when `method='wilcoxon'`.
- `rankby_abs`: ranks by absolute score while returned scores keep their signs.
- `pts`: calculates fractions of cells expressing each gene.
- `key_added`: output key in `adata.uns`; required for implementations that
  must avoid overwriting previous marker results.
- `mask_var`: optional gene mask or `.var` key limiting tested genes.

## Minimal Use

```python
import scanpy as sc

marker_key = "rank_genes_groups_leiden_wilcoxon"
sc.tl.rank_genes_groups(
    adata,
    groupby="leiden",
    method="wilcoxon",
    reference="rest",
    use_raw=False,
    layer="log1p_norm",
    n_genes=100,
    pts=True,
    key_added=marker_key,
)
markers = sc.get.rank_genes_groups_df(adata, group=None, key=marker_key)
```

Implementation wrappers should add table metadata columns that Scanpy does not
add by itself, including `method`, `groupby`, `reference`, expression source,
`key_added`, software version, and group sizes.

## Validation Checks

- Confirm `groupby` exists in `adata.obs`.
- Report group names, group sizes, and missing-label counts before ranking.
- Fail if fewer than two non-empty groups are available.
- Confirm the requested `adata.raw` or `adata.layers[...]` source exists.
- Confirm `.X` use is explicit when `.raw` is present, because Scanpy defaults
  to `.raw` with `use_raw=None`.
- Record whether the selected source is known to be logarithmized; reject or
  require explicit override for raw counts.
- Confirm `key_added` is supplied or the default key overwrite is approved.
- After ranking, confirm the output key exists in `adata.uns` and contains
  `names` and `scores`.
- When exporting a DataFrame, confirm required metadata columns have been added
  by the wrapper or reporting layer.
- If filtering is used, keep both original and filtered result keys traceable.

## Failure Modes

- `groupby` is missing, has one populated category, or contains unexpected
  missing labels.
- Requested `adata.raw` or layer is missing.
- `use_raw=None` consumes `adata.raw` unexpectedly when the user intended `.X`.
- Input source contains raw counts or scaled values rather than log-expression.
- `logfoldchanges` is absent for `logreg` or is overinterpreted as exact fold
  change for log-expression inputs.
- Very small groups produce unstable rankings.
- Highly similar groups produce weak or non-specific markers.
- Existing `adata.uns` result keys can be overwritten if `key_added` is not
  controlled.
- Dense and sparse matrix paths may show slight numerical inconsistencies.

## Statistical Caveats

- Scanpy's own documentation warns that comparing cells inflates p-values
  because cells are not independent observations. Do not describe marker
  ranking p-values as sample-level inferential evidence.
- This function does not model donor, sample, batch, paired design, condition,
  or other experimental design terms.
- For condition-level differential expression, route to a guarded pseudobulk or
  other replicate-aware method using raw counts and sample metadata.
- Marker ranking can support annotation review, but a ranked gene list alone
  does not prove a cell type identity.
- Log fold changes are approximate for t-test-like methods and should be
  reported with the method and expression source.

## Adapter Notes

- Execution adapters should call an approved wrapper, not embed ad hoc analysis
  logic.
- The wrapper should perform no normalization, filtering, clustering,
  integration, or annotation.
- The wrapper should own only the declared `adata.uns[key_added]` marker result
  and exported marker/group-size artifacts.
- Output tables should be deterministic in ordering: group, rank, then gene.
- Store enough metadata for later provenance checks: group key, group sizes,
  method, correction method, reference, groups, expression source, result key,
  Scanpy version, and warning/caveat text.

## Sources Used

- Public Scanpy docs for `scanpy.tl.rank_genes_groups`:
  `https://scanpy.readthedocs.io/en/stable/generated/scanpy.tl.rank_genes_groups.html`.
- Public Scanpy docs for `scanpy.get.rank_genes_groups_df`:
  `https://scanpy.readthedocs.io/en/stable/generated/scanpy.get.rank_genes_groups_df.html`.
- Public Scanpy docs for `scanpy.tl.filter_rank_genes_groups`:
  `https://scanpy.readthedocs.io/en/stable/generated/scanpy.tl.filter_rank_genes_groups.html`.
- Local archive paths listed in frontmatter were used only as supporting source
  material; this ref is intended to remain usable without those folders.
