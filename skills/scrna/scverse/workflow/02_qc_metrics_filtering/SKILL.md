---
id: scrna.scverse.workflow.qc_metrics_filtering
schema_version: "0.1.0"
kind: skill
domain: scrna
stage: qc_metrics_filtering
status: filled
state_in: ["raw-count AnnData"]
state_out: ["QC metrics and approved filters"]
registered_refs: [scrna.scverse.package.scanpy, scrna.scverse.tool.scanpy_calculate_qc_metrics]
validation: [backend_neutral, state_contract_checked]
---
# QC Metrics And Filtering

## Purpose

Compute per-cell and per-feature quality-control metrics from a declared
raw-count source, review thresholds, and record the approved filtering policy.
This stage separates metric calculation from scientific threshold approval so
that filtering decisions are explicit, reproducible, and inspectable.

This stage does not normalize, log-transform the expression matrix, detect
doublets, integrate batches, run PCA, cluster, or annotate cells. It may write
QC metrics and a reviewed keep/drop mask, but physical subsetting requires a
separate approval record.

## When Required

- Before normalization, feature selection, doublet detection, graph
  construction, clustering, or marker review on newly ingested raw counts.
- When the object lacks declared cell-level metrics such as total counts,
  detected genes, mitochondrial percentage, or top-gene complexity metrics.
- When feature-level metrics are needed before gene filtering.
- When QC thresholds need to be documented for reproducible reruns.

## When Optional

- A prior approved QC run already produced compatible metrics, thresholds, and
  keep/drop masks for the current object state.
- The current request is read-only state inspection or conceptual guidance.
- A specialized upstream pipeline already produced validated QC annotations and
  the user approves reusing them.

## When Forbidden

- Do not calculate QC metrics from log-normalized or scaled expression when the
  metrics are intended to describe raw counts.
- Do not apply default thresholds without user or protocol approval.
- Do not use organism-specific feature masks, such as mitochondrial or
  ribosomal masks, before the feature namespace and organism are declared.
- Do not remove cells or genes physically unless the filtering action and output
  artifact are explicitly approved.
- Do not interpret QC filtering as doublet removal, batch correction, or
  biological annotation.

## Required Input State

- A readable AnnData object with a declared raw-count source, preferably
  `layers["counts"]` or explicitly approved `.X`.
- Nonzero observation and variable axes after ingest.
- Declared organism and feature namespace when deriving QC feature masks.
- Boolean `.var` masks for requested QC groups, such as mitochondrial,
  ribosomal, hemoglobin, ERCC, antibody, or other protocol-specific features.
- A threshold review plan: metrics to inspect, per-sample or global threshold
  policy, whether filtering is mask-only or subsetting, and output key names.
- Existing QC columns and filter masks checked for collisions before writing.

## Produced Output State

- Per-cell QC metrics in `.obs` or an exported metrics table, including total
  counts, detected genes, top-gene count percentages, and percentages for
  declared QC feature masks when requested.
- Per-feature QC metrics in `.var` or an exported metrics table, including
  detected-cell counts, mean counts, dropout percentage, and total counts when
  produced by the selected tool.
- Approved keep/drop masks or threshold records for cells and features.
- Optional filtered AnnData artifact only when physical subsetting is approved.
- Provenance recording count source, QC feature masks, metric parameters,
  thresholds, per-sample versus global policy, output keys, and whether
  subsetting occurred.

## User Decision Points

- Which raw-count source to use: `.X`, `.raw`, or a named count layer.
- Which QC feature masks to compute, and how those masks are derived from gene
  identifiers or symbols.
- Which top-feature ranks to report for library-complexity metrics.
- Whether thresholds are global, per sample/library, per chemistry, or
  stratified by another approved technical field.
- Which metrics define cell filtering, feature filtering, and warning-only
  flags.
- Whether to write only metrics and masks or also produce a physically filtered
  object.
- How to handle existing QC metrics, masks, or filtered outputs.

## Registered Package Refs

- `scrna.scverse.package.scanpy`

## Registered Tool Refs

- `scrna.scverse.tool.scanpy_calculate_qc_metrics`

## Expected Artifacts

- Updated AnnData object or exported tables with declared QC metrics.
- Cell-level QC metrics table and feature-level QC metrics table when exports
  are requested.
- Threshold decision log, including rationale and any sample-stratified values.
- Keep/drop mask summary with counts retained and removed by each rule.
- Optional filtered AnnData output only when subsetting is explicitly approved.

## Validation Checks

- Confirm the declared count source exists and is count-like enough for QC
  metric calculation.
- Confirm all requested QC feature mask keys exist in `.var` and are
  boolean-like.
- Confirm `percent_top` values are positive and do not exceed the retained
  feature count.
- Confirm expected QC metric columns or exported tables were produced.
- Confirm thresholds and masks are recorded before any physical filtering.
- Confirm physical subsetting did not occur unless explicitly approved.
- Confirm raw counts remain present after metric calculation and filtering.
- Confirm no normalization, HVG mask, PCA representation, graph, embedding,
  cluster, marker, or doublet output was created by this stage.

## Failure Modes

- The selected matrix is log-normalized, scaled, or otherwise not raw counts.
- Mitochondrial or other QC masks are wrong because organism or feature
  namespace was misdeclared.
- `percent_top` requests ranks larger than the number of retained features.
- Existing QC columns are overwritten without approval.
- Thresholds are copied from another dataset without considering chemistry,
  tissue, nucleus/cell protocol, or sample composition.
- Global thresholds remove one sample disproportionately because QC structure is
  sample-specific.
- Physical filtering removes rare but real biology or keeps low-quality cells
  because thresholds were not reviewed.

## Allowed Claims

- The declared QC metrics and filters were calculated or recorded from the
  declared count source using the approved parameters.
- The retained and removed cell or feature counts are known for each approved
  filtering rule.
- The filtered object, when produced, reflects the recorded QC policy.

## Forbidden Claims

- QC filtering proves that all remaining cells are biologically valid singlets.
- Generic mitochondrial or gene-count thresholds are universally appropriate.
- Filtering corrected batch effects, normalized expression, assigned cell
  identities, or handled replicate-aware inference.
- A normalized expression matrix can replace raw counts for raw-count QC
  metrics without a documented exception.

## Next Stage Routing

- Route to `03_doublet_detection` after basic low-quality cells are removed or
  a mask-only policy is approved, and a per-sample raw-count source remains.
- Route to `04_normalization_transform` when the count source is preserved and
  QC filtering has been accepted.
- Route back to `01_data_ingest` if required metadata, feature namespace, or a
  trustworthy count source is missing.
- Route to state inspection when the user needs to review metrics and masks
  before committing to physical subsetting.

## Backend-Neutral Rule

Do not place workflow-engine, shell, script, or notebook syntax in this skill.
Execution belongs in wrappers and adapters after the user approves the exact
operation, parameters, and artifacts.
