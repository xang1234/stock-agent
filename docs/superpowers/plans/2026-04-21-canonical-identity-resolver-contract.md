# Canonical Identity Resolver Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the deterministic resolver responsibilities, typed resolution-envelope outcomes, accepted input families, and ambiguity rules explicit in the narrative spec so later search, market-data, fundamentals, screener, and chat-routing work shares one stable resolver contract.

**Architecture:** Treat this bead as a narrative contract-pack update, not a resolver algorithm or search-flow implementation. Add a small file-based contract test that asserts the required resolver responsibility, envelope, ambiguity, and downstream-consumer wording exists, watch it fail first, then patch the narrative spec so the resolver contract is explicit and internally consistent with the identity model and service-boundary sections.

**Tech Stack:** Markdown spec, Python 3 `unittest`

---

## File Structure

- Modify: `spec/finance_research_spec.md`
  Responsibility: narrative resolver rules near the identity and service-boundary sections, including deterministic resolver responsibilities, typed resolution-envelope outcomes, accepted input families, ambiguity-preservation rules, and downstream consumer notes.
- Create: `tests/contracts/test_canonical_identity_resolver_contract.py`
  Responsibility: file-level contract checks enforcing the required resolver responsibility, envelope, ambiguity, and downstream-consumer wording anchors in the narrative spec.

### Task 1: Add failing resolver contract checks

**Files:**
- Create: `tests/contracts/test_canonical_identity_resolver_contract.py`
- Test: `tests/contracts/test_canonical_identity_resolver_contract.py`

- [ ] **Step 1: Write the failing test**

```python
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"


class CanonicalIdentityResolverContractTest(unittest.TestCase):
    def test_spec_declares_resolver_responsibilities_and_typed_envelope(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 6.1 Identity and resolver service", spec_text)
        self.assertIn(
            "The resolver is the deterministic boundary that converts user-entered lookup input and provider-origin identity records into canonical finance identity outputs.",
            spec_text,
        )
        self.assertIn(
            "The resolver owns normalization, candidate generation, canonical reference selection when unambiguous, and explicit ambiguity preservation when multiple canonical targets remain plausible.",
            spec_text,
        )
        self.assertIn(
            "The resolver is distinct from search UI, user disambiguation flow, and downstream subject hydration.",
            spec_text,
        )
        self.assertIn(
            "The contract defines a typed resolution envelope rather than an untyped candidate list.",
            spec_text,
        )
        self.assertIn(
            "`resolved` means the resolver can name one canonical target confidently enough for deterministic downstream use.",
            spec_text,
        )
        self.assertIn(
            "`ambiguous` means multiple canonical issuer, instrument, listing, or `SubjectRef` targets remain plausible after normalization and matching, so the resolver must return ranked candidates without silently picking one.",
            spec_text,
        )
        self.assertIn(
            "`not_found` means the resolver could normalize the input but could not map it to a supported canonical target.",
            spec_text,
        )

    def test_spec_declares_input_families_and_ambiguity_rules(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn(
            "The contract explicitly covers two input families: user-entered lookup text and provider-origin identity records.",
            spec_text,
        )
        self.assertIn(
            "User-entered lookup text includes ticker-like strings, issuer names, aliases, and other concise finance lookup inputs.",
            spec_text,
        )
        self.assertIn(
            "Provider-origin identity records include external ids and structured provider payload fields such as ticker, exchange, CIK, ISIN, or other identifier-bearing records.",
            spec_text,
        )
        self.assertIn(
            "The resolver may start from ticker or alias lookup, but downstream output must promote that lookup into explicit issuer, instrument, listing, or `SubjectRef` candidates.",
            spec_text,
        )
        self.assertIn(
            "Ticker-only identity remains insufficient because the same symbol can map to different listings, venues, or securities, and issuer-level workflows often need a different canonical target than market-data workflows.",
            spec_text,
        )
        self.assertIn(
            "The resolver should expose the ambiguity axis when possible, such as issuer-versus-listing ambiguity or multiple plausible listings for one ticker string.",
            spec_text,
        )
        self.assertIn(
            "Ranked candidates are advisory metadata, not permission to silently collapse ambiguity into one winner.",
            spec_text,
        )
        self.assertIn(
            "`resolved` should include the canonical identity level that was chosen so downstream systems know whether they received issuer, instrument, listing, or already-formed `SubjectRef` output.",
            spec_text,
        )

    def test_spec_declares_resolver_downstream_consumers(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 6.1.1 Downstream consumer rules", spec_text)
        self.assertIn(
            "Search-to-subject resolution flow (`P0.3b`) depends on the resolver outcome vocabulary it will carry through candidate search, user choice, and downstream subject hydration.",
            spec_text,
        )
        self.assertIn(
            "Market data service (`P1.1`) depends on the rule that quote and bar consumers must receive listing-appropriate canonical output rather than ticker strings or issuer-level guesses.",
            spec_text,
        )
        self.assertIn(
            "Fundamentals service (`P1.2`) depends on the rule that issuer-backed fundamentals cannot rely on ticker-only identity and must consume issuer-appropriate canonical output or preserved ambiguity.",
            spec_text,
        )
        self.assertIn(
            "Screener surface and saved-screen handoff depends on deterministic subject identity shapes even before later hydration flow is applied.",
            spec_text,
        )
        self.assertIn(
            "Pre-resolve router and budget policy (`P2.2`) depends on the rule that deterministic pre-resolve routing consumes resolver envelopes rather than asking the model to silently choose among ambiguous identity candidates.",
            spec_text,
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.contracts.test_canonical_identity_resolver_contract -v`
Expected: `FAIL` because the new resolver-envelope and downstream-consumer wording does not exist yet.

