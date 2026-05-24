# Skills

This directory is the canonical project skill tree. Skills route user intent,
state requirements, method choices, validation expectations, and human approval
gates. Concrete package/API details live under `refs/`, and execution backend
syntax lives under `execution/adapters/`.

Codex-loadable skills live under `.agents/skills/`. That directory provides the
Spec Kit-style command surface (`$biokit-constitution`, `$biokit-specify`,
`$biokit-plan`, `$biokit-tasks`, `$biokit-distill`, `$biokit-implement`, and related commands)
plus Bioinfo SDD section helpers such as `bioinfo-sdd-plan-section`.

The public skills in this directory remain the domain guidance tree. The
`.agents/skills/` files are the agent-facing entry points that load the right
context and keep the workflow moving. Both layers must preserve the same
contract: analysis sections use `section.yml`, stop at review gates, keep
`tool_market/` inactive until a bundle is installed into section-local
`installed_refs/`, and accept only evidence-backed claims.
