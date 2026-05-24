# Bioinfo SDD Implementation Plan: Spec Kit Usage Parity For Bioinfo Skills

**Branch**: `001-speckit-usage-parity` | **Date**: 2026-05-24 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/001-speckit-usage-parity/spec.md`

**Note**: This plan intentionally targets Linux + Codex only. Upstream Spec Kit
is an architecture and usage reference, not a dependency to vendor wholesale.

## Summary

Align Bioinfo-skills with the upstream Spec Kit user journey for Codex users:
install/load skills under `.agents/skills`, invoke `$biokit-*` skills in the
same high-level sequence, persist the active feature path in
`.specify/feature.json`, and update `AGENTS.md` with the active plan. Preserve
Bioinfo SDD semantics: analysis work remains section-scoped, `section.yml`
remains canonical for sections, concrete tools stay inactive in `tool_market/`
until installed into section-local `installed_refs/`, and gates/evidence remain
mandatory for section workflows.

The immediate skill-loader warnings are fixed by adding YAML frontmatter to the
four Bioinfo section helper skills:
`bioinfo-sdd-spec-section`, `bioinfo-sdd-plan-section`,
`bioinfo-sdd-tasks-section`, and `bioinfo-sdd-evidence-section`.

## Technical Context

**Change Type**: infrastructure, skill guidance, templates, docs, validation
**Language/Version**: Python 3.10+, Bash, YAML, Markdown
**Primary Dependencies**: existing standard library code plus PyYAML; no new runtime dependency
**Domain/Ecosystem**: Bioinfo SDD / Codex; first biological domain remains scrna / scverse
**Section ID**: N/A for this feature
**Canonical Section State**: N/A for this feature; section requests still use `sdd/sections/<section_id>/section.yml`
**Pack/Workflow/Task Refs**: Existing `sdd/packs/scrna_scverse/pack.yml`, `sdd/workflows/section-sdd.yml`, and section task refs stay unchanged
**Installed Refs**: No new active tool bundle for this infrastructure feature; analysis sections must use section-local `installed_refs/`
**Bioinfo Tool Context**: `bioinfo_tool` choices remain inactive in `tool_market/` until installed into section-local `installed_refs/`
**Wrapper/Adapter**: No wrapper or adapter change in this planning phase
**Testing**: frontmatter presence checks, core skill presence checks, `.specify/feature.json` pointer check, `bioinfo-sdd run-check skill_tree`, targeted unit tests if discovery code changes
**Storage**: `.agents/skills/`, `.specify/feature.json`, `AGENTS.md`, `specs/001-speckit-usage-parity/`, README/runtime docs, tests
**Target Platform**: Linux local filesystem with Codex skills; Bash scripts only for BioKit helper scripts
**Constraints**: Do not add PowerShell support, multi-agent integration switching, remote workflow catalogs, remote marketplaces, or arbitrary executable plugin loading in this feature
**Scale/Scope**: One Codex integration path, nine core `$biokit-*` skills, four Bioinfo section helper skills, current scRNA/scverse exemplar as validation context

## Constitution Check

*GATE: Must pass before research/design. Re-check after design and before tasks.*

- **Section Scope**: PASS - This is explicitly non-analysis infrastructure. It does not authorize a biological state transition or expand an existing section.
- **Domain-Neutral Engine**: PASS - Planned core changes, if any, are feature discovery or validation helpers. Bioinformatics meaning remains in packs, skills, sections, refs, wrappers, adapters, and evidence.
- **Installed Ref Context**: PASS - No tool bundle is activated for this feature. The plan keeps `tool_market/` inactive and requires section-local `installed_refs/` for analysis requests.
- **Gates And Evidence**: PASS - Generated guidance must preserve `spec_review`, `plan_review`, `task_review`, and `evidence_acceptance` for analysis sections; this feature has a requirements checklist and deterministic validation instead of section evidence.
- **Wrapper/Adapter Boundary**: PASS - No executable analysis wrapper or adapter is changed. Guidance continues to require wrappers for analysis logic and adapters only for binding.
- **Deterministic Validation**: PASS - The warning fix and planned usability changes have focused validations: YAML frontmatter checks, skill discovery checks, active feature pointer checks, and `skill_tree`.

## Project Structure

### Documentation And Section Artifacts

```text
specs/001-speckit-usage-parity/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── linux-codex-skill-workflow.md
└── checklists/
    └── requirements.md
