# scRNA Scverse Skill-System v0 SPEC

Status: draft

This SPEC defines the first scverse-focused skill system for `Bioinfo-skills`.
It is a living planning document for building a backend-neutral, state-gated
single-cell RNA analysis skill tree.

## 1. Purpose

The v0 system should help an agent and user reason through scverse/scRNA
analysis one validated section at a time. It should not be a one-shot workflow
generator. It should separate:

- task and stage skills: biological intent, AnnData state, routing, caveats
- package references: package-level documentation, install/runtime status
- tool references: concrete APIs, parameters, examples, and scientific limits
- execution adapters: Snakemake, Nextflow, bash, Python, Rscript, or notebook
  execution for an already approved task

The central abstraction is the state of an `AnnData`, `MuData`, or related
scverse object, not a workflow engine.

Core rule:

```text
Task nodes describe what scientific state transition is intended.
Package/tool references describe which APIs can perform it.
Execution adapters describe how a selected implementation is run.
```

Snakemake is the first durable execution adapter, but it is not the ontology.

## 2. Current Workspace Grounding

Current repository state:

- `Bioinfo-skills/` currently contains the general SPEC documents only.
- There is no runtime `skills/` tree yet.
- Local scverse references are available under the workspace, especially:
  - `BioBrain/reference/scverse_docs/`
  - `bioinfo_tutorial/scverse_ecosystem/`
  - `BioBrain/docs/ENVIRONMENTS.md`
- These local references are source material for distillation only. The skill
  tree, package/tool refs, validators, wrappers, and workflow tests must remain
  usable if those folders are absent.
- Distilled refs should cite the public documentation URL and documentation or
  package version used when available, while local HTML/archive paths remain
  optional source pointers rather than dependencies.
- Verified runtime information exists for a scverse environment, but the skill
  content must remain portable and repo-relative.

Important runtime facts discovered during planning:

- installed core packages include `scanpy 1.11.5`, `anndata 0.12.13`,
  `mudata 0.3.8`, `muon 0.1.7`, `spatialdata 0.7.3`, `squidpy 1.8.1`,
  `scvi-tools 1.4.2`, `scirpy 0.22.5`, `pertpy 1.0.3`,
  `decoupler 2.1.6`, `scvelo 0.3.4`, `cellrank 2.0.7`,
  `infercnvpy 0.6.1`, `moscot 0.5.0`, `scib 1.1.7`,
  `scFates 1.2.4`, `palantir 1.4.4`,
  `doubletdetection 4.3.0.post1`, and `pydeseq2 0.5.4`.
- many locally mirrored ecosystem packages are not currently installed.
- missing packages still need package-level nodes and runtime status records.

## 3. V0 Scope

V0 includes:

- `skills/` as the canonical project skill tree.
- a deep scRNA/scverse workflow-stage tree.
- package-level references for all locally listed scverse ecosystem packages.
- detailed Scanpy core API references first.
- machine-readable schemas for skill, reference, runtime, artifact, and
  provenance documents.
- explicit AnnData/scRNA state contracts and statistical validity policies.
- provenance templates for run manifests, decisions, artifacts, and software
  versions.
- container and lockfile template locations for later reproducible builds.
- fixture and expected-output manifests for later biological execution tests.
- structural placeholders for R/Seurat and Rscript execution.
- structural placeholders for Seurat and scverse/Seurat interoperability.
- a backend-neutral execution adapter model.
- Snakemake adapter templates as the first durable runner.
- runtime availability reporting under `reports/runtime/`.
- planned validators for skill tree structure and runtime availability.

V0 excludes:

- real biological wrappers.
- real Snakemake analysis rules.
- Nextflow implementation beyond placeholders.
- full Seurat/R API extraction.
- exhaustive function-level coverage for every ecosystem package.
- built Docker or Apptainer images.
- real binary `.h5ad` fixtures.
- a runtime provenance engine.
- a workflow compiler.
- automated biological interpretation without human approval.

## 4. Target Repository Layout

The SPEC authorizes this future structure. Creating the full skeleton is a
separate implementation step after this SPEC is accepted.

