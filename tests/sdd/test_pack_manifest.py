import unittest
from pathlib import Path

from bioinfo_sdd.packs import discover_packs, resolve_workflow, validate_pack_file


ROOT = Path(__file__).resolve().parents[2]


class PackManifestTest(unittest.TestCase):
    def test_scrna_scverse_pack_manifest_validates(self):
        pack_path = ROOT / "sdd/packs/scrna_scverse/pack.yml"
        self.assertEqual(validate_pack_file(pack_path, root=ROOT), [])

    def test_pack_resolves_default_workflow(self):
        workflow = resolve_workflow(
            ROOT,
            ["scrna.scverse.core"],
            "bioinfo.sdd.workflow.section_default.v0",
        )
        self.assertEqual(workflow, ROOT / "sdd/workflows/section-sdd.yml")

    def test_pack_exposes_graph_clustering_task_template(self):
        pack = discover_packs(ROOT)["scrna.scverse.core"]
        task = pack.task_templates()["scrna.scverse.task.graph_clustering.v0"]
        self.assertEqual(
            [slot["slot_id"] for slot in task["tool_slots"]],
            ["neighbor_graph", "embedding_visualization", "clustering"],
        )


if __name__ == "__main__":
    unittest.main()
