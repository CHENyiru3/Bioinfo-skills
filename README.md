# Bioinfo-skills

Bioinfo-skills is a repo-local skill, reference, and section-SDD system for
building bioinformatics workflows one approved analysis section at a time.

The project is designed for humans and Codex-style agents working together.
Skills describe biological intent and state transitions, SDD section artifacts
record decisions and review gates, and executable wrappers/adapters do only the
approved work for the selected section.

The current v0 focus is scRNA/scverse workflows centered on explicit AnnData
state transitions. Tool and package choices are intentionally replaceable:
concrete refs live in the inactive `tool_market/`, and a selected bundle is
copied into a section-local `installed_refs/` revision before it becomes active
context.

## Core Model

- `skills/`: routing and stage guidance for biological workflow intent.
- `sdd/sections/<section_id>/`: durable section specs, plans, tasks, gates,
  evidence, run state, and active installed refs.
- `tool_market/`: inactive source registry of selectable tool bundles and
  package/tool refs.
- `wrappers/`: approved executable units that perform bounded operations.
- `workflow/`: execution-adapter bindings, with Snakemake first.
- `src/bioinfo_sdd/`: package-backed CLI, validation checks, pack resolution,
  installed-ref management, and workflow state handling.

The SDD engine stays domain-neutral. Capability packs under `sdd/packs/`
declare domain workflows, task templates, stage skills, checks, wrappers, and
adapters. The first pack is `scrna.scverse.core`.

## Quickstart

Run commands from the repository root. After package installation, use
`bioinfo-sdd`; during local development, use:

```bash
PYTHONPATH=src python -m bioinfo_sdd --help
```

Inspect installable tool bundles:

```bash
PYTHONPATH=src python -m bioinfo_sdd market-list
PYTHONPATH=src python -m bioinfo_sdd market-show scrna.scverse.bundle.scanpy_graph_clustering.v0
```

Validate the graph-clustering exemplar:

```bash
PYTHONPATH=src python -m bioinfo_sdd validate-section scrna_graph_clustering_m1
PYTHONPATH=src python -m bioinfo_sdd installed-refs scrna_graph_clustering_m1
PYTHONPATH=src python -m bioinfo_sdd run-check section_catalog_links --section scrna_graph_clustering_m1
PYTHONPATH=src python -m bioinfo_sdd run-check installed_refs --section scrna_graph_clustering_m1
PYTHONPATH=src python -m bioinfo_sdd run-check task_slots_filled --section scrna_graph_clustering_m1
```

Run or resume the section workflow:

```bash
PYTHONPATH=src python -m bioinfo_sdd run-workflow scrna_graph_clustering_m1 --run-id local-review
PYTHONPATH=src python -m bioinfo_sdd set-gate scrna_graph_clustering_m1 spec_review approved --reason "reviewed"
```

Create a new section from templates:

```bash
PYTHONPATH=src python -m bioinfo_sdd create-section scrna_example_m1
PYTHONPATH=src python -m bioinfo_sdd market-list --task-ref scrna.scverse.task.graph_clustering.v0
PYTHONPATH=src python -m bioinfo_sdd install-tool-bundle scrna_example_m1 scrna.scverse.bundle.scanpy_graph_clustering.v0
PYTHONPATH=src python -m bioinfo_sdd validate-section scrna_example_m1
```

## Current Exemplar

`sdd/sections/scrna_graph_clustering_m1/` is the first complete section
example. It binds:

- task: `scrna.scverse.task.graph_clustering.v0`
- bundle: `scrna.scverse.bundle.scanpy_graph_clustering.v0`
- package ref: `scrna.scverse.package.scanpy`
- tool refs: Scanpy neighbors, UMAP, and Leiden
- wrapper: `wrappers/python/scanpy_neighbors_umap_leiden.py`
- adapter: `workflow/rules/scrna_graph_clustering.smk`

The allowed claims are limited to graph construction, UMAP coordinates, Leiden
community labels, and cluster-size summaries for declared keys. The section
does not claim normalization, feature selection, PCA computation, annotation,
condition-level inference, or final biological interpretation.

## Validation

List all deterministic checks:

```bash
PYTHONPATH=src python -m bioinfo_sdd list-checks
```

Common repository checks:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m bioinfo_sdd run-check market_manifest
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m bioinfo_sdd run-check runtime_report
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m bioinfo_sdd run-check skill_tree
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m bioinfo_sdd run-check snakemake_policy
```

Regenerate the scverse runtime report from market package refs:

```bash
PYTHONDONTWRITEBYTECODE=1 python scripts/check_scverse_runtime.py
```

## Guardrails

- Do not hide preprocessing inside downstream wrappers.
- Do not treat Snakemake or any execution backend as the source of biological
  task meaning.
- Do not load the whole tool market into active section context; install only
  selected bundles into `installed_refs/`.
- Do not expand biological claims beyond the approved section evidence.
- Do not treat marker ranking as condition-level differential expression.

## More Detail

- `sdd/README.md`: section-SDD layout and CLI workflow.
- `SPEC/bioinfo_native_section_sdd_plan.md`: accepted architecture plan.
- `tool_market/README.md`: inactive bundle market behavior.
- `SPEC/README.md`: index of design and implementation specs.
