import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from bioinfo_sdd.checks import run_check


class SkillTreeStructureTest(unittest.TestCase):
    def test_skill_tree_validator_passes(self):
        result = run_check("skill_tree", ROOT)
        self.assertEqual(result.status, "pass", result.details)


if __name__ == "__main__":
    unittest.main()
