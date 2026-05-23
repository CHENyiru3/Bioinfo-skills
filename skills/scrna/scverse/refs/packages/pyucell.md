---
id: scrna.scverse.package.pyucell
kind: package_ref
package: pyucell
import_name: pyucell
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/community/python/pyucell
source_url: https://pyucell.readthedocs.io/en/latest/
source_urls: [https://pyucell.readthedocs.io/en/latest/, https://pyucell.readthedocs.io/en/stable/generated/pyucell.compute_ucell_scores.html, https://pyucell.readthedocs.io/en/stable/generated/pyucell.get_rankings.html, https://pyucell.readthedocs.io/en/stable/generated/pyucell.smooth_knn_scores.html]
source_version: pyUCell latest/stable docs accessed 2026-05-23; runtime missing
source_accessed_at: 2026-05-23
distillation_status: distilled
runtime_status: missing
workflow_stages: ["16_specialized_ecosystem"]
install_probe: pending
import_probe: "import pyucell"
---
# pyucell

## Role In Scverse Workflow

pyUCell computes rank-based gene signature scores for AnnData objects. It is a
specialized signature-scoring option when the signature set and matrix source
are explicit.

## Supported Stages

- `13_signature_scoring`: per-cell gene signature scoring.
- `16_specialized_ecosystem`: pyUCell-specific smoothing and ranking workflows.

## Required Object State

- AnnData with cells by genes and gene identifiers matching the requested
  signatures.
- The consumed expression source must be declared: `.X` or a named layer.
- kNN smoothing requires existing score columns in `.obs` and either a
  representation such as `.obsm["X_pca"]` or a precomputed graph in `.obsp`.

## Produced Object State

- `compute_ucell_scores` adds signature score columns to `.obs`.
- `get_rankings` returns a sparse rank matrix and need not mutate AnnData.
- `smooth_knn_scores` adds smoothed score columns to `.obs`.

## Major API Families

- Signature scoring: `pyucell.compute_ucell_scores`.
- Ranking: `pyucell.get_rankings`.
- Score smoothing: `pyucell.smooth_knn_scores`.
- Parameters controlling layers, rank caps, missing genes, negative signatures,
  chunking, and parallelism.

## Runtime Availability

Status is `missing`. A runtime report must confirm `import pyucell` before
wrappers can select this scorer.

## Failure Modes

- Signature genes may be absent or use incompatible identifiers.
- Very large matrices can exceed memory if chunking is not configured.
- Smoothing can fail when the requested representation or graph is missing.
- In-place `.obs` column names can collide with existing score columns.

## Scientific Caveats

- Scores reflect relative ranks, not absolute pathway activity.
- Signature quality, gene identifier mapping, and negative-gene conventions
  drive interpretability.
- kNN smoothing can blur rare-cell or boundary signals.

## When To Avoid

- Avoid when signatures have poor overlap with `adata.var_names`.
- Avoid smoothing when neighborhood structure has not been validated.
- Avoid using scores as standalone proof of cell identity or mechanism.

## Sources Used

- Public docs: `https://pyucell.readthedocs.io/en/latest/`.
- Public API docs: `https://pyucell.readthedocs.io/en/stable/generated/pyucell.compute_ucell_scores.html`.
- Public API docs: `https://pyucell.readthedocs.io/en/stable/generated/pyucell.get_rankings.html`.
- Public API docs: `https://pyucell.readthedocs.io/en/stable/generated/pyucell.smooth_knn_scores.html`.
