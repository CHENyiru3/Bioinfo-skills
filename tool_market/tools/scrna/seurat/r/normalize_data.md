---
id: scrna.seurat.tool.normalize_data
kind: tool_ref
package_ref: scrna.seurat.package.seurat
api_entrypoint: Seurat::NormalizeData
method_family: normalization
state_in: [seurat_object_counts]
state_out: [normalized_data_layer]
parameters: [object, normalization.method, scale.factor, margin, block.size, assay]
caveats: [counts_required, active_assay_policy]
compatible_adapters: [rscript, snakemake, bash, ipython_notebook]
source_urls: [https://satijalab.org/seurat/reference/normalizedata]
source_version: local Seurat docs mirror label 5.4.0
source_accessed_at: 2026-05-25
source_local_paths: [seurat_tutorial/reference/normalizedata.html]
distillation_status: needs_version_check
---
# Seurat::NormalizeData

## API Entry Point

`Seurat::NormalizeData(object, normalization.method = "LogNormalize", scale.factor = 10000, assay = NULL, ...)`

## Method Family

Normalize counts for an assay.

## Required Object State

The selected assay must contain counts. The active assay or explicit assay must
match the approved plan.

## Output State

Normalized values in the assay data layer and updated command provenance.

## Important Parameters

`normalization.method`, `scale.factor`, and `assay`.

## Minimal Use

```r
obj <- Seurat::NormalizeData(obj, assay = "RNA", scale.factor = 10000)
```

## Validation Checks

Check counts layer exists, output data layer exists, dimensions are unchanged,
and active assay handling is explicit.

## Failure Modes

Wrong assay, missing counts, accidental renormalization, and hidden active-assay
side effects.

## Statistical Caveats

Log normalization is not a replicate-aware transformation and should not be
mixed silently with SCT workflows.

## Adapter Notes

Record assay, method, scale factor, input object path, output object path, and
package version.

## Sources Used

- Local reference: `seurat_tutorial/reference/normalizedata.html`.
