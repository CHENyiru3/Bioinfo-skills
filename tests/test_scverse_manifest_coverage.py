import json
import csv
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def _frontmatter(path: Path) -> dict:
    text = path.read_text()
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    return yaml.safe_load(text[4:end]) or {}


def _package_ref_stems(language: str, ecosystem: str) -> set[str]:
    refs = set()
    for ref in (ROOT / "tool_market/packages").glob("**/*.md"):
        if ref.name == "README.md":
            continue
        meta = _frontmatter(ref)
        if meta.get("language") == language and meta.get("ecosystem") == ecosystem:
            refs.add(ref.stem)
    return refs


def _reported_ref_stems(report_name: str) -> set[str]:
    report = json.loads((ROOT / "reports/runtime" / report_name).read_text())
    return {
        Path(row["ref_path"]).stem
        for row in report["packages"]
        if row.get("ref_path")
    }


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

    def test_runtime_reports_are_schema_shaped(self):
        report = json.loads((ROOT / "reports/runtime/scverse_runtime_status.json").read_text())
        self.assertIn("schema_version", report)
        self.assertIn("generated_at", report)
        self.assertIn("packages", report)
        self.assertIsInstance(report["packages"], list)
        report = json.loads((ROOT / "reports/runtime/seurat_runtime_status.json").read_text())
        self.assertIn("schema_version", report)
        self.assertIn("generated_at", report)
        self.assertIn("packages", report)
        self.assertIsInstance(report["packages"], list)
        self.assertIn("r_version", report)

    def test_missing_optional_source_route_packages_are_waived(self):
        report = json.loads((ROOT / "reports/runtime/seurat_runtime_status.json").read_text())
        offenders = []
        for row in report["packages"]:
            if row.get("status") == "missing" and row.get("declared_runtime_status") == "optional_missing":
                if not row.get("waiver_reason"):
                    offenders.append(row.get("package"))
        self.assertFalse(offenders)

    def test_runtime_reports_match_market_package_refs_by_ecosystem(self):
        self.assertEqual(
            _reported_ref_stems("scverse_runtime_status.json"),
            _package_ref_stems("python", "scverse"),
        )
        self.assertEqual(
            _reported_ref_stems("seurat_runtime_status.json"),
            _package_ref_stems("r", "seurat"),
        )

    def test_package_matrix_refs_exist(self):
        matrix = yaml.safe_load((ROOT / "envs/package-matrix.yml").read_text())
        self.assertEqual(matrix["schema_version"], "0.1.0")
        package_refs = {str(path.relative_to(ROOT)) for path in (ROOT / "tool_market/packages").glob("**/*.md")}
        skill_refs = {str(path.relative_to(ROOT)) for path in (ROOT / "skills").glob("**/SKILL.md")}
        for row in matrix["packages"]:
            with self.subTest(package=row["id"]):
                self.assertIn(row["package_ref"], package_refs)
                for skill_ref in row.get("skill_refs", []):
                    self.assertIn(skill_ref, skill_refs)
                for group in row.get("env_groups", []):
                    self.assertIn(group, matrix["environment_groups"])

    def test_seurat_source_route_packages_are_pinned(self):
        matrix = yaml.safe_load((ROOT / "envs/package-matrix.yml").read_text())
        source_rows = {
            row["package"]: row
            for row in matrix["packages"]
            if row.get("language") == "r"
            and row.get("ecosystem") == "seurat"
            and row.get("install_route") == "source"
        }
        lock_path = ROOT / "containers/lockfiles/r-seurat-source-packages.tsv"
        with lock_path.open(newline="", encoding="utf-8") as handle:
            lock_rows = {row["package"]: row for row in csv.DictReader(handle, delimiter="\t")}
        self.assertEqual(set(source_rows), set(lock_rows))
        for package, row in source_rows.items():
            with self.subTest(package=package):
                commit = row.get("source_commit")
                archive = row.get("source_archive")
                self.assertRegex(commit or "", r"^[0-9a-f]{40}$")
                self.assertIn(commit, archive or "")
                self.assertEqual(lock_rows[package]["commit"], commit)
                self.assertEqual(lock_rows[package]["archive_url"], archive)
        installer = (ROOT / "scripts/install_seurat_source_packages.R").read_text()
        self.assertNotIn("refs/heads", installer)


if __name__ == "__main__":
    unittest.main()
