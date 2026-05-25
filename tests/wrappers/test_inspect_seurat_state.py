import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def relocated_r() -> tuple[Path | None, dict[str, str]]:
    env_prefix = ROOT.parent / "seurat_tutorial" / "conda_env"
    r_home = env_prefix / "lib" / "R"
    r_exec = r_home / "bin" / "exec" / "R"
    if not r_exec.exists():
        return None, {}
    return r_exec, {
        "R_HOME": str(r_home),
        "R_SHARE_DIR": str(r_home / "share"),
        "R_INCLUDE_DIR": str(r_home / "include"),
        "R_DOC_DIR": str(r_home / "doc"),
        "LD_LIBRARY_PATH": str(env_prefix / "lib"),
    }


class InspectSeuratStateTest(unittest.TestCase):
    def test_wrapper_reports_seurat_state(self):
        r_exec, r_env = relocated_r()
        if r_exec is None:
            self.skipTest("missing local relocated R runtime")
        env = {**os.environ, **r_env}
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            input_rds = tmpdir / "toy.rds"
            output_json = tmpdir / "state.json"
            output_md = tmpdir / "state.md"
            versions_json = tmpdir / "versions.json"
            create = (
                "suppressPackageStartupMessages(library(Seurat)); "
                "set.seed(1); "
                "counts <- matrix(rpois(120, lambda=3), nrow=12); "
                "rownames(counts) <- paste0('gene', seq_len(12)); "
                "colnames(counts) <- paste0('cell', seq_len(10)); "
                "obj <- CreateSeuratObject(counts=counts, assay='RNA'); "
                f"saveRDS(obj, {json.dumps(str(input_rds))})"
            )
            subprocess.run(
                [str(r_exec), "--slave", "-e", create],
                cwd=ROOT,
                env=env,
                text=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            subprocess.run(
                [
                    str(r_exec),
                    "--slave",
                    "-f",
                    str(ROOT / "wrappers/r/inspect_seurat_state.R"),
                    "--args",
                    "--input-rds",
                    str(input_rds),
                    "--output-json",
                    str(output_json),
                    "--output-md",
                    str(output_md),
                    "--versions-json",
                    str(versions_json),
                ],
                cwd=ROOT,
                env=env,
                text=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            report = json.loads(output_json.read_text())
            self.assertEqual(report["object_type"], "Seurat")
            self.assertEqual(report["dimensions"]["cells"], 10)
            self.assertEqual(report["active_assay"], "RNA")
            self.assertEqual(report["assays"][0]["layers"], "counts")
            versions = json.loads(versions_json.read_text())
            self.assertIn("Seurat", versions["packages"])
            self.assertTrue(output_md.read_text().startswith("# Seurat State Inspection"))


if __name__ == "__main__":
    unittest.main()
