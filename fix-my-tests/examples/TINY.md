# Worked example: what comes back

A synthetic two-file repo, so the shape is visible without you running anything. It is small on purpose: the same shape holds at 500 test files, it is just longer.

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

Three tests, all green. This is the state the skill is asked about: *"something about my tests feels wrong."*

---

## What it derives before looking at the tests

| Risk | Product surface | Material bad outcome | Obligation |
|---|---|---|---|
| RA-01 | `charge(event)` — the payment entry point | A retried webhook charges the customer twice | `HARD_INVARIANT` |
| RA-02 | `verify_signature` gate | An unsigned payload grants a paid entitlement | `HARD_INVARIANT` |

Both come from reading the production code, not the tests. Existing tests never define the risk model.

## Evidence capability, from the failure mechanism

| Risk | Failure mechanism | Capability that could expose it |
|---|---|---|
| RA-01 | Duplicate `event.id` reaches `ledger.insert` | Deliver the same event twice, assert one ledger row **and** one charge |
| RA-02 | Signature check bypassed or skipped | Deliver an unsigned payload, assert no ledger row and no charge |

## Qualification of the evidence that exists

| EV | Risk | Test | What it actually asserts | Oracle independent? | Qualification |
|---|---|---|---|---|---|
| EV-01 | RA-01 | `test_charge_calls_stripe` | that a mock was called | **no** — the assertion is about the mock the test installed | `UNQUALIFIED` — common-mode change detector |
| EV-02 | RA-01 | `test_duplicate_delivery_no_second_row` | one ledger row after two deliveries | **yes** — the unique key is the claim, not recomputed from `charge()` | `QUALIFIED` for RA-01 |
| EV-03 | — | `test_handler_exists` | that a function exists | n/a | `UNQUALIFIED` — hollow, verifies nothing |
| EV-04 | RA-02 | (none) | — | — | `GAP` |

## Portfolio

```text
RA-01  COVERED        (EV-02)
RA-02  GAP            no test can fail if the signature check is removed
```

## The two lists

```text
failures nothing would catch   RA-02  unsigned payload grants entitlement
tests that protect nothing     EV-01  test_charge_calls_stripe
                               EV-03  test_handler_exists
```

Note what EV-01 is not. It is green, deterministic, and it would fail if `stripe.charge` stopped being called — so it is a real test. It simply cannot distinguish *correct* from *incorrect* for RA-01, because its expected answer comes from the same mock arrangement it is judging.

## First moves (max 5, ordered)

1. `ADD_EVIDENCE` for RA-02 — one unsigned payload, assert no ledger row.
2. `KEEP` EV-02, and confirm it fails when the unique key is dropped.
3. `DELETE_CANDIDATE` EV-03.
4. `DELETE_CANDIDATE` EV-01 — or keep it as a wiring check and stop counting it as payment evidence.
5. Re-run the portfolio: RA-02 should move `GAP` → `COVERED`.

## First-repair exit

```text
EVIDENCE_GAPS_FIRST
```

The material next action is not "write more tests". It is to close the one gap where no evidence exists, because no quantity of local tests converts into evidence for an invariant nobody checks.

## What it refuses to say

- No coverage percentage and no health score. A suite can be 90% covered and `GAP` on the risk that ends the company.
- No claim that the repository is safe, and no claim that the analysis saw everything it did not open.
- It does not modify the repository. Dispositions are recommendations; `DELETE_CANDIDATE` is a name for a decision you make, not an action taken.
