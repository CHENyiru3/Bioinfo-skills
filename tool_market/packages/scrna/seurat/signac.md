---
id: scrna.seurat.package.signac
kind: package_ref
package: Signac
import_name: Signac
language: r
ecosystem: seurat
docs_local: seurat_tutorial
source_urls: [https://stuartlab.org/signac/]
source_version: local Seurat docs mirror label 5.4.0; Signac docs version needs verification
source_accessed_at: 2026-05-25
source_local_paths: [seurat_tutorial/articles/seurat5_atacseq_integration_vignette.html, seurat_tutorial/articles/weighted_nearest_neighbor_analysis.html]
distillation_status: needs_version_check
runtime_status: installed
workflow_stages: [01_data_ingest, 07_batch_integration, 12_annotation_support, 16_specialized_ecosystem]
install_probe: "R -q -e 'library(Signac); packageVersion(\"Signac\")'"
import_probe: "library(Signac)"
---
# Signac

## Role In Workflow

Signac extends Seurat for scATAC-seq and chromatin modality analysis.

## Supported Stages

Use it for ATAC ingest, gene activity, motif analysis, multimodal integration,
and WNN-style workflows when ATAC state is present.

## Required Object State

ATAC assays require feature ranges, fragment or count state, genome annotation,
and modality metadata.

## Produced Object State

Signac can create chromatin assays, gene activity assays, motif state,
reductions, and modality-specific metadata.

## Major API Families

Chromatin assay construction, gene activity, motif analysis, fragment handling,
and ATAC visualization utilities.

## Runtime Availability

The local mirrored tutorial environment contains Signac.

## Failure Modes

Missing genome annotation packages, incompatible genome build, absent fragment
files, and loss of feature-range metadata during conversion.

## Scientific Caveats

Gene activity and motif results are model-based summaries and need modality
specific interpretation.

## When To Avoid

Avoid Signac when no ATAC/chromatin modality exists or when genome annotations
cannot be matched to the data.

## Sources Used

- Public docs: `https://stuartlab.org/signac/`.
- Local archive: `seurat_tutorial/articles/seurat5_atacseq_integration_vignette.html`.
- Local archive: `seurat_tutorial/articles/weighted_nearest_neighbor_analysis.html`.
