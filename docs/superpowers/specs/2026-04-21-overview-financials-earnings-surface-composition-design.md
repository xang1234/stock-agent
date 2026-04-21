# Overview Financials And Earnings Surface Composition Design

## Goal

Define the deterministic composition contract for the `overview`, `financials`, and `earnings` tabs inside symbol detail so those core tabs reuse existing market, fundamentals, and event contracts without absorbing later interpretive surfaces.

## Scope

This design covers:

- the responsibilities of the `overview`, `financials`, and `earnings` tabs inside the subject-detail shell
- the shared service dependencies those tabs compose from
- local navigation and handoff rules between the tabs and adjacent symbol-detail work
- downstream consumer expectations for `P1.3b`, `P4.2`, and `P4.4`
- a narrative spec update plus a file-based contract test

This design does not define holders, Reddit or signals content, Analyze workflow behavior, final visual polish, or narrative evidence experiences.

## Core Contract

### Tab responsibilities

- `overview` should own the deterministic single-subject summary that extends the thin quote landing state into a durable core tab.
- `overview` should compose listing-aware quote context, company profile context, key stats, and a limited performance or context summary, but it should not become a second home for full statement tables, holders, or interpretive evidence flows.
- `financials` should own normalized statement tables, statement-linked trend views, and segment-aware financial breakdowns for the selected subject.
- `financials` should compose normalized statement outputs plus the aggregation layer for key stats and segment facts rather than rebuilding fundamentals logic from provider-specific payloads.
- `earnings` should own deterministic earnings chronology, expectation-versus-result views, and consensus summaries for the selected subject.
- `earnings` should compose earnings-release events, EPS surprise history, analyst consensus, and price-target context without turning transcript reading, news clustering, or freeform commentary into tab-owned responsibilities.

### Shared dependencies and navigation

- All three tabs live inside the same subject-detail shell and share the same subject header context, nested-route navigation model, and public-route assumptions already established for symbol detail.
- The core tab composition should depend on hydrated subject identity, market quote and series services, fundamentals profile and statement services, aggregation outputs, and structured earnings events through backend contracts rather than direct provider payloads or chat-style tool loops.
- Moving between `overview`, `financials`, and `earnings` should preserve subject context and shell chrome; it is a local section transition, not a new top-level workspace or a fresh subject-resolution flow.
- The tabs may link to one another through stable section destinations, but they should not collapse into one scrolling page or duplicate ownership of the same deterministic modules.
- Holders, signals or Reddit, and Analyze entry points remain outside this bead and should layer onto the subject-detail shell after the core tab responsibilities are fixed.

## Downstream Consumer Matrix

### Holders, Reddit, and Analyze tab integration (`P1.3b`)

- `P1.3b` depends on `overview`, `financials`, and `earnings` having stable deterministic responsibilities so later holders, Reddit, and Analyze entry points can attach without redefining the core symbol-detail tabs.

### Analyze template system (`P4.2`)

- `P4.2` depends on the explicit boundary between deterministic symbol tabs and later artifact-driven analysis so Analyze can launch from symbol detail without inheriting ownership of overview, financials, or earnings composition.

### Home feed (`P4.4`)

- `P4.4` depends on stable symbol-tab destinations and shared subject context so findings and summaries can deep-link into the right deterministic surface instead of inventing custom readouts per card.

## Normative File Changes

### `spec/finance_research_spec.md`

- Expand the symbol-detail product surface with subsections that define the three core tab responsibilities, their shared service dependencies, and downstream consumer notes.

### `tests/contracts/test_overview_financials_earnings_surface_composition_contract.py`

- Add a file-based contract test that asserts the narrative spec contains the required tab-responsibility, dependency, navigation, and downstream-consumer wording anchors.

## Acceptance Mapping

- The tab-responsibility section satisfies the acceptance around documenting overview, financials, and earnings ownership separately.
- The shared-dependency and navigation section satisfies the acceptance around shared service dependencies and local section expectations.
- The downstream consumer matrix satisfies the acceptance around `P1.3b`, `P4.2`, and `P4.4`.
