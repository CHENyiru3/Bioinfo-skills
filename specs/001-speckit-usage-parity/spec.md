# Bioinfo SDD Specification: Spec Kit Usage Parity For Bioinfo Skills

**Feature Branch**: `001-speckit-usage-parity`
**Created**: 2026-05-24
**Status**: Draft
**Input**: User description: "Review `/home/heybro/mnt/workspace/spec-kit`; make the current project usage exactly similar to Spec Kit through callable skills, while retaining the Bioinfo SDD workflow and tool-market contract so users can load these skill sets and work with the skill system well."

## Section Scope And Biological Intent *(mandatory)*

This is a non-analysis infrastructure and workflow-usability feature. It aligns
Bioinfo-skills with the upstream Spec Kit usage model: users initialize or load
a project, invoke a small sequence of agent skills, and get durable feature
artifacts that downstream skills can locate without guessing from branch names.

The Bioinfo-skills command surface must feel like Spec Kit for Codex users
while using a Bioinfo-owned namespace that does not conflict with upstream
Spec Kit: `$biokit-constitution`, `$biokit-specify`, `$biokit-clarify`,
`$biokit-checklist`, `$biokit-plan`, `$biokit-tasks`, `$biokit-analyze`,
`$biokit-distill`, and `$biokit-implement` are the primary entry points. Those
entries must route into Bioinfo SDD behavior rather than generic application
generation. Bioinfo
section workflows, section gates, capability packs, `tool_market/` bundles,
and section-local `installed_refs/` remain authoritative.

**Primary section ID**: N/A
**Domain/Ecosystem**: bioinfo-sdd / multi-domain; first validated domain is
scrna / scverse
**Out of scope**: This feature does not add a new biological analysis section,
does not change scRNA method semantics, does not create a remote marketplace,
does not allow arbitrary executable plugin loading, and does not bypass
section gates or installed-ref revisions.

## Clarifications

### Session 2026-05-24

- Q: Which command namespace should Bioinfo-skills use to avoid conflict with upstream Spec Kit? → A: `biokit-*`

## Scenarios And Review Tests *(mandatory)*

### Scenario 1 - Use Spec Kit Style Skills For Bioinfo SDD (Priority: P1)

A Bioinfo-skills user working in Codex can follow the same mental model as
upstream Spec Kit: define project rules, specify a feature, clarify it, check
it, plan it, generate tasks, analyze consistency, distill current state, and
implement. The user does
not need to learn a separate command vocabulary before they can operate the
bioinformatics SDD system.

**Why this priority**: The current goal is adoption and usability. If users
cannot load and call the skill set in the same way as Spec Kit, the Bioinfo SDD
system will feel custom and harder to operate even when the underlying
contracts are stronger.

**Independent Test**: In a fresh checkout, a reviewer can inspect the installed
skill directories and confirm that each core `biokit-*` skill name exists with
Bioinfo SDD-specific instructions and handoff guidance.

**Acceptance Scenarios**:

1. **Given** a Codex user in the Bioinfo-skills repository, **When** they
   invoke `$biokit-specify` with a bioinformatics workflow request, **Then**
   the skill creates a feature spec path that downstream skills can discover
   and the content preserves Bioinfo SDD scope, gates, and refs.
2. **Given** a user familiar with upstream Spec Kit, **When** they review the
   available skill names and recommended command sequence, **Then** they can
   recognize the same high-level workflow while seeing Bioinfo-specific
   constraints where generic app-building behavior would otherwise apply.

---

### Scenario 2 - Preserve Bioinfo Workflow And Tool-Market Contract (Priority: P1)

A maintainer can update skills and templates so Spec Kit-style usage never
turns into a generic application workflow. The generated specs, plans, and
tasks must keep `section.yml` as the canonical state for analysis sections and
must require installed refs for active package/tool context.

**Why this priority**: Usage parity is valuable only if it does not weaken the
scientific review model. The Bioinfo SDD workflow depends on section-scoped
state transitions, gates, packs, tool bundles, installed refs, wrappers,
adapters, deterministic checks, and evidence.

**Independent Test**: Generate or inspect a feature spec and plan for a
bioinformatics analysis request. The artifacts must name section scope, gates,
pack refs, tool-market selection, installed-ref activation, wrapper/adapter
boundaries, deterministic checks, and evidence expectations.

**Acceptance Scenarios**:

1. **Given** a feature that affects an analysis section, **When** planning
   begins, **Then** the plan requires section-local installed refs instead of
   loading the full inactive `tool_market/` as active context.
