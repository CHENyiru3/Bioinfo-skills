---
id: scrna.seurat.tool.as_single_cell_experiment
kind: tool_ref
package_ref: scrna.seurat.package.seurat
api_entrypoint: Seurat::as.SingleCellExperiment
method_family: interoperability
state_in: [seurat_object]
state_out: [singlecellexperiment_object]
parameters: [x, assay]
caveats: [state_loss_review, assay_mapping]
compatible_adapters: [rscript, bash]
source_urls: [https://satijalab.org/seurat/reference/as.singlecellexperiment]
source_version: local Seurat docs mirror label 5.4.0
source_accessed_at: 2026-05-25
source_local_paths: [seurat_tutorial/reference/as.singlecellexperiment.html]
distillation_status: needs_version_check
---
# Seurat::as.SingleCellExperiment

## API Entry Point

`Seurat::as.SingleCellExperiment(x, assay = NULL, ...)`

## Method Family

Convert Seurat objects to SingleCellExperiment.

## Required Object State

Assay, layer, metadata, reductions, and unsupported state must be reviewed.

## Output State

A SingleCellExperiment object with mapped assays, colData, rowData, and reduced
dimensions where supported.

## Important Parameters

`assay` and conversion scope.

## Minimal Use

```r
sce <- Seurat::as.SingleCellExperiment(obj, assay = "RNA")
```

## Validation Checks

Check dimensions, cell names, feature names, assay mapping, metadata columns,
and reductions after conversion.

## Failure Modes

Lost graphs, image state, layer mismatch, and unsupported modality metadata.

## Statistical Caveats

Conversion does not validate analysis results.

## Adapter Notes

Record source object, assay mapping, dropped fields, and output format.

## Sources Used

- Local reference: `seurat_tutorial/reference/as.singlecellexperiment.html`.
