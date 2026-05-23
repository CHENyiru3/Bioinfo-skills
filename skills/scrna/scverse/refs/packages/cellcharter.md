---
id: scrna.scverse.package.cellcharter
kind: package_ref
package: cellcharter
import_name: cellcharter
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/community/python/cellcharter
source_url: https://cellcharter.readthedocs.io/en/latest/
source_urls: [https://cellcharter.readthedocs.io/en/latest/, https://cellcharter.readthedocs.io/en/latest/generated/cellcharter.gr.aggregate_neighbors.html, https://cellcharter.readthedocs.io/en/latest/generated/cellcharter.tl.Cluster.html]
source_version: cellcharter latest public docs; runtime report records package missing
source_accessed_at: 2026-05-23
distillation_status: distilled
runtime_status: missing
workflow_stages: ["16_specialized_ecosystem"]
install_probe: pending
import_probe: "import cellcharter"
---
# cellcharter

## Role In Scverse Workflow

CellCharter identifies and characterizes spatial domains from spatial -omics
data by combining intrinsic cell features with neighborhood context. In this
skill system it is a specialized spatial clustering route.

## Supported Stages

- `16_specialized_ecosystem`: spatial domain discovery, characterization, and
  comparison after spatial graph and feature choices are approved.

## Required Object State

- AnnData with spatial features in `.X` or a declared `.obsm` representation.
- Spatial connectivity graph in `.obsp` or enough spatial coordinates to build
  one upstream.
- `sample_key` when multiple samples are present.
- Batch-aware latent representation if cross-sample domain calling is intended.

## Produced Object State

- Neighborhood-aggregated feature representation, commonly under an `.obsm`
  key such as `X_cellcharter`.
- Spatial domain labels from GMM clustering.
- Domain characterization outputs such as enrichment, boundaries, proportions,
  and shape metrics.

## Major API Families

- `cellcharter.gr`: aggregate neighbors and graph enrichment utilities.
- `cellcharter.tl.Cluster` and `ClusterAutoK`: spatial domain clustering.
- `cellcharter.tl`: boundaries, shape metrics, and TRVAE support.
- `cellcharter.pl`: stability, enrichment, boundary, and proportion plots.

## Runtime Availability

Status: `missing`. The recorded runtime report shows `ModuleNotFoundError` for
`import cellcharter`; use this ref for planning only until the environment is
updated.

## Failure Modes

- Missing or inconsistent spatial graph keys.
- Multiple samples analyzed without a valid `sample_key`.
- Domain labels driven by batch, tissue section, or segmentation artifacts.
- GPU, PyTorch, or optional dimensionality-reduction dependencies unavailable.

## Scientific Caveats

- Spatial domains are model-derived neighborhoods, not directly observed tissue
  compartments.
- Domain number and covariance assumptions affect results.
- Cross-sample comparisons require matched tissue context and batch handling.

## When To Avoid

- Avoid when spatial coordinates or neighborhood graph are absent.
- Avoid when segmentation or registration quality is unresolved.
- Avoid using domain labels as final biology without marker, morphology, or
  pathology validation.

## Sources Used

- Public docs: `https://cellcharter.readthedocs.io/en/latest/`.
- Public API docs: `https://cellcharter.readthedocs.io/en/latest/generated/cellcharter.gr.aggregate_neighbors.html`.
- Public API docs: `https://cellcharter.readthedocs.io/en/latest/generated/cellcharter.tl.Cluster.html`.
- Runtime report: `reports/runtime/scverse_runtime_status.tsv`.
