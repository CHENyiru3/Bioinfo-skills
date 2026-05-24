---
id: scrna.seurat.tool.run_pca
kind: tool_ref
package_ref: scrna.seurat.package.seurat
api_entrypoint: Seurat::RunPCA
method_family: dimensionality_reduction
state_in: [scaled_data_layer, variable_features]
state_out: [pca_reduction]
parameters: [object, assay, features, npcs, reduction.name, seed.use]
caveats: [feature_scope, reduction_key_collision]
compatible_adapters: [rscript, snakemake, bash]
source_urls: [https://satijalab.org/seurat/reference/runpca]
source_version: local Seurat docs mirror label 5.4.0
source_accessed_at: 2026-05-25
source_local_paths: [seurat_tutorial/reference/runpca.html]
distillation_status: needs_version_check
---
# Seurat::RunPCA

## API Entry Point

`Seurat::RunPCA(object, features = NULL, npcs = 50, reduction.name = "pca", ...)`

## Method Family

Compute PCA reduction from selected features.

## Required Object State

Scaled data and feature scope must be declared.

## Output State

A named PCA reduction with cell embeddings and feature loadings.

## Important Parameters

`features`, `npcs`, `reduction.name`, `assay`, and seed.

## Minimal Use

```r
obj <- Seurat::RunPCA(obj, features = VariableFeatures(obj), npcs = 30, reduction.name = "pca")
```

## Validation Checks

Check reduction exists, dimensions match cells, and key replacement was
approved.

## Failure Modes

Missing scaled data, too few features, overwritten reduction, and randomized
differences from seed/backend changes.

## Statistical Caveats

PCA captures dominant variation, which may include batch or QC effects.

## Adapter Notes

Record assay, features, components, seed, and reduction name.

## Sources Used

- Local reference: `seurat_tutorial/reference/runpca.html`.
