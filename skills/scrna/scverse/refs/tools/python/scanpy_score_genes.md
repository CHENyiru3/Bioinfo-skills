---
id: scrna.scverse.tool.scanpy_score_genes
kind: tool_ref
package_ref: scrna.scverse.package.scanpy
api_entrypoint: scanpy.tl.score_genes
method_family: signature_scoring
source_urls: [https://scanpy.readthedocs.io/en/stable/generated/scanpy.tl.score_genes.html]
source_version: scanpy stable docs with viewcode 1.12.1; local runtime records scanpy 1.11.5
source_accessed_at: 2026-05-23
source_local_paths: [BioBrain/reference/scverse_docs/scanpy_docs/scanpy.readthedocs.io/en/stable/generated/scanpy.tl.score_genes.html, BioBrain/reference/scverse_docs/scanpy_docs/scanpy.readthedocs.io/en/stable/_sources/generated/scanpy.tl.score_genes.rst]
distillation_status: distilled
state_in: [AnnData, declared_expression_source, validated_gene_set]
state_out: [adata_obs_score_key]
parameters: [gene_list, ctrl_as_ref, ctrl_size, gene_pool, n_bins, score_name, random_state, copy, use_raw, layer]
caveats: [signature_score_is_relative_not_causal_proof, control_gene_sampling_affects_values, not_marker_ranking_or_condition_de]
compatible_adapters: [snakemake, python_script, ipython_notebook]
---
# scanpy.tl.score_genes

## API Entry Point

`scanpy.tl.score_genes(adata, gene_list, *, ctrl_as_ref=True, ctrl_size=50,
gene_pool=None, n_bins=25, score_name='score', random_state=0, copy=False,
use_raw=None, layer=None)`

## Method Family

Signature scoring or module scoring for predefined gene sets. The function
summarizes expression of a declared gene list relative to sampled reference
genes with similar expression bins. It is not de novo marker ranking,
annotation by itself, or replicate-aware condition-level differential
expression.

## Required Object State

- `adata` is an AnnData object with observations to score.
- The expression source is declared as one of:
  - `use_raw=True` to use `adata.raw`.
  - `layer="..."` to use a named `adata.layers` matrix.
  - `use_raw=False` and `layer=None` to use `adata.X`.
- The selected source should be appropriate for expression scoring, usually
  normalized/log-transformed expression rather than raw counts or scaled
  residuals unless the user explicitly accepts that interpretation.
- `gene_list` has been checked against the selected feature namespace.
- `gene_pool`, if supplied, uses the same namespace and is large enough for
  expression-bin control sampling.
- `score_name` is absent from `adata.obs` or overwrite is explicitly approved.

## Output State

- With `copy=False`, Scanpy mutates `adata` in place and returns `None`.
- With `copy=True`, Scanpy returns a copied AnnData object containing the score.
- Scores are written to `adata.obs[score_name]` as one floating-point value per
  observation.
- Scanpy does not write a missing-gene report or provenance metadata by itself;
  wrappers should add those artifacts externally.

## Important Parameters

- `gene_list`: required list of genes used for score calculation.
- `ctrl_as_ref`: defaults to `True`; the stable docs note this default will
  change in Scanpy 2.0.
- `ctrl_size`: number of reference genes sampled from each expression bin;
  Scanpy suggests using the gene-list length when the signature is not too
  small.
- `gene_pool`: genes eligible for reference sampling; defaults to all genes.
- `n_bins`: number of expression bins used for sampling reference genes.
- `score_name`: `.obs` column written by the function.
- `random_state`: seed used for reference gene sampling.
- `copy`: controls in-place mutation versus returning a copied AnnData object.
- `use_raw`: `None` uses `.raw` when present; wrappers should make this choice
  explicit.
- `layer`: named layer to score. Do not silently fall back to `.X` when a
  requested layer is absent.

## Minimal Use

```python
import scanpy as sc

score_key = "score_interferon"
sc.tl.score_genes(
    adata,
    gene_list=interferon_genes,
    score_name=score_key,
    ctrl_size=50,
    gene_pool=None,
    n_bins=25,
    random_state=0,
    use_raw=False,
    layer="log1p_norm",
)
```

Implementation wrappers should report retained genes, missing genes, expression
source, score key, control parameters, random seed, and Scanpy version.

## Validation Checks

- Confirm the selected expression source exists.
- Confirm `.raw` use is explicit when `.raw` is present, because `use_raw=None`
  can choose it automatically.
- Confirm all gene-list entries are in the approved namespace or report missing
  entries before scoring.
- Fail or require approval when too few genes remain after filtering.
- Confirm `gene_pool` genes exist and are sufficient for control sampling.
- Confirm `score_name` does not overwrite an existing `.obs` field unless
  approved.
- Record `ctrl_size`, `n_bins`, `ctrl_as_ref`, `random_state`, expression
  source, and gene-set source.
- After scoring, confirm `adata.obs[score_name]` exists, has one value per
  observation, and is numeric.

## Failure Modes

- Gene namespace mismatch causes most or all signature genes to be dropped.
- Too few retained signature genes make scores unstable or uninterpretable.
- `use_raw=None` selects `.raw` unexpectedly.
- Raw counts, scaled data, or residuals are scored while interpreted as
  normalized expression.
- Small or biased `gene_pool` produces poor reference-gene sampling.
- Stochastic control sampling produces different values when random seed or
  control pool changes.
- Existing `.obs` score columns are overwritten without approval.

## Statistical Caveats

- The score is relative to sampled control genes; it is not an absolute
  expression, pathway activity, or causal measurement.
- Score magnitude depends on expression normalization, gene availability,
  control-gene sampling, gene set length, and selected expression source.
- Scores from different gene sets are not automatically calibrated against each
  other.
- Per-cell score summaries are descriptive. Condition-level inference requires
  a sample-replicate-aware design and model.
- A signature score can support annotation review but does not prove a cell type
  identity by itself.

## Adapter Notes

- Execution adapters should call an approved wrapper that performs namespace,
  expression-source, and overwrite checks before invoking Scanpy.
- The wrapper should not normalize, filter, rank markers, annotate cells, or run
  DE unless those stages were separately approved.
- Persist a score table and metadata even when the AnnData object is also
  updated.
- For multiple signatures, use deterministic score-key naming and produce one
  missing-gene report per signature.
- Keep group-level summaries separate from inferential statistical tests.

## Sources Used

- Public Scanpy docs for `scanpy.tl.score_genes`:
  `https://scanpy.readthedocs.io/en/stable/generated/scanpy.tl.score_genes.html`.
- Local archive paths listed in frontmatter were used as supporting source
  material; this ref is intended to remain usable without those folders.
