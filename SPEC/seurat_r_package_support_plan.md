# Seurat R Package Support Plan

Status: implemented v0

This SPEC plans the R/Seurat package layer that should sit beside the existing
scverse skill system. It is intentionally a planning artifact: it lists package
tiers, reference targets, environment decisions, and implementation tasks before
actual package refs, skill content, wrappers, or locks are changed.

## 1. Relationship To Other Specs

This SPEC depends on:

- `SPEC/environment_transferability_and_version_traceability.md`
- `SPEC/scverse_content_and_code_fill_plan.md`
- `SPEC/scrna_scverse_skill_system_v0.md`

The Seurat support should follow the same separation already used for scverse:

```text
stage skill       = task and routing guidance
package ref       = package role, install status, docs source, caveats
tool ref          = function-level API notes
wrapper           = executable R code
adapter binding   = Snakemake/Nextflow/bash/notebook execution shape
runtime report    = observed package availability
```

## 2. Source Inventory

Local source material inspected for this plan:

- `seurat_tutorial/environment.yml`
- `seurat_tutorial/SETUP.md`
- `seurat_tutorial/install_v5.html`
- `seurat_tutorial/articles/*.html`
- `seurat_tutorial/reference/*.html`

Important observations:

- The local Seurat docs mirror displays a `5.4.0` docs label on article and
  reference pages.
- Article `sessionInfo()` blocks vary across Seurat 5.0.x, 5.1.x, and 5.3.x
  examples, so those blocks are evidence but not the sole version policy.
- The local tutorial environment is conda-based and pins `r-base=4.4`.
- The current Bioinfo-skills R environment is only
  `envs/r-seurat-placeholder.yml`.
- The current Seurat skill is only `skills/scrna/seurat/SKILL.md` placeholder.

## 3. Target Package Tiers

### Tier 0: Core Seurat Runtime

These packages should be in the default R/Seurat environment.

| R package | Conda package | Source evidence | Role |
| --- | --- | --- | --- |
| Seurat | r-seurat | install page, environment.yml, most articles | Core analysis API |
| SeuratObject | r-seuratobject | environment.yml, BPCells article | Object model and assays |
| sctransform | r-sctransform | environment.yml, SCT vignette | Variance-stabilizing transform |
| Matrix | r-matrix | environment.yml | Sparse matrix support |
| future | r-future | environment.yml, articles | Parallel execution controls |

### Tier 1: Recommended Performance And Scale

These packages are recommended by the Seurat install page or used by large-data
vignettes. They should be available in the base env when conda can resolve them,
or classified as optional with a documented install route.

| R package | Conda package | Source evidence | Role |
| --- | --- | --- | --- |
| BPCells | r-bpcells | install page, environment.yml, BPCells/sketch articles | On-disk matrices and large data |
| presto | r-presto | install page, sessionInfo blocks | Faster marker tests |
| glmGamPoi | bioconductor-glmgampoi | install page, environment.yml | Faster SCT/count models |
| Rfast2 | verify | spatial article mention | Optional spatial speedup |

### Tier 2: Common Tutorial Data, Plotting, And Wrangling

These packages support examples and user-facing workflows. Most are acceptable
in a general Seurat environment, but dataset packages should remain separate.

| R package | Conda package | Source evidence | Role |
| --- | --- | --- | --- |
| ggplot2 | r-ggplot2 | environment.yml, many articles | Plot objects and custom graphics |
| patchwork | r-patchwork | environment.yml, many articles | Combine plots |
| cowplot | r-cowplot | environment.yml, many articles | Plot assembly |
| dplyr | r-dplyr | environment.yml, many articles | Tabular manipulation |
| tibble | r-tibble | environment.yml | Tidy tables |
| magrittr | r-magrittr | environment.yml | Pipe helpers |
| ggrepel | verify | article library calls | Label placement |
| reshape2 | verify | article library calls | Legacy reshape helpers |
| scales | verify | article library calls | Plot scales |
| plotly | r-plotly | environment.yml | Interactive plots |
| SeuratData | source or optional conda route | install page, article data calls | Dataset loader |
| dataset packages | source only | article data calls | Tutorial datasets |

Dataset packages observed in local articles:

- `bmcite`
- `hcabm40k`
- `ifnb`
- `panc8`
- `pbmc3k`
- `pbmcMultiome`
- `pbmcsca`
- `ssHippo`
- `stxBrain`
- `thp1.eccite`

These must be treated as tutorial data assets, not default runtime packages.

### Tier 3: Modalities, Integration, Spatial, And Reference Mapping

