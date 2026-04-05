import html
import re

import pandas as pd

# Set by main.build before write_md to link badges to docs/tags/<slug>/.
TAG_SLUG_MAP: dict[str, str] | None = None

_BR_TAG = re.compile(r"(?i)<br\s*/?>")


def iter_markdown_inline_links(text: str):
    """
    Yield (start, end, label, href) for each ``[label](href)`` in text.

    ``href`` may contain unescaped ``)`` (e.g. Wiley ``(ISSN)…`` URLs). A balanced
    scan finds the closing ``)`` of the link, unlike a naive ``[^)]*`` regex.
    Skips image links ``![...](...)``.
    """
    n = len(text)
    i = 0
    while i < n:
        start = text.find("[", i)
        if start < 0:
            return
        if start > 0 and text[start - 1] == "!":
            i = start + 1
            continue
        close_br = text.find("]", start + 1)
        if close_br < 0:
            return
        if close_br + 1 >= n or text[close_br + 1] != "(":
            i = start + 1
            continue
        href_start = close_br + 2
        depth = 1
        j = href_start
        while j < n and depth > 0:
            c = text[j]
            if c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
            j += 1
        if depth != 0:
            i = start + 1
            continue
        label = text[start + 1 : close_br]
        href = text[href_start : j - 1]
        yield (start, j, label, href)
        i = j


def _anchor_id(name: str) -> str:
    """Fallback slug when NAME_FOR_LINK is missing."""
    return "-".join(str(name).strip().lower().split()) or "entry"


def _heading_id_attr(row: pd.Series) -> str:
    """Match summary-table links from format_table.fix_name_link (NAME_FOR_LINK)."""
    if "NAME_FOR_LINK" in row.index and pd.notna(row["NAME_FOR_LINK"]):
        s = str(row["NAME_FOR_LINK"]).strip()
        if s:
            return s
    return _anchor_id(str(row["NAME"]))


def _escape_with_md_links(text: str) -> str:
    """HTML-escape text but preserve markdown [label](href) as real <a> tags."""
    out: list[str] = []
    pos = 0
    for start, end, label_raw, href_raw in iter_markdown_inline_links(text):
        out.append(html.escape(text[pos:start]))
        label = html.escape(label_raw)
        href = html.escape(href_raw, quote=True)
        out.append(f'<a href="{href}">{label}</a>')
        pos = end
    out.append(html.escape(text[pos:]))
    return "".join(out)


def _format_rich_field_html(text: str) -> str:
    """
    Escape for safe HTML and markdown links; real <br> and newlines become HTML line breaks.
    """
    s = str(text).replace("\r\n", "\n").replace("\r", "\n")
    s = _BR_TAG.sub("<br>", s)
    s = s.replace("\n", "<br>")
    chunks = re.split(r"(?i)<br>", s)
    parts: list[str] = []
    for c in chunks:
        t = c.strip()
        parts.append(_escape_with_md_links(t) if t else "")
    return "<br>\n".join(parts)


def _format_field_html(text: str) -> str:
    return _format_rich_field_html(text)


# Default MkDocs / card tags when JSON has no TAG / TAGS / BADGE / BADGES.
_SECTION_DEFAULT_BADGES: dict[str, str] = {
    "Tools": "Tool",
    "Biobanks": "Biobank / cohort",
    "References": "Reference",
    "Single_Cell": "Single cell",
    "Sumstats": "Summary statistics",
    "Journals": "Journal",
    "Projects": "Program",
    "Coding": "Coding",
}


def _badge_cell_nonempty(val) -> bool:
    """True if TAGS/TAG/BADGE cell should be read (safe for list-valued JSON)."""
    if val is None:
        return False
    if hasattr(val, "tolist") and not isinstance(val, (list, tuple, str, bytes)):
        try:
            val = val.tolist()
        except Exception:
            pass
    if isinstance(val, (list, tuple)):
        return any(str(x).strip() for x in val)
    if isinstance(val, str):
        return bool(val.strip())
    try:
        if pd.isna(val):
            return False
    except (ValueError, TypeError):
        pass
    return True


