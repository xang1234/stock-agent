# Identity And Research Subject Contract Design

## Goal

Define the canonical contract for finance identity and research-subject references so downstream services use the same vocabulary and do not treat tickers as stable identity.

## Scope

This design covers:

- canonical identity rules for issuer, instrument, and listing
- `SubjectRef` selection rules for entity-centric and non-entity subjects
- downstream consumer expectations for resolver, market data, fundamentals, chat/analyze, and agent workflows
- normative updates to the implementation spec, OpenAPI schema, and SQL schema notes

This design does not cover resolver algorithms, vendor selection, non-US coverage implementation, or ingestion workflows outside the contract notes required to unblock dependent beads.

## Core Contract

### Identity layers

- `Issuer` is the canonical reference for the legal or reporting entity.
- `Instrument` is the canonical reference for the tradable security definition issued by an issuer.
- `Listing` is the canonical reference for an exchange-specific trading venue representation of an instrument.
- `ticker` is a listing attribute and lookup handle, not canonical identity.

### Boundary rules

- Use `issuer` when the subject is a company, filer, management team, business profile, reporting entity, or issuer-level fundamentals.
- Use `instrument` when the subject is a security definition such as a share class, ADR, ETF, bond, or crypto instrument independent of venue.
- Use `listing` when the subject depends on venue-specific symbol, currency, session, corporate action alignment, or local market context.
- Resolution may begin from a ticker or alias, but any downstream contract must promote that lookup into an explicit `SubjectRef`.
- A downstream surface may display a ticker, but it must not persist or join on ticker where an issuer, instrument, or listing identity exists.

### `SubjectRef` selection

- `SubjectRef(kind='issuer')` is the default for issuer research, filing-backed facts, company summaries, and issuer-scoped findings.
- `SubjectRef(kind='instrument')` is the default for instrument-level analytics that should survive listing changes or multiple venue representations.
- `SubjectRef(kind='listing')` is required for quote, bar, session, and venue-bound market interactions.
- `theme`, `macro_topic`, `portfolio`, and `screen` remain valid non-entity research subjects and do not replace entity identity.

## Downstream Consumer Matrix

### Resolver service

The resolver owns alias, ticker, and external identifier mapping into explicit issuer, instrument, or listing candidates. It must surface ambiguity instead of collapsing multiple listings into one ticker string.

### Market data service

The market data service keys quotes, bars, session state, and venue-sensitive performance on `listing`, with optional rollups to `instrument` only when the transformation is explicit.

### Fundamentals service

The fundamentals service keys issuer profile, filings-backed statements, and fiscal normalization on `issuer`. Instrument-specific metadata may be attached where needed, but ticker is not a stable join key.

### Chat and Analyze

Chat and Analyze may accept user input such as tickers or company names, but persisted subject context must be stored as `SubjectRef[]`. Rendering may show human-friendly tickers while provenance, snapshots, and retrieval use canonical subject references.

### Agents and findings

Agent definitions, runs, findings, and subscriptions must carry `SubjectRef[]` so monitoring remains stable across ticker changes, cross-listings, ADRs, and dual-class structures.

## Normative File Changes

### `spec/finance_research_spec.md`

- Add a canonical identity rules subsection beneath the finance identity layer.
- Expand the research subject section with `SubjectRef` selection rules.
- Add a downstream consumer matrix near the service boundaries.

### `spec/finance_research_openapi.yaml`

- Add descriptive schema text to `SubjectKind`, `SubjectRef`, and `ResolvedSubject` clarifying canonical identity and ticker-as-listing semantics.

### `spec/finance_research_db_schema.sql`

- Add schema notes near the identity tables and `subject_kind` enum clarifying issuer vs instrument vs listing ownership and the rule that ticker is a listing locator, not canonical identity.

## Acceptance Mapping

- Explicit issuer/instrument/listing and `SubjectRef` boundaries satisfy the contract portion of `stock-agent-h3e.1.1.1`.
- The downstream consumer matrix unblocks resolver (`P0.3`), fundamentals (`P1`), chat/analyze (`P2`), and non-US coverage follow-on work (`P6.2`).
- The notes explicitly preserve the invariant that ticker is not canonical identity.
