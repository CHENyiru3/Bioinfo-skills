<!--
Sync Impact Report
Version change: template -> 1.0.0
Modified principles:
- Template principle 1 -> I. Section-Scoped Biological State Transitions
- Template principle 2 -> II. Domain-Neutral Engine, Pack-Owned Meaning
- Template principle 3 -> III. Installed References Are Active Context
- Template principle 4 -> IV. Gates, Evidence, And Bounded Claims
- Template principle 5 -> V. Wrapper Boundaries And Deterministic Validation
Added sections:
- Bioinformatics SDD Constraints
- Section Development Workflow
Removed sections:
- Generic placeholder section guidance
Templates requiring updates:
- ✅ updated: .specify/templates/plan-template.md
- ✅ updated: .specify/templates/spec-template.md
- ✅ updated: .specify/templates/tasks-template.md
- ✅ updated: .specify/templates/checklist-template.md
- ✅ updated: .specify/extensions/git/commands/biokit.git.commit.md
- ✅ updated: .specify/extensions/git/commands/biokit.git.initialize.md
- ✅ updated: .specify/extensions/git/commands/biokit.git.feature.md
- ✅ updated: .specify/extensions/git/commands/biokit.git.remote.md
- ✅ checked: .specify/extensions/git/commands/biokit.git.validate.md
- ✅ checked: sdd/templates/spec.md, sdd/templates/plan.md, sdd/templates/tasks.md,
  sdd/templates/evidence.md
Follow-up TODOs: None
-->
# Bioinfo-skills SDD Constitution

## Core Principles

### I. Section-Scoped Biological State Transitions
Every approved unit of work MUST be an analysis section representing exactly
one bounded biological or data-state transition. Each section MUST declare its
biological intent, domain, ecosystem, input state, output state, expected
artifacts, allowed claims, forbidden claims, and review gates before executable
work proceeds. Unknown input state MUST be resolved by a state-inspection
section before downstream analysis sections are planned. A section MUST NOT
hide upstream preprocessing, downstream annotation, condition-level inference,
or final biological interpretation inside a narrower task.

Rationale: Bioinformatics workflows are scientifically reviewable only when
state changes and claim boundaries are explicit at section granularity.

### II. Domain-Neutral Engine, Pack-Owned Meaning
The `src/bioinfo_sdd` engine MUST own repository-local file state, template
rendering, manifest resolution, validation, gates, deterministic checks,
installed-ref management, workflow run state, and CLI dispatch. Domain meaning
MUST live in capability packs, section artifacts, skills, package refs, tool
refs, wrappers, adapters, contracts, and evidence. Core lifecycle code MUST NOT
hard-code biological task semantics, ecosystem APIs, or execution-backend
syntax as the meaning of a task. Domain-specific checks are allowed only as
named deterministic checks that are declared by packs or section contracts.

Rationale: Replaceability requires the same SDD engine to support scverse,
Seurat, and later bioinformatics domains without rewriting core workflow
semantics.

### III. Installed References Are Active Context
Package and tool references in `tool_market/` are inactive source material
until a selected bundle is copied into a section-local `installed_refs/`
revision. Agents and review workflows MUST use the active installed-ref
revision for the current section, not the full inactive market, when selecting
or explaining tools. Replacing, adding, or uninstalling a bundle MUST create or
record section-local installed-ref state and MUST trigger review of input
state, output state, parameters, wrapper, adapter, claims, checks, and evidence
expectations. Historical installed-ref revisions MUST remain available for
reproducibility.

Rationale: Active context must be small, auditable, and reproducible while the
project keeps a broader replaceable tool market.

### IV. Gates, Evidence, And Bounded Claims
`section.yml` MUST remain the canonical machine-readable source of truth for a
section. Markdown specs, plans, tasks, and evidence files are review artifacts
that explain and justify that state without expanding it. Workflows MUST pause
at `spec_review`, `plan_review`, `task_review`, and `evidence_acceptance`
unless the relevant gate is approved. Evidence MUST record the actual pack
refs, workflow ref, task refs, installed-ref revision, package refs, tool refs,
wrapper, adapter, check IDs, check outcomes, skipped capabilities, outputs,
caveats, and accepted claims. Evidence MUST NOT claim results outside
`claims.allowed`.

