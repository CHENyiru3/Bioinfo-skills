# Bioinfo-Native Section SDD Plan

Status: accepted-for-implementation

This SPEC defines the next architecture step for Bioinfo-skills: a
bioinformatics-native, section-level Spec-Driven Development system. It adapts
the useful parts of Spec Kit's local workflow infrastructure pattern while
keeping the Bioinfo-skills ontology centered on biological state transitions,
approved analysis sections, executable wrappers, adapter bindings, and evidence.

The core SDD engine must stay domain-neutral. Concrete bioinformatics work
should be supplied by replaceable local capability packs: file-backed bundles
that declare workflows, task templates, stage skills, package refs, tool refs,
wrappers, adapters, checks, and Codex guidance for a domain/ecosystem.

## 1. Purpose

Bioinfo-skills should become a local, versionable SDD system for building
bioinformatics workflows one approved analysis section at a time.

The core unit is an analysis section, not a full project and not an individual
tool wrapper. A section represents one bounded scientific or data-state
transition, such as graph construction, clustering, marker ranking,
normalization, feature selection, or pseudobulk aggregation.

Each section must keep these decisions together:

- biological intent
- domain and ecosystem
- required input state
- produced output state
- selected skill, package, and tool references
- parameters and high-impact defaults
- wrapper and execution-adapter binding
- expected artifacts
- allowed and forbidden claims
- review gates
- validation and evidence

The goal is to make the agent workflow inspectable, reproducible, and
reviewable in Git without turning the system into a one-shot workflow compiler.

The second goal is replaceability. A graph-clustering section should be able to
bind a scRNA/scverse pack today, a Seurat pack later, or a different
bioinformatics domain pack without rewriting the SDD engine. The engine owns
state, validation, gates, and evidence. Packs own domain meaning and executable
bindings.

## 2. Reference Architecture Lessons

Spec Kit is used as an architecture reference, not as a dependency or blueprint
to copy wholesale.

Patterns to adopt:

- Store process state in the repository as durable files.
- Use templates for repeatable specs, plans, tasks, and evidence reports.
- Keep agent guidance in local command or skill assets.
- Persist workflow run state so interrupted work can resume.
- Add explicit review gates before implementation and before accepting results.
- Treat generated artifacts as managed project state that can be validated.
- Resolve workflows, task templates, checks, package refs, tool refs, wrappers,
  and adapters through explicit local manifests instead of hard-coded core
  assumptions.

Patterns to avoid in the first Bioinfo-skills implementation:

- No broad multi-agent adapter layer.
- No external plugin marketplace, installer, or remote preset package system.
- No generated workflow compiler.
- No agent CLI dispatch from inside the workflow engine.
- No heavy string-based prompt transformation pipeline.
- No dynamic loading of unreviewed executable code from arbitrary pack paths.

The v1 implementation should be Codex-first and Bioinfo-skills-native. It may
inspect Spec Kit source during implementation for design guidance, but copied
code requires explicit attribution and review.

## 3. Core Unit: Analysis Section

An analysis section is a bounded workflow segment that transforms or inspects a
declared biological data state.

Examples:

- inspect an AnnData object and report available state
- construct a neighbor graph from an existing representation
- compute UMAP coordinates from a declared graph
- assign Leiden clusters from a declared graph
- rank marker genes for existing groups
- score a gene signature
- aggregate raw counts into pseudobulk units

A section is valid only when it declares:

- `section_id`
- `domain`
- `ecosystem`
- `pack_refs`
- `workflow_ref`
- `stage_ids`
- `task_refs`
- `input_state`
- `output_state`
- `skill_refs`
- `package_refs`
- `tool_refs`
- `check_refs`
- `wrapper`
- `adapter`
- `parameters`
- `claims.allowed`
- `claims.forbidden`
- `expected_artifacts`
- `gates`

The section does not need to include all upstream and downstream workflow
stages. It should instead state its preconditions and its produced state so
neighboring sections can be composed later.

## 4. Replaceable Capability Packs

The SDD system should use plugin-like local capability packs, not hard-coded
domain behavior in the core engine.

A capability pack is a versioned repository-local bundle that can declare:

- `pack_id`, `schema_version`, `domain`, `ecosystems`, and supported section
  types.
