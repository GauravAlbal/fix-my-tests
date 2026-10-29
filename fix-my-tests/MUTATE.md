# Fix My Tests — mutate step v0.7.0

Status: public. This is the **only** file that authorises writing to the target repository, and only after every precondition below is met. Everything else in this pack is read-only.

## Preconditions (all of them)

1. A diagnosis sitting is complete: bounded risk register, capability derivation, qualification per test, portfolio status.
2. The operator has granted mutation explicitly, in their own words, naming the scope. A request to "look at the tests" is not a grant.
3. The first-repair exit permits it:

| Sit exit | First move |
| --- | --- |
| `CLEANUP_READY` | `D`/`C`; `A` only if subtraction exposes a gap |
| `TESTS_NEED_REPAIR` | `F` before volume `A` |
| `EVIDENCE_GAPS_FIRST` | `A` on hard invariants; `D` only with `unique_evidence_lost_if_removed: none` |
| `INSTRUMENTS_FIRST` | harness `F`; no portfolio `D`/`A` until interpretable |
| `BINDING_FIRST` | bind existing `QUALIFIED`; no duplicate `A` |
| `MINIMUM_FLOOR_NEEDED` | `A` floor only; no deletion campaign |
| `NEEDS_MORE_EVIDENCE` / `NO_MATERIAL_CHANGE` | **do not mutate** |

Missing any precondition: return to diagnosis. Do not mutate to make the report come out even.

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

One tranche at a time, small enough to review:

1. Record HEAD.
2. Apply `D`/`C`, then `F`, then `A`, in that order — subtracting first means added tests are not carrying the weight of tests that were only pretending to.
3. Run the repo's verify command.
4. Report: what was removed, what each removal's unique evidence was and where it now lives, and what was added.

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

- Never delete a test to clear a failure. A red test may be reporting a product bug: reproduce it, and repair the owner.
- Never delete a test whose `unique_evidence_lost_if_removed` is `UNKNOWN`. Unknown is not none.
- Never add a replacement test whose only purpose is to justify a delete.
- Never edit production behaviour to make a test deletable, beyond removing test-only seams the deletion genuinely unlocked.
- Hard invariants are noncompensatory: a `HARD_INVARIANT` gap must receive a keeper in the same tranche as any delete of its false owners.
- Never optimise for deletion count.

## Non-claims

This step does not establish that the repository is safe, that the remaining suite is complete, or that removed coverage was worthless — only that the evidence named in the ledger moved to a keeper that demonstrably fails when the contract breaks.
