# Finance Research App — schema pack and implementation contract

This document is the concrete implementation companion to the architecture plan. It defines the canonical domain model, service boundaries, API contracts, block model, tool registry conventions, and the end-to-end workflows needed to build a finance research product with the same functional shape as the reference videos: typed chat blocks, theme and ticker chats, Analyze templates, cross-agent Home feed, right-rail activity, and in-message interactive charts.

## 1. Scope

The system is a desktop-first research terminal with five primary top-level workspaces and one entered subject-detail surface family:

- Primary top-level workspaces: Home, Agents, Chat, Screener, Analyze
- Entered subject-detail surfaces: Symbol detail

The app is built around three subsystems on one evidence plane:

1. Deterministic terminal surfaces
2. Interactive research chat
3. Background agents and findings

## 2. Operating invariants

### 2.1 Truth and provenance
- No displayed number exists without a backing `Fact` or `Computation` row.
- A displayed value always carries provenance, timestamps, method, and disclosure tier.
- Facts are immutable except through supersession.
- Candidate facts from narrative sources do not become authoritative without explicit promotion rules.

### 2.2 Structured reasoning boundary
- Documents are evidence, not truth.
- The reader path may ingest raw untrusted text.
- The analyst path never sees raw untrusted text.
- All inter-stage handoffs are structured schemas.

### 2.3 Snapshot and interactivity
- Every assistant response is pinned to a sealed `SnapshotManifest`.
- In-message interactions are allowed only when they are listed in `allowed_transforms` and do not require fresher data than `as_of`.
- Changing the timeframe of a historical comparison chart is allowed if the range end remains less than or equal to `as_of` and the subject set, basis, and normalization stay constant.
- Any request for fresher data, different peers, different basis, or different normalization requires refresh.

### 2.4 User actions and approvals
- Alerts, digests, external exports, and any future transactional action require explicit approval.
- Low-risk actions such as adding an item to a watchlist may be auto-approved if policy allows.

## 3. Product surfaces and ownership

### 3.1 Home
Home is a findings-first surface. It is the union of recent `Finding` objects across active agents, deduped by `ClaimCluster`, ranked by recency, severity, and user relevance.

### 3.2 Agents
Agents are scheduled research processes over a universe of `SubjectRef`s. They produce `Finding` objects and `RunActivity` rows.

### 3.3 Chat
Chat is the flagship research interface. Assistant messages are strict `Block[]` artifacts, not plain markdown transcripts.

### 3.4 Symbol detail
Symbol detail is an entered subject workspace with sections such as Overview, Financials, Earnings, Holders, and Signals. It may launch into top-level `Analyze` with carried subject context.

### 3.5 Analyze
Analyze is a saved, template-driven workflow with editable instructions, source categories, added subjects, and a memo-style block layout. It renders through the same `BlockRegistry` as chat and can be added to chat.

### 3.6 Watchlists and portfolio
Watchlists support `manual`, `screen`, `agent`, `theme`, and `portfolio` modes. Portfolio is lightweight holdings tracking, not brokerage execution.

### 3.7 Workspace shell and route skeleton

- The app uses one persistent workspace shell rather than surface-specific chrome for each page.
- The shell owns three regions: left navigation, main workspace canvas, and a right-rail slot.
- Left navigation holds the primary workspaces: `Home`, `Agents`, `Chat`, `Screener`, and `Analyze`.
- Shell chrome persists while moving between those primary workspaces.
- `Analyze` is a top-level workspace rather than only a symbol-detail tab.
- The right rail is a shell-owned slot rather than a surface-owned layout invention.
- `Home`, `Agents`, `Chat`, symbol detail, and `Analyze` use the right rail by default.
- `Screener` defaults to a denser main-canvas layout and may opt into the rail later without changing the shell contract.

### 3.8 Symbol-detail route skeleton

- Primary workspace route groups are `home`, `agents`, `chat`, `screener`, and `analyze`.
- These workspace route groups describe app navigation, not `/v1/*` HTTP endpoint groups.
- `Chat` remains thread-scoped rather than symbol-scoped because threads may span themes, multiple subjects, or imported Analyze artifacts.
- Symbol detail is an entered route group keyed by canonical subject identity rather than a primary left-nav workspace.
- Entering symbol detail swaps the main canvas into a subject-detail shell while preserving the surrounding shell chrome.
- The subject-detail shell owns shared subject header context and local section navigation.
- Nested routes are the durable model for subject-detail sections.
- The initial durable subject-detail sections are `overview`, `financials`, `earnings`, `holders`, and `signals`.
- `signals` is the extensible section for community, sentiment, news pulse, and future alt-data views.
- Symbol detail may deep-link into top-level `Analyze` with carried `SubjectRef` context or a prefilled analyze intent.