```text
skills/
  README.md
  entry/
    SKILL.md
  scrna/
    SKILL.md
    scverse/
      SKILL.md
      workflow/
        00_state_inspection/
          SKILL.md
        01_data_ingest/
          SKILL.md
        02_qc_metrics_filtering/
          SKILL.md
        03_doublet_detection/
          SKILL.md
        04_normalization_transform/
          SKILL.md
        05_feature_selection/
          SKILL.md
        06_dimensionality_reduction/
          SKILL.md
        07_batch_integration/
          SKILL.md
        08_neighbor_graph/
          SKILL.md
        09_embedding_visualization/
          SKILL.md
        10_clustering/
          SKILL.md
        11_marker_ranking/
          SKILL.md
        12_annotation_support/
          SKILL.md
        13_signature_scoring/
          SKILL.md
        14_aggregation_pseudobulk_de/
          SKILL.md
        15_trajectory_fate_velocity/
          SKILL.md
        16_specialized_ecosystem/
          SKILL.md
      refs/
        packages/
        tools/
          python/
          r/
      seurat/
        SKILL.md
        README.md
      interoperability/
        SKILL.md
        README.md

schemas/
  skill_manifest.schema.json
  package_ref.schema.json
  tool_ref.schema.json
  workflow_node.schema.json
  anndata_state.schema.json
  runtime_report.schema.json
  artifact_manifest.schema.json
  provenance_run_manifest.schema.json
  decision_log.schema.json

contracts/
  anndata_scrna_state_v0.yml
  layer_slot_policy.md
  obs_var_uns_schema.md
  embeddings_graph_schema.md
  scrna_required_metadata.md
  statistical_validity_policy.md

execution/
  adapters/
    snakemake/
      README.md
      python_rule_template.smk
      rscript_rule_template.smk
    nextflow/
      README.md
    bash/
      README.md
    python_script/
      README.md
    rscript/
      README.md
    ipython_notebook/
      README.md

envs/
  scverse-python.yml
  scverse-python-extra.txt
  r-seurat.yml
  r-seurat-optional.yml
  r-seurat-notebook.yml

containers/
  Dockerfile.scverse.template
  scverse.apptainer.def.template
  lockfiles/
    README.md
    scverse-python.conda-lock.placeholder.yml
    r-seurat.renv-decision.md

scripts/
  check_scverse_runtime.py
  render_skill_manifest.py
  # structural validators are exposed through bioinfo-sdd run-check

provenance/
  run_manifest.template.yml
  decision_log.template.yml
  artifact_manifest.template.yml
  software_versions.template.yml

reports/
  runtime/
    README.md

tests/
  fixtures/
    README.md
    fixtures_manifest.yml
  expected/
    README.md
    expected_snapshots_manifest.yml
  test_skill_tree_structure.py
  test_scverse_manifest_coverage.py
  test_backend_neutral_nodes.py
  test_anndata_state_contract.py
```

## 5. Backend-Neutral Layer Model

The skill system has four independent layers.

### 5.1 Task And Stage Skills

Task skills answer:

- What does the user want biologically or analytically?
- What input state is required?
- What output state should be produced?
- What user decisions are missing?
- What claims are allowed or forbidden?
- Which package/tool references are relevant?

Task skills must not contain backend syntax.

Forbidden in task nodes:

- Snakemake `rule`, `Snakefile`, `wildcards`, `snakemake.input`,
  `snakemake.output`, `threads`, or rule `params`
- Nextflow `process`, `channel`, or executor syntax
- shell pipes, redirection, heredocs, glob expansion, or bash variables
- notebook cell execution assumptions

### 5.2 Package References

Package references answer:

- What package exists?
- Which ecosystem and language does it belong to?
- What source docs were used, if known?
- What public documentation URL and version was distilled, if known?
- Is it installed in the current runtime?
- Which workflow stages can use it?
- What input state does it usually require?
- What outputs does it usually create?

### 5.3 Tool References

Tool references answer:

