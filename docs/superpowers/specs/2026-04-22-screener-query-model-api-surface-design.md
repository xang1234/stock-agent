# Screener Query Model And API Surface Design

## Goal

Define the screening query model and service-owned API boundary that build deterministic screener results, so later UI flow, saved screens, and dynamic watchlists depend on a stable query-and-row contract rather than ad hoc client joins.

## Scope

This design covers:

- the first structured query model for screener execution
- result-set semantics for ranked screener rows
- the service boundary between `/v1/screener/*` and the underlying market and fundamentals services
- the relation between reusable screen definitions and derived result sets
- downstream consumer expectations for `P1.4b` and `P4.7`
- a narrative spec update plus a file-based contract test

This design does not define the visual screener builder, saved-screen navigation flow, client layout details, comparison workflows, or dynamic watchlist rendering.

## Core Contract

### Query model

- Screener queries should be explicit structured filter-and-rank envelopes rather than a freeform analytics DSL or arbitrary user-authored formulas.
- The minimum query dimensions should cover universe constraints, market or quote constraints, fundamentals or aggregate constraints, sort specification, and page or limit controls.
- Query clauses should bind to screener-owned fields backed by the market-data and fundamentals services rather than exposing raw provider payload columns or frontend-computed joins.

### Result semantics

- A screener response should be an ordered derived result set rather than a new canonical identity type for returned entities.
- Each result row should carry canonical market subject identity, display identity, ranking or sort context, and compact quote or fundamentals summaries sufficient for screener-table rendering.
- Screener rows should remain thinner than symbol-detail hydration: selecting a row hands off canonical subject identity for later subject-entry flows rather than embedding a full symbol workspace payload.
- A reusable `screen` subject should represent the persisted query definition plus ordering semantics, not a frozen list of prehydrated row payloads.

### Service and API ownership

- The Screener service should own query validation, execution, ranking, pagination, and row-envelope assembly.
- `/v1/screener/*` should remain the client boundary for screener queries and results, even when the service internally reads market-data and fundamentals outputs.
- Clients should not reconstruct screener tables by fanning out across `/v1/market/*` and `/v1/fundamentals/*` and inventing their own join semantics.

## Downstream Consumer Matrix

### Screener UI flow and saved-screen handoff (`P1.4b`)

- `P1.4b` depends on stable query envelopes and result-row semantics so browse, refine, save, and subject-entry flows can stay thin and avoid inventing a second client-side screener model.

### Dynamic watchlists and portfolio overlays (`P4.7`)

- `P4.7` depends on screen definitions remaining replayable, service-owned query objects so later dynamic watchlists can regenerate a screen universe without scraping transient UI state or storing raw row payloads as truth.

## Normative File Changes

### `spec/finance_research_spec.md`

- Expand the screening-service section with a screener query-and-result contract subsection.
- Add a downstream-consumer subsection naming `P1.4b` and `P4.7`.
- Keep the screener contract clearly separate from later UI-flow and saved-screen behavior.

### `tests/contracts/test_screener_query_model_api_surface_contract.py`

- Add a file-based contract test that asserts the narrative spec contains the query-model, result-semantics, service-ownership, and downstream-consumer wording anchors.

## Acceptance Mapping

- The query-dimension rules satisfy the acceptance around the screening query model.
- The result-set rules satisfy the acceptance around result semantics.
- The service-boundary and downstream notes satisfy the acceptance around owning API boundaries and later consumers.
