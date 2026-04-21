# Symbol Search And Quote Snapshot Surface Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the first symbol-search entry and thin quote snapshot landing explicit in the narrative spec so shell search, entered symbol detail, and early quote retrieval share one stable contract before manual watchlists, portfolio basics, and fuller symbol overview work arrive.

**Architecture:** Treat this bead as a narrative surface-contract update, not a UI implementation or market-data service build. Add a file-based contract test that asserts the shell-owned search entry, subject-detail landing outcome, quote snapshot minimum, listing-oriented retrieval rule, best-effort profile companion rule, and downstream consumer notes exist, watch it fail first, then patch the narrative spec with a dedicated early-symbol-entry subsection and consumer matrix.

**Tech Stack:** Markdown spec, Python 3 `unittest`

---

## File Structure

- Modify: `spec/finance_research_spec.md`
  Responsibility: add a new early-symbol-entry surface section after the auth and session rules, defining the shell-owned symbol search entry, navigation into entered symbol detail, thin quote snapshot landing contract, listing-oriented quote retrieval rule, and best-effort profile companion behavior.
- Create: `tests/contracts/test_symbol_search_quote_snapshot_surface_contract.py`
  Responsibility: file-level contract checks enforcing the shell-entry, subject-detail landing, quote snapshot minimum, best-effort profile, reuse, and downstream consumer wording anchors in the narrative spec.

### Task 1: Add failing early-symbol-entry contract checks

**Files:**
- Create: `tests/contracts/test_symbol_search_quote_snapshot_surface_contract.py`
- Test: `tests/contracts/test_symbol_search_quote_snapshot_surface_contract.py`

- [ ] **Step 1: Write the failing test**

```python
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"


class SymbolSearchQuoteSnapshotSurfaceContractTest(unittest.TestCase):
    def test_spec_declares_shell_owned_search_entry_and_navigation(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 3.12 Symbol search and quote snapshot surface", spec_text)
        self.assertIn(
            "The persistent workspace shell owns the primary symbol search entry rather than delegating search behavior to each surface.",
            spec_text,
        )
        self.assertIn(
            "Later flows such as add-to-watchlist or portfolio entry reuse the same shell-owned search contract rather than redefining symbol search per surface.",
            spec_text,
        )
        self.assertIn(
            "Candidate handling reuses the existing search-to-subject flow: unique deterministic hits may auto-advance, ambiguous hits require explicit choice, and `not_found` ends without subject hydration.",
            spec_text,
        )
        self.assertIn(
            "A successful subject resolution enters symbol detail rather than opening a detached quote page or staying inline in the originating workspace.",
            spec_text,
        )
        self.assertIn(
            "The main canvas swaps into the entered subject-detail shell while preserving the surrounding workspace shell.",
            spec_text,
        )
        self.assertIn(
            "The first quote snapshot is the initial landing state of entered symbol detail rather than a competing top-level workspace.",
            spec_text,
        )

    def test_spec_declares_thin_quote_snapshot_minimum(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "The required landing content is a market identity strip plus a price-first quote snapshot.",
            spec_text,
        )
        self.assertIn(
            "That minimum quote snapshot includes canonical subject display identity, listing-sensitive trading symbol context, latest price, absolute move, percentage move, freshness or session state, and a small recent-range or chart hook.",
            spec_text,
        )
        self.assertIn(
            "Quote retrieval is listing-oriented even when the hydrated subject bundle also carries issuer context.",
            spec_text,
        )
        self.assertIn(
            "A light issuer summary or profile companion is allowed when available, but it is best-effort and must not block the landing state.",
            spec_text,
        )
        self.assertIn(
            "This bead does not define earnings, holders, filings, peer tables, or a finished overview surface.",
            spec_text,
        )

    def test_spec_declares_downstream_consumers_for_early_symbol_entry(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "### 3.13 Downstream consumer rules for early symbol entry work",
            spec_text,
        )
        self.assertIn(
            "Manual watchlist management baseline (`P0.4b`) depends on the reusable search entry and selected-subject handoff that manual watchlist actions will sit on top of.",
            spec_text,
        )
        self.assertIn(
            "Portfolio and watchlist basics (`P1.5`) depends on the first quote and subject-entry behavior that later portfolio and watchlist basics reuse before overlays exist.",
            spec_text,
        )
        self.assertIn(
            "Symbol overview shell (`P1.3`) depends on entered symbol detail having a thin initial landing state before fuller overview, financials, and earnings composition is defined.",
            spec_text,
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.contracts.test_symbol_search_quote_snapshot_surface_contract -v`
Expected: `FAIL` because the new early-symbol-entry section and downstream consumer wording do not exist yet.

- [ ] **Step 3: Commit**

```bash
git add tests/contracts/test_symbol_search_quote_snapshot_surface_contract.py
git commit -m "test: add symbol search quote snapshot surface checks"
```

