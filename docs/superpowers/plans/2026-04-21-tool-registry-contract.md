# Tool Registry And Bundle Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the tool-registry, bundle-selection, reader-versus-analyst, and side-effect boundaries explicit across the narrative spec and registry artifact so downstream routing, extraction, automation, and orchestration work rely on one stable contract.

**Architecture:** Treat this bead as a contract-pack update, not a runtime redesign. Add a small file-based contract test that asserts the required tool-registry wording and structural metadata exist, watch it fail first, then patch the narrative spec and the normative registry artifact so the bundle and policy contract is aligned across human-facing and machine-readable files.

**Tech Stack:** Markdown spec, JSON registry artifact, Python 3 `unittest`

---

## File Structure

- Modify: `spec/finance_research_spec.md`
  Responsibility: narrative tool-registry rules for bundle groups, reader versus analyst boundaries, key tool families, side-effect categories, and downstream consumers.
- Modify: `spec/finance_research_tool_registry.json`
  Responsibility: normative registry descriptions and design rules for bundle selection, tool-versus-response-artifact separation, reader-only raw-text access, and write-intent policy boundaries.
- Create: `tests/contracts/test_tool_registry_contract.py`
  Responsibility: file-level contract checks enforcing the required wording anchors and structural metadata across the narrative spec and the registry artifact.

### Task 1: Add failing contract checks

**Files:**
- Create: `tests/contracts/test_tool_registry_contract.py`
- Test: `tests/contracts/test_tool_registry_contract.py`

- [ ] **Step 1: Write the failing test**

