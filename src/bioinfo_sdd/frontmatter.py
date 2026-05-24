"""YAML frontmatter parsing for repo-local skills and refs."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def split_frontmatter(text: str, path: Path | None = None) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        label = str(path) if path else "document"
        raise ValueError(f"{label}: missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        label = str(path) if path else "document"
        raise ValueError(f"{label}: unterminated YAML frontmatter")
    meta = yaml.safe_load(text[4:end]) or {}
    if not isinstance(meta, dict):
        label = str(path) if path else "document"
        raise ValueError(f"{label}: frontmatter must be a mapping")
    return meta, text[end + 5 :]


def read_frontmatter(path: Path) -> dict[str, Any]:
    meta, _body = split_frontmatter(path.read_text(encoding="utf-8"), path=path)
    return meta
