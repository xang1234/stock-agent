# Holdings Model And Overlay Inputs Design

## Goal

Define the lightweight holdings model, its base-currency assumptions, and the overlay inputs it contributes to later research surfaces, without drifting into brokerage, transaction-ledger, or portfolio-UI behavior.

## Scope

This design covers:

- the scope boundary for portfolio holdings inside the product
- the meaning of `Portfolio.base_currency`
- the intended identity and semantics of `PortfolioHolding`
- the minimum overlay inputs later surfaces may consume from holdings
- the separation between holdings, manual watchlists, and later UI behavior
- downstream consumer expectations for `P1.5b` and `P4.7`
- a narrative spec update plus a file-based contract test

This design does not define brokerage execution, cash balances, lot accounting, fee tracking, transaction history, tax logic, FX trade capture, or the actual UI behaviors of portfolio and watchlist surfaces.

## Core Contract

### Holdings scope and base-currency assumptions

- Portfolio support should remain lightweight research context: it tracks held exposure for overlays and monitoring, not brokerage execution, order management, tax lots, cash ledgers, or settlement workflows.
- Watchlists should continue to model saved-subject membership, while portfolios model held exposure; those are related but distinct user-owned concepts.
- A `Portfolio` should own one explicit `base_currency` that defines the reporting currency for holding cost assumptions and later overlay totals.
- `base_currency` should be treated as a reporting and comparison assumption, not proof that the underlying listing trades in that currency and not a full FX accounting system.
- A `PortfolioHolding` should persist canonical market identity plus quantity, optional cost basis, and open or closed timestamps rather than raw ticker strings, provider payloads, or transaction histories.
- The holdings model should stay intentionally thin: no lot-by-lot reconstruction, realized tax accounting, fee capture, margin state, or order history.

### Overlay input boundary

- Holdings should contribute reusable overlay inputs to later surfaces instead of UI-owned ad hoc calculations.
- The minimum overlay input contract should be subject-keyed and portfolio-aware: held-state, contributing `portfolio_id`, quantity, optional cost basis context, and a base-currency label for any derived valuation or gain or loss display.
- Overlay inputs should be read models derived from holdings plus market hydration, not new canonical subject identities and not stored UI payloads.
- If multiple portfolios hold the same subject with different base currencies, this bead should keep those contributions distinct rather than silently netting them through an implicit FX layer.
- Holding a subject should not implicitly add it to a manual watchlist, and saving a subject to a watchlist should not create a holding.

### Boundary and downstream consumers

- This bead should define the lightweight holdings scope, the `base_currency` reporting rule, and the overlay-input boundary only.
- It should not define portfolio pages, quote-card behavior, symbol-level overlay rendering, cross-list merge rules, or dynamic watchlist derivation behavior. Those belong to `P1.5b` and `P4.7`.
- The contract should remain compatible with the existing listing-oriented market identity and manual watchlist baseline instead of creating a second subject or quote model for holdings.

## Downstream Consumer Matrix

### Portfolio and watchlist surface behaviors (`P1.5b`)

- `P1.5b` depends on the lightweight holdings scope and explicit `base_currency` assumption so first-surface behaviors can render held-state and cost context without inventing brokerage rules.

### Dynamic watchlists and portfolio overlays (`P4.7`)

- `P4.7` depends on holdings producing reusable overlay inputs rather than UI-owned ad hoc calculations so later overlay layers can merge portfolio context with watchlists, themes, screens, and subject views consistently.

## Normative File Changes

### `spec/finance_research_spec.md`

- Refine `3.6` so portfolio is explicitly lightweight overlay-context tracking rather than execution semantics.
- Add a product-surface subsection for holdings scope and downstream consumers.
- Add a research-subject subsection for `Portfolio`, `PortfolioHolding`, `base_currency`, and overlay-input assumptions.

### `tests/contracts/test_holdings_model_overlay_inputs_contract.py`

- Add a file-based contract test that asserts the narrative spec contains the holdings scope, `base_currency` assumptions, overlay-input boundary, and downstream-consumer wording anchors.

## Acceptance Mapping

- The lightweight holdings scope and explicit non-goals satisfy the acceptance around holdings scope.
- The `base_currency` rules satisfy the acceptance around base-currency assumptions.
- The overlay-input boundary and downstream matrix satisfy the acceptance around reusable overlay inputs for `P1.5b` and `P4.7`.
