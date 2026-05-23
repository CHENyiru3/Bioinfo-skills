---
id: scrna.scverse.package.moscot
kind: package_ref
package: moscot
import_name: moscot
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/community/python/moscot
source_urls: [https://moscot.readthedocs.io/en/latest/user/problems.html, https://moscot.readthedocs.io/en/latest/user_guide.html]
source_version: Read the Docs latest archive; current runtime report marks import missing
source_accessed_at: 2026-05-23
source_local_paths: [bioinfo_tutorial/scverse_ecosystem/community/python/moscot/moscot.readthedocs.io/en/latest/user/problems.html, bioinfo_tutorial/scverse_ecosystem/community/python/moscot/moscot.readthedocs.io/en/latest/user_guide.html]
distillation_status: distilled
runtime_status: missing
workflow_stages: ["15_trajectory_fate_velocity"]
install_probe: pending
import_probe: "import moscot"
---
# moscot

## Role In Scverse Workflow

moscot models temporal, lineage, spatial, and multimodal relationships with
optimal transport. In this tree it is a specialized trajectory and mapping
backend that requires explicit biological time, spatial, or modality design.

## Supported Stages

- `15_trajectory_fate_velocity`: temporal transport, fate mapping, and
  lineage-related push or pull analyses.
- Related spatial or multimodal uses should route through
  `16_specialized_ecosystem` unless a trajectory stage explicitly owns them.

## Required Object State

- AnnData objects with declared representation, time, batch, spatial, lineage,
  or modality keys as required by the selected problem.
- For temporal workflows, an `.obs` time key with ordered categories or numeric
  time points.
- For spatial or multimodal workflows, matching feature spaces or declared
  cost construction.

## Produced Object State

- Problem objects hold transport subproblems and solutions.
- Analysis methods produce transition summaries, push or pull distributions,
  entropy, batch distances, and optional plots.
- Any persisted AnnData outputs must use declared `.obs`, `.obsm`, `.uns`, or
  artifact keys from wrapper policy.

## Major API Families

- Problem classes: `moscot.problems.time.TemporalProblem`,
  `LineageProblem`, `space.AlignmentProblem`, `space.MappingProblem`,
  `spatiotemporal.SpatioTemporalProblem`, `cross_modality.TranslationProblem`.
- Workflow methods: `prepare`, `solve`, `push`, `pull`, `cell_transition`,
  `annotation_mapping`, `sankey`, `save`, `load`.
- Generic OT problems: `SinkhornProblem`, `GWProblem`, `FGWProblem`.

## Runtime Availability

Status is `missing` in the current repo runtime report:
`ModuleNotFoundError: No module named 'moscot'`. Treat all moscot execution as
unavailable until a runtime probe says otherwise.

## Failure Modes

- Missing design keys prevent problem preparation.
- Cost matrices can become invalid when representations have incompatible
  scales or missing values.
- Solver settings can fail to converge or produce unstable transport plans.
- Large all-pairs transport problems can exceed memory.

## Scientific Caveats

- Optimal transport infers couplings; it does not observe actual cell
  transitions.
- Transport results depend on marginal assumptions, cost choice, and time
  sampling density.
- Temporal direction and lineage interpretation must be justified by the study
  design.

## When To Avoid

- Avoid for unordered snapshots without defensible time, lineage, or spatial
  structure.
- Avoid when the selected representation is dominated by batch or technical
  effects.
- Avoid presenting transport probabilities as direct lineage tracing.

## Sources Used

- Public docs: `https://moscot.readthedocs.io/en/latest/user/problems.html`.
- Public docs: `https://moscot.readthedocs.io/en/latest/user_guide.html`.
- Local archive: `bioinfo_tutorial/scverse_ecosystem/community/python/moscot/`.
- Runtime report: `Bioinfo-skills/reports/runtime/scverse_runtime_status.tsv`.
