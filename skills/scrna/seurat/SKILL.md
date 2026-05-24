---
id: scrna.seurat
schema_version: "0.1.0"
kind: skill
domain: scrna
stage: seurat_routing
status: filled
state_in: [scrna_request, seurat_or_r_request]
state_out: [seurat_workflow_stage_route]
registered_refs: [scrna.seurat.package.seurat, scrna.seurat.package.seuratobject, scrna.seurat.package.sctransform, scrna.seurat.package.bpcells, scrna.seurat.package.presto, scrna.seurat.package.glmgampoi, scrna.seurat.package.signac, scrna.seurat.package.harmony]
validation: [confirm_seurat_object_state, backend_neutral]
---
# Seurat Skill

Route R/Seurat single-cell requests through state-gated workflow stages. Use
this route when the user provides a Seurat object, asks for Seurat/R code, needs
Seurat v5 layer behavior, or requests a Seurat tutorial-backed workflow.

Do not choose an execution adapter until the Seurat object state, assay/layer
policy, method, parameters, output keys, and artifacts are approved.

## Routing Rules

- Route object inspection, assay/layer summaries, and version checks to
  `00_state_inspection`.
- Route 10x, HDF5, BPCells, and tutorial dataset loading to `01_data_ingest`.
- Route metadata-based filtering and QC summaries to `02_qc_metrics_filtering`.
- Route log normalization or SCT to `04_normalization_transform`.
- Route variable feature selection to `05_feature_selection`.
- Route PCA and other reductions to `06_dimensionality_reduction`.
- Route CCA/RPCA/Harmony/layer integration to `07_batch_integration`.
- Route nearest-neighbor graph construction to `08_neighbor_graph`.
- Route UMAP and plotting support to `09_embedding_visualization`.
- Route graph community labels to `10_clustering`.
- Route descriptive markers to `11_marker_ranking`.
- Route label transfer and reference mapping to `12_annotation_support`.
- Route gene/module scores to `13_signature_scoring`.
- Route pseudobulk summaries and replicate-aware DE planning to
  `14_aggregation_pseudobulk_de`.
- Route BPCells, Signac, spatial, sketch, Azimuth, and SeuratWrappers work to
  `16_specialized_ecosystem` unless a narrower stage already owns the task.
