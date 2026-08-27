# Fix My Tests

Risk-first verification portfolio diagnosis for software repositories.

Most test reviews start from the suite. Fix My Tests starts from the product:

```text
product surface
→ material bad outcome
→ failure mechanism
→ evidence capability
→ current test qualification
→ smallest trustworthy portfolio
```

Use it when tests feel missing, hollow, flaky, slow, redundant, over-mocked, or attached to the wrong gate—or when a vibe-coded project is approaching production and the question is simply “what must I test before I trust this?”

## What it returns

- a bounded product-risk register;
- hard invariants that lower-risk greens cannot compensate for;
- a failure-mechanism-derived evidence method for each material risk;
- qualification of consequential current tests;
- coverage, gap, invalidity, redundancy, and cadence decisions;
- at most five first moves;
- one typed first-repair exit;
- a direct answer with an explicit evidence boundary.

## Install as an Agent Skill

```sh
ln -s "$PWD/fix-my-tests" ~/.agents/skills/fix-my-tests
```

For OMP, use `~/.omp/agent/skills/fix-my-tests`. Restart the client after installation.

## Run without installing

Give a repo-aware coding/review agent `fix-my-tests/RUN_PROMPT.md` and the repository path plus your plain-language question. The sitting is read-only.

## Files

- `SKILL.md` — activation and compact contract.
- `PROTOCOL.md` — complete analysis procedure.
- `RISK_METHOD_MATRIX.md` — normative risk/evidence kernel.
- `SIT.md` — reusable output template.
- `RUN_PROMPT.md` — standalone execution prompt.
- `VERIFICATION_MAP.md` — implementation-ready risk → method → drive → oracle → receipt template.

## Request a dogfood sitting

Open a **Fix My Tests dogfood request** issue with a repository revision and a plain-language question. Public sittings are bounded and read-only. The report may identify missing or invalid evidence; it will not certify that the software is safe.

## Why this sequence

Read [Assurance-first sequence](notes/ASSURANCE_FIRST_SEQUENCE.md) for the progression from one wrong-method test to risk-first diagnosis, exact-change assurance, a bounded retrofit, and demand-gated repeated acceptance.

## Boundaries

Fix My Tests diagnoses the evidence portfolio. It does not implement tests, repair CI, gate changes, prove the repository safe, estimate defect reduction, or infer customer demand. Model agreement is not evidence authority.

## License

CC BY 4.0. See [LICENSE.md](LICENSE.md).
