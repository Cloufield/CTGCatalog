"""Validate internal links in generated docs/*.md (targets + optional #fragments)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from print_level import iter_markdown_inline_links

_HTML_HREF = re.compile(r"""href\s*=\s*(")([^"]+)(")|href\s*=\s*(')([^']+)(')""", re.IGNORECASE)
_ID_ATTR = re.compile(r"""id\s*=\s*["']([^"']+)["']""", re.IGNORECASE)


def _repo_docs_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "docs"


def _split_href(raw: str) -> tuple[str, str | None]:
    raw = raw.strip()
    if "#" in raw:
        path_part, frag = raw.split("#", 1)
        frag = frag.strip() or None
    else:
        path_part, frag = raw, None
    path_part = path_part.split("?", 1)[0].strip()
    return path_part, frag


def _is_external(path_part: str) -> bool:
    pl = path_part.lower()
    return pl.startswith(
        ("http://", "https://", "mailto:", "tel:", "javascript:", "//")
    )


def _normalize_to_docs_relpath(path_part: str) -> str:
    """Map href path to a path relative to docs/ (POSIX-style), from docs root only."""
    p = path_part.strip()
    while p.startswith("/"):
        p = p[1:]
    while p.startswith("../"):
        p = p[3:]
    while p.startswith("./"):
        p = p[2:]
    p = p.rstrip("/")
    if not p:
        return ""
    name = Path(p).name
    if "." not in name:
        p = f"{p}.md"
    return p.replace("\\", "/")


def _resolve_internal_md_target(docs_dir: Path, src: Path, path_part: str) -> Path | None:
    """Resolve path_part relative to src's directory; return existing *.md under docs_dir."""
    p = path_part.split("#")[0].split("?")[0].strip()
    if not p:
        return None
    root = docs_dir.resolve()
    try:
        cand = (src.parent / p).resolve(strict=False)
        cand.relative_to(root)
    except (ValueError, OSError, RuntimeError):
        return None
    if cand.is_file() and cand.suffix == ".md":
        return cand
    if cand.is_dir():
        idx = cand / "index.md"
        if idx.is_file():
            return idx
    md_path = cand.with_suffix(".md")
    if md_path.is_file():
        return md_path
    return None


def _fragment_defined(content: str, frag: str) -> bool:
    for m in _ID_ATTR.finditer(content):
        if m.group(1) == frag:
            return True
    return False


def check_docs_internal_links(docs_dir: Path | None = None) -> list[str]:
    """
    Walk docs_dir for *.md, collect internal hrefs from markdown + HTML.
    Returns a list of error messages (empty if all OK).
    """
    docs_dir = (docs_dir or _repo_docs_dir()).resolve()
    if not docs_dir.is_dir():
        return [f"Link check: docs directory missing: {docs_dir}"]

    errors: list[str] = []
    md_files = sorted(docs_dir.rglob("*.md"))
    content_cache: dict[Path, str] = {}

    for src in md_files:
        try:
            text = src.read_text(encoding="utf-8")
        except OSError as e:
            errors.append(f"{src}: cannot read ({e})")
            continue
        lines = text.splitlines()
        try:
            src_disp = src.relative_to(docs_dir).as_posix()
        except ValueError:
            src_disp = src.name

        def note_line(url: str) -> int:
            for i, line in enumerate(lines, start=1):
                if url in line:
                    return i
            return 0

        seen_in_file: set[tuple[str, str | None]] = set()

        def check_url(url: str) -> None:
            path_part, frag = _split_href(url)
            if _is_external(path_part):
                return
            if path_part == "":
                if frag is None:
                    return
                target = src
            else:
                target = _resolve_internal_md_target(docs_dir, src, path_part)
                if target is None or not target.is_file():
                    try:
                        asset = (src.parent / path_part).resolve(strict=False)
                        asset.relative_to(docs_dir)
                        if asset.is_file() and asset.suffix.lower() in {
                            ".html",
                            ".htm",
                            ".svg",
                            ".json",
                            ".png",
                            ".jpg",
                            ".jpeg",
                            ".webp",
                            ".gif",
                        }:
                            return
                    except (ValueError, OSError):
                        pass
                    rel_try = _normalize_to_docs_relpath(path_part)
                    target = docs_dir / rel_try if rel_try else None
                    if target is None or not target.is_file():
                        ln = note_line(url)
                        errors.append(
                            f"{src_disp}:{ln or '?'}: missing target {url!r} "
                            f"(from path {path_part!r})"
                        )
                        return

            key = (str(target), frag)
            if key in seen_in_file:
                return
            seen_in_file.add(key)

            if frag is None:
                return
            if target not in content_cache:
                try:
                    content_cache[target] = target.read_text(encoding="utf-8")
                except OSError as e:
                    errors.append(
                        f"{src_disp}: cannot read fragment target {target.name} ({e})"
                    )
                    return
            tgt_text = content_cache[target]
            if not _fragment_defined(tgt_text, frag):
                ln = note_line(url)
                errors.append(
                    f"{src_disp}:{ln or '?'}: missing anchor #{frag!r} in "
                    f"{target.relative_to(docs_dir).as_posix()} (from {url!r})"
                )

        for _s, _e, _lab, href in iter_markdown_inline_links(text):
            check_url(href.strip())

        for m in _HTML_HREF.finditer(text):
            url = m.group(2) or m.group(5)
            if url:
                check_url(url.strip())

    return errors


def run_link_check(docs_dir: Path | None = None) -> int:
    errs = check_docs_internal_links(docs_dir)
    if errs:
        print("Link check: FAILED", file=sys.stderr)
        for e in errs:
            print(f"  {e}", file=sys.stderr)
        return 1
    print("Link check: OK.")
    return 0
