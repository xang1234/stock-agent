# Manual Watchlist Management Baseline Design

## Goal

Define the first manual watchlist capability as a single saved-subject baseline with thin quote row hydration, so later portfolio, dynamic-list, and automation work extends one understandable list model rather than inventing a second one.

## Scope

This design covers:

- the single implicit manual watchlist baseline and its membership-focused CRUD floor
- the rule that watchlist membership persists canonical subject identity rather than raw ticker strings or stored quote payloads
- thin quote-on-read row hydration for saved subjects
- inline auth-resume add behavior from public subject routes
- the relation between manual watchlist membership and the existing search-to-subject and symbol-entry contracts
- downstream consumer expectations for portfolio basics, dynamic watchlists, and automation or agent flows
- a narrative spec update plus a file-based contract test

This design does not define multiple manual lists, list rename or delete, list sharing, holdings data model, derived list modes, overlay behavior, or autonomous list mutation.

## Core Contract

### Manual watchlist baseline and membership model

- This bead should define one implicit default manual watchlist as the baseline saved-subject model.
- The baseline CRUD floor is membership-only: view current members, add a resolved subject, and remove a saved subject.
- This bead should not require create-list, rename-list, delete-list, sharing, reordering, or multiple manual lists.
- The persisted membership unit is canonical subject identity, not raw ticker strings and not stored quote payloads.
- Add-to-watchlist consumes the existing shell-owned search and subject-resolution contract rather than inventing a separate lookup path.
- Membership is idempotent at the subject level: adding the same canonical subject twice does not create duplicates.
- This baseline manual mode exists so later `screen`, `agent`, `theme`, and `portfolio` list modes extend one understandable membership model instead of replacing it.
- The persistence rule should be explicit: the manual watchlist stores durable canonical subject identity and derives display or market context from later hydration rather than treating quote data as part of the membership record.

### Quote row hydration and add flow

- The manual watchlist persists only canonical subject membership. Quote data is not part of the membership record.
- When the watchlist is viewed, each row hydrates a thin quote-on-read view from the saved canonical subject identity.
- The row hydration contract should stay lightweight: subject display identity, listing-sensitive symbol context when applicable, latest price, absolute and percentage move, and freshness or session state.
- Deeper quote snapshots, profile modules, or multi-card symbol detail content remain outside the watchlist baseline.
- Quote hydration should reuse the same listing-oriented market identity rule established by the early symbol-entry bead rather than inventing a watchlist-specific quote identity model.
- Add-to-watchlist from public symbol routes should use the existing inline auth interrupt contract. If the user is unauthenticated, the system preserves the current route and pending resolved subject, then resumes the add after sign-in.
- The add flow should operate on a resolved canonical subject, not on raw search text or a best-guess ticker string.
- This bead should also make the removal rule explicit: removing a member affects watchlist membership only; it does not mutate the underlying subject, quote, or later portfolio overlays.

### Boundary and downstream consumers

- This bead should define the implicit single manual watchlist, subject-level membership CRUD, refresh-on-read quote row hydration, and inline auth-resume add behavior tied to resolved subjects.
- It should not define multi-list management, list sharing, portfolio holdings, derived list modes, overlay semantics, or autonomous list mutation. Those belong to later `P1.5`, `P4.7`, and agent or automation work.
- The contract should make one hydration rule explicit: quote rows are hydrated on read from saved canonical subject identity, and stale or unavailable market data affects row display only, not membership persistence.
- It should also make one mutation rule explicit: add or remove changes watchlist membership only; it does not alter the underlying subject, market snapshot, or later portfolio overlay state.

## Downstream Consumer Matrix

### Portfolio and watchlist basics (`P1.5`)

- `P1.5` depends on this bead for the simple saved-subject baseline and quote row behavior that later portfolio and holdings surfaces build on.

### Dynamic watchlists and portfolio overlays (`P4.7`)

- `P4.7` depends on this bead for the manual list baseline that later dynamic watchlist derivation modes and overlay behavior extend rather than replace.

### Agent CRUD and scheduling (`P5.1`)

- `P5.1` depends on this bead for a simple, user-owned list object and membership model that automation or agent creation flows may later target without inventing a separate subject collection system.

## Normative File Changes

### `spec/finance_research_spec.md`

- Add a narrative subsection that defines the implicit manual watchlist baseline, membership-only CRUD floor, quote-on-read row hydration, and inline auth-resume add behavior.
- Add downstream consumer notes for portfolio basics, dynamic watchlists, and automation or agent flows.

### `tests/contracts/test_manual_watchlist_management_baseline_contract.py`

- Add a file-based contract test that asserts the narrative spec contains the single-list baseline, membership CRUD floor, quote-on-read row hydration, auth-resume add rule, and downstream-consumer wording anchors.

## Acceptance Mapping

- The single-list baseline and membership CRUD floor satisfy the acceptance around watchlist CRUD scope.
- Quote-on-read row hydration and listing-oriented row identity satisfy the acceptance around quote hydration assumptions.
- The add-flow and persistence rules satisfy the acceptance around relation to subject resolution while keeping later list and automation work layered on top of the same baseline.