These packages should be optional groups with explicit capability labels.

| R package | Conda package | Source evidence | Role |
| --- | --- | --- | --- |
| Signac | r-signac | install page, environment.yml, ATAC/WNN articles | scATAC and chromatin analysis |
| harmony | r-harmony | environment.yml | Harmony integration backend |
| SeuratWrappers | source route | install page, article library calls | Additional methods |
| Azimuth | source route | install page, BPCells article | Reference mapping |
| AzimuthAPI | source route | article library calls | Azimuth service/API support |
| SeuratDisk | source route | BPCells article | h5Seurat/h5ad conversion |
| spacexr | verify | spatial article library call | Spatial deconvolution |
| Banksy | verify | article library calls | Spatial domain methods |

### Tier 4: ATAC And Genome Annotation

These packages support specific ATAC/motif workflows and should not be part of
the default Seurat runtime.

| R package | Source evidence | Role |
| --- | --- | --- |
| EnsDb.Hsapiens.v86 | ATAC article library call | Gene annotation |
| BSgenome.Hsapiens.UCSC.hg38 | article library call | Genome sequence |
| JASPAR2020 | WNN/sessionInfo evidence | Motif database |
| TFBSTools | WNN/sessionInfo evidence | Motif tooling |
| chromVAR | article library call | Motif deviation |
| motifmatchr | article library call | Motif matching |

### Tier 5: Notebook, Build, And Install Tooling

These packages/tools should be in a notebook/docs overlay, not necessarily in
the minimal execution env.

| Package/tool | Conda package | Source evidence | Role |
| --- | --- | --- | --- |
| IRkernel | r-irkernel | environment.yml | R Jupyter kernel |
| rmarkdown | r-rmarkdown | environment.yml | Rendered docs |
| knitr | r-knitr | environment.yml, article calls | Literate examples |
| htmltools | r-htmltools | environment.yml | HTML rendering |
| htmlwidgets | r-htmlwidgets | environment.yml | Widget rendering |
| reticulate | r-reticulate | environment.yml | Python/R bridge |
| remotes | r-remotes | install page, environment.yml | Source installs |
| devtools | r-devtools | environment.yml | Development installs |
| jupyterlab | jupyterlab | environment.yml | Notebook UI |
| pandoc | pandoc | environment.yml | Document conversion |
| git | git | environment.yml | Source package installs |

## 4. Package Ref Targets

Planned package refs should live under:

```text
tool_market/packages/scrna/seurat/
```

Initial refs:

- `seurat.md`
- `seuratobject.md`
- `sctransform.md`
- `bpcells.md`
- `presto.md`
- `glmgampoi.md`
- `signac.md`
- `harmony.md`
- `seuratdata.md`
- `seuratwrappers.md`
- `azimuth.md`
- `seuratdisk.md`

Specialized refs after the initial Seurat core works:

- `spacexr.md`
- `banksy.md`
- `ensdb-hsapiens-v86.md`
- `bsgenome-hsapiens-ucsc-hg38.md`
- `jaspar2020.md`
- `tfbstools.md`
- `chromvar.md`
- `motifmatchr.md`

Every package ref must include:

- package role
- supported workflow stages
- object state assumptions
- major API families
- install/runtime status
- source URLs
- local source paths
- docs/source version
- source access date
- failure modes
- scientific caveats
- when to avoid

## 5. Tool Ref Priorities

Planned tool refs should live under:

```text
tool_market/tools/scrna/seurat/r/
```

Priority 0: Core object and preprocessing tools.

- `Seurat::CreateSeuratObject`
- `Seurat::Read10X`
- `Seurat::Read10X_h5`
- `Seurat::NormalizeData`
- `Seurat::SCTransform`
- `Seurat::FindVariableFeatures`
- `Seurat::ScaleData`

Priority 1: Dimensionality, graph, clustering, and marker tools.

- `Seurat::RunPCA`
- `Seurat::FindNeighbors`
- `Seurat::RunUMAP`
- `Seurat::FindClusters`
- `Seurat::FindMarkers`
- `Seurat::FindAllMarkers`
- `Seurat::AddModuleScore`

Priority 2: Integration, mapping, and conversion.

- `Seurat::IntegrateLayers`
- `Seurat::FindIntegrationAnchors`
- `Seurat::IntegrateData`
- `Seurat::FindTransferAnchors`
- `Seurat::MapQuery`
- `Seurat::as.SingleCellExperiment`
- `SeuratDisk::SaveH5Seurat`
- `SeuratDisk::Convert`

