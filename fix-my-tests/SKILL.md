---
name: fix-my-tests
description: >
  Use when a repository's tests feel missing, hollow, flaky, slow, redundant,
  over-mocked, implementation-coupled, or wired to the wrong decision, or when
  AI-generated tests are green but you do not know what they actually prove.
  Derive product risks before inspecting the suite, assign evidence methods from
  failure mechanisms, qualify current evidence including oracle independence,
  and return the smallest trustworthy portfolio plus a bounded first repair.
  Read-only diagnosis only.
license: CC-BY-4.0
metadata:
  author: Gaurav Albal
  version: "0.6.0"
---

# Fix My Tests

## Moment

Something about this repository's tests feels wrong, or the operator needs to know what must be tested before trusting the software.

## Governing question

What product risks deserve evidence here, what capability can expose each failure mechanism, what do current tests qualify as evidence for, and what is the smallest trustworthy portfolio appropriate to this repository?

## Required references

Read and obey the sibling files in this order:

1. `RISK_METHOD_MATRIX.md` — normative risk, failure-mechanism, oracle-independence, and evidence-method law.
2. `PROTOCOL.md` — bounded analysis procedure and decision contracts.
3. `SIT.md` — output contract.
4. `RUN_PROMPT.md` — full execution constraints.

Load `VERIFICATION_MAP.md` only when the operator needs an implementation-ready risk-to-evidence plan after the diagnostic sitting.

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

A test whose expected answer is materially derived from the same implementation may be a common-mode change detector rather than independent correctness evidence. A captured baseline may establish preservation when preservation is the named claim; it does not prove the captured behavior was correct by itself.

## Exit

Fill `SIT.md`, answer the operator's actual question, choose exactly one first-repair exit, and stop. Do not modify the target repository. Do not claim the repository is safe.
