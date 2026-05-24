---
id: scrna.seurat.package.seuratdisk
kind: package_ref
package: SeuratDisk
import_name: SeuratDisk
language: r
ecosystem: seurat
docs_local: seurat_tutorial
source_urls: [https://mojaveazure.github.io/seurat-disk/]
source_commit: 877d4e18ab38c686f5db54f8cd290274ccdbe295
source_archive: https://github.com/mojaveazure/seurat-disk/archive/877d4e18ab38c686f5db54f8cd290274ccdbe295.tar.gz
source_version: local BPCells article uses SeuratDisk; runtime observed 0.0.0.9021
source_accessed_at: 2026-05-25
source_local_paths: [seurat_tutorial/articles/seurat5_bpcells_interaction_vignette.html]
distillation_status: distilled
runtime_status: installed
runtime_required: optional
install_route: source
source_install_script: scripts/install_seurat_source_packages.R
workflow_stages: [01_data_ingest, 16_specialized_ecosystem]
install_probe: "R -q -e 'library(SeuratDisk); packageVersion(\"SeuratDisk\")'"
import_probe: "library(SeuratDisk)"
---
# SeuratDisk

## Role In Scverse Workflow

SeuratDisk supports h5Seurat storage and Seurat/AnnData conversion workflows.

## Supported Stages

Use it for interoperability and file conversion after explicit state-loss review.

## Required Object State

The source object, target format, assay/layer mapping, embeddings, metadata, and
unsupported fields must be declared.

## Produced Object State

SeuratDisk can write h5Seurat files and convert between h5Seurat and h5ad.

## Major API Families

`SaveH5Seurat`, `LoadH5Seurat`, and `Convert`.

## Runtime Availability

SeuratDisk is source-route and optional, but the current relocated Seurat
tutorial runtime loads version `0.0.0.9021`. Reinstall or repair it with
`scripts/install_seurat_source_packages.R --packages=SeuratDisk` when
rebuilding the environment.

## Failure Modes

Unsupported object state, version incompatibility, lost graph or layer metadata,
and large-file I/O failures.

## Scientific Caveats

Conversion preserves containers only when mappings are explicit; it does not
validate analysis results.

## When To Avoid

Avoid conversion when critical object state cannot be represented in the target
format.

## Sources Used

- Public docs: `https://mojaveazure.github.io/seurat-disk/`.
- Local archive: `seurat_tutorial/articles/seurat5_bpcells_interaction_vignette.html`.