- Which function, class, CLI, or API entrypoint should be used?
- What parameters and defaults matter?
- What input state and output state are expected?
- What failure modes and caveats are known?
- What examples can guide a wrapper later?

Tool references may list compatible adapters, but runnable backend syntax
belongs in execution adapters.

### 5.4 Execution Adapters

Execution adapters answer:

- How does an approved task run in a concrete backend?
- How is the backend plan validated?
- How are logs, reports, versions, and provenance collected?

Snakemake is the first supported adapter. Other adapters are represented by
placeholders in v0.

## 6. Task Node Contract

Every workflow-stage `SKILL.md` should use Markdown with YAML frontmatter.

Minimum frontmatter:

```yaml
id:
schema_version:
kind: skill
domain:
stage:
status:
state_in:
state_out:
registered_refs:
validation:
```

Recommended body sections:

```text
# <Stage Name>

## Purpose
## When Required
## When Optional
## When Forbidden
## Required Input State
## Produced Output State
## User Decision Points
## Registered Package/Tool References
## Expected Artifacts
## Validation Checks
## Failure Modes
## Allowed Claims
## Forbidden Claims
## Next Stage Routing
```

Important semantic keys that stage nodes should emit or consume:

- `counts_layer`
- `expression_layer`
- `feature_mask_key`
- `representation_key`
- `integration_key`
- `neighbors_key`
- `embedding_key`
- `cluster_key`
- `marker_result_key`
- `annotation_key`
- `score_key`
- `pseudobulk_key`

These keys keep stages composable without assuming one fixed implementation.

## 7. Package Reference Contract

Package reference files should live under the tool market and be installed into
section-local `installed_refs/` revisions when selected:

```text
tool_market/packages/
sdd/sections/<section_id>/installed_refs/
```

Minimum frontmatter:

```yaml
id:
kind: package_ref
package:
import_name:
language:
ecosystem:
docs_local:
source_url:
source_urls:
source_version:
source_accessed_at:
source_local_paths:
distillation_status:
runtime_status:
workflow_stages:
install_probe:
import_probe:
```

Recommended body sections:

```text
# <Package>

## Role In Scverse Workflow
## Supported Stages
## Required Object State
## Produced Object State
## Main APIs Or Tool Families
## Runtime Availability
## Installation Notes
## Validation Checks
## Failure Modes
## Scientific Caveats
## When To Avoid
```

Runtime status values:

- `installed`
- `missing`
- `docs_only`
- `platform_limited`
- `gpu_limited`
- `waived_with_evidence`
- `unknown`

## 8. Tool Reference Contract

Tool references should live under the tool market and be installed into
section-local `installed_refs/` revisions when selected:

```text
tool_market/tools/
sdd/sections/<section_id>/installed_refs/
```

Minimum frontmatter:

```yaml
id:
kind: tool_ref
package_ref:
api_entrypoint:
method_family:
source_urls:
source_version:
source_accessed_at:
source_local_paths:
distillation_status:
state_in:
state_out:
parameters:
caveats:
compatible_adapters:
```

Recommended body sections:

```text
# <Tool Or API>

## Purpose
## When To Use
## When To Avoid
## Required Input State
## Produced Output State
## API Signature
## Parameters
## Defaults And Tradeoffs
## Minimal Example
## Validation Checks
## Failure Modes
## Scientific Caveats
## Adapter Notes
```

Adapter notes must stay declarative. Concrete rule/process/shell syntax belongs
under `execution/adapters/`.

## 9. Execution Adapter Contract

Each adapter should eventually provide:

- `capabilities`: DAG support, scatter/gather, conda, containers, dry-run,
  reports, provenance, cluster/cloud support
- `validate`: adapter-specific feasibility checks
- `plan`: execution plan without mutation
- `materialize`: backend-specific files
- `dry_run`: structural validation
- `execute`: real run after approval
- `collect_status`: per-task status and logs
- `collect_provenance`: versions, configs, parameters, outputs, caveats

V0 adapter status:

