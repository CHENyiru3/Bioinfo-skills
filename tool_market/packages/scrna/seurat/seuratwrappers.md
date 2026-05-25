---
id: scrna.seurat.package.seuratwrappers
kind: package_ref
package: SeuratWrappers
import_name: SeuratWrappers
language: r
ecosystem: seurat
docs_local: seurat_tutorial
source_urls: [https://github.com/satijalab/seurat-wrappers]
source_commit: ffaf74e306279b1ec16e31c9cb2142ebb2bc4bc1
source_archive: https://github.com/satijalab/seurat-wrappers/archive/ffaf74e306279b1ec16e31c9cb2142ebb2bc4bc1.tar.gz
source_version: local Seurat install docs recommend SeuratWrappers; runtime observed 0.4.0
source_accessed_at: 2026-05-25
source_local_paths: [seurat_tutorial/install_v5.html]
distillation_status: distilled
runtime_status: installed
runtime_required: optional
install_route: source
source_install_script: scripts/install_seurat_source_packages.R
workflow_stages: [07_batch_integration, 14_aggregation_pseudobulk_de, 16_specialized_ecosystem]
install_probe: "R -q -e 'library(SeuratWrappers); packageVersion(\"SeuratWrappers\")'"
import_probe: "library(SeuratWrappers)"
---
# SeuratWrappers

## Role In Scverse Workflow

SeuratWrappers exposes additional methods that integrate with Seurat objects.

## Supported Stages

Use it only when a specific method wrapper is chosen and documented as a tool
ref.

## Required Object State

The required assays, reductions, metadata, and external package dependencies
depend on the selected wrapper method.

## Produced Object State

Outputs vary by method and must be declared in the method-specific tool ref.

## Major API Families

Integration, trajectory, differential expression, and specialized method
bridges maintained outside Seurat core.

## Runtime Availability

The local mirrored tutorial environment contains SeuratWrappers.

## Failure Modes

Method-specific dependencies, changing APIs, and hidden assumptions inherited
from wrapped packages.

## Scientific Caveats

Each wrapped method has its own statistical assumptions and cannot be validated
by Seurat object compatibility alone.

## When To Avoid

Avoid generic SeuratWrappers use without a named method, tool ref, and runtime
probe for the wrapped dependency.

## Sources Used

- Public repository: `https://github.com/satijalab/seurat-wrappers`.
- Local archive: `seurat_tutorial/install_v5.html`.
