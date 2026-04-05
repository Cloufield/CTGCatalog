from __future__ import annotations

import html
import json
import re
import sys
import os
import shutil
from pathlib import Path

import pandas as pd
import yaml

from format_table import format_main
from print_level import _badges_for_row, iter_markdown_inline_links, write_markdown

_STANDARD_CARD_OUTPUT_ITEMS = [
    "NAME",
    "COMPANY",
    "PUBMED_LINK",
    "SHORT NAME",
    "FULL NAME",
    "STAGE_PERIOD",
    "DESCRIPTION",
    "URL",
    "KEYWORDS",
    "USE",
    "PREPRINT_DOI",
    "SERVER",
    "TITLE",
    "CITATION",
    "MESH_MAJOR",
    "MESH_MINOR",
    "ABSTRACT",
    "DOI",
    "RELATED_BIOBANK",
    "MAIN_ANCESTRY",
    "PARTICIPANTS",
    "SAMPLE SIZE",
    "ARRAY",
    "WGS/WES",
    "TRANSCRIPTOME",
    "METABOLOME",
    "PROTEOME",
    "METHYLOME",
    "METAGENOME",
    "IMAGAING",
    "DATA ACCESS",
    "ARROW_SUMMARY",
    "AI_GENERATED",
]


def _is_journals_catalog_doc(path: str) -> bool:
    """Single-page Journals section (same nav pattern as Catalog statistics)."""
    return Path(path).name == "Journals.md"


