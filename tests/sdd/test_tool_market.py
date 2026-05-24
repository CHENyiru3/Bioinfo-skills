import shutil
import tempfile
import unittest
from pathlib import Path

from bioinfo_sdd.checks import run_check
from bioinfo_sdd.installed_refs import install_tool_bundle, replace_tool_bundle, uninstall_tool_bundle
from bioinfo_sdd.market import bundles_for_task, load_bundle, validate_market
from bioinfo_sdd.models import load_section


ROOT = Path(__file__).resolve().parents[2]
SECTION = ROOT / "sdd/sections/scrna_graph_clustering_m1"
GRAPH_BUNDLE = "scrna.scverse.bundle.scanpy_graph_clustering.v0"
MARKER_BUNDLE = "scrna.scverse.bundle.scanpy_marker_ranking.v0"


class ToolMarketTest(unittest.TestCase):
    def section_copy(self, tmp: str) -> Path:
        target = Path(tmp) / "scrna_graph_clustering_m1"
        shutil.copytree(SECTION, target)
        shutil.rmtree(target / "installed_refs", ignore_errors=True)
        section = load_section(target)
        section.data["package_refs"] = []
        section.data["tool_refs"] = []
        section.data["wrapper"] = None
        section.data["adapter"] = None
        from bioinfo_sdd.io import write_yaml

        write_yaml(section.path, section.data)
        return target

    def test_market_manifest_validates(self):
        self.assertEqual(validate_market(ROOT), [])

    def test_market_lists_bundles_for_task(self):
        bundles = bundles_for_task(ROOT, "scrna.scverse.task.graph_clustering.v0")
        self.assertIn(GRAPH_BUNDLE, bundles)
        self.assertEqual(load_bundle(ROOT, GRAPH_BUNDLE).data["wrapper"], "wrappers/python/scanpy_neighbors_umap_leiden.py")

    def test_install_bundle_creates_section_revision_and_fills_slots(self):
        with tempfile.TemporaryDirectory() as tmp:
            section = self.section_copy(tmp)
            manifest = install_tool_bundle(ROOT, section, GRAPH_BUNDLE)
            self.assertTrue((section / manifest["packages"][0]["installed_path"]).exists())
            self.assertEqual(run_check("installed_refs", ROOT, section).status, "pass")
            self.assertEqual(run_check("task_slots_filled", ROOT, section).status, "pass")
            self.assertEqual(run_check("section_catalog_links", ROOT, section).status, "pass")

    def test_section_without_installed_refs_fails_concrete_resolution(self):
        with tempfile.TemporaryDirectory() as tmp:
            section = self.section_copy(tmp)
            self.assertEqual(run_check("task_slots_filled", ROOT, section).status, "fail")
            self.assertEqual(run_check("section_catalog_links", ROOT, section).status, "pass")

    def test_section_declared_tool_refs_fail_without_installed_refs(self):
        with tempfile.TemporaryDirectory() as tmp:
            section = Path(tmp) / "scrna_graph_clustering_m1"
            shutil.copytree(SECTION, section)
            shutil.rmtree(section / "installed_refs", ignore_errors=True)
            self.assertEqual(run_check("section_catalog_links", ROOT, section).status, "fail")

    def test_replace_preserves_previous_revision(self):
        with tempfile.TemporaryDirectory() as tmp:
            section = self.section_copy(tmp)
            first = install_tool_bundle(ROOT, section, GRAPH_BUNDLE)
            second = replace_tool_bundle(ROOT, section, GRAPH_BUNDLE)
            self.assertNotEqual(first["revision_id"], second["revision_id"])
            self.assertTrue((section / "installed_refs/revisions" / first["revision_id"]).exists())
            self.assertTrue((section / "installed_refs/revisions" / second["revision_id"]).exists())

    def test_uninstall_deactivates_without_deleting_revision(self):
        with tempfile.TemporaryDirectory() as tmp:
            section = self.section_copy(tmp)
            manifest = install_tool_bundle(ROOT, section, GRAPH_BUNDLE)
            selection = uninstall_tool_bundle(ROOT, section, GRAPH_BUNDLE)
            self.assertIsNone(selection["active_revision"])
            self.assertTrue((section / "installed_refs/revisions" / manifest["revision_id"]).exists())


if __name__ == "__main__":
    unittest.main()
