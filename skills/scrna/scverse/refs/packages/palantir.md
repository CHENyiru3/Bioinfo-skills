---
id: scrna.scverse.package.palantir
kind: package_ref
package: palantir
import_name: palantir
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/community/python/palantir
source_urls: [https://palantir.readthedocs.io/en/latest/core.html, https://palantir.readthedocs.io/en/latest/presults.html]
source_version: Read the Docs latest archive; current runtime report marks import missing
source_accessed_at: 2026-05-23
source_local_paths: [bioinfo_tutorial/scverse_ecosystem/community/python/palantir/palantir.readthedocs.io/en/latest/core.html, bioinfo_tutorial/scverse_ecosystem/community/python/palantir/palantir.readthedocs.io/en/latest/presults.html]
distillation_status: distilled
runtime_status: missing
workflow_stages: ["15_trajectory_fate_velocity"]
install_probe: pending
import_probe: "import palantir"
---
# palantir

## Role In Scverse Workflow

Palantir derives pseudotime, terminal fate probabilities, and differentiation
entropy from multiscale diffusion map space. It is a trajectory and fate
analysis backend after preprocessing and biological start-state policy.

## Supported Stages

- `15_trajectory_fate_velocity`: infer pseudotime, fate probabilities,
  branch-associated cells, and gene trends.

## Required Object State

- AnnData or data frame containing multiscale diffusion components.
- A declared early cell or start state.
- Optional terminal state definitions when terminal cells should be fixed.
- For gene trends, expression layer and prior Palantir pseudotime/fate keys.

## Produced Object State

- `.obs` keys such as `palantir_pseudotime` and `palantir_entropy`.
- `.obsm` key such as `palantir_fate_probabilities`.
- `.uns` entries for waypoints and terminal-state metadata.
- Optional `.varm` and `.uns` gene-trend outputs.

## Major API Families

- Core: `palantir.core.run_palantir`, `identify_terminal_states`.
- Preprocessing: diffusion maps and multiscale space helpers.
- Results: `palantir.presults.PResults`, `compute_gene_trends`,
  `select_branch_cells`, `cluster_gene_trends`.
- Plotting utilities for pseudotime, entropy, fate probabilities, and trends.

## Runtime Availability

Status is `missing` in the current repo runtime report:
`ModuleNotFoundError: No module named 'palantir'`. Do not claim the package is
installed unless the runtime report changes.

## Failure Modes

- Missing diffusion components or wrong `eigvec_key` prevents execution.
- Poor start-cell selection can invert or distort pseudotime.
- Terminal-state inference can be unstable with weak manifold structure.
- AnnData serialization may differ for data frames stored in `.obsm`.

## Scientific Caveats

- Pseudotime is an ordering on a manifold, not measured time.
- Fate probabilities are model-derived branch likelihoods, not lineage-tracing
  observations.
- Gene trends depend on imputation or selected expression layer and smoothing
  choices.

## When To Avoid

- Avoid when cells do not represent a continuum or branching process.
- Avoid without defensible early-state and terminal-state assumptions.
- Avoid treating Palantir branch probabilities as causal fate commitment.

## Sources Used

- Public docs: `https://palantir.readthedocs.io/en/latest/core.html`.
- Public docs: `https://palantir.readthedocs.io/en/latest/presults.html`.
- Local archive: `bioinfo_tutorial/scverse_ecosystem/community/python/palantir/`.
- Runtime report: `Bioinfo-skills/reports/runtime/scverse_runtime_status.tsv`.
