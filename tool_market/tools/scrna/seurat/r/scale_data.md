---
id: scrna.seurat.tool.scale_data
kind: tool_ref
package_ref: scrna.seurat.package.seurat
api_entrypoint: Seurat::ScaleData
method_family: scaling
state_in: [normalized_assay, variable_features]
state_out: [scaled_data_layer]
parameters: [object, features, assay, vars.to.regress, model.use, do.scale, do.center]
caveats: [feature_scope, regression_covariates]
compatible_adapters: [rscript, snakemake, bash]
source_urls: [https://satijalab.org/seurat/reference/scaledata]
source_version: local Seurat docs mirror label 5.4.0
source_accessed_at: 2026-05-25
source_local_paths: [seurat_tutorial/reference/scaledata.html]
distillation_status: needs_version_check
---
# Seurat::ScaleData

## API Entry Point

`Seurat::ScaleData(object, features = NULL, assay = NULL, vars.to.regress = NULL, ...)`

## Method Family

Scale and center expression values for dimensionality reduction.

## Required Object State

The selected assay must have normalized data and declared feature set.

## Output State

Scaled values in the assay `scale.data` layer.

## Important Parameters

`features`, `assay`, regression variables, centering, and scaling flags.

## Minimal Use

```r
obj <- Seurat::ScaleData(obj, assay = "RNA", features = VariableFeatures(obj))
```

## Validation Checks

Check feature scope, output dimensions, and regression covariate availability.

## Failure Modes

Dense memory use, wrong feature set, missing covariates, and hidden active-assay
selection.

## Statistical Caveats

Regression can remove biological signal if covariates are confounded.

## Adapter Notes

Record feature scope and regression covariates.

## Sources Used

- Local reference: `seurat_tutorial/reference/scaledata.html`.