- workflow profiles such as `bioinfo.sdd.workflow.section_default.v0`.
- task templates such as `scrna.scverse.task.graph_clustering.v0`.
- package refs and tool refs used by those tasks.
- stage skill refs and routing guidance.
- wrapper bindings and adapter bindings.
- deterministic checks exposed by stable check IDs.
- expected artifact contracts and evidence report templates.
- Codex skill guidance for creating or reviewing section artifacts.

Packs are deliberately file-backed and reviewable. They are "plugin-like" in
that sections resolve their workflow, tasks, tools, packages, wrappers, and
checks through manifests, but v1 should not implement a remote plugin manager
or arbitrary Python entry-point loading.

The core engine may know how to:

- read pack manifests
- resolve IDs to local files
- validate section references
- run approved deterministic check IDs
- render templates
- execute lifecycle steps
- persist state, logs, check results, gates, and evidence

The core engine must not know that graph clustering means Scanpy, Seurat,
Leiden, Snakemake, AnnData, or any other specific biological or backend choice.
Those choices belong to packs and section artifacts.

Minimum pack manifest shape:

```yaml
schema_version: "0.1.0"
pack_id: scrna.scverse.core
name: scRNA scverse core pack
domain: scrna
ecosystems: [scverse]
workflows:
  bioinfo.sdd.workflow.section_default.v0: sdd/workflows/section-sdd.yml
task_templates:
  scrna.scverse.task.graph_clustering.v0:
    stages: [08_neighbor_graph, 09_embedding_visualization, 10_clustering]
    skills:
      - scrna.scverse.workflow.neighbor_graph
      - scrna.scverse.workflow.embedding_visualization
      - scrna.scverse.workflow.clustering
    tool_slots:
      - slot_id: neighbor_graph
        stage_id: 08_neighbor_graph
        method_family: neighbor_graph
      - slot_id: embedding_visualization
        stage_id: 09_embedding_visualization
        method_family: graph_embedding
      - slot_id: clustering
        stage_id: 10_clustering
        method_family: graph_clustering
checks:
  - section_schema
  - section_catalog_links
  - wrapper_binding
  - adapter_binding
```

Pack replacement rules:

- A section must declare the pack IDs it depends on.
- A section must declare the workflow profile it runs.
- A section should declare task refs before choosing tool refs. Tool refs are
  implementation choices inside a task, not the task itself.
- Package refs and tool refs must resolve through the section's active
  installed-ref revision, not through the full pack or market catalog.
- Wrapper and adapter bindings should be selected by installed tool bundles or
  explicit section-local overrides.
- A replacement pack can satisfy the same task ref with different tool refs,
  wrappers, adapters, and checks if the input/output state and claims remain
  explicit.
- Evidence must record the actual pack IDs, workflow ref, task refs, tool refs,
  package refs, wrapper, adapter, and check IDs used for the run.

## 5. Tool Market And Installed Refs

Concrete tool and package references should live outside active SDD packs in an
inactive, repo-local tool market.

The market is a selectable registry, not the active section context:

- `tool_market/market.yml` indexes installable bundles.
- `tool_market/packages/` stores package refs.
- `tool_market/tools/` stores tool refs.
- `tool_market/bundles/` maps selectable bundles to task refs, stages, package
  refs, tool refs, wrappers, adapters, checks, allowed claims, and caveats.

Installing a bundle into a section creates section-local state:

- `installed_refs/selection.yml` records the active installed revision and
  active bundle IDs.
- `installed_refs/revisions/<rev_id>/manifest.yml` records source bundle IDs,
  copied refs, checksums, wrapper, adapter, checks, and install time.
- `installed_refs/revisions/<rev_id>/packages/` contains copied package refs.
- `installed_refs/revisions/<rev_id>/tools/` contains copied tool refs.

Installed refs are per-section. Replacing a tool bundle creates a new revision
and preserves older revisions for evidence reproducibility. Uninstalling or
deactivating a bundle must not delete historical revision directories.

## 6. Target Repository Layout

The refactor should add a package-backed SDD layer and durable section
artifacts. It should also add local capability-pack manifests so domain
behavior remains replaceable.

Target layout:

