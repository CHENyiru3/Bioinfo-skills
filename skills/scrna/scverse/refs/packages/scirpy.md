---
id: scrna.scverse.package.scirpy
kind: package_ref
package: scirpy
import_name: scirpy
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/core/frameworks/scirpy
source_urls: [https://scirpy.scverse.org/en/latest/api.html, https://scirpy.scverse.org/en/latest/data-structure.html, https://scirpy.scverse.org/en/latest/generated/scirpy.io.read_airr.html]
source_version: scirpy latest docs archive 0.24.1.dev2+g38f05cdaa; local runtime missing
source_accessed_at: 2026-05-23
source_local_paths: [bioinfo_tutorial/scverse_ecosystem/core/frameworks/scirpy/scirpy.scverse.org/en/latest/api.html, bioinfo_tutorial/scverse_ecosystem/core/frameworks/scirpy/scirpy.scverse.org/en/latest/data-structure.html, bioinfo_tutorial/scverse_ecosystem/core/frameworks/scirpy/scirpy.scverse.org/en/latest/generated/scirpy.io.read_airr.html]
distillation_status: distilled
runtime_status: missing
workflow_stages: ["16_specialized_ecosystem"]
install_probe: pending
import_probe: "import scirpy"
---
# scirpy

## Role In Scverse Workflow

Scirpy analyzes single-cell immune receptor data, including AIRR, TCR, and BCR
rearrangements. It is used when receptor contigs must be merged with expression
state, indexed, compared, and summarized as clonotypes or repertoires.

## Supported Stages

- `16_specialized_ecosystem`: immune-receptor data ingestion, chain QC,
  clonotype calling, distance calculation, clonal expansion, and repertoire
  summaries.

## Required Object State

- AnnData or MuData with AIRR/VDJ records aligned to cell barcodes.
- Valid receptor chain fields, productive-chain calls, CDR3 sequences, and loci.
- Optional expression AnnData state if receptor annotations are merged with
  transcriptomic clusters or embeddings.

## Produced Object State

- AIRR annotations in the Scirpy data structure.
- Chain indices, receptor QC labels, immune-receptor distance matrices,
  clonotype or clonotype-cluster labels, and repertoire summaries.
- Plot-ready summaries for clonal expansion, overlap, modularity, and usage.

## Major API Families

- I/O: `scirpy.io.read_airr`, `read_10x_vdj`, `read_h5ad`, `read_h5mu`,
  AIRR conversion helpers.
- Preprocessing: `scirpy.pp.index_chains`, `merge_airr`, `ir_dist`.
- Tools: `scirpy.tl.chain_qc`, `define_clonotypes`,
  `define_clonotype_clusters`, `clonal_expansion`, `repertoire_overlap`.
- Distance utilities: `scirpy.ir_dist.sequence_dist` and distance calculators.
- Plotting: `scirpy.pl` repertoire and clonotype visualizations.

## Runtime Availability

Status is `missing` in `reports/runtime/scverse_runtime_status.tsv`; the import
probe failed with `ModuleNotFoundError: No module named 'scirpy'`.

## Failure Modes

- Cell barcodes may not match between VDJ and expression objects.
- AIRR schema fields or chain annotations can be incomplete or inconsistent.
- Sequence distance calculations can be expensive for large repertoires.
- Optional GPU or alignment accelerators may be absent.

## Scientific Caveats

- Clonotype definitions depend on chain choice, CDR3 similarity metric, and
  threshold policy.
- Repertoire overlap and expansion are sample-design dependent.
- TCR/BCR sequence similarity does not by itself prove shared antigen response.

## When To Avoid

- Avoid when receptor contigs are absent or barcode linkage is unreliable.
- Avoid patient, clone, or antigen claims without replicate and metadata
  support.
- Avoid merging receptor state into expression data without recording barcode
  matching and filtering policy.

## Sources Used

- Public docs: `https://scirpy.scverse.org/en/latest/api.html`.
- Public docs: `https://scirpy.scverse.org/en/latest/data-structure.html`.
- Public docs: `https://scirpy.scverse.org/en/latest/generated/scirpy.io.read_airr.html`.
- Local archive: `bioinfo_tutorial/scverse_ecosystem/core/frameworks/scirpy/scirpy.scverse.org/en/latest/`.
- Runtime report: `reports/runtime/scverse_runtime_status.tsv`.
