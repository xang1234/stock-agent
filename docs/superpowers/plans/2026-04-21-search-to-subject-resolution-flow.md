# Search To Subject Resolution Flow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the search-to-subject flow explicit in the narrative spec so candidate search, canonical selection, and hydrated subject handoff follow one deterministic contract across quote snapshots, market data, fundamentals, chat pre-resolution, and watchlist entry flows.

**Architecture:** Treat this bead as a narrative flow-contract update, not a search UI or resolver implementation. Add a file-based contract test that asserts the staged-flow, auto-advance, ambiguity-stop, hydrated-bundle, persistence, and downstream-consumer wording exists, watch it fail first, then patch the narrative spec with a dedicated search-to-subject subsection and a downstream consumer matrix.

**Tech Stack:** Markdown spec, Python 3 `unittest`

---

## File Structure

- Modify: `spec/finance_research_spec.md`
  Responsibility: add the search-to-subject staged flow contract beneath the identity and resolver boundary, including candidate search rules, auto-advance behavior, ambiguity stop behavior, hydrated subject bundle contents, and durable `SubjectRef` persistence guidance.
- Create: `tests/contracts/test_search_to_subject_resolution_flow_contract.py`
  Responsibility: file-level contract checks enforcing the new staged flow, hydrated bundle, and downstream consumer wording anchors in the narrative spec.

### Task 1: Add failing search-to-subject flow checks

**Files:**
- Create: `tests/contracts/test_search_to_subject_resolution_flow_contract.py`
- Test: `tests/contracts/test_search_to_subject_resolution_flow_contract.py`

- [ ] **Step 1: Write the failing test**

```python
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"


class SearchToSubjectResolutionFlowContractTest(unittest.TestCase):
    def test_spec_declares_staged_flow_and_auto_advance_rules(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 6.1.2 Search-to-subject resolution flow", spec_text)
        self.assertIn(
            "Search-to-subject flow is the deterministic orchestration that carries lookup input from candidate search through canonical selection into downstream-safe subject hydration.",
            spec_text,
        )
        self.assertIn(
            "The staged flow is candidate search, canonical selection, and hydrated subject handoff.",
            spec_text,
        )
        self.assertIn(
            "Candidate search may return zero, one, or many candidates, but it must not invent a silent winner from ambiguous matches.",
            spec_text,
        )
        self.assertIn(
            "If candidate search yields exactly one deterministic candidate that already satisfies the resolver contract, the flow may auto-advance to canonical selection without a separate chooser step.",
            spec_text,
        )
        self.assertIn(
            "If multiple plausible candidates remain, the flow must pause at explicit ambiguity preservation and surface ranked candidates for later user or caller choice.",
            spec_text,
        )
        self.assertIn(
            "`not_found` ends the flow without subject hydration.",
            spec_text,
        )
        self.assertIn(
            "Only a `resolved` outcome may produce hydrated subject handoff.",
            spec_text,
        )

    def test_spec_declares_hydrated_subject_bundle_contract(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "The hydrated subject bundle includes the canonical `SubjectRef`, the resolved identity level, stable display labels, normalized lookup input, resolution path (`auto_advanced` or `explicit_choice`), and enough issuer, instrument, or listing context for immediate downstream use.",
            spec_text,
        )
        self.assertIn(
            "Watchlists, chat turns, Analyze entry, and service-to-service calls consume the same hydrated subject bundle contract even if they later project only the fields they need.",
            spec_text,
        )
        self.assertIn(
            "One hydrated bundle may carry joined issuer and active listing context, but the canonical `SubjectRef` remains the durable key.",
            spec_text,
        )
        self.assertIn(
            "Downstream systems persist the canonical `SubjectRef` and treat the rest of the hydrated bundle as entry context that may be refreshed later.",
            spec_text,
        )

    def test_spec_declares_search_flow_downstream_consumers(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "### 6.1.3 Downstream consumer rules for search-to-subject flow",
            spec_text,
        )
        self.assertIn(
            "Symbol search and quote snapshot surface (`P0.4`) depends on symbol search entry points, explicit candidate-choice rules, and hydrated subject handoff for quote snapshots.",
            spec_text,
        )
        self.assertIn(
            "Market data service (`P1.1`) depends on listing-appropriate subject handoff into quote and bar retrieval rather than ticker-string lookup.",
            spec_text,
        )
        self.assertIn(
            "Fundamentals service (`P1.2`) depends on issuer-appropriate subject handoff into statement and metric normalization instead of rediscovering identity downstream.",
            spec_text,
        )
        self.assertIn(
            "Pre-resolve router and budget policy (`P2.2`) depends on deterministic subject handoff so chat turns start from canonical subject context rather than ad hoc model interpretation of search strings.",
            spec_text,
        )
        self.assertIn(
            "Watchlist and saved-subject entry flows depend on the same hydrated subject bundle contract so selected subjects can be saved, reopened, and re-entered without rediscovering identity from raw lookup text.",
            spec_text,
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.contracts.test_search_to_subject_resolution_flow_contract -v`
Expected: `FAIL` because the search-to-subject staged flow section and downstream consumer wording do not exist yet.

- [ ] **Step 3: Commit**

```bash
git add tests/contracts/test_search_to_subject_resolution_flow_contract.py
git commit -m "test: add search to subject resolution flow checks"
```

