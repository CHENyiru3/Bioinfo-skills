#!/usr/bin/env python3
"""Generate a scverse package availability report from tool-market package refs."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports/runtime"
PACKAGE_REFS = ROOT / "tool_market" / "packages"

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


def local_relocated_python() -> Path | None:
    python_exec = ROOT.parent / "bioinfo_tutorial" / "conda_env" / "bin" / "python"
    if python_exec.exists():
        return python_exec
    return None


def discover_python() -> tuple[Path, str]:
    requested = os.environ.get("BIOINFO_PYTHON_EXEC")
    if requested:
        return Path(requested), "BIOINFO_PYTHON_EXEC"
    relocated = local_relocated_python()
    if relocated:
        return relocated, "local_relocated_bioinfo_tutorial"
    return Path(sys.executable), "current_python"


def run_python(python_exec: Path, code: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env.setdefault("MPLCONFIGDIR", "/tmp/bioinfo-skills-matplotlib")
    return subprocess.run(
        [str(python_exec), "-c", code],
        cwd=ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=120,
    )


def tsv_row(row: dict[str, str | None]) -> dict[str, str]:
    return {key: str(value) if value is not None else "NA" for key, value in row.items()}


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
    for ref in sorted(PACKAGE_REFS.glob("**/*.md")):
        if ref.name == "README.md":
            continue
        meta = frontmatter(ref)
        if meta.get("language") and meta.get("language") != "python":
            continue
        if meta.get("ecosystem") and meta.get("ecosystem") != "scverse":
            continue
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


def python_version(python_exec: Path) -> str | None:
    result = run_python(python_exec, "import platform; print(platform.python_version())")
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def probe(row: dict[str, str], python_exec: Path) -> dict[str, str | None]:
    package = row["package"]
    import_name = row["import_name"]
    dist_name = row["distribution"]
    code = f"""
import importlib
import importlib.metadata as metadata
import json

dist_name = {json.dumps(dist_name)}
import_name = {json.dumps(import_name)}
version = None
failure_reason = None
try:
    version = metadata.version(dist_name)
except Exception as exc:
    failure_reason = f"metadata: {{type(exc).__name__}}"
try:
    importlib.import_module(import_name)
    status = "installed"
    failure_reason = None
except Exception as exc:
    status = "missing"
    failure_reason = f"import: {{type(exc).__name__}}: {{exc}}"
print("BIOINFO_RUNTIME_PROBE\\t" + json.dumps({{
    "version": version,
    "status": status,
    "failure_reason": failure_reason,
}}))
"""
    try:
        result = run_python(python_exec, code)
    except subprocess.TimeoutExpired:
        status = "missing"
        version = None
        failure_reason = "probe timed out"
    else:
        probe_lines = [line for line in result.stdout.splitlines() if line.startswith("BIOINFO_RUNTIME_PROBE\t")]
        if result.returncode == 0 and probe_lines:
            payload = json.loads(probe_lines[-1].split("\t", 1)[1])
            status = payload.get("status") or "missing"
            version = payload.get("version")
            failure_reason = payload.get("failure_reason")
        else:
            status = "missing"
            version = None
            failure_reason = (result.stderr or result.stdout).strip().splitlines()[-1] if (result.stderr or result.stdout).strip() else f"python exited {result.returncode}"
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
    python_exec, python_source = discover_python()
    package_rows = [probe(row, python_exec) for row in packages()]
    report = {
        "schema_version": "0.1.0",
        "generated_at": generated_at,
        "runtime_profile": "current_python",
        "python_executable": str(python_exec),
        "python_executable_source": python_source,
        "python_version": python_version(python_exec),
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
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(tsv_row(row) for row in package_rows)
    lines = ["# scverse Runtime Status", "", f"Generated: {generated_at}", ""]
    lines.append(f"Python executable: `{report['python_executable']}` ({python_source})")
    lines.append(f"Python version: `{report['python_version'] or 'unknown'}`")
    lines.append("")
    for row in package_rows:
        version = row["version"] or ""
        note = row["failure_reason"] or ""
        lines.append(f"- `{row['package']}`: {row['status']} {version} {note}".rstrip())
    (REPORT_DIR / "scverse_runtime_status.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote runtime report for {len(package_rows)} packages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
