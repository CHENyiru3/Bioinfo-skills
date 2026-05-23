---
id: scrna.scverse.package.rapids_singlecell
kind: package_ref
package: rapids_singlecell
import_name: rapids_singlecell
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/core/frameworks/rapids_singlecell
source_urls: [https://rapids-singlecell.readthedocs.io/en/stable/usage_principles.html, https://rapids-singlecell.readthedocs.io/en/stable/api/scanpy_gpu.html, https://rapids-singlecell.readthedocs.io/en/stable/memory_management.html]
source_version: Read the Docs stable archive; current runtime report marks import missing
source_accessed_at: 2026-05-23
source_local_paths: [bioinfo_tutorial/scverse_ecosystem/core/frameworks/rapids_singlecell/rapids-singlecell.readthedocs.io/en/stable/usage_principles.html, bioinfo_tutorial/scverse_ecosystem/core/frameworks/rapids_singlecell/rapids-singlecell.readthedocs.io/en/stable/api/scanpy_gpu.html, bioinfo_tutorial/scverse_ecosystem/core/frameworks/rapids_singlecell/rapids-singlecell.readthedocs.io/en/stable/memory_management.html]
distillation_status: distilled
runtime_status: missing
workflow_stages: ["08_neighbor_graph", "16_specialized_ecosystem"]
install_probe: pending
import_probe: "import rapids_singlecell"
---
# rapids_singlecell

## Role In Scverse Workflow

rapids-singlecell provides GPU-accelerated, Scanpy-like preprocessing, graph,
embedding, clustering, scoring, and selected ecosystem helpers for AnnData.
Use it only when GPU runtime support is explicitly available.

## Supported Stages

- `08_neighbor_graph`: GPU neighbor graph construction when the runtime and
  matrix placement are validated.
- `16_specialized_ecosystem`: GPU-accelerated large-scale or ecosystem helper
  workflows such as decoupler, squidpy, and pertpy-style operations.

## Required Object State

- AnnData with declared `.X` or layer matrix source.
- GPU-compatible CuPy, cuDF, cuML, and RAPIDS stack in the active runtime.
- Data moved to GPU where required, for example through
  `rapids_singlecell.get.anndata_to_GPU`.
- Sufficient GPU memory or an out-of-core Dask policy.

## Produced Object State

- Scanpy-compatible outputs such as `.var["highly_variable"]`,
  `.obsm["X_pca"]`, neighbor graphs, embeddings, clusters, scores, and
  aggregate tables.
- GPU-resident arrays may remain in AnnData until moved back to CPU.

## Major API Families

- Preprocessing: `rapids_singlecell.pp.calculate_qc_metrics`, `filter_cells`,
  `normalize_total`, `log1p`, `highly_variable_genes`, `pca`, `neighbors`,
  `bbknn`, `scrublet`.
- Tools: `rapids_singlecell.tl.umap`, `tsne`, `diffmap`, `leiden`, `louvain`,
  `kmeans`, `score_genes`, `rank_genes_groups`.
- GPU transfer and aggregation: `rapids_singlecell.get.anndata_to_GPU`,
  `anndata_to_CPU`, `X_to_GPU`, `X_to_CPU`, `aggregate`.
- Ecosystem helpers: `dcg`, `gr`, and `ptg` namespaces.

## Runtime Availability

Status is `missing` in the current repo runtime report:
`ModuleNotFoundError: No module named 'rapids_singlecell'`. The docs mirror
does not imply CUDA or RAPIDS availability.

## Failure Modes

- Import can fail without a compatible CUDA/RAPIDS installation.
- GPU memory exhaustion can occur during PCA, neighbors, UMAP, or dense
  conversions.
- Leaving GPU arrays in AnnData can break CPU-only downstream tools.
- CPU and GPU implementations may differ slightly in numeric results.

## Scientific Caveats

- GPU acceleration changes runtime, not the statistical assumptions of the
  underlying Scanpy-like method.
- Large datasets still require documented filtering, normalization, and
  representation choices.
- Faster execution does not justify skipping validation plots and state checks.

## When To Avoid

- Avoid on CPU-only environments.
- Avoid when reproducibility requires exact parity with a previously validated
  CPU workflow.
- Avoid mixing CPU and GPU states without explicit transfer and provenance.

## Sources Used

- Public docs: `https://rapids-singlecell.readthedocs.io/en/stable/usage_principles.html`.
- Public docs: `https://rapids-singlecell.readthedocs.io/en/stable/api/scanpy_gpu.html`.
- Public docs: `https://rapids-singlecell.readthedocs.io/en/stable/memory_management.html`.
- Local archive: `bioinfo_tutorial/scverse_ecosystem/core/frameworks/rapids_singlecell/`.
- Runtime report: `Bioinfo-skills/reports/runtime/scverse_runtime_status.tsv`.
