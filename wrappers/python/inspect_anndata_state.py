#!/usr/bin/env python3
"""Read-only AnnData state inspection wrapper."""

from __future__ import annotations

import argparse
import json
import math
from importlib import metadata
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import scanpy as sc

try:
    from scipy import sparse
except Exception:  # pragma: no cover - scipy is expected with scanpy
    sparse = None


SCHEMA_VERSION = "0.1.0"
MATRIX_SAMPLE_LIMIT = 10_000
AXIS_SAMPLE_LIMIT = 200


def json_safe(value: Any) -> Any:
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        if math.isnan(float(value)):
            return None
        return float(value)
    if isinstance(value, (np.bool_,)):
        return bool(value)
    if isinstance(value, Path):
        return str(value)
    return value


def version_or_missing(distribution: str) -> str | None:
    try:
        return metadata.version(distribution)
    except metadata.PackageNotFoundError:
        return None


def matrix_sample(matrix: Any) -> np.ndarray:
    if sparse is not None and sparse.issparse(matrix):
        data = matrix.data[:MATRIX_SAMPLE_LIMIT]
        return np.asarray(data)
    shape = getattr(matrix, "shape", None)
    if not shape or len(shape) != 2:
        return np.asarray([])
    n_obs = min(int(shape[0]), AXIS_SAMPLE_LIMIT)
    n_vars = min(int(shape[1]), AXIS_SAMPLE_LIMIT)
    try:
        sample = matrix[:n_obs, :n_vars]
    except Exception:
        return np.asarray([])
    if sparse is not None and sparse.issparse(sample):
        return np.asarray(sample.data[:MATRIX_SAMPLE_LIMIT])
    return np.asarray(sample).reshape(-1)[:MATRIX_SAMPLE_LIMIT]


def matrix_summary(matrix: Any) -> dict[str, Any]:
    shape = getattr(matrix, "shape", None)
    dtype = getattr(matrix, "dtype", None)
    summary: dict[str, Any] = {
        "type": type(matrix).__name__,
        "shape": [int(x) for x in shape] if shape is not None else None,
        "dtype": str(dtype) if dtype is not None else None,
        "is_sparse": bool(sparse is not None and sparse.issparse(matrix)),
    }
    if summary["is_sparse"]:
        summary["sparse_format"] = getattr(matrix, "format", None)
        summary["nnz"] = int(getattr(matrix, "nnz", 0))
    else:
        summary["sparse_format"] = None
        summary["nnz"] = None

    values = matrix_sample(matrix)
    numeric_values = values[np.isfinite(values)] if values.size else values
    summary["sample_size"] = int(values.size)
    if numeric_values.size:
        summary["sample_min"] = json_safe(np.min(numeric_values))
        summary["sample_max"] = json_safe(np.max(numeric_values))
        summary["sample_nonnegative"] = bool(np.all(numeric_values >= 0))
        summary["sample_integer_like"] = bool(np.all(np.isclose(numeric_values, np.round(numeric_values))))
    else:
        summary["sample_min"] = None
        summary["sample_max"] = None
        summary["sample_nonnegative"] = None
        summary["sample_integer_like"] = None
    return summary


def dataframe_summary(frame: pd.DataFrame) -> dict[str, Any]:
    categorical = []
    for column in frame.columns:
        series = frame[column]
        if isinstance(series.dtype, pd.CategoricalDtype) or series.dtype == object:
            categorical.append(str(column))
    return {
        "n_columns": int(frame.shape[1]),
        "columns": [str(column) for column in frame.columns],
        "dtypes": {str(column): str(dtype) for column, dtype in frame.dtypes.items()},
        "categorical_or_object_columns": categorical,
        "index_unique": bool(frame.index.is_unique),
        "duplicate_index_count": int(frame.index.duplicated().sum()),
    }


def mapping_shapes(mapping: Any) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key in mapping.keys():
        value = mapping[key]
        shape = getattr(value, "shape", None)
        dtype = getattr(value, "dtype", None)
        result[str(key)] = {
            "type": type(value).__name__,
            "shape": [int(x) for x in shape] if shape is not None else None,
            "dtype": str(dtype) if dtype is not None else None,
        }
    return result


