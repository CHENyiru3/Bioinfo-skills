---
id: scrna.seurat.package.azimuth
kind: package_ref
package: Azimuth
import_name: Azimuth
language: r
ecosystem: seurat
docs_local: seurat_tutorial
source_urls: [https://github.com/satijalab/azimuth, https://azimuth.hubmapconsortium.org/references/]
source_commit: ad5929686e005ae91d8452187a3a1d8c0563fdd5
source_archive: https://github.com/satijalab/azimuth/archive/ad5929686e005ae91d8452187a3a1d8c0563fdd5.tar.gz
source_version: local Seurat install docs recommend Azimuth; runtime observed 0.5.1
source_accessed_at: 2026-05-25
source_local_paths: [seurat_tutorial/install_v5.html, seurat_tutorial/articles/seurat5_bpcells_interaction_vignette.html]
distillation_status: distilled
runtime_status: installed
runtime_required: optional
install_route: source
source_install_script: scripts/install_seurat_source_packages.R
workflow_stages: [12_annotation_support, 16_specialized_ecosystem]
install_probe: "R -q -e 'library(Azimuth); packageVersion(\"Azimuth\")'"
import_probe: "library(Azimuth)"
---
# Azimuth

## Role In Scverse Workflow

Azimuth supports reference mapping and local annotation workflows for scRNA-seq
and scATAC-seq queries.

## Supported Stages

Use it for annotation support only when a specific reference, species, and
mapping plan are approved.

## Required Object State

Input features, species, assay scale, and reference compatibility must be
verified before mapping.

## Produced Object State

Azimuth can add predicted labels, scores, embeddings, and reference-mapping
metadata to a Seurat object.

## Major API Families

Reference loading, query mapping, label transfer, and helper utilities used in
Seurat reference workflows.

## Runtime Availability

Azimuth is source-route and optional, but the current relocated Seurat tutorial
runtime loads version `0.5.1`. Reinstall or repair it with
`scripts/install_seurat_source_packages.R --packages=Azimuth` when rebuilding
the environment.

## Failure Modes

Large dependency stack, GitHub/API availability, reference downloads, species
mismatch, feature mismatch, and overconfident label transfer.

## Scientific Caveats

Reference mapping proposes labels; it does not replace marker review or expert
annotation.

## When To Avoid

Avoid Azimuth when reference provenance, species, or feature compatibility
cannot be established.

## Sources Used

- Public repository: `https://github.com/satijalab/azimuth`.
- Public references: `https://azimuth.hubmapconsortium.org/references/`.
- Local archive: `seurat_tutorial/install_v5.html`.
