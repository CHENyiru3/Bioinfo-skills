---
id: scrna.seurat.tool.find_neighbors
kind: tool_ref
package_ref: scrna.seurat.package.seurat
api_entrypoint: Seurat::FindNeighbors
method_family: neighbor_graph
state_in: [reduction_key]
state_out: [neighbor_graph]
parameters: [object, reduction, dims, k.param, graph.name, nn.method, annoy.metric, l2.norm]
caveats: [declared_reduction_required, graph_key_collision]
compatible_adapters: [rscript, snakemake, bash]
source_urls: [https://satijalab.org/seurat/reference/findneighbors]
source_version: local Seurat docs mirror label 5.4.0
source_accessed_at: 2026-05-25
source_local_paths: [seurat_tutorial/reference/findneighbors.html]
distillation_status: needs_version_check
---
# Seurat::FindNeighbors

## API Entry Point

`Seurat::FindNeighbors(object, reduction = "pca", dims = 1:30, graph.name = NULL, ...)`

## Method Family

Construct neighbor and shared-nearest-neighbor graphs.

## Required Object State

The declared reduction must exist and contain enough dimensions.

## Output State

Neighbor graph objects stored under named graph keys.

## Important Parameters

`reduction`, `dims`, `k.param`, `graph.name`, nearest-neighbor method, and
metric.

## Minimal Use

```r
obj <- Seurat::FindNeighbors(obj, reduction = "pca", dims = 1:30, graph.name = "RNA_snn")
```

## Validation Checks

Check reduction dimensions, graph names, graph matrix shape, and overwrite
policy.

## Failure Modes

Stale reduction, wrong dimensions, overwritten graph, fragmented graph, and
batch-driven neighborhoods.

## Statistical Caveats

Graph structure is model-derived and inherits reduction and distance choices.

## Adapter Notes

Record reduction, dimensions, k, graph names, method, metric, and seed/backend.

## Sources Used

- Local reference: `seurat_tutorial/reference/findneighbors.html`.
