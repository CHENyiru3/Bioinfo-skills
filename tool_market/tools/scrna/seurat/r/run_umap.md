---
id: scrna.seurat.tool.run_umap
kind: tool_ref
package_ref: scrna.seurat.package.seurat
api_entrypoint: Seurat::RunUMAP
method_family: embedding_visualization
state_in: [reduction_or_graph]
state_out: [umap_reduction]
parameters: [object, reduction, graph, dims, reduction.name, seed.use, umap.method, metric]
caveats: [visualization_not_evidence, reduction_key_collision]
compatible_adapters: [rscript, snakemake, bash]
source_urls: [https://satijalab.org/seurat/reference/runumap]
source_version: local Seurat docs mirror label 5.4.0
source_accessed_at: 2026-05-25
source_local_paths: [seurat_tutorial/reference/runumap.html]
distillation_status: needs_version_check
---
# Seurat::RunUMAP

## API Entry Point

`Seurat::RunUMAP(object, reduction = "pca", dims = 1:30, reduction.name = "umap", ...)`

## Method Family

Compute UMAP embeddings for visualization and diagnostics.

## Required Object State

The declared reduction or graph must exist and match the approved plan.

## Output State

A named UMAP reduction with cell embeddings.

## Important Parameters

`reduction`, `graph`, `dims`, `reduction.name`, `seed.use`, method, and metric.

## Minimal Use

```r
obj <- Seurat::RunUMAP(obj, reduction = "pca", dims = 1:30, reduction.name = "umap")
```

## Validation Checks

Check embedding shape, finite coordinates, reduction name, and provenance.

## Failure Modes

Missing graph/reduction, non-reproducible embedding, key overwrite, and
misinterpretation of visual distance.

## Statistical Caveats

UMAP is a visualization model, not direct quantitative evidence.

## Adapter Notes

Record input reduction or graph, dimensions, seed, method, and output key.

## Sources Used

- Local reference: `seurat_tutorial/reference/runumap.html`.
