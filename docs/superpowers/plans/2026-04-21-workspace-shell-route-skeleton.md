# Workspace Shell And Route Skeleton Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the persistent workspace shell, top-level workspace map, symbol-detail route skeleton, and selective right-rail rules explicit in the narrative spec so later shell and surface work shares one stable navigation contract.

**Architecture:** Treat this bead as a narrative contract-pack update, not a router or UI implementation. Add a small file-based contract test that asserts the required shell, route-group, symbol-detail, and downstream-consumer wording exists, watch it fail first, then patch the narrative spec so the workspace-shell contract is explicit and internally consistent.

**Tech Stack:** Markdown spec, Python 3 `unittest`

---

## File Structure

- Modify: `spec/finance_research_spec.md`
  Responsibility: narrative shell and route-skeleton rules for persistent shell regions, top-level workspaces, subject-detail nesting, `Analyze` deep-link behavior, and downstream consumer notes.
- Create: `tests/contracts/test_workspace_shell_route_skeleton_contract.py`
  Responsibility: file-level contract checks enforcing the required workspace-shell, route-group, symbol-detail, and right-rail wording anchors in the narrative spec.

### Task 1: Add failing workspace-shell contract checks

**Files:**
- Create: `tests/contracts/test_workspace_shell_route_skeleton_contract.py`
- Test: `tests/contracts/test_workspace_shell_route_skeleton_contract.py`

- [ ] **Step 1: Write the failing test**

```python
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"


class WorkspaceShellRouteSkeletonContractTest(unittest.TestCase):
    def test_spec_declares_persistent_shell_and_primary_workspaces(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 3.7 Workspace shell and route skeleton", spec_text)
        self.assertIn(
            "The app uses one persistent workspace shell rather than surface-specific chrome for each page.",
            spec_text,
        )
        self.assertIn(
            "The shell owns three regions: left navigation, main workspace canvas, and a right-rail slot.",
            spec_text,
        )
        self.assertIn(
            "Left navigation holds the primary workspaces: `Home`, `Agents`, `Chat`, `Screener`, and `Analyze`.",
            spec_text,
        )
        self.assertIn(
            "Shell chrome persists while moving between those primary workspaces.",
            spec_text,
        )
        self.assertIn(
            "The right rail is a shell-owned slot rather than a surface-owned layout invention.",
            spec_text,
        )
        self.assertIn(
            "`Home`, `Agents`, `Chat`, symbol detail, and `Analyze` use the right rail by default.",
            spec_text,
        )
        self.assertIn(
            "`Screener` defaults to a denser main-canvas layout and may opt into the rail later without changing the shell contract.",
            spec_text,
        )

    def test_spec_declares_symbol_detail_routes_and_analyze_handoff(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 3.4 Symbol detail", spec_text)
        self.assertIn(
            "Symbol detail is an entered subject workspace with sections such as Overview, Financials, Earnings, Holders, and Signals. It may launch into top-level `Analyze` with carried subject context.",
            spec_text,
        )
        self.assertIn("### 3.8 Symbol-detail route skeleton", spec_text)
        self.assertIn(
            "Primary workspace route groups are `home`, `agents`, `chat`, `screener`, and `analyze`.",
            spec_text,
        )
        self.assertIn(
            "`Chat` remains thread-scoped rather than symbol-scoped because threads may span themes, multiple subjects, or imported Analyze artifacts.",
            spec_text,
        )
        self.assertIn(
            "Symbol detail is an entered route group keyed by canonical subject identity rather than a primary left-nav workspace.",
            spec_text,
        )
        self.assertIn(
            "Entering symbol detail swaps the main canvas into a subject-detail shell while preserving the surrounding shell chrome.",
            spec_text,
        )
        self.assertIn(
            "Nested routes are the durable model for subject-detail sections.",
            spec_text,
        )
        self.assertIn(
            "The initial durable subject-detail sections are `overview`, `financials`, `earnings`, `holders`, and `signals`.",
            spec_text,
        )
        self.assertIn(
            "`signals` is the extensible section for community, sentiment, news pulse, and future alt-data views.",
            spec_text,
        )
        self.assertIn(
            "Symbol detail may deep-link into top-level `Analyze` with carried `SubjectRef` context or a prefilled analyze intent.",
            spec_text,
        )

    def test_spec_declares_shell_downstream_consumers(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 3.9 Downstream consumer rules for shell and route work", spec_text)
        self.assertIn(
            "Symbol search and quote snapshot surface (`P0.4`) depends on the distinction between primary workspaces and entered symbol-detail routes.",
            spec_text,
        )
        self.assertIn(
            "Symbol overview shell (`P1.3`) depends on the subject-detail shell owning shared identity context and local section navigation.",
            spec_text,
        )
        self.assertIn(
            "Symbol detail tabs and context modules (`P1.4`) depend on durable nested-route buckets inside the subject-detail shell.",
            spec_text,
        )
        self.assertIn(
            "Thread coordinator and transport (`P2.1`) depends on `Chat` being a primary workspace inside the persistent shell.",
            spec_text,
        )
        self.assertIn(
            "Analyze workspace surfaces (`P4.4`) depends on `Analyze` being top-level while still accepting deep-linked subject context.",
            spec_text,
        )
        self.assertIn(
            "Right-rail activity (`P4.5`) depends on the shell-owned right-rail slot and selective default population.",
            spec_text,
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.contracts.test_workspace_shell_route_skeleton_contract -v`
Expected: `FAIL` because the new shell and route-skeleton headings and wording do not exist yet.

