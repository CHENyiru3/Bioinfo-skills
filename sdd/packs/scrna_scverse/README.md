# scRNA scverse Capability Pack

This local capability pack exposes the repository's scRNA/scverse stage skills,
task templates, workflow profile, and deterministic checks to the generic
`bioinfo_sdd` engine.

Concrete package/tool refs are selected from `tool_market/` and copied into a
section-local installed-ref revision. The pack is file-backed and reviewable. It
does not install dependencies or load arbitrary code; it resolves stable task
and workflow IDs to repository paths and approved check IDs.
