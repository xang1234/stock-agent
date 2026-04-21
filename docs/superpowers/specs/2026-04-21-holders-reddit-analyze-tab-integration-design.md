# Holders Reddit And Analyze Tab Integration Design

## Goal

Define how the `holders` section, Reddit-like or news-style signals entry points, and `Analyze` launch behavior fit into symbol detail without blurring the boundary between deterministic subject tabs and artifact-driven research flows.

## Scope

This design covers:

- the role of the `holders` section inside symbol detail
- how Reddit-like or news-style entry points fit under the existing `signals` route bucket
- how symbol detail launches top-level `Analyze`
- the distinction between symbol-detail-owned sections and shared artifact workflows
- downstream consumer expectations for `P4.2`, `P4.3`, and `P4.6`
- a narrative spec update plus a file-based contract test

This design does not define holders table contents in detail, final social-block rendering behavior, Analyze template internals, or add-to-chat import mechanics.

## Core Contract

### Holders, signals, and Analyze entry boundaries

- `holders` should remain the deterministic symbol-detail section for institutional and insider holder views tied to the selected subject.
- `holders` should compose structured holder outputs from the fundamentals service and remain distinct from portfolio overlays, watchlist state, and user-owned monitoring context.
- `signals` should remain the symbol-detail section for Reddit-like community views, news pulse, and future alt-data entry points; this bead should not replace that route bucket with a source-specific `reddit` shell contract.
- Reddit-like or news-specialized content inside `signals` should compose evidence-backed blocks, claim clusters, evidence bundles, and trend-style renderers rather than raw social-text panes or provider-specific mini-pages.
- `Analyze` should remain a top-level workspace rather than a durable nested symbol-detail section.
- Symbol detail should launch `Analyze` with carried `SubjectRef` context or an explicit analyze intent, but resulting artifacts should live on the shared snapshot and block plane rather than inside a persistent symbol-detail tab.

### Navigation and handoff rules

- Entering `holders` or `signals` from symbol detail preserves subject context inside the same nested-route family and subject-detail shell.
- Launching `Analyze` from symbol detail is a workspace transition that still preserves carried subject context and does not reinterpret the subject from raw ticker text.
- The handoff from symbol detail into `Analyze` should stay explicit so later shared-artifact and replay flows can point to durable snapshot-backed artifacts instead of scraped UI state.
- This bead should not redefine the core deterministic ownership of `overview`, `financials`, or `earnings`; it layers adjacent sections and launch points on top of that contract.

## Downstream Consumer Matrix

### Analyze template system (`P4.2`)

- `P4.2` depends on explicit handoff from symbol detail into top-level `Analyze` with carried subject context so template and saved-workflow work can distinguish launch context from tab ownership.

### Shared artifact flow (`P4.3`)

- `P4.3` depends on `Analyze` entry from symbol detail producing artifact and snapshot boundaries outside the symbol-detail shell so add-to-chat or replay flows import a sealed artifact instead of scraping tab state.

### Specialized social and news blocks (`P4.6`)

- `P4.6` depends on Reddit-like entry living under `signals` and composing shared evidence-backed blocks so specialized social or news views do not redefine the symbol shell or bypass the block registry.

## Normative File Changes

### `spec/finance_research_spec.md`

- Expand the symbol-detail product surface with subsections that define `holders` ownership, `signals` placement for Reddit-like entry points, `Analyze` launch behavior, and downstream consumer notes.

### `tests/contracts/test_holders_reddit_analyze_tab_integration_contract.py`

- Add a file-based contract test that asserts the narrative spec contains the required holders, signals, Analyze-handoff, and downstream-consumer wording anchors.

## Acceptance Mapping

- The holders, signals, and Analyze boundary section satisfies the acceptance around entry-point behavior for holders, Reddit-like views, and Analyze.
- The navigation and handoff section satisfies the acceptance around symbol-detail fit and explicit cross-surface behavior.
- The downstream consumer matrix satisfies the acceptance around `P4.2`, `P4.3`, and `P4.6`.
