# Contract: Linux Codex Skill Workflow

## Scope

This contract defines the user-visible workflow for Bioinfo-skills when used
on Linux with Codex skills. It does not define behavior for other agents,
PowerShell, remote workflow catalogs, or remote marketplaces.

## Skill Invocation Contract

Required core skills:

- `$biokit-constitution`
- `$biokit-specify`
- `$biokit-clarify`
- `$biokit-checklist`
- `$biokit-plan`
- `$biokit-tasks`
- `$biokit-analyze`
- `$biokit-distill`
- `$biokit-implement`

Each required skill must exist at:

```text
.agents/skills/<skill-name>/SKILL.md
```

Each `SKILL.md` must contain YAML frontmatter delimited by `---` and must
describe Bioinfo SDD behavior when it differs from generic Spec Kit behavior.

## Feature Discovery Contract

`$biokit-specify` must persist the active feature directory in:

```json
{
  "feature_directory": "specs/<feature-directory>"
}
```

Downstream skills must resolve the active feature in this order:

1. Explicit `SPECIFY_FEATURE_DIRECTORY`, when provided.
2. `.specify/feature.json` `feature_directory`.
3. Branch-name-based fallback.

## Continuity Distillation Contract

`$biokit-distill` must create or refresh:

```text
specs/<active-feature>/current-understanding.md
```

The report must summarize current workflow state, active section or N/A,
installed refs, packages/tools actually in use, referenced market bundles,
wrappers, adapters, checks, evidence status, pending tasks, risks, and exact
next actions. It must not mutate section state, gates, installed refs, task
state, wrappers, adapters, checks, or evidence.

## Agent Context Contract

`AGENTS.md` must retain the managed marker block:

```markdown
<!-- SPECKIT START -->
...
<!-- SPECKIT END -->
```

After planning, the managed block must point to the current plan path:

```text
specs/001-speckit-usage-parity/plan.md
```

## Bioinfo SDD Preservation Contract

Spec Kit-style skills must preserve these Bioinfo SDD constraints:

- Analysis requests use `section.yml` as canonical machine-readable state.
- Analysis workflows pause at `spec_review`, `plan_review`, `task_review`, and
  `evidence_acceptance`.
- Concrete package and tool refs in `tool_market/` are inactive until selected
  bundles are installed into section-local `installed_refs/`.
- `bioinfo_tool` context means installed Bioinfo package/tool refs from the
  active section-local installed-ref revision, not the full inactive market.
- Wrappers contain bounded analysis logic; adapters bind wrappers.
- Evidence cannot exceed `claims.allowed`.

## Validation Contract

Planning or implementation is valid only when:

- Core workflow skill files exist.
- Bioinfo helper skill files have YAML frontmatter.
- `.specify/feature.json` points to an existing feature directory.
- `bioinfo-sdd run-check skill_tree` passes.
- Any code change that alters discovery, templates, checks, wrappers, adapters,
  or workflow state has a focused deterministic test.
