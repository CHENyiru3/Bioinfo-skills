---
id: scrna.seurat.package.seuratdata
kind: package_ref
package: SeuratData
import_name: SeuratData
language: r
ecosystem: seurat
docs_local: seurat_tutorial
source_urls: [https://github.com/satijalab/seurat-data]
source_commit: 3e51f44303069b64f5dc4d68e6a3d4a343f55c39
source_archive: https://github.com/satijalab/seurat-data/archive/3e51f44303069b64f5dc4d68e6a3d4a343f55c39.tar.gz
source_version: local tutorial data usage; runtime observed 0.2.2.9002
source_accessed_at: 2026-05-25
source_local_paths: [seurat_tutorial/articles/spatial_vignette.html, seurat_tutorial/articles/integration_introduction.html, seurat_tutorial/articles/visualization_vignette.html]
distillation_status: distilled
runtime_status: installed
runtime_required: optional
install_route: source
source_install_script: scripts/install_seurat_source_packages.R
workflow_stages: [01_data_ingest]
install_probe: "R -q -e 'library(SeuratData); packageVersion(\"SeuratData\")'"
import_probe: "library(SeuratData)"
---
# SeuratData

## Role In Scverse Workflow

SeuratData loads tutorial and reference datasets used by Seurat vignettes.

## Supported Stages

Use it only for tutorial reproduction, fixtures, or examples where external
dataset downloads are approved.

## Required Object State

The dataset name and version must be declared, and large downloads must be
explicitly approved.

## Produced Object State

SeuratData returns prebuilt Seurat objects or dataset-specific objects.

## Major API Families

Dataset installation and dataset loading helpers.

## Runtime Availability

The local mirrored tutorial environment contains SeuratData, but dataset
packages are not part of the default Bioinfo-skills runtime.

## Failure Modes

Large network downloads, missing dataset packages, changed dataset versions, and
examples that silently depend on preinstalled data.

## Scientific Caveats

Tutorial datasets are not evidence for a user's experiment.

## When To Avoid

Avoid adding SeuratData dataset packages to the base runtime.

## Sources Used

- Public repository: `https://github.com/satijalab/seurat-data`.
- Local tutorial archives that call `InstallData` and `LoadData`.
