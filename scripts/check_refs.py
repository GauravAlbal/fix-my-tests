#!/usr/bin/env python3
"""Resolve local markdown links and pack-file mentions under fix-my-tests/.

Stdlib only. Exit 0 when every local target exists and no private path,
non-public skill:// URI, or forbidden term (repeatable --forbid TERM) is present.

Usage: check_refs.py [PACK_DIR] [--forbid TERM ...]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

PUBLIC_SKILLS = {
    "fix-my-tests",
    "fix-my-requirements",
    "proof",
    "done",
    "ddx",
    "scope",
    "simplify",
}

LINK_RE = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)]+)\)")
SKILL_RE = re.compile(r"skill://([a-z0-9-]+)", re.IGNORECASE)
PRIVATE_PATH_RE = re.compile(r"(?:/Users/|~/repos)")
# Pack docs / scripts, not example production files (bill.py) or code identifiers.
PACK_FILE_RE = re.compile(
    r"`((?:[\w.-]+/)*[A-Za-z][\w.-]*\.(?:md|py|yml|yaml|json))`"
)
FENCE_RE = re.compile(r"^```")


def strip_anchor(url: str) -> str:
    url = url.strip()
    if url.startswith("<") and url.endswith(">"):
        url = url[1:-1]
    url = url.split()[0] if url else url
    return url.split("#", 1)[0]


def is_external(url: str) -> bool:
    u = url.strip().lower()
    return u.startswith(
        ("http://", "https://", "mailto:", "data:", "ftp://", "skill://")
    ) or u.startswith("#")


def iter_md_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*.md") if p.is_file())


def prose_lines(text: str) -> list[tuple[int, str]]:
    """Line numbers (1-based) and text, excluding fenced code."""
    out: list[tuple[int, str]] = []
    fenced = False
    for i, line in enumerate(text.splitlines(), 1):
        if FENCE_RE.match(line.strip()):
            fenced = not fenced
            continue
        if not fenced:
            out.append((i, line))
    return out


def resolve_local(path: Path, url: str, pack_root: Path) -> Path | None:
    target = strip_anchor(url)
    if not target or is_external(target) or target.startswith(("`", "{")):
        return None
    if PRIVATE_PATH_RE.search(target):
        return Path(target)
    p = Path(target)
    if p.is_absolute():
        return p
    from_file = (path.parent / p).resolve()
    from_pack = (pack_root / p).resolve()
    if from_file.exists():
        return from_file
    return from_pack


def forbidden_terms(line: str, terms: list[str]) -> list[str]:
    return [t for t in terms if re.search(rf"\b{re.escape(t)}\b", line, re.IGNORECASE)]


def check_pack(pack_root: Path, forbid: list[str] | None = None) -> list[str]:
    forbid = forbid or []
    errors: list[str] = []
    pack_root = pack_root.resolve()
    if not pack_root.is_dir():
        return [f"missing pack directory: {pack_root}"]

    pack_files = {p.resolve() for p in pack_root.rglob("*") if p.is_file()}

    for md in iter_md_files(pack_root):
        text = md.read_text(encoding="utf-8")
        rel = md.relative_to(pack_root.parent) if pack_root.parent in md.parents else md
        for lineno, line in prose_lines(text):
            loc = f"{rel}:{lineno}"

            if PRIVATE_PATH_RE.search(line):
                errors.append(f"{loc}: private path (/Users/ or ~/repos)")

            for m in SKILL_RE.finditer(line):
                name = m.group(1).lower()
                if name not in PUBLIC_SKILLS:
                    errors.append(f"{loc}: non-public skill://{name}")

            for term in forbidden_terms(line, forbid):
                errors.append(f"{loc}: forbidden term {term!r}")

            for m in LINK_RE.finditer(line):
                url = m.group(2).strip()
                if is_external(url):
                    if url.lower().startswith("skill://"):
                        continue
                    continue
                if PRIVATE_PATH_RE.search(url):
                    errors.append(f"{loc}: private path in link {url!r}")
                    continue
                resolved = resolve_local(md, url, pack_root)
                if resolved is None:
                    continue
                if not resolved.exists():
                    errors.append(f"{loc}: missing link target {url!r}")

            for m in PACK_FILE_RE.finditer(line):
                mention = m.group(1)
                if PRIVATE_PATH_RE.search(mention):
                    errors.append(f"{loc}: private path in file mention {mention!r}")
                    continue
                if Path(mention).name.lower() in {"bill.py", "test_bill.py"}:
                    continue
                candidate = Path(mention)
                hits = []
                if not candidate.is_absolute():
                    hits.append((md.parent / candidate).resolve())
                    hits.append((pack_root / candidate).resolve())
                    hits.append((pack_root / Path(mention).name).resolve())
                else:
                    hits.append(candidate)
                if not any(h.exists() for h in hits):
                    # Allow a mention of a file that exists anywhere in the pack
                    # by basename only when it is unique.
                    basename = Path(mention).name
                    matches = [p for p in pack_files if p.name == basename]
                    if len(matches) != 1:
                        errors.append(f"{loc}: missing file mention {mention!r}")

    return errors


def parse_args(argv: list[str]) -> tuple[Path | None, list[str]]:
    pack: Path | None = None
    forbid: list[str] = []
    args = iter(argv[1:])
    for arg in args:
        if arg == "--forbid":
            term = next(args, None)
            if not term:
                raise SystemExit("check_refs: --forbid needs a TERM")
            forbid.append(term)
        else:
            pack = Path(arg).resolve()
    return pack, forbid


def main(argv: list[str]) -> int:
    here = Path(__file__).resolve()
    repo = here.parent.parent
    pack, forbid = parse_args(argv)
    pack = pack or repo / "fix-my-tests"
    errors = check_pack(pack, forbid)
    if errors:
        print("check_refs: FAIL")
        for e in errors:
            print(e)
        return 1
    print(f"check_refs: ok ({pack})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
