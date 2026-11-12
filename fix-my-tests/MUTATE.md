# Fix My Tests — mutate step v0.7.1

Status: public. This file is the pack's **only** write-authority definition. Diagnosis default is read-only. Explicitly granted modes: `prune`, `add`, `prune_and_add`. Everything else in this pack is read-only.

## Preconditions (all of them)

1. A diagnosis sitting is complete: bounded risk register, capability derivation, qualification per test, portfolio status.
2. The operator has granted mutation explicitly, in their own words, naming the scope and one of `prune`, `add`, or `prune_and_add`. A request to "look at the tests" is not a grant.
3. Intersect **Grant × action** first. Then apply **Authorized actions → first mutation** for the sit's exit. Repair priority never mints permission.

Missing any precondition: return to diagnosis. Do not mutate to make the report come out even.

## Grant × action

Intersect permission **before** ordering by the diagnostic exit. Classify the actual effect, not just the mark; a disguised delete is still pruning.

| Grant | Allowed action | Not authorized |
| --- | --- | --- |
| `none` | read-only diagnosis/recommendations (`R` is observation, not a write) | all mutations |
| `add` | `A`; extend a keeper to add missing evidence while **preserving** its contracts | `C`/`D`, pruning, weakening/removing assertions, standalone unrelated `F` |
| `prune` | `C`/`D` subject to preservation; necessary `F` that carries existing contracts into a keeper without adding a new evidence obligation | `A`, new-risk coverage, unrelated repairs, broader product changes |
| `prune_and_add` | `A`/`F`/`C`/`D` on tests, oracles, and instruments within the sitting and original ask | production behavior change unless the operator named that owner and the intended behavior; unrelated work |

`R` retains without mutation under any grant.

`F` is not a permission wildcard: it is assertion/oracle/instrument repair. Standalone test-side `F` needs an explicit matching repair grant (or the broad “fix them” / `prune_and_add` grant). A narrow add/prune grant covers it only as a necessary part of that authorized action. A test grant — including `prune_and_add` and “fix them” — does **not** by itself authorize changing production behavior. Repair production behavior only within the original authorized ask (the operator named that owner and the intended behavior). A necessary seam repair that an authorized test action cannot proceed without (e.g. an injection point) is allowed; it must not change observable product behavior. Optional adjacent product fixes are never covered.

Add-only never removes or relaxes assertions. Prune-only never mints new-risk evidence or broadens product changes.

Urgency, a severe adjacent defect, and first-repair priority cannot expand authorization.

If safe pruning depends on a new `A` outside a prune-only grant, do not delete that owner. Record the dependency and the permission needed, and complete remaining independent authorized work. Add-only duplicate discovery is a recommendation, never a precondition authorizing deletion.

A real product defect is never erased by deleting its test. Reproduce it and **report** it. Repair the production owner only within the original authorized ask, not merely because a test grant exists. Do not delete or relax the failing test to go green.

## Authorized actions → first mutation

This is priority among **already authorized** actions, not a grant table.

| Sit exit | First move, if permitted |
| --- | --- |
| `CLEANUP_READY` | `D`/`C` if pruning granted; `A` only for an independently named gap with add authority |
| `TESTS_NEED_REPAIR` | authorized `F` before volume `A`; otherwise record repair outside grant |
| `EVIDENCE_GAPS_FIRST` | `A` on hard invariants if add granted; `D` only if prune granted and unique-lost=`none` |
| `INSTRUMENTS_FIRST` | authorized harness `F`; no portfolio `D`/`A` until interpretable |
| `BINDING_FIRST` | bind existing `QUALIFIED` only with matching authority; no duplicate `A` |
| `MINIMUM_FLOOR_NEEDED` | `A` floor only with add grant; no deletion campaign |
| `NEEDS_MORE_EVIDENCE` / `NO_MATERIAL_CHANGE` | **do not mutate** |

## Ledger marks

One mark per declaration, recorded read-only before any edit:

```text
R  retain — contract + the bug it catches; carries RA-/EV- ids
F  retain contract, repair assertion/oracle/instrument
C  consolidate into a named keeper; carry the assertions in the same unit
D  delete — requires remaining qualified proof and unique-lost = none
A  add — requires RA-, required capability, and boundary
```

Before writing, produce the ledger and let the operator see it. Fan out read-only research across independent owners; **one writer per file**.

## Tranche

One tranche at a time, small enough to review. Apply **only authorized** marks:

1. Record HEAD.
2. Among authorized work: apply `D`/`C`, then `F`, then `A`, in that order — subtracting first means added tests are not carrying the weight of tests that were only pretending to. Add-only skips `D`/`C`. Prune-only skips `A`.
3. Run the repo's verify command.
4. Report: what was removed, what each removal's unique evidence was and where it now lives, what was added, and which out-of-grant dependencies remain.

Stop after one tranche and report. Do not chain tranches inside one session unless the operator asks.

## Preservation proof (not optional)

A delete is only safe if the evidence it uniquely provided still exists somewhere that can fail:

```text
1. Record HEAD (or stash).
2. Change one production line the keeper's contract depends on.
3. Run VERIFY. The keeper MUST go red, for that reason.
   If it stays green, the keeper is hollow — restore and do NOT delete the old test.
4. Restore the line byte for byte.
5. VERIFY green; diff against step 1 shows no mutation left.
6. Never commit the mutated production line.
```

This step is what separates a prune from a gamble. Skipping it converts "these tests were redundant" into an assertion nobody checked.

## Hard rules

- Never delete a test to clear a failure. A red test may be reporting a product bug: reproduce it and report it; repair the production owner only within the original authorized ask (the operator named that owner and the intended behavior).
- Never treat a test grant, including `prune_and_add` or “fix them”, as production-behavior authority by itself.
- Never delete a test whose `unique_evidence_lost_if_removed` is `UNKNOWN`. Unknown is not none.
- Never add a replacement test whose only purpose is to justify a delete.
- Never edit production behaviour to make a test deletable, beyond removing test-only seams the deletion genuinely unlocked.
- Hard invariants are noncompensatory: a `HARD_INVARIANT` gap must receive a keeper in the same tranche as any delete of its false owners — and only when add is granted. Under prune-only, leave those false owners in place and report the missing add grant.
- Never optimise for deletion count.
- Never treat `F` as a wildcard around add-only or prune-only.
- Never let an urgent exit (`EVIDENCE_GAPS_FIRST`, `TESTS_NEED_REPAIR`, …) widen the grant.

## Non-claims

This step does not establish that the repository is safe, that the remaining suite is complete, or that removed coverage was worthless — only that the evidence named in the ledger moved to a keeper that demonstrably fails when the contract breaks.
