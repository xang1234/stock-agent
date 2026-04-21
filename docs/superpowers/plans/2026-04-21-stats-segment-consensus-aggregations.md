# Stats Segment And Consensus Aggregations Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the fundamentals aggregation-layer boundary, family separation, and downstream consumer rules explicit in the narrative spec so deterministic consumers share one stable aggregation contract before symbol composition, specialized blocks, and hard-case coverage work build on it.

**Architecture:** Treat this bead as a narrative contract update, not an implementation of the aggregation engine. Add a file-based contract test that asserts the aggregation-layer boundary, service-level ownership, family-specific rules, warning semantics, and downstream consumer notes exist, watch it fail first, then patch the `6.3` fundamentals section with dedicated aggregation subsections.

**Tech Stack:** Markdown spec, Python 3 `unittest`

---

## File Structure

- Modify: `spec/finance_research_spec.md`
  Responsibility: expand the fundamentals section with aggregation-layer rules, family separation, coverage and warning semantics, and downstream consumer notes.
- Create: `tests/contracts/test_stats_segment_consensus_aggregations_contract.py`
  Responsibility: file-level contract checks enforcing the aggregation boundary, family-specific wording, ownership rules, and downstream consumer anchors.

### Task 1: Add failing aggregation contract checks

**Files:**
- Create: `tests/contracts/test_stats_segment_consensus_aggregations_contract.py`
- Test: `tests/contracts/test_stats_segment_consensus_aggregations_contract.py`

- [ ] **Step 1: Write the failing test**

```python
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"


class StatsSegmentConsensusAggregationsContractTest(unittest.TestCase):
    def test_spec_declares_aggregation_boundary_and_families(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 6.3.3 Stats, segment, and consensus aggregations", spec_text)
        self.assertIn(
            "The fundamentals aggregation layer sits above normalized statement facts and canonical metrics and produces reusable read models for key stats, segment facts, analyst consensus, and comparison-ready derived outputs.",
            spec_text,
        )
        self.assertIn(
            "Aggregation outputs are service-level views, not replacements for canonical `Fact` or `Computation` rows, and they must keep their derivation inputs, freshness, and coverage assumptions explicit.",
            spec_text,
        )
        self.assertIn(
            "Key stats and derived ratios may combine normalized fundamentals, market context, and deterministic computations, but they must expose the basis, period, and `as_of` assumptions needed to explain each value.",
            spec_text,
        )
        self.assertIn(
            "Segment facts remain distinct from consolidated statement outputs: they carry segment axis, segment definitions, period context, and coverage warnings instead of flattening segment disclosures into issuer-level statement tables.",
            spec_text,
        )
        self.assertIn(
            "Analyst consensus remains distinct from both reported statements and promoted evidence facts: rating distributions, price-target summaries, analyst counts, and coverage warnings are service-level aggregates with explicit `as_of` semantics.",
            spec_text,
        )
        self.assertIn(
            "Comparison-ready derived outputs may package reusable aggregate slices for peer views or ranking-style surfaces, but they must not become an opaque cache of UI-specific payloads.",
            spec_text,
        )

    def test_spec_declares_aggregation_warning_and_ownership_rules(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "When aggregation inputs are incomplete, stale, or inconsistent, the service surfaces warnings and partial-coverage metadata instead of fabricating complete comparisons or silently filling gaps.",
            spec_text,
        )
        self.assertIn(
            "The aggregation layer may read canonical facts, computations, and provider-backed consensus or segment inputs, but provenance, supersession, and truth-promotion state remain owned by the canonical value plane.",
            spec_text,
        )

    def test_spec_declares_aggregation_downstream_consumers(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "### 6.3.4 Downstream consumer rules for aggregation outputs",
            spec_text,
        )
        self.assertIn(
            "Symbol detail surfaces (`P1.3`) depends on separate stats, segment, and consensus aggregation families so overview, financials, and earnings modules can reuse deterministic read models instead of rebuilding UI-specific payloads from raw statements.",
            spec_text,
        )
        self.assertIn(
            "Pre-resolve router and budget policy (`P2.2`) depends on the distinction between normalized statement reads and aggregation-layer reads so routing can classify heavier fundamentals requests before the tool loop starts.",
            spec_text,
        )
        self.assertIn(
            "Specialized social and news blocks (`P4.6`) depends on reusable key stats and consensus outputs so narrative product blocks can cite stable aggregate envelopes without embedding ad hoc ratio or target-calculation logic.",
            spec_text,
        )
        self.assertIn(
            "Segment extraction refinement (`P6.1`) depends on segment aggregates preserving axis, definition, and coverage-warning semantics so harder extraction cases can evolve without changing the consumer-facing aggregation contract.",
            spec_text,
        )
        self.assertIn(
            "Non US identity data and coverage gaps (`P6.2`) depends on aggregation outputs keeping basis, freshness, and coverage assumptions explicit so later international expansion can widen issuer and provider coverage without pretending the aggregates are uniformly comparable.",
            spec_text,
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.contracts.test_stats_segment_consensus_aggregations_contract -v`
Expected: `FAIL` because the `6.3.3` and `6.3.4` aggregation sections do not exist yet.