def _parse_badges_cell(val) -> list[str]:
    """Normalize TAG / TAGS / BADGE / BADGES from JSON (string, list, or semicolon-separated)."""
    if val is None:
        return []
    if isinstance(val, float) and pd.isna(val):
        return []
    if isinstance(val, (list, tuple)):
        return [str(x).strip() for x in val if str(x).strip()]
    if hasattr(val, "tolist"):
        try:
            return _parse_badges_cell(val.tolist())
        except Exception:
            pass
    s = str(val).strip()
    if not s or s.lower() == "nan":
        return []
    if ";" in s:
        return [p.strip() for p in s.split(";") if p.strip()]
    return [s]


def _badges_for_row(row: pd.Series) -> list[str]:
    if "TAGS" in row.index and _badge_cell_nonempty(row["TAGS"]):
        parsed = _parse_badges_cell(row["TAGS"])
        if parsed:
            return parsed
    if "TAG" in row.index and _badge_cell_nonempty(row["TAG"]):
        parsed = _parse_badges_cell(row["TAG"])
        if parsed:
            return parsed
    if "BADGES" in row.index and _badge_cell_nonempty(row["BADGES"]):
        parsed = _parse_badges_cell(row["BADGES"])
        if parsed:
            return parsed
    if "BADGE" in row.index and _badge_cell_nonempty(row["BADGE"]):
        parsed = _parse_badges_cell(row["BADGE"])
        if parsed:
            return parsed
    sec = str(row.get("SECTION", "") or "").strip()
    if sec in _SECTION_DEFAULT_BADGES:
        return [_SECTION_DEFAULT_BADGES[sec]]
    if sec:
        return [sec.replace("_", " ")]
    return []


def _norm_compare(s: str) -> str:
    """Collapse whitespace for comparing display strings."""
    return " ".join(str(s).strip().split()).casefold()


def _skip_redundant_name_field(item: str, raw: str, display_name: str) -> bool:
    """Omit NAME / SHORT NAME / FULL NAME when same as the card title (heading)."""
    if item == "NAME":
        return _norm_compare(raw) == _norm_compare(display_name)
    if item not in ("SHORT NAME", "FULL NAME"):
        return False
    return _norm_compare(raw) == _norm_compare(display_name)


def _short_name_for_title(row: pd.Series, output_items) -> str | None:
    """If SHORT NAME differs from title, return it to show as (abbr) next to the heading."""
    if "SHORT NAME" not in output_items or "SHORT NAME" not in row.index:
        return None
    val = row["SHORT NAME"]
    if pd.isna(val):
        return None
    short = str(val).strip()
    if not short:
        return None
    display_name = str(row["NAME"]).strip()
    if _norm_compare(short) == _norm_compare(display_name):
        return None
    return short


def _card_section_class(field_key: str) -> str:
    base = "catalog-entry-card__section"
    primary = field_key.split("\n", 1)[0].strip()
    if primary == "CITATION":
        return f"{base} {base}--citation"
    return base


_COLLAPSIBLE_KIND_UI: dict[str, tuple[str, str]] = {
    "abstract": ("Show or hide full abstract text", "Show full abstract"),
    "description": ("Show or hide full description text", "Show full description"),
    "mesh_major": ("Show or hide full MeSH major terms", "Show full MeSH major"),
    "mesh_minor": ("Show or hide full MeSH minor terms", "Show full MeSH minor"),
    "keywords": ("Show or hide full keywords", "Show full keywords"),
}


