---
id: scrna.seurat.package.presto
kind: package_ref
package: presto
import_name: presto
language: r
ecosystem: seurat
docs_local: seurat_tutorial
source_urls: [https://github.com/immunogenomics/presto]
source_version: local Seurat install docs recommend presto; package docs need verification
source_accessed_at: 2026-05-25
source_local_paths: [seurat_tutorial/install_v5.html, seurat_tutorial/articles/announcements.html]
distillation_status: needs_version_check
runtime_status: installed
workflow_stages: [11_marker_ranking]
install_probe: "R -q -e 'library(presto); packageVersion(\"presto\")'"
import_probe: "library(presto)"
---
# presto

## Role In Workflow

presto accelerates selected marker and differential-expression style tests used
by Seurat when available.

## Supported Stages

Use it as an optional performance dependency for descriptive marker ranking.

## Required Object State

Group labels and expression source must be declared before marker ranking.

## Produced Object State

presto produces test statistics and marker tables through Seurat-facing methods
or direct calls.

## Major API Families

Fast Wilcoxon/AUC marker-testing utilities.

## Runtime Availability

The local mirrored tutorial environment contains presto.

## Failure Modes

Missing package, incompatible sparse matrix type, unintended test selection, or
large memory use from coerced matrices.

## Scientific Caveats

Fast cell-level marker testing is descriptive and not a replicate-aware
condition-level differential expression design.

## When To Avoid

Avoid using presto as a substitute for sample-level pseudobulk or mixed-model
analysis when biological replicates and conditions are the question.

## Sources Used

- Public repository: `https://github.com/immunogenomics/presto`.
- Local archive: `seurat_tutorial/install_v5.html`.
- Local archive: `seurat_tutorial/articles/announcements.html`.
