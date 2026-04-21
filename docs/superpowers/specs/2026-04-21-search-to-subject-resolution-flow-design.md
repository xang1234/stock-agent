# Search To Subject Resolution Flow Design

## Goal

Define the deterministic flow from symbol or name search through canonical subject selection and downstream subject hydration, so every caller enters watchlists, quote surfaces, fundamentals, and chat with the same stable subject handoff.

## Scope

This design covers:

- the staged flow from lookup input to candidate search, canonical selection, and hydrated subject handoff
- the rule that exact unique deterministic hits may auto-advance without a chooser, while ambiguity must stop at explicit candidate preservation
- the minimal hydrated subject bundle that downstream consumers receive after selection
- persistence and escalation rules for `resolved`, `ambiguous`, and `not_found` outcomes inside the search flow
- downstream consumer expectations for quote snapshots, market data, fundamentals, chat pre-resolution, and watchlist or saved-subject entry flows
- a narrative spec update plus a file-based contract test

This design does not define search ranking UI, chooser interaction design, quote rendering, fundamentals payloads, watchlist CRUD, or full chat-router policy beyond the subject handoff this flow provides.

## Core Contract

### Search-to-subject flow stages

- This bead should define a deterministic staged flow from free-text or provider-backed lookup input to downstream subject hydration.
- The stages are: candidate search, canonical selection, and hydrated subject handoff.
- Candidate search may return zero, one, or many candidates, but it does not itself invent a silent winner from ambiguous matches.
- If search produces exactly one deterministic candidate that already satisfies the resolver contract, the flow may auto-advance to canonical selection without a user choice step.
- If multiple plausible candidates remain, the flow must stop at explicit ambiguity preservation and surface ranked candidates for a later user or caller choice.
- Canonical selection consumes either the auto-advanced unique candidate or an explicit chosen candidate and normalizes it into deterministic canonical subject identity.
- Hydrated subject handoff begins only after canonical selection succeeds; it is a downstream-safe package rather than a loose ticker or raw provider record.
- This flow should stay distinct from search ranking UX and from the lower-level resolver contract. The resolver defines `resolved`, `ambiguous`, and `not_found`; this bead defines how search and selection carry those outcomes into subject hydration.

### Hydrated subject bundle and consumer handoff

- This bead should define a downstream-safe hydrated subject bundle rather than stopping at a bare canonical `SubjectRef`.
- The hydrated bundle should include the selected canonical `SubjectRef`, the resolved identity level, stable display labels, and enough issuer, instrument, or listing context for immediate downstream use without another identity round trip.
- The hydrated bundle should also carry resolver provenance, including the normalized lookup input and whether the subject came from auto-advanced unique resolution or explicit candidate choice.
- The flow should preserve the distinction between identity levels inside the bundle. Quote and market consumers may need listing context, while filing and fundamentals consumers may need issuer context, and callers should not infer that from a ticker string.
- Watchlists, chat turns, Analyze entry, and service-to-service calls should all consume the same hydrated subject bundle contract even if they later project only the fields they need.
- The flow should allow one canonical selection to produce more than one joined identity facet in the bundle, such as an issuer-backed view plus its active market listing context, as long as the canonical `SubjectRef` remains explicit.
- Downstream consumers may persist the canonical `SubjectRef` as their durable key, but they should treat the rest of the hydrated bundle as handoff context rather than inventing their own identity joins.
- This bead should not define full quote, fundamentals, or watchlist payloads. It only defines the minimal hydrated subject package that makes those downstream flows deterministic and cheap to enter.

### Boundary and downstream consumers

- This bead should define the staged contract from search input through candidate handling, canonical selection, and hydrated subject handoff.
- It should not define search ranking UI, quote rendering, fundamentals tables, watchlist CRUD, or chat routing policy beyond the subject handoff those systems consume.
- The flow contract should make one escalation rule explicit: `not_found` ends the flow without hydration, `ambiguous` pauses at explicit candidate choice, and only `resolved` may produce a hydrated subject bundle.
- The contract should also make one persistence rule explicit: downstream systems persist the canonical `SubjectRef` as the durable subject key, while hydrated bundle metadata is entry context that may be refreshed later.

## Downstream Consumer Matrix

### Symbol search and quote snapshot surface (`P0.4`)

- `P0.4` depends on this bead for symbol search entry points, explicit candidate choice rules, and the hydrated subject handoff that quote snapshot surfaces can enter with.

### Market data service (`P1.1`)

- `P1.1` depends on this bead for listing-appropriate subject handoff into quote and bar retrieval rather than ticker-string lookup.

### Fundamentals service (`P1.2`)

- `P1.2` depends on this bead for issuer-appropriate subject handoff into statement and metric normalization instead of asking fundamentals consumers to rediscover identity.

### Pre-resolve router and budget policy (`P2.2`)

- `P2.2` depends on this bead for deterministic subject handoff into pre-resolve routing so chat turns start from canonical subject context rather than ad hoc model interpretation of search strings.

### Watchlist and saved-subject entry flows

- Watchlist and saved-subject entry flows depend on the same hydrated subject bundle contract so selected subjects can be saved, reopened, and re-entered without rediscovering identity from raw lookup text.

## Normative File Changes

### `spec/finance_research_spec.md`

- Add a new narrative subsection under the identity and resolver boundary that defines candidate search, auto-advance for unique deterministic hits, ambiguity stop conditions, canonical selection, hydrated subject bundle contents, and the durable `SubjectRef` persistence rule.
- Add downstream consumer notes for quote snapshots, market data, fundamentals, pre-resolve routing, and watchlist or saved-subject entry flows.

### `tests/contracts/test_search_to_subject_resolution_flow_contract.py`

- Add a file-based contract test that asserts the narrative spec contains the staged-flow, auto-advance, ambiguity-stop, hydrated-bundle, persistence, and downstream-consumer wording anchors.

## Acceptance Mapping

- Candidate search, explicit ambiguity handling, and canonical selection satisfy the bead acceptance around search candidates and deterministic subject selection.
- The hydrated subject bundle and durable `SubjectRef` persistence rule satisfy the acceptance around subject hydration into watchlists, services, and chat turns.
- The downstream consumer matrix unblocks `P0.4`, `P1.1`, `P1.2`, `P2.2`, and watchlist or saved-subject entry flows.
