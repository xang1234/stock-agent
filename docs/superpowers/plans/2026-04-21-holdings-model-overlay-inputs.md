# Holdings Model And Overlay Inputs Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the lightweight holdings model, `base_currency` assumptions, and overlay-input boundary explicit in the narrative spec so later portfolio surfaces and overlay features share one stable contract.

**Architecture:** Treat this bead as a narrative holdings-and-overlay contract update, not a portfolio UI or brokerage implementation. Add a file-based contract test that asserts the holdings scope, `base_currency` meaning, `PortfolioHolding` assumptions, and downstream consumer notes exist, watch it fail first, then patch the product-surface and research-subject sections with dedicated holdings subsections.

**Tech Stack:** Markdown spec, Python 3 `unittest`

---

## File Structure

- Modify: `spec/finance_research_spec.md`
  Responsibility: refine the portfolio statement, add holdings-scope and downstream-consumer subsections under product surfaces, and add `Portfolio` / `PortfolioHolding` / overlay-input rules under the research-subject model.
- Create: `tests/contracts/test_holdings_model_overlay_inputs_contract.py`
  Responsibility: file-level contract checks enforcing holdings scope, `base_currency` assumptions, overlay-input rules, and downstream consumer anchors.

### Task 1: Add failing holdings-model and overlay-input contract checks

**Files:**
- Create: `tests/contracts/test_holdings_model_overlay_inputs_contract.py`
- Test: `tests/contracts/test_holdings_model_overlay_inputs_contract.py`

- [ ] **Step 1: Write the failing test**

```python
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"


class HoldingsModelOverlayInputsContractTest(unittest.TestCase):
    def test_spec_declares_holdings_scope_and_base_currency(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "Watchlists support `manual`, `screen`, `agent`, `theme`, and `portfolio` modes. Portfolio is lightweight holdings tracking for overlay context and monitoring, not brokerage execution.",
            spec_text,
        )
        self.assertIn(
            "### 3.16 Portfolio holdings model and overlay inputs",
            spec_text,
        )
        self.assertIn(
            "Portfolio support remains lightweight research context: it tracks held exposure for overlays and monitoring, not brokerage execution, order management, tax lots, cash ledgers, or settlement workflows.",
            spec_text,
        )
        self.assertIn(
            "A portfolio owns one explicit `base_currency` that defines the reporting currency for holding cost assumptions and later overlay totals.",
            spec_text,
        )
        self.assertIn(
            "`base_currency` is a reporting and comparison assumption, not proof that the underlying listing trades in that currency and not a full FX accounting model.",
            spec_text,
        )
        self.assertIn(
            "Manual watchlists and holdings remain separate: saving a subject does not create a holding, and holding a subject does not implicitly add it to a watchlist.",
            spec_text,
        )

    def test_spec_declares_portfolio_holding_and_overlay_input_rules(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "### 4.2.1 Portfolio holding and overlay input rules",
            spec_text,
        )
        self.assertIn(
            "`Portfolio` is a user-owned research container, not a brokerage account surrogate.",
            spec_text,
        )
        self.assertIn(
            "`Portfolio.base_currency` is required and interprets `cost_basis` plus any portfolio-level overlay totals in one explicit reporting currency.",
            spec_text,
        )
        self.assertIn(
            "`PortfolioHolding` binds to canonical market identity, typically `instrument` or `listing`, and must not persist raw ticker strings or higher-order subjects such as `theme`, `macro_topic`, `portfolio`, or `screen` as holding identity.",
            spec_text,
        )
        self.assertIn(
            "`cost_basis` is optional and, when present, is interpreted in the containing portfolio's `base_currency`; this bead does not define separate transaction currencies, FX lots, or fee-adjusted basis accounting.",
            spec_text,
        )
        self.assertIn(
            "Overlay inputs derived from holdings are read models keyed by subject and contributing portfolio, not new canonical subject identities or stored UI payloads.",
            spec_text,
        )
        self.assertIn(
            "The minimum overlay input contract is held-state, contributing `portfolio_id`, quantity, optional cost basis context, and a base-currency label for any derived valuation or gain/loss display.",
            spec_text,
        )
        self.assertIn(
            "If multiple portfolios hold the same subject with different base currencies, this bead keeps those contributions distinct rather than silently netting them through an implicit FX layer.",
            spec_text,
        )

    def test_spec_declares_holdings_downstream_consumers(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "### 3.17 Downstream consumer rules for holdings model and overlay inputs",
            spec_text,
        )
        self.assertIn(
            "Portfolio and watchlist surface behaviors (`P1.5b`) depends on the lightweight holdings scope and explicit `base_currency` assumption so first-surface behaviors can render held-state and cost context without inventing brokerage rules.",
            spec_text,
        )
        self.assertIn(
            "Dynamic watchlists and portfolio overlays (`P4.7`) depends on holdings producing reusable overlay inputs rather than UI-owned ad hoc calculations so later overlay layers can merge portfolio context with watchlists, themes, screens, and subject views consistently.",
            spec_text,
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.contracts.test_holdings_model_overlay_inputs_contract -v`
Expected: `FAIL` because the holdings-model sections and `4.2.1` overlay-input wording do not exist yet.

