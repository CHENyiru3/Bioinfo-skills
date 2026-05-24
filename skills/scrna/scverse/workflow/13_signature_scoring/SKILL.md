---
id: scrna.scverse.workflow.signature_scoring
schema_version: "0.1.0"
kind: skill
domain: scrna
stage: signature_scoring
status: filled
state_in: ["declared expression source and validated gene sets"]
state_out: ["score_key"]
registered_refs: [scrna.scverse.package.scanpy, scrna.scverse.tool.scanpy_score_genes]
validation: [backend_neutral, state_contract_checked]
---
# Signature Scoring

## Purpose

Score predefined gene sets or programs on cells or observations using a
declared expression source and validated gene namespace. This stage applies
known signatures; it does not discover markers, annotate clusters by itself, or
perform replicate-aware condition-level differential expression.

## When Required

- The user asks to calculate a known gene program, module, pathway-like score,
  cell-cycle score, stress score, lineage score, or curated marker-set score.
- Annotation support needs a supplementary score for declared gene sets.
- A downstream report needs per-cell or per-group summaries of predefined
  signatures with missing-gene and parameter metadata.

## When Optional

- The task is de novo marker ranking for existing groups.
- Candidate labels can be reviewed directly from marker tables and references.
- The user only needs condition-level differential expression or pseudobulk
  testing.
- The requested signature scores already exist with compatible provenance.

## When Forbidden

- No gene set is declared or the gene set has not been checked against the
  feature namespace.
- The expression source is absent, ambiguous, or silently inferred.
- The user expects the score to prove pathway activity, cell identity, or
  treatment effect without supporting evidence.
- The task is marker discovery, automatic annotation, or condition-level
  differential expression.

## Required Input State

- AnnData object with a declared expression source: `.raw`, `.X`, or a named
  layer.
- Validated gene set or sets in the same namespace as the selected feature
  matrix.
- Missing-gene policy, including the minimum number or fraction of signature
  genes required to score.
- Approved output `score_key` or naming convention that does not overwrite
  existing `.obs` columns without approval.
- Control gene sampling policy when using a reference-gene scoring method:
  control pool, number of bins, control size, and random seed.

## Produced Output State

- One numeric score column per declared signature, normally stored under an
  approved `.obs[score_key]`.
- Missing-gene report for each signature.
- Parameter and provenance metadata recording expression source, gene set,
  control gene policy, random seed, score key, software/tool reference, and
  caveats.
- Optional summary tables by cluster, annotation, sample, batch, or condition
  for interpretation only.

## User Decision Points

- Which gene set or sets to score, and their source.
- Expression source: `.raw`, `.X`, or named layer; do not infer silently.
- Missing-gene threshold and whether to stop, warn, or continue after
  namespace mismatches.
- Scoring method and tool reference.
- Output score key names and overwrite policy.
- Control-gene pool, control size, number of bins, random seed, and whether
  control genes may overlap the scored set when the selected tool exposes that
  choice.
- Which grouping columns, if any, should be used only for post-score summaries.

## Registered Package Refs

- `scrna.scverse.package.scanpy`

## Registered Tool Refs

- `scrna.scverse.tool.scanpy_score_genes`

## Expected Artifacts

- Score table keyed by cell/observation ID and `score_key`.
- Missing-gene and retained-gene report for every scored signature.
- Summary table by requested group keys, clearly labeled as descriptive.
- Provenance record with method, expression source, gene set source, seed,
  control parameters, and software version.
- Updated AnnData object only when an execution step is approved to write the
  declared score key.

## Validation Checks

- Confirm selected expression source exists and is documented.
- Confirm gene set identifiers match `adata.var_names` or the approved feature
  namespace mapping.
- Report missing, duplicate, and retained genes before scoring.
- Enforce the minimum retained-gene threshold.
- Confirm score keys are new or replacement is explicitly approved.
- Record random seed and control-gene parameters when stochastic control
  sampling is used.
- After scoring, check that output values are numeric, finite or explicitly
  explained, and have one value per observation.
- Keep score summaries separate from inferential condition-level tests.

## Failure Modes

- Gene symbols, Ensembl IDs, aliases, or species are mismatched.
- Too few signature genes are present to support a meaningful score.
- Control gene pool is too small or biased relative to the signature genes.
- `.raw` is used unexpectedly when the user intended `.X` or a layer.
- Raw counts, scaled data, or residuals are scored without acknowledging how the
  expression source changes interpretation.
- Multiple signatures are compared as if they were calibrated on the same
  absolute scale.
- Existing score columns are overwritten without approval.

## Scientific Caveats

- Signature scores are relative summaries of declared gene sets and selected
  expression sources; they are not direct measurements of pathway activity.
- Score magnitude depends on normalization, gene availability, control-gene
  sampling, and gene set length.
- A high score can support annotation review but does not prove cell type
  identity by itself.
- Per-cell score differences across conditions are descriptive unless routed to
  a replicate-aware model with appropriate sample-level design.

## Allowed Claims

- "The declared signature was scored using the recorded expression source,
  retained genes, and control parameters."
- "Score summaries describe how the predefined program varies across requested
  groups."
- "Missing genes and namespace assumptions were reported with the score."

## Forbidden Claims

- "The score discovers marker genes."
- "The score proves a cell type, pathway activity, perturbation response, or
  disease mechanism."
- "Per-cell score comparisons are replicate-aware condition-level differential
  expression."
- "Scores from different signatures are directly comparable without calibration
  or context."

## Next Stage Routing

- Route to `12_annotation_support` when scores should be interpreted alongside
  marker evidence and reference knowledge.
- Route to `11_marker_ranking` when the user wants de novo markers for existing
  groups instead of scoring predefined genes.
- Route to `14_aggregation_pseudobulk_de` when the user asks for
  replicate-aware condition-level testing of scores or expression programs.
- Route back to state inspection when expression source, gene namespace, or
  existing score provenance is unclear.
