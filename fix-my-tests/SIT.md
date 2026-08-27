# Fix My Tests — live sit v0.6.0

Copy per sitting. One repo / one bounded test-system question. Read-only.

## Identity

```yaml
repo:
revision:
operator:
date:
operator_ask:
operator_ask_source: explicit | reconstructed
out_of_scope:
```

## First-repair routing

Choose the dominant system problem only as a prioritization aid:

```text
MINIMUM_FLOOR
TEST_QUALITY
MISSING_EVIDENCE
UNBOUND_EVIDENCE
FLAKE_OR_INSTRUMENT
PORTFOLIO_FRICTION
CADENCE
UNKNOWN
```

Other applicable shapes:

```text
...
```

## Bounded risk register

Derive these rows independently of the existing tests. One row per material bad outcome.

| Risk | Surface | Bad outcome | Discovery lens | Likelihood | Severity | Obligation | Basis | Claim | Failure mechanism | Required capability |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RA- |  |  |  | COMMON / PLAUSIBLE / RARE / UNKNOWN | CATASTROPHIC / HIGH / MODERATE / LOW / UNKNOWN | HARD_INVARIANT / MATERIAL / DEFERRED / UNKNOWN |  |  |  |  |

Hard invariants are noncompensatory.

### Discovery coverage

```yaml
risk_discovery_scope: BOUNDED | BROAD | UNKNOWN
lenses_considered:
  - contract_user_outcome:
  - state_lifecycle:
  - persistence_crash:
  - boundary_real_seam:
  - input_space_factor_interactions:
  - concurrency_ordering:
  - resource_performance:
  - statistical_model_quality:
  - security_authorization:
  - historical_regression:
  - structural_maintainability:
material_surfaces_not_resolved:
```

Do not force a risk from every lens. Record why a consequential lens is not applicable or remains unknown when that matters.

## Evidence capability derivation

Do this before judging current tests.

| Risk | Why this capability can expose the mechanism | Plausible bug a weaker method misses | Stronger method adds unique value? |
| --- | --- | --- | --- |
| RA- |  |  | YES / NO / UNKNOWN — why |

If the method derivation is not defensible, mark the required capability `UNKNOWN`.

## Existing evidence mapping + qualification

| Evidence | Risk | Intended claim | Claim map | Falsifiable | Oracle | Oracle independence | Method fit | Real seam | Instrument | Current provenance | Qualification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EV- | RA- |  | ESTABLISHED / PARTIAL / NONE / UNKNOWN | VALID / HOLLOW / UNKNOWN | RIGHT / WRONG / UNKNOWN | ESTABLISHED / COMMON_MODE / UNKNOWN | RIGHT / WRONG / UNKNOWN | YES / NO / N/A / UNKNOWN | VALID / INVALID / UNAVAILABLE / UNKNOWN | YES / NO / UNKNOWN | QUALIFIED / PARTIAL / UNQUALIFIED / UNKNOWN |

Allowed defect findings:

```text
CLAIM_MAPPING_GAP
HOLLOW
WRONG_ORACLE
COMMON_MODE_ORACLE
CHANGE_DETECTOR
TEST_LOGIC_UNVERIFIED
WRONG_METHOD
REAL_SEAM_UNTESTED
INSTRUMENT_INVALID
PROVIDER_UNAVAILABLE
STALE_PROVENANCE
UNATTRIBUTABLE_FAILURE
IRRELEVANT_TO_CLAIM
UNKNOWN
```

A passing `UNQUALIFIED` row contributes zero blocking authority to its risk.

### Characterization note

If an evidence row uses a captured baseline/snapshot/golden, state the actual claim it can support:

```yaml
characterization:
  baseline_authority:
  preservation_claim:
  correctness_claim_supported: YES | NO | UNKNOWN
```

Matching an old implementation is not automatically proof that the old behavior was correct.

## Portfolio reconciliation

Every material risk in scope gets one status.

| Risk | Status | Qualified evidence | Missing / invalid capability | Notes |
| --- | --- | --- | --- | --- |
| RA- | COVERED / UNDERCOVERED / GAP / INVALID / REDUNDANT / DEFERRED / UNKNOWN |  |  |  |

For hard invariants, only qualifying evidence can produce `COVERED`.

