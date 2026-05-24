import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MISSING = [
    package
    for package in ["snakemake", "anndata", "numpy", "pandas", "scanpy", "leidenalg", "igraph"]
    if importlib.util.find_spec(package) is None
]


class GraphClusteringWorkflowTest(unittest.TestCase):
    @unittest.skipIf(MISSING, "missing optional workflow dependencies: " + ", ".join(MISSING))
    def test_graph_clustering_snakemake_execution(self):
        import anndata as ad
        import numpy as np
        import pandas as pd
        import scanpy as sc

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            fixture = tmp_path / "represented.h5ad"
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
            adata.write_h5ad(fixture)

            config = tmp_path / "config.yml"
            config.write_text(
                "\n".join(
                    [
                        'schema_version: "0.1.0"',
                        "input_h5ad: " + str(fixture),
                        "outputs:",
                        "  h5ad: " + str(tmp_path / "out.h5ad"),
                        "  embedding_tsv: " + str(tmp_path / "embedding.tsv"),
                        "  cluster_sizes_json: " + str(tmp_path / "cluster_sizes.json"),
                        "  params_json: " + str(tmp_path / "params.json"),
                        "  versions_json: " + str(tmp_path / "versions.json"),
                        "logs:",
                        "  graph_clustering: " + str(tmp_path / "graph_clustering.log"),
                        "benchmarks:",
                        "  graph_clustering: " + str(tmp_path / "graph_clustering.tsv"),
                        "params:",
                        "  representation_key: X_pca",
                        "  neighbors_key: neighbors_x_pca",
                        "  embedding_key: X_umap_neighbors_x_pca",
                        "  cluster_key: leiden_neighbors_x_pca",
                        "  n_neighbors: 3",
                        "  n_pcs: 3",
                        "  metric: euclidean",
                        "  neighbors_method: umap",
                        "  umap_min_dist: 0.5",
                        "  umap_spread: 1.0",
                        "  resolution: 0.5",
                        "  random_state: 7",
                        "  leiden_flavor: leidenalg",
                        "  overwrite: false",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            env = os.environ.copy()
            env.setdefault("MPLCONFIGDIR", str(tmp_path / "mpl"))
            env.setdefault("XDG_CACHE_HOME", str(tmp_path / "cache"))
            env["PATH"] = str(Path(sys.executable).parent) + os.pathsep + env.get("PATH", "")
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "snakemake",
                    "--snakefile",
                    str(ROOT / "workflow/Snakefile"),
                    "--configfile",
                    str(config),
                    "--directory",
                    str(ROOT),
                    "--cores",
                    "1",
                ],
                cwd=ROOT,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            clustered = sc.read_h5ad(tmp_path / "out.h5ad")
            params = json.loads((tmp_path / "params.json").read_text())
            self.assertIn("neighbors_x_pca", clustered.uns)
            self.assertIn("X_umap_neighbors_x_pca", clustered.obsm)
            self.assertIn("leiden_neighbors_x_pca", clustered.obs)
            self.assertEqual(params["tool_refs"][0], "scrna.scverse.tool.scanpy_neighbors")


if __name__ == "__main__":
    unittest.main()
