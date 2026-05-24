---
id: scrna.seurat.tool.bpcells_open_matrix_dir
kind: tool_ref
package_ref: scrna.seurat.package.bpcells
api_entrypoint: BPCells::open_matrix_dir
method_family: large_matrix_io
state_in: [bpcells_matrix_directory]
state_out: [bpcells_matrix]
parameters: [dir]
caveats: [path_portability, on_disk_backing]
compatible_adapters: [rscript, snakemake, bash]
source_urls: [https://bnprks.github.io/BPCells/reference/matrix_io.html]
source_version: BPCells docs version needs verification
source_accessed_at: 2026-05-25
source_local_paths: [seurat_tutorial/articles/seurat5_bpcells_interaction_vignette.html]
distillation_status: needs_version_check
---
# BPCells::open_matrix_dir

## API Entry Point

`BPCells::open_matrix_dir(dir)`

## Method Family

Open an on-disk BPCells matrix directory.

## Required Object State

The directory must exist, be portable, and contain a valid BPCells matrix.

## Output State

A BPCells matrix object usable as Seurat assay counts.

## Important Parameters

`dir`.

## Minimal Use

```r
mat <- BPCells::open_matrix_dir("counts_bpcells")
```

## Validation Checks

Check path existence, dimensions, feature/cell names, and matrix class.

## Failure Modes

Moved directories, permission failures, unsupported directory contents, and
accidental in-memory conversion.

## Statistical Caveats

Storage format does not define preprocessing state.

## Adapter Notes

Record directory path and portability constraints.

## Sources Used

- Public docs: `https://bnprks.github.io/BPCells/reference/matrix_io.html`.
- Local archive: `seurat_tutorial/articles/seurat5_bpcells_interaction_vignette.html`.
