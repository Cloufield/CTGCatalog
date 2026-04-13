"""Generate Major databases hub, per-continent listing pages, and mkdocs ``not_in_nav`` paths (no top tab)."""

from __future__ import annotations

import html
import json
import re
from io import StringIO
from pathlib import Path

import yaml

from catalog_sources import repo_databases_dir
from print_level import _format_field_html, _write_collapsible_field_section

_DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
_HUB_PATH = _DOCS_DIR / "Major_Databases.md"

_COUNTRY_ORDER = [
    "international",
    "china",
    "japan",
    "republic_of_korea",
    "united_states",
    "united_kingdom_and_europe",
    "germany",
    "australia",
    "canada",
]

_COUNTRY_HEADINGS = {
    "international": "International",
    "china": "China",
    "japan": "Japan",
    "republic_of_korea": "Republic of Korea",
    "united_states": "United States",
    "united_kingdom_and_europe": "United Kingdom / Europe",
    "germany": "Germany",
    "australia": "Australia",
    "canada": "Canada",
}

# json/databases/<folder>/ → continent tab in the left nav (same labels as Biobanks).
_FOLDER_TO_CONTINENT: dict[str, str] = {
    "china": "ASIA",
    "japan": "ASIA",
    "republic_of_korea": "ASIA",
    "united_states": "AMERICA",
    "canada": "AMERICA",
    "united_kingdom_and_europe": "EUROPE",
    "germany": "EUROPE",
    "australia": "OCEANIA",
}

# Hub + sidebar order: International first, then continents (aligned with Biobanks).
_NAV_LISTING_ORDER: tuple[str, ...] = (
    "International",
    "AFRICA",
    "AMERICA",
    "ASIA",
    "EUROPE",
    "OCEANIA",
)

_HUB_LEAD = """National and regional archives that host sequence reads, assemblies, variants, and related metadata—especially those that mirror or complement the [INSDC](https://www.insdc.org/) (International Nucleotide Sequence Database Collaboration). Curated as JSON under [json/databases/](https://github.com/Cloufield/CTGCatalog/tree/main/json/databases) (one file per resource, grouped by country folder). Use the **continent** links below for each listing (same grouping as **Biobanks**)."""

_HUB_FOOTER = """If a resource should be added or updated, edit the JSON under `json/databases/<country>/` or open an issue or pull request on the [CTGCatalog repository](https://github.com/Cloufield/CTGCatalog/)."""


def _dump_front_matter(fm: dict) -> str:
    return (
        "---\n"
        + yaml.safe_dump(
            fm,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )
        + "---\n\n"
    )


