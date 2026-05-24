---
name: "biokit-distill"
description: "Create or refresh a current-understanding.md continuity report for a Bioinfo SDD feature or half-finished workflow by reviewing current specs, plans, tasks, section state, installed refs, selected packages/tools, wrappers, adapters, checks, evidence, and unresolved next steps."
compatibility: "Requires spec-kit project structure with .specify/ directory"
metadata:
  author: "github-spec-kit"
  source: "bioinfo-skills/commands/distill.md"
---

## Bioinfo SDD Contract

This skill keeps the upstream Spec Kit-style Codex invocation, but the output is
a Bioinfo SDD continuity artifact. It may create or replace only
`current-understanding.md` in the active feature directory unless the user names
a different output path. Do not change `section.yml`, gates, tasks, installed
refs, wrappers, adapters, checks, evidence, or biological claims. For
analysis-section work, distinguish active section-local `installed_refs/` from
inactive `tool_market/` source material and keep claims bounded by evidence.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Execution Checks

**Check for extension hooks (before distillation)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_distill` key
- If the YAML cannot be parsed or is invalid, skip hook checking silently and continue normally
- Filter out hooks where `enabled` is explicitly `false`. Treat hooks without an `enabled` field as enabled by default.
- For each remaining hook, do **not** attempt to interpret or evaluate hook `condition` expressions:
  - If the hook has no `condition` field, or it is null/empty, treat the hook as executable
  - If the hook defines a non-empty `condition`, skip the hook and leave condition evaluation to the HookExecutor implementation
- When constructing slash commands from hook command names, replace dots (`.`) with hyphens (`-`). For example, `biokit.git.commit` -> `/biokit-git-commit`.
- For each executable hook, output the following based on its `optional` flag:
  - **Optional hook** (`optional: true`):
    ```
    ## Extension Hooks

    **Optional Pre-Hook**: {extension}
    Command: `/{command}`
    Description: {description}

    Prompt: {prompt}
    To execute: `/{command}`
    ```
  - **Mandatory hook** (`optional: false`):
    ```
    ## Extension Hooks

    **Automatic Pre-Hook**: {extension}
    Executing: `/{command}`
    EXECUTE_COMMAND: {command}

    Wait for the result of the hook command before proceeding to the Goal.
    ```
- If no hooks are registered or `.specify/extensions.yml` does not exist, skip silently

## Goal

Create a compact, actionable continuity report for the current feature or
partially completed pipeline so a future Codex session can resume without
re-reading every artifact. The default output is:

```text
FEATURE_DIR/current-understanding.md
```

## Operating Constraints

- **Low mutation**: Only write the continuity report. Do not edit source
  specs, plans, tasks, section files, installed refs, wrappers, adapters,
  checks, or evidence unless the user explicitly changes the task.
- **Current state over aspiration**: Separate what exists now from intended
  future work. Mark unknowns as unknown instead of inferring package state.
- **Active refs only**: Treat section-local `installed_refs/` as active
  package/tool context. Treat `tool_market/` entries as selectable source
  material unless they are installed into the section.
- **Resume focused**: Prefer exact file paths, command outputs, task IDs,
  gate states, and next commands over broad explanation.

## Execution Steps

1. **Resolve active feature**
   - Run `.specify/scripts/bash/check-prerequisites.sh --json --include-tasks`
     from repo root.
   - Parse `FEATURE_DIR` and `AVAILABLE_DOCS`.
   - If that script cannot resolve a feature, read `.specify/feature.json`
     directly. Abort only if no active feature can be identified.

2. **Load feature artifacts**
   - Read available `spec.md`, `plan.md`, `tasks.md`, `research.md`,
     `data-model.md`, `quickstart.md`, and files under `contracts/`.
   - Load only enough content to identify current goal, section scope,
     constraints, completed work, pending work, and unresolved decisions.

3. **Resolve analysis-section state when applicable**
   - Identify section IDs from feature artifacts.
   - If exactly one section ID is in scope, inspect:
     - `sdd/sections/<section_id>/section.yml`
     - `sdd/sections/<section_id>/installed_refs/`
     - gate/evidence/run-state files present in the section directory
   - If no section applies, record `Section: N/A`.
   - If multiple section IDs are plausible, list candidates and mark the
     active section as unresolved.

4. **Distill packages, tools, and execution surface**
   - Summarize active package/tool refs from section-local installed refs.
   - Summarize referenced inactive `tool_market/` bundles separately.
   - List wrappers, adapters, checks, workflow engines, and important command
     invocations referenced by the artifacts.
   - Record missing refs, skipped capabilities, or state that cannot be
     verified from local files.

5. **Summarize task and gate progress**
   - Count completed and incomplete checklist/task items when present.
   - List the next unfinished task IDs and the files they touch.
   - For analysis sections, list gate states if discoverable; otherwise mark
     them unknown.

6. **Write `current-understanding.md`**
   - Replace the existing report atomically enough for normal repository use.
   - Use this structure:

     ```markdown
     # Current Understanding: <Feature Or Section>

     **Generated**: <YYYY-MM-DD>
     **Feature Directory**: `<FEATURE_DIR>`
     **Section**: `<section_id or N/A or unresolved>`
     **Status**: <one sentence>

     ## Resume Summary
     - <highest-signal facts needed to continue>

     ## Active Artifacts
     - Feature spec: `<path or missing>`
     - Plan: `<path or missing>`
     - Tasks: `<path or missing>`
     - Section state: `<path or N/A>`

     ## Workflow State
     - Current phase: <specify/plan/tasks/analyze/distill/implement/evidence/unknown>
     - Completed work: <brief bullets>
     - Pending work: <brief bullets>
     - Gates: <gate states or unknown>

     ## Packages And Tools
     - Active installed refs: <refs or none>
     - Referenced market bundles: <refs or none>
     - Packages/tools actually in use: <names/versions if known>

     ## Execution Surface
     - Wrappers: <paths or none>
     - Adapters/workflows: <paths or none>
     - Checks/tests: <commands or check IDs>

     ## Risks And Unknowns
     - <blockers, ambiguous section state, missing refs, skipped evidence>

     ## Next Actions
     1. <exact next action>
     2. <optional next action>
     3. <optional next action>
     ```

7. **Report result**
   - Print the output path.
   - Mention whether the report found an analysis section, active installed
     refs, unresolved gates, and pending tasks.

8. **Check for extension hooks (after distillation)**
   - Check `.specify/extensions.yml` for `hooks.after_distill`.
   - Apply the same hook filtering and command-format rules used before
     distillation.
   - For each executable optional hook, output:
     ```
     ## Extension Hooks

     **Optional Hook**: {extension}
     Command: `/{command}`
     Description: {description}

     Prompt: {prompt}
     To execute: `/{command}`
     ```
   - For each executable mandatory hook, output:
     ```
     ## Extension Hooks

     **Automatic Hook**: {extension}
     Executing: `/{command}`
     EXECUTE_COMMAND: {command}
     ```

## Quality Bar

- The report must be short enough to scan, but specific enough to resume work.
- Every package/tool claim must be traceable to an active installed ref or
  explicitly labeled as market-only/reference-only.
- Every recommended next action must name the command, task ID, or file path
  that the next Codex session should use.
