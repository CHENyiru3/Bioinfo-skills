---
description: "Bioinfo SDD task list template"
---

# Tasks: [FEATURE OR SECTION NAME]

**Input**: Design documents from `/specs/[###-feature-name]/` and section
artifacts under `sdd/sections/[section_id]/` when applicable.

**Prerequisites**: plan.md, spec.md, `.specify/memory/constitution.md`, and any
relevant `section.yml`, `gates.yml`, pack manifests, installed refs, wrappers,
adapters, contracts, and tool refs.

**Validation**: Include deterministic tests or `bioinfo-sdd` checks for changed
schemas, packs, section contracts, wrappers, adapters, CLI behavior, and
workflow state. If a deterministic test is impossible, add an explicit review
task explaining why.

**Organization**: Tasks are grouped by SDD phase so each review gate can be
validated independently.

## Format: `[ID] [P?] [Phase] Description`

- **[P]**: Can run in parallel because it touches different files and has no
  dependency on another open task.
- **[Phase]**: Context, Spec, Plan, Implement, Validate, Evidence, or Review.
- Include exact file paths and command names.
- Keep each task bounded to the approved section or infrastructure change.

## Phase 1: Context And Scope

**Purpose**: Load the governing files and confirm the bounded work unit.

- [ ] T001 [Context] Read `.specify/memory/constitution.md`, `README.md`, and
  relevant SPEC docs.
- [ ] T002 [Context] Identify the affected section, pack, tool market, wrapper,
  adapter, contracts, checks, or CLI files.
- [ ] T003 [Context] Record out-of-scope biological claims, preprocessing,
  downstream interpretation, and overwrite behavior.

**Checkpoint**: Scope is explicit and does not exceed the approved section or
infrastructure change.

---

## Phase 2: Section Contract And Spec

**Purpose**: Make the machine-readable section contract and review spec complete.

- [ ] T004 [Spec] Update `sdd/sections/[section_id]/section.yml` with input
  state, output state, refs, expected artifacts, claims, and gates.
- [ ] T005 [Spec] Update `sdd/sections/[section_id]/spec.md` with biological
  intent, allowed claims, forbidden claims, and review conditions.
- [ ] T006 [Spec] Run `PYTHONPATH=src python -m bioinfo_sdd validate-section [section_id]`.
- [ ] T007 [Review] Obtain or document `spec_review` status in gates.

**Checkpoint**: `spec_review` is ready for approval before planning continues.

---

## Phase 3: Pack, Tool, Wrapper, And Adapter Plan

**Purpose**: Resolve domain meaning separately from concrete execution choices.

- [ ] T008 [Plan] Resolve `pack_refs`, `workflow_ref`, and `task_refs` through
  `sdd/packs/*/pack.yml`.
- [ ] T009 [Plan] Inspect only relevant stage skills, contracts, and task
  templates.
- [ ] T010 [Plan] List candidate bundles with
  `PYTHONPATH=src python -m bioinfo_sdd market-list --task-ref [task_ref]`.
- [ ] T011 [Plan] Install or replace the selected bundle into
  section-local `installed_refs/`.
- [ ] T012 [Plan] Update plan artifacts with wrapper, adapter, high-impact
  parameters, keys written, overwrite policy, checks, and caveats.
- [ ] T013 [Review] Obtain or document `plan_review` status in gates.

**Checkpoint**: `plan_review` is ready for approval before executable work.

---

## Phase 4: Implementation

**Purpose**: Make scoped code or artifact changes after the approved plan.

- [ ] T014 [Implement] Update wrapper, adapter, pack, market, schema, contract,
  CLI, or documentation files named in the plan.
- [ ] T015 [Implement] Keep biological analysis logic inside wrappers and keep
  adapter files as bindings only.
- [ ] T016 [Implement] Preserve historical installed-ref revisions and avoid
  loading the inactive full market as active context.
- [ ] T017 [Review] Obtain or document `task_review` status in gates.

**Checkpoint**: Implementation remains bounded and task review is complete.

---

## Phase 5: Validation And Evidence

**Purpose**: Prove the section or infrastructure change with deterministic
checks and bounded evidence.

- [ ] T018 [Validate] Run relevant unit tests under `tests/`.
- [ ] T019 [Validate] Run relevant `bioinfo-sdd run-check` commands.
- [ ] T020 [Validate] Run wrapper tests, adapter dry-runs, or workflow runs when
  runtime dependencies are available.
- [ ] T021 [Evidence] Record pass, fail, and skip outcomes with reasons.
- [ ] T022 [Evidence] Update `sdd/sections/[section_id]/evidence.md` or the
  relevant report with refs, run state, logs, checks, artifacts, caveats, and
  bounded claims.
- [ ] T023 [Review] Obtain or document `evidence_acceptance` status.

**Checkpoint**: Evidence is reviewable and does not exceed allowed claims.

---

## Dependencies & Execution Order

- Context tasks block all later work.
- Spec tasks block planning until `spec_review` is approved or explicitly left
  pending for human review.
- Plan tasks block implementation until `plan_review` is approved.
- Implementation tasks block evidence until `task_review` is approved.
- Evidence acceptance is the final review gate.
- Tasks marked `[P]` may run in parallel only when they touch distinct files and
  do not depend on another unfinished task.

## Notes

- Do not add upstream preprocessing or downstream interpretation tasks unless
  the section contract is revised first.
- Do not treat Snakemake, Nextflow, bash, notebooks, or any backend adapter as
  the source of biological task meaning.
- Do not accept skipped optional runtime checks as success unless the skip
  reason is recorded.
- Commit after a completed gate or a coherent artifact group when Git hooks are
  enabled.