```text
tool_market/
  market.yml
  packages/
  tools/
  bundles/

sdd/
  README.md
  templates/
    section.yml
    spec.md
    plan.md
    tasks.md
    evidence.md
  workflows/
    section-sdd.yml
  packs/
    scrna_scverse/
      pack.yml
      README.md
  sections/
    <section_id>/
      section.yml
      spec.md
      plan.md
      tasks.md
      evidence.md
      gates.yml
      installed_refs/
        selection.yml
        revisions/
          <revision_id>/
            manifest.yml
            packages/
            tools/
      runs/
        <run_id>/
          state.json
          log.jsonl
          checks/
            <check_id>.json

src/
  bioinfo_sdd/
    __init__.py
    cli.py
    catalog.py
    checks.py
    frontmatter.py
    installed_refs.py
    io.py
    market.py
    models.py
    packs.py
    sections.py
    templates.py
    workflow.py

tests/
  sdd/
    test_pack_manifest.py
    test_pack_resolution.py
    test_section_schema.py
    test_section_templates.py
    test_workflow_gates.py
    test_workflow_resume.py
    test_check_registry.py
```

Existing standalone validator scripts may be refactored into package APIs and
removed if the command-line replacement is clear. The implementation does not
need to preserve old script paths if tests and documentation are updated in the
same change.

## 7. Section Artifact Contract

Each section folder is the durable SDD record for one analysis section.

Required files:

- `section.yml`: machine-readable source of truth.
- `spec.md`: user-facing scientific and behavioral specification.
- `plan.md`: implementation plan and adapter choice.
- `tasks.md`: ordered implementation and validation tasks.
- `evidence.md`: final report of checks, outputs, caveats, and acceptance.
- `gates.yml`: review-gate status.
- `runs/<run_id>/state.json`: workflow run state.
- `runs/<run_id>/log.jsonl`: append-only workflow event log.
- `runs/<run_id>/checks/*.json`: structured check results.

`section.yml` must remain the canonical machine-readable artifact. Markdown
files are review artifacts that explain and justify the machine-readable state.

Minimum `section.yml` shape:

```yaml
schema_version: "0.1.0"
section_id: scrna_graph_clustering_m1
domain: scrna
ecosystem: scverse
pack_refs: []
workflow_ref: bioinfo.sdd.workflow.section_default.v0
stage_ids: []
task_refs: []
input_state: []
output_state: []
skill_refs: []
package_refs: []
tool_refs: []
check_refs: []
wrapper: null
adapter: null
parameters: {}
expected_artifacts: []
claims:
  allowed: []
  forbidden: []
gates:
  spec_review: pending
  plan_review: pending
  task_review: pending
  evidence_acceptance: pending
```

The section contract should preserve two layers of meaning:

- Task refs describe the scientific/data-state operation, such as graph
  clustering.
- Tool/package refs describe one implementation of that task, such as Scanpy
  neighbors, UMAP, and Leiden.

This distinction is required for replacement. A section can keep the same task
and state contract while replacing the ecosystem, tools, package refs, wrapper,
or adapter after review.

`tool_refs`, `package_refs`, `wrapper`, `adapter`, and `check_refs` should be
materialized from the active section-local installed-ref revision after a tool
bundle is selected.

## 8. Workflow Lifecycle

The canonical section SDD lifecycle is:

1. Specify the section.
2. Review and approve the section spec.
3. Plan the implementation.
4. Review and approve the implementation plan.
5. Generate implementation and validation tasks.
6. Review and approve the task list.
7. Run structural, wrapper, and adapter checks.
8. Record evidence.
9. Review and accept or reject the evidence.

The first workflow engine should support only deterministic local step types:

- `validate_section`
- `gate`
- `run_check`
- `record_evidence`

Workflow definitions are also pack-resolved artifacts. The default v1 lifecycle
is `bioinfo.sdd.workflow.section_default.v0`, but a pack may provide a stricter
domain workflow with additional gates or checks if it still uses deterministic
step types.

The workflow engine must not dispatch Codex or any other AI agent. Codex guides
artifact creation through skills; the engine validates files, pauses at gates,
runs named checks, records results, and persists run state.

Gate behavior:

- A pending gate pauses the workflow.
- Approved gates allow the next step.
- Rejected gates stop the workflow and record the rejection reason.
- Resume reloads the run state and continues from the paused or failed step.

Run state must be stored under the relevant section directory instead of a
global hidden directory.

## 9. Codex-First Operating Model

Codex is the first target because this repository already uses `SKILL.md` as
the native guidance format.

Add local Codex skills under `.agents/skills/`:

- `bioinfo-sdd-spec-section/SKILL.md`
- `bioinfo-sdd-plan-section/SKILL.md`
- `bioinfo-sdd-tasks-section/SKILL.md`
- `bioinfo-sdd-evidence-section/SKILL.md`

