# Relational Schema Contract Design

## Goal

Define the database-schema boundary from the schema pack so later services can understand table ownership, storage concerns, and coupling without rereading the full SQL artifact.

## Scope

This design covers:

- the major table families in `finance_research_db_schema.sql`
- which subsystems own or consume each family
- the storage split between app metadata, evidence-plane relational data, and raw document blobs
- normative updates to the narrative spec, SQL schema notes, and a small file-based contract test

This design does not restate every column, redesign the storage platform, or add new schema tables. It clarifies ownership and coupling in the existing schema pack.

## Core Contract

### Reference and universe tables

- `issuers`, `instruments`, `listings`, `themes`, `theme_memberships`, `portfolios`, `portfolio_holdings`, `watchlists`, and `watchlist_members` define reusable subject context and membership state.
- These tables support identity resolution, user-curated universes, and subject scoping for downstream services.
- They are canonical reference data, not evidence records and not user-facing artifact storage.

### Evidence-plane relational tables

- `metrics`, `sources`, `documents`, `mentions`, `claims`, `claim_arguments`, `entity_impacts`, `claim_evidence`, `claim_clusters`, `claim_cluster_members`, `events`, `event_subjects`, `facts`, `computations`, `snapshots`, `findings`, `run_activities`, `citation_logs`, `verifier_fail_logs`, and `eval_run_results` form the relational evidence plane.
- This family is where provenance, auditability, promotion state, sealed snapshots, and snapshotted findings live.
- These tables are the canonical relational backbone for the fact, claim, event, and snapshot model and should remain distinct from app metadata.

### App metadata and orchestration tables

- `users`, `chat_threads`, `chat_messages`, `analyze_templates`, `agents`, and `tool_call_logs` support product flows, user state, orchestration, and coordination.
- These tables may reference evidence-plane objects such as snapshots or findings, but they do not redefine the evidence contract.
- JSON fields in orchestration tables are workflow state around the evidence plane rather than replacements for canonical evidence objects.

### Storage split

- App metadata may live in smaller app storage such as D1 or Postgres, depending on deployment constraints.
- Evidence objects and snapshots belong to the relational evidence plane and should live in Postgres-class storage that preserves relational integrity and auditability.
- Raw document bytes are outside the relational schema and should live in object storage, addressed by `raw_blob_id` and related metadata stored in relational tables.

### Snapshot bridge

- `snapshots` are evidence-plane records, not just app metadata.
- Snapshots seal references across facts, claims, events, sources, and tool calls at a specific `as_of`.
- Snapshots bridge the evidence plane to user-facing artifacts such as chat messages and findings.

## Downstream Consumer Matrix

### Quote and bar provider abstraction (`P1.1`)

Quote and bar work consumes reference tables plus evidence-plane value tables as lookup and persistence context. It should not depend on chat or template tables for source-of-truth semantics.

### Statement and metric normalization (`P1.2`)

Statement normalization consumes `metrics`, `facts`, `computations`, identity tables, and snapshot references as the canonical relational backbone for normalized values.

### Source document and provenance model (`P3.1`)

Source and provenance work owns `sources`, `documents`, and related evidence-plane tables that track where evidence came from, how it was parsed, and how it is referenced downstream.

### Promotion rules for candidate facts (`P3.5`)

Promotion work consumes `claims`, `claim_evidence`, `events`, `facts`, and `computations` inside the evidence plane. It should not use orchestration JSON blobs as a substitute for promotion state.

## Normative File Changes

### `spec/finance_research_spec.md`

- Add a relational schema contract section that groups tables into reference and universe, evidence-plane, and app metadata families.
- Add storage-split notes explaining that raw document bytes live outside the relational schema and that snapshots bridge evidence to user-facing artifacts.

### `spec/finance_research_db_schema.sql`

- Add schema notes near the top of the file clarifying the major table families and their intended storage or ownership boundaries.

### `tests/contracts/test_relational_schema_contract.py`

- Add a file-based contract test that asserts the required section headings and exact wording anchors exist in the narrative spec and SQL notes.

## Acceptance Mapping

- The major table families and their owners satisfy the schema-boundary requirement for `stock-agent-h3e.1.1.3`.
- The storage split clarifies that app metadata, evidence objects, snapshots, and raw document blobs have distinct concerns.
- The consumer matrix unblocks quote or bar abstraction (`P1.1`), statement normalization (`P1.2`), source document or provenance work (`P3.1`), and candidate-fact promotion (`P3.5`).
