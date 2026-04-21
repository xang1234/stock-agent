# Screener UI Flow And Saved Screen Handoff Design

## Goal

Define the first screener surface flow and saved-screen handoff contract so the workspace, saved-screen resume behavior, and subject or list handoffs stay deterministic on top of the existing screener service boundary.

## Scope

This design covers:

- the first workspace-level screener flow for query controls and result rows
- public browse versus session-gated saved-screen behavior
- how saved screens are resumed back into the screener surface
- how screener result rows hand off into symbol-detail entry
- how screener state hands off into later list and theme workflows
- downstream consumer expectations for `P4.1` and `P4.7`
- a narrative spec update plus a file-based contract test

This design does not define screener ranking logic, query semantics, dynamic watchlist derivation rules, theme membership inference, bulk actions, or final visual widget layout.

## Core Contract

### Screener workspace flow

- `Screener` should remain a primary workspace for building, refining, and viewing one active screen definition plus its current result set inside the persistent shell.
- The surface should keep query controls and result rows in one workspace flow rather than splitting query editing, results, and saved screens into separate primary surfaces.
- Public screener browsing may execute and refine unsaved screens without requiring a session, reusing the public-route and backend-owned screener query contract already defined elsewhere.

### Saved-screen behavior

- Saving a screen, opening a user-owned saved screen, or mutating saved-screen metadata should require a session and use the existing in-shell auth interrupt and resume behavior rather than leaving the screener route family.
- Saving a screen should persist the replayable screen definition, user-owned screen record, and ordering semantics rather than a frozen cache of row payloads or a detached export artifact.
- Reopening a saved screen should restore the screener workspace with the saved screen definition as the active query context and rehydrate results through the screener service rather than replaying stale table rows from client storage.

### Subject and list handoff rules

- Selecting a screener result row should hand off canonical subject identity into the existing symbol-detail entry flow rather than opening a screener-specific quote view or embedding a full subject workspace inline.
- Handoffs from screener into later list or theme workflows should carry explicit `screen` context or the saved query definition as the source reference so downstream derivation and theme flows can explain where a generated universe came from.
- This bead should not define dynamic watchlist derivation rules, theme membership inference, or bulk portfolio-overlay behavior; it only defines the screener surface flow and saved-screen handoff seam.

## Downstream Consumer Matrix

### Themes and macro subjects (`P4.1`)

- `P4.1` depends on screen-to-theme or derived-universe handoffs carrying explicit screen source context so later theme workflows can distinguish screen-derived membership inputs from manual or inferred membership.

### Dynamic watchlists and portfolio overlays (`P4.7`)

- `P4.7` depends on saved screens remaining replayable user-owned screen definitions with explicit source handoff so later dynamic watchlists can regenerate and explain screen-derived lists without scraping transient screener UI state.

## Normative File Changes

### `spec/finance_research_spec.md`

- Add product-surface subsections after the current watchlist and portfolio work for screener flow and saved-screen handoff.
- Make public browse, session-gated save or resume, saved-screen restoration, and subject or list handoff rules explicit.
- Add downstream consumer notes for `P4.1` and `P4.7`.

### `tests/contracts/test_screener_ui_flow_saved_screen_handoff_contract.py`

- Add a file-based contract test that asserts the narrative spec contains the screener workspace-flow, saved-screen, and downstream-consumer wording anchors.

## Acceptance Mapping

- The screener workspace and saved-screen rules satisfy the acceptance around screener UI flow and saved-screen behavior.
- The subject-detail and list-source handoff rules satisfy the acceptance around handoff into subject or list workflows.
- The downstream matrix satisfies the acceptance around later `P4.1` and `P4.7` consumers.
