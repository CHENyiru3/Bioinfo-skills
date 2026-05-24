import json
import os
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CORE_SKILLS = [
    "speckit-constitution",
    "speckit-specify",
    "speckit-clarify",
    "speckit-checklist",
    "speckit-plan",
    "speckit-tasks",
    "speckit-analyze",
    "speckit-implement",
]


def _frontmatter(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise AssertionError(f"{path} missing YAML frontmatter delimited by ---")
    return match.group(1)


class CodexSkillContractTest(unittest.TestCase):
    def test_core_speckit_skills_exist_with_frontmatter(self):
        for skill_name in CORE_SKILLS:
            with self.subTest(skill=skill_name):
                path = ROOT / ".agents" / "skills" / skill_name / "SKILL.md"
                self.assertTrue(path.is_file(), path)
                frontmatter = _frontmatter(path)
                self.assertIn(f'name: "{skill_name}"', frontmatter)
                self.assertIn("description:", frontmatter)
                text = path.read_text(encoding="utf-8")
                self.assertIn("## Bioinfo SDD Contract", text)

    def test_active_feature_pointer_resolves_required_artifacts(self):
        pointer_path = ROOT / ".specify" / "feature.json"
        pointer = json.loads(pointer_path.read_text(encoding="utf-8"))
        feature_directory = pointer.get("feature_directory")
        self.assertEqual(feature_directory, "specs/001-speckit-usage-parity")

        feature_path = ROOT / feature_directory
        self.assertTrue(feature_path.is_dir(), feature_path)
        for artifact in ["spec.md", "plan.md", "tasks.md"]:
            with self.subTest(artifact=artifact):
                self.assertTrue((feature_path / artifact).is_file())

    def test_agents_context_points_to_active_plan(self):
        text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("<!-- SPECKIT START -->", text)
        self.assertIn("<!-- SPECKIT END -->", text)
        self.assertIn("specs/001-speckit-usage-parity/plan.md", text)

    def test_prerequisites_use_feature_json_before_branch_fallback(self):
        result = subprocess.run(
            [
                str(ROOT / ".specify" / "scripts" / "bash" / "check-prerequisites.sh"),
                "--json",
                "--require-tasks",
                "--include-tasks",
            ],
            cwd=ROOT,
            env={**os.environ, "SPECIFY_FEATURE": "main"},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(
            payload["FEATURE_DIR"],
            str(ROOT / "specs" / "001-speckit-usage-parity"),
        )


if __name__ == "__main__":
    unittest.main()