- [ ] **Step 3: Commit**

```bash
git add tests/contracts/test_workspace_shell_route_skeleton_contract.py
git commit -m "test: add workspace shell route skeleton checks"
```

### Task 2: Patch the shell and route contract in the narrative spec

**Files:**
- Modify: `spec/finance_research_spec.md`
- Test: `tests/contracts/test_workspace_shell_route_skeleton_contract.py`

- [ ] **Step 1: Replace the old symbol-detail summary**

```md
### 3.4 Symbol detail
Symbol detail is an entered subject workspace with sections such as Overview, Financials, Earnings, Holders, and Signals. It may launch into top-level `Analyze` with carried subject context.
```

- [ ] **Step 2: Add the workspace-shell and route-skeleton subsections**

```md
### 3.7 Workspace shell and route skeleton

- The app uses one persistent workspace shell rather than surface-specific chrome for each page.
- The shell owns three regions: left navigation, main workspace canvas, and a right-rail slot.
- Left navigation holds the primary workspaces: `Home`, `Agents`, `Chat`, `Screener`, and `Analyze`.
- Shell chrome persists while moving between those primary workspaces.
- `Analyze` is a top-level workspace rather than only a symbol-detail tab.
- The right rail is a shell-owned slot rather than a surface-owned layout invention.
- `Home`, `Agents`, `Chat`, symbol detail, and `Analyze` use the right rail by default.
- `Screener` defaults to a denser main-canvas layout and may opt into the rail later without changing the shell contract.

### 3.8 Symbol-detail route skeleton

- Primary workspace route groups are `home`, `agents`, `chat`, `screener`, and `analyze`.
- `Chat` remains thread-scoped rather than symbol-scoped because threads may span themes, multiple subjects, or imported Analyze artifacts.
- Symbol detail is an entered route group keyed by canonical subject identity rather than a primary left-nav workspace.
- Entering symbol detail swaps the main canvas into a subject-detail shell while preserving the surrounding shell chrome.
- The subject-detail shell owns shared subject header context and local section navigation.
- Nested routes are the durable model for subject-detail sections.
- The initial durable subject-detail sections are `overview`, `financials`, `earnings`, `holders`, and `signals`.
- `signals` is the extensible section for community, sentiment, news pulse, and future alt-data views.
- Symbol detail may deep-link into top-level `Analyze` with carried `SubjectRef` context or a prefilled analyze intent.

### 3.9 Downstream consumer rules for shell and route work

- Symbol search and quote snapshot surface (`P0.4`) depends on the distinction between primary workspaces and entered symbol-detail routes.
- Symbol overview shell (`P1.3`) depends on the subject-detail shell owning shared identity context and local section navigation.
- Symbol detail tabs and context modules (`P1.4`) depend on durable nested-route buckets inside the subject-detail shell.
- Thread coordinator and transport (`P2.1`) depends on `Chat` being a primary workspace inside the persistent shell.
- Analyze workspace surfaces (`P4.4`) depends on `Analyze` being top-level while still accepting deep-linked subject context.
- Right-rail activity (`P4.5`) depends on the shell-owned right-rail slot and selective default population.
```

- [ ] **Step 3: Run the contract test and confirm green**

Run: `python3 -m unittest tests.contracts.test_workspace_shell_route_skeleton_contract -v`
Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add spec/finance_research_spec.md
git commit -m "docs: define workspace shell route skeleton contract"
```

### Task 3: Verify and land the bead

**Files:**
- Modify: `.beads/issues.jsonl` (via `bd close` / `bd sync`)
- Test: `tests/contracts/test_workspace_shell_route_skeleton_contract.py`

- [ ] **Step 1: Inspect repo state**

Run: `git status --short`
Expected: only the intended spec, test, plan, and bead metadata changes remain, plus the known unrelated untracked baseline files.

- [ ] **Step 2: Close the bead**

Run: `bd close stock-agent-h3e.1.2.1 --reason "Completed"`
Expected: bead marked `closed`

- [ ] **Step 3: Sync bead metadata**

Run: `bd sync`
Expected: `.beads/issues.jsonl` updated for the closed bead state

- [ ] **Step 4: Re-run the contract test after bead sync**

Run: `python3 -m unittest tests.contracts.test_workspace_shell_route_skeleton_contract -v`
Expected: `OK`

- [ ] **Step 5: Commit bead metadata if needed**

```bash
git add .beads/issues.jsonl docs/superpowers/plans/2026-04-21-workspace-shell-route-skeleton.md
git commit -m "chore: sync bead status for stock-agent-h3e.1.2.1"
```

Only do this if `bd sync` changed tracked files that are not already committed.

- [ ] **Step 6: Publish the feature branch**

Run: `git push -u origin stock-agent-h3e.1.2.1`
Expected: remote branch updated successfully

- [ ] **Step 7: Fast-forward `main` and verify there**

Run: `git checkout main && git pull --rebase origin main && git merge --ff-only stock-agent-h3e.1.2.1 && python3 -m unittest tests.contracts.test_workspace_shell_route_skeleton_contract -v`
Expected: fast-forward merge succeeds and the contract test reports `OK`

- [ ] **Step 8: Push `main` and verify final status**

Run: `git push origin main && git status`
Expected: `main` is up to date with `origin/main`, with only the known unrelated untracked baseline files remaining

- [ ] **Step 9: Delete the local feature branch**

Run: `git branch -d stock-agent-h3e.1.2.1`
Expected: local feature branch deleted after the fast-forward merge
