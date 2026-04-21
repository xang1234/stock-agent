# Workspace Shell And Route Skeleton Design

## Goal

Define the persistent workspace shell, top-level workspace route groups, and symbol-detail route skeleton so later shell, symbol, chat, Analyze, and activity work all depend on one stable navigation contract.

## Scope

This design covers:

- the persistent shell topology shared across primary workspaces
- the distinction between primary workspaces and entered detail flows
- the top-level route groups for `Home`, `Agents`, `Chat`, `Screener`, and `Analyze`
- the symbol-detail shell and its nested route model
- the shell-owned right-rail slot and its selective default usage
- the downstream consumers named in the bead acceptance criteria
- a narrative spec update plus a file-based contract test

This design does not freeze framework-specific file paths, auth policy, responsive collapse behavior, or final UI styling. Those belong to later shell and surface beads.

## Core Contract

### Persistent workspace shell

- The app uses one persistent workspace shell rather than surface-specific chrome for each page.
- The shell owns three regions: left navigation, main workspace canvas, and a right-rail slot.
- Left navigation holds the primary workspaces: `Home`, `Agents`, `Chat`, `Screener`, and `Analyze`.
- Shell chrome persists while moving between those primary workspaces.
- The main canvas swaps between workspace-specific content regions and entered detail shells.

### Right-rail ownership

- The right rail is a shell-owned slot rather than a surface-owned layout invention.
- `Home`, `Agents`, `Chat`, symbol detail, and `Analyze` use the right rail by default.
- `Screener` defaults to a denser main-canvas layout and may opt into the rail later without changing the shell contract.
- Surfaces may populate the rail differently, but they should not redefine its global placement or existence.

### Primary workspaces versus entered detail flows

- The shell contract distinguishes durable primary workspaces from entered flows such as symbol detail.
- `Analyze` is a top-level workspace, not only a tab inside symbol detail.
- Symbol detail is not a primary left-nav workspace. It is an entered workspace reached from search, watchlists, Home, chat references, or other subject-linked surfaces.
- Entering symbol detail swaps the main canvas into a subject-detail shell while preserving the surrounding shell chrome.

## Route Skeleton

### Primary route groups

- Primary workspace route groups are `home`, `agents`, `chat`, `screener`, and `analyze`.
- `Chat` remains thread-scoped rather than symbol-scoped because threads may span themes, multiple subjects, or imported Analyze artifacts.
- `Analyze` is top-level and can accept carried `SubjectRef` context from other surfaces.

### Symbol-detail shell

- Symbol detail is a separate entered route group keyed by canonical subject identity.
- The subject-detail shell owns shared subject header context and local section navigation.
- Nested routes are the durable model for subject-detail sections; this contract does not collapse those sections into one client-tabbed page.
- The initial durable nested sections are `overview`, `financials`, `earnings`, `holders`, and `signals`.
- `signals` is the extensible section for community, sentiment, news pulse, and future alt-data views, so today’s Reddit-like view can evolve without renaming the shell contract.
- Additional subject-detail nested routes may be added later as long as they live inside the same subject-detail shell and do not redefine the top-level workspace map.

### Deep-linking between surfaces

- Symbol detail may deep-link into top-level `Analyze` with carried `SubjectRef` context or a prefilled analyze intent.
- Shell routing should preserve the distinction between moving within a workspace, entering symbol detail, and launching Analyze from another surface.
- Route naming should be stable and descriptive enough that downstream work can depend on the semantic buckets before framework-specific route files exist.

## Downstream Consumer Matrix

### Symbol search and quote snapshot surface (`P0.4`)

Search and entry flows depend on the distinction between primary workspaces and entered symbol-detail routes, plus the rule that symbol detail lands inside the persistent shell rather than as a detached page.

### Symbol overview shell (`P1.3`)

The symbol-overview shell depends on the subject-detail shell owning shared identity context, local section navigation, and a stable nested-route model.

### Symbol detail tabs and context modules (`P1.4`)

Detail sections depend on the durable nested-route buckets and the rule that section changes happen within the subject-detail shell rather than reconstructing page-level chrome.

### Thread coordinator and transport (`P2.1`)

Thread placement depends on `Chat` being a primary workspace inside the persistent shell, with thread-scoped routes that coexist with subject and Analyze entry flows.

### Analyze workspace surfaces (`P4.4`)

Analyze depends on being a top-level workspace that can still accept deep-linked subject context from symbol detail and other surfaces.

### Right-rail activity (`P4.5`)

Activity work depends on the shell-owned right-rail slot and the rule that the rail is globally placed but selectively populated by default.

## Normative File Changes

### `spec/finance_research_spec.md`

- Add an app-shell and route-skeleton subsection that defines the persistent shell regions, top-level workspace map, subject-detail shell, selective right rail, and `Analyze` deep-link behavior.
- Add explicit downstream consumer notes for symbol entry, symbol detail, chat placement, Analyze, and right-rail activity.

### `tests/contracts/test_workspace_shell_route_skeleton_contract.py`

- Add a file-based contract test that asserts the required workspace-shell, route-group, subject-detail, and right-rail wording anchors exist in the narrative spec.

## Acceptance Mapping

- The top-level workspace map and shell-region rules satisfy the route-group and shell-responsibility acceptance criteria.
- The subject-detail shell and nested-route model satisfy the acceptance requirement around symbol surfaces.
- The selective right-rail rule satisfies the shared-shell-responsibility requirement without overfreezing surface behavior.
- The consumer matrix unblocks `P0.4`, `P1.3`, `P1.4`, `P2.1`, `P4.4`, and `P4.5`.
