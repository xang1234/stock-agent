# Block Schema Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the block schema/render/provenance boundary explicit across the narrative spec and JSON schema artifact so downstream services depend on the same typed `Block[]` contract instead of markdown-like output.

**Architecture:** Treat this bead as a contract-pack update, not a block-system redesign. Add a small file-based contract test that asserts the required block-family, `data_ref`, disclosure, and consumer wording exists, watch it fail first, then patch the narrative spec and the normative block schema artifact so the contract is aligned across human-facing and machine-readable files.

**Tech Stack:** Markdown spec, JSON Schema, Python 3 `unittest`

---

## File Structure

- Modify: `spec/finance_research_spec.md`
  Responsibility: narrative block-schema rules for shared `BaseBlock` bindings, block families, `data_ref` terminology, snapshot-safe interactions, and downstream consumers.
- Modify: `spec/finance_research_block_schema.json`
  Responsibility: normative schema descriptions clarifying the typed-response purpose of the artifact, the role of `BaseBlock`, and the canonical `data_ref` terminology.
- Create: `tests/contracts/test_block_schema_contract.py`
  Responsibility: file-level contract checks enforcing the required wording anchors across the narrative spec and the schema artifact.

### Task 1: Add failing contract checks

**Files:**
- Create: `tests/contracts/test_block_schema_contract.py`
- Test: `tests/contracts/test_block_schema_contract.py`

- [ ] **Step 1: Write the failing test**

```python
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"
SCHEMA_PATH = ROOT / "spec" / "finance_research_block_schema.json"


class BlockSchemaContractTest(unittest.TestCase):
    def test_spec_declares_block_bindings_and_consumers(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 8.1 Block schema contract and render rules", spec_text)
        self.assertIn(
            "Every block kind inherits the `BaseBlock` contract: `id`, `kind`, `snapshot_id`, `data_ref`, `source_refs`, and `as_of`.",
            spec_text,
        )
        self.assertIn("The canonical schema field is `data_ref`.", spec_text)
        self.assertIn(
            "Earlier analysis used `dataRef` or `queryRef`; the schema standardizes this as `data_ref`.",
            spec_text,
        )
        self.assertIn(
            "`Sources` is the required provenance surface whenever external evidence appears in the answer.",
            spec_text,
        )
        self.assertIn("### 8.2 Downstream consumer rules for block artifacts", spec_text)
        self.assertIn(
            "Thread coordinator and transport (`P2.1`) consumes `Block[]` as the streamed and persisted assistant payload.",
            spec_text,
        )
        self.assertIn(
            "Frontend renderer (`PX.3`) consumes `Block[]` via a shared `BlockRegistry` and must not treat rendering as a tool invocation.",
            spec_text,
        )

    def test_schema_describes_typed_response_boundary(self) -> None:
        schema_text = SCHEMA_PATH.read_text()
        self.assertIn(
            "Typed assistant-response schema for structured Block[] artifacts rendered by Chat, Analyze, and findings surfaces.",
            schema_text,
        )
        self.assertIn(
            "Canonical backend binding for a block. Historical dataRef/queryRef language maps to data_ref in this schema.",
            schema_text,
        )
        self.assertIn(
            "Shared render, audit, provenance, and snapshot binding fields for every block.",
            schema_text,
        )
        self.assertIn(
            "Provenance block required whenever external evidence appears in the answer.",
            schema_text,
        )
        self.assertIn(
            "Disclosure block for trust and compliance notes; orchestration may inject it.",
            schema_text,
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.contracts.test_block_schema_contract -v`
Expected: `FAIL` because the new block-schema headings and schema descriptions do not exist yet.

- [ ] **Step 3: Commit**

```bash
git add tests/contracts/test_block_schema_contract.py
git commit -m "test: add block schema contract checks"
```

### Task 2: Patch the block-schema contract files

**Files:**
- Modify: `spec/finance_research_spec.md`
- Modify: `spec/finance_research_block_schema.json`
- Test: `tests/contracts/test_block_schema_contract.py`

- [ ] **Step 1: Expand the narrative block-model section**

