#!/usr/bin/env python3
"""
Stream PubMed baseline Medline XML (.xml.gz), aggregate GWAS-related term trends
by year and journal rankings for a configurable year window.

Designed for local NCBI baseline dumps (e.g. pubmed26n0001.xml.gz). Uses
iterparse + element clear for bounded memory; optional parallel workers per file.

Workflow (large corpora):
  1. Parse each baseline file and write a raw JSON shard under ``--shards-dir``
     (default: ``<out-dir>/shards/*.shard.json``). Use ``--skip-existing`` to
     resume. Use ``--shard-only`` to only produce shards.
  2. Run ``--summarize-only --shards-dir ... --out-dir ...`` to merge all
     ``*.shard.json`` into the final CSVs (year window must match across shards).
"""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import re
import sys
import time
import xml.etree.ElementTree as ET
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import date
from multiprocessing import cpu_count
from pathlib import Path


def _tag_local(tag: str) -> str:
    if tag.startswith("{"):
        return tag.rsplit("}", 1)[-1]
    return tag


def _find_child(parent: ET.Element, name: str) -> ET.Element | None:
    for c in parent:
        if _tag_local(c.tag) == name:
            return c
    return None


def _findall_children(parent: ET.Element, name: str) -> list[ET.Element]:
    return [c for c in parent if _tag_local(c.tag) == name]


def _parse_year_from_string(s: str) -> int | None:
    s = s.strip()
    if len(s) >= 4 and s[:4].isdigit():
        y = int(s[:4])
        if 1800 <= y <= 2100:
            return y
    return None


def _parse_medline_date_year(s: str) -> int | None:
    m = re.match(r"(\d{4})", s.strip())
    if m:
        return _parse_year_from_string(m.group(1))
    return None


def _extract_pub_year(medline: ET.Element) -> int | None:
    article = _find_child(medline, "Article")
    if article is None:
        return None
    journal = _find_child(article, "Journal")
    if journal is not None:
        issue = _find_child(journal, "JournalIssue")
        if issue is not None:
            pubdate = _find_child(issue, "PubDate")
            if pubdate is not None:
                y_el = _find_child(pubdate, "Year")
                if y_el is not None and y_el.text:
                    py = _parse_year_from_string(y_el.text)
                    if py is not None:
                        return py
                md = _find_child(pubdate, "MedlineDate")
                if md is not None and md.text:
                    py = _parse_medline_date_year(md.text)
                    if py is not None:
                        return py
    for ad in _findall_children(article, "ArticleDate"):
        y_el = _find_child(ad, "Year")
        if y_el is not None and y_el.text:
            py = _parse_year_from_string(y_el.text)
            if py is not None:
                return py
    return None


def _extract_journal_key_title(medline: ET.Element, article: ET.Element) -> tuple[str, str]:
    key = ""
    title = ""
    mj = _find_child(medline, "MedlineJournalInfo")
    if mj is not None:
        ta = _find_child(mj, "MedlineTA")
        if ta is not None and ta.text:
            key = ta.text.strip()
    journal = _find_child(article, "Journal")
    if journal is not None:
        jt = _find_child(journal, "Title")
        if jt is not None and jt.text:
            title = jt.text.strip()
        if not key:
            iso = _find_child(journal, "ISOAbbreviation")
            if iso is not None and iso.text:
                key = iso.text.strip()
    if not key:
        key = title or "UNKNOWN"
    if not title:
        title = key
    return key, title


def _collect_title_abstract_keywords(article: ET.Element) -> str:
    parts: list[str] = []
    t_el = _find_child(article, "ArticleTitle")
    if t_el is not None:
        parts.append("".join(t_el.itertext()))
    abs_el = _find_child(article, "Abstract")
    if abs_el is not None:
        for child in abs_el:
            if _tag_local(child.tag) == "AbstractText":
                parts.append("".join(child.itertext()))
    kw_list = _find_child(article, "KeywordList")
    if kw_list is not None:
        for kw in _findall_children(kw_list, "Keyword"):
            parts.append("".join(kw.itertext()))
    return " \n ".join(p for p in parts if p)


