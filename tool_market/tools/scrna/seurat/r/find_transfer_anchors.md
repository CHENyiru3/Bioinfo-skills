---
id: scrna.seurat.tool.find_transfer_anchors
kind: tool_ref
package_ref: scrna.seurat.package.seurat
api_entrypoint: Seurat::FindTransferAnchors
method_family: annotation_support
state_in: [reference_object, query_object]
state_out: [transfer_anchorset]
parameters: [reference, query, normalization.method, reference.reduction, dims, features]
caveats: [reference_query_compatibility, label_transfer_uncertainty]
compatible_adapters: [rscript, snakemake, bash]
source_urls: [https://satijalab.org/seurat/reference/findtransferanchors]
source_version: local Seurat docs mirror label 5.4.0
source_accessed_at: 2026-05-25
source_local_paths: [seurat_tutorial/reference/findtransferanchors.html, seurat_tutorial/articles/integration_mapping.html]
distillation_status: needs_version_check
---
# Seurat::FindTransferAnchors

## API Entry Point

`Seurat::FindTransferAnchors(reference, query, normalization.method, reference.reduction, dims, ...)`

## Method Family

Find anchors for reference mapping and label transfer.

## Required Object State

Reference and query objects must have compatible species, feature names, assays,
normalization, and reductions.

## Output State

A TransferAnchorSet used by mapping or transfer APIs.

## Important Parameters

Reference, query, normalization method, reduction, dimensions, and feature set.

## Minimal Use

```r
anchors <- Seurat::FindTransferAnchors(reference = ref, query = query, dims = 1:30)
```

## Validation Checks

Check shared features, reference labels, query assay, dimensions, and anchor set
creation.

## Failure Modes

Feature mismatch, species mismatch, missing reference labels, and inappropriate
reference choice.

## Statistical Caveats

Transfer anchors enable annotation hypotheses, not definitive labels.

## Adapter Notes

Record reference provenance, feature overlap, dimensions, and label fields.

## Sources Used

- Local reference: `seurat_tutorial/reference/findtransferanchors.html`.
- Local vignette: `seurat_tutorial/articles/integration_mapping.html`.
