# Quote And Bar Provider Abstraction Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the market-data provider boundary explicit in the narrative spec so quote and bar consumers share one provider-neutral contract before adjusted-series, symbol-detail, routing, and scale-hardening work build on it.

**Architecture:** Treat this bead as a narrative contract update, not a provider integration or cache implementation. Add a file-based contract test that asserts the provider-neutral boundary, quote responsibilities, bar responsibilities, and downstream consumer notes exist, watch it fail first, then patch the `6.2` market-data section in the main spec with dedicated quote/bar abstraction subsections.

**Tech Stack:** Markdown spec, Python 3 `unittest`

---

## File Structure

- Modify: `spec/finance_research_spec.md`
  Responsibility: expand the market-data section with provider-neutral boundary rules, quote retrieval responsibilities, bar retrieval responsibilities, and downstream consumer notes for later market, symbol-detail, routing, and scale-hardening work.
- Create: `tests/contracts/test_quote_bar_provider_abstraction_contract.py`
  Responsibility: file-level contract checks enforcing the provider-neutral boundary, listing-oriented retrieval rule, normalized quote fields, normalized bar metadata, and downstream consumer wording anchors in the narrative spec.

### Task 1: Add failing quote-and-bar provider abstraction checks

**Files:**
- Create: `tests/contracts/test_quote_bar_provider_abstraction_contract.py`
- Test: `tests/contracts/test_quote_bar_provider_abstraction_contract.py`

- [ ] **Step 1: Write the failing test**

```python
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"


class QuoteBarProviderAbstractionContractTest(unittest.TestCase):
    def test_spec_declares_provider_neutral_market_data_boundary(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 6.2.1 Quote and bar provider abstraction", spec_text)
        self.assertIn(
            "Market data service is the sole internal boundary for quote and bar provider interaction.",
            spec_text,
        )
        self.assertIn(
            "Downstream consumers call the market data service or analyst tools rather than provider SDKs, raw provider endpoints, or provider-specific payload helpers.",
            spec_text,
        )
        self.assertIn(
            "Quote and bar retrieval start from listing-appropriate hydrated subject context or a listing `SubjectRef`, not from raw ticker strings, venue text, or provider identifiers standing in for canonical market identity.",
            spec_text,
        )
        self.assertIn(
            "Provider adapters normalize provider-specific response shapes, identifiers, rate limits, and availability quirks into stable internal market records before those records reach downstream consumers.",
            spec_text,
        )
        self.assertIn(
            "The provider-neutral contract preserves `as_of`, `delay_class`, `currency`, and `source_id` for quote and bar retrieval, plus `adjustment_basis` whenever a bar response has already crossed an adjustment boundary.",
            spec_text,
        )

    def test_spec_declares_quote_and_bar_responsibilities(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "Quote retrieval owns the latest listing-oriented market snapshot for a tradable subject.",
            spec_text,
        )
        self.assertIn(
            "The normalized quote contract covers latest price, absolute move, percentage move, freshness or session state, `as_of`, `delay_class`, `currency`, and `source_id`.",
            spec_text,
        )
        self.assertIn(
            "Quote retrieval is lightweight and snapshot-oriented; it does not answer historical range questions, adjusted-series questions, or comparison normalization.",
            spec_text,
        )
        self.assertIn(
            "Bar retrieval owns ordered intraday and historical OHLCV series for a listing-oriented subject across a requested range and interval.",
            spec_text,
        )
        self.assertIn(
            "The normalized bar contract exposes requested subject identity, range, interval, `as_of`, `delay_class`, `currency`, `source_id`, and `adjustment_basis`.",
            spec_text,
        )
        self.assertIn(
            "Comparison charts, adjusted-series APIs, and snapshot-safe transform rules consume this bar contract later rather than bypassing it with provider-specific chart fetches.",
            spec_text,
        )

    def test_spec_declares_provider_abstraction_downstream_consumers(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "### 6.2.2 Downstream consumer rules for quote and bar provider abstraction",
            spec_text,
        )
        self.assertIn(
            "Adjusted series query and caching surface (`P1.1b`) depends on the provider-neutral quote and bar boundary, normalized market metadata fields, and the explicit split between snapshot reads and ordered time-series retrieval.",
            spec_text,
        )
        self.assertIn(
            "Symbol detail surfaces (`P1.3`) depends on a stable quote snapshot contract and reusable bar retrieval boundary so symbol modules do not embed provider-specific market fetch logic.",
            spec_text,
        )
        self.assertIn(
            "Pre-resolve router and budget policy (`P2.2`) depends on the distinction between lightweight quote reads and heavier historical-bar reads so routing and budget policy can choose the right market-data cost class without guessing from provider names or ticker text.",
            spec_text,
        )
        self.assertIn(
            "Scale hardening (`P6.5`) depends on a provider-neutral market-data seam with explicit freshness and source metadata so bottleneck audits, caching, and hardening work optimize the boundary rather than coupling consumers to one upstream vendor.",
            spec_text,
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.contracts.test_quote_bar_provider_abstraction_contract -v`
Expected: `FAIL` because the `6.2.1` and `6.2.2` provider-abstraction sections do not exist yet.

