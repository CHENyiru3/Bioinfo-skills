---
id: scrna.scverse.workflow.specialized_ecosystem
schema_version: "0.1.0"
kind: skill
domain: scrna
stage: specialized_ecosystem
status: filled
state_in: ["declared specialized task", "task-specific AnnData, MuData, SpatialData, or package-compatible object state", "package runtime and reference availability"]
state_out: ["routing decision", "package-specific object-state plan", "package-specific outputs or gap report"]
registered_refs: [scrna.scverse.package.bento, scrna.scverse.package.biolord, scrna.scverse.package.cell2location, scrna.scverse.package.cellannotator, scrna.scverse.package.cellcharter, scrna.scverse.package.cellmapper, scrna.scverse.package.celloracle, scrna.scverse.package.cellphonedb, scrna.scverse.package.decoupler, scrna.scverse.package.dandelion, scrna.scverse.package.episcanpy, scrna.scverse.package.hotspot, scrna.scverse.package.infercnvpy, scrna.scverse.package.liana, scrna.scverse.package.mudata, scrna.scverse.package.muon, scrna.scverse.package.muon_tutorials, scrna.scverse.package.omicverse, scrna.scverse.package.pegasus, scrna.scverse.package.pertpy, scrna.scverse.package.popv, scrna.scverse.package.pyscenic, scrna.scverse.package.pyucell, scrna.scverse.package.rapids_singlecell, scrna.scverse.package.scgen, scrna.scverse.package.schist, scrna.scverse.package.scib, scrna.scverse.package.scirpy, scrna.scverse.package.scvi_tools, scrna.scverse.package.scyan, scrna.scverse.package.sincei, scrna.scverse.package.snapatac2, scrna.scverse.package.sopa, scrna.scverse.package.spatialdata, scrna.scverse.package.squidpy, scrna.scverse.package.tangram]
validation: [backend_neutral, state_contract_checked]
---
# Specialized Ecosystem

## Purpose

Route specialized scverse ecosystem requests that do not fit cleanly into the
core Scanpy-style workflow stages. This stage identifies the task family,
eligible package refs, required object state, missing concrete refs, runtime
constraints, expected outputs, and scientific caveats before any execution path
is selected.

This stage is a routing and requirements gate. It must not pretend that a
package-level ref is enough to execute a method when no concrete tool ref or
wrapper exists.

## When Required

- The user names a specialized package or asks for a task family outside the
  core stages, such as multimodal integration, spatial analysis, regulatory
  network inference, perturbation modeling, receptor analysis, CNV inference,
  ATAC/epigenomic analysis, spatial mapping, cell-cell communication, or
  large-scale acceleration.
- The task requires `MuData`, `SpatialData`, receptor contigs, image-linked
  spatial coordinates, chromatin accessibility matrices, copy-number state,
  regulatory networks, or package-specific model artifacts.
- The requested package has a repo-local package ref but no concrete tool ref,
  requiring a bounded package/tool fill unit before implementation.
- The user needs a feasibility decision based on package runtime status,
  object compatibility, and available metadata.

## When Optional

- A core stage already covers the requested operation with a documented tool
  ref, for example normalization, HVG selection, PCA, neighbor graph, embedding,
  clustering, marker ranking, signature scoring, pseudobulk aggregation, or
  trajectory routing.
- The user only wants a conceptual comparison of package families and no
  object will be consumed.
- The package-specific result already exists with provenance and the current
  task only needs downstream review through a core stage.

## When Forbidden

- Do not use this stage to bypass core stage state checks, statistical
  validity rules, or human approval.
- Do not claim a package can be executed when its runtime status is `missing`
  unless the user explicitly asks for planning rather than execution.
- Do not cite concrete package APIs, classes, command-line interfaces, or
  output keys as supported unless matching tool refs or wrappers exist in this
  repository.
- Do not route a task from package name alone; require the biological question,
  object type, required slots, and expected artifact shape.
- Do not mutate AnnData, MuData, SpatialData, or package-specific objects from
  this routing stage.

## Required Input State

- A clear specialized question, package request, or task family.
- Declared object type and location: AnnData, MuData, SpatialData, tabular
  inputs, image-linked spatial object, receptor object, model artifact, or
  other package-compatible object.
- Required slots and metadata for the task, such as expression layers,
  modalities, spatial coordinates, images, sample identifiers, conditions,
  perturbation labels, receptor chains, regions, peaks, copy-number references,
  or ligand-receptor resources.
- Runtime status and package ref for each candidate package.
- Decision on whether the current turn is only routing/planning or whether a
  new package/tool fill unit should be created before execution.

## Produced Output State

- Routing decision that selects a core workflow stage, a specialized package
  ref, or a gap report.
- Package-specific object-state plan describing required inputs, expected
  output keys or files, runtime constraints, validation checks, and caveats.
- List of missing package refs, missing concrete tool refs, missing runtime
  dependencies, or missing object slots that block execution.
- No object mutation unless a separate approved implementation step exists.

## User Decision Points

- Which specialized task family is in scope and which biological claim the user
  wants to support.
- Which package ref should be considered when multiple packages could address
  the same task.
- Whether missing runtime dependencies should block execution or be handled as
  planning-only evidence.
- Which object type, modality, coordinates, sample metadata, reference data,
  gene namespace, and output artifacts are required.
- Whether the next unit should be a package ref fill, concrete tool ref fill,
  wrapper implementation, or routing back to a core stage.
