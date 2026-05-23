# Marker Ranking Policy

Status: draft

This policy defines the allowed state transition for cluster marker ranking.
It keeps marker discovery separate from condition-level differential expression
and from upstream preprocessing or clustering.

## Scope

Cluster marker ranking may rank genes that characterize existing groups in an
AnnData object. The group key must already exist in `adata.obs`; this policy
does not authorize creating groups, normalizing expression, integrating batches,
or annotating cells.

## Required Inputs

- Existing `groupby` column in `adata.obs`.
- At least two populated groups after excluding missing labels.
- Explicit expression source: `.raw`, `.X`, or a named `adata.layers[...]`
  matrix.
- For Scanpy marker ranking, logarithmized expression in the selected source.
- Declared output key for method results.

## Required Outputs

- Group-size summary, including missing-label counts when present.
- Marker result key and marker table path or object key.
- Marker table metadata: method, groupby, selected groups, reference,
  expression source, result key, software/tool version, and caveat text.

## Required Refusals

- Refuse missing `groupby` keys.
- Refuse missing requested `.raw` or layer sources.
- Refuse ambiguous expression source selection.
- Refuse to silently overwrite an existing marker result key.
- Refuse condition-level or replicate-aware differential expression claims.

## Allowed Claims

- Ranked genes characterize the declared groups under the chosen method,
  expression source, and reference.
- Marker tables can support candidate annotation review.

## Forbidden Claims

- Cells are independent biological replicates.
- Marker ranking p-values are condition-level differential expression evidence.
- Marker ranking accounts for sample, donor, batch, paired design, or treatment
  effects without a separate approved model.
- Marker ranking proves final cell type labels without human review and
  supporting evidence.

## Routing

Use marker ranking before annotation support when the user needs cluster marker
evidence. Use aggregation and pseudobulk differential expression when the user
asks for condition-level inference across replicated biological samples.
