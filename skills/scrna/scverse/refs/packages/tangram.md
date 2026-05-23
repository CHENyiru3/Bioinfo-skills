---
id: scrna.scverse.package.tangram
kind: package_ref
package: tangram
import_name: tangram
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/community/python/tangram
source_url: https://tangram-sc.readthedocs.io/en/latest/
source_urls: [https://tangram-sc.readthedocs.io/en/latest/, https://tangram-sc.readthedocs.io/en/latest/classes/tangram.mapping_utils.map_cells_to_space.html, https://tangram-sc.readthedocs.io/en/latest/classes/tangram.utils.project_genes.html, https://tangram-sc.readthedocs.io/en/latest/classes/tangram.utils.project_cell_annotations.html]
source_version: Tangram 0.4.0 docs accessed 2026-05-23; runtime missing
source_accessed_at: 2026-05-23
distillation_status: distilled
runtime_status: missing
workflow_stages: ["16_specialized_ecosystem"]
install_probe: pending
import_probe: "import tangram"
---
# tangram

## Role In Scverse Workflow

Tangram maps single-cell or single-nucleus gene expression profiles onto spatial
gene expression data using shared genes. It is a specialized spatial mapping
tool, not a general annotation or integration default.

## Supported Stages

- `12_annotation_support`: optional spatial projection of cell annotations.
- `16_specialized_ecosystem`: single-cell to spatial expression mapping and
  projection.

## Required Object State

- Single-cell AnnData and spatial AnnData from the same or comparable tissue
  context.
- Shared gene set selected and prepared before mapping.
- Spatial AnnData must contain spatial expression and coordinate metadata
  required by downstream plotting/interpretation.
- Cluster mode requires a declared `adata_sc.obs` cluster or cell-type key.

## Produced Object State

- `map_cells_to_space` returns a cell-by-spot AnnData containing mapping
  probabilities and training genes in `.uns`.
- `project_genes` returns a spot-by-gene AnnData with projected expression.
- `project_cell_annotations` updates spatial AnnData with annotation
  probabilities in `.obsm`.

## Major API Families

- Preprocessing and gene matching: `pp_adatas`, `get_matched_genes`,
  cross-validation helpers.
- Mapping: `map_cells_to_space`, mapping optimizers.
- Projection: `project_genes`, `project_cell_annotations`,
  `transfer_annotations_prob`, annotation counting/deconvolution utilities.
- Evaluation and plotting utilities.

## Runtime Availability

Status is `missing`. Runtime checks must confirm `import tangram`, PyTorch, and
Scanpy-compatible dependencies before use.

## Failure Modes

- Poor shared-gene overlap or inconsistent gene order can invalidate mapping.
- GPU/torch dependency mismatch can prevent or slow optimization.
- Spatial density priors and optimizer hyperparameters can strongly change
  results.
- Mapping can fail scientifically when reference and spatial tissue contexts do
  not match.

## Scientific Caveats

- Tangram infers spatial alignment from shared expression; it does not observe
  individual cell locations directly.
- Projected annotations or genes need validation against spatial markers and
  tissue anatomy.
- Mapping uncertainty should be reported, especially in low-resolution spatial
  assays.

## When To Avoid

- Avoid when single-cell and spatial data are from unrelated tissues, species,
  or incompatible assays.
- Avoid when the shared gene set is too small or dominated by technical genes.
- Avoid presenting projected labels as ground truth locations.

## Sources Used

- Public docs: `https://tangram-sc.readthedocs.io/en/latest/`.
- Public API docs: `https://tangram-sc.readthedocs.io/en/latest/classes/tangram.mapping_utils.map_cells_to_space.html`.
- Public API docs: `https://tangram-sc.readthedocs.io/en/latest/classes/tangram.utils.project_genes.html`.
- Public API docs: `https://tangram-sc.readthedocs.io/en/latest/classes/tangram.utils.project_cell_annotations.html`.
