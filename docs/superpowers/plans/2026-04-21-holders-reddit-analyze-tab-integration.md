# Holders Reddit And Analyze Tab Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the `holders` section, Reddit-like `signals` entry points, and `Analyze` launch behavior explicit in the narrative spec so symbol detail and later artifact-driven work share one stable handoff contract.

**Architecture:** Treat this bead as a narrative surface-and-handoff contract update, not a UI implementation. Add a file-based contract test that asserts the holders boundary, `signals` placement, `Analyze` launch rules, and downstream consumer notes exist, watch it fail first, then patch the `3.4` symbol-detail section with dedicated integration subsections.

**Tech Stack:** Markdown spec, Python 3 `unittest`

---

## File Structure

- Modify: `spec/finance_research_spec.md`
  Responsibility: expand the symbol-detail product-surface section with `holders` ownership, `signals` or Reddit-like entry rules, `Analyze` handoff behavior, and downstream consumer notes.
- Create: `tests/contracts/test_holders_reddit_analyze_tab_integration_contract.py`
  Responsibility: file-level contract checks enforcing the handoff boundary, signals placement, Analyze launch rules, and downstream consumer anchors.

### Task 1: Add failing holders and Analyze integration contract checks

**Files:**
- Create: `tests/contracts/test_holders_reddit_analyze_tab_integration_contract.py`
- Test: `tests/contracts/test_holders_reddit_analyze_tab_integration_contract.py`

- [ ] **Step 1: Write the failing test**

```python
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"


class HoldersRedditAnalyzeTabIntegrationContractTest(unittest.TestCase):
    def test_spec_declares_holders_signals_and_analyze_boundaries(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "### 3.4.4 Holders, signals, and Analyze entry integration",
            spec_text,
        )
        self.assertIn(
            "`holders` remains the deterministic symbol-detail section for institutional and insider holder views tied to the selected subject.",
            spec_text,
        )
        self.assertIn(
            "`holders` composes structured holder outputs from the fundamentals service and remains distinct from portfolio overlays, watchlist state, and user-owned monitoring context.",
            spec_text,
        )
        self.assertIn(
            "`signals` remains the symbol-detail section for Reddit-like community views, news pulse, and future alt-data entry points; this bead does not replace that route bucket with a source-specific `reddit` shell contract.",
            spec_text,
        )
        self.assertIn(
            "Reddit-like or news-specialized content inside `signals` composes evidence-backed blocks, claim clusters, evidence bundles, and trend-style renderers rather than raw social-text panes or provider-specific mini-pages.",
            spec_text,
        )
        self.assertIn(
            "`Analyze` remains a top-level workspace rather than a durable nested symbol-detail section.",
            spec_text,
        )
        self.assertIn(
            "Symbol detail launches `Analyze` with carried `SubjectRef` context or an explicit analyze intent, but resulting artifacts live on the shared snapshot and block plane rather than inside a persistent symbol-detail tab.",
            spec_text,
        )

    def test_spec_declares_navigation_and_handoff_rules(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "### 3.4.5 Navigation and handoff rules for holders, signals, and Analyze",
            spec_text,
        )
        self.assertIn(
            "Entering `holders` or `signals` from symbol detail preserves subject context inside the same nested-route family and subject-detail shell.",
            spec_text,
        )
        self.assertIn(
            "Launching `Analyze` from symbol detail is a workspace transition that still preserves carried subject context and does not reinterpret the subject from raw ticker text.",
            spec_text,
        )
        self.assertIn(
            "The handoff from symbol detail into `Analyze` stays explicit so later shared-artifact and replay flows can point to durable snapshot-backed artifacts instead of scraped UI state.",
            spec_text,
        )
        self.assertIn(
            "This bead does not redefine the core deterministic ownership of `overview`, `financials`, or `earnings`; it layers adjacent sections and launch points on top of that contract.",
            spec_text,
        )

    def test_spec_declares_downstream_consumers_for_holders_and_analyze_entry(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "### 3.4.6 Downstream consumer rules for holders, signals, and Analyze entry work",
            spec_text,
        )
        self.assertIn(
            "Analyze template system (`P4.2`) depends on explicit handoff from symbol detail into top-level `Analyze` with carried subject context so template and saved-workflow work can distinguish launch context from tab ownership.",
            spec_text,
        )
        self.assertIn(
            "Shared artifact flow (`P4.3`) depends on `Analyze` entry from symbol detail producing artifact and snapshot boundaries outside the symbol-detail shell so add-to-chat or replay flows import a sealed artifact instead of scraping tab state.",
            spec_text,
        )
        self.assertIn(
            "Specialized social and news blocks (`P4.6`) depends on Reddit-like entry living under `signals` and composing shared evidence-backed blocks so specialized social or news views do not redefine the symbol shell or bypass the block registry.",
            spec_text,
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.contracts.test_holders_reddit_analyze_tab_integration_contract -v`
Expected: `FAIL` because the `3.4.4`, `3.4.5`, and `3.4.6` symbol-detail integration sections do not exist yet.

