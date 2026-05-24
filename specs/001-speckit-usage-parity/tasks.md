# Tasks: Spec Kit Usage Parity For Bioinfo Skills

**Input**: Design artifacts from `specs/001-speckit-usage-parity/`
**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/linux-codex-skill-workflow.md`, `quickstart.md`

**Tests**: Include focused contract tests because the feature is a workflow/tooling contract and regressions are easiest to catch with deterministic repository checks.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel because it touches different files and has no dependency on another in-flight task.
- **[Story]**: User story label, such as `[US1]`, required for story-scoped tasks.
- Every task names the exact file or directory it changes or validates.

## Phase 1: Setup And Orientation

**Purpose**: Confirm the active feature context and source references before changing repository behavior.

- [X] T001 Read `.specify/memory/constitution.md`, `specs/001-speckit-usage-parity/spec.md`, `specs/001-speckit-usage-parity/plan.md`, `specs/001-speckit-usage-parity/research.md`, `specs/001-speckit-usage-parity/data-model.md`, `specs/001-speckit-usage-parity/contracts/linux-codex-skill-workflow.md`, and `specs/001-speckit-usage-parity/quickstart.md` to confirm acceptance criteria.
- [X] T002 Inspect `/home/heybro/mnt/workspace/spec-kit/src/specify_cli/integrations/codex/__init__.py` and `.agents/skills/` to confirm current Spec Kit Codex skill layout and local Bioinfo skill layout.
- [X] T003 Verify `.specify/feature.json` points to `specs/001-speckit-usage-parity` and that `AGENTS.md` references `specs/001-speckit-usage-parity/plan.md`.

---

## Phase 2: Foundational Contract Tests

**Purpose**: Add or tighten repository-level checks that protect the workflow contract before implementation changes.

- [X] T004 Create or extend `tests/test_codex_skill_contract.py` to assert all required core skills exist under `.agents/skills/biokit-*/SKILL.md` with YAML frontmatter.
- [X] T005 Extend `tests/test_codex_skill_contract.py` to assert `.specify/feature.json` resolves to an existing feature directory containing `spec.md`, `plan.md`, and `tasks.md`.
- [X] T006 Extend `tests/test_codex_skill_contract.py` to assert `AGENTS.md` contains the Spec Kit marker block and references the active plan path `specs/001-speckit-usage-parity/plan.md`.
- [X] T007 Create or extend `tests/test_bioinfo_sdd_contract.py` to assert Bioinfo SDD templates and plans preserve `section.yml`, `installed_refs`, `tool_market`, `bioinfo_tool`, and evidence/report gate terminology.
- [X] T008 Extend `tests/test_bioinfo_sdd_contract.py` to assert `.agents/skills/bioinfo-sdd-spec-section/SKILL.md`, `.agents/skills/bioinfo-sdd-plan-section/SKILL.md`, `.agents/skills/bioinfo-sdd-tasks-section/SKILL.md`, and `.agents/skills/bioinfo-sdd-evidence-section/SKILL.md` contain valid YAML frontmatter.

**Checkpoint**: Contract tests are present and expected to fail only where implementation is incomplete.

---

## Phase 3: User Story 1 - Use Spec Kit-style skills for Bioinfo SDD (Priority: P1)

**Goal**: A Codex user can invoke `$biokit-constitution`, `$biokit-specify`, `$biokit-plan`, `$biokit-tasks`, `$biokit-distill`, and `$biokit-implement` from this repository with Spec Kit-like ergonomics.

**Independent Test**: From the repository root, inspect `.agents/skills/biokit-*/SKILL.md`, `.specify/feature.json`, and `AGENTS.md`; each command skill should have valid frontmatter, discover the active feature without branch-name dependence, and point Codex to the active plan.

- [X] T009 [US1] Update `.agents/skills/biokit-constitution/SKILL.md` to preserve Spec Kit command ergonomics while generating the Bioinfo SDD constitution.
- [X] T010 [US1] Update `.agents/skills/biokit-specify/SKILL.md` to preserve Spec Kit command ergonomics while creating Bioinfo SDD feature specifications and contracts.
- [X] T011 [US1] Update `.agents/skills/biokit-plan/SKILL.md` to preserve Spec Kit command ergonomics while producing Bioinfo SDD implementation plans and section design artifacts.
- [X] T012 [US1] Update `.agents/skills/biokit-tasks/SKILL.md` to preserve Spec Kit command ergonomics while producing dependency-ordered Bioinfo SDD task lists.
- [X] T013 [US1] Update `.agents/skills/biokit-implement/SKILL.md` to preserve Spec Kit command ergonomics while executing `tasks.md` through Codex.
- [X] T014 [US1] Update `.specify/scripts/bash/common.sh` and `.specify/scripts/bash/setup-plan.sh` so active feature discovery uses `.specify/feature.json` before any git branch fallback.
- [X] T015 [US1] Update `.specify/templates/spec-template.md`, `.specify/templates/plan-template.md`, and `.specify/templates/tasks-template.md` so generated artifacts keep Spec Kit file names while using Bioinfo SDD section language.

**Checkpoint**: `$biokit-*` skills are usable as Codex skills and resolve the same active feature directory.

---

## Phase 4: User Story 2 - Preserve Bioinfo workflow and marketer contract (Priority: P1)

**Goal**: Spec Kit-style usage must not dilute the Bioinfo SDD workflow, section contract, or tool-market installation references.

**Independent Test**: Run `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m bioinfo_sdd run-check skill_tree` from the repository root and inspect the generated plan/spec artifacts for `installed_refs`, `tool_market`, `section.yml`, and evidence gate language.

- [X] T016 [US2] Update `.agents/skills/bioinfo-sdd-spec-section/SKILL.md` so its YAML frontmatter and workflow explicitly maintain `section.yml` contract requirements.
- [X] T017 [US2] Update `.agents/skills/bioinfo-sdd-plan-section/SKILL.md` so its YAML frontmatter and workflow explicitly maintain `installed_refs`, `tool_market`, and `bioinfo_tool` requirements.
- [X] T018 [US2] Update `.agents/skills/bioinfo-sdd-tasks-section/SKILL.md` so its YAML frontmatter and workflow explicitly maintain dependency-ordered Bioinfo section task generation.
- [X] T019 [US2] Update `.agents/skills/bioinfo-sdd-evidence-section/SKILL.md` so its YAML frontmatter and workflow explicitly maintain evidence/report gate requirements.
- [X] T020 [US2] Update `.specify/memory/constitution.md` to keep BioKit command parity subordinate to Bioinfo SDD reproducibility, tool-market, and evidence principles.
- [X] T021 [US2] Update `specs/001-speckit-usage-parity/contracts/linux-codex-skill-workflow.md` if implementation details change the Linux/Codex contract for skills, active feature discovery, or Bioinfo SDD validation.

**Checkpoint**: Existing Bioinfo helper skills remain loadable and the tool-market contract is still explicitly enforced.

---

## Phase 5: User Story 3 - Document the user journey clearly (Priority: P2)

**Goal**: A Linux/Codex user can understand how to load the skills and run the Spec Kit-style Bioinfo SDD workflow without reading implementation internals.

**Independent Test**: Follow `specs/001-speckit-usage-parity/quickstart.md` from a clean shell in the repository root and confirm every documented command maps to files in this repository.

- [X] T022 [P] [US3] Update `README.md` with the Linux/Codex skill loading path, `$biokit-*` command sequence, and Bioinfo SDD contract expectations.
- [X] T023 [P] [US3] Update `skills/README.md` with the relationship between public Bioinfo skills, `.agents/skills/`, and the Spec Kit-style Codex command skills.
- [X] T024 [US3] Update `specs/001-speckit-usage-parity/quickstart.md` so its verification commands match the final skill names, file paths, and validation checks.

**Checkpoint**: The documented user journey is executable without relying on unstated project knowledge.

---

## Phase 6: Validation And Polish

**Purpose**: Prove the feature works end to end and leave the worktree ready for review.

- [X] T025 Run `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests` from `/home/heybro/mnt/workspace/bioinfo_skills/Bioinfo-skills` and fix failures in `tests/` or implementation files.
- [X] T026 Run `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m bioinfo_sdd run-check skill_tree` from `/home/heybro/mnt/workspace/bioinfo_skills/Bioinfo-skills` and fix any skill metadata or contract failures in `.agents/skills/`.
- [X] T027 Run `rg -n "NEEDS [C]LARIFICATION:|TO[D]O\\(|<[A-Z_][A-Z0-9_ -]*>" specs/001-speckit-usage-parity .specify/templates .agents/skills --glob '!.agents/skills/biokit-*/SKILL.md'` from `/home/heybro/mnt/workspace/bioinfo_skills/Bioinfo-skills` and resolve accidental unresolved placeholders in `specs/001-speckit-usage-parity/`, `.specify/templates/`, and `.agents/skills/`.
- [X] T028 Run `git status --short` from `/home/heybro/mnt/workspace/bioinfo_skills/Bioinfo-skills` and summarize changed files for review.

---

## Phase 7: BioKit Namespace Implementation

**Purpose**: Apply the clarified non-conflicting command namespace to actual loadable skills, extension commands, and documentation.

- [X] T029 Rename core workflow skill directories from `.agents/skills/speckit-*` to `.agents/skills/biokit-*` and update each `SKILL.md` frontmatter name.
- [X] T030 Rename git helper skill directories from `.agents/skills/speckit-git-*` to `.agents/skills/biokit-git-*` and update hook references to `/biokit-git-*`.
- [X] T031 Rename extension command files from `.specify/extensions/git/commands/speckit.git.*.md` to `.specify/extensions/git/commands/biokit.git.*.md` and update workflow command identifiers to `biokit.*`.
- [X] T032 Update README, quickstart, contracts, research, data model, plan, templates, and integration manifests so user-facing canonical commands are `$biokit-*`.
- [X] T033 Re-run unit tests and Bioinfo SDD skill-tree validation after the namespace rename.
- [X] T034 Re-run stale `speckit-*` reference scan and `git diff --check` after the namespace rename.

---

## Phase 8: BioKit Distill Continuity Skill

**Purpose**: Add a resume-oriented command that distills current feature, section, package/tool, and workflow state into one Markdown continuity artifact.

- [X] T035 Add `.agents/skills/biokit-distill/SKILL.md` with frontmatter, Bioinfo SDD contract, artifact-loading rules, package/tool distillation rules, and `current-understanding.md` output structure.
- [X] T036 Wire `$biokit-distill` into README, skill guidance, feature contracts, data model, quickstart, workflow metadata, and git hook configuration.
- [X] T037 Extend `tests/test_codex_skill_contract.py` to assert `biokit-distill` is installed and preserves the continuity report contract.
- [X] T038 Re-run unit tests, skill-tree validation, manifest hash validation, stale reference scan, and `git diff --check` after adding `biokit-distill`.

---

## Dependencies And Execution Order

1. Phase 1 must complete before writing tests or implementation changes.
2. Phase 2 must complete before story implementation so contract expectations are explicit.
3. User Story 1 and User Story 2 are both P1; complete both before relying on the workflow.
4. User Story 3 depends on final command names and paths from User Story 1 and User Story 2.
5. Phase 6 runs after all selected user stories are complete.
6. Phase 7 records the clarified `biokit-*` namespace implementation and runs
   after the command namespace decision is finalized.
7. Phase 8 adds the optional resume/continuity distillation command after the
   namespace is stable.

## Parallel Opportunities

- T022 and T023 can run in parallel because they update different documentation files.
- After T004-T008 are complete, T009-T013 can be split across different `.agents/skills/biokit-*` files.
- T016-T019 can be split across the four `.agents/skills/bioinfo-sdd-*-section/SKILL.md` files.
- T020 and T021 can run in parallel with documentation work if no implementation contract details are changing.

## Implementation Strategy

### MVP First

Complete Phase 1, Phase 2, User Story 1, User Story 2, and Phase 6 tasks T025-T026. This delivers the required Linux/Codex Spec Kit-style skill workflow while preserving Bioinfo SDD constraints.

### Incremental Delivery

1. Deliver User Story 1 to make the `$biokit-*` commands usable.
2. Deliver User Story 2 to lock the Bioinfo workflow and tool-market contract.
3. Deliver User Story 3 to make the workflow easy for future users to adopt.
4. Run Phase 6 validation before commit or review.

## Summary

- Total tasks: 38
- User Story 1: 7 tasks
- User Story 2: 6 tasks
- User Story 3: 3 tasks
- Setup/foundational/validation/namespace/distill: 22 tasks
- Parallel tasks marked `[P]`: 2
- MVP scope: Phases 1-4 plus T025-T026
