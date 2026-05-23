---
id: scrna.scverse.package.bento
kind: package_ref
package: bento
import_name: bento
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/community/python/bento
source_url: https://bento-tools.readthedocs.io/en/latest/
source_urls: [https://bento-tools.readthedocs.io/en/latest/, https://bento-tools.readthedocs.io/en/latest/api.html, https://bento-tools.readthedocs.io/en/latest/howitworks.html]
source_version: bento-tools latest public docs; runtime report records package missing
source_accessed_at: 2026-05-23
distillation_status: distilled
runtime_status: missing
workflow_stages: ["16_specialized_ecosystem"]
install_probe: pending
import_probe: "import bento"
---
# bento

## Role In Scverse Workflow

Bento supports subcellular spatial transcriptomics analysis on `SpatialData`
objects. In this skill system it is a specialized spatial package for
cell-centric molecule, shape, RNA localization, and colocalization summaries.

## Supported Stages

- `16_specialized_ecosystem`: route only after spatial objects, segmentation,
  molecule coordinates, and biological question are explicit.

## Required Object State

- `SpatialData` object with aligned points, shapes, labels, images, and an
  AnnData table as needed.
- Spatial indices prepared before Bento tools are run.
- Cell, nucleus, or other region boundaries matched to molecule coordinates.

## Produced Object State

- Updated `SpatialData` metadata and tables with composition, point-feature,
  shape-feature, RNAflux, RNAforest, or RNAcoloc results.
- Optional static plots for spatial points, shapes, embeddings, and summaries.

## Major API Families

- `bento.io`: preparation and SpatialData compatibility.
- `bento.tl`: composition, point features, shape statistics, RNAflux,
  RNAforest, and colocalization tools.
- `bento.pl`: spatial and result plotting.
- `bento.ut` and `bento.geo`: data access and geometric operations.

## Runtime Availability

Status: `missing`. The recorded runtime report shows `ModuleNotFoundError` for
`import bento`; use this ref for planning only until the environment is updated.

## Failure Modes

- Missing or inconsistent SpatialData coordinate systems.
- Unprepared spatial indices or mismatched cell boundaries and molecule points.
- Segmentation errors propagating into cell-centric summaries.
- Large point or shape collections causing memory or runtime pressure.

## Scientific Caveats

- Subcellular localization summaries depend on assay resolution and
  segmentation quality.
- Spatial enrichment or colocalization is descriptive unless paired with a
  suitable experimental design.
- Shape and molecule features do not by themselves identify cell state or
  causal regulation.

## When To Avoid

- Avoid when data are only cell-by-gene counts without spatial coordinates or
  region geometry.
- Avoid when segmentation, registration, or coordinate transforms have not been
  validated.
- Avoid making mechanistic claims from visualization-only outputs.

## Sources Used

- Public docs: `https://bento-tools.readthedocs.io/en/latest/`.
- Public API docs: `https://bento-tools.readthedocs.io/en/latest/api.html`.
- Data model notes: `https://bento-tools.readthedocs.io/en/latest/howitworks.html`.
- Runtime report: `reports/runtime/scverse_runtime_status.tsv`.