### Task 2: Patch the narrative search-to-subject flow contract

**Files:**
- Modify: `spec/finance_research_spec.md`
- Test: `tests/contracts/test_search_to_subject_resolution_flow_contract.py`

- [ ] **Step 1: Add the staged flow subsection under the resolver boundary**

```md
### 6.1.2 Search-to-subject resolution flow

- Search-to-subject flow is the deterministic orchestration that carries lookup input from candidate search through canonical selection into downstream-safe subject hydration.
- The staged flow is candidate search, canonical selection, and hydrated subject handoff.
- Candidate search may return zero, one, or many candidates, but it must not invent a silent winner from ambiguous matches.
- If candidate search yields exactly one deterministic candidate that already satisfies the resolver contract, the flow may auto-advance to canonical selection without a separate chooser step.
- If multiple plausible candidates remain, the flow must pause at explicit ambiguity preservation and surface ranked candidates for later user or caller choice.
- Canonical selection consumes either the auto-advanced unique candidate or an explicit chosen candidate and normalizes it into canonical subject identity.
- `not_found` ends the flow without subject hydration.
- Only a `resolved` outcome may produce hydrated subject handoff.
- The hydrated subject bundle includes the canonical `SubjectRef`, the resolved identity level, stable display labels, normalized lookup input, resolution path (`auto_advanced` or `explicit_choice`), and enough issuer, instrument, or listing context for immediate downstream use.
- Watchlists, chat turns, Analyze entry, and service-to-service calls consume the same hydrated subject bundle contract even if they later project only the fields they need.
- One hydrated bundle may carry joined issuer and active listing context, but the canonical `SubjectRef` remains the durable key.
- Downstream systems persist the canonical `SubjectRef` and treat the rest of the hydrated bundle as entry context that may be refreshed later.
```

- [ ] **Step 2: Add the downstream consumer matrix for the flow**

```md
### 6.1.3 Downstream consumer rules for search-to-subject flow

- Symbol search and quote snapshot surface (`P0.4`) depends on symbol search entry points, explicit candidate-choice rules, and hydrated subject handoff for quote snapshots.
- Market data service (`P1.1`) depends on listing-appropriate subject handoff into quote and bar retrieval rather than ticker-string lookup.
- Fundamentals service (`P1.2`) depends on issuer-appropriate subject handoff into statement and metric normalization instead of rediscovering identity downstream.
- Pre-resolve router and budget policy (`P2.2`) depends on deterministic subject handoff so chat turns start from canonical subject context rather than ad hoc model interpretation of search strings.
- Watchlist and saved-subject entry flows depend on the same hydrated subject bundle contract so selected subjects can be saved, reopened, and re-entered without rediscovering identity from raw lookup text.
```

- [ ] **Step 3: Run the search-to-subject contract test and confirm green**

Run: `python3 -m unittest tests.contracts.test_search_to_subject_resolution_flow_contract -v`
Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add spec/finance_research_spec.md
git commit -m "docs: define search to subject resolution flow"
```

### Task 3: Verify and land the bead

**Files:**
- Modify: `.beads/issues.jsonl` (via `bd close` / `bd sync`)
- Modify: `docs/superpowers/plans/2026-04-21-search-to-subject-resolution-flow.md` if the plan file itself was not yet committed
- Test: `tests/contracts/test_search_to_subject_resolution_flow_contract.py`

- [ ] **Step 1: Inspect repo state**

Run: `git status --short`
Expected: only the intended spec, test, plan, and bead metadata changes remain, plus the known unrelated untracked baseline files.

- [ ] **Step 2: Close the bead**

Run: `bd close stock-agent-h3e.1.3.2 --reason "Completed"`
Expected: bead marked `closed`

- [ ] **Step 3: Sync bead metadata**

Run: `bd sync`
Expected: `.beads/issues.jsonl` updated for the closed bead state

- [ ] **Step 4: Re-run the search-to-subject contract test after bead sync**

Run: `python3 -m unittest tests.contracts.test_search_to_subject_resolution_flow_contract -v`
Expected: `OK`

- [ ] **Step 5: Commit bead metadata if needed**

```bash
git add .beads/issues.jsonl docs/superpowers/plans/2026-04-21-search-to-subject-resolution-flow.md
git commit -m "chore: sync bead status for stock-agent-h3e.1.3.2"
```

Only do this if `bd sync` changed tracked files that are not already committed.

- [ ] **Step 6: Publish the feature branch**

Run: `git push -u origin stock-agent-h3e.1.3.2`
Expected: remote branch updated successfully

- [ ] **Step 7: Fast-forward `main` and verify there**

Run: `git checkout main && git pull --rebase origin main && git merge --ff-only stock-agent-h3e.1.3.2 && python3 -m unittest tests.contracts.test_search_to_subject_resolution_flow_contract -v`
Expected: fast-forward merge succeeds and the search-to-subject contract test reports `OK`

- [ ] **Step 8: Push `main` and verify final status**

Run: `git push origin main && git status`
Expected: `main` is up to date with `origin/main`, with only the known unrelated untracked baseline files remaining

- [ ] **Step 9: Delete the local feature branch**

Run: `git branch -d stock-agent-h3e.1.3.2`
Expected: local feature branch deleted after the fast-forward merge