def _write_collapsible_field_section(
    file, field_label: str, text: str, toggle_uid: int, kind: str
) -> None:
    """Long text clipped (~few lines) + expand (kind selects aria / button label)."""
    tid = f"catalog-col-{kind}-{toggle_uid}"
    body = _format_rich_field_html(str(text).strip())
    aria, more_txt = _COLLAPSIBLE_KIND_UI.get(
        kind,
        ("Show or hide full field text", "Show full text"),
    )
    name_esc = html.escape(field_label)
    file.write(
        '  <section class="catalog-entry-card__section '
        'catalog-entry-card__section--collapsible">\n'
    )
    file.write(f'    <div class="catalog-entry-card__field-name">{name_esc}</div>\n')
    file.write(
        f'    <input type="checkbox" id="{tid}" class="catalog-collapsible-toggle" '
        f'aria-label="{html.escape(aria, quote=True)}">\n'
    )
    file.write(f'    <div class="catalog-entry-card__collapsible-clipped">{body}</div>\n')
    file.write(f'    <label for="{tid}" class="catalog-collapsible-label">')
    file.write(f'<span class="catalog-collapsible-more">{html.escape(more_txt)}</span>')
    file.write('<span class="catalog-collapsible-less">Show less</span>')
    file.write("</label>\n")
    file.write("  </section>\n")


_CARD_FIELD_LABELS: dict[str, str] = {
    "MAIN_ANCESTRY": "MAIN ANCESTRY",
    "CITATION": "Main citation",
    "COMPANY": "Company",
}


def _card_field_label(item: str) -> str:
    return _CARD_FIELD_LABELS.get(item, item)


def section_theme_slug_for_row(row) -> str | None:
    """HTML data-catalog-section value; matches CSS [data-catalog-section=…] and hub SECTION slugs."""
    sec = str(row.get("SECTION", "") or "").strip()
    topic = str(row.get("TOPIC", "") or "").strip()
    if sec == "Tools" and topic == "Population_Genetics":
        return "Population_Genetics"
    if not sec:
        return None
    return sec


