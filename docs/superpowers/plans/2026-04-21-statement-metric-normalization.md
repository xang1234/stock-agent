# Statement And Metric Normalization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make statement-normalization scope, metric ownership, and canonical-value relations explicit in the narrative spec so fundamentals consumers share one stable contract before aggregation, symbol-detail, routing, promotion, and international work build on it.

**Architecture:** Treat this bead as a narrative contract update, not a normalization implementation or API redesign. Add a file-based contract test that asserts the statement-normalization boundary, metric ownership rules, canonical `Fact` or `Computation` relation, and downstream consumer notes exist, watch it fail first, then patch the `6.3` fundamentals section with dedicated normalization subsections.

**Tech Stack:** Markdown spec, Python 3 `unittest`

---

## File Structure

- Modify: `spec/finance_research_spec.md`
  Responsibility: expand the fundamentals section with statement-normalization rules, metric ownership, explicit basis handling, canonical value relations, and downstream consumer notes.
- Create: `tests/contracts/test_statement_metric_normalization_contract.py`
  Responsibility: file-level contract checks enforcing normalization scope, metric ownership, canonical `Fact` or `Computation` relation, and downstream consumer wording anchors in the narrative spec.

### Task 1: Add failing statement-normalization contract checks

**Files:**
- Create: `tests/contracts/test_statement_metric_normalization_contract.py`
- Test: `tests/contracts/test_statement_metric_normalization_contract.py`

- [ ] **Step 1: Write the failing test**

```python
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"


class StatementMetricNormalizationContractTest(unittest.TestCase):
    def test_spec_declares_statement_normalization_scope_and_basis(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 6.3.1 Statement and metric normalization", spec_text)
        self.assertIn(
            "Statement normalization is the fundamentals-service layer that turns filing-backed or vendor-backed statement inputs into canonical value objects keyed by metric definitions.",
            spec_text,
        )
        self.assertIn(
            "Statement reads begin from issuer-appropriate subject context rather than listing identity or ticker-only lookup.",
            spec_text,
        )
        self.assertIn(
            "The service normalizes the three core statement families explicitly: `income`, `balance`, and `cashflow`.",
            spec_text,
        )
        self.assertIn(
            "Statement basis remains explicit at the query and output boundary: `as_reported` and `as_restated` are different normalization modes and must not be silently merged.",
            spec_text,
        )
        self.assertIn(
            "Period selection, fiscal labels, scale normalization, and unit normalization are part of the statement-normalization contract rather than caller-specific cleanup work.",
            spec_text,
        )

    def test_spec_declares_metric_ownership_and_canonical_value_relation(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "`Metric` remains the canonical definition object for what can be measured, how a value is interpreted, and which source class a normalized value belongs to.",
            spec_text,
        )
        self.assertIn(
            "Fundamentals service owns the mapping from normalized statement lines into canonical metric definitions, but it does not turn `Metric` into a mutable value store.",
            spec_text,
        )
        self.assertIn(
            "Displayed statement values resolve to `Fact` rows when the value is directly observed or promoted as truth, and to `Computation` rows when the value is deterministically derived from structured inputs.",
            spec_text,
        )
        self.assertIn(
            "Statement normalization must not introduce a second truth layer made of UI-only statement cells or provider-specific blobs that bypass `Fact` and `Computation`.",
            spec_text,
        )
        self.assertIn(
            "When source material is incomplete, conflicting, or pending promotion, the service preserves coverage and verification state through canonical value objects rather than inventing complete normalized tables.",
            spec_text,
        )

    def test_spec_declares_statement_normalization_downstream_consumers(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "### 6.3.2 Downstream consumer rules for statement and metric normalization",
            spec_text,
        )
        self.assertIn(
            "Later aggregation layer (`P1.2b`) consumes normalized issuer statement facts and canonical metrics so later aggregation work builds on one shared value layer without redefining statement normalization.",
            spec_text,
        )
        self.assertIn(
            "Symbol detail surfaces (`P1.3`) depends on normalized statement outputs carrying explicit basis, period, and coverage semantics so overview, financials, and earnings tabs can render trustworthy tables and charts.",
            spec_text,
        )
        self.assertIn(
            "Pre-resolve router and budget policy (`P2.2`) depends on the issuer-oriented normalization boundary so routing can distinguish fundamentals reads from market-data reads before the tool loop starts.",
            spec_text,
        )
        self.assertIn(
            "Promotion rules for candidate facts (`P3.5`) depends on the rule that normalized statement values become `Fact` or `Computation` objects rather than a separate fundamentals-only truth store, so promotion and supersession work target the canonical value plane.",
            spec_text,
        )
        self.assertIn(
            "Non US identity data and coverage gaps (`P6.2`) depends on explicit metric ownership, basis handling, and issuer-oriented normalization rules so later international work can extend accounting mappings without weakening the canonical value contract.",
            spec_text,
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.contracts.test_statement_metric_normalization_contract -v`
Expected: `FAIL` because the `6.3.1` and `6.3.2` normalization sections do not exist yet.

