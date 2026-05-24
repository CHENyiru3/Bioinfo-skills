---
id: scrna.seurat.tool.find_clusters
kind: tool_ref
package_ref: scrna.seurat.package.seurat
api_entrypoint: Seurat::FindClusters
method_family: clustering
state_in: [neighbor_graph]
state_out: [cluster_key]
parameters: [object, graph.name, resolution, algorithm, random.seed, cluster.name]
caveats: [graph_required, labels_not_cell_types]
compatible_adapters: [rscript, snakemake, bash]
source_urls: [https://satijalab.org/seurat/reference/findclusters]
source_version: local Seurat docs mirror label 5.4.0
source_accessed_at: 2026-05-25
source_local_paths: [seurat_tutorial/reference/findclusters.html]
distillation_status: needs_version_check
---
# Seurat::FindClusters

## API Entry Point

`Seurat::FindClusters(object, graph.name = NULL, resolution = 0.8, cluster.name = NULL, ...)`

## Method Family

Graph community detection.

## Required Object State

A declared neighbor graph must exist.

## Output State

Cluster labels in metadata and updated identities unless controlled by wrapper
policy.

## Important Parameters

`graph.name`, `resolution`, `algorithm`, `random.seed`, and `cluster.name`.

## Minimal Use

```r
obj <- Seurat::FindClusters(obj, graph.name = "RNA_snn", resolution = 0.8, cluster.name = "seurat_clusters_r08")
```

## Validation Checks

Check cluster key, label count, cluster sizes, graph provenance, and overwrite
policy.

## Failure Modes

Wrong graph, over/underclustering, overwritten identities, and tiny unstable
clusters.

## Statistical Caveats

Clusters are graph communities, not final cell types or condition effects.

## Adapter Notes

Record graph name, resolution, algorithm, seed, output key, and cluster-size
table.

## Sources Used

- Local reference: `seurat_tutorial/reference/findclusters.html`.
