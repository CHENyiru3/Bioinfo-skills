# Skill System Core Workflow SPEC

Status: initial draft

This document defines the core principles for the Bioinfo-skills system: a
layered, backend-neutral, human-in-the-loop skill tree for bioinformatics
workflows. It is intentionally general and should guide later creation of
runtime `SKILL.md` files, method references, tool references, wrappers, tests,
and execution-adapter bindings.

## 1. Purpose

The Bioinfo-skills system should help agents and users build reliable
bioinformatics workflows one validated section at a time. The system is not a
single-chat workflow generator. It is a guided decision and execution framework
that separates task understanding, method selection, tool-specific execution,
execution-backend binding, validation, and reporting.

The initial goal is to create a clean control structure that can later support
specialized domains such as downstream scRNA analysis, clustering, marker
ranking, spatial analysis, pseudobulk differential expression, and other
bioinformatics workflows.

## 2. Core Principles

1. Task and method nodes are backend-neutral.
   A biological task, required input state, produced output state, and
   scientific caveats should be defined independently from any runner. Snakemake,
   Nextflow, bash, Python scripts, Rscript, and notebooks are execution
   adapters, not the core ontology.

2. Skills are guidance layers, not tools.
   A `SKILL.md` file should guide routing, reasoning, method choice, validation,
   review, and user interaction. Concrete tools such as Leiden, mclust, Scanpy
   functions, R functions, CLI commands, `.py` scripts, and `.R` scripts should
   live as references or runnable assets that are loaded only when needed.

3. The skill tree is layered.
   General entry skills route user intent. Domain and method skills explain
   scientific context and decision points. Tool references provide concrete API,
   parameters, use cases, and runnable examples.

4. Build one workflow section at a time.
   The agent must not build an entire workflow in one chat. Each section should
   follow a loop: understand, plan, choose method/tool, set parameters, implement
   the approved section, test, report, revise if needed, then ask before moving
   to the next section.

5. Human approval is required at phase gates.
   Approval is required before final method/tool choice, before binding an
   execution section into a concrete adapter, and before moving to the next
   workflow task. Routine exploration and read-only inspection can happen before
   approval when it helps the user decide.

6. Scientific claims must be bounded.
   Each skill and tool reference should state what the method can claim, what it
   cannot claim, required input state, important caveats, and failure modes.

7. Reports should drive iteration.
   Repeated work should be automated, but decisions should be based on visible
   feedback: command output, test results, dry-runs, summary tables, plots, or
   runlogs.

## 3. Vocabulary

- Entry skill: the first `SKILL.md` layer. It traces the current issue,
  understands the user request, classifies the task, and routes to the relevant
  domain or method skill.
- Domain skill: a skill for a biological or data domain, such as scRNA, spatial
  transcriptomics, bulk RNA-seq, variant calling, or metagenomics.
- Method skill: a skill for an analysis concept, such as clustering, marker
  ranking, gene signature scoring, pseudobulk differential expression, or
  workflow provenance.
- Tool reference: a non-skill reference for a concrete implementation option,
  such as Scanpy Leiden, Seurat FindClusters, mclust, PyDESeq2, decoupler
  pseudobulk, or a custom wrapper.
- Execution adapter: a backend-specific layer that runs an approved task through
  Snakemake, Nextflow, bash, Python, Rscript, or notebook/IPython organization.
- Runnable asset: a `.py`, `.R`, shell wrapper, notebook section, or workflow
  rule that executes a tool after method choice and parameter approval.
- Workflow section: one bounded piece of a larger workflow, represented by
  backend-neutral task state plus an optional execution-adapter binding.
- Phase gate: a point where the user must approve before the agent proceeds.

## 4. Layered Skill Tree Model

The system should use a hybrid tree: start from user intent, route through
domain and method knowledge, then load tool references only after the choice is
narrowed.

Conceptual layout:

```text
entry SKILL.md
  -> classify user issue
  -> identify domain, task, input state, and missing decisions
  -> route to domain or method skill

domain SKILL.md
  -> define domain assumptions and boundaries
  -> list allowed method families
  -> route to method skill

method SKILL.md
  -> explain what the method is and why it is used
  -> define required inputs, outputs, caveats, and review checks
  -> list registered tool references
  -> help user choose a tool or design a comparison

tool reference
  -> concrete API/function/CLI information
  -> hyperparameters and defaults
  -> expected inputs and outputs
  -> runnable `.py` or `.R` use cases
  -> testing and adapter compatibility notes

execution adapter
  -> approved wrapper/script/notebook/command binding
  -> backend-specific wrapper, rule, process, command, or notebook section
  -> dry-run/test evidence
  -> report or runlog
```

This layout keeps skills stable and compact while allowing many tools to be
registered under a method without turning every tool into a separate top-level
skill.

## 5. Standard Human-in-the-Loop Workflow

Every workflow-building interaction should follow this sequence.

1. Trace and classify the issue.
   The entry skill restates the user request, identifies the likely task class,
   checks current context, and decides which domain or method skill is relevant.

