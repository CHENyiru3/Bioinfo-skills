---
id: scrna.scverse.package.infercnvpy
kind: package_ref
package: infercnvpy
import_name: infercnvpy
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/community/python/infercnvpy
source_urls: [https://infercnvpy.readthedocs.io/en/latest/api.html, https://infercnvpy.readthedocs.io/en/latest/infercnv.html]
source_version: Read the Docs latest archive; current runtime report marks import missing
source_accessed_at: 2026-05-23
source_local_paths: [bioinfo_tutorial/scverse_ecosystem/community/python/infercnvpy/infercnvpy.readthedocs.io/en/latest/api.html, bioinfo_tutorial/scverse_ecosystem/community/python/infercnvpy/infercnvpy.readthedocs.io/en/latest/infercnv.html]
distillation_status: distilled
runtime_status: missing
workflow_stages: ["16_specialized_ecosystem"]
install_probe: pending
import_probe: "import infercnvpy"
---
# infercnvpy

## Role In Scverse Workflow

infercnvpy provides Scanpy-style tools for exploratory copy-number variation
inference from single-cell expression. It belongs in the specialized ecosystem
stage after QC, annotation, and tumor or normal reference policy are explicit.

## Supported Stages

- `16_specialized_ecosystem`: infer smoothed expression-based CNV profiles,
  CNV embeddings, CNV scores, and related plots.

## Required Object State

- AnnData with filtered cells and genes.
- Gene genomic positions in `.var` or retrievable from GTF/BioMart helpers.
- A declared expression layer or `.X` and a reference cell annotation in
  `.obs` when normal-cell references are used.
- Clear organism, chromosome naming, and tumor or normal category definitions.

## Produced Object State

- CNV matrix representations, typically in `.obsm`.
- CNV-derived PCA, neighbor, embedding, cluster, and score keys.
- Plot artifacts such as chromosome heatmaps and CNV embeddings.

## Major API Families

- I/O: `infercnvpy.io.genomic_position_from_biomart`,
  `genomic_position_from_gtf`, `read_scevan`.
- Preprocessing: `infercnvpy.pp.neighbors`.
- Tools: `infercnvpy.tl.infercnv`, `copykat`, `cnv_score`, `pca`, `umap`,
  `tsne`, `leiden`, `ithcna`, `ithgex`.
- Plotting: `infercnvpy.pl.chromosome_heatmap`, `chromosome_heatmap_summary`,
  `umap`, `tsne`.

## Runtime Availability

Status is `missing` in the current repo runtime report:
`ModuleNotFoundError: No module named 'infercnvpy'`. Do not claim local
availability without rerunning the runtime probe.

## Failure Modes

- Missing or inconsistent genomic coordinates prevent ordered CNV windows.
- Wrong reference categories can center tumor signal incorrectly.
- Very sparse expression or over-filtered genes can produce noisy CNV tracks.
- Large matrices can be slow or memory-heavy during smoothing and embedding.

## Scientific Caveats

- Expression-derived CNV is an inference from transcript abundance, not DNA copy
  number measurement.
- Immune activation, cell cycle, and tissue composition can mimic broad
  expression shifts.
- Results are most credible when compared with orthogonal CNV, histology, or
  known tumor annotations.

## When To Avoid

- Avoid for non-malignant datasets without a CNV-driven biological question.
- Avoid when normal reference cells are absent or poorly annotated.
- Avoid making clone-level claims from heatmaps alone.

## Sources Used

- Public docs: `https://infercnvpy.readthedocs.io/en/latest/api.html`.
- Public docs: `https://infercnvpy.readthedocs.io/en/latest/infercnv.html`.
- Local archive: `bioinfo_tutorial/scverse_ecosystem/community/python/infercnvpy/`.
- Runtime report: `Bioinfo-skills/reports/runtime/scverse_runtime_status.tsv`.
