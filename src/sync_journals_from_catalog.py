#!/usr/bin/env python3
"""
Build ``json/journals/*.json`` — one file per distinct journal (ISO abbreviation
or full title) aggregated from all other catalog JSON under ``json/``.

Official ``URL`` values are resolved from the **NLM Catalog** (NCBI E-utilities)
when online; use ``--offline`` to skip HTTP and retain existing URLs.

Run from ``src/``::

    cd src && python sync_journals_from_catalog.py
    python sync_journals_from_catalog.py --offline
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from catalog_sources import repo_json_dir, repo_journals_dir, slugify_segment
from journal_nlm_homepage import nlm_catalog_journal_homepage_url


# Top-level trees that are not citation sources for journal aggregation.
_SKIP_JOURNAL_SOURCES = frozenset({"journals", "projects", "tags"})


def _skip_for_journal_aggregate(path: Path, json_root: Path) -> bool:
    try:
        rel = path.relative_to(json_root)
    except ValueError:
        return False
    return bool(rel.parts) and rel.parts[0] in _SKIP_JOURNAL_SOURCES


def _norm_iso(v) -> str:
    if v is None or v != v:
        return ""
    return str(v).strip()


def _norm_journal(v) -> str:
    if v is None or v != v:
        return ""
    return str(v).strip()


def _canonical_key(iso: str, journal: str) -> str:
    if iso:
        return iso.casefold()
    return slugify_segment(journal, default="unknown-journal")


def _norm_source_section(rec: dict) -> str:
    """Align with ``catalog_sources.normalize_folder_field`` (scalar)."""
    v = rec.get("SECTION")
    if v is None:
        return "MISC"
    try:
        if v != v:  # NaN
            return "MISC"
    except (TypeError, ValueError):
        pass
    s = str(v).strip()
    if not s:
        return "MISC"
    s = re.sub(r"\s+", "_", s)
    s = s.replace("-", "_")
    return s or "MISC"


_SECTION_WRITE_ORDER = (
    "Tools",
    "Sumstats",
    "References",
    "Single_Cell",
    "Biobanks",
    "Projects",
    "Coding",
    "Journals",
    "MISC",
)


def _section_dict_sort_key(item: tuple[str, int]) -> tuple[int, str]:
    sec, _ = item
    try:
        idx = _SECTION_WRITE_ORDER.index(sec)
    except ValueError:
        idx = len(_SECTION_WRITE_ORDER)
    return (idx, sec)


def _unique_stem(base: str, used: set[str]) -> str:
    s = base
    n = 2
    while s in used:
        s = f"{base}-{n}"
        n += 1
    used.add(s)
    return s


def collect_journals(json_root: Path) -> dict[str, dict]:
    """Map canonical_key -> {iso, journal, count, section_counts, examples}."""
    buckets: dict[str, dict] = {}
    for path in sorted(json_root.rglob("*.json")):
        if path.name.startswith("."):
            continue
        if _skip_for_journal_aggregate(path, json_root):
            continue
        with open(path, encoding="utf-8") as f:
            rec = json.load(f)
        iso = _norm_iso(rec.get("ISO"))
        journal = _norm_journal(rec.get("JOURNAL"))
        if not iso and not journal:
            continue
        key = _canonical_key(iso, journal)
        if key not in buckets:
            buckets[key] = {
                "iso": iso,
                "journal": journal,
                "count": 0,
                "section_counts": {},
                "examples": [],
            }
        b = buckets[key]
        b["count"] += 1
        sec = _norm_source_section(rec)
        sc = b["section_counts"]
        sc[sec] = sc.get(sec, 0) + 1
        if iso and (not b["iso"] or len(iso) > len(b["iso"])):
            b["iso"] = iso
        if journal and (not b["journal"] or len(journal) > len(b["journal"])):
            b["journal"] = journal
        name = rec.get("NAME")
        if name and len(b["examples"]) < 5:
            t = str(name).strip()
            if t not in b["examples"]:
                b["examples"].append(t)
    return buckets


def write_journal_files(
    json_root: Path,
    journals_dir: Path,
    *,
    dry_run: bool,
    offline: bool,
) -> int:
    buckets = collect_journals(json_root)
    if not buckets:
        print("No ISO/JOURNAL fields found in catalog JSON.", file=sys.stderr)
        return 1

    journals_dir.mkdir(parents=True, exist_ok=True)
    used_stems: set[str] = set()
    targets: dict[str, Path] = {}

    for key in sorted(buckets.keys()):
        b = buckets[key]
        iso = b["iso"]
        journal = b["journal"]
        display = journal if journal else iso
        if not display:
            continue

        base_stem = slugify_segment(key, default=slugify_segment(display, default="journal"))
        stem = _unique_stem(base_stem, used_stems)
        out_path = journals_dir / f"{stem}.json"
        targets[stem] = out_path

        prev_url = ""
        if out_path.is_file():
            try:
                old = json.loads(out_path.read_text(encoding="utf-8"))
                prev_url = str(old.get("URL") or "").strip()
            except (OSError, json.JSONDecodeError, TypeError):
                prev_url = ""

        if offline or dry_run:
            url = prev_url
        else:
            url = nlm_catalog_journal_homepage_url(iso, journal) or prev_url

        cited_by = dict(
            sorted(b["section_counts"].items(), key=_section_dict_sort_key)
        )
        rec = {
            "NAME": display,
            "SECTION": "Journals",
            "TOPIC": "Index",
            "ISO": iso,
            "JOURNAL": journal,
            "URL": url,
            "ENTRY_COUNT": b["count"],
            "CITED_BY_SECTION": cited_by,
            "_meta": {"source_sheet": "Journals"},
        }
        if b["examples"]:
            rec["EXAMPLE_ENTRIES"] = b["examples"]

        if dry_run:
            print(f"would write {out_path.relative_to(json_root.parent)}")
            continue

        out_path.write_text(
            json.dumps(rec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    if dry_run:
        print(f"Would write {len(targets)} journal file(s) under {journals_dir}.")
        return 0

    for p in journals_dir.glob("*.json"):
        if p.stem not in targets:
            p.unlink()

    print(f"Wrote {len(targets)} journal file(s) under {journals_dir}.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Regenerate json/journals/*.json from catalog.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Do not call NCBI; keep existing URL from each journal JSON if present.",
    )
    parser.add_argument("--json-dir", type=Path, default=None)
    args = parser.parse_args(argv)

    json_root = args.json_dir or repo_json_dir()
    jdir = repo_journals_dir() if args.json_dir is None else (args.json_dir / "journals")
    return write_journal_files(
        json_root, jdir, dry_run=args.dry_run, offline=args.offline
    )


if __name__ == "__main__":
    raise SystemExit(main())