def _write_entry_card(
    file,
    row,
    columns,
    output_items,
    heading_tag: str,
    toggle_uid: int,
    *,
    tag_slug_map: dict[str, str] | None = None,
    badge_listing_links: bool = True,
    canonical_href: str | None = None,
) -> None:
    name = str(row["NAME"]).strip()
    aid = html.escape(_heading_id_attr(row), quote=True)
    short_in_title = _short_name_for_title(row, output_items)
    title_inner = html.escape(name)
    if short_in_title is not None:
        title_inner += (
            ' <span class="catalog-entry-card__title-abbr">'
            f"({html.escape(short_in_title)})</span>"
        )
    if canonical_href:
        title_inner = (
            f'<a class="catalog-entry-card__title-link" '
            f'href="{html.escape(canonical_href, quote=True)}">{title_inner}</a>'
        )
    badges = _badges_for_row(row)
    sec_slug = section_theme_slug_for_row(row)
    file.write("\n\n")
    if sec_slug:
        esc_sec = html.escape(sec_slug, quote=True)
        file.write(f'<article class="catalog-entry-card" data-catalog-section="{esc_sec}">\n')
    else:
        file.write('<article class="catalog-entry-card">\n')
    file.write('  <header class="catalog-entry-card__header">\n')
    file.write(
        f'    <{heading_tag} id="{aid}" '
        f'class="catalog-entry-card__title">{title_inner}</{heading_tag}>\n'
    )
    if badges:
        file.write('    <div class="catalog-entry-card__badges" role="list">\n')
        sm = tag_slug_map if tag_slug_map is not None else TAG_SLUG_MAP
        for b in badges:
            slug = sm.get(b) if sm else None
            if slug:
                href = f"../tags/{slug}/" if badge_listing_links else f"{slug}/"
                file.write(
                    f'      <a href="{html.escape(href, quote=True)}" '
                    f'class="catalog-badge catalog-badge--link" role="listitem">'
                    f"{html.escape(b)}</a>\n"
                )
            else:
                file.write(
                    f'      <span class="catalog-badge" role="listitem">'
                    f"{html.escape(b)}</span>\n"
                )
        file.write("    </div>\n")
    file.write("  </header>\n")
    file.write('  <div class="catalog-entry-card__fields">\n')

    for item in output_items:
        if item not in columns:
            continue
        if item in ("TAG", "TAGS", "BADGE", "BADGES"):
            continue
        if item == "SHORT NAME" and short_in_title is not None:
            continue
        val = row[item]
        if pd.isna(val):
            continue
        raw = str(val).strip()
        if not raw:
            continue
        if _skip_redundant_name_field(item, raw, name):
            continue
        if "\n" in item:
            for record in raw.split("\n"):
                record = record.strip()
                if not record:
                    continue
                file.write(f'  <section class="{_card_section_class(item)}">\n')
                file.write(
                    f'    <div class="catalog-entry-card__field-name">'
                    f"{html.escape(_card_field_label(item.strip()))}</div>\n"
                )
                file.write(f'    <div class="catalog-entry-card__value">{_format_field_html(record)}</div>\n')
                file.write("  </section>\n")
            continue
        if item == "ABSTRACT":
            _write_collapsible_field_section(file, "ABSTRACT", raw, toggle_uid, "abstract")
            continue
        if item == "DESCRIPTION":
            _write_collapsible_field_section(file, "DESCRIPTION", raw, toggle_uid, "description")
            continue
        if item == "MESH_MAJOR":
            _write_collapsible_field_section(
                file, _card_field_label(item), raw, toggle_uid, "mesh_major"
            )
            continue
        if item == "MESH_MINOR":
            _write_collapsible_field_section(
                file, _card_field_label(item), raw, toggle_uid, "mesh_minor"
            )
            continue
        if item == "KEYWORDS":
            _write_collapsible_field_section(
                file, _card_field_label(item), raw, toggle_uid, "keywords"
            )
            continue
        file.write(f'  <section class="{_card_section_class(item)}">\n')
        file.write(
            f'    <div class="catalog-entry-card__field-name">'
            f"{html.escape(_card_field_label(item))}</div>\n"
        )
        file.write(f'    <div class="catalog-entry-card__value">{_format_field_html(raw)}</div>\n')
        file.write("  </section>\n")

    file.write("  </div>\n</article>\n")


def _sort_for_entry_cards(df_combined: pd.DataFrame) -> pd.DataFrame:
    """Prefer STAGE_ORDER (Projects phases) when the column exists and is populated."""
    if "STAGE_ORDER" in df_combined.columns and df_combined["STAGE_ORDER"].notna().any():
        return df_combined.sort_values(
            by=["STAGE_ORDER", "NAME"],
            na_position="last",
        )
    return df_combined.sort_values(by=["NAME"])


def print_one_level(filename, df_combined, output_items):
    toggle_uid = 0
    with open(filename, "a") as file:
        for _index, row in _sort_for_entry_cards(df_combined).iterrows():
            toggle_uid += 1
            _write_entry_card(
                file, row, df_combined.columns, output_items, "h2", toggle_uid
            )


def print_two_level(filename, df_combined, output_items):
    toggle_uid = 0
    with open(filename, "a") as file:
        for category in df_combined["CATEGORY"].sort_values().unique():
            file.write("\n\n")
            file.write(f"## {category}\n\n")

            sub = _sort_for_entry_cards(
                df_combined.loc[df_combined["CATEGORY"] == category, :]
            )
            for _index, row in sub.iterrows():
                toggle_uid += 1
                _write_entry_card(
                    file, row, df_combined.columns, output_items, "h3", toggle_uid
                )


def write_markdown(filename, df_combined, output_items):
    if not df_combined["CATEGORY"].isna().all():
        print_two_level(filename, df_combined, output_items)
    else:
        print_one_level(filename, df_combined, output_items)
