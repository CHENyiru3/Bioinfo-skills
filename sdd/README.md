# Bioinfo Section SDD

This directory stores durable section-level Spec-Driven Development artifacts.
A section is a bounded biological data-state transition with explicit input
state, output state, pack refs, task refs, package/tool refs, wrappers, adapter
bindings, review gates, and evidence.

`section.yml` is the canonical machine-readable artifact. The Markdown files
are review artifacts that explain the scientific intent, implementation plan,
tasks, and evidence without expanding the claims beyond the approved section.

## Layout

- `templates/`: reusable artifact templates for new sections.
- `workflows/section-sdd.yml`: deterministic local lifecycle for validation,
  review gates, checks, and evidence recording.
- `packs/`: local capability-pack manifests that resolve workflow, task,
  stage skill, and check IDs.
- `sections/<section_id>/`: durable state for one analysis section, including
  section-local installed tool/package refs.

Concrete tool/package refs are selected from `tool_market/` and copied into
`sections/<section_id>/installed_refs/revisions/<revision_id>/`.

## CLI

Use `bioinfo-sdd` after installing this repository, or run it with
`PYTHONPATH=src python -m bioinfo_sdd` from the repository root.

Common commands:

```bash
bioinfo-sdd create-section scrna_example_m1
bioinfo-sdd validate-section scrna_example_m1
bioinfo-sdd market-list --task-ref scrna.scverse.task.graph_clustering.v0
bioinfo-sdd install-tool-bundle scrna_example_m1 scrna.scverse.bundle.scanpy_graph_clustering.v0
bioinfo-sdd installed-refs scrna_example_m1
bioinfo-sdd run-workflow scrna_example_m1 --run-id local-review
bioinfo-sdd set-gate scrna_example_m1 spec_review approved --reason "reviewed"
bioinfo-sdd run-check section_catalog_links --section scrna_example_m1
```
