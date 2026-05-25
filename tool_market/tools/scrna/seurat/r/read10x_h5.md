---
id: scrna.seurat.tool.read10x_h5
kind: tool_ref
package_ref: scrna.seurat.package.seurat
api_entrypoint: Seurat::Read10X_h5
method_family: data_ingest
state_in: [tenx_hdf5_file]
state_out: [count_matrix]
parameters: [filename, use.names, unique.features]
caveats: [hdf5_layout, modality_names]
compatible_adapters: [rscript, snakemake, bash]
source_urls: [https://satijalab.org/seurat/reference/read10x_h5]
source_version: local Seurat docs mirror label 5.4.0
source_accessed_at: 2026-05-25
source_local_paths: [seurat_tutorial/reference/read10x_h5.html]
distillation_status: needs_version_check
---
# Seurat::Read10X_h5

## API Entry Point

`Seurat::Read10X_h5(filename, use.names = TRUE, unique.features = TRUE)`

## Method Family

Read 10x HDF5 feature-barcode files.

## Required Object State

Input HDF5 file must be readable and match a supported 10x layout.

## Output State

A count matrix or named list for multimodal files.

## Important Parameters

`use.names` and `unique.features` define feature-name handling.

## Minimal Use

```r
counts <- Seurat::Read10X_h5("filtered_feature_bc_matrix.h5")
```

## Validation Checks

Check file existence, HDF5 readability, output dimensions, and modality names.

## Failure Modes

Unsupported HDF5 layout, missing hdf5 libraries, and duplicate feature names.

## Statistical Caveats

HDF5 ingest does not establish QC or normalization state.

## Adapter Notes

Record source file, checksum if available, and feature-name policy.

## Sources Used

- Local reference: `seurat_tutorial/reference/read10x_h5.html`.