- [ ] **Step 3: Commit**

```bash
git add tests/contracts/test_canonical_identity_resolver_contract.py
git commit -m "test: add canonical identity resolver checks"
```

### Task 2: Patch the resolver contract in the narrative spec

**Files:**
- Modify: `spec/finance_research_spec.md`
- Test: `tests/contracts/test_canonical_identity_resolver_contract.py`

- [ ] **Step 1: Expand the identity and resolver service section with the deterministic resolver contract**

```md
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
```

- [ ] **Step 2: Replace the downstream consumer notes with the resolver-specific consumer matrix**

```md
### 6.1.1 Downstream consumer rules

- Search-to-subject resolution flow (`P0.3b`) depends on the resolver outcome vocabulary it will carry through candidate search, user choice, and downstream subject hydration.
- Market data service (`P1.1`) depends on the rule that quote and bar consumers must receive listing-appropriate canonical output rather than ticker strings or issuer-level guesses.
- Fundamentals service (`P1.2`) depends on the rule that issuer-backed fundamentals cannot rely on ticker-only identity and must consume issuer-appropriate canonical output or preserved ambiguity.
- Screener surface and saved-screen handoff depends on deterministic subject identity shapes even before later hydration flow is applied.
- Pre-resolve router and budget policy (`P2.2`) depends on the rule that deterministic pre-resolve routing consumes resolver envelopes rather than asking the model to silently choose among ambiguous identity candidates.
```

- [ ] **Step 3: Run the resolver contract test and confirm green**

Run: `python3 -m unittest tests.contracts.test_canonical_identity_resolver_contract -v`
Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add spec/finance_research_spec.md
git commit -m "docs: define canonical identity resolver contract"
```

### Task 3: Verify and land the bead

**Files:**
- Modify: `.beads/issues.jsonl` (via `bd close` / `bd sync`)
- Test: `tests/contracts/test_canonical_identity_resolver_contract.py`

- [ ] **Step 1: Inspect repo state**

Run: `git status --short`
Expected: only the intended spec, test, plan, and bead metadata changes remain, plus the known unrelated untracked baseline files.

- [ ] **Step 2: Close the bead**

Run: `bd close stock-agent-h3e.1.3.1 --reason "Completed"`
Expected: bead marked `closed`

- [ ] **Step 3: Sync bead metadata**

Run: `bd sync`
Expected: `.beads/issues.jsonl` updated for the closed bead state

- [ ] **Step 4: Re-run the resolver contract test after bead sync**

Run: `python3 -m unittest tests.contracts.test_canonical_identity_resolver_contract -v`
Expected: `OK`

- [ ] **Step 5: Commit bead metadata if needed**

```bash
git add .beads/issues.jsonl docs/superpowers/plans/2026-04-21-canonical-identity-resolver-contract.md
git commit -m "chore: sync bead status for stock-agent-h3e.1.3.1"
```

Only do this if `bd sync` changed tracked files that are not already committed.

- [ ] **Step 6: Publish the feature branch**

Run: `git push -u origin stock-agent-h3e.1.3.1`
Expected: remote branch updated successfully

- [ ] **Step 7: Fast-forward `main` and verify there**

Run: `git checkout main && git pull --rebase origin main && git merge --ff-only stock-agent-h3e.1.3.1 && python3 -m unittest tests.contracts.test_canonical_identity_resolver_contract -v`
Expected: fast-forward merge succeeds and the resolver contract test reports `OK`

- [ ] **Step 8: Push `main` and verify final status**

Run: `git push origin main && git status`
Expected: `main` is up to date with `origin/main`, with only the known unrelated untracked baseline files remaining

- [ ] **Step 9: Delete the local feature branch**

Run: `git branch -d stock-agent-h3e.1.3.1`
Expected: local feature branch deleted after the fast-forward merge
