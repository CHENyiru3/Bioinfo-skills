---
id: scrna.scverse.package.pyscenic
kind: package_ref
package: pyscenic
import_name: pyscenic
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/community/python/pyscenic
source_urls: [https://pyscenic.readthedocs.io/en/latest/index.html, https://pyscenic.readthedocs.io/en/latest/tutorial.html, https://pyscenic.readthedocs.io/en/latest/faq.html]
source_version: Read the Docs latest archive; current runtime report marks import missing
source_accessed_at: 2026-05-23
source_local_paths: [bioinfo_tutorial/scverse_ecosystem/community/python/pyscenic/pyscenic.readthedocs.io/en/latest/index.html, bioinfo_tutorial/scverse_ecosystem/community/python/pyscenic/pyscenic.readthedocs.io/en/latest/tutorial.html, bioinfo_tutorial/scverse_ecosystem/community/python/pyscenic/pyscenic.readthedocs.io/en/latest/faq.html]
distillation_status: distilled
runtime_status: missing
workflow_stages: ["16_specialized_ecosystem"]
install_probe: pending
import_probe: "import pyscenic"
---
# pyscenic

## Role In Scverse Workflow

pySCENIC runs SCENIC-style gene regulatory network inference, motif pruning,
and regulon activity scoring. It is a specialized regulatory analysis package
that usually consumes exported matrices rather than mutating AnnData directly.

## Supported Stages

- `16_specialized_ecosystem`: infer TF-target modules, prune by motif rankings,
  compute AUCell regulon activity, and import activity scores for downstream
  visualization or clustering.

## Required Object State

- Expression matrix with cells and genes, exported to loom or CSV-compatible
  formats when using the CLI.
- Species-appropriate TF list.
- cisTarget ranking databases and motif annotation tables matching the species
  and genome build.
- Optional AnnData object for re-importing AUCell scores into `.obsm` or
  `.obs`.

## Produced Object State

- GRN adjacency table from GENIE3 or GRNBoost2.
- Pruned motif enrichment table and regulon definitions.
- AUCell activity matrix, often written as loom output or imported into AnnData.
- Optional SCope-compatible loom artifacts.

## Major API Families

- CLI pipeline: `pyscenic grn`, `ctx`, `aucell`, and related export utilities.
- Python APIs: `arboreto.algo.grnboost2`, `modules_from_adjacencies`,
  `pyscenic.prune.prune2df`, `df2regulons`, `pyscenic.aucell.aucell`.
- Utilities for motif loading, regulon serialization, and loom export.

## Runtime Availability

Status is `missing` in the current repo runtime report:
`ModuleNotFoundError: No module named 'pyscenic'`. Also verify external ranking
database files before any execution plan.

## Failure Modes

- Missing Feather v2 ranking databases or motif annotations stop pruning.
- TF lists that do not match gene symbols lead to empty or sparse regulons.
- Dask or multiprocessing configuration can fail on constrained runtimes.
- Large expression matrices and repeated GRN runs are computationally
  expensive.

## Scientific Caveats

- GRN inference from expression is correlative and sensitive to sparsity.
- Motif pruning supports direct regulation hypotheses but does not prove TF
  binding in the assayed cells.
- AUCell scores are relative regulon activity summaries, not measured TF
  activity.

## When To Avoid

- Avoid when species-matched motif databases and TF lists are unavailable.
- Avoid on very small cell numbers or poorly normalized expression matrices.
- Avoid regulatory causality claims without perturbation or chromatin evidence.

## Sources Used

- Public docs: `https://pyscenic.readthedocs.io/en/latest/index.html`.
- Public docs: `https://pyscenic.readthedocs.io/en/latest/tutorial.html`.
- Public docs: `https://pyscenic.readthedocs.io/en/latest/faq.html`.
- Local archive: `bioinfo_tutorial/scverse_ecosystem/community/python/pyscenic/`.
- Runtime report: `Bioinfo-skills/reports/runtime/scverse_runtime_status.tsv`.
