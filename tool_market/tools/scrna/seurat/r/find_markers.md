---
id: scrna.seurat.tool.find_markers
kind: tool_ref
package_ref: scrna.seurat.package.seurat
api_entrypoint: Seurat::FindMarkers
method_family: marker_ranking
state_in: [group_key, expression_source]
state_out: [marker_table]
parameters: [object, ident.1, ident.2, group.by, assay, slot, test.use, logfc.threshold, min.pct]
caveats: [descriptive_not_replicate_aware, expression_scale_policy]
compatible_adapters: [rscript, snakemake, bash]
source_urls: [https://satijalab.org/seurat/reference/findmarkers]
source_version: local Seurat docs mirror label 5.4.0
source_accessed_at: 2026-05-25
source_local_paths: [seurat_tutorial/reference/findmarkers.html]
distillation_status: needs_version_check
---
# Seurat::FindMarkers

## API Entry Point

`Seurat::FindMarkers(object, ident.1, ident.2 = NULL, group.by = NULL, assay = NULL, slot = "data", test.use = "wilcox", ...)`

## Method Family

Marker ranking or pairwise group comparison.

## Required Object State

Group labels and expression source must be declared and valid for all cells.

## Output State

A marker table with statistics and per-feature summaries.

## Important Parameters

`ident.1`, `ident.2`, `group.by`, `assay`, `slot`, `test.use`, thresholds, and
latent-variable settings.

## Minimal Use

```r
markers <- Seurat::FindMarkers(obj, ident.1 = "0", group.by = "cluster", assay = "RNA", slot = "data")
```

## Validation Checks

Check group counts, selected assay/slot, feature universe, output columns, and
method provenance.

## Failure Modes

Wrong identities, missing groups, incompatible slot/test combination, and
condition-level overclaims from cell-level tests.

## Statistical Caveats

Cluster marker ranking is descriptive and not replicate-aware condition-level
differential expression.

## Adapter Notes

Record grouping, comparison, assay/slot, method, thresholds, and package
versions.

## Sources Used

- Local reference: `seurat_tutorial/reference/findmarkers.html`.
