"""
Fetch PubMed records via NCBI Entrez (efetch), cache raw XML on disk, and parse
into rows compatible with catalog JSON / ``load_data`` bibliography columns.

Contact email for E-utilities is taken from ``NCBI_EMAIL`` if set, otherwise
``DEFAULT_NCBI_EMAIL`` (project maintainer). Override per machine with env if
you prefer not to use the default.

Optional ``NCBI_API_KEY`` (create at https://www.ncbi.nlm.nih.gov/account/settings/)
raises the allowed request rate; see limits below.

**NCBI E-utilities limits** (https://www.ncbi.nlm.nih.gov/books/NBK25497/):

- Without an API key: at most **3 requests per second** (global to your IP).
- With an API key on the request: up to **10 requests per second**.
- This repo enforces spacing via ``NCBI_MAX_RPS_*`` and ``ENTREZ_RATE_HEADROOM``
  (see constants below): one efetch batch, then sleep before the next.
- Heavy or abusive use can lead to throttling or blocking; NCBI may contact you
  at the supplied email before blocking.

Example:

    python pubmed_entrez.py --pmid-file ../not_in_lib.pmidlist
    NCBI_EMAIL=other@example.com python pubmed_entrez.py 33070389
"""

from __future__ import annotations

import http.client
import json
import os
import re
import time
from datetime import date, timedelta
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
DEFAULT_TOOL = "CTGCatalog"
# Identifying contact for NCBI E-utilities (overridable via NCBI_EMAIL).
DEFAULT_NCBI_EMAIL = "yunyehe.ctg@gmail.com"
DEFAULT_BATCH = 80

# --- Rate limits for this repo (NCBI E-utilities, NBK25497) ---
# Official maximum sustained HTTP request rates for Entrez:
NCBI_MAX_RPS_WITHOUT_API_KEY = 3
NCBI_MAX_RPS_WITH_API_KEY = 10
# Multiply the ideal spacing (1 / max_rps) by this to stay under the cap in
# practice (network jitter, clock skew). >1.0 means slower / more conservative.
ENTREZ_RATE_HEADROOM = 1.2


def _entrez_batch_interval_seconds(has_api_key: bool) -> float:
    cap = (
        NCBI_MAX_RPS_WITH_API_KEY if has_api_key else NCBI_MAX_RPS_WITHOUT_API_KEY
    )
    return ENTREZ_RATE_HEADROOM / cap


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


def _text(el: ET.Element | None) -> str:
    if el is None or el.text is None:
        return ""
    return el.text.strip()


def _collect_abstract_text(abstract_el: ET.Element | None) -> tuple[str, str]:
    """Return (joined abstract body, copyright line if any)."""
    if abstract_el is None:
        return "", ""
    parts: list[str] = []
    copyright_line = ""
    for child in abstract_el:
        t = _tag_local(child.tag)
        if t == "CopyrightInformation":
            copyright_line = (child.text or "").strip()
            continue
        if t == "AbstractText":
            label = child.attrib.get("Label", "")
            chunk = "".join(child.itertext()).strip()
            if label:
                parts.append(f"{label}: {chunk}" if chunk else label)
            elif chunk:
                parts.append(chunk)
    body = " ".join(parts).strip()
    return body, copyright_line


def _format_author(author_el: ET.Element) -> str | None:
    collective = _find_child(author_el, "CollectiveName")
    if collective is not None:
        s = _text(collective)
        return s if s else None
    last = _text(_find_child(author_el, "LastName"))
    initials = _text(_find_child(author_el, "Initials"))
    fore = _text(_find_child(author_el, "ForeName"))
    if not last:
        return None
    if initials:
        return f"{last} {initials}".strip()
    if fore:
        ini = fore[0] if fore else ""
        return f"{last} {ini}".strip() if ini else last
    return last


