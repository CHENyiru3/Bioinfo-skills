---
id: scrna.scverse.package.cellrank
kind: package_ref
package: cellrank
import_name: cellrank
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/community/python/cellrank
source_urls: [https://cellrank.readthedocs.io/en/stable/api/index.html, https://cellrank.readthedocs.io/en/stable/api/kernels.html, https://cellrank.readthedocs.io/en/stable/api/estimators.html]
source_version: cellrank stable docs archive; local runtime missing
source_accessed_at: 2026-05-23
source_local_paths: [bioinfo_tutorial/scverse_ecosystem/community/python/cellrank/cellrank.readthedocs.io/en/stable/api/index.html, bioinfo_tutorial/scverse_ecosystem/community/python/cellrank/cellrank.readthedocs.io/en/stable/api/kernels.html, bioinfo_tutorial/scverse_ecosystem/community/python/cellrank/cellrank.readthedocs.io/en/stable/api/estimators.html]
distillation_status: distilled
runtime_status: missing
workflow_stages: ["15_trajectory_fate_velocity"]
install_probe: pending
import_probe: "import cellrank"
---
# cellrank

## Role In Scverse Workflow

CellRank estimates fate probabilities and driver genes from Markov transition
models built on velocity, neighborhood, pseudotime, or precomputed kernels. It
is downstream of graph, velocity, or trajectory state and should not create
that state implicitly.

## Supported Stages

- `15_trajectory_fate_velocity`: transition kernels, terminal or initial state
  inference, macrostates, fate probabilities, lineage drivers, and fate plots.

## Required Object State

- AnnData with a valid transition source: velocity graph, neighbor graph,
  pseudotime, CytoTRACE-like signal, or precomputed transition matrix.
- Embeddings, clusters, and grouping keys needed for interpretation.
- A documented choice of forward or backward directionality.

## Produced Object State

- Kernel and estimator objects during analysis.
- Transition matrices, macrostate or terminal-state annotations, fate
  probabilities, and lineage-driver summaries written to declared AnnData keys.
- Plots and tables that summarize model-derived fate structure.

## Major API Families

- Kernels: `VelocityKernel`, `ConnectivityKernel`, `CytoTRACEKernel`,
  pseudotime or precomputed kernels, and kernel combinations.
- Estimators: `GPCCA` and `CFLARE`.
- Estimator methods for macrostates, terminal states, fate probabilities, and
  lineage drivers.
- Plotting helpers, including aggregate fate probability plots.

## Runtime Availability

Status is `missing` in `reports/runtime/scverse_runtime_status.tsv`; the import
probe failed with `ModuleNotFoundError: No module named 'cellrank'`.

## Failure Modes

- Missing velocity or neighbor graph state prevents kernel construction.
- Disconnected or weakly connected graphs can yield unstable fate probabilities.
- Large eigendecompositions can be slow or memory intensive.
- Directionality choices can invert biological interpretation.

## Scientific Caveats

- Fate probabilities are model-based transition summaries, not lineage tracing.
- Terminal states and drivers depend on graph construction, kernel weighting,
  and preprocessing.
- Driver genes from CellRank require independent biological validation.

## When To Avoid

- Avoid when there is no credible transition hypothesis or trajectory context.
- Avoid using CellRank before velocity, neighbor, or pseudotime state is
  validated.
- Avoid comparing fate probabilities across conditions without matched
  preprocessing and replicate-aware design.

## Sources Used

- Public docs: `https://cellrank.readthedocs.io/en/stable/api/index.html`.
- Public docs: `https://cellrank.readthedocs.io/en/stable/api/kernels.html`.
- Public docs: `https://cellrank.readthedocs.io/en/stable/api/estimators.html`.
- Local archive: `bioinfo_tutorial/scverse_ecosystem/community/python/cellrank/cellrank.readthedocs.io/en/stable/`.
- Runtime report: `reports/runtime/scverse_runtime_status.tsv`.
