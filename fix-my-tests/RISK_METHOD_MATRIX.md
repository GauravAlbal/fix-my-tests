# Fix My Tests — risk / method kernel

**Status:** normative for Fix My Tests v0.6.0. This is a bounded RACS kernel, not the Arq Assurance Planner and not a universal risk catalog.

## Governing law

Existing tests do **not** define what matters.

Derive the portfolio in this order:

```text
PRODUCT SURFACE
→ RISK ARCHETYPE
→ MATERIALITY / HARD INVARIANT
→ CLAIM
→ FAILURE MECHANISM
→ REQUIRED EVIDENCE CAPABILITY
→ EXISTING EVIDENCE
→ EVIDENCE QUALIFICATION
→ COVERED | GAP | INVALID | REDUNDANT | DEFERRED
```

A test only counts as coverage after the risk/claim/method derivation exists independently of that test.

---

# 1. Discover risks from independent lenses

For each consequential product surface, scan the applicable lenses below. Do not force one risk from every lens. Do not skip a lens merely because no existing test points at it.

| Lens | Question | Typical bad outcomes |
| --- | --- | --- |
| **Contract / user outcome** | What externally visible promise can be wrong while the program still runs? | wrong result, missing effect, incompatible response |
| **State / lifecycle** | What state may become impossible, duplicated, stale, skipped, or terminal incorrectly? | illegal transition, double apply, resurrection, lost terminal state |
| **Persistence / crash** | What must survive process death or partial commit? | lost intent, torn state, false durability, unrecoverable journal |
| **Boundary / real seam** | Where does correctness depend on another process, DB, filesystem, network, provider, serializer, or CLI? | contract drift, wrong argv/wire shape, mock-only confidence |
| **Input space** | What valid breadth, malformed shape, or factor/configuration interaction can examples miss? | parser edge, combinatorial case, malformed acceptance, configuration-only failure |
| **Concurrency / ordering** | What can interleave, race, duplicate, reorder, or starve? | lost update, double spend, deadlock, order violation |
| **Resource / performance** | What fails only near a named capacity, latency, memory, quota, or exhaustion boundary? | tail blowup, OOM, queue collapse, timeout cascade |
| **Statistical / model quality** | What is distributional rather than pointwise? | regression hidden by anecdotes, calibration drift, unstable rank |
| **Security / authorization** | What must an untrusted caller, input, tenant, or agent never be able to do? | privilege widening, injection, cross-boundary mutation |
| **Historical regression** | What escaped before, required a repair, or produced a workaround? | recurrence of known defect |
| **Structural maintainability** | What structural property itself protects future correctness? | forbidden dependency, cyclic authority, schema drift |

## Separate verification-system risks

Do not confuse product risks with risks in the evidence machinery itself.

Verification-system risks include:

```text
HOLLOW_ORACLE
WRONG_ORACLE
COMMON_MODE_ORACLE
CHANGE_DETECTOR
TEST_LOGIC_UNVERIFIED
WRONG_METHOD
REAL_SEAM_REPLACED_BY_MOCK
FLAKE
RETRY_LAUNDERING
STALE_PROVENANCE
WRONG_ENVIRONMENT
SKIP_AS_GREEN
UNBOUND_EVIDENCE
UNATTRIBUTABLE_FAILURE
```

They affect whether evidence deserves authority; they are not substitutes for product-risk discovery.

---

# 2. Risk row — house format

Use one row per material bad outcome, not one row per test file.

```yaml
risk:
  id: RA-XX
  surface: <product surface>
  bad_outcome: <observable failure>
  discovery_lens: <one of the lenses above>
  likelihood: COMMON | PLAUSIBLE | RARE | UNKNOWN
  severity: CATASTROPHIC | HIGH | MODERATE | LOW | UNKNOWN
  obligation: HARD_INVARIANT | MATERIAL | DEFERRED | UNKNOWN
  basis: <spec / API / incident / code invariant / explicit operator requirement>
  claim: <positive property that must hold>
  failure_mechanism: <typed mechanism below>
  required_capability: <evidence capability derived below>
```

### Materiality law

