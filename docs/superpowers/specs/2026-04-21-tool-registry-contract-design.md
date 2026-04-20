# Tool Registry And Bundle Contract Design

## Goal

Define the tool-registry and bundle boundary from the registry artifact so routing, reader extraction, analyst orchestration, and approval-sensitive actions all depend on one explicit contract for what tools exist and who may use them.

## Scope

This design covers:

- the bundle groups in `finance_research_tool_registry.json`
- the reader versus analyst audience boundary
- the key analyst, reader, and write-intent tool families
- approval-sensitive and non-read-only tool categories
- the distinction between tool contracts and response-artifact contracts
- the downstream consumers named in the bead acceptance criteria
- normative updates to the narrative spec, the JSON registry artifact, and a small file-based contract test

This design does not redesign routing algorithms, approval UX, or the reader and analyst runtime. It clarifies the registry and policy boundary already implied by the artifact.

## Core Contract

### Tool registry boundary

- `spec/finance_research_tool_registry.json` is the normative artifact for bundle membership, tool audience, approval sensitivity, and JSON-schema-constrained inputs and outputs.
- The tool registry is a separate contract from the block schema.
- Tools are backend data and action surfaces; `Block[]` remains the assistant's typed response artifact.
- The system chooses the bundle; the model chooses tools within the bundle.

### Bundle groups

- The registry should document the existing bundle groups explicitly: `quote_lookup`, `single_subject_analysis`, `peer_comparison`, `theme_research`, `segment_deep_dive`, `document_research`, `filing_research`, `screener`, `agent_management`, `alert_management`, and `analyze_template_run`.
- Bundle selection is a routing and policy decision that happens before the analyst tool loop.
- Bundle membership is the stable contract that downstream orchestrators and budget policy rely on, not an implementation detail hidden inside prompts.

### Reader versus analyst boundary

- `reader` tools are the only tools allowed to access raw untrusted text or raw documents.
- `analyst` tools operate only on structured outputs, canonical subject and period resolution, evidence bundles, facts, claims, events, and approval-mediated write intents.
- Raw text must not leak into analyst-facing tools.
- Reader and analyst bundles are not interchangeable: reader tools transform untrusted inputs into typed extractions; analyst tools reason over trusted structured objects.

### Key tool families

- Analyst tool families include subject and period resolution, market and fundamentals reads, evidence and lineage reads, peer and screen tools, and write-intent tools.
- Reader tool families include raw document search and fetch plus typed extraction and classification tools.
- Key reader tools should be called out explicitly: `search_raw_documents`, `fetch_raw_document`, `extract_mentions`, `extract_claims`, `extract_candidate_facts`, `extract_events`, and `classify_sentiment`.
- Key analyst tools should be called out explicitly across the bundle surface: `resolve_subjects`, `resolve_period`, `get_quote`, `get_series`, `get_statement_facts`, `get_claims`, `get_events`, `get_evidence_bundle`, `get_peer_set`, and `screen`.

### Side-effect and approval categories

- Approval-sensitive tools today are `create_alert` and `create_agent`.
- These tools are non-read-only and `approval_required: true`; downstream systems should treat them as pending actions until orchestration or the user confirms them.
- `add_to_watchlist` is also a non-read-only write-intent tool even though it is not currently approval-required.
- The contract should explicitly state that not every non-read-only tool is approval-gated today, but every non-read-only tool is still a policy boundary that downstream systems must classify intentionally.

### JSON-schema and traceability rules

- Every tool input and output remains JSON-schema constrained.
- Tool outputs must be traceable to source refs or deterministic computations.
- Reader-only access to raw untrusted content is a trust boundary, not just a cost or performance hint.

## Downstream Consumer Matrix

### Pre-resolve routing and budget policy (`P2.2`)

Routing and budget policy depends on deterministic bundle selection, audience separation, and registry metadata such as `cost_class`, `freshness_expectation`, `read_only`, and `approval_required` before the analyst loop starts.

### Document ingestion and extraction (`P3.2`)

Document ingestion and extraction depends on the reader boundary staying sharp: raw document search, fetch, and extraction tools belong to the reader audience, and their typed outputs are the only supported path by which raw text becomes analyst-consumable evidence.

### Alerting and automation (`P5.1`)

Alerting and automation depends on the side-effect categories and approval sensitivity in the registry so create and update flows do not execute directly from model output.

### Tool runtime and orchestration (`PX.2`)

The runtime depends on bundle membership, audience, `read_only`, `approval_required`, `cost_class`, and `freshness_expectation` as the policy envelope around model tool use.

## Normative File Changes

### `spec/finance_research_spec.md`

- Expand the tool-registry section with bundle groups, audience boundaries, key tool families, and the distinction between tools and response artifacts.
- Add explicit downstream consumer notes for routing policy, reader extraction, automation, and orchestration runtime.

### `spec/finance_research_tool_registry.json`

- Add top-level and bundle or tool descriptions that clarify audience boundaries, approval-sensitive write-intent behavior, and the distinction between reader and analyst surfaces.
- Preserve the rule that reader-only tools may touch raw untrusted content while analyst-facing tools may not.

### `tests/contracts/test_tool_registry_contract.py`

- Add a file-based contract test that asserts the required wording anchors exist in the narrative spec and the registry artifact.

## Acceptance Mapping

- The documented bundle groups satisfy the acceptance requirement around bundle groups.
- The explicit reader versus analyst rules satisfy the acceptance requirement around reader versus analyst boundaries.
- The approval-sensitive and non-read-only write-intent notes satisfy the acceptance requirement around side-effect categories and approval-sensitive tools.
- The consumer matrix unblocks `P2.2`, `P3.2`, `P5.1`, and `PX.2`.