These skills should instruct Codex to:

- load the entry and domain skill tree before choosing methods
- inspect declared pack manifests before choosing workflow, task, package, tool,
  wrapper, or adapter refs
- use `bioinfo-sdd market-list`, `market-show`, `install-tool-bundle`,
  `replace-tool-bundle`, and `installed-refs` for concrete tool selection
- inspect relevant stage skills, task refs, package refs, and tool refs
- write or update the section artifacts
- keep biological claims bounded
- use `bioinfo-sdd` validation commands
- stop at review gates

The skills should not duplicate large tool API references. They should route to
existing Bioinfo-skills refs through declared pack manifests.

## 10. Bioinformatics Guardrails

The SDD system must preserve the existing Bioinfo-skills guardrails:

- No hidden preprocessing inside downstream wrappers.
- No backend syntax in task or stage skills.
- No biological interpretation beyond approved evidence.
- Every executable section declares input and output object state.
- Every executable wrapper declares matrix/layer policy and keys written.
- Existing object keys are not overwritten without explicit approval.
- Wrapper execution tests and workflow dry-runs are separate evidence.
- Missing optional packages produce skipped checks, not false success.
- Condition-level differential expression must not be represented as marker
  ranking.
- State inspection is required when the input state is unknown.
- A pack must not hide preprocessing inside a task template, wrapper, or adapter
  that is presented as a downstream-only task.
- Replacing a tool/package pack must trigger review of input state, output
  state, parameters, claims, and evidence expectations.
- Agents should load installed section refs for the current section instead of
  scanning the full inactive tool market.

## 11. First Exemplar

The first proof section is:

```text
section_id: scrna_graph_clustering_m1
```

It covers these workflow stages:

- `08_neighbor_graph`
- `09_embedding_visualization`
- `10_clustering`

It binds this pack, workflow, and task:

- `pack_refs`: `scrna.scverse.core`
- `workflow_ref`: `bioinfo.sdd.workflow.section_default.v0`
- `task_refs`: `scrna.scverse.task.graph_clustering.v0`
- installed bundle: `scrna.scverse.bundle.scanpy_graph_clustering.v0`

It binds this package reference:

- `scrna.scverse.package.scanpy`

It binds these tool references:

- `scrna.scverse.tool.scanpy_neighbors`
- `scrna.scverse.tool.scanpy_umap`
- `scrna.scverse.tool.scanpy_leiden`

It uses this wrapper:

```text
wrappers/python/scanpy_neighbors_umap_leiden.py
```

It should add this Snakemake binding:

```text
workflow/rules/scrna_graph_clustering.smk
```

Deterministic exemplar parameters:

```yaml
representation_key: X_pca
neighbors_key: neighbors_x_pca
embedding_key: X_umap_neighbors_x_pca
cluster_key: leiden_neighbors_x_pca
n_neighbors: 3
n_pcs: 3
metric: euclidean
neighbors_method: umap
umap_min_dist: 0.5
umap_spread: 1.0
resolution: 0.5
random_state: 7
leiden_flavor: leidenalg
overwrite: false
```

Expected artifacts:

- output `.h5ad`
- embedding TSV
- cluster-size JSON
- resolved-parameter JSON
- software-version JSON
- workflow log
- evidence report

Allowed claims:

- neighbor graph was constructed from the declared representation
- UMAP coordinates were computed from the declared graph
- Leiden graph communities were assigned under the recorded parameters
- cluster-size summaries correspond to the declared cluster key

Forbidden claims:

- cell type annotation
- condition-level inference
- normalization
- feature selection
- PCA computation
- final biological state interpretation

## 12. Implementation Milestones

Milestone 1: SPEC and templates.

- Add this SPEC.
- Update `SPEC/README.md`.
- Add SDD artifact templates.
- Add a minimal SDD README.
- Add the pack manifest contract and first local scRNA/scverse pack manifest.
- Add the repo-local inactive tool market and first Scanpy bundles.

Milestone 2: package and CLI.

- Add `pyproject.toml`.
- Add `src/bioinfo_sdd/`.
- Implement section loading, writing, validation, and template rendering.
- Implement pack manifest loading and ID resolution.
- Implement market loading, installed-ref revisions, and install/replace
  commands.
- Implement a CLI entry point named `bioinfo-sdd`.

Milestone 3: validator migration.

- Move existing skill-tree, schema, backend-neutral, runtime-report, and
  Snakefile checks into package APIs.
