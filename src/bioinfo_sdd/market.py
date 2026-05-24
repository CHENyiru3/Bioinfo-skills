"""Repo-local inactive tool market support."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .io import read_yaml


REQUIRED_MARKET_KEYS = ["schema_version", "market_id", "bundles"]
REQUIRED_BUNDLE_KEYS = [
    "schema_version",
    "bundle_id",
    "domain",
    "ecosystem",
    "task_refs",
    "stage_ids",
    "package_refs",
    "tool_refs",
    "wrapper",
    "adapter",
    "check_refs",
]


@dataclass(frozen=True)
class ToolBundle:
    path: Path
    data: dict[str, Any]

    @property
    def bundle_id(self) -> str:
        return str(self.data["bundle_id"])

    @property
    def task_refs(self) -> list[str]:
        return list(self.data.get("task_refs") or [])

    @property
    def package_refs(self) -> list[dict[str, Any]]:
        return list(self.data.get("package_refs") or [])

    @property
    def tool_refs(self) -> list[dict[str, Any]]:
        return list(self.data.get("tool_refs") or [])


def market_path(root: Path) -> Path:
    return root / "tool_market" / "market.yml"


def load_market(root: Path) -> dict[str, Any]:
    return read_yaml(market_path(root))


def load_bundle(root: Path, bundle_id: str) -> ToolBundle:
    market = load_market(root)
    rel = (market.get("bundles") or {}).get(bundle_id)
    if not rel:
        raise KeyError(f"bundle_id not found in tool market: {bundle_id}")
    path = resolve_market_path(root, str(rel))
    return ToolBundle(path=path, data=read_yaml(path))


def discover_bundles(root: Path) -> dict[str, ToolBundle]:
    market = load_market(root)
    bundles: dict[str, ToolBundle] = {}
    for bundle_id, rel in sorted((market.get("bundles") or {}).items()):
        path = resolve_market_path(root, str(rel))
        bundle = ToolBundle(path=path, data=read_yaml(path))
        bundles[bundle_id] = bundle
    return bundles


def resolve_market_path(root: Path, rel: str) -> Path:
    path = root / rel
    if path.exists():
        return path
    return root / "tool_market" / rel


def market_package_ref_paths(root: Path) -> list[Path]:
    return _market_ref_paths(root, "packages")


def market_tool_ref_paths(root: Path) -> list[Path]:
    return _market_ref_paths(root, "tools")


def _market_ref_paths(root: Path, kind: str) -> list[Path]:
    return sorted(
        path for path in (root / "tool_market" / kind).glob("**/*.md") if path.name != "README.md"
    )


def bundles_for_task(root: Path, task_ref: str) -> dict[str, ToolBundle]:
    return {
        bundle_id: bundle
        for bundle_id, bundle in discover_bundles(root).items()
        if task_ref in bundle.task_refs
    }


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_market(root: Path) -> list[str]:
    errors: list[str] = []
    try:
        market = load_market(root)
    except Exception as exc:
        return [str(exc)]
    for key in REQUIRED_MARKET_KEYS:
        if key not in market:
            errors.append(f"market.yml: missing required key {key}")
    bundles = market.get("bundles")
    if not isinstance(bundles, dict):
        errors.append("market.yml: bundles must be a mapping")
        return errors
    for bundle_id, rel in bundles.items():
        path = resolve_market_path(root, str(rel))
        if not path.exists():
            errors.append(f"market.yml: bundle path does not exist for {bundle_id}: {rel}")
            continue
        errors.extend(f"{path}: {error}" for error in validate_bundle(root, path, expected_id=bundle_id))
    return errors


def validate_bundle(root: Path, path: Path, expected_id: str | None = None) -> list[str]:
    errors: list[str] = []
    try:
        data = read_yaml(path)
    except Exception as exc:
        return [str(exc)]
    for key in REQUIRED_BUNDLE_KEYS:
        if key not in data:
            errors.append(f"bundle: missing required key {key}")
    if errors:
        return errors
    bundle_id = data.get("bundle_id")
    if expected_id and bundle_id != expected_id:
        errors.append(f"bundle_id mismatch: market has {expected_id}, file has {bundle_id}")
    for key in ["task_refs", "stage_ids", "package_refs", "tool_refs", "check_refs"]:
        if not isinstance(data.get(key), list):
            errors.append(f"bundle: {key} must be a list")
    for ref in data.get("package_refs", []):
        _validate_source_ref(root, "package_refs", ref, errors)
    for ref in data.get("tool_refs", []):
        _validate_source_ref(root, "tool_refs", ref, errors)
        for key in ["slot_id", "stage_id", "method_family"]:
            if key not in ref:
                errors.append(f"bundle: tool ref missing {key}: {ref}")
    for key in ["wrapper", "adapter"]:
        rel = data.get(key)
        if not isinstance(rel, str) or not rel:
            errors.append(f"bundle: {key} must be a non-empty path string")
        elif not (root / rel).exists():
            errors.append(f"bundle: {key} path does not exist: {rel}")
    return errors


def _validate_source_ref(root: Path, kind: str, ref: Any, errors: list[str]) -> None:
    if not isinstance(ref, dict):
        errors.append(f"bundle: {kind} entry must be a mapping: {ref}")
        return
    for key in ["id", "path"]:
        if not ref.get(key):
            errors.append(f"bundle: {kind} entry missing {key}: {ref}")
    rel = ref.get("path")
    if rel and not (root / str(rel)).exists():
        errors.append(f"bundle: source ref path does not exist: {rel}")
