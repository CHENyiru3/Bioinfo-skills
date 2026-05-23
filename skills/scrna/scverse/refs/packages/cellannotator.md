---
id: scrna.scverse.package.cellannotator
kind: package_ref
package: cellannotator
import_name: cellannotator
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/community/python/cellannotator
source_url: https://cell-annotator.readthedocs.io/en/stable/
source_urls: [https://cell-annotator.readthedocs.io/en/stable/, https://cell-annotator.readthedocs.io/en/stable/generated/cell_annotator.CellAnnotator.html, https://cell-annotator.readthedocs.io/en/latest/api.html]
source_version: cell-annotator stable and latest public docs; runtime report records package missing
source_accessed_at: 2026-05-23
distillation_status: distilled
runtime_status: missing
workflow_stages: ["16_specialized_ecosystem"]
install_probe: pending
import_probe: "import cellannotator"
---
# cellannotator

## Role In Scverse Workflow

CellAnnotator supports LLM-assisted cluster annotation from marker genes in
AnnData. In this skill system it is an annotation-support candidate whose
outputs require expert review.

## Supported Stages

- `16_specialized_ecosystem`: LLM-assisted label suggestion and annotation
  triage after marker ranking and cluster metadata exist.

## Required Object State

- AnnData with cell-level observations and a cluster column such as
  `.obs["leiden"]`.
- Species, tissue, and developmental stage supplied by the user.
- Marker gene evidence per cluster or permission to compute markers.
- Valid model/provider configuration and API key if execution is approved.

## Produced Object State

- Suggested cluster annotations in `.obs[key_added]`.
- Annotation tables and prompt or response records if wrapper provenance is
  implemented.
- API-access diagnostics and optional expected marker lists.

## Major API Families

- `cell_annotator.CellAnnotator`: orchestrates sample and cluster annotation.
- Marker support: `get_cluster_markers`, `get_expected_cell_type_markers`.
- LLM support: `query_llm`, `check_api_access`, `list_available_models`.
- Annotation: `annotate_clusters`.

## Runtime Availability

Status: `missing`. The recorded runtime report shows `ModuleNotFoundError` for
`import cellannotator`; use this ref for planning only until the environment is
updated.

## Failure Modes

- Missing cluster key or weak marker signal.
- Provider credentials, rate limits, model availability, or network failures.
- Hallucinated labels or labels outside the tissue and species context.
- Non-reproducible outputs if prompts, model, and response metadata are not
  recorded.

## Scientific Caveats

- LLM output is a suggestion, not an authoritative cell type assignment.
- Marker-based annotation is limited by marker specificity, dropout, and
  cluster quality.
- Sample-specific or rare states require domain review and external evidence.

## When To Avoid

- Avoid as the sole source of final annotations.
- Avoid when species, tissue, or cluster evidence is uncertain.
- Avoid sending sensitive data or unpublished context to external providers
  without approval.

## Sources Used

- Public docs: `https://cell-annotator.readthedocs.io/en/stable/`.
- Public API docs: `https://cell-annotator.readthedocs.io/en/stable/generated/cell_annotator.CellAnnotator.html`.
- Latest API index: `https://cell-annotator.readthedocs.io/en/latest/api.html`.
- Runtime report: `reports/runtime/scverse_runtime_status.tsv`.