def _collect_authors(article_el: ET.Element) -> str:
    al = _find_child(article_el, "AuthorList")
    if al is None:
        return ""
    names: list[str] = []
    for a in _findall_children(al, "Author"):
        if a.attrib.get("ValidYN", "Y").upper() == "N":
            continue
        fmt = _format_author(a)
        if fmt:
            names.append(fmt)
    return ",".join(names)


def _journal_fields(article_el: ET.Element) -> dict[str, str]:
    out = {
        "Journal": "",
        "Full journal": "",
        "Volume": "",
        "Issue": "",
        "Pages": "",
        "Publication year": "",
    }
    journal = _find_child(article_el, "Journal")
    if journal is None:
        return out
    out["Full journal"] = _text(_find_child(journal, "Title"))
    out["Journal"] = _text(_find_child(journal, "ISOAbbreviation")) or out[
        "Full journal"
    ]
    ji = _find_child(journal, "JournalIssue")
    if ji is not None:
        out["Volume"] = _text(_find_child(ji, "Volume"))
        out["Issue"] = _text(_find_child(ji, "Issue"))
        pd = _find_child(ji, "PubDate")
        if pd is not None:
            y = _text(_find_child(pd, "Year"))
            md = _text(_find_child(pd, "MedlineDate"))
            out["Publication year"] = y or (md.split(" ", 1)[0] if md else "")
    art = _find_child(article_el, "Pagination")
    if art is not None:
        pgn = _text(_find_child(art, "MedlinePgn"))
        if pgn:
            out["Pages"] = pgn
        else:
            sp = _text(_find_child(art, "StartPage"))
            ep = _text(_find_child(art, "EndPage"))
            if sp and ep:
                out["Pages"] = f"{sp}-{ep}"
            elif sp:
                out["Pages"] = sp
    # Electronic-only articles sometimes use ArticleDate
    if not out["Publication year"]:
        for ad in _findall_children(article_el, "ArticleDate"):
            if ad.attrib.get("DateType") == "Electronic":
                y = _text(_find_child(ad, "Year"))
                if y:
                    out["Publication year"] = y
                    break
    return out


def _article_ids(pubmed_article: ET.Element) -> dict[str, str]:
    ids: dict[str, str] = {}
    pd = _find_child(pubmed_article, "PubmedData")
    if pd is None:
        return ids
    id_list = _find_child(pd, "ArticleIdList")
    if id_list is None:
        return ids
    for node in id_list:
        if _tag_local(node.tag) != "ArticleId":
            continue
        id_type = node.attrib.get("IdType", "pubmed").lower()
        val = (node.text or "").strip()
        if not val:
            continue
        ids[id_type] = val
    return ids


def parse_pubmed_article_element(pubmed_article: ET.Element) -> dict[str, str]:
    """
    Map one <PubmedArticle> element to flat string fields (input for ``catalog_biblio_from_pubmed_parsed``).
    """
    mc = _find_child(pubmed_article, "MedlineCitation")
    if mc is None:
        raise ValueError("PubmedArticle missing MedlineCitation")
    pmid_el = _find_child(mc, "PMID")
    pmid = _text(pmid_el)
    if not pmid:
        raise ValueError("Missing PMID in MedlineCitation")
    article = _find_child(mc, "Article")
    if article is None:
        raise ValueError(f"No Article for PMID {pmid}")

    title = _text(_find_child(article, "ArticleTitle"))
    title = re.sub(r"\s+", " ", title)

    jf = _journal_fields(article)
    abstract, copyright_line = _collect_abstract_text(_find_child(article, "Abstract"))
    authors = _collect_authors(article)
    aid = _article_ids(pubmed_article)
    doi = aid.get("doi", "")
    pmc = aid.get("pmc", "")

    row: dict[str, str] = {
        "Item type": "Journal Article",
        "Authors": authors,
        "Editors": "",
        "Title": title,
        "Journal": jf["Journal"],
        "Full journal": jf["Full journal"],
        "Publication year": jf["Publication year"],
        "Volume": jf["Volume"],
        "Issue": jf["Issue"],
        "Pages": jf["Pages"],
        "DOI": doi,
        "PMID": pmid,
        "Abstract": abstract,
        "Copyright": copyright_line,
        "PMC ID": pmc,
    }
    return row


