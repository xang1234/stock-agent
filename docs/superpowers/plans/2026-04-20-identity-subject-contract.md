# Identity And Research Subject Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the finance identity contract explicit across the normative spec, OpenAPI schema, and SQL schema notes so downstream work keys issuer, instrument, listing, and `SubjectRef` consistently.

**Architecture:** Treat this bead as a contract-pack update, not application logic. Add a small file-based contract test that asserts the required identity language exists, watch it fail first, then patch the three normative files so the test and acceptance criteria line up.

**Tech Stack:** Markdown spec, OpenAPI YAML, PostgreSQL schema SQL, Python 3 `unittest`

---

## File Structure

- Modify: `spec/finance_research_spec.md`
  Responsibility: normative contract language for identity layers, `SubjectRef` selection rules, and downstream service consumers.
- Modify: `spec/finance_research_openapi.yaml`
  Responsibility: schema descriptions for `SubjectKind`, `SubjectRef`, and `ResolvedSubject`.
- Modify: `spec/finance_research_db_schema.sql`
  Responsibility: schema notes explaining issuer vs instrument vs listing and the rule that ticker is not canonical identity.
- Create: `tests/contracts/test_identity_subject_contract.py`
  Responsibility: file-level contract checks that enforce the required wording anchors across the normative files.

### Task 1: Add failing contract checks

**Files:**
- Create: `tests/contracts/test_identity_subject_contract.py`
- Test: `tests/contracts/test_identity_subject_contract.py`

- [ ] **Step 1: Write the failing test**

```python
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"
OPENAPI_PATH = ROOT / "spec" / "finance_research_openapi.yaml"
SQL_PATH = ROOT / "spec" / "finance_research_db_schema.sql"


class IdentitySubjectContractTest(unittest.TestCase):
    def test_spec_declares_canonical_identity_rules(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 4.1.1 Canonical identity rules", spec_text)
        self.assertIn("ticker is a listing attribute and lookup handle, not canonical identity", spec_text)
        self.assertIn("### 6.1.1 Downstream consumer rules", spec_text)
        self.assertIn("Chat and Analyze persist subject context as SubjectRef[]", spec_text)

    def test_openapi_describes_subject_ref_identity_boundary(self) -> None:
        openapi_text = OPENAPI_PATH.read_text()
        self.assertIn("Ticker is a listing locator, not canonical identity.", openapi_text)
        self.assertIn("kind determines whether the id points to an issuer, instrument, listing", openapi_text)

    def test_sql_notes_preserve_ticker_boundary(self) -> None:
        sql_text = SQL_PATH.read_text()
        self.assertIn("ticker is a listing locator, not canonical identity", sql_text)
        self.assertIn("issuer = reporting entity; instrument = tradable security definition; listing = venue-specific symbol", sql_text)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.contracts.test_identity_subject_contract -v`
Expected: `FAIL` because the new canonical identity headings and wording do not exist yet.

- [ ] **Step 3: Commit**

```bash
git add tests/contracts/test_identity_subject_contract.py
git commit -m "test: add identity contract checks"
```

### Task 2: Patch the normative contract files

**Files:**
- Modify: `spec/finance_research_spec.md`
- Modify: `spec/finance_research_openapi.yaml`
- Modify: `spec/finance_research_db_schema.sql`
- Test: `tests/contracts/test_identity_subject_contract.py`

- [ ] **Step 1: Add the spec contract sections**

```md
### 4.1.1 Canonical identity rules

- `Issuer` is the canonical identity for the legal and reporting entity.
- `Instrument` is the canonical identity for the tradable security definition issued by an issuer.
- `Listing` is the canonical identity for an exchange-specific venue representation of an instrument.
- `ticker` is a listing attribute and lookup handle, not canonical identity.
```

- [ ] **Step 2: Add the downstream consumer matrix**

```md
### 6.1.1 Downstream consumer rules

- Resolver service resolves aliases, tickers, and external identifiers into explicit issuer, instrument, or listing candidates.
- Market data service keys quotes, bars, session state, and venue-sensitive performance on `listing`.
- Fundamentals service keys issuer profile, filing-backed statements, and fiscal normalization on `issuer`.
- Chat and Analyze persist subject context as `SubjectRef[]` even when the user entered a ticker.
- Agents and findings carry `SubjectRef[]` so monitoring survives ticker changes and cross-listings.
```

- [ ] **Step 3: Add OpenAPI schema descriptions**

```yaml
    SubjectKind:
      type: string
      description: Canonical subject discriminator. Ticker is a listing locator, not canonical identity.
```

```yaml
    SubjectRef:
      type: object
      description: kind determines whether the id points to an issuer, instrument, listing, theme, macro topic, portfolio, or screen.
```

- [ ] **Step 4: Add SQL schema notes**

```sql
-- Identity contract:
-- issuer = reporting entity; instrument = tradable security definition; listing = venue-specific symbol.
-- ticker is a listing locator, not canonical identity.
```

- [ ] **Step 5: Commit**

```bash
git add spec/finance_research_spec.md spec/finance_research_openapi.yaml spec/finance_research_db_schema.sql
git commit -m "docs: define identity subject contract"
```

### Task 3: Verify and land the bead

**Files:**
- Modify: `.beads/issues.jsonl` (via `bd close` / `bd sync`)
- Test: `tests/contracts/test_identity_subject_contract.py`

- [ ] **Step 1: Run the contract test and confirm green**

Run: `python3 -m unittest tests.contracts.test_identity_subject_contract -v`
Expected: `OK`

- [ ] **Step 2: Inspect repo state**

Run: `git status --short`
Expected: only intended spec, test, plan, and beads metadata changes remain.

- [ ] **Step 3: Close the bead**

Run: `bd close stock-agent-h3e.1.1.1 --reason "Completed"`
Expected: issue status becomes `CLOSED`.

- [ ] **Step 4: Sync and commit bead metadata**

Run: `bd sync`
Expected: beads metadata is committed without errors.

- [ ] **Step 5: Rebase and push**

Run: `git pull --rebase`
Expected: branch rebases cleanly or reports already up to date.

Run: `git push`
Expected: push succeeds.

- [ ] **Step 6: Confirm final status**

Run: `git status`
Expected: `working tree clean` and branch is up to date with `origin`.
