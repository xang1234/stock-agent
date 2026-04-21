# Stats Segment And Consensus Aggregations Design

## Goal

Define the fundamentals aggregation layer that turns normalized statement facts, segment disclosures, analyst-consensus feeds, and deterministic derived stats into reusable aggregate read models for deterministic product surfaces.

## Scope

This design covers:

- the service-level aggregation layer inside the fundamentals service
- separate aggregate families for key stats and derived ratios, segment facts, analyst consensus, and comparison-ready derived outputs
- ownership boundaries between canonical `Fact` or `Computation` rows and service-level aggregation read models
- explicit freshness, basis, coverage, and warning semantics for aggregation outputs
- downstream consumer expectations for `P1.3`, `P2.2`, `P4.6`, `P6.1`, and `P6.2`
- a narrative spec update plus a file-based contract test

This design does not define peer-ranking algorithms, final symbol-detail composition, evidence-promotion policy, segment-extraction internals, or international-accounting mappings in detail.

## Core Contract

### Aggregation boundary

- The fundamentals aggregation layer sits above normalized statement facts and canonical metrics and produces reusable read models for deterministic consumers.
- Aggregation outputs are service-level views, not replacements for canonical `Fact` or `Computation` rows, and they keep derivation inputs, freshness, and coverage assumptions explicit.
- The aggregation layer may read canonical facts, computations, and provider-backed consensus or segment inputs, but provenance, supersession, and truth-promotion state remain owned by the canonical value plane.
- Raw normalized statements remain the input boundary for consolidation and basis handling; aggregation work does not redefine statement normalization or hide the difference between raw statement rows and aggregated views.

### Aggregation families

- Key stats and derived ratios should combine normalized fundamentals, market context, and deterministic computations into reusable outputs with explicit basis, period, and `as_of` assumptions.
- Segment facts should remain distinct from consolidated statement outputs: they should preserve segment axis, segment definitions, period context, and coverage warnings instead of flattening segment disclosures into issuer-level statement tables.
- Analyst consensus should remain distinct from both reported statements and promoted evidence facts: rating distributions, price-target summaries, analyst counts, and coverage warnings are service-level aggregates with explicit `as_of` semantics.
- Comparison-ready derived outputs may package reusable aggregate slices for peer views or ranking-style surfaces, but they should not become an opaque cache of UI-specific payloads.

### Coverage and warning rules

- When aggregation inputs are incomplete, stale, or inconsistent, the service should surface warnings and partial-coverage metadata instead of fabricating complete comparisons or silently filling gaps.
- Consumers should be able to tell whether an output came from statement-backed values, market context, consensus inputs, or segment disclosures without reverse-engineering UI behavior.

## Downstream Consumer Matrix

### Symbol detail surfaces (`P1.3`)

- `P1.3` depends on separate stats, segment, and consensus aggregation families so overview, financials, and earnings modules can reuse deterministic read models instead of rebuilding UI-specific payloads from raw statements.

### Pre-resolve router and budget policy (`P2.2`)

- `P2.2` depends on the distinction between normalized statement reads and aggregation-layer reads so routing can classify heavier fundamentals requests before the tool loop starts.

### Specialized social and news blocks (`P4.6`)

- `P4.6` depends on reusable key stats and consensus outputs so narrative product blocks can cite stable aggregate envelopes without embedding ad hoc ratio or target-calculation logic.

### Segment extraction refinement (`P6.1`)

- `P6.1` depends on segment aggregates preserving axis, definition, and coverage-warning semantics so harder extraction cases can evolve without changing the consumer-facing aggregation contract.

### Non US identity data and coverage gaps (`P6.2`)

- `P6.2` depends on aggregation outputs keeping basis, freshness, and coverage assumptions explicit so later international expansion can widen issuer and provider coverage without pretending the aggregates are uniformly comparable.

## Normative File Changes

### `spec/finance_research_spec.md`

- Expand the fundamentals section with aggregation subsections that define the aggregation-layer boundary, the separate output families, and the downstream consumer rules.

### `tests/contracts/test_stats_segment_consensus_aggregations_contract.py`

- Add a file-based contract test that asserts the narrative spec contains the aggregation-boundary, family-separation, ownership, warning, and downstream-consumer wording anchors.

## Acceptance Mapping

- The aggregation-boundary section satisfies the acceptance around documenting aggregate families separately from raw statements.
- The family-separation bullets satisfy the acceptance around key stats, segment facts, analyst consensus, and related comparison-ready outputs.
- The downstream consumer matrix satisfies the acceptance around `P1.3`, `P2.2`, `P4.6`, `P6.1`, and `P6.2`.
