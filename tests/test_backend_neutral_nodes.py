import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATTERNS = [
    r"^\s*rule\s+\w+",
    r"\bSnakefile\b",
    r"\bwildcards\b",
    r"\bsnakemake\.",
    r"^\s*process\s+\w+",
]


class BackendNeutralNodesTest(unittest.TestCase):
    def test_workflow_skill_nodes_are_backend_neutral(self):
        offenders = []
        workflow_roots = [
            ROOT / "skills/scrna/scverse/workflow",
            ROOT / "skills/scrna/seurat/workflow",
        ]
        paths = [path for root in workflow_roots for path in root.glob("*/SKILL.md")]
        self.assertTrue(paths)
        for path in paths:
            text = path.read_text()
            for pattern in PATTERNS:
                if re.search(pattern, text, flags=re.MULTILINE):
                    offenders.append(f"{path}: {pattern}")
        self.assertFalse(offenders)


if __name__ == "__main__":
    unittest.main()
