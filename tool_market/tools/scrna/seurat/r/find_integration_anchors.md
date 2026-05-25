---
id: scrna.seurat.tool.find_integration_anchors
kind: tool_ref
package_ref: scrna.seurat.package.seurat
api_entrypoint: Seurat::FindIntegrationAnchors
method_family: batch_integration
state_in: [object_list, integration_features]
state_out: [anchorset]
parameters: [object.list, anchor.features, reduction, dims, normalization.method]
caveats: [object_list_policy, integration_design]
compatible_adapters: [rscript, snakemake, bash]
source_urls: [https://satijalab.org/seurat/reference/findintegrationanchors]
source_version: local Seurat docs mirror label 5.4.0
source_accessed_at: 2026-05-25
source_local_paths: [seurat_tutorial/reference/findintegrationanchors.html, seurat_tutorial/articles/integration_introduction.html]
distillation_status: needs_version_check
---
# Seurat::FindIntegrationAnchors

## API Entry Point

`Seurat::FindIntegrationAnchors(object.list, anchor.features, reduction, dims, normalization.method, ...)`

## Method Family

Anchor discovery for multi-object integration.

## Required Object State

Each object must be preprocessed consistently and retain required features and
metadata.

## Output State

An AnchorSet consumed by integration or label-transfer functions.

## Important Parameters

Object list, feature set, reduction, dimensions, and normalization method.

## Minimal Use

```r
anchors <- Seurat::FindIntegrationAnchors(object.list = objects, dims = 1:30)
```

## Validation Checks

Check object count, shared features, dimensions, normalization method, and
anchor set creation.

## Failure Modes

Mismatched feature names, incompatible normalization, confounded batches, and
large memory use.

## Statistical Caveats

Anchors encode assumed cross-dataset correspondence and require design review.

## Adapter Notes

Record object sources, features, method, dimensions, and normalization policy.

## Sources Used

- Local reference: `seurat_tutorial/reference/findintegrationanchors.html`.
- Local vignette: `seurat_tutorial/articles/integration_introduction.html`.