- `HARD_INVARIANT` is noncompensatory. If applicable, it requires qualifying evidence regardless of estimated likelihood.
- `MATERIAL` risks are prioritized using ordinal likelihood × severity. Do not multiply fake numbers or produce a health score.
- `DEFERRED` requires a reason. “No test exists” is not a reason.
- `UNKNOWN` widens inquiry; it does not silently become low risk.
- The aspirational “cover ~95% of key risks” is an empirical portfolio target over real failure incidence, not permission to sum invented risk scores.

---

# 3. Failure mechanism → required evidence capability

Choose the capability that can expose the mechanism. Test framework names are implementation choices after this step.

| Failure mechanism | Default evidence capability | Common wrong substitute |
| --- | --- | --- |
| `PURE_BEHAVIOR` | focused example; property when the domain has meaningful algebra/breadth | giant end-to-end test for a pure function |
| `BROAD_INPUT_SPACE` | property/generative testing; differential/metamorphic when an independent relation/reference exists | a few handpicked examples |
| `COMBINATORIAL_INTERACTION` | covering array / pairwise or higher-strength t-way interaction coverage, plus targeted property/negative cases where needed | a few examples or unguided random generation with no interaction-coverage claim |
| `MALFORMED_INPUT` | negative property + fuzz/adversarial corpus | happy-path unit examples |
| `WEAK_ORACLE` | mutation, negative control, independent differential reference, or metamorphic evidence | more cases using the same weak/common-mode oracle |
| `REAL_INTERFACE` | contract/integration against the real protocol or faithful executable seam | mocking the interface being claimed |
| `PERSISTENCE_OR_CRASH` | deterministic fault injection + recovery/durability assertion | clean-shutdown integration test |
| `STATE_MACHINE` | stateful property/model checking or exhaustive transition evidence for bounded state | isolated point examples only |
| `CONCURRENCY_OR_ORDERING` | systematic concurrency, deterministic simulation/DST, model checking, or controlled schedule exploration | sleeps, wall-clock races, one lucky threaded run |
| `EXTERNAL_COMPATIBILITY` | contract test plus minimal live probe when the external service/version itself is the claim | internal fake only |
| `PERFORMANCE_CAPACITY` | benchmark/load under a named envelope with controlled environment | incidental wall time from functional tests |
| `STATISTICAL_QUALITY` | frozen eval + statistical comparison/uncertainty appropriate to the metric | a handful of golden anecdotes |
| `HISTORICAL_REGRESSION` | minimal deterministic reproducer tied to the escaped defect | broad unrelated suite |
| `STRUCTURAL_MAINTAINABILITY` | static/structural rule with an explicit forbidden/required shape | claiming runtime behavior from grep/path checks |
| `SECURITY_OR_AUTHORIZATION` | negative/abuse-case evidence at the actual authority boundary; property/fuzz/integration as mechanism requires | permission helper unit test while bypass path remains unexercised |
| `UNKNOWN` | investigate before assigning authority | choosing a familiar test type by habit |

### Assignment test

For each material risk, answer before reading the current test result:

```text
Why can this evidence capability expose this mechanism?
What plausible bug would a weaker method miss?
Would a stronger method add unique material evidence worth its friction?
```

If the first answer is weak, method assignment is not established.

### Combinatorial-interaction law

Use `COMBINATORIAL_INTERACTION` only when the material defect requires an interaction among independently varying factors such as flags, roles, versions, configuration options, environment dimensions, protocol modes, or feature combinations.

A covering array makes a bounded **t-way interaction coverage** claim. It is not exhaustive correctness evidence, and pairwise coverage must not be rounded up to higher-strength coverage without evidence.

---

# 4. Evidence qualification

Map existing evidence to the independently derived risk row.

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

`QUALIFIED` requires all applicable authority dimensions to be established. `COMMON_MODE` cannot produce blocking `QUALIFIED` evidence for a correctness claim.

