---
id: scrna.seurat.tool.sctransform
kind: tool_ref
package_ref: scrna.seurat.package.sctransform
api_entrypoint: Seurat::SCTransform
method_family: normalization_transform
state_in: [seurat_object_counts]
state_out: [sct_assay]
parameters: [object, assay, new.assay.name, vars.to.regress, method, vst.flavor, conserve.memory]
caveats: [count_scale_required, model_provenance]
compatible_adapters: [rscript, snakemake, bash, ipython_notebook]
source_urls: [https://satijalab.org/seurat/reference/sctransform]
source_version: local Seurat docs mirror label 5.4.0
source_accessed_at: 2026-05-25
source_local_paths: [seurat_tutorial/reference/sctransform.html, seurat_tutorial/articles/sctransform_vignette.html]
distillation_status: needs_version_check
---
# Seurat::SCTransform

## API Entry Point

`Seurat::SCTransform(object, assay = "RNA", new.assay.name = "SCT", ...)`

## Method Family

Variance-stabilizing count transformation.

## Required Object State

The selected assay must preserve count data and relevant covariates must exist
before regression.

## Output State

An SCT assay with transformed values, model metadata, and variable features.

## Important Parameters

`assay`, `new.assay.name`, `vars.to.regress`, `method`, `vst.flavor`, and
memory options.

## Minimal Use

```r
obj <- Seurat::SCTransform(obj, assay = "RNA", new.assay.name = "SCT")
```

## Validation Checks

Check count source, SCT assay creation, model metadata, dimensions, and
variable feature state.

## Failure Modes

Missing counts, wrong assay, invalid covariates, memory pressure, and model fit
errors.

## Statistical Caveats

SCT residuals and log-normalized data are different scales; downstream tests
must declare which scale they consume.

## Adapter Notes

Record assay, new assay name, regression covariates, method, and package
versions.

## Sources Used

- Local reference: `seurat_tutorial/reference/sctransform.html`.
- Local vignette: `seurat_tutorial/articles/sctransform_vignette.html`.
