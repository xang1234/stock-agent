# Snapshot Semantics Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the sealed-snapshot, in-snapshot-transform, and refresh-boundary rules explicit in the narrative spec so verifier, shared-artifact, and renderer work depend on one stable contract.

**Architecture:** Treat this bead as a narrative contract-pack update, not a runtime or schema redesign. Add a small file-based contract test that asserts the required snapshot-manifest, transform, and refresh wording exists, watch it fail first, then patch the snapshot-semantics section of the spec so the product-logic boundary is explicit for downstream consumers.

**Tech Stack:** Markdown spec, Python 3 `unittest`

---

## File Structure

- Modify: `spec/finance_research_spec.md`
  Responsibility: narrative snapshot-manifest rules, in-snapshot transform limits, refresh triggers, and downstream consumer notes.
- Create: `tests/contracts/test_snapshot_semantics_contract.py`
  Responsibility: file-level contract checks enforcing the required snapshot, transform, and refresh wording anchors in the narrative spec.

### Task 1: Add failing snapshot contract checks

**Files:**
- Create: `tests/contracts/test_snapshot_semantics_contract.py`
- Test: `tests/contracts/test_snapshot_semantics_contract.py`

- [ ] **Step 1: Write the failing test**

```python
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"


class SnapshotSemanticsContractTest(unittest.TestCase):
    def test_spec_declares_sealed_snapshot_manifest(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("## 10. Snapshot semantics", spec_text)
        self.assertIn("### 10.1 Sealed snapshot manifest", spec_text)
        self.assertIn(
            "A sealed snapshot pins the subject set, `as_of`, basis, normalization, coverage window, source set, bound fact / claim / event refs, and exact `allowed_transforms`.",
            spec_text,
        )
        self.assertIn(
            "`allowed_transforms` is explicit manifest state, not a UI guess derived from block kind alone.",
            spec_text,
        )
        self.assertIn(
            "Persisted chat and analyze artifacts must continue to point at that sealed snapshot rather than reconstructing support opportunistically later.",
            spec_text,
        )

    def test_spec_declares_in_snapshot_transform_rules(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 10.2 In-snapshot transforms", spec_text)
        self.assertIn(
            "A transform is legal inside a sealed snapshot only when it preserves the subject set and does not require fresher evidence than `as_of`.",
            spec_text,
        )
        self.assertIn(
            "In-snapshot transforms may change presentation or range only when the required rows or series are already inside the sealed data boundary.",
            spec_text,
        )
        self.assertIn(
            "Changing `YTD` to `1Y` on a performance chart is allowed only if the requested range end is less than or equal to `as_of`.",
            spec_text,
        )
        self.assertIn(
            "The manifest, not the client, determines whether a transform is allowed.",
            spec_text,
        )

    def test_spec_declares_refresh_boundary_and_consumers(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 10.3 Refresh and new-run boundary", spec_text)
        self.assertIn(
            "Any request that changes subject membership, peer set, basis, normalization, or freshness crosses the snapshot boundary.",
            spec_text,
        )
        self.assertIn(
            "Requests for fresher data, different peers, different basis, or different normalization require refresh or a new run.",
            spec_text,
        )
        self.assertIn(
            "Crossing the snapshot boundary must be explicit rather than a silent mutation of a sealed answer.",
            spec_text,
        )
        self.assertIn("### 10.4 Downstream consumer rules for snapshot semantics", spec_text)
        self.assertIn(
            "Block registry versioning and validation (`P2.3`) depends on snapshot rules being stable enough to know which interactions are legal within existing block bindings and which require a new backend result.",
            spec_text,
        )
        self.assertIn(
            "Snapshot assembler and verifier (`P2.4`) depends on the sealed manifest contents, sealing order, and refresh boundary to prove that rendered blocks still correspond to the same evidence-backed snapshot.",
            spec_text,
        )
        self.assertIn(
            "Shared artifact flow (`P4.3`) depends on sealed snapshots remaining reusable product artifacts.",
            spec_text,
        )
        self.assertIn(
            "Frontend renderer (`PX.3`) depends on presentation-only interactions staying local only when they remain inside the sealed snapshot contract.",
            spec_text,
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.contracts.test_snapshot_semantics_contract -v`
Expected: `FAIL` because the new snapshot subsection headings and explicit manifest or refresh wording do not exist yet.

- [ ] **Step 3: Commit**

```bash
git add tests/contracts/test_snapshot_semantics_contract.py
git commit -m "test: add snapshot semantics contract checks"
```

### Task 2: Patch the snapshot-semantics contract in the narrative spec

**Files:**
- Modify: `spec/finance_research_spec.md`
- Test: `tests/contracts/test_snapshot_semantics_contract.py`

- [ ] **Step 1: Expand the snapshot semantics section**

