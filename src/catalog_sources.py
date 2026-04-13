"""Catalog paths, slug helpers, and homepage statistics filters."""

import re
from pathlib import Path

# Values of FIELD (from JSON `_meta.source_sheet`) included in the Sumstats block on
# Catalog_statistics.md.
HOMEPAGE_SUMSTATS_SHEETS = [
    "Sumstats",
    "Proteomics",
    "Transcriptomics",
    "Epigenetics",
    "SV",
    "Imaging",
    "Gut_microbiome",
    "Behaviour",
    "GxE",
]


def repo_json_dir() -> Path:
    """json/ at repository root (parent of src/)."""
    return Path(__file__).resolve().parent.parent / "json"


# Top-level directories under json/ whose *.json files are registries, not catalog rows.
_JSON_NON_CATALOG_TOP_DIRS = frozenset({"tags", "databases"})


def is_catalog_json_file(json_dir: Path, path: Path) -> bool:
    """True if ``path`` is a UTF-8 catalog entry under ``json_dir`` (excludes e.g. ``json/tags/``)."""
    if path.name.startswith("."):
        return False
    try:
        rel = path.relative_to(json_dir)
    except ValueError:
        return False
    return not (rel.parts and rel.parts[0] in _JSON_NON_CATALOG_TOP_DIRS)


def repo_journals_dir() -> Path:
    """json/journals/ — one JSON file per publication venue (see sync_journals_from_catalog)."""
    return repo_json_dir() / "journals"


def repo_projects_dir() -> Path:
    """json/projects/ — umbrella entries for multi-phase programs (1KG, UKB, GTEx, …)."""
    return repo_json_dir() / "projects"


def repo_databases_dir() -> Path:
    """json/databases/<country>/ — one JSON file per major database (see process_major_databases)."""
    return repo_json_dir() / "databases"


def slugify_catalog_tag(tag: str) -> str:
    """URL/filename slug for a tag label (tag listing pages under docs/tags/)."""
    t = str(tag).strip().lower().replace("/", "-")
    t = re.sub(r"\s+", "-", t)
    t = re.sub(r"[^a-z0-9_-]+", "-", t)
    t = re.sub(r"-+", "-", t).strip("-")
    return t or "tag"


def assign_tag_slugs(tags) -> dict[str, str]:
    """Stable unique slug per tag string (collision suffix -2, -3, …)."""
    tag_list = sorted(set(tags), key=lambda s: str(s).lower())
    used: set[str] = set()
    out: dict[str, str] = {}
    for tag in tag_list:
        base = slugify_catalog_tag(tag)
        if base == "index":
            base = "index-tag"
        s = base
        n = 2
        while s in used:
            s = f"{base}-{n}"
            n += 1
        used.add(s)
        out[str(tag)] = s
    return out


def slugify_segment(value, default="misc") -> str:
    """Filesystem-safe segment from SECTION/TOPIC/SUBTOPIC/NAME."""
    if value is None:
        return default
    try:
        if value != value:  # NaN
            return default
    except (TypeError, ValueError):
        pass
    t = str(value).strip().lower()
    t = re.sub(r"\s+", "-", t)
    t = re.sub(r"[^a-z0-9_-]+", "", t)
    t = re.sub(r"-+", "-", t).strip("-")
    return t or default


def normalize_folder_field(series):
    """Match load_data: spaces -> underscore, hyphen -> underscore."""
    return (
        series.fillna("")
        .astype(str)
        .str.replace(r"\s+", "_", regex=True)
        .str.replace("-", "_", regex=True)
    )
