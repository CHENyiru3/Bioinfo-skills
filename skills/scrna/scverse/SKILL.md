---
id: scrna.scverse
schema_version: "0.1.0"
kind: skill
domain: scrna
stage: scverse_routing
status: draft
state_in: [scrna_request]
state_out: [workflow_stage_route]
registered_refs: []
validation: [confirm_anndata_state]
---
# scverse Skill

Route scverse/AnnData tasks through the state-gated workflow stages. Task nodes are backend-neutral; package/tool references and execution adapters are loaded only when needed.