Typical rejection reasons:

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
```

A passing result from `UNQUALIFIED` evidence contributes **zero blocking authority** to the risk claim.

`PARTIAL` may be useful diagnostic evidence, but it does not satisfy a hard invariant by itself.

## Oracle-independence law

`ESTABLISHED` means the expected distinction between right and wrong is grounded independently of the candidate implementation: for example an explicit requirement/invariant, an accepted external reference, a fixed prior accepted baseline for a preservation claim, an independently derived model, or a valid metamorphic relation.

`COMMON_MODE` means the oracle or expected interaction is materially derived from the same implementation it is supposed to judge. Examples:

- the test reimplements the production algorithm to calculate the expected output;
- an AI-generated test mirrors the candidate's branch structure and calls that expected behavior;
- a strict mock sequence mechanically restates the current call graph when that sequence is not itself the product claim;
- a snapshot/golden is regenerated from the same candidate and then used as correctness proof.

`UNKNOWN` means the basis cannot be established.

### Characterization boundary

A captured baseline can be legitimate evidence for a claim such as **“this accepted behavior did not change”** when the baseline revision/artifact is explicitly the authority and is independent of the candidate under test.

The same baseline does not establish **“this behavior is correct”** merely because it records what the old implementation happened to do. Characterization is descriptive until a requirement, invariant, accepted baseline policy, or other authority makes preservation normative.

### Change-detector boundary

A test that fails on implementation changes but has no material behavior/structural claim is a `CHANGE_DETECTOR`, not valuable coverage. Strict interaction testing is valid when the interaction itself is the material claim—for example exactly-once side effect, order-dependent protocol, or bounded resource call—not merely because the current implementation happens to make those calls.

### Test-logic boundary

Do not ban loops, conditionals, helpers, builders, or generated expectations categorically. But if test-side logic is complex enough that the expected result or failure path cannot be independently verified by inspection or its own qualified evidence, mark `TEST_LOGIC_UNVERIFIED`; instrument validity and/or oracle independence remain `UNKNOWN` until resolved.

---

# 5. Reconcile the portfolio

Every material risk in the bounded sitting receives one status:

```text
COVERED        — sufficient qualified evidence for the obligation in this sitting
UNDERCOVERED   — relevant evidence exists but capability/independence is insufficient
GAP            — no qualifying evidence for the material risk
INVALID        — apparent evidence exists but is unqualified
REDUNDANT      — this evidence adds no unique material risk/mechanism coverage
DEFERRED       — intentionally not covered here with explicit rationale
UNKNOWN        — cannot establish risk or evidence status
```

For hard invariants:

```text
COVERED requires qualifying evidence.
UNDERCOVERED / GAP / INVALID / UNKNOWN cannot be compensated by many low-risk greens.
```

For subtraction:

```text
DELETE_CANDIDATE only if removing the evidence leaves every material risk it supports sufficiently covered by other qualified evidence.
```

Record:

```text
UNIQUE_EVIDENCE_LOST_IF_REMOVED: none | <risk/mechanism> | UNKNOWN
```

`UNKNOWN` blocks confident deletion.

---

# 6. Representative analysis without self-certification

A “mechanism-diverse sample” is not established by choosing tests that look diverse.

Use this order:

1. derive a bounded risk register from product surfaces and independent discovery lenses;
2. select evidence spanning distinct **risk rows / mechanisms**, prioritizing hard invariants, high-materiality risks, expensive/flaky tests, generated tests, suspicious seams, and likely common-mode oracles;
3. qualify those tests;
4. state exactly which risk rows were and were not sampled.

A clean representative slice can establish that the inspected evidence is good. It cannot establish that undiscovered risk archetypes do not exist.

Use separate conclusions:

```text
RISK_DISCOVERY_SCOPE: BOUNDED | BROAD | UNKNOWN
EVIDENCE_QUALITY_SCOPE: REPRESENTATIVE | EXHAUSTIVE | UNKNOWN
PORTFOLIO_PREVALENCE: ESTABLISHED | NOT_ESTABLISHED
```

This prevents a good sample of existing tests from becoming accidental proof that the repo tests the right things.

---

# 7. Progressive depth

This kernel scales down as well as up.

### Tiny / vibe-coded repo

Derive only the 3–7 consequential risks/hard invariants visible from the product surface. Recommend the smallest capability set that protects them. Do not manufacture every archetype.

### Mature repo

Broaden risk discovery using requirements, public interfaces, state machines, history/incidents, external seams, execution tiers, and material configuration/factor interactions. Portfolio subtraction requires stronger claim/risk mapping than representative quality review.

### Stop rule

Stop when the bounded risk register is sufficient to change the requested decision and the uncertainty boundary is explicit. Do not turn the free dogfood into an exhaustive Arq assurance program.
