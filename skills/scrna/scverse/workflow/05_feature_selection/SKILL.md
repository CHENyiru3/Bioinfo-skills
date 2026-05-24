---
id: scrna.scverse.workflow.feature_selection
schema_version: "0.1.0"
kind: skill
domain: scrna
stage: feature_selection
status: filled
state_in: ["normalized/log expression or raw counts for selected flavor"]
state_out: ["feature_mask_key"]
registered_refs: [scrna.scverse.package.scanpy, scrna.scverse.tool.scanpy_highly_variable_genes]
validation: [backend_neutral, state_contract_checked]
---
# Feature Selection

## Purpose

Select informative genes for PCA and graph construction while preserving the
full feature table unless a separate, provenance-recorded subsetting decision is
approved. In the Scanpy path this usually means computing HVG metrics and
writing a declared boolean mask such as `var["highly_variable"]`.

This stage does not normalize, log-transform, integrate batches, run PCA, or
physically drop genes by default. The chosen HVG flavor determines whether the
input must be normalized/log expression or raw counts.

## When Required

- Before PCA when the analysis plan calls for PCA over HVGs instead of all
  genes.
- Before graph construction workflows that expect a declared `feature_mask_key`.
- When a user needs a reproducible, recorded feature-selection policy for later
  reruns or comparisons.

## When Optional

- When PCA or another representation is intentionally computed over all
  retained genes.
- When a model-based downstream method has its own feature-selection policy and
  the user approves that method-specific path.

## When Forbidden

- Do not run an HVG flavor on the wrong expression state.
- Do not silently subset the AnnData object to HVGs.
- Do not infer a missing `batch_key`; batch-aware selection requires an
  existing `.obs` column chosen by the user or upstream state policy.
- Do not treat HVGs as marker genes, cell-type labels, or biological
  interpretation.

## Required Input State

- For dispersion-based flavors such as `seurat` or `cell_ranger`, a declared
  normalized/log expression source.
- For `seurat_v3` or `seurat_v3_paper`, a declared raw-count source and
  availability of required optional dependencies.
- Optional `obs[batch_key]` only when batch-aware HVG selection is explicitly
  requested.
- A nonempty gene axis after prior QC/filtering.
- A declared intended `feature_mask_key`, commonly `highly_variable`.

## Produced Output State

- A boolean feature mask under the declared `feature_mask_key`, conventionally
  `var["highly_variable"]`.
- HVG metrics appropriate for the selected flavor, such as means and normalized
  dispersions or normalized variances.
- If `batch_key` is used, batch-aware HVG fields such as number of batches or
  intersection status when produced by the selected tool.
- Provenance recording expression source, flavor, `n_top_genes` or threshold
  policy, `batch_key`, output mask key, and subsetting policy.

## User Decision Points

- Which expression source to use and whether it matches the chosen flavor.
- Which HVG flavor to use: `seurat`, `cell_ranger`, `seurat_v3`, or
  `seurat_v3_paper`.
- The number of genes or threshold parameters used to define the mask.
- Whether to use a `batch_key`; if yes, which `.obs` column is the correct
  technical or sample-level batch field.
- Whether the stage should only write a mask or physically subset features.
  The default policy is mask-only.
- How to handle an existing mask or metrics columns: fail, choose a new key, or
  explicitly overwrite with provenance.

## Registered Package Refs

- `scrna.scverse.package.scanpy`

## Registered Tool Refs

- `scrna.scverse.tool.scanpy_highly_variable_genes`

## Expected Artifacts

- Mutated AnnData output with the declared feature mask and HVG metrics.
- Parameter/provenance entry recording flavor, batch key, expression source,
  `n_top_genes` or thresholds, and output mask key.
- Validation summary reporting mask existence, selected-gene count, and whether
  feature subsetting occurred.

## Validation Checks

- Confirm the expression source exists and matches the count/log requirement of
  the selected flavor.
- Confirm `batch_key` exists in `.obs` when requested and is recorded even when
  `None`.
- Confirm the declared `feature_mask_key` exists in `.var` and is boolean-like.
- Confirm the selected-gene count is greater than zero and less than or equal to
  the number of retained genes.
- Confirm no physical feature subsetting occurred unless explicitly approved.
- Confirm the flavor, `batch_key`, thresholds, and expression source are
  recorded in provenance.

## Failure Modes

- Wrong count/log state for the chosen flavor.
- `batch_key` is missing, biologically confounded, or has too few cells per
  batch for stable estimates.
- `seurat_v3` dependencies such as `scikit-misc` are unavailable.
- Too few genes pass thresholds or all selected genes are dominated by QC,
  ribosomal, mitochondrial, cell-cycle, or batch effects.
- Existing HVG columns are overwritten without an explicit decision.
- Physical subsetting removes genes needed by later marker or signature stages.

## Allowed Claims

- A declared HVG mask and metrics were produced using the recorded flavor and
  expression source.
- The feature mask is available for PCA or other approved downstream methods.
- Batch-aware HVG selection used the recorded `.obs` batch key when provided.

## Forbidden Claims

- HVGs are marker genes or proof of cell identity.
- HVG selection corrects batch effects.
- A feature mask produced from a confounded design is biologically unbiased.
- The selected features are appropriate for condition-level inference without
  a separate statistical design check.

## Next Stage Routing

- Route to `06_dimensionality_reduction` when PCA should use the declared
  feature mask.
- Route back to `04_normalization_transform` if the requested flavor requires a
  different count/log state.
- Route to `07_batch_integration` only after PCA or another representation is
  produced; HVG selection alone is not integration.
- Route to marker or signature stages only through their own state checks,
  because HVG selection can remove genes of interest.

## Backend-Neutral Rule

Do not place workflow-engine, shell, script, or notebook syntax in this skill.
Execution belongs in wrappers and adapters after the user approves the exact
operation, parameters, and artifacts.
