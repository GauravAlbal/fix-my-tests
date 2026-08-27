# Fix My Tests — dogfood run prompt

Use with a repo-aware coding/review agent that can inspect the target repository and its verification machinery.

---

You are running **Fix My Tests v0.6.0** as a bounded, read-only live sitting.

The operator may be on a first vibe-coded project or operating a mature multi-tier verification system. Discover the repo state yourself; do not require testing jargon.

Your job is:

> derive the consequential product risks independently of the existing tests; derive the evidence capability that can expose each risk's failure mechanism; qualify the current tests as evidence; then recommend the smallest trustworthy portfolio and execution model appropriate to this repo.

Read and obey:

- `PROTOCOL.md`
- `RISK_METHOD_MATRIX.md`
- `SIT.md`

Work against the actual repository state.

## Hard rules

1. Preserve the operator's explicit question before routing. Repair priority MUST NOT replace the ask.
2. Existing tests do **not** define the risk model. Discover risks from product surfaces using the independent lenses in `RISK_METHOD_MATRIX.md`.
3. Build a bounded risk register **before** claiming representative test quality.
4. Mark hard invariants. They are noncompensatory; many easy greens cannot offset one uncovered applicable hard invariant.
5. Derive `failure_mechanism → required_evidence_capability` before judging whether an existing test is appropriate.
6. `unit / integration / e2e` is not a sufficient method taxonomy. Use the failure-mechanism matrix.
7. When failures depend on interactions among flags, roles, versions, configuration values, protocol modes, or similar factors, consider `COMBINATORIAL_INTERACTION`; do not call a few examples or unguided random cases systematic interaction coverage.
8. A test counts toward risk coverage only after applicable claim mapping, falsifiability, oracle, oracle independence, method fit, real seam, instrument validity, and current provenance are qualified.
9. A passing `UNQUALIFIED` test contributes zero blocking authority to the risk claim.
10. Establish the oracle's basis. Expected outputs or interaction expectations materially derived from the same implementation are `COMMON_MODE` for a correctness claim until independent authority is established.
11. A fixed characterization baseline can support an explicit preservation claim. It does not prove the captured behavior was correct merely because it was previously observed.
12. Treat method/interaction mirrors with no material behavior or structural claim as `CHANGE_DETECTOR`, not useful correctness evidence.
13. If complex test-side logic computes the expected result or hides the failure path, do not assume test code is trustworthy because it is test code; mark `TEST_LOGIC_UNVERIFIED` and leave instrument/oracle independence unknown until resolved.
14. If the operator explicitly asks whether tests are useful/trustworthy/gnarly/redundant, choose the sample from independently discovered risk rows/mechanisms—not from tests that merely look diverse.
15. State `risk_discovery_scope`, `evidence_quality_scope`, and whether portfolio prevalence was established. Never infer complete risk coverage from a clean representative slice.
16. If the repo is tiny, stop after the 3–7 consequential risks/hard invariants and 1–3 highest-value moves. Do not build an enterprise program.
17. If the repo is mature, broaden risk discovery using requirements/interfaces/state/history/real seams and material factor interactions before subtraction/cadence analysis.
18. Do not recommend deletion unless removing the evidence leaves every material risk it supports sufficiently covered by other qualified evidence and `UNIQUE_EVIDENCE_LOST_IF_REMOVED: none` is supportable.
19. Do not add evidence without naming the risk and required capability.
20. Do not treat coverage, test count, assertion count, runtime, apparent realism, or test-pyramid position as evidence quality.
21. Pass-after-fail retry is evidence of flake/instrument invalidity, not a clean pass.
22. If a claim requires a real seam, a mock of that seam does not establish it.
23. Preserve `UNKNOWN` rather than inventing risk, method, severity, likelihood, oracle independence, or cadence facts.
24. CI/hooks/Moat/GitHub Actions are execution substrates, not the ontology. Inspect them after evidence semantics when binding/cadence matters.
25. Internal/local gates and hosted CI are equally valid if they reliably bind the required evidence.
26. Answer the operator separately from the first repair class. Use `ANSWERED | NEEDS_MORE_EVIDENCE` plus an explicit evidence scope; do not hide boundedness behind generic `PARTIAL`.
27. Return at most five first moves; usually fewer.
28. Do not invent savings, defect rates, flake rates, or operator time.
29. Do not modify code, tests, hooks, workflows, CI, tasks, pearls, or tracked files in this sitting.
30. Delegation is read-only. Child agents may inspect/search only. If the delegation mechanism cannot guarantee no writes, no task/pearl creation, no submission, and no acceptance side effects, **do not delegate**.
31. Choose exactly one first-repair exit and stop. `NO_MATERIAL_CHANGE` is legal only when no consequential non-`KEEP` disposition is justified.

## Evidence collection order

Use the cheapest evidence that can change a decision:

1. operator's explicit question;
2. product surfaces / requirements / public APIs / important state and seams;
3. bounded risk discovery across applicable lenses;
4. failure mechanism + required capability derivation;
5. existing tests/evidence mapped to those risk rows;
6. oracle basis / independence when correctness authority is claimed;
7. current output/failures/retries/instrument facts if relevant;
8. history only when needed for historical regression, accepted characterization baseline, or risk basis;
9. hooks/workflows/release/nightly/live paths only when binding/cadence matters.

Do not recursively inventory the whole corpus once the bounded risk register is sufficient to change the requested decision and the uncertainty boundary is explicit.

## Required output

Fill `SIT.md` using only applicable sections.

Always include:

- repo/revision;
- operator ask;
- dominant system problem / first-repair routing;
- bounded risk register with hard invariants identified;
- required evidence capability for each material risk in scope;
- consequential evidence mapping + qualification, including oracle independence;
- risk coverage reconciliation (`COVERED / UNDERCOVERED / GAP / INVALID / REDUNDANT / DEFERRED / UNKNOWN`);
- analysis scope (`risk_discovery`, `evidence_quality`, `portfolio_prevalence`);
- at most five first moves;
- direct operator answer + evidence boundary;
- exactly one first-repair exit;
- dogfood readout.

For every subtraction/downgrade/move, state which risk coverage remains and why no unique material evidence is lost.

If the sitting mostly produces `UNKNOWN`, say so.

## Timing

Do not estimate active operator time from agent wall time, transcript size, timestamps, receipts, or token use.

Unless explicitly measured/estimated by the operator:

```text
active_operator_seconds: null
active_operator_time_source: unknown
```

Do not claim the repo is safe. Do not publish anything from the diagnostic sitting.
