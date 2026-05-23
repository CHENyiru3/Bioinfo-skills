---
id: scrna.scverse.package.hotspot
kind: package_ref
package: hotspot
import_name: hotspot
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/community/python/hotspot
source_url: https://hotspot.readthedocs.io/en/latest/
source_urls: [https://hotspot.readthedocs.io/en/latest/, https://hotspot.readthedocs.io/en/latest/hotspot.html]
source_version: Hotspot latest public docs; runtime report records package missing
source_accessed_at: 2026-05-23
distillation_status: distilled
runtime_status: missing
workflow_stages: ["16_specialized_ecosystem"]
install_probe: pending
import_probe: "import hotspot"
---
# hotspot

## Role In Scverse Workflow

Hotspot identifies informative genes and gene modules whose expression varies
locally over a chosen cell similarity metric. In this skill system it is a
specialized gene-program and spatial or lineage pattern analysis route.

## Supported Stages

- `16_specialized_ecosystem`: gene autocorrelation, local correlation, module
  discovery, and module scoring after the similarity metric is declared.

## Required Object State

- AnnData with cells by genes and raw or count-like data in `.X` or a declared
  layer.
- One cell similarity source: latent `.obsm` coordinates, `.obsp` distances, or
  a lineage tree.
- UMI count or size-factor metadata when depth-adjusted models are used.
- Gene subset and null model choice appropriate to the data type.

## Produced Object State

- Hotspot object with KNN graph, autocorrelation results, local-correlation
  matrix, module assignments, and module scores.
- Pandas DataFrames or Series for results that can be written to reports or
  AnnData by a wrapper.

## Major API Families

- `hotspot.Hotspot`: analysis object around AnnData and a similarity metric.
- `create_knn_graph`: builds the graph used for local statistics.
- `compute_autocorrelations` and `compute_local_correlations`: informative
  gene and gene-pair statistics.
- `create_modules`, `calculate_module_scores`, and plotting helpers.

## Runtime Availability

Status: `missing`. The recorded runtime report shows `ModuleNotFoundError` for
`import hotspot`; use this ref for planning only until the environment is
updated.

## Failure Modes

- Missing latent, distance, or tree input for cell similarity.
- Wrong expression source for the selected null model.
- Very large gene sets making local correlations expensive.
- Approximate neighbor, GPU, or dependency differences changing performance or
  reproducibility.

## Scientific Caveats

- Informative genes are defined relative to the chosen cell metric.
- Gene modules are local-correlation patterns, not necessarily regulatory
  modules.
- Spatial or lineage interpretation requires that the metric itself is valid.

## When To Avoid

- Avoid when no defensible cell similarity metric exists.
- Avoid using normalized or transformed values with a count-model assumption.
- Avoid treating module scores as condition-level differential expression.

## Sources Used

- Public docs: `https://hotspot.readthedocs.io/en/latest/`.
- Public function reference: `https://hotspot.readthedocs.io/en/latest/hotspot.html`.
- Runtime report: `reports/runtime/scverse_runtime_status.tsv`.
