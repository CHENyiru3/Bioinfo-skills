import unittest
from pathlib import Path

from bioinfo_sdd.checks import run_check
from bioinfo_sdd.models import validate_section_file


ROOT = Path(__file__).resolve().parents[2]
SECTION = ROOT / "sdd/sections/scrna_graph_clustering_m1"


class SectionSchemaTest(unittest.TestCase):
    def test_graph_clustering_section_schema_validates(self):
        self.assertEqual(validate_section_file(SECTION), [])

    def test_graph_clustering_section_resolves_pack_catalog_links(self):
        result = run_check("section_catalog_links", ROOT, SECTION)
        self.assertEqual(result.status, "pass", result.details)
        self.assertEqual(result.details["pack_refs"], ["scrna.scverse.core"])
        self.assertEqual(result.details["task_refs"], ["scrna.scverse.task.graph_clustering.v0"])


if __name__ == "__main__":
    unittest.main()