Priority 3: Large data and specialized modalities.

- `BPCells::open_matrix_dir`
- `BPCells::open_matrix_10x_hdf5`
- `BPCells::open_matrix_anndata_hdf5`
- `BPCells::write_matrix_dir`
- `Seurat::SketchData`
- `Signac::GeneActivity`
- `spacexr` entrypoints to be verified
- `Banksy` entrypoints to be verified

Each tool ref must describe the Seurat object slots, assays, layers,
reductions, graphs, identities, and metadata it reads or writes.

## 6. Skill Tree Plan

The current `skills/scrna/seurat/SKILL.md` should become the Seurat router.
It should not contain executable R code. It should route to stage skills that
mirror the existing scverse stage names where possible.

Proposed structure:

```text
skills/scrna/seurat/
  SKILL.md
  README.md
  workflow/
    00_state_inspection/SKILL.md
    01_data_ingest/SKILL.md
    02_qc_metrics_filtering/SKILL.md
    04_normalization_transform/SKILL.md
    05_feature_selection/SKILL.md
    06_dimensionality_reduction/SKILL.md
    07_batch_integration/SKILL.md
    08_neighbor_graph/SKILL.md
    09_embedding_visualization/SKILL.md
    10_clustering/SKILL.md
    11_marker_ranking/SKILL.md
    12_annotation_support/SKILL.md
    13_signature_scoring/SKILL.md
    14_aggregation_pseudobulk_de/SKILL.md
    16_specialized_ecosystem/SKILL.md
```

Seurat-specific state terms should be defined before wrappers are written:

- object path: `.rds`, `.qs`, `.h5seurat`, or converted `.h5ad`
- assays: `RNA`, `SCT`, `ADT`, `ATAC`, spatial assays
- layers: `counts`, `data`, `scale.data`, split layers
- reductions: `pca`, `umap`, `harmony`, integrated reductions
- graphs: nearest-neighbor and shared-nearest-neighbor graphs
- identities: `Idents(object)` and metadata columns
- provenance: commands, parameters, package versions, and written keys

## 7. Environment Plan

The base env should be derived from `seurat_tutorial/environment.yml`, but
trimmed and grouped by capability.

Initial base `envs/r-seurat.yml` package intent:

```text
r-base=4.4
r-seurat
r-seuratobject
r-sctransform
r-bpcells
r-presto
bioconductor-glmgampoi
r-ggplot2
r-patchwork
r-dplyr
r-cowplot
r-tibble
r-magrittr
r-matrix
r-future
r-hdf5r
r-harmony
```

Initial optional `envs/r-seurat-optional.yml` package intent:

```text
r-signac
r-reticulate
r-plotly
r-remotes
r-devtools
source-route: SeuratData
source-route: SeuratWrappers
source-route: Azimuth
source-route: SeuratDisk
verify-route: spacexr
verify-route: Banksy
verify-route: Rfast2
verify-route: ATAC annotation packages
```

Initial notebook/docs `envs/r-seurat-notebook.yml` package intent:

```text
r-irkernel
r-rmarkdown
r-knitr
r-htmltools
r-htmlwidgets
jupyterlab
pandoc
git
```

Implementation must verify conda package availability before committing final
package names for optional packages.

## 8. Runtime And Test Plan

Before claiming Seurat support as installed:

- Add an R runtime probe that loads all base packages and reports versions.
- Add optional probes that classify missing optional packages without failing
  the base runtime.
- Add a small Seurat object fixture or generated toy object for wrapper tests.
- Add Rscript adapter tests separately from wrapper tests.
- Add package-ref coverage tests for the Seurat package matrix.
- Add skill-tree tests that prevent Seurat stage skills from embedding backend
  syntax.

## 9. Implementation Tasks

### Phase 0: Source Audit

- `SEURAT-001`: Record `seurat_tutorial/environment.yml` as local source
  evidence in the Seurat package support notes.
- `SEURAT-002`: Record the package names loaded by article `library()` calls.
- `SEURAT-003`: Record the dataset names loaded through `SeuratData`.
- `SEURAT-004`: Record docs-label evidence that the local mirror is Seurat docs
  `5.4.0`, while article runtime sessions vary.
- `SEURAT-005`: Decide whether the implementation will verify current public
  docs before distilling package refs, or use only the local mirror and mark
  refs `needs_version_check`.

### Phase 1: Environment And Traceability

- `SEURAT-006`: Add Seurat packages to `envs/package-matrix.yml`.
- `SEURAT-007`: Replace `envs/r-seurat-placeholder.yml` with
  `envs/r-seurat.yml`.