- How package-specific outputs should be validated before interpretation.

## Registered Package Refs

- Multimodal and data structures: `scrna.scverse.package.mudata`,
  `scrna.scverse.package.muon`, `scrna.scverse.package.muon_tutorials`.
- Spatial analysis and mapping: `scrna.scverse.package.spatialdata`,
  `scrna.scverse.package.squidpy`, `scrna.scverse.package.cell2location`,
  `scrna.scverse.package.tangram`, `scrna.scverse.package.sopa`,
  `scrna.scverse.package.bento`, `scrna.scverse.package.cellcharter`.
- Probabilistic, perturbation, and model-based analysis:
  `scrna.scverse.package.scvi_tools`, `scrna.scverse.package.pertpy`,
  `scrna.scverse.package.scgen`, `scrna.scverse.package.biolord`.
- Regulatory, activity, and gene-program analysis:
  `scrna.scverse.package.decoupler`, `scrna.scverse.package.pyscenic`,
  `scrna.scverse.package.celloracle`, `scrna.scverse.package.hotspot`,
  `scrna.scverse.package.pyucell`.
- Cell-cell communication: `scrna.scverse.package.liana`,
  `scrna.scverse.package.cellphonedb`.
- Immune receptor and cytometry-oriented analysis:
  `scrna.scverse.package.scirpy`, `scrna.scverse.package.dandelion`,
  `scrna.scverse.package.scyan`.
- CNV, epigenomics, and ATAC-oriented analysis:
  `scrna.scverse.package.infercnvpy`, `scrna.scverse.package.episcanpy`,
  `scrna.scverse.package.snapatac2`, `scrna.scverse.package.sincei`.
- Integration benchmarking, annotation, scale, clustering, and broad toolkits:
  `scrna.scverse.package.scib`, `scrna.scverse.package.cellmapper`,
  `scrna.scverse.package.popv`, `scrna.scverse.package.cellannotator`,
  `scrna.scverse.package.rapids_singlecell`, `scrna.scverse.package.pegasus`,
  `scrna.scverse.package.omicverse`, `scrna.scverse.package.schist`.

## Registered Tool Refs

- No stage-wide specialized ecosystem tool refs are registered. Existing core
  Scanpy tool refs belong to their core stages, and package-specific execution
  requires a concrete tool ref before implementation.

## Expected Artifacts

- Routing memo that records the selected task family, candidate package refs,
  runtime status, object requirements, missing refs, and next unit.
- Package feasibility report with input object type, required slots, expected
  outputs, validation checks, and scientific caveats.
- Gap report when a requested package exists only as a package-level ref or is
  missing from the runtime environment.
- If execution is later approved through a concrete tool ref, package-specific
  output files or object keys plus validation and provenance artifacts.

## Validation Checks

- Confirm every registered or selected package ref exists in this repository.
- Confirm runtime status is reported and not upgraded from `missing` by
  assumption.
- Confirm the requested task is not better served by an existing core workflow
  stage with stronger state checks.
- Confirm object type and required slots match the selected package family
  before implementation is proposed.
- Confirm a concrete tool ref exists before any wrapper or adapter execution is
  claimed as supported.
- Confirm package-specific outputs are named without overwriting existing
  object keys or files unless the user approves.
- Confirm allowed claims are limited to the selected package ref, available
  state, and validation evidence.

## Failure Modes

- The package ref exists but lacks enough object-state detail for the requested
  operation.
- The selected package is missing from the runtime environment.
- Required object modality, spatial coordinates, receptor fields, image data,
  reference resources, model artifacts, or metadata are absent.
- The task is actually a core stage problem and specialized routing would skip
  stronger checks.
- Gene namespace, species, assay, sample metadata, or coordinate system is
  incompatible with the selected package.
- Package outputs are too model-specific to interpret without additional
  diagnostics or domain review.
- GPU, memory, platform, or external resource constraints make execution
  impractical in the current environment.

## Allowed Claims

- A specialized task was routed to a package ref, core stage, or gap report.
- Required object state, runtime status, missing concrete refs, and validation
  needs were identified.
- Execution is blocked when package runtime, object state, or concrete tool
  references are insufficient.

## Forbidden Claims

- A package-specific analysis is executable because a package ref exists.
- A missing package is installed or usable.
- Package-level documentation implies a concrete supported API in this
  repository.
- Spatial, regulatory, communication, perturbation, immune, CNV, or multimodal
  claims are biologically valid without task-specific validation.
- Specialized outputs replace replicate-aware statistics, marker review, or
  human annotation approval when those are required.

## Next Stage Routing

- Route back to core workflow stages when the requested operation fits their
  state contract, especially `03_doublet_detection`, `07_batch_integration`,
  `12_annotation_support`, `13_signature_scoring`,
  `14_aggregation_pseudobulk_de`, or `15_trajectory_fate_velocity`.
- Route to a package-ref fill unit when the selected package ref lacks enough
  operational detail for the requested task.
- Route to a concrete tool-ref fill unit when the package ref is adequate but
  no executable entrypoint is documented.
- Route to wrapper and adapter implementation only after package ref, tool ref,
  input state, output artifacts, validation checks, and caveats are approved.

## Backend-Neutral Rule

Do not place workflow-engine, shell, script, or notebook syntax in this skill.
Execution belongs in wrappers and adapters after the user approves the exact
operation, parameters, and artifacts.