def classify_state(report: dict[str, Any]) -> dict[str, Any]:
    x = report["slots"]["X"]
    layers = report["slots"]["layers"]
    raw = report["slots"]["raw"]
    obs = report["slots"]["obs"]
    var = report["slots"]["var"]

    has_counts_layer = "counts" in layers
    has_log_layer = "log1p_norm" in layers
    x_integer_like = x.get("sample_integer_like")
    x_nonnegative = x.get("sample_nonnegative")
    x_looks_like_counts = bool(x_integer_like and x_nonnegative)
    x_looks_like_log = bool(x_nonnegative and x_integer_like is False)
    warnings: list[str] = []

    if not has_counts_layer:
        warnings.append("No layers['counts'] key was found; count source is not declared.")
    if not has_log_layer:
        warnings.append("No layers['log1p_norm'] key was found; log-normalized source is not declared.")
    if raw["present"]:
        warnings.append(".raw is present but its biological meaning must still be confirmed.")
    if x_looks_like_counts and not has_counts_layer:
        warnings.append(".X sample is count-like, but this is not a declared counts layer.")
    if x_looks_like_log and not has_log_layer:
        warnings.append(".X sample is transformed-looking, but this is not a declared log1p layer.")
    if not obs["index_unique"]:
        warnings.append(".obs_names are not unique.")
    if not var["index_unique"]:
        warnings.append(".var_names are not unique.")

    return {
        "has_counts_layer": has_counts_layer,
        "has_log1p_norm_layer": has_log_layer,
        "has_raw": bool(raw["present"]),
        "x_sample_nonnegative": x_nonnegative,
        "x_sample_integer_like": x_integer_like,
        "x_looks_like_counts": x_looks_like_counts,
        "x_looks_like_log1p_or_scaled": x_looks_like_log,
        "ambiguous_expression_state": bool(warnings),
        "warnings": warnings,
    }


def inspect_h5ad(path: Path, backed: str | None) -> dict[str, Any]:
    adata = sc.read_h5ad(path, backed=backed)
    raw_summary: dict[str, Any]
    if adata.raw is None:
        raw_summary = {"present": False}
    else:
        raw_summary = {
            "present": True,
            "shape": [int(x) for x in adata.raw.shape],
            "X": matrix_summary(adata.raw.X),
            "var": dataframe_summary(adata.raw.var),
        }

    report: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "input_path": str(path),
        "backed_mode": backed,
        "object_type": type(adata).__name__,
        "shape": [int(adata.n_obs), int(adata.n_vars)],
        "is_view": bool(adata.is_view),
        "isbacked": bool(adata.isbacked),
        "slots": {
            "X": matrix_summary(adata.X),
            "obs": dataframe_summary(adata.obs),
            "var": dataframe_summary(adata.var),
            "layers": {str(key): matrix_summary(adata.layers[key]) for key in adata.layers.keys()},
            "raw": raw_summary,
            "obsm": mapping_shapes(adata.obsm),
            "obsp": {str(key): matrix_summary(adata.obsp[key]) for key in adata.obsp.keys()},
            "varm": mapping_shapes(adata.varm),
            "varp": {str(key): matrix_summary(adata.varp[key]) for key in adata.varp.keys()},
            "uns": {"keys": [str(key) for key in adata.uns.keys()]},
        },
    }
    report["state_flags"] = classify_state(report)
    if getattr(adata, "file", None) is not None:
        adata.file.close()
    return report


def versions_report() -> dict[str, Any]:
    packages = ["anndata", "scanpy", "numpy", "pandas", "scipy", "h5py"]
    return {
        "schema_version": SCHEMA_VERSION,
        "packages": {package: version_or_missing(package) for package in packages},
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, default=json_safe) + "\n", encoding="utf-8")


def write_markdown(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    flags = report["state_flags"]
    lines = [
        "# AnnData State Inspection",
        "",
        f"- Input: `{report['input_path']}`",
        f"- Shape: `{report['shape'][0]}` observations x `{report['shape'][1]}` variables",
        f"- Backed mode: `{report['backed_mode']}`",
        f"- `.X`: `{report['slots']['X']['type']}` `{report['slots']['X']['dtype']}`",
        f"- Layers: {', '.join(report['slots']['layers'].keys()) or 'none'}",
        f"- `.raw`: {'present' if flags['has_raw'] else 'absent'}",
        f"- Embeddings: {', '.join(report['slots']['obsm'].keys()) or 'none'}",
        f"- Pairwise obs matrices: {', '.join(report['slots']['obsp'].keys()) or 'none'}",
        "",
        "## State Flags",
        "",
        f"- counts layer: `{flags['has_counts_layer']}`",
        f"- log1p_norm layer: `{flags['has_log1p_norm_layer']}`",
        f"- ambiguous expression state: `{flags['ambiguous_expression_state']}`",
    ]
    if flags["warnings"]:
        lines.extend(["", "## Warnings", ""])
        lines.extend([f"- {warning}" for warning in flags["warnings"]])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect an AnnData .h5ad file without mutating it.")
    parser.add_argument("--input-h5ad", required=True, type=Path)
    parser.add_argument("--output-json", required=True, type=Path)
    parser.add_argument("--output-md", required=True, type=Path)
    parser.add_argument("--versions-json", required=True, type=Path)
    parser.add_argument("--backed", choices=["none", "r"], default="none")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_h5ad = args.input_h5ad
    if not input_h5ad.exists():
        raise FileNotFoundError(f"input .h5ad does not exist: {input_h5ad}")
    if input_h5ad.suffix.lower() != ".h5ad":
        raise ValueError(f"input path must have .h5ad suffix: {input_h5ad}")

    backed = None if args.backed == "none" else args.backed
    report = inspect_h5ad(input_h5ad, backed=backed)
    if report["shape"][0] == 0 or report["shape"][1] == 0:
        raise ValueError("AnnData object must have nonzero observations and variables")

    write_json(args.output_json, report)
    write_markdown(args.output_md, report)
    write_json(args.versions_json, versions_report())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
