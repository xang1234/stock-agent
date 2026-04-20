# Truth Evidence And Finding Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the truth, evidence, snapshot, and finding roles explicit across the normative spec, OpenAPI schema, and SQL schema notes so downstream systems preserve the “documents are evidence, not truth” contract.

**Architecture:** Treat this bead as a contract-pack update, not application logic. Add a small file-based contract test that asserts the required role and consumer language exists, watch it fail first, then patch the three normative files so the wording aligns across the human spec, machine schema, and relational notes.

**Tech Stack:** Markdown spec, OpenAPI YAML, PostgreSQL schema SQL, Python 3 `unittest`

---

## File Structure

- Modify: `spec/finance_research_spec.md`
  Responsibility: normative truth/evidence role rules plus downstream consumer rules for fundamentals, evidence extraction, Home feed, and agent findings.
- Modify: `spec/finance_research_openapi.yaml`
  Responsibility: schema descriptions for `Fact`, `Claim`, `Event`, `SnapshotManifest`, and `Finding`.
- Modify: `spec/finance_research_db_schema.sql`
  Responsibility: schema notes clarifying provenance, supersession, verification status, and snapshot-backed finding semantics.
- Create: `tests/contracts/test_truth_evidence_finding_contract.py`
  Responsibility: file-level contract checks that enforce the required wording anchors across the normative files.

### Task 1: Add failing contract checks

**Files:**
- Create: `tests/contracts/test_truth_evidence_finding_contract.py`
- Test: `tests/contracts/test_truth_evidence_finding_contract.py`

- [ ] **Step 1: Write the failing test**

```python
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"
OPENAPI_PATH = ROOT / "spec" / "finance_research_openapi.yaml"
SQL_PATH = ROOT / "spec" / "finance_research_db_schema.sql"


class TruthEvidenceFindingContractTest(unittest.TestCase):
    def test_spec_declares_truth_evidence_role_rules(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 4.3.1 Truth and evidence role rules", spec_text)
        self.assertIn("Documents are evidence, not truth.", spec_text)
        self.assertIn("### 6.4.1 Downstream consumer rules for truth and evidence objects", spec_text)
        self.assertIn("Home feed consumes Finding, SnapshotManifest, and ClaimCluster", spec_text)

    def test_openapi_describes_truth_and_finding_roles(self) -> None:
        openapi_text = OPENAPI_PATH.read_text()
        self.assertIn("Facts are the unit of truth for displayed values.", openapi_text)
        self.assertIn("Claims are extracted assertions from evidence, not canonical truth.", openapi_text)
        self.assertIn("Findings are snapshotted product artifacts built from evidence graph objects.", openapi_text)

    def test_sql_notes_preserve_provenance_and_snapshot_rules(self) -> None:
        sql_text = SQL_PATH.read_text()
        self.assertIn("facts are immutable except through supersession or invalidation", sql_text)
        self.assertIn("claims remain evidence-layer assertions rather than canonical truth", sql_text)
        self.assertIn("findings must point at a sealed snapshot and remain user-facing artifacts", sql_text)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.contracts.test_truth_evidence_finding_contract -v`
Expected: `FAIL` because the new truth/evidence headings and wording do not exist yet.

- [ ] **Step 3: Commit**

```bash
git add tests/contracts/test_truth_evidence_finding_contract.py
git commit -m "test: add truth evidence contract checks"
```

### Task 2: Patch the normative contract files

**Files:**
- Modify: `spec/finance_research_spec.md`
- Modify: `spec/finance_research_openapi.yaml`
- Modify: `spec/finance_research_db_schema.sql`
- Test: `tests/contracts/test_truth_evidence_finding_contract.py`

- [ ] **Step 1: Add the spec role rules**

```md
### 4.3.1 Truth and evidence role rules

- `Metric` is a definition object, not an observed value.
- `Fact` is the unit of truth for displayed values and must carry provenance, verification status, and supersession state.
- `Claim` is an extracted assertion from evidence and is not canonical truth.
- `Event` is the unit of state change assembled from claims and sources.
- `Finding` is a user-facing product artifact built from a sealed snapshot over the evidence graph.
- Documents are evidence, not truth.
```

- [ ] **Step 2: Add the downstream consumer rules**

```md
### 6.4.1 Downstream consumer rules for truth and evidence objects

- Fundamentals consumes `Metric`, `Fact`, and `Computation` as the canonical value layer.
- Evidence extraction owns `Source`, `Document`, `Mention`, `Claim`, `ClaimArgument`, `ClaimEvidence`, `ClaimCluster`, `Event`, and `EntityImpact`.
- Home feed consumes `Finding`, `SnapshotManifest`, and `ClaimCluster` as the deduped product artifact layer.
- Agent workflows consume `SnapshotManifest`, `Finding`, `RunActivity`, `ClaimCluster`, and `EntityImpact`.
- Reader and extraction flows may ingest raw documents; analyst and user-facing flows must operate on structured objects instead of raw untrusted text.
```

- [ ] **Step 3: Add OpenAPI schema descriptions**

```yaml
    Fact:
      type: object
      description: Facts are the unit of truth for displayed values.
```

```yaml
    Claim:
      type: object
      description: Claims are extracted assertions from evidence, not canonical truth.
```

```yaml
    Finding:
      type: object
      description: Findings are snapshotted product artifacts built from evidence graph objects.
```

- [ ] **Step 4: Add SQL schema notes**

```sql
-- Truth and evidence contract:
-- facts are immutable except through supersession or invalidation.
-- claims remain evidence-layer assertions rather than canonical truth.
-- findings must point at a sealed snapshot and remain user-facing artifacts.
```

- [ ] **Step 5: Commit**

```bash
git add spec/finance_research_spec.md spec/finance_research_openapi.yaml spec/finance_research_db_schema.sql
git commit -m "docs: define truth evidence finding contract"
```

### Task 3: Verify and land the bead

**Files:**
- Modify: `.beads/issues.jsonl` (via `bd close` / `bd sync`)
- Test: `tests/contracts/test_truth_evidence_finding_contract.py`

- [ ] **Step 1: Run the contract test and confirm green**

Run: `python3 -m unittest tests.contracts.test_truth_evidence_finding_contract -v`
Expected: `OK`

- [ ] **Step 2: Inspect repo state**

Run: `git status --short`
Expected: only intended spec, test, plan, and beads metadata changes remain.

- [ ] **Step 3: Close the bead**

Run: `bd close stock-agent-h3e.1.1.2 --reason "Completed"`
Expected: issue status becomes `CLOSED`.

- [ ] **Step 4: Sync and commit bead metadata**

Run: `bd sync`
Expected: beads metadata is exported cleanly.

- [ ] **Step 5: Rebase and push**

Run: `git pull --rebase origin main`
Expected: branch rebases cleanly or reports already up to date.

Run: `git push origin stock-agent-h3e.1.1.2`
Expected: push succeeds.

- [ ] **Step 6: Merge or fast-forward to main**

Run: `git checkout main && git pull --rebase origin main && git merge --ff-only stock-agent-h3e.1.1.2`
Expected: `main` now contains the bead commits without a merge commit.

- [ ] **Step 7: Push main and confirm final status**

Run: `git push origin main`
Expected: push succeeds.

Run: `git status`
Expected: branch is up to date with `origin/main`; any remaining untracked files are unrelated baseline artifacts already tracked by follow-up issue `stock-agent-dkz`.
