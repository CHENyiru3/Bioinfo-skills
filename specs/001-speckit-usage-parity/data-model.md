# Data Model: Spec Kit Usage Parity For Bioinfo Skills

## Skill Set

Represents the installed Codex skills a user can invoke.

Fields:
- `name`: Stable skill directory name, such as `speckit-plan` or
  `bioinfo-sdd-plan-section`.
- `path`: Repository-relative path to `SKILL.md`.
- `description`: YAML frontmatter summary used by the skill loader.
- `kind`: Core Spec Kit workflow skill, git extension skill, or Bioinfo section
  helper skill.
- `invocation`: User-facing Codex invocation where applicable, such as
  `$speckit-plan`.

Validation rules:
- `SKILL.md` must start with `---` and contain a closing `---`.
- `name` in frontmatter must match the skill directory name.
- Core workflow skills must exist for constitution, specify, clarify,
  checklist, plan, tasks, analyze, and implement.

## Feature Directory

Represents the active Spec Kit-style feature artifact directory.

Fields:
- `path`: Repository-relative path under `specs/`.
- `spec`: `spec.md`.
- `plan`: `plan.md`.
- `research`: `research.md`.
- `data_model`: `data-model.md`.
- `quickstart`: `quickstart.md`.
- `contracts`: Optional contract documents.
- `checklists`: Quality checklists.

Validation rules:
- The active path must match `.specify/feature.json`.
- `spec.md` and `plan.md` must contain no unresolved template placeholders.
- Downstream plan/tasks/analyze/implement skills must read this directory
  before branch-name fallback.

## Active Feature Pointer

Represents `.specify/feature.json`.

Fields:
- `feature_directory`: Repository-relative or absolute path to the active
  feature directory.

Validation rules:
- The JSON file must parse as an object.
- `feature_directory` must be non-empty.
- The referenced directory must exist.

State transitions:
- Created or replaced by `$speckit-specify`.
- Read by `$speckit-plan`, `$speckit-tasks`, `$speckit-analyze`, and
  `$speckit-implement`.

## Bioinfo SDD Section

Represents a bounded analysis section when the feature affects scientific
workflow execution.

Fields:
- `section_id`
- `section_yml`
- `gates`
- `pack_refs`
- `workflow_ref`
- `task_refs`
- `package_refs`
- `tool_refs`
- `check_refs`
- `wrapper`
- `adapter`
- `installed_refs`
- `runs`
- `evidence`

Validation rules:
- `section.yml` is canonical when present.
- Section workflows must pause at declared gates.
- Tool and package refs are active only through installed-ref revisions.

## Tool Market Bundle

Represents an inactive selectable implementation bundle.

Fields:
- `bundle_id`
- `task_refs`
- `stage_ids`
- `package_refs`
- `tool_refs`
- `wrapper`
- `adapter`
- `check_refs`

Validation rules:
- A bundle must resolve through `tool_market/market.yml`.
- A bundle becomes active only after installation into
  `sdd/sections/<section_id>/installed_refs/revisions/<revision_id>/`.
- Replacement preserves historical revisions and triggers review of state,
  parameters, claims, checks, wrapper, adapter, and evidence expectations.