## Representative analysis scope

Use when the operator asked whether a nontrivial suite is useful/trustworthy/gnarly/redundant.

```yaml
risk_discovery_scope: BOUNDED | BROAD | UNKNOWN
evidence_quality_scope: REPRESENTATIVE | EXHAUSTIVE | UNKNOWN
portfolio_prevalence: ESTABLISHED | NOT_ESTABLISHED
sampled_risks:
  - RA-
unsampled_material_risks:
  - RA-
sample_basis:
what_this_establishes:
what_this_does_not_establish:
```

The sample must be selected from independently discovered risk rows/mechanisms, not from tests that merely look diverse.

## Waste / overlap

Use only when coverage is intelligible enough to reason about subtraction.

```yaml
candidate:
risks_supported:
mechanisms_supported:
retained_qualified_evidence:
coverage_after_removal:
unique_evidence_lost_if_removed: none | <risk/mechanism> | UNKNOWN
burden_fact:
```

`UNKNOWN` blocks confident deletion.

## Execution / binding / cadence

Use only when where/how evidence runs affects the problem.

| Boundary | Actual authority | Qualified evidence bound there | Topology |
| --- | --- | --- | --- |
| MANUAL / EVERY_CHANGE / MERGE / RELEASE / NIGHTLY / WEEKLY / ON_DEMAND / LIVE / OTHER |  |  | NO_BAR / AD_HOC_BAR / DOCUMENTED_BAR_UNBOUND / BOUND_BAR / UNKNOWN |

Use:

- `PROCESS_GATE_ONLY` when something can block progress without proving product behavior;
- `UNBOUND_AUTHORITY` when required/qualified evidence is not stably required where needed;
- `MOVE_LATER` only when the later cadence is appropriate and the earlier boundary remains sufficiently protected.

## Consequential dispositions

Every disposition references a risk row or explicit verification-system risk.

| Test / surface | Disposition | Risk | Required capability | Why | Caveat |
| --- | --- | --- | --- | --- | --- |
|  | KEEP / FIX_ORACLE / FIX_INSTRUMENT / REPLACE_METHOD / ADD_EVIDENCE / DELETE_CANDIDATE / DOWNGRADE_NONBLOCKING / QUARANTINE / MOVE_LATER / BIND_EVIDENCE / UNKNOWN | RA- / verification risk |  |  |  |

`ADD_EVIDENCE` without a named risk + required capability is invalid.

## First moves — max 5

```yaml
move:
  action:
  why_now:
  risk_id:
  current_evidence:
  required_capability:
  disposition:
  expected_benefit:
  subtraction_safety:
  caveat:
```

Repeat only as justified.

## Answer the operator ask

Answer separately from repair priority.

```yaml
operator_answer:
  status: ANSWERED | NEEDS_MORE_EVIDENCE
  scope: BOUNDED | REPRESENTATIVE | EXHAUSTIVE | UNKNOWN
  portfolio_prevalence: ESTABLISHED | NOT_ESTABLISHED
  answer:
  evidence_boundary:
```

Do not use generic `PARTIAL`. If something useful was established, answer it and state the boundary. If the requested decision genuinely cannot be answered, use `NEEDS_MORE_EVIDENCE`.

## First-repair exit

Choose exactly one:

```text
MINIMUM_FLOOR_NEEDED
TESTS_NEED_REPAIR
EVIDENCE_GAPS_FIRST
INSTRUMENTS_FIRST
BINDING_FIRST
CLEANUP_READY
NEEDS_MORE_EVIDENCE
NO_MATERIAL_CHANGE
```

This says what should be repaired first. It is not the operator-answer disposition.

`NO_MATERIAL_CHANGE` is legal only when no consequential non-`KEEP` action is justified.

### Why

One paragraph. No score.

## Dogfood readout

```yaml
active_operator_seconds: <measured integer> | null
active_operator_time_source: measured | operator_estimate | unknown
action_changed: yes | no | unclear
what_changed:
would_reach_for_again: yes | no | unclear
felt_too_heavy_where:
missing_input_that_mattered:
protocol_bug_or_taxonomy_split:
```

Do not infer operator time from wall time, transcript size, timestamps, receipts, or token count.

Stop. Do not modify the repo or expand into a broader assurance program automatically.
