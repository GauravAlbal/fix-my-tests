---
name: fix-my-tests
description: >
  Use when a repository's tests feel missing, hollow, flaky, slow, redundant,
  over-mocked, or wired to the wrong decision, or when a vibe-coded project is
  approaching production and the operator asks what must be tested. Derive
  product risks before inspecting the suite, assign evidence methods from
  failure mechanisms, qualify current evidence, and return the smallest
  trustworthy portfolio plus a bounded first repair. Read-only diagnosis only.
metadata:
  author: Gaurav Albal
  version: "0.5.0"
---

# Fix My Tests

## Moment

Something about this repository's tests feels wrong, or the operator needs to know what must be tested before trusting the software.

## Governing question

What product risks deserve evidence here, what capability can expose each failure mechanism, what do current tests qualify as evidence for, and what is the smallest trustworthy portfolio appropriate to this repository?

## Required references

Read and obey the sibling files in this order:

1. `RISK_METHOD_MATRIX.md` — normative risk and evidence-method law.
2. `PROTOCOL.md` — bounded analysis procedure and decision contracts.
3. `SIT.md` — output contract.
4. `RUN_PROMPT.md` — full execution constraints.

## Non-negotiable order

```text
PRODUCT SURFACE
→ MATERIAL BAD OUTCOME
→ CLAIM / HARD INVARIANT
→ FAILURE MECHANISM
→ REQUIRED EVIDENCE CAPABILITY
→ EXISTING EVIDENCE
→ QUALIFICATION
→ PORTFOLIO STATUS
```

Existing tests never define the risk model. A green result from unqualified evidence has no authority for the claim. Hard invariants are noncompensatory.

## Exit

Fill `SIT.md`, answer the operator's actual question, choose exactly one first-repair exit, and stop. Do not modify the target repository. Do not claim the repository is safe.
