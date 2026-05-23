# Scverse Content And Code Fill Plan

Status: draft

This SPEC defines how to turn the current scverse skill-system scaffold into
real filled content and executable code without losing the layered,
backend-neutral architecture.

The goal is continuous implementation, not a one-shot full workflow. Each
iteration should fill one bounded unit, validate it, report what changed, and
only then move to the next unit.

## 0. Reference Independence Rule

The skill set must work independently from the current collected Seurat and
scverse HTML/reference folders.

Archived tutorials, HTML pages, manifests, and API captures are source material
for building distilled package/tool references. They are not runtime
dependencies and should not be required for normal skill routing, wrapper
execution, tests, or workflow dry-runs.

This means:

- `SKILL.md` files must contain enough routing guidance to operate without
  opening archived HTML docs.
- package refs must summarize package role, supported stages, object-state
  assumptions, runtime status, and caveats without requiring external folders.
- tool refs must contain the API-critical usage pattern, high-impact
  parameters, input/output state, and failure modes needed for implementation.
- archived doc paths may be recorded as provenance or source pointers, but
  validators and wrappers must not require those paths to exist.
- if the local HTML/reference archive disappears, the skill tree should still
  route tasks, select refs, run wrappers, and validate known code.

Distillation and citation policy:

- Distill the operational content from the source HTML, tutorials, API pages,
  package documentation, or archived text. Do not paste long copied
  documentation into refs.
- Preserve the exact public documentation URL used when available.
- Preserve the documentation or package version used when available, for
  example `scanpy 1.11.5`, `anndata 0.12.13`, or a docs path such as
  `/en/stable/`.
- Preserve the source access date for any web or archived source.
- If the local HTML archive and the public source disagree, prefer the public
  version-specific documentation URL and record the archive path as supporting
  source material.
- If only archived content is available, record the archive path and mark the
  public URL or version as `unknown` until verified.
- Package and tool refs should cite sources as metadata plus a short
  `## Sources Used` section.

Recommended source metadata for refs:

```yaml
source_urls:
  - https://scanpy.readthedocs.io/en/stable/generated/scanpy.tl.leiden.html
source_version: scanpy 1.11.5
source_accessed_at: 2026-05-23
source_local_paths:
  - BioBrain/reference/scverse_docs/...
distillation_status: distilled
```

## 1. Current Baseline

The repository currently has the first scaffold:

- `SPEC/` architecture documents.
- `skills/` layered scRNA/scverse skill tree.
- `skills/scrna/scverse/workflow/00-16/SKILL.md` placeholders.
- `skills/scrna/scverse/refs/packages/` package reference placeholders.
- `skills/scrna/scverse/refs/tools/python/` initial Scanpy tool references.
- `schemas/` structural schemas.
- `contracts/` AnnData/scRNA state and statistical policy documents.
- `execution/adapters/` backend adapter templates.
- `scripts/` structural validators.
- `tests/` structural tests.

The repository does not yet have:

- real analysis wrappers
- real Snakemake workflow rules for analysis
- real pipeline specs for executable sections
- real `.h5ad` fixtures
- real biological output snapshots
- real runlogs from wrapper execution
- filled stage skill content beyond placeholders

This SPEC governs that next step.

## 2. Non-Negotiable Rules

1. Do not build a full workflow in one chat.
   Each implementation cycle handles one stage, one tool, or one wrapper.

2. Keep task skills backend-neutral.
   `skills/**/SKILL.md` files may describe routing, state, tool choices, and
   validation. They must not contain Snakemake rules, Nextflow processes, shell
   pipelines, or notebook execution assumptions.

3. Separate concept, API, code, and backend binding.

   ```text
   stage SKILL.md      = biological/task guidance
   package ref         = package-level role and availability
   tool ref            = concrete API and parameters
   wrapper             = executable Python/R code
   adapter binding     = Snakemake/Nextflow/bash/notebook run shape
   provenance/runlog   = evidence and caveats
   ```

4. Preserve AnnData state explicitly.
   Every executable wrapper must declare required input state, produced output
   state, matrix/layer policy, keys written, and keys it refuses to mutate.

5. Human-in-the-loop remains mandatory.
   Before implementing a biological transformation, summarize method, tool,
   parameters, expected outputs, validation, and caveats. Proceed only for that
   approved section.

6. Wrapper tests and backend dry-runs are different evidence.
   A wrapper execution test proves the script works. A Snakemake dry-run proves
   workflow structure. Neither substitutes for the other.

## 3. Target Code Layout

Add real executable code gradually under these locations:

