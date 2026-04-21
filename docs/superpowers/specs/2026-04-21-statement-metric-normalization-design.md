# Statement And Metric Normalization Design

## Goal

Define how reported statements and canonical metrics normalize into shared fact shapes so deterministic surfaces and later aggregation layers consume one explicit fundamentals contract instead of ad hoc table-specific payloads.

## Scope

This design covers:

- the statement-normalization layer inside the fundamentals service
- metric ownership rules for definition objects versus observed values
- the relation between normalized statement outputs and the canonical `Fact` and `Computation` objects
- issuer-oriented subject rules and explicit statement basis handling
- downstream consumer expectations for `P1.2b`, `P1.3`, `P2.2`, `P3.5`, and `P6.2`
- a narrative spec update plus a file-based contract test

This design does not define segment aggregations, analyst consensus, comparison-ready derived stats, extraction algorithms, or non-US accounting mappings in detail.

## Core Contract

### Statement normalization boundary

- Statement normalization should define the fundamentals-service layer that turns filing-backed or vendor-backed statement inputs into canonical value objects keyed by metric definitions.
- Statement reads begin from issuer-appropriate subject context rather than listing identity or ticker-only lookup.
- The service should normalize the three core statement families explicitly: `income`, `balance`, and `cashflow`.
- Statement basis remains explicit at the query and output boundary: `as_reported` and `as_restated` are different normalization modes and must not be silently merged.
- Period selection, fiscal labels, scale normalization, and unit normalization are part of the statement-normalization contract rather than caller-specific cleanup work.

### Metric ownership and canonical value relation

- `Metric` remains the canonical definition object for what can be measured, how a value is interpreted, and which source class a normalized value belongs to.
- Fundamentals service owns the mapping from normalized statement lines into canonical metric definitions, but it does not turn `Metric` into a mutable value store.
- Displayed statement values should resolve to `Fact` rows when the value is directly observed or promoted as truth, and to `Computation` rows when the value is deterministically derived from structured inputs.
- Statement normalization must not introduce a second truth layer made of UI-only statement cells or provider-specific blobs that bypass `Fact` and `Computation`.
- When source material is incomplete, conflicting, or pending promotion, the service should preserve coverage and verification state through canonical value objects rather than inventing complete normalized tables.

### Boundary and downstream consumers

- This bead should define normalization scope, metric ownership, and the relation between normalized statement outputs and canonical truth objects.
- It should not define segment aggregations, peer comparison payloads, consensus models, or specialized symbol-surface composition.
- The contract should make one ownership rule explicit: fundamentals normalization owns metric mapping and statement shaping, while the evidence plane continues to own canonical values, provenance, supersession, and verification state.
- The contract should also make one basis rule explicit: `as_reported` and `as_restated` are distinct normalization requests and downstream consumers must treat them as explicit inputs rather than display toggles over one cached table.

## Downstream Consumer Matrix

### Later aggregation layer (`P1.2b`)

- `P1.2b` consumes normalized issuer statement facts and canonical metrics so later aggregation work builds on one shared value layer without redefining statement normalization.

### Symbol detail surfaces (`P1.3`)

- `P1.3` depends on normalized statement outputs carrying explicit basis, period, and coverage semantics so overview, financials, and earnings tabs can render trustworthy tables and charts.

### Pre-resolve router and budget policy (`P2.2`)

- `P2.2` depends on the issuer-oriented normalization boundary so routing can distinguish fundamentals reads from market-data reads before the tool loop starts.

### Promotion rules for candidate facts (`P3.5`)

- `P3.5` depends on the rule that normalized statement values become `Fact` or `Computation` objects rather than a separate fundamentals-only truth store, so promotion and supersession work target the canonical value plane.

### Non US identity data and coverage gaps (`P6.2`)

- `P6.2` depends on explicit metric ownership, basis handling, and issuer-oriented normalization rules so later international work can extend accounting mappings without weakening the canonical value contract.

## Normative File Changes

### `spec/finance_research_spec.md`

- Expand the fundamentals section with a statement-and-metric normalization subsection that defines issuer-oriented statement normalization, explicit statement basis, metric ownership, and the relation to canonical `Fact` and `Computation` objects.
- Add a downstream consumer subsection that names `P1.2b`, `P1.3`, `P2.2`, `P3.5`, and `P6.2`.

### `tests/contracts/test_statement_metric_normalization_contract.py`

- Add a file-based contract test that asserts the narrative spec contains the normalization-boundary, metric-ownership, canonical-value, and downstream-consumer wording anchors.

## Acceptance Mapping

- The normalization-boundary section satisfies the acceptance around normalization scope.
- The metric-ownership section satisfies the acceptance around metric ownership.
- The canonical-value relation plus downstream consumer matrix satisfy the acceptance around relation to canonical facts and unblock the named follow-on beads.