### 3.9 Downstream consumer rules for shell and route work

- Symbol search and quote snapshot surface (`P0.4`) depends on the distinction between primary workspaces and entered symbol-detail routes.
- Symbol overview shell (`P1.3`) depends on the subject-detail shell owning shared identity context and local section navigation.
- Symbol detail tabs and context modules (`P1.4`) depend on durable nested-route buckets inside the subject-detail shell.
- Thread coordinator and transport (`P2.1`) depends on `Chat` being a primary workspace inside the persistent shell.
- Analyze workspace surfaces (`P4.4`) depends on `Analyze` being top-level while still accepting deep-linked subject context.
- Right-rail activity (`P4.5`) depends on the shell-owned right-rail slot and selective default population.

### 3.10 Auth session and navigation guardrails

- The persistent workspace shell is not auth-gated as a whole. Unauthenticated users may enter the shell and navigate public research routes.
- Public browsing surfaces are `Home`, `Screener`, top-level `Analyze` entry, and entered symbol-detail routes.
- Public browsing may render market data, fundamentals, findings, and subject context that do not depend on user-owned state or persisted session history.
- Session-scoped workspaces and flows are `Chat`, `Agents`, watchlist views and mutations, persisted Analyze runs, saved prompts or templates, and any user-owned thread or run history.
- A route may be publicly enterable yet still host protected actions. Top-level `Analyze` may render only a public entry state with carried `SubjectRef` context, while any user-owned draft, save, or persisted-run state requires a session.
- Protected workspaces and routes use soft in-shell guards rather than replacing the shell with a separate auth-page model.
- Unauthenticated navigation to `Chat`, `Agents`, watchlists, or any other session-scoped route keeps shell chrome visible and replaces protected main-canvas content with an auth gate for that destination.
- The guard preserves intended destination context so successful sign-in can resume the same workspace, thread, agent view, watchlist view, or persisted run target.
- Public routes may launch protected actions through inline auth interrupts. Examples include `save to watchlist`, `start chat`, `open persisted run`, and any action that would create or reveal user-owned state.
- Inline auth interrupts preserve the current public route plus the pending action payload so sign-in can resume the action instead of forcing a route change.
- If a session expires or the user logs out inside a protected surface, protected content collapses to the same in-shell auth gate rather than redirecting away.
- Session loss preserves return-to context for the current protected route, but it must not continue rendering user-owned content after invalidation.
- Public routes remain navigable after logout or expiry without reconstructing the shell.
- Public surfaces continue to render public research context while protected panels and actions re-gate in place.
- The shell remains the durable navigation frame regardless of auth state; auth changes what the main canvas may reveal or mutate.
- This contract is written in terms of authenticated session scope rather than a specific identity or entitlement backend.

### 3.11 Downstream consumer rules for auth and session work

- Symbol overview and subject detail (`P1.3`) depends on the rule that entered subject detail may render public market, fundamentals, findings, and subject context without requiring a session.
- Screener surface and saved-screen handoff depends on `Screener` remaining publicly browsable inside the persistent shell while saved outputs and user-scoped handoffs require a session.
- Thread coordinator and transport (`P2.1`) depends on `Chat` being session-scoped even though it lives inside the same persistent shell as public routes.
- Agent management and scheduling depends on `Agents` and related user-owned configuration flows being session-scoped workspaces.

## 4. Canonical domain model

### 4.1 Finance identity layer

```ts
Issuer {
  issuer_id: UUID
  legal_name: string
  former_names: string[]
  cik?: string
  lei?: string
  domicile?: string
  sector?: string
  industry?: string
  created_at: timestamp
  updated_at: timestamp
}

Instrument {
  instrument_id: UUID
  issuer_id: UUID
  asset_type: 'common_stock' | 'adr' | 'etf' | 'index' | 'crypto' | 'fx' | 'bond'
  share_class?: string
  isin?: string
  figi_composite?: string
  created_at: timestamp
  updated_at: timestamp
}

Listing {
  listing_id: UUID
  instrument_id: UUID
  mic: string
  ticker: string
  trading_currency: string
  timezone: string
  active_from?: timestamp
  active_to?: timestamp
  created_at: timestamp
  updated_at: timestamp
}
```

### 4.1.1 Canonical identity rules

