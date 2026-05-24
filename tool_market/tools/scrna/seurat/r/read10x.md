---
id: scrna.seurat.tool.read10x
kind: tool_ref
package_ref: scrna.seurat.package.seurat
api_entrypoint: Seurat::Read10X
method_family: data_ingest
state_in: [tenx_matrix_directory]
state_out: [count_matrix]
parameters: [data.dir, gene.column, cell.column, unique.features, strip.suffix]
caveats: [feature_id_policy, barcode_suffix_policy]
compatible_adapters: [rscript, snakemake, bash]
source_urls: [https://satijalab.org/seurat/reference/read10x]
source_version: local Seurat docs mirror label 5.4.0
source_accessed_at: 2026-05-25
source_local_paths: [seurat_tutorial/reference/read10x.html]
distillation_status: needs_version_check
---
# Seurat::Read10X

## API Entry Point

`Seurat::Read10X(data.dir, gene.column = 2, cell.column = 1, unique.features = TRUE, strip.suffix = FALSE)`

## Method Family

Read 10x Genomics matrix directories into sparse matrices.

## Required Object State

The directory must contain compatible matrix, barcode, and feature files.

## Output State

A sparse count matrix or named list of matrices.

## Important Parameters

`gene.column`, `cell.column`, `unique.features`, and `strip.suffix` affect
feature and cell identifiers.

## Minimal Use

```r
counts <- Seurat::Read10X(data.dir = "filtered_feature_bc_matrix")
```

## Validation Checks

Check matrix dimensions, unique identifiers, modality names, and expected sparse
matrix type.

## Failure Modes

Malformed 10x directory, duplicate feature names, unexpected multiome output,
and barcode suffix mismatches.

## Statistical Caveats

Reading data is not QC; downstream filtering decisions remain separate.

## Adapter Notes

Record source path, file checks, and identifier policy.

## Sources Used

- Local reference: `seurat_tutorial/reference/read10x.html`.