def catalog_biblio_from_pubmed_parsed(p: dict[str, str]) -> dict[str, str]:
    """
    Map ``parse_pubmed_article_element`` / ``parse_cached_pmid`` output to catalog
    JSON keys and ``format_citation.cite`` column names (used by sync, not load_data).
    """
    from format_citation import cite

    pmid = (p.get("PMID") or "").strip()
    doi_raw = (p.get("DOI") or "").strip()
    authors = (p.get("Authors") or "").strip()
    cite_row = {
        "PMID": pmid,
        "Authors": authors,
        "TITLE": (p.get("Title") or "").strip(),
        "ISO": (p.get("Journal") or "").strip(),
        "PAGE": (p.get("Pages") or "").strip(),
        "DOI": doi_raw if doi_raw else None,
        "YEAR": (p.get("Publication year") or "").strip(),
        "VOLUME": (p.get("Volume") or "").strip(),
        "ISSUE": (p.get("Issue") or "").strip(),
    }
    citation = cite(cite_row)
    first = authors.split(",")[0].strip() if authors else ""
    return {
        "TITLE": cite_row["TITLE"],
        "ISO": cite_row["ISO"],
        "JOURNAL": (p.get("Full journal") or "").strip(),
        "YEAR": cite_row["YEAR"],
        "VOLUME": cite_row["VOLUME"],
        "ISSUE": cite_row["ISSUE"],
        "PAGE": cite_row["PAGE"],
        "Authors": authors,
        "ABSTRACT": (p.get("Abstract") or "").strip(),
        "DOI": doi_raw,
        "PMC ID": (p.get("PMC ID") or "").strip(),
        "CITATION": citation,
        "FIRST_AUTHOR": first,
    }


def parse_pubmed_efetch_xml(xml_bytes: bytes) -> list[dict[str, str]]:
    """Parse efetch XML (one or many articles). Skips malformed entries."""
    root = ET.fromstring(xml_bytes)
    rows: list[dict[str, str]] = []
    for child in root:
        if _tag_local(child.tag) != "PubmedArticle":
            continue
        try:
            rows.append(parse_pubmed_article_element(child))
        except ValueError:
            continue
    return rows


def pubmed_cache_dir(repo_root: Path | None = None) -> Path:
    base = repo_root or Path(__file__).resolve().parent.parent
    d = base / ".cache" / "pubmed"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _entrez_email() -> str:
    return (os.environ.get("NCBI_EMAIL") or DEFAULT_NCBI_EMAIL).strip()


def _entrez_api_key() -> str | None:
    k = (os.environ.get("NCBI_API_KEY") or "").strip()
    return k or None


def _parse_esearch_result_xml(xml_bytes: bytes) -> tuple[int, int, int, list[str]]:
    """
    Parse esearch XML. Returns (total_count, retstart, retmax, id_list).
    """
    root = ET.fromstring(xml_bytes)

    def find_text(name: str) -> str:
        for el in root.iter():
            if _tag_local(el.tag) == name and el.text:
                return el.text.strip()
        return ""

    count = int(find_text("Count") or "0")
    retstart = int(find_text("RetStart") or "0")
    retmax = int(find_text("RetMax") or "0")
    ids: list[str] = []
    id_list_el = None
    for el in root.iter():
        if _tag_local(el.tag) == "IdList":
            id_list_el = el
            break
    if id_list_el is not None:
        for el in id_list_el:
            if _tag_local(el.tag) == "Id" and el.text:
                ids.append(el.text.strip())
    return count, retstart, retmax, ids


