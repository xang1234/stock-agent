# Adjusted Series Query And Caching Surface Design

## Goal

Define the adjusted-series query surface, cache assumptions, and snapshot-safe series semantics so deterministic market consumers and interactive blocks reuse one stable time-series contract.

## Scope

This design covers:

- the adjusted-series query layer that sits above raw bar retrieval inside the market data service
- explicit basis and normalization semantics for returned market series
- cache assumptions for reusing series results without changing externally visible semantics
- the relation between cached series reuse and sealed snapshot transform rules
- coverage and partial-history expectations for deterministic consumers and interactive blocks
- downstream consumer expectations for `P1.3`, `P2.3`, `P4.6`, `P6.2`, and `P6.5`
- a narrative spec update plus a file-based contract test

This design does not choose cache TTLs, define a concrete cache backend, add new chart block kinds, choose UI defaults, or expand non-market basis terms beyond the market-series contract.

## Core Contract

### Adjusted-series query surface

- This bead should define adjusted-series query as the market-data surface above raw bar retrieval that produces comparison-ready or interactive time series from canonical listing subject input.
- Series queries should bind explicit `subject_refs`, `range`, `interval`, `basis`, and `normalization` before execution, caching, and snapshot binding.
- Market-series basis should remain explicit and limited to the market-data vocabulary already in the contract: `unadjusted`, `split_adjusted`, and `split_and_div_adjusted`.
- The service must not silently mix bases inside one returned series set, one chart artifact, or one comparison response.
- Multi-subject performance responses should share one basis, one normalization, one `as_of`, and one requested range contract even when coverage start differs by subject.
- Series responses should expose the effective coverage window and any partial or unavailable history explicitly rather than backfilling missing periods or implying full coverage where it does not exist.

### Cache assumptions and correctness boundary

- Cache is an internal optimization behind the market data service, not a separate semantic source of truth for charts, symbol tabs, or blocks.
- Cache identity should include the canonical subject set, range, interval, basis, normalization, and freshness boundary used for the series request.
- A cache hit may reuse prior series material only when the request preserves subject membership, basis, normalization, and does not require data newer than the request or snapshot `as_of`.
- Cache hits and misses should return the same observable contract: stable series semantics, explicit `as_of`, preserved basis or `adjustment_basis`, and the same provenance-facing metadata as uncached reads.
- If basis, normalization, peer set, or freshness changes, the system should treat that as a different series request and refresh or recompute rather than mutating a cached answer in place.
- This bead should not define numeric TTLs or store selection. It only defines the semantic boundary cache must preserve.

### Snapshot-safe series semantics

- In-snapshot transforms may reuse cached series only when the requested range or interval is already legal under the sealed snapshot manifest and remains inside `allowed_transforms`.
- Changing basis or normalization is out-of-snapshot behavior even if compatible cached material exists somewhere in storage.
- Series bindings in blocks and symbol surfaces should point to the same explicit series spec that was sealed into the snapshot rather than reconstructing adjustment choices from UI state later.
- Deterministic consumers should treat coverage gaps, partial history, and stale series as explicit output conditions, not as permission to synthesize missing history or silently widen freshness.

### Boundary and downstream consumers

- This bead should define adjusted-series query identity, cache correctness assumptions, and snapshot-safe reuse rules for returned market series.
- It should not define provider abstraction, chart-block implementation details, UI default ranges, warehouse topology, or concrete hardening thresholds.
- The contract should make one semantics rule explicit: basis and normalization are part of series identity, not presentation-only toggles that can be changed without a new series request.
- The contract should also make one cache rule explicit: reuse is allowed only when it preserves the same subject set, basis, normalization, and freshness boundary visible to the caller.

## Downstream Consumer Matrix

### Symbol detail surfaces (`P1.3`)

- `P1.3` depends on explicit basis and coverage semantics so price charts and comparison modules do not silently switch between adjusted and unadjusted histories.

### Block registry and initial block catalog (`P2.3`)

- `P2.3` depends on stable series query identity and in-snapshot cache reuse rules so interactive blocks know which transforms are legal without redefining market semantics per block kind.

### Specialized social and news blocks (`P4.6`)

- `P4.6` depends on the same series semantics and cache contract for trend-style blocks so source-specific renderers reuse shared market rules rather than inventing bespoke chart caching behavior.

### Non US identity data and coverage gaps (`P6.2`)

- `P6.2` depends on explicit basis, coverage-window, and partial-history rules so later international work can surface venue and provider differences without pretending uniform history quality.

### Scale hardening (`P6.5`)

- `P6.5` depends on the declared cache identity and refresh rules so audits and ops work optimize hit rate and storage layout without weakening snapshot correctness.

## Normative File Changes

### `spec/finance_research_spec.md`

- Expand the market-data section with an adjusted-series query and caching subsection that defines explicit series identity, basis semantics, cache correctness rules, and the relation to snapshot-safe transforms.
- Add a downstream consumer subsection that names `P1.3`, `P2.3`, `P4.6`, `P6.2`, and `P6.5`.

### `tests/contracts/test_adjusted_series_query_caching_surface_contract.py`

- Add a file-based contract test that asserts the narrative spec contains the adjusted-series identity, cache-assumption, snapshot-safe reuse, and downstream-consumer wording anchors.

## Acceptance Mapping

- The adjusted-series query surface and explicit basis rules satisfy the acceptance around adjusted-series rules.
- The cache-boundary section satisfies the acceptance around cache assumptions.
- The series-semantics section plus downstream consumer matrix satisfy the acceptance around deterministic and interactive series behavior for the named follow-on beads.
