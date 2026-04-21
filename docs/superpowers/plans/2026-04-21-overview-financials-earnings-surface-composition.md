# Overview Financials And Earnings Surface Composition Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the deterministic `overview`, `financials`, and `earnings` tab responsibilities explicit in the narrative spec so symbol-detail composition, later tab integrations, and downstream product surfaces share one stable surface contract.

**Architecture:** Treat this bead as a narrative surface-contract update, not a UI implementation. Add a file-based contract test that asserts the tab-responsibility, service-dependency, navigation, and downstream-consumer wording anchors exist, watch it fail first, then patch the `3.4` symbol-detail section with dedicated composition subsections.

**Tech Stack:** Markdown spec, Python 3 `unittest`

---

## File Structure

- Modify: `spec/finance_research_spec.md`
  Responsibility: expand the symbol-detail product-surface section with core tab responsibilities, shared dependency rules, navigation expectations, and downstream consumer notes.
- Create: `tests/contracts/test_overview_financials_earnings_surface_composition_contract.py`
  Responsibility: file-level contract checks enforcing the tab-boundary, shared-dependency, navigation, and downstream-consumer wording anchors.

### Task 1: Add failing symbol-detail composition contract checks

**Files:**
- Create: `tests/contracts/test_overview_financials_earnings_surface_composition_contract.py`
- Test: `tests/contracts/test_overview_financials_earnings_surface_composition_contract.py`

- [ ] **Step 1: Write the failing test**

```python
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"


class OverviewFinancialsEarningsSurfaceCompositionContractTest(unittest.TestCase):
    def test_spec_declares_core_symbol_tab_responsibilities(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "### 3.4.1 Overview, financials, and earnings tab composition",
            spec_text,
        )
        self.assertIn(
            "`overview` owns the deterministic single-subject summary that extends the thin quote landing state into a durable core tab.",
            spec_text,
        )
        self.assertIn(
            "`overview` composes listing-aware quote context, company profile context, key stats, and a limited performance or context summary, but it does not become a second home for full statement tables, holders, or interpretive evidence flows.",
            spec_text,
        )
        self.assertIn(
            "`financials` owns normalized statement tables, statement-linked trend views, and segment-aware financial breakdowns for the selected subject.",
            spec_text,
        )
        self.assertIn(
            "`financials` composes normalized statement outputs plus the aggregation layer for key stats and segment facts rather than rebuilding fundamentals logic from provider-specific payloads.",
            spec_text,
        )
        self.assertIn(
            "`earnings` owns deterministic earnings chronology, expectation-versus-result views, and consensus summaries for the selected subject.",
            spec_text,
        )
        self.assertIn(
            "`earnings` composes earnings-release events, EPS surprise history, analyst consensus, and price-target context without turning transcript reading, news clustering, or freeform commentary into tab-owned responsibilities.",
            spec_text,
        )

    def test_spec_declares_shared_dependencies_and_navigation_rules(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "### 3.4.2 Shared dependencies and navigation expectations for core symbol tabs",
            spec_text,
        )
        self.assertIn(
            "All three tabs live inside the same subject-detail shell and share the same subject header context, nested-route navigation model, and public-route assumptions already established for symbol detail.",
            spec_text,
        )
        self.assertIn(
            "The core tab composition depends on hydrated subject identity, market quote and series services, fundamentals profile and statement services, aggregation outputs, and structured earnings events through backend contracts rather than direct provider payloads or chat-style tool loops.",
            spec_text,
        )
        self.assertIn(
            "Moving between `overview`, `financials`, and `earnings` preserves subject context and shell chrome; it is a local section transition, not a new top-level workspace or a fresh subject-resolution flow.",
            spec_text,
        )
        self.assertIn(
            "The tabs may link to one another through stable section destinations, but they must not collapse into one scrolling page or duplicate ownership of the same deterministic modules.",
            spec_text,
        )
        self.assertIn(
            "Holders, signals or Reddit, and Analyze entry points remain outside this bead and layer onto the subject-detail shell after the core tab responsibilities are fixed.",
            spec_text,
        )

    def test_spec_declares_downstream_consumers_for_core_symbol_tabs(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "### 3.4.3 Downstream consumer rules for core symbol tabs",
            spec_text,
        )
        self.assertIn(
            "Holders, Reddit, and Analyze tab integration (`P1.3b`) depends on `overview`, `financials`, and `earnings` having stable deterministic responsibilities so later holders, Reddit, and Analyze entry points can attach without redefining the core symbol-detail tabs.",
            spec_text,
        )
        self.assertIn(
            "Analyze template system (`P4.2`) depends on the explicit boundary between deterministic symbol tabs and later artifact-driven analysis so Analyze can launch from symbol detail without inheriting ownership of overview, financials, or earnings composition.",
            spec_text,
        )
        self.assertIn(
            "Home feed (`P4.4`) depends on stable symbol-tab destinations and shared subject context so findings and summaries can deep-link into the right deterministic surface instead of inventing custom readouts per card.",
            spec_text,
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.contracts.test_overview_financials_earnings_surface_composition_contract -v`
Expected: `FAIL` because the `3.4.1`, `3.4.2`, and `3.4.3` symbol-detail composition sections do not exist yet.

