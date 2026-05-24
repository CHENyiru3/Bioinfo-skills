# Design Principles

Status: draft

The Bioinfo-skills system is a backend-neutral skill and reference layer for
building bioinformatics workflows one approved task at a time.

## Principles

- Keep biological task reasoning independent from execution backends.
- Treat `SKILL.md` files as routing and decision guidance, not API dumps.
- Keep concrete package and function knowledge in references.
- Represent scRNA analysis through explicit AnnData state transitions.
- Record statistical limits where a method is selected, not only after results.
- Prefer small, reviewable workflow sections over one-shot workflow generation.
- Require human approval before irreversible filtering, labeling, or inference
  claims.
- Make generated evidence durable through reports, manifests, and provenance.

## Non-Goals

- No workflow compiler in v0.
- No hidden preprocessing inside downstream tools.
- No final biological interpretation without evidence and review.
- No backend-specific syntax in task nodes.

