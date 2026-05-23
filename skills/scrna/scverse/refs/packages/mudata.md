---
id: scrna.scverse.package.mudata
kind: package_ref
package: mudata
import_name: mudata
language: python
ecosystem: scverse
docs_local: BioBrain/reference/scverse_docs/mudata_docs
source_urls: [https://mudata.readthedocs.io/en/stable/api.html, https://mudata.readthedocs.io/en/stable/generated/mudata.MuData.html, https://mudata.readthedocs.io/en/stable/io/mudata.html]
source_version: mudata stable docs archive 0.1.dev60+g2eaa318f6; local runtime missing
source_accessed_at: 2026-05-23
source_local_paths: [BioBrain/reference/scverse_docs/mudata_docs/mudata.readthedocs.io/stable/api.html, BioBrain/reference/scverse_docs/mudata_docs/mudata.readthedocs.io/stable/generated/mudata.MuData.html, BioBrain/reference/scverse_docs/mudata_docs/mudata.readthedocs.io/stable/io/mudata.html]
distillation_status: distilled
runtime_status: missing
workflow_stages: ["00_state_inspection", "16_specialized_ecosystem"]
install_probe: pending
import_probe: "import mudata"
---
# mudata

## Role In Scverse Workflow

mudata provides the MuData container and `.h5mu` I/O for multimodal omics.
It is a state container, not an integration method: stage skills must still
decide how modalities are normalized, aligned, and interpreted.

## Supported Stages

- `00_state_inspection`: inspect `.h5mu` structure, modality keys, and shared
  observation state.
- `16_specialized_ecosystem`: route multimodal workflows that need modality
  containers before analysis-specific tools are chosen.

## Required Object State

- A readable MuData object or `.h5mu` file, or AnnData objects to combine.
- Declared modality names under `.mod`, such as RNA, ATAC, protein, or AIRR.
- Cell and feature identifiers whose axis relationship is known; do not assume
  all modalities share all observations or variables.

## Produced Object State

- A MuData object with modality-specific AnnData objects in `.mod`.
- Shared and modality-specific annotations in MuData and AnnData slots.
- Optional `.h5mu`, `.zarr`, or converted AnnData outputs when explicitly
  requested.

## Major API Families

- Container: `mudata.MuData`.
- I/O: `read`, `read_h5mu`, `read_zarr`, `write`, `write_h5mu`, `write_zarr`.
- Conversion: `to_mudata`, `to_anndata`, `read_h5ad`, `read_anndata`.
- Combination and extension: `concat`, `register_mudata_namespace`.

## Runtime Availability

Status is `missing` in `reports/runtime/scverse_runtime_status.tsv`; the import
probe failed with `ModuleNotFoundError: No module named 'mudata'`. Recheck the
intended runtime before executing any MuData workflow.

## Failure Modes

- Modality observations are not synchronized, producing silent join mistakes.
- Conversion to AnnData can flatten or drop modality-specific information.
- Large multimodal objects may exceed memory when read fully rather than backed
  or chunked.
- Modality key collisions or ambiguous axis annotations make downstream routing
  unsafe.

## Scientific Caveats

- A valid MuData object does not prove modalities are biologically aligned.
- Shared cell barcodes are not sufficient evidence that assays have comparable
  noise models or normalization requirements.
- MuData stores state; it does not select multimodal integration parameters.

## When To Avoid

- Avoid for single-modality data where AnnData is enough.
- Avoid using MuData conversion as a substitute for explicit modality mapping.
- Avoid writing `.h5mu` outputs until modality naming and axis policy are
  recorded.

## Sources Used

- Public docs: `https://mudata.readthedocs.io/en/stable/api.html`.
- Public docs: `https://mudata.readthedocs.io/en/stable/generated/mudata.MuData.html`.
- Public docs: `https://mudata.readthedocs.io/en/stable/io/mudata.html`.
- Local archive: `BioBrain/reference/scverse_docs/mudata_docs/mudata.readthedocs.io/stable/`.
- Runtime report: `reports/runtime/scverse_runtime_status.tsv`.
