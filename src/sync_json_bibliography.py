#!/usr/bin/env python3
"""
Fetch PubMed metadata via Entrez, cache XML under .cache/pubmed/, and merge
bibliography fields into catalog JSON files (same shape ``load_data`` expects).

Run from ``src/``::

    cd src && python sync_json_bibliography.py
    python sync_json_bibliography.py --only-missing
    python sync_json_bibliography.py --force
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from catalog_sources import is_catalog_json_file, repo_json_dir
from pubmed_entrez import (
    catalog_biblio_from_pubmed_parsed,
    fetch_pubmed_batch_cached,
    parse_cached_pmid,
    pubmed_cache_dir,
)

def _normalize_pmid(value) -> str | None:
    if value is None or value != value:  # NaN
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return str(value)
    s = str(value).strip()
    if not s:
        return None
    m = re.sub(r"\D", "", s)
    return m or None


def _iter_catalog_json_paths(json_dir: Path) -> list[Path]:
    paths = []
    for path in sorted(json_dir.rglob("*.json")):
        if not is_catalog_json_file(json_dir, path):
            continue
        paths.append(path)
    return paths


def _needs_biblio(rec: dict, only_missing: bool) -> bool:
    if not only_missing:
        return True
    authors = rec.get("Authors")
    title = rec.get("TITLE")
    citation = rec.get("CITATION")
    a_ok = authors is not None and str(authors).strip() != ""
    t_ok = title is not None and str(title).strip() != ""
    c_ok = citation is not None and str(citation).strip() != ""
    return not (a_ok and t_ok and c_ok)


def _write_record(path: Path, rec: dict) -> None:
    meta = rec.pop("_meta", None)
    ordered = {k: v for k, v in rec.items()}
    if meta is not None:
        ordered["_meta"] = meta
        rec["_meta"] = meta
    path.write_text(
        json.dumps(ordered, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Merge PubMed bibliography fields into catalog JSON under json/."
    )
    parser.add_argument(
        "--only-missing",
        action="store_true",
        help="Only update files lacking both TITLE and Authors",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Refetch PubMed XML (ignore .cache/pubmed/)",
    )
    parser.add_argument(
        "--json-dir",
        type=Path,
        default=None,
        help="Default: repository json/",
    )
    args = parser.parse_args(argv)

    json_dir = args.json_dir or repo_json_dir()
    if not json_dir.is_dir():
        print(f"Missing JSON directory: {json_dir}", file=sys.stderr)
        return 1

    cache_dir = pubmed_cache_dir(json_dir.parent)
    paths = _iter_catalog_json_paths(json_dir)

    pmid_to_paths: dict[str, list[Path]] = {}
    path_records: dict[Path, dict] = {}

    for path in paths:
        with open(path, encoding="utf-8") as f:
            rec = json.load(f)
        pmid = _normalize_pmid(rec.get("PMID"))
        if not pmid:
            continue
        if not _needs_biblio(rec, args.only_missing):
            continue
        pmid_to_paths.setdefault(pmid, []).append(path)
        path_records[path] = rec

    unique_pmids = sorted(pmid_to_paths.keys())
    if not unique_pmids:
        print("No JSON entries to update (check PMID / --only-missing).")
        return 0

    print(f"Fetching {len(unique_pmids)} unique PMIDs (cache: {cache_dir}) …")
    fetch_pubmed_batch_cached(
        unique_pmids,
        cache_dir=cache_dir,
        force=args.force,
    )

    updated = 0
    failed: list[tuple[str, str]] = []
    for pmid in unique_pmids:
        parsed = parse_cached_pmid(pmid, cache_dir=cache_dir)
        if not parsed or not (parsed.get("Authors") or "").strip():
            for p in pmid_to_paths[pmid]:
                failed.append((str(p), pmid))
            continue
        biblio = catalog_biblio_from_pubmed_parsed(parsed)
        for path in pmid_to_paths[pmid]:
            rec = path_records[path]
            for k, v in biblio.items():
                rec[k] = v
            _write_record(path, rec)
            updated += 1

    print(f"Updated {updated} JSON file(s).")
    if failed:
        print(f"Skipped {len(failed)} file(s) with no PubMed record:", file=sys.stderr)
        for fp, pid in failed[:20]:
            print(f"  PMID {pid}: {fp}", file=sys.stderr)
        if len(failed) > 20:
            print(f"  … and {len(failed) - 20} more", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
