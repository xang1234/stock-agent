# Manual Watchlist Management Baseline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the first manual watchlist baseline explicit in the narrative spec so saved-subject membership, thin quote row hydration, and add-to-watchlist auth behavior share one stable contract before portfolio basics, dynamic lists, and automation extend it.

**Architecture:** Treat this bead as a narrative list-baseline contract update, not a watchlist UI build or persistence implementation. Add a file-based contract test that asserts the single-list baseline, membership-only CRUD floor, quote-on-read row hydration, inline auth-resume add rule, and downstream consumer notes exist, watch it fail first, then patch the narrative spec with a dedicated manual-watchlist subsection and consumer matrix.

**Tech Stack:** Markdown spec, Python 3 `unittest`

---

## File Structure

- Modify: `spec/finance_research_spec.md`
  Responsibility: add a new manual-watchlist baseline section after the early-symbol-entry rules, defining the implicit default manual watchlist, membership-only CRUD floor, quote-on-read row hydration, and inline auth-resume add behavior.
- Create: `tests/contracts/test_manual_watchlist_management_baseline_contract.py`
  Responsibility: file-level contract checks enforcing the single-list baseline, membership CRUD floor, quote-on-read hydration, mutation rules, and downstream consumer wording anchors in the narrative spec.

### Task 1: Add failing manual-watchlist baseline checks

**Files:**
- Create: `tests/contracts/test_manual_watchlist_management_baseline_contract.py`
- Test: `tests/contracts/test_manual_watchlist_management_baseline_contract.py`

- [ ] **Step 1: Write the failing test**

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.contracts.test_manual_watchlist_management_baseline_contract -v`
Expected: `FAIL` because the manual-watchlist baseline section and downstream consumer wording do not exist yet.

- [ ] **Step 3: Commit**

```bash
git add tests/contracts/test_manual_watchlist_management_baseline_contract.py
git commit -m "test: add manual watchlist management baseline checks"
```

### Task 2: Patch the manual-watchlist narrative contract

**Files:**
- Modify: `spec/finance_research_spec.md`
- Test: `tests/contracts/test_manual_watchlist_management_baseline_contract.py`

- [ ] **Step 1: Add the new manual-watchlist baseline section after `3.13`**

```md
### 3.14 Manual watchlist management baseline

- The product starts from one implicit default manual watchlist as the baseline saved-subject model.
- The manual baseline CRUD floor is membership-only: view current members, add a resolved subject, and remove a saved subject.
- This bead does not define create-list, rename-list, delete-list, sharing, reordering, or multiple manual lists.
- The persisted membership unit is canonical subject identity rather than raw ticker strings or stored quote payloads.
- Membership is idempotent at the subject level, so adding the same canonical subject twice does not create duplicates.
- Manual watchlist rows hydrate quote context on read from saved canonical subject identity rather than storing quote payloads in membership records.
- The row hydration contract is lightweight: subject display identity, listing-sensitive symbol context when applicable, latest price, absolute move, percentage move, and freshness or session state.
- Quote row hydration reuses the same listing-oriented market identity rule as early symbol entry rather than inventing a watchlist-specific quote identity model.
- Add-to-watchlist from public subject routes uses the existing inline auth interrupt contract: if the user is unauthenticated, the current route and pending resolved subject are preserved and the add resumes after sign-in.
- Removing a member changes watchlist membership only and does not mutate the underlying subject, quote snapshot, or later portfolio overlay state.
```

- [ ] **Step 2: Add the downstream consumer matrix for the manual baseline**

```md
### 3.15 Downstream consumer rules for manual watchlist baseline work

- Portfolio and watchlist basics (`P1.5`) depends on the simple saved-subject baseline and quote row behavior that later portfolio and holdings surfaces build on.
- Dynamic watchlists and portfolio overlays (`P4.7`) depends on the manual list baseline that later derivation modes and overlay behavior extend rather than replace.
- Agent CRUD and scheduling (`P5.1`) depends on a simple, user-owned list object and membership model that later automation or agent creation flows may target without inventing a separate subject collection system.
```

- [ ] **Step 3: Run the manual-watchlist contract test and confirm green**

Run: `python3 -m unittest tests.contracts.test_manual_watchlist_management_baseline_contract -v`
Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add spec/finance_research_spec.md
git commit -m "docs: define manual watchlist management baseline"
```

### Task 3: Verify and land the bead

**Files:**
- Modify: `.beads/issues.jsonl` (via `bd close` / `bd sync`)
- Modify: `docs/superpowers/plans/2026-04-21-manual-watchlist-management-baseline.md` if the plan file itself was not yet committed
- Test: `tests/contracts/test_manual_watchlist_management_baseline_contract.py`

- [ ] **Step 1: Inspect repo state**

Run: `git status --short`
Expected: only the intended spec, test, plan, and bead metadata changes remain, plus the known unrelated untracked baseline files.

- [ ] **Step 2: Close the bead**

Run: `bd close stock-agent-h3e.1.4.2 --reason "Completed"`
Expected: bead marked `closed`

- [ ] **Step 3: Sync bead metadata**

Run: `bd sync`
Expected: `.beads/issues.jsonl` updated for the closed bead state

- [ ] **Step 4: Re-run the manual-watchlist contract test after bead sync**

Run: `python3 -m unittest tests.contracts.test_manual_watchlist_management_baseline_contract -v`
Expected: `OK`

- [ ] **Step 5: Commit bead metadata if needed**

```bash
git add .beads/issues.jsonl docs/superpowers/plans/2026-04-21-manual-watchlist-management-baseline.md
git commit -m "chore: sync bead status for stock-agent-h3e.1.4.2"
```

Only do this if `bd sync` changed tracked files that are not already committed.

- [ ] **Step 6: Publish the feature branch**

Run: `git push -u origin stock-agent-h3e.1.4.2`
Expected: remote branch updated successfully

- [ ] **Step 7: Fast-forward `main` and verify there**

Run: `git checkout main && git pull --rebase origin main && git merge --ff-only stock-agent-h3e.1.4.2 && python3 -m unittest tests.contracts.test_manual_watchlist_management_baseline_contract -v`
Expected: fast-forward merge succeeds and the manual-watchlist contract test reports `OK`

- [ ] **Step 8: Push `main` and verify final status**

Run: `git push origin main && git status`
Expected: `main` is up to date with `origin/main`, with only the known unrelated untracked baseline files remaining

- [ ] **Step 9: Delete the local feature branch**

Run: `git branch -d stock-agent-h3e.1.4.2`
Expected: local feature branch deleted after the fast-forward merge
