#!/usr/bin/env python3
"""Validate the Bioinfo-skills scaffold and promoted fill units.

This is a structural/content validator, not a biological execution test. Draft
placeholders are allowed to remain shallow, but any stage marked ``filled`` and
any reference marked ``distilled`` or ``verified`` must be self-contained.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "SPEC/README.md",
    "SPEC/skill_system_core_workflow.md",
    "SPEC/scrna_scverse_skill_system_v0.md",
    "schemas/skill_manifest.schema.json",
    "contracts/anndata_scrna_state_v0.yml",
    "skills/entry/SKILL.md",
    "skills/scrna/SKILL.md",
    "skills/scrna/scverse/SKILL.md",
    "execution/adapters/snakemake/python_rule_template.smk",
    "execution/adapters/snakemake/rscript_rule_template.smk",
    "reports/runtime/README.md",
]

STAGES = [
    "00_state_inspection",
    "01_data_ingest",
    "02_qc_metrics_filtering",
    "03_doublet_detection",
    "04_normalization_transform",
    "05_feature_selection",
    "06_dimensionality_reduction",
    "07_batch_integration",
    "08_neighbor_graph",
    "09_embedding_visualization",
    "10_clustering",
    "11_marker_ranking",
    "12_annotation_support",
    "13_signature_scoring",
    "14_aggregation_pseudobulk_de",
    "15_trajectory_fate_velocity",
    "16_specialized_ecosystem",
]

BACKEND_SYNTAX = [
    r"^\s*rule\s+\w+",
    r"\bSnakefile\b",
    r"\bwildcards\b",
    r"\bsnakemake\.",
    r"^\s*process\s+\w+",
    r"\bchannel\b",
    r"<<\s*[A-Z]+",
]

FILLED_STAGE_SECTIONS = [
    "## Purpose",
    "## When Required",
    "## When Optional",
    "## When Forbidden",
    "## Required Input State",
    "## Produced Output State",
    "## User Decision Points",
    "## Registered Package Refs",
    "## Registered Tool Refs",
    "## Expected Artifacts",
    "## Validation Checks",
    "## Failure Modes",
    "## Allowed Claims",
    "## Forbidden Claims",
    "## Next Stage Routing",
]

DISTILLED_PACKAGE_SECTIONS = [
    "## Role In Scverse Workflow",
    "## Supported Stages",
    "## Required Object State",
    "## Produced Object State",
    "## Major API Families",
    "## Runtime Availability",
    "## Failure Modes",
    "## Scientific Caveats",
    "## When To Avoid",
    "## Sources Used",
]

DISTILLED_TOOL_SECTIONS = [
    "## API Entry Point",
    "## Method Family",
    "## Required Object State",
    "## Output State",
    "## Important Parameters",
    "## Minimal Use",
    "## Validation Checks",
    "## Failure Modes",
    "## Statistical Caveats",
    "## Adapter Notes",
    "## Sources Used",
]

PLACEHOLDER_PHRASES = [
    "To be filled",
    "runtime routing placeholder",
    "authoritative stage definition",
]

DISTILLED_STATUSES = {"distilled", "verified"}


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError(f"{path}: unterminated YAML frontmatter")
    data: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def inline_list(value: str | None) -> list[str]:
    if not value:
        return []
    text = value.strip()
    if text.startswith("[") and text.endswith("]"):
        text = text[1:-1]
    return [part.strip().strip('"').strip("'") for part in text.split(",") if part.strip()]


def require_sections(path: Path, text: str, sections: list[str], errors: list[str]) -> None:
    for section in sections:
        if section not in text:
            errors.append(f"{path}: missing required section {section}")


def reject_placeholder_phrases(path: Path, text: str, errors: list[str]) -> None:
    for phrase in PLACEHOLDER_PHRASES:
        if phrase in text:
            errors.append(f"{path}: contains unresolved placeholder phrase {phrase!r}")


def load_schema_files(errors: list[str]) -> None:
    for path in sorted((ROOT / "schemas").glob("*.schema.json")):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{path}: invalid JSON schema: {exc}")


def collect_ref_ids(kind: str) -> set[str]:
    if kind == "package":
        paths = (ROOT / "skills/scrna/scverse/refs/packages").glob("*.md")
    elif kind == "tool":
        paths = (ROOT / "skills/scrna/scverse/refs/tools").glob("**/*.md")
    else:
        raise ValueError(kind)
    ids: set[str] = set()
    for path in paths:
        if path.name == "README.md":
            continue
        try:
            meta = frontmatter(path)
        except ValueError:
            continue
        if "id" in meta:
            ids.add(meta["id"])
    return ids


def validate() -> list[str]:
    errors: list[str] = []
    load_schema_files(errors)
    package_ids = collect_ref_ids("package")
    tool_ids = collect_ref_ids("tool")

    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            errors.append(f"missing required file: {rel}")

    for stage in STAGES:
        skill = ROOT / f"skills/scrna/scverse/workflow/{stage}/SKILL.md"
        if not skill.exists():
            errors.append(f"missing stage skill: {stage}")
            continue
        try:
            meta = frontmatter(skill)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        for key in ["id", "schema_version", "kind", "domain", "stage", "status"]:
            if key not in meta:
                errors.append(f"{skill}: missing frontmatter key {key}")
        body = skill.read_text(encoding="utf-8")
        for pattern in BACKEND_SYNTAX:
            if re.search(pattern, body, flags=re.MULTILINE):
                errors.append(f"{skill}: contains backend syntax matching {pattern}")
        if meta.get("status") == "filled":
            require_sections(skill, body, FILLED_STAGE_SECTIONS, errors)
            reject_placeholder_phrases(skill, body, errors)
            refs = inline_list(meta.get("registered_refs"))
            if not refs:
                errors.append(f"{skill}: filled stage must declare registered_refs")
            for ref_id in refs:
                if ref_id.startswith("scrna.scverse.package.") and ref_id not in package_ids:
                    errors.append(f"{skill}: registered package ref not found: {ref_id}")
                if ref_id.startswith("scrna.scverse.tool.") and ref_id not in tool_ids:
                    errors.append(f"{skill}: registered tool ref not found: {ref_id}")

    for ref in sorted((ROOT / "skills/scrna/scverse/refs/packages").glob("*.md")):
        if ref.name == "README.md":
            continue
        try:
            meta = frontmatter(ref)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        for key in ["id", "kind", "package", "language", "ecosystem", "runtime_status"]:
            if key not in meta:
                errors.append(f"{ref}: missing frontmatter key {key}")
        if meta.get("distillation_status") in DISTILLED_STATUSES:
            for key in ["source_urls", "source_version", "source_accessed_at", "distillation_status"]:
                if key not in meta:
                    errors.append(f"{ref}: distilled package ref missing frontmatter key {key}")
            body = ref.read_text(encoding="utf-8")
            require_sections(ref, body, DISTILLED_PACKAGE_SECTIONS, errors)
            reject_placeholder_phrases(ref, body, errors)

    for ref in sorted((ROOT / "skills/scrna/scverse/refs/tools").glob("**/*.md")):
        if ref.name == "README.md":
            continue
        try:
            meta = frontmatter(ref)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        for key in ["id", "kind", "package_ref", "api_entrypoint", "method_family"]:
            if key not in meta:
                errors.append(f"{ref}: missing frontmatter key {key}")
        if meta.get("package_ref") and meta["package_ref"] not in package_ids:
            errors.append(f"{ref}: package_ref not found: {meta['package_ref']}")
        if meta.get("distillation_status") in DISTILLED_STATUSES:
            for key in ["source_urls", "source_version", "source_accessed_at", "distillation_status"]:
                if key not in meta:
                    errors.append(f"{ref}: distilled tool ref missing frontmatter key {key}")
            body = ref.read_text(encoding="utf-8")
            require_sections(ref, body, DISTILLED_TOOL_SECTIONS, errors)
            reject_placeholder_phrases(ref, body, errors)

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("skill tree validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
