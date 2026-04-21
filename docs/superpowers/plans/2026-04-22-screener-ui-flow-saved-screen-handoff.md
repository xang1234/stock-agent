# Screener UI Flow And Saved Screen Handoff Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the screener workspace flow and saved-screen handoff explicit in the narrative spec so later screen-derived lists and theme inputs reuse one deterministic surface contract.

**Architecture:** Treat this bead as a product-surface contract update layered on top of the existing screener service contract. Add a file-based contract test that asserts the spec defines screener browse flow, session-gated save or resume behavior, saved-screen restoration, subject handoff, and downstream consumer notes. Watch that test fail first, then patch the product-surface section with dedicated `3.20` and `3.21` subsections.

**Tech Stack:** Markdown spec, Python 3 `unittest`

---

## File Structure

- Modify: `spec/finance_research_spec.md`
  Responsibility: add the screener workspace-flow and saved-screen handoff subsections after the current watchlist and portfolio surface work.
- Create: `tests/contracts/test_screener_ui_flow_saved_screen_handoff_contract.py`
  Responsibility: file-level contract checks enforcing screener browse, save or resume, subject handoff, and downstream-consumer anchors.

### Task 1: Add failing screener surface-flow contract checks

**Files:**
- Create: `tests/contracts/test_screener_ui_flow_saved_screen_handoff_contract.py`
- Test: `tests/contracts/test_screener_ui_flow_saved_screen_handoff_contract.py`

- [ ] **Step 1: Write the failing test**

```python
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


if __name__ == \"__main__\":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.contracts.test_screener_ui_flow_saved_screen_handoff_contract -v`
Expected: `FAIL` because the `3.20` and `3.21` screener surface sections do not exist yet.

- [ ] **Step 3: Commit**

```bash
git add tests/contracts/test_screener_ui_flow_saved_screen_handoff_contract.py
git commit -m "test: add screener saved-screen handoff checks"
```

### Task 2: Patch the screener surface narrative

**Files:**
- Modify: `spec/finance_research_spec.md`
- Test: `tests/contracts/test_screener_ui_flow_saved_screen_handoff_contract.py`

- [ ] **Step 1: Add the screener surface subsections**

```md
### 3.20 Screener surface flow and saved-screen handoff

- `Screener` remains a primary workspace for building, refining, and viewing one active screen definition plus its current result set inside the persistent shell.
- The screener surface keeps query controls and result rows in one workspace flow rather than splitting query editing, results, and saved screens into separate primary surfaces.
- Public screener browsing may execute and refine unsaved screens without requiring a session, reusing the public-route and backend-owned screener query contract already defined elsewhere.
- Saving a screen, opening a user-owned saved screen, or mutating saved-screen metadata requires a session and uses the existing in-shell auth interrupt and resume behavior rather than leaving the screener route family.
- Saving a screen persists the replayable screen definition, user-owned screen record, and ordering semantics rather than a frozen cache of row payloads or a detached export artifact.
- Reopening a saved screen restores the screener workspace with the saved screen definition as the active query context and rehydrates results through the screener service rather than replaying stale table rows from client storage.
- Selecting a screener result row hands off canonical subject identity into the existing symbol-detail entry flow rather than opening a screener-specific quote view or embedding a full subject workspace inline.
- Handoffs from screener into later list or theme workflows carry explicit `screen` context or the saved query definition as the source reference so downstream derivation and theme flows can explain where a generated universe came from.
- This bead does not define dynamic watchlist derivation rules, theme membership inference, or bulk portfolio-overlay behavior; it only defines the screener surface flow and saved-screen handoff seam.

### 3.21 Downstream consumer rules for screener surface work

- Themes and macro subjects (`P4.1`) depends on screen-to-theme or derived-universe handoffs carrying explicit screen source context so later theme workflows can distinguish screen-derived membership inputs from manual or inferred membership.
- Dynamic watchlists and portfolio overlays (`P4.7`) depends on saved screens remaining replayable user-owned screen definitions with explicit source handoff so later dynamic watchlists can regenerate and explain screen-derived lists without scraping transient screener UI state.
```

- [ ] **Step 2: Run the screener surface contract tests and confirm green**

Run: `python3 -m unittest tests.contracts.test_screener_ui_flow_saved_screen_handoff_contract tests.contracts.test_auth_session_navigation_guardrails_contract tests.contracts.test_canonical_identity_resolver_contract tests.contracts.test_screener_query_model_api_surface_contract -v`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add spec/finance_research_spec.md
git commit -m "docs: define screener saved-screen handoff"
```

### Task 3: Verify and land the bead

**Files:**
- Modify: `.beads/issues.jsonl` (via `bd close` / `bd sync`)
- Test: `tests/contracts/test_screener_ui_flow_saved_screen_handoff_contract.py`

- [ ] **Step 1: Inspect repo state**

Run: `git status --short`
Expected: only the intended screener-surface files and bead metadata changes remain, plus known unrelated local untracked files.

- [ ] **Step 2: Close the bead**

Run: `bd --no-daemon close stock-agent-h3e.2.4.2 --reason "Completed"`
Expected: bead marked `closed`

- [ ] **Step 3: Sync bead metadata**

Run: `bd --no-daemon sync`
Expected: `.beads/issues.jsonl` updated for the closed bead state

- [ ] **Step 4: Re-run the screener surface contract tests after bead sync**

Run: `python3 -m unittest tests.contracts.test_screener_ui_flow_saved_screen_handoff_contract tests.contracts.test_auth_session_navigation_guardrails_contract tests.contracts.test_canonical_identity_resolver_contract tests.contracts.test_screener_query_model_api_surface_contract -v`
Expected: `OK`

- [ ] **Step 5: Commit bead metadata if needed**

```bash
git add .beads/issues.jsonl docs/superpowers/plans/2026-04-22-screener-ui-flow-saved-screen-handoff.md
git commit -m "chore: sync bead status for stock-agent-h3e.2.4.2"
```

Only do this if `bd sync` changed tracked files that are not already committed.

- [ ] **Step 6: Pull, push, and confirm remote state**

Run: `git pull --rebase && git push && git status`
Expected: rebase succeeds, push succeeds, and status reports the branch is up to date with origin.