def entrez_esearch_pubmed(
    term: str,
    *,
    retmax: int = 10000,
    retstart: int = 0,
    mindate: str | None = None,
    maxdate: str | None = None,
    datetype: str = "pdat",
    email: str | None = None,
    api_key: str | None = None,
    tool: str = DEFAULT_TOOL,
    timeout: int = 60,
) -> tuple[int, list[str]]:
    """
    GET esearch.fcgi for db=pubmed. Returns (total_count_matching_term, ids_this_page).

    When mindate/maxdate are set (YYYY/MM/DD), they restrict by datetype (default pdat).
    """
    em = (email or _entrez_email()).strip()
    if not em:
        raise RuntimeError(
            "Set NCBI_EMAIL or DEFAULT_NCBI_EMAIL in pubmed_entrez.py for Entrez "
            "(see https://www.ncbi.nlm.nih.gov/books/NBK25497/)."
        )
    key = api_key if api_key is not None else _entrez_api_key()
    params: dict[str, str] = {
        "db": "pubmed",
        "term": term,
        "retmode": "xml",
        "retmax": str(min(retmax, 10_000)),
        "retstart": str(retstart),
        "email": em,
        "tool": tool,
    }
    if mindate:
        params["mindate"] = mindate
    if maxdate:
        params["maxdate"] = maxdate
    if mindate or maxdate:
        params["datetype"] = datetype
    if key:
        params["api_key"] = key
    q = urllib.parse.urlencode(params)
    url = f"{EUTILS}/esearch.fcgi?{q}"
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            xml_bytes = resp.read()
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Entrez esearch HTTP {e.code}: {body[:500]}") from e
    total, _rs, _rm, ids = _parse_esearch_result_xml(xml_bytes)
    return total, ids


def _parse_nlm_date(s: str) -> date:
    y, m, d = (int(x) for x in s.strip().split("/"))
    return date(y, m, d)


def _fmt_nlm_date(d: date) -> str:
    return f"{d.year}/{d.month:02d}/{d.day:02d}"


