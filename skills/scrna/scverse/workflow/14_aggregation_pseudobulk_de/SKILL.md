---
id: scrna.scverse.workflow.aggregation_pseudobulk_de
schema_version: "0.1.0"
kind: skill
domain: scrna
stage: aggregation_pseudobulk_de
status: filled
state_in: ["raw counts, sample_id, condition, design"]
state_out: ["pseudobulk_key and DE outputs"]
registered_refs: [scrna.scverse.package.scanpy, scrna.scverse.tool.scanpy_get_aggregate]
validation: [backend_neutral, state_contract_checked]
---
# Aggregation And Pseudobulk DE

## Purpose

Prepare sample-level pseudobulk count matrices and route condition-level
differential expression through a replicate-aware model. This stage is for
inference across biological samples or donors. Aggregation alone is not a DE
model, and cluster marker ranking or per-cell signature scoring must not be
presented as replicate-aware condition-level DE.

## When Required

- The user asks for condition, disease, treatment, genotype, timepoint, or
  perturbation differential expression within all cells or within annotated
  groups.
- Biological samples, donors, or experimental units must be treated as
  replicates rather than individual cells.
- Raw counts and sample-level metadata are available and the design can be
  stated.
- Existing marker ranking results are being considered for condition-level
  claims and need to be replaced by a valid replicate-aware path.

## When Optional

- The task is only to compute descriptive cluster markers.
- The user only wants candidate annotation support or predefined signature
  scoring.
- Condition-level testing has already been performed with documented
  sample-level design and compatible outputs.
- The dataset is exploratory and lacks the replication needed for valid
  condition-level inference.

## When Forbidden

- Raw count data are unavailable or cannot be identified.
- `sample_id`, condition, or required design covariates are missing.
- There are no biological replicates for at least one tested condition.
- The design is completely confounded, for example condition equals batch or
  donor.
- The user asks to treat cells as independent replicates for condition-level
  p-values.
- Grouping by condition alone would pool biological replicates before modeling.

## Required Input State

- AnnData or exported matrix with a declared raw count source in `.X` or a named
  layer.
- `sample_id` identifying the biological or experimental replicate unit.
- Condition column and any design covariates needed for the requested contrast.
- Optional cell group key, such as approved annotation or cluster label, when
  testing within groups.
- Minimum cell-count policy per sample and group before aggregation.
- Confirmed replicate counts per condition after filtering.
- A declared DE engine or downstream model path for condition-level testing.

## Produced Output State

- Pseudobulk count object or matrix keyed by sample and optional cell group.
- Aggregation metadata including grouping columns, count source, number of
  cells aggregated, dropped groups, and sample-level design table.
- `pseudobulk_key` or artifact identifier for downstream modeling.
- DE output tables from the approved replicate-aware model, including contrast,
  term, gene, effect size, test statistic when available, raw p-value,
  adjusted p-value, base expression/mean when available, and model metadata.
- QC summaries for library sizes, cell counts, replicate balance, and filtered
  genes or samples.

## User Decision Points

- Raw count source: `.X` or named layer.
- Aggregation level: sample only, or sample by annotation/cluster group.
- Group key for within-cell-type or within-cluster testing, if any.
- Minimum cells per sample/group and minimum samples per condition.
- DE engine and statistical model family.
- Design formula, covariates, blocking or pairing terms, and contrasts.
- Gene filtering policy before model fitting.
- Output naming for pseudobulk object, design table, and DE result tables.
- How to handle groups with insufficient replication or complete confounding.

## Registered Package Refs

- `scrna.scverse.package.scanpy`

## Registered Tool Refs

- `scrna.scverse.tool.scanpy_get_aggregate`, for aggregation only. A separate
  approved DE tool or wrapper is required for condition-level inference.

## Expected Artifacts

- Pseudobulk count matrix or AnnData object with sample-level observations.
- Sample/design table aligned to the pseudobulk matrix.
- Cell-count table per sample and optional group.
- Library-size and replicate-balance QC table.
- DE result tables for each approved contrast and group.
- Provenance record with count source, aggregation columns, filters, design,
  contrast, DE engine, software versions, and caveats.

## Validation Checks

- Confirm the selected matrix contains raw non-negative counts suitable for the
  chosen DE engine.
- Confirm `sample_id`, condition, covariates, and optional group key exist and
  have no unhandled missing values.
- Confirm aggregation groups include `sample_id`; condition-only aggregation is
  rejected for DE.
- Confirm every tested contrast has enough biological replicates after filters.
- Confirm design matrix is not singular or completely confounded.
- Confirm cell counts and library sizes are reported before model fitting.
- Confirm pseudobulk observations align one-to-one with design rows.
- Confirm DE result tables include contrast, model metadata, and multiple-test
  correction fields.

## Failure Modes

- Log-normalized expression is aggregated and modeled as counts.
- Cells are treated as independent replicates, inflating significance.
- Condition, batch, donor, chemistry, or sample source is confounded.
- Too few cells in a sample/group produce unstable pseudobulk counts.
- Too few biological replicates prevent valid condition-level inference.
- Aggregating by condition before modeling removes replicate variation.
- Annotation errors create misleading within-cell-type contrasts.
- Composition shifts are mistaken for gene-level expression changes.

## Scientific Caveats

- Pseudobulk DE tests sample-level aggregated expression under the specified
  design; it does not test individual cells as independent biological units.
- Aggregation is a data preparation step. Statistical inference depends on the
  downstream DE model, design, replication, and filtering.
- Within-group DE inherits uncertainty from the chosen annotation or clustering
  labels.
- Differential expression is association under the design and contrast; it does
  not prove mechanism or causality by itself.

## Allowed Claims

- "Raw counts were aggregated by sample and optional group under the recorded
  policy."
- "The DE table reports condition-associated expression changes under the
  approved sample-level design and contrast."
- "Groups or contrasts lacking sufficient replication were excluded or flagged."

## Forbidden Claims

- "Aggregation alone produced differential expression statistics."
- "Cluster marker ranking or per-cell signature scores are condition-level DE."
- "Cells were valid independent replicates for condition p-values."
- "A condition effect was estimated when condition was completely confounded
  with sample, donor, batch, or chemistry."
- "DE results prove cell identity, pathway activation, or causal mechanism."

## Next Stage Routing

- Route to a DE tool reference or execution adapter only after aggregation,
  design, contrast, and filters are approved.
- Route to `12_annotation_support` if within-group DE depends on missing or
  uncertain annotations.
- Route to `13_signature_scoring` only for descriptive predefined program
  scores, not as a replacement for count-based DE.
- Route back to state inspection or ingest if raw counts, sample metadata, or
  design fields are missing.
