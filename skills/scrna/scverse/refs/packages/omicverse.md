---
id: scrna.scverse.package.omicverse
kind: package_ref
package: omicverse
import_name: omicverse
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/community/python/omicverse
source_url: https://omicverse.readthedocs.io/en/latest/
source_urls: [https://omicverse.readthedocs.io/en/latest/, https://omicverse.readthedocs.io/en/latest/api/index.html, https://omicverse.readthedocs.io/en/latest/api/reference/omicverse.pp.qc.html]
source_version: OmicVerse v2 public docs; runtime report records package missing
source_accessed_at: 2026-05-23
distillation_status: distilled
runtime_status: missing
workflow_stages: ["16_specialized_ecosystem"]
install_probe: pending
import_probe: "import omicverse"
---
# omicverse

## Role In Scverse Workflow

OmicVerse is a broad Python framework for transcriptomics and multi-omics,
including single-cell, spatial, model-based, visualization, and AI-assisted
workflows. In this skill system it is a specialized umbrella toolkit and should
be routed to concrete APIs before execution.

## Supported Stages

- `16_specialized_ecosystem`: broad single-cell, spatial, bulk, multi-omics,
  annotation, trajectory, communication, enrichment, and visualization tasks
  when a specific OmicVerse API is selected.

## Required Object State

- AnnData, spatial object, count matrix, bulk matrix, or modality-specific
  input declared by the selected OmicVerse function.
- Explicit modality and task family because OmicVerse exposes many unrelated
  workflows.
- Required keys such as expression layer, `.obs` metadata, spatial coordinates,
  or external databases for the chosen method.

## Produced Object State

- Function-specific AnnData updates, returned AnnData, reports, plots, or
  external tool outputs.
- QC and preprocessing functions may filter cells or genes and write common
  preprocessing keys.
- Some modules wrap or orchestrate other packages and external resources.

## Major API Families

- `omicverse.io`: readers and writers for h5ad, 10x, spatial, and related
  inputs.
- `omicverse.pp`: QC, filtering, normalization, HVG, PCA, neighbors, clustering,
  embeddings, doublet detection, and GPU helpers.
- `omicverse.single`: annotation, integration, metacells, DE, GRN, trajectory,
  enrichment, velocity, and communication helpers.
- `omicverse.space`, `bulk`, `metabol`, `micro`, `pl`, and utilities for
  spatial, bulk, metabolomics, microbiome, plotting, and external lookups.

## Runtime Availability

Status: `missing`. The recorded runtime report shows `ModuleNotFoundError` for
`import omicverse`; use this ref for planning only until the environment is
updated.

## Failure Modes

- Selecting an OmicVerse wrapper without documenting the underlying method and
  required inputs.
- Heavy optional dependencies, GPU paths, R-backed tools, or external database
  downloads missing from the environment.
- Broad preprocessing helpers filtering or mutating AnnData more than intended.
- Version drift across wrapped packages.

## Scientific Caveats

- OmicVerse is an API collection; validity depends on the specific method used.
- Wrapper convenience does not remove the need for replicate-aware design,
  modality-appropriate preprocessing, or external validation.
- AI-assisted or external lookup outputs require provenance and review.

## When To Avoid

- Avoid as a generic replacement for narrower approved Scanpy or scverse tools.
- Avoid when the task cannot name a concrete OmicVerse function family.
- Avoid hidden multi-step workflows unless each state mutation is approved.

## Sources Used

- Public docs: `https://omicverse.readthedocs.io/en/latest/`.
- Public API docs: `https://omicverse.readthedocs.io/en/latest/api/index.html`.
- Public API docs: `https://omicverse.readthedocs.io/en/latest/api/reference/omicverse.pp.qc.html`.
- Runtime report: `reports/runtime/scverse_runtime_status.tsv`.
