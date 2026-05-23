---
id: scrna.scverse.package.decoupler
kind: package_ref
package: decoupler
import_name: decoupler
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/core/frameworks/decoupler
source_urls: [https://decoupler.readthedocs.io/en/latest/api.html, https://decoupler.readthedocs.io/en/latest/api/mt.html, https://decoupler.readthedocs.io/en/latest/api/generated/decoupler.pp.pseudobulk.html]
source_version: decoupler latest docs archive 2.1.6; local runtime missing
source_accessed_at: 2026-05-23
source_local_paths: [bioinfo_tutorial/scverse_ecosystem/core/frameworks/decoupler/decoupler.readthedocs.io/en/latest/api.html, bioinfo_tutorial/scverse_ecosystem/core/frameworks/decoupler/decoupler.readthedocs.io/en/latest/api/mt.html, bioinfo_tutorial/scverse_ecosystem/core/frameworks/decoupler/decoupler.readthedocs.io/en/latest/api/generated/decoupler.pp.pseudobulk.html]
distillation_status: distilled
runtime_status: missing
workflow_stages: ["13_signature_scoring", "14_aggregation_pseudobulk_de", "16_specialized_ecosystem"]
install_probe: pending
import_probe: "import decoupler"
---
# decoupler

## Role In Scverse Workflow

decoupler infers pathway, transcription-factor, and gene-set activity from
omics matrices and prior-knowledge networks. It also provides pseudobulk and
filtering helpers that can feed replicate-aware differential workflows.

## Supported Stages

- `13_signature_scoring`: gene-set, regulator, pathway, and network activity
  scoring.
- `14_aggregation_pseudobulk_de`: pseudobulk aggregation and filtering before
  downstream differential analysis.
- `16_specialized_ecosystem`: OmniPath resource retrieval, benchmarking, and
  specialized enrichment workflows.

## Required Object State

- AnnData, DataFrame, or matrix with declared expression source and feature IDs.
- A network with source, target, and optional weight or sign columns whose
  target identifiers match matrix features.
- For pseudobulk, sample, group, and replicate metadata plus a true count
  source.

## Produced Object State

- Activity score matrices or AnnData annotations, commonly stored in declared
  `.obsm`, layer, or result-table keys by caller code.
- Pseudobulk AnnData or matrices with sample-level observations.
- Ranking, plotting, or benchmark outputs for networks and methods.

## Major API Families

- Methods: `decoupler.mt.ulm`, `mlm`, `ora`, `gsea`, `aucell`, `gsva`,
  `viper`, `zscore`, `consensus`, `decouple`.
- Resources: `decoupler.op.collectri`, `dorothea`, `progeny`, `hallmark`,
  `resource`, `translate`.
- Preprocessing: `decoupler.pp.pseudobulk`, `filter_samples`,
  `filter_by_expr`, `filter_by_prop`, `read_gmt`, `extract`.
- Tools and plotting: `decoupler.tl.rankby_group`, `rankby_obsm`,
  `decoupler.pl`, and benchmarking utilities.

## Runtime Availability

Status is `missing` in `reports/runtime/scverse_runtime_status.tsv`; the import
probe failed with `ModuleNotFoundError: No module named 'decoupler'`.

## Failure Modes

- Gene or identifier mismatches can leave too few targets per source.
- Sparse to dense conversion can cause memory failures.
- Online resource retrieval may fail or return different database versions.
- Pseudobulk aggregation is invalid if sample and group metadata are missing.

## Scientific Caveats

- Activity scores are model-derived summaries of target-gene patterns, not
  direct measurements of regulator activity.
- Prior-knowledge networks are incomplete and context dependent.
- Single-cell activity differences do not replace replicate-aware condition
  tests.

## When To Avoid

- Avoid when target overlap with the network is too small.
- Avoid if the network source, organism, and license cannot be recorded.
- Avoid pseudobulk or condition claims without biological replicates.

## Sources Used

- Public docs: `https://decoupler.readthedocs.io/en/latest/api.html`.
- Public docs: `https://decoupler.readthedocs.io/en/latest/api/mt.html`.
- Public docs: `https://decoupler.readthedocs.io/en/latest/api/generated/decoupler.pp.pseudobulk.html`.
- Local archive: `bioinfo_tutorial/scverse_ecosystem/core/frameworks/decoupler/decoupler.readthedocs.io/en/latest/`.
- Runtime report: `reports/runtime/scverse_runtime_status.tsv`.