- `Issuer` is the canonical identity for the legal and reporting entity.
- `Instrument` is the canonical identity for the tradable security definition issued by an issuer.
- `Listing` is the canonical identity for an exchange-specific venue representation of an instrument.
- `ticker` is a listing attribute and lookup handle, not canonical identity.
- ticker is a listing attribute and lookup handle, not canonical identity.
- Resolver entrypoints may start from ticker, alias, CIK, ISIN, or other external identifiers, but every downstream contract must promote the result into an explicit issuer, instrument, or listing identity.
- Downstream surfaces may display ticker strings for readability, but they must not persist or join on ticker where issuer, instrument, or listing identity exists.

### 4.2 Research subject layer

```ts
type SubjectRef =
  | { kind: 'issuer'; id: UUID }
  | { kind: 'instrument'; id: UUID }
  | { kind: 'listing'; id: UUID }
  | { kind: 'theme'; id: UUID }
  | { kind: 'macro_topic'; id: UUID }
  | { kind: 'portfolio'; id: UUID }
  | { kind: 'screen'; id: UUID }

Theme {
  theme_id: UUID
  name: string
  description?: string
  membership_mode: 'manual' | 'rule_based' | 'inferred'
  membership_spec?: json
  active_from?: timestamp
  active_to?: timestamp
}

ThemeMembership {
  theme_id: UUID
  subject_kind: SubjectKind
  subject_id: UUID
  score?: numeric
  rationale_claim_ids?: UUID[]
  effective_at: timestamp
  expires_at?: timestamp
}

Portfolio {
  portfolio_id: UUID
  user_id: UUID
  name: string
  base_currency: string
}

PortfolioHolding {
  portfolio_id: UUID
  subject_kind: SubjectKind
  subject_id: UUID
  quantity: numeric
  cost_basis?: numeric
  opened_at?: timestamp
  closed_at?: timestamp
}
```

`SubjectRef` selection rules:

- Use `issuer` for issuer research, filing-backed facts, company summaries, and issuer-scoped findings.
- Use `instrument` for security definitions that should survive listing changes, multiple venue representations, and share-class distinctions.
- Use `listing` for quotes, bars, session state, venue-sensitive performance, trading currency, and symbol-specific market context.
- `theme`, `macro_topic`, `portfolio`, and `screen` remain valid research subjects, but they do not replace entity identity when the subject is an issuer, instrument, or listing.

### 4.3 Metrics and truth objects

```ts
Metric {
  metric_id: UUID
  metric_key: string
  display_name: string
  unit_class: 'currency' | 'percent' | 'count' | 'ratio' | 'duration' | 'enum'
  aggregation: 'sum' | 'avg' | 'point_in_time' | 'ttm' | 'yoy' | 'qoq' | 'derived'
  interpretation: 'higher_is_better' | 'lower_is_better' | 'neutral'
  canonical_source_class: 'gaap' | 'ifrs' | 'vendor' | 'market' | 'derived'
  definition_version: integer
}

Fact {
  fact_id: UUID
  subject_kind: SubjectKind
  subject_id: UUID
  metric_id: UUID
  period_kind: 'point' | 'fiscal_q' | 'fiscal_y' | 'ttm' | 'range'
  period_start?: date
  period_end?: date
  fiscal_year?: integer
  fiscal_period?: string
  value_num?: numeric
  value_text?: string
  unit: string
  currency?: string
  scale: numeric
  as_of: timestamp
  reported_at?: timestamp
  observed_at: timestamp
  source_id: UUID
  method: 'reported' | 'derived' | 'estimated' | 'vendor' | 'extracted'
  adjustment_basis?: 'unadjusted' | 'split_adjusted' | 'split_and_div_adjusted'
  definition_version: integer
  verification_status: 'authoritative' | 'candidate' | 'corroborated' | 'disputed'
  freshness_class: 'real_time' | 'delayed_15m' | 'eod' | 'filing_time' | 'stale'
  coverage_level: 'full' | 'partial' | 'sparse' | 'unavailable'
  quality_flags: string[]
  entitlement_channels: ('app' | 'export' | 'email' | 'push')[]
  confidence: numeric
  supersedes?: UUID
  superseded_by?: UUID
  invalidated_at?: timestamp
  ingestion_batch_id?: UUID
}
```

### 4.3.1 Truth and evidence role rules

- `Metric` is a definition object, not an observed value.
- `Fact` is the unit of truth for displayed values and must carry provenance, verification status, freshness, coverage state, and supersession state.
- `Computation` is the deterministic derivation record for a produced value and explains how displayed numbers were calculated from structured inputs.
- `Claim` is an extracted assertion from evidence and is not canonical truth.
- `Event` is the unit of state change assembled from claims and source references.
- `EntityImpact` routes a claim onto affected subjects for feed ranking, alerting, and agent relevance.
- `Finding` is a user-facing product artifact built from a sealed snapshot over the evidence graph.
- Documents are evidence, not truth.
- Facts are immutable except through supersession or explicit invalidation.
- Verification status remains attached to facts so downstream consumers can distinguish authoritative values from candidate, corroborated, or disputed values.

