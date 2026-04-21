# Adjusted Series Query And Caching Surface Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make adjusted-series identity, cache assumptions, and snapshot-safe reuse explicit in the narrative spec so deterministic consumers and interactive blocks share one stable market-series contract before symbol surfaces, renderer work, international coverage, and scale hardening build on it.

**Architecture:** Treat this bead as a narrative contract update, not a cache implementation or UI build. Add a file-based contract test that asserts the adjusted-series query surface, basis rules, cache correctness boundary, snapshot-safe reuse rules, and downstream consumer notes exist, watch it fail first, then patch the `6.2` market-data section with dedicated adjusted-series subsections.

**Tech Stack:** Markdown spec, Python 3 `unittest`

---

## File Structure

- Modify: `spec/finance_research_spec.md`
  Responsibility: add adjusted-series query and caching subsections under the market-data service that define series identity, basis semantics, cache correctness assumptions, snapshot-safe reuse, and downstream consumers.
- Create: `tests/contracts/test_adjusted_series_query_caching_surface_contract.py`
  Responsibility: file-level contract checks enforcing adjusted-series identity, cache assumptions, snapshot-safe reuse, coverage semantics, and downstream consumer wording anchors in the narrative spec.

### Task 1: Add failing adjusted-series contract checks

**Files:**
- Create: `tests/contracts/test_adjusted_series_query_caching_surface_contract.py`
- Test: `tests/contracts/test_adjusted_series_query_caching_surface_contract.py`

- [ ] **Step 1: Write the failing test**

```python
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"


class AdjustedSeriesQueryCachingSurfaceContractTest(unittest.TestCase):
    def test_spec_declares_adjusted_series_identity_and_basis_rules(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 6.2.3 Adjusted series query and caching semantics", spec_text)
        self.assertIn(
            "Adjusted series query is the market-data surface above raw bar retrieval that produces comparison-ready or interactive time series from canonical listing subject input.",
            spec_text,
        )
        self.assertIn(
            "Series queries bind explicit `subject_refs`, `range`, `interval`, `basis`, and `normalization` before execution, caching, and snapshot binding.",
            spec_text,
        )
        self.assertIn(
            "Market-series basis remains explicit: `unadjusted`, `split_adjusted`, and `split_and_div_adjusted`.",
            spec_text,
        )
        self.assertIn(
            "The service must not silently mix bases inside one returned series set, one chart artifact, or one comparison response.",
            spec_text,
        )
        self.assertIn(
            "Series responses expose the effective coverage window and any partial or unavailable history explicitly rather than backfilling missing periods or implying full coverage.",
            spec_text,
        )

    def test_spec_declares_cache_assumptions_and_snapshot_safe_reuse(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "Cache is an internal optimization behind the market data service, not a separate semantic source of truth for charts, symbol tabs, or blocks.",
            spec_text,
        )
        self.assertIn(
            "Cache identity includes the canonical subject set, range, interval, basis, normalization, and freshness boundary used for the series request.",
            spec_text,
        )
        self.assertIn(
            "A cache hit may reuse prior series material only when the request preserves subject membership, basis, normalization, and does not require data newer than the request or snapshot `as_of`.",
            spec_text,
        )
        self.assertIn(
            "If basis, normalization, peer set, or freshness changes, the system treats that as a different series request and refreshes or recomputes rather than mutating a cached answer in place.",
            spec_text,
        )
        self.assertIn(
            "In-snapshot transforms may reuse cached series only when the requested range or interval is already legal under the sealed snapshot manifest and remains inside `allowed_transforms`.",
            spec_text,
        )
        self.assertIn(
            "Changing basis or normalization is out-of-snapshot behavior even if compatible cached material exists somewhere in storage.",
            spec_text,
        )

    def test_spec_declares_adjusted_series_downstream_consumers(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "### 6.2.4 Downstream consumer rules for adjusted series query and caching",
            spec_text,
        )
        self.assertIn(
            "Symbol detail surfaces (`P1.3`) depends on explicit basis and coverage semantics so price charts and comparison modules do not silently switch between adjusted and unadjusted histories.",
            spec_text,
        )
        self.assertIn(
            "Block registry and initial block catalog (`P2.3`) depends on stable series query identity and in-snapshot cache reuse rules so interactive blocks know which transforms are legal without redefining market semantics per block kind.",
            spec_text,
        )
        self.assertIn(
            "Specialized social and news blocks (`P4.6`) depends on the same series semantics and cache contract for trend-style blocks so source-specific renderers reuse shared market rules rather than inventing bespoke chart caching behavior.",
            spec_text,
        )
        self.assertIn(
            "Non US identity data and coverage gaps (`P6.2`) depends on explicit basis, coverage-window, and partial-history rules so later international work can surface venue and provider differences without pretending uniform history quality.",
            spec_text,
        )
        self.assertIn(
            "Scale hardening (`P6.5`) depends on the declared cache identity and refresh rules so audits and ops work optimize hit rate and storage layout without weakening snapshot correctness.",
            spec_text,
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.contracts.test_adjusted_series_query_caching_surface_contract -v`
Expected: `FAIL` because the `6.2.3` and `6.2.4` adjusted-series sections do not exist yet.

