# Relational Schema Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the relational schema ownership and storage boundaries explicit across the narrative spec and SQL schema notes so downstream services can reason about table families without rereading the full schema pack.

**Architecture:** Treat this bead as a schema-contract update, not a schema redesign. Add a small file-based contract test that asserts the required table-family and storage-boundary language exists, watch it fail first, then patch the narrative spec and SQL notes so the schema contract is aligned across human-facing and artifact-level documentation.

**Tech Stack:** Markdown spec, PostgreSQL schema SQL, Python 3 `unittest`

---

## File Structure

- Modify: `spec/finance_research_spec.md`
  Responsibility: narrative schema-contract section grouping tables into reference and universe, evidence-plane, and app metadata families, plus storage-split and snapshot-bridge notes.
- Modify: `spec/finance_research_db_schema.sql`
  Responsibility: top-level schema notes describing table families, storage split, and the role of snapshots inside the evidence plane.
- Create: `tests/contracts/test_relational_schema_contract.py`
  Responsibility: file-level contract checks enforcing the required wording anchors across the narrative spec and SQL schema notes.

### Task 1: Add failing contract checks

**Files:**
- Create: `tests/contracts/test_relational_schema_contract.py`
- Test: `tests/contracts/test_relational_schema_contract.py`

- [ ] **Step 1: Write the failing test**

```python
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"
SQL_PATH = ROOT / "spec" / "finance_research_db_schema.sql"


class RelationalSchemaContractTest(unittest.TestCase):
    def test_spec_declares_schema_families_and_storage_split(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("## 6A. Relational schema contract", spec_text)
        self.assertIn("Reference and universe tables", spec_text)
        self.assertIn("Evidence-plane relational tables", spec_text)
        self.assertIn("App metadata and orchestration tables", spec_text)
        self.assertIn("Raw document bytes are outside the relational schema.", spec_text)
        self.assertIn("Snapshots bridge the evidence plane to user-facing artifacts.", spec_text)

    def test_sql_notes_declare_table_family_boundaries(self) -> None:
        sql_text = SQL_PATH.read_text()
        self.assertIn("Table families:", sql_text)
        self.assertIn("reference and universe tables define reusable subject context", sql_text)
        self.assertIn("evidence-plane relational tables hold provenance, facts, claims, events, and snapshots", sql_text)
        self.assertIn("app metadata and orchestration tables support user state and workflow coordination", sql_text)
        self.assertIn("raw document bytes live outside the relational schema", sql_text)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.contracts.test_relational_schema_contract -v`
Expected: `FAIL` because the new schema-contract headings and wording do not exist yet.

- [ ] **Step 3: Commit**

```bash
git add tests/contracts/test_relational_schema_contract.py
git commit -m "test: add relational schema contract checks"
```

### Task 2: Patch the schema contract files

**Files:**
- Modify: `spec/finance_research_spec.md`
- Modify: `spec/finance_research_db_schema.sql`
- Test: `tests/contracts/test_relational_schema_contract.py`

- [ ] **Step 1: Add the narrative schema contract section**

```md
## 6A. Relational schema contract

### Reference and universe tables

- `issuers`, `instruments`, `listings`, `themes`, `theme_memberships`, `portfolios`, `portfolio_holdings`, `watchlists`, and `watchlist_members` define reusable subject context.

### Evidence-plane relational tables

- `metrics`, `sources`, `documents`, `claims`, `events`, `facts`, `computations`, `snapshots`, `findings`, and related provenance tables form the relational evidence plane.

### App metadata and orchestration tables

- `users`, `chat_threads`, `chat_messages`, `analyze_templates`, `agents`, and `tool_call_logs` support user state and orchestration.

- Raw document bytes are outside the relational schema.
- Snapshots bridge the evidence plane to user-facing artifacts.
```

- [ ] **Step 2: Add the SQL family and storage notes**

```sql
-- Table families:
-- reference and universe tables define reusable subject context and membership state.
-- evidence-plane relational tables hold provenance, facts, claims, events, and snapshots.
-- app metadata and orchestration tables support user state and workflow coordination.
-- raw document bytes live outside the relational schema and are referenced by metadata.
```

- [ ] **Step 3: Commit**

```bash
git add spec/finance_research_spec.md spec/finance_research_db_schema.sql
git commit -m "docs: define relational schema contract"
```

### Task 3: Verify and land the bead

**Files:**
- Modify: `.beads/issues.jsonl` (via `bd close` / `bd sync`)
- Test: `tests/contracts/test_relational_schema_contract.py`

- [ ] **Step 1: Run the contract test and confirm green**

Run: `python3 -m unittest tests.contracts.test_relational_schema_contract -v`
Expected: `OK`

- [ ] **Step 2: Inspect repo state**

Run: `git status --short`
Expected: only intended schema-contract files, test, plan, and bead metadata changes remain.

- [ ] **Step 3: Close the bead**

Run: `bd close stock-agent-h3e.1.1.3 --reason "Completed"`
Expected: issue status becomes `CLOSED`.

- [ ] **Step 4: Sync and commit bead metadata**

Run: `bd sync`
Expected: beads metadata is exported cleanly.

- [ ] **Step 5: Rebase and push branch**

Run: `git pull --rebase origin main`
Expected: branch rebases cleanly or reports already up to date.

Run: `git push -u origin stock-agent-h3e.1.1.3`
Expected: push succeeds.

- [ ] **Step 6: Fast-forward main**

Run: `git checkout main && git pull --rebase origin main && git merge --ff-only stock-agent-h3e.1.1.3`
Expected: `main` now contains the bead commits without a merge commit.

- [ ] **Step 7: Push main and confirm final status**

Run: `git push origin main`
Expected: push succeeds.

Run: `git status`
Expected: branch is up to date with `origin/main`; any remaining untracked files are unrelated baseline artifacts already tracked by follow-up issue `stock-agent-dkz`.