### 4.4 Claims, events, impacts, computations

```ts
Claim {
  claim_id: UUID
  document_id: UUID
  predicate: string
  text_canonical: string
  polarity: 'positive' | 'negative' | 'neutral' | 'mixed'
  modality: 'asserted' | 'estimated' | 'speculative' | 'rumored' | 'quoted'
  reported_by_source_id: UUID
  attributed_to_type?: 'issuer_mgmt' | 'journalist' | 'analyst' | 'tweet_author' | 'anonymous'
  attributed_to_id?: string
  effective_time?: timestamp
  confidence: numeric
  status: 'extracted' | 'corroborated' | 'disputed' | 'rejected'
}

ClaimArgument {
  claim_argument_id: UUID
  claim_id: UUID
  subject_kind: SubjectKind
  subject_id: UUID
  role: 'subject' | 'object' | 'customer' | 'supplier' | 'competitor' | 'regulator' | 'beneficiary' | 'constrained_party' | 'affected_party'
}

EntityImpact {
  entity_impact_id: UUID
  claim_id: UUID
  subject_kind: SubjectKind
  subject_id: UUID
  direction: 'positive' | 'negative' | 'mixed' | 'unknown'
  channel: 'demand' | 'pricing' | 'supply_chain' | 'regulation' | 'competition' | 'balance_sheet' | 'sentiment'
  horizon: 'near_term' | 'medium_term' | 'long_term'
  confidence: numeric
}

Event {
  event_id: UUID
  event_type: 'earnings_release' | 'guidance_update' | 'rating_change' | 'm_and_a' | 'split' | 'dividend' | 'product_launch' | 'lawsuit' | 'macro_event' | 'theme_event'
  occurred_at: timestamp
  status: 'reported' | 'confirmed' | 'canceled'
  source_claim_ids: UUID[]
  source_ids: UUID[]
  payload_json?: json
}

EventSubject {
  event_subject_id: UUID
  event_id: UUID
  subject_kind: SubjectKind
  subject_id: UUID
  role?: string
}

Computation {
  computation_id: UUID
  formula_id: string
  code_version: string
  input_refs: json
  output_ref: json
  created_at: timestamp
}
```

### 4.5 Sources, documents, mentions, clusters

```ts
Source {
  source_id: UUID
  provider: string
  kind: 'filing' | 'press_release' | 'transcript' | 'article' | 'research_note' | 'social_post' | 'upload' | 'internal'
  canonical_url?: string
  trust_tier: 'primary' | 'secondary' | 'tertiary' | 'user'
  license_class: string
  retrieved_at: timestamp
  content_hash?: string
}

Document {
  document_id: UUID
  source_id: UUID
  provider_doc_id?: string
  kind: 'filing' | 'transcript' | 'article' | 'research_note' | 'social_post' | 'thread' | 'upload'
  parent_document_id?: UUID
  conversation_id?: string
  title?: string
  author?: string
  published_at?: timestamp
  lang?: string
  content_hash: string
  raw_blob_id: string
  parse_status: 'pending' | 'parsed' | 'failed' | 'superseded'
  deleted_at?: timestamp
}

Mention {
  mention_id: UUID
  document_id: UUID
  subject_kind: SubjectKind
  subject_id: UUID
  prominence: 'headline' | 'lead' | 'body' | 'incidental'
  mention_count: integer
  confidence: numeric
}

ClaimEvidence {
  claim_evidence_id: UUID
  claim_id: UUID
  document_id: UUID
  locator: json
  excerpt_hash?: string
  confidence: numeric
}

ClaimCluster {
  cluster_id: UUID
  canonical_signature: string
  first_seen_at: timestamp
  last_seen_at: timestamp
  support_count: integer
  contradiction_count: integer
  aggregate_confidence: numeric
}

ClaimClusterMember {
  claim_cluster_member_id: UUID
  cluster_id: UUID
  claim_id: UUID
  relation: 'support' | 'contradict'
}
```

### 4.6 Snapshots, findings, activity, templates, chat