- `SEURAT-008`: Add optional and notebook Seurat env overlays.
- `SEURAT-009`: Add an R runtime probe script.
- `SEURAT-010`: Generate `reports/runtime/seurat_runtime_status.*`.
- `SEURAT-011`: Decide whether `renv.lock` is needed for source-route packages
  or whether the base stack is conda-owned.

### Phase 2: Package Refs

- `SEURAT-012`: Add package refs for Seurat, SeuratObject, and sctransform.
- `SEURAT-013`: Add package refs for BPCells, presto, and glmGamPoi.
- `SEURAT-014`: Add package refs for ggplot2, patchwork, dplyr, cowplot, and
  Matrix only if they are referenced directly by skills or wrappers.
- `SEURAT-015`: Add package refs for Signac and Harmony.
- `SEURAT-016`: Add optional package refs for SeuratData, SeuratWrappers,
  Azimuth, and SeuratDisk.
- `SEURAT-017`: Add specialized package refs for spatial and ATAC packages
  after the core Seurat layer is validated.

### Phase 3: Skill Tree

- `SEURAT-018`: Expand `skills/scrna/seurat/SKILL.md` from placeholder router
  to backend-neutral Seurat router.
- `SEURAT-019`: Add Seurat workflow stage placeholders with state terms,
  decision points, validation checks, and registered refs.
- `SEURAT-020`: Add Seurat object-state contract docs for assays, layers,
  reductions, graphs, identities, and metadata.
- `SEURAT-021`: Update entry routing so explicit R/Seurat requests route to
  Seurat skills and Python/scverse requests route to scverse skills.

### Phase 4: Tool Refs

- `SEURAT-022`: Add Priority 0 tool refs for object creation and preprocessing.
- `SEURAT-023`: Add Priority 1 tool refs for PCA, graph, UMAP, clustering, and
  marker ranking.
- `SEURAT-024`: Add Priority 2 tool refs for integration, transfer mapping, and
  conversion.
- `SEURAT-025`: Add Priority 3 tool refs for BPCells, sketching, ATAC, and
  spatial packages after optional package status is known.

### Phase 5: Wrappers And Adapters

- `SEURAT-026`: Add `wrappers/r/inspect_seurat_state.R`.
- `SEURAT-027`: Add a minimal Seurat graph/clustering wrapper only after the
  matching tool refs and package refs are accepted.
- `SEURAT-028`: Add an Rscript adapter binding using existing adapter patterns.
- `SEURAT-029`: Add wrapper tests using a small fixture and runtime probes.
- `SEURAT-030`: Add workflow dry-run tests separate from R wrapper execution
  tests.

## 10. Acceptance Criteria

This plan is complete when:

- The Seurat package set is split into core, performance, optional modalities,
  notebook/docs, and tutorial data groups.
- Every planned package has an intended package ref path and environment group.
- Version provenance is explicit enough to distinguish docs label, article
  runtime versions, environment pins, lock versions, and observed runtime
  versions.
- The first implementation phase can proceed without deciding package lists
  ad hoc inside wrappers or skills.
- The local Seurat tutorial mirror remains source evidence, not a runtime
  dependency.

## 11. v0 Implementation Notes

Implemented in v0:

- package tiers translated into `envs/package-matrix.yml`
- base, optional, and notebook Seurat conda env specs
- Seurat package refs for core, performance, modality, tutorial-data, and
  source-route packages
- Seurat tool refs for ingest, normalization, SCT, feature selection, scaling,
  PCA, graph construction, UMAP, clustering, marker ranking, integration,
  mapping, conversion, BPCells, sketching, and Signac gene activity
- backend-neutral Seurat skill router and stage tree
- `contracts/seurat_object_state_v0.yml`
- `wrappers/r/inspect_seurat_state.R`
- `wrappers/r/seurat_neighbors_umap_clusters.R`
- R runtime report generation and optional wrapper smoke test
- source-route installer for optional SeuratData, SeuratWrappers, Azimuth, and
  SeuratDisk packages
- local repair utility for relocated Seurat tutorial R launchers

Runtime evidence from the local relocated tutorial environment currently shows
Seurat, SeuratObject, sctransform, BPCells, presto, glmGamPoi, Signac, harmony,
SeuratData, SeuratWrappers, Azimuth, and SeuratDisk installed. Source-route
packages remain optional, but they are pinned in
`containers/lockfiles/r-seurat-source-packages.tsv` and loaded successfully in
`reports/runtime/seurat_runtime_status.*`.
