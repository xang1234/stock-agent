from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"


class OverviewFinancialsEarningsSurfaceCompositionContractTest(unittest.TestCase):
    def test_spec_declares_core_symbol_tab_responsibilities(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "### 3.4.1 Overview, financials, and earnings tab composition",
            spec_text,
        )
        self.assertIn(
            "`overview` owns the deterministic single-subject summary that extends the thin quote landing state into a durable core tab.",
            spec_text,
        )
        self.assertIn(
            "`overview` composes listing-aware quote context, company profile context, key stats, and a limited performance or context summary, but it does not become a second home for full statement tables, holders, or interpretive evidence flows.",
            spec_text,
        )
        self.assertIn(
            "`financials` owns normalized statement tables, statement-linked trend views, and segment-aware financial breakdowns for the selected subject.",
            spec_text,
        )
        self.assertIn(
            "`financials` composes normalized statement outputs plus the aggregation layer for key stats and segment facts rather than rebuilding fundamentals logic from provider-specific payloads.",
            spec_text,
        )
        self.assertIn(
            "`earnings` owns deterministic earnings chronology, expectation-versus-result views, and consensus summaries for the selected subject.",
            spec_text,
        )
        self.assertIn(
            "`earnings` composes earnings-release events, EPS surprise history, analyst consensus, and price-target context without turning transcript reading, news clustering, or freeform commentary into tab-owned responsibilities.",
            spec_text,
        )

    def test_spec_declares_shared_dependencies_and_navigation_rules(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "### 3.4.2 Shared dependencies and navigation expectations for core symbol tabs",
            spec_text,
        )
        self.assertIn(
            "All three tabs live inside the same subject-detail shell and share the same subject header context, nested-route navigation model, and public-route assumptions already established for symbol detail.",
            spec_text,
        )
        self.assertIn(
            "The core tab composition depends on hydrated subject identity, market quote and series services, fundamentals profile and statement services, aggregation outputs, and structured earnings events through backend contracts rather than direct provider payloads or chat-style tool loops.",
            spec_text,
        )
        self.assertIn(
            "Moving between `overview`, `financials`, and `earnings` preserves subject context and shell chrome; it is a local section transition, not a new top-level workspace or a fresh subject-resolution flow.",
            spec_text,
        )
        self.assertIn(
            "The tabs may link to one another through stable section destinations, but they must not collapse into one scrolling page or duplicate ownership of the same deterministic modules.",
            spec_text,
        )
        self.assertIn(
            "Holders, signals or Reddit, and Analyze entry points remain outside this bead and layer onto the subject-detail shell after the core tab responsibilities are fixed.",
            spec_text,
        )

    def test_spec_declares_downstream_consumers_for_core_symbol_tabs(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "### 3.4.3 Downstream consumer rules for core symbol tabs",
            spec_text,
        )
        self.assertIn(
            "Holders, Reddit, and Analyze tab integration (`P1.3b`) depends on `overview`, `financials`, and `earnings` having stable deterministic responsibilities so later holders, Reddit, and Analyze entry points can attach without redefining the core symbol-detail tabs.",
            spec_text,
        )
        self.assertIn(
            "Analyze template system (`P4.2`) depends on the explicit boundary between deterministic symbol tabs and later artifact-driven analysis so Analyze can launch from symbol detail without inheriting ownership of overview, financials, or earnings composition.",
            spec_text,
        )
        self.assertIn(
            "Home feed (`P4.4`) depends on stable symbol-tab destinations and shared subject context so findings and summaries can deep-link into the right deterministic surface instead of inventing custom readouts per card.",
            spec_text,
        )


if __name__ == "__main__":
    unittest.main()