```python
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"
REGISTRY_PATH = ROOT / "spec" / "finance_research_tool_registry.json"


class ToolRegistryContractTest(unittest.TestCase):
    def test_spec_declares_bundle_audience_and_side_effect_rules(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 9.1 Tool registry and bundle rules", spec_text)
        self.assertIn(
            "`spec/finance_research_tool_registry.json` is the normative artifact for bundle membership, tool audience, approval sensitivity, and JSON-schema-constrained inputs and outputs.",
            spec_text,
        )
        self.assertIn(
            "Tools are backend data and action surfaces; `Block[]` remains the response artifact contract.",
            spec_text,
        )
        self.assertIn(
            "`reader` tools are the only tools allowed to access raw untrusted text or raw documents.",
            spec_text,
        )
        self.assertIn(
            "Raw text must not leak into analyst-facing tools.",
            spec_text,
        )
        self.assertIn(
            "Approval-sensitive tools today are `create_alert` and `create_agent`.",
            spec_text,
        )
        self.assertIn("### 9.2 Downstream consumer rules for tool runtime", spec_text)
        self.assertIn(
            "Pre-resolve routing and budget policy (`P2.2`) depends on deterministic bundle selection, audience separation, and registry metadata before the analyst loop starts.",
            spec_text,
        )
        self.assertIn(
            "Document ingestion and extraction (`P3.2`) depends on raw document search, fetch, and extraction tools belonging to the `reader` audience.",
            spec_text,
        )
        self.assertIn(
            "Alerting and automation (`P5.1`) depends on side-effect categories and approval sensitivity so create and update flows do not execute directly from model output.",
            spec_text,
        )
        self.assertIn(
            "Tool runtime and orchestration (`PX.2`) depends on bundle membership, audience, `read_only`, `approval_required`, `cost_class`, and `freshness_expectation`.",
            spec_text,
        )

    def test_registry_declares_bundle_groups_and_design_rules(self) -> None:
        registry = json.loads(REGISTRY_PATH.read_text())

        self.assertEqual(
            registry["description"],
            "Normative tool registry for reader and analyst bundles. Tools are backend data and action surfaces; Block[] is the separate response artifact contract.",
        )
        self.assertIn(
            "System selects tool bundle; model selects tools within the bundle.",
            registry["design_rules"],
        )
        self.assertIn(
            "Reader-only tools may access raw untrusted content; analyst-facing tools may not.",
            registry["design_rules"],
        )
        self.assertIn(
            "Non-read-only tools remain write-intent policy boundaries even when approval_required is false.",
            registry["design_rules"],
        )
        self.assertEqual(
            [bundle["bundle_id"] for bundle in registry["bundles"]],
            [
                "quote_lookup",
                "single_subject_analysis",
                "peer_comparison",
                "theme_research",
                "segment_deep_dive",
                "document_research",
                "filing_research",
                "screener",
                "agent_management",
                "alert_management",
                "analyze_template_run",
            ],
        )

    def test_registry_preserves_reader_boundary_and_write_intent_categories(self) -> None:
        registry = json.loads(REGISTRY_PATH.read_text())
        tools = {tool["name"]: tool for tool in registry["tools"]}

        reader_tools = {
            name for name, tool in tools.items() if tool["audience"] == "reader"
        }
        self.assertEqual(
            reader_tools,
            {
                "search_raw_documents",
                "fetch_raw_document",
                "extract_mentions",
                "extract_claims",
                "extract_candidate_facts",
                "extract_events",
                "classify_sentiment",
            },
        )
        for tool_name in reader_tools:
            self.assertTrue(tools[tool_name]["read_only"], msg=tool_name)

        self.assertEqual(
            tools["search_raw_documents"]["description"],
            "Reader-only raw document search surface for untrusted text retrieval before extraction.",
        )
        self.assertEqual(
            tools["fetch_raw_document"]["description"],
            "Reader-only raw document fetch surface for parsing or extraction.",
        )

        self.assertEqual(
            {name for name, tool in tools.items() if tool["approval_required"]},
            {"create_alert", "create_agent"},
        )
        self.assertEqual(
            {name for name, tool in tools.items() if not tool["read_only"]},
            {"create_alert", "add_to_watchlist", "create_agent"},
        )
        self.assertEqual(
            tools["create_alert"]["description"],
            "Approval-sensitive write-intent tool that returns a pending action until orchestration or the user confirms it.",
        )
        self.assertEqual(
            tools["add_to_watchlist"]["description"],
            "Write-intent tool that may be auto-approved by policy but remains a policy boundary.",
        )
        self.assertEqual(
            tools["create_agent"]["description"],
            "Approval-sensitive write-intent tool that returns a pending action until explicit approval.",
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.contracts.test_tool_registry_contract -v`
Expected: `FAIL` because the new tool-registry headings, top-level registry description, and updated tool descriptions do not exist yet.

- [ ] **Step 3: Commit**

```bash
git add tests/contracts/test_tool_registry_contract.py
git commit -m "test: add tool registry contract checks"
```

### Task 2: Patch the tool-registry contract files

**Files:**
- Modify: `spec/finance_research_spec.md`
- Modify: `spec/finance_research_tool_registry.json`
- Test: `tests/contracts/test_tool_registry_contract.py`

- [ ] **Step 1: Expand the narrative tool-registry section**

```md
### 9.1 Tool registry and bundle rules

- `spec/finance_research_tool_registry.json` is the normative artifact for bundle membership, tool audience, approval sensitivity, and JSON-schema-constrained inputs and outputs.
- Tools are backend data and action surfaces; `Block[]` remains the response artifact contract.
- The system chooses the bundle; the model chooses tools within the bundle.
- Bundle groups: `quote_lookup`, `single_subject_analysis`, `peer_comparison`, `theme_research`, `segment_deep_dive`, `document_research`, `filing_research`, `screener`, `agent_management`, `alert_management`, and `analyze_template_run`.
- `reader` tools are the only tools allowed to access raw untrusted text or raw documents.
- `analyst` tools operate only on structured outputs, canonical subject and period resolution, evidence bundles, facts, claims, events, and approval-mediated write intents.
- Raw text must not leak into analyst-facing tools.
- Approval-sensitive tools today are `create_alert` and `create_agent`.
- `add_to_watchlist` is a non-read-only write-intent tool even though it is not currently approval-required.

### 9.2 Downstream consumer rules for tool runtime

- Pre-resolve routing and budget policy (`P2.2`) depends on deterministic bundle selection, audience separation, and registry metadata before the analyst loop starts.
- Document ingestion and extraction (`P3.2`) depends on raw document search, fetch, and extraction tools belonging to the `reader` audience.
- Alerting and automation (`P5.1`) depends on side-effect categories and approval sensitivity so create and update flows do not execute directly from model output.
- Tool runtime and orchestration (`PX.2`) depends on bundle membership, audience, `read_only`, `approval_required`, `cost_class`, and `freshness_expectation`.
```

