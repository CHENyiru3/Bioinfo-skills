---
id: scrna.scverse.package.sincei
kind: package_ref
package: sincei
import_name: sincei
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/community/python/sincei
source_url: https://sincei.readthedocs.io/en/latest/
source_urls: [https://sincei.readthedocs.io/en/latest/, https://sincei.readthedocs.io/en/latest/content/tools/scCountReads.html, https://sincei.readthedocs.io/en/latest/content/tools/scBulkCoverage.html]
source_version: sincei 0.6.0 docs accessed 2026-05-23; runtime missing
source_accessed_at: 2026-05-23
distillation_status: distilled
runtime_status: missing
workflow_stages: ["16_specialized_ecosystem"]
install_probe: pending
import_probe: "import sincei"
---
# sincei

## Role In Scverse Workflow

sinCEI is a toolkit for QC, counting, clustering, plotting, and coverage
generation in single-cell epigenomics workflows. It is primarily file and CLI
oriented rather than an AnnData-first scRNA package.

## Supported Stages

- `16_specialized_ecosystem`: single-cell epigenomics workflows from BAM,
  barcode, count, and coverage files.

## Required Object State

- Aligned BAM files or fragment/read files with cell barcodes.
- Barcode whitelist, grouping tables, genomic bins, or feature definitions as
  required by the selected command.
- For clustering or coverage steps, prior count matrices or per-cell grouping
  output from earlier sinCEI commands.

## Produced Object State

- Count matrices, QC/filter statistics, clustering coordinates, grouping TSVs,
  and coverage tracks such as bigWig or bedGraph.
- Outputs are file artifacts; any AnnData conversion must be a separate,
  declared adapter step.

## Major API Families

- Barcode and read filtering: `scFilterBarcodes`, `scFilterStats`.
- Counting and QC: `scCountReads`, `scCountQC`, `scCombineCounts`.
- Epigenomic features: `scFindVCRs`, `scScoreFeatures`.
- Clustering and plotting: `scClusterCells` and related visualization outputs.
- Coverage generation: `scBulkCoverage`.

## Runtime Availability

Status is `missing`. Runtime checks must confirm command availability and
Python import behavior before wrappers select sinCEI.

## Failure Modes

- BAM/barcode naming mismatches can produce empty or misassigned matrices.
- Genome-bin or feature definitions can be inconsistent with alignment
  reference names.
- Coverage outputs require valid grouping tables.
- CLI dependencies and file indexing can fail outside a prepared environment.

## Scientific Caveats

- sinCEI outputs describe chromatin or epigenomic signal, not transcript
  abundance.
- Gene activity scores are proxy features and should not be interpreted as
  measured RNA expression.
- QC thresholds and feature bins must be assay- and genome-specific.

## When To Avoid

- Avoid for standard scRNA AnnData workflows.
- Avoid when only processed expression matrices are available.
- Avoid mixing sinCEI file outputs into AnnData without an explicit schema and
  provenance conversion.

## Sources Used

- Public docs: `https://sincei.readthedocs.io/en/latest/`.
- Public tool docs: `https://sincei.readthedocs.io/en/latest/content/tools/scCountReads.html`.
- Public tool docs: `https://sincei.readthedocs.io/en/latest/content/tools/scBulkCoverage.html`.
