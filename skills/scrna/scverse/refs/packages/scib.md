---
id: scrna.scverse.package.scib
kind: package_ref
package: scib
import_name: scib
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/community/python/scib
source_urls: [https://scib.readthedocs.io/en/latest/user_guide.html, https://scib.readthedocs.io/en/latest/api.html]
source_version: Read the Docs latest archive; current runtime report marks import missing
source_accessed_at: 2026-05-23
source_local_paths: [bioinfo_tutorial/scverse_ecosystem/community/python/scib/scib.readthedocs.io/en/latest/user_guide.html, bioinfo_tutorial/scverse_ecosystem/community/python/scib/scib.readthedocs.io/en/latest/api.html]
distillation_status: distilled
runtime_status: missing
workflow_stages: ["16_specialized_ecosystem"]
install_probe: pending
import_probe: "import scib"
---
# scib

## Role In Scverse Workflow

scIB evaluates batch integration outputs using biological conservation and
batch-mixing metrics. It is a benchmarking package, not a default integration
method for production analysis.

## Supported Stages

- `16_specialized_ecosystem`: benchmark integration outputs and compare
  embeddings, graphs, or corrected feature matrices after the integration
  stage has produced candidate results.

## Required Object State

- Unintegrated and integrated AnnData objects with shared cell identities.
- Batch key and biological label key in `.obs`.
- Representation-specific state: embeddings in `.obsm`, graph connectivities
  in `.obsp`, or PCA/HVG state for feature-space metrics.
- Optional optimized cluster labels for NMI/ARI-style metrics.

## Produced Object State

- Metric tables as pandas data frames or report artifacts.
- Optional cluster labels from `cluster_optimal_resolution`.
- No biological state transition should be claimed from metrics alone.

## Major API Families

- Preprocessing: `scib.preprocessing.normalize`, `scale_batch`, `hvg_batch`.
- Integration wrappers: `scib.integration.bbknn`, `combat`, `harmony`, `mnn`,
  `scanorama`, `scvi`, `scanvi`, and related helpers.
- Metrics: `ari`, `nmi`, `silhouette`, `clisi_graph`, `ilisi_graph`, `kBET`,
  `graph_connectivity`, `pcr_comparison`, `hvg_overlap`.
- Wrappers: `scib.metrics.metrics`, `metrics_fast`, `metrics_slim`,
  `metrics_all`.

## Runtime Availability

Status is `missing` in the current repo runtime report:
`ModuleNotFoundError: No module named 'scib'`. Do not claim local execution
support until a fresh probe succeeds.

## Failure Modes

- Metrics fail when required keys or graph slots are absent.
- Label imbalance or sparse batches can make metric values unstable.
- Optional metric dependencies can be missing even when `scib` imports.
- Comparing objects with different cells or preprocessing histories invalidates
  scores.

## Scientific Caveats

- Integration metrics optimize tradeoffs; no single score proves the best
  biological analysis.
- Strong batch mixing can erase real biology when batch is confounded with
  condition or tissue.
- Benchmark labels inherit annotation uncertainty.

## When To Avoid

- Avoid as a substitute for checking marker biology and experimental design.
- Avoid ranking integrations when batch and biological labels are perfectly
  confounded.
- Avoid mixing metric results from different cell sets or preprocessing
  policies.

## Sources Used

- Public docs: `https://scib.readthedocs.io/en/latest/user_guide.html`.
- Public docs: `https://scib.readthedocs.io/en/latest/api.html`.
- Local archive: `bioinfo_tutorial/scverse_ecosystem/community/python/scib/`.
- Runtime report: `Bioinfo-skills/reports/runtime/scverse_runtime_status.tsv`.
