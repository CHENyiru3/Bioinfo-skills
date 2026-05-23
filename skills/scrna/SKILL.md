---
id: scrna
schema_version: "0.1.0"
kind: skill
domain: scrna
stage: domain_routing
status: draft
state_in: [classified_scrna_request]
state_out: [ecosystem_route]
registered_refs: []
validation: [confirm_modality_and_input_state]
---
# scRNA Skill

Route single-cell RNA requests to scverse, Seurat, or interoperability skills. Require explicit input state and biological goal before selecting tools.
