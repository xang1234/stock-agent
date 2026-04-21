# Portfolio And Watchlist Surface Behaviors Design

## Goal

Define the first portfolio and watchlist surface behaviors that sit on top of the manual baseline and holdings model, so list rows, held-state context, and subject-view augmentation follow one stable contract before dynamic overlays arrive.

## Scope

This design covers:

- the first shared row behavior for manual watchlists and portfolio-held surfaces
- how holdings context layers onto the existing thin quote hydration contract
- how watchlist and held-state context appears when entering subject views
- the separation between shared quote hydration and user-owned overlay state
- downstream consumer expectations for `P4.7` and `P6.4`
- a narrative spec update plus a file-based contract test

This design does not define dynamic watchlist derivation modes, theme or screen merge logic, export entitlement policy, dense portfolio analytics, or a finished portfolio product surface.

## Core Contract

### Shared quote hydration and row behavior

- Manual watchlist and portfolio-held surfaces should reuse the same thin quote-on-read row hydration contract rather than inventing separate quote-fetch behavior for held subjects.
- Portfolio-held rows should layer held-state context, quantity, and optional cost-basis context on top of that shared quote row skeleton.
- The first surface behavior should stay intentionally light: no portfolio analytics dashboard, no brokerage position card, and no private quote model distinct from symbol entry.
- If a subject is both watchlisted and held, the surface should keep both states visible rather than collapsing one concept into the other.

### Relation to subject views

- Selecting a row from either a watchlist or portfolio-held surface should enter the same symbol-detail route keyed by canonical subject identity.
- Entered subject views may show lightweight saved-state and held-state context plus adjacent actions, but that context should augment the existing quote snapshot and subject modules rather than creating a portfolio-specific subject shell.
- Watchlist and holdings state remain user-owned overlay context on top of shared subject and market-data contracts.

### Boundary and downstream consumers

- This bead should define first-surface row behavior and subject-view augmentation only.
- It should not define dynamic overlay combination rules, theme/screen/portfolio merge policy, export eligibility policy, or dense performance analytics. Those belong to later `P4.7` and `P6.4` work.

## Downstream Consumer Matrix

### Dynamic watchlists and portfolio overlays (`P4.7`)

- `P4.7` depends on shared quote-row behavior and stable subject-view augmentation so later theme, screen, portfolio, and watchlist combinations can add more context without rewriting the base surfaces.

### Export and share policy (`P6.4`)

- `P6.4` depends on user-owned watchlist and holdings context staying visually and semantically distinct from canonical quote and subject content so later export or share rules can reason about what private overlay state may travel with a shared artifact.

## Normative File Changes

### `spec/finance_research_spec.md`

- Add first-surface portfolio and watchlist behavior subsections after the holdings-model contract.
- Make shared quote-row behavior, dual watchlist-plus-holding visibility, and subject-view augmentation explicit.
- Add downstream consumer notes for `P4.7` and `P6.4`.

### `tests/contracts/test_portfolio_watchlist_surface_behaviors_contract.py`

- Add a file-based contract test that asserts the narrative spec contains the first-surface row behavior, subject-view augmentation, and downstream-consumer wording anchors.

## Acceptance Mapping

- The shared row and quote-hydration rules satisfy the acceptance around relation to quote hydration.
- The subject-view augmentation rules satisfy the acceptance around relation to subject views.
- The downstream matrix satisfies the acceptance around future overlay and share-policy consumers.
