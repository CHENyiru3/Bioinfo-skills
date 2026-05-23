---
id: scrna.scverse.package.scvelo
kind: package_ref
package: scvelo
import_name: scvelo
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/community/python/scvelo
source_urls: [https://scvelo.readthedocs.io/en/stable/api.html, https://scvelo.readthedocs.io/en/stable/VelocityBasics.html, https://scvelo.readthedocs.io/en/stable/DynamicalModeling.html]
source_version: scvelo stable docs archive; local runtime missing
source_accessed_at: 2026-05-23
source_local_paths: [bioinfo_tutorial/scverse_ecosystem/community/python/scvelo/scvelo.readthedocs.io/en/stable/api.html, bioinfo_tutorial/scverse_ecosystem/community/python/scvelo/scvelo.readthedocs.io/en/stable/VelocityBasics.html, bioinfo_tutorial/scverse_ecosystem/community/python/scvelo/scvelo.readthedocs.io/en/stable/DynamicalModeling.html]
distillation_status: distilled
runtime_status: missing
workflow_stages: ["15_trajectory_fate_velocity"]
install_probe: pending
import_probe: "import scvelo"
---
# scvelo

## Role In Scverse Workflow

scVelo estimates RNA velocity from spliced and unspliced counts and projects
velocity-derived transitions onto embeddings or trajectory summaries. It belongs
only in the trajectory, fate, and velocity stage after object state is verified.

## Supported Stages

- `15_trajectory_fate_velocity`: RNA velocity preprocessing, velocity
  estimation, velocity graph construction, latent time, terminal states, and
  velocity visualization.

## Required Object State

- AnnData with `layers["spliced"]` and `layers["unspliced"]` from a valid
  velocity-count workflow.
- Feature filtering, normalization, PCA or neighbor graph state, and moment
  calculation appropriate for the chosen model.
- Existing embedding and cluster keys when plotting or grouping velocity
  summaries.

## Produced Object State

- Moment layers such as `Ms` and `Mu`.
- Velocity estimates in a velocity layer and velocity graph state.
- Velocity embeddings in `.obsm`, latent time or pseudotime in `.obs`, and
  rankings or summaries in `.uns`.

## Major API Families

- Preprocessing: `scvelo.pp.filter_genes`, `normalize_per_cell`,
  `filter_and_normalize`, `moments`.
- Velocity tools: `scvelo.tl.velocity`, `velocity_graph`,
  `recover_dynamics`, `latent_time`, `terminal_states`,
  `rank_velocity_genes`, `rank_dynamical_genes`.
- Plotting: `scvelo.pl.velocity_embedding`, `velocity_embedding_grid`,
  `velocity_embedding_stream`, phase portraits, and heatmaps.
- Utilities: `scvelo.utils.merge`, `get_transition_matrix`, `get_df`.

## Runtime Availability

Status is `missing` in `reports/runtime/scverse_runtime_status.tsv`; the import
probe failed with `ModuleNotFoundError: No module named 'scvelo'`.

## Failure Modes

- Missing or poor-quality spliced/unspliced layers make velocity invalid.
- Dynamical model fitting can fail or produce unstable parameters.
- Velocity graph computation can be slow and memory intensive.
- Incompatible Scanpy, AnnData, or dependency versions can break imports or
  plotting.

## Scientific Caveats

- RNA velocity depends on kinetic assumptions and capture of unspliced RNA.
- Directionality is model-based and should not be interpreted as lineage proof.
- Cell-cycle, stress, or technical variation can dominate velocity fields.

## When To Avoid

- Avoid without validated spliced and unspliced count layers.
- Avoid if the biological system violates velocity assumptions or lacks a
  plausible dynamic process.
- Avoid condition-level claims from velocity plots alone.

## Sources Used

- Public docs: `https://scvelo.readthedocs.io/en/stable/api.html`.
- Public docs: `https://scvelo.readthedocs.io/en/stable/VelocityBasics.html`.
- Public docs: `https://scvelo.readthedocs.io/en/stable/DynamicalModeling.html`.
- Local archive: `bioinfo_tutorial/scverse_ecosystem/community/python/scvelo/scvelo.readthedocs.io/en/stable/`.
- Runtime report: `reports/runtime/scverse_runtime_status.tsv`.