- [ ] **Step 3: Commit**

```bash
git add tests/contracts/test_holders_reddit_analyze_tab_integration_contract.py
git commit -m "test: add symbol detail handoff checks"
```

### Task 2: Patch the symbol-detail handoff narrative

**Files:**
- Modify: `spec/finance_research_spec.md`
- Test: `tests/contracts/test_holders_reddit_analyze_tab_integration_contract.py`

- [ ] **Step 1: Add integration subsections under `3.4`**

```md
### 3.4.4 Holders, signals, and Analyze entry integration

- `holders` remains the deterministic symbol-detail section for institutional and insider holder views tied to the selected subject.
- `holders` composes structured holder outputs from the fundamentals service and remains distinct from portfolio overlays, watchlist state, and user-owned monitoring context.
- `signals` remains the symbol-detail section for Reddit-like community views, news pulse, and future alt-data entry points; this bead does not replace that route bucket with a source-specific `reddit` shell contract.
- Reddit-like or news-specialized content inside `signals` composes evidence-backed blocks, claim clusters, evidence bundles, and trend-style renderers rather than raw social-text panes or provider-specific mini-pages.
- `Analyze` remains a top-level workspace rather than a durable nested symbol-detail section.
- Symbol detail launches `Analyze` with carried `SubjectRef` context or an explicit analyze intent, but resulting artifacts live on the shared snapshot and block plane rather than inside a persistent symbol-detail tab.

### 3.4.5 Navigation and handoff rules for holders, signals, and Analyze

- Entering `holders` or `signals` from symbol detail preserves subject context inside the same nested-route family and subject-detail shell.
- Launching `Analyze` from symbol detail is a workspace transition that still preserves carried subject context and does not reinterpret the subject from raw ticker text.
- The handoff from symbol detail into `Analyze` stays explicit so later shared-artifact and replay flows can point to durable snapshot-backed artifacts instead of scraped UI state.
- This bead does not redefine the core deterministic ownership of `overview`, `financials`, or `earnings`; it layers adjacent sections and launch points on top of that contract.

### 3.4.6 Downstream consumer rules for holders, signals, and Analyze entry work

- Analyze template system (`P4.2`) depends on explicit handoff from symbol detail into top-level `Analyze` with carried subject context so template and saved-workflow work can distinguish launch context from tab ownership.
- Shared artifact flow (`P4.3`) depends on `Analyze` entry from symbol detail producing artifact and snapshot boundaries outside the symbol-detail shell so add-to-chat or replay flows import a sealed artifact instead of scraping tab state.
- Specialized social and news blocks (`P4.6`) depends on Reddit-like entry living under `signals` and composing shared evidence-backed blocks so specialized social or news views do not redefine the symbol shell or bypass the block registry.
```

- [ ] **Step 2: Run the symbol-detail handoff contract tests and confirm green**

Run: `python3 -m unittest tests.contracts.test_holders_reddit_analyze_tab_integration_contract tests.contracts.test_overview_financials_earnings_surface_composition_contract tests.contracts.test_workspace_shell_route_skeleton_contract tests.contracts.test_snapshot_semantics_contract tests.contracts.test_block_schema_contract -v`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add spec/finance_research_spec.md
git commit -m "docs: define symbol detail handoff rules"
```

### Task 3: Verify and land the bead

**Files:**
- Modify: `.beads/issues.jsonl` (via `bd close` / `bd sync`)
- Test: `tests/contracts/test_holders_reddit_analyze_tab_integration_contract.py`

- [ ] **Step 1: Inspect repo state**

Run: `git status --short`
Expected: only the intended symbol-detail handoff files and bead metadata changes remain, plus any known unrelated local untracked files.

- [ ] **Step 2: Close the bead**

Run: `bd close stock-agent-h3e.2.3.2 --reason "Completed"`
Expected: bead marked `closed`

- [ ] **Step 3: Sync bead metadata**

Run: `bd sync`
Expected: `.beads/issues.jsonl` updated for the closed bead state

- [ ] **Step 4: Re-run the symbol-detail handoff contract tests after bead sync**

Run: `python3 -m unittest tests.contracts.test_holders_reddit_analyze_tab_integration_contract tests.contracts.test_overview_financials_earnings_surface_composition_contract tests.contracts.test_workspace_shell_route_skeleton_contract tests.contracts.test_snapshot_semantics_contract tests.contracts.test_block_schema_contract -v`
Expected: `OK`

- [ ] **Step 5: Commit bead metadata if needed**

```bash
git add .beads/issues.jsonl docs/superpowers/plans/2026-04-21-holders-reddit-analyze-tab-integration.md
git commit -m "chore: sync bead status for stock-agent-h3e.2.3.2"
```

Only do this if `bd sync` changed tracked files that are not already committed.

- [ ] **Step 6: Pull, push, and confirm remote state**

Run: `git pull --rebase && git push && git status`
Expected: rebase succeeds, push succeeds, and status reports the branch is up to date with origin.