### Task 2: Patch the early-symbol-entry narrative contract

**Files:**
- Modify: `spec/finance_research_spec.md`
- Test: `tests/contracts/test_symbol_search_quote_snapshot_surface_contract.py`

- [ ] **Step 1: Add the new early-symbol-entry section after `3.11`**

```md
### 3.12 Symbol search and quote snapshot surface

- The persistent workspace shell owns the primary symbol search entry rather than delegating search behavior to each surface.
- Later flows such as add-to-watchlist or portfolio entry reuse the same shell-owned search contract rather than redefining symbol search per surface.
- Candidate handling reuses the existing search-to-subject flow: unique deterministic hits may auto-advance, ambiguous hits require explicit choice, and `not_found` ends without subject hydration.
- A successful subject resolution enters symbol detail rather than opening a detached quote page or staying inline in the originating workspace.
- The main canvas swaps into the entered subject-detail shell while preserving the surrounding workspace shell.
- The first quote snapshot is the initial landing state of entered symbol detail rather than a competing top-level workspace.
- The required landing content is a market identity strip plus a price-first quote snapshot.
- That minimum quote snapshot includes canonical subject display identity, listing-sensitive trading symbol context, latest price, absolute move, percentage move, freshness or session state, and a small recent-range or chart hook.
- Quote retrieval is listing-oriented even when the hydrated subject bundle also carries issuer context.
- A light issuer summary or profile companion is allowed when available, but it is best-effort and must not block the landing state.
- Lightweight downstream affordances such as watchlist entry or deeper symbol navigation may appear here, but they do not define full watchlist management or full symbol modules.
- This bead does not define earnings, holders, filings, peer tables, or a finished overview surface.
```

- [ ] **Step 2: Add the downstream consumer matrix for early symbol entry**

```md
### 3.13 Downstream consumer rules for early symbol entry work

- Manual watchlist management baseline (`P0.4b`) depends on the reusable search entry and selected-subject handoff that manual watchlist actions will sit on top of.
- Portfolio and watchlist basics (`P1.5`) depends on the first quote and subject-entry behavior that later portfolio and watchlist basics reuse before overlays exist.
- Symbol overview shell (`P1.3`) depends on entered symbol detail having a thin initial landing state before fuller overview, financials, and earnings composition is defined.
```

- [ ] **Step 3: Run the early-symbol-entry contract test and confirm green**

Run: `python3 -m unittest tests.contracts.test_symbol_search_quote_snapshot_surface_contract -v`
Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add spec/finance_research_spec.md
git commit -m "docs: define symbol search quote snapshot surface"
```

### Task 3: Verify and land the bead

**Files:**
- Modify: `.beads/issues.jsonl` (via `bd close` / `bd sync`)
- Modify: `docs/superpowers/plans/2026-04-21-symbol-search-quote-snapshot-surface.md` if the plan file itself was not yet committed
- Test: `tests/contracts/test_symbol_search_quote_snapshot_surface_contract.py`

- [ ] **Step 1: Inspect repo state**

Run: `git status --short`
Expected: only the intended spec, test, plan, and bead metadata changes remain, plus the known unrelated untracked baseline files.

- [ ] **Step 2: Close the bead**

Run: `bd close stock-agent-h3e.1.4.1 --reason "Completed"`
Expected: bead marked `closed`

- [ ] **Step 3: Sync bead metadata**

Run: `bd sync`
Expected: `.beads/issues.jsonl` updated for the closed bead state

- [ ] **Step 4: Re-run the early-symbol-entry contract test after bead sync**

Run: `python3 -m unittest tests.contracts.test_symbol_search_quote_snapshot_surface_contract -v`
Expected: `OK`

- [ ] **Step 5: Commit bead metadata if needed**

```bash
git add .beads/issues.jsonl docs/superpowers/plans/2026-04-21-symbol-search-quote-snapshot-surface.md
git commit -m "chore: sync bead status for stock-agent-h3e.1.4.1"
```

Only do this if `bd sync` changed tracked files that are not already committed.

- [ ] **Step 6: Publish the feature branch**

Run: `git push -u origin stock-agent-h3e.1.4.1`
Expected: remote branch updated successfully

- [ ] **Step 7: Fast-forward `main` and verify there**

Run: `git checkout main && git pull --rebase origin main && git merge --ff-only stock-agent-h3e.1.4.1 && python3 -m unittest tests.contracts.test_symbol_search_quote_snapshot_surface_contract -v`
Expected: fast-forward merge succeeds and the early-symbol-entry contract test reports `OK`

- [ ] **Step 8: Push `main` and verify final status**

Run: `git push origin main && git status`
Expected: `main` is up to date with `origin/main`, with only the known unrelated untracked baseline files remaining

- [ ] **Step 9: Delete the local feature branch**

Run: `git branch -d stock-agent-h3e.1.4.1`
Expected: local feature branch deleted after the fast-forward merge
