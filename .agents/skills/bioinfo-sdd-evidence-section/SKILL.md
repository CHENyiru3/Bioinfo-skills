# Bioinfo SDD Evidence Section

Use this skill when creating or revising `evidence.md` for a Bioinfo-skills
analysis section.

## Workflow

1. Confirm `task_review` is approved.
2. Run the deterministic workflow:
   `PYTHONPATH=src python -m bioinfo_sdd run-workflow <section_id> --run-id <run_id>`.
3. Inspect `runs/<run_id>/state.json`, `log.jsonl`, and `checks/*.json`.
4. Record pass, fail, and skip results explicitly. Skips must name the missing
   package or unavailable capability.
5. Link evidence to actual `pack_refs`, `workflow_ref`, `task_refs`,
   active installed-ref revision, source bundle IDs, `package_refs`,
   `tool_refs`, wrapper, adapter, and check IDs.
6. Keep claims within `section.yml` `claims.allowed`; repeat forbidden claims as
   caveats when relevant.
7. Stop at `evidence_acceptance` unless it is already approved.

Evidence is not biological interpretation. It is a review record for whether
the declared section ran or validated under the declared constraints.
