# Routing Policy

Status: draft

This policy defines how the entry skill should route user requests through the
skill tree.

## Routing Order

1. Identify the biological domain.
2. Identify input object state.
3. Identify intended output or decision.
4. Route to the narrowest applicable workflow-stage skill.
5. Load package/tool references only after the stage and candidate method are
   clear.
6. Select an execution adapter only after method, parameters, and expected
   artifacts are approved.

## Required Classifications

- domain: `scrna`, `spatial`, `bulk_rna`, or other future domain
- ecosystem: `scverse`, `seurat`, `interoperability`, or mixed
- state: raw counts, QC-ready, analysis-ready, clustered, annotated,
  pseudobulk-ready, trajectory-ready, or unknown
- task: inspect, ingest, QC, normalize, integrate, cluster, rank markers,
  annotate, score signatures, test pseudobulk DE, trajectory/fate/velocity, or
  specialized ecosystem task

## Guardrails

- If state is unknown, route to state inspection.
- If the user asks for condition-level DE, route away from marker ranking and
  require pseudobulk/replicate metadata.
- If a task would mutate data, require an explicit approval checkpoint.
- If a backend is requested before the biological method is clear, defer backend
  binding until method selection is complete.

