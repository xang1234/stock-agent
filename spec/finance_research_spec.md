# Finance Research App — schema pack and implementation contract

This document is the concrete implementation companion to the architecture plan. It defines the canonical domain model, service boundaries, API contracts, block model, tool registry conventions, and the end-to-end workflows needed to build a finance research product with the same functional shape as the reference videos: typed chat blocks, theme and ticker chats, Analyze templates, cross-agent Home feed, right-rail activity, and in-message interactive charts.

## 1. Scope

The system is a desktop-first research terminal with six primary surfaces:

- Home
- Agents
- Chat
- Screener
- Symbol detail
- Analyze

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
Overview, Financials, Earnings, Holders, Reddit, Analyze.

### 3.5 Analyze
Analyze is a saved, template-driven workflow with editable instructions, source categories, added subjects, and a memo-style block layout. It renders through the same `BlockRegistry` as chat and can be added to chat.

### 3.6 Watchlists and portfolio
Watchlists support `manual`, `screen`, `agent`, `theme`, and `portfolio` modes. Portfolio is lightweight holdings tracking, not brokerage execution.

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

### 6.1.1 Downstream consumer rules

- Resolver service resolves aliases, tickers, and external identifiers into explicit issuer, instrument, or listing candidates and must preserve ambiguity when multiple listings are plausible.
- Market data service keys quotes, bars, corporate actions, session state, and venue-sensitive performance on `listing`, with any rollup to `instrument` called out explicitly.
- Fundamentals service keys issuer profile, filing-backed statements, ratios, holders, insiders, estimates, and fiscal normalization on `issuer`, with instrument metadata attached only when the metric is security-specific.
- Chat and Analyze persist subject context as SubjectRef[] even when the user entered a ticker or company alias.
- Agent definitions, runs, findings, and subscriptions carry `SubjectRef[]` so monitoring survives ticker changes, cross-listings, ADRs, and dual-class structures.

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

Top-level route groups:
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

## 8. Block model

Assistant output is always a `Block[]` envelope. The normative JSON Schema is in `finance_research_block_schema.json`.

Key design rules:
- blocks are typed artifacts, not rendered HTML
- `RichText` binds to facts, claims, and events by reference
- `Section` is first-class and holds child blocks
- `PerfComparison` is snapshot-aware and transform-aware
- `Sources` is required whenever external evidence was used
- `Disclosure` can be injected by the orchestrator

## 9. Tool registry

The normative analyst tool registry is in `finance_research_tool_registry.json`.

Design rules:
- the system chooses the bundle; the model chooses tools within the bundle
- tools are provider-agnostic and JSON-schema constrained
- reader-only tools can touch raw text; analyst-facing tools cannot
- side-effecting tools require approval
- every tool output must be traceable to source refs or deterministic computation refs

## 10. Snapshot semantics

A snapshot pins:
- subject set
- `as_of`
- basis
- normalization
- coverage start
- source set
- fact / claim / event refs
- allowed transforms

Transforms are allowed inside a sealed snapshot only when they preserve the subject set and do not require fresher evidence than `as_of`.

Example:
- changing `YTD` to `1Y` on a performance chart is allowed if the requested range end is less than or equal to `as_of`
- changing peers or basis is not allowed in-snapshot and requires refresh or a new run

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
