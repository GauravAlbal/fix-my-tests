# Worked example: what comes back

A synthetic two-file repo, so the shape is visible without you running anything. It is small on purpose: the same shape holds at 500 test files, it is just longer.

**Instructional assumptions.** This is not a real repository and was not executed. There is no run receipt, no pytest output, and no provider statement. Copy the *shape*, not the product names. Qualifications below follow from the source bytes printed here, under the fixture assumptions stated with EV-02.

---

## The repo

```text
bill.py
tests/test_bill.py
```

`bill.py`:

```python
def charge(event):
    verify_signature(event)                      # raises on bad signature
    ledger.insert(event.id, amount=event.amount)  # unique key on event.id
    stripe.charge(event.amount)
```

`tests/test_bill.py`:

```python
def test_handler_exists():
    assert charge

def test_charge_calls_stripe(mocker):
    stripe = mocker.patch("bill.stripe")
    charge(valid_event())
    assert stripe.charge.called

def test_duplicate_delivery_no_second_row(ledger):
    charge(valid_event())      # same event.id twice
    charge(valid_event())
    assert len(ledger.rows) == 1
```

Three tests, all described as green in this illustration. This is the state the skill is asked about: *"something about my tests feels wrong."*

---

## What it derives before looking at the tests

Ledger uniqueness, external charging, and crash effects are **separate** obligations. One unique ledger row can coexist with two charges; sequential deliveries do not exercise crash/recovery.

| Risk | Product surface | Material bad outcome | Obligation |
|---|---|---|---|
| RA-01 | `charge(event)` — the payment entry point | A retried webhook **charges the customer twice** | `HARD_INVARIANT` |
| RA-02 | `verify_signature` gate | An unsigned payload grants a paid entitlement | `HARD_INVARIANT` |
| RA-03 | `ledger.insert` then `stripe.charge` | A crash between recording and charging leaves them disagreed | `HARD_INVARIANT` |

Both come from reading the production code, not the tests. Existing tests never define the risk model.

A distinct **recording** claim is also visible: repeat signed delivery must not insert a second ledger row. That is not RA-01.

## Evidence capability, from the failure mechanism

| Risk | Failure mechanism | Capability that could expose it |
|---|---|---|
| RA-01 | Duplicate `event.id` reaches `stripe.charge` twice | Deliver the same signed event twice; assert **one external charge** (provider receipt or idempotency record), not merely one ledger row |
| RA-02 | Signature check bypassed or skipped | Deliver an unsigned payload; assert no ledger row and no charge |
| RA-03 | Process dies after insert, before charge | Inject crash/restart after insert; assert recording and charging either both happened once or neither |

Ledger uniqueness, if claimed on its own, needs two signed deliveries and **one ledger row**, with a fixture that *can* hold two rows.

## Qualification of the evidence that exists

| EV | Risk | Test | What it actually asserts | Oracle independent? | Qualification |
|---|---|---|---|---|---|
| EV-01 | RA-01 | `test_charge_calls_stripe` | that a mock was called | **this assertion** is about the mock the test installed | `UNQUALIFIED` — common-mode for this charging claim |
| EV-02 | RA-01 | `test_duplicate_delivery_no_second_row` | one ledger row after two deliveries | **yes for ledger recording** — the unique key is that claim, not recomputed from `charge()` | `QUALIFIED` for **ledger recording only**. Does not qualify RA-01. |
| EV-03 | — | `test_handler_exists` | that a function exists | n/a | `UNQUALIFIED` — hollow, verifies nothing |

No EV row for RA-02 or RA-03: missing tests are not invented. Those gaps live on the risk/portfolio rows.

**Why EV-02 is qualified for recording, and how easily it wouldn't.** Its assertion is only real if the ledger *can* express the failure. Built as a list with a duplicate guard, removing the guard would yield two rows. Built as a dict keyed by `event.id`, the same assertion cannot fail — a dict cannot hold two rows for one key, so it would measure the data structure, not the recording behaviour. That contrast is an instructional illustration, not a run receipt.

EV-01 is a real, deterministic check that would fail if `stripe.charge` stopped being called. It still cannot distinguish *correct* from *incorrect* charging, because its expected answer comes from the same mock arrangement it is judging. That is a fact about **this** assertion. Mocks are not inherently common-mode: a mock that carries an independently specified oracle, and is not itself the thing under judgment, can still be evidence.

## Portfolio

```text
RA-01  UNDERCOVERED   EV-02 establishes ledger uniqueness only; one row ≠ one charge
RA-02  GAP            no test exists (gap is this row, not an EV-)
RA-03  GAP            no crash/recovery evidence
recording uniqueness  COVERED by EV-02 (not RA-01), under the list-fixture assumption above
```

RA-01 is **not** `COVERED`. Ledger-only evidence cannot close a double-charge risk.

## The two lists

```text
failures nothing would catch   RA-01  retried webhook charges twice
                               RA-02  unsigned payload grants entitlement
                               RA-03  crash between ledger and charge
tests that protect nothing     EV-01  test_charge_calls_stripe (as charging evidence)
                               EV-03  test_handler_exists
```

## First moves (max 5, ordered)

1. `ADD_EVIDENCE` for RA-01 — two signed deliveries, assert one **external** charge.
2. `ADD_EVIDENCE` for RA-02 — one unsigned payload, assert no ledger row and no charge.
3. `KEEP` EV-02 as ledger-recording evidence; do not count it as RA-01 coverage.
4. `DELETE_CANDIDATE` EV-03.
5. `DELETE_CANDIDATE` EV-01 — or keep it as a wiring check and stop counting it as payment evidence.

## First-repair exit

```text
EVIDENCE_GAPS_FIRST
```

The material next action is not "write more tests". It is to close the charging and signature gaps, because a qualified ledger-row check does not convert into at-most-once charging.

## What it refuses to say

- No coverage percentage and no health score. A suite can be 90% covered and `GAP` on the risk that ends the company.
- No claim that the repository is safe, and no claim that the analysis saw everything it did not open.
- This example is **diagnosis**. It does not modify the repository. Dispositions are recommendations; `DELETE_CANDIDATE` is a name for a decision you make, not an action taken. Mutation needs an explicit `prune` / `add` / `prune_and_add` grant.
- No run receipt exists for this illustration.
- No claim that every mock is common-mode.
