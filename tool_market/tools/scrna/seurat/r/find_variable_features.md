---
id: scrna.seurat.tool.find_variable_features
kind: tool_ref
package_ref: scrna.seurat.package.seurat
api_entrypoint: Seurat::FindVariableFeatures
method_family: feature_selection
state_in: [normalized_assay]
state_out: [variable_features]
parameters: [object, assay, selection.method, nfeatures, mean.cutoff, dispersion.cutoff]
caveats: [assay_scale_policy, downstream_pca_dependency]
compatible_adapters: [rscript, snakemake, bash]
source_urls: [https://satijalab.org/seurat/reference/findvariablefeatures]
source_version: local Seurat docs mirror label 5.4.0
source_accessed_at: 2026-05-25
source_local_paths: [seurat_tutorial/reference/findvariablefeatures.html]
distillation_status: needs_version_check
---
# Seurat::FindVariableFeatures

## API Entry Point

`Seurat::FindVariableFeatures(object, selection.method, nfeatures, assay = NULL, ...)`

## Method Family

Feature selection for downstream dimensionality reduction.

## Required Object State

The selected assay must be normalized or transformed according to the approved
workflow.

## Output State

Variable feature names stored on the selected assay.

## Important Parameters

`selection.method`, `nfeatures`, and cutoff parameters.

## Minimal Use

```r
obj <- Seurat::FindVariableFeatures(obj, assay = "RNA", nfeatures = 2000)
```

## Validation Checks

Check selected features are present, nonempty, unique, and linked to the
expected assay.

## Failure Modes

Wrong assay scale, too few features, stale variable features after filtering,
and hidden active-assay use.

## Statistical Caveats

Feature selection affects downstream PCA, graph, clustering, and markers.

## Adapter Notes

Record assay, method, nfeatures, and resulting feature count.

## Sources Used

- Local reference: `seurat_tutorial/reference/findvariablefeatures.html`.
