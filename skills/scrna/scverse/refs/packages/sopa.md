---
id: scrna.scverse.package.sopa
kind: package_ref
package: sopa
import_name: sopa
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/community/python/sopa
source_url: https://gustaveroussy.github.io/sopa/
source_urls: [https://gustaveroussy.github.io/sopa/, https://gustaveroussy.github.io/sopa/tutorials/api_usage/, https://gustaveroussy.github.io/sopa/api/segmentation/, https://gustaveroussy.github.io/sopa/api/aggregation/]
source_version: Sopa docs accessed 2026-05-23; runtime missing
source_accessed_at: 2026-05-23
distillation_status: distilled
runtime_status: missing
workflow_stages: ["16_specialized_ecosystem"]
install_probe: pending
import_probe: "import sopa"
---
# sopa

## Role In Scverse Workflow

Sopa is a spatial omics processing and analysis toolkit built on SpatialData. It
supports image-based and spatial-transcriptomics workflows with segmentation,
aggregation, and spatial operations.

## Supported Stages

- `16_specialized_ecosystem`: SpatialData-based spatial omics preprocessing,
  segmentation, aggregation, and analysis.

## Required Object State

- `SpatialData` object with technology-specific images, transcripts, points,
  labels, shapes, or tables.
- Segmentation requires declared image channels, diameter/model settings, and
  optional tissue masks.
- Aggregation requires valid cell boundaries or labels and transcript/channel
  elements.

## Produced Object State

- Segmentation adds shapes or labels containing cell/tissue boundaries to
  SpatialData.
- Aggregation creates an AnnData table of features per cell and stores it in
  the SpatialData object.
- Spatial operations may add derived geometries, patches, tables, or exported
  artifacts for visualization.

## Major API Families

- Readers for supported spatial technologies.
- Patches and tiling for large images.
- Segmentation: `sopa.segmentation.cellpose`, `stardist`, `baysor`, `comseg`,
  `proseg`, tissue and custom segmentation helpers.
- Aggregation: `sopa.aggregate` and technology-specific feature aggregation.
- CLI, API, and Snakemake pipeline entry points.

## Runtime Availability

Status is `missing`. Runtime checks must confirm `import sopa`, SpatialData, and
selected segmentation extras before execution.

## Failure Modes

- Missing optional extras such as Cellpose, StarDist, or transcript-based
  segmenters can disable selected methods.
- Incorrect channel names, scale transforms, or coordinate systems can make
  segmentation/aggregation invalid.
- Large images can fail on memory, cache, or disk limits.
- Aggregation can produce misleading tables when boundaries are poor.

## Scientific Caveats

- Segmentation quality is a major determinant of downstream single-cell spatial
  claims.
- SpatialData coordinate systems and transformations must be preserved.
- Aggregated cell tables are derived from spatial boundaries, not independent
  single-cell capture events.

## When To Avoid

- Avoid for non-spatial scRNA AnnData workflows.
- Avoid when image channels, transcripts, or coordinate systems are not
  available or not trusted.
- Avoid using aggregation output without segmentation QC.

## Sources Used

- Public docs: `https://gustaveroussy.github.io/sopa/`.
- Public tutorial: `https://gustaveroussy.github.io/sopa/tutorials/api_usage/`.
- Public API docs: `https://gustaveroussy.github.io/sopa/api/segmentation/`.
- Public API docs: `https://gustaveroussy.github.io/sopa/api/aggregation/`.
