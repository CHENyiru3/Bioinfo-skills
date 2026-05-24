"""Template rendering for section artifacts."""

from __future__ import annotations

from pathlib import Path
from string import Template
from typing import Any

from .models import validate_section_file


DEFAULT_TEMPLATE_FILES = [
    "section.yml",
    "spec.md",
    "plan.md",
    "tasks.md",
    "evidence.md",
    "gates.yml",
]


def render_text(text: str, values: dict[str, Any]) -> str:
    normalized = {key: str(value) for key, value in values.items()}
    return Template(text).safe_substitute(normalized)


def create_section_from_templates(
    section_id: str,
    sections_root: Path,
    template_dir: Path,
    values: dict[str, Any] | None = None,
    *,
    force: bool = False,
) -> Path:
    context = {
        "section_id": section_id,
        "domain": "scrna",
        "ecosystem": "scverse",
    }
    if values:
        context.update(values)
    target = sections_root / section_id
    target.mkdir(parents=True, exist_ok=True)
    for name in DEFAULT_TEMPLATE_FILES:
        source = template_dir / name
        destination = target / name
        if destination.exists() and not force:
            continue
        destination.write_text(render_text(source.read_text(encoding="utf-8"), context), encoding="utf-8")
    errors = validate_section_file(target)
    if errors:
        raise ValueError("\n".join(errors))
    return target
