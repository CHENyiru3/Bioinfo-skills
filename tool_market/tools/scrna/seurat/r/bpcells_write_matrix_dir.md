---
id: scrna.seurat.tool.bpcells_write_matrix_dir
kind: tool_ref
package_ref: scrna.seurat.package.bpcells
api_entrypoint: BPCells::write_matrix_dir
method_family: large_matrix_io
state_in: [matrix]
state_out: [bpcells_matrix_directory]
parameters: [mat, dir]
caveats: [path_portability, output_overwrite_policy]
compatible_adapters: [rscript, snakemake, bash]
source_urls: [https://bnprks.github.io/BPCells/reference/matrix_io.html]
source_version: BPCells docs version needs verification
source_accessed_at: 2026-05-25
source_local_paths: [seurat_tutorial/articles/seurat5_bpcells_interaction_vignette.html]
distillation_status: needs_version_check
---
# BPCells::write_matrix_dir

## API Entry Point

`BPCells::write_matrix_dir(mat, dir)`

## Method Family

Write a matrix into BPCells on-disk format.

## Required Object State

Input matrix must have stable dimensions and identifiers.

## Output State

An on-disk BPCells matrix directory.

## Important Parameters

`mat` and output `dir`.

## Minimal Use

```r
BPCells::write_matrix_dir(mat = counts, dir = "counts_bpcells")
```

## Validation Checks

Check output directory, matrix reopening, dimensions, identifiers, and overwrite
policy.

## Failure Modes

Output path collision, permissions, disk space, and lost metadata.

## Statistical Caveats

Writing storage does not alter biological state unless data are transformed
before writing.

## Adapter Notes

Record output path, source matrix, and whether overwrite was approved.

## Sources Used

- Public docs: `https://bnprks.github.io/BPCells/reference/matrix_io.html`.
- Local archive: `seurat_tutorial/articles/seurat5_bpcells_interaction_vignette.html`.
