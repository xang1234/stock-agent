from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"
OPENAPI_PATH = ROOT / "spec" / "finance_research_openapi.yaml"
SQL_PATH = ROOT / "spec" / "finance_research_db_schema.sql"


class TruthEvidenceFindingContractTest(unittest.TestCase):
    def test_spec_declares_truth_evidence_role_rules(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 4.3.1 Truth and evidence role rules", spec_text)
        self.assertIn("Documents are evidence, not truth.", spec_text)
        self.assertIn(
            "### 6.4.1 Downstream consumer rules for truth and evidence objects",
            spec_text,
        )
        self.assertIn(
            "Home feed consumes Finding, SnapshotManifest, and ClaimCluster",
            spec_text,
        )

    def test_openapi_describes_truth_and_finding_roles(self) -> None:
        openapi_text = OPENAPI_PATH.read_text()
        self.assertIn("Facts are the unit of truth for displayed values.", openapi_text)
        self.assertIn(
            "Claims are extracted assertions from evidence, not canonical truth.",
            openapi_text,
        )
        self.assertIn(
            "Findings are snapshotted product artifacts built from evidence graph objects.",
            openapi_text,
        )

    def test_sql_notes_preserve_provenance_and_snapshot_rules(self) -> None:
        sql_text = SQL_PATH.read_text()
        self.assertIn(
            "facts are immutable except through supersession or invalidation", sql_text
        )
        self.assertIn(
            "claims remain evidence-layer assertions rather than canonical truth",
            sql_text,
        )
        self.assertIn(
            "findings must point at a sealed snapshot and remain user-facing artifacts",
            sql_text,
        )


if __name__ == "__main__":
    unittest.main()
