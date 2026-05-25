#!/usr/bin/env python3
"""Generate an R/Seurat package availability report from package refs."""

from __future__ import annotations

import csv
import json
import os
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports" / "runtime"
PACKAGE_REFS = ROOT / "tool_market" / "packages"


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
        if meta.get("language") != "r":
            continue
        if meta.get("ecosystem") != "seurat":
            continue
        package = meta.get("package") or re.sub(r"\.md$", "", ref.name)
        rows.append(
            {
                "package": package,
                "import_name": meta.get("import_name", package),
                "declared_runtime_status": meta.get("runtime_status", "unknown"),
                "runtime_required": meta.get("runtime_required", "required"),
                "install_route": meta.get("install_route", "unknown"),
                "ref_path": str(ref.relative_to(ROOT)),
            }
        )
    return rows


def local_relocated_r() -> tuple[Path, dict[str, str]] | None:
    env_prefix = ROOT.parent / "seurat_tutorial" / "conda_env"
    r_home = env_prefix / "lib" / "R"
    r_exec = r_home / "bin" / "exec" / "R"
    if not r_exec.exists():
        return None
    env = {
        "R_HOME": str(r_home),
        "R_SHARE_DIR": str(r_home / "share"),
        "R_INCLUDE_DIR": str(r_home / "include"),
        "R_DOC_DIR": str(r_home / "doc"),
        "LD_LIBRARY_PATH": str(env_prefix / "lib"),
    }
    return r_exec, env


def discover_r() -> tuple[Path | None, dict[str, str], str]:
    env = dict(os.environ)
    requested = os.environ.get("BIOINFO_R_EXEC")
    if requested:
        return Path(requested), env, "BIOINFO_R_EXEC"
    path_r = shutil.which("R")
    if path_r:
        return Path(path_r), env, "PATH"
    relocated = local_relocated_r()
    if relocated:
        r_exec, r_env = relocated
        env.update(r_env)
        return r_exec, env, "local_relocated_seurat_tutorial"
    return None, env, "not_found"


def run_r(r_exec: Path, env: dict[str, str], expression: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(r_exec), "--slave", "-e", expression],
        cwd=ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=120,
    )


def ascii_message(value: str) -> str:
    return value.replace("\u2018", "'").replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')


def tsv_row(row: dict[str, str | None]) -> dict[str, str]:
    return {key: str(value) if value is not None else "NA" for key, value in row.items()}


def r_version(r_exec: Path | None, env: dict[str, str]) -> str | None:
    if r_exec is None:
        return None
    result = run_r(r_exec, env, 'cat(as.character(getRversion()), "\\n")')
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def probe(row: dict[str, str], r_exec: Path | None, env: dict[str, str]) -> dict[str, str | None]:
    package = row["package"]
    import_name = row["import_name"]
    waiver_reason = None
    if row.get("runtime_required") == "optional" and row.get("install_route") == "source":
        waiver_reason = "optional source-route package; install with scripts/install_seurat_source_packages.R"
    if r_exec is None:
        return {
            "package": package,
            "import_name": import_name,
            "declared_runtime_status": row.get("declared_runtime_status"),
            "runtime_required": row.get("runtime_required"),
            "install_route": row.get("install_route"),
            "ref_path": row.get("ref_path"),
            "version": None,
            "status": "missing",
            "failure_reason": "R executable not found",
            "waiver_reason": waiver_reason,
        }
    expression = (
        "tryCatch(suppressPackageStartupMessages({"
        f"pkg <- {json.dumps(import_name)}; "
        "library(pkg, character.only = TRUE); "
        "cat(as.character(packageVersion(pkg)), \"\\n\")"
        "}), error = function(e) { message(conditionMessage(e)); quit(status = 1) })"
    )
    try:
        result = run_r(r_exec, env, expression)
    except subprocess.TimeoutExpired:
        return {
            "package": package,
            "import_name": import_name,
            "declared_runtime_status": row.get("declared_runtime_status"),
            "runtime_required": row.get("runtime_required"),
            "install_route": row.get("install_route"),
            "ref_path": row.get("ref_path"),
            "version": None,
            "status": "missing",
            "failure_reason": "R probe timed out",
            "waiver_reason": waiver_reason,
        }
    if result.returncode == 0:
        return {
            "package": package,
            "import_name": import_name,
            "declared_runtime_status": row.get("declared_runtime_status"),
            "runtime_required": row.get("runtime_required"),
            "install_route": row.get("install_route"),
            "ref_path": row.get("ref_path"),
            "version": result.stdout.strip() or None,
            "status": "installed",
            "failure_reason": None,
            "waiver_reason": None,
        }
    failure = [
        line
        for line in (result.stderr or result.stdout).strip().splitlines()
        if line.strip() and line.strip() != "Execution halted"
    ]
    error_lines = [line for line in failure if "Error" in line]
    failure_reason = error_lines[-1] if error_lines else (failure[-1] if failure else f"R exited {result.returncode}")
    failure_reason = ascii_message(failure_reason)
    return {
        "package": package,
        "import_name": import_name,
        "declared_runtime_status": row.get("declared_runtime_status"),
        "runtime_required": row.get("runtime_required"),
        "install_route": row.get("install_route"),
        "ref_path": row.get("ref_path"),
        "version": None,
        "status": "missing",
        "failure_reason": failure_reason,
        "waiver_reason": waiver_reason,
    }


def main() -> int:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    generated_at = datetime.now(timezone.utc).isoformat()
    r_exec, env, source = discover_r()
    version = r_version(r_exec, env)
    package_rows = [probe(row, r_exec, env) for row in packages()]
    report = {
        "schema_version": "0.1.0",
        "generated_at": generated_at,
        "runtime_profile": "current_r",
        "r_executable": str(r_exec) if r_exec else None,
        "r_executable_source": source,
        "r_version": version,
        "packages": package_rows,
    }

    (REPORT_DIR / "seurat_runtime_status.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    fieldnames = [
        "package",
        "import_name",
        "declared_runtime_status",
        "runtime_required",
        "install_route",
        "ref_path",
        "version",
        "status",
        "failure_reason",
        "waiver_reason",
    ]
    with (REPORT_DIR / "seurat_runtime_status.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(tsv_row(row) for row in package_rows)
    lines = ["# Seurat Runtime Status", "", f"Generated: {generated_at}", ""]
    lines.append(f"R executable: `{report['r_executable']}` ({source})")
    lines.append(f"R version: `{version or 'unknown'}`")
    lines.append("")
    for row in package_rows:
        version_text = row["version"] or ""
        note = row["failure_reason"] or ""
        waiver = f" waiver: {row['waiver_reason']}" if row.get("waiver_reason") else ""
        lines.append(f"- `{row['package']}`: {row['status']} {version_text} {note}{waiver}".rstrip())
    (REPORT_DIR / "seurat_runtime_status.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote runtime report for {len(package_rows)} R packages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
