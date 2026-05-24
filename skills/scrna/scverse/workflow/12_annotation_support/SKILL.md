---
id: scrna.scverse.workflow.annotation_support
schema_version: "0.1.0"
kind: skill
domain: scrna
stage: annotation_support
status: filled
state_in: ["marker evidence", "cluster key", "species/gene namespace"]
state_out: ["annotation candidates"]
registered_refs: [scrna.scverse.package.scanpy, scrna.scverse.tool.scanpy_rank_genes_groups]
validation: [backend_neutral, state_contract_checked]
---
# Annotation Support

## Purpose

Support human review of candidate labels for existing clusters or cell groups by
connecting marker evidence, known marker biology, species/gene namespace, and
reference context. This stage is interpretive support: it proposes candidate
annotations and records evidence, conflicts, and uncertainty. It does not rank
markers, score gene signatures, perform condition-level differential
expression, or finalize biological labels without user approval.

## When Required

- The user asks for candidate cell type or state labels for existing clusters,
  groups, or imported labels.
- Marker ranking results or trusted marker tables need to be interpreted into a
  reviewable annotation table.
- The analysis needs an evidence ledger linking clusters to supporting markers,
  conflicting markers, reference sources, and confidence notes.
- Existing labels must be harmonized, renamed, or compared against marker
  evidence before downstream summaries.

## When Optional

- Curated annotations already exist, have provenance, and satisfy the current
  question.
- The user only asks to rank markers, score a declared signature, visualize
  existing labels, or run replicate-aware condition-level differential
  expression.
- Annotation review is intentionally deferred until clustering or marker
  ranking choices are revisited.

## When Forbidden

- No declared group or cluster key is available.
- No marker evidence, reference marker list, or domain knowledge source is
  available for review.
- The species or gene identifier namespace is unknown or incompatible with the
  marker evidence.
- The user asks for condition-level inference, treatment response testing, or
  replicate-aware differential expression.
- The requested output would present automatic labels as final truth without
  human review and caveats.

## Required Input State

- AnnData state or exported tables with a declared group key, usually a cluster
  or existing annotation column.
- Marker evidence for each group, such as ranked marker tables from
  `11_marker_ranking`, curated marker lists, or imported reference evidence.
- Species and gene namespace policy, including whether identifiers are gene
  symbols, Ensembl IDs, or another feature namespace.
- Group-size summary and, when available, sample/batch/condition cross-tabs to
  detect confounded labels.
- Optional reference source metadata: tissue, species, assay, citation, atlas,
  or expert-provided marker set.
- Optional existing labels that should be retained, compared, or replaced only
  after approval.

## Produced Output State

- Annotation candidate table with one row per reviewed group or per
  group-candidate pair.
- For each candidate: proposed label, label granularity, supporting markers,
  absent expected markers, conflicting markers, reference/source notes,
  uncertainty level, and review status.
- Optional draft annotation key name for later execution, only if the user
  approves writing labels back to object state.
- Provenance metadata describing marker evidence source, group key, species,
  namespace mapping, reference sources, reviewer decisions, and caveats.

## User Decision Points

- Which group key to annotate.
- Which marker evidence source to trust for each group.
- Species and gene identifier namespace, including any ortholog or symbol
  mapping policy.
- Label granularity: broad lineage, cell type, subtype, activation state,
  cycling state, stress state, or "unknown".
- Reference sources to consider authoritative for the tissue and assay.
- How to handle mixed, low-quality, doublet-like, or ambiguous groups.
- Whether candidate labels should remain a table only or later be written to a
  draft `.obs` annotation key.
- Naming convention for labels and confidence/review-status fields.

## Registered Package Refs

- `scrna.scverse.package.scanpy`

## Registered Tool Refs

- `scrna.scverse.tool.scanpy_rank_genes_groups`, only as a common upstream
  source of marker evidence. This stage must not execute marker ranking.

## Expected Artifacts

- Candidate annotation table keyed by group.
- Evidence table or ledger listing positive, negative, and conflicting markers
  used for each candidate.
- Group-size and optional sample/batch/condition summary used during review.
- Optional label mapping table from original group labels to approved draft
  labels.
- Caveat record for ambiguous, low-confidence, mixed, or unsupported groups.

## Validation Checks

- Confirm the group key exists and every reviewed group has marker evidence or
  an explicit "insufficient evidence" status.
- Confirm marker gene identifiers match the declared species and namespace.
- Confirm marker evidence includes provenance: upstream method or source,
  expression source when relevant, and group sizes.
- Check that candidate labels are not silently written over existing curated
  annotations.
- Check that broad and fine-grained labels are not mixed without an explicit
  granularity decision.
- Flag groups dominated by QC, cell-cycle, mitochondrial, ribosomal, sample,
  batch, or condition signals rather than lineage markers.
- Preserve ambiguous or conflicting evidence instead of forcing a single label.

## Failure Modes

- Marker names from the wrong species or namespace produce false matches.
- Marker ranking output is interpreted as final identity rather than candidate
  evidence.
- A cluster contains multiple biological populations, causing mixed marker
  evidence.
- Low-quality, doublet-like, stressed, or cycling groups mimic meaningful cell
  states.
- Batch, donor, sample, chemistry, or condition structure is mistaken for cell
  identity.
- Reference markers are tissue- or assay-specific and do not transfer cleanly.
- Overly fine labels are assigned from too few or non-specific markers.

## Scientific Caveats

- Annotation support is an inference and review layer. It cannot prove cell type
  identity without suitable marker evidence and biological context.
- A ranked marker list describes differences between declared groups; it is not
  replicate-aware condition-level differential expression.
- Signature scores can support interpretation but do not replace marker review
  or reference evidence.
- Automated labels should be treated as candidates until reviewed and approved.

## Allowed Claims

- "These are candidate annotations for the declared groups, supported by the
  listed markers and reference notes."
- "Ambiguous or conflicting groups were flagged rather than forced into a final
  label."
- "The annotation table records the marker evidence, species namespace, and
  review status used for each candidate."

## Forbidden Claims

- "The labels are final cell type truth without human review."
- "Marker evidence proves treatment response, disease effect, or condition-level
  differential expression."
- "Cluster labels, marker rankings, and annotations are interchangeable."
- "The stage generated new markers, calculated signature scores, or ran a DE
  model unless a separate approved stage did so."
- "A low-confidence or mixed group can be treated as a pure cell type."

## Next Stage Routing

- Route to `13_signature_scoring` when the user wants to score declared marker
  programs or support annotation review with predefined gene sets.
- Route to `11_marker_ranking` when marker evidence is absent, stale, or tied to
  the wrong group key or expression source.
- Route to `14_aggregation_pseudobulk_de` when the question is
  replicate-aware condition-level differential expression within annotated
  groups.
- Route back to clustering or upstream graph review if annotation conflicts
  suggest unstable or confounded groups.
