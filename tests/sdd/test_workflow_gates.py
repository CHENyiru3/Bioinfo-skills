import shutil
import tempfile
import unittest
from pathlib import Path

from bioinfo_sdd.sections import update_gate
from bioinfo_sdd.workflow import WorkflowRunner


ROOT = Path(__file__).resolve().parents[2]
SECTION = ROOT / "sdd/sections/scrna_graph_clustering_m1"
WORKFLOW = ROOT / "sdd/workflows/section-sdd.yml"


class WorkflowGatesTest(unittest.TestCase):
    def test_workflow_pauses_at_pending_evidence_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            section_copy = Path(tmp) / "scrna_graph_clustering_m1"
            shutil.copytree(SECTION, section_copy)
            state = WorkflowRunner(ROOT, WORKFLOW, section_copy, "unit-test").run()
            self.assertEqual(state["status"], "paused")
            self.assertEqual(state["paused_gate"], "evidence_acceptance")
            self.assertTrue((section_copy / "runs/unit-test/checks/section_catalog_links.json").exists())

    def test_workflow_rejects_rejected_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            section_copy = Path(tmp) / "scrna_graph_clustering_m1"
            shutil.copytree(SECTION, section_copy)
            update_gate(section_copy, "evidence_acceptance", "rejected", "unit test rejection")
            state = WorkflowRunner(ROOT, WORKFLOW, section_copy, "unit-test-reject").run()
            self.assertEqual(state["status"], "rejected")
            self.assertEqual(state["rejected_gate"], "evidence_acceptance")


if __name__ == "__main__":
    unittest.main()
