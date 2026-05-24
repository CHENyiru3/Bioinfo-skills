import os
import subprocess
import sys
import tempfile
import unittest
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MISSING = [
    package
    for package in ["snakemake", "anndata", "numpy", "pandas", "scanpy"]
    if importlib.util.find_spec(package) is None
]


class MarkerRankingWorkflowTest(unittest.TestCase):
    @unittest.skipIf(MISSING, "missing optional workflow dependencies: " + ", ".join(MISSING))
    def test_marker_ranking_snakemake_execution(self):
        import anndata as ad
        import numpy as np
        import pandas as pd
        import scanpy as sc

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            fixture = tmp_path / "clustered.h5ad"
            counts = np.array(
                [
                    [10, 1, 0, 0],
                    [9, 1, 0, 1],
                    [0, 0, 9, 1],
                    [1, 0, 10, 0],
                ],
                dtype=np.int64,
            )
            adata = ad.AnnData(
                X=np.log1p(counts.astype(float)),
                obs=pd.DataFrame({"leiden": pd.Categorical(["0", "0", "1", "1"])}, index=[f"cell{i}" for i in range(4)]),
                var=pd.DataFrame(index=[f"gene{i}" for i in range(4)]),
            )
            adata.layers["log1p_norm"] = adata.X.copy()
            adata.write_h5ad(fixture)

            config = tmp_path / "config.yml"
            config.write_text(
                "\n".join(
                    [
                        'schema_version: "0.1.0"',
                        "input_h5ad: " + str(fixture),
                        "outputs:",
                        "  h5ad: " + str(tmp_path / "out.h5ad"),
                        "  markers_tsv: " + str(tmp_path / "markers.tsv"),
                        "  group_sizes_json: " + str(tmp_path / "group_sizes.json"),
                        "  params_json: " + str(tmp_path / "params.json"),
                        "  versions_json: " + str(tmp_path / "versions.json"),
                        "logs:",
                        "  marker_ranking: " + str(tmp_path / "marker_ranking.log"),
                        "benchmarks:",
                        "  marker_ranking: " + str(tmp_path / "marker_ranking.tsv"),
                        "params:",
                        "  groupby: leiden",
                        "  expression_source: layer",
                        "  layer: log1p_norm",
                        "  method: wilcoxon",
                        "  reference: rest",
                        "  n_genes: 3",
                        "  key_added: bioinfo_marker_ranking",
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
            ranked = sc.read_h5ad(tmp_path / "out.h5ad")
            markers = pd.read_csv(tmp_path / "markers.tsv", sep="\t")
            params = json.loads((tmp_path / "params.json").read_text())
            self.assertIn("bioinfo_marker_ranking", ranked.uns)
            self.assertGreater(len(markers), 0)
            self.assertEqual(params["groupby"], "leiden")


if __name__ == "__main__":
    unittest.main()
