---
id: scrna.scverse.package.dynamo
kind: package_ref
package: dynamo
import_name: dynamo
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/community/python/dynamo
source_url: https://dynamo-release.readthedocs.io/en/latest/
source_urls: [https://dynamo-release.readthedocs.io/en/latest/, https://dynamo-release.readthedocs.io/en/latest/api/user.html, https://dynamo-release.readthedocs.io/en/latest/api/reference/dynamo.tl.cell_velocities.html, https://dynamo-release.readthedocs.io/en/stable/tutorials/notebooks/202_extvelo.html]
source_version: dynamo latest public docs; runtime report records package missing
source_accessed_at: 2026-05-23
distillation_status: distilled
runtime_status: missing
workflow_stages: ["15_trajectory_fate_velocity"]
install_probe: pending
import_probe: "import dynamo"
---
# dynamo

## Role In Scverse Workflow

dynamo models expression dynamics, RNA velocity, vector fields, potential
landscapes, trajectories, and perturbation predictions. In this skill system it
belongs to trajectory, fate, and velocity analysis after object state is
explicit.

## Supported Stages

- `15_trajectory_fate_velocity`: RNA velocity, vector-field reconstruction,
  fate prediction, differential geometry, and perturbation-oriented dynamics.

## Required Object State

- AnnData or loom-derived object with raw and processed expression layers.
- For velocity, compatible spliced, unspliced, labeling, protein, or imported
  velocity layers declared by key.
- Neighbor graph, PCA or embedding keys, and dynamics metadata as required by
  the selected method.
- Transition gene masks or criteria for selecting velocity genes.

## Produced Object State

- AnnData updates in `.obs`, `.var`, `.layers`, `.obsm`, `.obsp`, and `.uns`
  for preprocessing, moments, dynamics, velocities, transition matrices, and
  vector fields.
- Plots for velocity, vector fields, topography, fate, and perturbation.

## Major API Families

- `dynamo.pp`: preprocessing, filtering, normalization, scaling, PCA, and
  recipes.
- `dynamo.tl`: neighbors, moments, dynamics, velocities, clustering,
  pseudotime, and markers.
- `dynamo.vf`: vector fields, fixed points, Jacobian, divergence, curl, and
  related differential-geometry tools.
- `dynamo.pd`, `dynamo.pl`, `dynamo.mv`, and `dynamo.sim`: fate, perturbation,
  plotting, animation, and simulations.

## Runtime Availability

Status: `missing`. The recorded runtime report shows `ModuleNotFoundError` for
`import dynamo`; use this ref for planning only until the environment is
updated.

## Failure Modes

- Missing or inconsistent velocity layers and dynamics metadata.
- Dimension mismatch among expression, velocity, and embedding matrices.
- Invalid neighbor graph or transition genes with no velocity data.
- Optional methods needing numba, GPU, or external velocity packages not
  available.

## Scientific Caveats

- Velocity and vector-field directions are model estimates, not observed cell
  trajectories.
- Kinetic assumptions differ across conventional, splicing, metabolic-labeling,
  and external velocity workflows.
- Fate or perturbation predictions need independent validation.

## When To Avoid

- Avoid when only static expression is available and no valid velocity or
  dynamics model is justified.
- Avoid hidden preprocessing that changes layers before trajectory review.
- Avoid interpreting arrows or streamlines without checking model fit and
  transition genes.

## Sources Used

- Public docs: `https://dynamo-release.readthedocs.io/en/latest/`.
- Public API docs: `https://dynamo-release.readthedocs.io/en/latest/api/user.html`.
- Public API docs: `https://dynamo-release.readthedocs.io/en/latest/api/reference/dynamo.tl.cell_velocities.html`.
- External velocity tutorial: `https://dynamo-release.readthedocs.io/en/stable/tutorials/notebooks/202_extvelo.html`.
- Runtime report: `reports/runtime/scverse_runtime_status.tsv`.
