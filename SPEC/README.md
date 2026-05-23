# SPEC Index

This folder stores architecture and planning specifications for the
Bioinfo-skills system. SPEC documents define durable design decisions before
runtime skills, tool references, wrappers, schemas, or execution-adapter
workflows are created.

## Current Specs

- [Skill System Core Workflow](skill_system_core_workflow.md): core principles,
  layered skill tree model, execution-adapter boundary, and human-in-the-loop
  workflow for building bioinformatics tasks step by step.
- [scRNA Scverse Skill-System v0](scrna_scverse_skill_system_v0.md):
  backend-neutral scverse task tree plan, AnnData state gates, package/tool
  reference contracts, execution adapter model, and v0 implementation phases.
- [Design Principles](design_principles.md): high-level design guardrails for
  the skill and reference system.
- [Routing Policy](routing_policy.md): entry-skill routing rules for domain,
  state, task, and backend selection.
- [Scverse Content And Code Fill Plan](scverse_content_and_code_fill_plan.md):
  implementation roadmap for turning scaffolded scverse skills, refs, schemas,
  wrappers, adapter bindings, tests, and provenance into actual working content
  one validated section at a time.

## SPEC Rules

- SPEC files are planning artifacts, not executable workflow components.
- Runtime skills should be created only after their governing SPEC is clear.
- Tool-specific API notes, scripts, and wrappers are references loaded by
  skills when needed; they are not themselves the top-level skill.
- Task nodes and package/tool references should be independent of a workflow
  runner. Snakemake, Nextflow, bash, Python scripts, Rscript, and notebooks are
  execution adapters.
- Workflow construction should happen incrementally: plan, test, report,
  revise, approve, then continue.
