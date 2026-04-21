# Auth Session And Navigation Guardrails Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make auth scope, in-shell route guards, inline auth interrupts, and session-loss behavior explicit in the narrative spec so later shell, symbol, chat, screener, and agent work shares one stable access contract.

**Architecture:** Treat this bead as a narrative contract-pack update, not an auth-provider or router implementation. Add a small file-based contract test that asserts the required public-versus-session-scoped surface split, guard behavior, session-loss rules, and downstream-consumer wording exists, watch it fail first, then patch the narrative spec so the session model is explicit and internally consistent with the persistent shell.

**Tech Stack:** Markdown spec, Python 3 `unittest`

---

## File Structure

- Modify: `spec/finance_research_spec.md`
  Responsibility: narrative auth-scope and navigation-guardrail rules near the shell and route sections, including public browsing surfaces, session-scoped workspaces, soft in-shell guards, inline auth interrupts, session-loss behavior, and downstream consumer notes.
- Create: `tests/contracts/test_auth_session_navigation_guardrails_contract.py`
  Responsibility: file-level contract checks enforcing the required auth-scope, guard, session-loss, and downstream-consumer wording anchors in the narrative spec.

### Task 1: Add failing auth-session guardrail checks

**Files:**
- Create: `tests/contracts/test_auth_session_navigation_guardrails_contract.py`
- Test: `tests/contracts/test_auth_session_navigation_guardrails_contract.py`

- [ ] **Step 1: Write the failing test**

```python
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
            "Session-scoped workspaces and flows are `Chat`, `Agents`, watchlists, persisted Analyze runs, saved prompts or templates, and any user-owned thread or run history.",
            spec_text,
        )
        self.assertIn(
            "A route may be publicly enterable yet still host protected actions. Top-level `Analyze` may render public entry and carried `SubjectRef` context, while saving or reopening persisted runs requires a session.",
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
            "Screener surface and saved-screen handoff (`P1.4`) depends on `Screener` remaining publicly browsable inside the persistent shell while saved outputs and user-scoped handoffs require a session.",
            spec_text,
        )
        self.assertIn(
            "Thread coordinator and transport (`P2.1`) depends on `Chat` being session-scoped even though it lives inside the same persistent shell as public routes.",
            spec_text,
        )
        self.assertIn(
            "Agent management and scheduling (`P5.1`) depends on `Agents` and related user-owned configuration flows being session-scoped workspaces.",
            spec_text,
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.contracts.test_auth_session_navigation_guardrails_contract -v`
Expected: `FAIL` because the new auth-session guardrail headings and wording do not exist yet.

- [ ] **Step 3: Commit**

```bash
git add tests/contracts/test_auth_session_navigation_guardrails_contract.py
git commit -m "test: add auth session guardrail checks"
```

### Task 2: Patch the auth and session contract in the narrative spec

**Files:**
- Modify: `spec/finance_research_spec.md`
- Test: `tests/contracts/test_auth_session_navigation_guardrails_contract.py`

- [ ] **Step 1: Add the auth-session guardrail subsection below the shell-route sections**

```md
### 3.10 Auth session and navigation guardrails

- The persistent workspace shell is not auth-gated as a whole. Unauthenticated users may enter the shell and navigate public research routes.
- Public browsing surfaces are `Home`, `Screener`, top-level `Analyze` entry, and entered symbol-detail routes.
- Public browsing may render market data, fundamentals, findings, and subject context that do not depend on user-owned state or persisted session history.
- Session-scoped workspaces and flows are `Chat`, `Agents`, watchlists, persisted Analyze runs, saved prompts or templates, and any user-owned thread or run history.
- A route may be publicly enterable yet still host protected actions. Top-level `Analyze` may render public entry and carried `SubjectRef` context, while saving or reopening persisted runs requires a session.
- Protected workspaces and routes use soft in-shell guards rather than replacing the shell with a separate auth-page model.
- Unauthenticated navigation to `Chat`, `Agents`, watchlists, or any other session-scoped route keeps shell chrome visible and replaces protected main-canvas content with an auth gate for that destination.
- The guard preserves intended destination context so successful sign-in can resume the same workspace, thread, agent view, watchlist view, or persisted run target.
- Public routes may launch protected actions through inline auth interrupts. Examples include `save to watchlist`, `start chat`, `open persisted run`, and any action that would create or reveal user-owned state.
- Inline auth interrupts preserve the current public route plus the pending action payload so sign-in can resume the action instead of forcing a route change.
- If a session expires or the user logs out inside a protected surface, protected content collapses to the same in-shell auth gate rather than redirecting away.
- Session loss preserves return-to context for the current protected route, but it must not continue rendering user-owned content after invalidation.
- Public routes remain navigable after logout or expiry without reconstructing the shell.
- Public surfaces continue to render public research context while protected panels and actions re-gate in place.
- The shell remains the durable navigation frame regardless of auth state; auth changes what the main canvas may reveal or mutate.
- This contract is written in terms of authenticated session scope rather than a specific identity or entitlement backend.
```

