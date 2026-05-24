"""Section-local installed tool ref revisions."""

from __future__ import annotations

import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .io import read_yaml, write_yaml
from .market import ToolBundle, load_bundle, sha256_file
from .models import load_section


def installed_refs_dir(section_dir: Path) -> Path:
    return section_dir / "installed_refs"


def selection_path(section_dir: Path) -> Path:
    return installed_refs_dir(section_dir) / "selection.yml"


def load_selection(section_dir: Path) -> dict[str, Any]:
    path = selection_path(section_dir)
    if not path.exists():
        section = load_section(section_dir)
        return {
            "schema_version": "0.1.0",
            "section_id": section.section_id,
            "active_revision": None,
            "active_bundles": [],
            "revisions": [],
        }
    return read_yaml(path)


def active_manifest(section_dir: Path) -> dict[str, Any] | None:
    selection = load_selection(section_dir)
    revision = selection.get("active_revision")
    if not revision:
        return None
    path = installed_refs_dir(section_dir) / "revisions" / str(revision) / "manifest.yml"
    if not path.exists():
        return None
    return read_yaml(path)


def active_ref_paths(section_dir: Path, kind: str) -> list[Path]:
    manifest = active_manifest(section_dir)
    if not manifest:
        return []
    key = "packages" if kind == "package" else "tools"
    paths = []
    for row in manifest.get(key, []):
        rel = row.get("installed_path")
        if rel:
            paths.append(section_dir / rel)
    return paths


def install_tool_bundle(root: Path, section_dir: Path, bundle_id: str, *, append: bool = True) -> dict[str, Any]:
    bundle_ids = list(load_selection(section_dir).get("active_bundles") or []) if append else []
    if bundle_id not in bundle_ids:
        bundle_ids.append(bundle_id)
    return _write_revision(root, section_dir, bundle_ids)


def replace_tool_bundle(root: Path, section_dir: Path, bundle_id: str) -> dict[str, Any]:
    return _write_revision(root, section_dir, [bundle_id])


def uninstall_tool_bundle(root: Path, section_dir: Path, bundle_id: str) -> dict[str, Any]:
    selection = load_selection(section_dir)
    active_bundles = [bundle for bundle in selection.get("active_bundles", []) if bundle != bundle_id]
    if active_bundles:
        return _write_revision(root, section_dir, active_bundles)
    selection["active_bundles"] = active_bundles
    selection["active_revision"] = None
    write_yaml(selection_path(section_dir), selection)
    _update_section_from_manifest(section_dir, None)
    return selection


def _write_revision(root: Path, section_dir: Path, bundle_ids: list[str]) -> dict[str, Any]:
    bundles = [load_bundle(root, bundle_id) for bundle_id in bundle_ids]
    revision_id = _next_revision_id(section_dir)
    revision_dir = installed_refs_dir(section_dir) / "revisions" / revision_id
    packages_dir = revision_dir / "packages"
    tools_dir = revision_dir / "tools"
    packages_dir.mkdir(parents=True, exist_ok=True)
    tools_dir.mkdir(parents=True, exist_ok=True)

    package_rows = _copy_refs(root, section_dir, revision_dir, packages_dir, bundles, "package_refs")
    tool_rows = _copy_refs(root, section_dir, revision_dir, tools_dir, bundles, "tool_refs")
    wrappers = sorted({str(bundle.data.get("wrapper")) for bundle in bundles if bundle.data.get("wrapper")})
    adapters = sorted({str(bundle.data.get("adapter")) for bundle in bundles if bundle.data.get("adapter")})
    if len(wrappers) > 1 or len(adapters) > 1:
        raise ValueError("v1 installed refs support one wrapper and one adapter per active section revision")

    manifest = {
        "schema_version": "0.1.0",
        "revision_id": revision_id,
        "section_id": load_section(section_dir).section_id,
        "installed_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "source_bundles": bundle_ids,
        "task_refs": _unique(bundle.data.get("task_refs", []) for bundle in bundles),
        "stage_ids": _unique(bundle.data.get("stage_ids", []) for bundle in bundles),
        "skill_refs": _unique(bundle.data.get("skill_refs", []) for bundle in bundles),
        "package_refs": [row["id"] for row in package_rows],
        "tool_refs": [row["id"] for row in tool_rows],
        "packages": package_rows,
        "tools": tool_rows,
        "wrapper": wrappers[0] if wrappers else None,
        "adapter": adapters[0] if adapters else None,
        "check_refs": _unique(bundle.data.get("check_refs", []) for bundle in bundles),
    }
    write_yaml(revision_dir / "manifest.yml", manifest)
    _write_selection(section_dir, revision_id, bundle_ids)
    _update_section_from_manifest(section_dir, manifest)
    return manifest


def _copy_refs(
    root: Path,
    section_dir: Path,
    revision_dir: Path,
    destination_dir: Path,
    bundles: list[ToolBundle],
    key: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for bundle in bundles:
        for ref in bundle.data.get(key, []):
            ref_id = str(ref["id"])
            if ref_id in seen:
                continue
            seen.add(ref_id)
            source = root / str(ref["path"])
            destination = destination_dir / source.name
            shutil.copy2(source, destination)
            rows.append(
                {
                    "id": ref_id,
                    "source_path": str(source.relative_to(root)),
                    "installed_path": str(destination.relative_to(section_dir)),
                    "sha256": sha256_file(destination),
                    **{k: v for k, v in ref.items() if k not in {"id", "path"}},
                }
            )
    return rows


def _write_selection(section_dir: Path, revision_id: str, bundle_ids: list[str]) -> None:
    selection = load_selection(section_dir)
    revisions = list(selection.get("revisions") or [])
    if revision_id not in revisions:
        revisions.append(revision_id)
    selection.update(
        {
            "active_revision": revision_id,
            "active_bundles": bundle_ids,
            "revisions": revisions,
        }
    )
    write_yaml(selection_path(section_dir), selection)


def _update_section_from_manifest(section_dir: Path, manifest: dict[str, Any] | None) -> None:
    section = load_section(section_dir)
    if manifest is None:
        section.data.update({"package_refs": [], "tool_refs": [], "check_refs": [], "wrapper": None, "adapter": None})
    else:
        for key in ["stage_ids", "skill_refs", "package_refs", "tool_refs", "check_refs"]:
            section.data[key] = list(manifest.get(key) or [])
        section.data["wrapper"] = manifest.get("wrapper")
        section.data["adapter"] = manifest.get("adapter")
    write_yaml(section.path, section.data)


def _next_revision_id(section_dir: Path) -> str:
    base = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    revisions_dir = installed_refs_dir(section_dir) / "revisions"
    candidate = base
    counter = 2
    while (revisions_dir / candidate).exists():
        candidate = f"{base}-{counter}"
        counter += 1
    return candidate


def _unique(groups: Any) -> list[str]:
    seen: set[str] = set()
    values: list[str] = []
    for group in groups:
        for value in group or []:
            text = str(value)
            if text not in seen:
                seen.add(text)
                values.append(text)
    return values