def _entry_anchor_id(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", str(name).strip().lower())
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "database"


def _description_body(rec: dict) -> str:
    """Prose for the collapsible DESCRIPTION (KEY_DATABASES are separate card sections)."""
    return str(rec["DESCRIPTION"]).strip()


def _iter_key_databases(rec: dict) -> list[tuple[str, str, str, str]]:
    """(label, url, optional_description, optional_name_zh) from KEY_DATABASES."""
    keys = rec.get("KEY_DATABASES")
    if not isinstance(keys, list) or not keys:
        return []
    out: list[tuple[str, str, str, str]] = []
    for item in keys:
        if not isinstance(item, dict):
            continue
        n = str(item.get("NAME", "")).strip()
        u = str(item.get("URL", "")).strip()
        if not n or not u:
            continue
        d = str(item.get("DESCRIPTION") or "").strip()
        zh = str(item.get("NAME_ZH") or "").strip()
        out.append((n, u, d, zh))
    return out


def _load_by_country(root: Path) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    if not root.is_dir():
        return {}
    for country_dir in sorted(root.iterdir()):
        if not country_dir.is_dir() or country_dir.name.startswith("."):
            continue
        slug = country_dir.name
        bucket: list[tuple[str, dict]] = []
        for path in sorted(country_dir.glob("*.json")):
            if path.name.startswith("."):
                continue
            with open(path, encoding="utf-8") as f:
                rec = json.load(f)
            order = rec.get("DISPLAY_ORDER")
            try:
                order_n = int(order) if order is not None else 0
            except (TypeError, ValueError):
                order_n = 0
            bucket.append((order_n, path.name, rec))
        bucket.sort(key=lambda x: (x[0], x[1]))
        out[slug] = [row for _, _, row in bucket]
    return out


def _country_heading(slug: str) -> str:
    return _COUNTRY_HEADINGS.get(slug, slug.replace("_", " ").title())


def _nav_key_for_folder(slug: str) -> str:
    if slug == "international":
        return "International"
    cont = _FOLDER_TO_CONTINENT.get(slug)
    if cont is None:
        raise ValueError(
            f"json/databases/{slug}/ is not mapped to a continent; add it to "
            "_FOLDER_TO_CONTINENT in process_major_databases.py (or use folder "
            "`international` for non-regional hubs)."
        )
    return cont


def _listing_doc_basename(nav_key: str) -> str:
    return f"Major_Databases_{nav_key}.md"


def _sort_merged_items(items: list[tuple[str, dict]]) -> list[tuple[str, dict]]:
    def country_rank(folder: str) -> int:
        try:
            return _COUNTRY_ORDER.index(folder)
        except ValueError:
            return 999

    def sort_key(item: tuple[str, dict]) -> tuple[int, int, str]:
        folder, rec = item
        order = rec.get("DISPLAY_ORDER")
        try:
            on = int(order) if order is not None else 0
        except (TypeError, ValueError):
            on = 0
        nm = str(rec.get("NAME") or "")
        return (country_rank(folder), on, nm.casefold())

    return sorted(items, key=sort_key)


def _group_by_nav_listing(
    by_country: dict[str, list[dict]],
) -> dict[str, list[tuple[str, dict]]]:
    groups: dict[str, list[tuple[str, dict]]] = {}
    for folder_slug, rows in by_country.items():
        if not rows:
            continue
        nav_key = _nav_key_for_folder(folder_slug)
        bucket = groups.setdefault(nav_key, [])
        for rec in rows:
            bucket.append((folder_slug, rec))
    for k in list(groups):
        groups[k] = _sort_merged_items(groups[k])
    return groups


def _ordered_nav_keys(groups: dict[str, list[tuple[str, dict]]]) -> list[str]:
    nonempty = {k for k, v in groups.items() if v}
    ordered = [k for k in _NAV_LISTING_ORDER if k in nonempty]
    rest = sorted(nonempty - set(ordered))
    return ordered + rest


def _cleanup_stale_listing_pages(docs_dir: Path, keep_stem_suffixes: set[str]) -> None:
    for path in docs_dir.glob("Major_Databases_*.md"):
        stem = path.stem
        if not stem.startswith("Major_Databases_"):
            continue
        suffix = stem.removeprefix("Major_Databases_")
        if suffix not in keep_stem_suffixes:
            path.unlink()


def _append_database_card(lines: list[str], rec: dict, toggle_uid: int) -> None:
    name = str(rec["NAME"]).strip()
    url = str(rec["URL"]).strip()
    aid = html.escape(_entry_anchor_id(name), quote=True)
    desc = _description_body(rec)
    abbr = str(rec.get("ABBREVIATION") or "").strip()

    title_inner = html.escape(name)
    if abbr and abbr.casefold() != name.casefold():
        title_inner += (
            ' <span class="catalog-entry-card__title-abbr">'
            f"({html.escape(abbr)})</span>"
        )

    name_zh = str(rec.get("NAME_ZH") or "").strip()

    lines.append('\n\n<article class="catalog-entry-card" data-catalog-section="Major_Databases">\n')
    lines.append('  <header class="catalog-entry-card__header">\n')
    lines.append(
        f'    <h2 id="{aid}" class="catalog-entry-card__title">{title_inner}</h2>\n'
    )
    lines.append('    <div class="catalog-entry-card__badges" role="list">\n')
    lines.append(
        '      <span class="catalog-badge" role="listitem">Database</span>\n'
    )
    lines.append("    </div>\n")
    lines.append("  </header>\n")
    if name_zh:
        lines.append(
            f'  <p class="catalog-entry-card__name-zh" lang="zh-Hans">{html.escape(name_zh)}</p>\n'
        )
    lines.append('  <div class="catalog-entry-card__fields">\n')

    buf = StringIO()
    _write_collapsible_field_section(buf, "DESCRIPTION", desc, toggle_uid, "description")
    lines.append(buf.getvalue())

    for key_name, key_url, key_desc, key_name_zh in _iter_key_databases(rec):
        kn_esc = html.escape(key_name)
        ku_h = html.escape(key_url, quote=True)
        ku_d = html.escape(key_url)
        lines.append('  <section class="catalog-entry-card__section">\n')
        lines.append('    <div class="catalog-entry-card__field-name">')
        lines.append(kn_esc)
        if key_name_zh:
            kzh = html.escape(key_name_zh)
            lines.append(
                f'<br><span class="catalog-entry-card__field-name-zh" lang="zh-Hans">{kzh}</span>'
            )
        lines.append("</div>\n")
        lines.append('    <div class="catalog-entry-card__value">\n')
        lines.append(f'      <a href="{ku_h}">{ku_d}</a>\n')
        if key_desc:
            lines.append(
                '      <div class="catalog-entry-card__key-database-desc">'
                f"{_format_field_html(key_desc)}"
                "</div>\n"
            )
        lines.append("    </div>\n")
        lines.append("  </section>\n")

    url_href = html.escape(url, quote=True)
    url_disp = html.escape(url)
    lines.append('  <section class="catalog-entry-card__section">\n')
    lines.append('    <div class="catalog-entry-card__field-name">URL</div>\n')
    lines.append(
        f'    <div class="catalog-entry-card__value">'
        f'<a href="{url_href}">{url_disp}</a></div>\n'
    )
    lines.append("  </section>\n")

    subtitle = str(rec.get("SUBTITLE") or "").strip()
    if subtitle and subtitle.casefold() != abbr.casefold():
        lines.append('  <section class="catalog-entry-card__section">\n')
        lines.append('    <div class="catalog-entry-card__field-name">Also known as</div>\n')
        lines.append(
            f'    <div class="catalog-entry-card__value">{html.escape(subtitle)}</div>\n'
        )
        lines.append("  </section>\n")

    lines.append("  </div>\n</article>\n")


def _write_listing_page(
    docs_dir: Path,
    nav_key: str,
    items: list[tuple[str, dict]],
) -> None:
    path = docs_dir / _listing_doc_basename(nav_key)
    fm = {
        "hide": ["tags"],
        "tags": ["Reference", "Catalog"],
        "class": "catalog-section-Major_Databases",
    }
    folders = sorted({f for f, _ in items})
    folder_phrase = ", ".join(f"`{s}/`" for s in folders)
    lines: list[str] = [
        _dump_front_matter(fm),
        '<div class="catalog-nav-lead" markdown="block">\n\n',
        f"Curation of **{nav_key}** — major databases in this region (see the [Major databases hub](Major_Databases.md)).\n\n",
        "</div>\n\n",
        "## Summary Table\n\n",
        "*Click a column header to sort the table.*\n\n",
        '<div class="catalog-summary-table">\n\n',
        "<table>\n<thead>\n<tr>\n<th>NAME</th>\n<th>REGION</th>\n<th>URL</th>\n</tr>\n</thead>\n<tbody>\n",
    ]
    for folder_slug, rec in items:
        nm = str(rec["NAME"]).strip()
        ur = str(rec["URL"]).strip()
        eid_raw = _entry_anchor_id(nm)
        nm_esc = html.escape(nm)
        ur_esc = html.escape(ur)
        ur_href = html.escape(ur, quote=True)
        reg_esc = html.escape(_country_heading(folder_slug))
        name_zh = str(rec.get("NAME_ZH") or "").strip()
        lines.append("<tr>\n")
        lines.append(f'<td><a href="#{eid_raw}">{nm_esc}</a>')
        if name_zh:
            lines.append(
                f'<br><span class="catalog-summary-name-zh" lang="zh-Hans">'
                f"{html.escape(name_zh)}</span>"
            )
        lines.append("</td>\n")
        lines.append(f"<td>{reg_esc}</td>\n")
        lines.append(
            f'<td><a href="{ur_href}">{ur_esc}</a></td>\n'
        )
        lines.append("</tr>\n")
    lines.append("</tbody>\n</table>\n\n</div>\n")

    toggle_uid = 0
    for _folder_slug, rec in items:
        toggle_uid += 1
        _append_database_card(lines, rec, toggle_uid)

    lines.append("\n---\n\n")
    lines.append(
        f"Edit JSON under `json/databases/` (folders {folder_phrase}), then run "
        "`python main.py` from `src/`.\n\n"
    )
    path.write_text("".join(lines), encoding="utf-8")


def _write_hub(
    docs_dir: Path,
    groups: dict[str, list[tuple[str, dict]]],
    ordered_nav_keys: list[str],
) -> None:
    fm = {
        "hide": ["tags"],
        "tags": ["Reference", "Catalog"],
        "class": "catalog-section-Major_Databases",
    }
    lines: list[str] = [
        _dump_front_matter(fm),
        '<div class="catalog-nav-lead" markdown="block">\n\n',
        _HUB_LEAD,
        "\n\n</div>\n\n",
    ]
    if not ordered_nav_keys:
        lines.append(
            "_No entries yet._ Add `json/databases/<country_slug>/<name>.json` files "
            "(see `.design/database-entry.schema.json`).\n\n"
        )
    else:
        lines.append("## Contents - Major databases \n\n")
        lines.append('<div class="catalog-section-contents" markdown="block">\n\n')
        for nav_key in ordered_nav_keys:
            n = len(groups[nav_key])
            bn = _listing_doc_basename(nav_key)
            lines.append(f"  - [{nav_key}]({bn}) : {n}\n")
        lines.append("\n</div>\n\n")

    lines.append("---\n\n")
    lines.append(_HUB_FOOTER)
    lines.append("\n")
    _HUB_PATH.write_text("".join(lines), encoding="utf-8")


def major_databases_not_in_nav_paths() -> list[str]:
    """Paths relative to ``docs/`` for mkdocs ``not_in_nav`` (built site; no top tab)."""
    by = _load_by_country(repo_databases_dir())
    groups = _group_by_nav_listing(by)
    ordered = _ordered_nav_keys(groups)
    paths = ["Major_Databases.md"]
    for nav_key in ordered:
        paths.append(_listing_doc_basename(nav_key))
    return paths


def write_major_databases_md() -> None:
    """Write hub + per-continent pages; remove stale listing files."""
    root = repo_databases_dir()
    by_country = _load_by_country(root)
    groups = _group_by_nav_listing(by_country)
    ordered = _ordered_nav_keys(groups)
    keep_suffixes = set(ordered)

    _DOCS_DIR.mkdir(parents=True, exist_ok=True)
    _cleanup_stale_listing_pages(_DOCS_DIR, keep_suffixes)

    for nav_key in ordered:
        _write_listing_page(_DOCS_DIR, nav_key, groups[nav_key])

    _write_hub(_DOCS_DIR, groups, ordered)
