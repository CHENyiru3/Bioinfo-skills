---
id: scrna.scverse.workflow.trajectory_fate_velocity
schema_version: "0.1.0"
kind: skill
domain: scrna
stage: trajectory_fate_velocity
status: filled
state_in: ["declared graph, embedding, clustering, time, root, terminal, or velocity-compatible layer state as required by selected method family"]
state_out: ["pseudotime, trajectory graph, velocity graph, fate probabilities, transition summaries, or package-specific diagnostics"]
registered_refs: [scrna.scverse.package.scanpy, scrna.scverse.package.scvelo, scrna.scverse.package.cellrank, scrna.scverse.package.palantir, scrna.scverse.package.moscot, scrna.scverse.package.scfates, scrna.scverse.package.dynamo]
validation: [backend_neutral, state_contract_checked]
---
# Trajectory Fate And Velocity

## Purpose

Route and validate analyses that order cells along continua, summarize lineage
topology, estimate fate tendencies, or use velocity-compatible measurements to
study dynamic state changes. This stage requires explicit biological
assumptions about roots, terminal states, time, graph topology, or velocity
layers.

Trajectory, fate, and velocity outputs are model-dependent summaries. They do
not by themselves prove chronological time, causal lineage, or experimental
fate.

## When Required

- The user asks for pseudotime, lineage topology, branch structure, terminal
  states, fate probabilities, RNA velocity, transition tendencies, or dynamic
  vector-field style interpretation.
- A downstream report needs ordered cells or branch-aware summaries rather than
  unordered clusters.
- The analysis has known developmental, differentiation, perturbation-time, or
  sampling-time structure that the user wants represented explicitly.
- A selected package requires root, terminal, time, graph, or velocity state to
  be declared before execution.

## When Optional

- The biological question is adequately answered by clustering, annotation,
  marker ranking, signature scoring, or pseudobulk comparisons.
- Existing trajectory or velocity outputs already have compatible provenance
  and the user only wants review or plotting.
- The task is exploratory and the user has not yet approved root, terminal, or
  time assumptions.
- The dataset is cross-sectional with no plausible continuum and no stated
  trajectory hypothesis.

## When Forbidden

- Do not infer hidden root or terminal choices when the selected method requires
  them.
- Do not run velocity-oriented analysis without velocity-compatible layers or
  equivalent package-required dynamic state.
- Do not treat pseudotime as real chronological time unless the design and
  selected method support that interpretation.
- Do not use this stage for condition-level differential expression,
  replicate-aware testing, or cell-type annotation.
- Do not overwrite existing trajectory, velocity, fate, graph, embedding, or
  cluster keys without explicit approval.

## Required Input State

- AnnData object with the graph, embedding, representation, cluster, or
  expression state required by the selected package.
- A declared `neighbors_key`, graph key, embedding key, or cluster key when the
  method consumes topology inferred from the analyzed cells.
- Root cells, root cluster, terminal states, sampling time, lineage labels, or
  prior biological ordering when required by the selected method.
- For velocity methods, named spliced and unspliced layers or other documented
  velocity-compatible measurements with matching cell and gene axes.
- Metadata needed to judge confounding by sample, donor, batch, condition,
  library, or time point.
- Output-key and overwrite policy for pseudotime, fate, velocity, transition,
  and diagnostic fields.

## Produced Output State

- One or more declared output keys for pseudotime, branch assignment,
  trajectory graph, velocity graph, transition matrix, fate probability,
  terminal-state assignment, or package-specific diagnostic state.
- Exportable tables for per-cell scores, per-state probabilities, branch labels,
  or transition summaries when produced by the selected package.
- Diagnostic plots or summaries for graph connectivity, root/terminal
  selection, branch structure, velocity consistency, and fate uncertainty.
- Provenance recording package, method family, input graph or layer keys,
  root/terminal/time choices, output keys, random seed when relevant, and
  scientific caveats.

## User Decision Points

- Which question family is being asked: pseudotime ordering, topology/branch
  graph, fate probabilities, velocity, optimal-transport style time mapping, or
  package-specific dynamic modeling.
- Which package reference is eligible for the requested family and available in
  the runtime environment.
