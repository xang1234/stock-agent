# HTTP API Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the HTTP API ownership, consumer boundaries, and client/BFF rules explicit across the narrative spec and OpenAPI artifact so frontend work stays behind `/v1/*` backend contracts.

**Architecture:** Treat this bead as an API-contract update, not an API redesign. Add a small file-based contract test that asserts the required endpoint-group and client-boundary language exists, watch it fail first, then patch the narrative spec and OpenAPI descriptions so the BFF contract is consistent across both artifacts.

**Tech Stack:** Markdown spec, OpenAPI YAML, Python 3 `unittest`

---

## File Structure

- Modify: `spec/finance_research_spec.md`
  Responsibility: narrative API-contract section describing endpoint-group ownership, primary consumers, and the rule that the client only talks to `/v1/*`.
- Modify: `spec/finance_research_openapi.yaml`
  Responsibility: top-level and endpoint descriptions clarifying that the API is the client-facing BFF surface and that chat streaming and snapshot transforms are backend-mediated.
- Create: `tests/contracts/test_http_api_contract.py`
  Responsibility: file-level contract checks enforcing the required wording anchors across the narrative spec and OpenAPI artifact.

### Task 1: Add failing contract checks

**Files:**
- Create: `tests/contracts/test_http_api_contract.py`
- Test: `tests/contracts/test_http_api_contract.py`

- [ ] **Step 1: Write the failing test**

```python
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"
OPENAPI_PATH = ROOT / "spec" / "finance_research_openapi.yaml"


class HttpApiContractTest(unittest.TestCase):
    def test_spec_declares_api_ownership_and_client_boundary(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 7.1 HTTP API ownership and consumer rules", spec_text)
        self.assertIn("The frontend only talks to `/v1/*` backend contracts.", spec_text)
        self.assertIn("The frontend does not call third-party providers directly.", spec_text)
        self.assertIn("`Chat` plus `Snapshots` define the run, stream, and render boundary.", spec_text)

    def test_openapi_describes_bff_surface_and_backend_mediation(self) -> None:
        openapi_text = OPENAPI_PATH.read_text()
        self.assertIn("The /v1 API is the client-facing backend-for-frontend surface.", openapi_text)
        self.assertIn("Clients must not call third-party providers directly.", openapi_text)
        self.assertIn("SSE chat streaming is a backend-mediated run transport.", openapi_text)
        self.assertIn("Snapshot transforms are backend-mediated interactions over sealed snapshots.", openapi_text)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.contracts.test_http_api_contract -v`
Expected: `FAIL` because the new HTTP API ownership and BFF wording do not exist yet.

- [ ] **Step 3: Commit**

```bash
git add tests/contracts/test_http_api_contract.py
git commit -m "test: add HTTP API contract checks"
```

### Task 2: Patch the API contract files

**Files:**
- Modify: `spec/finance_research_spec.md`
- Modify: `spec/finance_research_openapi.yaml`
- Test: `tests/contracts/test_http_api_contract.py`

- [ ] **Step 1: Add the narrative API-contract subsection**

```md
### 7.1 HTTP API ownership and consumer rules

- `Subjects`, `Market`, `Fundamentals`, `Evidence`, `Snapshots`, `Chat`, `Analyze`, `Agents`, `Home`, `Watchlists`, and `Screener` are the stable endpoint groups exposed to clients.
- The frontend only talks to `/v1/*` backend contracts.
- The frontend does not call third-party providers directly.
- `Chat` plus `Snapshots` define the run, stream, and render boundary.
```

- [ ] **Step 2: Add OpenAPI BFF and transport descriptions**

```yaml
info:
  description: The /v1 API is the client-facing backend-for-frontend surface.
```

```yaml
  /v1/chat/threads/{threadId}/stream:
    get:
      description: SSE chat streaming is a backend-mediated run transport.
```

```yaml
  /v1/snapshots/{snapshotId}/transform:
    post:
      description: Snapshot transforms are backend-mediated interactions over sealed snapshots.
```

```yaml
paths:
  # contract rule: Clients must not call third-party providers directly.
```

- [ ] **Step 3: Commit**

```bash
git add spec/finance_research_spec.md spec/finance_research_openapi.yaml
git commit -m "docs: define HTTP API contract"
```

### Task 3: Verify and land the bead

**Files:**
- Modify: `.beads/issues.jsonl` (via `bd close` / `bd sync`)
- Test: `tests/contracts/test_http_api_contract.py`

- [ ] **Step 1: Run the contract test and confirm green**

Run: `python3 -m unittest tests.contracts.test_http_api_contract -v`
Expected: `OK`

- [ ] **Step 2: Inspect repo state**

Run: `git status --short`
Expected: only intended API-contract files, test, plan, and bead metadata changes remain.

- [ ] **Step 3: Close the bead**

Run: `bd close stock-agent-h3e.1.1.4 --reason "Completed"`
Expected: issue status becomes `CLOSED`.

- [ ] **Step 4: Sync and commit bead metadata**

Run: `bd sync`
Expected: beads metadata is exported cleanly.

- [ ] **Step 5: Rebase and push branch**

Run: `git pull --rebase origin main`
Expected: branch rebases cleanly or reports already up to date.

Run: `git push -u origin stock-agent-h3e.1.1.4`
Expected: push succeeds.

- [ ] **Step 6: Fast-forward main**

Run: `git checkout main && git pull --rebase origin main && git merge --ff-only stock-agent-h3e.1.1.4`
Expected: `main` now contains the bead commits without a merge commit.

- [ ] **Step 7: Push main and confirm final status**

Run: `git push origin main`
Expected: push succeeds.

Run: `git status`
Expected: branch is up to date with `origin/main`; any remaining untracked files are unrelated baseline artifacts already tracked by follow-up issue `stock-agent-dkz`.
