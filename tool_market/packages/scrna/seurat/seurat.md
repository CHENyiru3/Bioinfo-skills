---
id: scrna.seurat.package.seurat
kind: package_ref
package: Seurat
import_name: Seurat
language: r
ecosystem: seurat
docs_local: seurat_tutorial
source_urls: [https://satijalab.org/seurat/, https://cran.r-project.org/package=Seurat]
source_version: local Seurat docs mirror label 5.4.0; local tutorial runtime observed separately
source_accessed_at: 2026-05-25
source_local_paths: [seurat_tutorial/index.html, seurat_tutorial/install_v5.html, seurat_tutorial/reference/seurat-package.html]
distillation_status: needs_version_check
runtime_status: installed
workflow_stages: [01_data_ingest, 02_qc_metrics_filtering, 04_normalization_transform, 05_feature_selection, 06_dimensionality_reduction, 07_batch_integration, 08_neighbor_graph, 09_embedding_visualization, 10_clustering, 11_marker_ranking, 12_annotation_support, 13_signature_scoring, 14_aggregation_pseudobulk_de, 16_specialized_ecosystem]
install_probe: "R -q -e 'library(Seurat); packageVersion(\"Seurat\")'"
import_probe: "library(Seurat)"
---
# Seurat

## Role In Workflow

Seurat is the primary R backend for single-cell object creation, preprocessing,
integration, graph analysis, clustering, visualization, marker ranking, and
specialized single-cell workflows. Bioinfo-skills should call Seurat through
approved tool refs and wrappers, not through ad hoc R snippets in adapters.

## Supported Stages

Seurat supports the core scRNA workflow from ingest through clustering and
marker ranking, plus multimodal, spatial, sketch, and integration workflows when
the optional package stack is available.

## Required Object State

Most APIs operate on a Seurat object with declared assays, layers, reductions,
graphs, identities, and metadata columns. Wrappers must name the assay/layer and
output keys they consume or mutate.

## Produced Object State

Seurat functions usually mutate or return Seurat objects with new assay layers,
reductions, graphs, metadata columns, or identity classes. Wrappers must record
package version, parameters, active assay, output keys, and replacement policy.

## Major API Families

Object creation and I/O, normalization and SCT, variable feature selection,
scaling, dimensionality reduction, graph construction, embedding, clustering,
marker ranking, integration, transfer mapping, visualization, and specialized
spatial/multimodal utilities.

## Runtime Availability

The local mirrored tutorial environment contains Seurat. Regenerate
`reports/runtime/seurat_runtime_status.*` in the target runtime before claiming
installed support elsewhere.

## Failure Modes

Hidden active-assay changes, overwritten reductions or metadata columns,
incompatible v3/v5 assay assumptions, missing optional dependencies, and
analysis choices embedded in adapters instead of wrappers.

## Scientific Caveats

Seurat provides analysis mechanics. It does not make clustering, annotation,
integration, or marker results biologically valid without state checks, design
review, metadata review, and appropriate statistical interpretation.

## When To Avoid

Avoid direct Seurat calls when the task needs AnnData-native processing, when
object conversion would lose required state, or when optional R dependencies
are unavailable and the method requires them.

## Sources Used

- Public docs: `https://satijalab.org/seurat/`.
- Public package page: `https://cran.r-project.org/package=Seurat`.
- Local archive: `seurat_tutorial/index.html`.
- Local archive: `seurat_tutorial/install_v5.html`.
- Local archive: `seurat_tutorial/reference/seurat-package.html`.
