# ${section_id} Specification

## Biological Intent

Describe the bounded biological or data-state transition for this section.

## Pack And Task Binding

- Declare `pack_refs`, `workflow_ref`, and `task_refs` in `section.yml`.
- Select package refs, tool refs, wrappers, adapters, and checks by installing
  a tool bundle from `tool_market/` into section-local `installed_refs/`.

## Required Input State

- Declare the required object state before this section can run.

## Produced Output State

- Declare only the object state written by this section.

## Allowed Claims

- List claims this section may support after evidence review.

## Forbidden Claims

- List claims this section must not make.

## Review Gate

`spec_review` must be approved before implementation planning continues.
