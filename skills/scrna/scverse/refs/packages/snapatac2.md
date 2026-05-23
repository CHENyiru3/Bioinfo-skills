---
id: scrna.scverse.package.snapatac2
kind: package_ref
package: snapatac2
import_name: snapatac2
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/core/frameworks/snapatac2
source_url: https://scverse.org/SnapATAC2/
source_urls: [https://scverse.org/SnapATAC2/, https://scverse.org/SnapATAC2/api/index.html, https://scverse.org/SnapATAC2/tutorials/pbmc.html]
source_version: SnapATAC2 2.9.0 docs and 2.8.0 tutorial pages accessed 2026-05-23; runtime missing
source_accessed_at: 2026-05-23
distillation_status: distilled
runtime_status: missing
workflow_stages: ["16_specialized_ecosystem"]
install_probe: pending
import_probe: "import snapatac2"
---
# snapatac2

## Role In Scverse Workflow

SnapATAC2 is a Python/Rust single-cell epigenomics framework with backed
AnnData support, fragment import, scATAC preprocessing, embedding, clustering,
peak analysis, and regulatory analyses.

## Supported Stages

- `16_specialized_ecosystem`: scATAC and related single-cell omics workflows.
- It has ATAC-specific analogs for QC, feature selection, doublet filtering,
  dimensionality reduction, graph building, embedding, clustering, marker
  region analysis, and differential accessibility.

## Required Object State

- Fragment files, BAM-derived fragment files, or SnapATAC2 AnnData/AnnDataSet
  objects.
- Genome chromosome sizes and any blacklist/whitelist resources must match the
  reference assembly.
- Downstream steps require declared matrices, selected features, and embeddings
  such as spectral coordinates when used.

## Produced Object State

- `pp.import_fragments` can create in-memory or backed AnnData with fragment
  metadata and QC fields.
- Tile, peak, and gene matrices add or return AnnData objects with `.obs`,
  `.var`, `.obsm`, and `.uns` outputs.
- Tools write spectral embeddings, UMAP, clusters, peak calls, marker regions,
  differential tests, motif results, and aggregate matrices.

## Major API Families

- Data structures and I/O: `AnnDataSet`, `read`, `read_mtx`,
  `read_10x_mtx`, `read_dataset`, `concat`.
- Preprocessing: `pp.make_fragment_file`, `pp.import_fragments`,
  `pp.add_tile_matrix`, `pp.make_peak_matrix`, `pp.make_gene_matrix`,
  `pp.filter_cells`, `pp.select_features`, `pp.knn`, `pp.scrublet`.
- Tools: `tl.spectral`, `tl.umap`, `tl.leiden`, `tl.macs3`,
  `tl.marker_regions`, `tl.diff_test`, motif and network helpers.
- Metrics and plotting: TSSE, FRiP, fragment sizes, UMAP and QC plots.

## Runtime Availability

Status is `missing`. Runtime checks must confirm `import snapatac2`, Rust-backed
extension availability, and optional external tools before execution.

## Failure Modes

- Fragment sorting, barcode whitelists, or genome naming mismatches can corrupt
  cell-level counts.
- Backed mode changes mutation and I/O behavior relative to in-memory AnnData.
- Peak calling and motif analysis require external resources or tools.
- Large fragment files can exhaust disk or temporary storage.

## Scientific Caveats

- Accessibility and gene activity are not direct measurements of transcript
  abundance.
- TSS enrichment, FRiP, and fragment thresholds are assay- and dataset-specific.
- Differential accessibility and motif enrichment need design-aware
  interpretation.

## When To Avoid

- Avoid for ordinary scRNA-only workflows.
- Avoid when raw fragments/BAMs or genome resources are unavailable.
- Avoid mixing ATAC-derived gene activity with RNA expression without labeling
  the feature source.

## Sources Used

- Public docs: `https://scverse.org/SnapATAC2/`.
- Public API docs: `https://scverse.org/SnapATAC2/api/index.html`.
- Public tutorial: `https://scverse.org/SnapATAC2/tutorials/pbmc.html`.
