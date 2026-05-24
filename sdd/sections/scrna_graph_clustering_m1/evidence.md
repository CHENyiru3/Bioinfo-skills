# scrna_graph_clustering_m1 Evidence

## Deterministic Checks

Current SDD structural checks are recorded under
`runs/2026-05-24-tool-market/checks/`.

- `pack_manifest`: declared local capability packs are valid.
- `market_manifest`: inactive tool market and bundles are valid.
- `installed_refs`: active section-local copied refs and checksums are valid.
- `task_slots_filled`: installed tools satisfy graph, embedding, and clustering
  slots.
- `section_schema`: section artifact shape is valid.
- `section_catalog_links`: stage skills and tool refs resolve.
- `wrapper_binding`: wrapper path exists.
- `adapter_binding`: adapter path exists.
- `section_artifacts`: required review artifacts exist.

## Execution Evidence

Wrapper behavior is covered by `tests/wrappers/test_scanpy_neighbors_umap_leiden.py`
using synthetic AnnData when `anndata`, `scanpy`, Leiden dependencies, and their
runtime stack are available. Snakemake adapter behavior is covered by the
dependency-aware graph clustering workflow test when Snakemake is installed.

The selected capability pack is `scrna.scverse.core`; the selected workflow ref
is `bioinfo.sdd.workflow.section_default.v0`; the selected task ref is
`scrna.scverse.task.graph_clustering.v0`; and the installed tool bundle is
`scrna.scverse.bundle.scanpy_graph_clustering.v0`.

## Outputs

No production biological outputs are accepted by this repository artifact. The
section records expected output types and validation paths only.

## Caveats

This evidence supports wrapper and adapter structure for graph clustering. It
does not support cell type annotation, condition-level inference, normalization,
feature selection, PCA computation, or final biological interpretation.
