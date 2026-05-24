# Bioinfo SDD Tasks Section

Use this skill when creating or revising `tasks.md` for a Bioinfo-skills
analysis section.

## Workflow

1. Confirm `plan_review` is approved.
2. Convert the approved section spec and plan into ordered implementation and
   validation tasks.
3. Include pack resolution, section validation, wrapper checks, adapter checks,
   dependency-aware execution tests, evidence recording, and gate updates.
4. Keep tasks bounded to the declared section. Do not add upstream preprocessing
   or downstream interpretation tasks unless the section contract is revised.
5. Run `PYTHONPATH=src python -m bioinfo_sdd validate-section <section_id>`.
6. Stop at `task_review` unless it is already approved.

Task files are review artifacts. The executable source of truth remains
`section.yml`, the pack manifest, wrappers, adapters, and checks.