| Adapter | V0 Status | Notes |
| --- | --- | --- |
| Snakemake | template-level supported | first durable runner |
| Nextflow | placeholder | future workflow backend |
| bash | placeholder | useful for simple local tasks |
| Python script | placeholder | useful for wrapper development |
| Rscript | placeholder | reserved for Seurat/Bioconductor tools |
| IPython/notebook | placeholder | useful for exploratory organization |

Snakemake adapter constraints:

- keep analysis logic out of the Snakefile
- call approved scripts or wrappers
- pass configuration externally
- support dry-run validation
- collect logs, benchmark, versions, outputs, and runlog metadata

## 10. Scverse Workflow Stage Registry

### Stage 00: State Inspection

Purpose: classify current object/data state before transformation.

Input state:

- declared dataset paths or existing `AnnData`/`MuData`
- known organism, modality, and sample/batch fields if available

Produced state:

- state JSON/Markdown report only
- no data mutation

Must record:

- object shape
- `X` type and sparse/dense/backed status
- `obs`, `var`, `layers`, `raw`, `obsm`, `obsp`, `uns` keys
- uniqueness of `obs_names` and `var_names`
- raw count versus normalized/log ambiguity
- sample/batch key candidates

Primary APIs:

- `anndata.AnnData`
- `scanpy.read_h5ad`
- `mudata.read_h5mu`
- AnnData key inspection methods

Forbidden:

- normalization
- filtering
- writing `.h5ad`
- any backend syntax

Failure modes:

- ambiguous count state
- duplicate names
- absent batch metadata
- mixed modalities treated as single RNA counts

### Stage 01: Data Ingest

Purpose: construct a canonical scverse object from source files.

Input state:

- source path
- declared format
- sample metadata

Produced state:

- `AnnData` with raw count matrix in `.X` or preserved in `layers["counts"]`
- `.obs` sample/batch annotations
- `.var` gene identifiers, symbols, and feature types

Primary APIs:

- `scanpy.read_10x_mtx`
- `scanpy.read_10x_h5`
- `scanpy.read_h5ad`
- `scanpy.read_mtx`
- `anndata.concat`

Forbidden:

- filtering
- log transformation
- losing raw counts

Failure modes:

- wrong matrix orientation
- duplicate gene symbols
- missing 10x files
- accidental ADT/HTO inclusion or exclusion

### Stage 02: QC Metrics And Filtering

Purpose: compute QC metrics, review distributions, and apply explicit filters.

Input state:

- raw-count `AnnData`
- organism-specific mitochondrial, ribosomal, or hemoglobin masks

Produced state:

- `.obs` QC columns such as `total_counts`, `n_genes_by_counts`,
  `pct_counts_mt`
- `.var` QC columns such as `n_cells_by_counts`
- filtered object only after threshold approval

Primary APIs:

- `scanpy.pp.calculate_qc_metrics`
- `scanpy.pp.filter_cells`
- `scanpy.pp.filter_genes`
- `scanpy.pl.violin`
- `scanpy.pl.scatter`

Forbidden:

- aggressive hard-coded thresholds without review
- filtering doublets before doublet detection
- treating high mitochondrial percentage as universally invalid biology

Failure modes:

- organism prefix mismatch, such as `MT-` versus `Mt-`
- empty dataset after filtering
- thresholds computed on log data

### Stage 03: Doublet Detection

Purpose: annotate likely technical doublets before downstream analysis.

Input state:

- post-basic-QC raw-count `AnnData`
- `batch_key` or sample key for multi-sample data

Produced state:

- `.obs["doublet_score"]`
- `.obs["predicted_doublet"]`
- optional singlet mask after review

Primary APIs:

- `scanpy.pp.scrublet`
- `scanpy.pp.scrublet_simulate_doublets`
- `scanpy.pl.scrublet_score_distribution`
- optional `doubletdetection`

Forbidden:

- silently dropping predicted doublets
- claiming biological doublet identity from score alone
- running raw-count methods on log-normalized data

Failure modes:

- wrong expected doublet rate
- mixed samples without `batch_key`
- over-removal of rare transitional states

### Stage 04: Normalization And Transform

Purpose: preserve raw counts and create analysis-scale expression.

Input state:

- QC/doublet-annotated `AnnData` with raw counts retained

Produced state:

- normalized/log expression in declared target
- raw counts preserved in `layers["counts"]` or equivalent
- transform parameters and raw-count preservation check

Primary APIs:

- `scanpy.pp.normalize_total`
- `scanpy.pp.log1p`

Forbidden:

- double `log1p`
- losing raw counts
- HVG selection in this stage

Boundary:

- HVG belongs to Stage 05, not Stage 04.

Failure modes:

- raw counts lost
- wrong transform order
- memory issues on large sparse matrices

### Stage 05: Feature Selection

Purpose: select informative genes before PCA and graph construction.

Input state:

- normalized/log expression for default HVG flavors
- raw counts for `seurat_v3`
- optional `obs[batch_key]`

Produced state:

- `var["highly_variable"]`
- HVG metrics
- `feature_mask_key`
- optional `uns["hvg"]`

Primary APIs:

- `scanpy.pp.highly_variable_genes`
- `scanpy.pl.highly_variable_genes`

Forbidden:

- silent physical gene dropping without provenance
- wrong count/log state for chosen flavor

Failure modes:

- missing `batch_key`
- too few genes
- missing `scikit-misc`
- HVGs dominated by batch or QC signal

### Stage 06: Dimensionality Reduction

Purpose: compute low-dimensional representation for graph construction.

Input state:

- normalized/log expression
- `feature_mask_key` or explicit feature mask

Produced state:

- `obsm["X_pca"]` or another declared representation
- `varm["PCs"]`
- `uns["pca"]`
- `representation_key`

Primary APIs:

- `scanpy.pp.pca`
- PCA plotting APIs

Forbidden:

- hidden PCA inside neighbor graph stage
- assuming PCA is the only valid representation

Failure modes:

- empty feature mask
- too many PCs
- memory issues
- PCs driven by QC or batch

### Stage 07: Batch Integration

Purpose: conditionally correct or align batch effects.

Input state:

- batch labels in `.obs`
- PCA or other representation
- explicit integration goal

Produced state:

- integrated representation
- graph
- corrected matrix
- or query/reference mapping

Primary APIs and packages:

- `scanpy.external.pp.bbknn`
- `scanpy.external.pp.harmony_integrate`
- `scanpy.external.pp.scanorama_integrate`
- `scanpy.external.pp.mnn_correct`
- `scanpy.pp.combat`
- `scanpy.tl.ingest`
- `scvi-tools`

Forbidden:

- overwriting biological signal blindly
- using corrected matrices for DE without caveat

Failure modes:

- overcorrection
- confounded batch/design
- missing package
- query/reference mismatch

### Stage 08: Neighbor Graph

Purpose: construct kNN/connectivity graph for embeddings and graph clustering.

Input state:

- selected `representation_key`
- or existing graph from graph-producing integration

Produced state:

- `obsp["distances"]`
- `obsp["connectivities"]`
- `uns["neighbors"]`
- `neighbors_key`

Primary APIs:

- `scanpy.pp.neighbors`
- optional `rapids_singlecell`

Forbidden:

- accidental high-dimensional `.X` fallback
- overwriting alternate graphs without keying

Failure modes:

- missing representation
- excessive `n_pcs`
- disconnected graph
- poor batch mixing

### Stage 09: Embedding And Visualization

Purpose: produce visual diagnostics from graph topology.

Input state:

- `neighbors_key`
- graph connectivities

Produced state:

- `obsm["X_umap"]` or other embedding
- `embedding_key`
- plot files

Primary APIs:

- `scanpy.tl.umap`
- `scanpy.pl.umap`
- `scanpy.tl.tsne`
- `scanpy.tl.diffmap`
- `scanpy.tl.embedding_density`

Forbidden:

- clustering on UMAP without explicit approval
- treating UMAP distances as primary statistical evidence

Failure modes:

- stale graph key
- stochastic layout differences
- misleading overcorrection visualizations

### Stage 10: Clustering

Purpose: assign graph communities for annotation and marker analysis.

Input state:

- `neighbors_key`

Produced state:

- `.obs[cluster_key]`
- cluster-size table
- cluster parameter metadata

Primary APIs:

- `scanpy.tl.leiden`
- legacy `scanpy.tl.louvain`
- optional graph clustering ecosystem packages

Forbidden:

- treating clusters as cell types without marker/reference evidence
- overwriting existing labels without a new key

Failure modes:

- overclustering
- underclustering
- batch-driven clusters
- unstable small clusters

### Stage 11: Marker Ranking

Purpose: rank genes that characterize existing groups.

Input state:

- `cluster_key` or other valid group key
- declared expression source
- logarithmized data for Scanpy marker ranking

Produced state:

- marker TSV/JSON tables
- `adata.uns[marker_result_key]`
- marker plots
- group-size summary

Primary APIs:

- `scanpy.tl.rank_genes_groups`
- `scanpy.get.rank_genes_groups_df`
- `scanpy.tl.filter_rank_genes_groups`
- `scanpy.pl.rank_genes_groups_*`

Forbidden:

- condition-level DE claims
- replicate-aware DE claims
- treating cells as biological replicates

Failure modes:

- wrong raw/layer selection
- small groups
- sparse genes
- inflated p-values from cell-level comparisons

### Stage 12: Annotation Support

Purpose: create candidate labels with evidence and human review.

Input state:

- marker ranking outputs
- cluster key
- species/gene ID convention
- curated markers or reference object

Produced state:

- annotation candidate table
- evidence/confidence table
- optional final annotation key after approval

Primary APIs and packages:

- `scanpy.tl.marker_gene_overlap`
- `scanpy.tl.ingest`
- `scvi-tools` scANVI
- future PopV/cellmapper references

Forbidden:

- silent auto-labeling from one marker
- overwriting curated labels without approval

Failure modes:

- reference mismatch
- gene symbol mismatch
- rare or transitional populations forced into labels

### Stage 13: Signature Scoring

Purpose: quantify activity of gene programs, cell-cycle signatures, pathways,
or regulator networks.

Input state:

- declared expression source
- validated signature table/list
- gene ID mapping
- minimum overlap threshold

Produced state:

- `.obs` score columns
- score matrices
- missing-gene report
- embedding overlays and distribution plots

Primary APIs and packages:

- `scanpy.tl.score_genes`
- `scanpy.tl.score_genes_cell_cycle`
- `decoupler`
- future `pyucell`

Forbidden:

- inventing signatures
- mixing species or gene namespaces
- claiming causal pathway activation from a score alone

Failure modes:

- low signature overlap
- dropout sensitivity
- bad control gene pool
- wrong normalization state

### Stage 14: Aggregation And Pseudobulk DE

Purpose: aggregate cells by biological sample/group and perform
replicate-aware condition testing.

Input state:

- raw integer counts
- sample key
- group/cell-type key
- condition and covariate metadata
- valid design and contrast

Produced state:

- pseudobulk `AnnData` or matrices
- cell-count and count-depth summaries
- DE tables
- model logs and plots

Primary APIs and packages:

- `decoupler.pp.pseudobulk`
- `decoupler.pp.filter_samples`
- `decoupler.pp.filter_by_expr`
- `scanpy.get.aggregate` for non-model aggregation
- `pydeseq2`
- `pertpy.tools.PyDESeq2`
- future R edgeR/DESeq2 references

Forbidden:

- DESeq2/PyDESeq2 on log-normalized means
- treating cells as replicates
- testing designs with no replication

Boundary:

- split into two durable nodes later:
  - `aggregate_pseudobulk`
  - `test_pseudobulk_de`

Failure modes:

- rank-deficient design
- non-integer counts
- too few replicates
- compositional confounding
- all-zero genes

### Stage 15: Trajectory, Fate, And Velocity

Purpose: model pseudotime, fate probabilities, RNA velocity, or dynamic paths.

Input state:

- graph/embedding and cluster state for topology methods
- root/terminal/time decisions where required
- spliced/unspliced layers for velocity methods

Produced state:

- pseudotime columns
- PAGA graphs
- velocity graphs
- fate probabilities
- trajectory plots and diagnostics