def _mesh_has_gwas(medline: ET.Element) -> bool:
    mesh_list = _find_child(medline, "MeshHeadingList")
    if mesh_list is None:
        return False
    for mh in _findall_children(mesh_list, "MeshHeading"):
        dn = _find_child(mh, "DescriptorName")
        if dn is not None:
            text = "".join(dn.itertext()).strip().lower()
            if "genome-wide association" in text:
                return True
    return False


# Trend buckets: pre-compiled regex lists (case-insensitive).
_BUCKET_PATTERNS: dict[str, list[re.Pattern[str]]] = {
    "text_GWAS_core": [
        re.compile(r"genome[-\s]wide\s+association", re.I),
        re.compile(r"\bgwas(?:es)?\b", re.I),
        re.compile(r"\bgwa\s+stud", re.I),
    ],
    "text_PRS": [
        re.compile(r"polygenic\s+risk", re.I),
        re.compile(r"\bprs\b", re.I),
        re.compile(r"polygenic\s+score", re.I),
    ],
    "text_MR": [
        re.compile(r"mendelian\s+randomi[sz]ation", re.I),
    ],
}


def _text_bucket_hits(blob: str) -> set[str]:
    hits: set[str] = set()
    for bucket, pats in _BUCKET_PATTERNS.items():
        if any(p.search(blob) for p in pats):
            hits.add(bucket)
    return hits


def _is_gwas_related(mesh_gwas: bool, blob: str) -> bool:
    if mesh_gwas:
        return True
    return bool(_text_bucket_hits(blob) & {"text_GWAS_core"})


SHARD_SUFFIX = ".shard.json"
SCHEMA_VERSION = 2
# Unlikely in bucket names; avoids ambiguity vs journal keys with tabs.
TREND_KEY_SEP = "\x1f"


@dataclass
class ShardResult:
    trends: Counter[tuple[int, str]]
    journal_total: Counter[str]
    journal_gwas: Counter[str]
    journal_title: dict[str, str]
    journal_total_by_year: Counter[tuple[int, str]]
    journal_gwas_by_year: Counter[tuple[int, str]]


def _shard_stem(src: Path) -> str:
    name = src.name
    if name.endswith(".xml.gz"):
        return name[: -len(".xml.gz")]
    return src.stem


def _shard_path_for_source(shards_dir: Path, src: Path) -> Path:
    return shards_dir / f"{_shard_stem(src)}{SHARD_SUFFIX}"


def _encode_trend_key(year: int, bucket: str) -> str:
    return f"{year}{TREND_KEY_SEP}{bucket}"


def _decode_trend_key(key: str) -> tuple[int, str]:
    year_s, bucket = key.split(TREND_KEY_SEP, 1)
    return int(year_s), bucket


