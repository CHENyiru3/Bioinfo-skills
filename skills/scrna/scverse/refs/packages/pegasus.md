---
id: scrna.scverse.package.pegasus
kind: package_ref
package: pegasus
import_name: pegasus
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/community/python/pegasus
source_url: https://pegasus.readthedocs.io/en/stable/
source_urls: [https://pegasus.readthedocs.io/en/stable/, https://pegasus.readthedocs.io/en/latest/api/, https://pegasusio.readthedocs.io/]
source_version: Pegasus 1.10.x stable/latest docs and PegasusIO 0.10.0 docs accessed 2026-05-23; runtime missing
source_accessed_at: 2026-05-23
distillation_status: distilled
runtime_status: missing
workflow_stages: ["16_specialized_ecosystem"]
install_probe: pending
import_probe: "import pegasus"
---
# pegasus

## Role In Scverse Workflow

Pegasus is a single-cell analysis package and command-line toolkit with its own
PegasusIO data containers. In this skill tree it is a specialized ecosystem
reference, not a drop-in replacement for AnnData-first Scanpy wrappers.

## Supported Stages

- `16_specialized_ecosystem`: Pegasus-native analysis workflows.
- Pegasus has analogs for ingest, QC, normalization, feature selection,
  dimensionality reduction, graph/embedding/clustering, marker analysis, and
  pseudobulk, but those should remain package-specific unless wrappers define a
  conversion boundary.

## Required Object State

- Pegasus APIs generally expect `pegasusio.MultimodalData` or related
  PegasusIO containers.
- Input can be read from formats including h5ad, loom, 10x, mtx, csv, tsv,
  fcs, nanostring, and visium through PegasusIO/Pegasus readers.
- Stage wrappers must declare any AnnData-to-Pegasus conversion and matrix
  source before calling Pegasus functions.

## Produced Object State

- Pegasus functions update PegasusIO containers with `.obs`, `.var`, `.obsm`,
  `.uns`, matrices, embeddings, clusters, and analysis results.
- Pseudobulk APIs can return a separate `MultimodalData`/`UnimodalData` object
  rather than mutating the input.
- Export back to AnnData or files must be an explicit adapter step.

## Major API Families

- I/O: `pegasus.read_input`, PegasusIO readers and writers.
- Preprocessing/QC: `qc_metrics`, filtering, normalization, HVF selection.
- Analysis: `pca`, `neighbors`, `umap`, `leiden`, doublet annotation, marker
  and signature utilities.
- Pseudobulk and DE: `pseudobulk`, `deseq2`, `pseudo.*` helpers.
- CLI and cloud workflow integrations exist outside the AnnData wrapper layer.

## Runtime Availability

Status is `missing`. A runtime report must confirm `import pegasus` and the
PegasusIO dependency set before execution.

## Failure Modes

- Import can fail because Pegasus has compiled and graph/statistical
  dependencies.
- PegasusIO object state can diverge from AnnData assumptions used elsewhere in
  the skill tree.
- Hidden conversion can drop layers, raw counts, categorical metadata, or
  modality names.
- Pseudobulk and DE calls fail when replicate/group keys are absent.

## Scientific Caveats

- Pegasus clustering and marker outputs are descriptive unless paired with an
  appropriate experimental design.
- Pseudobulk DE requires valid biological replicate structure and count-scale
  input.
- Large-scale defaults are not automatically appropriate for small or unusual
  datasets.

## When To Avoid

- Avoid inside AnnData-first wrappers unless conversion and provenance are
  explicit.
- Avoid when the workflow must preserve exact `.layers`, `.raw`, or `.uns`
  semantics without a tested round trip.
- Avoid as a substitute for replicate-aware DE design review.

## Sources Used

- Public docs: `https://pegasus.readthedocs.io/en/stable/`.
- Public API docs: `https://pegasus.readthedocs.io/en/latest/api/`.
- PegasusIO docs: `https://pegasusio.readthedocs.io/`.
