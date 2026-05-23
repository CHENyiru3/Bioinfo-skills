---
id: entry
schema_version: "0.1.0"
kind: skill
domain: general
stage: routing
status: draft
state_in: [user_request]
state_out: [classified_request]
registered_refs: []
validation: [route_to_domain_skill]
---
# Entry Skill

Classify the user's request, identify domain, input state, intended result, missing decisions, and route to the narrowest relevant skill. If the biological/data state is unknown, route to state inspection before method selection.

Do not choose an execution backend until the task, method, parameters, and artifacts are approved.
