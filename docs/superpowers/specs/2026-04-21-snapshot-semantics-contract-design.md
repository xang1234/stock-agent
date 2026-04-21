# Snapshot Semantics Contract Design

## Goal

Define the snapshot-semantics boundary so chat, analyze, verifier, and renderer work all depend on the same rules for what a sealed snapshot contains, which transforms stay in-snapshot, and which requests require refresh or a new run.

## Scope

This design covers:

- the normative snapshot-manifest contract in `spec/finance_research_spec.md`
- the fields and bindings a sealed snapshot must pin
- the rule for when a transform is legal inside an existing snapshot
- the explicit boundary between in-snapshot interaction and refresh or new-run behavior
- the downstream consumers named in the bead acceptance criteria
- a file-based contract test that locks the required wording in place

This design does not introduce a new snapshot schema artifact, redesign transport, or redefine the block registry. It clarifies the product-logic boundary already implied by the current spec.

## Core Contract

### Normative source of truth

- `spec/finance_research_spec.md` remains the normative source for snapshot semantics.
- Snapshot semantics are product rules, not transport trivia and not renderer-local behavior.
- The renderer, chat runtime, and verifier must all treat the sealed manifest as the authority for what data and interactions are legal.
- A later bead may add a dedicated snapshot-manifest schema, but this contract should not invent one early and split the source of truth.

### Sealed snapshot manifest

- A sealed snapshot pins the subject set, `as_of`, basis, normalization, coverage window, source set, bound fact or claim or event refs, and exact `allowed_transforms`.
- The manifest is the boundary between evidence-backed output and free-floating presentation state.
- Persisted chat and analyze artifacts must continue to point at that sealed snapshot rather than reconstructing support opportunistically later.
- `allowed_transforms` is explicit manifest state, not a UI guess derived from block kind alone.

### Sealing and persistence rules

- Snapshot sealing happens only after binding and disclosure verification.
- Once sealed, the snapshot is the evidence and freshness envelope for the rendered artifact.
- Message persistence, findings, and shared analysis artifacts must preserve the snapshot binding rather than copying only rendered prose or chart state.
- Earlier narrative and later interactive views must remain consistent because they are bound to the same sealed manifest.

### In-snapshot transforms

- A transform is legal inside a sealed snapshot only when it preserves the subject set and does not require fresher evidence than `as_of`.
- In-snapshot transforms may change presentation or range only when the required rows or series are already inside the sealed data boundary.
- Time-range changes such as `YTD` to `1Y` are allowed only when the requested range end stays less than or equal to `as_of`.
- The manifest, not the client, determines whether a transform is allowed.

### Refresh and new-run boundary

- Any request that changes subject membership, peer set, basis, normalization, or freshness crosses the snapshot boundary.
- Requests for fresher data, different peers, different basis, or different normalization require refresh or a new run.
- The system must treat those requests as explicit boundary crossings instead of silently mutating a sealed answer.
- This boundary is the guardrail that prevents narrative drift between the original answer and later interactive views.

## Downstream Consumer Matrix

### Block registry versioning and validation (`P2.3`)

Block registry and validation work depends on snapshot rules being stable enough to know which interactions are legal within existing block bindings and which require a new backend result.

### Snapshot assembler and verifier (`P2.4`)

Assembler and verifier work depends on the sealed manifest contents, sealing order, and refresh boundary to prove that rendered blocks still correspond to the same evidence-backed snapshot.

### Shared artifact flow (`P4.3`)

Analyze-to-chat artifact sharing depends on sealed snapshots remaining reusable product artifacts. Importing or replaying an artifact must preserve its original snapshot boundary rather than silently widening it.

### Frontend renderer (`PX.3`)

Frontend rendering depends on a clear rule that presentation-only interactions may stay local only when they remain inside the sealed snapshot contract. Any data-bearing or freshness-crossing interaction must go back through backend snapshot APIs.

## Interaction Rules

- Interactivity stays inside snapshot scope unless the user explicitly refreshes.
- Clients may perform presentation-only transforms locally when the needed data is already present and the manifest permits the transform.
- Clients must not infer permission for a transform from UI affordances alone.
- Data-bearing transforms remain backend-mediated even when the interaction starts from a rendered block.
- The contract rejects silent refresh: crossing the snapshot boundary must be explicit in product behavior.

## Normative File Changes

### `spec/finance_research_spec.md`

- Expand `## 10. Snapshot semantics` so the sealed manifest fields, sealing rule, allowed-transform boundary, and refresh triggers are explicit.
- Add explicit downstream consumer notes for block validation, snapshot verification, shared artifacts, and frontend rendering.

### `tests/contracts/test_snapshot_semantics_contract.py`

- Add a file-based contract test that asserts the required snapshot, transform, and refresh wording anchors exist in the narrative spec.

## Acceptance Mapping

- The sealed-manifest definition satisfies the acceptance requirement around snapshot manifest semantics.
- The in-snapshot transform rules satisfy the acceptance requirement around allowed transforms and transform limits.
- The refresh-boundary rules satisfy the acceptance requirement around explicit refresh triggers and out-of-snapshot behavior.
- The consumer matrix unblocks `P2.3`, `P2.4`, `P4.3`, and `PX.3`.