- [ ] **Step 3: Commit**

```bash
git add tests/contracts/test_quote_bar_provider_abstraction_contract.py
git commit -m "test: add quote bar provider abstraction checks"
```

### Task 2: Patch the market-data provider abstraction narrative

**Files:**
- Modify: `spec/finance_research_spec.md`
- Test: `tests/contracts/test_quote_bar_provider_abstraction_contract.py`

- [ ] **Step 1: Add provider-abstraction subsections under `6.2`**

```md
### 6.2.1 Quote and bar provider abstraction

- Market data service is the sole internal boundary for quote and bar provider interaction.
- Downstream consumers call the market data service or analyst tools rather than provider SDKs, raw provider endpoints, or provider-specific payload helpers.
- Quote and bar retrieval start from listing-appropriate hydrated subject context or a listing `SubjectRef`, not from raw ticker strings, venue text, or provider identifiers standing in for canonical market identity.
- Provider adapters normalize provider-specific response shapes, identifiers, rate limits, and availability quirks into stable internal market records before those records reach downstream consumers.
- The provider-neutral contract preserves `as_of`, `delay_class`, `currency`, and `source_id` for quote and bar retrieval, plus `adjustment_basis` whenever a bar response has already crossed an adjustment boundary.
- Corporate actions remain part of the market data service domain, but this bead only establishes that provider normalization may depend on them; adjusted-series and cache semantics belong to `P1.1b`.
- Quote retrieval owns the latest listing-oriented market snapshot for a tradable subject.
- The normalized quote contract covers latest price, absolute move, percentage move, freshness or session state, `as_of`, `delay_class`, `currency`, and `source_id`.
- Quote retrieval is lightweight and snapshot-oriented; it does not answer historical range questions, adjusted-series questions, or comparison normalization.
- Bar retrieval owns ordered intraday and historical OHLCV series for a listing-oriented subject across a requested range and interval.
- The normalized bar contract exposes requested subject identity, range, interval, `as_of`, `delay_class`, `currency`, `source_id`, and `adjustment_basis`.
- Comparison charts, adjusted-series APIs, and snapshot-safe transform rules consume this bar contract later rather than bypassing it with provider-specific chart fetches.

### 6.2.2 Downstream consumer rules for quote and bar provider abstraction

- Adjusted series query and caching surface (`P1.1b`) depends on the provider-neutral quote and bar boundary, normalized market metadata fields, and the explicit split between snapshot reads and ordered time-series retrieval.
- Symbol detail surfaces (`P1.3`) depends on a stable quote snapshot contract and reusable bar retrieval boundary so symbol modules do not embed provider-specific market fetch logic.
- Pre-resolve router and budget policy (`P2.2`) depends on the distinction between lightweight quote reads and heavier historical-bar reads so routing and budget policy can choose the right market-data cost class without guessing from provider names or ticker text.
- Scale hardening (`P6.5`) depends on a provider-neutral market-data seam with explicit freshness and source metadata so bottleneck audits, caching, and hardening work optimize the boundary rather than coupling consumers to one upstream vendor.
```

- [ ] **Step 2: Run the provider-abstraction contract test and confirm green**

Run: `python3 -m unittest tests.contracts.test_quote_bar_provider_abstraction_contract -v`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add spec/finance_research_spec.md
git commit -m "docs: define quote and bar provider abstraction"
```

### Task 3: Verify and land the bead

**Files:**
- Modify: `.beads/issues.jsonl` (via `bd close` / `bd sync`)
- Test: `tests/contracts/test_quote_bar_provider_abstraction_contract.py`

- [ ] **Step 1: Inspect repo state**

Run: `git status --short`
Expected: only the intended market-data contract files and bead metadata changes remain, plus any known unrelated local untracked files.

- [ ] **Step 2: Close the bead**

Run: `bd close stock-agent-h3e.2.1.1 --reason "Completed"`
Expected: bead marked `closed`

- [ ] **Step 3: Sync bead metadata**

Run: `bd sync`
Expected: `.beads/issues.jsonl` updated for the closed bead state

- [ ] **Step 4: Re-run the provider-abstraction contract test after bead sync**

Run: `python3 -m unittest tests.contracts.test_quote_bar_provider_abstraction_contract -v`
Expected: `OK`

- [ ] **Step 5: Commit bead metadata if needed**

```bash
git add .beads/issues.jsonl docs/superpowers/plans/2026-04-21-quote-bar-provider-abstraction.md
git commit -m "chore: sync bead status for stock-agent-h3e.2.1.1"
```

Only do this if `bd sync` changed tracked files that are not already committed.

- [ ] **Step 6: Pull, push, and confirm remote state**

Run: `git pull --rebase && git push && git status`
Expected: rebase succeeds, push succeeds, and status reports the branch is up to date with origin.
