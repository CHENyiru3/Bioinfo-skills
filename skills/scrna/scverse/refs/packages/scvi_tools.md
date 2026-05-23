---
id: scrna.scverse.package.scvi_tools
kind: package_ref
package: scvi_tools
import_name: scvi
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/core/frameworks/scvi_tools
source_urls: [https://docs.scvi-tools.org/en/stable/api/index.html, https://docs.scvi-tools.org/en/stable/api/reference/scvi.model.SCVI.html, https://docs.scvi-tools.org/en/stable/tutorials/index_scrna.html]
source_version: scvi-tools stable docs archive 1.4.3; local runtime missing
source_accessed_at: 2026-05-23
source_local_paths: [bioinfo_tutorial/scverse_ecosystem/core/frameworks/scvi_tools/docs.scvi-tools.org/en/stable/api/index.html, bioinfo_tutorial/scverse_ecosystem/core/frameworks/scvi_tools/docs.scvi-tools.org/en/stable/api/reference/scvi.model.SCVI.html, bioinfo_tutorial/scverse_ecosystem/core/frameworks/scvi_tools/docs.scvi-tools.org/en/stable/tutorials/index_scrna.html]
distillation_status: distilled
runtime_status: missing
workflow_stages: ["07_batch_integration", "12_annotation_support", "16_specialized_ecosystem"]
install_probe: pending
import_probe: "import scvi"
---
# scvi_tools

## Role In Scverse Workflow

scvi-tools provides probabilistic deep generative models for AnnData-backed
single-cell data. In this skill tree it is relevant for batch-aware latent
representations, reference mapping, annotation support, multimodal models, and
selected model-based differential expression.

## Supported Stages

- `07_batch_integration`: learn latent representations such as `X_scVI` for
  downstream graph and embedding steps.
- `12_annotation_support`: use supervised or semi-supervised models such as
  SCANVI when labels and reference design are explicit.
- `16_specialized_ecosystem`: route scvi-tools models for multimodal,
  perturbation, or deep learning workflows.

## Required Object State

- AnnData with raw counts in `.X` or a declared count layer.
- Batch, label, covariate, or modality columns required by the selected model.
- `setup_anndata` or model-specific setup completed with recorded registry
  fields.
- Sufficient cells and batches for training and validation.

## Produced Object State

- A trained model object and serialized model artifacts when saved.
- Latent representations, usually written to `.obsm` by caller code.
- Optional normalized expression, denoised values, label predictions, or
  differential-expression result tables.
- AnnData registry metadata used by scvi-tools to interpret fields.

## Major API Families

- Models: `scvi.model.SCVI`, `SCANVI`, `TOTALVI`, `MULTIVI`, `PEAKVI`,
  `SOLO`, and related classes.
- Data setup and registries: `setup_anndata`, `AnnDataManager`, data loaders.
- Model methods: `train`, `get_latent_representation`,
  `get_normalized_expression`, `differential_expression`, `save`, `load`.
- Tutorials and use cases for scRNA-seq, multimodal data, reference mapping,
  and downstream analysis.

## Runtime Availability

Status is `missing` in `reports/runtime/scverse_runtime_status.tsv`; the import
probe failed with `ModuleNotFoundError: No module named 'scvi'`. Runtime also
depends on PyTorch and optional accelerator libraries.

## Failure Modes

- Using normalized or log-transformed values as counts invalidates count-based
  model assumptions.
- Missing or changed categorical levels can break saved model loading or
  reference mapping.
- GPU, CUDA, PyTorch, JAX, or accelerator mismatches can prevent training.
- Stochastic training, early stopping, and hyperparameters can change outputs.

## Scientific Caveats

- Latent integration can remove or retain biological signal depending on model
  covariates and training choices.
- Model-based differential expression is not a substitute for a documented
  replicate-aware design when condition-level inference is required.
- Annotation transfer depends on reference quality and label ontology.

## When To Avoid

- Avoid when a simple deterministic Scanpy workflow is adequate.
- Avoid if raw counts, batch labels, or model covariates cannot be verified.
- Avoid training large models in unsupported runtimes or without saved seeds,
  parameters, and model artifacts.

## Sources Used

- Public docs: `https://docs.scvi-tools.org/en/stable/api/index.html`.
- Public docs: `https://docs.scvi-tools.org/en/stable/api/reference/scvi.model.SCVI.html`.
- Public docs: `https://docs.scvi-tools.org/en/stable/tutorials/index_scrna.html`.
- Local archive: `bioinfo_tutorial/scverse_ecosystem/core/frameworks/scvi_tools/docs.scvi-tools.org/en/stable/`.
- Runtime report: `reports/runtime/scverse_runtime_status.tsv`.
