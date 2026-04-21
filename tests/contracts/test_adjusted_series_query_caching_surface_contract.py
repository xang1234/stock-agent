from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"


class AdjustedSeriesQueryCachingSurfaceContractTest(unittest.TestCase):
    def test_spec_declares_adjusted_series_identity_and_basis_rules(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 6.2.3 Adjusted series query and caching semantics", spec_text)
        self.assertIn(
            "Adjusted series query is the market-data surface above raw bar retrieval that produces comparison-ready or interactive time series from canonical listing subject input.",
            spec_text,
        )
        self.assertIn(
            "Series queries bind explicit `subject_refs`, `range`, `interval`, `basis`, and `normalization` before execution, caching, and snapshot binding.",
            spec_text,
        )
        self.assertIn(
            "Market-series basis remains explicit: `unadjusted`, `split_adjusted`, and `split_and_div_adjusted`.",
            spec_text,
        )
        self.assertIn(
            "The service must not silently mix bases inside one returned series set, one chart artifact, or one comparison response.",
            spec_text,
        )
        self.assertIn(
            "Series responses expose the effective coverage window and any partial or unavailable history explicitly rather than backfilling missing periods or implying full coverage.",
            spec_text,
        )

    def test_spec_declares_cache_assumptions_and_snapshot_safe_reuse(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "Cache is an internal optimization behind the market data service, not a separate semantic source of truth for charts, symbol tabs, or blocks.",
            spec_text,
        )
        self.assertIn(
            "Cache identity includes the canonical subject set, range, interval, basis, normalization, and freshness boundary used for the series request.",
            spec_text,
        )
        self.assertIn(
            "A cache hit may reuse prior series material only when the request preserves subject membership, basis, normalization, and does not require data newer than the request or snapshot `as_of`.",
            spec_text,
        )
        self.assertIn(
            "If basis, normalization, peer set, or freshness changes, the system treats that as a different series request and refreshes or recomputes rather than mutating a cached answer in place.",
            spec_text,
        )
        self.assertIn(
            "In-snapshot transforms may reuse cached series only when the requested range or interval is already legal under the sealed snapshot manifest and remains inside `allowed_transforms`.",
            spec_text,
        )
        self.assertIn(
            "Changing basis or normalization is out-of-snapshot behavior even if compatible cached material exists somewhere in storage.",
            spec_text,
        )

    def test_spec_declares_adjusted_series_downstream_consumers(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "### 6.2.4 Downstream consumer rules for adjusted series query and caching",
            spec_text,
        )
        self.assertIn(
            "Symbol detail surfaces (`P1.3`) depends on explicit basis and coverage semantics so price charts and comparison modules do not silently switch between adjusted and unadjusted histories.",
            spec_text,
        )
        self.assertIn(
            "Block registry and initial block catalog (`P2.3`) depends on stable series query identity and in-snapshot cache reuse rules so interactive blocks know which transforms are legal without redefining market semantics per block kind.",
            spec_text,
        )
        self.assertIn(
            "Specialized social and news blocks (`P4.6`) depends on the same series semantics and cache contract for trend-style blocks so source-specific renderers reuse shared market rules rather than inventing bespoke chart caching behavior.",
            spec_text,
        )
        self.assertIn(
            "Non US identity data and coverage gaps (`P6.2`) depends on explicit basis, coverage-window, and partial-history rules so later international work can surface venue and provider differences without pretending uniform history quality.",
            spec_text,
        )
        self.assertIn(
            "Scale hardening (`P6.5`) depends on the declared cache identity and refresh rules so audits and ops work optimize hit rate and storage layout without weakening snapshot correctness.",
            spec_text,
        )


if __name__ == "__main__":
    unittest.main()
