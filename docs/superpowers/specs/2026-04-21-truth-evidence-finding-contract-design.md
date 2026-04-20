# Truth Evidence And Finding Contract Design

## Goal

Define the shared contract for metrics, facts, claims, events, impacts, findings, and related evidence objects so downstream services preserve the architecture rule that documents are evidence, not truth.

## Scope

This design covers:

- role boundaries for `Metric`, `Fact`, `Computation`, `Claim`, `Event`, `EntityImpact`, `Finding`, and the evidence-layer support objects
- downstream consumer expectations for fundamentals, evidence extraction, Home feed, and agent findings
- provenance, supersession, and verification-status rules that later contract beads must preserve
- normative updates to the implementation spec, OpenAPI schema, SQL schema notes, and a small file-based contract test

This design does not cover extraction algorithms, ranking logic, promotion implementation, or new schema tables beyond the notes needed to make the shared contract explicit.

## Core Contract

### Truth and evidence roles

- `Metric` defines what can be measured and how downstream systems interpret a value. It is a definition object, not an observed value.
- `Fact` is the unit of truth for displayed values. A fact must carry provenance, timing fields, verification status, coverage state, and supersession or invalidation links when the value changes.
- `Computation` is the deterministic derivation record for a produced value. It explains how a displayed value was calculated from fact or series inputs.
- `Claim` is the unit of assertion extracted from evidence. A claim may be important, but it is not canonical truth.
- `Event` is the unit of state change assembled from one or more claims and source references.
- `EntityImpact` is the routing object that projects a claim onto affected subjects for agent relevance, alerting, and feed ranking.
- `Finding` is a user-facing, snapshotted product artifact assembled from evidence graph objects. It summarizes a conclusion; it does not replace the underlying facts, claims, or events.

### Evidence support objects

- `Source` captures provider, trust tier, license, retrieval time, and content identity.
- `Document` is the exact retrieved artifact and remains evidence even when later extraction promotes some content into facts.
- `Mention` captures subject linkage inside a document without turning that mention into a claim or fact.
- `ClaimEvidence` ties a claim to concrete document locators and excerpts.
- `ClaimCluster` groups support and contradiction across repeated claims so downstream consumers can dedupe a development without treating every article as a new independent truth signal.
- `SnapshotManifest` seals the exact fact, claim, event, and source references that support an answer or finding at a specific `as_of`.

### Invariants

- Documents are evidence, not truth.
- Claims are assertions, not truth.
- Facts and computations back displayed values.
- Findings are product artifacts built from snapshots over the evidence graph.
- Facts are immutable except through supersession or explicit invalidation.
- Verification status must remain attached to facts so downstream services can distinguish authoritative values from candidate or disputed values.

## Downstream Consumer Matrix

### Fundamentals service

Fundamentals consumes `Metric`, `Fact`, and `Computation` as the canonical value layer. It may read claims and events for explanatory context, but it must not treat raw document text or unresolved claims as displayed truth.

### Evidence extraction platform

Evidence extraction owns `Source`, `Document`, `Mention`, `Claim`, `ClaimArgument`, `ClaimEvidence`, `ClaimCluster`, `Event`, and `EntityImpact`. Its responsibility is to convert raw documents into structured evidence and candidate truth inputs, not into final user-facing value objects.

### Home feed

Home feed consumes `Finding`, `SnapshotManifest`, and `ClaimCluster` as the deduped product artifact layer. Feed items should represent snapshotted developments rather than raw documents or ungrouped claims.

### Agent findings

Agent workflows consume `SnapshotManifest`, `Finding`, `RunActivity`, `ClaimCluster`, and `EntityImpact`. Agents may reason over claims and events, but their persisted outputs must be snapshotted findings with subject refs and evidence-backed support.

### Raw-content boundary

Reader and extraction flows may ingest raw documents. Analyst and user-facing flows must operate on structured facts, claims, events, snapshots, findings, and evidence bundles rather than raw untrusted text.

## Normative File Changes

### `spec/finance_research_spec.md`

- Add a truth-and-evidence role rules subsection beneath the metrics and evidence model sections.
- Add downstream consumer rules describing how fundamentals, extraction, Home, and agent findings are allowed to consume these objects.

### `spec/finance_research_openapi.yaml`

- Add descriptive schema text to `Fact`, `Claim`, `Event`, `SnapshotManifest`, and `Finding` clarifying their intended roles and the truth/evidence boundary.

### `spec/finance_research_db_schema.sql`

- Add schema comments near the fact, claim, event, snapshot, and finding tables clarifying provenance, supersession, verification-status, and snapshot-backed finding expectations.

### `tests/contracts/test_truth_evidence_finding_contract.py`

- Add a file-based contract test that asserts the required section headings and exact wording anchors exist across the normative files.

## Acceptance Mapping

- Explicit truth and evidence object roles satisfy the contract boundary for `stock-agent-h3e.1.1.2`.
- Provenance, supersession, and verification-status rules unblock statement normalization (`P1.2`) and promotion/extraction work in `P3`.
- Finding and snapshot consumer rules unblock Home feed (`P4.4`) and agent findings (`P5.3`).
- The raw-content boundary note preserves the downstream expectation for `PX.1`.