def write_shard_json(
    shard_path: Path,
    source: Path,
    year_min: int,
    year_max: int,
    result: ShardResult,
) -> None:
    trends_obj = {
        _encode_trend_key(y, b): int(c) for (y, b), c in result.trends.items()
    }
    jby: dict[str, dict[str, dict[str, int]]] = {}
    for (y, jk), c in result.journal_total_by_year.items():
        ys = str(y)
        jby.setdefault(ys, {"journal_total": {}, "journal_gwas": {}})[
            "journal_total"
        ][jk] = int(c)
    for (y, jk), c in result.journal_gwas_by_year.items():
        ys = str(y)
        block = jby.setdefault(ys, {"journal_total": {}, "journal_gwas": {}})
        block["journal_gwas"][jk] = int(c)

    doc: dict = {
        "schema_version": SCHEMA_VERSION,
        "source_file": source.name,
        "source_path": str(source.resolve()),
        "year_min": year_min,
        "year_max": year_max,
        "trends": trends_obj,
        "journal_total": dict(result.journal_total),
        "journal_gwas": dict(result.journal_gwas),
        "journal_title": result.journal_title,
        "journal_by_year": jby,
    }
    shard_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = shard_path.with_suffix(shard_path.suffix + ".tmp")
    tmp.write_text(json.dumps(doc, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(shard_path)


def read_shard_json(shard_path: Path) -> tuple[ShardResult, dict]:
    raw = json.loads(shard_path.read_text(encoding="utf-8"))
    trends: Counter[tuple[int, str]] = Counter()
    for k, v in raw.get("trends", {}).items():
        y, b = _decode_trend_key(k)
        trends[(y, b)] = int(v)
    jt_y: Counter[tuple[int, str]] = Counter()
    jg_y: Counter[tuple[int, str]] = Counter()
    for y_str, block in raw.get("journal_by_year", {}).items():
        y = int(y_str)
        for jk, c in block.get("journal_total", {}).items():
            jt_y[(y, jk)] = int(c)
        for jk, c in block.get("journal_gwas", {}).items():
            jg_y[(y, jk)] = int(c)
    result = ShardResult(
        trends=trends,
        journal_total=Counter(raw.get("journal_total", {})),
        journal_gwas=Counter(raw.get("journal_gwas", {})),
        journal_title=dict(raw.get("journal_title", {})),
        journal_total_by_year=jt_y,
        journal_gwas_by_year=jg_y,
    )
    return result, raw


def discover_shard_files(shards_dir: Path) -> list[Path]:
    return sorted(shards_dir.glob(f"*{SHARD_SUFFIX}"))


def load_and_merge_shards(
    shard_paths: list[Path],
) -> tuple[
    Counter[tuple[int, str]],
    Counter[str],
    Counter[str],
    dict[str, str],
    Counter[tuple[int, str]],
    Counter[tuple[int, str]],
    dict[str, int],
]:
    """Merge shard JSON files; raises ValueError on year window mismatch."""
    if not shard_paths:
        raise ValueError("No shard files to merge.")
    trends: Counter[tuple[int, str]] = Counter()
    journal_total: Counter[str] = Counter()
    journal_gwas: Counter[str] = Counter()
    journal_title: dict[str, str] = {}
    journal_total_by_year: Counter[tuple[int, str]] = Counter()
    journal_gwas_by_year: Counter[tuple[int, str]] = Counter()
    y0: int | None = None
    y1: int | None = None
    for sp in shard_paths:
        if not sp.is_file():
            raise FileNotFoundError(f"Missing shard (parse that baseline file first): {sp}")
        res, meta = read_shard_json(sp)
        ym, yx = int(meta["year_min"]), int(meta["year_max"])
        if y0 is None:
            y0, y1 = ym, yx
        elif (ym, yx) != (y0, y1):
            raise ValueError(
                f"Year window mismatch: {sp.name} has {ym}–{yx}, "
                f"expected {y0}–{y1} (use a clean --shards-dir per window)."
            )
        trends.update(res.trends)
        journal_total.update(res.journal_total)
        journal_gwas.update(res.journal_gwas)
        journal_title.update(res.journal_title)
        journal_total_by_year.update(res.journal_total_by_year)
        journal_gwas_by_year.update(res.journal_gwas_by_year)
    window = {"year_min": y0, "year_max": y1} if y0 is not None else {}
    return (
        trends,
        journal_total,
        journal_gwas,
        journal_title,
        journal_total_by_year,
        journal_gwas_by_year,
        window,
    )


def _write_one_shard_job(
    src_str: str,
    year_min: int,
    year_max: int,
    shard_path_str: str,
    skip_existing: bool,
) -> tuple[str, str]:
    """Top-level worker for ProcessPoolExecutor. Returns (status, detail)."""
    src = Path(src_str)
    shard_path = Path(shard_path_str)
    if skip_existing and shard_path.is_file():
        return "skipped", src.name
    result = parse_pubmed_baseline_file(src, year_min, year_max)
    write_shard_json(shard_path, src, year_min, year_max, result)
    return "written", src.name


def parse_pubmed_baseline_file(
    path: Path,
    year_min: int,
    year_max: int,
) -> ShardResult:
    trends: Counter[tuple[int, str]] = Counter()
    journal_total: Counter[str] = Counter()
    journal_gwas: Counter[str] = Counter()
    journal_title: dict[str, str] = {}
    journal_total_by_year: Counter[tuple[int, str]] = Counter()
    journal_gwas_by_year: Counter[tuple[int, str]] = Counter()

    with gzip.open(path, "rb") as f:
        for _event, elem in ET.iterparse(f, events=("end",)):
            if _tag_local(elem.tag) != "PubmedArticle":
                continue
            medline = _find_child(elem, "MedlineCitation")
            if medline is None:
                elem.clear()
                continue
            article = _find_child(medline, "Article")
            if article is None:
                elem.clear()
                continue

            year = _extract_pub_year(medline)
            if year is None or year < year_min or year > year_max:
                elem.clear()
                continue

            mesh_gwas = _mesh_has_gwas(medline)
            blob = _collect_title_abstract_keywords(article)
            text_hits = _text_bucket_hits(blob)

            if mesh_gwas:
                trends[(year, "MeSH_GWAS")] += 1
            for b in text_hits:
                trends[(year, b)] += 1

            jkey, jtitle = _extract_journal_key_title(medline, article)
            journal_title[jkey] = jtitle
            journal_total[jkey] += 1
            journal_total_by_year[(year, jkey)] += 1
            if _is_gwas_related(mesh_gwas, blob):
                journal_gwas[jkey] += 1
                journal_gwas_by_year[(year, jkey)] += 1

            elem.clear()

    return ShardResult(
        trends=trends,
        journal_total=journal_total,
        journal_gwas=journal_gwas,
        journal_title=journal_title,
        journal_total_by_year=journal_total_by_year,
        journal_gwas_by_year=journal_gwas_by_year,
    )


def _discover_baseline_files(root: Path) -> list[Path]:
    files = sorted(root.glob("pubmed*.xml.gz"))
    return [p for p in files if not p.name.endswith(".md5")]


def _write_trends_csv(
    path: Path,
    trends: Counter[tuple[int, str]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = sorted(
        ((y, b, n) for (y, b), n in trends.items()),
        key=lambda r: (r[0], r[1]),
    )
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["year", "bucket", "n_articles"])
        w.writerows(rows)


def _journal_rows(
    journal_total: Counter[str],
    journal_gwas: Counter[str],
    journal_title: dict[str, str],
    min_articles: int,
) -> list[tuple[str, str, int, int, float | None, str]]:
    """Return rows: (key, full_title, gwas_hits, total, fraction or None, meets Y/N)."""
    keys = set(journal_total) | set(journal_gwas)
    rows: list[tuple[str, str, int, int, float | None, str]] = []
    for k in keys:
        tot = journal_total.get(k, 0)
        gh = journal_gwas.get(k, 0)
        frac: float | None = (gh / tot) if tot else None
        meets = "Y" if tot >= min_articles else "N"
        rows.append((k, journal_title.get(k, k), gh, tot, frac, meets))
    return rows


def _sort_volume(rows: list[tuple[str, str, int, int, float | None, str]]) -> list:
    """Most GWAS hits first; tie-break by fraction (desc), then journal key."""

    def sk(r: tuple[str, str, int, int, float | None, str]) -> tuple:
        _k, _t, gh, tot, frac, _m = r
        f = frac if frac is not None else -1.0
        return (-gh, -f, _k)

    return sorted(rows, key=sk)


def _sort_share(
    rows: list[tuple[str, str, int, int, float | None, str]],
    min_articles: int,
) -> list[tuple[str, str, int, int, float | None, str]]:
    """Journals with >= min articles and at least one GWAS-related hit; highest share first."""
    eligible = [
        r
        for r in rows
        if r[3] >= min_articles and r[3] > 0 and r[4] is not None and r[2] > 0
    ]

    def sk(r: tuple[str, str, int, int, float | None, str]) -> tuple:
        _k, _t, gh, tot, frac, _m = r
        assert frac is not None
        return (-frac, -gh, -tot, _k)

    return sorted(eligible, key=sk)


def _write_journal_ranking_volume(
    path: Path,
    rows_sorted: list[tuple[str, str, int, int, float | None, str]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "rank_volume",
                "journal_key",
                "full_title",
                "gwas_hits",
                "total_articles",
                "fraction_gwas",
                "meets_min_total",
            ]
        )
        for i, r in enumerate(rows_sorted, start=1):
            k, title, gh, tot, frac, meets = r
            frac_s = f"{frac:.6f}" if frac is not None else ""
            w.writerow([i, k, title, gh, tot, frac_s, meets])


def _write_journal_ranking_share(
    path: Path,
    rows_share_sorted: list[tuple[str, str, int, int, float | None, str]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "rank_share",
                "journal_key",
                "full_title",
                "gwas_hits",
                "total_articles",
                "fraction_gwas",
            ]
        )
        for i, r in enumerate(rows_share_sorted, start=1):
            k, title, gh, tot, frac, _meets = r
            assert frac is not None
            w.writerow([i, k, title, gh, tot, f"{frac:.6f}"])


def _journal_counters_for_single_year(
    journal_total_by_year: Counter[tuple[int, str]],
    journal_gwas_by_year: Counter[tuple[int, str]],
    year: int,
) -> tuple[Counter[str], Counter[str]]:
    jt = Counter()
    jg = Counter()
    for (y, jk), c in journal_total_by_year.items():
        if y == year:
            jt[jk] = c
    for (y, jk), c in journal_gwas_by_year.items():
        if y == year:
            jg[jk] = c
    return jt, jg


def _years_in_journal_by_year(
    journal_total_by_year: Counter[tuple[int, str]],
    journal_gwas_by_year: Counter[tuple[int, str]],
) -> list[int]:
    ys = {y for (y, _jk) in journal_total_by_year} | {
        y for (y, _jk) in journal_gwas_by_year
    }
    return sorted(ys)


def _write_journal_ranking_volume_by_year(
    path: Path,
    journal_total_by_year: Counter[tuple[int, str]],
    journal_gwas_by_year: Counter[tuple[int, str]],
    journal_title: dict[str, str],
    min_articles: int,
) -> int:
    """One table: year column, rank_volume resets per year. Returns row count."""
    path.parent.mkdir(parents=True, exist_ok=True)
    years = _years_in_journal_by_year(journal_total_by_year, journal_gwas_by_year)
    n_rows = 0
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "year",
                "rank_volume",
                "journal_key",
                "full_title",
                "gwas_hits",
                "total_articles",
                "fraction_gwas",
                "meets_min_total",
            ]
        )
        for year in years:
            jt, jg = _journal_counters_for_single_year(
                journal_total_by_year, journal_gwas_by_year, year
            )
            jrows = _journal_rows(jt, jg, journal_title, min_articles)
            vol_sorted = _sort_volume(jrows)
            for i, r in enumerate(vol_sorted, start=1):
                k, title, gh, tot, frac, meets = r
                frac_s = f"{frac:.6f}" if frac is not None else ""
                w.writerow([year, i, k, title, gh, tot, frac_s, meets])
                n_rows += 1
    return n_rows


def _write_journal_ranking_share_by_year(
    path: Path,
    journal_total_by_year: Counter[tuple[int, str]],
    journal_gwas_by_year: Counter[tuple[int, str]],
    journal_title: dict[str, str],
    min_articles: int,
) -> int:
    """Per calendar year: rank_share among journals with >= min_articles that year."""
    path.parent.mkdir(parents=True, exist_ok=True)
    years = _years_in_journal_by_year(journal_total_by_year, journal_gwas_by_year)
    n_rows = 0
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "year",
                "rank_share",
                "journal_key",
                "full_title",
                "gwas_hits",
                "total_articles",
                "fraction_gwas",
            ]
        )
        for year in years:
            jt, jg = _journal_counters_for_single_year(
                journal_total_by_year, journal_gwas_by_year, year
            )
            jrows = _journal_rows(jt, jg, journal_title, min_articles)
            share_sorted = _sort_share(jrows, min_articles)
            for i, r in enumerate(share_sorted, start=1):
                k, title, gh, tot, frac, _m = r
                assert frac is not None
                w.writerow([year, i, k, title, gh, tot, f"{frac:.6f}"])
                n_rows += 1
    return n_rows


