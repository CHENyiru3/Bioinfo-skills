---
id: scrna.scverse.package.doubletdetection
kind: package_ref
package: doubletdetection
import_name: doubletdetection
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/community/python/doubletdetection
source_urls: [https://doubletdetection.readthedocs.io/en/latest/api.html, https://doubletdetection.readthedocs.io/en/latest/tutorial.html]
source_version: Read the Docs latest archive; current runtime report marks import missing
source_accessed_at: 2026-05-23
source_local_paths: [bioinfo_tutorial/scverse_ecosystem/community/python/doubletdetection/doubletdetection.readthedocs.io/en/latest/api.html, bioinfo_tutorial/scverse_ecosystem/community/python/doubletdetection/doubletdetection.readthedocs.io/en/latest/tutorial.html]
distillation_status: distilled
runtime_status: missing
workflow_stages: ["03_doublet_detection"]
install_probe: pending
import_probe: "import doubletdetection"
---
# doubletdetection

## Role In Scverse Workflow

DoubletDetection predicts likely droplet multiplets from a raw or lightly
filtered scRNA-seq count matrix. In this skill tree it is an optional
implementation source for the doublet detection stage, not a hidden QC step.

## Supported Stages

- `03_doublet_detection`: call candidate doublets and store scores after the
  count source and thresholds are declared.

## Required Object State

- AnnData with cells in rows and genes in columns.
- A count-like matrix source, usually `.X` or a named counts layer; normalized
  or log-transformed matrices should not be used for fitting.
- Genes should be minimally filtered to remove all-zero or near-empty features.

## Produced Object State

- Boolean doublet calls can be written to a declared `.obs` key such as
  `doubletdetection_doublet`.
- Continuous scores can be written to `.obs`, for example
  `doubletdetection_score`.
- Diagnostic plots are artifacts only; they are not AnnData state by
  themselves.

## Major API Families

- Classifier: `doubletdetection.BoostClassifier`.
- Fitting and scoring: `BoostClassifier.fit`, `predict`, `doublet_score`.
- Diagnostics: `doubletdetection.plot.convergence` and `plot.threshold`.

## Runtime Availability

Status is `missing` in the current repo runtime report:
`ModuleNotFoundError: No module named 'doubletdetection'`. Do not claim this
package is installed unless a fresh runtime report proves it.

## Failure Modes

- Dense conversion or standard scaling can exhaust memory on large count
  matrices.
- Threshold choices can strongly change the number of called doublets.
- Optional clustering backends and Scanpy dependencies can fail if versions are
  mismatched.
- Running after aggressive filtering can remove signal needed to identify
  artificial doublet neighborhoods.

## Scientific Caveats

- Doublet calls are probabilistic QC annotations, not ground truth.
- Homotypic doublets are harder to detect than heterotypic doublets.
- Expected doublet rate depends on loading chemistry and cell recovery.

## When To Avoid

- Avoid when only normalized expression is available and counts cannot be
  recovered.
- Avoid automatic removal without reporting thresholds and retained cell counts.
- Avoid using this as the only doublet evidence for multiplexed or hash-tagged
  designs where sample-tag evidence is available.

## Sources Used

- Public docs: `https://doubletdetection.readthedocs.io/en/latest/api.html`.
- Public docs: `https://doubletdetection.readthedocs.io/en/latest/tutorial.html`.
- Local archive: `bioinfo_tutorial/scverse_ecosystem/community/python/doubletdetection/`.
- Runtime report: `Bioinfo-skills/reports/runtime/scverse_runtime_status.tsv`.
