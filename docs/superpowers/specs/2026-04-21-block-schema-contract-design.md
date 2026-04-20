# Block Schema Contract Design

## Goal

Define the typed assistant-response boundary from the block schema artifact so chat, analyze, findings, and frontend rendering all depend on the same structured `Block[]` contract instead of ad hoc markdown or tool-shaped output.

## Scope

This design covers:

- the shared `BaseBlock` binding fields in `finance_research_block_schema.json`
- the core block families and their intended product role
- the render, provenance, disclosure, and `as_of` rules consumers must honor
- the distinction between typed response blocks and backend tools
- the downstream consumers named in the bead acceptance criteria
- normative updates to the narrative spec, the JSON schema artifact, and a small file-based contract test

This design does not redesign the block system, add new rendering surfaces, or introduce a second binding model alongside the existing schema.

## Core Contract

### Typed response boundary

- Assistant output is always a typed `Block[]` response envelope, not plain markdown and not a tool call.
- Backend tools fetch, compute, or act; the block schema defines the assistant's user-facing artifact contract.
- `spec/finance_research_block_schema.json` is the normative artifact for block shape.
- `spec/finance_research_spec.md` explains the behavioral and consumer rules that sit around the schema.

### Shared block bindings

- Every block kind inherits the `BaseBlock` contract: `id`, `kind`, `snapshot_id`, `data_ref`, `source_refs`, and `as_of`.
- These fields are the minimum render, audit, and provenance boundary for any user-visible artifact block.
- `snapshot_id` binds the block to a sealed evidence snapshot.
- `source_refs` binds the rendered block to the source plane used to support it.
- `as_of` is part of the render contract, not decorative metadata. Consumers must treat it as the freshness boundary of the visible artifact.

### Binding terminology

- The canonical schema field is `data_ref`.
- Earlier analysis material described `dataRef` or `queryRef` as the way blocks refer to backend-bound data.
- This contract standardizes that idea as `data_ref` with a typed `{ kind, id, params? }` object rather than introducing a second first-class `query_ref` field.
- Downstream work should treat `dataRef` or `queryRef` language as historical terminology for the current `data_ref` binding model unless a future bead intentionally expands the schema.

### Core block families

- Narrative and layout blocks: `rich_text`, `section`
- Tabular and compact metric blocks: `metric_row`, `table`
- Chart and comparison blocks: `line_chart`, `revenue_bars`, `perf_comparison`, `segment_donut`, `segment_trajectory`, `metrics_comparison`, `sentiment_trend`, `mention_volume`
- Research and evidence summary blocks: `analyst_consensus`, `price_target_range`, `eps_surprise`, `filings_list`, `news_cluster`, `finding_card`
- Trust and rendering-boundary blocks: `sources`, `disclosure`

### Block-specific rules

- `RichText` remains reference-bound through fact, claim, and event refs rather than free-floating prose.
- `Section` is the first-class composition primitive for nested block layouts.
- `PerfComparison` is snapshot-aware and transform-aware; in-snapshot changes may vary timeframe only when the requested range stays within the sealed `as_of` boundary and preserves subject set, basis, and normalization.
- `Sources` is the required provenance surface whenever external evidence appears in the answer.
- `Disclosure` is the explicit trust and compliance surface and may be injected by orchestration even when the model did not emit it directly.

## Downstream Consumer Matrix

### Thread coordinator and transport (`P2.1`)

Thread transport depends on `Block[]` as the streamed and persisted assistant payload. Runs produce typed blocks rather than markdown transcripts.

### Block registry versioning and validation (`P2.3`)

Registry and validator work depends on the exact block kinds plus the shared `BaseBlock` fields as the stable schema boundary.

### Snapshot assembler and verifier (`P2.4`)

Snapshot assembly and verification depend on `snapshot_id`, `source_refs`, `data_ref`, and `as_of` to prove that rendered artifacts are bound to sealed evidence rather than free-floating UI content.

### Findings, home feed, and explainability (`P4.2`, `P4.3`, `P4.6`)

Finding and explainability surfaces depend on `finding_card`, `sources`, `disclosure`, and the same snapshot-safe render rules used in chat and analyze.

### Frontend renderer (`PX.3`)

Frontend rendering depends on the schema distinction between typed response blocks and backend tools. Rendering code consumes `Block[]` via a shared `BlockRegistry` and does not treat block generation as a tool invocation.

## Interaction And Rendering Rules

- Chat, Analyze, and agent-produced findings all render through the same `BlockRegistry`, keyed by block `kind`.
- Interactivity stays inside snapshot scope unless the user explicitly refreshes.
- `interactive` metadata may expose controls such as ranges, intervals, sort fields, hover details, or collapsible behavior, but those controls cannot silently cross the sealed `as_of` boundary.
- Client renderers may perform local presentation-only actions when the relevant rows or series are already present in the sealed payload.
- Data-bearing interactions still go back through backend snapshot APIs rather than turning the renderer into a direct data client.
- The contract continues to reject "rendering as a tool." Tools are backend actions or data access; the block schema is the typed response envelope.

## Normative File Changes

### `spec/finance_research_spec.md`

- Expand the block model section to document the shared `BaseBlock` bindings, the block families, the `data_ref` terminology decision, and the snapshot-safe render rules.
- Add explicit downstream consumer notes for transport, registry validation, snapshot verification, findings, and frontend rendering.

### `spec/finance_research_block_schema.json`

- Add top-level or definition-level schema descriptions that clarify the typed-response purpose of the artifact, the shared role of `BaseBlock`, and the canonical `data_ref` terminology.
- Preserve the distinction between response schema and tool registry rather than blending the two contracts.

### `tests/contracts/test_block_schema_contract.py`

- Add a file-based contract test that asserts the required wording anchors exist in the narrative spec and the JSON schema artifact.

## Acceptance Mapping

- The documented block families satisfy the acceptance requirement around core block families.
- The `data_ref` terminology note satisfies the acceptance requirement around `dataRef` or `queryRef` expectations without introducing a second binding model.
- The `Sources`, `Disclosure`, and `as_of` rules satisfy the disclosure and freshness requirements.
- The consumer matrix unblocks `P2.1`, `P2.3`, `P2.4`, `P4.2`, `P4.3`, `P4.6`, and `PX.3`.