def _parse_args(argv: list[str]) -> argparse.Namespace:
    today = date.today()
    y_default_max = today.year
    # Inclusive 20-year window ending in the current calendar year.
    y_default_min = today.year - 19
    p = argparse.ArgumentParser(
        description="GWAS-related trends and journal stats from PubMed baseline XML.gz"
    )
    p.add_argument(
        "--baseline-dir",
        type=Path,
        default=None,
        help="Directory with pubmed*.xml.gz (default: scan this tree; required if --xml-gz omitted)",
    )
    p.add_argument(
        "--xml-gz",
        type=Path,
        nargs="*",
        default=[],
        metavar="FILE",
        help="Explicit shard path(s); if set, only these files are processed (still must be .xml.gz)",
    )
    p.add_argument(
        "--out-dir",
        type=Path,
        default=Path("pubmed_gwas_out"),
        help="Output directory for CSV reports and default shards dir parent",
    )
    p.add_argument(
        "--shards-dir",
        type=Path,
        default=None,
        help="Per-baseline JSON shards (*.shard.json); default <out-dir>/shards",
    )
    p.add_argument(
        "--shard-only",
        action="store_true",
        help="Only write shard JSON for each baseline file; skip final CSV merge",
    )
    p.add_argument(
        "--summarize-only",
        action="store_true",
        help="Only merge all *.shard.json under --shards-dir into final CSVs (no XML I/O)",
    )
    p.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip parsing when the target .shard.json already exists (resume)",
    )
    p.add_argument(
        "--year-min",
        type=int,
        default=y_default_min,
        help=f"First publication year (inclusive); default {y_default_min}",
    )
    p.add_argument(
        "--year-max",
        type=int,
        default=y_default_max,
        help=f"Last publication year (inclusive); default {y_default_max}",
    )
    p.add_argument(
        "--workers",
        type=int,
        default=0,
        help="Parallel worker processes (0 = min(CPU, files))",
    )
    p.add_argument(
        "--limit-files",
        type=int,
        default=0,
        help="Process at most N files (0 = all); for smoke tests",
    )
    p.add_argument(
        "--min-articles",
        type=int,
        default=50,
        help="Mark meets_min_total in journal CSV when total_articles >= this",
    )
    return p.parse_args(argv)


