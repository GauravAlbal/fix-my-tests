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
  version: "0.7.0"
---

# Fix My Tests

## Moment

Something about this repository's tests feels wrong, or the operator needs to know what must be tested before trusting the software.

## Governing question

What product risks deserve evidence here, what capability can expose each failure mechanism, what do current tests qualify as evidence for, and what is the smallest trustworthy portfolio appropriate to this repository?

## Read-only

This pack diagnoses. It does not edit, delete, add, or move a test, and it does not touch production code. Dispositions (`KEEP`, `FIX_*`, `ADD_EVIDENCE`, `DELETE_CANDIDATE`) are recommendations for the operator to act on, named so the decision is explicit rather than implied.

## Required references

Read and obey the sibling files in this order:

1. `RISK_METHOD_MATRIX.md` — governing risk, failure-mechanism, oracle-independence, and evidence-method law.
2. `PROTOCOL.md` — bounded analysis procedure and decision contracts.
3. `SIT.md` — output contract.
4. `RUN_PROMPT.md` — full execution constraints.

Load later, only when the question calls for it:

| When | File |
| --- | --- |
| a disposition is contested | `PRINCIPLES.md` (hot 6 first) |
| the operator wants an implementation-ready risk-to-evidence plan after diagnosis | `VERIFICATION_MAP.md` |
| the output shape is unclear, or they ask what a diagnosis looks like | `examples/TINY.md` |

## Cold analysis (parent and children)

This sitting starts ignorant. **You** (this chat) and every subagent:

- Open current production, test, and instrument bytes before claiming what they do.
- Do not assume production works, matches its name/docs, or implements the claimed behaviour.
- Do not assume a test is valid, unique, mapped, or measures that claim because it exists, is green, is named well, or a child/parent said so.
- Do not assume pytest, coverage, CI, or a probe is a **normative** oracle for the claim until this sitting shows what it actually asserts and executes.
- Memory, prior sittings, training, and summaries are not evidence. Unread path → `UNKNOWN`.

**Fan-out.** Independent files may be read by children in parallel; their reports are hypotheses. The parent re-opens at least one production file and, for every test-controlling mark, **that test**. `QUALIFIED`, `KEEP`, or any disposition on a test requires parent-opened bytes for that test. Examined absence (`existing_tests: none` after a search this sitting) is not unread. Other child-cited paths stay `UNKNOWN`.

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

Existing tests never define the risk model. A green result from unqualified evidence has no authority for the claim. Hard invariants cannot be offset by other passing tests.

A test whose expected answer is materially derived from the same implementation may be a common-mode change detector rather than independent correctness evidence. A captured baseline may establish preservation when preservation is the named claim; it does not prove the captured behavior was correct by itself.

## Exit

Fill `SIT.md`, answer the operator's actual question at an explicit evidence boundary, name at most five first moves, choose exactly one first-repair exit, and stop. Do not modify the target repository. Do not claim the repository is safe.
