---
id: scrna.scverse.package.squidpy
kind: package_ref
package: squidpy
import_name: squidpy
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/core/frameworks/squidpy
source_urls: [https://squidpy.readthedocs.io/en/stable/api.html, https://squidpy.readthedocs.io/en/stable/api/squidpy.gr.spatial_neighbors.html, https://squidpy.readthedocs.io/en/stable/classes/squidpy.im.ImageContainer.html]
source_version: squidpy stable docs archive 1.8.0; local runtime missing
source_accessed_at: 2026-05-23
source_local_paths: [bioinfo_tutorial/scverse_ecosystem/core/frameworks/squidpy/squidpy.readthedocs.io/en/stable/api.html, bioinfo_tutorial/scverse_ecosystem/core/frameworks/squidpy/squidpy.readthedocs.io/en/stable/api/squidpy.gr.spatial_neighbors.html, bioinfo_tutorial/scverse_ecosystem/core/frameworks/squidpy/squidpy.readthedocs.io/en/stable/classes/squidpy.im.ImageContainer.html]
distillation_status: distilled
runtime_status: missing
workflow_stages: ["16_specialized_ecosystem"]
install_probe: pending
import_probe: "import squidpy"
---
# squidpy

## Role In Scverse Workflow

Squidpy provides spatial molecular analysis for AnnData and related spatial
objects. It is used for spatial neighbor graphs, neighborhood enrichment,
spatial autocorrelation, image containers, image features, and spatial plots.

## Supported Stages

- `16_specialized_ecosystem`: spatial transcriptomics and spatial image
  analysis after coordinates, images, and cluster or feature keys are validated.

## Required Object State

- AnnData with spatial coordinates, usually `obsm["spatial"]`, or compatible
  spatial table state.
- For graph statistics, a valid cluster, group, or feature key in `.obs` or
  `.var`.
- For image workflows, image data and library identifiers must match the
  expression observations.

## Produced Object State

- Spatial graph matrices such as spatial connectivities and distances.
- Results in `.uns` for neighborhood enrichment, co-occurrence, interaction,
  autocorrelation, ligand-receptor, or related spatial summaries.
- Optional image features, segmentations, or crops written to declared AnnData
  keys or image containers.

## Major API Families

- Reading: `squidpy.read.visium`, `vizgen`, `nanostring`.
- Graph statistics: `squidpy.gr.spatial_neighbors`, `nhood_enrichment`,
  `co_occurrence`, `centrality_scores`, `interaction_matrix`, `ripley`,
  `spatial_autocorr`, `ligrec`, `sepal`.
- Image: `squidpy.im.ImageContainer`, `process`, `segment`,
  `calculate_image_features`.
- Plotting and tools: `squidpy.pl`, `squidpy.tl`, and bundled datasets.

## Runtime Availability

Status is `missing` in `reports/runtime/scverse_runtime_status.tsv`; the import
probe failed with `ModuleNotFoundError: No module named 'squidpy'`.

## Failure Modes

- Missing or mis-scaled spatial coordinates produce invalid neighborhoods.
- Cluster keys, library IDs, or image keys can be absent or misaligned.
- Permutation-based spatial tests may be slow or unstable on very large data.
- Optional image and segmentation dependencies may be absent.

## Scientific Caveats

- Spatial enrichment and autocorrelation depend strongly on neighborhood
  definition and tissue sampling density.
- Ligand-receptor or co-occurrence outputs are hypotheses, not direct evidence
  of physical interaction.
- Image-derived features inherit segmentation and staining artifacts.

## When To Avoid

- Avoid when no trusted spatial coordinates or image metadata are present.
- Avoid comparing spatial statistics across samples without harmonized
  neighborhood definitions and replicate-aware design.
- Avoid using plotting output as the only support for spatial biological claims.

## Sources Used

- Public docs: `https://squidpy.readthedocs.io/en/stable/api.html`.
- Public docs: `https://squidpy.readthedocs.io/en/stable/api/squidpy.gr.spatial_neighbors.html`.
- Public docs: `https://squidpy.readthedocs.io/en/stable/classes/squidpy.im.ImageContainer.html`.
- Local archive: `bioinfo_tutorial/scverse_ecosystem/core/frameworks/squidpy/squidpy.readthedocs.io/en/stable/`.
- Runtime report: `reports/runtime/scverse_runtime_status.tsv`.
