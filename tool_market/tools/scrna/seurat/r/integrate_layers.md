---
id: scrna.seurat.tool.integrate_layers
kind: tool_ref
package_ref: scrna.seurat.package.seurat
api_entrypoint: Seurat::IntegrateLayers
method_family: batch_integration
state_in: [split_layers, reduction_key]
state_out: [integrated_reduction]
parameters: [object, method, orig.reduction, new.reduction, assay, layers, scale.layer]
caveats: [integration_can_remove_biology, layer_policy]
compatible_adapters: [rscript, snakemake, bash]
source_urls: [https://satijalab.org/seurat/reference/integratelayers]
source_version: local Seurat docs mirror label 5.4.0
source_accessed_at: 2026-05-25
source_local_paths: [seurat_tutorial/reference/integratelayers.html, seurat_tutorial/articles/seurat5_integration.html]
distillation_status: needs_version_check
---
# Seurat::IntegrateLayers

## API Entry Point

`Seurat::IntegrateLayers(object, method, orig.reduction, new.reduction, assay = NULL, ...)`

## Method Family

Seurat v5 layer-aware integration.

## Required Object State

The object must have declared split layers, a source reduction, and integration
metadata such as batch/sample labels.

## Output State

An integrated reduction or integrated object state under a declared key.

## Important Parameters

`method`, `orig.reduction`, `new.reduction`, `assay`, layer selection, and scale
layer.

## Minimal Use

```r
obj <- Seurat::IntegrateLayers(obj, method = Seurat::CCAIntegration, orig.reduction = "pca", new.reduction = "integrated.cca")
```

## Validation Checks

Check layer names, source reduction, output reduction shape, and integration
provenance.

## Failure Modes

Wrong layer split, confounded design, missing method dependency, and
overcorrection.

## Statistical Caveats

Integration is a modeling decision and can remove true biology.

## Adapter Notes

Record batch variables, method, source and output reductions, and layer policy.

## Sources Used

- Local reference: `seurat_tutorial/reference/integratelayers.html`.
- Local vignette: `seurat_tutorial/articles/seurat5_integration.html`.
