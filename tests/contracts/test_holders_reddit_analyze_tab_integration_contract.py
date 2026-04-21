from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"


class HoldersRedditAnalyzeTabIntegrationContractTest(unittest.TestCase):
    def test_spec_declares_holders_signals_and_analyze_boundaries(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "### 3.4.4 Holders, signals, and Analyze entry integration",
            spec_text,
        )
        self.assertIn(
            "`holders` remains the deterministic symbol-detail section for institutional and insider holder views tied to the selected subject.",
            spec_text,
        )
        self.assertIn(
            "`holders` composes structured holder outputs from the fundamentals service and remains distinct from portfolio overlays, watchlist state, and user-owned monitoring context.",
            spec_text,
        )
        self.assertIn(
            "`signals` remains the symbol-detail section for Reddit-like community views, news pulse, and future alt-data entry points; this bead does not replace that route bucket with a source-specific `reddit` shell contract.",
            spec_text,
        )
        self.assertIn(
            "Reddit-like or news-specialized content inside `signals` composes evidence-backed blocks, claim clusters, evidence bundles, and trend-style renderers rather than raw social-text panes or provider-specific mini-pages.",
            spec_text,
        )
        self.assertIn(
            "`Analyze` remains a top-level workspace rather than a durable nested symbol-detail section.",
            spec_text,
        )
        self.assertIn(
            "Symbol detail launches `Analyze` with carried `SubjectRef` context or an explicit analyze intent, but resulting artifacts live on the shared snapshot and block plane rather than inside a persistent symbol-detail tab.",
            spec_text,
        )

    def test_spec_declares_navigation_and_handoff_rules(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "### 3.4.5 Navigation and handoff rules for holders, signals, and Analyze",
            spec_text,
        )
        self.assertIn(
            "Entering `holders` or `signals` from symbol detail preserves subject context inside the same nested-route family and subject-detail shell.",
            spec_text,
        )
        self.assertIn(
            "Launching `Analyze` from symbol detail is a workspace transition that still preserves carried subject context and does not reinterpret the subject from raw ticker text.",
            spec_text,
        )
        self.assertIn(
            "The handoff from symbol detail into `Analyze` stays explicit so later shared-artifact and replay flows can point to durable snapshot-backed artifacts instead of scraped UI state.",
            spec_text,
        )
        self.assertIn(
            "This bead does not redefine the core deterministic ownership of `overview`, `financials`, or `earnings`; it layers adjacent sections and launch points on top of that contract.",
            spec_text,
        )

    def test_spec_declares_downstream_consumers_for_holders_and_analyze_entry(
        self,
    ) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "### 3.4.6 Downstream consumer rules for holders, signals, and Analyze entry work",
            spec_text,
        )
        self.assertIn(
            "Analyze template system (`P4.2`) depends on explicit handoff from symbol detail into top-level `Analyze` with carried subject context so template and saved-workflow work can distinguish launch context from tab ownership.",
            spec_text,
        )
        self.assertIn(
            "Shared artifact flow (`P4.3`) depends on `Analyze` entry from symbol detail producing artifact and snapshot boundaries outside the symbol-detail shell so add-to-chat or replay flows import a sealed artifact instead of scraping tab state.",
            spec_text,
        )
        self.assertIn(
            "Specialized social and news blocks (`P4.6`) depends on Reddit-like entry living under `signals` and composing shared evidence-backed blocks so specialized social or news views do not redefine the symbol shell or bypass the block registry.",
            spec_text,
        )


if __name__ == "__main__":
    unittest.main()
