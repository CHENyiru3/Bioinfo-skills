# Required scRNA Metadata

Status: draft

Minimum metadata depends on the task.

## Always Useful

- organism
- assay/modality
- feature namespace
- sample or library identifier

## Required By Stage

- QC: organism-specific mitochondrial/ribosomal/hemoglobin feature masks.
- Integration: `batch` or equivalent technical covariate.
- Pseudobulk DE: `sample_id`, `condition`, optional covariates, and raw counts.
- Annotation: species, gene namespace, marker source or reference source.
- Trajectory/velocity: root/time/terminal-state decision points and velocity
  layers where applicable.