def _write_final_outputs(
    out_dir: Path,
    trends: Counter[tuple[int, str]],
    journal_total: Counter[str],
    journal_gwas: Counter[str],
    journal_title: dict[str, str],
    journal_total_by_year: Counter[tuple[int, str]],
    journal_gwas_by_year: Counter[tuple[int, str]],
    min_articles: int,
) -> tuple[int, int, int, int]:
    out_dir.mkdir(parents=True, exist_ok=True)
    _write_trends_csv(out_dir / "gwas_trends_by_year.csv", trends)
    jrows = _journal_rows(
        journal_total, journal_gwas, journal_title, min_articles
    )
    vol_sorted = _sort_volume(jrows)
    share_sorted = _sort_share(jrows, min_articles)
    _write_journal_ranking_volume(out_dir / "journal_gwas_ranking.csv", vol_sorted)
    _write_journal_ranking_share(
        out_dir / "journal_gwas_ranking_by_share.csv", share_sorted
    )
    n_vol_y = _write_journal_ranking_volume_by_year(
        out_dir / "journal_gwas_ranking_by_year.csv",
        journal_total_by_year,
        journal_gwas_by_year,
        journal_title,
        min_articles,
    )
    n_sh_y = _write_journal_ranking_share_by_year(
        out_dir / "journal_gwas_ranking_by_share_by_year.csv",
        journal_total_by_year,
        journal_gwas_by_year,
        journal_title,
        min_articles,
    )
    return len(jrows), len(share_sorted), n_vol_y, n_sh_y


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv or sys.argv[1:])
    if args.shard_only and args.summarize_only:
        print("Use only one of --shard-only and --summarize-only.", file=sys.stderr)
        return 1

    out_dir = args.out_dir.expanduser().resolve()
    year_min, year_max = args.year_min, args.year_max
    if year_min > year_max:
        print("--year-min must be <= --year-max", file=sys.stderr)
        return 1

    if args.summarize_only:
        if args.shards_dir is None:
            print("--summarize-only requires --shards-dir", file=sys.stderr)
            return 1
        shards_dir = args.shards_dir.expanduser().resolve()
        if not shards_dir.is_dir():
            print(f"Not a directory: {shards_dir}", file=sys.stderr)
            return 1
        shard_paths = discover_shard_files(shards_dir)
        if not shard_paths:
            print(f"No *{SHARD_SUFFIX} files under {shards_dir}", file=sys.stderr)
            return 1
        t0 = time.perf_counter()
        try:
            (
                trends,
                journal_total,
                journal_gwas,
                journal_title,
                journal_total_by_year,
                journal_gwas_by_year,
                window,
            ) = load_and_merge_shards(shard_paths)
        except (ValueError, FileNotFoundError) as e:
            print(e, file=sys.stderr)
            return 1
        elapsed = time.perf_counter() - t0
        n_j, n_js, n_jy, n_jsy = _write_final_outputs(
            out_dir,
            trends,
            journal_total,
            journal_gwas,
            journal_title,
            journal_total_by_year,
            journal_gwas_by_year,
            args.min_articles,
        )
        meta = {
            "mode": "summarize_only",
            "elapsed_seconds": round(elapsed, 2),
            "shards_dir": str(shards_dir),
            "n_shard_files": len(shard_paths),
            "year_min": window.get("year_min", year_min),
            "year_max": window.get("year_max", year_max),
            "min_articles_for_share_rank": args.min_articles,
            "n_journals_any": n_j,
            "n_journals_share_ranked": n_js,
            "n_journal_rows_by_year_volume": n_jy,
            "n_journal_rows_by_year_share": n_jsy,
            "outputs": [
                "gwas_trends_by_year.csv",
                "journal_gwas_ranking.csv",
                "journal_gwas_ranking_by_share.csv",
                "journal_gwas_ranking_by_year.csv",
                "journal_gwas_ranking_by_share_by_year.csv",
            ],
        }
        (out_dir / "run_meta.json").write_text(
            json.dumps(meta, indent=2) + "\n", encoding="utf-8"
        )
        print(f"Merged {len(shard_paths)} shards in {elapsed:.1f}s", file=sys.stderr)
        print(f"Wrote {out_dir / 'gwas_trends_by_year.csv'}", file=sys.stderr)
        print(f"Wrote {out_dir / 'journal_gwas_ranking.csv'}", file=sys.stderr)
        print(f"Wrote {out_dir / 'journal_gwas_ranking_by_share.csv'}", file=sys.stderr)
        print(f"Wrote {out_dir / 'journal_gwas_ranking_by_year.csv'}", file=sys.stderr)
        print(f"Wrote {out_dir / 'journal_gwas_ranking_by_share_by_year.csv'}", file=sys.stderr)
        print(f"Wrote {out_dir / 'run_meta.json'}", file=sys.stderr)
        return 0

    if not args.xml_gz and args.baseline_dir is None:
        print("Either --baseline-dir or one or more --xml-gz paths is required.", file=sys.stderr)
        return 1

    if args.xml_gz:
        files = [p.expanduser().resolve() for p in args.xml_gz]
        for p in files:
            if not p.is_file():
                print(f"Not a file: {p}", file=sys.stderr)
                return 1
    else:
        root = args.baseline_dir.expanduser().resolve()
        if not root.is_dir():
            print(f"Not a directory: {root}", file=sys.stderr)
            return 1
        files = _discover_baseline_files(root)
        if args.limit_files > 0:
            files = files[: args.limit_files]
    if not files:
        print("No input baseline files to process.", file=sys.stderr)
        return 1

    shards_dir = (
        args.shards_dir.expanduser().resolve()
        if args.shards_dir is not None
        else out_dir / "shards"
    )

    n_workers = args.workers
    if n_workers <= 0:
        n_workers = min(cpu_count() or 1, len(files))
    n_workers = max(1, min(n_workers, len(files)))

    print(
        f"Files: {len(files)}  workers: {n_workers}  years: {year_min}–{year_max}  "
        f"shards: {shards_dir}",
        file=sys.stderr,
    )

    t0 = time.perf_counter()
    shard_paths = [_shard_path_for_source(shards_dir, fp) for fp in files]
    written = skipped = 0

    if n_workers == 1:
        for fp, sp in zip(files, shard_paths, strict=True):
            if args.skip_existing and sp.is_file():
                skipped += 1
                continue
            result = parse_pubmed_baseline_file(fp, year_min, year_max)
            write_shard_json(sp, fp, year_min, year_max, result)
            written += 1
    else:
        jobs = [
            (
                str(fp.resolve()),
                year_min,
                year_max,
                str(sp.resolve()),
                args.skip_existing,
            )
            for fp, sp in zip(files, shard_paths, strict=True)
        ]
        with ProcessPoolExecutor(max_workers=n_workers) as ex:
            futs = {ex.submit(_write_one_shard_job, *job): job[0] for job in jobs}
            for fut in as_completed(futs):
                try:
                    status, name = fut.result()
                    if status == "skipped":
                        skipped += 1
                    else:
                        written += 1
                except Exception as e:
                    print(f"Failed {futs[fut]}: {e}", file=sys.stderr)
                    raise

    parse_elapsed = time.perf_counter() - t0
    print(
        f"Shards: {written} written, {skipped} skipped (existing), dir={shards_dir}",
        file=sys.stderr,
    )

    if args.shard_only:
        meta = {
            "mode": "shard_only",
            "elapsed_seconds": round(parse_elapsed, 2),
            "n_baseline_files": len(files),
            "written": written,
            "skipped_existing": skipped,
            "workers": n_workers,
            "year_min": year_min,
            "year_max": year_max,
            "shards_dir": str(shards_dir),
        }
        if args.xml_gz:
            meta["input_mode"] = "explicit_xml_gz"
        else:
            meta["input_mode"] = "baseline_dir"
            meta["baseline_dir"] = str(args.baseline_dir.expanduser().resolve())
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "run_meta.json").write_text(
            json.dumps(meta, indent=2) + "\n", encoding="utf-8"
        )
        print(f"Wrote {out_dir / 'run_meta.json'} (shard-only)", file=sys.stderr)
        return 0

    merge_t0 = time.perf_counter()
    try:
        (
            trends,
            journal_total,
            journal_gwas,
            journal_title,
            journal_total_by_year,
            journal_gwas_by_year,
            _window,
        ) = load_and_merge_shards(shard_paths)
    except (ValueError, FileNotFoundError) as e:
        print(e, file=sys.stderr)
        return 1
    merge_elapsed = time.perf_counter() - merge_t0
    total_elapsed = time.perf_counter() - t0

    n_j, n_js, n_jy, n_jsy = _write_final_outputs(
        out_dir,
        trends,
        journal_total,
        journal_gwas,
        journal_title,
        journal_total_by_year,
        journal_gwas_by_year,
        args.min_articles,
    )

    meta = {
        "mode": "parse_and_summarize",
        "elapsed_seconds": round(total_elapsed, 2),
        "parse_elapsed_seconds": round(parse_elapsed, 2),
        "merge_elapsed_seconds": round(merge_elapsed, 2),
        "n_baseline_files": len(files),
        "written": written,
        "skipped_existing": skipped,
        "workers": n_workers,
        "year_min": year_min,
        "year_max": year_max,
        "min_articles_for_share_rank": args.min_articles,
        "n_journals_any": n_j,
        "n_journals_share_ranked": n_js,
        "n_journal_rows_by_year_volume": n_jy,
        "n_journal_rows_by_year_share": n_jsy,
        "shards_dir": str(shards_dir),
        "outputs": [
            "gwas_trends_by_year.csv",
            "journal_gwas_ranking.csv",
            "journal_gwas_ranking_by_share.csv",
            "journal_gwas_ranking_by_year.csv",
            "journal_gwas_ranking_by_share_by_year.csv",
        ],
    }
    if args.xml_gz:
        meta["input_mode"] = "explicit_xml_gz"
        meta["n_explicit_files"] = len(args.xml_gz)
    else:
        meta["input_mode"] = "baseline_dir"
        meta["baseline_dir"] = str(args.baseline_dir.expanduser().resolve())

    (out_dir / "run_meta.json").write_text(
        json.dumps(meta, indent=2) + "\n", encoding="utf-8"
    )

    print(f"Wrote {out_dir / 'gwas_trends_by_year.csv'}", file=sys.stderr)
    print(f"Wrote {out_dir / 'journal_gwas_ranking.csv'}", file=sys.stderr)
    print(f"Wrote {out_dir / 'journal_gwas_ranking_by_share.csv'}", file=sys.stderr)
    print(f"Wrote {out_dir / 'journal_gwas_ranking_by_year.csv'}", file=sys.stderr)
    print(f"Wrote {out_dir / 'journal_gwas_ranking_by_share_by_year.csv'}", file=sys.stderr)
    print(f"Wrote {out_dir / 'run_meta.json'}", file=sys.stderr)
    print(f"Done in {total_elapsed:.1f}s (merge {merge_elapsed:.2f}s)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
