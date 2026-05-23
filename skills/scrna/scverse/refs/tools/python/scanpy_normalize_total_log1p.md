---
id: scrna.scverse.tool.scanpy_normalize_total_log1p
kind: tool_ref
package_ref: scrna.scverse.package.scanpy
api_entrypoint: scanpy.pp.normalize_total + scanpy.pp.log1p
method_family: normalization_transform
source_urls: [https://scanpy.readthedocs.io/en/stable/generated/scanpy.pp.normalize_total.html, https://scanpy.readthedocs.io/en/stable/generated/scanpy.pp.log1p.html]
source_version: scanpy 1.11.5 local runtime; stable generated docs archived locally
source_accessed_at: 2026-05-23
source_local_paths: [BioBrain/reference/scverse_docs/scanpy_docs/scanpy.readthedocs.io/en/stable/generated/scanpy.pp.normalize_total.html, BioBrain/reference/scverse_docs/scanpy_docs/scanpy.readthedocs.io/en/stable/generated/scanpy.pp.log1p.html]
distillation_status: distilled
state_in: [raw_counts_preserved]
state_out: [log1p_normalized_expression]
parameters: [target_sum, exclude_highly_expressed, max_fraction, key_added, layer, base, chunked, chunk_size]
caveats: [preserve_counts_before_overwriting_X, do_not_log1p_twice]
compatible_adapters: [snakemake, python_script, ipython_notebook]
---
# Scanpy Normalize Total And Log1p

## API Entry Point

`scanpy.pp.normalize_total(adata, *, target_sum=None, exclude_highly_expressed=False, max_fraction=0.05, key_added=None, layer=None, obsm=None, inplace=True, copy=False)`

`scanpy.pp.log1p(data, *, base=None, copy=False, chunked=None, chunk_size=None, layer=None, obsm=None)`

Use these APIs together only after an approved count-source policy exists.
`normalize_total` scales each observation to a target total or, when
`target_sum=None`, to the median pre-normalization total. `log1p` applies
`log(x + 1)`, using the natural logarithm unless `base` is specified.

## Method Family

Normalization and transform for count-derived single-cell expression.

## Required Object State

- AnnData has a declared raw-count source, preferably `layers["counts"]`.
- If `.X` contains raw counts and will be overwritten, raw counts must first be
  preserved in a declared layer by explicit policy.
- The intended output target does not already exist, or overwrite has been
  explicitly approved and recorded.
- The selected source has not already been normalized/log-transformed for this
  stage.

## Output State

- Normalized/log expression exists in the declared output target, conventionally
  `layers["log1p_norm"]` or an approved working `.X`.
- Raw counts remain present in the declared count source.
- Optional size factors or normalization factors may be recorded in `.obs` when
  `key_added` is used.
- Provenance records `target_sum`, log transform, log base, source key, output
  key, and overwrite policy.

## Important Parameters

- `target_sum`: target total count per cell. Common policies include `1e4` for
  counts per cell or `1e6` for CPM-like values; `None` uses the median total.
- `layer`: named layer to transform instead of `.X`; never silently fall back to
  `.X` if the requested layer is absent.
- `base`: log base for `log1p`; `None` means natural log.
- `key_added`: optional `.obs` field for normalization factors; record the key
  if used.
- `exclude_highly_expressed` and `max_fraction`: optional normalization policy
  for excluding very highly expressed genes while computing size factors.
- `chunked` and `chunk_size`: memory controls for `log1p` on large AnnData
  objects.
- `copy` and `inplace`: API mutation controls; wrappers still need explicit
  output-key and count-preservation policy.

## Minimal Use

The approved operation should follow this semantic sequence:

1. Identify the count source from the state report.
2. Preserve counts under a declared count key if the mutable target would
   overwrite them.
3. Normalize the declared working target with the recorded `target_sum`.
4. Apply `log1p` once with the recorded `base`.
5. Write or retain the result under the declared normalized/log expression key.
6. Record source key, output key, `target_sum`, log policy, and overwrite
   decision.

This reference intentionally does not define a reusable wrapper.

## Validation Checks

- Count source exists before transformation and remains present afterward.
- Output target exists after transformation and has the same shape as the input
  cell-by-gene matrix.
- No existing count or expression key was overwritten without an explicit
  policy record.
- `target_sum`, log flag, log base, input source, and output key are present in
  provenance.
- Matrix-state checks do not indicate a second `log1p` application.
- No HVG, PCA, graph, embedding, cluster, or marker keys were produced by this
  operation.

## Failure Modes

- Raw counts are lost because `.X` or a count layer was overwritten.
- The input matrix was already log-transformed and receives another `log1p`.
- A requested `layer` is absent and an implementation falls back to `.X`.
- `target_sum` is omitted or inconsistent with downstream expectations.
- Existing `layers["log1p_norm"]` or `.obs` factor keys are overwritten without
  approval.
- Dask, sparse, dense, or backed arrays trigger unexpected compute or memory
  behavior for the chosen parameters.

## Statistical Caveats

- Library-size normalization and `log1p` are preprocessing transforms, not
  batch correction or condition-level statistical modeling.
- Scaling to a common total can change relative influence of high-abundance
  genes; the chosen target and exclusion policy should be recorded.
- Log-normalized values must not be used as raw counts for count-based DE,
  doublet detection, or `seurat_v3` HVG selection.
- Normalization success does not prove that QC thresholds, sample design, or
  biological interpretation are valid.

## Adapter Notes

- Adapters should pass explicit source, output, `target_sum`, log base, and
  overwrite-policy values to an approved implementation.
- Adapters should fail when the declared count source or output policy is
  missing instead of choosing defaults silently.
- Reports should include Scanpy version, input/output keys, matrix shape, and
  count-preservation check results.
- Do not combine this operation with HVG, PCA, graph, clustering, marker, or
  plotting work in a single adapter step.

## Sources Used

- Public docs: `https://scanpy.readthedocs.io/en/stable/generated/scanpy.pp.normalize_total.html`.
- Public docs: `https://scanpy.readthedocs.io/en/stable/generated/scanpy.pp.log1p.html`.
- Local archive: `BioBrain/reference/scverse_docs/scanpy_docs/scanpy.readthedocs.io/en/stable/generated/scanpy.pp.normalize_total.html`.
- Local archive: `BioBrain/reference/scverse_docs/scanpy_docs/scanpy.readthedocs.io/en/stable/generated/scanpy.pp.log1p.html`.
- Runtime version observed in the scverse tutorial environment: `scanpy 1.11.5`.