```md
## 10. Snapshot semantics

### 10.1 Sealed snapshot manifest

- A sealed snapshot pins the subject set, `as_of`, basis, normalization, coverage window, source set, bound fact / claim / event refs, and exact `allowed_transforms`.
- `allowed_transforms` is explicit manifest state, not a UI guess derived from block kind alone.
- Persisted chat and analyze artifacts must continue to point at that sealed snapshot rather than reconstructing support opportunistically later.

### 10.2 In-snapshot transforms

- A transform is legal inside a sealed snapshot only when it preserves the subject set and does not require fresher evidence than `as_of`.
- In-snapshot transforms may change presentation or range only when the required rows or series are already inside the sealed data boundary.
- Changing `YTD` to `1Y` on a performance chart is allowed only if the requested range end is less than or equal to `as_of`.
- The manifest, not the client, determines whether a transform is allowed.

### 10.3 Refresh and new-run boundary

- Any request that changes subject membership, peer set, basis, normalization, or freshness crosses the snapshot boundary.
- Requests for fresher data, different peers, different basis, or different normalization require refresh or a new run.
- Crossing the snapshot boundary must be explicit rather than a silent mutation of a sealed answer.

### 10.4 Downstream consumer rules for snapshot semantics

- Block registry versioning and validation (`P2.3`) depends on snapshot rules being stable enough to know which interactions are legal within existing block bindings and which require a new backend result.
- Snapshot assembler and verifier (`P2.4`) depends on the sealed manifest contents, sealing order, and refresh boundary to prove that rendered blocks still correspond to the same evidence-backed snapshot.
- Shared artifact flow (`P4.3`) depends on sealed snapshots remaining reusable product artifacts.
- Frontend renderer (`PX.3`) depends on presentation-only interactions staying local only when they remain inside the sealed snapshot contract.
```

- [ ] **Step 2: Keep the workflow section aligned with the contract**

```md
### 11.1 Chat turn
1. Resolve subjects and period
2. Select bundle
3. Run analyst tool loop
4. Stage snapshot manifest
5. Verify bindings and disclosures
6. Seal snapshot
7. Stream `Block[]`
8. Persist message, snapshot, citations, and summary

### 11.2 Analyze template run
1. Load template
2. Resolve source categories into tool bundle and policy
3. Add primary subject plus template-added subjects
4. Run analyst
5. Seal snapshot
6. Persist analysis artifact
7. Optionally add artifact to chat thread
```

Apply this step as an alignment check: keep these workflow steps intact or only make minimal wording adjustments if the new snapshot contract would otherwise contradict them.

- [ ] **Step 3: Run the contract test and confirm green**

Run: `python3 -m unittest tests.contracts.test_snapshot_semantics_contract -v`
Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add spec/finance_research_spec.md
git commit -m "docs: define snapshot semantics contract"
```

### Task 3: Verify and land the bead

**Files:**
- Modify: `.beads/issues.jsonl` (via `bd close` / `bd sync`)
- Test: `tests/contracts/test_snapshot_semantics_contract.py`

- [ ] **Step 1: Inspect repo state**

Run: `git status --short`
Expected: only the intended spec, test, plan, and bead metadata changes remain, plus the known unrelated untracked baseline files.

- [ ] **Step 2: Close the bead**

Run: `bd close stock-agent-h3e.1.1.7 --reason "Completed"`
Expected: bead marked `closed`

- [ ] **Step 3: Sync bead metadata**

Run: `bd sync`
Expected: `.beads/issues.jsonl` updated for the closed bead state

- [ ] **Step 4: Re-run the contract test after bead sync**

Run: `python3 -m unittest tests.contracts.test_snapshot_semantics_contract -v`
Expected: `OK`

- [ ] **Step 5: Commit bead metadata if needed**

```bash
git add .beads/issues.jsonl docs/superpowers/plans/2026-04-21-snapshot-semantics-contract.md
git commit -m "chore: sync bead status for stock-agent-h3e.1.1.7"
```

Only do this if `bd sync` changed tracked files that are not already committed.

- [ ] **Step 6: Push the feature branch**

Run: `git pull --rebase origin stock-agent-h3e.1.1.7 && git push origin stock-agent-h3e.1.1.7`
Expected: remote branch updated successfully

- [ ] **Step 7: Fast-forward `main` and verify there**

Run: `git checkout main && git pull --rebase origin main && git merge --ff-only stock-agent-h3e.1.1.7 && python3 -m unittest tests.contracts.test_snapshot_semantics_contract -v`
Expected: fast-forward merge succeeds and the contract test reports `OK`

- [ ] **Step 8: Push `main` and verify final status**

Run: `git push origin main && git status`
Expected: `main` is up to date with `origin/main`, with only the known unrelated untracked baseline files remaining

- [ ] **Step 9: Delete the local feature branch**

Run: `git branch -d stock-agent-h3e.1.1.7`
Expected: local feature branch deleted after the fast-forward merge
