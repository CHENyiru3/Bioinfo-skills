import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class AnnDataStateContractTest(unittest.TestCase):
    def test_anndata_contract_check_passes(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/check_anndata_contract.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
