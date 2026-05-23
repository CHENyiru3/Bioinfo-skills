---
id: scrna.scverse.package.episcanpy
kind: package_ref
package: episcanpy
import_name: episcanpy
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/community/python/episcanpy
source_url: https://episcanpy.readthedocs.io/en/latest/
source_urls: [https://episcanpy.readthedocs.io/en/latest/, https://episcanpy.readthedocs.io/en/latest/basic_usage.html, https://episcanpy.readthedocs.io/en/latest/api/]
source_version: epiScanpy 0.2.0+66.g32c2282 public docs; runtime report records package missing
source_accessed_at: 2026-05-23
distillation_status: distilled
runtime_status: missing
workflow_stages: ["16_specialized_ecosystem"]
install_probe: pending
import_probe: "import episcanpy"
---
# episcanpy

## Role In Scverse Workflow

epiScanpy extends Scanpy-style workflows to single-cell epigenomic data such as
scATAC-seq and single-cell DNA methylation. In this skill system it is a
specialized epigenomics route, not a default scRNA-seq tool.

## Supported Stages

- `16_specialized_ecosystem`: epigenomic matrix construction, preprocessing,
  clustering, embedding, feature ranking, and gene-activity workflows.

## Required Object State

- AnnData containing cells by epigenomic features, or input files and feature
  annotations for building count matrices.
- Declared modality, such as open chromatin or methylation, because count and
  methylation values have different meanings.
- Metadata for batches, cell annotations, or conditions if downstream
  comparisons are planned.

## Produced Object State

- AnnData objects with epigenomic counts, methylation values, binarized
  matrices, selected variable features, PCA, neighbors, embeddings, clusters,
  ranked features, or gene activity matrices.
- Plots parallel to selected preprocessing and tools functions.

## Major API Families

- `episcanpy.api.ct`: feature loading and count-matrix construction.
- `episcanpy.api.pp`: filtering, coverage, binarization, imputation,
  normalization, PCA, neighbors, and lazy preprocessing.
- `episcanpy.api.tl`: ranking features, gene activity, embeddings,
  clustering, trajectories, and cluster metrics.
- `episcanpy.api.pl`: plotting utilities parallel to `pp` and `tl`.

## Runtime Availability

Status: `missing`. The recorded runtime report shows `ModuleNotFoundError` for
`import episcanpy`; use this ref for planning only until the environment is
updated.

## Failure Modes

- Using RNA-oriented assumptions on sparse epigenomic matrices.
- Missing genome annotations, feature coordinates, or modality-specific count
  semantics.
- Dense conversion or imputation causing memory pressure.
- Version age and compatibility drift with current Scanpy or AnnData.

## Scientific Caveats

- Open chromatin, methylation, and gene activity are indirect regulatory
  measurements and should not be treated as expression.
- Differential openness or methylation needs replicate-aware design outside
  simple cluster summaries.
- Feature-to-gene mapping can be ambiguous.

## When To Avoid

- Avoid for ordinary scRNA-seq workflows when Scanpy covers the task.
- Avoid when the epigenomic feature annotation or genome build is unknown.
- Avoid mixing methylation levels and count matrices without explicit modality
  handling.

## Sources Used

- Public docs: `https://episcanpy.readthedocs.io/en/latest/`.
- Public usage principles: `https://episcanpy.readthedocs.io/en/latest/basic_usage.html`.
- Public API docs: `https://episcanpy.readthedocs.io/en/latest/api/`.
- Runtime report: `reports/runtime/scverse_runtime_status.tsv`.
