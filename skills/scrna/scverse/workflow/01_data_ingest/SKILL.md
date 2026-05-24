---
id: scrna.scverse.workflow.data_ingest
schema_version: "0.1.0"
kind: skill
domain: scrna
stage: data_ingest
status: filled
state_in: ["declared source format and sample metadata"]
state_out: ["canonical raw-count AnnData/scverse object"]
registered_refs: [scrna.scverse.package.anndata, scrna.scverse.package.scanpy, scrna.scverse.tool.scanpy_read_h5ad]
validation: [backend_neutral, state_contract_checked]
---
# Data Ingest

## Purpose

Convert a declared single-cell source into a canonical AnnData/scverse object
with explicit sample metadata, feature namespace, count-source policy, and
provenance. This stage establishes the object state that later QC,
normalization, doublet detection, and downstream analysis stages consume.

Data ingest is not QC, normalization, filtering, doublet detection, clustering,
or annotation. Its job is to make the input readable, preserve raw counts when
available, and record enough metadata to prevent later stages from guessing.

## When Required

- The user provides a raw matrix directory, matrix file, `.h5ad`, or other
  source that has not yet been accepted into this skill system.
- A state inspection report says the current object is unreadable, ambiguous, or
  missing required metadata for the next requested stage.
- Multiple samples, libraries, or feature namespaces need to be combined or
  labeled before QC.
- The input source has no recorded count-source policy.

## When Optional

- A prior approved ingest already produced a validated AnnData object and no
  source files or metadata tables changed.
- The current turn only needs conceptual guidance and does not consume a data
  object.
- The user supplies an existing `.h5ad` that only needs read-only state
  inspection before deciding whether ingest should be repeated.

## When Forbidden

- Do not infer missing sample, library, organism, assay, or feature-namespace
  metadata when those fields affect downstream interpretation.
- Do not silently merge samples or libraries without a declared join policy.
- Do not normalize, log-transform, filter cells or genes, remove doublets, run
  dimensionality reduction, cluster, or annotate during ingest.
- Do not overwrite an existing canonical object or count layer without an
  explicit overwrite decision.

## Required Input State

- Declared source format, such as existing `.h5ad`, 10x-style matrix output,
  Matrix Market plus barcode/feature tables, or another approved reader path.
- Declared file paths and expected modality or assay.
- Sample or library metadata sufficient to populate stable observation fields,
  including sample/library identifiers when more than one source is present.
- Declared organism and feature namespace when mitochondrial, ribosomal,
  hemoglobin, or gene-symbol decisions will be needed by QC.
- A count-source expectation: whether the source is raw UMI counts, filtered
  counts, unfiltered counts, normalized expression, or unknown.
- A collision policy for observation names, variable names, sample identifiers,
  output path, and canonical layer names.

## Produced Output State

- A readable AnnData object or `.h5ad` artifact with observations in rows and
  features in columns.
- Raw counts preserved in the declared count source when available, preferably
  `layers["counts"]`, with `.X` state explicitly described.
- Required `.obs` fields populated or explicitly reported missing, including
  sample/library identifiers needed by later QC and replicate-aware stages.
- Feature identifiers and display names recorded in `.var` without silently
  discarding the stable identifier namespace.
- Provenance under the system-owned metadata location recording source paths,
  source format, reader family, sample metadata source, count-source policy,
  feature namespace, output path, and collision decisions.

## User Decision Points

- Which input files or directories belong to the ingest unit.
- Whether each source represents raw counts, filtered counts, unfiltered counts,
  or an already processed object.
- Which observation metadata columns should become canonical sample, library,
  batch, condition, or donor fields.
- Whether to keep gene identifiers, gene symbols, or both, and which should be
  the primary variable index.
- How to resolve duplicate cell barcodes, duplicate gene symbols, and sample
  name collisions.
- Whether `.X` should contain raw counts after ingest or whether raw counts
  should be stored in a named layer with `.X` left as the current working
  matrix.
- Whether an existing output artifact may be overwritten.

## Registered Package Refs

- `scrna.scverse.package.anndata`
- `scrna.scverse.package.scanpy`

## Registered Tool Refs

- `scrna.scverse.tool.scanpy_read_h5ad` for `.h5ad` ingest and read-only
  inspection paths.
- Other input formats require a matching tool reference or an explicit
  package-level routing decision before execution.

## Expected Artifacts

- Canonical `.h5ad` or equivalent AnnData artifact.
- Ingest manifest listing source files, sample metadata file, source format,
  reader family, output object, and object shape.
- Validation report covering object readability, axis names, count-source
  preservation, required metadata, feature namespace, and duplicate handling.
- Provenance entry recording all user-approved ingest decisions.

## Validation Checks

- Confirm all declared input paths exist and match the selected source format.
- Confirm the resulting AnnData object has nonzero observation and variable
  axes.
- Confirm observation names and variable names are unique, or that duplicate
  handling is recorded and approved.
- Confirm raw counts are present in the declared count source when the input was
  expected to contain counts.
- Confirm `.obs` contains the declared sample/library fields or reports them as
  intentionally absent.
- Confirm `.var` retains stable identifiers or records why they are unavailable.
- Confirm no QC filters, normalization, embeddings, clusters, marker results, or
  doublet annotations were produced by ingest.

## Failure Modes

- Source paths are missing, incomplete, compressed differently than expected, or
  inconsistent with the selected reader family.
- Barcodes or feature identifiers are duplicated and no collision policy is
  approved.
- Feature rows are gene symbols only and cannot be mapped reliably to stable
  identifiers.
- Multiple samples are combined without stable sample/library labels.
- The input matrix is normalized or transformed even though later stages expect
  raw counts.
- Count data are stored only in `.X` and later overwritten because count
  preservation was not declared.
- Large inputs exceed memory or require a backed or chunked ingest policy.

## Allowed Claims

- The declared source was converted or accepted as a readable AnnData/scverse
  object using the recorded source and metadata policy.
- Raw counts are present in the declared source if validation confirms that
  state.
- Later stages may use the produced object only after their own state checks
  pass.

## Forbidden Claims

- The data are high quality because ingest succeeded.
- The object is normalized, filtered, doublet-free, clustered, annotated, or
  biologically valid.
- `.X` contains raw counts unless the ingest report explicitly declares and
  validates that state.
- Missing sample or feature metadata can be ignored for downstream scientific
  interpretation.

## Next Stage Routing

- Route to `00_state_inspection` when the object should be summarized before
  any mutation.
- Route to `02_qc_metrics_filtering` when a raw-count source and QC feature
  masks can be declared.
- Route to `03_doublet_detection` only after basic QC decisions and a
  per-sample raw-count source are available.
- Route to `04_normalization_transform` only after counts are preserved and the
  user approves the normalization policy.

## Backend-Neutral Rule

Do not place workflow-engine, shell, script, or notebook syntax in this skill.
Execution belongs in wrappers and adapters after the user approves the exact
operation, parameters, and artifacts.
