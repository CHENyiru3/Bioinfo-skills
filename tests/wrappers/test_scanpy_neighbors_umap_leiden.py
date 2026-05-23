import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import anndata as ad
import numpy as np
import pandas as pd
import scanpy as sc


ROOT = Path(__file__).resolve().parents[2]
WRAPPER = ROOT / "wrappers/python/scanpy_neighbors_umap_leiden.py"


class ScanpyNeighborsUmapLeidenTest(unittest.TestCase):
    def make_fixture(self, path: Path) -> None:
        obs = pd.DataFrame(index=[f"cell{i}" for i in range(10)])
        var = pd.DataFrame(index=[f"gene{i}" for i in range(4)])
        x = np.array(
            [
                [1.0, 0.8, 0.1, 0.0],
                [0.9, 0.7, 0.0, 0.1],
                [1.1, 0.9, 0.1, 0.0],
                [0.8, 0.6, 0.1, 0.1],
                [1.0, 0.7, 0.0, 0.2],
                [-1.0, -0.8, 0.1, 0.0],
                [-0.9, -0.7, 0.0, -0.1],
                [-1.1, -0.9, 0.1, 0.0],
                [-0.8, -0.6, -0.1, -0.1],
                [-1.0, -0.7, 0.0, -0.2],
            ]
        )
        adata = ad.AnnData(X=x, obs=obs, var=var)
        adata.obsm["X_pca"] = x[:, :3]
        adata.write_h5ad(path)

    def run_wrapper(self, fixture: Path, outdir: Path, extra_args=None) -> subprocess.CompletedProcess:
        env = os.environ.copy()
        env.setdefault("MPLCONFIGDIR", str(outdir / "mpl"))
        env.setdefault("XDG_CACHE_HOME", str(outdir / "cache"))
        command = [
            sys.executable,
            str(WRAPPER),
            "--input-h5ad",
            str(fixture),
            "--output-h5ad",
            str(outdir / "graph_clustered.h5ad"),
            "--embedding-tsv",
            str(outdir / "embedding.tsv"),
            "--cluster-sizes-json",
            str(outdir / "cluster_sizes.json"),
            "--params-json",
            str(outdir / "params.json"),
            "--versions-json",
            str(outdir / "versions.json"),
            "--representation-key",
            "X_pca",
            "--neighbors-key",
            "neighbors_x_pca",
            "--embedding-key",
            "X_umap_neighbors_x_pca",
            "--cluster-key",
            "leiden_neighbors_x_pca",
            "--n-neighbors",
            "3",
            "--n-pcs",
            "3",
            "--resolution",
            "0.5",
            "--random-state",
            "7",
        ]
        if extra_args:
            command.extend(extra_args)
        return subprocess.run(command, cwd=ROOT, env=env, text=True, capture_output=True, check=False)

    def test_wrapper_writes_declared_graph_embedding_and_clusters(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            fixture = tmp_path / "represented.h5ad"
            self.make_fixture(fixture)

            result = self.run_wrapper(fixture, tmp_path)
            self.assertEqual(result.returncode, 0, result.stderr)

            output = sc.read_h5ad(tmp_path / "graph_clustered.h5ad")
            params = json.loads((tmp_path / "params.json").read_text())
            cluster_sizes = json.loads((tmp_path / "cluster_sizes.json").read_text())
            versions = json.loads((tmp_path / "versions.json").read_text())
            embedding_text = (tmp_path / "embedding.tsv").read_text()

            self.assertIn("neighbors_x_pca", output.uns)
            self.assertIn("neighbors_x_pca_connectivities", output.obsp)
            self.assertIn("neighbors_x_pca_distances", output.obsp)
            self.assertIn("X_umap_neighbors_x_pca", output.obsm)
            self.assertIn("leiden_neighbors_x_pca", output.obs)
            self.assertEqual(params["representation_key"], "X_pca")
            self.assertEqual(params["neighbors_key"], "neighbors_x_pca")
            self.assertEqual(sum(cluster_sizes["clusters"].values()), output.n_obs)
            self.assertIn("scanpy", versions["packages"])
            self.assertIn("cell_id", embedding_text.splitlines()[0])

    def test_wrapper_fails_on_missing_representation(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            fixture = tmp_path / "represented.h5ad"
            self.make_fixture(fixture)

            result = self.run_wrapper(fixture, tmp_path, extra_args=["--representation-key", "missing"])
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("representation key not found", result.stderr)


if __name__ == "__main__":
    unittest.main()