```ts
SnapshotManifest {
  snapshot_id: UUID
  created_at: timestamp
  subject_refs: SubjectRef[]
  fact_refs: UUID[]
  claim_refs: UUID[]
  event_refs: UUID[]
  series_specs: json
  source_ids: UUID[]
  tool_call_ids: UUID[]
  as_of: timestamp
  basis: 'unadjusted' | 'split_adjusted' | 'split_and_div_adjusted' | 'reported' | 'restated'
  normalization: 'raw' | 'pct_return' | 'index_100' | 'currency_normalized'
  coverage_start?: timestamp
  allowed_transforms: json
  model_version?: string
  parent_snapshot?: UUID
}

Finding {
  finding_id: UUID
  agent_id: UUID
  snapshot_id: UUID
  subject_refs: SubjectRef[]
  claim_cluster_ids: UUID[]
  severity: 'low' | 'medium' | 'high' | 'critical'
  headline: string
  summary_blocks: Block[]
  created_at: timestamp
}

RunActivity {
  run_activity_id: UUID
  agent_id: UUID
  stage: 'reading' | 'investigating' | 'found' | 'dismissed'
  subject_refs: SubjectRef[]
  source_refs: UUID[]
  summary: string
  ts: timestamp
}

AnalyzeTemplate {
  template_id: UUID
  user_id: UUID
  name: string
  prompt_template: string
  source_categories: string[]
  added_subject_refs: SubjectRef[]
  block_layout_hint?: json
  peer_policy?: json
  disclosure_policy?: json
  version: integer
  created_at: timestamp
  updated_at: timestamp
}

ChatThread {
  thread_id: UUID
  user_id: UUID
  primary_subject_kind?: SubjectKind
  primary_subject_id?: UUID
  title?: string
  latest_snapshot_id?: UUID
  created_at: timestamp
  updated_at: timestamp
}

ChatMessage {
  message_id: UUID
  thread_id: UUID
  role: 'user' | 'assistant' | 'tool'
  snapshot_id?: UUID
  blocks: Block[]
  content_hash: string
  created_at: timestamp
}
```

## 5. Evidence and document handling

### 5.1 Ingestion pipeline

```text
Acquire raw document
  -> Canonicalize
  -> Parse
  -> Entity-link
  -> Reader extraction
  -> Claims / impacts / candidate facts / events
  -> Cluster / corroborate / promote
  -> Snapshot / findings / blocks / alerts
```

### 5.2 Promotion rules by source class
- Filing and issuer disclosure may create authoritative facts.
- Transcript and earnings-call commentary typically create claims and events; facts become authoritative only when tied to formal disclosure or validated extraction rules.
- News articles and research notes generally create claims, events, candidate facts, and impacts; they do not directly create authoritative facts unless matched to a primary source.
- Tweets, Reddit posts, and similar social sources create claims, sentiment, and leads only.
- User uploads create user-scoped evidence unless promoted by explicit validation workflows.

### 5.3 Multi-entity reasoning
A document can mention multiple subjects. The reasoning unit is the claim plus its arguments and `EntityImpact` edges. Routing, alerting, and theme assignment should rely on claims and impacts rather than bare document mention tags.

## 6. Service boundaries

### 6.1 Identity and resolver service
Owns issuer, instrument, listing, theme, macro-topic, and subject resolution.

- The resolver is the deterministic boundary that converts user-entered lookup input and provider-origin identity records into canonical finance identity outputs.
- The resolver owns normalization, candidate generation, canonical reference selection when unambiguous, and explicit ambiguity preservation when multiple canonical targets remain plausible.
- The resolver is distinct from search UI, user disambiguation flow, and downstream subject hydration.
- Every successful resolver path must end in explicit canonical refs rather than ticker strings or raw provider ids standing in for identity.
- The resolver must promote lookup handles into issuer, instrument, listing, or `SubjectRef` outputs that downstream systems can persist and join on safely.
- The contract defines a typed resolution envelope rather than an untyped candidate list.
- `resolved` means the resolver can name one canonical target confidently enough for deterministic downstream use.
- `ambiguous` means multiple canonical issuer, instrument, listing, or `SubjectRef` targets remain plausible after normalization and matching, so the resolver must return ranked candidates without silently picking one.
- `not_found` means the resolver could normalize the input but could not map it to a supported canonical target.
- The contract explicitly covers two input families: user-entered lookup text and provider-origin identity records.
- User-entered lookup text includes ticker-like strings, issuer names, aliases, and other concise finance lookup inputs.
- Provider-origin identity records include external ids and structured provider payload fields such as ticker, exchange, CIK, ISIN, or other identifier-bearing records.
- The resolver must normalize input before matching, but normalization must not erase identity-level distinctions between issuer, instrument, and listing.
- The resolver may start from ticker or alias lookup, but downstream output must promote that lookup into explicit issuer, instrument, listing, or `SubjectRef` candidates.
- Ticker-only identity remains insufficient because the same symbol can map to different listings, venues, or securities, and issuer-level workflows often need a different canonical target than market-data workflows.
- The resolver should expose the ambiguity axis when possible, such as issuer-versus-listing ambiguity or multiple plausible listings for one ticker string.
- Ranked candidates are advisory metadata, not permission to silently collapse ambiguity into one winner.
- `resolved` should include the canonical identity level that was chosen so downstream systems know whether they received issuer, instrument, listing, or already-formed `SubjectRef` output.