_JOURNAL_SECTION_BAR_ORDER = (
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

_JOURNAL_SECTION_CSS_VARS: dict[str, str] = {
    "Tools": "var(--catalog-journal-sec-tools)",
    "Sumstats": "var(--catalog-journal-sec-sumstats)",
    "References": "var(--catalog-journal-sec-references)",
    "Single_Cell": "var(--catalog-journal-sec-single_cell)",
    "Biobanks": "var(--catalog-journal-sec-biobanks)",
    "Projects": "var(--catalog-journal-sec-projects)",
    "Coding": "var(--catalog-journal-sec-coding)",
    "Journals": "var(--catalog-journal-sec-journals)",
    "MISC": "var(--catalog-journal-sec-misc)",
}


def _journal_section_bar_keys(counts: dict[str, int]) -> list[str]:
    keys = {k for k, v in counts.items() if v and int(v) > 0}
    ordered = [s for s in _JOURNAL_SECTION_BAR_ORDER if s in keys]
    rest = sorted(keys - set(ordered))
    return ordered + rest


def _journal_section_counts_from_row(row: pd.Series) -> dict[str, int]:
    v = row.get("CITED_BY_SECTION")
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return {}
    if isinstance(v, dict):
        out: dict[str, int] = {}
        for k, n in v.items():
            try:
                iv = int(n)
            except (TypeError, ValueError):
                continue
            if iv > 0:
                out[str(k)] = iv
        return out
    if isinstance(v, str):
        try:
            d = json.loads(v)
        except json.JSONDecodeError:
            return {}
        if isinstance(d, dict):
            out = {}
            for k, n in d.items():
                try:
                    iv = int(n)
                except (TypeError, ValueError):
                    continue
                if iv > 0:
                    out[str(k)] = iv
            return out
    return {}


def _journal_cite_background(counts: dict[str, int], fill_pct: float) -> str:
    """Same bar geometry as ``catalog-stats-count``: fill from the right, full cell height."""
    keys = [k for k in _journal_section_bar_keys(counts) if counts.get(k, 0) > 0]
    if not keys:
        return (
            "linear-gradient(to left, transparent 0%, transparent 100%)"
        )
    total = sum(counts[k] for k in keys)
    if total <= 0:
        return (
            "linear-gradient(to left, transparent 0%, transparent 100%)"
        )
    f = min(100.0, max(0.0, fill_pct)) / 100.0
    if f <= 0:
        return (
            "linear-gradient(to left, transparent 0%, transparent 100%)"
        )
    rev = list(reversed(keys))
    stops: list[str] = []
    cum = 0.0
    for sec in rev:
        col = _JOURNAL_SECTION_CSS_VARS.get(sec, "var(--catalog-journal-sec-unknown)")
        w = counts[sec] / total
        g0 = cum * f * 100.0
        cum += w
        g1 = cum * f * 100.0
        stops.append(f"{col} {g0:.4f}%")
        stops.append(f"{col} {g1:.4f}%")
    stops.append(f"transparent {g1:.4f}%")
    return f"linear-gradient(to left, {', '.join(stops)})"


def _write_journals_legend_html(file, df: pd.DataFrame) -> None:
    union: set[str] = set()
    for _, row in df.iterrows():
        union.update(_journal_section_counts_from_row(row).keys())
    order = _journal_section_bar_keys({k: 1 for k in union})
    file.write('<div class="catalog-journals-legend">\n')
    file.write(
        '<p class="catalog-journals-legend-title">'
        "Cited in CTGCatalog — section colors</p>\n"
    )
    file.write('<div class="catalog-journals-legend-row">\n')
    for sec in order:
        label = html.escape(sec.replace("_", " "))
        esc = html.escape(sec)
        file.write(
            f'<span class="catalog-journals-legend-item">'
            f'<span class="catalog-journals-swatch" data-section="{esc}"></span> '
            f'<span class="catalog-journals-legend-label">{label}</span></span>\n'
        )
    file.write("</div>\n</div>\n\n")


def _write_journals_stats_table_html(file, df: pd.DataFrame) -> None:
    totals = pd.to_numeric(df["ENTRY_COUNT"], errors="coerce").fillna(0).astype(int)
    max_total = int(totals.max()) if len(totals) else 0
    max_total = max(max_total, 1)

    file.write('<table class="catalog-stats-table catalog-journals-table">\n')
    file.write(
        "<thead><tr><th>Journal</th>"
        "<th>Cited in CTGCatalog</th></tr></thead>\n<tbody>\n"
    )
    for (_, row), total in zip(df.iterrows(), totals):
        name_plain = str(row.get("_NAME", "") or "").strip()
        slug = str(row.get("NAME_FOR_LINK", "") or "").strip()
        if not slug:
            slug = re.sub(
                r"[^a-z0-9-]+",
                "",
                re.sub(r"\s+", "-", name_plain.lower()),
                flags=re.I,
            )
        name_esc = html.escape(name_plain)
        slug_esc = html.escape(slug)
        counts = _journal_section_counts_from_row(row)
        if not counts and total > 0:
            counts = {"MISC": total}
        fill_pct = min(100.0, 100.0 * float(total) / float(max_total))
        bg = _journal_cite_background(counts, fill_pct)
        file.write("<tr>\n")
        file.write(
            f'<td class="catalog-journals-name">'
            f'<a href="#{slug_esc}">{name_esc}</a></td>\n'
        )
        file.write(
            f'<td class="catalog-stats-count" style="background:{bg}">'
            f"{int(total)}</td>\n"
        )
        file.write("</tr>\n")
    file.write("</tbody></table>\n")


# Biobank cards: keep a single SAMPLE SIZE; omit per-modality breakdowns.
_BIOBANKS_OMIT_CARD_FIELDS = frozenset(
    {
        "ARRAY",
        "WGS/WES",
        "TRANSCRIPTOME",
        "METABOLOME",
        "PROTEOME",
        "METHYLOME",
        "METAGENOME",
        "IMAGAING",
    }
)


def _card_output_items_for_path(md_path: str) -> list[str]:
    """Journal hub cards: no DESCRIPTION; show URL near the top."""
    if _is_journals_catalog_doc(md_path):
        items = [i for i in _STANDARD_CARD_OUTPUT_ITEMS if i != "DESCRIPTION"]
        items.remove("URL")
        items.insert(items.index("NAME") + 1, "URL")
        return items
    base = Path(md_path).name
    if base.startswith("Biobanks"):
        return [
            i
            for i in _STANDARD_CARD_OUTPUT_ITEMS
            if i not in _BIOBANKS_OMIT_CARD_FIELDS
        ]
    return list(_STANDARD_CARD_OUTPUT_ITEMS)


_SUMMARY_TRUNCATE_COLS = frozenset(
    {"CITATION", "TITLE", "MAIN_ANCESTRY", "PARTICIPANTS"}
)
_SUMMARY_TRUNCATE_LEN = 118
_BR_HTML = re.compile(r"(?i)<br\s*/?>")
_URL_SPLIT = re.compile(r"\s+")


def _summary_cell_str(v) -> str:
    if v is None:
        return ""
    if isinstance(v, float) and pd.isna(v):
        return ""
    try:
        if pd.isna(v):
            return ""
    except TypeError:
        pass
    s = str(v).strip()
    if s in ("", "NA", "nan"):
        return ""
    return s


def _author_count_from_authors_field(v) -> int:
    s = _summary_cell_str(v)
    if not s:
        return 0
    return len([p for p in s.split(",") if p.strip()])


def _minimal_summary_citation(row: pd.Series) -> str:
    """Compact table line: first author (et al.), journal abbr or name, year."""
    fa = _summary_cell_str(row.get("FIRST_AUTHOR"))
    if not fa:
        auth = _summary_cell_str(row.get("Authors"))
        if auth:
            fa = auth.split(",")[0].strip()

    journal = _summary_cell_str(row.get("ISO")) or _summary_cell_str(row.get("JOURNAL"))
    year = _summary_cell_str(row.get("YEAR"))
    n_auth = _author_count_from_authors_field(row.get("Authors"))

    parts: list[str] = []
    if fa:
        if n_auth > 1:
            parts.append(f"{fa} et al.")
        elif n_auth == 1:
            parts.append(fa)
        else:
            parts.append(f"{fa} et al.")
    if journal:
        parts.append(journal)
    if year:
        parts.append(year)

    if parts:
        return ", ".join(parts)

    cit = row.get("CITATION")
    if cit is not None and not pd.isna(cit):
        s = str(cit).strip()
        if s:
            s = _BR_HTML.sub(" · ", s)
            return _truncate_summary_cell(s)
    return "NA"


def _full_citation_for_tooltip(row: pd.Series) -> str:
    """Plain text for HTML title= on summary “Main citation” cells."""
    cit = row.get("CITATION")
    if cit is not None and not pd.isna(cit):
        s = str(cit).strip()
        if s:
            return _BR_HTML.sub(" · ", s)
    return _minimal_summary_citation(row)


def _truncate_summary_cell(val, max_len: int = _SUMMARY_TRUNCATE_LEN) -> str:
    """Shorten long citation/title cells for the summary table (word-aware)."""
    if pd.isna(val):
        return "NA"
    s = str(val).strip()
    if s == "" or s == "NA":
        return s or "NA"
    if len(s) <= max_len:
        return s
    cut = s[: max_len - 1]
    if " " in cut:
        cut = cut.rsplit(" ", 1)[0]
    return cut + "\u2026"


def _apply_summary_truncation(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in out.columns:
        if col in _SUMMARY_TRUNCATE_COLS:
            out[col] = out[col].apply(_truncate_summary_cell)
    return out


def _sanitize_summary_table_cell(val) -> str:
    """
    One line per cell for valid GitHub-style pipe tables: no raw | or HTML breaks.
    """
    if pd.isna(val):
        return "NA"
    s = str(val).strip()
    if not s or s == "NA":
        return s or "NA"
    s = _BR_HTML.sub(" · ", s)
    s = s.replace("|", "\\|")
    s = re.sub(r"\s+", " ", s).strip()
    return s if s else "NA"


def _sanitize_summary_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in out.columns:
        out[col] = out[col].map(_sanitize_summary_table_cell)
    return out


def _undo_markdown_pipe_escape(s: str) -> str:
    """GitHub pipe-table escaping: show literal | in HTML cells."""
    return s.replace("\\|", "|")


def _summary_name_cell_to_html(val) -> str:
    """NAME column uses markdown [label](#anchor) from format_table."""
    if pd.isna(val):
        return html.escape("NA")
    s = _undo_markdown_pipe_escape(str(val).strip())
    if not s or s == "NA":
        return html.escape(s or "NA")
    m = re.fullmatch(r"\[([^\]]*)\]\(([^)]+)\)", s)
    if m:
        return (
            f'<a href="{html.escape(m.group(2), quote=True)}">'
            f"{html.escape(m.group(1))}</a>"
        )
    return html.escape(s)


def _summary_value_is_empty_for_column_drop(val) -> bool:
    """Treat NA, blank, and literal “NA” as empty when deciding to hide a column."""
    if pd.isna(val):
        return True
    s = str(val).strip()
    return s == "" or s == "NA"


def _summary_column_entirely_empty(col: pd.Series) -> bool:
    return all(_summary_value_is_empty_for_column_drop(v) for v in col)


def _urls_from_summary_cell(raw) -> list[str]:
    """
    URLs for summary-table links. ``format_main`` stores URL as markdown ``[u](u)``
    (see ``format_table.fix_url``); also accept plain ``https://`` tokens.
    """
    if pd.isna(raw):
        return []
    s = _undo_markdown_pipe_escape(str(raw).strip())
    if not s or s == "NA":
        return []
    found: list[str] = []
    for _s, _e, _lab, href in iter_markdown_inline_links(s):
        h = href.strip()
        if h:
            found.append(h)
    if found:
        return found
    for part in re.split(r"\s*,\s*", s):
        part = part.strip()
        if not part or part == "NA":
            continue
        for p in _URL_SPLIT.split(part):
            p = p.strip().rstrip(",").strip()
            if p.startswith(("http://", "https://")):
                found.append(p)
    return found


def _summary_url_cell_to_html(raw) -> str:
    """Markdown or plain URLs → linked anchors (matches card URL field after fix_url)."""
    parts = _urls_from_summary_cell(raw)
    if not parts:
        return html.escape("NA")
    chunks: list[str] = []
    for u in parts:
        esc_href = html.escape(u.strip(), quote=True)
        display = u.strip()
        if len(display) > 56:
            display = display[:53] + "…"
        chunks.append(f'<a href="{esc_href}">{html.escape(display)}</a>')
    return " · ".join(chunks)


def _drop_all_empty_summary_columns(
    to_output: pd.DataFrame, df_sorted: pd.DataFrame
) -> pd.DataFrame:
    """
    Remove columns where every cell is empty/NA; optionally append URL when a column
    was removed and the source rows have at least one non-empty URL.
    """
    dropped_any = False
    keep: list[str] = []
    for c in to_output.columns:
        if c == "NAME":
            keep.append(c)
            continue
        if _summary_column_entirely_empty(to_output[c]):
            dropped_any = True
            continue
        keep.append(c)
    out = to_output.loc[:, keep].copy()
    if (
        "URL" not in out.columns
        and "URL" in df_sorted.columns
        and dropped_any
        and df_sorted["URL"].map(_summary_cell_str).str.len().gt(0).any()
    ):
        insert_at = 1
        if "CATEGORY" in out.columns:
            insert_at = out.columns.get_loc("CATEGORY") + 1
        url_cells = [
            _sanitize_summary_table_cell(u) for u in df_sorted["URL"].tolist()
        ]
        out.insert(insert_at, "URL", url_cells)
    return out


def _write_summary_table_html(
    file,
    df: pd.DataFrame,
    *,
    citation_tooltips: list[str] | None = None,
) -> None:
    """HTML summary table so “Main citation” can be visually clipped (see extra.css)."""
    cite_col = "Main citation"
    file.write("<table>\n<thead>\n<tr>\n")
    for col in df.columns:
        file.write(f"<th>{html.escape(str(col))}</th>\n")
    file.write("</tr>\n</thead>\n<tbody>\n")
    for i, (_, row) in enumerate(df.iterrows()):
        file.write("<tr>\n")
        for col in df.columns:
            raw = row[col]
            if pd.isna(raw):
                val = "NA"
            else:
                val = str(raw)
            if col == "NAME":
                inner = _summary_name_cell_to_html(raw)
                file.write(f"<td>{inner}</td>\n")
            elif col == cite_col:
                plain = _undo_markdown_pipe_escape(val)
                body = html.escape(plain)
                tip = (
                    citation_tooltips[i]
                    if citation_tooltips is not None and i < len(citation_tooltips)
                    else plain
                )
                title_attr = html.escape(tip, quote=True)
                file.write(
                    '<td class="catalog-summary-citation-cell">'
                    f'<div class="catalog-summary-citation-clip" title="{title_attr}">'
                    f"{body}</div></td>\n"
                )
            elif col == "URL":
                file.write(f"<td>{_summary_url_cell_to_html(raw)}</td>\n")
            else:
                inner = html.escape(_undo_markdown_pipe_escape(val))
                file.write(f"<td>{inner}</td>\n")
        file.write("</tr>\n")
    file.write("</tbody>\n</table>\n")


def configure_type(filename):
    type = "tools"
    if "Sumstats" in filename:
        type="sumstats"
    return type

def configure_table_columns(df_combined, filename):
    ## topic-specifc table
    sort_cols = ["NAME"]
    if "Sumstats." in filename:
        table_columns = ["NAME","MAIN_ANCESTRY"]
    elif "Proteomics" in filename:
        table_columns = ["NAME","PLATFORM","YEAR","TITLE"]
    elif "Biobanks_" in filename:
        table_columns = [
            "NAME",
            "MAIN_ANCESTRY",
            "PARTICIPANTS",
            "CONTINENT",
            "SAMPLE SIZE",
            "URL",
        ]
    elif "Projects_" in filename:
        table_columns = ["NAME", "STAGE_PERIOD", "URL"]
        if (
            "STAGE_ORDER" in df_combined.columns
            and df_combined["STAGE_ORDER"].notna().any()
        ):
            sort_cols = ["STAGE_ORDER", "NAME"]
    elif _is_journals_catalog_doc(filename):
        table_columns = ["NAME", "ENTRY_COUNT"]
    elif "AI_Coding" in filename or "AI_Major_model_series" in filename:
        table_columns = ["NAME", "COMPANY", "URL", "DESCRIPTION"]
    elif "Coding_" in filename:
        table_columns = ["NAME", "URL", "DESCRIPTION"]
    else:
        table_columns = ["NAME","CITATION","YEAR"]

    if "Projects_" not in filename and "CATEGORY" in df_combined.columns:
        if not df_combined["CATEGORY"].isna().all():
            table_columns.insert(1,"CATEGORY")
            sort_cols.insert(0,"CATEGORY")
            df_combined["CATEGORY"] = df_combined["CATEGORY"].fillna("MISC")
    
    return table_columns, sort_cols


def _collect_unique_page_tags(df: pd.DataFrame) -> list[str]:
    """Union of per-entry badges for MkDocs Material search tag filters (page-level tags)."""
    ordered: list[str] = []
    seen: set[str] = set()
    for _, row in df.iterrows():
        for b in _badges_for_row(row):
            if b not in seen:
                seen.add(b)
                ordered.append(b)
    return ordered


def _catalog_section_page_class(df: pd.DataFrame, filename: str) -> str | None:
    """MkDocs Material `class` meta → `article.catalog-section-<…>` for themed chrome."""
    if _is_journals_catalog_doc(filename):
        return "catalog-section-Journals"
    if df.empty:
        return None
    r0 = df.iloc[0]
    sec = str(r0.get("SECTION", "") or "").strip()
    topic = str(r0.get("TOPIC", "") or "").strip()
    if sec == "Tools" and topic == "Population_Genetics":
        return "catalog-section-Population_Genetics"
    if not sec:
        return None
    return f"catalog-section-{sec}"


def _write_page_front_matter(
    file,
    tags: list[str],
    *,
    hide_primary_nav: bool = False,
    section_class: str | None = None,
) -> None:
    if not tags and not hide_primary_nav and not section_class:
        return
    hide = ["tags"]
    if hide_primary_nav:
        hide.append("navigation")
    fm: dict = {"hide": hide}
    if tags:
        fm["tags"] = tags
    if section_class:
        fm["class"] = section_class
    file.write("---\n")
    file.write(
        yaml.safe_dump(
            fm,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )
    )
    file.write("---\n\n")


def _summary_table_wrapper_class(filename: str) -> str:
    return "catalog-summary-table"


def _humanize_nav_label(label: str) -> str:
    s = (label or "").strip().replace("_", " ")
    return s if s else "this category"


def _nav_section_display(section: str) -> str:
    s = (section or "").strip()
    return {
        "Tools": "GWAS Tools",
        "Sumstats": "Summary statistics",
        "Biobanks": "Biobanks",
        "References": "References",
        "Single_Cell": "Single cell",
        "Projects": "Projects",
        "AI": "AI",
        "Coding": "Coding",
    }.get(s, _humanize_nav_label(s))


def _catalog_listing_lead(df: pd.DataFrame) -> str:
    """Short intro for catalog topic pages (Markdown inside .catalog-nav-lead)."""
    if df.empty:
        return ""
    r = df.iloc[0]
    sec = str(r.get("SECTION", "") or "").strip()
    topic = str(r.get("TOPIC", "") or "").strip()
    sub = str(r.get("SUBTOPIC", "") or "").strip()
    sec_d = _nav_section_display(sec)
    topic_h = _humanize_nav_label(topic)
    sub_h = _humanize_nav_label(sub)
    if sub:
        inner = (
            f"Curation of **{sub_h}** within **{topic_h}** "
            f"— listings under the **{sec_d}** tab."
        )
    else:
        inner = f"Curation of **{topic_h}** — listings under the **{sec_d}** tab."
    return (
        '<div class="catalog-nav-lead" markdown="block">\n\n'
        + inner
        + "\n\n</div>\n\n"
    )


def overwrite_markdown(filename, df_combined, output_items):
    df_work = format_main(df_combined.copy(), configure_type(filename))
    table_columns, sort_cols = configure_table_columns(df_work, filename)
    page_tags = _collect_unique_page_tags(df_work)
    summary_wrap = _summary_table_wrapper_class(filename)
    is_journals = _is_journals_catalog_doc(filename)

    if is_journals and "ENTRY_COUNT" in df_work.columns:
        _ec = pd.to_numeric(df_work["ENTRY_COUNT"], errors="coerce")
        df_sorted = (
            df_work.assign(_entry_sort=_ec)
            .sort_values(
                by=["_entry_sort", "NAME"],
                ascending=[False, True],
                na_position="last",
            )
            .drop(columns=["_entry_sort"])
        )
    else:
        df_sorted = df_work.sort_values(by=sort_cols)

    section_class = _catalog_section_page_class(df_sorted, filename)
    with open(filename, "w") as file:
        _write_page_front_matter(
            file,
            page_tags,
            hide_primary_nav=is_journals,
            section_class=section_class,
        )
        if is_journals:
            file.write("# Journals\n\n")
            file.write(
                "Publication venues cited from catalog entries. "
                "The **Cited in CTGCatalog** column shows the total; the colored bar "
                "stacks counts by catalog section. Bar length scales to the largest "
                "total on this page (same idea as the count bars on "
                "[Catalog statistics](Catalog_statistics.md)).\n\n"
            )
            _write_journals_legend_html(file, df_sorted)
            file.write("## Summary Table\n\n")
            _write_journals_stats_table_html(file, df_sorted)
            file.write("\n")
        else:
            file.write(_catalog_listing_lead(df_sorted))
            file.write("## Summary Table\n\n")
            file.write(
                "*Click a column header to sort the table.*\n\n"
            )
            file.write(
                f'<div class="{summary_wrap}" markdown="block">\n\n'
            )

    if not is_journals:
        to_output = df_sorted.loc[:, table_columns].fillna("NA")
        if "Biobanks_" in filename or "Sumstats." in filename:
            to_output = to_output.rename(
                columns={"MAIN_ANCESTRY": "MAIN ANCESTRY"},
            )
        if "CITATION" in to_output.columns:
            to_output = to_output.rename(columns={"CITATION": "Main citation"})
        if "ENTRY_COUNT" in to_output.columns:
            to_output = to_output.rename(
                columns={"ENTRY_COUNT": "Cited in CTGCatalog"},
            )
        cite_tooltips: list[str] | None = None
        if "Main citation" in to_output.columns:
            cite_tooltips = [
                _full_citation_for_tooltip(df_sorted.iloc[j])
                for j in range(len(df_sorted))
            ]
            to_output = to_output.copy()
            to_output["Main citation"] = df_sorted.apply(
                _minimal_summary_citation, axis=1
            ).values
        to_output = _sanitize_summary_dataframe(to_output)
        to_output = _apply_summary_truncation(to_output)
        to_output = _drop_all_empty_summary_columns(to_output, df_sorted)
        if "Main citation" not in to_output.columns:
            cite_tooltips = None
        with open(filename, "a") as file:
            file.write("\n")
            _write_summary_table_html(
                file, to_output, citation_tooltips=cite_tooltips
            )
            file.write("\n\n</div>\n\n")

    df_cards = df_sorted.drop(columns=["NAME"], errors="ignore").rename(
        columns={"_NAME": "NAME"}
    )
    write_markdown(filename, df_cards, output_items)


###########################################################################################################################################################################################################################

def write_md(pop_pmid):
    pop_pmid = add_path(pop_pmid)

    for path in pop_pmid["PATH"].unique():
        df_combined = pop_pmid.loc[pop_pmid["PATH"] == path, :]
        overwrite_markdown(
            path, df_combined, _card_output_items_for_path(path)
        )


def format_path_full(series):
    path_list=[]
    for i in series:
        if i!="":
            path_list.append(i)
    if path_list and path_list[0] == "Journals":
        return "../docs/Journals.md"
    return "../docs/"+"_".join(path_list)+".md"

def add_path(df_combined):
    folder_cols =["SECTION","TOPIC","SUBTOPIC"]
    
    if "TOPIC" not in df_combined.columns:
        df_combined["TOPIC"]=""
    if "SUBTOPIC" not in df_combined.columns:
        df_combined["SUBTOPIC"]=""   
    
    # create a path 
    # SECTION [_TOPIC] [_SUBTOPIC]
    df_combined["PATH"] = df_combined[folder_cols].fillna("").apply(lambda x: format_path_full(x), axis=1)
    
    return df_combined