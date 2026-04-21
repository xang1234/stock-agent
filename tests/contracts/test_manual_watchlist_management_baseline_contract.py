from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"


class ManualWatchlistManagementBaselineContractTest(unittest.TestCase):
    def test_spec_declares_single_manual_watchlist_membership_baseline(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 3.14 Manual watchlist management baseline", spec_text)
        self.assertIn(
            "The product starts from one implicit default manual watchlist as the baseline saved-subject model.",
            spec_text,
        )
        self.assertIn(
            "The manual baseline CRUD floor is membership-only: view current members, add a resolved subject, and remove a saved subject.",
            spec_text,
        )
        self.assertIn(
            "This bead does not define create-list, rename-list, delete-list, sharing, reordering, or multiple manual lists.",
            spec_text,
        )
        self.assertIn(
            "The persisted membership unit is canonical subject identity rather than raw ticker strings or stored quote payloads.",
            spec_text,
        )
        self.assertIn(
            "Membership is idempotent at the subject level, so adding the same canonical subject twice does not create duplicates.",
            spec_text,
        )

    def test_spec_declares_quote_on_read_hydration_and_auth_resume_add(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "Manual watchlist rows hydrate quote context on read from saved canonical subject identity rather than storing quote payloads in membership records.",
            spec_text,
        )
        self.assertIn(
            "The row hydration contract is lightweight: subject display identity, listing-sensitive symbol context when applicable, latest price, absolute move, percentage move, and freshness or session state.",
            spec_text,
        )
        self.assertIn(
            "Quote row hydration reuses the same listing-oriented market identity rule as early symbol entry rather than inventing a watchlist-specific quote identity model.",
            spec_text,
        )
        self.assertIn(
            "Add-to-watchlist from public subject routes uses the existing inline auth interrupt contract: if the user is unauthenticated, the current route and pending resolved subject are preserved and the add resumes after sign-in.",
            spec_text,
        )
        self.assertIn(
            "Removing a member changes watchlist membership only and does not mutate the underlying subject, quote snapshot, or later portfolio overlay state.",
            spec_text,
        )

    def test_spec_declares_watchlist_baseline_downstream_consumers(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "### 3.15 Downstream consumer rules for manual watchlist baseline work",
            spec_text,
        )
        self.assertIn(
            "Portfolio and watchlist basics (`P1.5`) depends on the simple saved-subject baseline and quote row behavior that later portfolio and holdings surfaces build on.",
            spec_text,
        )
        self.assertIn(
            "Dynamic watchlists and portfolio overlays (`P4.7`) depends on the manual list baseline that later derivation modes and overlay behavior extend rather than replace.",
            spec_text,
        )
        self.assertIn(
            "Agent CRUD and scheduling (`P5.1`) depends on a simple, user-owned list object and membership model that later automation or agent creation flows may target without inventing a separate subject collection system.",
            spec_text,
        )


if __name__ == "__main__":
    unittest.main()
