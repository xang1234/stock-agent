from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"


class SearchToSubjectResolutionFlowContractTest(unittest.TestCase):
    def test_spec_declares_staged_flow_and_auto_advance_rules(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 6.1.2 Search-to-subject resolution flow", spec_text)
        self.assertIn(
            "Search-to-subject flow is the deterministic orchestration that carries lookup input from candidate search through canonical selection into downstream-safe subject hydration.",
            spec_text,
        )
        self.assertIn(
            "The staged flow is candidate search, canonical selection, and hydrated subject handoff.",
            spec_text,
        )
        self.assertIn(
            "Candidate search may return zero, one, or many candidates, but it must not invent a silent winner from ambiguous matches.",
            spec_text,
        )
        self.assertIn(
            "If candidate search yields exactly one deterministic candidate that already satisfies the resolver contract, the flow may auto-advance to canonical selection without a separate chooser step.",
            spec_text,
        )
        self.assertIn(
            "If multiple plausible candidates remain, the flow must pause at explicit ambiguity preservation and surface ranked candidates for later user or caller choice.",
            spec_text,
        )
        self.assertIn("`not_found` ends the flow without subject hydration.", spec_text)
        self.assertIn(
            "Only a `resolved` outcome may produce hydrated subject handoff.",
            spec_text,
        )

    def test_spec_declares_hydrated_subject_bundle_contract(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "The hydrated subject bundle includes the canonical `SubjectRef`, the resolved identity level, stable display labels, normalized lookup input, resolution path (`auto_advanced` or `explicit_choice`), and enough issuer, instrument, or listing context for immediate downstream use.",
            spec_text,
        )
        self.assertIn(
            "Watchlists, chat turns, Analyze entry, and service-to-service calls consume the same hydrated subject bundle contract even if they later project only the fields they need.",
            spec_text,
        )
        self.assertIn(
            "One hydrated bundle may carry joined issuer and active listing context, but the canonical `SubjectRef` remains the durable key.",
            spec_text,
        )
        self.assertIn(
            "Downstream systems persist the canonical `SubjectRef` and treat the rest of the hydrated bundle as entry context that may be refreshed later.",
            spec_text,
        )

    def test_spec_declares_search_flow_downstream_consumers(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "### 6.1.3 Downstream consumer rules for search-to-subject flow",
            spec_text,
        )
        self.assertIn(
            "Symbol search and quote snapshot surface (`P0.4`) depends on symbol search entry points, explicit candidate-choice rules, and hydrated subject handoff for quote snapshots.",
            spec_text,
        )
        self.assertIn(
            "Market data service (`P1.1`) depends on listing-appropriate subject handoff into quote and bar retrieval rather than ticker-string lookup.",
            spec_text,
        )
        self.assertIn(
            "Fundamentals service (`P1.2`) depends on issuer-appropriate subject handoff into statement and metric normalization instead of rediscovering identity downstream.",
            spec_text,
        )
        self.assertIn(
            "Pre-resolve router and budget policy (`P2.2`) depends on deterministic subject handoff so chat turns start from canonical subject context rather than ad hoc model interpretation of search strings.",
            spec_text,
        )
        self.assertIn(
            "Watchlist and saved-subject entry flows depend on the same hydrated subject bundle contract so selected subjects can be saved, reopened, and re-entered without rediscovering identity from raw lookup text.",
            spec_text,
        )


if __name__ == "__main__":
    unittest.main()
