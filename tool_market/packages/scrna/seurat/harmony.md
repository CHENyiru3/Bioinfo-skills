---
id: scrna.seurat.package.harmony
kind: package_ref
package: harmony
import_name: harmony
language: r
ecosystem: seurat
docs_local: seurat_tutorial
source_urls: [https://portals.broadinstitute.org/harmony/, https://github.com/immunogenomics/harmony]
source_version: local Seurat environment includes harmony; docs version needs verification
source_accessed_at: 2026-05-25
source_local_paths: [seurat_tutorial/environment.yml, seurat_tutorial/reference/harmonyintegration.html]
distillation_status: needs_version_check
runtime_status: installed
workflow_stages: [07_batch_integration, 08_neighbor_graph, 09_embedding_visualization]
install_probe: "R -q -e 'library(harmony); packageVersion(\"harmony\")'"
import_probe: "library(harmony)"
---
# harmony

## Role In Workflow

harmony provides a batch-integration backend used through Seurat integration
entrypoints or direct Harmony APIs.

## Supported Stages

Use it when the approved plan calls for Harmony integration and downstream graph
steps should consume the integrated reduction.

## Required Object State

The object needs a declared reduction, batch covariate, and reviewed integration
goal.

## Produced Object State

Harmony produces an integrated reduction that downstream graph, embedding, and
clustering steps can consume.

## Major API Families

Harmony matrix/reduction correction and Seurat integration helpers.

## Runtime Availability

The local mirrored tutorial environment contains harmony.

## Failure Modes

Missing batch column, overcorrection, incompatible reduction dimensions, and
comparison of integrated and unintegrated outputs without provenance.

## Scientific Caveats

Integration can remove technical variation and may also remove biological
variation if the design is confounded.

## When To Avoid

Avoid integration when batch is confounded with the biological condition and no
analysis plan defines the interpretation limits.

## Sources Used

- Public docs: `https://portals.broadinstitute.org/harmony/`.
- Public repository: `https://github.com/immunogenomics/harmony`.
- Local reference: `seurat_tutorial/reference/harmonyintegration.html`.
