# Layer Slot Policy

Status: draft

`adata.X` is the current working matrix and must never be assumed to contain raw
counts unless a state inspection report says so.

## Conventions

- `adata.layers["counts"]`: raw UMI counts when available.
- `adata.layers["log1p_norm"]`: log-normalized expression.
- `adata.raw`: optional frozen reference. Its use must be declared.
- method wrappers must record which source they consume: `.X`, `.raw`, or a
  named layer.

## Guardrails

- Preserve raw counts before overwriting `.X`.
- Do not run `log1p` twice.
- Do not use log-normalized means for count-based DE models.
- Do not silently fall back from a missing layer to `.X`.