Primary APIs and packages:

- `scanpy.tl.paga`
- `scanpy.tl.dpt`
- `scvelo`
- `cellrank`
- `palantir`
- `moscot`
- `scFates`
- future `dynamo`

Forbidden:

- hidden root/terminal choices
- causal lineage claims without appropriate design
- velocity analysis without velocity-compatible layers

Failure modes:

- invalid root state
- weak graph topology
- missing velocity layers
- terminal-state disagreement
- overinterpreted pseudotime

### Stage 16: Specialized Ecosystem

Purpose: route specialized tasks that do not fit the core Scanpy flow.

Package families:

- multimodal/spatial: `mudata`, `muon`, `spatialdata`, `squidpy`
- probabilistic and perturbation: `scvi-tools`, `pertpy`, `scgen`,
  `biolord`
- regulatory and activity: `decoupler`, `pyscenic`, `celloracle`,
  `hotspot`, `pyucell`
- cell-cell communication: `liana`, `cellphonedb`
- spatial mapping and domains: `cell2location`, `tangram`, `sopa`,
  `bento`, `cellcharter`
- immune receptor and cytometry: `scirpy`, `dandelion`, `scyan`
- CNV, epigenomics, ATAC: `infercnvpy`, `episcanpy`, `SnapATAC2`,
  `sincei`
- integration, QC, annotation: `scib`, `doubletdetection`,
  `cellmapper`, `popv`, `cellannotator`
- DE, workflow, scale, clustering: `pydeseq2`, `rapids_singlecell`,
  `pegasus`, `omicverse`, `schist`

Each package node must record:

- required object type and object slots
- expected outputs
- install/import status
- platform or GPU constraints
- scientific caveats
- supported workflow stages

## 11. Ecosystem Coverage Plan

Source manifests:

- `bioinfo_tutorial/scverse_ecosystem/core_docs_manifest.tsv`
- `bioinfo_tutorial/scverse_ecosystem/community/python_docs_manifest.tsv`
- `BioBrain/reference/scverse_docs/README.md`

Coverage levels:

| Level | Meaning |
| --- | --- |
| Level 1 | package node exists with docs path and runtime status |
| Level 2 | package maps to workflow stages and required input state |
| Level 3 | key APIs/tools extracted |
| Level 4 | runnable example or wrapper template |
| Level 5 | execution adapter binding and tests |

V0 target:

- all manifest packages reach Level 1
- Scanpy core reaches Level 3
- Snakemake reaches adapter-template level
- R/Seurat placeholders exist and are marked incomplete

Packages not installed locally are not skipped. They receive package nodes with
runtime status `missing`, `docs_only`, `platform_limited`, or
`waived_with_evidence` as appropriate.

## 12. Runtime Availability Tracking

Runtime reports should live under:

```text
reports/runtime/
```

Report fields:

- timestamp
- workspace
- runtime profile
- package
- distribution name
- import name
- executable name where relevant
- expected version or version range
- discovered version
- import probe
- install attempt status
- failure reason
- waiver reason
- recommended next action

Installation policy:

- prefer conda/mamba where appropriate
- use pip fallback when appropriate
- attempt install/import checks for all listed packages
- allow waivers for GPU-heavy or platform-limited packages only with evidence

The skill content should not hard-code the current workspace environment path.
Runtime checks may read local configuration and generate local reports.

## 13. AnnData State And Statistical Contracts

The v0 system should include explicit contracts rather than relying only on
prose in `SKILL.md` files.

Default AnnData/scRNA state conventions:

```text
adata.layers["counts"]      raw UMI counts when available
adata.X                     current working matrix, never assumed raw
adata.layers["log1p_norm"]  log-normalized expression when produced
adata.raw                   optional frozen reference, policy-controlled
adata.obs["sample_id"]      required for pseudobulk and condition analysis
adata.obs["batch"]          required before batch integration
adata.obsm["X_pca"]         PCA or declared representation
adata.obsm["X_umap"]        embedding artifact
adata.uns["neighbors"]      graph metadata
adata.uns["bioinfo_skills"] provenance and parameter log
```