2. **Given** a feature that changes a tool bundle, wrapper, adapter, pack, or
   check, **When** tasks are generated, **Then** the task list includes review
   of input state, output state, parameters, claims, checks, and evidence.

---

### Scenario 3 - Document The User Journey Clearly (Priority: P2)

A new user can read project guidance and understand how Bioinfo-skills maps the
upstream Spec Kit flow onto bioinformatics workflows. The guidance must explain
which commands to call, what artifacts are created, when to approve gates, and
how market bundles become active context.

**Why this priority**: The skill system will be easier to use if the command
surface, README guidance, and examples tell the same story.

**Independent Test**: A reviewer can read the updated guidance and complete a
dry-run walkthrough from feature request to tasks without asking which command
or artifact comes next.

**Acceptance Scenarios**:

1. **Given** a user who knows Spec Kit but not Bioinfo-skills, **When** they
   read the Bioinfo-skills usage guide, **Then** they can identify the
   equivalent skill sequence and the Bioinfo-specific artifacts created at each
   phase.
2. **Given** a generated feature directory, **When** downstream skills run,
   **Then** they locate the active feature from `.specify/feature.json` and do
   not rely only on Git branch naming.

### Edge Cases

- A user requests generic software behavior rather than a bioinformatics
  section; the workflow must still produce a valid feature spec but mark the
  change as non-analysis infrastructure.
- A user requests a biological operation with unknown input object state; the
  specification must route to state inspection before downstream section work.
- A user asks to choose a concrete package/tool directly; the workflow must
  route through pack/task context and install a selected bundle into
  section-local `installed_refs/`.
- A user replaces a tool bundle; the workflow must preserve historical
  installed-ref revisions and force review of changed state, claims, checks,
  and evidence expectations.
- A user invokes commands from a branch whose name does not match the feature
  directory; downstream commands must use `.specify/feature.json`.
- Multiple agent integrations may exist later; Codex skills under
  `.agents/skills/` must remain isolated and loadable.

## Section Contract *(mandatory for analysis sections)*

### Machine-Readable Source Of Truth

- Canonical artifact for this feature: `specs/001-speckit-usage-parity/spec.md`
- Active feature pointer: `.specify/feature.json`
- Analysis-section canonical artifact when applicable:
  `sdd/sections/<section_id>/section.yml`
- Required gates for analysis sections: `spec_review`, `plan_review`,
  `task_review`, `evidence_acceptance`
- Required refs for analysis sections: `pack_refs`, `workflow_ref`,
  `task_refs`, `skill_refs`, `package_refs`, `tool_refs`, `check_refs`

### Required Input State

- Existing Bioinfo-skills repository with `.specify/`, `.agents/skills/`,
  `sdd/`, `tool_market/`, `skills/`, `wrappers/`, `workflow/`, and
  `src/bioinfo_sdd/` present.
- Upstream Spec Kit checkout is available for review at
  `/home/heybro/mnt/workspace/spec-kit`.
- Current constitution defines Bioinfo SDD principles and must remain the
  governing authority for this feature.

### Produced Output State

- Bioinfo-skills has user-facing `biokit-*` skill guidance that mirrors
  upstream Spec Kit command ergonomics for Codex users without reusing the
  upstream `speckit-*` namespace.
- The workflow stores the active feature directory in `.specify/feature.json`
  for downstream skill discovery.
- Generated specs, plans, tasks, and checklists explain Bioinfo SDD scope,
  gates, pack resolution, tool-market selection, installed refs,
  wrapper/adapter boundaries, deterministic checks, and evidence.
- README or equivalent runtime guidance explains the Spec Kit-like `biokit-*`
  skill sequence for Bioinfo-skills users.

### Allowed Claims

- Users can operate Bioinfo-skills through a Spec Kit-like `biokit-*` skill
  sequence.
- The Bioinfo command surface preserves section-scoped workflows and
  tool-market/installed-ref contracts.
- Downstream skills can discover the active feature without relying only on
  branch naming.
- The updated guidance makes the skill system easier to load and use.

### Forbidden Claims

- The project is a drop-in copy of upstream Spec Kit.
- Generic Spec Kit app-generation behavior overrides Bioinfo SDD governance.
- The inactive `tool_market/` is active context without section-local install.
- Tool, package, wrapper, adapter, or check selection can bypass section gates.
- Biological claims can exceed section evidence because the user invoked a
  Spec Kit-style `biokit-*` skill.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST expose or document the same core user workflow as
  upstream Spec Kit for Codex users under the Bioinfo-owned `biokit-*`
  namespace: constitution, specify, clarify, checklist, plan, tasks, analyze,
  distill, and implement.
