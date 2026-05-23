---
id: scrna.scverse.package.popv
kind: package_ref
package: popv
import_name: popv
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/community/python/popv
source_url: https://popv.readthedocs.io/en/stable/
source_urls: [https://popv.readthedocs.io/en/stable/, https://popv.readthedocs.io/en/latest/api.html, https://popv.readthedocs.io/en/stable/reference/popv.preprocessing.Process_Query.html, https://popv.readthedocs.io/en/latest/generated/popv.annotation.annotate_data.html]
source_version: popV stable/latest docs accessed 2026-05-23; runtime missing
source_accessed_at: 2026-05-23
distillation_status: distilled
runtime_status: missing
workflow_stages: ["16_specialized_ecosystem"]
install_probe: pending
import_probe: "import popv"
---
# popv

## Role In Scverse Workflow

popV supports reference-based cell type annotation by combining multiple
transfer/classification methods and reporting agreement. In this skill tree it
belongs to annotation support with explicit reference provenance.

## Supported Stages

- `12_annotation_support`: consensus label transfer from annotated references.
- `16_specialized_ecosystem`: popV-specific model, ontology, and hub workflows.

## Required Object State

- Query AnnData and reference AnnData with shared features.
- Reference `.obs` must contain the declared cell-type label key and batch key
  when used.
- Raw-count layers may be required through `query_layer_key` or `ref_layer_key`
  for some modes.
- `Process_Query` must prepare the combined AnnData before `annotate_data`.

## Produced Object State

- `Process_Query` returns or exposes a combined AnnData and stores annotation
  configuration in `.uns`.
- `annotate_data` writes classifier predictions, consensus labels, agreement
  scores, and optional embeddings/probabilities into AnnData fields.
- Optional model artifacts may be read from or written to a training-model path.

## Major API Families

- Preprocessing: `popv.preprocessing.Process_Query`.
- Annotation pipeline: `popv.annotation.annotate_data`, `AlgorithmsNT`.
- Algorithms: KNN over scVI/BBKNN/Harmony/Scanorama embeddings, scANVI,
  support vector, random forest, XGBoost, OnClass, and CellTypist.
- Visualization: agreement, prediction score, cell-type ratio, and confusion
  matrix plots.
- Hub helpers for pretrained model metadata and downloads.

## Runtime Availability

Status is `missing`. Runtime checks must verify `import popv` and optional
method dependencies before selecting algorithms.

## Failure Modes

- Missing optional dependencies can disable selected classifiers.
- Reference/query gene mismatch, missing label keys, or missing raw-count layers
  can stop preprocessing.
- GPU-backed modes can be slow or unavailable.
- Ontology resources are required for OnClass unless ontology use is disabled.

## Scientific Caveats

- popV is intended to highlight cells needing manual review, not to replace
  expert annotation.
- Consensus agreement is not proof that the transferred label is biologically
  correct.
- Reference tissue, assay, ontology, and batch composition strongly affect
  results.

## When To Avoid

- Avoid when no appropriate annotated reference is available.
- Avoid for novel states where forcing known labels would be misleading.
- Avoid using predictions without reporting reference provenance and agreement
  diagnostics.

## Sources Used

- Public docs: `https://popv.readthedocs.io/en/stable/`.
- Public API docs: `https://popv.readthedocs.io/en/latest/api.html`.
- Public API docs: `https://popv.readthedocs.io/en/stable/reference/popv.preprocessing.Process_Query.html`.
- Public API docs: `https://popv.readthedocs.io/en/latest/generated/popv.annotation.annotate_data.html`.
