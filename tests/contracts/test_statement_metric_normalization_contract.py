from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"


class StatementMetricNormalizationContractTest(unittest.TestCase):
    def test_spec_declares_statement_normalization_scope_and_basis(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 6.3.1 Statement and metric normalization", spec_text)
        self.assertIn(
            "Statement normalization is the fundamentals-service layer that turns filing-backed or vendor-backed statement inputs into canonical value objects keyed by metric definitions.",
            spec_text,
        )
        self.assertIn(
            "Statement reads begin from issuer-appropriate subject context rather than listing identity or ticker-only lookup.",
            spec_text,
        )
        self.assertIn(
            "The service normalizes the three core statement families explicitly: `income`, `balance`, and `cashflow`.",
            spec_text,
        )
        self.assertIn(
            "Statement basis remains explicit at the query and output boundary: `as_reported` and `as_restated` are different normalization modes and must not be silently merged.",
            spec_text,
        )
        self.assertIn(
            "Period selection, fiscal labels, scale normalization, and unit normalization are part of the statement-normalization contract rather than caller-specific cleanup work.",
            spec_text,
        )

    def test_spec_declares_metric_ownership_and_canonical_value_relation(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "`Metric` remains the canonical definition object for what can be measured, how a value is interpreted, and which source class a normalized value belongs to.",
            spec_text,
        )
        self.assertIn(
            "Fundamentals service owns the mapping from normalized statement lines into canonical metric definitions, but it does not turn `Metric` into a mutable value store.",
            spec_text,
        )
        self.assertIn(
            "Displayed statement values resolve to `Fact` rows when the value is directly observed or promoted as truth, and to `Computation` rows when the value is deterministically derived from structured inputs.",
            spec_text,
        )
        self.assertIn(
            "Statement normalization must not introduce a second truth layer made of UI-only statement cells or provider-specific blobs that bypass `Fact` and `Computation`.",
            spec_text,
        )
        self.assertIn(
            "When source material is incomplete, conflicting, or pending promotion, the service preserves coverage and verification state through canonical value objects rather than inventing complete normalized tables.",
            spec_text,
        )

    def test_spec_declares_statement_normalization_downstream_consumers(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "### 6.3.2 Downstream consumer rules for statement and metric normalization",
            spec_text,
        )
        self.assertIn(
            "Stats, segment, and consensus aggregations (`P1.2b`) depends on normalized issuer statement facts and canonical metric ownership so later aggregation families build on one shared value layer instead of restating statement normalization rules.",
            spec_text,
        )
        self.assertIn(
            "Symbol detail surfaces (`P1.3`) depends on normalized statement outputs carrying explicit basis, period, and coverage semantics so overview, financials, and earnings tabs can render trustworthy tables and charts.",
            spec_text,
        )
        self.assertIn(
            "Pre-resolve router and budget policy (`P2.2`) depends on the issuer-oriented normalization boundary so routing can distinguish fundamentals reads from market-data reads before the tool loop starts.",
            spec_text,
        )
        self.assertIn(
            "Promotion rules for candidate facts (`P3.5`) depends on the rule that normalized statement values become `Fact` or `Computation` objects rather than a separate fundamentals-only truth store, so promotion and supersession work target the canonical value plane.",
            spec_text,
        )
        self.assertIn(
            "Non US identity data and coverage gaps (`P6.2`) depends on explicit metric ownership, basis handling, and issuer-oriented normalization rules so later international work can extend accounting mappings without weakening the canonical value contract.",
            spec_text,
        )


if __name__ == "__main__":
    unittest.main()
