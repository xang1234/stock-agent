# HTTP API Contract Design

## Goal

Define the HTTP API boundary from the OpenAPI artifact so frontend, orchestration, and rendering work depend on stable backend contracts rather than direct provider integrations.

## Scope

This design covers:

- the major endpoint groups in `finance_research_openapi.yaml`
- which service or product surface owns each group
- which downstream subsystems consume each group
- explicit non-goals around direct third-party calls from the client
- normative updates to the narrative spec, OpenAPI descriptions, and a small file-based contract test

This design does not redesign the API surface, add new endpoints, or change transport semantics beyond clarifying ownership and consumer boundaries already implied by the artifact.

## Core Contract

### Endpoint groups and owners

- `Subjects` owns free-text resolution into canonical subject references.
- `Market` owns quote and series reads for market data.
- `Fundamentals` owns normalized profile and statement reads.
- `Evidence` owns claims, events, documents, and evidence-bundle reads over structured backend state.
- `Snapshots` owns sealed snapshot retrieval and allowed in-snapshot transforms.
- `Chat` owns thread creation, message creation, and SSE run streaming.
- `Analyze` owns template listing, template creation, and template-run initiation.
- `Agents` owns agent CRUD-adjacent reads plus findings and activity retrieval.
- `Home` owns findings-first feed retrieval.
- `Watchlists` owns watchlist listing and creation.
- `Screener` owns backend-executed screen searches.

### BFF and client boundary

- The frontend only talks to `/v1/*` backend contracts.
- The frontend does not call third-party providers directly for market, fundamentals, evidence, or screening data.
- Interactive updates such as chat streaming, snapshot transforms, and series refreshes stay inside backend-managed endpoints rather than bypassing the API layer.

### Snapshot and transport boundary

- `Chat` plus `Snapshots` define the run, stream, and render boundary for assistant turns.
- Message creation starts a backend run.
- SSE events stream backend-owned turn and block lifecycle updates.
- Snapshot retrieval and transform endpoints are the only supported path for snapshot-safe post-generation interactions.

## Downstream Consumer Matrix

### App shell and route groups (`P0.2`, `P0.4`)

Shell and route work consumes the `/v1/*` groups as the stable backend surface behind Home, Agents, Chat, Screener, Watchlists, Analyze, and symbol-detail flows.

### Market and fundamentals consumers (`P1`)

Market and fundamentals surfaces consume `Subjects`, `Market`, and `Fundamentals` as the client-visible BFF boundary. Provider-specific identifiers, auth, and payload shapes stay behind this layer.

### Thread coordinator and transport (`P2.1`)

Thread transport depends on `Chat` and `Snapshots`: message creation starts runs, SSE streams incremental lifecycle events, and sealed snapshots back the final rendered result.

### Block rendering and interactive artifacts (`PX.3`)

Renderer and post-generation interactivity depend on `Snapshots`, `Analyze`, `Home`, and other `/v1/*` APIs. Rendering code should never fetch provider data directly.

## Normative File Changes

### `spec/finance_research_spec.md`

- Add an HTTP API ownership and consumer rules subsection beneath the API contracts section.
- Add explicit non-goals around direct third-party calls from the client.

### `spec/finance_research_openapi.yaml`

- Add top-level and endpoint-group descriptions clarifying that `/v1/*` is the client-facing BFF surface.
- Add clarifying descriptions on chat streaming and snapshot transform endpoints as backend-mediated interactions.

### `tests/contracts/test_http_api_contract.py`

- Add a file-based contract test that asserts the required ownership and client-boundary wording exists in the narrative spec and OpenAPI artifact.

## Acceptance Mapping

- Major endpoint groups and their owners satisfy the API-boundary requirement for `stock-agent-h3e.1.1.4`.
- The client/BFF non-goal satisfies the acceptance note around direct third-party calls from the client.
- The consumer matrix unblocks shell and route work (`P0.2`, `P0.4`), market and fundamentals surfaces (`P1`), chat transport (`P2.1`), and block-renderer work (`PX.3`).
