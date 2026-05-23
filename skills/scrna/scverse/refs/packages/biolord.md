---
id: scrna.scverse.package.biolord
kind: package_ref
package: biolord
import_name: biolord
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/community/python/biolord
source_url: https://biolord.readthedocs.io/en/latest/
source_urls: [https://biolord.readthedocs.io/en/latest/generated/biolord.Biolord.html, https://biolord.readthedocs.io/en/latest/tutorials/biolord_pipeline.html]
source_version: biolord latest public docs; runtime report records package missing
source_accessed_at: 2026-05-23
distillation_status: distilled
runtime_status: missing
workflow_stages: ["16_specialized_ecosystem"]
install_probe: pending
import_probe: "import biolord"
---
# biolord

## Role In Scverse Workflow

biolord provides a deep generative model for learning representations tied to
known ordered or categorical attributes in AnnData. In this skill system it is
a specialized model-based route, not a default preprocessing step.

## Supported Stages

- `16_specialized_ecosystem`: disentangled representation learning,
  prediction, and attribute embedding tasks after design review.

## Required Object State

- AnnData with expression in `.X` or a declared layer.
- Supervised attribute keys in `.obs` or `.obsm`, declared through
  `Biolord.setup_anndata`.
- Optional train, validation, and test split labels in `.obs`.

## Produced Object State

- Trained `Biolord` model artifacts.
- Latent representations, attribute embeddings, or predicted expression
  AnnData objects returned by model methods.
- Optional saved model directory and optional saved AnnData.

## Major API Families

- `biolord.Biolord.setup_anndata`: register expression layer and attributes.
- `biolord.Biolord`: model construction, training, save, and load.
- Representation and prediction methods: `get_latent_representation_adata`,
  `predict`, `compute_prediction_adata`.
- Evaluation and attribute embedding helpers.

## Runtime Availability

Status: `missing`. The recorded runtime report shows `ModuleNotFoundError` for
`import biolord`; use this ref for planning only until the environment is
updated.

## Failure Modes

- Missing or mis-specified supervised attribute keys.
- Leakage or invalid evaluation when split labels do not match the study
  design.
- GPU, PyTorch, or scvi-tools dependency incompatibilities.
- Unstable results from insufficient training data, poor convergence, or
  undocumented random seeds.

## Scientific Caveats

- Learned latent factors are model constructs and need biological validation.
- Attribute disentanglement depends on the correctness and completeness of the
  annotated covariates.
- Predictions are not experimental perturbation evidence.

## When To Avoid

- Avoid when the intended attributes are absent, sparse, or confounded.
- Avoid for routine QC, clustering, or annotation when simpler stage-specific
  tools are sufficient.
- Avoid treating generated expression as observed data.

## Sources Used

- Public API docs: `https://biolord.readthedocs.io/en/latest/generated/biolord.Biolord.html`.
- Public tutorial: `https://biolord.readthedocs.io/en/latest/tutorials/biolord_pipeline.html`.
- Runtime report: `reports/runtime/scverse_runtime_status.tsv`.
