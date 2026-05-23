---
id: scrna.scverse.package.muon_tutorials
kind: package_ref
package: muon_tutorials
import_name: muon_tutorials
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/core/frameworks/muon_tutorials
source_url: https://muon-tutorials.readthedocs.io/en/latest/
source_urls: [https://muon-tutorials.readthedocs.io/en/latest/, https://muon.readthedocs.io/en/latest/, https://muon.readthedocs.io/en/latest/io/mudata.html]
source_version: muon tutorials latest docs and muon latest docs accessed 2026-05-23; runtime missing
source_accessed_at: 2026-05-23
distillation_status: distilled
runtime_status: missing
workflow_stages: ["16_specialized_ecosystem"]
install_probe: pending
import_probe: "import muon_tutorials"
---
# muon_tutorials

## Role In Scverse Workflow

`muon_tutorials` is documentation and example material for multimodal `muon`
workflows, not a primary analysis runtime for this skill tree. Treat it as a
source of examples for MuData, RNA+ATAC, CITE-seq, and MOFA-style workflows.

## Supported Stages

- `16_specialized_ecosystem`: tutorial reference for multimodal scverse
  workflows.

## Required Object State

- No object state is required to read the tutorials.
- Examples generally assume `muon.MuData` with modality-specific AnnData
  members in `.mod`, or AnnData objects prepared by Scanpy/muon steps.
- Workflow wrappers must depend on `muon` APIs directly, not on tutorial text.

## Produced Object State

- The tutorial package itself should not mutate workflow objects.
- Example workflows may produce MuData-level `.obs`, `.obsm`, modality `.obs`,
  modality `.var`, and `.h5mu` outputs when implemented with `muon`.

## Major API Families

- Tutorial pages for RNA+ATAC integration, CITE-seq integration, trimodal data,
  MEFISTO examples, and CLL analysis.
- Related runtime APIs live in `muon`, such as `muon.MuData`, `muon.pp`,
  `muon.tl`, `muon.atac`, and `muon.prot`.

## Runtime Availability

Status is `missing`. Do not import this package in workflow wrappers unless a
runtime report confirms that it exists and provides importable Python APIs.

## Failure Modes

- The import target may not correspond to an installable analysis package.
- Tutorials may lag current runtime behavior or depend on optional packages.
- Notebook examples can include hidden preprocessing assumptions.

## Scientific Caveats

- Tutorial examples are explanatory references, not validation evidence.
- Multimodal analyses require explicit modality alignment, feature provenance,
  and per-modality QC before claims are made.
- MOFA, WNN, and ATAC examples must be interpreted under their own method
  assumptions.

## When To Avoid

- Avoid using `muon_tutorials` as an executable dependency.
- Avoid copying tutorial notebooks into production wrappers without declaring
  object state, parameters, and validation checks.
- Avoid applying multimodal examples to single-modality AnnData objects.

## Sources Used

- Public docs: `https://muon-tutorials.readthedocs.io/en/latest/`.
- Public docs: `https://muon.readthedocs.io/en/latest/`.
- Public docs: `https://muon.readthedocs.io/en/latest/io/mudata.html`.
