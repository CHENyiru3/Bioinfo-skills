---
id: scrna.scverse.package.scyan
kind: package_ref
package: scyan
import_name: scyan
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/community/python/scyan
source_url: https://mics-lab.github.io/scyan/
source_urls: [https://mics-lab.github.io/scyan/, https://mics-lab.github.io/scyan/api/model/, https://mics-lab.github.io/scyan/tutorials/preprocessing/]
source_version: Scyan docs accessed 2026-05-23; runtime missing
source_accessed_at: 2026-05-23
distillation_status: distilled
runtime_status: missing
workflow_stages: ["16_specialized_ecosystem"]
install_probe: pending
import_probe: "import scyan"
---
# scyan

## Role In Scverse Workflow

Scyan is a biology-driven probabilistic model for cytometry cell-population
annotation using AnnData plus an expert knowledge table. It is specialized for
flow or mass cytometry-style marker panels.

## Supported Stages

- `12_annotation_support`: marker-table guided population annotation.
- `16_specialized_ecosystem`: cytometry-specific preprocessing, correction,
  and model workflows.

## Required Object State

- AnnData containing preprocessed and scaled cytometry marker measurements.
- A knowledge table with populations by markers; table columns must match
  `adata.var_names`.
- Optional covariate keys in `.obs` may be used for continuous, categorical, or
  batch effects.

## Produced Object State

- `Scyan.fit` trains a model attached to the provided AnnData.
- `Scyan.predict` writes population labels to `.obs["scyan_pop"]` by default
  and can add hierarchy levels.
- `predict_proba` returns per-population probabilities.
- Batch correction can return corrected marker values for caller-managed
  storage.

## Major API Families

- Model wrapper: `scyan.Scyan`.
- Training and refinement: `fit`, `refine_fit`.
- Annotation: `predict`, `predict_proba`.
- Correction and simulation: `batch_effect_correction`, `sample`.
- I/O, preprocessing, tools, and plotting helpers.

## Runtime Availability

Status is `missing`. Runtime checks must confirm `import scyan`, PyTorch, and
Lightning dependencies before use.

## Failure Modes

- Missing or mismatched marker names between AnnData and the knowledge table.
- Poor preprocessing, scaling, or transform choice can invalidate model input.
- Some populations may not be predicted because of table errors, model
  settings, or true absence.
- GPU/torch dependency conflicts can prevent training.

## Scientific Caveats

- The model is only as good as the expert knowledge table and marker panel.
- Cytometry annotations do not directly transfer to transcriptome-only scRNA
  data without a justified marker mapping.
- Missing predicted populations are not automatically technical failures.

## When To Avoid

- Avoid for standard scRNA expression matrices without cytometry-like marker
  preprocessing.
- Avoid when no vetted knowledge table exists.
- Avoid using predictions without reviewing marker distributions and uncertain
  populations.

## Sources Used

- Public docs: `https://mics-lab.github.io/scyan/`.
- Public API docs: `https://mics-lab.github.io/scyan/api/model/`.
- Public preprocessing docs: `https://mics-lab.github.io/scyan/tutorials/preprocessing/`.
