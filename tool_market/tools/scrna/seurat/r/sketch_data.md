---
id: scrna.seurat.tool.sketch_data
kind: tool_ref
package_ref: scrna.seurat.package.seurat
api_entrypoint: Seurat::SketchData
method_family: large_data_sketch
state_in: [large_seurat_object]
state_out: [sketch_assay]
parameters: [object, ncells, method, sketched.assay, features, seed]
caveats: [sampling_bias, projection_policy]
compatible_adapters: [rscript, snakemake, bash]
source_urls: [https://satijalab.org/seurat/reference/sketchdata]
source_version: local Seurat docs mirror label 5.4.0
source_accessed_at: 2026-05-25
source_local_paths: [seurat_tutorial/reference/sketchdata.html, seurat_tutorial/articles/seurat5_sketch_analysis.html]
distillation_status: needs_version_check
---
# Seurat::SketchData

## API Entry Point

`Seurat::SketchData(object, ncells, method, sketched.assay, ...)`

## Method Family

Select representative cells for scalable analysis of large datasets.

## Required Object State

Input object must contain the assay/layers needed for sketching and enough
cells for the requested sample size.

## Output State

A sketch assay or object state containing selected cells.

## Important Parameters

`ncells`, `method`, `sketched.assay`, feature set, and seed.

## Minimal Use

```r
obj <- Seurat::SketchData(obj, ncells = 5000, method = "LeverageScore", sketched.assay = "sketch")
```

## Validation Checks

Check selected cell count, assay names, seed, and relationship to full object.

## Failure Modes

Unrepresentative sketch, missing large-data backing, memory pressure, and
projection mismatch.

## Statistical Caveats

Sketches approximate full data and may miss rare states if parameters or data
quality are poor.

## Adapter Notes

Record method, seed, requested cells, selected cells, and projection plan.

## Sources Used

- Local reference: `seurat_tutorial/reference/sketchdata.html`.
- Local vignette: `seurat_tutorial/articles/seurat5_sketch_analysis.html`.
