#!/usr/bin/env python3
"""Build neighbors, UMAP, and Leiden labels from an existing representation."""

from __future__ import annotations

import argparse
import json
from importlib import metadata
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import scanpy as sc


SCHEMA_VERSION = "0.1.0"


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
    if args.n_neighbors < 2:
        raise ValueError("--n-neighbors must be at least 2")
    if args.n_pcs is not None and args.n_pcs < 1:
        raise ValueError("--n-pcs must be positive when supplied")
    if args.resolution <= 0:
        raise ValueError("--resolution must be positive")
    for value, name in [
        (args.representation_key, "--representation-key"),
        (args.neighbors_key, "--neighbors-key"),
        (args.embedding_key, "--embedding-key"),
        (args.cluster_key, "--cluster-key"),
    ]:
        if not value:
            raise ValueError(f"{name} must be non-empty")


def validate_input_state(adata: Any, args: argparse.Namespace) -> None:
    if adata.n_obs == 0 or adata.n_vars == 0:
        raise ValueError("AnnData object must have nonzero observations and variables")
    if args.representation_key not in adata.obsm:
        raise ValueError(f"representation key not found in adata.obsm: {args.representation_key}")
    representation = adata.obsm[args.representation_key]
    if representation.shape[0] != adata.n_obs:
        raise ValueError("representation row count must match adata.n_obs")
    if args.n_pcs is not None and args.n_pcs > representation.shape[1]:
        raise ValueError(f"--n-pcs exceeds representation dimensions: {args.n_pcs} > {representation.shape[1]}")
    if args.n_neighbors >= adata.n_obs:
        raise ValueError("--n-neighbors must be smaller than number of observations")
    if not args.overwrite:
        collisions = []
        if args.neighbors_key in adata.uns:
            collisions.append(f"uns[{args.neighbors_key!r}]")
        if f"{args.neighbors_key}_distances" in adata.obsp:
            collisions.append(f"obsp[{args.neighbors_key + '_distances'!r}]")
        if f"{args.neighbors_key}_connectivities" in adata.obsp:
            collisions.append(f"obsp[{args.neighbors_key + '_connectivities'!r}]")
        if args.embedding_key in adata.obsm:
            collisions.append(f"obsm[{args.embedding_key!r}]")
        if args.cluster_key in adata.obs:
            collisions.append(f"obs[{args.cluster_key!r}]")
        if collisions:
            raise ValueError("refusing to overwrite existing keys without --overwrite: " + ", ".join(collisions))


def versions_report() -> dict[str, Any]:
    packages = ["anndata", "scanpy", "numpy", "pandas", "scipy", "leidenalg", "igraph", "umap-learn"]
    return {
        "schema_version": SCHEMA_VERSION,
        "packages": {package: version_or_missing(package) for package in packages},
    }


def resolved_parameters(args: argparse.Namespace, cluster_sizes: pd.Series) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "tool_refs": [
            "scrna.scverse.tool.scanpy_neighbors",
            "scrna.scverse.tool.scanpy_umap",
            "scrna.scverse.tool.scanpy_leiden",
        ],
        "input_h5ad": str(args.input_h5ad),
        "output_h5ad": str(args.output_h5ad),
        "representation_key": args.representation_key,
        "neighbors_key": args.neighbors_key,
        "embedding_key": args.embedding_key,
        "cluster_key": args.cluster_key,
        "n_neighbors": args.n_neighbors,
        "n_pcs": args.n_pcs,
        "metric": args.metric,
        "neighbors_method": args.neighbors_method,
        "umap_min_dist": args.umap_min_dist,
        "umap_spread": args.umap_spread,
        "resolution": args.resolution,
        "random_state": args.random_state,
        "leiden_flavor": args.leiden_flavor,
        "overwrite": args.overwrite,
        "cluster_sizes": cluster_sizes.to_dict(),
        "claims": {
            "allowed": [
                "neighbor graph, UMAP coordinates, and Leiden graph communities from the declared representation",
                "cluster-size summary for the declared cluster key",
            ],
            "forbidden": [
                "cell type annotation",
                "condition-level inference",
                "normalization, feature selection, or PCA performed by this wrapper",
            ],
        },
    }


