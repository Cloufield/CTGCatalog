"""Per-tag pages under docs/tags/ and shared bucket/slug data for badge links."""

from __future__ import annotations

from io import StringIO
from pathlib import Path

import pandas as pd
import yaml

from catalog_sources import assign_tag_slugs
from format_table import format_main
from print_level import _badges_for_row, _heading_id_attr, _write_entry_card
from process_md import (
    add_path,
    configure_type,
    _card_output_items_for_path,
    _nav_section_display,
)


def collect_tag_page_data(
    catalog: pd.DataFrame,
) -> tuple[
    dict[str, dict[tuple[str, str], tuple[str, str, str]]],
    dict[str, dict[tuple[str, str], tuple[pd.Series, str]]],
]:
    """
    Buckets: tag -> (stem, anchor_id) -> (link_label, section_sort, name_sort).
    Card_rows: tag -> (stem, anchor_id) -> (formatted row Series, PATH str for card fields).
    stem is docs/*.md basename without .md (MkDocs page stem).
    """
    df = add_path(catalog.copy())
    buckets: dict[str, dict[tuple[str, str], tuple[str, str, str]]] = {}
    card_rows: dict[str, dict[tuple[str, str], tuple[pd.Series, str]]] = {}
    if df.empty or "PATH" not in df.columns:
        return buckets, card_rows

    for path_str, group in df.groupby("PATH", sort=False):
        if not isinstance(path_str, str) or not path_str.endswith(".md"):
            continue
        stem = Path(path_str).stem
        if stem == "tags":
            continue
        try:
            df_g = format_main(group.copy(), configure_type(path_str))
        except Exception:
            continue
        for _, row in df_g.iterrows():
            name = str(row.get("_NAME", "") or row.get("NAME", "") or "").strip()
            if not name or name.upper() == "NA":
                continue
            sec = str(row.get("SECTION", "") or "").strip()
            section_label = _nav_section_display(sec)
            anchor = _heading_id_attr(row)
            aid = str(anchor).strip() if anchor is not None else ""
            key = (stem, aid)
            label = _safe_md_link_label(name, section_label)
            sort_key = (section_label.casefold(), name.casefold())
            row_copy = row.copy()
            for tag in _badges_for_row(row):
                if not tag:
                    continue
                t = str(tag)
                bucket = buckets.setdefault(t, {})
                if key not in bucket:
                    bucket[key] = (label, sort_key[0], sort_key[1])
                card_rows.setdefault(t, {})[key] = (row_copy, path_str)
    return buckets, card_rows


def collect_tag_buckets(
    catalog: pd.DataFrame,
) -> dict[str, dict[tuple[str, str], tuple[str, str, str]]]:
    """Backward-compatible wrapper; prefer collect_tag_page_data for card rendering."""
    buckets, _ = collect_tag_page_data(catalog)
    return buckets


def _row_for_entry_card(row: pd.Series) -> pd.Series:
    """Match process_md card prep: plain display NAME from _NAME, not markdown TABLE_NAME."""
    r = row.copy()
    if "_NAME" in r.index and "NAME" in r.index:
        r = r.drop(labels=["NAME"])
        r = r.rename({"_NAME": "NAME"})
    return r


def _safe_md_link_label(name: str, section_label: str) -> str:
    n = str(name).replace("\n", " ").strip()
    n = n.replace("[", "(").replace("]", ")")
    return f"{n} — {section_label}"


def write_tag_pages(
    buckets: dict[str, dict[tuple[str, str], tuple[str, str, str]]],
    slug_map: dict[str, str],
    card_rows: dict[str, dict[tuple[str, str], tuple[pd.Series, str]]] | None = None,
) -> None:
    """Hub at docs/tags/index.md; one page per tag at docs/tags/<slug>.md."""
    docs_root = Path(__file__).resolve().parent.parent / "docs"
    tags_dir = docs_root / "tags"

    legacy = docs_root / "tags.md"
    if legacy.is_file():
        legacy.unlink()

    if tags_dir.is_dir():
        for p in tags_dir.glob("*.md"):
            p.unlink()
    else:
        tags_dir.mkdir(parents=True)

    tag_list = sorted(buckets.keys(), key=lambda s: s.lower())

    hub_fm = {
        "hide": ["navigation", "toc", "tags"],
        "tags": ["Catalog"],
        "title": "Browse by tag",
        "class": "catalog-tags-hub",
    }
    hub_lines = [
        "---",
        yaml.safe_dump(
            hub_fm, default_flow_style=False, allow_unicode=True, sort_keys=False
        ).rstrip(),
        "---",
        "",
        "Open a **tag** to see every catalog entry that uses it (all sections). "
        "From a listing page, click a tag on a card to jump here.",
        "",
    ]
    for tag in tag_list:
        slug = slug_map[tag]
        hub_lines.append(f"- [{tag}]({slug}/)")
    hub_lines.append("")
    (tags_dir / "index.md").write_text("\n".join(hub_lines), encoding="utf-8")

    for tag in tag_list:
        slug = slug_map[tag]
        bucket = buckets[tag]
        sorted_items = sorted(
            bucket.items(),
            key=lambda kv: (kv[1][1], kv[1][2], kv[0][0], kv[0][1]),
        )
        page_fm = {
            "hide": ["navigation", "tags"],
            "tags": ["Catalog"],
            "title": f"Tag: {tag}",
            "class": "catalog-tag-page",
        }
        body: list[str] = [
            "---",
            yaml.safe_dump(
                page_fm, default_flow_style=False, allow_unicode=True, sort_keys=False
            ).rstrip(),
            "---",
            "",
            f"# {tag}",
            "",
            "Catalog entries using this tag (links open the entry card on its page):",
            "",
        ]
        for (stem, aid), (label, _, _) in sorted_items:
            frag = f"#{aid}" if aid else ""
            href = f"../../{stem}/{frag}"
            body.append(f"- [{label}]({href})")
        body.append("")
        body.append("## Entries")
        body.append("")
        cards_for_tag = (card_rows or {}).get(tag, {})
        card_chunks: list[str] = []
        for idx, ((stem, aid), _) in enumerate(sorted_items):
            packed = cards_for_tag.get((stem, aid))
            if not packed:
                continue
            row, path_str = packed
            row_card = _row_for_entry_card(row)
            frag = f"#{aid}" if aid else ""
            canonical = f"../../{stem}/{frag}"
            out = StringIO()
            cols = row_card.index
            items = _card_output_items_for_path(path_str)
            _write_entry_card(
                out,
                row_card,
                cols,
                items,
                "h2",
                idx + 1,
                tag_slug_map=slug_map,
                badge_listing_links=False,
                canonical_href=canonical,
            )
            card_chunks.append(out.getvalue().rstrip())
        if card_chunks:
            body.append("\n".join(card_chunks))
            body.append("")
        (tags_dir / f"{slug}.md").write_text("\n".join(body), encoding="utf-8")


def prepare_tag_index(catalog: pd.DataFrame) -> tuple[
    dict[str, dict[tuple[str, str], tuple[str, str, str]]],
    dict[str, str],
    dict[str, dict[tuple[str, str], tuple[pd.Series, str]]],
]:
    """Single pass over the catalog; reuse for slug map, badge hrefs, and tag pages."""
    buckets, tag_card_rows = collect_tag_page_data(catalog)
    slug_map = assign_tag_slugs(buckets.keys())
    return buckets, slug_map, tag_card_rows
