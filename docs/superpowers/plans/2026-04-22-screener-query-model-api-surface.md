# Screener Query Model And API Surface Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the first screener query model and API boundary explicit in the narrative spec so later screener UI and dynamic list flows consume one stable query-and-result contract.

**Architecture:** Treat this bead as a service-boundary contract update, not a screener UI implementation. Add a file-based contract test that asserts the screening-service section defines structured query dimensions, row semantics, and service ownership. Watch that test fail first, then patch the screener service section with dedicated `6.7.1` and `6.7.2` subsections.

**Tech Stack:** Markdown spec, Python 3 `unittest`

---

## File Structure

- Modify: `spec/finance_research_spec.md`
  Responsibility: expand the screening-service section with the screener query-and-result contract plus downstream-consumer rules.
- Create: `tests/contracts/test_screener_query_model_api_surface_contract.py`
  Responsibility: file-level contract checks enforcing query-model, result-semantics, service-boundary, and downstream-consumer anchors.

### Task 1: Add failing screener query contract checks

**Files:**
- Create: `tests/contracts/test_screener_query_model_api_surface_contract.py`
- Test: `tests/contracts/test_screener_query_model_api_surface_contract.py`

- [ ] **Step 1: Write the failing test**

```python
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"


class ScreenerQueryModelApiSurfaceContractTest(unittest.TestCase):
    def test_spec_declares_screener_query_model(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 6.7.1 Screener query model and result contract", spec_text)
        self.assertIn(
            "Screener queries are explicit structured filter-and-rank envelopes rather than a freeform analytics DSL or arbitrary user-authored formulas.",
            spec_text,
        )
        self.assertIn(
            "The minimum query dimensions are universe constraints, market or quote constraints, fundamentals or aggregate constraints, sort specification, and page or limit controls.",
            spec_text,
        )
        self.assertIn(
            "Query clauses bind to screener-owned fields backed by the market-data and fundamentals services rather than exposing raw provider payload columns or frontend-computed joins.",
            spec_text,
        )

    def test_spec_declares_screener_result_semantics_and_service_boundary(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "A screener response is an ordered derived result set rather than a new canonical identity type for returned entities.",
            spec_text,
        )
        self.assertIn(
            "Each result row carries canonical market subject identity, display identity, ranking or sort context, and compact quote or fundamentals summaries sufficient for screener-table rendering.",
            spec_text,
        )
        self.assertIn(
            "Screener rows remain thinner than symbol-detail hydration: selecting a row hands off canonical subject identity for later subject-entry flows rather than embedding a full symbol workspace payload.",
            spec_text,
        )
        self.assertIn(
            "A reusable `screen` subject represents the persisted query definition plus ordering semantics, not a frozen list of prehydrated row payloads.",
            spec_text,
        )
        self.assertIn(
            "The Screener service owns query validation, execution, ranking, pagination, and row-envelope assembly.",
            spec_text,
        )
        self.assertIn(
            "`/v1/screener/*` remains the client boundary for screener queries and results, even when the service internally reads market-data and fundamentals outputs.",
            spec_text,
        )
        self.assertIn(
            "Clients must not reconstruct screener tables by fanning out across `/v1/market/*` and `/v1/fundamentals/*` and inventing their own join semantics.",
            spec_text,
        )

    def test_spec_declares_screener_downstream_consumers(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 6.7.2 Downstream consumer rules for screener query work", spec_text)
        self.assertIn(
            "Screener UI flow and saved-screen handoff (`P1.4b`) depends on stable query envelopes and result-row semantics so later screener surface and saved-screen work can reuse one service-owned screener contract instead of inventing a second client-side model.",
            spec_text,
        )
        self.assertIn(
            "Dynamic watchlists and portfolio overlays (`P4.7`) depends on screen definitions remaining replayable, service-owned query objects so later dynamic watchlists can regenerate a screen universe without scraping transient UI state or storing raw row payloads as truth.",
            spec_text,
        )


if __name__ == \"__main__\":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.contracts.test_screener_query_model_api_surface_contract -v`
Expected: `FAIL` because the `6.7.1` and `6.7.2` screener contract sections do not exist yet.

- [ ] **Step 3: Commit**

```bash
git add tests/contracts/test_screener_query_model_api_surface_contract.py
git commit -m "test: add screener query model contract checks"
```

### Task 2: Patch the screener service narrative

**Files:**
- Modify: `spec/finance_research_spec.md`
- Test: `tests/contracts/test_screener_query_model_api_surface_contract.py`

- [ ] **Step 1: Add the screener service subsections**

```md
### 6.7.1 Screener query model and result contract

- Screener queries are explicit structured filter-and-rank envelopes rather than a freeform analytics DSL or arbitrary user-authored formulas.
- The minimum query dimensions are universe constraints, market or quote constraints, fundamentals or aggregate constraints, sort specification, and page or limit controls.
- Query clauses bind to screener-owned fields backed by the market-data and fundamentals services rather than exposing raw provider payload columns or frontend-computed joins.
- A screener response is an ordered derived result set rather than a new canonical identity type for returned entities.
- Each result row carries canonical market subject identity, display identity, ranking or sort context, and compact quote or fundamentals summaries sufficient for screener-table rendering.
- Screener rows remain thinner than symbol-detail hydration: selecting a row hands off canonical subject identity for later subject-entry flows rather than embedding a full symbol workspace payload.
- A reusable `screen` subject represents the persisted query definition plus ordering semantics, not a frozen list of prehydrated row payloads.
- The Screener service owns query validation, execution, ranking, pagination, and row-envelope assembly.
- `/v1/screener/*` remains the client boundary for screener queries and results, even when the service internally reads market-data and fundamentals outputs.
- Clients must not reconstruct screener tables by fanning out across `/v1/market/*` and `/v1/fundamentals/*` and inventing their own join semantics.

### 6.7.2 Downstream consumer rules for screener query work

- Screener UI flow and saved-screen handoff (`P1.4b`) depends on stable query envelopes and result-row semantics so later screener surface and saved-screen work can reuse one service-owned screener contract instead of inventing a second client-side model.
- Dynamic watchlists and portfolio overlays (`P4.7`) depends on screen definitions remaining replayable, service-owned query objects so later dynamic watchlists can regenerate a screen universe without scraping transient UI state or storing raw row payloads as truth.
```

- [ ] **Step 2: Run the screener contract tests and confirm green**

Run: `python3 -m unittest tests.contracts.test_screener_query_model_api_surface_contract tests.contracts.test_workspace_shell_route_skeleton_contract tests.contracts.test_tool_registry_contract -v`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add spec/finance_research_spec.md
git commit -m "docs: define screener query model api surface"
```

### Task 3: Verify and land the bead

**Files:**
- Modify: `.beads/issues.jsonl` (via `bd close` / `bd sync`)
- Test: `tests/contracts/test_screener_query_model_api_surface_contract.py`

- [ ] **Step 1: Inspect repo state**

Run: `git status --short`
Expected: only the intended screener-contract files and bead metadata changes remain, plus known unrelated local untracked files.

- [ ] **Step 2: Close the bead**

Run: `bd --no-daemon close stock-agent-h3e.2.4.1 --reason "Completed"`
Expected: bead marked `closed`

- [ ] **Step 3: Sync bead metadata**

Run: `bd --no-daemon sync`
Expected: `.beads/issues.jsonl` updated for the closed bead state

- [ ] **Step 4: Re-run the screener contract tests after bead sync**

Run: `python3 -m unittest tests.contracts.test_screener_query_model_api_surface_contract tests.contracts.test_workspace_shell_route_skeleton_contract tests.contracts.test_tool_registry_contract -v`
Expected: `OK`

- [ ] **Step 5: Commit bead metadata if needed**

```bash
git add .beads/issues.jsonl docs/superpowers/plans/2026-04-22-screener-query-model-api-surface.md
git commit -m "chore: sync bead status for stock-agent-h3e.2.4.1"
```

Only do this if `bd sync` changed tracked files that are not already committed.

- [ ] **Step 6: Pull, push, and confirm remote state**

Run: `git pull --rebase && git push && git status`
Expected: rebase succeeds, push succeeds, and status reports the branch is up to date with origin.
