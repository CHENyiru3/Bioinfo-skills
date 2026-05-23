#!/usr/bin/env python3
"""Check that the AnnData state contract contains required conventions."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts/anndata_scrna_state_v0.yml"
REQUIRED_TOKENS = [
    'layers:',
    'counts:',
    'log1p_norm:',
    'sample_id:',
    'batch:',
    'X_pca:',
    'X_umap:',
    'bioinfo_skills:',
]


def main() -> int:
    text = CONTRACT.read_text(encoding="utf-8")
    missing = [token for token in REQUIRED_TOKENS if token not in text]
    if missing:
        for token in missing:
            print(f"missing contract token: {token}", file=sys.stderr)
        return 1
    print("AnnData contract check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

