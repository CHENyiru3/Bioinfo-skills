---
id: scrna.scverse.package.scfates
kind: package_ref
package: scfates
import_name: scFates
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/community/python/scfates
source_urls: [https://scfates.readthedocs.io/en/latest/api.html, https://scfates.readthedocs.io/en/latest/Tree_operations.html]
source_version: Read the Docs latest archive; current runtime report marks import missing
source_accessed_at: 2026-05-23
source_local_paths: [bioinfo_tutorial/scverse_ecosystem/community/python/scfates/scfates.readthedocs.io/en/latest/api.html, bioinfo_tutorial/scverse_ecosystem/community/python/scfates/scfates.readthedocs.io/en/latest/Tree_operations.html]
distillation_status: distilled
runtime_status: missing
workflow_stages: ["15_trajectory_fate_velocity"]
install_probe: pending
import_probe: "import scFates"
---
# scfates

## Role In Scverse Workflow

scFates builds and analyzes principal curves or trees for pseudotime,
bifurcation, and branch-specific expression programs in Scanpy-compatible
AnnData objects.

## Supported Stages

- `15_trajectory_fate_velocity`: infer principal graphs, choose roots,
  compute pseudotime, test branch-associated genes, and visualize trajectories.

## Required Object State

- AnnData with a suitable low-dimensional representation or graph basis.
- Preprocessed expression and enough cells to support a continuous trajectory.
- Root or milestone assumptions for interpreting pseudotime direction.
- Optional existing CellRank output when converting fate structure to a tree.

## Produced Object State

- Principal graph state under `.uns["graph"]`.
- Pseudotime, segment, and milestone annotations in `.obs`.
- Pseudotime projection metadata under `.uns["pseudotime_list"]`.
- Gene association, trend, module, and branch-specific result tables.

## Major API Families

- Preprocessing: `scFates.pp.filter_cells`, `batch_correct`,
  `find_overdispersed`, `diffusion`.
- Tree inference and operations: `scFates.tl.tree`, `curve`, `circle`,
  `cellrank_to_tree`, `cleanup`, `subset_tree`, `attach_tree`, `simplify`.
- Pseudotime and tests: `root`, `pseudotime`, `test_association`, `fit`,
  `cluster`, `test_fork`, `branch_specific`.
- Plotting and getters: `scFates.pl.graph`, `trajectory`, `dendrogram`,
  `trends`; `scFates.get.modules`, `fork_stats`.

## Runtime Availability

Status is `missing` in the current repo runtime report:
`ModuleNotFoundError: No module named 'scFates'`. Keep wrappers disabled until
the import probe succeeds.

## Failure Modes

- Principal graph inference can fail or overfit when the representation is
  noisy, disconnected, or batch-driven.
- Root and milestone choices can change pseudotime and branch labels.
- Tree subsetting or attachment can leave stale graph metadata if not tracked.
- Gene trend fitting can be slow for many genes.

## Scientific Caveats

- Principal trees are abstractions of continuous expression structure.
- Branch points are hypotheses, not directly observed fate decisions.
- Pseudotime direction requires biological anchoring.

## When To Avoid

- Avoid on discrete unrelated populations with no expected continuum.
- Avoid before strong batch correction and annotation checks.
- Avoid reporting branch-specific genes without multiple-testing and design
  caveats.

## Sources Used

- Public docs: `https://scfates.readthedocs.io/en/latest/api.html`.
- Public docs: `https://scfates.readthedocs.io/en/latest/Tree_operations.html`.
- Local archive: `bioinfo_tutorial/scverse_ecosystem/community/python/scfates/`.
- Runtime report: `Bioinfo-skills/reports/runtime/scverse_runtime_status.tsv`.
