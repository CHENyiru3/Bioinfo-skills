---
id: scrna.scverse.package.cellmapper
kind: package_ref
package: cellmapper
import_name: cellmapper
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/community/python/cellmapper
source_url: https://cellmapper.readthedocs.io/en/stable/
source_urls: [https://cellmapper.readthedocs.io/en/stable/, https://cellmapper.readthedocs.io/en/latest/generated/cellmapper.CellMapper.html, https://cellmapper.readthedocs.io/en/stable/notebooks/tutorials/query_to_reference_mapping.html]
source_version: cellmapper stable and latest public docs; runtime report records package missing
source_accessed_at: 2026-05-23
distillation_status: distilled
runtime_status: missing
workflow_stages: ["16_specialized_ecosystem"]
install_probe: pending
import_probe: "import cellmapper"
---
# cellmapper

## Role In Scverse Workflow

CellMapper transfers labels, embeddings, or expression between query and
reference AnnData objects using kNN-based mapping matrices in a joint
representation. In this skill system it is a specialized mapping and transfer
candidate.

## Supported Stages

- `16_specialized_ecosystem`: query-reference mapping, modality transfer,
  spatial mapping, or self-mapping after representation choices are explicit.

## Required Object State

- Query AnnData and, except in self-mapping mode, reference AnnData.
- Joint embedding stored in matching `.obsm` keys, or explicit approval to
  compute a baseline joint PCA or CCA.
- Requested transfer keys in reference `.obs`, `.obsm`, `.layers`, or `.X`.
- Shared feature space when expression transfer or joint PCA is used.

## Produced Object State

- Query-side transferred observation labels, embeddings, or imputed expression.
- Mapping matrix and optional presence scores or evaluation outputs.
- Plots or confusion matrices when evaluation labels are available.

## Major API Families

- `cellmapper.CellMapper`: query/reference mapping object.
- Embedding helpers: `compute_joint_pca`, `compute_fast_cca`.
- Mapping steps: `compute_neighbors`, `compute_mapping_matrix`, `map`.
- Transfer helpers: `map_obs`, `map_obsm`, `map_layers`.
- Evaluation: `evaluate_label_transfer`, `evaluate_expression_transfer`,
  `compute_presence_score`.

## Runtime Availability

Status: `missing`. The recorded runtime report shows `ModuleNotFoundError` for
`import cellmapper`; use this ref for planning only until the environment is
updated.

## Failure Modes

- Missing or incomparable joint embeddings.
- Feature-name mismatch during expression transfer.
- Label transfer dominated by batch effects or poor reference coverage.
- Backend-specific neighbor search differences across sklearn, pynndescent,
  faiss, or rapids.

## Scientific Caveats

- Transferred labels are predictions from a chosen reference, not observed
  annotations.
- Mapping quality depends on representation learning and reference relevance.
- Presence scores and imputed values should be validated against held-out or
  orthogonal evidence.

## When To Avoid

- Avoid when query and reference are not biologically comparable.
- Avoid when no joint representation or shared feature basis can be justified.
- Avoid using transferred labels as final annotations without confidence and
  marker review.

## Sources Used

- Public docs: `https://cellmapper.readthedocs.io/en/stable/`.
- Public API docs: `https://cellmapper.readthedocs.io/en/latest/generated/cellmapper.CellMapper.html`.
- Public tutorial: `https://cellmapper.readthedocs.io/en/stable/notebooks/tutorials/query_to_reference_mapping.html`.
- Runtime report: `reports/runtime/scverse_runtime_status.tsv`.
