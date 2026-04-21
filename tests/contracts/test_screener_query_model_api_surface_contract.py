from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"


class ScreenerQueryModelApiSurfaceContractTest(unittest.TestCase):
    def test_spec_declares_screener_query_model(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 6.7.1 Screener query model and result contract", spec_text)
        self.assertIn(
            "Screener queries are explicit structured filter-and-rank envelopes rather than a freeform analytics DSL or arbitrary user-authored formulas.",
            spec_text,
        )
        self.assertIn(
            "The minimum query dimensions are universe constraints, market or quote constraints, fundamentals or aggregate constraints, sort specification, and page or limit controls.",
            spec_text,
        )
        self.assertIn(
            "Query clauses bind to screener-owned fields backed by the market-data and fundamentals services rather than exposing raw provider payload columns or frontend-computed joins.",
            spec_text,
        )

    def test_spec_declares_screener_result_semantics_and_service_boundary(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "A screener response is an ordered derived result set rather than a new canonical identity type for returned entities.",
            spec_text,
        )
        self.assertIn(
            "Each result row carries canonical market subject identity, display identity, ranking or sort context, and compact quote or fundamentals summaries sufficient for screener-table rendering.",
            spec_text,
        )
        self.assertIn(
            "Screener rows remain thinner than symbol-detail hydration: selecting a row hands off canonical subject identity for later subject-entry flows rather than embedding a full symbol workspace payload.",
            spec_text,
        )
        self.assertIn(
            "A reusable `screen` subject represents the persisted query definition plus ordering semantics, not a frozen list of prehydrated row payloads.",
            spec_text,
        )
        self.assertIn(
            "The Screener service owns query validation, execution, ranking, pagination, and row-envelope assembly.",
            spec_text,
        )
        self.assertIn(
            "`/v1/screener/*` remains the client boundary for screener queries and results, even when the service internally reads market-data and fundamentals outputs.",
            spec_text,
        )
        self.assertIn(
            "Clients must not reconstruct screener tables by fanning out across `/v1/market/*` and `/v1/fundamentals/*` and inventing their own join semantics.",
            spec_text,
        )

    def test_spec_declares_screener_downstream_consumers(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 6.7.2 Downstream consumer rules for screener query work", spec_text)
        self.assertIn(
            "Screener UI flow and saved-screen handoff (`P1.4b`) depends on stable query envelopes and result-row semantics so later screener surface and saved-screen work can reuse one service-owned screener contract instead of inventing a second client-side model.",
            spec_text,
        )
        self.assertIn(
            "Dynamic watchlists and portfolio overlays (`P4.7`) depends on screen definitions remaining replayable, service-owned query objects so later dynamic watchlists can regenerate a screen universe without scraping transient UI state or storing raw row payloads as truth.",
            spec_text,
        )


if __name__ == "__main__":
    unittest.main()
