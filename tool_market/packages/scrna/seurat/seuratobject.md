---
id: scrna.seurat.package.seuratobject
kind: package_ref
package: SeuratObject
import_name: SeuratObject
language: r
ecosystem: seurat
docs_local: seurat_tutorial
source_urls: [https://satijalab.github.io/seurat-object/]
source_version: local Seurat docs mirror label 5.4.0; local tutorial runtime observed separately
source_accessed_at: 2026-05-25
source_local_paths: [seurat_tutorial/articles/seurat5_essential_commands.html, seurat_tutorial/reference/seurat-class.html, seurat_tutorial/reference/assay-class.html]
distillation_status: needs_version_check
runtime_status: installed
workflow_stages: [00_state_inspection, 01_data_ingest, 04_normalization_transform, 07_batch_integration, 16_specialized_ecosystem]
install_probe: "R -q -e 'library(SeuratObject); packageVersion(\"SeuratObject\")'"
import_probe: "library(SeuratObject)"
---
# SeuratObject

## Role In Workflow

SeuratObject provides the Seurat object model: assays, assay layers, reductions,
graphs, images, metadata, identities, and object accessors.

## Supported Stages

It is required wherever Bioinfo-skills reads, validates, mutates, or serializes
a Seurat object.

## Required Object State

Wrappers should inspect assay names, active assay, layer availability,
reductions, graph names, metadata columns, and identity state before calling
analysis functions.

## Produced Object State

SeuratObject accessors create or modify object slots. Bioinfo-skills wrappers
must limit writes to approved slots and record the affected keys.

## Major API Families

Object accessors, assay accessors, metadata accessors, identity management, v3
and v5 assay creation, and object validation helpers.

## Runtime Availability

The local mirrored tutorial environment contains SeuratObject.

## Failure Modes

Assay v3/v5 confusion, active-assay mismatch, slot/layer name mismatch,
identity overwrite, and conversion loss when moving between ecosystems.

## Scientific Caveats

Object validity does not imply biological validity. It only proves that the
container state can support the requested analysis step.

## When To Avoid

Avoid low-level slot mutation when an accessor or approved wrapper can express
the intended state transition.

## Sources Used

- Public docs: `https://satijalab.github.io/seurat-object/`.
- Local archive: `seurat_tutorial/articles/seurat5_essential_commands.html`.
- Local archive: `seurat_tutorial/reference/seurat-class.html`.