Rationale: Scientific acceptance depends on visible human review gates and
durable evidence tied to the exact files and refs used.

### V. Wrapper Boundaries And Deterministic Validation
Executable wrappers MUST perform only the approved bounded operation for the
section and MUST declare or preserve matrix, layer, key-writing, overwrite, and
artifact behavior. Execution adapters such as Snakemake, Nextflow, bash,
Python, Rscript, or notebooks MUST bind and run wrappers; they MUST NOT contain
hidden biological analysis logic. Changes to schemas, packs, section
contracts, checks, wrappers, adapters, CLI behavior, or workflow state MUST
include focused deterministic tests or an explicit review note explaining why a
deterministic test is not possible. Missing optional runtime packages MUST
produce skipped checks with reasons, not false success.

Rationale: Backend separation and deterministic validation make agent-created
workflow pieces inspectable before they affect scientific conclusions.

## Bioinformatics SDD Constraints

- The first supported domain is scRNA/scverse, centered on explicit AnnData
  state transitions; the constitution applies equally to later domains and
  ecosystems.
- Capability packs under `sdd/packs/` MUST be file-backed, versioned, and
  reviewable. They MAY declare workflows, task templates, stage skills,
  catalogs, checks, wrappers, adapters, and guidance.
- The repository-local `tool_market/` MUST remain a selectable registry, not
  active section context. Selected bundles MUST be installed into
  `sdd/sections/<section_id>/installed_refs/`.
- `bioinfo_tool` context is active only when derived from the section-local
  installed-ref revision; the inactive market is never active execution context.
- Biological task refs MUST describe scientific or data-state operations.
  Package refs and tool refs MUST describe one implementation of those tasks.
- Wrapper and adapter bindings MUST be explicit paths in section state or the
  active installed-ref manifest.
- Existing object keys MUST NOT be overwritten without explicit approval in
  the section contract.
- Marker ranking MUST NOT be represented as condition-level differential
  expression. Condition-level inference requires its own approved section,
  state contract, statistical validity policy, checks, and evidence.
- Final biological interpretation MUST NOT be accepted as evidence for a
  computational section unless the section explicitly implements and validates
  that interpretive task.
- Remote marketplaces, arbitrary executable plugin loading, and generated
  workflow compilers are outside the v1 governance scope.

## Section Development Workflow

1. Specify the section: create or update `section.yml` and `spec.md` with
   biological intent, state contract, refs, expected artifacts, claims, and
   gate status.
2. Approve `spec_review` before implementation planning.
3. Plan the section: resolve pack, workflow, task, package, tool, wrapper,
   adapter, parameters, checks, and installed-ref choices.
4. Approve `plan_review` before task generation or executable changes.
5. Generate tasks from the approved spec and plan; tasks MUST include
   validation, wrapper or adapter checks, evidence recording, and gate updates.
6. Approve `task_review` before running or accepting implementation work.
7. Run deterministic checks and section workflow steps through `bioinfo-sdd`
   or `PYTHONPATH=src python -m bioinfo_sdd`.
8. Record evidence from run state, logs, check JSON, artifacts, refs, caveats,
   and skipped capabilities.
9. Approve or reject `evidence_acceptance`; accepted evidence MUST remain
   bounded to the section's allowed claims.

## Governance

This constitution supersedes conflicting repository practices, templates,
runtime guidance, and generated artifacts. README files, SPEC documents,
skills, templates, checks, and code MUST be interpreted through these
principles when they conflict.

Amendments MUST update `.specify/memory/constitution.md`, include a Sync Impact
Report, explain the version bump, and review dependent templates or guidance in
the same change. Amendments that remove or redefine a principle require a MAJOR
version bump. Amendments that add principles, sections, gates, or materially
expanded obligations require a MINOR version bump. Clarifications that preserve
existing obligations require a PATCH version bump.

Every feature plan, section plan, task list, wrapper change, adapter change,
pack change, and evidence review MUST include a constitution compliance check.
Violations MUST be fixed before proceeding or documented in a complexity or
review section with the reason, affected principle, simpler alternative, and
approval status.

**Version**: 1.0.0 | **Ratified**: 2026-05-24 | **Last Amended**: 2026-05-24
