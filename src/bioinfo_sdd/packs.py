"""File-backed capability pack manifests."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .io import read_yaml


REQUIRED_PACK_KEYS = [
    "schema_version",
    "pack_id",
    "name",
    "domain",
    "ecosystems",
    "workflows",
    "task_templates",
    "checks",
]


@dataclass(frozen=True)
class CapabilityPack:
    path: Path
    data: dict[str, Any]

    @property
    def pack_id(self) -> str:
        return str(self.data["pack_id"])

    @property
    def root(self) -> Path:
        return self.path.parents[3]

    def workflows(self) -> dict[str, str]:
        return dict(self.data.get("workflows") or {})

    def task_templates(self) -> dict[str, dict[str, Any]]:
        return dict(self.data.get("task_templates") or {})

    def checks(self) -> list[str]:
        checks = self.data.get("checks") or []
        if isinstance(checks, dict):
            return list(checks)
        return list(checks)


def load_pack(path: Path) -> CapabilityPack:
    return CapabilityPack(path=path, data=read_yaml(path))


def discover_packs(root: Path) -> dict[str, CapabilityPack]:
    packs: dict[str, CapabilityPack] = {}
    for path in sorted((root / "sdd" / "packs").glob("*/pack.yml")):
        pack = load_pack(path)
        packs[pack.pack_id] = pack
    return packs


def validate_pack_data(data: dict[str, Any], root: Path | None = None) -> list[str]:
    errors: list[str] = []
    for key in REQUIRED_PACK_KEYS:
        if key not in data:
            errors.append(f"pack.yml: missing required key {key}")
    if errors:
        return errors

    if not isinstance(data.get("pack_id"), str) or not data["pack_id"]:
        errors.append("pack.yml: pack_id must be a non-empty string")
    if not isinstance(data.get("ecosystems"), list):
        errors.append("pack.yml: ecosystems must be a list")
    for key in ["workflows", "task_templates"]:
        if not isinstance(data.get(key), dict):
            errors.append(f"pack.yml: {key} must be a mapping")
    checks = data.get("checks")
    if not isinstance(checks, (list, dict)):
        errors.append("pack.yml: checks must be a list or mapping")

    if root is not None and isinstance(data.get("workflows"), dict):
        for workflow_id, rel in data["workflows"].items():
            if not isinstance(rel, str):
                errors.append(f"pack.yml: workflow {workflow_id} must map to a path string")
                continue
            if not (root / rel).exists():
                errors.append(f"pack.yml: workflow {workflow_id} path does not exist: {rel}")

    if root is not None and isinstance(data.get("task_templates"), dict):
        for task_id, task in data["task_templates"].items():
            if not isinstance(task, dict):
                errors.append(f"pack.yml: task {task_id} must be a mapping")
                continue
            for key in ["stages", "skills", "tool_slots", "checks"]:
                if key in task and not isinstance(task[key], list):
                    errors.append(f"pack.yml: task {task_id}.{key} must be a list")
            for slot in task.get("tool_slots", []):
                if not isinstance(slot, dict):
                    errors.append(f"pack.yml: task {task_id}.tool_slots entries must be mappings")
                    continue
                for key in ["slot_id", "stage_id", "method_family"]:
                    if key not in slot:
                        errors.append(f"pack.yml: task {task_id}.tool_slots entry missing {key}")
            for key in ["default_wrapper", "default_adapter"]:
                rel = task.get(key)
                if rel and not (root / rel).exists():
                    errors.append(f"pack.yml: task {task_id}.{key} path does not exist: {rel}")
    return errors


def validate_pack_file(path: Path, root: Path | None = None) -> list[str]:
    try:
        pack = load_pack(path)
    except Exception as exc:
        return [str(exc)]
    return validate_pack_data(pack.data, root=root)


def resolve_workflow(root: Path, pack_ids: list[str], workflow_ref: str) -> Path:
    packs = discover_packs(root)
    for pack_id in pack_ids:
        pack = packs.get(pack_id)
        if not pack:
            continue
        rel = pack.workflows().get(workflow_ref)
        if rel:
            return root / rel
    fallback = root / workflow_ref
    if fallback.exists():
        return fallback
    raise KeyError(f"workflow_ref not found in declared packs: {workflow_ref}")


def task_templates_for_section(root: Path, pack_ids: list[str], task_refs: list[str]) -> dict[str, dict[str, Any]]:
    packs = discover_packs(root)
    resolved: dict[str, dict[str, Any]] = {}
    for task_ref in task_refs:
        for pack_id in pack_ids:
            pack = packs.get(pack_id)
            if pack and task_ref in pack.task_templates():
                resolved[task_ref] = pack.task_templates()[task_ref]
                break
    return resolved
