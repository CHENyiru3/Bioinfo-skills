# Quickstart: Spec Kit Usage Parity For Bioinfo Skills

Run commands from the repository root on Linux.

## 1. Confirm Active Feature

```bash
cat .specify/feature.json
```

Expected:

```json
{
  "feature_directory": "specs/001-speckit-usage-parity"
}
```

## 2. Confirm Codex Skill Load Path

Codex skills for this project live under `.agents/skills/`. The core workflow
keeps Spec Kit-style command names, while the skill bodies preserve Bioinfo SDD
rules.

## 3. Confirm Core Codex Skills

```bash
find .agents/skills -maxdepth 2 -name SKILL.md | sort
```

The output must include:

```text
.agents/skills/speckit-constitution/SKILL.md
.agents/skills/speckit-specify/SKILL.md
.agents/skills/speckit-clarify/SKILL.md
.agents/skills/speckit-checklist/SKILL.md
.agents/skills/speckit-plan/SKILL.md
.agents/skills/speckit-tasks/SKILL.md
.agents/skills/speckit-analyze/SKILL.md
.agents/skills/speckit-implement/SKILL.md
```

## 4. Confirm Bioinfo Helper Skill Frontmatter

```bash
for skill in \
  .agents/skills/bioinfo-sdd-spec-section/SKILL.md \
  .agents/skills/bioinfo-sdd-plan-section/SKILL.md \
  .agents/skills/bioinfo-sdd-tasks-section/SKILL.md \
  .agents/skills/bioinfo-sdd-evidence-section/SKILL.md
do
  sed -n '1,8p' "$skill"
done
```

Each file must begin with `---`, include `name:` and `description:`, and close
the frontmatter with `---`.

## 5. Validate Contract Tests

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest \
  tests.test_codex_skill_contract \
  tests.test_bioinfo_sdd_contract
```

Expected result: all tests pass.

## 6. Validate Existing Skill Tree

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m bioinfo_sdd run-check skill_tree
```

Expected result: `status` is `pass`.

## 7. User Workflow

Use the Spec Kit-style Codex sequence:

```text
$speckit-constitution
$speckit-specify
$speckit-clarify
$speckit-checklist
$speckit-plan
$speckit-tasks
$speckit-analyze
$speckit-implement
```

For Bioinfo analysis requests, the skills must route into section SDD:

```text
section.yml -> spec_review -> plan_review -> task_review -> evidence_acceptance
```

Concrete tools and `bioinfo_tool` context stay inactive in `tool_market/` until
installed into the current section's `installed_refs/`.
