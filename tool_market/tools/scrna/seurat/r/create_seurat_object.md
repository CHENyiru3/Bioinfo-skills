---
id: scrna.seurat.tool.create_seurat_object
kind: tool_ref
package_ref: scrna.seurat.package.seurat
api_entrypoint: Seurat::CreateSeuratObject
method_family: object_creation
state_in: [count_matrix, optional_metadata]
state_out: [seurat_object, assay_counts_layer]
parameters: [counts, project, assay, names.field, names.delim, meta.data, min.cells, min.features]
caveats: [preserve_counts, metadata_alignment]
compatible_adapters: [rscript, snakemake, bash, ipython_notebook]
source_urls: [https://satijalab.org/seurat/reference/createseuratobject]
source_version: local Seurat docs mirror label 5.4.0
source_accessed_at: 2026-05-25
source_local_paths: [seurat_tutorial/reference/createseuratobject.html]
distillation_status: needs_version_check
---
# Seurat::CreateSeuratObject

## API Entry Point

`Seurat::CreateSeuratObject(counts, project, assay, meta.data, min.cells, min.features, ...)`

## Method Family

Create a Seurat object from a count matrix and optional cell metadata.

## Required Object State

Input counts must have cells and features with stable names. Metadata rows must
align exactly to cell names.

## Output State

A Seurat object with a declared assay and counts layer.

## Important Parameters

`counts`, `assay`, `meta.data`, `min.cells`, and `min.features` control object
creation and initial filtering.

## Minimal Use

```r
obj <- Seurat::CreateSeuratObject(counts = counts, assay = "RNA", meta.data = meta)
```

## Validation Checks

Check nonempty dimensions, unique row and column names, metadata alignment, and
the expected assay/layer keys.

## Failure Modes

Metadata mismatch, duplicate cell names, accidental initial filtering, and
memory pressure from dense matrices.

## Statistical Caveats

Initial filtering changes the analysis population and must be recorded.

## Adapter Notes

Adapters should pass input paths and parameters to wrappers; wrappers should
write object summaries and provenance.

## Sources Used

- Local reference: `seurat_tutorial/reference/createseuratobject.html`.