- Expose migrated checks through stable check IDs that pack manifests can
  reference.
- Add `market_manifest`, `installed_refs`, and `task_slots_filled` checks.
- Update tests to call package APIs or the new CLI.
- Remove or deprecate standalone scripts only after equivalent commands exist.

Milestone 4: workflow engine.

- Implement `section-sdd.yml`.
- Implement run state, logs, gates, pause, reject, and resume.
- Implement deterministic step types only.

Milestone 5: Codex skills.

- Add section spec, plan, tasks, and evidence skills.
- Keep them small and route through pack manifests to the existing skill tree
  and refs.

Milestone 6: graph clustering exemplar.

- Add `sdd/sections/scrna_graph_clustering_m1/`.
- Declare pack refs, workflow ref, and task refs in `section.yml`.
- Select and install the Scanpy graph-clustering bundle so package refs, tool
  refs, check refs, wrapper, and adapter are materialized from the active
  section-local installed-ref revision.
- Add `workflow/rules/scrna_graph_clustering.smk`.
- Add pipeline config and provenance/evidence artifacts.
- Validate wrapper and adapter behavior with synthetic AnnData.

Milestone 7: docs and cleanup.

- Update `README.md`.
- Update `SPEC/README.md`.
- Update tests and remove stale status text.
- Ensure all structural checks and dependency-aware tests pass.

## 13. Acceptance Criteria

The SDD refactor is acceptable when:

- A new section can be created from templates.
- Section artifacts validate against the section schema.
- Pack manifests validate and resolve workflow, task, package, tool, wrapper,
  adapter, and check IDs.
- Market bundles validate and can be installed into a section-local installed
  revision.
- Section catalog links resolve only through active installed refs for package
  and tool refs.
- The core engine can run the same lifecycle using a workflow ref resolved from
  a pack manifest.
- The workflow run pauses at review gates.
- Approved gates allow workflow resume.
- Rejected gates stop the workflow and record the reason.
- Existing skill-tree validation still passes.
- Backend-neutral skill validation still passes.
- Existing wrapper tests pass or skip cleanly based on optional dependencies.
- The graph/clustering exemplar has complete spec, plan, tasks, evidence, gate
  state, and check logs.
- The graph/clustering Snakemake binding passes a dry-run or skips cleanly when
  Snakemake is unavailable.
- README and SPEC index describe the new SDD layer without claiming unsupported
  biological automation.

## 14. Test Plan

Add focused tests for:

- pack manifest schema validation
- pack ID and artifact resolution
- market manifest and bundle validation
- section-local install, replace, uninstall, and checksum validation
- task slot satisfaction from installed refs
- task refs resolving to package refs, tool refs, wrappers, adapters, and checks
- section YAML schema validation
- section template creation
- frontmatter parsing for existing skill and ref catalogs
- lookup of stage skills and tool refs by ID
- workflow gate pause, approve, reject, and resume
- run-state and log persistence
- check result recording
- migration of existing validators into package-backed checks
- graph/clustering section artifact completeness
- graph/clustering wrapper behavior with synthetic AnnData
- graph/clustering Snakemake binding behavior when Snakemake is installed

Dependency-aware behavior:

- If `anndata` or `scanpy` is absent, wrapper execution tests skip.
- If `snakemake` is absent, adapter execution tests skip.
- If `leidenalg` or `igraph` is absent, Leiden-specific execution checks skip
  with an explicit check result.
- Skipped checks must state the missing package and the skipped capability.

## 15. Non-Goals

- Do not build a full workflow compiler.
- Do not add a multi-agent adapter framework.
- Do not create a remote extension marketplace, installer, or dependency
  resolver for packs.
- Do not allow packs to silently load arbitrary unreviewed executable code.
- Do not install the full tool market into active SDD context.
- Do not dispatch Codex from the workflow engine.
- Do not make Snakemake the source of biological task meaning.
- Do not convert every package/tool ref into a top-level skill.
- Do not treat generated evidence as biological interpretation.

## 16. Compatibility Policy

The implementation may perform a full internal restructure when it improves
maintainability. Existing paths do not need to be preserved as public APIs.

However, any moved behavior must remain discoverable through:

- updated tests
- updated README/SPEC documentation
- new package-backed CLI commands
- clear migration notes in the implementation summary

The preferred stable interface after the refactor is `bioinfo-sdd`, not the old
standalone script paths.
