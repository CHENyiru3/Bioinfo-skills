---
id: scrna.seurat.tool.signac_gene_activity
kind: tool_ref
package_ref: scrna.seurat.package.signac
api_entrypoint: Signac::GeneActivity
method_family: atac_gene_activity
state_in: [chromatin_assay]
state_out: [gene_activity_matrix]
parameters: [object, assay, features, extend.upstream, extend.downstream, biotypes]
caveats: [genome_annotation_required, gene_activity_is_proxy]
compatible_adapters: [rscript, snakemake, bash]
source_urls: [https://stuartlab.org/signac/reference/GeneActivity.html]
source_version: Signac docs version needs verification
source_accessed_at: 2026-05-25
source_local_paths: [seurat_tutorial/articles/seurat5_atacseq_integration_vignette.html]
distillation_status: needs_version_check
---
# Signac::GeneActivity

## API Entry Point

`Signac::GeneActivity(object, assay = NULL, features = NULL, ...)`

## Method Family

Estimate gene activity scores from chromatin accessibility.

## Required Object State

The chromatin assay must have genomic ranges and compatible gene annotation.

## Output State

A gene activity matrix suitable for adding as an assay or integration input.

## Important Parameters

Assay, feature set, upstream/downstream extension, and gene biotypes.

## Minimal Use

```r
activity <- Signac::GeneActivity(obj, assay = "ATAC")
```

## Validation Checks

Check annotation genome build, output dimensions, gene identifiers, and sparse
matrix type.

## Failure Modes

Missing annotations, wrong genome build, absent ranges, and slow runtime.

## Statistical Caveats

Gene activity is a proxy for regulatory potential, not measured expression.

## Adapter Notes

Record genome annotation source, assay, extension parameters, and output assay
mapping.

## Sources Used

- Public docs: `https://stuartlab.org/signac/reference/GeneActivity.html`.
- Local archive: `seurat_tutorial/articles/seurat5_atacseq_integration_vignette.html`.
