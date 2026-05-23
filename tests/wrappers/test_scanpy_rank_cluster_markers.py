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
WRAPPER = ROOT / "wrappers/python/scanpy_rank_cluster_markers.py"


class ScanpyRankClusterMarkersTest(unittest.TestCase):
    def make_fixture(self, path: Path) -> None:
        counts = np.array(
            [
                [10, 1, 0, 0, 1],
                [9, 2, 0, 0, 1],
                [11, 1, 0, 1, 0],
                [0, 0, 10, 2, 1],
                [1, 0, 9, 1, 0],
                [0, 1, 11, 2, 1],
            ],
            dtype=np.int64,
        )
        obs = pd.DataFrame(
            {
                "leiden": pd.Categorical(["0", "0", "0", "1", "1", "1"]),
                "sample_id": ["s1", "s1", "s2", "s2", "s3", "s3"],
            },
            index=[f"cell{i}" for i in range(6)],
        )
        var = pd.DataFrame(index=[f"gene{i}" for i in range(5)])
        log_norm = np.log1p(counts.astype(float))
        adata = ad.AnnData(X=log_norm.copy(), obs=obs, var=var)
        adata.layers["counts"] = counts
        adata.layers["log1p_norm"] = log_norm
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
            str(outdir / "ranked.h5ad"),
            "--output-table",
            str(outdir / "markers.tsv"),
            "--group-sizes-json",
            str(outdir / "group_sizes.json"),
            "--params-json",
            str(outdir / "params.json"),
            "--versions-json",
            str(outdir / "versions.json"),
            "--groupby",
            "leiden",
            "--expression-source",
            "layer",
            "--layer",
            "log1p_norm",
            "--method",
            "wilcoxon",
            "--n-genes",
            "3",
            "--key-added",
            "bioinfo_marker_ranking",
        ]
        if extra_args:
            command.extend(extra_args)
        return subprocess.run(command, cwd=ROOT, env=env, text=True, capture_output=True, check=False)

    def test_marker_wrapper_writes_declared_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            fixture = tmp_path / "clustered.h5ad"
            self.make_fixture(fixture)

            result = self.run_wrapper(fixture, tmp_path)
            self.assertEqual(result.returncode, 0, result.stderr)

            markers = pd.read_csv(tmp_path / "markers.tsv", sep="\t")
            params = json.loads((tmp_path / "params.json").read_text())
            group_sizes = json.loads((tmp_path / "group_sizes.json").read_text())
            versions = json.loads((tmp_path / "versions.json").read_text())
            ranked = sc.read_h5ad(tmp_path / "ranked.h5ad")

            self.assertIn("bioinfo_marker_ranking", ranked.uns)
            self.assertIn("bioinfo_skills", ranked.uns)
            self.assertEqual(params["expression_source"], "layer")
            self.assertEqual(params["layer"], "log1p_norm")
            self.assertEqual(group_sizes["groups"], {"0": 3, "1": 3})
            self.assertIn("scanpy", versions["packages"])
            self.assertIn("group", markers.columns)
            self.assertIn("names", markers.columns)
            self.assertIn("expression_source", markers.columns)
            self.assertEqual(set(markers["expression_source"]), {"layer"})

    def test_marker_wrapper_fails_on_missing_groupby(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            fixture = tmp_path / "clustered.h5ad"
            self.make_fixture(fixture)

            result = self.run_wrapper(fixture, tmp_path, extra_args=["--groupby", "missing"])
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("groupby column not found", result.stderr)


if __name__ == "__main__":
    unittest.main()
