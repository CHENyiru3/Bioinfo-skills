import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ScverseManifestCoverageTest(unittest.TestCase):
    def test_market_package_refs_have_required_frontmatter(self):
        refs = sorted((ROOT / "tool_market/packages").glob("**/*.md"))
        self.assertTrue(refs)
        offenders = []
        for ref in refs:
            if ref.name == "README.md":
                continue
            text = ref.read_text()
            if not text.startswith("---\n") or "\n---\n" not in text[4:]:
                offenders.append(f"{ref}: missing frontmatter")
                continue
            frontmatter = text[4 : text.find("\n---\n", 4)]
            for key in ["id:", "kind:", "package:", "language:", "ecosystem:", "runtime_status:"]:
                if key not in frontmatter:
                    offenders.append(f"{ref}: missing {key}")
        self.assertFalse(offenders)

    def test_runtime_report_placeholder_is_schema_shaped(self):
        report = json.loads((ROOT / "reports/runtime/scverse_runtime_status.json").read_text())
        self.assertIn("schema_version", report)
        self.assertIn("generated_at", report)
        self.assertIn("packages", report)
        self.assertIsInstance(report["packages"], list)

    def test_runtime_report_matches_market_package_refs(self):
        report = json.loads((ROOT / "reports/runtime/scverse_runtime_status.json").read_text())
        reported = {row["package"] for row in report["packages"]}
        refs = {
            ref.stem
            for ref in (ROOT / "tool_market/packages").glob("**/*.md")
            if ref.name != "README.md"
        }
        self.assertEqual(reported, refs)


if __name__ == "__main__":
    unittest.main()