2. Load the method skill.
   The method skill explains the method, why it is used, key assumptions,
   required input state, common outputs, known caveats, and registered tool
   options.

3. Select or compare tools.
   If the user names a tool, load that tool reference and validate suitability.
   If the user is unsure, explain candidate tools and, when feasible, run small
   tests or comparisons before recommending one.

4. Set parameters.
   The tool reference should expose required parameters, optional parameters,
   defaults, allowed values, and high-impact tradeoffs. The agent should ask
   the user for important choices or propose evidence-based defaults.

5. Get phase-gate approval.
   Before implementation, the agent summarizes the selected method, tool,
   input assumptions, outputs, parameters, and validation plan. The user must
   approve this bounded section.

6. Implement only the approved section.
   The agent creates or modifies the minimal script, wrapper, config, or
   adapter binding needed for the approved section. It must not silently add
   unrelated workflow stages.

7. Test and report.
   The agent runs focused tests, wrapper smoke tests, adapter dry-runs, or other
   backend-specific checks as appropriate. It reports what passed, what failed,
   outputs created, and any caveats.

8. Iterate or move on.
   If results are unsatisfactory, adjust parameters or implementation in the
   same section. Move to the next workflow task only after the user approves.

## 6. Execution Adapter Operating Model

Execution adapters provide durable or interactive execution after task and tool
selection. The first durable adapter is Snakemake, but the task tree and package
references must remain usable by Nextflow, bash, Python scripts, Rscript, and
notebook/IPython organization.

- Prefer one tested wrapper, script, command, or notebook section per adapter
  binding.
- Keep analysis logic out of workflow-engine boilerplate.
- Prefer manual, transparent bindings over generated compilers in early
  versions.
- Use dry-runs or structural checks where the adapter supports them.
- Record inputs, outputs, parameters, versions, and caveats in runlogs or
  provenance files.
- Treat wrapper execution tests and adapter structural validation as separate
  evidence.

For the first Snakemake adapter:

- call wrappers/scripts from rules
- pass configuration through external config files such as `--configfile`
- keep analysis code out of the Snakefile body
- use Snakemake dry-runs to validate workflow structure before real execution

## 7. Tool Reference Requirements

A registered tool reference should contain enough information for an agent to
use the tool safely after the method choice is approved.

Minimum required content:

- Tool name and ecosystem.
- Method family it belongs to.
- When to use it and when to avoid it.
- Required input state.
- Expected outputs.
- Complete or linked API parameters.
- Recommended defaults and important hyperparameters.
- Failure modes and validation checks.
- Minimal `.py`, `.R`, or CLI use case when applicable.
- execution-adapter compatibility notes.
- Scientific/statistical caveats.

Tool references should be loaded only when the entry/domain/method skill has
identified that they are relevant. This avoids overloading the agent with every
possible implementation before the user intent is clear.

## 8. Clustering Example

If the user asks to conduct clustering, the expected route is:

```text
entry SKILL.md
  -> classify request as clustering
  -> check domain and input state
  -> load clustering/SKILL.md

clustering/SKILL.md
  -> explain what clustering is
  -> explain why clustering is used
  -> state assumptions and risks
  -> list registered clustering tool references
  -> help user select or compare tools

tool reference, e.g. Leiden or mclust
  -> expose API and hyperparameters
  -> provide runnable use case
  -> define validation outputs

approved workflow section
  -> implement script/wrapper
  -> bind through an execution adapter
  -> dry-run and test
  -> report results
```

The clustering method skill should cover general concepts such as graph-based
clustering, model-based clustering, resolution, stability, cluster size,
reproducibility, and biological interpretability. It should not contain every
tool's full API. Concrete tools such as Leiden, Louvain, mclust, or other
registered methods should be referenced separately with their own parameter and
execution notes.

If the user knows the desired tool, the agent should validate the choice and
ask for high-impact parameters. If the user does not know which tool to use,
the agent should compare options, run small tests when possible, summarize
advantages and drawbacks, recommend a path, and wait for user approval before
implementation.

## 9. Initial Non-Goals

- Do not create a full workflow generator.
- Do not create a Snakemake or Nextflow compiler.
- Do not turn every tool into a top-level skill.
- Do not build multiple workflow stages in one chat.
- Do not couple task nodes or package references to one execution backend.
- Do not hide preprocessing, normalization, model choices, or statistical
  caveats inside tool execution.
- Do not claim biological conclusions beyond what the selected method and
  input state support.

## 10. Acceptance Criteria for This Core System

The first working version of the skill system should be considered acceptable
when:

- The entry skill can classify a user request and route to a method skill.
- A method skill can explain the method and registered tool choices without
  loading every tool reference.
- Tool references can be loaded on demand and contain concrete APIs,
  hyperparameters, use cases, and validation notes.
- A single approved workflow section can be implemented as a script/wrapper and
  bound through an execution adapter, with Snakemake as the first durable
  adapter.
- Tests or dry-runs can be run and reported before moving to the next section.
- The user remains in control at phase gates.