def run(args: argparse.Namespace) -> None:
    validate_args(args)
    adata = sc.read_h5ad(args.input_h5ad)
    validate_input_state(adata, args)

    sc.pp.neighbors(
        adata,
        use_rep=args.representation_key,
        n_neighbors=args.n_neighbors,
        n_pcs=args.n_pcs,
        metric=args.metric,
        method=args.neighbors_method,
        random_state=args.random_state,
        key_added=args.neighbors_key,
    )
    sc.tl.umap(
        adata,
        neighbors_key=args.neighbors_key,
        min_dist=args.umap_min_dist,
        spread=args.umap_spread,
        random_state=args.random_state,
        key_added=args.embedding_key,
    )
    sc.tl.leiden(
        adata,
        neighbors_key=args.neighbors_key,
        resolution=args.resolution,
        random_state=args.random_state,
        key_added=args.cluster_key,
        flavor=args.leiden_flavor,
    )

    cluster_sizes = adata.obs[args.cluster_key].astype(str).value_counts().sort_index()
    params = resolved_parameters(args, cluster_sizes)
    adata.uns.setdefault("bioinfo_skills", {})
    adata.uns["bioinfo_skills"].setdefault("neighbors_umap_leiden", {})
    adata.uns["bioinfo_skills"]["neighbors_umap_leiden"][args.cluster_key] = params

    embedding = pd.DataFrame(
        np.asarray(adata.obsm[args.embedding_key]),
        index=adata.obs_names,
        columns=[f"{args.embedding_key}_{i + 1}" for i in range(adata.obsm[args.embedding_key].shape[1])],
    )
    embedding.insert(0, "cell_id", embedding.index)

    args.output_h5ad.parent.mkdir(parents=True, exist_ok=True)
    adata.write_h5ad(args.output_h5ad)
    args.embedding_tsv.parent.mkdir(parents=True, exist_ok=True)
    embedding.to_csv(args.embedding_tsv, sep="\t", index=False)
    write_json(args.cluster_sizes_json, {"schema_version": SCHEMA_VERSION, "cluster_key": args.cluster_key, "clusters": cluster_sizes.to_dict()})
    write_json(args.params_json, params)
    write_json(args.versions_json, versions_report())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run Scanpy neighbors, UMAP, and Leiden from an existing representation."
    )
    parser.add_argument("--input-h5ad", required=True, type=Path)
    parser.add_argument("--output-h5ad", required=True, type=Path)
    parser.add_argument("--embedding-tsv", required=True, type=Path)
    parser.add_argument("--cluster-sizes-json", required=True, type=Path)
    parser.add_argument("--params-json", required=True, type=Path)
    parser.add_argument("--versions-json", required=True, type=Path)
    parser.add_argument("--representation-key", required=True)
    parser.add_argument("--neighbors-key", required=True)
    parser.add_argument("--embedding-key", required=True)
    parser.add_argument("--cluster-key", required=True)
    parser.add_argument("--n-neighbors", type=int, default=15)
    parser.add_argument("--n-pcs", type=int)
    parser.add_argument("--metric", default="euclidean")
    parser.add_argument("--neighbors-method", default="umap", choices=["umap", "gauss"])
    parser.add_argument("--umap-min-dist", type=float, default=0.5)
    parser.add_argument("--umap-spread", type=float, default=1.0)
    parser.add_argument("--resolution", type=float, default=1.0)
    parser.add_argument("--random-state", type=int, default=0)
    parser.add_argument("--leiden-flavor", default="leidenalg", choices=["leidenalg", "igraph"])
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> int:
    run(parse_args())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
