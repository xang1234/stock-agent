from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"


class SymbolSearchQuoteSnapshotSurfaceContractTest(unittest.TestCase):
    def test_spec_declares_shell_owned_search_entry_and_navigation(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 3.12 Symbol search and quote snapshot surface", spec_text)
        self.assertIn(
            "The persistent workspace shell owns the primary symbol search entry rather than delegating search behavior to each surface.",
            spec_text,
        )
        self.assertIn(
            "Later flows such as add-to-watchlist or portfolio entry reuse the same shell-owned search contract rather than redefining symbol search per surface.",
            spec_text,
        )
        self.assertIn(
            "Candidate handling reuses the existing search-to-subject flow: unique deterministic hits may auto-advance, ambiguous hits require explicit choice, and `not_found` ends without subject hydration.",
            spec_text,
        )
        self.assertIn(
            "A successful subject resolution enters symbol detail rather than opening a detached quote page or staying inline in the originating workspace.",
            spec_text,
        )
        self.assertIn(
            "The main canvas swaps into the entered subject-detail shell while preserving the surrounding workspace shell.",
            spec_text,
        )
        self.assertIn(
            "The first quote snapshot is the initial landing state of entered symbol detail rather than a competing top-level workspace.",
            spec_text,
        )

    def test_spec_declares_thin_quote_snapshot_minimum(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "The required landing content is a market identity strip plus a price-first quote snapshot.",
            spec_text,
        )
        self.assertIn(
            "That minimum quote snapshot includes canonical subject display identity, listing-sensitive trading symbol context, latest price, absolute move, percentage move, freshness or session state, and a small recent-range or chart hook.",
            spec_text,
        )
        self.assertIn(
            "Quote retrieval is listing-oriented even when the hydrated subject bundle also carries issuer context.",
            spec_text,
        )
        self.assertIn(
            "A light issuer summary or profile companion is allowed when available, but it is best-effort and must not block the landing state.",
            spec_text,
        )
        self.assertIn(
            "This bead does not define earnings, holders, filings, peer tables, or a finished overview surface.",
            spec_text,
        )

    def test_spec_declares_downstream_consumers_for_early_symbol_entry(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "### 3.13 Downstream consumer rules for early symbol entry work",
            spec_text,
        )
        self.assertIn(
            "Manual watchlist management baseline (`P0.4b`) depends on the reusable search entry and selected-subject handoff that manual watchlist actions will sit on top of.",
            spec_text,
        )
        self.assertIn(
            "Portfolio and watchlist basics (`P1.5`) depends on the first quote and subject-entry behavior that later portfolio and watchlist basics reuse before overlays exist.",
            spec_text,
        )
        self.assertIn(
            "Symbol overview shell (`P1.3`) depends on entered symbol detail having a thin initial landing state before fuller overview, financials, and earnings composition is defined.",
            spec_text,
        )


if __name__ == "__main__":
    unittest.main()
