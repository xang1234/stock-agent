# Auth Session And Navigation Guardrails Design

## Goal

Define how auth, session scope, and navigation guardrails interact with the shared workspace shell and workspace route groups so downstream surfaces know when content may render publicly, when a session is required, and how auth interruptions preserve navigation intent.

## Scope

This design covers:

- the public-versus-session-scoped surface split inside the persistent shell
- auth expectations for public subject browsing versus user-owned state
- soft in-shell guard behavior for protected workspaces and routes
- inline auth interrupts for protected actions launched from public routes
- session-expiry and logout behavior
- the downstream consumers named in the bead acceptance criteria
- a narrative spec update plus a file-based contract test

This design does not choose an identity provider, auth library, org or role model, pricing or entitlement policy, or framework-specific middleware, loader, or component structure.

## Core Contract

### Access scope model

- The persistent workspace shell is not auth-gated as a whole. Unauthenticated users may enter the shell and navigate public research routes.
- Public browsing surfaces are `Home`, `Screener`, top-level `Analyze` entry, and entered symbol-detail routes.
- Public browsing may render market data, fundamentals, findings, and subject context that do not depend on user-owned state or persisted session history.
- Session-scoped workspaces and flows are `Chat`, `Agents`, watchlist views and mutations, persisted Analyze runs, saved prompts or templates, and any user-owned thread or run history.
- A route may be publicly enterable yet still host protected actions. Top-level `Analyze` may render only a public entry state with carried `SubjectRef` context, while any user-owned draft, save, or persisted-run state requires a session.
- This contract is written in terms of authenticated session scope rather than a specific identity or entitlement backend.

### Navigation guards

- Protected workspaces and routes use soft in-shell guards rather than replacing the shell with a separate auth-page model.
- Unauthenticated navigation to `Chat`, `Agents`, watchlists, or any other session-scoped route keeps shell chrome visible and replaces protected main-canvas content with an auth gate for that destination.
- The guard preserves intended destination context so successful sign-in can resume the same workspace, thread, agent view, watchlist view, or persisted run target.
- Public routes may launch protected actions through inline auth interrupts. Examples include `save to watchlist`, `start chat`, `open persisted run`, and any action that would create or reveal user-owned state.
- Inline auth interrupts preserve the current public route plus the pending action payload so sign-in can resume the action instead of forcing a route change.
- Guard behavior is a semantic contract, not a framework-specific requirement about middleware, route loaders, or component boundaries.

### Session loss and logout behavior

- If a session expires or the user logs out inside a protected surface, protected content collapses to the same in-shell auth gate rather than redirecting away.
- Session loss preserves return-to context for the current protected route, but it must not continue rendering user-owned content after invalidation.
- Public routes remain navigable after logout or expiry without reconstructing the shell.
- Public surfaces continue to render public research context while protected panels and actions re-gate in place.
- The shell remains the durable navigation frame regardless of auth state; auth changes what the main canvas may reveal or mutate.

## Downstream Consumer Matrix

### Symbol overview and subject detail (`P1.3`)

- `P1.3` depends on the rule that symbol overview and entered subject detail may render public market, fundamentals, findings, and subject context without requiring a session.
- It also depends on user-owned actions from subject detail using inline auth interrupts with preserved return-to context rather than ejecting the user from symbol detail.

### Screener surface and saved-screen handoff

- Screener surface and saved-screen handoff depends on `Screener` remaining publicly browsable inside the persistent shell while saved outputs and user-scoped handoffs require a session.
- Saved screens, watchlist handoffs, agent handoffs, and other user-scoped screener outputs depend on the session-scoped action rules and in-shell guards.

### Thread coordinator and transport (`P2.1`)

- `P2.1` depends on `Chat` being session-scoped even though it lives inside the same persistent shell as public routes.
- Thread routes must collapse to the in-shell auth gate on unauthenticated entry, logout, or session expiry while preserving return-to thread context.

### Agent management and scheduling

- Agent management and scheduling depends on `Agents` and related user-owned configuration flows being session-scoped workspaces.
- Agent creation, management, and scheduling entry points launched from public routes depend on inline auth interrupts or in-shell guards rather than a separate page model.

## Normative File Changes

### `spec/finance_research_spec.md`

- Add an auth and session guardrail subsection near the shell and route sections defining public browsing surfaces, session-scoped surfaces, soft in-shell guards, inline auth interrupts, and session-loss behavior.
- Add downstream consumer notes for symbol detail, screener, chat transport, and agent management.

### `tests/contracts/test_auth_session_navigation_guardrails_contract.py`

- Add a file-based contract test that asserts the narrative spec contains the required public-versus-session-scoped split, guard behavior, session-loss rules, and downstream consumer anchors.

## Acceptance Mapping

- The public-versus-session-scoped surface classification satisfies the auth and session assumption boundary.
- Soft in-shell guards and inline auth interrupts satisfy the navigation behavior requirement without breaking the persistent shell model from `P0.2a`.
- Session-loss collapse rules satisfy the route protection behavior for protected surfaces after logout or expiry.
- The consumer matrix unblocks `P1.3`, screener saved-screen handoff, `P2.1`, and agent management and scheduling.