- Which graph, embedding, representation, expression source, or velocity layers
  the method may consume.
- How roots, terminal states, sampling time, or lineage priors are selected and
  documented.
- Which output keys should be written and whether existing keys may be
  overwritten.
- Which biological markers, annotations, time points, or perturbation labels
  should be used to sanity-check the result.

## Registered Package Refs

- `scrna.scverse.package.scanpy`
- `scrna.scverse.package.scvelo`
- `scrna.scverse.package.cellrank`
- `scrna.scverse.package.palantir`
- `scrna.scverse.package.moscot`
- `scrna.scverse.package.scfates`
- `scrna.scverse.package.dynamo`

## Registered Tool Refs

- No concrete trajectory, fate, or velocity tool refs are registered in this
  repository for this stage. Package refs may guide routing, but executable
  entrypoints require separate tool refs and wrappers before implementation.

## Expected Artifacts

- Updated AnnData or package-specific object output only after method,
  assumptions, input keys, and output keys are approved.
- Per-cell pseudotime, fate, branch, transition, or velocity tables when the
  selected method produces them.
- Root, terminal, time, and graph-decision report.
- Diagnostic figures or summaries for review, clearly labeled as model
  diagnostics.
- Software-version and package-runtime report for the selected package.

## Validation Checks

- Confirm all required input keys exist and have shapes compatible with the
  current cell and gene axes.
- Confirm root, terminal, time, or lineage choices are present when required and
  correspond to existing cells, clusters, labels, or metadata values.
- Confirm velocity-compatible layers exist before any velocity path and are not
  confused with normalized/log expression layers.
- Confirm the selected graph is connected enough for the claimed trajectory
  scope or report disconnected components explicitly.
- Confirm output keys are new or explicitly approved for overwrite.
- Confirm pseudotime values, fate probabilities, or transition summaries are
  finite and aligned to the current observations.
- Confirm batch, sample, condition, and time metadata are reviewed for
  confounding before biological interpretation.

## Failure Modes

- Missing runtime package or missing concrete tool ref for the requested
  method.
- Root or terminal choices are absent, arbitrary, unstable, or inconsistent
  with known biology.
- Graph topology is weak, disconnected, batch-driven, or dominated by
  preprocessing artifacts.
- Velocity-compatible layers are absent, sparse, misaligned, or generated with
  incompatible preprocessing.
- Terminal-state or fate estimates disagree across markers, annotations, time
  points, or package diagnostics.
- Cross-sectional data are overinterpreted as time-resolved lineage evidence.
- Large transition or velocity graphs exceed memory limits.

## Allowed Claims

- Cells were ordered or assigned model-derived dynamic summaries under the
  recorded method and assumptions.
- The selected output keys contain pseudotime, branch, fate, transition, or
  velocity summaries as defined by the selected package.
- Diagnostics support human review of whether the result is plausible for the
  stated biological question.

## Forbidden Claims

- Pseudotime is true chronological time without supporting design and method
  evidence.
- Velocity or fate output proves a causal differentiation path.
- Root and terminal states were objective if they were chosen from prior
  assumptions or heuristic diagnostics.
- Fate probabilities are experimentally validated cell fates.
- Trajectory output replaces annotation, marker review, or replicate-aware
  condition testing.

## Next Stage Routing

- Route to `09_embedding_visualization` when trajectory, fate, or velocity
  values need overlay plots on an existing embedding.
- Route to `12_annotation_support` when branch or terminal labels need
  marker-backed biological interpretation.
- Route to `13_signature_scoring` when ordered cells should be summarized by
  declared gene programs.
- Route to `14_aggregation_pseudobulk_de` for condition-level inference using
  sample-level replication and raw counts; do not use pseudotime output as a
  substitute for a valid design.
- Route back to `08_neighbor_graph` or `10_clustering` if graph or cluster
  state is missing, stale, or unsuitable.
- Route to `16_specialized_ecosystem` when the requested dynamic model belongs
  to a package family whose object state or concrete tool refs are not covered
  here.

## Backend-Neutral Rule

Do not place workflow-engine, shell, script, or notebook syntax in this skill.
Execution belongs in wrappers and adapters after the user approves the exact
operation, parameters, and artifacts.
