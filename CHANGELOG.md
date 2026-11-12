# Changelog

The skill version lives in `fix-my-tests/SKILL.md` frontmatter. Earlier releases are recorded by git tags (through `v0.6.0`) and commit history; `v0.7.0` added the public diagnosis line, with mutation (`MUTATE.md`, `PRUNE.md`) added later under the same minor.

## 0.7.1 — 2026-11-12

A patch release: `prune`, `add`, and `prune_and_add` already shipped in 0.7.0. This release tightens how a grant limits the actual action and repairs correctness defects. It adds no new capability.

### Fixed

- Worked example (`examples/TINY.md`): ledger uniqueness, external charging, and crash effects are separate obligations. EV-02 qualifies ledger recording only; RA-01 (double charge) is not `COVERED` by a ledger-row assertion. The `(none)` EV-04 row for a nonexistent test is removed; missing tests sit on the risk/portfolio row. Instructional assumptions and the absence of a run receipt are explicit. Mocks are not treated as inherently common-mode.
- Write authority has one definition: diagnosis is read-only by default; granted modes are `prune`, `add`, `prune_and_add`. `RUN_PROMPT` rule 29, `PROTOCOL` intro and §9, the README limits, and `VERIFICATION_RETROFIT` now agree with `MUTATE.md`.
- `MUTATE.md` intersects the grant with the actual action before repair priority: add-only never removes or relaxes assertions; prune-only never adds new-risk evidence or broadens product changes; `F` is not a permission wildcard; urgency cannot expand authorization; out-of-grant dependencies are reported while independent authorized work proceeds; a real product defect is never erased by deleting its test.
- A test grant, including `prune_and_add` or “fix them”, no longer reads as authority to change production behavior. Report a real product defect; repair the production owner only within the original authorized ask (the operator named that owner and the intended behavior). `SKILL.md`, `RUN_PROMPT.md` rule 29, `PROTOCOL.md` §13, and `PRUNE.md` agree.
- `PRINCIPLES.md` no longer points to a process sequence or scale table that this pack does not contain. Tiny versus campaign selection lives in `SKILL.md`. The terms sitting, constitution, and scale are defined in the pack.
- The wedding-app case no longer claims prevalence (“normal outcome”) or that meaningful payment/identity evidence must be live, and no longer cites a path in a private repository. The h11 case remains explicitly retrospective.
- `LICENSE.md` contained a display-clipping marker (`[Showing lines 1-300 of 397 …]`) in the middle of section 5(b). The complete CC BY 4.0 International legal code is restored; the file is byte-equal to creativecommons.org `legalcode.txt`.

### Added

- `scripts/check_refs.py`: a standard-library check that every local markdown link and pack-file mention under `fix-my-tests/` resolves, and that no private path or non-public `skill://` URI appears. `--forbid TERM` (repeatable) also fails on any listed term.
