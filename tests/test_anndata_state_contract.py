import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from bioinfo_sdd.checks import run_check


class AnnDataStateContractTest(unittest.TestCase):
    def test_anndata_contract_check_passes(self):
        result = run_check("anndata_contract", ROOT)
        self.assertEqual(result.status, "pass", result.details)


if __name__ == "__main__":
    unittest.main()
