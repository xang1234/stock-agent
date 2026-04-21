# Portfolio And Watchlist Surface Behaviors Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the first portfolio and watchlist surface behaviors explicit in the narrative spec so shared quote rows, held-state context, and subject-view augmentation follow one stable contract.

**Architecture:** Treat this bead as a narrative surface-behavior contract update, not a portfolio UI implementation. Add a file-based contract test that asserts shared quote hydration, dual watchlist-plus-holding visibility, subject-view augmentation, and downstream consumer notes exist, watch it fail first, then patch the product-surface section with dedicated portfolio and watchlist behavior subsections.

**Tech Stack:** Markdown spec, Python 3 `unittest`

---

## File Structure

- Modify: `spec/finance_research_spec.md`
  Responsibility: add first-surface portfolio and watchlist behavior subsections after the holdings-model contract, defining shared quote-row behavior, subject-view augmentation, and downstream consumers.
- Create: `tests/contracts/test_portfolio_watchlist_surface_behaviors_contract.py`
  Responsibility: file-level contract checks enforcing row behavior, subject-view behavior, and downstream consumer anchors.

### Task 1: Add failing portfolio/watchlist surface-behavior contract checks

**Files:**
- Create: `tests/contracts/test_portfolio_watchlist_surface_behaviors_contract.py`
- Test: `tests/contracts/test_portfolio_watchlist_surface_behaviors_contract.py`

- [ ] **Step 1: Write the failing test**

```python
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"


class PortfolioWatchlistSurfaceBehaviorsContractTest(unittest.TestCase):
    def test_spec_declares_shared_quote_row_behavior(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "### 3.18 Portfolio and watchlist first surface behaviors",
            spec_text,
        )
        self.assertIn(
            "Manual watchlist and portfolio-held surfaces reuse the same thin quote-on-read row hydration contract rather than inventing separate quote-fetch behavior for held subjects.",
            spec_text,
        )
        self.assertIn(
            "Portfolio-held rows layer held-state context, quantity, and optional cost-basis context on top of that shared quote row skeleton.",
            spec_text,
        )
        self.assertIn(
            "The first surface behavior stays intentionally light: it does not define a portfolio analytics dashboard, brokerage position card, or private quote model distinct from symbol entry.",
            spec_text,
        )
        self.assertIn(
            "If a subject is both watchlisted and held, the surface keeps both states visible rather than collapsing one concept into the other.",
            spec_text,
        )

    def test_spec_declares_subject_view_augmentation_rules(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "Selecting a row from either a watchlist or portfolio-held surface enters the same symbol-detail route keyed by canonical subject identity.",
            spec_text,
        )
        self.assertIn(
            "Entered subject views may show lightweight saved-state and held-state context plus adjacent actions, but that context augments the existing quote snapshot and subject modules rather than creating a portfolio-specific subject shell.",
            spec_text,
        )
        self.assertIn(
            "Watchlist and holdings state remain user-owned overlay context on top of shared subject and market-data contracts.",
            spec_text,
        )

    def test_spec_declares_surface_behavior_downstream_consumers(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "### 3.19 Downstream consumer rules for portfolio and watchlist surface behaviors",
            spec_text,
        )
        self.assertIn(
            "Dynamic watchlists and portfolio overlays (`P4.7`) depends on shared quote-row behavior and stable subject-view augmentation so later theme, screen, portfolio, and watchlist combinations can add more context without rewriting the base surfaces.",
            spec_text,
        )
        self.assertIn(
            "Export and share policy (`P6.4`) depends on user-owned watchlist and holdings context staying visually and semantically distinct from canonical quote and subject content so later export or share rules can reason about what private overlay state may travel with a shared artifact.",
            spec_text,
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.contracts.test_portfolio_watchlist_surface_behaviors_contract -v`
Expected: `FAIL` because the `3.18` and `3.19` portfolio/watchlist behavior sections do not exist yet.

- [ ] **Step 3: Commit**

```bash
git add tests/contracts/test_portfolio_watchlist_surface_behaviors_contract.py
git commit -m "test: add portfolio watchlist surface behavior checks"
```

