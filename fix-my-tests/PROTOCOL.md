# Fix My Tests — live protocol v0.6.0

Status: public protocol for the v0.6 line.

Read `RISK_METHOD_MATRIX.md` as normative method law for this protocol.

## Moment

> “Something about my tests feels wrong. Help me fix them.”

This can mean missing tests, hollow tests, flaky tests, slow tests, too many tests, wrong tests, implementation-coupled tests, common-mode oracles, or useful tests wired to the wrong decision.

## Governing question

> **What product risks deserve evidence here, what evidence capability can actually expose each failure mechanism, what do the current tests qualify as evidence for, and what is the smallest trustworthy portfolio appropriate to this repo?**

The existing suite is evidence to inspect. It is **not** the source of truth for which risks matter.

---

# 0. Preserve the operator ask

Record the user's actual question before routing.

```yaml
operator:
  ask: <plain language>
  source: explicit | reconstructed
  status: OPEN
```

A more severe adjacent defect may control the first repair without replacing the user's question.

Before exit, record separately:

```yaml
operator_answer:
  status: ANSWERED | NEEDS_MORE_EVIDENCE
  scope: BOUNDED | REPRESENTATIVE | EXHAUSTIVE | UNKNOWN
  portfolio_prevalence: ESTABLISHED | NOT_ESTABLISHED
  answer: <direct answer>
```

Do not encode epistemic humility as vague `PARTIAL`. Say what was answered and bind the evidence boundary.

---

# 1. Orient without letting tests define the problem

Recover only enough structure to find consequential product surfaces:

```text
repo / revision
languages / frameworks
user-facing or public interfaces
important state / persistence / external seams
obvious invariants
material configuration / feature / role dimensions
historical defect pointers if readily available
test / eval / check entrypoints
execution / promotion boundaries only if relevant later
```

Classify a dominant system problem only as routing for the **first repair**:

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

This is not the answer to the operator ask.

---

# 2. Build a bounded risk register first

Use `RISK_METHOD_MATRIX.md`.

For each consequential surface, scan applicable independent discovery lenses:

```text
contract / user outcome
state / lifecycle
persistence / crash
boundary / real seam
input space / factor interactions
concurrency / ordering
resource / performance
statistical / model quality
security / authorization
historical regression
structural maintainability
```

Do not require one risk per lens. Do not skip a lens because the suite has no test for it.

Create one row per material **bad outcome**, not per test file:

```yaml
risk:
  id: RA-XX
  surface:
  bad_outcome:
  discovery_lens:
  likelihood: COMMON | PLAUSIBLE | RARE | UNKNOWN
  severity: CATASTROPHIC | HIGH | MODERATE | LOW | UNKNOWN
  obligation: HARD_INVARIANT | MATERIAL | DEFERRED | UNKNOWN
  basis:
  claim:
  failure_mechanism:
  required_capability:
```

## Hard-invariant law

`HARD_INVARIANT` is noncompensatory.

Many greens on lower-risk behavior cannot make an uncovered hard invariant acceptable.

For ordinary material risks, use ordinal likelihood × severity to prioritize. Do not invent numeric scores.

If risk discovery is bounded rather than broad, say so. A clean sample of existing tests cannot prove that undiscovered risk archetypes do not exist.

---

# 3. Derive the evidence capability from the failure mechanism

Before judging the existing test, derive what kind of evidence could expose the failure.

Use the normative matrix in `RISK_METHOD_MATRIX.md`.

Examples:

```text
broad structured input        → property / generative
factor/config interactions    → covering array / t-way combinatorial
malformed/adversarial input   → negative property / fuzz
weak/common-mode oracle       → mutation / negative control / independent differential / metamorphic
real interface                → contract / integration at the real protocol
persistence/crash             → deterministic fault injection + recovery
state machine                 → stateful property / model checking
concurrency/ordering          → systematic concurrency / DST / model
external compatibility        → contract + minimal live probe when external state is the claim
performance/capacity          → benchmark/load under named envelope
statistical quality           → frozen eval + appropriate statistical comparison
historical regression         → minimal deterministic reproducer
structural maintainability    → explicit static/structural rule
security/authorization        → abuse/negative evidence at the actual authority boundary
```

For every material risk answer:

```text
Why can this capability expose this mechanism?
What plausible bug would a weaker method miss?
Would a stronger method add unique material evidence worth the friction?
```

If that derivation is not defensible, use `UNKNOWN`. Do not choose a familiar test type by habit.

A test-size label (`unit`, `integration`, `e2e`) is not a sufficient capability derivation. Size and scope affect cost and fidelity; the failure mechanism decides what the evidence must be able to observe.

---

