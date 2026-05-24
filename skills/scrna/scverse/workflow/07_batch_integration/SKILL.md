---
id: scrna.scverse.workflow.batch_integration
schema_version: "0.1.0"
kind: skill
domain: scrna
stage: batch_integration
status: filled
state_in: ["AnnData with declared batch metadata", "declared representation or count state appropriate to selected integration family", "explicit integration goal"]
state_out: ["integration_key", "integrated representation, graph, corrected matrix, or query/reference mapping report"]
registered_refs: [scrna.scverse.package.scanpy, scrna.scverse.package.scvi_tools]
validation: [backend_neutral, state_contract_checked]
---
# Batch Integration

## Purpose

Select and validate a batch-aware alignment strategy when unwanted technical
variation interferes with representation learning, graph construction, mapping,
or visual diagnostics. This stage is about a declared integration goal, not a
default preprocessing step.

Integration may produce an integrated representation, an integration-specific
graph, a corrected expression matrix, or a query/reference mapping. The stage
must preserve the original count and metadata state, record the chosen batch
key, and keep biological design caveats visible.

## When Required

- The user asks to correct, align, integrate, map, or compare cells across
  batches, technologies, donors, libraries, or studies.
- A state or visualization report shows that an unwanted technical covariate is
  dominating the representation or graph intended for clustering, embedding, or
  annotation support.
- A downstream stage requires a declared integrated representation or mapping
  result instead of the current PCA or graph.
- A query dataset must be projected onto a declared reference state.

## When Optional

- Batch labels exist, but the current task is count-based pseudobulk
  aggregation, sample-level differential expression, or other analysis that
  should consume raw counts and a statistical design instead of an integrated
  representation.
- The user is only inspecting object state, reviewing existing labels, or
  plotting metadata without claiming that a new integrated state is needed.
- A prior approved integration already produced a current, documented
  `integration_key` and the same input state has not changed.
- Batch and biology are strongly confounded and the safer action is to report
  the limitation instead of forcing correction.

## When Forbidden

- Do not run if the batch key is missing, ambiguous, or silently inferred from
  file names without user approval.
- Do not integrate away a covariate that is the biological condition of
  interest or is inseparable from that condition in the available design.
- Do not use corrected expression matrices for condition-level differential
  expression without a separate count-based design and caveat.
- Do not overwrite raw counts, original metadata, existing representations, or
  existing graphs without an explicit output-key and overwrite decision.
- Do not hide normalization, feature selection, PCA, graph construction,
  clustering, or annotation inside this stage.

## Required Input State

- AnnData object with a declared `.obs[batch_key]` or equivalent technical
  covariate selected by the user.
- A documented upstream state appropriate to the selected method family: usually
  normalized/log expression plus PCA for representation-level correction, or
  raw counts and covariates for model-based latent representation methods.
- Raw counts preserved when any downstream count-based analysis remains in
  scope.
- Metadata needed to evaluate confounding, especially sample, donor, condition,
  technology, and library fields when available.
- Declared output policy for `integration_key`, representation key, graph key,
  corrected matrix key, or mapping result key.

## Produced Output State

- One declared integration output, such as an integrated `.obsm[...]`
  representation, integration-owned neighbor graph, corrected matrix, or
  query/reference mapping report.
- An `integration_key` or equivalent provenance entry recording method family,
  package, input keys, batch key, covariates, output keys, random seed when
  relevant, and overwrite decisions.
- Original raw counts, original batch metadata, and pre-integration
  representations retained unless the user approved a separate archival policy.
- Diagnostics describing batch composition, biological covariate composition,
  and key-level changes produced by the stage.

## User Decision Points

- What integration is meant to accomplish: batch mixing for visualization,
  graph/clustering input, reference mapping, model-based latent representation,
  or corrected expression for a narrow downstream purpose.
- Which `.obs` column is the batch key and which fields are biological
  covariates that must not be removed.
