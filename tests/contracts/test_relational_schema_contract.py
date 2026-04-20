from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"
SQL_PATH = ROOT / "spec" / "finance_research_db_schema.sql"


class RelationalSchemaContractTest(unittest.TestCase):
    def test_spec_declares_schema_families_and_storage_split(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("## 6A. Relational schema contract", spec_text)
        self.assertIn("Reference and universe tables", spec_text)
        self.assertIn("Evidence-plane relational tables", spec_text)
        self.assertIn("App metadata and orchestration tables", spec_text)
        self.assertIn("Raw document bytes are outside the relational schema.", spec_text)
        self.assertIn(
            "Snapshots bridge the evidence plane to user-facing artifacts.",
            spec_text,
        )

    def test_sql_notes_declare_table_family_boundaries(self) -> None:
        sql_text = SQL_PATH.read_text()
        self.assertIn("Table families:", sql_text)
        self.assertIn(
            "reference and universe tables define reusable subject context", sql_text
        )
        self.assertIn(
            "evidence-plane relational tables hold provenance, facts, claims, events, and snapshots",
            sql_text,
        )
        self.assertIn(
            "app metadata and orchestration tables support user state and workflow coordination",
            sql_text,
        )
        self.assertIn("raw document bytes live outside the relational schema", sql_text)


if __name__ == "__main__":
    unittest.main()
