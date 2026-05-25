---
id: scrna.seurat.package.bpcells
kind: package_ref
package: BPCells
import_name: BPCells
language: r
ecosystem: seurat
docs_local: seurat_tutorial
source_urls: [https://bnprks.github.io/BPCells/, https://satijalab.org/seurat/articles/seurat5_bpcells_interaction_vignette.html]
source_version: local Seurat docs mirror label 5.4.0; BPCells docs version needs verification
source_accessed_at: 2026-05-25
source_local_paths: [seurat_tutorial/articles/seurat5_bpcells_interaction_vignette.html, seurat_tutorial/articles/seurat5_sketch_analysis.html]
distillation_status: needs_version_check
runtime_status: installed
workflow_stages: [01_data_ingest, 05_feature_selection, 16_specialized_ecosystem]
install_probe: "R -q -e 'library(BPCells); packageVersion(\"BPCells\")'"
import_probe: "library(BPCells)"
---
# BPCells

## Role In Workflow

BPCells provides on-disk matrix storage and scalable matrix I/O used by Seurat
large-data and sketch workflows.

## Supported Stages

Use it for large matrix ingest, on-disk count storage, sketch workflows, and
memory-aware Seurat object construction.

## Required Object State

The source matrix or on-disk matrix directory must be declared, stable, and
compatible with the target Seurat assay.

## Produced Object State

BPCells functions can produce on-disk matrix directories and Seurat assays whose
counts are backed by BPCells matrices.

## Major API Families

10x HDF5 reads, h5ad matrix reads, matrix directory reads/writes, and on-disk
matrix operations consumed by Seurat.

## Runtime Availability

The local mirrored tutorial environment contains BPCells.

## Failure Modes

Missing on-disk directories, moved matrix paths, unsupported h5ad layout,
filesystem permission errors, and performance regressions from accidental
in-memory conversion.

## Scientific Caveats

On-disk backing changes scale and storage behavior, not the biological meaning
of downstream results.

## When To Avoid

Avoid BPCells when small in-memory matrices are simpler, when path portability
cannot be maintained, or when a downstream method cannot consume BPCells-backed
layers.

## Sources Used

- Public docs: `https://bnprks.github.io/BPCells/`.
- Local archive: `seurat_tutorial/articles/seurat5_bpcells_interaction_vignette.html`.
- Local archive: `seurat_tutorial/articles/seurat5_sketch_analysis.html`.
