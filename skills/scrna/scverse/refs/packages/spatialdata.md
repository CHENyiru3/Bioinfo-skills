---
id: scrna.scverse.package.spatialdata
kind: package_ref
package: spatialdata
import_name: spatialdata
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/core/data_structures/spatialdata
source_urls: [https://spatialdata.scverse.org/en/latest/api.html, https://spatialdata.scverse.org/en/latest/api/SpatialData.html, https://spatialdata.scverse.org/en/latest/api/transformations.html]
source_version: spatialdata latest docs archive 0.7.4.dev7+gd8bf26541; local runtime missing
source_accessed_at: 2026-05-23
source_local_paths: [bioinfo_tutorial/scverse_ecosystem/core/data_structures/spatialdata/spatialdata.scverse.org/en/latest/api.html, bioinfo_tutorial/scverse_ecosystem/core/data_structures/spatialdata/spatialdata.scverse.org/en/latest/api/SpatialData.html, bioinfo_tutorial/scverse_ecosystem/core/data_structures/spatialdata/spatialdata.scverse.org/en/latest/api/transformations.html]
distillation_status: distilled
runtime_status: missing
workflow_stages: ["16_specialized_ecosystem"]
install_probe: pending
import_probe: "import spatialdata"
---
# spatialdata

## Role In Scverse Workflow

SpatialData is the scverse container for spatial omics elements: images,
labels, shapes, points, tables, and coordinate transformations. In this tree it
is a specialized state container for spatial workflows before analysis tools
such as Squidpy or image-processing code are selected.

## Supported Stages

- `16_specialized_ecosystem`: spatial omics object construction, validation,
  coordinate-aware querying, and routing to spatial analysis packages.

## Required Object State

- A SpatialData object, readable SpatialData store, or declared spatial element
  inputs.
- Coordinate systems and transformations for each spatial element.
- Table annotations whose region and instance keys can be joined to spatial
  elements.
- For raster workflows, image scale and channel metadata must be known.

## Produced Object State

- SpatialData objects or Zarr-backed stores.
- Queried, transformed, aggregated, or subset spatial elements.
- Tables linked to spatial regions or labels; downstream statistical results
  are produced by separate analysis packages.

## Major API Families

- Object model: `spatialdata.SpatialData`.
- I/O and data formats for SpatialData stores.
- Operations, spatial queries, and aggregation utilities.
- Transformations and coordinate-system utilities.
- Element models for images, labels, shapes, points, and tables.

## Runtime Availability

Status is `missing` in `reports/runtime/scverse_runtime_status.tsv`; the import
probe failed with `ModuleNotFoundError: No module named 'spatialdata'`.

## Failure Modes

- Missing or incorrect transformations cause spatial overlays and joins to be
  wrong even when files load.
- Table keys may not map cleanly to region or label elements.
- Large image or label arrays can require chunked, lazy, or Zarr-backed access.
- Optional geospatial, image, or Dask dependencies can fail independently.

## Scientific Caveats

- Coordinate registration is a technical prerequisite, not biological evidence.
- Segmentation, spot assignment, and image-derived features can dominate
  downstream conclusions.
- SpatialData stores geometry and metadata; it does not test spatial biology by
  itself.

## When To Avoid

- Avoid for non-spatial AnnData workflows.
- Avoid if spatial coordinates are absent, untrusted, or not tied to expression
  observations.
- Avoid replacing statistical spatial analysis with object-format conversion.

## Sources Used

- Public docs: `https://spatialdata.scverse.org/en/latest/api.html`.
- Public docs: `https://spatialdata.scverse.org/en/latest/api/SpatialData.html`.
- Public docs: `https://spatialdata.scverse.org/en/latest/api/transformations.html`.
- Local archive: `bioinfo_tutorial/scverse_ecosystem/core/data_structures/spatialdata/spatialdata.scverse.org/en/latest/`.
- Runtime report: `reports/runtime/scverse_runtime_status.tsv`.
