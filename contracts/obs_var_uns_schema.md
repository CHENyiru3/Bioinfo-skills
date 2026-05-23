# Obs, Var, And Uns Schema Policy

Status: draft

This policy defines common single-cell metadata conventions.

## `.obs`

- `sample_id`: biological replicate or sample. Required for pseudobulk DE.
- `batch`: technical batch. Required before batch integration.
- `condition`: experimental condition. Required for condition-level inference.
- `leiden` or declared `cluster_key`: clustering result.
- annotation columns must distinguish candidate labels from final labels.

## `.var`

- gene identifiers and symbols should be explicitly declared.
- HVG masks should be keyed and provenance-recorded.

## `.uns`

- `neighbors`: graph metadata.
- method outputs should use declared keys.
- `bioinfo_skills`: provenance, parameter decisions, and caveats.