# 4. Map and qualify the existing evidence

Only now inspect consequential tests/checks as evidence for the independently derived risk rows.

```yaml
evidence:
  id: EV-XX
  risk_id: RA-XX
  claim_mapping: ESTABLISHED | PARTIAL | NONE | UNKNOWN
  falsifiability: VALID | HOLLOW | UNKNOWN
  oracle: RIGHT | WRONG | UNKNOWN
  oracle_independence: ESTABLISHED | COMMON_MODE | UNKNOWN
  method_fit: RIGHT | WRONG | UNKNOWN
  real_seam: YES | NO | N/A | UNKNOWN
  instrument: VALID | INVALID | UNAVAILABLE | UNKNOWN
  provenance_current: YES | NO | UNKNOWN
  qualification: QUALIFIED | PARTIAL | UNQUALIFIED | UNKNOWN
```

Use these failure findings when applicable:

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

A passing result from `UNQUALIFIED` evidence contributes zero blocking authority to the risk claim.

`PARTIAL` evidence may help diagnosis; it does not satisfy a hard invariant by itself.

## 4.1 Oracle-independence check

Ask where the expected distinction between right and wrong came from.

`ESTABLISHED` examples:

```text
explicit requirement / invariant
accepted external reference implementation
fixed accepted baseline for an explicit preservation claim
independently derived model
valid metamorphic relation
```

`COMMON_MODE` examples:

```text
expected output recomputed with the same algorithm as production
AI-generated expected branches mechanically mirror candidate implementation
strict mock sequence restates current call graph although call order is not the claim
snapshot/golden regenerated from the same candidate then offered as proof of correctness
```

A common-mode oracle can still detect some changes. That does not make it independent correctness evidence.

## 4.2 Characterization boundary

A fixed baseline can legitimately support:

> “This accepted behavior did not change.”

when preservation is the actual claim and the baseline revision/artifact is the authority.

It does not establish:

> “This behavior is correct.”

merely because it captures what an earlier implementation did.

Map the test to the claim it can actually support.

## 4.3 Change-detector boundary

Tests should normally encode material behavior, not mechanically mirror methods or implementation structure.

A strict interaction test is valid when the interaction itself is material—for example exactly-once side effect, order-sensitive protocol, resource-call bound, or required authority boundary.

If the test merely fails whenever implementation structure changes while no material claim changes, use `CHANGE_DETECTOR` and treat it as waste/invalid evidence for the claimed behavior.

## 4.4 Test-logic boundary

Loops, conditionals, helpers, builders, and generated expectations are not automatically defects.

But if test-side logic is complex enough that the expected answer or failure path cannot be independently checked by inspection or its own qualified evidence:

```text
instrument: UNKNOWN or INVALID as evidence establishes
oracle_independence: UNKNOWN or COMMON_MODE as evidence establishes
finding: TEST_LOGIC_UNVERIFIED
```

Do not trust opaque test code merely because it is test code.

---

# 5. Reconcile risk coverage before optimizing the suite

Every material risk in the bounded sitting receives one portfolio status:

```text
COVERED
UNDERCOVERED
GAP
INVALID
REDUNDANT
DEFERRED
UNKNOWN
```

Interpretation:

- `COVERED` — sufficient qualified evidence for this obligation.
- `UNDERCOVERED` — relevant evidence exists but capability/independence is insufficient.
- `GAP` — no qualifying evidence.
- `INVALID` — apparent evidence exists but is unqualified.
- `REDUNDANT` — this evidence adds no unique material risk/mechanism coverage.
- `DEFERRED` — intentionally not covered here with explicit rationale.
- `UNKNOWN` — risk or coverage status cannot be established.

Do not let 50 easy covered rows compensate for one uncovered hard invariant.

---

# 6. Representative test-quality analysis must be risk-driven

If the operator asks whether a large suite is useful/trustworthy/gnarly/redundant, inspect a bounded representative slice—but derive the slice **from the risk register**, not by picking tests that look diverse.

Selection order:

1. hard invariants;
2. high-materiality risks;
3. distinct failure mechanisms, including applicable combinatorial interactions;
4. expensive/flaky/generated/high-mock tests;
5. suspicious or real seams;
6. likely common-mode oracles / change detectors;
7. tests claimed to be unique blockers.

Record:

```yaml
analysis_scope:
  risk_discovery: BOUNDED | BROAD | UNKNOWN
  evidence_quality: REPRESENTATIVE | EXHAUSTIVE | UNKNOWN
  portfolio_prevalence: ESTABLISHED | NOT_ESTABLISHED
  sampled_risks: [RA-...]
  unsampled_material_risks: [RA-...]
```

