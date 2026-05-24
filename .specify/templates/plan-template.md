# Bioinfo SDD Implementation Plan: [FEATURE OR SECTION]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature or section specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit-plan` workflow. It must
align with `.specify/memory/constitution.md` and the Bioinfo-skills SDD model.

## Summary

[Extract the bounded section or engine capability from the spec. State the
technical approach without expanding biological claims.]

## Technical Context

**Change Type**: [analysis section/core engine/capability pack/tool market/wrapper/adapter/docs]
**Language/Version**: [e.g., Python 3.10+, R, Snakemake, YAML, Markdown or N/A]
**Primary Dependencies**: [e.g., PyYAML, Scanpy, AnnData, Snakemake or N/A]
**Domain/Ecosystem**: [e.g., scrna/scverse or N/A]
**Section ID**: [section_id or N/A]
**Canonical Section State**: [path to section.yml or N/A]
**Pack/Workflow/Task Refs**: [pack_refs, workflow_ref, task_refs or N/A]
**Installed Refs**: [active installed-ref revision or planned bundle selection]
**Bioinfo Tool Context**: [`bioinfo_tool` refs active through installed_refs or N/A]
**Wrapper/Adapter**: [paths or pending]
**Testing**: [unit tests, wrapper tests, workflow dry-run, bioinfo-sdd checks]
**Storage**: [repository files, section runs, installed_refs, reports, artifacts]
**Target Platform**: [local filesystem, Linux, container/runtime assumptions]
**Constraints**: [state preconditions, overwrite policy, runtime package limits]
**Scale/Scope**: [fixtures, exemplar section, expected data size, or N/A]

## Constitution Check

*GATE: Must pass before research/design. Re-check after design and before tasks.*

- **Section Scope**: PASS/FAIL - The plan names one bounded biological or
  data-state transition, or states why the change is non-analysis infrastructure.
- **Domain-Neutral Engine**: PASS/FAIL - Core code remains free of hard-coded
  biological task meaning except named deterministic checks or explicit pack
  declarations.
- **Installed Ref Context**: PASS/FAIL - Active package/tool context comes from
  section-local `installed_refs/`, not the full inactive `tool_market/`.
- **Gates And Evidence**: PASS/FAIL - Required review gates, run state, check
  outputs, evidence, and bounded claims are planned.
- **Wrapper/Adapter Boundary**: PASS/FAIL - Executable work lives in approved
  wrappers; adapters bind wrappers without hidden analysis logic.
- **Deterministic Validation**: PASS/FAIL - Changed schemas, checks, wrappers,
  adapters, CLI behavior, or section contracts have focused tests or an
  explicit review note.

## Project Structure

### Documentation And Section Artifacts

```text
specs/[###-feature]/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
└── tasks.md

sdd/sections/[section_id]/
├── section.yml
├── spec.md
├── plan.md
├── tasks.md
├── evidence.md
├── gates.yml
├── installed_refs/
└── runs/
```

### Source Code And Runtime Assets

```text
src/bioinfo_sdd/          # domain-neutral SDD engine and CLI
sdd/packs/                # capability-pack manifests
tool_market/              # inactive package/tool/bundle registry
skills/                   # routing and stage guidance
wrappers/                 # bounded executable units
workflow/                 # execution-adapter bindings
contracts/                # state and statistical contracts
tests/                    # deterministic unit, contract, wrapper, and workflow checks
```

**Structure Decision**: [Document the exact files this change will read or edit.
Delete paths that are not involved.]

## Implementation Plan

### Phase 0: Context And Research

- Load `.specify/memory/constitution.md`, `README.md`, relevant SPEC docs, and
  current section artifacts.
- Resolve relevant packs, task templates, stage skills, installed refs, and
  contracts before selecting concrete tools.
- Document unresolved scientific, state, runtime, or review questions.

### Phase 1: Design

- Update section contract, manifest schema, pack binding, wrapper design,
  adapter binding, or CLI behavior as needed.
- Name high-impact parameters, matrix/layer policy, keys written, overwrite
  policy, artifacts, and forbidden claims.
- Re-run the Constitution Check and record any justified violations below.

### Phase 2: Validation Strategy

- Name deterministic checks: `validate-section`, `run-check`, unit tests,
  wrapper tests, workflow dry-runs, runtime report checks, or manual gate review.
- Define expected pass/fail/skip behavior and evidence artifacts.

## Complexity Tracking

> Fill only if a Constitution Check item fails and an approved exception is required.

| Violation | Affected Principle | Why Needed | Simpler Alternative Rejected Because | Approval |
|-----------|--------------------|------------|-------------------------------------|----------|
| [example] | [principle] | [reason] | [reason] | [pending/approved] |
