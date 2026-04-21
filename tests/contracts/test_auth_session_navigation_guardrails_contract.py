from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"


class AuthSessionNavigationGuardrailsContractTest(unittest.TestCase):
    def test_spec_declares_public_and_session_scoped_surfaces(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 3.10 Auth session and navigation guardrails", spec_text)
        self.assertIn(
            "The persistent workspace shell is not auth-gated as a whole. Unauthenticated users may enter the shell and navigate public research routes.",
            spec_text,
        )
        self.assertIn(
            "Public browsing surfaces are `Home`, `Screener`, top-level `Analyze` entry, and entered symbol-detail routes.",
            spec_text,
        )
        self.assertIn(
            "Public browsing may render market data, fundamentals, findings, and subject context that do not depend on user-owned state or persisted session history.",
            spec_text,
        )
        self.assertIn(
            "Session-scoped workspaces and flows are `Chat`, `Agents`, watchlist views and mutations, persisted Analyze runs, saved prompts or templates, and any user-owned thread or run history.",
            spec_text,
        )
        self.assertIn(
            "A route may be publicly enterable yet still host protected actions. Top-level `Analyze` may render only a public entry state with carried `SubjectRef` context, while any user-owned draft, save, or persisted-run state requires a session.",
            spec_text,
        )
        self.assertIn(
            "This contract is written in terms of authenticated session scope rather than a specific identity or entitlement backend.",
            spec_text,
        )

    def test_spec_declares_soft_gates_and_inline_auth_interrupts(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "Protected workspaces and routes use soft in-shell guards rather than replacing the shell with a separate auth-page model.",
            spec_text,
        )
        self.assertIn(
            "Unauthenticated navigation to `Chat`, `Agents`, watchlists, or any other session-scoped route keeps shell chrome visible and replaces protected main-canvas content with an auth gate for that destination.",
            spec_text,
        )
        self.assertIn(
            "The guard preserves intended destination context so successful sign-in can resume the same workspace, thread, agent view, watchlist view, or persisted run target.",
            spec_text,
        )
        self.assertIn(
            "Public routes may launch protected actions through inline auth interrupts. Examples include `save to watchlist`, `start chat`, `open persisted run`, and any action that would create or reveal user-owned state.",
            spec_text,
        )
        self.assertIn(
            "Inline auth interrupts preserve the current public route plus the pending action payload so sign-in can resume the action instead of forcing a route change.",
            spec_text,
        )

    def test_spec_declares_session_loss_and_downstream_consumers(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "If a session expires or the user logs out inside a protected surface, protected content collapses to the same in-shell auth gate rather than redirecting away.",
            spec_text,
        )
        self.assertIn(
            "Session loss preserves return-to context for the current protected route, but it must not continue rendering user-owned content after invalidation.",
            spec_text,
        )
        self.assertIn(
            "Public routes remain navigable after logout or expiry without reconstructing the shell.",
            spec_text,
        )
        self.assertIn(
            "The shell remains the durable navigation frame regardless of auth state; auth changes what the main canvas may reveal or mutate.",
            spec_text,
        )
        self.assertIn("### 3.11 Downstream consumer rules for auth and session work", spec_text)
        self.assertIn(
            "Symbol overview and subject detail (`P1.3`) depends on the rule that entered subject detail may render public market, fundamentals, findings, and subject context without requiring a session.",
            spec_text,
        )
        self.assertIn(
            "Screener surface and saved-screen handoff depends on `Screener` remaining publicly browsable inside the persistent shell while saved outputs and user-scoped handoffs require a session.",
            spec_text,
        )
        self.assertIn(
            "Thread coordinator and transport (`P2.1`) depends on `Chat` being session-scoped even though it lives inside the same persistent shell as public routes.",
            spec_text,
        )
        self.assertIn(
            "Agent management and scheduling depends on `Agents` and related user-owned configuration flows being session-scoped workspaces.",
            spec_text,
        )


if __name__ == "__main__":
    unittest.main()