A good representative slice establishes quality of inspected evidence. It does not establish that the repo selected the right risks unless the risk discovery itself was broad enough.

---

# 7. Find waste only after coverage is intelligible

Use portfolio analysis when the suite is rich enough or the operator explicitly asks about waste.

Before delete/downgrade/move:

```text
Which risk rows does this evidence support?
Which failure mechanism does it expose?
What qualified evidence remains if it is removed?
Is that remaining portfolio still sufficient for every supported material risk?
```

Then record:

```text
UNIQUE_EVIDENCE_LOST_IF_REMOVED: none | <risk/mechanism> | UNKNOWN
```

`UNKNOWN` blocks confident deletion.

Candidate waste includes:

```text
duplicated evidence for the same risk + mechanism
expensive evidence dominated by cheaper equally strong evidence
stale tests for removed behavior
change-detector tests with no material claim
implementation-detail checks with no material risk
mock-heavy tests that replace the claimed seam
common-mode tests presented as independent correctness evidence
broad suites dominated by focused deterministic reproducers
flaky blockers
unattributable failures
generated volume with weak oracle diversity
```

No deletion candidate is a valid result until subtraction preserves all material evidence it uniquely supplies.

---

# 8. Inspect execution, binding, and cadence only when they matter

Evidence semantics come first. CI topology is not the ontology.

Inspect hooks, hosted CI, release/nightly jobs, manual probes, live checks, or equivalent gates only when the operator's question depends on **where** qualified evidence runs or whether it actually blocks the relevant transition.

Use:

```text
PROCESS_GATE_ONLY
UNBOUND_AUTHORITY
BOUND_EVIDENCE
MOVE_LATER
```

Rules:

- A process gate can block work without proving product behavior.
- Qualified evidence that is never required at the material decision boundary is `UNBOUND_AUTHORITY` for that boundary.
- Local and hosted gates are equally valid when they reliably bind the required evidence.
- Moving expensive evidence later is legal only when earlier boundaries remain sufficiently protected.
- Do not turn cadence preferences into evidence quality.

---

# 9. Produce consequential dispositions

Every recommended change must reference a risk row or explicit verification-system risk.

Allowed dispositions:

```text
KEEP
FIX_ORACLE
FIX_INSTRUMENT
REPLACE_METHOD
ADD_EVIDENCE
DELETE_CANDIDATE
DOWNGRADE_NONBLOCKING
QUARANTINE
MOVE_LATER
BIND_EVIDENCE
UNKNOWN
```

Laws:

- `ADD_EVIDENCE` requires a named risk + required capability.
- `FIX_ORACLE` includes common-mode oracles that need an independent authority/reference.
- `DELETE_CANDIDATE` requires `UNIQUE_EVIDENCE_LOST_IF_REMOVED: none`.
- `UNKNOWN` is preferable to a confident subtraction whose surviving evidence cannot be established.

Return at most five first moves. Usually fewer.

---

# 10. Answer the operator separately from repair priority

Do not let a severe adjacent issue replace the original question.

```yaml
operator_answer:
  status: ANSWERED | NEEDS_MORE_EVIDENCE
  scope: BOUNDED | REPRESENTATIVE | EXHAUSTIVE | UNKNOWN
  portfolio_prevalence: ESTABLISHED | NOT_ESTABLISHED
  answer:
  evidence_boundary:
```

A bounded answer can still be useful. State exactly what it establishes and what it does not.

---

# 11. Choose exactly one first-repair exit

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

Interpretation:

- `MINIMUM_FLOOR_NEEDED` — consequential product risks are not yet represented by a credible minimum portfolio.
- `TESTS_NEED_REPAIR` — current tests map to the right risks but their oracle/method/independence is defective.
- `EVIDENCE_GAPS_FIRST` — material risks lack the needed capability.
- `INSTRUMENTS_FIRST` — flake, environment, stale/common-mode test machinery, or attribution prevents trustworthy interpretation.
- `BINDING_FIRST` — qualified evidence exists but is not bound to the relevant progression boundary.
- `CLEANUP_READY` — coverage is intelligible enough that subtraction/consolidation is the highest-value first move.
- `NEEDS_MORE_EVIDENCE` — the sitting cannot establish the requested decision.
- `NO_MATERIAL_CHANGE` — no consequential non-`KEEP` action is justified.

This exit says what should be repaired first. It is not the operator-answer disposition.

---

# 12. Dogfood readout and stop

Record:

```yaml
dogfood:
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

Stop when the bounded risk register and evidence qualification are sufficient to change the requested decision and the uncertainty boundary is explicit.

Do not modify the target repository in the diagnostic sitting. Do not claim the repository is safe.
