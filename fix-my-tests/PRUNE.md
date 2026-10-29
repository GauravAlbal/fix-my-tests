# Fix My Tests — prune procedure v0.7.0

Status: public. Load only from `MUTATE.md`, after a diagnosis sitting and an explicit prune grant. This file governs deleting tests. It never
authorises deleting production behaviour.

## Retention bar

Keep independent public API, SDK, protocol, config, migration, storage, security, platform, default, prompt-byte, generated-language, package, release, architecture, and observable-ordering contracts. Keep credible regressions.

Static or slow ≠ disposable. Source inspection is valid only when it is the cheapest independent guard of a user-facing key/byte/path **and** survives identifier-only refactoring.

A baseline failure may be a product bug: reproduce and repair the owner. Never delete the test to clear the failure.

Map retention to the sitting: a retained test must remain `R`/`F` with `RA-`/`EV-` ids, or it is unverified inventory.

## Candidate evidence (before any delete)

Read the full test and production owner **this sitting**. Do not infer bodies from memory or assume a green test is valid. Also read entry point, callers, callees, siblings, overlapping proof, CI routing, history. Dependency-backed claims: inspect dependency source/types. Parallel discovery: one read-only agent per independent owner.

Record:

```yaml
candidate:
  name:
  location:
  detectable_failure:
  non_test_callers_of_seam:
  stronger_remaining_owner:
  history_reason:
  deletion_unlocks:
  risks_supported: [RA-]
  mechanisms_supported:
  retained_qualified_evidence:
  unique_evidence_lost_if_removed: none | <risk/mechanism> | UNKNOWN
  risk:
  verify:
```

`UNKNOWN` or missing remaining proof → no deletion. Discovery is read-only; report before edits. Prefer few high-confidence candidates. Fan out read-only discovery across independent owners.

Delete obsolete seams and dead paths. Move retained regressions to the keeper. Consolidate generic package/dependency contracts into one owner. Prefer net-negative **production** LOC from unlocked test-only seams. Never add replacement implementation tests to justify a delete. Never optimize for deletion counts.

## Ledger marks

From `MUTATE.md`: `R` `F` `C` `D`. `D` requires `unique_evidence_lost_if_removed: none` and remaining qualified coverage for every supported material risk.

`C` names the keeper **first**. Carry assertions into that keeper in the same unit that deletes the duplicate. A consolidate that only deletes is a `D` in disguise.

## Cutover

Edit lane by lane. One writer. Shared harnesses through one owner. With each lane, remove the test-only production seams it unlocks (injection parameters, getters, reset exports, indirection). Register moved suites in CI/inventories. Update shrink-only line-cap baselines if the repo has them. Durable ownership rules go in the subsystem's agent instructions only when this campaign actually found the mistake.

Done: lane plan applied; keepers pass; unlocked seams gone.

## Preservation

Independent review: one read-only reviewer who did not write the mark. Deleted coverage vs keepers. Unreachable assertions. Mutation: one production-owner edit per restored contract; keeper red; restore source byte for byte.

## Validation

Owner and sibling tests. Removed source greps: exercise the owning executable or dry-run. Targeted format / diff check per repo convention. Report causes, removed categories/seams, retained false positives, proof/cost, production vs test/support LOC, follow-ups.

Refresh from `main` and rediscover before another audit batch.
