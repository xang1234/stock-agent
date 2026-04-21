from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"


class QuoteBarProviderAbstractionContractTest(unittest.TestCase):
    def test_spec_declares_provider_neutral_market_data_boundary(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 6.2.1 Quote and bar provider abstraction", spec_text)
        self.assertIn(
            "Market data service is the sole internal boundary for quote and bar provider interaction.",
            spec_text,
        )
        self.assertIn(
            "Downstream consumers call the market data service or analyst tools rather than provider SDKs, raw provider endpoints, or provider-specific payload helpers.",
            spec_text,
        )
        self.assertIn(
            "Quote and bar retrieval start from listing-appropriate hydrated subject context or a listing `SubjectRef`, not from raw ticker strings, venue text, or provider identifiers standing in for canonical market identity.",
            spec_text,
        )
        self.assertIn(
            "Provider adapters normalize provider-specific response shapes, identifiers, rate limits, and availability quirks into stable internal market records before those records reach downstream consumers.",
            spec_text,
        )
        self.assertIn(
            "The provider-neutral contract preserves `as_of`, `delay_class`, `currency`, and `source_id` for quote and bar retrieval, plus `adjustment_basis` whenever a bar response has already crossed an adjustment boundary.",
            spec_text,
        )

    def test_spec_declares_quote_and_bar_responsibilities(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "Quote retrieval owns the latest listing-oriented market snapshot for a tradable subject.",
            spec_text,
        )
        self.assertIn(
            "The normalized quote contract covers latest price, absolute move, percentage move, freshness or session state, `as_of`, `delay_class`, `currency`, and `source_id`.",
            spec_text,
        )
        self.assertIn(
            "Quote retrieval is lightweight and snapshot-oriented; it does not answer historical range questions, adjusted-series questions, or comparison normalization.",
            spec_text,
        )
        self.assertIn(
            "Bar retrieval owns ordered intraday and historical OHLCV series for a listing-oriented subject across a requested range and interval.",
            spec_text,
        )
        self.assertIn(
            "The normalized bar contract exposes requested subject identity, range, interval, `as_of`, `delay_class`, `currency`, `source_id`, and `adjustment_basis`.",
            spec_text,
        )
        self.assertIn(
            "Comparison charts, adjusted-series APIs, and snapshot-safe transform rules consume this bar contract later rather than bypassing it with provider-specific chart fetches.",
            spec_text,
        )

    def test_spec_declares_provider_abstraction_downstream_consumers(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "### 6.2.2 Downstream consumer rules for quote and bar provider abstraction",
            spec_text,
        )
        self.assertIn(
            "Adjusted series query and caching surface (`P1.1b`) depends on the provider-neutral quote and bar boundary, normalized market metadata fields, and the explicit split between snapshot reads and ordered time-series retrieval.",
            spec_text,
        )
        self.assertIn(
            "Symbol detail surfaces (`P1.3`) depends on a stable quote snapshot contract and reusable bar retrieval boundary so symbol modules do not embed provider-specific market fetch logic.",
            spec_text,
        )
        self.assertIn(
            "Pre-resolve router and budget policy (`P2.2`) depends on the distinction between lightweight quote reads and heavier historical-bar reads so routing and budget policy can choose the right market-data cost class without guessing from provider names or ticker text.",
            spec_text,
        )
        self.assertIn(
            "Scale hardening (`P6.5`) depends on a provider-neutral market-data seam with explicit freshness and source metadata so bottleneck audits, caching, and hardening work optimize the boundary rather than coupling consumers to one upstream vendor.",
            spec_text,
        )


if __name__ == "__main__":
    unittest.main()
