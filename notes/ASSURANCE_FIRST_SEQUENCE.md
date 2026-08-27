# Assurance-first sequence

Five short pieces for one market question: **how do we make AI-generated changes cheaper to trust?**

The order is deliberate. Start with a recognizable evidence mistake. Widen to repository risk. Then name the operational products only when the job changes.

---

## 1. A test can prove the wrong thing

A test can be green, deterministic, and genuinely falsifiable—and still be the wrong evidence.

Suppose a unit test proves that `recover(state)` returns the expected value. That does not prove the system survives a process death between two filesystem writes. The function may be correct while the persistence protocol tears state on disk.

Or suppose a threaded test sleeps for 100 ms and passes. That does not prove an ordering invariant. It proves one schedule happened not to expose the race.

A useful check has four independent edges:

```text
falsifiability
oracle authority
method / seam fitness
current execution provenance
```

- **Falsifiability:** would the check turn red if the behavior were absent?
- **Oracle authority:** does the expected result come from a real contract, invariant, or qualified reference?
- **Method fitness:** can this kind of check observe the named failure mechanism?
- **Current provenance:** did this check run on this revision, in the environment relevant to the claim?

Green is a result. Evidence authority comes from the relationship between one claim and one check.

Use the free [`proof`](https://github.com/GauravAlbal/agent-skills/tree/main/proof) skill for that one decision.

---

## 2. Existing tests do not define product risk

Most test audits begin with the suite:

```text
list tests
→ count failures
→ inspect coverage
→ recommend more or fewer tests
```

That reverses the dependency.

A repository can have hundreds of credible tests and still miss the thing that matters: a paid webhook that never grants access, a journal that lies about durability, a cross-tenant authorization bypass, or two implementations that silently drift.

Start here instead:

```text
product surface
→ material bad outcome
→ positive claim / hard invariant
→ failure mechanism
→ required evidence capability
→ existing evidence
```

This changes recommendations.

- A mocked Stripe handler may be useful, but it cannot establish the live subscription and metadata path.
- A clean-shutdown integration test cannot establish crash durability.
- A few golden examples cannot establish a distributional quality claim.
- More unit tests do not repair an untested CLI or wire protocol.

Hard invariants are noncompensatory. Fifty easy greens cannot offset one uncovered authorization or durability invariant.

That is the job of [Fix My Tests](https://github.com/GauravAlbal/fix-my-tests): derive the risk model before letting the existing suite influence it.

---

## 3. Repository evidence is not exact-change assurance

A repository may have a trustworthy evidence portfolio and still fail the next decision.

“The property suite is good” is not the same claim as “candidate `abc123` is acceptable.”

Exact-change assurance needs binding:

```text
candidate identity
+ repository revision
+ declared claim set
+ required evidence
+ current execution
+ authority to accept or refuse
```

Without those bindings, a remembered green can judge the wrong revision. A valid test can run in the wrong environment. A required check can exist but never control merge or release. A human-readable summary can accidentally become a second source of truth.

This is why the progression matters:

```text
risk-first repository diagnosis
→ verification map
→ exact candidate
→ revision-bound receipts
→ independent acceptance decision
```

The diagnosis tells you what evidence should exist. It does not silently grant authority to a candidate.

---

## 4. The audit was right; now someone has to rebuild the evidence system

A strong diagnosis can create work:

- move an assertion to the real protocol boundary;
- add deterministic crash injection;
- replace sleeps with controlled schedule exploration;
- bind a qualified check to release;
- delete a redundant test only after unique coverage is known to be preserved.

That is no longer a more correct answer to the same free question. It is implementation labor against a larger job.

The founding **Verification Retrofit** offer takes a completed Fix My Tests map and installs one bounded evidence tranche:

```text
risk → claim → failure mechanism → method → drive → oracle → receipt → cadence
```

Completion requires runnable, revision-bound evidence for the selected rows—not a longer report. The service stops after handoff. It does not become permanent PR adjudication, generic CI modernization, or a claim that the repository is safe.

Demand is not assumed. The offer exists to test whether operators who accept the diagnosis want the implementation burden removed.

---

## 5. When repeated candidate adjudication becomes the pain

After the evidence system improves, a different problem may appear:

> Every consequential candidate still requires someone to reconstruct the claim, revision, required evidence, current results, and exceptions.

That is repeated operation, not another test audit.

A durable acceptance system can own that bounded loop:

```text
exact candidate
→ required evidence
→ current receipts
→ independent accept / refuse
```

That is the job Moat may eventually package for external users. Internal architectural maturity is not proof of demand, so the product stays held until operators repeatedly ask for the loop to be run—not merely for the evidence system to be repaired once.

The ladder is based on changing jobs, not feature withholding:

```text
free judgment: Is this evidence credible?
free diagnosis: Does this repository protect the right risks?
paid retrofit: Install the missing evidence system.
repeated software: Operate exact-candidate acceptance.
integrated system: Own the broader engineering lifecycle.
```

A user may stop at any layer. Upgrade is not mandatory.
