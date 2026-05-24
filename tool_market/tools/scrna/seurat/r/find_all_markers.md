---
id: scrna.seurat.tool.find_all_markers
kind: tool_ref
package_ref: scrna.seurat.package.seurat
api_entrypoint: Seurat::FindAllMarkers
method_family: marker_ranking
state_in: [cluster_key, expression_source]
state_out: [marker_table]
parameters: [object, group.by, assay, slot, test.use, only.pos, logfc.threshold, min.pct]
caveats: [descriptive_not_replicate_aware, group_size_policy]
compatible_adapters: [rscript, snakemake, bash]
source_urls: [https://satijalab.org/seurat/reference/findallmarkers]
source_version: local Seurat docs mirror label 5.4.0
source_accessed_at: 2026-05-25
source_local_paths: [seurat_tutorial/reference/findallmarkers.html]
distillation_status: needs_version_check
---
# Seurat::FindAllMarkers

## API Entry Point

`Seurat::FindAllMarkers(object, assay = NULL, slot = "data", test.use = "wilcox", only.pos = FALSE, ...)`

## Method Family

Rank markers for all identity groups or a declared grouping column.

## Required Object State

Group labels, assay, and expression slot must be declared.

## Output State

A long marker table keyed by cluster or group.

## Important Parameters

`group.by`, `assay`, `slot`, `test.use`, `only.pos`, thresholds, and minimum
cell policies.

## Minimal Use

```r
markers <- Seurat::FindAllMarkers(obj, group.by = "cluster", assay = "RNA", slot = "data")
```

## Validation Checks

Check group sizes, output columns, method, thresholds, and feature universe.

## Failure Modes

Tiny groups, stale identities, incompatible expression scale, and overclaiming
cell-level markers as condition effects.

## Statistical Caveats

All-cluster marker ranking is exploratory and descriptive.

## Adapter Notes

Record grouping column, assay/slot, method, thresholds, and output path.

## Sources Used

- Local reference: `seurat_tutorial/reference/findallmarkers.html`.
