---
id: scrna.scverse.package.anndata
kind: package_ref
package: anndata
import_name: anndata
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/core/data_structures/anndata
source_urls: [https://anndata.readthedocs.io/en/stable/generated/anndata.AnnData.html, https://anndata.readthedocs.io/en/stable/generated/anndata.io.read_h5ad.html]
source_version: anndata 0.12.13 local runtime; stable docs archived as 0.12.14
source_accessed_at: 2026-05-23
source_local_paths: [bioinfo_tutorial/scverse_ecosystem/core/data_structures/anndata/anndata.readthedocs.io/en/stable/generated/anndata.AnnData.html, bioinfo_tutorial/scverse_ecosystem/core/data_structures/anndata/anndata.readthedocs.io/en/stable/generated/anndata.io.read_h5ad.html]
distillation_status: distilled
runtime_status: installed
workflow_stages: ["00_state_inspection", "01_data_ingest"]
install_probe: "python -c 'import anndata'"
import_probe: "import anndata"
---
# anndata

## Role In Scverse Workflow

AnnData is the object model for single-cell matrices and annotations. In this
skill system it is the state boundary: wrappers inspect or transform declared
AnnData slots rather than assuming a workflow engine or notebook context.

## Supported Stages

- `00_state_inspection`: read and summarize `.h5ad` object structure.
- `01_data_ingest`: create, read, or validate AnnData containers before later
  analysis stages.

## Required Object State

- A readable AnnData object or `.h5ad` file.
- Matrix axis semantics: observations in rows and variables in columns.
- Downstream stages must declare which expression source they consume: `.X`,
  `.raw`, or a named layer.

## Produced Object State

- AnnData readers produce an in-memory or backed AnnData object.
- State inspection produces reports only and must not write AnnData changes.
- Ingest wrappers may produce a new `.h5ad`, but that is a separate approved
  stage.

## Major API Families

- Object container: `anndata.AnnData`.
- Axis annotations: `.obs`, `.var`, `.obs_names`, `.var_names`.
- Matrix and alternate matrices: `.X`, `.layers`, `.raw`.
- Multidimensional and pairwise annotations: `.obsm`, `.varm`, `.obsp`, `.varp`.
- Unstructured metadata: `.uns`.
- I/O: `anndata.io.read_h5ad`, `AnnData.write_h5ad`, and related readers.

## Runtime Availability

Status is `installed` in the recorded scverse runtime used for this scaffold
(`anndata 0.12.13`). Regenerate `reports/runtime/scverse_runtime_status.*` from
the intended Python environment before relying on runtime availability.

## Failure Modes

- `.h5ad` file is missing, corrupt, or from an incompatible storage layout.
- Backed mode limits mutation behavior and can hide expensive I/O behind simple
  slot access.
- Duplicate observation or variable names can make downstream joins ambiguous.
- `.X` may contain counts, normalized values, scaled values, or transformed
  expression; AnnData itself does not enforce the biological meaning.

## Scientific Caveats

- AnnData structure is not evidence that preprocessing was valid.
- Presence of `sample_id`, `batch`, clusters, or embeddings does not prove they
  are biologically meaningful.
- Count-based statistical methods require a true count source, not a structural
  guess.

## When To Avoid

- Do not use AnnData slot presence alone to make biological claims.
- Do not silently use `.X` when a required layer or `.raw` source is absent.
- Do not overwrite `.X`, `.raw`, or canonical layers without an explicit state
  policy and user approval.

## Sources Used

- Public docs: `https://anndata.readthedocs.io/en/stable/generated/anndata.AnnData.html`.
- Public docs: `https://anndata.readthedocs.io/en/stable/generated/anndata.io.read_h5ad.html`.
- Local archive: `bioinfo_tutorial/scverse_ecosystem/core/data_structures/anndata/anndata.readthedocs.io/en/stable/`.
- Runtime version observed in the scverse tutorial environment: `anndata 0.12.13`.