- [ ] **Step 2: Add the registry contract descriptions**

```json
{
  "version": "1.0.0",
  "description": "Normative tool registry for reader and analyst bundles. Tools are backend data and action surfaces; Block[] is the separate response artifact contract.",
  "design_rules": [
    "System selects tool bundle; model selects tools within the bundle.",
    "Reader-only tools may access raw untrusted content; analyst-facing tools may not.",
    "Tool inputs and outputs must validate against JSON Schema.",
    "All outputs must be traceable to source refs or deterministic computations.",
    "Side-effecting tools return pending actions unless policy explicitly auto-approves them.",
    "Non-read-only tools remain write-intent policy boundaries even when approval_required is false."
  ]
}
```

```json
{
  "name": "search_raw_documents",
  "description": "Reader-only raw document search surface for untrusted text retrieval before extraction."
}
```

```json
{
  "name": "fetch_raw_document",
  "description": "Reader-only raw document fetch surface for parsing or extraction."
}
```

```json
{
  "name": "create_alert",
  "description": "Approval-sensitive write-intent tool that returns a pending action until orchestration or the user confirms it."
}
```

```json
{
  "name": "add_to_watchlist",
  "description": "Write-intent tool that may be auto-approved by policy but remains a policy boundary."
}
```

```json
{
  "name": "create_agent",
  "description": "Approval-sensitive write-intent tool that returns a pending action until explicit approval."
}
```

- [ ] **Step 3: Run the contract test and confirm green**

Run: `python3 -m unittest tests.contracts.test_tool_registry_contract -v`
Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add spec/finance_research_spec.md spec/finance_research_tool_registry.json
git commit -m "docs: define tool registry contract"
```

### Task 3: Verify and land the bead

**Files:**
- Modify: `.beads/issues.jsonl` (via `bd close` / `bd sync`)
- Test: `tests/contracts/test_tool_registry_contract.py`

- [ ] **Step 1: Inspect repo state**

Run: `git status --short`
Expected: only intended spec, registry, test, plan, and bead metadata changes remain; `spec/finance_research_tool_registry.json` is now an intentional tracked file for this bead.

- [ ] **Step 2: Close the bead**

Run: `bd close stock-agent-h3e.1.1.6 --reason "Completed"`
Expected: issue status becomes `CLOSED`.

- [ ] **Step 3: Sync and commit bead metadata**

Run: `bd sync`
Expected: beads metadata is exported cleanly.

- [ ] **Step 4: Rebase and push branch**

Run: `git pull --rebase origin main`
Expected: branch rebases cleanly or reports already up to date.

Run: `git push -u origin stock-agent-h3e.1.1.6`
Expected: push succeeds.

- [ ] **Step 5: Fast-forward main**

Run: `git checkout main && git pull --rebase origin main && git merge --ff-only stock-agent-h3e.1.1.6`
Expected: `main` now contains the bead commits without a merge commit.

- [ ] **Step 6: Push main and confirm final status**

Run: `git push origin main`
Expected: push succeeds.

Run: `git status`
Expected: branch is up to date with `origin/main`; any remaining untracked files are unrelated baseline artifacts outside this bead.
