---
id: scrna.scverse.package.muon
kind: package_ref
package: muon
import_name: muon
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/core/frameworks/muon
source_urls: [https://muon.readthedocs.io/en/latest/api/index.html, https://muon.readthedocs.io/en/latest/api/generated/muon.MuData.html, https://muon.readthedocs.io/en/latest/io/mudata.html]
source_version: muon latest docs archive; local runtime missing
source_accessed_at: 2026-05-23
source_local_paths: [bioinfo_tutorial/scverse_ecosystem/core/frameworks/muon/muon.readthedocs.io/en/latest/api/index.html, bioinfo_tutorial/scverse_ecosystem/core/frameworks/muon/muon.readthedocs.io/en/latest/api/generated/muon.MuData.html, bioinfo_tutorial/scverse_ecosystem/core/frameworks/muon/muon.readthedocs.io/en/latest/io/mudata.html]
distillation_status: distilled
runtime_status: missing
workflow_stages: ["16_specialized_ecosystem"]
install_probe: pending
import_probe: "import muon"
---
# muon

## Role In Scverse Workflow

muon provides multimodal analysis utilities around MuData, especially for
RNA plus ATAC or protein workflows. In this skill tree it is a specialized
ecosystem package for multimodal state handling and selected modality-aware
preprocessing, embedding, and visualization.

## Supported Stages

- `16_specialized_ecosystem`: multimodal workflows that require MuData,
  modality-specific preprocessing, or joint representations.

## Required Object State

- A MuData object, `.h5mu` file, or compatible single-modality inputs.
- Declared modality keys and cell alignment policy across modalities.
- For ATAC utilities, peak coordinates and any fragment/genome resources must
  be present and explicitly versioned.
- For protein utilities, protein-count source and normalization intent must be
  declared.

## Produced Object State

- Updated MuData or AnnData modality objects.
- Modality-specific normalized values, embeddings, neighbors, and annotations.
- Joint outputs such as MOFA, SNF, UMAP, Leiden/Louvain, or modality-specific
  ATAC/protein results when those tools are run.

## Major API Families

- Container and I/O: `muon.MuData`, `read_10x_h5`, `read_10x_mtx`.
- Multimodal preprocessing: `muon.pp.filter_obs`, `filter_var`,
  `intersect_obs`, `neighbors`, `l2norm`.
- Multimodal tools and plots: `muon.tl`, `muon.pl`, `muon.tl.mofa`,
  `muon.tl.snf`, `muon.tl.umap`.
- Modality modules: `muon.atac.pp`, `muon.atac.tl`, `muon.prot.pp`.

## Runtime Availability

Status is `missing` in `reports/runtime/scverse_runtime_status.tsv`; the import
probe failed with `ModuleNotFoundError: No module named 'muon'`. Treat muon refs
as docs-only until the runtime is rebuilt.

## Failure Modes

- Modality observations can be intersected or sampled in ways that change the
  analysis population.
- ATAC routines may require external genome, fragment, or peak resources that
  are not bundled with the object.
- Optional modeling or visualization dependencies may be unavailable even when
  `muon` imports.
- Joint embeddings can be dominated by one modality if scaling is not declared.

## Scientific Caveats

- Multimodal integration is sensitive to assay quality, feature selection, and
  modality weighting.
- ATAC, RNA, and protein matrices use different measurement models; do not use
  one normalization policy for all modalities by default.
- Joint clusters or embeddings are exploratory unless validated against the
  experimental design.

## When To Avoid

- Avoid when a single AnnData object and Scanpy workflow are sufficient.
- Avoid hidden modality intersection or filtering in downstream wrappers.
- Avoid using muon as a black-box multimodal integration step without recording
  modality weights, inputs, and output keys.

## Sources Used

- Public docs: `https://muon.readthedocs.io/en/latest/api/index.html`.
- Public docs: `https://muon.readthedocs.io/en/latest/api/generated/muon.MuData.html`.
- Public docs: `https://muon.readthedocs.io/en/latest/io/mudata.html`.
- Local archive: `bioinfo_tutorial/scverse_ecosystem/core/frameworks/muon/muon.readthedocs.io/en/latest/`.
- Runtime report: `reports/runtime/scverse_runtime_status.tsv`.
