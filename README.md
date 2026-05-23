# Bioinfo-skills

Bioinfo-skills is a backend-neutral skill and reference layer for building
bioinformatics workflows one approved section at a time.

The current v0 focus is a scRNA/scverse skill system centered on explicit
AnnData state transitions. Biological task nodes, package/tool references, and
execution adapters are separate layers.

## Layout

- `SPEC/`: architecture and planning documents.
- `skills/`: user-intent routing, scRNA/scverse workflow stages, and placeholder
  Seurat/interoperability skills.
- `contracts/`: AnnData/scRNA state and statistical validity policies.
- `schemas/`: JSON Schemas for skill/reference/provenance/runtime structures.
- `execution/`: backend adapter templates, with Snakemake first.
- `envs/`: portable environment specifications.
- `containers/`: container and lockfile templates.
- `provenance/`: run, decision, artifact, and version templates.
- `scripts/`: structural validators and runtime probes.
- `wrappers/`: approved executable units, starting with read-only AnnData state
  inspection.
- `reports/`: generated evidence such as runtime status.
- `tests/`: structural tests and fixture manifests.

## Current Status

The repository contains the scaffold, validators, distilled state-inspection
refs, and a read-only AnnData inspection wrapper. It does not yet contain
biological transformation wrappers, executable analysis rules, or binary test
fixtures.