- **FR-002**: The system MUST keep Codex skills loadable from
  `.agents/skills/biokit-*/SKILL.md` with command names that match the
  `$biokit-*` invocation style.
- **FR-003**: The system MUST preserve Bioinfo SDD terminology and behavior in
  generated artifacts, including section scope, gates, packs, tool bundles,
  installed refs, wrappers, adapters, checks, and evidence.
- **FR-004**: The system MUST persist the active feature directory in
  `.specify/feature.json` whenever `$biokit-specify` creates a feature spec.
- **FR-005**: Downstream skills MUST locate the active feature from
  `.specify/feature.json` before using branch-name conventions.
- **FR-005a**: `$biokit-distill` MUST create or refresh
  `current-understanding.md` in the active feature directory by summarizing the
  current workflow state, active section, installed refs, packages/tools,
  wrappers, adapters, checks, evidence, pending tasks, risks, and next actions.
- **FR-006**: Analysis-section requests MUST keep `section.yml` as the
  canonical machine-readable source of truth.
- **FR-007**: Package and tool selections MUST become active only through
  section-local `installed_refs/` revisions.
- **FR-008**: Tool bundle replacement MUST trigger review of input state,
  output state, parameters, claims, checks, wrapper, adapter, and evidence
  expectations.
- **FR-009**: Skill and template guidance MUST distinguish generic
  infrastructure features from biological analysis sections.
- **FR-010**: User guidance MUST include at least one Spec Kit-like `biokit-*`
  command sequence and one Bioinfo-specific note about gates and installed refs.

### Validation Requirements

- **VR-001**: Validation MUST confirm that required skill directories and
  `SKILL.md` files exist for the core workflow commands.
- **VR-002**: Validation MUST confirm that generated feature specs contain no
  unresolved template placeholders or clarification markers.
- **VR-003**: Validation MUST confirm that `.specify/feature.json` points to
  the generated feature directory.
- **VR-004**: Validation MUST confirm that Bioinfo SDD constitution checks are
  reflected in plan and task templates.
- **VR-005**: Validation MUST run relevant deterministic checks such as
  `skill_tree` and targeted tests for feature discovery or skill presence.

### Key Entities *(include if feature involves data)*

- **Skill Set**: The installed Codex skill directories that users invoke with
  `$biokit-*` names.
- **Feature Directory**: The durable `specs/<feature>/` folder containing the
  feature spec, quality checklist, plan, tasks, and related design artifacts.
- **Active Feature Pointer**: `.specify/feature.json`, which records the
  feature directory for downstream commands.
- **Bioinfo SDD Section**: A bounded analysis unit with `section.yml`, gates,
  refs, wrappers, adapters, checks, runs, and evidence.
- **Tool Market Bundle**: An inactive selectable bundle that becomes active
  only after installation into a section-local installed-ref revision.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A reviewer can list the core workflow skills and find a
  corresponding `SKILL.md` file for every command in under 2 minutes.
- **SC-002**: A new feature created through `$biokit-specify` writes
  `.specify/feature.json` and downstream commands can identify the feature
  directory without relying on the branch name.
- **SC-003**: In a generated Bioinfo SDD plan, 100% of constitution check items
  address section scope, domain-neutral engine behavior, installed refs, gates,
  evidence, wrapper/adapter boundaries, and deterministic validation.
- **SC-004**: In a generated task list for an analysis-section change, 100% of
  executable tasks remain tied to section artifacts, installed refs, wrappers,
  adapters, checks, or evidence.
- **SC-005**: A user familiar with upstream Spec Kit can correctly identify the
  next Bioinfo-skills `biokit-*` command in the workflow for at least 8 of the
  9 core workflow phases from the project guidance.

## Assumptions

- "Marketer contract" in the user request refers to the repository's
  `tool_market/` and installed-ref contract.
- Codex remains the first supported integration for this repository, with
  Bioinfo workflow skills installed under `.agents/skills/biokit-*/`.
- Upstream Spec Kit is a usage and ergonomics reference, not a dependency to
  copy wholesale.
- The feature should improve command and skill guidance before adding a full
  custom integration installer.
- Historical `$speckit-*` references are documentation-only migration context;
  loadable Bioinfo workflow skills use the Bioinfo-owned `biokit-*` namespace
  described here.
- Bioinfo SDD gates and installed refs are non-negotiable for analysis-section
  work even when the workflow phases mirror upstream Spec Kit.
