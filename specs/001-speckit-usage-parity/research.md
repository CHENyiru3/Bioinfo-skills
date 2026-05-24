# Research: Spec Kit Usage Parity For Bioinfo Skills

## Decision: Target Linux + Codex Only

Rationale: The user explicitly scoped the work to Linux and Codex for now.
The current repository already has Codex skills in `.agents/skills/`, Bash
helper scripts under `.specify/scripts/bash/`, and an `AGENTS.md` context file.
Limiting scope avoids importing upstream Spec Kit's cross-agent integration
matrix, PowerShell scripts, TOML command formats, and multi-install management
before they are needed.

Alternatives considered:
- Full upstream parity for all Spec Kit integrations: rejected because it adds
  broad platform and agent surface unrelated to current Bioinfo-skills usage.
- Reusing upstream `$speckit-*` command names: rejected after clarification
  because Bioinfo-skills must not conflict with an upstream Spec Kit install.

## Decision: Preserve Upstream Codex Skill Layout With BioKit Names

Rationale: Upstream Spec Kit's Codex integration uses the
`.agents/skills/<command-name>/SKILL.md` layout, defaults to skills mode, and
uses `$ARGUMENTS`. Bioinfo-skills preserves that layout and phase sequence but
uses Bioinfo-owned `biokit-*` command names so it can coexist with upstream
`speckit-*` skills.

Alternatives considered:
- Keep `$speckit-*` as canonical: rejected because it creates namespace
  collision risk.
- Add both namespaces as equal first-class commands: rejected because it keeps
  the collision surface and weakens user guidance.

## Decision: Use `.specify/feature.json` As The Active Feature Pointer

Rationale: Upstream helper scripts now support feature discovery through
`.specify/feature.json` before falling back to branch-name conventions. This
is useful in Bioinfo-skills because a feature may be infrastructure-only and
not tied to an analysis `section_id`; it also makes downstream skills robust
when a branch name and feature directory diverge.

Alternatives considered:
- Branch-only feature discovery: rejected because it is brittle and was a
  known limitation addressed by upstream Spec Kit.
- Section-only discovery: rejected because this feature and future
  infrastructure features may not have `section.yml`.

## Decision: Keep Bioinfo SDD Engine Separate From Spec Kit Workflow Engine

Rationale: Upstream Spec Kit has a general workflow engine with command,
prompt, shell, gate, conditional, loop, fan-out, and fan-in step types. Current
Bioinfo-skills already has a narrower deterministic section workflow runner
with `validate_section`, `gate`, `run_check`, and `record_evidence`. The
Bioinfo runner persists run state under each section, which matches the
constitution's evidence and section-local state principles.

Alternatives considered:
- Port upstream workflow engine into Bioinfo-skills now: rejected because it
  would add unneeded command-dispatch and control-flow complexity.
- Remove Bioinfo workflow runner and use upstream workflow runs: rejected
  because section-local evidence and installed-ref behavior are Bioinfo-specific.

## Decision: Treat Tool Market And Installed Refs As Non-Negotiable Contracts

Rationale: Upstream Spec Kit does not have Bioinfo-skills' inactive tool
market, selected bundles, or section-local installed-ref revisions. Usage
parity must stop at the command/skill experience. Concrete package and tool
choices must still be selected through `tool_market/` and copied into
`sdd/sections/<section_id>/installed_refs/` before becoming active context.

Alternatives considered:
- Let `$biokit-plan` load all `tool_market/` refs as active context: rejected
  because it violates the constitution and bloats context.
- Put tool refs directly into command skills: rejected because it makes tool
  replacement and evidence weaker.

## Decision: Fix Bioinfo Helper Skill Frontmatter Immediately

Rationale: Codex skill loaders expect YAML frontmatter delimited by `---`.
The four helper skills lacked that structure, causing warnings and making them
less reliable as loadable skill assets. Adding minimal frontmatter is a
low-risk compatibility fix and does not change their workflow content.

Alternatives considered:
- Leave the warnings for implementation tasks: rejected because the user
  explicitly requested the fix during planning and it is safely scoped.
