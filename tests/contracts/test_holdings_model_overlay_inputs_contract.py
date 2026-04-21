from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"


class HoldingsModelOverlayInputsContractTest(unittest.TestCase):
    def test_spec_declares_holdings_scope_and_base_currency(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "Watchlists support `manual`, `screen`, `agent`, `theme`, and `portfolio` modes. Portfolio is lightweight holdings tracking for overlay context and monitoring, not brokerage execution.",
            spec_text,
        )
        self.assertIn(
            "### 3.16 Portfolio holdings model and overlay inputs",
            spec_text,
        )
        self.assertIn(
            "Portfolio support remains lightweight research context: it tracks held exposure for overlays and monitoring, not brokerage execution, order management, tax lots, cash ledgers, or settlement workflows.",
            spec_text,
        )
        self.assertIn(
            "A portfolio owns one explicit `base_currency` that defines the reporting currency for holding cost assumptions and later overlay totals.",
            spec_text,
        )
        self.assertIn(
            "`base_currency` is a reporting and comparison assumption, not proof that the underlying listing trades in that currency and not a full FX accounting model.",
            spec_text,
        )
        self.assertIn(
            "Manual watchlists and holdings remain separate: saving a subject does not create a holding, and holding a subject does not implicitly add it to a watchlist.",
            spec_text,
        )

    def test_spec_declares_portfolio_holding_and_overlay_input_rules(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "### 4.2.1 Portfolio holding and overlay input rules",
            spec_text,
        )
        self.assertIn(
            "`Portfolio` is a user-owned research container, not a brokerage account surrogate.",
            spec_text,
        )
        self.assertIn(
            "`Portfolio.base_currency` is required and interprets `cost_basis` plus any portfolio-level overlay totals in one explicit reporting currency.",
            spec_text,
        )
        self.assertIn(
            "`PortfolioHolding` binds to canonical market identity, typically `instrument` or `listing`, and must not persist raw ticker strings or higher-order subjects such as `theme`, `macro_topic`, `portfolio`, or `screen` as holding identity.",
            spec_text,
        )
        self.assertIn(
            "`cost_basis` is optional and, when present, is interpreted in the containing portfolio's `base_currency`; this bead does not define separate transaction currencies, FX lots, or fee-adjusted basis accounting.",
            spec_text,
        )
        self.assertIn(
            "Overlay inputs derived from holdings are read models keyed by subject and contributing portfolio, not new canonical subject identities or stored UI payloads.",
            spec_text,
        )
        self.assertIn(
            "The minimum overlay input contract is held-state, contributing `portfolio_id`, quantity, optional cost basis context, and a base-currency label for any derived valuation or gain/loss display.",
            spec_text,
        )
        self.assertIn(
            "If multiple portfolios hold the same subject with different base currencies, this bead keeps those contributions distinct rather than silently netting them through an implicit FX layer.",
            spec_text,
        )

    def test_spec_declares_holdings_downstream_consumers(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "### 3.17 Downstream consumer rules for holdings model and overlay inputs",
            spec_text,
        )
        self.assertIn(
            "Portfolio and watchlist surface behaviors (`P1.5b`) depends on the lightweight holdings scope and explicit `base_currency` assumption so first-surface behaviors can render held-state and cost context without inventing brokerage rules.",
            spec_text,
        )
        self.assertIn(
            "Dynamic watchlists and portfolio overlays (`P4.7`) depends on holdings producing reusable overlay inputs rather than UI-owned ad hoc calculations so later overlay layers can merge portfolio context with watchlists, themes, screens, and subject views consistently.",
            spec_text,
        )


if __name__ == "__main__":
    unittest.main()
