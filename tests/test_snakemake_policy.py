import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SnakemakePolicyTest(unittest.TestCase):
    def test_snakemake_policy_check_passes(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/inspect_snakefile_policy.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
