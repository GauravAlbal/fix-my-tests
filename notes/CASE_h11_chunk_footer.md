# Case: 78 green tests, one unchecked byte pair

**Repository:** `python-hyper/h11` — **revision audited:** `dff7cc3~1` (the commit before the fix)
**Suite at that revision:** `78 passed in 0.30s` (run for this sitting, not remembered)
**What happened next:** `dff7cc3` — *Validate Chunked-Encoding chunk footer* — shipped the missing check.
**Advisory:** CVE-2025-43859.

This is not a security review. h11 is a well-run project with a real suite. It is here because it is the cheapest honest demonstration of the thing this skill claims to catch: a suite that is green, deterministic, and falsifiable, whose tests cannot distinguish correct behaviour from incorrect behaviour on the risk that later broke.

---

## Risk register

| Risk | Product surface | Material bad outcome | Obligation |
|---|---|---|---|
| RA-01 | HTTP/1.1 chunked body parser (`ChunkedReader`) | Two HTTP processors in one request path disagree about where a body ends → request smuggling / response desync | `HARD_INVARIANT` |

**Failure mechanism.** After a chunk's declared bytes, the parser consumed two bytes and discarded them without checking that they were `CRLF`. Any downstream processor that keeps reading to the next `CRLF` — as several do — ends at a different offset. Two parsers, one request, two interpretations.

**Required evidence capability.** Adversarial chunk terminators: a body whose declared length is honoured but whose trailing bytes are not `CRLF`, plus one-byte-mismatch variants; the parser must reject each with `LocalProtocolError`. Correctness here means *rejecting*, so the oracle has to be the invariant, not the decoder's output.

## Existing evidence, as qualified

What the suite at `dff7cc3~1` actually contains around this surface:

| Existing test | Covers | Qualification for RA-01 |
|---|---|---|
| `test_ChunkedReader` — well-formed bodies, extensions, split buffers | decoding correctness on valid input | `VALID` for decoding, `UNQUALIFIED` for framing — every case is well-formed, so an unchecked suffix costs nothing |
| `test_ChunkedReader` — oversized chunk size, garbage chunk count | rejects malformed *sizes* | `VALID` for size parsing, `UNQUALIFIED` for terminators — the malformed cases stop before the footer |
| `test_chunk_boundaries`, `test_chunked` (connection level) | event sequencing | `UNQUALIFIED` — asserts on well-formed framing only |

Nothing in the repository, at that revision, referenced a chunk footer at all:

```
$ grep -rn "footer\|malformed chunk" h11/tests/*.py
(no matches)
```

**Portfolio status:** `GAP`. **Disposition:** `ADD_EVIDENCE`.

## First move

Add the three negative cases the fix itself added — one per distinct mismatch, because a length check that reads the wrong pair passes two of them:

```python
t_body_reader(ChunkedReader, b"3\r\nxxx__1a\r\n", [LocalProtocolError])   # neither byte is CR/LF
t_body_reader(ChunkedReader, b"3\r\nxxx\r_1a\r\n", [LocalProtocolError])   # first byte only
t_body_reader(ChunkedReader, b"3\r\nxxx_\n1a\r\n", [LocalProtocolError])   # second byte only
```

Run against both revisions for this note — accepted before, rejected after:

```text
BEFORE fix (dff7cc3~1)
  b'3\r\nxxx__1a\r\n' -> ACCEPTED as [Data(data=b'xxx', ...)]
  b'3\r\nxxx\r_1a\r\n' -> ACCEPTED as [Data(data=b'xxx', ...)]
  b'3\r\nxxx_\n1a\r\n' -> ACCEPTED as [Data(data=b'xxx', ...)]

AFTER fix (dff7cc3)
  b'3\r\nxxx__1a\r\n' -> rejected: malformed chunk footer: b'__' (expected b'\r\n')
  b'3\r\nxxx\r_1a\r\n' -> rejected: malformed chunk footer: b'\r_' (expected b'\r\n')
  b'3\r\nxxx_\n1a\r\n' -> rejected: malformed chunk footer: b'_\n' (expected b'\r\n')
```

That is what makes them evidence rather than decoration: they can fail for the reason the risk names.

## What this demonstrates, and what it does not

It demonstrates that "78 tests pass" is a statement about the tests. The suite was not weak; it was **pointed at a different question** than the one that mattered, because every test was written from valid input and the failure lived in invalid input.

It does not demonstrate that this skill would have prevented the CVE — h11 was audited after the fact, by reading the fix. Nor does it claim the maintainers did anything wrong; the advisory came from an external report, and the fix is careful. The claim is narrower and more useful: **the gap was visible from the tests alone, before the fix existed, by asking what could break rather than what is covered.**

## Reproduction

```bash
git clone https://github.com/python-hyper/h11
cd h11 && git checkout dff7cc3~1
python -m pytest -q                     # 78 passed
grep -rn "footer" h11/tests/*.py        # no matches
```

Then ask this skill for a read-only diagnosis of the chunked reader, and compare the risk register to the list above.
