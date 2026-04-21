from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"


class PortfolioWatchlistSurfaceBehaviorsContractTest(unittest.TestCase):
    def test_spec_declares_shared_quote_row_behavior(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "### 3.18 Portfolio and watchlist first surface behaviors",
            spec_text,
        )
        self.assertIn(
            "Manual watchlist and portfolio-held surfaces reuse the same thin quote-on-read row hydration contract rather than inventing separate quote-fetch behavior for held subjects.",
            spec_text,
        )
        self.assertIn(
            "Portfolio-held rows layer held-state context, quantity, and optional cost-basis context on top of that shared quote row skeleton.",
            spec_text,
        )
        self.assertIn(
            "The first surface behavior stays intentionally light: it does not define a portfolio analytics dashboard, brokerage position card, or private quote model distinct from symbol entry.",
            spec_text,
        )
        self.assertIn(
            "If a subject is both watchlisted and held, the surface keeps both states visible rather than collapsing one concept into the other.",
            spec_text,
        )

    def test_spec_declares_subject_view_augmentation_rules(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "Selecting a row from either a watchlist or portfolio-held surface enters the same symbol-detail route keyed by canonical subject identity.",
            spec_text,
        )
        self.assertIn(
            "Entered subject views may show lightweight saved-state and held-state context plus adjacent actions, but that context augments the existing quote snapshot and subject modules rather than creating a portfolio-specific subject shell.",
            spec_text,
        )
        self.assertIn(
            "Watchlist and holdings state remain user-owned overlay context on top of shared subject and market-data contracts.",
            spec_text,
        )

    def test_spec_declares_surface_behavior_downstream_consumers(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "### 3.19 Downstream consumer rules for portfolio and watchlist surface behaviors",
            spec_text,
        )
        self.assertIn(
            "Dynamic watchlists and portfolio overlays (`P4.7`) depends on shared quote-row behavior and stable subject-view augmentation so later theme, screen, portfolio, and watchlist combinations can add more context without rewriting the base surfaces.",
            spec_text,
        )
        self.assertIn(
            "Export and share policy (`P6.4`) depends on user-owned watchlist and holdings context staying visually and semantically distinct from canonical quote and subject content so later export or share rules can reason about what private overlay state may travel with a shared artifact.",
            spec_text,
        )


if __name__ == "__main__":
    unittest.main()
