from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"
OPENAPI_PATH = ROOT / "spec" / "finance_research_openapi.yaml"
SQL_PATH = ROOT / "spec" / "finance_research_db_schema.sql"


class IdentitySubjectContractTest(unittest.TestCase):
    def test_spec_declares_canonical_identity_rules(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 4.1.1 Canonical identity rules", spec_text)
        self.assertIn(
            "ticker is a listing attribute and lookup handle, not canonical identity",
            spec_text,
        )
        self.assertIn("### 6.1.1 Downstream consumer rules", spec_text)
        self.assertIn("Chat and Analyze persist subject context as SubjectRef[]", spec_text)

    def test_openapi_describes_subject_ref_identity_boundary(self) -> None:
        openapi_text = OPENAPI_PATH.read_text()
        self.assertIn("Ticker is a listing locator, not canonical identity.", openapi_text)
        self.assertIn(
            "kind determines whether the id points to an issuer, instrument, listing",
            openapi_text,
        )

    def test_sql_notes_preserve_ticker_boundary(self) -> None:
        sql_text = SQL_PATH.read_text()
        self.assertIn("ticker is a listing locator, not canonical identity", sql_text)
        self.assertIn(
            "issuer = reporting entity; instrument = tradable security definition; listing = venue-specific symbol",
            sql_text,
        )


if __name__ == "__main__":
    unittest.main()
