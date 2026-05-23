---
id: scrna.scverse.package.cellphonedb
kind: package_ref
package: cellphonedb
import_name: cellphonedb
language: python
ecosystem: scverse
docs_local: bioinfo_tutorial/scverse_ecosystem/community/python/cellphonedb
source_urls: [https://cellphonedb.readthedocs.io/en/stable/RESULTS-DOCUMENTATION.html, https://cellphonedb.readthedocs.io/en/stable/cellphonedb.utils.html]
source_version: Read the Docs stable archive; current runtime report marks import missing
source_accessed_at: 2026-05-23
source_local_paths: [bioinfo_tutorial/scverse_ecosystem/community/python/cellphonedb/cellphonedb.readthedocs.io/en/stable/RESULTS-DOCUMENTATION.html, bioinfo_tutorial/scverse_ecosystem/community/python/cellphonedb/cellphonedb.readthedocs.io/en/stable/cellphonedb.utils.html]
distillation_status: distilled
runtime_status: missing
workflow_stages: ["16_specialized_ecosystem"]
install_probe: pending
import_probe: "import cellphonedb"
---
# cellphonedb

## Role In Scverse Workflow

CellphoneDB detects candidate ligand-receptor interactions between annotated
cell groups using a curated interaction database. It is a specialized
cell-cell communication package for post-annotation analysis.

## Supported Stages

- `16_specialized_ecosystem`: run statistical, DEG-driven, scoring, or
  database-query workflows for cell-cell communication hypotheses.

## Required Object State

- Count or normalized expression input accepted by CellphoneDB, preferably an
  `.h5ad` export or compatible matrix.
- Metadata mapping cells to cluster or cell type labels.
- Gene identifiers compatible with the requested `counts-data` namespace, such
  as HGNC symbols.
- Optional microenvironment, DEG, active-TF, or custom database files.

## Produced Object State

- Result files or data frames such as means, p-values, significant means,
  relevant interactions, scores, and deconvoluted complex outputs.
- Database utility outputs for local CellphoneDB database inspection or custom
  input generation.
- Plotting is external to the core result state.

## Major API Families

- Analysis methods: statistical analysis, DEG analysis, and scoring workflows.
- Database utilities: `get_remote_database_versions_html`,
  `generate_input_files.generate_all`, `db_utils.create_db`,
  `get_interactions_genes_complex`.
- Search utilities for genes, complexes, interactions, and result tables.

## Runtime Availability

Status is `missing` in the current repo runtime report:
`ModuleNotFoundError: No module named 'cellphonedb'`. Do not claim installed
package or bundled database availability unless probed.

## Failure Modes

- Gene namespace mismatches can remove ligand or receptor partners.
- Missing or inconsistent metadata breaks cluster-pair construction.
- Database download or custom database creation can fail in restricted
  runtimes.
- Large datasets may require subsampling or long permutation runtimes.

## Scientific Caveats

- Co-expression and curated interaction presence suggest possible interaction,
  not physical contact or active signaling.
- Permutation p-values depend on group sizes and annotation granularity.
- Microenvironment constraints can improve relevance but encode prior
  assumptions.

## When To Avoid

- Avoid before stable cell type labels are available.
- Avoid when gene identifiers cannot be mapped to the CellphoneDB database.
- Avoid causal signaling claims without spatial, perturbation, or protein-level
  evidence.

## Sources Used

- Public docs: `https://cellphonedb.readthedocs.io/en/stable/RESULTS-DOCUMENTATION.html`.
- Public docs: `https://cellphonedb.readthedocs.io/en/stable/cellphonedb.utils.html`.
- Local archive: `bioinfo_tutorial/scverse_ecosystem/community/python/cellphonedb/`.
- Runtime report: `Bioinfo-skills/reports/runtime/scverse_runtime_status.tsv`.