### 6.1.1 Downstream consumer rules

- Search-to-subject resolution flow (`P0.3b`) depends on the resolver outcome vocabulary it will carry through candidate search, user choice, and downstream subject hydration.
- Market data service (`P1.1`) depends on the rule that quote and bar consumers must receive listing-appropriate canonical output rather than ticker strings or issuer-level guesses.
- Fundamentals service (`P1.2`) depends on the rule that issuer-backed fundamentals cannot rely on ticker-only identity and must consume issuer-appropriate canonical output or preserved ambiguity.
- Screener surface and saved-screen handoff depends on deterministic subject identity shapes even before later hydration flow is applied.
- Pre-resolve router and budget policy (`P2.2`) depends on the rule that deterministic pre-resolve routing consumes resolver envelopes rather than asking the model to silently choose among ambiguous identity candidates.

### 6.2 Market data service
Owns quotes, bars, corporate actions, aligned performance series, and market session state.

### 6.3 Fundamentals service
Owns company profile, statements, ratios, holders, insiders, estimates, and fiscal-calendar normalization.

### 6.4 Evidence service
Owns sources, documents, mentions, claims, claim arguments, impacts, events, facts, computations, clusters, snapshots, provenance, and evidence bundles.

### 6.4.1 Downstream consumer rules for truth and evidence objects

- Fundamentals consumes `Metric`, `Fact`, and `Computation` as the canonical value layer and may read claims or events only for explanatory context.
- Evidence extraction owns `Source`, `Document`, `Mention`, `Claim`, `ClaimArgument`, `ClaimEvidence`, `ClaimCluster`, `Event`, and `EntityImpact`.
- Home feed consumes Finding, SnapshotManifest, and ClaimCluster as the deduped product artifact layer.
- Agent workflows consume `SnapshotManifest`, `Finding`, `RunActivity`, `ClaimCluster`, and `EntityImpact`.
- Reader and extraction flows may ingest raw documents; analyst and user-facing flows must operate on structured facts, claims, events, snapshots, findings, and evidence bundles instead of raw untrusted text.

### 6.5 Filing extraction platform
Owns filing retrieval, section parsing, extension handling, segment extraction, footnote extraction, management claim extraction, event detection, and reviewer queues.

### 6.6 Search service
Owns symbol typeahead, corpus retrieval, and evidence-bundle assembly.

### 6.7 Screening service
Owns screens, ranking, saved filters, and dynamic universe generation.

### 6.8 Home feed service
Owns cross-agent findings feed generation, cluster dedupe, and ranking.

### 6.9 Notification service
Owns email, push, SMS, and digest delivery.

## 6A. Relational schema contract

### Reference and universe tables

- `issuers`, `instruments`, `listings`, `themes`, `theme_memberships`, `portfolios`, `portfolio_holdings`, `watchlists`, and `watchlist_members` define reusable subject context and membership state.
- This family supports identity resolution, subject scoping, and user-curated universes without becoming part of the evidence graph.

### Evidence-plane relational tables

- `metrics`, `sources`, `documents`, `mentions`, `claims`, `claim_arguments`, `entity_impacts`, `claim_evidence`, `claim_clusters`, `claim_cluster_members`, `events`, `event_subjects`, `facts`, `computations`, `snapshots`, `findings`, `run_activities`, `citation_logs`, `verifier_fail_logs`, and `eval_run_results` form the relational evidence plane.
- This family holds provenance, auditability, promotion state, snapshotted findings, and the fact or claim or event model that downstream services depend on directly.

### App metadata and orchestration tables

- `users`, `chat_threads`, `chat_messages`, `analyze_templates`, `agents`, and `tool_call_logs` support user state, orchestration, and workflow coordination around the evidence plane.
- These tables may reference snapshots, findings, or subject refs, but they do not replace the canonical evidence-plane tables.

### Storage split

- App metadata may live in smaller app storage such as D1 or Postgres, depending on deployment constraints.
- Evidence objects and snapshots belong to the relational evidence plane and should live in Postgres-class storage that preserves relational integrity and auditability.
- Raw document bytes are outside the relational schema.

### Snapshot bridge

- `snapshots` are evidence-plane records rather than ordinary app metadata.
- Snapshots seal the refs that support answers and findings at a specific `as_of`.
- Snapshots bridge the evidence plane to user-facing artifacts.

