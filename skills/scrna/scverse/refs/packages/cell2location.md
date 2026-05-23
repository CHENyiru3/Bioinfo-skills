---
id: scrna.scverse.package.cell2location
kind: package_ref
package: cell2location
import_name: cell2location
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/community/python/cell2location
source_urls: [https://cell2location.readthedocs.io/en/latest/cell2location.reference_models.html, https://cell2location.readthedocs.io/en/latest/cell2location.html, https://cell2location.readthedocs.io/en/latest/commonerrors.html]
source_version: Read the Docs latest archive; current runtime report marks import missing
source_accessed_at: 2026-05-23
source_local_paths: [bioinfo_tutorial/scverse_ecosystem/community/python/cell2location/cell2location.readthedocs.io/en/latest/cell2location.reference_models.html, bioinfo_tutorial/scverse_ecosystem/community/python/cell2location/cell2location.readthedocs.io/en/latest/cell2location.html, bioinfo_tutorial/scverse_ecosystem/community/python/cell2location/cell2location.readthedocs.io/en/latest/commonerrors.html]
distillation_status: distilled
runtime_status: missing
workflow_stages: ["16_specialized_ecosystem"]
install_probe: pending
import_probe: "import cell2location"
---
# cell2location

## Role In Scverse Workflow

cell2location maps single-cell reference signatures onto spatial transcriptomic
locations with Bayesian models. It is a specialized spatial deconvolution tool
used after single-cell reference annotation and spatial data QC.

## Supported Stages

- `16_specialized_ecosystem`: learn reference signatures, map cell abundance
  into spatial locations, and run downstream co-location models.

## Required Object State

- Reference AnnData with raw count-like expression and cell type labels.
- Spatial AnnData with count-like expression, spatial coordinates, sample keys
  when applicable, and genes aligned to the reference signatures.
- Prior choices such as expected cells per location and batch/sample policy.

## Produced Object State

- Reference expression signatures as data frames or model outputs.
- Spatial posterior summaries for cell abundance, commonly stored in `.obsm`
  and `.uns`.
- Optional downstream co-location or archetypal analysis outputs.

## Major API Families

- Reference models: negative-binomial regression models for cell type
  signatures.
- Spatial model: cell2location location models with `setup_anndata`, `train`,
  and posterior export workflows.
- Downstream models: co-located group NMF and archetypal analysis.
- Utilities and plotting for filtering, posterior inspection, and spatial maps.

## Runtime Availability

Status is `missing` in the current repo runtime report:
`ModuleNotFoundError: No module named 'cell2location'`. Do not claim Pyro,
scvi-tools, or GPU availability for this package from docs alone.

## Failure Modes

- Pyro/scvi-tools or CUDA stack mismatches can prevent import or training.
- Poor reference coverage can cause NaNs, bad fits, or misleading abundance
  estimates.
- Gene mismatch between reference and spatial data can remove informative
  markers.
- Training can be slow or memory-heavy, especially with many locations,
  signatures, or samples.

## Scientific Caveats

- Cell abundance estimates are posterior model summaries, not direct cell
  counts.
- Priors such as `N_cells_per_location` influence absolute abundance scale.
- Spatial spots may contain mixtures, ambient RNA, and platform-specific
  effects not represented by the reference.

## When To Avoid

- Avoid without a comprehensive, tissue-matched reference.
- Avoid when spatial data lack count-like values or reliable sample metadata.
- Avoid absolute abundance claims without histology or orthogonal calibration.

## Sources Used

- Public docs: `https://cell2location.readthedocs.io/en/latest/cell2location.reference_models.html`.
- Public docs: `https://cell2location.readthedocs.io/en/latest/cell2location.html`.
- Public docs: `https://cell2location.readthedocs.io/en/latest/commonerrors.html`.
- Local archive: `bioinfo_tutorial/scverse_ecosystem/community/python/cell2location/`.
- Runtime report: `Bioinfo-skills/reports/runtime/scverse_runtime_status.tsv`.
