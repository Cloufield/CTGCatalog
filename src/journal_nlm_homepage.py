"""
Resolve a journal's official website URL via NCBI NLM Catalog (E-utilities).

NLM Catalog records often include ``ELocationID`` with ``EIdType="url"`` pointing
at the publisher site (e.g. nature.com). PMC browse links are filtered out.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

from pubmed_entrez import DEFAULT_NCBI_EMAIL

_NCBI_ES = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
_last_ncbi_mono = 0.0


def _ncbi_throttle() -> None:
    """Stay under ~3 req/s without API key (NLM + PubMed share limits)."""
    global _last_ncbi_mono
    min_gap = 0.34
    if os.environ.get("NCBI_API_KEY", "").strip():
        min_gap = 0.11
    now = time.monotonic()
    wait = min_gap - (now - _last_ncbi_mono)
    if wait > 0:
        time.sleep(wait)
    _last_ncbi_mono = time.monotonic()


def _ncbi_tool_params() -> str:
    email = (os.environ.get("NCBI_EMAIL") or DEFAULT_NCBI_EMAIL).strip()
    q = [("tool", "CTGCatalog"), ("email", email or "dev@localhost")]
    key = (os.environ.get("NCBI_API_KEY") or "").strip()
    if key:
        q.append(("api_key", key))
    return urllib.parse.urlencode(q)


def _http_get(url: str) -> bytes:
    _ncbi_throttle()
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": f"CTGCatalog/sync_journals (mailto:{(os.environ.get('NCBI_EMAIL') or DEFAULT_NCBI_EMAIL).strip() or 'dev@localhost'})",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def _xml_local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def _nlm_esearch_ids(term: str) -> list[str]:
    if not term.strip():
        return []
    params = [
        ("db", "nlmcatalog"),
        ("retmode", "json"),
        ("retmax", "40"),
        ("term", term.strip()),
    ]
    url = f"{_NCBI_ES}/esearch.fcgi?{urllib.parse.urlencode(params)}&{_ncbi_tool_params()}"
    try:
        raw = _http_get(url)
        data = json.loads(raw.decode())
        return list(data.get("esearchresult", {}).get("idlist", []) or [])
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError):
        return []


def _nlm_efetch_xml(id_list: list[str]) -> str:
    if not id_list:
        return ""
    params = [
        ("db", "nlmcatalog"),
        ("id", ",".join(id_list[:30])),
        ("retmode", "xml"),
    ]
    url = f"{_NCBI_ES}/efetch.fcgi?{urllib.parse.urlencode(params)}&{_ncbi_tool_params()}"
    try:
        return _http_get(url).decode("utf-8", errors="replace")
    except (urllib.error.URLError, TimeoutError):
        return ""


def _iter_nlmcatalog_records(root: ET.Element):
    for el in root:
        if _xml_local(el.tag) == "NLMCatalogRecord":
            yield el


def _medline_ta(record: ET.Element) -> str:
    for el in record.iter():
        if _xml_local(el.tag) == "MedlineTA" and el.text:
            return el.text.strip()
    return ""


def _title_main(record: ET.Element) -> str:
    for el in record.iter():
        if _xml_local(el.tag) == "TitleMain":
            for t in el.iter():
                if _xml_local(t.tag) == "Title" and t.text:
                    return t.text.strip().rstrip(".")
    return ""


def _collect_elocation_urls(record: ET.Element) -> list[str]:
    out: list[str] = []
    for el in record.iter():
        if _xml_local(el.tag) != "ELocationID":
            continue
        if el.attrib.get("EIdType") != "url" or not el.text:
            continue
        u = el.text.strip()
        if u:
            out.append(u)
    return out


def _pick_publisher_url(urls: list[str]) -> str:
    if not urls:
        return ""
    bad_substrings = (
        "pmc.ncbi.nlm.nih.gov/journals/",
        "ncbi.nlm.nih.gov/nlmcatalog",
    )
    for u in urls:
        if not any(b in u for b in bad_substrings):
            return u
    return urls[0]


def _score_record(record: ET.Element, iso: str, journal: str) -> int:
    ta = _medline_ta(record).casefold()
    iso_cf = (iso or "").strip().casefold()
    jour_cf = (journal or "").strip().casefold().rstrip(".")
    title = _title_main(record).casefold()
    s = 0
    if iso_cf and ta == iso_cf:
        s += 200
    elif iso_cf and ta.replace(" ", "") == iso_cf.replace(" ", ""):
        s += 160
    if jour_cf and jour_cf in title:
        s += 80
    elif jour_cf and title and jour_cf[:20] in title:
        s += 40
    return s


def nlm_catalog_journal_homepage_url(iso: str, journal: str) -> str:
    """
    Return an official journal website URL from the NLM Catalog, or "" if none found.
    """
    iso = (iso or "").strip()
    journal = (journal or "").strip()
    uids: list[str] = []

    if iso:
        uids = _nlm_esearch_ids(f"{iso}[ta]")
    if not uids and journal:
        uids = _nlm_esearch_ids(f"{journal}[jour]")

    if not uids:
        return ""

    xml = _nlm_efetch_xml(uids)
    if not xml.strip():
        return ""

    try:
        root = ET.fromstring(xml)
    except ET.ParseError:
        return ""

    best_score = -1
    best_url = ""
    for rec in _iter_nlmcatalog_records(root):
        sc = _score_record(rec, iso, journal)
        url = _pick_publisher_url(_collect_elocation_urls(rec))
        if url and sc > best_score:
            best_score = sc
            best_url = url

    if best_url:
        return best_url

    for rec in _iter_nlmcatalog_records(root):
        url = _pick_publisher_url(_collect_elocation_urls(rec))
        if url:
            return url
    return ""