## 7. API contracts

The normative API surface is defined in `finance_research_openapi.yaml`.

Top-level API endpoint groups:
- `/v1/subjects/*`
- `/v1/market/*`
- `/v1/fundamentals/*`
- `/v1/evidence/*`
- `/v1/snapshots/*`
- `/v1/chat/*`
- `/v1/analyze/*`
- `/v1/agents/*`
- `/v1/home/*`
- `/v1/watchlists/*`
- `/v1/screener/*`

### 7.1 HTTP API ownership and consumer rules

- `Subjects`, `Market`, `Fundamentals`, `Evidence`, `Snapshots`, `Chat`, `Analyze`, `Agents`, `Home`, `Watchlists`, and `Screener` are the stable endpoint groups exposed to clients.
- The frontend only talks to `/v1/*` backend contracts.
- The frontend does not call third-party providers directly.
- `Chat` plus `Snapshots` define the run, stream, and render boundary.
- Interactive updates such as snapshot transforms, chat streaming, and market refreshes stay inside backend-managed endpoints rather than bypassing the API layer.

## 8. Block model

Assistant output is always a `Block[]` envelope. The normative JSON Schema is in `finance_research_block_schema.json`.

Key design rules:
- blocks are typed artifacts, not rendered HTML
- `RichText` binds to facts, claims, and events by reference
- `Section` is first-class and holds child blocks
- `PerfComparison` is snapshot-aware and transform-aware
- `Sources` is required whenever external evidence was used
- `Disclosure` can be injected by the orchestrator

### 8.1 Block schema contract and render rules

- Assistant output is always a typed `Block[]` response envelope, not plain markdown and not a tool call.
- Every block kind inherits the `BaseBlock` contract: `id`, `kind`, `snapshot_id`, `data_ref`, `source_refs`, and `as_of`.
- The canonical schema field is `data_ref`.
- Earlier analysis used `dataRef` or `queryRef`; the schema standardizes this as `data_ref`.
- Narrative and layout blocks: `rich_text`, `section`
- Tabular and compact metric blocks: `metric_row`, `table`
- Chart and comparison blocks: `line_chart`, `revenue_bars`, `perf_comparison`, `segment_donut`, `segment_trajectory`, `metrics_comparison`, `sentiment_trend`, `mention_volume`
- Research and evidence summary blocks: `analyst_consensus`, `price_target_range`, `eps_surprise`, `filings_list`, `news_cluster`, `finding_card`
- Trust and rendering-boundary blocks: `sources`, `disclosure`
- `Sources` is the required provenance surface whenever external evidence appears in the answer.
- `Disclosure` is the explicit trust and compliance surface and may be injected by orchestration.
- `as_of` is the freshness boundary for the rendered artifact.

### 8.2 Downstream consumer rules for block artifacts

- Thread coordinator and transport (`P2.1`) consumes `Block[]` as the streamed and persisted assistant payload.
- Block registry versioning and validation (`P2.3`) consumes the exact block kinds plus the shared `BaseBlock` fields.
- Snapshot assembler and verifier (`P2.4`) consumes `snapshot_id`, `source_refs`, `data_ref`, and `as_of` to verify rendered artifacts against sealed evidence.
- Findings, home feed, and explainability (`P4.2`, `P4.3`, `P4.6`) consume `finding_card`, `sources`, `disclosure`, and the same snapshot-safe render rules used in chat and analyze.
- Frontend renderer (`PX.3`) consumes `Block[]` via a shared `BlockRegistry` and must not treat rendering as a tool invocation.
- Chat, Analyze, and agent-produced findings all render through the same `BlockRegistry`, keyed by block `kind`.
- Interactivity stays inside snapshot scope unless the user explicitly refreshes.

## 9. Tool registry

The normative analyst tool registry is in `finance_research_tool_registry.json`.

### 9.1 Tool registry and bundle rules

- `spec/finance_research_tool_registry.json` is the normative artifact for bundle membership, tool audience, approval sensitivity, and JSON-schema-constrained inputs and outputs.
- Tools are backend data and action surfaces; `Block[]` remains the response artifact contract.
- The system chooses the bundle; the model chooses tools within the bundle.
- Bundle groups: `quote_lookup`, `single_subject_analysis`, `peer_comparison`, `theme_research`, `segment_deep_dive`, `document_research`, `filing_research`, `screener`, `agent_management`, `alert_management`, and `analyze_template_run`.
- `reader` tools are the only tools allowed to access raw untrusted text or raw documents.
- `analyst` tools operate only on structured outputs, canonical subject and period resolution, evidence bundles, facts, claims, events, and approval-mediated write intents.
- Raw text must not leak into analyst-facing tools.
- Approval-sensitive tools today are `create_alert` and `create_agent`.
- `add_to_watchlist` is a non-read-only write-intent tool even though it is not currently approval-required.

