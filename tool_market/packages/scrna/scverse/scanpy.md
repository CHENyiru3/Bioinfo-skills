---
id: scrna.scverse.package.scanpy
kind: package_ref
package: scanpy
import_name: scanpy
language: python
ecosystem: scverse
docs_local: BioBrain/reference/scverse_docs/scanpy_docs
source_urls: [https://scanpy.readthedocs.io/en/stable/usage-principles.html, https://scanpy.readthedocs.io/en/stable/generated/scanpy.read_h5ad.html]
source_version: scanpy 1.11.5 local runtime; stable docs archived with generated pages
source_accessed_at: 2026-05-23
source_local_paths: [BioBrain/reference/scverse_docs/scanpy_docs/scanpy.readthedocs.io/en/stable/usage-principles.html, BioBrain/reference/scverse_docs/scanpy_docs/scanpy.readthedocs.io/en/stable/generated/scanpy.read_h5ad.html]
distillation_status: distilled
runtime_status: installed
workflow_stages: ["00_state_inspection", "01_data_ingest", "02_qc_metrics_filtering", "04_normalization_transform", "05_feature_selection", "06_dimensionality_reduction", "08_neighbor_graph", "09_embedding_visualization", "10_clustering", "11_marker_ranking", "13_signature_scoring", "14_aggregation_pseudobulk_de", "15_trajectory_fate_velocity"]
install_probe: "python -c 'import scanpy'"
import_probe: "import scanpy"
---
# scanpy

## Role In Scverse Workflow

Scanpy provides core Python APIs for reading AnnData objects, preprocessing,
neighborhood graphs, embeddings, clustering, marker ranking, scoring, and
aggregation. In this repository, Scanpy is a tool source for approved wrappers;
the biological stage skill defines the intended state transition.

## Supported Stages

- `00_state_inspection`: read `.h5ad` and inspect object state.
- `01_data_ingest`: read supported single-cell files into AnnData.
- `02_qc_metrics_filtering`: calculate QC metrics and support filtering after
  explicit thresholds are approved.
- `04_normalization_transform`: normalize and log-transform after count-source
  policy is declared.
- `05_feature_selection`: select highly variable genes.
- `06_dimensionality_reduction`: compute PCA or related representations.
- `08_neighbor_graph`, `09_embedding_visualization`, `10_clustering`: build and
  use graph, embedding, and cluster keys from declared representations.
- `11_marker_ranking`: rank genes for existing groups.
- `13_signature_scoring`: score declared gene sets.
- `14_aggregation_pseudobulk_de`: aggregate expression, but condition-level DE
  needs separate replicate-aware tooling.
- `15_trajectory_fate_velocity`: selected graph and trajectory utilities, with
  specialized caveats.

## Required Object State

- Most Scanpy functions operate on AnnData.
- Each wrapper must declare the consumed matrix source: `.X`, `.raw`, or a named
  layer.
- Downstream tools that use existing keys must check those keys first, such as
  `obsm["X_pca"]`, neighbor graph keys, or an `.obs` group column.

## Produced Object State

- Scanpy tools commonly write into AnnData in place.
- Wrapper code must constrain mutations to approved keys and record parameter
  choices under system-owned provenance.
- Read-only state inspection produces reports and no mutated AnnData object.

## Major API Families

- I/O: `scanpy.read_h5ad`, `scanpy.read`, `scanpy.read_10x_mtx`.
- Preprocessing: `scanpy.pp.calculate_qc_metrics`, `normalize_total`, `log1p`,
  `highly_variable_genes`, `pca`, `neighbors`.
- Tools: `scanpy.tl.umap`, `leiden`, `rank_genes_groups`, `score_genes`.
- Accessors: `scanpy.get.rank_genes_groups_df`, `scanpy.get.aggregate`.
- Plotting APIs exist but are not evidence-generating analysis steps by
  themselves.

## Runtime Availability

Status is `installed` in the recorded scverse tutorial runtime
(`scanpy 1.11.5`). Regenerate runtime reports from the intended environment
before executing wrappers.

## Failure Modes

- Import may fail if optional compiled dependencies are absent.
- In-place mutation can overwrite keys when wrapper parameters are not explicit.
- Functions may assume normalized/log expression, neighbor graphs, or group
  labels that are not present.
- Backed reads are useful for memory but restrict mutation behavior.

## Scientific Caveats

- Scanpy functions expose analysis mechanics; they do not validate biological
  design by default.
- Cluster marker ranking is descriptive and is not sample-replicate-aware
  condition-level differential expression.
- Count-based methods require preserved counts and should not consume
  log-normalized values.

## When To Avoid

- Avoid direct Scanpy calls in workflow adapter files; call approved wrappers.
- Avoid hidden preprocessing inside downstream wrappers.
- Avoid using Scanpy plotting output as sole evidence for biological claims.
- Avoid proceeding when the AnnData state report cannot identify the required
  source keys.

## Sources Used

- Public docs: `https://scanpy.readthedocs.io/en/stable/usage-principles.html`.
- Public docs: `https://scanpy.readthedocs.io/en/stable/generated/scanpy.read_h5ad.html`.
- Local archive: `BioBrain/reference/scverse_docs/scanpy_docs/scanpy.readthedocs.io/en/stable/`.
- Runtime version observed in the scverse tutorial environment: `scanpy 1.11.5`.
