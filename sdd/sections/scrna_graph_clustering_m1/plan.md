# scrna_graph_clustering_m1 Plan

## Wrapper

Use `wrappers/python/scanpy_neighbors_umap_leiden.py`. The wrapper validates
input state, refuses key collisions unless `--overwrite` is supplied, writes the
mutated `.h5ad`, and emits sidecar JSON/TSV artifacts.

The wrapper is selected through the `scrna.scverse.core` capability pack task
template `scrna.scverse.task.graph_clustering.v0` and the installed market
bundle `scrna.scverse.bundle.scanpy_graph_clustering.v0`, not by the core SDD
engine.

## Adapter

Use `workflow/rules/scrna_graph_clustering.smk` as a Snakemake adapter-only
binding. The rule passes config values to the wrapper and keeps Scanpy logic out
of the workflow file.

The lifecycle workflow is resolved from
`bioinfo.sdd.workflow.section_default.v0` in the declared pack manifest.
Concrete package and tool refs are copied into the section's active
`installed_refs` revision before catalog checks run.

## Parameters

- `representation_key`: `X_pca`
- `neighbors_key`: `neighbors_x_pca`
- `embedding_key`: `X_umap_neighbors_x_pca`
- `cluster_key`: `leiden_neighbors_x_pca`
- `n_neighbors`: `3`
- `n_pcs`: `3`
- `metric`: `euclidean`
- `neighbors_method`: `umap`
- `umap_min_dist`: `0.5`
- `umap_spread`: `1.0`
- `resolution`: `0.5`
- `random_state`: `7`
- `leiden_flavor`: `leidenalg`
- `overwrite`: `false`

## Validation

- Validate `section.yml`.
- Validate the tool market and installed refs.
- Confirm installed refs fill all task tool slots.
- Resolve section stage skills and tool refs.
- Check wrapper and adapter paths.
- Run wrapper tests with synthetic AnnData when dependencies are present.
- Run Snakemake dry-run or skip cleanly when Snakemake is unavailable.

## Review Gate

`plan_review` is approved for the wrapper and adapter binding above.
