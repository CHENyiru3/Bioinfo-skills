---
id: scrna.scverse.tool.scanpy_read_h5ad
kind: tool_ref
package_ref: scrna.scverse.package.scanpy
api_entrypoint: scanpy.read_h5ad
method_family: state_inspection_data_ingest
source_urls: [https://scanpy.readthedocs.io/en/stable/generated/scanpy.read_h5ad.html]
source_version: scanpy 1.11.5 local runtime; stable docs page signature archived
source_accessed_at: 2026-05-23
source_local_paths: [BioBrain/reference/scverse_docs/scanpy_docs/scanpy.readthedocs.io/en/stable/generated/scanpy.read_h5ad.html]
distillation_status: distilled
state_in: [h5ad_file]
state_out: [AnnData]
parameters: [filename, backed, as_sparse, as_sparse_fmt, chunk_size]
caveats: [backed_objects_may_not_be_mutable, reader_does_not_validate_biological_state]
compatible_adapters: [snakemake, python_script, ipython_notebook]
---
# scanpy.read_h5ad

## API Entry Point

`scanpy.read_h5ad(filename, backed=None, *, as_sparse=(), as_sparse_fmt=csr_matrix, chunk_size=6000)`

Use this reader for `.h5ad` state inspection and ingest. For read-only
inspection, load the object, summarize state, and do not write changes back to
the input file.

## Method Family

State inspection and data ingest.

## Required Object State

- Input path points to an existing `.h5ad`.
- The file is compatible with AnnData/scverse I/O.
- No biological preprocessing state is required before reading.

## Output State

- Returns an AnnData object in memory by default.
- With backed read mode, returns an AnnData object linked to the source file.
- The reader itself does not create a state report; wrappers must serialize any
  inspection results explicitly.

## Important Parameters

- `filename`: required path to the `.h5ad` file.
- `backed`: default `None`. Use read-only backed mode only when memory requires
  it and the wrapper will not mutate the object.
- `as_sparse`: default empty. Can read named dense arrays as sparse matrices.
- `as_sparse_fmt`: default CSR sparse matrix class for arrays listed in
  `as_sparse`.
- `chunk_size`: default `6000`; used while converting dense stored arrays to
  sparse on read.

## Minimal Use

```python
import scanpy as sc

adata = sc.read_h5ad("input.h5ad")
shape = adata.shape
layer_names = list(adata.layers.keys())
```

## Validation Checks

- Assert the input path exists and has an `.h5ad` suffix before reading.
- Verify the returned object has observation and variable axes.
- Record `.X`, `.raw`, `.layers`, `.obsm`, `.obsp`, `.varm`, `.varp`, and
  `.uns` keys.
- Record the reader package versions.
- For state inspection, verify that no output `.h5ad` is written.

## Failure Modes

- Missing or unreadable file.
- HDF5 or AnnData storage incompatibility.
- Backed arrays cannot be summarized the same way as in-memory arrays.
- Large dense matrices can make full in-memory inspection expensive.

## Statistical Caveats

- Reading a file does not prove that counts, normalization, cluster labels, or
  sample design are valid.
- A present `.raw` object is not automatically the correct expression source.
- A count-like `.X` sample is only a structural hint; downstream count use still
  requires explicit approval.

## Adapter Notes

- Adapter bindings should call a wrapper such as
  `wrappers/python/inspect_anndata_state.py`; do not embed direct reader logic
  in the workflow adapter.
- Pass input and report paths as explicit CLI arguments.
- Capture reader versions in a separate versions artifact.

## Sources Used

- Public docs: `https://scanpy.readthedocs.io/en/stable/generated/scanpy.read_h5ad.html`.
- Local archive: `BioBrain/reference/scverse_docs/scanpy_docs/scanpy.readthedocs.io/en/stable/generated/scanpy.read_h5ad.html`.
- Runtime version observed in the scverse tutorial environment: `scanpy 1.11.5`.
