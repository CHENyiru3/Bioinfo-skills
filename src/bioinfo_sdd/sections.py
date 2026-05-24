"""Section artifact helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .io import read_yaml, write_yaml
from .models import GATE_STATUSES, REQUIRED_GATES, load_section, validate_section_file


def resolve_section_dir(root: Path, section: str | Path) -> Path:
    path = Path(section)
    if path.exists():
        return path if path.is_dir() else path.parent
    return root / "sdd" / "sections" / str(section)


def load_gates(section_dir: Path) -> dict[str, Any]:
    gates_path = section_dir / "gates.yml"
    if gates_path.exists():
        return read_yaml(gates_path)
    section = load_section(section_dir)
    return {"schema_version": section.data.get("schema_version", "0.1.0"), "gates": section.gates}


def gate_status(section_dir: Path, gate: str) -> str:
    gates_doc = load_gates(section_dir)
    gate_data = (gates_doc.get("gates") or {}).get(gate)
    if isinstance(gate_data, dict):
        return str(gate_data.get("status", "pending"))
    if isinstance(gate_data, str):
        return gate_data
    section = load_section(section_dir)
    return section.gates.get(gate, "pending")


def update_gate(section_dir: Path, gate: str, status: str, reason: str | None = None) -> None:
    if gate not in REQUIRED_GATES:
        raise ValueError(f"unknown gate: {gate}")
    if status not in GATE_STATUSES:
        raise ValueError(f"invalid gate status: {status}")

    section = load_section(section_dir)
    section.data.setdefault("gates", {})[gate] = status
    write_yaml(section.path, section.data)

    gates_path = section_dir / "gates.yml"
    gates_doc = load_gates(section_dir)
    gates_doc.setdefault("schema_version", section.data.get("schema_version", "0.1.0"))
    gates_doc.setdefault("section_id", section.section_id)
    gates = gates_doc.setdefault("gates", {})
    current = gates.get(gate)
    if not isinstance(current, dict):
        current = {}
    current["status"] = status
    if reason:
        current["reason"] = reason
    gates[gate] = current
    write_yaml(gates_path, gates_doc)

    errors = validate_section_file(section_dir)
    if errors:
        raise ValueError("\n".join(errors))
