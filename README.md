# Fix My Tests

**Figure out which tests matter, what is missing, and what you can safely delete.**

Coding agents can write tests much faster than you can review them. It is easy to end up with hundreds of green tests without knowing what they actually protect.

Fix My Tests works backward from your software instead:

```text
what can break?
→ what evidence would catch it?
→ do your current tests provide that evidence?
→ keep / fix / add / delete / move
```

It is a read-only Agent Skill. It inspects the repository and gives you a verification plan; it does not rewrite your tests.

## Use it when

- Claude, Codex, or another agent generated a pile of tests and you do not know which ones matter.
- The suite is green but you do not trust it.
- CI is slow or flaky and you want to remove tests safely.
- The tests are heavily mocked and you are unsure what they prove.
- A vibe-coded project is approaching production.
- You are not sure what should block a merge, run later, or disappear entirely.

If your question is smaller—**“does this one test actually prove this one claim?”**—use [`proof`](https://github.com/GauravAlbal/agent-skills/tree/main/proof) from [The Kit](https://github.com/GauravAlbal/agent-skills). Fix My Tests is for when the test system itself becomes the problem.

## The idea

Most test reviews start with the test suite. Fix My Tests starts with the product.

Suppose a payment must grant the right entitlement exactly once. The useful questions are not “how many webhook tests do we have?” or “what is coverage?” They are:

```text
What bad outcome matters?
Duplicate or missing entitlement.

How could that happen?
The real payment event and our metadata/entitlement path disagree.

What evidence could catch it?
A check that crosses the real protocol boundary.

What do the current tests prove?
Now inspect them.
```

A mocked handler test may still be worth keeping. But if it cannot expose a mismatch at the real payment boundary, it does not prove that boundary works.

**Existing tests do not decide what matters. What can break does.**

## What you get

A run returns the important risks it found, the evidence your current tests actually provide, the gaps that matter, and a short list of first moves.

A finding looks roughly like this:

```text
RISK
Payment succeeds but access is not granted.

CURRENT EVIDENCE
Webhook unit test with a mocked provider payload.

FINDING
WRONG METHOD

WHY
The test checks handler logic but cannot catch a mismatch
between the real provider event and the production metadata path.

MOVE
Keep the unit test for handler logic.
Add one check at the real provider boundary.
```

Fix My Tests can also conclude that a test is useful, that deletion is unsafe, or that the available evidence is not enough to decide.

## Install

Clone the repository:

```sh
git clone https://github.com/GauravAlbal/fix-my-tests.git
cd fix-my-tests
```

For Agent Skills-compatible clients that discover user skills under `~/.agents/skills/`:

```sh
mkdir -p "$HOME/.agents/skills"
ln -s "$PWD/fix-my-tests" "$HOME/.agents/skills/fix-my-tests"
```

For OMP (Oh My Pi):

```sh
mkdir -p "$HOME/.omp/agent/skills"
ln -s "$PWD/fix-my-tests" "$HOME/.omp/agent/skills/fix-my-tests"
```

Restart the client after installation so it reloads skill metadata.

## Run it

Ask a repo-aware agent a normal question. For example:

```text
Review this repository with Fix My Tests.

I have about 600 mostly AI-generated tests. Which ones are
protecting something important, what am I missing, and what
can I safely delete?
```

Or:

```text
Use Fix My Tests on this repo. The suite is green, but most of
it is mocked and I do not trust it. What evidence do I actually have?
```

The skill preserves your question and answers it at an explicit evidence boundary.

## How it works

The analysis follows one dependency chain:

```text
product behavior
→ material bad outcome
→ failure mechanism
→ right kind of evidence
→ current tests
→ smallest sufficient portfolio
```

Three rules do most of the work:

1. **A real test can still be the wrong kind of evidence.** A unit test may be perfectly falsifiable and still be unable to expose a crash, race, wire-protocol mismatch, or other failure at a different seam.
2. **Hard invariants are noncompensatory.** Lots of easy green tests cannot make up for one uncovered authorization, durability, or other must-not-break property.
3. **Deletion must preserve evidence.** A test is only safe to remove when the material evidence it uniquely provides survives somewhere else.

For the full method, see [`PROTOCOL.md`](fix-my-tests/PROTOCOL.md) and [`RISK_METHOD_MATRIX.md`](fix-my-tests/RISK_METHOD_MATRIX.md).

## Files

| File | Purpose |
| --- | --- |
| [`SKILL.md`](fix-my-tests/SKILL.md) | Agent Skill entry point |
| [`PROTOCOL.md`](fix-my-tests/PROTOCOL.md) | Full analysis procedure |
| [`RISK_METHOD_MATRIX.md`](fix-my-tests/RISK_METHOD_MATRIX.md) | Failure mechanism → evidence method guide |
| [`SIT.md`](fix-my-tests/SIT.md) | Structured analysis output |
| [`RUN_PROMPT.md`](fix-my-tests/RUN_PROMPT.md) | Standalone execution prompt |
| [`VERIFICATION_MAP.md`](fix-my-tests/VERIFICATION_MAP.md) | Risk → evidence implementation map |

## Limits

Fix My Tests is a diagnosis, not a safety certification. It does not modify the target repository, and a clean result does not prove that every possible product risk was discovered.

## License

CC BY 4.0. See [LICENSE.md](LICENSE.md).
