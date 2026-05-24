---
id: scrna.scverse.workflow.normalization_transform
schema_version: "0.1.0"
kind: skill
domain: scrna
stage: normalization_transform
status: filled
state_in: ["raw counts preserved"]
state_out: ["normalized/log expression"]
registered_refs: [scrna.scverse.package.scanpy, scrna.scverse.tool.scanpy_normalize_total_log1p]
validation: [backend_neutral, state_contract_checked]
---
# Normalization And Transform

## Purpose

Create an analysis-scale expression matrix from a declared raw-count source
while preserving the original counts. This stage covers library-size
normalization followed by an optional `log1p` transform, and it records the
normalization and transform policy needed by feature selection, PCA, marker
ranking, and signature scoring.

This stage is state-sensitive. It must not guess whether `.X` is raw counts,
must not silently replace an existing count layer, and must not hide feature
selection or PCA inside the normalization step.

## When Required

- Before Scanpy-style HVG selection, PCA, graph construction, clustering, marker
  ranking, or signature scoring when only raw counts are available.
- When a state inspection report says the working expression source is raw
  counts and no declared normalized/log expression layer exists.
- When the downstream method explicitly requires log-normalized expression.

## When Optional

- When a prior approved run already produced a declared normalized/log
  expression layer and recorded the target sum, log base, and count source.
- When the selected downstream method intentionally consumes raw counts, such as
  count-based HVG flavors or pseudobulk count aggregation.

## When Forbidden

- Do not run if no trustworthy count source has been declared.
- Do not run `log1p` on a matrix that has already been log-transformed.
- Do not overwrite `layers["counts"]`, `.raw`, or another declared count source
  without an explicit overwrite policy.
- Do not perform HVG selection, PCA, graph construction, clustering, or marker
  ranking in this stage.

## Required Input State

- A readable AnnData object with a declared raw-count source, preferably
  `layers["counts"]`.
- If `.X` is the count source, count preservation must be approved before `.X`
  is used as a mutable working matrix.
- Existing `layers["log1p_norm"]` or other candidate output keys must be checked
  before writing; collisions require explicit approval or a new key.
- The user or upstream decision log must declare the intended `target_sum`, log
  transform policy, output expression target, and count-source retention policy.

## Produced Output State

- A declared normalized/log expression target, conventionally
  `layers["log1p_norm"]` or an approved current working `.X`.
- Raw counts still present in the declared count source.
- Provenance under the system-owned metadata location recording count source,
  output expression target, `target_sum`, `normalize_total` parameters, whether
  `log1p` was applied, log base, output key, and overwrite decision.
- A validation report confirming that the count source remained present after
  transformation.

## User Decision Points

- Which matrix source contains raw counts: `layers["counts"]`, `.X`, `.raw`, or
  another named layer.
- Whether the normalized/log result should become the current working `.X` or a
  named layer such as `layers["log1p_norm"]`.
- The normalization `target_sum`, commonly `1e4` for counts per cell or `1e6`
  for CPM-like scaling.
- Whether to apply natural-log `log1p` or another log base, and how to verify
  that log transformation has not already occurred.
- How to handle an existing output key: fail, write a new key, or explicitly
  overwrite with provenance.

## Registered Package Refs

- `scrna.scverse.package.scanpy`

## Registered Tool Refs

- `scrna.scverse.tool.scanpy_normalize_total_log1p`

## Expected Artifacts

- Mutated AnnData output with raw counts preserved and normalized/log expression
  written to the declared target.
- Parameter/provenance entry recording `target_sum`, log transform, source key,
  output key, and overwrite policy.
- Validation summary reporting count-source presence, output-key presence, and
  basic matrix-state checks.

## Validation Checks

- Confirm the declared count source exists before transformation.
- Confirm the count source remains present after transformation.
- Confirm no existing output key was overwritten unless the decision log
  explicitly allowed that overwrite.
- Confirm the output expression target exists and has the expected shape.
- Confirm the recorded `target_sum` and log transform match the executed
  parameter choices.
- Confirm the stage did not create HVG masks, PCA representations, neighbor
  graphs, clusters, or marker-ranking output.

## Failure Modes

- Count source is absent, ambiguous, not integer-like, or already transformed.
- `.X` is treated as raw counts without a state-inspection decision.
- Existing `layers["counts"]` or `layers["log1p_norm"]` is silently overwritten.
- `log1p` is applied twice.
- `target_sum` is missing, unintended, or inconsistent with downstream
  assumptions.
- Large dense matrices or backed arrays exceed memory for in-place mutation.

## Allowed Claims

- A normalized/log expression target was produced from the declared count
  source using the recorded parameters.
- The declared raw-count source remained present after this stage.
- Downstream stages may consume the declared normalized/log expression if their
  own state checks pass.

## Forbidden Claims

- The normalization removed all technical effects.
- The normalized expression is sufficient for condition-level differential
  expression.
- HVGs, PCs, clusters, or markers are valid because normalization completed.
- A missing raw-count source can be reconstructed from log-normalized values.

## Next Stage Routing

- Route to `05_feature_selection` when HVGs should be selected from the
  declared normalized/log expression or from raw counts for an approved
  count-based flavor.
- Route to `06_dimensionality_reduction` only after a feature mask is declared
  or the user approves PCA on all retained features.
- Route to `11_marker_ranking` or `13_signature_scoring` only when those stages
  explicitly accept the produced log expression state.
- Route to `14_aggregation_pseudobulk_de` only through a separate count-based
  path that consumes preserved raw counts, not log-normalized expression.

## Backend-Neutral Rule

Do not place workflow-engine, shell, script, or notebook syntax in this skill.
Execution belongs in wrappers and adapters after the user approves the exact
operation, parameters, and artifacts.
