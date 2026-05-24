"""Catalog lookups for repo-local skills, stages, package refs, and tool refs."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .frontmatter import read_frontmatter
from .installed_refs import active_ref_paths
from .packs import discover_packs


@dataclass(frozen=True)
class CatalogEntry:
    id: str
    path: Path
    metadata: dict[str, Any]


def _collect_patterns(root: Path, patterns: list[str]) -> dict[str, CatalogEntry]:
    entries: dict[str, CatalogEntry] = {}
    for pattern in patterns:
        for path in sorted(root.glob(pattern)):
            if path.name == "README.md":
                continue
            try:
                metadata = read_frontmatter(path)
            except ValueError:
                continue
            entry_id = metadata.get("id")
            if isinstance(entry_id, str) and entry_id:
                entries[entry_id] = CatalogEntry(entry_id, path, metadata)
    return entries


def _collect(root: Path, pattern: str) -> dict[str, CatalogEntry]:
    return _collect_patterns(root, [pattern])


def _pack_catalog_patterns(root: Path, pack_ids: list[str] | None, catalog_key: str, fallback: str) -> list[str]:
    if not pack_ids:
        return [fallback]
    packs = discover_packs(root)
    patterns: list[str] = []
    for pack_id in pack_ids:
        pack = packs.get(pack_id)
        if not pack:
            continue
        catalogs = pack.data.get("catalogs") or {}
        values = catalogs.get(catalog_key) or []
        if isinstance(values, str):
            values = [values]
        patterns.extend(str(value) for value in values)
    return patterns or [fallback]


def stage_skills(root: Path, pack_ids: list[str] | None = None) -> dict[str, CatalogEntry]:
    patterns = _pack_catalog_patterns(root, pack_ids, "stage_skills", "skills/scrna/scverse/workflow/*/SKILL.md")
    return _collect_patterns(root, patterns)


def _collect_paths(paths: list[Path]) -> dict[str, CatalogEntry]:
    entries: dict[str, CatalogEntry] = {}
    for path in paths:
        try:
            metadata = read_frontmatter(path)
        except ValueError:
            continue
        entry_id = metadata.get("id")
        if isinstance(entry_id, str) and entry_id:
            entries[entry_id] = CatalogEntry(entry_id, path, metadata)
    return entries


def package_refs(
    root: Path,
    pack_ids: list[str] | None = None,
    section_dir: Path | None = None,
) -> dict[str, CatalogEntry]:
    if section_dir is not None:
        return _collect_paths(active_ref_paths(section_dir, "package"))
    patterns = _pack_catalog_patterns(root, pack_ids, "package_refs", "tool_market/packages/**/*.md")
    return _collect_patterns(root, patterns)


def tool_refs(
    root: Path,
    pack_ids: list[str] | None = None,
    section_dir: Path | None = None,
) -> dict[str, CatalogEntry]:
    if section_dir is not None:
        return _collect_paths(active_ref_paths(section_dir, "tool"))
    patterns = _pack_catalog_patterns(root, pack_ids, "tool_refs", "tool_market/tools/**/*.md")
    return _collect_patterns(root, patterns)


def skill_refs(root: Path, pack_ids: list[str] | None = None) -> dict[str, CatalogEntry]:
    entries = stage_skills(root, pack_ids)
    entries.update(_collect(root, "skills/**/SKILL.md"))
    return entries
