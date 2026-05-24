import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

HELPER_SKILLS = [
    "bioinfo-sdd-spec-section",
    "bioinfo-sdd-plan-section",
    "bioinfo-sdd-tasks-section",
    "bioinfo-sdd-evidence-section",
]

CONTRACT_TERMS = [
    "section.yml",
    "installed_refs",
    "tool_market",
    "bioinfo_tool",
    "spec_review",
    "plan_review",
    "task_review",
    "evidence_acceptance",
]


def _frontmatter(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise AssertionError(f"{path} missing YAML frontmatter delimited by ---")
    return match.group(1)


class BioinfoSddContractTest(unittest.TestCase):
    def test_templates_and_plan_preserve_contract_terms(self):
        paths = [
            ROOT / ".specify" / "templates" / "spec-template.md",
            ROOT / ".specify" / "templates" / "plan-template.md",
            ROOT / ".specify" / "templates" / "tasks-template.md",
            ROOT / "specs" / "001-speckit-usage-parity" / "plan.md",
        ]
        combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
        for term in CONTRACT_TERMS:
            with self.subTest(term=term):
                self.assertIn(term, combined)

    def test_bioinfo_helper_skills_have_frontmatter(self):
        for skill_name in HELPER_SKILLS:
            with self.subTest(skill=skill_name):
                path = ROOT / ".agents" / "skills" / skill_name / "SKILL.md"
                self.assertTrue(path.is_file(), path)
                frontmatter = _frontmatter(path)
                self.assertIn(f'name: "{skill_name}"', frontmatter)
                self.assertIn("description:", frontmatter)


if __name__ == "__main__":
    unittest.main()
