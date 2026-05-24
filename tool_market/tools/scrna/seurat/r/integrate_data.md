---
id: scrna.seurat.tool.integrate_data
kind: tool_ref
package_ref: scrna.seurat.package.seurat
api_entrypoint: Seurat::IntegrateData
method_family: batch_integration
state_in: [anchorset]
state_out: [integrated_assay]
parameters: [anchorset, new.assay.name, normalization.method, dims, features]
caveats: [integrated_scale_policy, downstream_count_policy]
compatible_adapters: [rscript, snakemake, bash]
source_urls: [https://satijalab.org/seurat/reference/integratedata]
source_version: local Seurat docs mirror label 5.4.0
source_accessed_at: 2026-05-25
source_local_paths: [seurat_tutorial/reference/integratedata.html]
distillation_status: needs_version_check
---
# Seurat::IntegrateData

## API Entry Point

`Seurat::IntegrateData(anchorset, new.assay.name = "integrated", normalization.method, dims, ...)`

## Method Family

Create integrated expression assay from anchors.

## Required Object State

An AnchorSet generated from compatible objects.

## Output State

An integrated assay in a Seurat object.

## Important Parameters

`new.assay.name`, `normalization.method`, `dims`, and feature set.

## Minimal Use

```r
obj <- Seurat::IntegrateData(anchorset = anchors, dims = 1:30)
```

## Validation Checks

Check integrated assay exists, dimensions, feature scope, and provenance.

## Failure Modes

Anchor mismatch, memory pressure, overcorrection, and use of integrated values
for count-based tests.

## Statistical Caveats

Integrated assays are for alignment and clustering, not direct count-scale DE.

## Adapter Notes

Record anchor source, output assay, dimensions, and downstream usage limits.

## Sources Used

- Local reference: `seurat_tutorial/reference/integratedata.html`.
