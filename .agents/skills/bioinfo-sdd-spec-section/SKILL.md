# Bioinfo SDD Spec Section

Use this skill when creating or revising `spec.md` and `section.yml` for a
Bioinfo-skills analysis section.

## Workflow

1. Read `SPEC/bioinfo_native_section_sdd_plan.md`.
2. Inspect declared `pack_refs` under `sdd/packs/*/pack.yml` before choosing
   workflow and task refs.
3. Treat package refs, tool refs, wrappers, and adapters as installed bundle
   outputs selected from `tool_market/`, not as pack-wide defaults.
4. Load the relevant entry/domain skill tree and stage skills referenced by the
   pack task template.
5. Keep `section.yml` as the machine-readable source of truth.
6. In `spec.md`, state biological intent, required input state, produced output
   state, allowed claims, forbidden claims, and review gate status.
7. Run `bioinfo-sdd validate-section <section_id>` or
   `PYTHONPATH=src python -m bioinfo_sdd validate-section <section_id>`.
8. Stop at `spec_review` unless it is already approved.

Do not embed backend syntax in task or stage descriptions. Do not claim
normalization, feature selection, PCA, annotation, condition inference, or
biological interpretation unless the section explicitly implements and validates
that state transition.
