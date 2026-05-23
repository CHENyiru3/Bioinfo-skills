---
id: scrna.scverse.package.pydeseq2
kind: package_ref
package: pydeseq2
import_name: pydeseq2
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/community/python/pydeseq2
source_urls: [https://pydeseq2.readthedocs.io/en/latest/api/index.html, https://pydeseq2.readthedocs.io/en/latest/usage/requirements.html, https://pydeseq2.readthedocs.io/en/latest/index.html]
source_version: PyDESeq2 latest docs archive 0.5.4; local runtime missing
source_accessed_at: 2026-05-23
source_local_paths: [bioinfo_tutorial/scverse_ecosystem/community/python/pydeseq2/pydeseq2.readthedocs.io/en/latest/api/index.html, bioinfo_tutorial/scverse_ecosystem/community/python/pydeseq2/pydeseq2.readthedocs.io/en/latest/usage/requirements.html, bioinfo_tutorial/scverse_ecosystem/community/python/pydeseq2/pydeseq2.readthedocs.io/en/latest/index.html]
distillation_status: distilled
runtime_status: missing
workflow_stages: ["14_aggregation_pseudobulk_de"]
install_probe: pending
import_probe: "import pydeseq2"
---
# pydeseq2

## Role In Scverse Workflow

PyDESeq2 is a Python implementation inspired by DESeq2 for count-based
differential expression. In this skill tree it belongs after pseudobulk
aggregation, where observations represent biological samples or sample-group
aggregates rather than individual cells.

## Supported Stages

- `14_aggregation_pseudobulk_de`: replicate-aware differential expression on
  pseudobulk or bulk count matrices.

## Required Object State

- Integer count matrix with samples as observations and genes as variables, or
  an AnnData object representing that state.
- Metadata with sample-level covariates and a design that is not confounded.
- Biological replicates for the tested condition or contrast.
- Declared contrast, alpha, and filtering policy.

## Produced Object State

- `DeseqDataSet` object with size factors, dispersions, model fit state, and
  normalized counts or intermediate fields.
- `DeseqStats` result tables with log2 fold changes, test statistics, p-values,
  and adjusted p-values.
- Optional serialized tables and provenance for design, contrast, and filters.

## Major API Families

- Dataset and model fitting: `pydeseq2.dds.DeseqDataSet`.
- Statistics and contrasts: `pydeseq2.ds.DeseqStats`.
- Execution backend: `pydeseq2.default_inference.DefaultInference` and
  `pydeseq2.inference.Inference`.
- Utilities, preprocessing, and grid-search helpers.

## Runtime Availability

Status is `missing` in `reports/runtime/scverse_runtime_status.tsv`; the import
probe failed with `ModuleNotFoundError: No module named 'pydeseq2'`.

## Failure Modes

- Non-integer, normalized, or log-transformed values invalidate the model.
- Too few replicates, all-zero genes, or rank-deficient designs can fail or
  produce unreliable estimates.
- Confounded batch and condition metadata make contrasts uninterpretable.
- PyDESeq2 0.5.4 docs note Python version constraints for recent releases.

## Scientific Caveats

- DESeq2-style inference assumes sample-level count data and a suitable
  negative-binomial model.
- Pseudobulk DE tests sample-level effects; it does not test individual cells as
  independent replicates.
- Results depend on the design formula, filtering, and contrast definition.

## When To Avoid

- Avoid on per-cell matrices without pseudobulk aggregation.
- Avoid when raw counts or biological replicates are unavailable.
- Avoid complex experimental designs that cannot be represented and checked in
  the selected PyDESeq2 interface.

## Sources Used

- Public docs: `https://pydeseq2.readthedocs.io/en/latest/api/index.html`.
- Public docs: `https://pydeseq2.readthedocs.io/en/latest/usage/requirements.html`.
- Public docs: `https://pydeseq2.readthedocs.io/en/latest/index.html`.
- Local archive: `bioinfo_tutorial/scverse_ecosystem/community/python/pydeseq2/pydeseq2.readthedocs.io/en/latest/`.
- Runtime report: `reports/runtime/scverse_runtime_status.tsv`.
