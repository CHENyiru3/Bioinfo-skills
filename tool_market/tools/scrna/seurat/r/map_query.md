---
id: scrna.seurat.tool.map_query
kind: tool_ref
package_ref: scrna.seurat.package.seurat
api_entrypoint: Seurat::MapQuery
method_family: annotation_support
state_in: [transfer_anchorset, reference_object, query_object]
state_out: [mapped_query]
parameters: [anchorset, query, reference, refdata, reference.reduction, reduction.model]
caveats: [reference_provenance, prediction_score_review]
compatible_adapters: [rscript, snakemake, bash]
source_urls: [https://satijalab.org/seurat/reference/mapquery]
source_version: local Seurat docs mirror label 5.4.0
source_accessed_at: 2026-05-25
source_local_paths: [seurat_tutorial/reference/mapquery.html, seurat_tutorial/articles/integration_mapping.html]
distillation_status: needs_version_check
---
# Seurat::MapQuery

## API Entry Point

`Seurat::MapQuery(anchorset, query, reference, refdata, reference.reduction, reduction.model, ...)`

## Method Family

Map a query object onto a reference and transfer labels or embeddings.

## Required Object State

Transfer anchors, reference metadata, and compatible query state must exist.

## Output State

Query object with transferred labels, scores, and projected reductions.

## Important Parameters

`refdata`, `reference.reduction`, `reduction.model`, and anchor set.

## Minimal Use

```r
query <- Seurat::MapQuery(anchorset = anchors, query = query, reference = ref, refdata = list(celltype = "celltype"))
```

## Validation Checks

Check transferred columns, score columns, reference provenance, and query cell
count.

## Failure Modes

Missing reference metadata, poor feature overlap, incompatible reductions, and
overconfident predictions.

## Statistical Caveats

Transferred labels need marker and domain review.

## Adapter Notes

Record reference source, transferred fields, prediction-score fields, and output
keys.

## Sources Used

- Local reference: `seurat_tutorial/reference/mapquery.html`.
- Local vignette: `seurat_tutorial/articles/integration_mapping.html`.
