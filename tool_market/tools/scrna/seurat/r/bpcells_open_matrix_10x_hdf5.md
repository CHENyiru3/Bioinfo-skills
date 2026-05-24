---
id: scrna.seurat.tool.bpcells_open_matrix_10x_hdf5
kind: tool_ref
package_ref: scrna.seurat.package.bpcells
api_entrypoint: BPCells::open_matrix_10x_hdf5
method_family: large_matrix_io
state_in: [tenx_hdf5_file]
state_out: [bpcells_matrix]
parameters: [path]
caveats: [hdf5_layout, feature_identifier_policy]
compatible_adapters: [rscript, snakemake, bash]
source_urls: [https://bnprks.github.io/BPCells/reference/open_matrix_10x_hdf5.html]
source_version: BPCells docs version needs verification
source_accessed_at: 2026-05-25
source_local_paths: [seurat_tutorial/articles/seurat5_bpcells_interaction_vignette.html]
distillation_status: needs_version_check
---
# BPCells::open_matrix_10x_hdf5

## API Entry Point

`BPCells::open_matrix_10x_hdf5(path)`

## Method Family

Open 10x HDF5 data through BPCells for large-data workflows.

## Required Object State

Input HDF5 file must follow a supported feature-barcode layout.

## Output State

A BPCells-backed matrix object.

## Important Parameters

Input path and feature identifier policy handled downstream.

## Minimal Use

```r
mat <- BPCells::open_matrix_10x_hdf5("filtered_feature_bc_matrix.h5")
```

## Validation Checks

Check file existence, matrix dimensions, row/column names, and class.

## Failure Modes

Unsupported HDF5 layout, missing file, and path-specific portability issues.

## Statistical Caveats

I/O does not perform QC or normalization.

## Adapter Notes

Record source file and any output matrix directory created later.

## Sources Used

- Public docs: `https://bnprks.github.io/BPCells/reference/open_matrix_10x_hdf5.html`.
- Local archive: `seurat_tutorial/articles/seurat5_bpcells_interaction_vignette.html`.