- [ ] **Step 3: Commit**

```bash
git add tests/contracts/test_holdings_model_overlay_inputs_contract.py
git commit -m "test: add holdings model overlay input checks"
```

### Task 2: Patch the holdings-model narrative contract

**Files:**
- Modify: `spec/finance_research_spec.md`
- Test: `tests/contracts/test_holdings_model_overlay_inputs_contract.py`

- [ ] **Step 1: Add the holdings and overlay-input sections**

```md
### 3.6 Watchlists and portfolio
Watchlists support `manual`, `screen`, `agent`, `theme`, and `portfolio` modes. Portfolio is lightweight holdings tracking for overlay context and monitoring, not brokerage execution.

### 3.16 Portfolio holdings model and overlay inputs

- Portfolio support remains lightweight research context: it tracks held exposure for overlays and monitoring, not brokerage execution, order management, tax lots, cash ledgers, or settlement workflows.
- A portfolio owns one explicit `base_currency` that defines the reporting currency for holding cost assumptions and later overlay totals.
- `base_currency` is a reporting and comparison assumption, not proof that the underlying listing trades in that currency and not a full FX accounting model.
- Holdings persist canonical market subject identity plus quantity, optional cost basis, and open or closed timestamps rather than raw ticker strings, provider payloads, or transaction histories.
- The holdings model does not require lot-by-lot reconstruction, realized tax accounting, fee capture, margin state, or order history.
- Manual watchlists and holdings remain separate: saving a subject does not create a holding, and holding a subject does not implicitly add it to a watchlist.

### 3.17 Downstream consumer rules for holdings model and overlay inputs

- Portfolio and watchlist surface behaviors (`P1.5b`) depends on the lightweight holdings scope and explicit `base_currency` assumption so first-surface behaviors can render held-state and cost context without inventing brokerage rules.
- Dynamic watchlists and portfolio overlays (`P4.7`) depends on holdings producing reusable overlay inputs rather than UI-owned ad hoc calculations so later overlay layers can merge portfolio context with watchlists, themes, screens, and subject views consistently.

### 4.2.1 Portfolio holding and overlay input rules

- `Portfolio` is a user-owned research container, not a brokerage account surrogate.
- `Portfolio.base_currency` is required and interprets `cost_basis` plus any portfolio-level overlay totals in one explicit reporting currency.
- `PortfolioHolding` binds to canonical market identity, typically `instrument` or `listing`, and must not persist raw ticker strings or higher-order subjects such as `theme`, `macro_topic`, `portfolio`, or `screen` as holding identity.
- `cost_basis` is optional and, when present, is interpreted in the containing portfolio's `base_currency`; this bead does not define separate transaction currencies, FX lots, or fee-adjusted basis accounting.
- Overlay inputs derived from holdings are read models keyed by subject and contributing portfolio, not new canonical subject identities or stored UI payloads.
- The minimum overlay input contract is held-state, contributing `portfolio_id`, quantity, optional cost basis context, and a base-currency label for any derived valuation or gain/loss display.
- If multiple portfolios hold the same subject with different base currencies, this bead keeps those contributions distinct rather than silently netting them through an implicit FX layer.
```

- [ ] **Step 2: Run the holdings-model contract tests and confirm green**

Run: `python3 -m unittest tests.contracts.test_holdings_model_overlay_inputs_contract tests.contracts.test_manual_watchlist_management_baseline_contract tests.contracts.test_symbol_search_quote_snapshot_surface_contract -v`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add spec/finance_research_spec.md
git commit -m "docs: define holdings model overlay inputs"
```

### Task 3: Verify and land the bead

**Files:**
- Modify: `.beads/issues.jsonl` (via `bd close` / `bd sync`)
- Test: `tests/contracts/test_holdings_model_overlay_inputs_contract.py`

- [ ] **Step 1: Inspect repo state**

Run: `git status --short`
Expected: only the intended holdings-contract files and bead metadata changes remain, plus known unrelated local untracked files.

- [ ] **Step 2: Close the bead**

Run: `bd --no-daemon close stock-agent-h3e.2.5.1 --reason "Completed"`
Expected: bead marked `closed`

- [ ] **Step 3: Sync bead metadata**

Run: `bd --no-daemon sync`
Expected: `.beads/issues.jsonl` updated for the closed bead state

- [ ] **Step 4: Re-run the holdings-model contract tests after bead sync**

Run: `python3 -m unittest tests.contracts.test_holdings_model_overlay_inputs_contract tests.contracts.test_manual_watchlist_management_baseline_contract tests.contracts.test_symbol_search_quote_snapshot_surface_contract -v`
Expected: `OK`

- [ ] **Step 5: Commit bead metadata if needed**

```bash
git add .beads/issues.jsonl docs/superpowers/plans/2026-04-21-holdings-model-overlay-inputs.md
git commit -m "chore: sync bead status for stock-agent-h3e.2.5.1"
```

Only do this if `bd sync` changed tracked files that are not already committed.

- [ ] **Step 6: Pull, push, and confirm remote state**

Run: `git pull --rebase && git push && git status`
Expected: rebase succeeds, push succeeds, and status reports the branch is up to date with origin.
