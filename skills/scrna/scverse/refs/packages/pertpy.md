---
id: scrna.scverse.package.pertpy
kind: package_ref
package: pertpy
import_name: pertpy
language: python
ecosystem: scverse
docs_local: BioBrain/reference/scverse_docs/pertpy_docs
source_urls: [https://pertpy.readthedocs.io/en/stable/api.html, https://pertpy.readthedocs.io/en/stable/api/tools_index.html, https://pertpy.readthedocs.io/en/stable/tutorials/tools.html]
source_version: pertpy stable docs archive 1.0.6; local runtime missing
source_accessed_at: 2026-05-23
source_local_paths: [BioBrain/reference/scverse_docs/pertpy_docs/pertpy.readthedocs.io/en/stable/api.html, BioBrain/reference/scverse_docs/pertpy_docs/pertpy.readthedocs.io/en/stable/api/tools_index.html, BioBrain/reference/scverse_docs/pertpy_docs/pertpy.readthedocs.io/en/stable/tutorials/tools.html]
distillation_status: distilled
runtime_status: missing
workflow_stages: ["13_signature_scoring", "14_aggregation_pseudobulk_de", "16_specialized_ecosystem"]
install_probe: pending
import_probe: "import pertpy"
---
# pertpy

## Role In Scverse Workflow

pertpy collects perturbation-analysis methods for single-cell data. It is
relevant for perturbation response scoring, pseudobulk or differential
abundance workflows, perturbation assignment, distance tests, and perturbation
spaces.

## Supported Stages

- `13_signature_scoring`: perturbation response summaries and prioritization.
- `14_aggregation_pseudobulk_de`: pseudobulk and differential testing helpers
  when sample-level design is explicit.
- `16_specialized_ecosystem`: perturbation assignment, compositional analysis,
  distance tests, and specialized perturbation-space workflows.

## Required Object State

- AnnData with perturbation labels, control labels, sample or replicate IDs,
  batch covariates, and relevant cell-type or cluster annotations.
- A declared count layer or expression representation appropriate to the chosen
  method.
- For graph or distance methods, validated neighbors, embeddings, or group keys.

## Produced Object State

- Tool-specific result tables, annotations, embeddings, perturbation-space
  objects, pseudobulk matrices, or differential-test summaries.
- Optional labels for perturbed versus non-perturbed cells, differential
  abundance results, distance-test results, and prioritization scores.

## Major API Families

- Tools: `pertpy.tools.Mixscape`, `Milo`, `Sccoda`, `Tasccoda`, `Distance`,
  `DistanceTest`, `Augur`, `Cinemaot`, `DBSCANSpace`, `PseudobulkSpace`.
- Tutorials for differential gene expression, Mixscape, Milo, distance tests,
  Augur, scGen-style prediction, and perturbation spaces.
- Preprocessing, metadata, and datasets modules for perturbation workflows.

## Runtime Availability

Status is `missing` in `reports/runtime/scverse_runtime_status.tsv`; the import
probe failed with `ModuleNotFoundError: No module named 'pertpy'`.

## Failure Modes

- Missing controls, replicates, or perturbation labels can invalidate analyses.
- Some tools rely on optional backends such as PyDESeq2, EdgeR, or probabilistic
  modeling dependencies.
- Perturbation labels can be confounded with batch, sample, or guide quality.
- Graph or embedding inputs can drive distance and abundance results.

## Scientific Caveats

- Perturbation analysis requires explicit experimental design; single cells are
  not independent biological replicates.
- Response scores and classifier-based prioritization are not direct causal
  effect estimates.
- Compositional and abundance methods need sample-level interpretation.

## When To Avoid

- Avoid on observational data without perturbation or control labels.
- Avoid condition-level claims without replicate-aware design.
- Avoid running multiple perturbation methods without declaring which result
  family will support the final claim.

## Sources Used

- Public docs: `https://pertpy.readthedocs.io/en/stable/api.html`.
- Public docs: `https://pertpy.readthedocs.io/en/stable/api/tools_index.html`.
- Public docs: `https://pertpy.readthedocs.io/en/stable/tutorials/tools.html`.
- Local archive: `BioBrain/reference/scverse_docs/pertpy_docs/pertpy.readthedocs.io/en/stable/`.
- Runtime report: `reports/runtime/scverse_runtime_status.tsv`.
