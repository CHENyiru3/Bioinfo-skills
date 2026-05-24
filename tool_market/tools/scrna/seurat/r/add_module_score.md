---
id: scrna.seurat.tool.add_module_score
kind: tool_ref
package_ref: scrna.seurat.package.seurat
api_entrypoint: Seurat::AddModuleScore
method_family: signature_scoring
state_in: [gene_sets, expression_source]
state_out: [metadata_score_columns]
parameters: [object, features, assay, name, nbin, ctrl, seed]
caveats: [gene_symbol_matching, control_gene_policy]
compatible_adapters: [rscript, snakemake, bash]
source_urls: [https://satijalab.org/seurat/reference/addmodulescore]
source_version: local Seurat docs mirror label 5.4.0
source_accessed_at: 2026-05-25
source_local_paths: [seurat_tutorial/reference/addmodulescore.html]
distillation_status: needs_version_check
---
# Seurat::AddModuleScore

## API Entry Point

`Seurat::AddModuleScore(object, features, assay = NULL, name = "Cluster", ...)`

## Method Family

Score gene signatures per cell.

## Required Object State

Gene sets must be declared and mapped to the object's feature naming scheme.

## Output State

Score columns added to object metadata.

## Important Parameters

`features`, `assay`, `name`, `nbin`, `ctrl`, and `seed`.

## Minimal Use

```r
obj <- Seurat::AddModuleScore(obj, features = list(signature), assay = "RNA", name = "sig")
```

## Validation Checks

Check gene-set overlap, output column names, finite scores, and seed.

## Failure Modes

Feature-name mismatch, weak overlap, overwritten metadata columns, and unstable
control-gene sampling.

## Statistical Caveats

Module scores are relative summaries and need context-specific interpretation.

## Adapter Notes

Record gene set source, matched/missing genes, assay, score column names, and
seed.

## Sources Used

- Local reference: `seurat_tutorial/reference/addmodulescore.html`.
