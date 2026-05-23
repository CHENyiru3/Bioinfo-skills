#!/usr/bin/env python3
"""Generate a scverse package availability report from repo-local package refs."""

from __future__ import annotations

import importlib
import importlib.metadata as metadata
import json
import re
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports/runtime"
PACKAGE_REFS = ROOT / "skills/scrna/scverse/refs/packages"

IMPORT_ALIASES = {
    "scvi_tools": "scvi",
    "scfates": "scFates",
    "pydeseq2": "pydeseq2",
}

DIST_ALIASES = {
    "scvi_tools": "scvi-tools",
    "rapids_singlecell": "rapids-singlecell",
    "scfates": "scFates",
}


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    data: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def packages() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for ref in sorted(PACKAGE_REFS.glob("*.md")):
        if ref.name == "README.md":
            continue
        meta = frontmatter(ref)
        package = meta.get("package") or re.sub(r"\.md$", "", ref.name)
        rows.append(
            {
                "package": package,
                "import_name": meta.get("import_name", IMPORT_ALIASES.get(package, package)),
                "distribution": DIST_ALIASES.get(package, package),
                "declared_runtime_status": meta.get("runtime_status", "unknown"),
                "ref_path": str(ref.relative_to(ROOT)),
            }
        )
    return rows


def probe(row: dict[str, str]) -> dict[str, str | None]:
    package = row["package"]
    import_name = row["import_name"]
    dist_name = row["distribution"]
    version = None
    status = "missing"
    failure_reason = None
    try:
        version = metadata.version(dist_name)
    except Exception as exc:
        failure_reason = f"metadata: {type(exc).__name__}"
    try:
        importlib.import_module(import_name)
        status = "installed"
        failure_reason = None
    except Exception as exc:
        if status != "installed":
            failure_reason = f"import: {type(exc).__name__}: {exc}"
    return {
        "package": package,
        "distribution": dist_name,
        "import_name": import_name,
        "declared_runtime_status": row.get("declared_runtime_status"),
        "ref_path": row.get("ref_path"),
        "version": version,
        "status": status,
        "failure_reason": failure_reason,
        "waiver_reason": None,
    }


def main() -> int:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    generated_at = datetime.now(timezone.utc).isoformat()
    package_rows = [probe(row) for row in packages()]
    report = {
        "schema_version": "0.1.0",
        "generated_at": generated_at,
        "runtime_profile": "current_python",
        "packages": package_rows,
    }

    (REPORT_DIR / "scverse_runtime_status.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    with (REPORT_DIR / "scverse_runtime_status.tsv").open("w", encoding="utf-8", newline="") as handle:
        import csv

        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "package",
                "distribution",
                "import_name",
                "declared_runtime_status",
                "ref_path",
                "version",
                "status",
                "failure_reason",
                "waiver_reason",
            ],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(package_rows)
    lines = ["# scverse Runtime Status", "", f"Generated: {generated_at}", ""]
    for row in package_rows:
        version = row["version"] or ""
        note = row["failure_reason"] or ""
        lines.append(f"- `{row['package']}`: {row['status']} {version} {note}".rstrip())
    (REPORT_DIR / "scverse_runtime_status.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote runtime report for {len(package_rows)} packages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