```text
wrappers/
  python/
    inspect_anndata_state.py
    scanpy_rank_cluster_markers.py
    scanpy_neighbors_umap_leiden.py
  r/
    README.md

workflow/
  Snakefile
  rules/
    state_inspection.smk
    scrna_marker_ranking.smk
  envs/
    scverse.yaml

pipelines/
  specs/
    inspect_anndata_state_m0.pipeline.yml
    scrna_marker_ranking_m1.pipeline.yml
  manifests/
    toy_downstream_sample.tsv

runs/
  dryrun_<run_id>/
    provenance/
      runlog.json

tests/
  wrappers/
  workflow/
  fixtures/
    downstream_h5ad/
  expected/
```

The existing `execution/adapters/` directory remains the adapter pattern and
template library. The future `workflow/` directory holds actual project-level
Snakemake files for approved sections.

## 4. Fill Unit Types

### 4.1 Stage Skill Fill Unit

Purpose: replace a placeholder stage `SKILL.md` with usable routing guidance.

Must include:

- concise purpose
- when required
- when optional
- when forbidden
- required input state
- produced output state
- user decision points
- registered package refs
- registered tool refs
- expected artifacts
- validation checks
- failure modes
- allowed claims
- forbidden claims
- next stage routing

Must not include:

- wrapper implementation
- Snakemake syntax
- Nextflow syntax
- shell command pipelines
- full copied API docs

Definition of done:

- `scripts/validate_skill_tree.py` passes.
- `tests/test_backend_neutral_nodes.py` passes.
- the skill names the relevant refs without overloading the context.

### 4.2 Package Reference Fill Unit

Purpose: turn one package placeholder into a useful package-level guide.

Must include:

- package role in the scverse workflow
- supported stages
- required object state
- produced object state
- major API families
- install/runtime status
- optional source pointers to archived docs/tutorials when available
- public documentation URL and version used when available
- `## Sources Used`
- failure modes
- scientific caveats
- when to avoid

Definition of done:

- package ref frontmatter validates against `schemas/package_ref.schema.json`.
- package appears in runtime status report when importable or explicitly missing.
- refs do not pretend missing packages are installed.

### 4.3 Tool Reference Fill Unit

Purpose: document one concrete function, class, CLI, or R function well enough
to implement a wrapper later.

Must include:

- exact API entrypoint
- method family
- required AnnData/MuData state
- output keys or files
- important parameters and defaults
- high-impact tradeoffs
- minimal Python/R use case
- validation checks
- failure modes
- statistical caveats
- adapter notes
- public documentation URL and version used when available
- `## Sources Used`

Definition of done:

- tool ref frontmatter validates against `schemas/tool_ref.schema.json`.
- API examples are small and scoped.
- caveats prevent overclaiming.

### 4.4 Wrapper Code Fill Unit

Purpose: implement one executable biological or state-inspection operation.

Wrapper requirements:

- CLI arguments with explicit input/output paths.
- explicit parameter serialization.
- versions serialization.
- loud failure on invalid input state.
- no hidden preprocessing or extra stages.
- deterministic output naming through CLI args, not hardcoded paths.
- object-state mutation limited to the approved output keys.
- clear exit status and useful error messages.

Wrapper files should live under:

```text
wrappers/python/
wrappers/r/
```

Definition of done:

- focused unit tests under `tests/wrappers/`.
- wrapper smoke test on a tiny fixture.
- expected output shape checked.
- resolved parameters written.
- versions written.
- if AnnData is mutated, the mutation is documented and tested.

### 4.5 Execution Adapter Fill Unit

Purpose: bind one approved wrapper to one backend.

For Snakemake:

- rule calls only the wrapper
- no Scanpy or R analysis logic inside rule body
- config passed externally
- rule has input, output, log, benchmark, conda, params
- dry-run passes

Definition of done:

- `tests/workflow/` dry-run test passes.
- `scripts/inspect_snakefile_policy.py` exists before complex rules expand.
- dry-run evidence appears in a runlog or test output.

### 4.6 Provenance Fill Unit

Purpose: record what was planned or executed.

Must include:

- run id
- mode: dry-run, test-run, or real-run
- input paths and optional checksums
- output paths and optional checksums
- method/tool references
- wrapper path
- adapter path
- resolved parameters
- package versions
- allowed and forbidden scientific claims
- warnings and caveats

Definition of done:

- runlog validates against the provenance schema.
- dry-run logs do not imply real biological execution.

## 5. Recommended Implementation Order

### Phase A: Make The Scaffold Auditable