### 9.2 Downstream consumer rules for tool runtime

- Pre-resolve routing and budget policy (`P2.2`) depends on deterministic bundle selection, audience separation, and registry metadata before the analyst loop starts.
- Document ingestion and extraction (`P3.2`) depends on raw document search, fetch, and extraction tools belonging to the `reader` audience.
- Alerting and automation (`P5.1`) depends on side-effect categories and approval sensitivity so create and update flows do not execute directly from model output.
- Tool runtime and orchestration (`PX.2`) depends on bundle membership, audience, `read_only`, `approval_required`, `cost_class`, and `freshness_expectation`.

## 10. Snapshot semantics

### 10.1 Sealed snapshot manifest

- A sealed snapshot pins the subject set, `as_of`, basis, normalization, coverage window, source set, bound fact / claim / event refs, and exact `allowed_transforms`.
- `allowed_transforms` is explicit manifest state, not a UI guess derived from block kind alone.
- Snapshot sealing happens only after binding and disclosure verification.
- Persisted chat and analyze artifacts must continue to point at that sealed snapshot rather than reconstructing support opportunistically later.

### 10.2 In-snapshot transforms

- A transform is legal inside a sealed snapshot only when it preserves the subject set and does not require fresher evidence than `as_of`.
- In-snapshot transforms may change presentation or range only when the required rows or series are already inside the sealed data boundary.
- Changing `YTD` to `1Y` on a performance chart is allowed only if the requested range end is less than or equal to `as_of`.
- The manifest, not the client, determines whether a transform is allowed.

### 10.3 Refresh and new-run boundary

- Any request that changes subject membership, peer set, basis, normalization, or freshness crosses the snapshot boundary.
- Requests for fresher data, different peers, different basis, or different normalization require refresh or a new run.
- Crossing the snapshot boundary must be explicit rather than a silent mutation of a sealed answer.

### 10.4 Downstream consumer rules for snapshot semantics

- Block registry versioning and validation (`P2.3`) depends on snapshot rules being stable enough to know which interactions are legal within existing block bindings and which require a new backend result.
- Snapshot assembler and verifier (`P2.4`) depends on the sealed manifest contents, sealing order, and refresh boundary to prove that rendered blocks still correspond to the same evidence-backed snapshot.
- Shared artifact flow (`P4.3`) depends on sealed snapshots remaining reusable product artifacts.
- Frontend renderer (`PX.3`) depends on presentation-only interactions staying local only when they remain inside the sealed snapshot contract.

## 11. Key workflows

### 11.1 Chat turn
1. Resolve subjects and period
2. Select bundle
3. Run analyst tool loop
4. Stage snapshot manifest
5. Verify bindings and disclosures
6. Seal snapshot
7. Stream `Block[]`
8. Persist message, snapshot, citations, and summary

### 11.2 Analyze template run
1. Load template
2. Resolve source categories into tool bundle and policy
3. Add primary subject plus template-added subjects
4. Run analyst
5. Seal snapshot
6. Persist analysis artifact
7. Optionally add artifact to chat thread

### 11.3 Agent run
1. Load due agents
2. Retrieve new documents and facts since watermark
3. Run reader extraction and clustering
4. Relevance-rank by thesis
5. Run analyst on relevant evidence
6. Create findings and activities
7. Evaluate alerts
8. Advance watermark transactionally

### 11.4 Home feed query
1. Load active agents
2. Pull recent findings
3. Dedupe by claim cluster
4. Rank by recency, severity, and user affinity
5. Return collapsed cards with expandable details

## 12. Build order

### Phase 1
- issuer/instrument/listing resolver
- market data service
- US fundamentals via SEC and market provider
- structured block renderer
- basic chat orchestrator and snapshots

### Phase 2
- document pipeline
- reader extraction
- evidence bundles
- claims, events, impacts, clusters

### Phase 3
- themes and macro subjects
- Analyze templates
- Home feed and activity stream
- dynamic watchlists and portfolio overlays

### Phase 4
- agents and notifications
- non-US coverage
- reviewer queues
- richer analytics and exports

## 13. Files in this artifact set
- `finance_research_spec.md` — this narrative spec
- `finance_research_db_schema.sql` — relational schema pack
- `finance_research_openapi.yaml` — HTTP API contracts
- `finance_research_block_schema.json` — block output schema
- `finance_research_tool_registry.json` — analyst and reader tool registry