```

### Source Code And Runtime Assets

```text
.agents/skills/
├── biokit-*/SKILL.md                  # Spec Kit-style Codex skills
├── biokit-git-*/SKILL.md               # Git extension skills
└── bioinfo-sdd-*-section/SKILL.md      # Bioinfo section helper skills

.specify/
├── feature.json                        # Active feature pointer
├── scripts/bash/*.sh                   # Linux-only helper scripts for now
├── templates/*.md                      # Bioinfo SDD-flavored templates
└── memory/constitution.md              # Governing principles

src/bioinfo_sdd/                        # Domain-neutral Bioinfo SDD engine
sdd/                                    # Section templates, packs, workflows, sections
tool_market/                            # Inactive package/tool/bundle registry
README.md                               # User-facing quickstart and workflow guidance
AGENTS.md                               # Codex context pointer to current plan
tests/                                  # Deterministic validation
```

**Structure Decision**: This feature reads upstream architecture from
`/home/heybro/mnt/workspace/spec-kit` and edits only this repository. The
initial implementation scope is `.agents/skills/bioinfo-sdd-*-section/SKILL.md`,
`.specify/feature.json`, `AGENTS.md`, current feature design artifacts,
README/runtime guidance, and focused tests or checks. It does not modify
biological wrappers, adapters, pack manifests, or tool bundle semantics unless
tasks later reveal a validation-only helper is required.

## Implementation Plan

### Phase 0: Context And Research

- Review upstream Spec Kit architecture for the Codex skill integration,
  integration state, command processing, active feature lookup, hook handling,
  context marker updates, and resumable workflow model.
- Review Bioinfo-skills architecture for the section SDD engine, section
  workflow runner, tool market, installed refs, checks, templates, and current
  Codex skills.
- Resolve platform scope to Linux + Codex only.
- Record decisions in `research.md`.

### Phase 1: Design

- Treat upstream Codex integration as the ergonomic target while using the
  Bioinfo-owned namespace:
  `.agents/skills/biokit-<command>/SKILL.md`, `$ARGUMENTS`,
  `$biokit-*` invocation, dot-to-hyphen hook normalization, and `AGENTS.md`
  managed context markers.
- Treat `.specify/feature.json` as the active feature pointer for downstream
  commands before branch-name fallback.
- Keep Bioinfo SDD behavior in templates and skills: feature specs may be
  non-analysis infrastructure, but analysis requests must route through
  section contracts, gates, packs, installed refs, wrappers, adapters, checks,
  and evidence.
- Add YAML frontmatter to Bioinfo helper skills so Codex can load them.
- Define the user-visible Linux/Codex skill workflow contract in
  `contracts/linux-codex-skill-workflow.md`.
- Update `AGENTS.md` to reference this plan.

### Phase 2: Validation Strategy

- Validate frontmatter by checking that the four Bioinfo helper skills begin
  with `---` and have a closing `---`.
- Validate core skill presence under `.agents/skills/` for constitution,
  specify, clarify, checklist, plan, tasks, analyze, distill, and implement.
- Validate `.specify/feature.json` points to
  `specs/001-speckit-usage-parity`.
- Run `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m bioinfo_sdd run-check skill_tree`.
- If implementation changes discovery behavior, add or update focused tests
  under `tests/` before completing `$biokit-implement`.

## Complexity Tracking

No constitution violations or complexity exceptions are required.