- [ ] **Step 3: Commit**

```bash
git add tests/contracts/test_overview_financials_earnings_surface_composition_contract.py
git commit -m "test: add symbol detail composition checks"
```

### Task 2: Patch the symbol-detail composition narrative

**Files:**
- Modify: `spec/finance_research_spec.md`
- Test: `tests/contracts/test_overview_financials_earnings_surface_composition_contract.py`

- [ ] **Step 1: Add composition subsections under `3.4`**

```md
### 3.4.1 Overview, financials, and earnings tab composition

- `overview` owns the deterministic single-subject summary that extends the thin quote landing state into a durable core tab.
- `overview` composes listing-aware quote context, company profile context, key stats, and a limited performance or context summary, but it does not become a second home for full statement tables, holders, or interpretive evidence flows.
- `financials` owns normalized statement tables, statement-linked trend views, and segment-aware financial breakdowns for the selected subject.
- `financials` composes normalized statement outputs plus the aggregation layer for key stats and segment facts rather than rebuilding fundamentals logic from provider-specific payloads.
- `earnings` owns deterministic earnings chronology, expectation-versus-result views, and consensus summaries for the selected subject.
- `earnings` composes earnings-release events, EPS surprise history, analyst consensus, and price-target context without turning transcript reading, news clustering, or freeform commentary into tab-owned responsibilities.

### 3.4.2 Shared dependencies and navigation expectations for core symbol tabs

- All three tabs live inside the same subject-detail shell and share the same subject header context, nested-route navigation model, and public-route assumptions already established for symbol detail.
- The core tab composition depends on hydrated subject identity, market quote and series services, fundamentals profile and statement services, aggregation outputs, and structured earnings events through backend contracts rather than direct provider payloads or chat-style tool loops.
- Moving between `overview`, `financials`, and `earnings` preserves subject context and shell chrome; it is a local section transition, not a new top-level workspace or a fresh subject-resolution flow.
- The tabs may link to one another through stable section destinations, but they must not collapse into one scrolling page or duplicate ownership of the same deterministic modules.
- Holders, signals or Reddit, and Analyze entry points remain outside this bead and layer onto the subject-detail shell after the core tab responsibilities are fixed.

### 3.4.3 Downstream consumer rules for core symbol tabs

- Holders, Reddit, and Analyze tab integration (`P1.3b`) depends on `overview`, `financials`, and `earnings` having stable deterministic responsibilities so later holders, Reddit, and Analyze entry points can attach without redefining the core symbol-detail tabs.
- Analyze template system (`P4.2`) depends on the explicit boundary between deterministic symbol tabs and later artifact-driven analysis so Analyze can launch from symbol detail without inheriting ownership of overview, financials, or earnings composition.
- Home feed (`P4.4`) depends on stable symbol-tab destinations and shared subject context so findings and summaries can deep-link into the right deterministic surface instead of inventing custom readouts per card.
```

- [ ] **Step 2: Run the symbol-detail composition contract tests and confirm green**

Run: `python3 -m unittest tests.contracts.test_overview_financials_earnings_surface_composition_contract tests.contracts.test_symbol_search_quote_snapshot_surface_contract tests.contracts.test_stats_segment_consensus_aggregations_contract -v`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add spec/finance_research_spec.md
git commit -m "docs: define core symbol tab composition"
```

### Task 3: Verify and land the bead

**Files:**
- Modify: `.beads/issues.jsonl` (via `bd close` / `bd sync`)
- Test: `tests/contracts/test_overview_financials_earnings_surface_composition_contract.py`

- [ ] **Step 1: Inspect repo state**

Run: `git status --short`
Expected: only the intended symbol-detail contract files and bead metadata changes remain, plus any known unrelated local untracked files.

- [ ] **Step 2: Close the bead**

Run: `bd close stock-agent-h3e.2.3.1 --reason "Completed"`
Expected: bead marked `closed`

- [ ] **Step 3: Sync bead metadata**

Run: `bd sync`
Expected: `.beads/issues.jsonl` updated for the closed bead state

- [ ] **Step 4: Re-run the symbol-detail composition contract tests after bead sync**

Run: `python3 -m unittest tests.contracts.test_overview_financials_earnings_surface_composition_contract tests.contracts.test_symbol_search_quote_snapshot_surface_contract tests.contracts.test_stats_segment_consensus_aggregations_contract -v`
Expected: `OK`

- [ ] **Step 5: Commit bead metadata if needed**

```bash
git add .beads/issues.jsonl docs/superpowers/plans/2026-04-21-overview-financials-earnings-surface-composition.md
git commit -m "chore: sync bead status for stock-agent-h3e.2.3.1"
```

Only do this if `bd sync` changed tracked files that are not already committed.

- [ ] **Step 6: Pull, push, and confirm remote state**

Run: `git pull --rebase && git push && git status`
Expected: rebase succeeds, push succeeds, and status reports the branch is up to date with origin.
