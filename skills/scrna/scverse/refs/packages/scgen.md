---
id: scrna.scverse.package.scgen
kind: package_ref
package: scgen
import_name: scgen
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/community/python/scgen
source_url: https://scgen.readthedocs.io/en/stable/
source_urls: [https://scgen.readthedocs.io/en/stable/, https://scgen.readthedocs.io/en/latest/api/reference/scgen.SCGEN.html, https://scgen.readthedocs.io/en/latest/tutorials/scgen_perturbation_prediction.html, https://scgen.readthedocs.io/en/latest/tutorials/scgen_batch_removal.html]
source_version: scGen stable/latest docs accessed 2026-05-23; runtime missing
source_accessed_at: 2026-05-23
distillation_status: distilled
runtime_status: missing
workflow_stages: ["16_specialized_ecosystem"]
install_probe: pending
import_probe: "import scgen"
---
# scgen

## Role In Scverse Workflow

scGen is a scvi-tools based generative model for perturbation response
prediction and labeled batch-effect removal. It is a specialized modeling
package, not a routine preprocessing default.

## Supported Stages

- `07_batch_integration`: only for labeled scGen batch-removal use cases.
- `16_specialized_ecosystem`: perturbation prediction and model evaluation.

## Required Object State

- AnnData registered through `scgen.SCGEN.setup_anndata`.
- Required `.obs` keys include condition/batch labels and cell-type labels for
  the intended training or prediction task.
- Training data should have appropriate normalization/HVG policy declared before
  model setup.
- Perturbation prediction requires control and stimulated condition labels and
  the target cell type or subset.

## Produced Object State

- Model training produces a trained `SCGEN` model and optional saved model
  artifacts.
- Latent representations can be written by callers into `.obsm`, commonly as
  `X_scgen`.
- `predict` returns predicted AnnData and a perturbation delta, rather than
  proving the prediction biologically.
- `batch_removal` returns corrected expression/state for downstream inspection.

## Major API Families

- Model setup and training: `SCGEN.setup_anndata`, `SCGEN`, `train`.
- Representation and decoding: `get_latent_representation`,
  `get_decoded_expression`.
- Perturbation prediction: `predict`, `binary_classifier`.
- Batch correction: `batch_removal`.
- Model persistence and diagnostics: `save`, `load`, `reg_mean_plot`,
  `reg_var_plot`.

## Runtime Availability

Status is `missing`. Runtime checks must confirm `import scgen`, scvi-tools,
PyTorch, and any accelerator requirements before use.

## Failure Modes

- Missing or imbalanced labels can make setup or prediction invalid.
- GPU/torch dependency mismatches can prevent training.
- Views, nonunique observation names, or modified AnnData after setup can cause
  warnings or invalid registrations.
- Predictions can be unstable when the target state is outside the training
  support.

## Scientific Caveats

- Predicted perturbation responses are model hypotheses and need experimental
  or held-out validation.
- Batch removal can erase real biological differences if labels or design are
  confounded.
- The method assumes meaningful shared latent structure across conditions,
  cell types, studies, or species.

## When To Avoid

- Avoid for routine integration without explicit labels and evaluation.
- Avoid when perturbation conditions are fully confounded with batch or donor.
- Avoid using generated expression as observed data in downstream claims.

## Sources Used

- Public docs: `https://scgen.readthedocs.io/en/stable/`.
- Public API docs: `https://scgen.readthedocs.io/en/latest/api/reference/scgen.SCGEN.html`.
- Public tutorial: `https://scgen.readthedocs.io/en/latest/tutorials/scgen_perturbation_prediction.html`.
- Public tutorial: `https://scgen.readthedocs.io/en/latest/tutorials/scgen_batch_removal.html`.
