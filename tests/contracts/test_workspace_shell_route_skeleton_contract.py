from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"


class WorkspaceShellRouteSkeletonContractTest(unittest.TestCase):
    def test_spec_declares_persistent_shell_and_primary_workspaces(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 3.7 Workspace shell and route skeleton", spec_text)
        self.assertIn(
            "The app uses one persistent workspace shell rather than surface-specific chrome for each page.",
            spec_text,
        )
        self.assertIn(
            "The shell owns three regions: left navigation, main workspace canvas, and a right-rail slot.",
            spec_text,
        )
        self.assertIn(
            "Left navigation holds the primary workspaces: `Home`, `Agents`, `Chat`, `Screener`, and `Analyze`.",
            spec_text,
        )
        self.assertIn(
            "Shell chrome persists while moving between those primary workspaces.",
            spec_text,
        )
        self.assertIn(
            "The right rail is a shell-owned slot rather than a surface-owned layout invention.",
            spec_text,
        )
        self.assertIn(
            "`Home`, `Agents`, `Chat`, symbol detail, and `Analyze` use the right rail by default.",
            spec_text,
        )
        self.assertIn(
            "`Screener` defaults to a denser main-canvas layout and may opt into the rail later without changing the shell contract.",
            spec_text,
        )

    def test_spec_declares_symbol_detail_routes_and_analyze_handoff(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 3.4 Symbol detail", spec_text)
        self.assertIn(
            "Symbol detail is an entered subject workspace with sections such as Overview, Financials, Earnings, Holders, and Signals. It may launch into top-level `Analyze` with carried subject context.",
            spec_text,
        )
        self.assertIn("### 3.8 Symbol-detail route skeleton", spec_text)
        self.assertIn(
            "Primary workspace route groups are `home`, `agents`, `chat`, `screener`, and `analyze`.",
            spec_text,
        )
        self.assertIn(
            "`Chat` remains thread-scoped rather than symbol-scoped because threads may span themes, multiple subjects, or imported Analyze artifacts.",
            spec_text,
        )
        self.assertIn(
            "Symbol detail is an entered route group keyed by canonical subject identity rather than a primary left-nav workspace.",
            spec_text,
        )
        self.assertIn(
            "Entering symbol detail swaps the main canvas into a subject-detail shell while preserving the surrounding shell chrome.",
            spec_text,
        )
        self.assertIn(
            "Nested routes are the durable model for subject-detail sections.",
            spec_text,
        )
        self.assertIn(
            "The initial durable subject-detail sections are `overview`, `financials`, `earnings`, `holders`, and `signals`.",
            spec_text,
        )
        self.assertIn(
            "`signals` is the extensible section for community, sentiment, news pulse, and future alt-data views.",
            spec_text,
        )
        self.assertIn(
            "Symbol detail may deep-link into top-level `Analyze` with carried `SubjectRef` context or a prefilled analyze intent.",
            spec_text,
        )

    def test_spec_declares_shell_downstream_consumers(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 3.9 Downstream consumer rules for shell and route work", spec_text)
        self.assertIn(
            "Symbol search and quote snapshot surface (`P0.4`) depends on the distinction between primary workspaces and entered symbol-detail routes.",
            spec_text,
        )
        self.assertIn(
            "Symbol overview shell (`P1.3`) depends on the subject-detail shell owning shared identity context and local section navigation.",
            spec_text,
        )
        self.assertIn(
            "Symbol detail tabs and context modules (`P1.4`) depend on durable nested-route buckets inside the subject-detail shell.",
            spec_text,
        )
        self.assertIn(
            "Thread coordinator and transport (`P2.1`) depends on `Chat` being a primary workspace inside the persistent shell.",
            spec_text,
        )
        self.assertIn(
            "Analyze workspace surfaces (`P4.4`) depends on `Analyze` being top-level while still accepting deep-linked subject context.",
            spec_text,
        )
        self.assertIn(
            "Right-rail activity (`P4.5`) depends on the shell-owned right-rail slot and selective default population.",
            spec_text,
        )


if __name__ == "__main__":
    unittest.main()
