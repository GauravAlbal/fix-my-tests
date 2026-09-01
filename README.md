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

It is a read-only [Agent Skill](https://agentskills.io/). It inspects your repository and tells you what your tests actually protect, what they miss, and what to do about it. It does not rewrite your tests.

## Try it now — no install

Paste this into any coding agent (Claude, Cursor, Windsurf, Copilot, etc.) that can read web links:

```text
Use Fix My Tests on this repository.

Read the skill at:
https://github.com/GauravAlbal/fix-my-tests/tree/main/fix-my-tests

Start with SKILL.md and follow the required references. Work read-only.

My question:
<put your test-system question here>
```

The skill files contain detailed instructions for the agent — you just need to add your question at the bottom.

<details><summary>Advanced prompt with full constraints</summary>

For more control over the analysis, use this expanded version:

```text
Use Fix My Tests on this repository.

Read the current skill at:
https://github.com/GauravAlbal/fix-my-tests/tree/main/fix-my-tests

Start with SKILL.md and obey the required sibling references. Work read-only.
Preserve my exact question. Derive the material product risks before inspecting
my tests. For each risk, derive the failure mechanism and the evidence capability
that could actually expose it. Then qualify the current tests, including whether
their oracle is independent of the implementation they judge.

Tell me what to keep, fix, add, delete, downgrade, or move. Return at most five
first moves, answer my question at an explicit evidence boundary, and choose one
first-repair exit. Do not claim the repository is safe.

My question:
<put your test-system question here>
```

</details>

If your agent cannot read the linked skill, install it once instead.

## Use it when

- Claude, Codex, or another agent generated a pile of tests and you do not know which ones matter.
- The suite is green but you do not trust it.
- CI is slow or flaky and you want to remove tests safely.
- The tests are heavily mocked or implementation-coupled and you are unsure what they prove.
- The AI-generated tests seem to just copy your code's logic into the expected answers — so they pass but prove nothing.
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

A run tells you which risks it found, what your current tests actually prove, what is missing, and a short list of concrete next steps.

Here is a condensed example of what a finding looks like:

```text
## Risk: Payment succeeds but access is not granted

Surface: Stripe webhook → entitlement grant
Obligation: HARD INVARIANT — this must never break
Failure mechanism: the test mocks the boundary it needs to check

Current evidence:
  webhook_handler_test.py — unit test with mocked provider payload

Finding: WRONG METHOD
  The test checks handler logic in isolation. It cannot detect a
  mismatch between the real Stripe event and your production
  metadata path because the provider boundary is mocked.

Move:
  Keep the unit test for handler logic.
  Add one integration check at the real provider boundary.
```

Fix My Tests can also conclude that a test is useful, that deletion is unsafe, or that the available evidence is not enough to decide.

## Install as an Agent Skill

The Agent Skills artifact is the [`fix-my-tests/`](fix-my-tests/) directory. The repository root just carries the README, license, and project material around it.

Agent Skills defines the skill format, not one universal install location. Point your client's skill discovery root at that directory.

For clients that discover user skills under `~/.agents/skills/`:

```sh
git clone --depth 1 https://github.com/GauravAlbal/fix-my-tests.git \
  "$HOME/.local/share/fix-my-tests"
mkdir -p "$HOME/.agents/skills"
ln -s "$HOME/.local/share/fix-my-tests/fix-my-tests" \
  "$HOME/.agents/skills/fix-my-tests"
```
Other agent clients may use a different skill directory — check your client's documentation for the correct path.

Restart the client after first install so it reloads skill metadata.

To update later, pull the same checkout; no relinking is needed:

```sh
git -C "$HOME/.local/share/fix-my-tests" pull --ff-only
```

If you already cloned the repository elsewhere, skip the clone and symlink that checkout's `fix-my-tests/` directory into your client's discovery root.

## Run it after installation

Ask a normal repo-level question. For example:

```text
Use Fix My Tests on this repo.

I have about 600 mostly AI-generated tests. Which ones are protecting
something important, what am I missing, and what can I safely delete?
```

Or:

```text
Use Fix My Tests on this repo. The suite is green, but most of it is mocked
and I do not trust it. What evidence do I actually have?
```

The skill preserves your question and gives you a direct answer with a clear boundary around what was and was not checked.

## How it works

The analysis follows one chain:

```text
what does the product do?
→ what bad outcome would actually matter?
→ how could that failure happen?
→ what kind of test could catch it?
→ do the current tests actually do that?
→ smallest set of tests that covers what matters
```

Five rules do most of the work:

1. **A passing test can still miss the real bug.** A unit test for your payment handler won't catch a crash between two database writes. The test is fine — it's just testing the wrong thing.
2. **A test needs an independent source of truth.** If the test computes its expected answer using the same logic as your code, it'll catch changes but can't tell you if the answer was right in the first place.
3. **Snapshots prove "nothing changed," not "this is correct."** A golden file from six months ago can tell you something shifted. It can't tell you the original output was right.
4. **Some bugs only appear in specific combinations.** When a failure requires admin + dark mode + v2 API, a handful of examples won't find it. You need systematic coverage of the interactions.
5. **Only delete a test when something else covers what it protects.** If nothing else catches that failure, the test stays — even if it's ugly.

Must-not-break properties (authorization, data durability, payment correctness) cannot be offset by passing tests elsewhere. One gap in something critical matters more than a hundred greens on easy stuff.

For the full method, see [`PROTOCOL.md`](fix-my-tests/PROTOCOL.md) and [`RISK_METHOD_MATRIX.md`](fix-my-tests/RISK_METHOD_MATRIX.md).

## Agent Skills format

`fix-my-tests/` follows the open [Agent Skills specification](https://agentskills.io/specification). Maintainers can validate the skill with:

```sh
uvx --from skills-ref agentskills validate ./fix-my-tests
```

## Files

| File | Purpose |
| --- | --- |
| [`SKILL.md`](fix-my-tests/SKILL.md) | Entry point — tells the agent when and how to run |
| [`PROTOCOL.md`](fix-my-tests/PROTOCOL.md) | Full analysis procedure |
| [`RISK_METHOD_MATRIX.md`](fix-my-tests/RISK_METHOD_MATRIX.md) | How to match failure types to the right kind of test |
| [`SIT.md`](fix-my-tests/SIT.md) | Output template the agent fills in |
| [`RUN_PROMPT.md`](fix-my-tests/RUN_PROMPT.md) | Execution rules and constraints |
| [`VERIFICATION_MAP.md`](fix-my-tests/VERIFICATION_MAP.md) | Risk → test implementation plan |

## Limits

Fix My Tests is a diagnosis, not a safety certification. It does not modify the target repository, and a clean result does not prove that every possible product risk was discovered.

## License

CC BY 4.0. See [LICENSE.md](LICENSE.md).
