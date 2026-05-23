---
id: scrna.scverse.package.liana
kind: package_ref
package: liana
import_name: liana
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/community/python/liana
source_urls: [https://liana-py.readthedocs.io/en/latest/index.html, https://liana-py.readthedocs.io/en/latest/api.html]
source_version: Read the Docs latest archive; current runtime report marks import missing
source_accessed_at: 2026-05-23
source_local_paths: [bioinfo_tutorial/scverse_ecosystem/community/python/liana/liana-py.readthedocs.io/en/latest/index.html, bioinfo_tutorial/scverse_ecosystem/community/python/liana/liana-py.readthedocs.io/en/latest/api.html]
distillation_status: distilled
runtime_status: missing
workflow_stages: ["16_specialized_ecosystem"]
install_probe: pending
import_probe: "import liana"
---
# liana

## Role In Scverse Workflow

LIANA+ supports ligand-receptor and multi-view cell-cell communication
analysis on AnnData and MuData. It is a specialized ecosystem package for
post-annotation communication hypotheses.

## Supported Stages

- `16_specialized_ecosystem`: run ligand-receptor methods, aggregate results,
  inspect resources, and build multi-sample or spatial communication views.

## Required Object State

- AnnData with normalized expression suitable for ligand and receptor scoring.
- Cell identity or sender/receiver groups in `.obs`.
- Gene identifiers matching the selected ligand-receptor resource.
- Optional sample, spatial coordinate, or MuData state for multi-sample and
  spatial workflows.

## Produced Object State

- LIANA results tables, commonly stored under declared `.uns` keys or returned
  as data frames.
- Optional MuData or AnnData views for multi-sample factorization workflows.
- Plot artifacts such as dotplots, tileplots, and connectivity visualizations.

## Major API Families

- Method instances: `liana.method.cellphonedb`, `cellchat`, `natmi`, `logfc`,
  `singlecellsignalr`, `connectome`, `rank_aggregate`.
- Multi-view utilities: `liana.multi.adata_to_views`, `lrs_to_views`,
  `to_tensor_c2c`, `nmf`.
- Resources: `liana.resource.select_resource`, `show_resources`,
  `generate_lr_geneset`, `explode_complexes`.
- Plotting and utilities: `liana.plotting.dotplot`, `tileplot`,
  `connectivity`, `liana.utils.spatial_neighbors`.

## Runtime Availability

Status is `missing` in the current repo runtime report:
`ModuleNotFoundError: No module named 'liana'`. Do not imply installed package
availability from the mirrored docs.

## Failure Modes

- Resource gene symbols may not match `.var_names`.
- Sparse groups or rare cell types can produce unstable ligand-receptor scores.
- Missing sample keys can invalidate multi-sample summaries.
- Spatial workflows fail when coordinates or neighborhood definitions are not
  present.

## Scientific Caveats

- Ligand-receptor co-expression suggests possible communication, not measured
  signaling.
- Results are resource-dependent and can miss non-curated or context-specific
  interactions.
- Differential communication claims need replicate-aware design, not only
  pooled cell-level scores.

## When To Avoid

- Avoid before robust cell annotation and group-level QC.
- Avoid when the gene namespace cannot be reconciled with the selected
  resource.
- Avoid interpreting communication rankings as causal signaling without
  orthogonal support.

## Sources Used

- Public docs: `https://liana-py.readthedocs.io/en/latest/index.html`.
- Public docs: `https://liana-py.readthedocs.io/en/latest/api.html`.
- Local archive: `bioinfo_tutorial/scverse_ecosystem/community/python/liana/`.
- Runtime report: `Bioinfo-skills/reports/runtime/scverse_runtime_status.tsv`.