Statistical validity boundaries:

- marker ranking is descriptive group marker discovery and must not be called
  replicate-aware condition-level differential expression.
- pseudobulk DE is a guarded sample-level path requiring raw counts, sample
  metadata, replicate structure, and a valid design.
- annotation support produces evidence and candidate labels; final labels
  require a human approval gate.
- signature scoring produces relative scores and must not be framed as causal
  pathway proof.

The contract layer should include:

- `contracts/anndata_scrna_state_v0.yml`
- `contracts/layer_slot_policy.md`
- `contracts/obs_var_uns_schema.md`
- `contracts/embeddings_graph_schema.md`
- `contracts/scrna_required_metadata.md`
- `contracts/statistical_validity_policy.md`

## 14. Validation Plan

Validator:

```text
bioinfo-sdd run-check skill_tree
```

Checks:

- required skill nodes exist
- required YAML frontmatter keys exist
- task nodes contain no backend-specific syntax
- all manifest packages have package references
- all registered references resolve
- Scanpy core references cover major stage APIs
- R placeholders are clearly incomplete
- execution adapters are separate from task nodes
- schemas and templates are present
- AnnData state contracts are present
- provenance templates validate against schema
- fixture and expected-output manifests exist

Future runtime checker:

```text
scripts/check_scverse_runtime.py
```

Checks:

- package import status
- package versions
- executable availability
- activation context
- missing packages
- waived packages
- generated TSV/JSON/Markdown reports

## 15. Implementation Phases

Phase 1: SPEC alignment

- status: in progress
- outputs:
  - update core SPEC to backend-neutral language
  - add this scverse v0 SPEC
  - update SPEC index
- done when:
  - SPEC documents agree that Snakemake is an adapter
  - v0 structure and stage registry are documented

Phase 2: skill-tree skeleton

- outputs:
  - `skills/entry/SKILL.md`
  - `skills/scrna/SKILL.md`
  - `skills/scrna/scverse/SKILL.md`
  - `skills/scrna/scverse/workflow/*/SKILL.md`
  - `skills/scrna/seurat/` placeholder
  - `skills/scrna/interoperability/` placeholder
- done when:
  - all stage files exist
  - frontmatter passes the planned validator

Phase 3: contract and schema scaffolding

- outputs:
  - `schemas/`
  - `contracts/`
  - `provenance/`
- done when:
  - schema and contract files exist
  - AnnData and statistical validity policies are explicit

Phase 4: package reference skeleton

- outputs:
  - one package node for every local manifest package
- done when:
  - every package has docs path, runtime status, and workflow-stage mapping

Phase 5: Scanpy core tool references

- outputs:
  - detailed API references for Scanpy core workflow stages
- done when:
  - state inspection through marker ranking has key API coverage

Phase 6: execution adapter templates

- outputs:
  - Snakemake Python and Rscript rule templates
  - placeholder adapter READMEs for other backends
- done when:
  - adapter docs do not leak into task nodes

Phase 7: containers, fixtures, and runtime availability checks

- outputs:
  - environment specs
  - container templates
  - fixture manifests
  - package probe script
  - generated report area
- done when:
  - installed, missing, failed, and waived packages are recorded

Phase 8: validators and review

- outputs:
  - skill-tree validator
  - runtime checker
  - acceptance report
- done when:
  - structure validates
  - package coverage validates
  - backend-neutral checks pass

## 16. Acceptance Criteria

V0 is acceptable when:

- the core SPEC is backend-neutral
- the scverse v0 SPEC defines all planned layers
- the 00-16 workflow stage registry is documented
- package/tool references are independent of execution backends
- Snakemake is described as the first adapter, not the ontology
- all manifest packages have a coverage plan
- marker ranking and pseudobulk DE are clearly separated
- schemas, contracts, provenance templates, container templates, and fixture
  manifests exist
- Seurat and interoperability placeholders are present and clearly incomplete
- runtime availability reporting is specified
- the next implementation step can create the skill skeleton without making
  architectural decisions
