# Canonical Identity Resolver Contract Design

## Goal

Define the deterministic resolver contract that turns user-entered lookup input and provider-origin identity records into canonical issuer, instrument, listing, and subject-reference outputs without silently collapsing ambiguity.

## Scope

This design covers:

- resolver responsibilities for normalization, candidate generation, and canonical output selection
- the accepted input families for user-entered lookup text and provider-origin identity records
- a typed resolution envelope for `resolved`, `ambiguous`, and `not_found` outcomes
- explicit ambiguity-preservation rules and why ticker-only identity is insufficient
- downstream consumer expectations for search-to-subject flow, market data, fundamentals, screener work, and chat routing
- a narrative spec update plus a file-based contract test

This design does not define search ranking UX, interactive disambiguation steps, downstream subject hydration, provider selection, or chat-router policy beyond the resolver contract notes needed to unblock dependent beads.

## Core Contract

### Resolver responsibilities

- The resolver is the deterministic boundary that converts user-entered lookup input and provider-origin identity records into canonical finance identity outputs.
- The resolver owns normalization, candidate generation, canonical reference selection when unambiguous, and explicit ambiguity preservation when multiple canonical targets remain plausible.
- The resolver is distinct from search UI, user disambiguation flow, and downstream subject hydration.
- Every successful resolver path must end in explicit canonical refs rather than ticker strings or raw provider ids standing in for identity.
- The resolver must promote lookup handles into issuer, instrument, listing, or `SubjectRef` outputs that downstream systems can persist and join on safely.

### Typed resolution envelope

- The contract should define a typed resolution envelope rather than an untyped candidate list.
- `resolved` means the resolver can name one canonical target confidently enough for deterministic downstream use.
- `ambiguous` means multiple canonical issuer, instrument, listing, or `SubjectRef` targets remain plausible after normalization and matching, so the resolver must return ranked candidates without silently picking one.
- `not_found` means the resolver could normalize the input but could not map it to a supported canonical target.
- The envelope should carry enough metadata for downstream consumers to know what input was normalized, what identity level was resolved, and whether ambiguity was preserved.

### Inputs, identity levels, and ambiguity rules

- The contract should explicitly cover two input families: user-entered lookup text and provider-origin identity records.
- User-entered lookup text includes ticker-like strings, issuer names, aliases, and other concise finance lookup inputs.
- Provider-origin identity records include external ids and structured provider payload fields such as ticker, exchange, CIK, ISIN, or other identifier-bearing records.
- The resolver must normalize input before matching, but normalization must not erase identity-level distinctions between issuer, instrument, and listing.
- The resolver may start from ticker or alias lookup, but downstream output must promote that lookup into explicit issuer, instrument, listing, or `SubjectRef` candidates.
- Ticker-only identity remains insufficient because the same symbol can map to different listings, venues, or securities, and issuer-level workflows often need a different canonical target than market-data workflows.
- The resolver should expose the ambiguity axis when possible, such as issuer-versus-listing ambiguity or multiple plausible listings for one ticker string.
- Ranked candidates are advisory metadata, not permission to silently collapse ambiguity into one winner.
- `resolved` should include the canonical identity level that was chosen so downstream systems know whether they received issuer, instrument, listing, or already-formed `SubjectRef` output.

## Downstream Consumer Matrix

### Search-to-subject resolution flow (`P0.3b`)

- `P0.3b` depends on the resolver outcome vocabulary it will carry through candidate search, user choice, and downstream subject hydration.
- The search flow may layer interaction on top, but it should not redefine the resolver’s `resolved`, `ambiguous`, and `not_found` contract.

### Market data service (`P1.1`)

- `P1.1` depends on the rule that quote and bar consumers must receive listing-appropriate canonical output rather than ticker strings or issuer-level guesses.

### Fundamentals service (`P1.2`)

- `P1.2` depends on the rule that issuer-backed fundamentals cannot rely on ticker-only identity and must consume issuer-appropriate canonical output or preserved ambiguity.

### Screener surface and saved-screen handoff

- Screener filters and saved-screen handoffs depend on deterministic subject identity shapes even before later hydration flow is applied.

### Pre-resolve router and budget policy (`P2.2`)

- `P2.2` depends on the rule that deterministic pre-resolve routing consumes resolver envelopes rather than asking the model to silently choose among ambiguous identity candidates.

## Normative File Changes

### `spec/finance_research_spec.md`

- Expand the identity and resolver service section with explicit resolver responsibilities, typed envelope outcomes, accepted input families, and ambiguity rules.
- Add downstream consumer notes for search-to-subject flow, market data, fundamentals, screener work, and pre-resolve routing.

### `tests/contracts/test_canonical_identity_resolver_contract.py`

- Add a file-based contract test that asserts the narrative spec contains the required resolver responsibility, envelope, ambiguity, and downstream-consumer wording anchors.

## Acceptance Mapping

- Resolver responsibilities, input families, and typed envelope outcomes satisfy the contract boundary for `stock-agent-h3e.1.3.1`.
- Explicit ambiguity preservation and ticker-is-not-identity notes satisfy the acceptance requirement around ambiguity handling and ticker insufficiency.
- The downstream consumer matrix unblocks `P0.3b`, `P1.1`, `P1.2`, screener saved-screen handoff work, and `P2.2`.
