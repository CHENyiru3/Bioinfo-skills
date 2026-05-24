import json
import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

MISSING = [
    package
    for package in ["anndata", "numpy", "pandas", "scipy"]
    if importlib.util.find_spec(package) is None
]
if not MISSING:
    import anndata as ad
    import numpy as np
    import pandas as pd
    from scipy import sparse


ROOT = Path(__file__).resolve().parents[2]
WRAPPER = ROOT / "wrappers/python/inspect_anndata_state.py"


@unittest.skipIf(MISSING, "missing optional wrapper dependencies: " + ", ".join(MISSING))
class InspectAnnDataStateTest(unittest.TestCase):
    def make_fixture(self, path: Path) -> None:
        counts = np.array(
            [
                [1, 0, 3],
                [0, 2, 1],
                [5, 0, 0],
                [0, 1, 4],
            ],
            dtype=np.int64,
        )
        obs = pd.DataFrame(
            {
                "sample_id": ["s1", "s1", "s2", "s2"],
                "batch": ["b1", "b1", "b2", "b2"],
                "leiden": pd.Categorical(["0", "0", "1", "1"]),
            },
            index=["cell1", "cell2", "cell3", "cell4"],
        )
        var = pd.DataFrame(
            {"gene_symbols": ["GeneA", "GeneB", "GeneC"]},
            index=["gene_a", "gene_b", "gene_c"],
        )
        log_norm = np.log1p(counts.astype(float))
        adata = ad.AnnData(X=log_norm, obs=obs, var=var)
        adata.layers["counts"] = counts
        adata.layers["log1p_norm"] = log_norm.copy()
        adata.raw = adata
        adata.obsm["X_pca"] = np.array(
            [
                [1.0, 0.1],
                [0.9, 0.2],
                [-0.8, 0.0],
                [-1.0, -0.2],
            ]
        )
        adata.obsp["connectivities"] = sparse.eye(adata.n_obs, format="csr")
        adata.uns["bioinfo_skills"] = {"fixture": "inspect_anndata_state"}
        adata.write_h5ad(path)

    def run_wrapper(self, fixture: Path, outdir: Path) -> subprocess.CompletedProcess:
        env = os.environ.copy()
        env.setdefault("MPLCONFIGDIR", str(outdir / "mpl"))
        env.setdefault("XDG_CACHE_HOME", str(outdir / "cache"))
        return subprocess.run(
            [
                sys.executable,
                str(WRAPPER),
                "--input-h5ad",
                str(fixture),
                "--output-json",
                str(outdir / "state.json"),
                "--output-md",
                str(outdir / "state.md"),
                "--versions-json",
                str(outdir / "versions.json"),
            ],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_wrapper_reports_state_without_writing_h5ad(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            fixture = tmp_path / "fixture.h5ad"
            self.make_fixture(fixture)

            result = self.run_wrapper(fixture, tmp_path)
            self.assertEqual(result.returncode, 0, result.stderr)

            report = json.loads((tmp_path / "state.json").read_text())
            versions = json.loads((tmp_path / "versions.json").read_text())
            markdown = (tmp_path / "state.md").read_text()

            self.assertEqual(report["shape"], [4, 3])
            self.assertIn("counts", report["slots"]["layers"])
            self.assertIn("log1p_norm", report["slots"]["layers"])
            self.assertTrue(report["slots"]["raw"]["present"])
            self.assertIn("X_pca", report["slots"]["obsm"])
            self.assertIn("connectivities", report["slots"]["obsp"])
            self.assertTrue(report["state_flags"]["has_counts_layer"])
            self.assertTrue(report["state_flags"]["has_log1p_norm_layer"])
            self.assertIn("scanpy", versions["packages"])
            self.assertIn("AnnData State Inspection", markdown)
            self.assertFalse((tmp_path / "output.h5ad").exists())


if __name__ == "__main__":
    unittest.main()
