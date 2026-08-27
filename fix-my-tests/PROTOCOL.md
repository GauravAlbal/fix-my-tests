# Fix My Tests — live protocol v0.5.0

Status: PUBLIC v0.5.0.

Read `RISK_METHOD_MATRIX.md` as normative method law for this protocol.

## Moment

> “Something about my tests feels wrong. Help me fix them.”

This can mean missing tests, hollow tests, flaky tests, slow tests, too many tests, wrong tests, or useful tests wired to the wrong decision.

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

Do not encode epistemic humility as a vague `PARTIAL`. Say what was answered and bound the scope.

---

# 1. Orient without letting tests define the problem

Recover only enough structure to find consequential product surfaces:

```text
repo / revision
languages / frameworks
user-facing or public interfaces
important state / persistence / external seams
obvious invariants
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
input space
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
broad structured input       → property / generative
malformed/adversarial input  → negative property / fuzz
weak oracle                  → mutation / negative control / metamorphic
real interface               → contract / integration at the real protocol
persistence/crash            → deterministic fault injection + recovery
state machine                → stateful property / model checking
concurrency/ordering         → systematic concurrency / DST / model
external compatibility       → contract + minimal live probe when external state is the claim
performance/capacity         → benchmark/load under named envelope
statistical quality          → frozen eval + appropriate statistical comparison
historical regression        → minimal deterministic reproducer
structural maintainability   → explicit static/structural rule
security/authorization       → abuse/negative evidence at the actual authority boundary
```

For every material risk answer:

```text
Why can this capability expose this mechanism?
What plausible bug would a weaker method miss?
Would a stronger method add unique material evidence worth the friction?
```

If that derivation is not defensible, use `UNKNOWN`. Do not choose a familiar test type by habit.

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
3. distinct failure mechanisms;
4. expensive/flaky/generated/high-mock tests;
5. suspicious or real seams;
6. tests claimed to be unique blockers.

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
implementation-detail checks with no material risk
mock-heavy tests that replace the claimed seam
broad suites dominated by focused deterministic reproducers
flaky blockers
unattributable failures
generated volume with weak oracle diversity
```

No deletion candidate is a valid result.

[Showing lines 1-300 of 528. Use :301 to continue]