Goal: every content/code addition has a validator target.

Implement:

- schema validation helper for YAML/JSON frontmatter where feasible
- `scripts/inspect_snakefile_policy.py`
- stronger tests for required stage-skill sections
- stronger tests for package/tool ref required sections
- fixture manifest validation

Do not implement biological wrappers yet unless validation for them exists.

Done when:

- structural tests fail when a stage skill is missing required sections
- tool refs and package refs can be linted consistently

### Phase B: Fill State Inspection First

Goal: create a safe read-only entry operation for any future analysis.

Fill:

- `skills/scrna/scverse/workflow/00_state_inspection/SKILL.md`
- `skills/scrna/scverse/refs/packages/anndata.md`
- `skills/scrna/scverse/refs/packages/scanpy.md`
- `skills/scrna/scverse/refs/tools/python/scanpy_read_h5ad.md`

Add code:

- `wrappers/python/inspect_anndata_state.py`
- `tests/wrappers/test_inspect_anndata_state.py`
- tiny fixture or fixture builder for a minimal `.h5ad`

Expected outputs:

- state report JSON
- state report Markdown or TSV
- versions JSON

Done when:

- wrapper reads `.h5ad`
- reports `obs`, `var`, `layers`, `raw`, `obsm`, `obsp`, `uns`
- reports shape and matrix type
- flags ambiguous raw/log state
- performs no data mutation

### Phase C: Fill Downstream Marker Ranking M1

Goal: implement the first downstream analysis section.

Fill:

- `skills/scrna/scverse/workflow/11_marker_ranking/SKILL.md`
- `skills/scrna/scverse/refs/tools/python/scanpy_rank_genes_groups.md`
- method contract for marker ranking

Add code:

- `wrappers/python/scanpy_rank_cluster_markers.py`
- `tests/wrappers/test_scanpy_rank_cluster_markers.py`
- tiny clustered `.h5ad` fixture or deterministic fixture builder
- `workflow/Snakefile`
- `workflow/rules/scrna_marker_ranking.smk`
- `workflow/envs/scverse.yaml`
- `pipelines/specs/scrna_marker_ranking_m1.pipeline.yml`
- dry-run runlog

Required guardrails:

- call this "cluster marker ranking", not condition-level DE
- require existing group labels
- require explicit expression source: `.raw`, `.X`, or named layer
- report group sizes
- fail on missing groupby
- fail on missing requested layer/raw
- do not normalize, filter, integrate, cluster, or annotate
- include pseudoreplication caveat

Done when:

- wrapper fixture execution passes
- Snakemake dry-run passes
- runlog validates
- marker table includes method, groupby, reference, and expression source metadata

### Phase D: Fill Clustering As A Decision-Centered Skill

Goal: implement clustering as a human-in-the-loop method choice, not a hidden
pipeline step.

Fill:

- `skills/scrna/scverse/workflow/08_neighbor_graph/SKILL.md`
- `skills/scrna/scverse/workflow/09_embedding_visualization/SKILL.md`
- `skills/scrna/scverse/workflow/10_clustering/SKILL.md`
- `skills/scrna/scverse/refs/tools/python/scanpy_neighbors.md`
- `skills/scrna/scverse/refs/tools/python/scanpy_umap.md`
- `skills/scrna/scverse/refs/tools/python/scanpy_leiden.md`

Add code only after method approval:

- `wrappers/python/scanpy_neighbors_umap_leiden.py`
- tests for required representation and written keys
- adapter binding only after wrapper works

Required guardrails:

- require declared representation, usually `X_pca`
- produce declared `neighbors_key`, `embedding_key`, and `cluster_key`
- record resolution, random state, and representation used
- do not run normalization, HVG, or PCA unless a separate approved stage did so

Done when:

- wrapper can run on tiny fixture with existing representation
- changing resolution changes only approved cluster key/output metadata
- user-facing report explains cluster counts and parameter choices

### Phase E: Fill Normalization And Feature Selection Only After State Policy

Goal: support upstream-like transformations while preserving counts and
downstream validity.

Fill:

- `04_normalization_transform`
- `05_feature_selection`
- `06_dimensionality_reduction`

Add code later:

- normalization wrapper
- HVG wrapper
- PCA wrapper

Required guardrails:

- preserve raw counts in a declared layer
- never overwrite count source without explicit policy
- record normalization target sum and log transform
- record HVG flavor and batch key
- record PCA representation key

Done when:

- wrappers prove count preservation
- output keys match the AnnData contract
- downstream wrappers can consume the declared outputs