def _merge_pmid_lists_unique(left: list[str], right: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for pid in left + right:
        if pid not in seen:
            seen.add(pid)
            out.append(pid)
    return out


def _esearch_pubmed_ids_one_slice(
    term: str,
    *,
    mindate: str,
    maxdate: str,
    datetype: str,
    expected_total: int,
    email: str | None,
    api_key: str | None,
    tool: str,
    timeout: int,
    sleep_between_pages: bool,
    interval: float,
) -> list[str]:
    """Collect all PMIDs when Count for this slice is <= 9999 (PubMed esearch cap)."""
    seen: set[str] = set()
    out: list[str] = []
    retstart = 0
    while len(out) < expected_total:
        _, chunk = entrez_esearch_pubmed(
            term,
            retmax=10_000,
            retstart=retstart,
            mindate=mindate,
            maxdate=maxdate,
            datetype=datetype,
            email=email,
            api_key=api_key,
            tool=tool,
            timeout=timeout,
        )
        if not chunk:
            break
        for pid in chunk:
            if pid not in seen:
                seen.add(pid)
                out.append(pid)
        retstart += len(chunk)
        if len(out) >= expected_total:
            break
        if len(chunk) < 10_000:
            break
        if sleep_between_pages and len(out) < expected_total:
            time.sleep(interval)
    return out


def _esearch_pubmed_date_split_pmids(
    term: str,
    *,
    mindate: str,
    maxdate: str,
    datetype: str,
    email: str | None,
    api_key: str | None,
    tool: str,
    timeout: int,
    sleep_between_pages: bool,
) -> list[str]:
    """
    Recursively split publication-date range so each esearch slice has Count <= 9999
    (PubMed cannot return retstart beyond 9998).
    """
    key = api_key if api_key is not None else _entrez_api_key()
    interval = _entrez_batch_interval_seconds(has_api_key=bool(key))

    def recurse(d0: date, d1: date) -> list[str]:
        if d0 > d1:
            return []
        ms, me = _fmt_nlm_date(d0), _fmt_nlm_date(d1)
        tot, _ = entrez_esearch_pubmed(
            term,
            retmax=0,
            retstart=0,
            mindate=ms,
            maxdate=me,
            datetype=datetype,
            email=email,
            api_key=api_key,
            tool=tool,
            timeout=timeout,
        )
        if sleep_between_pages:
            time.sleep(interval)
        if tot == 0:
            return []
        if tot <= 9999:
            return _esearch_pubmed_ids_one_slice(
                term,
                mindate=ms,
                maxdate=me,
                datetype=datetype,
                expected_total=tot,
                email=email,
                api_key=api_key,
                tool=tool,
                timeout=timeout,
                sleep_between_pages=sleep_between_pages,
                interval=interval,
            )
        if d0 == d1:
            raise RuntimeError(
                f"PubMed esearch slice {ms} has Count={tot} (>9999). "
                "Narrow the query or split by additional criteria."
            )
        mid = d0 + (d1 - d0) // 2
        left = recurse(d0, mid)
        right = recurse(mid + timedelta(days=1), d1)
        return _merge_pmid_lists_unique(left, right)

    if not mindate or not maxdate:
        raise ValueError("Date splitting requires mindate and maxdate")
    return recurse(_parse_nlm_date(mindate), _parse_nlm_date(maxdate))


def entrez_esearch_pubmed_all_pmids(
    term: str,
    *,
    mindate: str | None = None,
    maxdate: str | None = None,
    datetype: str = "pdat",
    email: str | None = None,
    api_key: str | None = None,
    tool: str = DEFAULT_TOOL,
    timeout: int = 90,
    page_size: int = 10_000,
    sleep_between_pages: bool = True,
) -> tuple[int, list[str]]:
    """
    Collect all PMIDs for the query. PubMed caps a single esearch at 9,999 records;
    when mindate/maxdate are set and Count exceeds that, this function **splits the
    date range recursively** so every slice stays under the cap.
    """
    key = api_key if api_key is not None else _entrez_api_key()
    interval = _entrez_batch_interval_seconds(has_api_key=bool(key))

    if mindate and maxdate:
        total, _ = entrez_esearch_pubmed(
            term,
            retmax=0,
            retstart=0,
            mindate=mindate,
            maxdate=maxdate,
            datetype=datetype,
            email=email,
            api_key=api_key,
            tool=tool,
            timeout=timeout,
        )
        if sleep_between_pages:
            time.sleep(interval)
        if total <= 9999:
            ids = _esearch_pubmed_ids_one_slice(
                term,
                mindate=mindate,
                maxdate=maxdate,
                datetype=datetype,
                expected_total=total,
                email=email,
                api_key=api_key,
                tool=tool,
                timeout=timeout,
                sleep_between_pages=sleep_between_pages,
                interval=interval,
            )
            return max(total, 0), ids
        ids = _esearch_pubmed_date_split_pmids(
            term,
            mindate=mindate,
            maxdate=maxdate,
            datetype=datetype,
            email=email,
            api_key=api_key,
            tool=tool,
            timeout=timeout,
            sleep_between_pages=sleep_between_pages,
        )
        return max(total, 0), ids

    # No date filter: cannot split; best-effort first 9999 only (PubMed limit).
    all_ids: list[str] = []
    seen: set[str] = set()
    retstart = 0
    total = -1
    while True:
        reported, chunk = entrez_esearch_pubmed(
            term,
            retmax=page_size,
            retstart=retstart,
            mindate=mindate,
            maxdate=maxdate,
            datetype=datetype,
            email=email,
            api_key=api_key,
            tool=tool,
            timeout=timeout,
        )
        if total < 0:
            total = reported
        for pid in chunk:
            if pid not in seen:
                seen.add(pid)
                all_ids.append(pid)
        if not chunk:
            break
        retstart += page_size
        if total >= 0 and (len(all_ids) >= total or retstart >= total):
            break
        if sleep_between_pages:
            time.sleep(interval)
    return max(total, 0), all_ids


def entrez_efetch_pubmed_xml(
    pmids: list[str],
    *,
    email: str | None = None,
    api_key: str | None = None,
    tool: str = DEFAULT_TOOL,
    timeout: int = 60,
    max_retries: int = 4,
    retry_base_sleep: float = 3.0,
) -> bytes:
    """POST efetch.fcgi for db=pubmed, retmode=xml. Retries on transient network errors."""
    em = (email or _entrez_email()).strip()
    if not em:
        raise RuntimeError(
            "Set NCBI_EMAIL or DEFAULT_NCBI_EMAIL in pubmed_entrez.py for Entrez "
            "(see https://www.ncbi.nlm.nih.gov/books/NBK25497/)."
        )
    key = api_key if api_key is not None else _entrez_api_key()
    ids = [re.sub(r"\D", "", p) for p in pmids if p and str(p).strip()]
    if not ids:
        raise ValueError("No valid PMIDs")
    params: dict[str, str] = {
        "db": "pubmed",
        "id": ",".join(ids),
        "retmode": "xml",
        "email": em,
        "tool": tool,
    }
    if key:
        params["api_key"] = key
    data = urllib.parse.urlencode(params).encode("ascii")
    url = f"{EUTILS}/efetch.fcgi"
    req = urllib.request.Request(url, data=data, method="POST")
    last_err: BaseException | None = None
    for attempt in range(max(1, max_retries)):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            last_err = e
            body = e.read().decode("utf-8", errors="replace")
            retriable = e.code in (429, 500, 502, 503, 504)
            if retriable and attempt + 1 < max_retries:
                time.sleep(retry_base_sleep * (2**attempt))
                continue
            raise RuntimeError(f"Entrez HTTP {e.code}: {body[:500]}") from e
        except http.client.IncompleteRead as e:
            last_err = e
            if attempt + 1 < max_retries:
                time.sleep(retry_base_sleep * (2**attempt))
                continue
            raise
        except urllib.error.URLError as e:
            last_err = e
            if attempt + 1 < max_retries:
                time.sleep(retry_base_sleep * (2**attempt))
                continue
            raise
    raise RuntimeError(f"Entrez efetch failed after {max_retries} attempts") from last_err


def _write_xml_cache(path: Path, xml_bytes: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(xml_bytes)


def _read_xml_cache(path: Path) -> bytes | None:
    if path.is_file():
        return path.read_bytes()
    return None


def fetch_pubmed_xml_cached(
    pmid: str,
    *,
    cache_dir: Path,
    email: str | None = None,
    api_key: str | None = None,
    force: bool = False,
    timeout: int = 60,
) -> bytes:
    """Return raw XML for one PMID, using cache_dir / '{pmid}.xml'."""
    clean = re.sub(r"\D", "", str(pmid))
    if not clean:
        raise ValueError(f"Invalid PMID: {pmid!r}")
    path = cache_dir / f"{clean}.xml"
    if not force:
        hit = _read_xml_cache(path)
        if hit is not None:
            return hit
    xml_bytes = entrez_efetch_pubmed_xml(
        [clean], email=email, api_key=api_key, timeout=timeout
    )
    _write_xml_cache(path, xml_bytes)
    return xml_bytes


def fetch_pubmed_batch_cached(
    pmids: list[str],
    *,
    cache_dir: Path,
    email: str | None = None,
    api_key: str | None = None,
    force: bool = False,
    batch_size: int = DEFAULT_BATCH,
    timeout: int = 90,
    efetch_max_retries: int = 4,
) -> dict[str, bytes]:
    """
    Fetch multiple PMIDs; uses per-PMID cache files. Returns map pmid -> xml bytes
    (from cache or fresh). Missing PMIDs on NCBI side simply omit articles in XML;
    callers should compare requested vs parsed PMIDs.
    """
    key = api_key if api_key is not None else _entrez_api_key()
    interval = _entrez_batch_interval_seconds(has_api_key=bool(key))
    clean_list = []
    seen: set[str] = set()
    for p in pmids:
        c = re.sub(r"\D", "", str(p))
        if c and c not in seen:
            seen.add(c)
            clean_list.append(c)
    out: dict[str, bytes] = {}
    to_request: list[str] = []
    for c in clean_list:
        pth = cache_dir / f"{c}.xml"
        if not force:
            hit = _read_xml_cache(pth)
            if hit is not None:
                out[c] = hit
                continue
        to_request.append(c)

    for i in range(0, len(to_request), batch_size):
        chunk = to_request[i : i + batch_size]
        xml_bytes = entrez_efetch_pubmed_xml(
            chunk,
            email=email,
            api_key=api_key,
            timeout=timeout,
            max_retries=efetch_max_retries,
        )
        found_pmids: set[str] = set()
        root = ET.fromstring(xml_bytes)
        for child in root:
            if _tag_local(child.tag) != "PubmedArticle":
                continue
            try:
                row = parse_pubmed_article_element(child)
                pid = row["PMID"]
            except (ValueError, KeyError):
                continue
            found_pmids.add(pid)
            one_xml = ET.tostring(child, encoding="utf-8", xml_declaration=False)
            wrapped = (
                b'<?xml version="1.0" encoding="UTF-8"?>\n<PubmedArticleSet>\n'
                + one_xml
                + b"\n</PubmedArticleSet>\n"
            )
            pth = cache_dir / f"{pid}.xml"
            _write_xml_cache(pth, wrapped)
            out[pid] = wrapped
        # NCBI omitted IDs: avoid infinite re-fetch — store empty marker
        empty_set = b'<?xml version="1.0" encoding="UTF-8"?><PubmedArticleSet></PubmedArticleSet>'
        for c in chunk:
            if c not in found_pmids and c not in out:
                stub = cache_dir / f"{c}.xml"
                _write_xml_cache(stub, empty_set)
                out[c] = empty_set
        if i + batch_size < len(to_request):
            time.sleep(interval)
    return out


def parse_cached_pmid(
    pmid: str,
    *,
    cache_dir: Path,
) -> dict[str, str] | None:
    """Read cache file and parse; None if missing or empty article set."""
    clean = re.sub(r"\D", "", str(pmid))
    path = cache_dir / f"{clean}.xml"
    raw = _read_xml_cache(path)
    if raw is None:
        return None
    rows = parse_pubmed_efetch_xml(raw)
    for r in rows:
        if r.get("PMID") == clean:
            return r
    return None


def _load_pmid_file(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    return [ln.strip() for ln in lines if ln.strip()]


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Fetch/cache PubMed XML via Entrez.")
    parser.add_argument("pmids", nargs="*", help="PubMed IDs")
    parser.add_argument(
        "--pmid-file",
        type=Path,
        help="File with one PMID per line (e.g. not_in_lib.pmidlist)",
    )
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=None,
        help="Default: <repo>/.cache/pubmed",
    )
    parser.add_argument("--force", action="store_true", help="Ignore cache")
    parser.add_argument(
        "--dump-json",
        action="store_true",
        help="Print parsed records as JSON to stdout",
    )
    args = parser.parse_args(argv)

    ids: list[str] = list(args.pmids)
    if args.pmid_file:
        ids.extend(_load_pmid_file(args.pmid_file.resolve()))

    if not ids:
        parser.error("Provide PMIDs or --pmid-file")

    cache = args.cache_dir or pubmed_cache_dir()
    fetch_pubmed_batch_cached(
        ids, cache_dir=cache, force=args.force
    )
    if args.dump_json:
        records: list[dict[str, str]] = []
        for p in ids:
            c = re.sub(r"\D", "", p)
            rec = parse_cached_pmid(c, cache_dir=cache)
            if rec:
                records.append(rec)
        print(json.dumps(records, indent=2))
    else:
        print(f"Cached under {cache}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
