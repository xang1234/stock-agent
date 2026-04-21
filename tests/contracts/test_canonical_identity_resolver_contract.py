from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"


class CanonicalIdentityResolverContractTest(unittest.TestCase):
    def test_spec_declares_resolver_responsibilities_and_typed_envelope(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 6.1 Identity and resolver service", spec_text)
        self.assertIn(
            "The resolver is the deterministic boundary that converts user-entered lookup input and provider-origin identity records into canonical finance identity outputs.",
            spec_text,
        )
        self.assertIn(
            "The resolver owns normalization, candidate generation, canonical reference selection when unambiguous, and explicit ambiguity preservation when multiple canonical targets remain plausible.",
            spec_text,
        )
        self.assertIn(
            "The resolver is distinct from search UI, user disambiguation flow, and downstream subject hydration.",
            spec_text,
        )
        self.assertIn(
            "The contract defines a typed resolution envelope rather than an untyped candidate list.",
            spec_text,
        )
        self.assertIn(
            "`resolved` means the resolver can name one canonical target confidently enough for deterministic downstream use.",
            spec_text,
        )
        self.assertIn(
            "`ambiguous` means multiple canonical issuer, instrument, listing, or `SubjectRef` targets remain plausible after normalization and matching, so the resolver must return ranked candidates without silently picking one.",
            spec_text,
        )
        self.assertIn(
            "`not_found` means the resolver could normalize the input but could not map it to a supported canonical target.",
            spec_text,
        )

    def test_spec_declares_input_families_and_ambiguity_rules(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "The contract explicitly covers two input families: user-entered lookup text and provider-origin identity records.",
            spec_text,
        )
        self.assertIn(
            "User-entered lookup text includes ticker-like strings, issuer names, aliases, and other concise finance lookup inputs.",
            spec_text,
        )
        self.assertIn(
            "Provider-origin identity records include external ids and structured provider payload fields such as ticker, exchange, CIK, ISIN, or other identifier-bearing records.",
            spec_text,
        )
        self.assertIn(
            "The resolver may start from ticker or alias lookup, but downstream output must promote that lookup into explicit issuer, instrument, listing, or `SubjectRef` candidates.",
            spec_text,
        )
        self.assertIn(
            "Ticker-only identity remains insufficient because the same symbol can map to different listings, venues, or securities, and issuer-level workflows often need a different canonical target than market-data workflows.",
            spec_text,
        )
        self.assertIn(
            "The resolver should expose the ambiguity axis when possible, such as issuer-versus-listing ambiguity or multiple plausible listings for one ticker string.",
            spec_text,
        )
        self.assertIn(
            "Ranked candidates are advisory metadata, not permission to silently collapse ambiguity into one winner.",
            spec_text,
        )
        self.assertIn(
            "`resolved` should include the canonical identity level that was chosen so downstream systems know whether they received issuer, instrument, listing, or already-formed `SubjectRef` output.",
            spec_text,
        )

    def test_spec_declares_resolver_downstream_consumers(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 6.1.1 Downstream consumer rules", spec_text)
        self.assertIn(
            "Search-to-subject resolution flow (`P0.3b`) depends on the resolver outcome vocabulary it will carry through candidate search, user choice, and downstream subject hydration.",
            spec_text,
        )
        self.assertIn(
            "Market data service (`P1.1`) depends on the rule that quote and bar consumers must receive listing-appropriate canonical output rather than ticker strings or issuer-level guesses.",
            spec_text,
        )
        self.assertIn(
            "Fundamentals service (`P1.2`) depends on the rule that issuer-backed fundamentals cannot rely on ticker-only identity and must consume issuer-appropriate canonical output or preserved ambiguity.",
            spec_text,
        )
        self.assertIn(
            "Screener surface and saved-screen handoff depends on deterministic subject identity shapes even before later hydration flow is applied.",
            spec_text,
        )
        self.assertIn(
            "Pre-resolve router and budget policy (`P2.2`) depends on the rule that deterministic pre-resolve routing consumes resolver envelopes rather than asking the model to silently choose among ambiguous identity candidates.",
            spec_text,
        )


if __name__ == "__main__":
    unittest.main()
