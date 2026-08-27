# Fix My Tests — verification map

Use after a sitting when the operator needs an implementation-ready evidence plan. One row per material bad outcome; never one row per existing test file.

## Identity

```yaml
repo:
revision:
operator_ask:
risk_discovery_scope: BOUNDED | BROAD | UNKNOWN
portfolio_prevalence: ESTABLISHED | NOT_ESTABLISHED
```

## Risk-to-evidence map

| Risk | Product surface | Bad outcome | Obligation | Positive claim / invariant | Failure mechanism | Required evidence capability | Drive recipe | Oracle | Receipt / provenance | Cadence / binding | Current status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RA- |  |  | HARD_INVARIANT / MATERIAL / DEFERRED / UNKNOWN |  |  |  | exact inputs, fault, schedule, or external interaction | authority that can distinguish right from wrong | revision, environment, command/probe identity, result | MANUAL / EVERY_CHANGE / MERGE / RELEASE / NIGHTLY / LIVE / OTHER | COVERED / UNDERCOVERED / GAP / INVALID / REDUNDANT / DEFERRED / UNKNOWN |

## Row laws

1. The product surface and bad outcome come before the current test.
2. Hard invariants are noncompensatory.
3. Derive the method from the failure mechanism; `unit`, `integration`, and `e2e` alone are insufficient.
4. The drive recipe must say what is actually exercised. A mock cannot establish a real-seam claim.
5. The oracle must name the authority that can distinguish correct from incorrect behavior.
6. The receipt must bind result to revision and current execution. A remembered green is not current evidence.
7. Required unavailable evidence remains explicit. It never becomes implicit success.
8. No health score. No additive confidence total. No model-consensus authority.

## Required unavailable evidence

| Risk | Missing capability | Why unavailable now | Effect on decision | Smallest way to obtain it |
| --- | --- | --- | --- | --- |
| RA- |  |  | BLOCKS / LIMITS / DOES_NOT_BLOCK — why |  |

## First implementation tranche

Select only rows that control a hard invariant or materially change the operator's next decision.

| Priority | Risk | Change | Acceptance criterion | Explicit non-goal |
| --- | --- | --- | --- | --- |
| 1 | RA- |  | observable red-before/green-after or live receipt |  |

## Completion boundary

```yaml
implemented_rows:
unimplemented_rows:
deferred_rows:
current_execution_receipts:
operator_claim_supported:
operator_claim_not_supported:
```
