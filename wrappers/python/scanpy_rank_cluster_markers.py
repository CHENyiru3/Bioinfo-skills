#!/usr/bin/env python3
"""Rank marker genes for existing AnnData groups with explicit state gates."""

from __future__ import annotations

import argparse
import json
from importlib import metadata
from pathlib import Path
from typing import Any

import pandas as pd
import scanpy as sc


SCHEMA_VERSION = "0.1.0"
VALID_METHODS = {"t-test", "t-test_overestim_var", "wilcoxon", "logreg"}
VALID_SOURCES = {"X", "raw", "layer"}


def version_or_missing(distribution: str) -> str | None:
    try:
        return metadata.version(distribution)
    except metadata.PackageNotFoundError:
        return None


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def validate_args(args: argparse.Namespace) -> None:
    if not args.input_h5ad.exists():
        raise FileNotFoundError(f"input .h5ad does not exist: {args.input_h5ad}")
    if args.input_h5ad.suffix.lower() != ".h5ad":
        raise ValueError(f"input path must have .h5ad suffix: {args.input_h5ad}")
    if args.expression_source not in VALID_SOURCES:
        raise ValueError(f"expression source must be one of {sorted(VALID_SOURCES)}")
    if args.expression_source == "layer" and not args.layer:
        raise ValueError("--layer is required when --expression-source layer")
    if args.expression_source != "layer" and args.layer:
        raise ValueError("--layer can only be used with --expression-source layer")
    if args.method not in VALID_METHODS:
        raise ValueError(f"method must be one of {sorted(VALID_METHODS)}")
    if args.n_genes < 1:
        raise ValueError("--n-genes must be positive")


def expression_kwargs(adata: Any, source: str, layer: str | None) -> dict[str, Any]:
    if source == "raw":
        if adata.raw is None:
            raise ValueError("expression source 'raw' requested, but adata.raw is absent")
        return {"use_raw": True, "layer": None}
    if source == "layer":
        if layer not in adata.layers:
            raise ValueError(f"expression layer not found: {layer}")
        return {"use_raw": False, "layer": layer}
    return {"use_raw": False, "layer": None}


def validate_groupby(adata: Any, groupby: str, reference: str) -> pd.Series:
    if groupby not in adata.obs:
        raise ValueError(f"groupby column not found in adata.obs: {groupby}")
    groups = adata.obs[groupby]
    if groups.isna().any():
        raise ValueError(f"groupby column contains missing values: {groupby}")
    group_sizes = groups.astype(str).value_counts().sort_index()
    if group_sizes.shape[0] < 2:
        raise ValueError(f"groupby column must contain at least two groups: {groupby}")
    if reference != "rest" and reference not in set(group_sizes.index):
        raise ValueError(f"reference must be 'rest' or an existing group in {groupby}: {reference}")
    return group_sizes


def versions_report() -> dict[str, Any]:
    packages = ["anndata", "scanpy", "numpy", "pandas", "scipy"]
    return {
        "schema_version": SCHEMA_VERSION,
        "packages": {package: version_or_missing(package) for package in packages},
    }


def resolved_parameters(args: argparse.Namespace, group_sizes: pd.Series) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "tool_ref": "scrna.scverse.tool.scanpy_rank_genes_groups",
        "method": "scanpy.tl.rank_genes_groups",
        "input_h5ad": str(args.input_h5ad),
        "output_h5ad": str(args.output_h5ad),
        "output_table": str(args.output_table),
        "groupby": args.groupby,
        "reference": args.reference,
        "rank_method": args.method,
        "expression_source": args.expression_source,
        "layer": args.layer,
        "n_genes": args.n_genes,
        "key_added": args.key_added,
        "groups": group_sizes.to_dict(),
        "claims": {
            "allowed": [
                "cluster marker ranking for existing groups",
                "descriptive per-cell group marker table",
            ],
            "forbidden": [
                "condition-level differential expression",
                "replicate-aware inference",
                "cell type annotation certainty",
            ],
        },
    }


def run(args: argparse.Namespace) -> None:
    validate_args(args)
    adata = sc.read_h5ad(args.input_h5ad)
    if adata.n_obs == 0 or adata.n_vars == 0:
        raise ValueError("AnnData object must have nonzero observations and variables")

    source_kwargs = expression_kwargs(adata, args.expression_source, args.layer)
    group_sizes = validate_groupby(adata, args.groupby, args.reference)

    sc.tl.rank_genes_groups(
        adata,
        groupby=args.groupby,
        method=args.method,
        reference=args.reference,
        n_genes=args.n_genes,
        key_added=args.key_added,
        use_raw=source_kwargs["use_raw"],
        layer=source_kwargs["layer"],
    )

    params = resolved_parameters(args, group_sizes)
    adata.uns.setdefault("bioinfo_skills", {})
    adata.uns["bioinfo_skills"].setdefault("marker_ranking", {})
    adata.uns["bioinfo_skills"]["marker_ranking"][args.key_added] = params

    marker_table = sc.get.rank_genes_groups_df(adata, group=None, key=args.key_added)
    marker_table.insert(0, "key_added", args.key_added)
    marker_table.insert(1, "groupby", args.groupby)
    marker_table.insert(2, "rank_method", args.method)
    marker_table.insert(3, "reference", args.reference)
    marker_table.insert(4, "expression_source", args.expression_source)
    marker_table.insert(5, "layer", args.layer or "")
    marker_table.insert(6, "tool_ref", "scrna.scverse.tool.scanpy_rank_genes_groups")

    args.output_h5ad.parent.mkdir(parents=True, exist_ok=True)
    args.output_table.parent.mkdir(parents=True, exist_ok=True)
    adata.write_h5ad(args.output_h5ad)
    marker_table.to_csv(args.output_table, sep="\t", index=False)
    write_json(args.group_sizes_json, {"schema_version": SCHEMA_VERSION, "groupby": args.groupby, "groups": group_sizes.to_dict()})
    write_json(args.params_json, params)
    write_json(args.versions_json, versions_report())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Rank marker genes for existing groups. This is not condition-level differential expression."
    )
    parser.add_argument("--input-h5ad", required=True, type=Path)
    parser.add_argument("--output-h5ad", required=True, type=Path)
    parser.add_argument("--output-table", required=True, type=Path)
    parser.add_argument("--group-sizes-json", required=True, type=Path)
    parser.add_argument("--params-json", required=True, type=Path)
    parser.add_argument("--versions-json", required=True, type=Path)
    parser.add_argument("--groupby", required=True)
    parser.add_argument("--expression-source", required=True, choices=sorted(VALID_SOURCES))
    parser.add_argument("--layer")
    parser.add_argument("--method", default="wilcoxon", choices=sorted(VALID_METHODS))
    parser.add_argument("--reference", default="rest")
    parser.add_argument("--n-genes", type=int, default=50)
    parser.add_argument("--key-added", default="rank_genes_groups")
    return parser.parse_args()


def main() -> int:
    run(parse_args())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
