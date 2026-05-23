---
id: scrna.scverse.package.dandelion
kind: package_ref
package: dandelion
import_name: dandelion
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/community/python/dandelion
source_url: https://sc-dandelion.readthedocs.io/en/latest/
source_urls: [https://sc-dandelion.readthedocs.io/en/latest/, https://sc-dandelion.readthedocs.io/en/latest/api.html, https://sc-dandelion.readthedocs.io/en/latest/notebooks/1_dandelion_preprocessing-10x_data.html]
source_version: dandelion latest public docs; runtime report records package missing
source_accessed_at: 2026-05-23
distillation_status: distilled
runtime_status: missing
workflow_stages: ["16_specialized_ecosystem"]
install_probe: pending
import_probe: "import dandelion"
---
# dandelion

## Role In Scverse Workflow

dandelion analyzes single-cell BCR/TCR V(D)J data and integrates repertoire
outputs with Scanpy and AnnData. In this skill system it is a specialized
immune-repertoire route.

## Supported Stages

- `16_specialized_ecosystem`: V(D)J preprocessing, clonotype analysis,
  repertoire summaries, and AnnData integration.

## Required Object State

- AIRR-compatible rearrangement files or supported platform outputs such as
  10x Cell Ranger V(D)J files.
- Optional paired gene-expression AnnData with matching cell barcodes.
- External tools and reference databases when reannotation with IgBLAST or
  related preprocessing is requested.
- Sample or donor metadata for clone overlap, diversity, and pseudobulk tasks.

## Produced Object State

- `Dandelion` objects, AIRR/10x-compatible tables, or `.h5ddl` files.
- AnnData `.obs` fields for contig, productivity, clone, isotype, and receptor
  summaries after transfer.
- Repertoire networks, clone diversity, overlap, pseudobulk, and plots.

## Major API Families

- `dandelion.pp`: FASTA formatting, gene reannotation, isotype assignment, and
  contig checks.
- `dandelion.io`: read AIRR, 10x, platform-specific, `.ddl`, and `.h5ddl`
  formats.
- `dandelion.tl`: clone definition, networks, diversity, overlap, transfer,
  pseudobulk, and scirpy conversion.
- `dandelion.pl`: repertoire and clone visualizations.

## Runtime Availability

Status: `missing`. The recorded runtime report shows `ModuleNotFoundError` for
`import dandelion`; use this ref for planning only until the environment is
updated.

## Failure Modes

- Cell barcode prefixes or suffixes do not match gene-expression AnnData.
- Missing IgBLAST, germline, or BLAST database paths for reannotation.
- Insufficient contigs for reliable clone or allele assignment.
- Mixed samples without donor-aware grouping.

## Scientific Caveats

- Clonotype definitions are parameterized and not universally interchangeable.
- Productive contigs and clone expansion do not prove antigen specificity.
- Repertoire diversity needs sample-level design and depth awareness.

## When To Avoid

- Avoid when no immune-receptor sequencing data are present.
- Avoid merging V(D)J and GEX outputs before barcode identity is checked.
- Avoid comparing clone diversity across samples without depth and donor
  controls.

## Sources Used

- Public docs: `https://sc-dandelion.readthedocs.io/en/latest/`.
- Public API docs: `https://sc-dandelion.readthedocs.io/en/latest/api.html`.
- Public preprocessing guide: `https://sc-dandelion.readthedocs.io/en/latest/notebooks/1_dandelion_preprocessing-10x_data.html`.
- Runtime report: `reports/runtime/scverse_runtime_status.tsv`.