### Phase F: Fill Pseudobulk DE As A Guarded Later Path

Goal: keep condition-level inference separate from marker ranking.

Fill:

- `14_aggregation_pseudobulk_de`
- `decoupler`, `scanpy.get.aggregate`, and `pydeseq2` refs

Add code only after sample metadata contracts exist:

- pseudobulk aggregation wrapper
- DE testing wrapper
- sample/condition design validation

Required guardrails:

- require sample IDs
- require condition/design fields
- aggregate before condition-level testing
- forbid cell-level p-values as sample-level DE evidence

Done when:

- wrapper fails without replicate/sample structure
- runlog records statistical design
- output claims are condition-level only when design supports them

### Phase G: Expand Specialized Ecosystem Coverage

Goal: fill package/tool refs by distilling local archived tutorials and API
docs into self-contained references.

Priority packages:

- `scvi_tools`
- `scvelo`
- `cellrank`
- `squidpy`
- `scirpy`
- `pertpy`
- `decoupler`
- `infercnvpy`
- `moscot`
- `liana`

For each package:

- fill package ref
- add one or two high-value tool refs
- add runtime import status
- defer wrappers until a user-approved workflow stage needs them

## 6. Stage Priority Matrix

| Priority | Stage | Reason |
| --- | --- | --- |
| P0 | 00 state inspection | safe, read-only, required before all real work |
| P0 | 11 marker ranking | first downstream method, clear output table |
| P1 | 08 neighbor graph | required for embedding/clustering |
| P1 | 09 embedding visualization | common downstream output |
| P1 | 10 clustering | common decision-heavy task |
| P2 | 04 normalization | important but upstream state-sensitive |
| P2 | 05 feature selection | required before PCA in many workflows |
| P2 | 06 dimensionality reduction | feeds downstream graph/clustering |
| P2 | 13 signature scoring | useful downstream interpretation with bounded claims |
| P3 | 14 pseudobulk DE | statistically important but needs metadata contracts |
| P3 | 12 annotation support | useful but easy to overclaim |
| P3 | 15 trajectory/fate/velocity | specialized assumptions |
| P3 | 16 specialized ecosystem | package-specific expansion |

## 7. Per-Iteration Checklist

Every content/code fill iteration should answer:

```text
What stage is being filled?
What package/tool refs are touched?
What input state is required?
What output state is produced?
What user decision is needed?
What code, if any, will be executable?
What tests will prove it works?
What adapter binding, if any, is allowed?
What claims are allowed?
What claims are forbidden?
```

Before editing:

- read the stage skill
- read relevant package/tool refs
- read relevant AnnData contract sections
- inspect archived tutorials/API docs only as source material when needed

After editing:

- run structural validators
- run wrapper tests if wrapper code changed
- run backend dry-run if adapter binding changed
- report changed files, tests, and remaining caveats

## 8. Acceptance Criteria For The Next Milestone

The next milestone is not "complete scRNA workflow." It is:

```text
one filled state-inspection stage
one filled downstream marker-ranking stage
one inspected tiny h5ad fixture
one marker-ranking wrapper
one Snakemake dry-run binding
one runlog
tests proving structure, wrapper behavior, and backend dry-run
```

This milestone proves that the system can move from skill guidance to actual
controlled code while preserving the architecture.

## 9. Anti-Patterns To Reject

- adding wrappers before the skill and tool refs define state and caveats
- hiding normalization inside marker ranking or clustering wrappers
- using Snakemake as the source of task meaning
- treating marker ranking as condition-level differential expression
- making a workflow compiler before manual rules are proven
- filling package refs by copying long docs instead of distilling API-critical
  behavior
- making skills, validators, wrappers, or tests depend on archived HTML folders
- adding broad dependencies without runtime status and environment evidence
- generating biological interpretation without user-approved evidence
- moving to a new stage before the current stage has tests and a report

## 10. Living Backlog

Immediate backlog:

1. strengthen validators for required stage and reference sections
2. fill `00_state_inspection/SKILL.md`
3. implement `inspect_anndata_state.py`
4. create tiny AnnData fixture builder or fixture file policy
5. fill `11_marker_ranking/SKILL.md`
6. write marker-ranking method contract
7. implement `scanpy_rank_cluster_markers.py`
8. bind marker ranking through Snakemake dry-run
9. create runlog validation for the M1 dry-run

Deferred backlog:

- Nextflow adapter implementation
- Seurat/R wrappers
- pseudobulk DE wrappers
- trajectory/velocity wrappers
- built containers and lockfiles
- real multi-sample biological fixtures
- full report generation
