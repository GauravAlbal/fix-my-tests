# Case: 5,747 tests that cannot answer the business question

**Repository:** a real, AI-written production app (wedding seating charts — Stripe checkout, Clerk identity, Fly deploys)
**Measured at:** `79f96ee3`, on the working tree as it stands
**What it is:** the app the agent wrote, and the suite the agent wrote for it. Neither was a toy. The failure here is not a small or careless suite.

---

## The pile, measured

```text
test files          539
test cases        5,747
assertions        15,984
weak assertions     128   (0.8% — toBeTruthy / toBeDefined / not.toThrow)
e2e files            72
```

This is not a suite of hollow placeholders. 16,000 assertions is a suite someone spent real effort on, and the assertions are specific — table assignments, seating rules, tone classes, cookie writes, UA classes. By the numbers that usually get quoted (coverage, test count, green/red), it looks strong.

## And yet

The product risks that decide whether this app works are:

| Risk | What would have to be true | Status | Why |
|---|---|---|---|
| RA-01 | A real payment completes and the webhook subscribes | `GAP` | no test reaches live Stripe; local fakes cannot cover a hard invariant |
| RA-02 | Refunds and disputes are handled | `GAP` | no live path exercised |
| RA-03 | Real Clerk JWKS verification | `GAP` | adversarial coverage exists against a fixture, not the live issuer |
| RA-05 | Data survives a Fly volume loss | `GAP` | no restore drill; local sqlite backup/restore is a different claim |
| RA-06 | A customer can return to their purchase from a public URL | `GAP` | the Playwright run recorded failure (stale provenance) |
| RA-07 | Two browsers see the same chart on Fly | `GAP` | single-browser local evidence only |

Every one of those is the kind of thing a wedding planner discovers on a Saturday with 180 guests seated.

## The detail that makes it legible

The suite's only production-facing check is opt-in, and it is green when unconfigured:

```text
scripts/run_wedding_live_smoke_gate.sh
  → runs only when WEDDING_LIVE_SMOKE is set
  → with it unset: exit 0, nothing exercised
```

That is `SKIP_AS_GREEN`, and it is worse than no test, because a missing test is honest about being missing. The sitting that audited this app also found `test-results/.last-run.json` recording a **failed** Playwright run under RA-06 — the repo's own receipt for its end-to-end check said failure while the suite as a whole read green. That file is not present at the revision measured here, so it is recorded as the sitting's finding, not as a current fact.

## What the diagnosis returned

```text
dominant problem:  REAL_SEAM_UNTESTED  (RA-01, RA-02, RA-03, RA-07)
                   WRONG_METHOD        (local persistence tests vs a durability claim)
                   SKIP_AS_GREEN       (live smoke gate)
                   STALE_PROVENANCE    (e2e last run failed)
first-repair exit: EVIDENCE_GAPS_FIRST
```

Not "write more tests". The material next action was to **stop adding local volume and go prove the live seams** — one real checkout, one real refund, one restore from a Fly snapshot — because no quantity of local tests can convert into evidence for a live-seam invariant.

## Why this one is worth telling

Because it is the normal outcome, not the pathological one. A capable agent wrote a large, careful, assertion-dense suite; every assertion is defensible; and the suite is still pointed at the wrong question, because tests are written from the code that exists rather than from the failures that matter.

> 5,747 tests, and not one of them could tell you whether a payment went through.

## Scope

Measured on the operator's own application, read-only, at the revision above. Counts are reproducible with the grep/find commands in this note's history. The sitting that produced the risk table is `agent-skills-internal/dogfood/fix-my-tests-v0.5/AI_GENERATED_APP.md`, which explicitly claims no defect reduction and no safety — only that the diagnosis was bounded and changed a material next action.
