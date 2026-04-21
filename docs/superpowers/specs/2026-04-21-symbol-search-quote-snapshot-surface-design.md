# Symbol Search And Quote Snapshot Surface Design

## Goal

Define the first shared symbol-search entry and the thin symbol-detail landing state that proves shell routing, subject resolution, and quote snapshot retrieval before fuller symbol-detail and watchlist surfaces exist.

## Scope

This design covers:

- the shell-owned symbol-search entry and its reusable handoff into entered symbol detail
- the navigation outcome from search result to the initial quote snapshot landing state
- the minimum required content for the first quote snapshot inside symbol detail
- the rule that profile or issuer-summary content is allowed as a best-effort companion but does not block the landing state
- retrieval and ownership rules for using hydrated subject context to load the first market snapshot
- downstream consumer expectations for manual watchlists, portfolio basics, and later symbol overview work
- a narrative spec update plus a file-based contract test

This design does not define search ranking UI, manual watchlist CRUD, holdings data model, overlay behavior, or the finished symbol overview composition.

## Core Contract

### Search entry and navigation outcome

- This bead should define the first shared symbol-search entry point as shell-owned rather than surface-owned.
- The persistent workspace shell owns the primary symbol search affordance, and later flows such as watchlist add or portfolio add may reuse the same search-to-subject contract instead of redefining search behavior.
- Search entry accepts ticker-like strings, issuer names, and other concise lookup input already covered by the resolver boundary.
- Candidate handling should defer to the existing search-to-subject flow contract: unique deterministic hits may auto-advance, ambiguous hits must stop at explicit candidate choice, and `not_found` ends the flow without subject hydration.
- A successful subject resolution enters symbol detail rather than opening a detached quote page or staying inline in the originating workspace.
- The main canvas swaps into the subject-detail shell while preserving the surrounding workspace shell, consistent with the route skeleton contract.
- This bead should make one outcome rule explicit: the first quote snapshot is the initial landing state of entered symbol detail, not a competing top-level workspace.
- Search entry behavior should stay reusable across shell search, watchlist add flows, and portfolio basics, but this bead does not yet define the full CRUD behavior of those downstream surfaces.

### Thin symbol-detail landing contract

- The first quote snapshot is the initial landing state of entered symbol detail, not the full symbol overview contract.
- This landing state should prove three things only: the selected subject identity is correct, the market-data handoff can retrieve a current quote snapshot for the right listing context, and symbol detail can render a stable first screen inside the shell.
- The required content is a market identity strip plus a price-first quote snapshot. That includes canonical subject display identity, listing-sensitive trading symbol context, latest price, absolute and percentage move, freshness or session state, and a small recent-range or chart hook.
- A light issuer summary or profile companion is allowed on this landing state, but it is best-effort rather than required. The surface should not block the landing state on full profile retrieval.
- The landing contract should make it explicit that quote retrieval is listing-oriented even when the hydrated bundle also carries issuer context.
- The landing state may expose lightweight actions such as enter watchlist flow or continue into deeper symbol sections, but those actions are downstream affordances, not proof that manual watchlist management or full symbol modules are already defined here.
- This bead should not define earnings, holders, filings, peer tables, or a finished overview surface. Those belong to later symbol beads.

### Boundary and downstream consumers

- This bead should define the shared shell search entry, the navigation outcome into entered symbol detail, the thin quote snapshot landing state, and the responsibilities around using hydrated subject context to retrieve the first market snapshot.
- It should not define manual watchlist CRUD, holdings data model, overlay semantics, or the finished symbol overview composition. Those belong to `P0.4b`, `P1.5`, and `P1.3`.
- The contract should make one retrieval rule explicit: the quote snapshot uses listing-appropriate market identity from the hydrated subject bundle, while any issuer summary companion remains best-effort and must not block the landing state.
- It should also make one reuse rule explicit: the shell-owned search contract is reused by later add-to-watchlist and portfolio-entry flows rather than redefined per surface.

## Downstream Consumer Matrix

### Manual watchlist management baseline (`P0.4b`)

- `P0.4b` depends on this bead for the reusable search entry and the selected-subject handoff that manual watchlist actions will sit on top of.

### Portfolio and watchlist basics (`P1.5`)

- `P1.5` depends on this bead for the first quote and subject-entry behavior that portfolio and watchlist basics can reuse before overlays exist.

### Symbol overview shell (`P1.3`)

- `P1.3` depends on this bead for the rule that entered symbol detail has a thin initial landing state before the fuller overview, financials, and earnings composition is defined.

## Normative File Changes

### `spec/finance_research_spec.md`

- Add a narrative subsection that defines the shell-owned symbol-search entry, symbol-detail navigation outcome, quote snapshot minimum, listing-oriented retrieval rule, and best-effort profile companion rule.
- Add downstream consumer notes for manual watchlists, portfolio basics, and later symbol overview work.

### `tests/contracts/test_symbol_search_quote_snapshot_surface_contract.py`

- Add a file-based contract test that asserts the narrative spec contains the shell-entry, symbol-detail landing, quote snapshot minimum, best-effort profile, and downstream-consumer wording anchors.

## Acceptance Mapping

- Shell-owned search entry points and symbol-detail navigation satisfy the acceptance around early symbol search entry behavior.
- The quote snapshot minimum and listing-oriented retrieval rule satisfy the acceptance around first quote snapshot retrieval.
- The reuse and downstream consumer rules satisfy the acceptance around subject hydration responsibilities for manual watchlists and portfolio basics while preserving the later `P1.3` symbol-overview boundary.
