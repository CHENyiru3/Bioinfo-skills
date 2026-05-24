# Bioinfo SDD Specification: [SECTION OR FEATURE NAME]

**Feature Branch**: `[###-feature-name]`
**Created**: [DATE]
**Status**: Draft
**Input**: User description: "$ARGUMENTS"

## Section Scope And Biological Intent *(mandatory)*

[Describe the bounded biological or data-state transition. Name whether this
is an analysis section, core engine capability, capability-pack change,
tool-market change, wrapper/adapter change, or documentation-only change.]

**Primary section ID**: `[section_id or N/A]`
**Domain/Ecosystem**: `[domain]` / `[ecosystem]`
**Out of scope**: [List upstream preprocessing, downstream interpretation, or
other tasks this specification does not authorize.]

## Scenarios And Review Tests *(mandatory)*

### Scenario 1 - [Brief Title] (Priority: P1)

[Describe the human or agent workflow in plain language.]

**Why this priority**: [Explain the scientific, reproducibility, or workflow value.]

**Independent Test**: [Describe the deterministic command, artifact review, or
gate review that proves this scenario independently.]

**Acceptance Scenarios**:

1. **Given** [declared input state], **When** [bounded action], **Then**
   [expected section state, artifact, check result, or gate result]
2. **Given** [review condition], **When** [validation runs], **Then**
   [expected pass/fail/skip behavior]

---

### Scenario 2 - [Brief Title] (Priority: P2)

[Describe this workflow slice only if it can be reviewed independently.]

**Why this priority**: [Explain value.]

**Independent Test**: [Describe independent verification.]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

[Add more scenarios only when each one remains independently reviewable.]

### Edge Cases

- What happens when required input object state is absent or unknown?
- What happens when a selected package or optional runtime dependency is unavailable?
- What happens when a tool bundle replacement changes parameters, keys, claims, or checks?
- What happens when a section attempts to overwrite existing object keys?
- What happens when evidence supports only a subset of allowed claims?

## Section Contract *(mandatory for analysis sections)*

### Machine-Readable Source Of Truth

- Canonical artifact: `sdd/sections/[section_id]/section.yml`
- Required gates: `spec_review`, `plan_review`, `task_review`,
  `evidence_acceptance`
- Required refs: `pack_refs`, `workflow_ref`, `task_refs`, `skill_refs`,
  `package_refs`, `tool_refs`, `check_refs`

### Required Input State

- [Declare object type, matrix/layer slots, keys, metadata columns, embeddings,
  graph state, grouping variables, or other preconditions.]

### Produced Output State

- [Declare only the object state and files this section writes.]

### Allowed Claims

- [List claims this section may support after evidence review.]

### Forbidden Claims

- [List claims this section must not make.]

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST preserve section scope as one bounded biological
  or data-state transition.
- **FR-002**: The system MUST keep `section.yml` as the canonical
  machine-readable source of truth when Markdown review artifacts differ.
- **FR-003**: The system MUST resolve pack, workflow, task, package, tool,
  wrapper, adapter, and check refs through declared local manifests.
- **FR-004**: The system MUST use section-local `installed_refs/` for active
  package and tool context.
- **FR-005**: The system MUST record allowed claims, forbidden claims, expected
  artifacts, gate status, and validation evidence.

### Validation Requirements

- **VR-001**: Plans and tasks MUST name the deterministic checks or tests that
  will validate changed behavior.
- **VR-002**: Wrapper or adapter changes MUST include binding checks and a
  focused execution or dry-run test when runtime dependencies are available.
- **VR-003**: Missing optional runtime dependencies MUST be recorded as skipped
  checks with reasons.
- **VR-004**: Evidence MUST link to actual run state, logs, check JSON, active
  installed-ref revision, wrapper, adapter, and accepted outputs.

### Key Entities *(include if feature involves data)*

- **Section**: A bounded SDD unit with state contract, refs, gates, tasks, and
  evidence.
- **Capability Pack**: A local manifest bundle that owns domain workflow and
  task meaning.
- **Tool Bundle**: An inactive market selection that installs package/tool refs
  and bindings into a section-local revision.
- **Installed Ref Revision**: The active, reproducible package/tool context for
  a section.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The feature can be validated with named `bioinfo-sdd` commands,
  unit tests, or explicit review gates.
- **SC-002**: Reviewers can identify the section scope, input state, output
  state, refs, checks, artifacts, and claim boundaries from repository files.
- **SC-003**: Replacing a tool/package choice preserves historical installed
  refs and forces review of changed state, parameters, claims, and evidence.
- **SC-004**: No accepted artifact expands biological claims beyond the section
  contract.

## Assumptions

- [Assumption about source object state, fixture availability, or runtime
  packages.]
- [Assumption about whether this change affects analysis sections, core engine,
  packs, tool market, wrappers, adapters, or docs.]
- [Assumption about review gate ownership and approval timing.]
