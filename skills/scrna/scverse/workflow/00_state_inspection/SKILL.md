---
id: scrna.scverse.workflow.state_inspection
schema_version: "0.1.0"
kind: skill
domain: scrna
stage: state_inspection
status: filled
state_in: ["declared dataset path or AnnData/MuData"]
state_out: ["state report only"]
registered_refs: [scrna.scverse.package.anndata, scrna.scverse.package.scanpy, scrna.scverse.tool.scanpy_read_h5ad]
validation: [backend_neutral, state_contract_checked]
---
# State Inspection

## Purpose

Inspect an existing `.h5ad` object before any transformation. This stage
answers what object state is present, which matrix source can be trusted, which
keys are available, and which downstream stages are currently allowed.

State inspection is read-only. It reports structure and ambiguity; it does not
normalize, filter, annotate, recluster, overwrite keys, or repair the object.

## When Required

- Before any wrapper consumes a user-provided `.h5ad`.
- Before choosing `.X`, `.raw`, or a named layer as an expression source.
- Before marker ranking, signature scoring, graph construction, clustering,
  pseudobulk aggregation, trajectory analysis, or annotation support.
- When the user cannot state whether `.X` contains counts, normalized values,
  or transformed expression.

## When Optional

- When the current turn only asks for conceptual guidance and no data object is
  consumed.
- When a fresh upstream wrapper in this system just produced a validated state
  report and no files changed after that run.

## When Forbidden

- Do not treat inspection as evidence of biological quality or correctness.
- Do not infer cell types, sample conditions, or differential expression from
  structural metadata alone.
- Do not mutate the input object during this stage.

## Required Input State

- A declared input path to an `.h5ad` file, or an explicit statement that an
  equivalent AnnData object is already loaded for inspection.
- The object must be readable by the selected scverse reader.
- No prior normalization, clustering, or metadata fields are required.

## Produced Output State

- A state report describing `shape`, `.X`, `.obs`, `.var`, `.layers`, `.raw`,
  `.obsm`, `.obsp`, `.varm`, `.varp`, and `.uns`.
- A versions report for the reader environment.
- Warnings for ambiguous count/log/raw state.
- No AnnData mutation and no output `.h5ad`.

## User Decision Points

- Which file should be inspected.
- Whether read-only backed mode is needed for memory constraints.
- Which downstream stage is being considered after inspection.
- Which expression source should be used later when multiple candidates exist.

## Registered Package Refs

- `scrna.scverse.package.anndata`
- `scrna.scverse.package.scanpy`

## Registered Tool Refs

- `scrna.scverse.tool.scanpy_read_h5ad`

## Expected Artifacts

- JSON state report.
- Markdown state summary for quick review.
- JSON software-version report.

## Validation Checks

- Input file exists and has an `.h5ad` suffix.
- Reader returns an AnnData object with nonzero observation and variable axes.
- Report includes top-level object slots and matrix summaries.
- Report flags whether `layers["counts"]`, `layers["log1p_norm"]`, and `.raw`
  exist.
- No output AnnData path is written by this stage.

## Failure Modes

- File path missing, unreadable, or not an `.h5ad`.
- Reader dependency missing from the selected environment.
- Object is corrupt or contains unsupported backed arrays.
- Matrix source cannot be classified as counts or transformed expression.
- Observation or variable names are duplicated.

## Allowed Claims

- The object was readable by the selected reader.
- Specific keys, layers, embeddings, pairwise matrices, and metadata columns are
  present or absent.
- The inspected matrix sample is integer-like, nonnegative, sparse, dense, or
  ambiguous according to the report.

## Forbidden Claims

- The data are high quality.
- The data are normalized correctly.
- The clusters, annotations, or marker genes are biologically valid.
- A condition-level statistical design is valid.
- A missing count layer can be safely replaced by `.X` without user approval.

## Next Stage Routing

- Route to `01_data_ingest` if the file cannot be read as the expected object.
- Route to `02_qc_metrics_filtering` only if a count source is present or the
  user explicitly approves the available source.
- Route to `08_neighbor_graph`, `10_clustering`, `11_marker_ranking`, or
  `13_signature_scoring` only after a downstream expression source and required
  keys are declared.
- Route to `14_aggregation_pseudobulk_de` only if sample and design metadata
  exist or the user agrees to add them in a separate step.

## Backend-Neutral Rule

Do not place workflow-engine, shell, script, or notebook syntax in this skill.
Execution belongs in wrappers and adapters after the user approves the exact
operation and artifacts.
