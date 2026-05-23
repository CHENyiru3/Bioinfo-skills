#!/usr/bin/env python3
"""Check that Snakemake bindings stay adapter-only.

Workflow rules may call approved wrappers, but they should not embed Scanpy,
AnnData, or R analysis logic directly inside rule bodies. This script is a
policy lint for workflow files; it is intentionally conservative and can be
expanded when real rules are added.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_DIR = ROOT / "workflow"

DISALLOWED_PATTERNS = [
    r"\bimport\s+scanpy\b",
    r"\bimport\s+anndata\b",
    r"\bscanpy\.",
    r"\bsc\.(pp|tl|pl|get)\.",
    r"\banndata\.",
    r"\bread_h5ad\(",
    r"\brank_genes_groups\(",
    r"\bnormalize_total\(",
    r"\blog1p\(",
    r"\bhighly_variable_genes\(",
    r"\bneighbors\(",
    r"\bumap\(",
    r"\bleiden\(",
]

ALLOWED_WRAPPER_HINTS = [
    "wrappers/python/",
    "wrappers/r/",
]


def inspect_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    for pattern in DISALLOWED_PATTERNS:
        if re.search(pattern, text):
            errors.append(f"{path}: embeds analysis logic matching {pattern}")
    if path.suffix == ".smk" and "rule " in text and not any(hint in text for hint in ALLOWED_WRAPPER_HINTS):
        errors.append(f"{path}: rule file should call a wrapper under wrappers/")
    return errors


def main() -> int:
    if not WORKFLOW_DIR.exists():
        print("no workflow directory found; policy check passed")
        return 0
    files = sorted([*WORKFLOW_DIR.glob("Snakefile"), *WORKFLOW_DIR.glob("rules/*.smk")])
    errors: list[str] = []
    for path in files:
        errors.extend(inspect_file(path))
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"Snakemake policy check passed for {len(files)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
