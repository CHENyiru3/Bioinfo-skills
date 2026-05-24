---
name: "bioinfo-sdd-plan-section"
description: "Create or revise Bioinfo-skills analysis section implementation plans."
compatibility: "Bioinfo-skills section SDD; Linux/Codex"
metadata:
  author: "bioinfo-skills"
  source: "SPEC/bioinfo_native_section_sdd_plan.md"
---

# Bioinfo SDD Plan Section

Use this skill when creating or revising `plan.md` for a Bioinfo-skills
analysis section.

## Workflow

1. Confirm `spec_review` is approved.
2. Read the section's `pack_refs`, `workflow_ref`, `task_refs`,
   `package_refs`, `tool_refs`, `wrapper`, `adapter`, and `check_refs`.
3. Resolve those IDs through `sdd/packs/*/pack.yml`.
4. Use `bioinfo-sdd market-list --task-ref <task_id>` and
   `bioinfo-sdd market-show <bundle_id>` before selecting concrete tools.
5. Install the chosen bundle with `bioinfo-sdd install-tool-bundle <section_id>
   <bundle_id>` or replace it with `bioinfo-sdd replace-tool-bundle`.
6. Treat `bioinfo_tool` as the active Bioinfo package/tool context only after
   the selected `tool_market/` bundle has been installed into section-local
   `installed_refs/`.
7. Inspect only the relevant stage skills, installed package refs, installed
   tool refs, wrapper, and adapter files from the active installed-ref revision.
8. Do not load the full inactive `tool_market/` as active planning context.
9. Document why the selected wrapper and adapter satisfy the declared input and
   output state without hidden preprocessing.
10. List high-impact parameters and keys written.
11. Run pack, market, installed-ref, and section checks:
   `PYTHONPATH=src python -m bioinfo_sdd run-check market_manifest`,
   `PYTHONPATH=src python -m bioinfo_sdd run-check installed_refs --section <section_id>`, and
   `PYTHONPATH=src python -m bioinfo_sdd run-check section_catalog_links --section <section_id>`.
12. Stop at `plan_review` unless it is already approved.

The plan should be replaceable: make it clear which choices come from the task
template and which are section-local overrides.
