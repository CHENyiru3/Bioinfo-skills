---
id: scrna.seurat.tool.bpcells_open_matrix_anndata_hdf5
kind: tool_ref
package_ref: scrna.seurat.package.bpcells
api_entrypoint: BPCells::open_matrix_anndata_hdf5
method_family: interoperability
state_in: [h5ad_file]
state_out: [bpcells_matrix]
parameters: [path]
caveats: [h5ad_matrix_selection, metadata_not_loaded]
compatible_adapters: [rscript, snakemake, bash]
source_urls: [https://bnprks.github.io/BPCells/reference/open_matrix_anndata_hdf5.html]
source_version: BPCells docs version needs verification
source_accessed_at: 2026-05-25
source_local_paths: [seurat_tutorial/articles/seurat5_bpcells_interaction_vignette.html]
distillation_status: needs_version_check
---
# BPCells::open_matrix_anndata_hdf5

## API Entry Point

`BPCells::open_matrix_anndata_hdf5(path)`

## Method Family

Open an AnnData HDF5 matrix as BPCells matrix data.

## Required Object State

The h5ad file must contain a matrix layout supported by BPCells.

## Output State

A BPCells matrix object, not a complete AnnData-to-Seurat conversion.

## Important Parameters

Input path and matrix selection policy.

## Minimal Use

```r
mat <- BPCells::open_matrix_anndata_hdf5("data.h5ad")
```

## Validation Checks

Check matrix dimensions and confirm metadata expectations separately.

## Failure Modes

Unsupported h5ad layout, missing metadata, and feature/cell name mismatch.

## Statistical Caveats

Matrix import alone does not preserve full AnnData state.

## Adapter Notes

Record which h5ad matrix was consumed and which metadata was ignored or loaded
elsewhere.

## Sources Used

- Public docs: `https://bnprks.github.io/BPCells/reference/open_matrix_anndata_hdf5.html`.
- Local archive: `seurat_tutorial/articles/seurat5_bpcells_interaction_vignette.html`.
