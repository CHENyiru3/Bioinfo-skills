---
id: scrna.scverse.package.schist
kind: package_ref
package: schist
import_name: schist
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/community/python/schist
source_url: https://schist.readthedocs.io/
source_urls: [https://schist.readthedocs.io/en/latest/readme.html, https://schist.readthedocs.io/en/latest/clustering_pbmc.html, https://schist.readthedocs.io/en/latest/autoapi/schist/tools/index.html]
source_version: schist 0.8.3 docs accessed 2026-05-23; runtime missing
source_accessed_at: 2026-05-23
distillation_status: distilled
runtime_status: missing
workflow_stages: ["16_specialized_ecosystem"]
install_probe: pending
import_probe: "import schist"
---
# schist

## Role In Scverse Workflow

schist provides a Scanpy-compatible interface to graph-tool stochastic block
model clustering on AnnData neighborhood graphs. It is a specialized clustering
and graph-interpretation package.

## Supported Stages

- `10_clustering`: nested stochastic block model clustering from a validated
  kNN graph.
- `12_annotation_support`: optional label-transfer utilities.
- `16_specialized_ecosystem`: schist-specific graph modeling and diagnostics.

## Required Object State

- AnnData with a precomputed neighborhood graph, usually from
  `scanpy.pp.neighbors`.
- The wrapper must declare `neighbors_key`, adjacency, direction, and weight
  handling.
- Plotting tree layouts require saved model state when graph-tool layouts are
  used.

## Produced Object State

- Model fitting writes nested cluster levels into `.obs`, commonly with
  `nsbm_level_*` names.
- Optional outputs include model state in `.uns`, cell marginals/affinities in
  `.obsm`, and stability or consistency metrics in `.obs`/`.uns`.
- Label transfer writes transferred labels into `.obs`.

## Major API Families

- Inference: `schist.inference.fit_model`.
- Graph tools: `calculate_affinity`, `cluster_consistency`,
  `cell_stability`, `cell_similarity`, `label_transfer`, `cr_lineages`.
- Plotting: hierarchy/alluvial/tree and graph layouts.
- Integration examples for Scanpy and CellRank objects.

## Runtime Availability

Status is `missing`. Runtime checks must confirm `import schist` and graph-tool
availability before use.

## Failure Modes

- graph-tool installation is platform-sensitive.
- Missing or mismatched neighbor graph keys stop inference.
- MCMC/inference can be slow and sensitive to graph construction choices.
- Large datasets may require sketching or alternate strategies.

## Scientific Caveats

- Block-model clusters describe graph structure, not automatically biological
  cell types.
- Results depend on preprocessing, dimensionality reduction, and kNN graph
  parameters.
- Hierarchical levels require interpretation against markers and metadata.

## When To Avoid

- Avoid when the neighborhood graph has not been validated.
- Avoid for very large datasets without an explicit scalability plan.
- Avoid treating hierarchy levels as annotations without biological review.

## Sources Used

- Public docs: `https://schist.readthedocs.io/en/latest/readme.html`.
- Public tutorial: `https://schist.readthedocs.io/en/latest/clustering_pbmc.html`.
- Public API docs: `https://schist.readthedocs.io/en/latest/autoapi/schist/tools/index.html`.
