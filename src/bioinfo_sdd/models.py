"""Models and validation for section artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .io import read_yaml


REQUIRED_SECTION_KEYS = [
    "schema_version",
    "section_id",
    "domain",
    "ecosystem",
    "pack_refs",
    "workflow_ref",
    "stage_ids",
    "task_refs",
    "input_state",
    "output_state",
    "skill_refs",
    "package_refs",
    "tool_refs",
    "check_refs",
    "wrapper",
    "adapter",
    "parameters",
    "claims",
    "expected_artifacts",
    "gates",
]

REQUIRED_GATES = [
    "spec_review",
    "plan_review",
    "task_review",
    "evidence_acceptance",
]

GATE_STATUSES = {"pending", "approved", "rejected"}


@dataclass(frozen=True)
class Section:
    path: Path
    data: dict[str, Any]

    @property
    def section_dir(self) -> Path:
        return self.path.parent

    @property
    def section_id(self) -> str:
        return str(self.data["section_id"])

    @property
    def gates(self) -> dict[str, str]:
        return dict(self.data.get("gates") or {})

    @property
    def wrapper_path(self) -> str | None:
        wrapper = self.data.get("wrapper")
        return str(wrapper) if wrapper else None

    @property
    def adapter_path(self) -> str | None:
        adapter = self.data.get("adapter")
        return str(adapter) if adapter else None


def load_section(path_or_dir: Path) -> Section:
    path = path_or_dir / "section.yml" if path_or_dir.is_dir() else path_or_dir
    return Section(path=path, data=read_yaml(path))


def validate_section_data(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key in REQUIRED_SECTION_KEYS:
        if key not in data:
            errors.append(f"section.yml: missing required key {key}")

    if not errors:
        for key in [
            "stage_ids",
            "pack_refs",
            "task_refs",
            "input_state",
            "output_state",
            "skill_refs",
            "package_refs",
            "tool_refs",
            "check_refs",
            "expected_artifacts",
        ]:
            if not isinstance(data.get(key), list):
                errors.append(f"section.yml: {key} must be a list")
        if not isinstance(data.get("workflow_ref"), str) or not data.get("workflow_ref"):
            errors.append("section.yml: workflow_ref must be a non-empty string")
        if not isinstance(data.get("parameters"), dict):
            errors.append("section.yml: parameters must be a mapping")
        claims = data.get("claims")
        if not isinstance(claims, dict):
            errors.append("section.yml: claims must be a mapping")
        else:
            for key in ["allowed", "forbidden"]:
                if not isinstance(claims.get(key), list):
                    errors.append(f"section.yml: claims.{key} must be a list")
        gates = data.get("gates")
        if not isinstance(gates, dict):
            errors.append("section.yml: gates must be a mapping")
        else:
            for gate in REQUIRED_GATES:
                if gate not in gates:
                    errors.append(f"section.yml: missing gate {gate}")
                elif gates[gate] not in GATE_STATUSES:
                    errors.append(f"section.yml: gate {gate} has invalid status {gates[gate]!r}")

    section_id = data.get("section_id")
    if section_id is not None and (not isinstance(section_id, str) or not section_id.strip()):
        errors.append("section.yml: section_id must be a non-empty string")
    return errors


def validate_section_file(path_or_dir: Path) -> list[str]:
    try:
        section = load_section(path_or_dir)
    except Exception as exc:
        return [str(exc)]
    return validate_section_data(section.data)