- [ ] **Step 3: Commit**

```bash
git add tests/contracts/test_statement_metric_normalization_contract.py
git commit -m "test: add statement metric normalization checks"
```

### Task 2: Patch the fundamentals normalization narrative

**Files:**
- Modify: `spec/finance_research_spec.md`
- Test: `tests/contracts/test_statement_metric_normalization_contract.py`

- [ ] **Step 1: Add normalization subsections under `6.3`**

```md
### 6.3.1 Statement and metric normalization

- Statement normalization is the fundamentals-service layer that turns filing-backed or vendor-backed statement inputs into canonical value objects keyed by metric definitions.
- Statement reads begin from issuer-appropriate subject context rather than listing identity or ticker-only lookup.
- The service normalizes the three core statement families explicitly: `income`, `balance`, and `cashflow`.
- Statement basis remains explicit at the query and output boundary: `as_reported` and `as_restated` are different normalization modes and must not be silently merged.
- Period selection, fiscal labels, scale normalization, and unit normalization are part of the statement-normalization contract rather than caller-specific cleanup work.
- `Metric` remains the canonical definition object for what can be measured, how a value is interpreted, and which source class a normalized value belongs to.
- Fundamentals service owns the mapping from normalized statement lines into canonical metric definitions, but it does not turn `Metric` into a mutable value store.
- Displayed statement values resolve to `Fact` rows when the value is directly observed or promoted as truth, and to `Computation` rows when the value is deterministically derived from structured inputs.
- Statement normalization must not introduce a second truth layer made of UI-only statement cells or provider-specific blobs that bypass `Fact` and `Computation`.
- When source material is incomplete, conflicting, or pending promotion, the service preserves coverage and verification state through canonical value objects rather than inventing complete normalized tables.

### 6.3.2 Downstream consumer rules for statement and metric normalization

- Later aggregation layer (`P1.2b`) consumes normalized issuer statement facts and canonical metrics so later aggregation work builds on one shared value layer without redefining statement normalization.
- Symbol detail surfaces (`P1.3`) depends on normalized statement outputs carrying explicit basis, period, and coverage semantics so overview, financials, and earnings tabs can render trustworthy tables and charts.
- Pre-resolve router and budget policy (`P2.2`) depends on the issuer-oriented normalization boundary so routing can distinguish fundamentals reads from market-data reads before the tool loop starts.
- Promotion rules for candidate facts (`P3.5`) depends on the rule that normalized statement values become `Fact` or `Computation` objects rather than a separate fundamentals-only truth store, so promotion and supersession work target the canonical value plane.
- Non US identity data and coverage gaps (`P6.2`) depends on explicit metric ownership, basis handling, and issuer-oriented normalization rules so later international work can extend accounting mappings without weakening the canonical value contract.
```

- [ ] **Step 2: Run the normalization contract test and confirm green**

Run: `python3 -m unittest tests.contracts.test_statement_metric_normalization_contract tests.contracts.test_truth_evidence_finding_contract tests.contracts.test_relational_schema_contract -v`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add spec/finance_research_spec.md
git commit -m "docs: define statement and metric normalization"
```

### Task 3: Verify and land the bead

**Files:**
- Modify: `.beads/issues.jsonl` (via `bd close` / `bd sync`)
- Test: `tests/contracts/test_statement_metric_normalization_contract.py`

- [ ] **Step 1: Inspect repo state**

Run: `git status --short`
Expected: only the intended normalization contract files and bead metadata changes remain, plus any known unrelated local untracked files.

- [ ] **Step 2: Close the bead**

Run: `bd close stock-agent-h3e.2.2.1 --reason "Completed"`
Expected: bead marked `closed`

- [ ] **Step 3: Sync bead metadata**

Run: `bd sync`
Expected: `.beads/issues.jsonl` updated for the closed bead state

- [ ] **Step 4: Re-run the normalization contract tests after bead sync**

Run: `python3 -m unittest tests.contracts.test_statement_metric_normalization_contract tests.contracts.test_truth_evidence_finding_contract tests.contracts.test_relational_schema_contract -v`
Expected: `OK`

- [ ] **Step 5: Commit bead metadata if needed**

```bash
git add .beads/issues.jsonl docs/superpowers/plans/2026-04-21-statement-metric-normalization.md
git commit -m "chore: sync bead status for stock-agent-h3e.2.2.1"
```

Only do this if `bd sync` changed tracked files that are not already committed.

- [ ] **Step 6: Pull, push, and confirm remote state**

Run: `git pull --rebase && git push && git status`
Expected: rebase succeeds, push succeeds, and status reports the branch is up to date with origin.