- Which package reference is eligible for the requested method family.
- Which input representation or matrix source is allowed.
- Output naming: `integration_key`, integrated representation key, graph key,
  corrected matrix key, and whether existing keys may be overwritten.
- How integration quality should be reviewed, including batch mixing, condition
  preservation, cluster preservation, and known marker behavior.
- Whether the design is too confounded to support correction.

## Registered Package Refs

- `scrna.scverse.package.scanpy`
- `scrna.scverse.package.scvi_tools`

## Registered Tool Refs

- No concrete batch-integration tool refs are registered in this repository for
  this stage. Do not cite specific integration functions as executable entry
  points until matching tool refs and wrappers are added.

## Expected Artifacts

- Updated AnnData output only after the user approves the selected method,
  input keys, output keys, and overwrite policy.
- Integration decision report with batch key, method family, package,
  covariates, input state, output state, and caveats.
- Batch/design summary table, including per-batch cell counts and available
  cross-tabs against sample, donor, condition, or cluster labels.
- Diagnostic embedding or graph summaries when requested, clearly labeled as
  review artifacts rather than proof of successful correction.
- Software-version report and package-runtime status for the selected package.

## Validation Checks

- Confirm the declared `batch_key` exists in `.obs`, has at least two populated
  levels, and has enough cells per level for the selected method.
- Confirm input matrix, representation, feature mask, and count layers required
  by the selected package are present before execution.
- Confirm biological covariates are not perfectly or near-perfectly confounded
  with the batch key without a documented stop-or-proceed decision.
- Confirm output keys are new or explicitly approved for overwrite.
- Confirm produced representations have one row per cell and corrected matrices
  have the expected cell and gene axes.
- Confirm raw counts and original batch metadata remain available after the
  stage.
- Confirm downstream graph, embedding, clustering, marker, or annotation stages
  use the declared integrated output only by explicit key.

## Failure Modes

- Selected package is missing in the runtime environment.
- Batch and biological condition are confounded, making correction
  scientifically unsafe.
- Overcorrection removes real biological structure or undercorrection leaves
  batch-dominated neighborhoods.
- Query and reference objects use incompatible feature namespaces, assays, or
  preprocessing states.
- Method-specific assumptions are unmet, such as missing count state, missing
  PCA state, incompatible covariates, or too few cells per batch.
- Stochastic model or neighbor outputs cannot be reproduced because seeds and
  versions were not recorded.
- Large dense matrices or model training exceed memory or accelerator limits.

## Allowed Claims

- A declared integration output was produced from named input keys using the
  selected package and recorded parameters.
- The original count and metadata state was preserved or intentionally archived
  according to the decision log.
- Batch-mixing and biological-preservation diagnostics are available for human
  review.

## Forbidden Claims

- Integration removed all technical effects.
- Integration preserved all biological signal.
- A corrected matrix is valid for replicate-aware condition-level differential
  expression.
- Batch mixing on an embedding proves that the analysis is unbiased.
- Confounded biological effects can be recovered by integration alone.

## Next Stage Routing

- Route to `08_neighbor_graph` when the approved output is an integrated
  representation intended for graph construction.
- Route to `09_embedding_visualization` to review embeddings derived from an
  integrated graph or representation.
- Route to `10_clustering`, `11_marker_ranking`, or `12_annotation_support`
  only after those stages declare the integrated key they consume.
- Route to `14_aggregation_pseudobulk_de` through preserved raw counts and a
  replicate-aware design, not through corrected expression.
- Route back to `04_normalization_transform`, `05_feature_selection`, or
  `06_dimensionality_reduction` if the selected method requires upstream state
  that is absent.
- Route to `16_specialized_ecosystem` when the user requests a package-specific
  integration family whose object state and concrete tool refs are not yet
  represented by this stage.

## Backend-Neutral Rule

Do not place workflow-engine, shell, script, or notebook syntax in this skill.
Execution belongs in wrappers and adapters after the user approves the exact
operation, parameters, and artifacts.
