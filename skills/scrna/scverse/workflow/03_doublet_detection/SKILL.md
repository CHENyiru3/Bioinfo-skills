---
id: scrna.scverse.workflow.doublet_detection
schema_version: "0.1.0"
kind: skill
domain: scrna
stage: doublet_detection
status: filled
state_in: ["post-basic-QC raw-count AnnData"]
state_out: ["doublet annotations"]
registered_refs: [scrna.scverse.package.doubletdetection]
validation: [backend_neutral, state_contract_checked]
---
# Doublet Detection

## Purpose

Identify likely technical doublets from a declared raw-count source after basic
QC, record scores and labels, and require user review before any removal. This
stage is an annotation and decision step: it can mark cells as likely doublet,
singlet, or ambiguous according to an approved method, but it must not silently
drop cells.

No concrete tool reference for doublet detection is currently registered in
this tree, so this stage registers only the package-level reference. Do not
route execution to a specific function, class, or API until a concrete tool
reference is added and validated.

## When Required

- Before clustering or annotation when droplet-based scRNA-seq data may contain
  multiplets and the user wants a documented doublet policy.
- After basic QC has removed clear low-quality cells but before normalization
  choices could obscure the raw-count structure needed by count-based methods.
- When multiple samples or libraries were combined and each run needs its own
  doublet-rate assumption or review.
- When downstream cluster interpretation depends on separating likely doublet
  clusters or ambiguous cells.

## When Optional

- The assay is not a droplet or combinatorial single-cell protocol where
  doublet modeling is meaningful.
- A validated upstream process already produced doublet scores, labels, and
  method metadata compatible with the current object.
- The current request is read-only inspection, QC metric review, or conceptual
  guidance.

## When Forbidden

- Do not run from log-normalized, scaled, integrated, or batch-corrected
  expression when the chosen method requires raw counts.
- Do not run across pooled samples or libraries when the method or protocol
  expects per-run analysis.
- Do not remove predicted doublets without a separate keep/drop approval.
- Do not treat doublet labels as cell-type annotations.
- Do not name or call a concrete API unless a corresponding tool reference has
  been registered in this repository.

## Required Input State

- AnnData object after basic QC metric review and accepted low-quality-cell
  policy.
- Declared raw-count source, preferably `layers["counts"]`.
- Sample/library/run key in `.obs` when data were generated from multiple
  captures or should be modeled separately.
- Declared method family and package reference, with runtime availability
  checked before execution.
- Approved expected doublet-rate policy or method-specific parameter plan.
- Existing doublet-score and doublet-label keys checked for collisions.

## Produced Output State

- Per-cell doublet score under a declared `.obs` key.
- Per-cell doublet label under a declared `.obs` key, with ambiguous or
  unclassified values preserved when produced by the selected method.
- Method metadata recording package, version, count source, sample/library
  stratification, parameters, score key, label key, threshold policy, and any
  manual overrides.
- Optional keep/drop mask only when the user approves a removal policy.
- No physical cell removal unless an explicit filtered output artifact is
  separately approved.

## User Decision Points

- Which raw-count source to use.
- Whether to run doublet detection per sample/library/run or on the whole
  object; per-run analysis is the conservative default for aggregated capture
  data.
- Which package or method family to use once a concrete tool reference exists.
- Expected doublet rate, threshold policy, number of review plots or tables, and
  how ambiguous calls should be handled.
- Output keys for score, label, and optional keep/drop mask.
- Whether predicted doublets should be retained with annotations, masked for
  downstream steps, or physically removed in a separate approved artifact.

## Registered Package Refs

- `scrna.scverse.package.doubletdetection`

## Registered Tool Refs

- None currently registered for this stage.
- Register and validate a concrete tool reference before binding this stage to
  a callable API.

## Expected Artifacts

- Updated AnnData object or exported table containing declared doublet score and
  label fields.
- Per-sample or per-library summary of predicted singlets, doublets, ambiguous
  cells, and score distributions.
- Parameter and provenance record including count source, package, runtime
  version, grouping key, threshold policy, output keys, and removal decision.
- Optional filtered AnnData artifact only when the user explicitly approves
  physical removal.

## Validation Checks

- Confirm the declared raw-count source exists after QC and remains present
  after annotation.
- Confirm sample/library grouping exists when per-run analysis is requested.
- Confirm runtime availability of the registered package before execution.
- Confirm score and label keys are new or approved for overwrite.
- Confirm score and label vectors have one value per retained observation.
- Confirm per-sample summaries include the number and fraction of predicted
  doublets and ambiguous calls.
- Confirm no cells were removed unless a separate filtering decision is
  recorded.
- Confirm no normalization, integration, clustering, marker ranking, or
  annotation labels were produced by this stage.

## Failure Modes

- The selected input is normalized, transformed, or integrated rather than raw
  counts.
- Low-quality cells remain and distort doublet modeling because basic QC was not
  reviewed first.
- Multiple captures are analyzed together even though expected doublet rates or
  cell compositions differ.
- A missing runtime dependency prevents the registered package from importing in
  the intended execution environment.
- Existing doublet annotations are overwritten without approval.
- Thresholds over-call rare transitional states or under-call heterotypic
  doublets in compositionally simple samples.
- Homotypic doublets are difficult to detect and may remain after this stage.

## Allowed Claims

- Doublet scores and labels were produced or imported using the recorded method,
  count source, grouping policy, and thresholds.
- Cells marked as doublets are candidates for review or removal under the
  approved policy.
- Downstream stages may use the declared doublet mask only after the user
  accepts it.

## Forbidden Claims

- Predicted doublets are guaranteed technical artifacts.
- All remaining cells are singlets after this stage.
- Doublet detection replaces QC filtering, batch correction, clustering review,
  or biological annotation.
- A method tuned for one chemistry, capture, or sample composition is valid for
  another without review.
- A package-level reference is enough to execute an undocumented API.

## Next Stage Routing

- Route to `04_normalization_transform` after doublet labels are reviewed and
  the retained count source is still declared.
- Route to `02_qc_metrics_filtering` if basic QC metrics or low-quality-cell
  decisions are missing.
- Route to state inspection when imported doublet annotations need to be checked
  before reuse.
- Route to downstream clustering or annotation only after the user decides how
  doublet labels or masks should affect retained cells.

## Backend-Neutral Rule

Do not place workflow-engine, shell, script, or notebook syntax in this skill.
Execution belongs in wrappers and adapters after the user approves the exact
operation, parameters, and artifacts.
