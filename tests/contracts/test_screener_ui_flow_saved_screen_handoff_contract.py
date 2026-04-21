from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"


class ScreenerUiFlowSavedScreenHandoffContractTest(unittest.TestCase):
    def test_spec_declares_screener_workspace_flow(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 3.20 Screener surface flow and saved-screen handoff", spec_text)
        self.assertIn(
            "`Screener` remains a primary workspace for building, refining, and viewing one active screen definition plus its current result set inside the persistent shell.",
            spec_text,
        )
        self.assertIn(
            "The screener surface keeps query controls and result rows in one workspace flow rather than splitting query editing, results, and saved screens into separate primary surfaces.",
            spec_text,
        )
        self.assertIn(
            "Public screener browsing may execute and refine unsaved screens without requiring a session, reusing the public-route and backend-owned screener query contract already defined elsewhere.",
            spec_text,
        )

    def test_spec_declares_saved_screen_and_subject_handoff_rules(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "Saving a screen, opening a user-owned saved screen, or mutating saved-screen metadata requires a session and uses the existing in-shell auth interrupt and resume behavior rather than leaving the screener route family.",
            spec_text,
        )
        self.assertIn(
            "Saving a screen persists the replayable screen definition, user-owned screen record, and ordering semantics rather than a frozen cache of row payloads or a detached export artifact.",
            spec_text,
        )
        self.assertIn(
            "Reopening a saved screen restores the screener workspace with the saved screen definition as the active query context and rehydrates results through the screener service rather than replaying stale table rows from client storage.",
            spec_text,
        )
        self.assertIn(
            "Selecting a screener result row hands off canonical subject identity into the existing symbol-detail entry flow rather than opening a screener-specific quote view or embedding a full subject workspace inline.",
            spec_text,
        )
        self.assertIn(
            "Handoffs from screener into later list or theme workflows carry explicit `screen` context or the saved query definition as the source reference so downstream derivation and theme flows can explain where a generated universe came from.",
            spec_text,
        )

    def test_spec_declares_screener_surface_downstream_consumers(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 3.21 Downstream consumer rules for screener surface work", spec_text)
        self.assertIn(
            "Themes and macro subjects (`P4.1`) depends on screen-to-theme or derived-universe handoffs carrying explicit screen source context so later theme workflows can distinguish screen-derived membership inputs from manual or inferred membership.",
            spec_text,
        )
        self.assertIn(
            "Dynamic watchlists and portfolio overlays (`P4.7`) depends on saved screens remaining replayable user-owned screen definitions with explicit source handoff so later dynamic watchlists can regenerate and explain screen-derived lists without scraping transient screener UI state.",
            spec_text,
        )


if __name__ == "__main__":
    unittest.main()