```md
### 8.1 Block schema contract and render rules

- Assistant output is always a typed `Block[]` response envelope, not plain markdown and not a tool call.
- Every block kind inherits the `BaseBlock` contract: `id`, `kind`, `snapshot_id`, `data_ref`, `source_refs`, and `as_of`.
- The canonical schema field is `data_ref`.
- Earlier analysis used `dataRef` or `queryRef`; the schema standardizes this as `data_ref`.
- Narrative and layout blocks: `rich_text`, `section`
- Tabular and compact metric blocks: `metric_row`, `table`
- Chart and comparison blocks: `line_chart`, `revenue_bars`, `perf_comparison`, `segment_donut`, `segment_trajectory`, `metrics_comparison`, `sentiment_trend`, `mention_volume`
- Research and evidence summary blocks: `analyst_consensus`, `price_target_range`, `eps_surprise`, `filings_list`, `news_cluster`, `finding_card`
- Trust and rendering-boundary blocks: `sources`, `disclosure`
- `Sources` is the required provenance surface whenever external evidence appears in the answer.
- `Disclosure` is the explicit trust and compliance surface and may be injected by orchestration.
- `as_of` is the freshness boundary for the rendered artifact.

### 8.2 Downstream consumer rules for block artifacts

- Thread coordinator and transport (`P2.1`) consumes `Block[]` as the streamed and persisted assistant payload.
- Block registry versioning and validation (`P2.3`) consumes the exact block kinds plus the shared `BaseBlock` fields.
- Snapshot assembler and verifier (`P2.4`) consumes `snapshot_id`, `source_refs`, `data_ref`, and `as_of` to verify rendered artifacts against sealed evidence.
- Findings, home feed, and explainability (`P4.2`, `P4.3`, `P4.6`) consume `finding_card`, `sources`, `disclosure`, and the same snapshot-safe render rules used in chat and analyze.
- Frontend renderer (`PX.3`) consumes `Block[]` via a shared `BlockRegistry` and must not treat rendering as a tool invocation.
- Chat, Analyze, and agent-produced findings all render through the same `BlockRegistry`, keyed by block `kind`.
- Interactivity stays inside snapshot scope unless the user explicitly refreshes.
```

- [ ] **Step 2: Add schema descriptions to the normative JSON artifact**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.com/schemas/finance_research_block_schema.json",
  "title": "Finance Research Block Schema",
  "description": "Typed assistant-response schema for structured Block[] artifacts rendered by Chat, Analyze, and findings surfaces.",
  "type": "object",
  "required": ["blocks"],
  "properties": {
    "blocks": {
      "type": "array",
      "items": { "$ref": "#/$defs/Block" },
      "minItems": 1
    }
  },
  "$defs": {
    "DataRef": {
      "type": "object",
      "description": "Canonical backend binding for a block. Historical dataRef/queryRef language maps to data_ref in this schema.",
      "required": ["kind", "id"],
      "properties": {
        "kind": { "type": "string" },
        "id": { "type": "string" },
        "params": { "type": "object", "additionalProperties": true }
      },
      "additionalProperties": false
    },
    "BaseBlock": {
      "type": "object",
      "description": "Shared render, audit, provenance, and snapshot binding fields for every block.",
      "required": ["id", "kind", "snapshot_id", "data_ref", "source_refs", "as_of"],
      "properties": {
        "id": { "type": "string" },
        "kind": { "type": "string" },
        "snapshot_id": { "$ref": "#/$defs/UUID" },
        "data_ref": { "$ref": "#/$defs/DataRef" },
        "source_refs": {
          "type": "array",
          "items": { "$ref": "#/$defs/UUID" }
        },
        "as_of": { "type": "string", "format": "date-time" }
      }
    },
    "Sources": {
      "allOf": [
        { "$ref": "#/$defs/BaseBlock" },
        {
          "type": "object",
          "description": "Provenance block required whenever external evidence appears in the answer.",
          "properties": {
            "kind": { "const": "sources" }
          }
        }
      ]
    },
    "Disclosure": {
      "allOf": [
        { "$ref": "#/$defs/BaseBlock" },
        {
          "type": "object",
          "description": "Disclosure block for trust and compliance notes; orchestration may inject it.",
          "properties": {
            "kind": { "const": "disclosure" }
          }
        }
      ]
    }
  }
}
```

- [ ] **Step 3: Run the contract test and confirm green**

Run: `python3 -m unittest tests.contracts.test_block_schema_contract -v`
Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add spec/finance_research_spec.md spec/finance_research_block_schema.json
git commit -m "docs: define block schema contract"
```

### Task 3: Verify and land the bead

**Files:**
- Modify: `.beads/issues.jsonl` (via `bd close` / `bd sync`)
- Test: `tests/contracts/test_block_schema_contract.py`

- [ ] **Step 1: Inspect repo state**

Run: `git status --short`
Expected: only intended spec, schema, test, plan, and bead metadata changes remain; `spec/finance_research_tool_registry.json` stays untracked.

- [ ] **Step 2: Close the bead**

Run: `bd close stock-agent-h3e.1.1.5 --reason "Completed"`
Expected: issue status becomes `CLOSED`.

- [ ] **Step 3: Sync and commit bead metadata**

Run: `bd sync`
Expected: beads metadata is exported cleanly.

- [ ] **Step 4: Rebase and push branch**

Run: `git pull --rebase origin main`
Expected: branch rebases cleanly or reports already up to date.

Run: `git push -u origin stock-agent-h3e.1.1.5`
Expected: push succeeds.

- [ ] **Step 5: Fast-forward main**

Run: `git checkout main && git pull --rebase origin main && git merge --ff-only stock-agent-h3e.1.1.5`
Expected: `main` now contains the bead commits without a merge commit.

- [ ] **Step 6: Push main and confirm final status**

Run: `git push origin main`
Expected: push succeeds.

Run: `git status`
Expected: branch is up to date with `origin/main`; any remaining untracked files are unrelated baseline artifacts already tracked by follow-up issue `stock-agent-dkz`.