- [ ] **Step 2: Add the downstream consumer subsection for auth and session work**

```md
### 3.11 Downstream consumer rules for auth and session work

- Symbol overview and subject detail (`P1.3`) depends on the rule that entered subject detail may render public market, fundamentals, findings, and subject context without requiring a session.
- Screener surface and saved-screen handoff (`P1.4`) depends on `Screener` remaining publicly browsable inside the persistent shell while saved outputs and user-scoped handoffs require a session.
- Thread coordinator and transport (`P2.1`) depends on `Chat` being session-scoped even though it lives inside the same persistent shell as public routes.
- Agent management and scheduling (`P5.1`) depends on `Agents` and related user-owned configuration flows being session-scoped workspaces.
```

- [ ] **Step 3: Run the contract test and confirm green**

Run: `python3 -m unittest tests.contracts.test_auth_session_navigation_guardrails_contract -v`
Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add spec/finance_research_spec.md
git commit -m "docs: define auth session navigation guardrails contract"
```

### Task 3: Verify and land the bead

**Files:**
- Modify: `.beads/issues.jsonl` (via `bd close` / `bd sync`)
- Test: `tests/contracts/test_auth_session_navigation_guardrails_contract.py`

- [ ] **Step 1: Inspect repo state**

Run: `git status --short`
Expected: only the intended spec, test, plan, and bead metadata changes remain, plus the known unrelated untracked baseline files.

- [ ] **Step 2: Close the bead**

Run: `bd close stock-agent-h3e.1.2.2 --reason "Completed"`
Expected: bead marked `closed`

- [ ] **Step 3: Sync bead metadata**

Run: `bd sync`
Expected: `.beads/issues.jsonl` updated for the closed bead state

- [ ] **Step 4: Re-run the contract test after bead sync**

Run: `python3 -m unittest tests.contracts.test_auth_session_navigation_guardrails_contract -v`
Expected: `OK`

- [ ] **Step 5: Commit bead metadata if needed**

```bash
git add .beads/issues.jsonl docs/superpowers/plans/2026-04-21-auth-session-navigation-guardrails.md
git commit -m "chore: sync bead status for stock-agent-h3e.1.2.2"
```

Only do this if `bd sync` changed tracked files that are not already committed.

- [ ] **Step 6: Publish the feature branch**

Run: `git push -u origin stock-agent-h3e.1.2.2`
Expected: remote branch updated successfully

- [ ] **Step 7: Fast-forward `main` and verify there**

Run: `git checkout main && git pull --rebase origin main && git merge --ff-only stock-agent-h3e.1.2.2 && python3 -m unittest tests.contracts.test_auth_session_navigation_guardrails_contract -v`
Expected: fast-forward merge succeeds and the contract test reports `OK`

- [ ] **Step 8: Push `main` and verify final status**

Run: `git push origin main && git status`
Expected: `main` is up to date with `origin/main`, with only the known unrelated untracked baseline files remaining

- [ ] **Step 9: Delete the local feature branch**

Run: `git branch -d stock-agent-h3e.1.2.2`
Expected: local feature branch deleted after the fast-forward merge
