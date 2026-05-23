---
id: scrna.scverse.workflow.marker_ranking
schema_version: "0.1.0"
kind: skill
domain: scrna
stage: marker_ranking
status: filled
state_in: ["existing group key in adata.obs", "declared expression source: .raw, .X, or named layer", "logarithmized expression for Scanpy ranking"]
state_out: ["marker_result_key in adata.uns", "marker tables", "group-size summary"]
registered_refs: [scrna.scverse.package.scanpy, scrna.scverse.tool.scanpy_rank_genes_groups]
validation: [backend_neutral, state_contract_checked, marker_policy_checked]
---
# Marker Ranking

## Purpose

Rank genes that characterize already-defined cell groups, usually clusters, so
the user can review candidate marker evidence for annotation or quality review.
This stage is cluster marker ranking. It is descriptive and is not
condition-level differential expression.

## When Required

- The user asks for markers for existing clusters or another declared grouping
  in `adata.obs`.
- Annotation support needs ranked marker evidence before assigning candidate
  labels.
- A downstream report needs per-group marker tables with method and expression
  source metadata.

## When Optional

- The user already supplied trusted marker tables with compatible group names
  and provenance.
- The analysis is only inspecting object state, plotting known annotations, or
  calculating signature scores.
- Marker review is deferred until after clustering, integration, or annotation
  choices are settled.

## When Forbidden

- No grouping column exists in `adata.obs`, or the requested group key is
  missing.
- The requested expression source is absent, ambiguous, or not declared.
- The task is condition-level inference, treatment response testing, or any
  replicate-aware comparison between biological samples.
- The user expects this stage to normalize, filter, integrate, cluster, or
  annotate cells.

## Required Input State

- AnnData object with a declared `groupby` column in `adata.obs`.
- At least two populated groups after excluding missing labels.
- Declared expression source, exactly one of `.raw`, `.X`, or a named
  `adata.layers[...]` key.
- For Scanpy ranking, the selected expression source should be logarithmized
  expression. Raw count-based differential expression belongs to a separate
  pseudobulk path.
- Gene identifiers in `adata.var_names`, with optional gene-symbol column
  declared separately if display names differ from feature IDs.

## Produced Output State

- A declared `marker_result_key`, normally an `adata.uns[...]` key containing
  per-group ranked genes and statistics from the selected tool.
- Exportable marker tables with at least `group`, `gene`, rank/order, score,
  available p-value columns, available log fold-change columns, and parameter
  metadata.
- Group-size summary for every tested group.
- Provenance metadata recording `groupby`, selected groups, reference group,
  method, correction method, expression source, key written, and caveats.

## User Decision Points

- `groupby`: cluster key or other grouping column to rank.
- Expression source: `.raw`, `.X`, or named layer; do not infer silently.
- Ranking method: `wilcoxon`, `t-test`, `t-test_overestim_var`, or `logreg`.
- Reference: `rest` or a specific group.
- Groups to include: all groups or an explicit subset.
- Number of ranked genes to retain and export.
- Whether to calculate expression fractions and whether to apply a post-ranking
  marker filter.
- Output key and table naming convention.

## Registered Package Refs

- `scrna.scverse.package.scanpy`

## Registered Tool Refs

- `scrna.scverse.tool.scanpy_rank_genes_groups`

## Expected Artifacts

- Marker table, preferably one long table with one row per group-gene ranking.
- Group-size table keyed by `groupby`.
- Optional filtered marker table when explicit marker filters are approved.
- Optional plots derived from marker ranking results for review, not as a
  replacement for tables.
- Updated AnnData object only when an execution step is approved to write the
  declared `marker_result_key`.

## Validation Checks

- `groupby` exists in `adata.obs` and has at least two non-empty groups.
- Missing group labels and group sizes are reported before ranking.
- Requested `.raw` or layer exists; missing sources fail instead of falling
  back to `.X`.
- Selected expression source is documented as log-expression or flagged as
  unsuitable for Scanpy marker ranking.
- `marker_result_key` does not overwrite an existing result unless overwrite is
  explicitly approved.
- Marker tables include `method`, `groupby`, `reference`, expression source,
  `marker_result_key`, and software/tool metadata.
- Result columns are checked for expected fields such as names, scores, and
  adjusted p-values when the chosen method produces them.

## Failure Modes

- Missing or misspelled grouping key.
- One group contains too few cells to support useful ranking.
- All cells belong to one group after filtering labels.
- Requested `.raw` or layer is absent.
- `.raw`, `.X`, or layer content does not match the expected gene namespace.
- Input is raw counts or otherwise not logarithmized, leading to invalid Scanpy
  marker ranking assumptions.
- Existing `adata.uns[...]` key would be overwritten without approval.
- Sparse and dense matrices can produce slight numerical differences.

## Statistical Caveats

- Marker ranking compares cells grouped by an existing label and is vulnerable
  to pseudoreplication when interpreted as sample-level inference.
- P-values from cell-level marker ranking do not replace replicate-aware
  condition-level differential expression.
- The method does not account for donor, sample, batch, pairing, or condition
  design unless a selected tool explicitly models those factors.
- Cluster markers are candidate evidence and require human review plus
  supporting biological context before final annotation.

## Allowed Claims

- "These genes are ranked markers that characterize the declared groups under
  the selected method and expression source."
- "Group sizes and parameter metadata were reported with the marker table."
- "This output can support human review of candidate cluster identities."

## Forbidden Claims

- "These markers prove a cell type identity without external evidence or human
  review."
- "These p-values are replicate-aware condition-level differential expression."
- "Cells are independent biological replicates."
- "The stage adjusted for sample, donor, batch, or condition effects unless an
  approved method explicitly did so."
- "Marker ranking normalized, clustered, integrated, or annotated the data."

## Next Stage Routing

- Route to annotation support when ranked markers are ready for human-reviewed
  candidate labels.
- Route to signature scoring when the user asks to score declared gene sets
  rather than rank de novo markers.
- Route to aggregation and pseudobulk differential expression for
  condition-level inference using sample-level replication and raw counts.
- Route back to clustering only if the grouping key is missing or the user
  decides that clusters need to be regenerated.
