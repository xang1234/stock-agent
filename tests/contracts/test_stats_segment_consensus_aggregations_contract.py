from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"


class StatsSegmentConsensusAggregationsContractTest(unittest.TestCase):
    def test_spec_declares_aggregation_boundary_and_families(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 6.3.3 Stats, segment, and consensus aggregations", spec_text)
        self.assertIn(
            "The fundamentals aggregation layer sits above normalized statement facts and canonical metrics and produces reusable read models for key stats, segment facts, analyst consensus, and comparison-ready derived outputs.",
            spec_text,
        )
        self.assertIn(
            "Aggregation outputs are service-level views, not replacements for canonical `Fact` or `Computation` rows, and they must keep their derivation inputs, freshness, and coverage assumptions explicit.",
            spec_text,
        )
        self.assertIn(
            "Key stats and derived ratios may combine normalized fundamentals, market context, and deterministic computations, but they must expose the basis, period, and `as_of` assumptions needed to explain each value.",
            spec_text,
        )
        self.assertIn(
            "Segment facts remain distinct from consolidated statement outputs: they carry segment axis, segment definitions, period context, and coverage warnings instead of flattening segment disclosures into issuer-level statement tables.",
            spec_text,
        )
        self.assertIn(
            "Analyst consensus remains distinct from both reported statements and promoted evidence facts: rating distributions, price-target summaries, analyst counts, and coverage warnings are service-level aggregates with explicit `as_of` semantics.",
            spec_text,
        )
        self.assertIn(
            "Comparison-ready derived outputs may package reusable aggregate slices for peer views or ranking-style surfaces, but they must not become an opaque cache of UI-specific payloads.",
            spec_text,
        )

    def test_spec_declares_aggregation_warning_and_ownership_rules(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "When aggregation inputs are incomplete, stale, or inconsistent, the service surfaces warnings and partial-coverage metadata instead of fabricating complete comparisons or silently filling gaps.",
            spec_text,
        )
        self.assertIn(
            "The aggregation layer may read canonical facts, computations, and provider-backed consensus or segment inputs, but provenance, supersession, and truth-promotion state remain owned by the canonical value plane.",
            spec_text,
        )

    def test_spec_declares_aggregation_downstream_consumers(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "### 6.3.4 Downstream consumer rules for aggregation outputs",
            spec_text,
        )
        self.assertIn(
            "Symbol detail surfaces (`P1.3`) depends on separate stats, segment, and consensus aggregation families so overview, financials, and earnings modules can reuse deterministic read models instead of rebuilding UI-specific payloads from raw statements.",
            spec_text,
        )
        self.assertIn(
            "Pre-resolve router and budget policy (`P2.2`) depends on the distinction between normalized statement reads and aggregation-layer reads so routing can classify heavier fundamentals requests before the tool loop starts.",
            spec_text,
        )
        self.assertIn(
            "Specialized social and news blocks (`P4.6`) depends on reusable key stats and consensus outputs so narrative product blocks can cite stable aggregate envelopes without embedding ad hoc ratio or target-calculation logic.",
            spec_text,
        )
        self.assertIn(
            "Segment extraction refinement (`P6.1`) depends on segment aggregates preserving axis, definition, and coverage-warning semantics so harder extraction cases can evolve without changing the consumer-facing aggregation contract.",
            spec_text,
        )
        self.assertIn(
            "Non US identity data and coverage gaps (`P6.2`) depends on aggregation outputs keeping basis, freshness, and coverage assumptions explicit so later international expansion can widen issuer and provider coverage without pretending the aggregates are uniformly comparable.",
            spec_text,
        )


if __name__ == "__main__":
    unittest.main()