### Task 2: Patch the portfolio/watchlist surface-behavior narrative

**Files:**
- Modify: `spec/finance_research_spec.md`
- Test: `tests/contracts/test_portfolio_watchlist_surface_behaviors_contract.py`

- [ ] **Step 1: Add the first-surface behavior sections**

```md
### 3.18 Portfolio and watchlist first surface behaviors

- Manual watchlist and portfolio-held surfaces reuse the same thin quote-on-read row hydration contract rather than inventing separate quote-fetch behavior for held subjects.
- Portfolio-held rows layer held-state context, quantity, and optional cost-basis context on top of that shared quote row skeleton.
- The first surface behavior stays intentionally light: it does not define a portfolio analytics dashboard, brokerage position card, or private quote model distinct from symbol entry.
- If a subject is both watchlisted and held, the surface keeps both states visible rather than collapsing one concept into the other.
- Selecting a row from either a watchlist or portfolio-held surface enters the same symbol-detail route keyed by canonical subject identity.
- Entered subject views may show lightweight saved-state and held-state context plus adjacent actions, but that context augments the existing quote snapshot and subject modules rather than creating a portfolio-specific subject shell.
- Watchlist and holdings state remain user-owned overlay context on top of shared subject and market-data contracts.

### 3.19 Downstream consumer rules for portfolio and watchlist surface behaviors

- Dynamic watchlists and portfolio overlays (`P4.7`) depends on shared quote-row behavior and stable subject-view augmentation so later theme, screen, portfolio, and watchlist combinations can add more context without rewriting the base surfaces.
- Export and share policy (`P6.4`) depends on user-owned watchlist and holdings context staying visually and semantically distinct from canonical quote and subject content so later export or share rules can reason about what private overlay state may travel with a shared artifact.
```

- [ ] **Step 2: Run the surface-behavior contract tests and confirm green**

Run: `python3 -m unittest tests.contracts.test_portfolio_watchlist_surface_behaviors_contract tests.contracts.test_holdings_model_overlay_inputs_contract tests.contracts.test_manual_watchlist_management_baseline_contract tests.contracts.test_symbol_search_quote_snapshot_surface_contract -v`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add spec/finance_research_spec.md
git commit -m "docs: define portfolio watchlist surface behaviors"
```

### Task 3: Verify and land the bead

**Files:**
- Modify: `.beads/issues.jsonl` (via `bd close` / `bd sync`)
- Test: `tests/contracts/test_portfolio_watchlist_surface_behaviors_contract.py`

- [ ] **Step 1: Inspect repo state**

Run: `git status --short`
Expected: only the intended surface-behavior files and bead metadata changes remain, plus known unrelated local untracked files.

- [ ] **Step 2: Close the bead**

Run: `bd --no-daemon close stock-agent-h3e.2.5.2 --reason "Completed"`
Expected: bead marked `closed`

- [ ] **Step 3: Sync bead metadata**

Run: `bd --no-daemon sync`
Expected: `.beads/issues.jsonl` updated for the closed bead state

- [ ] **Step 4: Re-run the surface-behavior contract tests after bead sync**

Run: `python3 -m unittest tests.contracts.test_portfolio_watchlist_surface_behaviors_contract tests.contracts.test_holdings_model_overlay_inputs_contract tests.contracts.test_manual_watchlist_management_baseline_contract tests.contracts.test_symbol_search_quote_snapshot_surface_contract -v`
Expected: `OK`

- [ ] **Step 5: Commit bead metadata if needed**

```bash
git add .beads/issues.jsonl docs/superpowers/plans/2026-04-22-portfolio-watchlist-surface-behaviors.md
git commit -m "chore: sync bead status for stock-agent-h3e.2.5.2"
```

Only do this if `bd sync` changed tracked files that are not already committed.

- [ ] **Step 6: Pull, push, and confirm remote state**

Run: `git pull --rebase && git push && git status`
Expected: rebase succeeds, push succeeds, and status reports the branch is up to date with origin.
