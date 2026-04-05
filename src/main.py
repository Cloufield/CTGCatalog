import subprocess
import sys
import os
import shutil
import pandas as pd
from pathlib import Path
import print_level
from load_data import load_table_and_ref
from process_md import write_md
from process_homepage import write_homepage
from process_mkdocs import write_mkdcos
from tag_pages import prepare_tag_index
from validate_catalog import validate_catalog
from check_docs_links import run_link_check


def _emit_trending_pages() -> None:
    """Write Trending hub + nested PubMed GWAS page so URLs match docs/Trending/...."""
    root = Path(__file__).resolve().parents[1]
    script = root / "scripts" / "render_trending_pubmed_gwas.py"
    primary = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(root),
        capture_output=True,
        text=True,
    )
    if primary.returncode == 0:
        return
    stub = subprocess.run(
        [sys.executable, str(script), "--stub"],
        cwd=str(root),
        capture_output=True,
        text=True,
    )
    if stub.returncode != 0:
        print(stub.stderr or stub.stdout or primary.stderr, file=sys.stderr)
        sys.exit(1)


if validate_catalog() != 0:
    sys.exit(1)

# Load Data and Ref
table_and_ref = load_table_and_ref()

_tag_buckets, _tag_slug_map, _tag_card_rows = prepare_tag_index(table_and_ref)
print_level.TAG_SLUG_MAP = _tag_slug_map
write_md(table_and_ref)
print_level.TAG_SLUG_MAP = None

write_homepage(table_and_ref)

write_mkdcos(
    tag_buckets=_tag_buckets,
    tag_slug_map=_tag_slug_map,
    tag_card_rows=_tag_card_rows,
)

_emit_trending_pages()

if run_link_check() != 0:
    sys.exit(1)