- [ ] **Step 3: Commit**

```bash
git add tests/contracts/test_stats_segment_consensus_aggregations_contract.py
git commit -m "test: add aggregation contract checks"
```

### Task 2: Patch the aggregation narrative

**Files:**
- Modify: `spec/finance_research_spec.md`
- Test: `tests/contracts/test_stats_segment_consensus_aggregations_contract.py`

- [ ] **Step 1: Add aggregation subsections under `6.3`**

```md
### 6.3.3 Stats, segment, and consensus aggregations

- The fundamentals aggregation layer sits above normalized statement facts and canonical metrics and produces reusable read models for key stats, segment facts, analyst consensus, and comparison-ready derived outputs.
- Aggregation outputs are service-level views, not replacements for canonical `Fact` or `Computation` rows, and they must keep their derivation inputs, freshness, and coverage assumptions explicit.
- Key stats and derived ratios may combine normalized fundamentals, market context, and deterministic computations, but they must expose the basis, period, and `as_of` assumptions needed to explain each value.
- Segment facts remain distinct from consolidated statement outputs: they carry segment axis, segment definitions, period context, and coverage warnings instead of flattening segment disclosures into issuer-level statement tables.
- Analyst consensus remains distinct from both reported statements and promoted evidence facts: rating distributions, price-target summaries, analyst counts, and coverage warnings are service-level aggregates with explicit `as_of` semantics.
- Comparison-ready derived outputs may package reusable aggregate slices for peer views or ranking-style surfaces, but they must not become an opaque cache of UI-specific payloads.
- When aggregation inputs are incomplete, stale, or inconsistent, the service surfaces warnings and partial-coverage metadata instead of fabricating complete comparisons or silently filling gaps.
- The aggregation layer may read canonical facts, computations, and provider-backed consensus or segment inputs, but provenance, supersession, and truth-promotion state remain owned by the canonical value plane.

### 6.3.4 Downstream consumer rules for aggregation outputs

- Symbol detail surfaces (`P1.3`) depends on separate stats, segment, and consensus aggregation families so overview, financials, and earnings modules can reuse deterministic read models instead of rebuilding UI-specific payloads from raw statements.
- Pre-resolve router and budget policy (`P2.2`) depends on the distinction between normalized statement reads and aggregation-layer reads so routing can classify heavier fundamentals requests before the tool loop starts.
- Specialized social and news blocks (`P4.6`) depends on reusable key stats and consensus outputs so narrative product blocks can cite stable aggregate envelopes without embedding ad hoc ratio or target-calculation logic.
- Segment extraction refinement (`P6.1`) depends on segment aggregates preserving axis, definition, and coverage-warning semantics so harder extraction cases can evolve without changing the consumer-facing aggregation contract.
- Non US identity data and coverage gaps (`P6.2`) depends on aggregation outputs keeping basis, freshness, and coverage assumptions explicit so later international expansion can widen issuer and provider coverage without pretending the aggregates are uniformly comparable.
```

- [ ] **Step 2: Run the aggregation contract tests and confirm green**

Run: `python3 -m unittest tests.contracts.test_stats_segment_consensus_aggregations_contract tests.contracts.test_statement_metric_normalization_contract tests.contracts.test_tool_registry_contract -v`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add spec/finance_research_spec.md
git commit -m "docs: define aggregation output boundaries"
```

### Task 3: Verify and land the bead

**Files:**
- Modify: `.beads/issues.jsonl` (via `bd close` / `bd sync`)
- Test: `tests/contracts/test_stats_segment_consensus_aggregations_contract.py`

- [ ] **Step 1: Inspect repo state**

Run: `git status --short`
Expected: only the intended aggregation contract files and bead metadata changes remain, plus any known unrelated local untracked files.

- [ ] **Step 2: Close the bead**

Run: `bd close stock-agent-h3e.2.2.2 --reason "Completed"`
Expected: bead marked `closed`

- [ ] **Step 3: Sync bead metadata**

Run: `bd sync`
Expected: `.beads/issues.jsonl` updated for the closed bead state

- [ ] **Step 4: Re-run the aggregation contract tests after bead sync**

Run: `python3 -m unittest tests.contracts.test_stats_segment_consensus_aggregations_contract tests.contracts.test_statement_metric_normalization_contract tests.contracts.test_tool_registry_contract -v`
Expected: `OK`

- [ ] **Step 5: Commit bead metadata if needed**

```bash
git add .beads/issues.jsonl docs/superpowers/plans/2026-04-21-stats-segment-consensus-aggregations.md
git commit -m "chore: sync bead status for stock-agent-h3e.2.2.2"
```

Only do this if `bd sync` changed tracked files that are not already committed.

- [ ] **Step 6: Pull, push, and confirm remote state**

Run: `git pull --rebase && git push && git status`
Expected: rebase succeeds, push succeeds, and status reports the branch is up to date with origin.
