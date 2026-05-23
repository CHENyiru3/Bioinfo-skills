---
id: scrna.scverse.package.celloracle
kind: package_ref
package: celloracle
import_name: celloracle
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/community/python/celloracle
source_url: https://morris-lab.github.io/CellOracle.documentation/
source_urls: [https://morris-lab.github.io/CellOracle.documentation/index.html, https://morris-lab.github.io/CellOracle.documentation/tutorials/index.html, https://morris-lab.github.io/CellOracle.documentation/modules/celloracle.html]
source_version: celloracle 0.18.0 public docs; runtime report records package missing
source_accessed_at: 2026-05-23
distillation_status: distilled
runtime_status: missing
workflow_stages: ["16_specialized_ecosystem"]
install_probe: pending
import_probe: "import celloracle"
---
# celloracle

## Role In Scverse Workflow

CellOracle models gene regulatory networks from single-cell omics data and
simulates transcription-factor perturbations. In this skill system it is a
specialized regulatory-analysis route that requires explicit GRN inputs.

## Supported Stages

- `16_specialized_ecosystem`: GRN inference, network analysis, and in silico
  TF perturbation planning.

## Required Object State

- Processed scRNA-seq AnnData with normalized and log-transformed expression.
- Cluster or cell-state metadata for network units when cluster-specific GRNs
  are intended.
- Base GRN or TF-target information from promoter databases, motif scans,
  scATAC-seq, bulk ATAC-seq, or a user-supplied TF-target list.
- Optional pseudotime or embedding information for perturbation interpretation.

## Produced Object State

- `Oracle`, `Net`, or `Links` objects and optional `.celloracle.*` HDF5 files.
- Inferred GRN links, filtered network scores, perturbation simulations, and
  visualization outputs.
- Optional converted AnnData from supported conversion utilities.

## Major API Families

- `celloracle.Oracle`: main GRN inference and perturbation workflow object.
- `celloracle.Net` and `Links`: network inference, filtering, and scoring.
- Motif and base-GRN utilities for TF regulatory input.
- Data, conversion, utility, and HDF5 load/save helpers.

## Runtime Availability

Status: `missing`. The recorded runtime report shows `ModuleNotFoundError` for
`import celloracle`; use this ref for planning only until the environment is
updated.

## Failure Modes

- Missing base GRN or incompatible gene identifiers.
- Unsupported OS or missing external dependencies for motif or ATAC workflows.
- Overfit or unstable GRNs from small clusters or noisy expression.
- Simulations outside the distribution of observed expression.

## Scientific Caveats

- In silico perturbations are model predictions, not experimental validation.
- GRN edges depend on candidate TF-target priors and preprocessing choices.
- Cell-state transition interpretation requires trajectory and experimental
  context.

## When To Avoid

- Avoid when no credible TF-target prior or regulatory input exists.
- Avoid for routine marker ranking or annotation tasks.
- Avoid claiming causal perturbation effects without external validation.

## Sources Used

- Public docs: `https://morris-lab.github.io/CellOracle.documentation/index.html`.
- Public tutorial index: `https://morris-lab.github.io/CellOracle.documentation/tutorials/index.html`.
- Public API docs: `https://morris-lab.github.io/CellOracle.documentation/modules/celloracle.html`.
- Runtime report: `reports/runtime/scverse_runtime_status.tsv`.
