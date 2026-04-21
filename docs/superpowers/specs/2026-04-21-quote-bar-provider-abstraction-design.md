# Quote And Bar Provider Abstraction Design

## Goal

Define the provider-neutral boundary for quote and historical-bar retrieval so symbol surfaces, charting, and orchestration depend on one stable market-data contract rather than provider-specific payloads or identifiers.

## Scope

This design covers:

- the internal provider abstraction boundary for quote and bar retrieval inside the market data service
- the rule that quote and bar retrieval begin from listing-appropriate hydrated subject context rather than raw ticker strings or provider ids
- normalized quote retrieval responsibilities, including freshness and provenance fields that downstream consumers can trust
- normalized bar retrieval responsibilities, including interval, range, and adjustment metadata boundaries
- the separation between provider normalization in this bead and later adjusted-series or caching policy work
- downstream consumer expectations for `P1.1b`, `P1.3`, `P2.2`, and `P6.5`
- a narrative spec update plus a file-based contract test

This design does not choose a vendor, define cache TTLs, settle adjusted-series semantics, specify chart-transform behavior, or implement symbol-detail UI.

## Core Contract

### Provider-neutral market data boundary

- This bead should define the market data service as the sole internal boundary for quote and bar provider interaction.
- Downstream consumers call the market data service or analyst tools rather than provider SDKs, raw provider endpoints, or provider-specific payload helpers.
- Retrieval starts from listing-appropriate hydrated subject context or a listing `SubjectRef`, not from raw ticker strings, venue text, or provider identifiers standing in for canonical market identity.
- Provider adapters normalize provider-specific response shapes, identifiers, rate-limit behavior, and availability quirks into stable internal market records before those records reach downstream consumers.
- The provider-neutral contract should preserve the market-data fields downstream systems actually need: `as_of`, `delay_class`, `currency`, and `source_id` for quote and bar retrieval, plus `adjustment_basis` whenever a bar response has already crossed an adjustment boundary.
- Provider-specific identifiers, entitlement rules, exchange-code quirks, and upstream transport details remain hidden behind the provider abstraction boundary.
- Corporate actions remain part of the market data service domain, but this bead only establishes that provider normalization may depend on them; adjusted-series and cache semantics are deferred to `P1.1b`.

### Quote retrieval responsibilities

- Quote retrieval should own the latest listing-oriented market snapshot for a tradable subject.
- The normalized quote contract should cover the price-first facts needed by downstream consumers: latest price, absolute move, percentage move, freshness or session state, `as_of`, `delay_class`, `currency`, and `source_id`.
- Quote retrieval is intentionally lightweight and snapshot-oriented. It should not be overloaded to answer historical range questions, adjusted-series questions, or comparison normalization that belong to bar and later series work.
- When the hydrated subject bundle also carries issuer context, quote retrieval still resolves the active market snapshot from listing context rather than treating issuer identity as sufficient on its own.
- Provider failures, stale data, or missing market coverage should surface as normalized market-data availability outcomes rather than raw provider error payloads leaking to callers.

### Bar retrieval responsibilities

- Bar retrieval should own ordered intraday and historical OHLCV series for a listing-oriented subject across a requested range and interval.
- The normalized bar contract should expose enough metadata for deterministic downstream use: requested subject identity, range, interval, `as_of`, `delay_class`, `currency`, `source_id`, and `adjustment_basis`.
- Bar retrieval owns provider normalization for ordered timestamps, venue-sensitive session interpretation, and basic corporate-action-aware bar shaping needed to produce one stable internal series shape.
- This bead does not define which adjustment policies are available to users or how cache keys are formed; it only requires the bar contract to make the resulting adjustment basis explicit whenever bars are served.
- Comparison charts, adjusted-series APIs, and snapshot-safe transform rules consume this bar contract later rather than bypassing it with provider-specific chart fetches.

### Boundary and downstream consumers

- This bead should define the provider-neutral market data boundary and the split between quote retrieval and bar retrieval responsibilities.
- It should not define vendor selection, failover policy, cache policy, adjusted-series options, chart interaction rules, or full symbol-detail composition.
- The contract should make one responsibility rule explicit: quote retrieval serves current market snapshot reads, while bar retrieval serves ordered time-series reads, and downstream systems should not infer that one can silently substitute for the other.
- The contract should also make one normalization rule explicit: downstream consumers depend on stable market-data fields and canonical subject identity, not on provider payload shape or provider-specific identifiers.

## Downstream Consumer Matrix

### Adjusted series query and caching surface (`P1.1b`)

- `P1.1b` depends on this bead for the provider-neutral quote and bar boundary, the normalized market metadata fields, and the explicit split between snapshot reads and ordered time-series retrieval before it defines adjustment and caching behavior.

### Symbol detail surfaces (`P1.3`)

- `P1.3` depends on this bead for a stable quote snapshot contract and a reusable bar retrieval boundary so overview, financials, earnings, and later chart modules do not embed provider-specific market fetch logic.

### Pre-resolve router and budget policy (`P2.2`)

- `P2.2` depends on this bead for the distinction between lightweight quote reads and heavier historical-bar reads so routing and budget policy can choose the right market-data cost class without guessing from provider names or ticker text.

### Scale hardening (`P6.5`)

- `P6.5` depends on this bead for a provider-neutral market-data seam with explicit freshness and source metadata so bottleneck audits, caching, and hardening work optimize the boundary rather than coupling consumers to one upstream vendor.

## Normative File Changes

### `spec/finance_research_spec.md`

- Expand `### 6.2 Market data service` with a quote-and-bar provider abstraction subsection that defines provider normalization, listing-oriented retrieval, normalized quote responsibilities, normalized bar responsibilities, and the boundary between this bead and later adjusted-series or cache work.
- Add a downstream consumer subsection that names `P1.1b`, `P1.3`, `P2.2`, and `P6.5`.

### `tests/contracts/test_quote_bar_provider_abstraction_contract.py`

- Add a file-based contract test that asserts the narrative spec contains the provider-neutral boundary, quote-responsibility, bar-responsibility, and downstream-consumer wording anchors.

## Acceptance Mapping

- The provider-neutral market-data boundary and normalization rule satisfy the acceptance around provider abstraction.
- The quote-responsibility section satisfies the acceptance around quote retrieval responsibilities.
- The bar-responsibility section plus downstream consumer matrix satisfy the acceptance around bar retrieval responsibilities and unblock the named follow-on beads.