- [ ] **Step 3: Commit**

```bash
git add tests/contracts/test_adjusted_series_query_caching_surface_contract.py
git commit -m "test: add adjusted series query caching checks"
```

### Task 2: Patch the adjusted-series narrative contract

**Files:**
- Modify: `spec/finance_research_spec.md`
- Test: `tests/contracts/test_adjusted_series_query_caching_surface_contract.py`

- [ ] **Step 1: Add adjusted-series subsections under `6.2`**

```md
### 6.2.3 Adjusted series query and caching semantics

- Adjusted series query is the market-data surface above raw bar retrieval that produces comparison-ready or interactive time series from canonical listing subject input.
- Series queries bind explicit `subject_refs`, `range`, `interval`, `basis`, and `normalization` before execution, caching, and snapshot binding.
- Market-series basis remains explicit: `unadjusted`, `split_adjusted`, and `split_and_div_adjusted`.
- The service must not silently mix bases inside one returned series set, one chart artifact, or one comparison response.
- Multi-subject performance responses share one basis, one normalization, one `as_of`, and one requested range contract even when coverage start differs by subject.
- Series responses expose the effective coverage window and any partial or unavailable history explicitly rather than backfilling missing periods or implying full coverage.
- Cache is an internal optimization behind the market data service, not a separate semantic source of truth for charts, symbol tabs, or blocks.
- Cache identity includes the canonical subject set, range, interval, basis, normalization, and freshness boundary used for the series request.
- A cache hit may reuse prior series material only when the request preserves subject membership, basis, normalization, and does not require data newer than the request or snapshot `as_of`.
- Cache hits and misses must return the same observable contract: stable series semantics, explicit `as_of`, preserved basis or `adjustment_basis`, and the same provenance-facing metadata as uncached reads.
- If basis, normalization, peer set, or freshness changes, the system treats that as a different series request and refreshes or recomputes rather than mutating a cached answer in place.
- In-snapshot transforms may reuse cached series only when the requested range or interval is already legal under the sealed snapshot manifest and remains inside `allowed_transforms`.
- Changing basis or normalization is out-of-snapshot behavior even if compatible cached material exists somewhere in storage.

### 6.2.4 Downstream consumer rules for adjusted series query and caching

- Symbol detail surfaces (`P1.3`) depends on explicit basis and coverage semantics so price charts and comparison modules do not silently switch between adjusted and unadjusted histories.
- Block registry and initial block catalog (`P2.3`) depends on stable series query identity and in-snapshot cache reuse rules so interactive blocks know which transforms are legal without redefining market semantics per block kind.
- Specialized social and news blocks (`P4.6`) depends on the same series semantics and cache contract for trend-style blocks so source-specific renderers reuse shared market rules rather than inventing bespoke chart caching behavior.
- Non US identity data and coverage gaps (`P6.2`) depends on explicit basis, coverage-window, and partial-history rules so later international work can surface venue and provider differences without pretending uniform history quality.
- Scale hardening (`P6.5`) depends on the declared cache identity and refresh rules so audits and ops work optimize hit rate and storage layout without weakening snapshot correctness.
```

- [ ] **Step 2: Run the adjusted-series contract test and confirm green**

Run: `python3 -m unittest tests.contracts.test_adjusted_series_query_caching_surface_contract -v`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add spec/finance_research_spec.md
git commit -m "docs: define adjusted series query caching surface"
```

### Task 3: Verify and land the bead

**Files:**
- Modify: `.beads/issues.jsonl` (via `bd close` / `bd sync`)
- Test: `tests/contracts/test_adjusted_series_query_caching_surface_contract.py`

- [ ] **Step 1: Inspect repo state**

Run: `git status --short`
Expected: only the intended adjusted-series contract files and bead metadata changes remain, plus any known unrelated local untracked files.

- [ ] **Step 2: Close the bead**

Run: `bd close stock-agent-h3e.2.1.2 --reason "Completed"`
Expected: bead marked `closed`

- [ ] **Step 3: Sync bead metadata**

Run: `bd sync`
Expected: `.beads/issues.jsonl` updated for the closed bead state

- [ ] **Step 4: Re-run the adjusted-series contract test after bead sync**

Run: `python3 -m unittest tests.contracts.test_adjusted_series_query_caching_surface_contract -v`
Expected: `OK`

- [ ] **Step 5: Commit bead metadata if needed**

```bash
git add .beads/issues.jsonl docs/superpowers/plans/2026-04-21-adjusted-series-query-caching-surface.md
git commit -m "chore: sync bead status for stock-agent-h3e.2.1.2"
```

Only do this if `bd sync` changed tracked files that are not already committed.

- [ ] **Step 6: Pull, push, and confirm remote state**

Run: `git pull --rebase && git push && git status`
Expected: rebase succeeds, push succeeds, and status reports the branch is up to date with origin.
